export class HttpError extends Error {
  constructor(status, code, message, extra = {}) {
    super(message);
    this.status = status;
    this.code = code;
    this.extra = extra;
  }
}

export function sendJson(res, status, body, extraHeaders = {}) {
  const payload = JSON.stringify(body);
  res.writeHead(status, {
    'content-type': 'application/json; charset=utf-8',
    'content-length': Buffer.byteLength(payload),
    ...extraHeaders,
  });
  res.end(payload);
}

export function sendError(res, err) {
  const status = err instanceof HttpError ? err.status : 500;
  const extra = err instanceof HttpError ? { ...err.extra } : {};
  const retryAfter = extra.retryAfter;
  delete extra.retryAfter;
  const body = {
    error: {
      code: err instanceof HttpError ? err.code : 'internal_error',
      message: err instanceof HttpError ? err.message : 'internal error',
    },
    ...extra,
  };
  const headers = {};
  if (status === 429) {
    if (typeof retryAfter === 'number') {
      headers['retry-after'] = String(retryAfter);
    } else if (extra.quota?.reset_at) {
      const seconds = Math.max(0, Math.ceil((Date.parse(extra.quota.reset_at) - Date.now()) / 1000));
      headers['retry-after'] = String(seconds);
    } else {
      headers['retry-after'] = '60';
    }
  }
  sendJson(res, status, body, headers);
}

export async function readJsonBody(req, limit = 64 * 1024) {
  const chunks = [];
  let size = 0;
  for await (const chunk of req) {
    size += chunk.length;
    if (size > limit) {
      throw new HttpError(400, 'body_too_large', 'request body too large');
    }
    chunks.push(chunk);
  }
  if (chunks.length === 0) return {};
  const raw = Buffer.concat(chunks).toString('utf8').trim();
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch {
    throw new HttpError(400, 'invalid_json', 'request body is not valid JSON');
  }
}

export function applyCors(req, res, origin) {
  const allowOrigin = origin || '*';
  res.setHeader('access-control-allow-origin', allowOrigin);
  res.setHeader('access-control-allow-headers', 'Authorization, Content-Type, X-Guest-Id');
  res.setHeader('access-control-allow-methods', 'GET, POST, OPTIONS');
  res.setHeader('access-control-expose-headers', 'Retry-After');
  res.setHeader('access-control-max-age', '86400');
  if (req.headers['access-control-request-private-network'] === 'true') {
    res.setHeader('access-control-allow-private-network', 'true');
  }
  if (allowOrigin !== '*') {
    res.setHeader('vary', 'Origin');
  }
}
