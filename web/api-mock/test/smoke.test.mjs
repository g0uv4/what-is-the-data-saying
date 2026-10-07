import assert from 'node:assert/strict';
import http from 'node:http';
import { after, test } from 'node:test';
import { createRequestListener } from '../lib/app.mjs';

const servers = [];

function listen(options = {}) {
  return new Promise((resolve) => {
    const server = http.createServer(createRequestListener(options));
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      const handle = { server, base: `http://127.0.0.1:${port}` };
      servers.push(handle);
      resolve(handle);
    });
  });
}

after(async () => {
  await Promise.all(servers.map(({ server }) => new Promise((resolve) => server.close(resolve))));
});

async function call(base, path, options = {}) {
  const headers = { ...(options.headers || {}) };
  let body = options.body;
  if (body && typeof body !== 'string' && !Buffer.isBuffer(body)) {
    headers['content-type'] = headers['content-type'] || 'application/json';
    body = JSON.stringify(body);
  }
  const res = await fetch(`${base}${path}`, {
    method: options.method || 'GET',
    headers,
    body,
    redirect: 'manual',
  });
  const text = await res.text();
  let json = null;
  if (text) {
    try {
      json = JSON.parse(text);
    } catch {
      json = null;
    }
  }
  return { res, json, text };
}

async function login(base, extra = {}) {
  const callback = await call(base, '/v1/auth/github/callback?code=mock&format=json');
  assert.equal(callback.res.status, 200);
  assert.equal(typeof callback.json.code, 'string');
  const { res, json } = await call(base, '/v1/auth/exchange', {
    method: 'POST',
    body: { code: callback.json.code },
  });
  assert.equal(res.status, 200);
  return { token: json.access_token, me: json, ...extra };
}

function auth(token) {
  return { authorization: `Bearer ${token}` };
}

test('GET /v1/health', async () => {
  const { base } = await listen();
  const { res, json } = await call(base, '/v1/health');
  assert.equal(res.status, 200);
  assert.deepEqual(json, { ok: true, mock: true });
});

test('GET /v1/me and /v1/entitlement as guest', async () => {
  const { base } = await listen();
  const me = await call(base, '/v1/me');
  assert.equal(me.res.status, 200);
  assert.equal(me.json.user, null);
  assert.equal(me.json.entitlement.plan, 'free');
  assert.equal(me.json.entitlement.status, 'none');
  assert.deepEqual(me.json.entitlement.features, []);
  assert.equal(me.json.entitlement.quota.guest_uploads_limit_per_day, 3);
  assert.equal(me.json.entitlement.quota.guest_uploads_remaining_today, 3);
  assert.equal(me.json.entitlement.quota.seats, 1);
  assert.equal(me.json.entitlement.source, 'anonymous');

  const ent = await call(base, '/v1/entitlement');
  assert.equal(ent.res.status, 200);
  assert.deepEqual(ent.json.entitlement, me.json.entitlement);
});

test('GitHub mock authorize + first login grants 7-day trial', async () => {
  const { base } = await listen();
  const authz = await call(base, '/v1/auth/github');
  assert.equal(authz.res.status, 200);
  assert.match(authz.json.authorize_url, /\/v1\/auth\/github\/callback\?code=mock$/);

  const missing = await call(base, '/v1/auth/github/callback');
  assert.equal(missing.res.status, 400);

  const callback = await call(base, '/v1/auth/github/callback?code=mock&format=json');
  assert.equal(callback.res.status, 200);
  assert.equal(typeof callback.json.code, 'string');
  assert.ok(callback.json.code.length > 16);
  assert.equal(callback.json.expires_in, 60);
  assert.equal(callback.json.access_token, undefined);

  const { res, json } = await call(base, '/v1/auth/exchange', {
    method: 'POST',
    body: { code: callback.json.code },
  });
  assert.equal(res.status, 200);
  assert.equal(typeof json.access_token, 'string');
  assert.ok(json.access_token.length > 16);
  assert.ok(!json.access_token.includes('.'), 'token must be opaque, not JWT');
  assert.equal(json.token_type, 'Bearer');
  assert.equal(json.user.login, 'wids-mock');
  assert.equal(json.entitlement.plan, 'trial');
  assert.equal(json.entitlement.status, 'trialing');
  assert.deepEqual(json.entitlement.features, ['save_history', 'hosted_quota', 'faster_ui']);
  assert.ok(json.entitlement.trial_ends_at.includes('+08:00'));

  const me = await call(base, '/v1/me', { headers: auth(json.access_token) });
  assert.equal(me.json.user.id, '1');
  assert.equal(me.json.entitlement.plan, 'trial');
});

