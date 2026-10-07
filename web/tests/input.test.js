'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const IN = require('../js/input.js');
const { parseCSV } = require('../js/csv.js');

const fix = (name) => path.join(__dirname, 'fixtures', name);
const read = (name) => fs.readFileSync(fix(name));

test('xlsx date cells become ISO strings and default to the first sheet', () => {
  const parsed = IN.parseFile('dates-multisheet.xlsx', read('dates-multisheet.xlsx'));
  assert.deepEqual(parsed.sheetNames, ['銷售', '人口']);
  assert.equal(parsed.sheetName, '銷售');
  assert.deepEqual(parsed.headers, ['date', 'product', 'value']);
  assert.equal(parsed.rows[0][0], '2026-10-07');
  assert.equal(parsed.rows[1][0], '2026-10-08');
  assert.equal(parsed.rows[0][1], 'tea');
  assert.equal(parsed.rows[0][2], '12');
  for (const row of parsed.rows) {
    assert.doesNotMatch(row[0], /^\d{4,6}(\.\d+)?$/);
  }
});

test('xlsx second sheet converts to the same table shape as CSV', () => {
  const parsed = IN.parseFile('dates-multisheet.xlsx', read('dates-multisheet.xlsx'));
  const second = IN.sheetToTable(parsed.workbook, '人口');
  assert.deepEqual(second.headers, ['year', 'region', 'count']);
  assert.deepEqual(second.rows, [['2024', '北', '100'], ['2025', '南', '80']]);
  const csv = parseCSV('year,region,count\n2024,北,100\n2025,南,80\n');
  assert.deepEqual(second.headers, csv.headers);
  assert.deepEqual(second.rows, csv.rows);
});

test('Excel serial 46302 (2026-10-07) becomes an ISO date, never the raw number', () => {
  assert.equal(IN.serialToISO(46302), '2026-10-07');
  assert.equal(IN.serialToISO(46303), '2026-10-08');
});

test('xls and ods parse the same multi-sheet workbook', () => {
  for (const name of ['dates-multisheet.xls', 'dates-multisheet.ods']) {
    const parsed = IN.parseFile(name, read(name));
    assert.ok(parsed.sheetNames.includes('銷售'), name);
    assert.equal(parsed.rows[0][0], '2026-10-07', name);
  }
});

test('Big5-encoded CSV falls back after fatal UTF-8 and strips no mojibake', () => {
  const buf = read('big5.csv');
  assert.throws(() => new TextDecoder('utf-8', { fatal: true }).decode(buf));
  const dec = IN.decodeBytes(buf);
  assert.equal(dec.encoding, 'big5');
  assert.match(dec.text, /產品/);
  const parsed = IN.parseFile('big5.csv', buf);
  assert.deepEqual(parsed.headers, ['產品', '數量']);
  assert.deepEqual(parsed.rows, [['茶葉', '3'], ['咖啡', '5']]);
  assert.equal(parsed.encoding, 'big5');
});

test('semicolon CSV is auto-detected', () => {
  const parsed = IN.parseFile('semicolon.csv', read('semicolon.csv'));
  assert.equal(parsed.delimiter, ';');
  assert.deepEqual(parsed.headers, ['city', 'temp', 'rain']);
  assert.deepEqual(parsed.rows[0], ['Taipei', '28', '0.2']);
});

test('nested JSON flattens dotted keys; {data:[...]} wrapper works', () => {
  const nested = IN.parseFile('nested.json', read('nested.json'));
  assert.deepEqual(nested.headers, ['name', 'meta.city', 'stats.score']);
  assert.deepEqual(nested.rows, [['A', 'Taipei', '10'], ['B', 'Tainan', '8']]);
  const wrapped = IN.parseFile('wrapped.json', read('wrapped.json'));
  assert.deepEqual(wrapped.headers, nested.headers);
  assert.deepEqual(wrapped.rows, nested.rows);
});

test('paste text detects JSON, not only file upload', () => {
  const pasted = IN.parseText('{"data":[{"a":{"b":1}},{"a":{"b":2}}]}');
  assert.deepEqual(pasted.headers, ['a.b']);
  assert.deepEqual(pasted.rows, [['1'], ['2']]);
  const csv = IN.parseText('a,b\n1,2\n');
  assert.equal(csv.format, 'csv');
  assert.deepEqual(csv.rows, [['1', '2']]);
});

test('UTF-8 BOM CSV still works; files over 10 MB and unknown types are rejected', () => {
  const bom = Buffer.from('\uFEFFa,b\n1,2\n', 'utf8');
  const parsed = IN.parseFile('ok.csv', bom);
  assert.deepEqual(parsed.headers, ['a', 'b']);
  const huge = { byteLength: IN.MAX_BYTES + 1, buffer: new ArrayBuffer(0) };
  assert.throws(() => IN.parseFile('x.csv', huge), /10 MB/);
  assert.equal(IN.detectFormat('scan.pdf', new Uint8Array([1, 2, 3])), 'unsupported');
  assert.throws(() => IN.parseFile('scan.pdf', new Uint8Array([1, 2, 3])), /unsupported/);
});

test('more than 50,000 rows keeps the first 50,000 and warns', () => {
  const lines = ['n,v'];
  for (let i = 0; i < 50005; i++) lines.push(i + ',1');
  const parsed = IN.parseText(lines.join('\n'));
  assert.equal(parsed.rows.length, 50000);
  assert.equal(parsed.rows[0][0], '0');
  assert.equal(parsed.rows[49999][0], '49999');
  assert.ok(parsed.warnings.some((w) => w === 'truncated:50005'));
});
