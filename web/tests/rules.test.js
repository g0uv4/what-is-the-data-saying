'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { parseCSV } = require('../js/csv.js');
const T = require('../js/types.js');
const R = require('../js/rules.js');
const C = require('../js/charts.js');

const skill = path.join(__dirname, '..', '..', 'skills', 'what-is-the-data-saying');
const load = (f) => T.profileTable(parseCSV(fs.readFileSync(path.join(skill, 'examples', 'data', f), 'utf8')));
const rec = (f) => R.recommend(load(f));
const topIds = (f, n) => rec(f).results.filter((r) => r.eligible).slice(0, n).map((r) => r.id);

test('rule table covers exactly the pattern files', () => {
  const files = fs.readdirSync(path.join(skill, 'examples')).filter((f) => f.endsWith('.md') && f !== 'README.md').map((f) => f.slice(0, -3)).sort();
  const ids = R.RULES.map((r) => r.id).sort();
  assert.equal(ids.length, files.length);
  assert.deepEqual(ids, files);
});

test('every rule is well-formed and references known hints / renderers', () => {
  for (const r of R.RULES) {
    assert.ok(r.zh && r.en && r.fields.zh && r.fields.en && r.why.zh && r.why.en, r.id);
    for (const h of r.need.concat(r.prefer, r.avoid)) for (const k of h.split('|')) assert.ok(R.HINTS[k.replace(/^!/, '')], `${r.id}: unknown hint ${k}`);
    for (const x of r.render) assert.ok(C.renderers[x.r], `${r.id}: unknown renderer ${x.r}`);
  }
  assert.ok(R.RULES.filter((r) => r.render.length).length >= 5);
});

const expectations = [
  ['sample-heatmap.csv', 'matrix-heatmap', 1],
  ['sample-spiral.csv', 'time-series-trend', 1],
  ['sample-spiral.csv', 'spiral-plot', 2],
  ['lollipop-categories.csv', 'lollipop-rank', 2],
  ['lollipop-categories.csv', 'categorical-comparison', 2],
  ['sample-boxplot.csv', 'boxplot-summary', 1],
  ['sample-bubble.csv', 'bubble-chart', 1],
  ['population-pyramid-long.csv', 'population-pyramid', 1],
  ['population-pyramid-wide.csv', 'population-pyramid', 1],
  ['sample-choropleth.csv', 'choropleth-map', 1],
  ['sample-tilemap.csv', 'tile-map', 1],
  ['sample-biofabric.csv', 'biofabric', 1],
  ['sample-biofabric.csv', 'adjacency-matrix', 3],
  ['sample-marimekko.csv', 'marimekko-chart', 2],
  ['streamgraph-categories.csv', 'time-series-trend', 1],
  ['streamgraph-categories.csv', 'streamgraph-composition', 2],
  ['streamgraph-wide.csv', 'streamgraph-composition', 3],
  ['dot-density-one-to-many.csv', 'dot-density-map', 1],
  ['dot-density-one-to-one.csv', 'dot-density-map', 1]
];
for (const [file, id, within] of expectations) {
  test(`${file} → ${id} within top ${within}`, () => {
    const top = topIds(file, within);
    assert.ok(top.includes(id), `top ${within}: ${top.join(', ')}`);
  });
}

test('simple charts beat novel ones on plain category + value data', () => {
  const ids = topIds('lollipop-categories.csv', 99);
  assert.ok(ids.indexOf('categorical-comparison') < ids.indexOf('circular-bar'));
  assert.ok(!ids.includes('choropleth-map'));
  assert.ok(!ids.includes('time-series-trend'));
});

test('ineligible rules explain what is missing; teaching-only rules are flagged', () => {
  const r = rec('lollipop-categories.csv').results;
  const gantt = r.find((x) => x.id === 'gantt-schedule');
  assert.equal(gantt.eligible, false);
  assert.ok(gantt.missing.length > 0);
  assert.equal(r.find((x) => x.id === 'biofabric').renderable, false);
  assert.equal(r.find((x) => x.id === 'matrix-heatmap').renderable, true);
});

test('hint detection on synthetic shapes', () => {
  const prof = (csv) => T.profileTable(parseCSV(csv));
  const funnel = R.computeShape(prof('stage,users\n曝光,1000\n點擊,300\n註冊,80\n購買,20'));
  assert.ok(funnel.hints.stages);
  const gantt = R.computeShape(prof('task,start,end\nA,2024-01-01,2024-01-10\nB,2024-01-05,2024-02-01'));
  assert.ok(gantt.hints.startEnd);
  const sets = R.computeShape(prof('item,a,b,c\nx,1,0,1\ny,0,1,1\nz,1,1,0'));
  assert.ok(sets.hints.sets);
  const daily = Array.from({ length: 90 }, (_, i) => `2024-${String(1 + Math.floor(i / 28)).padStart(2, '0')}-${String(1 + (i % 28)).padStart(2, '0')},${i}`).join('\n');
  const cal = R.computeShape(prof('date,v\n' + daily));
  assert.ok(cal.hints.daily);
  const wf = R.computeShape(prof('step,change\n起點,100\n價格,20\n成本,-35\n匯率,-5'));
  assert.ok(wf.hints.delta);
  assert.ok(!wf.hints.waterfallBridge, 'partial signed steps without start+end identity are not a bridge');
  const bridge = R.computeShape(prof('item,amt\n起點,100\n加項,20\n減項,-35\n終點,85'));
  assert.ok(bridge.hints.waterfallBridge);
  const funnelMono = R.computeShape(prof('stage,users\n曝光,1000\n點擊,300\n註冊,80\n購買,20'));
  assert.ok(funnelMono.hints.monotoneStages);
});

test('changing a column type changes recommendations (manual override)', () => {
  const parsed = parseCSV(fs.readFileSync(path.join(skill, 'examples', 'data', 'sample-spiral.csv'), 'utf8'));
  const asCat = T.profileTable(parsed, { month: 'category', year: 'category' });
  const ids = R.recommend(asCat).results.filter((r) => r.eligible).map((r) => r.id);
  assert.ok(!ids.includes('time-series-trend'));
});

test('renderers available for sample data', () => {
  assert.ok(C.available(load('sample-heatmap.csv')).includes('heatmap'));
  assert.ok(C.available(load('sample-bubble.csv')).includes('scatter'));
  assert.ok(!C.available(load('lollipop-categories.csv')).includes('scatter'));
});
