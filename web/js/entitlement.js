/*
 * Guest daily upload quota + account-bar helpers.
 * Works in browsers (window.WIDS_ENTITLEMENT) and Node (module.exports).
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.WIDS_ENTITLEMENT = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var LIMIT = 3;

  function memoryStorage() {
    var map = Object.create(null);
    return {
      getItem: function (key) {
        return Object.prototype.hasOwnProperty.call(map, key) ? map[key] : null;
      },
      setItem: function (key, value) {
        map[key] = String(value);
      },
      removeItem: function (key) {
        delete map[key];
      }
    };
  }

  function taipeiDateKey(now) {
    var parts = new Intl.DateTimeFormat('en-CA', {
      timeZone: 'Asia/Taipei',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    }).formatToParts(now || new Date());
    function pick(type) {
      var found = parts.filter(function (part) { return part.type === type; })[0];
      return found ? found.value : '';
    }
    return pick('year') + '-' + pick('month') + '-' + pick('day');
  }

  function uploadsKey(dateKey) {
    return 'wids_guest_uploads_' + dateKey;
  }

  function createGuestQuota(opts) {
    opts = opts || {};
    var storage = opts.storage || (typeof localStorage !== 'undefined' ? localStorage : memoryStorage());
    var nowFn = opts.now || function () { return new Date(); };
    var limit = typeof opts.limit === 'number' ? opts.limit : LIMIT;

    function dateKey() {
      return taipeiDateKey(nowFn());
    }

    function storageKey() {
      return uploadsKey(dateKey());
    }

    function getCount() {
      var n = Number(storage.getItem(storageKey()) || '0');
      if (!Number.isFinite(n) || n < 0) return 0;
      return Math.floor(n);
    }

    function remaining() {
      return Math.max(0, limit - getCount());
    }

    function increment() {
      storage.setItem(storageKey(), String(getCount() + 1));
      return remaining();
    }

    function syncFromApi(apiRemaining) {
      if (typeof apiRemaining !== 'number' || !Number.isFinite(apiRemaining)) return remaining();
      var used = Math.max(0, limit - Math.max(0, Math.floor(apiRemaining)));
      if (used > getCount()) storage.setItem(storageKey(), String(used));
      return remaining();
    }

    function effectiveRemaining(apiRemaining) {
      var local = remaining();
      if (typeof apiRemaining !== 'number' || !Number.isFinite(apiRemaining)) return local;
      return Math.min(local, Math.max(0, Math.floor(apiRemaining)));
    }

    return {
      LIMIT: limit,
      dateKey: dateKey,
      storageKey: storageKey,
      getCount: getCount,
      remaining: remaining,
      increment: increment,
      syncFromApi: syncFromApi,
      effectiveRemaining: effectiveRemaining
    };
  }

  function hasFeature(me, name) {
    var features = me && me.entitlement && me.entitlement.features;
    return Array.isArray(features) && features.indexOf(name) >= 0;
  }

  function isGuest(me) {
    return !me || !me.user;
  }

  function planOf(me) {
    return (me && me.entitlement && me.entitlement.plan) || 'free';
  }

  function canUpgrade(me) {
    if (isGuest(me)) return false;
    var plan = planOf(me);
    var status = me.entitlement && me.entitlement.status;
    return !(plan === 'pro' && status === 'active');
  }

  function planLabel(plan, t) {
    switch (plan) {
      case 'pro':
        return t('planPro');
      case 'trial':
        return t('planTrial');
      case 'free':
        return t('planFree');
      default:
        return plan || t('planFree');
    }
  }

  function setHidden(node, hidden) {
    if (!node) return;
    node.hidden = !!hidden;
  }

  function applyAccountUI(els, state, t) {
    els = els || {};
    state = state || {};
    var status = els.status;
    var login = els.login;
    var upgrade = els.upgrade;
    var logout = els.logout;
    var remaining = typeof state.remaining === 'number' ? state.remaining : LIMIT;
    var busy = !!state.busy;

    if (login) {
      login.textContent = t('loginGithub');
      login.disabled = busy;
    }
    if (upgrade) {
      upgrade.textContent = t('upgrade');
      upgrade.disabled = busy;
    }
    if (logout) {
      logout.textContent = t('logout');
      logout.disabled = busy;
    }

    var line;
    if (state.file) {
      line = t('planGuest', { n: remaining, limit: LIMIT }) + ' · ' + t('apiOfflineFile');
      setHidden(login, true);
      setHidden(upgrade, true);
      setHidden(logout, true);
    } else if (state.offline && isGuest(state.me)) {
      line = (state.message || t('apiOffline')) + ' · ' + t('planGuest', { n: remaining, limit: LIMIT });
      setHidden(login, true);
      setHidden(upgrade, true);
      setHidden(logout, true);
    } else if (isGuest(state.me)) {
      line = t('planGuest', { n: remaining, limit: LIMIT });
      setHidden(login, false);
      setHidden(upgrade, true);
      setHidden(logout, true);
    } else {
      line = t('planUser', { login: state.me.user.login, plan: planLabel(planOf(state.me), t) });
      setHidden(login, true);
      setHidden(upgrade, !canUpgrade(state.me));
      setHidden(logout, false);
    }

    if (state.message && !state.file && !(state.offline && isGuest(state.me))) {
      line += ' · ' + state.message;
    } else if (state.busy) {
      line += ' · ' + t('apiBusy');
    }
    if (status) status.textContent = line;
    return line;
  }

  return {
    LIMIT: LIMIT,
    taipeiDateKey: taipeiDateKey,
    uploadsKey: uploadsKey,
    createGuestQuota: createGuestQuota,
    hasFeature: hasFeature,
    isGuest: isGuest,
    planOf: planOf,
    canUpgrade: canUpgrade,
    planLabel: planLabel,
    applyAccountUI: applyAccountUI
  };
});
