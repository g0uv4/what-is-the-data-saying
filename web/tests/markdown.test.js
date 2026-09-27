'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { render } = require('../js/markdown.js');

test('headings, lists, bold, code, blockquote', () => {
  const h = render('# Title\n\n> **圖種**：x\n\n- a `c`\n  - b\n1. one');
  assert.match(h, /<h1>Title<\/h1>/);
  assert.match(h, /<blockquote><p><strong>圖種<\/strong>：x<\/p><\/blockquote>/);
  assert.match(h, /<ul><li>a <code>c<\/code><ul><li>b<\/li><\/ul><\/li><\/ul>/);
  assert.match(h, /<ol><li>one<\/li><\/ol>/);
});

test('HTML is escaped (no injection)', () => {
  const h = render('<script>alert(1)</script> <img src=x onerror=alert(1)> **<b>x</b>**');
  assert.ok(!/<script|<img|<b>/.test(h));
  assert.match(h, /&lt;script&gt;/);
});

test('external links open in a new tab with rel=noopener; unsafe schemes dropped', () => {
  const h = render('[ok](https://example.com/a_(b)) [bad](javascript:alert(1)) [data](data:text/html,x)');
  assert.match(h, /<a href="https:\/\/example.com\/a_\(b\)" target="_blank" rel="noopener noreferrer">ok<\/a>/);
  assert.ok(!/href="javascript/i.test(h));
  assert.ok(!/href="data:/.test(h));
  assert.match(h, /bad/);
});

test('attribute-breaking URLs are escaped', () => {
  const h = render('[x](https://a.com/"onmouseover="alert(1))');
  assert.ok(!/"onmouseover="/.test(h));
});

test('code spans are not formatted and can become internal links', () => {
  const h = render('see `**x**` and `spiral-plot.md`', { codeLink: (c) => (c === 'spiral-plot.md' ? 'spiral-plot' : null) });
  assert.match(h, /<code>\*\*x\*\*<\/code>/);
  assert.match(h, /data-pattern="spiral-plot"/);
});

test('fenced code, tables, task lists', () => {
  const h = render('```js\nconst a = "<x>";\n```\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n- [ ] todo\n- [x] done');
  assert.match(h, /<pre><code class="lang-js">const a = &quot;&lt;x&gt;&quot;;<\/code><\/pre>/);
  assert.match(h, /<table><thead><tr><th>a<\/th><th>b<\/th><\/tr><\/thead><tbody><tr><td>1<\/td><td>2<\/td><\/tr>/);
  assert.match(h, /☐ todo/);
  assert.match(h, /☑ done/);
});
