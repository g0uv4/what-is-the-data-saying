'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');

test('CSP connect-src is self only while accounts are off', () => {
  assert.match(html, /connect-src 'self'/);
  assert.doesNotMatch(html, /connect-src 'none'/);
  assert.doesNotMatch(html, /127\.0\.0\.1:8787|localhost:8787/);
  assert.match(html, /script-src 'self'/);
  assert.match(html, /object-src 'none'/);
});

test('page loads api client + entitlement scripts before app.js', () => {
  const order = ['js/config.js', 'js/api.js', 'js/entitlement.js', 'js/i18n.js', 'js/csv.js', 'js/input.js', 'js/app.js'];
  let last = -1;
  for (const src of order) {
    const idx = html.indexOf('src="' + src + '"');
    assert.ok(idx > 0, src);
    assert.ok(idx > last, src + ' should follow previous script');
    last = idx;
  }
  assert.match(html, /id="accountBar"/);
  assert.match(html, /id="accountBar"[^>]*\bhidden\b/);
  assert.match(html, /id="loginBtn"/);
  assert.match(html, /用 GitHub 登入/);
  assert.match(html, /id="upgradeBtn"/);
  assert.match(html, />升級</);
});

test('account bar hidden rule wins over display:flex', () => {
  const css = fs.readFileSync(path.join(__dirname, '..', 'css', 'style.css'), 'utf8');
  assert.match(css, /\.account\[hidden\]\s*\{\s*display:\s*none\s*!important/);
});

test('file input accepts CSV, Excel and JSON; SheetJS is self-hosted', () => {
  assert.match(html, /id="fileInput"/);
  assert.match(html, /accept="[^"]*\.xlsx[^"]*\.xls[^"]*\.ods[^"]*\.json/);
  assert.match(html, /上傳 CSV、Excel、JSON/);
  assert.match(html, /id="sheetSelect"/);
  assert.match(html, /src="vendor\/xlsx\.full\.min\.js"/);
  assert.doesNotMatch(html, /cdn\.sheetjs\.com|cdnjs\.cloudflare\.com|unpkg\.com|jsdelivr/i);
  assert.doesNotMatch(html, /script-src[^"]*cdn/);
  assert.match(html, /script-src 'self'/);
  assert.doesNotMatch(html, /script-src [^"]*'unsafe-eval'/);
});

test('title, description and Open Graph tags (no og:image)', () => {
  assert.match(html, /<title>資料在說什麼？貼上一張表，先看該畫哪張圖<\/title>/);
  assert.match(html, /<meta name="description" content="貼上一張表，依資料形狀排出該畫的圖並附理由；69 種都會推薦、9 種可直接畫。分析全部在你的瀏覽器內完成，資料不會離開你的電腦。">/);
  assert.match(html, /<meta property="og:title" content="資料在說什麼？貼上來，先告訴你該畫哪張圖">/);
  assert.match(html, /<meta property="og:description" content="貼上一張表，依資料形狀排出該畫的圖並附理由；69 種都會推薦、9 種可直接畫。分析全部在你的瀏覽器內完成，資料不會離開你的電腦。">/);
  assert.match(html, /<meta property="og:url" content="https:\/\/what-is-the-data-saying\.vercel\.app\/">/);
  assert.match(html, /<meta property="og:type" content="website">/);
  assert.doesNotMatch(html, /property="og:image"/);
  assert.match(html, /connect-src 'self'/);
});

test('footer privacy sentence is browser-local and names no entitlement API', () => {
  const i18n = require('../js/i18n.js').WIDS_I18N;
  assert.equal(
    i18n.strings.zh.footer,
    '內容來自 g0uv4/what-is-the-data-saying（MIT；教圖內容見 ATTRIBUTION）。分析全部在你的瀏覽器內完成，資料不會離開你的電腦。'
  );
  assert.match(i18n.strings.en.footer, /All analysis is completed in your browser; data never leaves your computer\./);
  assert.doesNotMatch(i18n.strings.zh.footer, /權限 API|8787|file:\/\//);
  assert.doesNotMatch(i18n.strings.en.footer, /entitlement API|8787|file:\/\//);
});

test('zh noData and footer chart-request link stay on their own i18n nodes', () => {
  const i18n = require('../js/i18n.js').WIDS_I18N;
  assert.equal(
    i18n.strings.zh.noData,
    '還沒有資料。選一份示範資料，或上傳、貼上你的表，就會排出推薦圖種。'
  );
  assert.equal(
    i18n.strings.en.noData,
    'No data yet. Load a sample, or upload or paste your table, to see recommended charts.'
  );
  assert.equal(i18n.strings.zh.chartRequest, '想要新圖種？到 GitHub 提出圖表請求');
  assert.equal(i18n.strings.en.chartRequest, 'Want a new chart type? Request it on GitHub');
  assert.match(
    html,
    /<a href="https:\/\/github\.com\/g0uv4\/what-is-the-data-saying\/issues\/new\?template=chart-request\.yml" target="_blank" rel="noopener noreferrer" data-i18n="chartRequest">/
  );
  const footerP = html.match(/<p data-i18n="footer">([\s\S]*?)<\/p>/);
  assert.ok(footerP, 'footer privacy sentence has its own paragraph');
  assert.equal(footerP[1], '');
  assert.match(html, /<footer class="site-footer">[\s\S]*<p data-i18n="footer"><\/p>[\s\S]*<a href="https:\/\/github\.com\/g0uv4\/what-is-the-data-saying\/issues\/new\?template=chart-request\.yml"/);
});

test('hidden sheet field stays hidden despite .field { display:flex }', () => {
  const css = fs.readFileSync(path.join(__dirname, '..', 'css', 'style.css'), 'utf8');
  assert.match(css, /\.field\[hidden\]\s*\{\s*display:\s*none\s*!important/);
});
