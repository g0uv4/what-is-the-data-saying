'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const T = require('../js/types.js');
const { parseCSV } = require('../js/csv.js');

const typeOf = (name, values) => T.inferColumn(name, values).type;

test('parseNumber handles thousands, %, currency, parentheses, unicode minus', () => {
  assert.equal(T.parseNumber('1,234.5'), 1234.5);
  assert.equal(T.parseNumber('12%'), 12);
  assert.equal(T.parseNumber('NT$ 300'), 300);
  assert.equal(T.parseNumber('(45)'), -45);
  assert.equal(T.parseNumber('\u22123'), -3);
  assert.ok(Number.isNaN(T.parseNumber('12a')));
  assert.ok(Number.isNaN(T.parseNumber('1,23')));
});

test('parseDate formats and granularity', () => {
  assert.equal(T.parseDate('2024-01').gran, 'month');
  assert.equal(T.parseDate('2024-01-15').gran, 'day');
  assert.equal(T.parseDate('2024/1/5 13:45').gran, 'datetime');
  assert.equal(T.parseDate('2024Q2').gran, 'quarter');
  assert.equal(T.parseDate('2024年3月').gran, 'month');
  assert.equal(T.parseDate('2024-02-30'), null);
  assert.equal(T.parseDate('2024'), null, 'bare year needs allowYear');
  assert.equal(T.parseDate('2024', true).gran, 'year');
});

test('number / category / date / boolean / id inference', () => {
  assert.equal(typeOf('value', ['1', '2.5', '3,000', '']), 'number');
  assert.equal(typeOf('region', ['北', '南', '北', '東']), 'category');
  assert.equal(typeOf('month', ['2024-01', '2024-02', '2024-03']), 'date');
  assert.equal(typeOf('year', ['2019', '2020', '2021']), 'date');
  assert.equal(typeOf('count', ['2019', '2020', '2021']), 'number');
  assert.equal(typeOf('active', ['yes', 'no', 'yes']), 'boolean');
  assert.equal(typeOf('flag', ['是', '否']), 'boolean');
  assert.equal(typeOf('id', ['1', '2', '3']), 'id');
  const many = Array.from({ length: 40 }, (_, i) => 'user-' + i);
  assert.equal(typeOf('user', many), 'id');
  assert.equal(typeOf('category', ['A', 'B', 'C']), 'category', 'few unique labels stay category');
});

test('missing values are counted and do not break inference', () => {
  const c = T.inferColumn('v', ['1', 'NA', '', '-', '4']);
  assert.equal(c.type, 'number');
  assert.equal(c.missing, 3);
  assert.equal(c.distinct, 2);
});

test('profileTable applies overrides and coerces values', () => {
  const parsed = parseCSV('year,sales\n2020,10\n2021,12\n');
  const p = T.profileTable(parsed);
  assert.equal(p.columns[0].type, 'date');
  assert.equal(p.columns[1].stats.sum, 22);
  const p2 = T.profileTable(parsed, { year: 'category' });
  assert.equal(p2.columns[0].type, 'category');
  assert.equal(p2.columns[0].inferred, 'date');
  assert.deepEqual(p2.columns[0].values, ['2020', '2021']);
});
