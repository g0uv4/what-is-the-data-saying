import { createStore, GUEST_UPLOADS_LIMIT } from './store.mjs';
import { applyCors, HttpError, readJsonBody, sendError, sendJson } from './http.mjs';
import { formatTaipei, nextTaipeiMidnight, secondsUntil } from './time.mjs';

const RAW_CSV_KEYS = ['csv', 'raw_csv', 'rawCsv', 'csv_text', 'raw', 'file', 'content'];
const HISTORY_FIELDS = ['pattern_id', 'source_name', 'row_count'];

export function createRequestListener(options = {}) {
  const store = createStore(options);
  const corsOrigin = options.corsOrigin ?? process.env.CORS_ORIGIN ?? '*';
  const frontendOrigin = resolveFrontendOrigin(options.frontendOrigin ?? process.env.FRONTEND_ORIGIN, corsOrigin);
  const publicBase = options.publicBase ?? process.env.PUBLIC_BASE_URL ?? null;

  return async function listener(req, res) {
    applyCors(req, res, corsOrigin);
    if (req.method === 'OPTIONS') {
      res.writeHead(204);
      res.end();
      return;
    }

    try {
      const url = new URL(req.url || '/', `http://${req.headers.host || '127.0.0.1'}`);
      const path = normalizePath(url.pathname);
      await dispatch(req, res, url, path, {
        store,
        corsOrigin,
        frontendOrigin,
        publicBase,
      });
    } catch (err) {
      sendError(res, err);
    }
  };
}

function resolveFrontendOrigin(explicit, corsOrigin) {
  if (explicit) return explicit.replace(/\/$/, '');
  if (corsOrigin && corsOrigin !== '*') return corsOrigin.replace(/\/$/, '');
  return 'http://127.0.0.1:4173';
}

function normalizePath(pathname) {
  if (pathname.length > 1 && pathname.endsWith('/')) return pathname.slice(0, -1);
  return pathname;
}

function requestBase(req, publicBase) {
  if (publicBase) return publicBase.replace(/\/$/, '');
  const host = req.headers.host || '127.0.0.1:8787';
  return `http://${host}`;
}

function guestIdOf(req) {
  const header = req.headers['x-guest-id'];
  if (typeof header === 'string' && header.trim()) return header.trim();
  return req.socket?.remoteAddress || 'anonymous';
}

function optionalUser(req, store) {
  const header = req.headers.authorization;
  if (!header) return null;
  const match = String(header).match(/^Bearer\s+(\S+)/i);
  if (!match) {
    throw new HttpError(401, 'unauthorized', 'invalid Authorization header');
  }
  const user = store.userFromToken(match[1]);
  if (!user) {
    throw new HttpError(401, 'unauthorized', 'token is invalid');
  }
  return user;
}

function requireUser(req, store) {
  const user = optionalUser(req, store);
  if (!user) {
    throw new HttpError(401, 'unauthorized', 'sign in required');
  }
  return user;
}

function wantsJson(req, url) {
  if (url.searchParams.get('format') === 'json') return true;
  const accept = String(req.headers.accept || '');
  return accept.includes('application/json');
}

function quotaExceeded(store, message, extraQuota = {}) {
  const resetAtDate = nextTaipeiMidnight(store.now());
  return new HttpError(429, 'quota_exceeded', message, {
    retryAfter: secondsUntil(resetAtDate, store.now()),
    quota: {
      reset_at: formatTaipei(resetAtDate),
      ...extraQuota,
    },
  });
}

