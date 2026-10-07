/*
 * WIDS hosted API base + storage keys + account feature flag.
 * ACCOUNTS_ENABLED is off by default (11/7 launch is free-only).
 * Runtime override: set window.WIDS_ACCOUNTS_ENABLED / window.WIDS_API_BASE
 * before this file loads (same pattern).
 * Turning accounts on also requires adding the API origin to CSP connect-src
 * in index.html (currently 'self' only).
 */
(function (root) {
  'use strict';
  var DEFAULT_API_BASE = 'http://127.0.0.1:8787';
  var ACCOUNTS_ENABLED = false;

  function trimBase(value) {
    return String(value || '').trim().replace(/\/$/, '');
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

  function resolveApiBase() {
    if (typeof root.WIDS_API_BASE === 'string' && trimBase(root.WIDS_API_BASE)) {
      return trimBase(root.WIDS_API_BASE);
    }
    return DEFAULT_API_BASE;
  }

  function accountsEnabled() {
    var parsed = parseFlag(root.WIDS_ACCOUNTS_ENABLED);
    if (parsed !== null) return parsed;
    return ACCOUNTS_ENABLED;
  }

  root.WIDS_CONFIG = {
    DEFAULT_API_BASE: DEFAULT_API_BASE,
    ACCOUNTS_ENABLED: ACCOUNTS_ENABLED,
    TOKEN_KEY: 'wids_token',
    GUEST_ID_KEY: 'wids_guest_id',
    GUEST_UPLOADS_LIMIT: 3,
    guestUploadsKey: function (dateKey) {
      return 'wids_guest_uploads_' + dateKey;
    },
    resolveApiBase: resolveApiBase,
    accountsEnabled: accountsEnabled
  };
})(typeof self !== 'undefined' ? self : this);
