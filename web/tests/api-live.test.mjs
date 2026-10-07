import assert from 'node:assert/strict';
import http from 'node:http';
import { createRequire } from 'node:module';
import { after, test } from 'node:test';
import { createRequestListener } from '../api-mock/lib/app.mjs';

const require = createRequire(import.meta.url);
const API = require('../js/api.js');

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

function memoryStorage() {
  const map = Object.create(null);
  return {
    getItem: (key) => (Object.prototype.hasOwnProperty.call(map, key) ? map[key] : null),
    setItem: (key, value) => { map[key] = String(value); },
    removeItem: (key) => { delete map[key]; }
  };
}

function clientFor(base, extra = {}) {
  return API.createApi({
    location: { protocol: 'http:', origin: 'http://127.0.0.1:4173' },
    apiBase: base,
    storage: extra.storage || memoryStorage(),
    accountsEnabled: extra.accountsEnabled !== false,
    fetch
  });
}

test('live mock: guest me, github login, history, upgrade', async () => {
  const { base } = await listen();
  const storage = memoryStorage();
  const api = clientFor(base, { storage });

  const health = await api.health();
  assert.deepEqual(health.json, { ok: true, mock: true });

  const guest = await api.me();
  assert.equal(guest.json.user, null);
  assert.equal(guest.json.entitlement.quota.guest_uploads_remaining_today, 3);

  await api.loginGithub();
  assert.ok(api.getToken());
  const trial = await api.me();
  assert.equal(trial.json.user.login, 'wids-mock');
  assert.equal(trial.json.entitlement.plan, 'trial');
  assert.ok(trial.json.entitlement.features.includes('save_history'));

  const hist = await api.saveHistory({
    pattern_id: 'lollipop-rank',
    source_name: 'demo.csv',
    row_count: 12
  });
  assert.equal(hist.status, 201);

  const upgraded = await api.upgrade();
  assert.equal(upgraded.json.entitlement.plan, 'pro');
  const me = await api.me();
  assert.equal(me.json.entitlement.plan, 'pro');
  assert.equal(me.json.entitlement.status, 'active');
});

test('accounts flag off: live mock is never contacted', async () => {
  let hits = 0;
  const { base } = await listen();
  const api = API.createApi({
    location: { protocol: 'http:', origin: 'http://127.0.0.1:4173' },
    apiBase: base,
    storage: memoryStorage(),
    accountsEnabled: false,
    fetch: async () => {
      hits += 1;
      throw new Error('accounts flag off must not fetch');
    }
  });
  assert.equal((await api.health()).skipped, true);
  assert.equal((await api.me()).skipped, true);
  assert.equal((await api.loginGithub()).skipped, true);
  assert.equal((await api.upgrade()).skipped, true);
  assert.equal((await api.saveHistory({ pattern_id: 'lollipop-rank', source_name: 'demo.csv', row_count: 1 })).skipped, true);
  assert.equal((await api.consumeGuestUpload('upload')).skipped, true);
  assert.equal(hits, 0);
});
