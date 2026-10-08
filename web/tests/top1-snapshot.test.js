'use strict';
/**
 * #1 eligible pattern for every sample-*.csv.
 * Search: repo-root recursive sample-*.csv (skip node_modules and .git).
 * 78 original files (web-poc 3222d7b) + 8 spectrogram teaching CSVs = 86 total.
 * All currently live in skills/what-is-the-data-saying/examples/data/.
 * The four demo fixtures under tests/fixtures/demos/ are not sample-*.csv.
 * The 8 spectrogram files are web/build/sample-exclude.json: not embedded in
 * samples.js, but still scored here (top1-snapshot-spectrogram.json).
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
const spectrogramSnapshotPath = path.join(__dirname, 'fixtures', 'top1-snapshot-spectrogram.json');
const excludePath = path.join(__dirname, '..', 'build', 'sample-exclude.json');
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

test('78 original sample-*.csv keep web-poc 3222d7b #1; extras are exactly the 8 excluded spectrogram files', () => {
  const files = listSampleCsv(repoRoot, []).sort();
  const names = files.map((f) => path.basename(f));
  const byName = new Map(files.map((f) => [path.basename(f), f]));
  const snap = JSON.parse(fs.readFileSync(snapshotPath, 'utf8'));
  const specSnap = JSON.parse(fs.readFileSync(spectrogramSnapshotPath, 'utf8'));
  const exclude = JSON.parse(fs.readFileSync(excludePath, 'utf8')).slice().sort();
  const snapNames = Object.keys(snap).sort();
  assert.equal(new Set(names).size, names.length, 'duplicate sample-*.csv basenames');
  assert.equal(snapNames.length, 78, '3222d7b snapshot should list 78 files');
  assert.equal(exclude.length, 8, 'sample-exclude.json should list the 8 spectrogram CSVs');
  const missing = snapNames.filter((n) => !byName.has(n));
  assert.deepEqual(missing, [], 'snapshot files missing from tree: ' + missing.join(', '));
  const extra = names.filter((n) => !Object.prototype.hasOwnProperty.call(snap, n)).sort();
  assert.deepEqual(extra, exclude, 'sample-*.csv outside the 3222d7b snapshot must equal the exclusion list (glob ' + SAMPLE_GLOB + ')');
  assert.equal(names.length, 86, '78 original + 8 spectrogram');
  const flips = [];
  for (const name of snapNames) {
    const got = top1Id(byName.get(name));
    if (got !== snap[name]) flips.push({ file: name, expected: snap[name], got: got });
  }
  assert.deepEqual(flips, [], 'sample #1 flipped vs 3222d7b: ' + JSON.stringify(flips));
  assert.deepEqual(Object.keys(specSnap).sort(), exclude);
  const specFlips = [];
  for (const name of exclude) {
    const got = top1Id(byName.get(name));
    if (got !== specSnap[name]) specFlips.push({ file: name, expected: specSnap[name], got: got });
  }
  assert.deepEqual(specFlips, [], 'spectrogram sample #1 flipped: ' + JSON.stringify(specFlips));
});
