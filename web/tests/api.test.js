'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const API = require('../js/api.js');
const cfgMod = require('../js/config.js');

function memoryStorage(seed) {
  const map = Object.assign(Object.create(null), seed || {});
  return {
    getItem: (key) => (Object.prototype.hasOwnProperty.call(map, key) ? map[key] : null),
    setItem: (key, value) => { map[key] = String(value); },
    removeItem: (key) => { delete map[key]; },
    _map: map
  };
}

function httpLoc() {
  return { protocol: 'http:', origin: 'http://127.0.0.1:4173' };
}

test('file:// and null origin never call fetch', async () => {
  let calls = 0;
  const fetchFn = async () => { calls += 1; throw new Error('should not fetch'); };
  const fileApi = API.createApi({
    location: { protocol: 'file:', origin: 'null' },
    fetch: fetchFn,
    storage: memoryStorage()
  });
  assert.equal(fileApi.canUseApi(), false);
  const me = await fileApi.me();
  assert.equal(me.skipped, true);
  assert.equal(calls, 0);

  const nullApi = API.createApi({
    location: { protocol: 'https:', origin: 'null' },
    fetch: fetchFn,
    storage: memoryStorage()
  });
  assert.equal(nullApi.canUseApi(), false);
  await nullApi.health();
  assert.equal(calls, 0);
  assert.equal(API.canUseApi({ protocol: 'file:', origin: 'file://' }), false);
});

test('resolveApiBase prefers window.WIDS_API_BASE then config default', () => {
  assert.equal(API.resolveApiBase({ WIDS_API_BASE: 'https://api.example.test/' }), 'https://api.example.test');
  assert.equal(API.resolveApiBase({ WIDS_CONFIG: { DEFAULT_API_BASE: 'http://127.0.0.1:8787' } }), 'http://127.0.0.1:8787');
  assert.equal(API.resolveApiBase({}, 'http://preview.example/api/'), 'http://preview.example/api');
  assert.equal(API.DEFAULT_BASE, 'http://127.0.0.1:8787');
  assert.equal(cfgMod.WIDS_CONFIG.DEFAULT_API_BASE, 'http://127.0.0.1:8787');
  assert.equal(cfgMod.WIDS_CONFIG.TOKEN_KEY, 'wids_token');
});

test('request sends Bearer + X-Guest-Id; 429 surfaces Retry-After and reset_at', async () => {
  const storage = memoryStorage({ wids_token: 'tok_abc', wids_guest_id: 'g_fixed' });
  const seen = [];
  const fetchFn = async (url, init) => {
    seen.push({ url, init });
    return {
      ok: false,
      status: 429,
      headers: { get: (name) => (name === 'Retry-After' ? '42' : null) },
      text: async () => JSON.stringify({
        error: { code: 'quota_exceeded', message: 'guest daily upload limit reached' },
        quota: { reset_at: '2026-10-08T00:00:00+08:00' }
      })
    };
  };
  const client = API.createApi({ location: httpLoc(), fetch: fetchFn, storage, apiBase: 'http://127.0.0.1:8787' });
  await assert.rejects(() => client.me(), (err) => {
    assert.equal(err.status, 429);
    assert.equal(err.retryAfter, '42');
    assert.equal(err.resetAt, '2026-10-08T00:00:00+08:00');
    assert.equal(err.code, 'quota_exceeded');
    return true;
  });
  assert.equal(seen[0].url, 'http://127.0.0.1:8787/v1/me');
  assert.equal(seen[0].init.headers.Authorization, 'Bearer tok_abc');
  assert.equal(seen[0].init.headers['X-Guest-Id'], 'g_fixed');
});

test('loginGithub stores opaque token from exchange', async () => {
  const storage = memoryStorage();
  const seen = [];
  const fetchFn = async (url, init) => {
    seen.push({ url: String(url), method: init && init.method, body: init && init.body });
    if (String(url).endsWith('/v1/auth/github')) {
      return {
        ok: true,
        status: 200,
        headers: { get: () => null },
        text: async () => JSON.stringify({ authorize_url: 'http://127.0.0.1:8787/v1/auth/github/callback?code=mock' })
      };
    }
    if (String(url).includes('/v1/auth/github/callback')) {
      assert.match(String(url), /\/v1\/auth\/github\/callback\?code=mock.*format=json/);
      return {
        ok: true,
        status: 200,
        headers: { get: () => null },
        text: async () => JSON.stringify({ code: 'once-code', expires_in: 60 })
      };
    }
    assert.match(String(url), /\/v1\/auth\/exchange$/);
    assert.equal(init.method, 'POST');
    assert.deepEqual(JSON.parse(init.body), { code: 'once-code' });
    return {
      ok: true,
      status: 200,
      headers: { get: () => null },
      text: async () => JSON.stringify({ access_token: 'opaque_token_no_dots', token_type: 'Bearer' })
    };
  };
  const client = API.createApi({ location: httpLoc(), fetch: fetchFn, storage, apiBase: 'http://127.0.0.1:8787' });
  const res = await client.loginGithub();
  assert.equal(res.json.access_token, 'opaque_token_no_dots');
  assert.equal(client.getToken(), 'opaque_token_no_dots');
  assert.ok(!client.getToken().includes('.'));
  assert.equal(seen[2].url, 'http://127.0.0.1:8787/v1/auth/exchange');
});

