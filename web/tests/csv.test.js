'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { parseCSV, parseRows, sniffDelimiter, stripLeadingComments } = require('../js/csv.js');

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

test('leading Chinese # comment block is skipped', () => {
  const text = [
    '# 虛構資料，數字未核｜圖 S1',
    '# 第二行說明：全形標點，不是表頭',
    'sample,x',
    'A,1',
    'B,2'
  ].join('\n');
  const r = parseCSV(text);
  assert.deepEqual(r.headers, ['sample', 'x']);
  assert.deepEqual(r.rows, [['A', '1'], ['B', '2']]);
  assert.equal(r.skippedLines, 2);
  assert.deepEqual(r.warnings, ['comments:2']);
  assert.equal(r.delimiter, ',');
});

test('a # comment with ASCII commas but a different field count is skipped', () => {
  const text = '# notes: (m,τ)=(1,1)/(2,8),x\na,b,c\n1,2,3\n';
  const r = parseCSV(text);
  assert.deepEqual(r.headers, ['a', 'b', 'c']);
  assert.deepEqual(r.rows, [['1', '2', '3']]);
  assert.equal(r.skippedLines, 1);
  assert.deepEqual(r.warnings, ['comments:1']);
});

test('# as its own first header cell is kept', () => {
  const r = parseCSV('#,name,value\n1,a,2\n3,b,4\n');
  assert.deepEqual(r.headers, ['#', 'name', 'value']);
  assert.deepEqual(r.rows, [['1', 'a', '2'], ['3', 'b', '4']]);
  assert.equal(r.skippedLines, 0);
  assert.deepEqual(r.warnings, []);
});

test('header whose first name starts with # is kept', () => {
  const r = parseCSV('#id,score\n7,9\n8,10\n');
  assert.deepEqual(r.headers, ['#id', 'score']);
  assert.deepEqual(r.rows, [['7', '9'], ['8', '10']]);
  assert.equal(r.skippedLines, 0);
  assert.deepEqual(r.warnings, []);
});

test('a comment before a #id header is skipped and the header is kept', () => {
  const r = parseCSV('# 這是註解\n#id,score\n7,9\n');
  assert.deepEqual(r.headers, ['#id', 'score']);
  assert.deepEqual(r.rows, [['7', '9']]);
  assert.equal(r.skippedLines, 1);
  assert.deepEqual(r.warnings, ['comments:1']);
});

test('# after the header has started is kept as data', () => {
  const r = parseCSV('id,note\n#3,x\n4,#foo\n');
  assert.deepEqual(r.headers, ['id', 'note']);
  assert.deepEqual(r.rows, [['#3', 'x'], ['4', '#foo']]);
  assert.equal(r.skippedLines, 0);
  assert.deepEqual(r.warnings, []);
});

test('a single # comment line followed by header and data is skipped', () => {
  const prose = parseCSV('# a note\nsample,x\n1,2\n');
  assert.deepEqual(prose.headers, ['sample', 'x']);
  assert.deepEqual(prose.rows, [['1', '2']]);
  assert.equal(prose.skippedLines, 1);
  assert.deepEqual(prose.warnings, ['comments:1']);

  const bare = parseCSV('#\nsample,x\n1,2\n');
  assert.deepEqual(bare.headers, ['sample', 'x']);
  assert.deepEqual(bare.rows, [['1', '2']]);
  assert.equal(bare.skippedLines, 1);
  assert.deepEqual(bare.warnings, ['comments:1']);
});

test('single-column: "# note" is a comment, "#id" is a header', () => {
  const note = parseCSV('# note\nvalue\n1\n2');
  assert.deepEqual(note.headers, ['value']);
  assert.deepEqual(note.rows, [['1'], ['2']]);
  assert.equal(note.skippedLines, 1);
  assert.deepEqual(note.warnings, ['comments:1']);

  const id = parseCSV('#id\n1\n2');
  assert.deepEqual(id.headers, ['#id']);
  assert.deepEqual(id.rows, [['1'], ['2']]);
  assert.equal(id.skippedLines, 0);
  assert.deepEqual(id.warnings, []);
});

test('CRLF comment block is skipped and the remaining endings are preserved', () => {
  const text = '# 註解一\r\n# 註解二\r\nsample,x\r\n1,2\r\n';
  const r = parseCSV(text);
  assert.deepEqual(r.headers, ['sample', 'x']);
  assert.deepEqual(r.rows, [['1', '2']]);
  assert.equal(r.skippedLines, 2);
  assert.deepEqual(r.warnings, ['comments:2']);
  const stripped = stripLeadingComments(text);
  assert.equal(stripped.text, 'sample,x\r\n1,2\r\n');
  assert.equal(stripped.skipped, 2);
  assert.equal(stripped.delimiter, ',');
});