test('history requires save_history; POST returns 201; raw CSV rejected', async () => {
  const { base } = await listen();
  const denied = await call(base, '/v1/history', {
    method: 'POST',
    body: { pattern_id: 'lollipop-rank', source_name: 'a.csv', row_count: 3 },
  });
  assert.equal(denied.res.status, 401);

  const { token } = await login(base);
  const raw = await call(base, '/v1/history', {
    method: 'POST',
    headers: auth(token),
    body: { pattern_id: 'lollipop-rank', source_name: 'a.csv', row_count: 3, csv: 'a,b\n1,2' },
  });
  assert.equal(raw.res.status, 400);

  const created = await call(base, '/v1/history', {
    method: 'POST',
    headers: auth(token),
    body: { pattern_id: 'lollipop-rank', source_name: 'demo.csv', row_count: 12 },
  });
  assert.equal(created.res.status, 201);
  assert.equal(typeof created.json.id, 'string');
  assert.equal(typeof created.json.created_at, 'string');
  assert.equal(Object.keys(created.json).sort().join(','), 'created_at,id');

  const list = await call(base, '/v1/history', { headers: auth(token) });
  assert.equal(list.res.status, 200);
  assert.equal(list.json.items.length, 1);
  assert.equal(list.json.items[0].pattern_id, 'lollipop-rank');
  assert.equal(list.json.items[0].source_name, 'demo.csv');
  assert.equal(list.json.items[0].row_count, 12);
  assert.ok(!Object.hasOwn(list.json.items[0], 'note'));
});

test('login redirect carries a one-time code and never an access token', async () => {
  const { base } = await listen({ frontendOrigin: 'http://127.0.0.1:4173' });
  const { res } = await call(base, '/v1/auth/github/callback?code=mock');
  assert.equal(res.status, 302);
  const location = res.headers.get('location');
  assert.ok(location);
  assert.doesNotMatch(location, /access_token/);
  const redirectTo = new URL(location);
  const code = redirectTo.searchParams.get('code');
  assert.equal(typeof code, 'string');
  assert.ok(code.length > 16);
  assert.equal(redirectTo.searchParams.get('access_token'), null);

  const first = await call(base, '/v1/auth/exchange', { method: 'POST', body: { code } });
  assert.equal(first.res.status, 200);
  assert.ok(!location.includes(first.json.access_token));
});

test('authorization code can be exchanged only once; expired and missing codes fail', async () => {
  let nowMs = Date.parse('2026-10-07T12:00:00+08:00');
  const { base } = await listen({
    now: () => new Date(nowMs),
    authCodeTtlMs: 60_000,
  });
  const callback = await call(base, '/v1/auth/github/callback?code=mock&format=json');
  assert.equal(callback.res.status, 200);
  const code = callback.json.code;

  const first = await call(base, '/v1/auth/exchange', { method: 'POST', body: { code } });
  assert.equal(first.res.status, 200);
  assert.equal(typeof first.json.access_token, 'string');

  const reuse = await call(base, '/v1/auth/exchange', { method: 'POST', body: { code } });
  assert.equal(reuse.res.status, 400);
  assert.equal(reuse.json.error.code, 'invalid_grant');

  const missing = await call(base, '/v1/auth/exchange', { method: 'POST', body: {} });
  assert.equal(missing.res.status, 400);
  assert.equal(missing.json.error.code, 'invalid_grant');

  const unknown = await call(base, '/v1/auth/exchange', { method: 'POST', body: { code: 'no-such-code' } });
  assert.equal(unknown.res.status, 400);
  assert.equal(unknown.json.error.code, 'invalid_grant');

  const later = await call(base, '/v1/auth/github/callback?code=mock&format=json');
  nowMs += 61_000;
  const expired = await call(base, '/v1/auth/exchange', {
    method: 'POST',
    body: { code: later.json.code },
  });
  assert.equal(expired.res.status, 400);
  assert.equal(expired.json.error.code, 'invalid_grant');
});