test('upgrade posts session then mock-complete and never opens checkout_url', async () => {
  const paths = [];
  const fetchFn = async (url, init) => {
    const u = new URL(url);
    paths.push({ path: u.pathname, method: init.method, body: init.body ? JSON.parse(init.body) : null });
    if (u.pathname === '/v1/checkout/session') {
      return {
        ok: true,
        status: 200,
        headers: { get: () => null },
        text: async () => JSON.stringify({
          session_id: 'cs_mock_1',
          checkout_url: 'http://127.0.0.1:8787/mock/checkout?session_id=cs_mock_1',
          mock: true
        })
      };
    }
    return {
      ok: true,
      status: 200,
      headers: { get: () => null },
      text: async () => JSON.stringify({ ok: true, session_id: 'cs_mock_1', entitlement: { plan: 'pro' } })
    };
  };
  const client = API.createApi({
    location: httpLoc(),
    fetch: fetchFn,
    storage: memoryStorage({ wids_token: 'tok' }),
    apiBase: 'http://127.0.0.1:8787'
  });
  const res = await client.upgrade();
  assert.equal(res.json.entitlement.plan, 'pro');
  assert.deepEqual(paths.map((p) => p.path), ['/v1/checkout/session', '/v1/checkout/mock-complete']);
  assert.deepEqual(paths[0].body, { plan: 'pro', interval: 'month' });
  assert.deepEqual(paths[1].body, { session_id: 'cs_mock_1' });
  assert.ok(paths.every((p) => p.path !== '/mock/checkout'));
});

test('saveHistory sends summary only (no raw CSV keys)', async () => {
  let body;
  const fetchFn = async (url, init) => {
    body = JSON.parse(init.body);
    return {
      ok: true,
      status: 201,
      headers: { get: () => null },
      text: async () => JSON.stringify({ id: 'hist_1', created_at: '2026-10-07T12:00:00+08:00' })
    };
  };
  const client = API.createApi({
    location: httpLoc(),
    fetch: fetchFn,
    storage: memoryStorage({ wids_token: 'tok' }),
    apiBase: 'http://127.0.0.1:8787'
  });
  const res = await client.saveHistory({
    pattern_id: 'lollipop-rank',
    source_name: 'demo.csv',
    row_count: 12,
    csv: 'this must not be sent',
    raw_csv: 'nope'
  });
  assert.equal(res.status, 201);
  assert.deepEqual(Object.keys(body).sort(), ['pattern_id', 'row_count', 'source_name']);
  assert.equal(body.pattern_id, 'lollipop-rank');
});

test('consumeAuthCodeFromSearch exchanges code and strips it from the URL', async () => {
  const storage = memoryStorage();
  let replaced = '';
  const fetchFn = async (url, init) => {
    assert.equal(url, 'http://127.0.0.1:8787/v1/auth/exchange');
    assert.equal(init.method, 'POST');
    assert.deepEqual(JSON.parse(init.body), { code: 'once-code' });
    return {
      ok: true,
      status: 200,
      headers: { get: () => null },
      text: async () => JSON.stringify({ access_token: 'tok_from_code', token_type: 'Bearer' })
    };
  };
  const client = API.createApi({ location: httpLoc(), fetch: fetchFn, storage, apiBase: 'http://127.0.0.1:8787' });
  const href = 'http://127.0.0.1:4173/app/?code=once-code&x=1#sample=demo.csv';
  const result = await client.consumeAuthCodeFromSearch('?code=once-code&x=1', href, function (_state, _title, next) {
    replaced = next;
  });
  assert.equal(result.consumed, true);
  assert.equal(client.getToken(), 'tok_from_code');
  assert.equal(replaced, '/app/?x=1#sample=demo.csv');
});

test('consumeAuthCodeFromSearch ignores access_token and still strips code on failure', async () => {
  const storage = memoryStorage();
  let replaced = '';
  const fetchFn = async () => ({
    ok: false,
    status: 400,
    headers: { get: () => null },
    text: async () => JSON.stringify({ error: { code: 'invalid_grant', message: 'authorization code is invalid or already used' } })
  });
  const client = API.createApi({ location: httpLoc(), fetch: fetchFn, storage, apiBase: 'http://127.0.0.1:8787' });
  assert.equal(typeof client.captureTokenFromSearch, 'undefined');
  const ignored = await client.consumeAuthCodeFromSearch(
    '?access_token=from_redirect&x=1',
    'http://127.0.0.1:4173/?access_token=from_redirect&x=1',
    function (_state, _title, next) { replaced = next; }
  );
  assert.equal(ignored.consumed, false);
  assert.equal(client.getToken(), '');
  assert.equal(replaced, '/?x=1');

  await assert.rejects(
    () => client.consumeAuthCodeFromSearch(
      '?code=used-code&keep=yes',
      'http://127.0.0.1:4173/?code=used-code&keep=yes#hash',
      function (_state, _title, next) { replaced = next; }
    ),
    (err) => {
      assert.equal(err.status, 400);
      assert.equal(err.code, 'invalid_grant');
      return true;
    }
  );
  assert.equal(client.getToken(), '');
  assert.equal(replaced, '/?keep=yes#hash');
});
