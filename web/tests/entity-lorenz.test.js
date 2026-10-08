'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const R = require('../js/rules.js');
const T = require('../js/types.js');
const { parseCSV } = require('../js/csv.js');

const shape = (csvText) => R.computeShape(T.profileTable(parseCSV(csvText)));

function table(headers, rows) {
  return [headers.join(',')].concat(rows.map((row) => row.join(','))).join('\n');
}

function result(csvText, id) {
  return R.evaluate(shape(csvText), 'en').find((r) => r.id === id);
}

const NAMES = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel', 'India', 'Juliet'];
const SEEDS = [12.4, 3.1, 27.9, 8.6, 15.2, 4.7, 19.3, 6.8, 11.5, 22.1, 9.4, 14.8];

function amount(i) {
  const raw = SEEDS[i % SEEDS.length] + Math.floor(i / SEEDS.length) * 0.37;
  return Math.round(raw * 100) / 100;
}

function code(i) {
  return 'P' + String(i).padStart(2, '0');
}

function subjectMonths(ids) {
  return table(['subject', 'months'], ids.map((id, i) => [id, amount(i)]));
}

function namedAmounts(names, values) {
  return table(['unit', 'amount'], names.map((name, i) => [name, values ? values[i] : amount(i)]));
}

test('unique subject ids set oneRowPerEntity and make swimmer-plot eligible', () => {
  const csv = subjectMonths(Array.from({ length: 12 }, (_, i) => code(i + 1)));
  const s = shape(csv);
  assert.equal(s.hints.oneRowPerEntity, true);
  assert.equal(s.roles.entity, 'subject');
  assert.equal(result(csv, 'swimmer-plot').eligible, true);
});

test('repeated subject codes do not set oneRowPerEntity and are not an entity key', () => {
  const ids = [];
  for (let i = 1; i <= 6; i++) ids.push(code(i), code(i));
  const csv = subjectMonths(ids);
  const s = shape(csv);
  assert.equal(s.hints.oneRowPerEntity, undefined);
  assert.equal(s.roles.entity, undefined);
  assert.equal(s.counts.id, 0);
  assert.equal(s.counts.label, 1);
  assert.equal(result(csv, 'swimmer-plot').eligible, true);
});

test('two uneven decimal measures and no id or category leave swimmer-plot and marey-chart ineligible', () => {
  const rows = [];
  for (let i = 0; i < 12; i++) rows.push([amount(i), Math.round((amount(i + 5) + 0.13) * 100) / 100]);
  const csv = table(['reading', 'score'], rows);
  const s = shape(csv);
  assert.equal(s.counts.id, 0);
  assert.equal(s.counts.category, 0);
  assert.equal(s.counts.measure, 2);
  const swimmer = result(csv, 'swimmer-plot');
  assert.equal(swimmer.eligible, false);
  assert.equal(result(csv, 'marey-chart').eligible, false);
  assert.ok(swimmer.missing.some((m) => m.includes('label')), swimmer.missing.join(', '));
});

test('unflagged rules do not treat a unique id as a label', () => {
  const csv = subjectMonths(Array.from({ length: 12 }, (_, i) => code(i + 1)));
  for (const id of ['lollipop-rank', 'categorical-comparison']) {
    const r = result(csv, id);
    assert.equal(r.eligible, false, id);
    assert.ok(r.missing.some((m) => m.includes('label')), id + ': ' + r.missing.join(', '));
  }
});

test('acceptsEntityKey is set exactly on swimmer-plot, lasagna-plot, and marey-chart', () => {
  const flagged = R.RULES.filter((r) => r.acceptsEntityKey).map((r) => r.id).sort();
  assert.deepEqual(flagged, ['lasagna-plot', 'marey-chart', 'swimmer-plot']);
  assert.equal(R.byId('lorenz-curve').acceptsEntityKey, undefined);
});

test('an id column with one missing value does not set oneRowPerEntity', () => {
  const ids = Array.from({ length: 12 }, (_, i) => (i === 6 ? '' : code(i + 1)));
  const csv = subjectMonths(ids);
  const s = shape(csv);
  assert.equal(s.counts.id, 1);
  assert.equal(s.hints.oneRowPerEntity, undefined);
  assert.equal(s.roles.entity, undefined);
});

test('ten named units with non-negative amounts make lorenz-curve eligible', () => {
  const csv = namedAmounts(NAMES);
  const s = shape(csv);
  assert.equal(s.counts.label, 1);
  assert.equal(s.counts.id, 0);
  assert.equal(result(csv, 'lorenz-curve').eligible, true);
});

test('nine named units leave lorenz-curve ineligible and name the unit floor', () => {
  const csv = namedAmounts(NAMES.slice(0, 9));
  const lorenz = result(csv, 'lorenz-curve');
  assert.equal(lorenz.eligible, false);
  assert.ok(lorenz.missing.includes('units ≥ 10'), lorenz.missing.join(', '));
});

test('a negative amount leaves lorenz-curve ineligible for nonNegative', () => {
  const values = NAMES.map((_, i) => (i === 1 ? -3.1 : amount(i)));
  const csv = namedAmounts(NAMES, values);
  const lorenz = result(csv, 'lorenz-curve');
  assert.equal(lorenz.eligible, false);
  assert.ok(lorenz.missing.includes('all values non-negative'), lorenz.missing.join(', '));
});

test('a subject id plus one non-negative measure does not make lorenz-curve eligible', () => {
  const csv = subjectMonths(Array.from({ length: 30 }, (_, i) => code(i + 1)));
  const s = shape(csv);
  assert.equal(s.counts.id, 1);
  assert.equal(s.hints.oneRowPerEntity, true);
  assert.equal(s.hints.nonNegative, true);
  assert.equal(result(csv, 'lorenz-curve').eligible, false);
});

test('lorenz units are the crossed category size, not the row count', () => {
  const wide = [];
  let k = 0;
  for (const group of ['A', 'B']) {
    for (const unit of NAMES) wide.push([group, unit, amount(k++)]);
  }
  const wideCsv = table(['group', 'unit', 'amount'], wide);
  const wideShape = shape(wideCsv);
  assert.equal(wideShape.units, 10);
  assert.equal(result(wideCsv, 'lorenz-curve').eligible, true);

  const narrow = [];
  k = 0;
  for (const group of ['A', 'B', 'C', 'D']) {
    for (const unit of NAMES.slice(0, 4)) narrow.push([group, unit, amount(k++)]);
  }
  const narrowCsv = table(['group', 'unit', 'amount'], narrow);
  const narrowShape = shape(narrowCsv);
  assert.equal(narrowShape.rows, 16);
  assert.equal(narrowShape.units, 4);
  assert.equal(result(narrowCsv, 'lorenz-curve').eligible, false);
});

test('a pure even-step sequence does not make lorenz-curve eligible', () => {
  const rows = [];
  for (let i = 1; i <= 30; i++) rows.push([i, amount(i - 1)]);
  const csv = table(['t', 'value'], rows);
  const s = shape(csv);
  assert.equal(s.hints.seqAxis, true);
  assert.equal(s.roles.seqAxis, 't');
  assert.ok(!s.roles.measures.includes('t'));
  assert.equal(result(csv, 'lorenz-curve').eligible, false);
});
