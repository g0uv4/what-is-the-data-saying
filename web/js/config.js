/*
 * WIDS hosted API base + storage keys.
 * Edit DEFAULT_API_BASE for Preview / Production, and add that same origin
 * to the CSP connect-src list in index.html.
 * Runtime override: set window.WIDS_API_BASE before this file loads.
 */
(function (root) {
  'use strict';
  var DEFAULT_API_BASE = 'http://127.0.0.1:8787';

  function trimBase(value) {
    return String(value || '').trim().replace(/\/$/, '');
  }

  function resolveApiBase() {
    if (typeof root.WIDS_API_BASE === 'string' && trimBase(root.WIDS_API_BASE)) {
      return trimBase(root.WIDS_API_BASE);
    }
    return DEFAULT_API_BASE;
  }

  root.WIDS_CONFIG = {
    DEFAULT_API_BASE: DEFAULT_API_BASE,
    TOKEN_KEY: 'wids_token',
    GUEST_ID_KEY: 'wids_guest_id',
    GUEST_UPLOADS_LIMIT: 3,
    guestUploadsKey: function (dateKey) {
      return 'wids_guest_uploads_' + dateKey;
    },
    resolveApiBase: resolveApiBase
  };
})(typeof self !== 'undefined' ? self : this);
