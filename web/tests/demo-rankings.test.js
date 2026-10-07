'use strict';
/**
 * Regression: main:demos/ 四則貼上表在網頁推薦引擎必須排到預期圖種第 1。
 * 圖庫沒有獨立的 pie pattern；圓餅的平級組成替代是 waffle-percent。
 * 堆疊長條對應 categorical-comparison（長條圖／排序／分組／堆疊）。
 */
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { parseCSV } = require('../js/csv.js');
const T = require('../js/types.js');
const R = require('../js/rules.js');

const dir = path.join(__dirname, 'fixtures', 'demos');
const load = (file) => T.profileTable(parseCSV(fs.readFileSync(path.join(dir, file), 'utf8')));
const rankOf = (results, id) => {
  const i = results.filter((r) => r.eligible).findIndex((r) => r.id === id);
  return i === -1 ? Infinity : i;
};
const topIds = (results, n) => results.filter((r) => r.eligible).slice(0, n).map((r) => r.id);

const cases = [
  {
    file: '01-inventory-icicle.csv',
    expected: 'hierarchy-icicle',
    avoid: 'waffle-percent',
    hint: 'deepHierarchy'
  },
  {
    file: '02-signup-funnel.csv',
    expected: 'funnel-stages',
    avoid: 'sankey-flow',
    hint: 'monotoneStages'
  },
  {
    file: '03-earnings-waterfall.csv',
    expected: 'waterfall-bridge',
    avoid: 'categorical-comparison',
    hint: 'waterfallBridge'
  },
  {
    file: '04-before-after-dumbbell.csv',
    expected: 'dumbbell-gap',
    avoid: 'slope-two-period',
    hint: 'pairedPeriods'
  }
];

for (const c of cases) {
  test(`${c.file} ranks ${c.expected} #1; ${c.avoid} is not above it`, () => {
    const rec = R.recommend(load(c.file));
    assert.ok(rec.shape.hints[c.hint], `${c.file} should set hint ${c.hint}; hints=${Object.keys(rec.shape.hints).join(',')}`);
    const expectedRank = rankOf(rec.results, c.expected);
    const avoidRank = rankOf(rec.results, c.avoid);
    assert.equal(
      expectedRank,
      0,
      `${c.file} top should be ${c.expected}, got ${topIds(rec.results, 4).join(', ')}`
    );
    assert.ok(
      avoidRank > expectedRank,
      `${c.file}: ${c.avoid} rank ${avoidRank} must be below ${c.expected}`
    );
  });
}

test('dumbbell demo is not treated as a map; slope stays below dumbbell', () => {
  const rec = R.recommend(load('04-before-after-dumbbell.csv'));
  assert.ok(!rec.shape.hints.geo, '門市 is a store column, not a geo unit');
  assert.ok(rankOf(rec.results, 'choropleth-map') > rankOf(rec.results, 'dumbbell-gap'));
});