test('POST /v1/history rejects note and any unknown field', async () => {
  const { base } = await listen();
  const { token } = await login(base);

  const withNote = await call(base, '/v1/history', {
    method: 'POST',
    headers: auth(token),
    body: { pattern_id: 'lollipop-rank', source_name: 'demo.csv', row_count: 12, note: '摘要' },
  });
  assert.equal(withNote.res.status, 400);
  assert.equal(withNote.json.error.code, 'unknown_field');

  const unknown = await call(base, '/v1/history', {
    method: 'POST',
    headers: auth(token),
    body: { pattern_id: 'lollipop-rank', source_name: 'demo.csv', row_count: 12, extra: 'nope' },
  });
  assert.equal(unknown.res.status, 400);
  assert.equal(unknown.json.error.code, 'unknown_field');
});

test('checkout mock complete upgrades to pro active; already-active is 403', async () => {
  const { base } = await listen();
  const unauth = await call(base, '/v1/checkout/session', {
    method: 'POST',
    body: { plan: 'pro', interval: 'month' },
  });
  assert.equal(unauth.res.status, 401);

  const { token } = await login(base);
  const bad = await call(base, '/v1/checkout/session', {
    method: 'POST',
    headers: auth(token),
    body: { plan: 'pro', interval: 'year' },
  });
  assert.equal(bad.res.status, 400);

  const stripe = await call(base, '/v1/checkout/session', {
    method: 'POST',
    headers: auth(token),
    body: { plan: 'pro', interval: 'month', provider: 'stripe' },
  });
  assert.equal(stripe.res.status, 501);

  const session = await call(base, '/v1/checkout/session', {
    method: 'POST',
    headers: auth(token),
    body: { plan: 'pro', interval: 'month' },
  });
  assert.equal(session.res.status, 200);
  assert.equal(session.json.mock, true);
  assert.ok(session.json.session_id);
  assert.ok(session.json.checkout_url.includes(session.json.session_id));

  const unknown = await call(base, '/v1/checkout/mock-complete', {
    method: 'POST',
    body: { session_id: 'cs_mock_nope' },
  });
  assert.equal(unknown.res.status, 404);

  const cancelSession = await call(base, '/v1/checkout/session', {
    method: 'POST',
    headers: auth(token),
    body: { plan: 'pro', interval: 'month' },
  });
  const canceled = await call(base, '/v1/checkout/mock-cancel', {
    method: 'POST',
    body: { session_id: cancelSession.json.session_id },
  });
  assert.equal(canceled.res.status, 200);
  assert.deepEqual(canceled.json, { ok: true });
  const stillTrial = await call(base, '/v1/me', { headers: auth(token) });
  assert.equal(stillTrial.json.entitlement.plan, 'trial');

  const done = await call(base, '/v1/checkout/mock-complete', {
    method: 'POST',
    body: { session_id: session.json.session_id },
  });
  assert.equal(done.res.status, 200);
  assert.equal(done.json.entitlement.plan, 'pro');
  assert.equal(done.json.entitlement.status, 'active');

  const again = await call(base, '/v1/checkout/session', {
    method: 'POST',
    headers: auth(token),
    body: { plan: 'pro', interval: 'month' },
  });
  assert.equal(again.res.status, 403);
});

