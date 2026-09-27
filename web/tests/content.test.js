'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const C = require('../js/charts.js');

const web = path.join(__dirname, '..');
const loadGlobal = (file) => { const ctx = { window: {} }; vm.runInNewContext(fs.readFileSync(path.join(web, file), 'utf8'), ctx); return ctx.window; };

test('generated content.js has all 49 patterns with markdown', () => {
  const w = loadGlobal('data/content.js');
  const p = w.WIDS_CONTENT.patterns;
  assert.equal(Object.keys(p).length, 49);
  for (const k of Object.keys(p)) assert.match(p[k].md, /^# Pattern: /, k);
});

test('generated samples.js matches examples/data/*.csv byte-for-byte (after newline normalisation)', () => {
  const w = loadGlobal('data/samples.js');
  const dir = path.join(web, '..', 'skills', 'what-is-the-data-saying', 'examples', 'data');
  const files = fs.readdirSync(dir).filter((f) => f.endsWith('.csv')).sort();
  assert.deepEqual(Array.from(w.WIDS_SAMPLES, (s) => s.file), files);
  for (const s of w.WIDS_SAMPLES) assert.equal(s.text, fs.readFileSync(path.join(dir, s.file), 'utf8').replace(/^\uFEFF/, '').replace(/\r\n?/g, '\n'), s.file);
});

test('chart helpers: aggregate, bins, boxStats, colour scale', () => {
  const agg = C.aggregate(['a', 'a', 'b'], null, [1, 2, 5], 'sum');
  assert.deepEqual(agg, { 'a\u0001': 3, 'b\u0001': 5 });
  assert.deepEqual(C.aggregate(['a', 'a', 'b'], null, null, 'sum'), { 'a\u0001': 2, 'b\u0001': 1 });
  const b = C.bins([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
  assert.equal(b.reduce((s, x) => s + x.count, 0), 10);
  const bs = C.boxStats([1, 2, 3, 4, 100]);
  assert.equal(bs.median, 3);
  assert.deepEqual(bs.outliers, [100]);
  assert.equal(C.colorScale(-1, 1).diverging, true);
  assert.equal(C.colorScale(0, 10).diverging, false);
});
