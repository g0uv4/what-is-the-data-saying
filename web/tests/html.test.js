'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');

test('CSP connect-src allows local mock API and is not none', () => {
  assert.match(html, /connect-src 'self' http:\/\/127\.0\.0\.1:8787 http:\/\/localhost:8787/);
  assert.doesNotMatch(html, /connect-src 'none'/);
  assert.match(html, /script-src 'self'/);
  assert.match(html, /object-src 'none'/);
});

test('page loads api client + entitlement scripts before app.js', () => {
  const order = ['js/config.js', 'js/api.js', 'js/entitlement.js', 'js/i18n.js', 'js/app.js'];
  let last = -1;
  for (const src of order) {
    const idx = html.indexOf('src="' + src + '"');
    assert.ok(idx > 0, src);
    assert.ok(idx > last, src + ' should follow previous script');
    last = idx;
  }
  assert.match(html, /id="loginBtn"/);
  assert.match(html, /用 GitHub 登入/);
  assert.match(html, /id="upgradeBtn"/);
  assert.match(html, />升級</);
});
