'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const ENT = require('../js/entitlement.js');

function memoryStorage(seed) {
  const map = Object.assign(Object.create(null), seed || {});
  return {
    getItem: (key) => (Object.prototype.hasOwnProperty.call(map, key) ? map[key] : null),
    setItem: (key, value) => { map[key] = String(value); },
    removeItem: (key) => { delete map[key]; },
    _map: map
  };
}

const t = (key, vars) => {
  const S = {
    loginGithub: '用 GitHub 登入',
    upgrade: '升級',
    logout: '登出',
    planGuest: '訪客 · 今日剩餘自貼 {n}/{limit}',
    planUser: '{login} · {plan}',
    planTrial: '試用',
    planPro: 'Pro',
    planFree: '免費',
    apiOffline: '權限 API 未連上',
    apiOfflineFile: 'file:// 不呼叫權限 API',
    apiBusy: '處理中…'
  };
  let s = S[key] || key;
  if (vars) Object.keys(vars).forEach((k) => { s = s.replace('{' + k + '}', vars[k]); });
  return s;
};

test('taipeiDateKey and guest localStorage key', () => {
  const key = ENT.taipeiDateKey(new Date('2026-10-07T01:00:00+08:00'));
  assert.match(key, /^\d{4}-\d{2}-\d{2}$/);
  assert.equal(ENT.uploadsKey('2026-10-07'), 'wids_guest_uploads_2026-10-07');
  assert.equal(ENT.LIMIT, 3);
});

test('guest quota increment, remaining, and API sync', () => {
  const now = new Date('2026-10-07T12:00:00+08:00');
  const storage = memoryStorage();
  const q = ENT.createGuestQuota({ storage, now: () => now });
  assert.equal(q.storageKey(), 'wids_guest_uploads_2026-10-07');
  assert.equal(q.remaining(), 3);
  q.increment();
  q.increment();
  assert.equal(q.getCount(), 2);
  assert.equal(q.remaining(), 1);
  q.syncFromApi(0);
  assert.equal(q.remaining(), 0);
  assert.equal(q.effectiveRemaining(2), 0);
  const other = ENT.createGuestQuota({ storage: memoryStorage(), now: () => now });
  assert.equal(other.effectiveRemaining(1), 1);
});

test('feature / guest / upgrade helpers', () => {
  assert.equal(ENT.isGuest(null), true);
  assert.equal(ENT.isGuest({ user: null }), true);
  assert.equal(ENT.planOf({ entitlement: { plan: 'trial' } }), 'trial');
  assert.equal(ENT.hasFeature({ entitlement: { features: ['save_history'] } }, 'save_history'), true);
  assert.equal(ENT.hasFeature({ entitlement: { features: [] } }, 'save_history'), false);
  assert.equal(ENT.canUpgrade({ user: { login: 'wids-mock' }, entitlement: { plan: 'trial', status: 'trialing' } }), true);
  assert.equal(ENT.canUpgrade({ user: { login: 'wids-mock' }, entitlement: { plan: 'pro', status: 'active' } }), false);
  assert.equal(ENT.canUpgrade({ user: null }), false);
});

test('account UI: guest login, trial upgrade, pro hides upgrade, file:// skips API buttons', () => {
  function els() {
    return {
      status: { textContent: '' },
      login: { textContent: '', hidden: true, disabled: false },
      upgrade: { textContent: '', hidden: true, disabled: false },
      logout: { textContent: '', hidden: true, disabled: false }
    };
  }

  const guest = els();
  ENT.applyAccountUI(guest, { remaining: 3, me: { user: null, entitlement: { plan: 'free' } } }, t);
  assert.equal(guest.login.hidden, false);
  assert.equal(guest.upgrade.hidden, true);
  assert.equal(guest.login.textContent, '用 GitHub 登入');
  assert.match(guest.status.textContent, /剩餘自貼 3\/3/);

  const trial = els();
  ENT.applyAccountUI(trial, {
    remaining: 3,
    me: { user: { login: 'wids-mock' }, entitlement: { plan: 'trial', status: 'trialing' } }
  }, t);
  assert.equal(trial.login.hidden, true);
  assert.equal(trial.upgrade.hidden, false);
  assert.equal(trial.upgrade.textContent, '升級');
  assert.match(trial.status.textContent, /wids-mock · 試用/);

  const pro = els();
  ENT.applyAccountUI(pro, {
    remaining: 3,
    me: { user: { login: 'wids-mock' }, entitlement: { plan: 'pro', status: 'active' } }
  }, t);
  assert.equal(pro.upgrade.hidden, true);
  assert.equal(pro.logout.hidden, false);
  assert.match(pro.status.textContent, /Pro/);

  const file = els();
  ENT.applyAccountUI(file, { file: true, remaining: 2, me: null }, t);
  assert.equal(file.login.hidden, true);
  assert.equal(file.upgrade.hidden, true);
  assert.match(file.status.textContent, /file:\/\//);
});
