/*
 * WIDS mock entitlement API client.
 * Works in browsers (window.WIDS_API) and Node (module.exports).
 * file:// / null origin never calls the network.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.WIDS_API = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var TOKEN_KEY = 'wids_token';
  var GUEST_ID_KEY = 'wids_guest_id';
  var DEFAULT_BASE = 'http://127.0.0.1:8787';

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

  function parseFlag(value) {
    if (value === true || value === 1) return true;
    if (value === false || value === 0) return false;
    if (typeof value === 'string') {
      var v = value.trim().toLowerCase();
      if (v === 'true' || v === '1') return true;
      if (v === 'false' || v === '0') return false;
    }
    return null;
  }

  function accountsEnabled(scope, override) {
    if (typeof override === 'boolean') return override;
    var parsed = parseFlag(scope && scope.WIDS_ACCOUNTS_ENABLED);
    if (parsed !== null) return parsed;
    if (scope && scope.WIDS_CONFIG && typeof scope.WIDS_CONFIG.accountsEnabled === 'function') {
      return !!scope.WIDS_CONFIG.accountsEnabled();
    }
    if (scope && scope.WIDS_CONFIG && typeof scope.WIDS_CONFIG.ACCOUNTS_ENABLED === 'boolean') {
      return scope.WIDS_CONFIG.ACCOUNTS_ENABLED;
    }
    return false;
  }

  function canUseApi(loc) {
    if (!loc) return false;
    var proto = loc.protocol || '';
    if (proto === 'file:' || proto === 'about:') return false;
    if (!loc.origin || loc.origin === 'null') return false;
    return proto === 'http:' || proto === 'https:';
  }

  function trimBase(value) {
    return String(value || '').trim().replace(/\/$/, '');
  }

  function resolveApiBase(scope, override) {
    if (typeof override === 'string') return trimBase(override);
    if (scope && typeof scope.WIDS_API_BASE === 'string' && trimBase(scope.WIDS_API_BASE)) {
      return trimBase(scope.WIDS_API_BASE);
    }
    if (scope && scope.WIDS_CONFIG && typeof scope.WIDS_CONFIG.resolveApiBase === 'function') {
      return trimBase(scope.WIDS_CONFIG.resolveApiBase()) || DEFAULT_BASE;
    }
    if (scope && scope.WIDS_CONFIG && scope.WIDS_CONFIG.DEFAULT_API_BASE) {
      return trimBase(scope.WIDS_CONFIG.DEFAULT_API_BASE) || DEFAULT_BASE;
    }
    return DEFAULT_BASE;
  }

  function createApi(opts) {
    opts = opts || {};
    var scope = opts.root || (typeof self !== 'undefined' ? self : (typeof globalThis !== 'undefined' ? globalThis : {}));
    var loc = opts.location || (typeof location !== 'undefined' ? location : { protocol: '', origin: '' });
    var storage = opts.storage || (typeof localStorage !== 'undefined' ? localStorage : memoryStorage());
    var fetchFn = opts.fetch;
    if (!fetchFn && typeof fetch === 'function') {
      fetchFn = fetch.bind(typeof globalThis !== 'undefined' ? globalThis : scope);
    }
    var cfg = scope.WIDS_CONFIG || {};
    var tokenKey = cfg.TOKEN_KEY || TOKEN_KEY;
    var guestKey = cfg.GUEST_ID_KEY || GUEST_ID_KEY;
    var base = resolveApiBase(scope, opts.apiBase);
    var accountsOn = accountsEnabled(scope, opts.accountsEnabled);

    function enabled() {
      return accountsOn && canUseApi(loc) && !!base;
    }

    function getToken() {
      return storage.getItem(tokenKey) || '';
    }

    function setToken(token) {
      if (!token) storage.removeItem(tokenKey);
      else storage.setItem(tokenKey, token);
    }

    function getGuestId() {
      var id = storage.getItem(guestKey);
      if (id) return id;
      id = 'g_' + Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
      storage.setItem(guestKey, id);
      return id;
    }

    function readSearchParams(search) {
      if (!search) return new URLSearchParams();
      var raw = String(search);
      if (raw.charAt(0) === '?') raw = raw.slice(1);
      return new URLSearchParams(raw);
    }

    function stripAuthParams(href, replaceState) {
      if (!href || typeof replaceState !== 'function') return '';
      var clean = new URL(href, 'http://127.0.0.1');
      clean.searchParams.delete('code');
      clean.searchParams.delete('access_token');
      var next = clean.pathname + clean.search + clean.hash;
      replaceState(null, '', next);
      return next;
    }

    function exchangeCode(code) {
      return request('POST', '/v1/auth/exchange', { code: code }).then(function (res) {
        if (res.skipped) return res;
        var token = res.json && res.json.access_token;
        if (!token) throw new Error('missing access_token');
        setToken(token);
        return res;
      });
    }

    function consumeAuthCodeFromSearch(search, href, replaceState) {
      var params = readSearchParams(search);
      var code = params.get('code');
      if (!code) {
        if (params.get('access_token')) stripAuthParams(href, replaceState);
        return Promise.resolve({ consumed: false, exchanged: false });
      }
      if (!enabled()) {
        stripAuthParams(href, replaceState);
        return Promise.resolve({ consumed: true, exchanged: false, skipped: true });
      }
      return exchangeCode(code).then(function (res) {
        stripAuthParams(href, replaceState);
        return { consumed: true, exchanged: !res.skipped, res: res };
      }, function (err) {
        stripAuthParams(href, replaceState);
        throw err;
      });
    }

    function headers(extra) {
      var out = { Accept: 'application/json' };
      var token = getToken();
      if (token) out.Authorization = 'Bearer ' + token;
      out['X-Guest-Id'] = getGuestId();
      if (extra) Object.keys(extra).forEach(function (key) { out[key] = extra[key]; });
      return out;
    }

    function skipped() {
      return { skipped: true, status: 0, json: null };
    }

    function request(method, path, body) {
      if (!enabled()) return Promise.resolve(skipped());
      if (!fetchFn) return Promise.reject(new Error('fetch is not available'));
      var init = { method: method, headers: headers() };
      if (body !== undefined) {
        init.headers['Content-Type'] = 'application/json';
        init.body = JSON.stringify(body);
      }
      return fetchFn(base + path, init).then(function (res) {
        return res.text().then(function (text) {
          var json = null;
          if (text) {
            try { json = JSON.parse(text); } catch (err) { json = null; }
          }
          if (!res.ok) {
            var retryAfter = res.headers && res.headers.get ? res.headers.get('Retry-After') : null;
            var resetAt = json && json.quota ? json.quota.reset_at : null;
            var message = (json && json.error && json.error.message) || ('HTTP ' + res.status);
            var error = new Error(message);
            error.status = res.status;
            error.code = json && json.error ? json.error.code : undefined;
            error.retryAfter = retryAfter;
            error.resetAt = resetAt;
            error.body = json;
            throw error;
          }
          return { skipped: false, status: res.status, json: json, res: res };
        });
      });
    }

    function health() {
      return request('GET', '/v1/health');
    }

    function me() {
      return request('GET', '/v1/me');
    }

    function loginGithub() {
      return request('GET', '/v1/auth/github').then(function (authz) {
        if (authz.skipped) return authz;
        var authorizeUrl = authz.json && authz.json.authorize_url;
        if (!authorizeUrl) throw new Error('missing authorize_url');
        var path = '/v1/auth/github/callback?code=mock&format=json';
        try {
          var parsed = new URL(authorizeUrl);
          if (!parsed.searchParams.get('code')) throw new Error('missing code');
          parsed.searchParams.set('format', 'json');
          path = parsed.pathname + parsed.search;
        } catch (err) {
          if (err.message === 'missing code') throw err;
        }
        return request('GET', path).then(function (callback) {
          if (callback.skipped) return callback;
          var code = callback.json && callback.json.code;
          if (!code) throw new Error('missing code');
          return exchangeCode(code);
        });
      });
    }

    function upgrade() {
      return request('POST', '/v1/checkout/session', { plan: 'pro', interval: 'month' }).then(function (session) {
        if (session.skipped) return session;
        var sessionId = session.json && session.json.session_id;
        if (!sessionId) throw new Error('missing session_id');
        return request('POST', '/v1/checkout/mock-complete', { session_id: sessionId });
      });
    }

    function saveHistory(summary) {
      var body = {
        pattern_id: summary.pattern_id,
        source_name: summary.source_name,
        row_count: summary.row_count
      };
      return request('POST', '/v1/history', body);
    }

    function consumeGuestUpload(kind) {
      return request('POST', '/v1/guest/consume-upload', { kind: kind === 'demo' ? 'demo' : 'upload' });
    }

    function logout() {
      setToken('');
    }

    return {
      TOKEN_KEY: tokenKey,
      GUEST_ID_KEY: guestKey,
      accountsEnabled: function () { return accountsOn; },
      canUseApi: enabled,
      apiBase: function () { return base; },
      getToken: getToken,
      setToken: setToken,
      getGuestId: getGuestId,
      consumeAuthCodeFromSearch: consumeAuthCodeFromSearch,
      exchangeCode: exchangeCode,
      stripAuthParams: stripAuthParams,
      request: request,
      health: health,
      me: me,
      loginGithub: loginGithub,
      upgrade: upgrade,
      saveHistory: saveHistory,
      consumeGuestUpload: consumeGuestUpload,
      logout: logout
    };
  }

  return {
    TOKEN_KEY: TOKEN_KEY,
    GUEST_ID_KEY: GUEST_ID_KEY,
    DEFAULT_BASE: DEFAULT_BASE,
    canUseApi: canUseApi,
    accountsEnabled: accountsEnabled,
    resolveApiBase: resolveApiBase,
    createApi: createApi
  };
});
