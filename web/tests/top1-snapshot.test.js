'use strict';
/**
 * #1 eligible pattern for every sample-*.csv must match web-poc 3222d7b.
 * Search: repo-root recursive sample-*.csv (skip node_modules and .git).
 * All 78 currently live in skills/what-is-the-data-saying/examples/data/.
 * The four demo fixtures under tests/fixtures/demos/ are not sample-*.csv.
 */
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { parseCSV } = require('../js/csv.js');
const T = require('../js/types.js');
const R = require('../js/rules.js');

const repoRoot = path.join(__dirname, '..', '..');
const snapshotPath = path.join(__dirname, 'fixtures', 'top1-snapshot-3222d7b.json');
const SAMPLE_GLOB = '**/sample-*.csv';

function listSampleCsv(dir, out) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const ent of entries) {
    if (ent.name === 'node_modules' || ent.name === '.git') continue;
    const full = path.join(dir, ent.name);
    if (ent.isDirectory()) listSampleCsv(full, out);
    else if (ent.isFile() && /^sample-.*\.csv$/.test(ent.name)) out.push(full);
  }
  return out;
}

function top1Id(file) {
  const rec = R.recommend(T.profileTable(parseCSV(fs.readFileSync(file, 'utf8'))));
  const first = rec.results.filter((r) => r.eligible)[0];
  return first ? first.id : null;
}

test('all 78 sample-*.csv keep web-poc 3222d7b #1 pattern', () => {
  const files = listSampleCsv(repoRoot, []).sort();
  const snap = JSON.parse(fs.readFileSync(snapshotPath, 'utf8'));
  const names = files.map((f) => path.basename(f));
  assert.equal(files.length, 78, 'glob ' + SAMPLE_GLOB + ' should find 78 files; got ' + names.join(', '));
  assert.deepEqual(names, Object.keys(snap).sort());
  const flips = [];
  for (const file of files) {
    const name = path.basename(file);
    const got = top1Id(file);
    if (got !== snap[name]) flips.push({ file: name, expected: snap[name], got: got });
  }
  assert.deepEqual(flips, [], 'sample #1 flipped vs 3222d7b: ' + JSON.stringify(flips));
});