async function dispatch(req, res, url, path, ctx) {
  switch (path) {
    case '/v1/health':
      assertMethod(req, ['GET']);
      sendJson(res, 200, { ok: true, mock: true });
      return;
    case '/v1/me':
      assertMethod(req, ['GET']);
      handleMe(req, res, ctx);
      return;
    case '/v1/entitlement':
      assertMethod(req, ['GET']);
      handleEntitlement(req, res, ctx);
      return;
    case '/v1/auth/github':
      assertMethod(req, ['GET']);
      handleGithubAuth(req, res, url, ctx);
      return;
    case '/v1/auth/github/callback':
      assertMethod(req, ['GET']);
      handleGithubCallback(req, res, url, ctx);
      return;
    case '/v1/auth/exchange':
      assertMethod(req, ['POST']);
      await handleAuthExchange(req, res, ctx);
      return;
    case '/v1/checkout/session':
      assertMethod(req, ['POST']);
      await handleCheckoutSession(req, res, ctx);
      return;
    case '/v1/checkout/mock-complete':
      assertMethod(req, ['POST']);
      await handleMockComplete(req, res, ctx);
      return;
    case '/v1/checkout/mock-cancel':
      assertMethod(req, ['POST']);
      await handleMockCancel(req, res, ctx);
      return;
    case '/v1/history':
      if (req.method === 'GET') {
        handleHistoryGet(req, res, ctx);
        return;
      }
      if (req.method === 'POST') {
        await handleHistoryPost(req, res, ctx);
        return;
      }
      throw new HttpError(405, 'method_not_allowed', 'use GET or POST');
    case '/v1/guest/consume-upload':
      assertMethod(req, ['POST']);
      await handleGuestConsume(req, res, ctx);
      return;
    default:
      throw new HttpError(404, 'not_found', 'unknown path');
  }
}

function assertMethod(req, allowed) {
  if (!allowed.includes(req.method)) {
    throw new HttpError(405, 'method_not_allowed', `use ${allowed.join(' or ')}`);
  }
}

function handleMe(req, res, ctx) {
  const user = optionalUser(req, ctx.store);
  const guestId = guestIdOf(req);
  sendJson(res, 200, {
    user: user ? ctx.store.publicUser(user) : null,
    entitlement: ctx.store.entitlementOf(user, guestId),
  });
}

function handleEntitlement(req, res, ctx) {
  const user = optionalUser(req, ctx.store);
  sendJson(res, 200, {
    entitlement: ctx.store.entitlementOf(user, guestIdOf(req)),
  });
}

function handleGithubAuth(req, res, url, ctx) {
  const authorizeUrl = `${requestBase(req, ctx.publicBase)}/v1/auth/github/callback?code=mock`;
  if (url.searchParams.get('redirect') === '1') {
    res.writeHead(302, { location: authorizeUrl });
    res.end();
    return;
  }
  sendJson(res, 200, { authorize_url: authorizeUrl });
}

function handleGithubCallback(req, res, url, ctx) {
  const githubCode = url.searchParams.get('code');
  if (!githubCode) {
    throw new HttpError(400, 'missing_code', 'code is required');
  }
  const { user } = ctx.store.loginMockUser();
  const issued = ctx.store.issueAuthCode(user);
  const body = {
    code: issued.code,
    expires_in: issued.expires_in,
  };
  if (wantsJson(req, url) || url.searchParams.get('redirect') === '0') {
    sendJson(res, 200, body);
    return;
  }
  const redirectTo = new URL(`${ctx.frontendOrigin}/`);
  redirectTo.searchParams.set('code', issued.code);
  res.writeHead(302, { location: redirectTo.toString() });
  res.end();
}

async function handleAuthExchange(req, res, ctx) {
  const body = await readJsonBody(req);
  const result = ctx.store.consumeAuthCode(body.code);
  if (!result.ok) {
    throw new HttpError(400, 'invalid_grant', grantMessage(result.reason));
  }
  sendJson(res, 200, {
    access_token: result.token,
    token_type: 'Bearer',
    user: ctx.store.publicUser(result.user),
    entitlement: ctx.store.entitlementOf(result.user, guestIdOf(req)),
  });
}

function grantMessage(reason) {
  if (reason === 'missing') return 'code is required';
  if (reason === 'expired') return 'authorization code has expired';
  return 'authorization code is invalid or already used';
}

async function handleCheckoutSession(req, res, ctx) {
  const user = requireUser(req, ctx.store);
  const live = ctx.store.entitlementOf(user, guestIdOf(req));
  if (live.plan === 'pro' && live.status === 'active') {
    throw new HttpError(403, 'already_active', 'pro is already active');
  }
  const body = await readJsonBody(req);
  if (body.provider && body.provider !== 'mock') {
    throw new HttpError(501, 'not_implemented', 'real checkout is not wired');
  }
  if (body.plan !== 'pro' || body.interval !== 'month') {
    throw new HttpError(400, 'invalid_checkout', 'body must be { "plan": "pro", "interval": "month" }');
  }
  const session = ctx.store.createCheckout(user, body.plan, body.interval);
  sendJson(res, 200, {
    session_id: session.session_id,
    checkout_url: `${requestBase(req, ctx.publicBase)}/mock/checkout?session_id=${encodeURIComponent(session.session_id)}`,
    mock: true,
  });
}