test('BOM before a leading # comment is stripped with the comment', () => {
  const text = '\uFEFF# 虛構資料，數字未核｜圖 S1\nsample,x\n1,2\n';
  const r = parseCSV(text);
  assert.deepEqual(r.headers, ['sample', 'x']);
  assert.deepEqual(r.rows, [['1', '2']]);
  assert.equal(r.skippedLines, 1);
  assert.deepEqual(r.warnings, ['comments:1']);
  assert.equal(stripLeadingComments(text).text, 'sample,x\n1,2\n');
});

test('semicolon data: delimiter is sniffed from the anchor, not the comment', () => {
  const text = '# notes, with, commas\nname;value;flag\na;1;y\n';
  const r = parseCSV(text);
  assert.equal(r.delimiter, ';');
  assert.deepEqual(r.headers, ['name', 'value', 'flag']);
  assert.deepEqual(r.rows, [['a', '1', 'y']]);
  assert.equal(r.skippedLines, 1);
  assert.deepEqual(r.warnings, ['comments:1']);

  const forced = parseCSV('#id;score\n1;2\n3;4\n', { delimiter: ',' });
  assert.equal(forced.delimiter, ',');
  assert.deepEqual(forced.headers, ['#id;score']);
  assert.deepEqual(forced.rows, [['1;2'], ['3;4']]);
  assert.equal(forced.skippedLines, 0);
});

test('empty file and a file of only # lines do not skip', () => {
  const empty = parseCSV('');
  assert.deepEqual(empty.headers, []);
  assert.deepEqual(empty.rows, []);
  assert.deepEqual(empty.warnings, ['empty']);
  assert.equal(empty.skippedLines, 0);

  const only = parseCSV('# only a comment\n# another line\n');
  assert.deepEqual(only.headers, ['# only a comment']);
  assert.deepEqual(only.rows, [['# another line']]);
  assert.equal(only.skippedLines, 0);
  assert.deepEqual(only.warnings, []);

  const blanksToo = parseCSV('# only a comment\n\n# another line\n');
  assert.deepEqual(blanksToo.headers, ['# only a comment']);
  assert.deepEqual(blanksToo.rows, [['# another line']]);
  assert.equal(blanksToo.skippedLines, 0);
});

test('blank lines between comment lines and the header stay in the block', () => {
  const text = '\n# 虛構資料，數字未核｜圖 S1\n\n# 第二行說明\n\nsample,x\n1,2\n';
  const r = parseCSV(text);
  assert.deepEqual(r.headers, ['sample', 'x']);
  assert.deepEqual(r.rows, [['1', '2']]);
  assert.equal(r.skippedLines, 2);
  assert.deepEqual(r.warnings, ['comments:2']);
  assert.equal(stripLeadingComments(text).text, 'sample,x\n1,2\n');
});

test('ragged counting ignores skipped comment lines', () => {
  const r = parseCSV('# a note\nx,y\n1,2,3\n4\n');
  assert.deepEqual(r.headers, ['x', 'y']);
  assert.deepEqual(r.rows, [['1', '2'], ['4', '']]);
  assert.equal(r.skippedLines, 1);
  assert.deepEqual(r.warnings, ['comments:1', 'ragged:2']);
});

test('parseRows itself does not strip leading # comments', () => {
  assert.deepEqual(parseRows('# c\na,b\n1,2\n'), [['# c'], ['a', 'b'], ['1', '2']]);
});

test('a comment with the same field count as the header is kept', () => {
  const r = parseCSV('# same,count\nreal,header\n1,2\n');
  assert.deepEqual(r.headers, ['# same', 'count']);
  assert.deepEqual(r.rows, [['real', 'header'], ['1', '2']]);
  assert.equal(r.skippedLines, 0);
});

test('text with no leading # block is unchanged by stripLeadingComments', () => {
  const text = 'a,b\n1,2\n';
  const stripped = stripLeadingComments(text);
  assert.equal(stripped.text, text);
  assert.equal(stripped.skipped, 0);
  assert.equal(stripped.delimiter, ',');
  assert.equal(parseCSV(text).skippedLines, 0);
});

test('example CSVs whose first line starts with # skip that comment block', () => {
  const dir = path.join(__dirname, '..', '..', 'skills', 'what-is-the-data-saying', 'examples', 'data');
  const names = fs.readdirSync(dir).filter((name) => name.endsWith('.csv')).sort();
  let seen = 0;
  for (const name of names) {
    const text = fs.readFileSync(path.join(dir, name), 'utf8');
    if (!text.split(/\r\n|\n|\r/, 1)[0].startsWith('#')) continue;
    seen += 1;
    const r = parseCSV(text);
    assert.ok(r.headers.every((h) => !h.startsWith('#')), name + ': ' + JSON.stringify(r.headers));
    assert.ok(r.skippedLines >= 1, name);
    assert.ok(r.warnings.some((w) => w.startsWith('comments:')), name + ': ' + JSON.stringify(r.warnings));
  }
  assert.ok(seen >= 1, 'no example CSV starts with #');
});
