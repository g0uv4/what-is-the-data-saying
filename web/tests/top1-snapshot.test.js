'use strict';
/**
 * #1 eligible pattern for every sample-*.csv.
 * Search: repo-root recursive sample-*.csv (skip node_modules and .git).
 * 78 original files + 8 spectrogram teaching CSVs + 8 autocorrelation teaching CSVs = 94 total.
 * The 78-file set was first captured at web-poc 3222d7b; values were
 * re-captured after parseCSV began skipping leading `#` comment lines
 * (the old values reflected comment text parsed as the header).
 * All currently live in skills/what-is-the-data-saying/examples/data/.
 * The four demo fixtures under tests/fixtures/demos/ are not sample-*.csv.
 * The 8 spectrogram files are web/build/sample-exclude.json: not embedded in
 * samples.js, but still scored here (top1-snapshot-spectrogram.json).
 * Those eight values were re-captured the same way.
 * Values were re-captured again after the recommender began treating
 * even-step integer columns as an order axis and id columns as non-categories.
 * Four values were re-captured after the Lorenz rule began requiring named
 * units (one row per category or category × unit cells) and at least 10 units per curve.
 * The 8 autocorrelation teaching CSVs (v0.3.33) are also in sample-exclude.json,
 * not embedded in samples.js, and their #1 (none is autocorrelation-plot, which
 * is teaching-only) is captured in top1-snapshot-autocorr.json; the 78-file and
 * spectrogram values did not change.
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
const autocorrSnapshotPath = path.join(__dirname, 'fixtures', 'top1-snapshot-autocorr.json');
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

test('78-file set (first captured at web-poc 3222d7b; values re-captured after leading # comment lines are skipped) keeps its #1; extras are exactly the 16 excluded teaching files', () => {
  const files = listSampleCsv(repoRoot, []).sort();
  const names = files.map((f) => path.basename(f));
  const byName = new Map(files.map((f) => [path.basename(f), f]));
  const snap = JSON.parse(fs.readFileSync(snapshotPath, 'utf8'));
  const specSnap = JSON.parse(fs.readFileSync(spectrogramSnapshotPath, 'utf8'));
  const autocorrSnap = JSON.parse(fs.readFileSync(autocorrSnapshotPath, 'utf8'));
  const exclude = JSON.parse(fs.readFileSync(excludePath, 'utf8')).slice().sort();
  const specExclude = exclude.filter((n) => n.startsWith('sample-spectrogram-'));
  const autocorrExclude = exclude.filter((n) => n.startsWith('sample-autocorr-'));
  const snapNames = Object.keys(snap).sort();
  assert.equal(new Set(names).size, names.length, 'duplicate sample-*.csv basenames');
  assert.equal(snapNames.length, 78, '3222d7b snapshot should list 78 files');
  assert.equal(exclude.length, 16, 'sample-exclude.json should list the 16 excluded teaching CSVs');
  const missing = snapNames.filter((n) => !byName.has(n));
  assert.deepEqual(missing, [], 'snapshot files missing from tree: ' + missing.join(', '));
  const extra = names.filter((n) => !Object.prototype.hasOwnProperty.call(snap, n)).sort();
  assert.deepEqual(extra, exclude, 'sample-*.csv outside the 3222d7b snapshot must equal the exclusion list (glob ' + SAMPLE_GLOB + ')');
  assert.equal(names.length, 94, '78 original + 8 spectrogram + 8 autocorrelation');
  const flips = [];
  for (const name of snapNames) {
    const got = top1Id(byName.get(name));
    if (got !== snap[name]) flips.push({ file: name, expected: snap[name], got: got });
  }
  assert.deepEqual(flips, [], 'sample #1 flipped vs re-captured snapshot: ' + JSON.stringify(flips));
  assert.deepEqual(Object.keys(specSnap).sort(), specExclude);
  const specFlips = [];
  const excludedTop = new Map();
  for (const name of specExclude) {
    const got = top1Id(byName.get(name));
    excludedTop.set(name, got);
    if (got !== specSnap[name]) specFlips.push({ file: name, expected: specSnap[name], got: got });
  }
  assert.deepEqual(specFlips, [], 'spectrogram sample #1 flipped: ' + JSON.stringify(specFlips));
  assert.deepEqual(Object.keys(autocorrSnap).sort(), autocorrExclude);
  const autocorrFlips = [];
  for (const name of autocorrExclude) {
    const got = top1Id(byName.get(name));
    excludedTop.set(name, got);
    if (got !== autocorrSnap[name]) autocorrFlips.push({ file: name, expected: autocorrSnap[name], got: got });
  }
  assert.deepEqual(autocorrFlips, [], 'autocorr sample #1 flipped: ' + JSON.stringify(autocorrFlips));
  assert.deepEqual(autocorrExclude.concat(specExclude), exclude);
  const acfTop = exclude.filter((name) => excludedTop.get(name) === 'autocorrelation-plot');
  assert.deepEqual(acfTop, [], 'excluded teaching file ranked autocorrelation-plot #1: ' + acfTop.join(', '));
});