async function handleMockComplete(req, res, ctx) {
  const body = await readJsonBody(req);
  if (!body.session_id || typeof body.session_id !== 'string') {
    throw new HttpError(400, 'invalid_body', 'session_id is required');
  }
  const completed = ctx.store.completeCheckout(body.session_id);
  if (!completed) {
    throw new HttpError(404, 'unknown_session', 'checkout session not found');
  }
  sendJson(res, 200, {
    ok: true,
    session_id: completed.session.session_id,
    entitlement: ctx.store.entitlementOf(completed.user, guestIdOf(req)),
  });
}

async function handleMockCancel(req, res, ctx) {
  const body = await readJsonBody(req);
  if (!body.session_id || typeof body.session_id !== 'string') {
    throw new HttpError(400, 'invalid_body', 'session_id is required');
  }
  const session = ctx.store.cancelCheckout(body.session_id);
  if (!session) {
    throw new HttpError(404, 'unknown_session', 'checkout session not found');
  }
  sendJson(res, 200, { ok: true });
}

function requireHistoryFeature(req, ctx) {
  const user = requireUser(req, ctx.store);
  const entitlement = ctx.store.entitlementOf(user, guestIdOf(req));
  if (!entitlement.features.includes('save_history')) {
    throw new HttpError(403, 'missing_feature', 'save_history is required');
  }
  return { user, entitlement };
}

function handleHistoryGet(req, res, ctx) {
  const { user } = requireHistoryFeature(req, ctx);
  sendJson(res, 200, { items: ctx.store.listHistory(user) });
}

async function handleHistoryPost(req, res, ctx) {
  const { user, entitlement } = requireHistoryFeature(req, ctx);
  if (entitlement.quota.hosted_runs_remaining === 0) {
    throw quotaExceeded(ctx.store, 'hosted quota exhausted', {
      hosted_runs_remaining: 0,
    });
  }
  const body = await readJsonBody(req);
  for (const key of RAW_CSV_KEYS) {
    if (Object.prototype.hasOwnProperty.call(body, key)) {
      throw new HttpError(400, 'raw_csv_rejected', 'history stores summary only; never send raw CSV');
    }
  }
  const extra = Object.keys(body).filter((key) => !HISTORY_FIELDS.includes(key));
  if (extra.length) {
    throw new HttpError(400, 'unknown_field', 'history only accepts pattern_id, source_name, row_count');
  }
  if (typeof body.pattern_id !== 'string' || !body.pattern_id.trim()) {
    throw new HttpError(400, 'invalid_body', 'pattern_id is required');
  }
  if (typeof body.source_name !== 'string' || !body.source_name.trim()) {
    throw new HttpError(400, 'invalid_body', 'source_name is required');
  }
  if (typeof body.row_count !== 'number' || !Number.isFinite(body.row_count) || body.row_count < 0) {
    throw new HttpError(400, 'invalid_body', 'row_count must be a non-negative number');
  }
  const record = ctx.store.addHistory(user, {
    pattern_id: body.pattern_id.trim(),
    source_name: body.source_name.trim(),
    row_count: body.row_count,
  });
  sendJson(res, 201, { id: record.id, created_at: record.created_at });
}

async function handleGuestConsume(req, res, ctx) {
  const body = await readJsonBody(req);
  const kind = body.kind === 'demo' || body.source === 'demo' ? 'demo' : 'upload';
  const guestId = guestIdOf(req);
  const result = ctx.store.consumeGuestUpload(guestId, kind);
  if (result.exceeded) {
    throw quotaExceeded(ctx.store, 'guest daily upload limit reached', {
      guest_uploads_remaining_today: 0,
      guest_uploads_limit_per_day: GUEST_UPLOADS_LIMIT,
    });
  }
  sendJson(res, 200, {
    ok: true,
    counted: result.counted,
    remaining: result.remaining,
    limit: GUEST_UPLOADS_LIMIT,
    kind,
  });
}

export { GUEST_UPLOADS_LIMIT };
