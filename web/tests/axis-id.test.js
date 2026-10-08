'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const R = require('../js/rules.js');
const T = require('../js/types.js');
const { parseCSV } = require('../js/csv.js');

const shape = (csvText) => R.computeShape(T.profileTable(parseCSV(csvText)));

function range(start, end, step) {
  const out = [];
  if (step > 0) for (let v = start; v <= end; v += step) out.push(v);
  else for (let v = start; v >= end; v += step) out.push(v);
  return out;
}

function repeatBlock(values, times) {
  const out = [];
  for (let t = 0; t < times; t++) out.push(...values);
  return out;
}

function table(headers, rows) {
  return [headers.join(',')].concat(rows.map((row) => row.join(','))).join('\n');
}

function limitCsv() {
  const rows = [];
  for (let i = 1; i <= 30; i++) rows.push([i, Math.round(50 + Math.sin(i) * 8), 50]);
  return table(['t', 'value', 'limit'], rows);
}

test('detectEvenStepAxis accepts even integer steps, including decreases and repeated runs', () => {
  assert.deepEqual(R.detectEvenStepAxis(range(0, 19, 1)), { step: 1, distinct: 20, runs: 1 });
  assert.deepEqual(R.detectEvenStepAxis(range(1, 25, 1)), { step: 1, distinct: 25, runs: 1 });
  assert.deepEqual(R.detectEvenStepAxis(range(0, 45, 5)), { step: 5, distinct: 10, runs: 1 });
  assert.deepEqual(R.detectEvenStepAxis(range(50, 30, -2)), { step: -2, distinct: 11, runs: 1 });
  assert.deepEqual(R.detectEvenStepAxis(repeatBlock(range(1, 12, 1), 5)), { step: 1, distinct: 12, runs: 5 });
});

test('detectEvenStepAxis rejects uneven, non-integer, short, constant, and short-segment series', () => {
  assert.equal(R.detectEvenStepAxis([1, 2, 4, 7, 11, 16, 22]), null);
  assert.equal(R.detectEvenStepAxis([0.5, 1.5, 2.5, 3.5, 4.5, 5.5]), null);
  assert.equal(R.detectEvenStepAxis([3, 8, 9, 15, 22, 30, 41]), null);
  assert.equal(R.detectEvenStepAxis([1, 2, 3, 4, 5]), null);
  assert.equal(R.detectEvenStepAxis([7, 7, 7, 7, 7, 7, 7]), null);
  assert.equal(R.detectEvenStepAxis(repeatBlock(range(1, 4, 1), 5)), null);
});

test('inferColumn treats unique codes and id-named integers as ids, not unique names or repeated subjects', () => {
  const codes = Array.from({ length: 30 }, (_, i) => 'P' + String(i + 1).padStart(2, '0'));
  assert.equal(T.inferColumn('person', codes).type, 'id');

  const subjects = Array.from({ length: 30 }, (_, i) => String(i + 1));
  assert.equal(T.inferColumn('subject', subjects).type, 'id');

  assert.equal(T.inferColumn('country', ['Japan', 'Taiwan', 'Korea', 'France', 'Brazil', 'Kenya', 'Peru']).type, 'category');
  assert.equal(T.inferColumn('product', ['Lamp', 'Chair', 'Desk', 'Mug', 'Kettle', 'Notebook', 'Blanket']).type, 'category');

  const band = [];
  for (let i = 0; i < 10; i++) band.push('A', 'B', 'C');
  assert.equal(T.inferColumn('band', band).type, 'category');

  const repeated = [];
  for (let s = 1; s <= 8; s++) {
    const code = 'S' + String(s).padStart(2, '0');
    repeated.push(code, code);
  }
  assert.notEqual(T.inferColumn('subject', repeated).type, 'id');
});

test('even integer axis is a sequence, not a measure, and a long one is a long series', () => {
  const rows = [];
  for (let i = 0; i < 100; i++) rows.push([i, Math.sin(i / 5)]);
  const s = shape(table(['t', 'z'], rows));
  assert.equal(s.hints.seqAxis, true);
  assert.equal(s.roles.seqAxis, 't');
  assert.ok(!s.roles.measures.includes('t'));
  assert.equal(s.hints.longSeries, true);
  assert.equal(s.hints.time, undefined);
});

test('uneven sorted measure stays a measure and is not a sequence axis', () => {
  const dose = [3, 8, 9, 15, 22, 30, 41, 55];
  const response = [1.2, 4.7, 3.1, 8.8, 6.4, 9.5, 2.9, 7.3];
  const s = shape(table(['dose', 'response'], dose.map((d, i) => [d, response[i]])));
  assert.equal(s.hints.seqAxis, undefined);
  assert.ok(s.roles.measures.includes('dose'));
});

test('constant text is not a label; only the varying item column counts', () => {
  const items = ['apple', 'basin', 'cedar', 'drum', 'ember', 'flint', 'grape', 'hazel'];
  const rows = items.map((item, i) => [item, i + 1, 'unchanged']);
  const s = shape(table(['item', 'value', 'note'], rows));
  assert.equal(s.counts.label, 1);
});

test('constant numeric column is a reference line, not a measure', () => {
  const s = shape(limitCsv());
  assert.ok(!s.roles.measures.includes('limit'));
  assert.equal(s.hints.refLines, true);
});

test('id columns are not labels and do not make one-row-per-category', () => {
  const rows = [];
  for (let i = 1; i <= 20; i++) {
    rows.push(['P' + String(i).padStart(2, '0'), i % 2 ? 'A' : 'B', i]);
  }
  const s = shape(table(['subject', 'group', 'time'], rows));
  assert.equal(s.counts.label, 1);
  assert.equal(s.counts.id, 1);
  assert.equal(s.hints.oneRowPerCat, undefined);
});

test('control chart is eligible and ranked first when a series has a reference limit', () => {
  const eligible = R.recommend(T.profileTable(parseCSV(limitCsv()))).results.filter((r) => r.eligible);
  assert.ok(eligible.some((r) => r.id === 'control-chart'));
  assert.equal(eligible[0].id, 'control-chart');
});