test('429 includes Retry-After and quota.reset_at', async () => {
  const { base } = await listen();
  const guest = 'browser-1';
  for (let i = 0; i < 3; i += 1) {
    const used = await call(base, '/v1/guest/consume-upload', {
      method: 'POST',
      headers: { 'x-guest-id': guest },
      body: { kind: 'upload' },
    });
    assert.equal(used.res.status, 200);
  }
  const demo = await call(base, '/v1/guest/consume-upload', {
    method: 'POST',
    headers: { 'x-guest-id': guest },
    body: { kind: 'demo' },
  });
  assert.equal(demo.res.status, 200);
  assert.equal(demo.json.counted, false);

  const blocked = await call(base, '/v1/guest/consume-upload', {
    method: 'POST',
    headers: { 'x-guest-id': guest },
    body: { kind: 'upload' },
  });
  assert.equal(blocked.res.status, 429);
  assert.ok(blocked.res.headers.get('retry-after'));
  assert.ok(Number(blocked.res.headers.get('retry-after')) >= 0);
  assert.ok(blocked.json.quota.reset_at);

  const quotaServer = await listen({ hostedRunsRemaining: 0 });
  const { token } = await login(quotaServer.base);
  const hist = await call(quotaServer.base, '/v1/history', {
    method: 'POST',
    headers: auth(token),
    body: { pattern_id: 'lollipop-rank', source_name: 'a.csv', row_count: 1 },
  });
  assert.equal(hist.res.status, 429);
  assert.ok(hist.res.headers.get('retry-after'));
  assert.ok(hist.json.quota.reset_at);
});

test('MOCK_PLAN=free hides history; MOCK_PLAN=active and force-active grant pro', async () => {
  const free = await listen({ mockPlan: 'free' });
  const freeLogin = await login(free.base);
  const freeMe = await call(free.base, '/v1/me', { headers: auth(freeLogin.token) });
  assert.equal(freeMe.json.entitlement.plan, 'free');
  const freeHist = await call(free.base, '/v1/history', { headers: auth(freeLogin.token) });
  assert.equal(freeHist.res.status, 403);

  const active = await listen({ mockPlan: 'active' });
  const activeLogin = await login(active.base);
  assert.equal(activeLogin.me.entitlement.plan, 'pro');
  assert.equal(activeLogin.me.entitlement.status, 'active');

  const forced = await listen({ mockPlan: 'free', forceActiveGithubIds: '1' });
  const forcedLogin = await login(forced.base);
  assert.equal(forcedLogin.me.entitlement.plan, 'pro');
  assert.equal(forcedLogin.me.entitlement.status, 'active');
  assert.equal(forcedLogin.me.entitlement.source, 'manual');
});

test('CORS allows configured origin and Authorization header', async () => {
  const { base } = await listen({ corsOrigin: 'http://127.0.0.1:4173' });
  const { res } = await call(base, '/v1/health', {
    headers: { origin: 'http://127.0.0.1:4173' },
  });
  assert.equal(res.headers.get('access-control-allow-origin'), 'http://127.0.0.1:4173');
  assert.match(res.headers.get('access-control-allow-headers') || '', /Authorization/);

  const preflight = await call(base, '/v1/auth/exchange', {
    method: 'OPTIONS',
    headers: {
      origin: 'http://127.0.0.1:4173',
      'access-control-request-method': 'POST',
      'access-control-request-headers': 'authorization,content-type',
    },
  });
  assert.equal(preflight.res.status, 204);
  assert.equal(preflight.res.headers.get('access-control-allow-origin'), 'http://127.0.0.1:4173');
  assert.match(preflight.res.headers.get('access-control-allow-headers') || '', /Authorization/);
  assert.match(preflight.res.headers.get('access-control-allow-headers') || '', /Content-Type/);
});

test('invalid bearer is 401', async () => {
  const { base } = await listen();
  const { res } = await call(base, '/v1/me', { headers: auth('not-a-real-token') });
  assert.equal(res.status, 401);
});
