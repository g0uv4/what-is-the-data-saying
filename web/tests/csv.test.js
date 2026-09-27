'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { parseCSV, parseRows, sniffDelimiter } = require('../js/csv.js');

test('basic header + rows', () => {
  const r = parseCSV('a,b\n1,2\n3,4\n');
  assert.deepEqual(r.headers, ['a', 'b']);
  assert.deepEqual(r.rows, [['1', '2'], ['3', '4']]);
});

test('quoted fields with commas, escaped quotes and newlines', () => {
  const r = parseCSV('name,note\n"Smith, J","He said ""hi"""\n"multi\nline",x');
  assert.deepEqual(r.rows, [['Smith, J', 'He said "hi"'], ['multi\nline', 'x']]);
});

test('CRLF, lone CR and trailing newline', () => {
  assert.deepEqual(parseCSV('a,b\r\n1,2\r\n').rows, [['1', '2']]);
  assert.deepEqual(parseCSV('a,b\r1,2\r3,4').rows, [['1', '2'], ['3', '4']]);
});

test('UTF-8 BOM is stripped from first header', () => {
  const r = parseCSV('\uFEFF類別,數值\n甲,1');
  assert.equal(r.headers[0], '類別');
});

test('empty quoted field and empty trailing field', () => {
  assert.deepEqual(parseCSV('a,b,c\n"",2,\n').rows, [['', '2', '']]);
});

test('blank lines are skipped; ragged rows padded / truncated with a warning', () => {
  const r = parseCSV('a,b,c\n\n1,2\n1,2,3,4\n');
  assert.deepEqual(r.rows, [['1', '2', ''], ['1', '2', '3']]);
  assert.ok(r.warnings.some((w) => w.startsWith('ragged:')));
});

test('delimiter sniffing: semicolon and tab; comma inside quotes ignored', () => {
  assert.equal(sniffDelimiter('a;b;c\n1;2;3'), ';');
  assert.equal(sniffDelimiter('a\tb\n1\t2'), '\t');
  assert.equal(sniffDelimiter('"x,y,z";b;c\n'), ';');
  assert.deepEqual(parseCSV('a;b\n"1,5";2').rows, [['1,5', '2']]);
});

test('duplicate and blank headers get unique names', () => {
  assert.deepEqual(parseCSV('x,x,\n1,2,3').headers, ['x', 'x_2', 'col_3']);
});

test('empty input', () => {
  assert.deepEqual(parseCSV('').headers, []);
  assert.deepEqual(parseRows(''), []);
});
