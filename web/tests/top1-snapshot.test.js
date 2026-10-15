'use strict';
/**
 * #1 eligible pattern for every sample-*.csv.
 * Search: repo-root recursive sample-*.csv (skip node_modules and .git).
 * 78 original files + 8 spectrogram teaching CSVs + 8 autocorrelation teaching CSVs + 8 lag plot teaching CSVs + 9 seasonal subseries teaching CSVs + 5 seasonal decomposition teaching CSVs = 116 total.
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
 * The 8 lag plot teaching CSVs (v0.3.34) are also excluded, their #1 (none is
 * lag-plot, teaching-only) is captured in top1-snapshot-lagplot.json, and the
 * other three snapshots did not change.
 * The 9 seasonal subseries teaching CSVs (v0.3.35) are also excluded, their #1
 * (none is seasonal-subseries-plot, teaching-only) is in
 * top1-snapshot-seasonal-subseries.json, and the other four snapshots did not change.
 * The 5 seasonal decomposition teaching CSVs (v0.3.36) are also excluded, their #1
 * (none is seasonal-decomposition-plot, teaching-only) is in
 * top1-snapshot-seasonal-decomp.json, and the other five snapshots did not change.
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
const lagplotSnapshotPath = path.join(__dirname, 'fixtures', 'top1-snapshot-lagplot.json');
const seasonalSnapshotPath = path.join(__dirname, 'fixtures', 'top1-snapshot-seasonal-subseries.json');
const decompSnapshotPath = path.join(__dirname, 'fixtures', 'top1-snapshot-seasonal-decomp.json');
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

test('78-file set (first captured at web-poc 3222d7b; values re-captured after leading # comment lines are skipped) keeps its #1; extras are exactly the 38 excluded teaching files', () => {
  const files = listSampleCsv(repoRoot, []).sort();
  const names = files.map((f) => path.basename(f));
  const byName = new Map(files.map((f) => [path.basename(f), f]));
  const snap = JSON.parse(fs.readFileSync(snapshotPath, 'utf8'));
  const specSnap = JSON.parse(fs.readFileSync(spectrogramSnapshotPath, 'utf8'));
  const autocorrSnap = JSON.parse(fs.readFileSync(autocorrSnapshotPath, 'utf8'));
  const lagplotSnap = JSON.parse(fs.readFileSync(lagplotSnapshotPath, 'utf8'));
  const seasonalSnap = JSON.parse(fs.readFileSync(seasonalSnapshotPath, 'utf8'));
  const decompSnap = JSON.parse(fs.readFileSync(decompSnapshotPath, 'utf8'));
  const exclude = JSON.parse(fs.readFileSync(excludePath, 'utf8')).slice().sort();
  const specExclude = exclude.filter((n) => n.startsWith('sample-spectrogram-'));
  const autocorrExclude = exclude.filter((n) => n.startsWith('sample-autocorr-'));
  const lagplotExclude = exclude.filter((n) => n.startsWith('sample-lagplot-'));
  const seasonalExclude = exclude.filter((n) => n.startsWith('sample-seasonal-subseries-'));
  const decompExclude = exclude.filter((n) => n.startsWith('sample-seasonal-decomp-'));
  const snapNames = Object.keys(snap).sort();
  assert.equal(new Set(names).size, names.length, 'duplicate sample-*.csv basenames');
  assert.equal(snapNames.length, 78, '3222d7b snapshot should list 78 files');
  assert.equal(exclude.length, 38, 'sample-exclude.json should list the 38 excluded teaching CSVs');
  const missing = snapNames.filter((n) => !byName.has(n));
  assert.deepEqual(missing, [], 'snapshot files missing from tree: ' + missing.join(', '));
  const extra = names.filter((n) => !Object.prototype.hasOwnProperty.call(snap, n)).sort();
  assert.deepEqual(extra, exclude, 'sample-*.csv outside the 3222d7b snapshot must equal the exclusion list (glob ' + SAMPLE_GLOB + ')');
  assert.equal(names.length, 116, '78 original + 8 spectrogram + 8 autocorrelation + 8 lag plot + 9 seasonal subseries + 5 seasonal decomposition');
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
  assert.deepEqual(Object.keys(lagplotSnap).sort(), lagplotExclude);
  const lagplotFlips = [];
  for (const name of lagplotExclude) {
    const got = top1Id(byName.get(name));
    excludedTop.set(name, got);
    if (got !== lagplotSnap[name]) lagplotFlips.push({ file: name, expected: lagplotSnap[name], got: got });
  }
  assert.deepEqual(lagplotFlips, [], 'lagplot sample #1 flipped: ' + JSON.stringify(lagplotFlips));
  assert.deepEqual(Object.keys(seasonalSnap).sort(), seasonalExclude);
  const seasonalFlips = [];
  for (const name of seasonalExclude) {
    const got = top1Id(byName.get(name));
    excludedTop.set(name, got);
    if (got !== seasonalSnap[name]) seasonalFlips.push({ file: name, expected: seasonalSnap[name], got: got });
  }
  assert.deepEqual(seasonalFlips, [], 'seasonal subseries sample #1 flipped: ' + JSON.stringify(seasonalFlips));
  assert.deepEqual(Object.keys(decompSnap).sort(), decompExclude);
  const decompFlips = [];
  for (const name of decompExclude) {
    const got = top1Id(byName.get(name));
    excludedTop.set(name, got);
    if (got !== decompSnap[name]) decompFlips.push({ file: name, expected: decompSnap[name], got: got });
  }
  assert.deepEqual(decompFlips, [], 'seasonal decomposition sample #1 flipped: ' + JSON.stringify(decompFlips));
  assert.deepEqual(autocorrExclude.concat(lagplotExclude, decompExclude, seasonalExclude, specExclude), exclude);
  const teachingTop = exclude.filter((name) => {
    const id = excludedTop.get(name);
    return id === 'autocorrelation-plot' || id === 'lag-plot' || id === 'seasonal-subseries-plot' || id === 'seasonal-decomposition-plot';
  });
  assert.deepEqual(teachingTop, [], 'excluded teaching file ranked autocorrelation-plot, lag-plot, seasonal-subseries-plot or seasonal-decomposition-plot #1: ' + teachingTop.join(', '));
});
