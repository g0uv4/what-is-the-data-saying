#!/usr/bin/env node
/*
 * Build web/data/content.js and web/data/samples.js from the skill's examples.
 *   node web/build/build-content.mjs
 * Output is deterministic (sorted, no timestamps) so re-running without source
 * changes produces no git diff.
 */
import { readFileSync, readdirSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const webDir = resolve(here, '..');
const repo = resolve(webDir, '..');
const skill = join(repo, 'skills', 'what-is-the-data-saying');
const exDir = join(skill, 'examples');
const dataDir = join(exDir, 'data');
const outDir = join(webDir, 'data');
mkdirSync(outDir, { recursive: true });

const read = (p) => readFileSync(p, 'utf8').replace(/^\uFEFF/, '').replace(/\r\n?/g, '\n');
const plugin = JSON.parse(read(join(repo, '.grok-plugin', 'plugin.json')));

// Pattern name map from examples/README.md table: | 中文 | `file.md` | source |
const readme = read(join(exDir, 'README.md'));
const tableNames = {};
for (const line of readme.split('\n')) {
  const m = /^\|\s*([^|]+?)\s*\|\s*`([\w-]+)\.md`\s*\|/.exec(line);
  if (m) tableNames[m[2]] = m[1];
}

const patterns = {};
for (const f of readdirSync(exDir).filter((f) => f.endsWith('.md') && f !== 'README.md').sort()) {
  const slug = f.slice(0, -3);
  const md = read(join(exDir, f));
  const chart = (/^>\s*\*\*圖種\*\*：(.+)$/m.exec(md) || [])[1] || '';
  const whenBlock = (/## When\n([\s\S]*?)\n## /.exec(md) || [])[1] || '';
  const shape = (/形狀：(.+)$/m.exec(whenBlock) || [])[1] || '';
  patterns[slug] = { slug, file: `examples/${f}`, name: tableNames[slug] || slug, chart: chart.trim(), shape: shape.trim(), md };
}

// Sample descriptions from examples/data/README.md table
const dataReadme = read(join(dataDir, 'README.md'));
const sampleDesc = {};
for (const line of dataReadme.split('\n')) {
  const m = /^\|\s*`([^`]+\.csv)`\s*\|\s*([^|]+?)\s*\|/.exec(line);
  if (m) sampleDesc[m[1]] = m[2];
}
// Which pattern each sample demonstrates (and which renderer to verify it with)
const samplePattern = {
  'dot-density-one-to-many.csv': 'dot-density-map',
  'dot-density-one-to-one.csv': 'dot-density-map',
  'lollipop-categories.csv': 'lollipop-rank',
  'population-pyramid-long.csv': 'population-pyramid',
  'population-pyramid-wide.csv': 'population-pyramid',
  'sample-biofabric.csv': 'biofabric',
  'sample-boxplot.csv': 'boxplot-summary',
  'sample-bubble.csv': 'bubble-chart',
  'sample-choropleth.csv': 'choropleth-map',
  'sample-heatmap.csv': 'matrix-heatmap',
  'sample-marimekko.csv': 'marimekko-chart',
  'sample-spiral.csv': 'spiral-plot',
  'sample-tilemap.csv': 'tile-map',
  'streamgraph-categories.csv': 'streamgraph-composition',
  'streamgraph-wide.csv': 'streamgraph-composition',
  // --- new patterns (v0.3.12–0.3.31); teaching-step CSVs map to parent slug ---
  'sample-ba-fictional.csv': 'bland-altman',
  'sample-circos-sectors.csv': 'circos',
  'sample-circos-links.csv': 'circos',
  'sample-circos-track.csv': 'circos',
  'sample-volcano-de-results.csv': 'volcano-plot',
  'sample-manhattan-gwas.csv': 'manhattan-plot',
  'sample-ma-fictional.csv': 'ma-plot',
  'sample-qq-fictional.csv': 'qq-plot',
  'sample-pp-fictional.csv': 'pp-plot',
  'sample-locuszoom-fictional.csv': 'locuszoom',
  'sample-karyotype-fictional.csv': 'karyotype-ideogram',
  'sample-forest-fictional.csv': 'forest-plot',
  'sample-horizon-fictional.csv': 'horizon-chart',
  'sample-pareto-fictional.csv': 'pareto-chart',
  'sample-s1-anatomy.csv': 'control-chart',
  'sample-s2-out-of-control.csv': 'control-chart',
  'sample-s3-run-same-side.csv': 'control-chart',
  'sample-s4-trend.csv': 'control-chart',
  'sample-s5-xbar-r.csv': 'control-chart',
  'sample-s6-spec-vs-control.csv': 'control-chart',
  'sample-s7-misread-specs.csv': 'control-chart',
  'sample-s8-before-after.csv': 'control-chart',
  'sample-lorenz-s1-anatomy.csv': 'lorenz-curve',
  'sample-lorenz-s2-equal-vs-unequal.csv': 'lorenz-curve',
  'sample-lorenz-s3-gini-area.csv': 'lorenz-curve',
  'sample-lorenz-s4-steps.csv': 'lorenz-curve',
  'sample-lorenz-s5-extremes.csv': 'lorenz-curve',
  'sample-lorenz-s6-misread-pareto.csv': 'lorenz-curve',
  'sample-lorenz-s7-same-shape.csv': 'lorenz-curve',
  'sample-lorenz-s8-two-groups.csv': 'lorenz-curve',
  'sample-marey-s1-anatomy.csv': 'marey-chart',
  'sample-marey-s2-local-vs-express.csv': 'marey-chart',
  'sample-marey-s3-single-track-meet.csv': 'marey-chart',
  'sample-marey-s4-plan-vs-actual.csv': 'marey-chart',
  'sample-marey-s5-bus-bunching.csv': 'marey-chart',
  'sample-marey-s6-misread-equal-spacing.csv': 'marey-chart',
  'sample-marey-s7-too-dense-zoom.csv': 'marey-chart',
  'sample-marey-s8-steps.csv': 'marey-chart',
  'sample-km-s1-anatomy.csv': 'kaplan-meier-survival',
  'sample-km-s2-two-groups.csv': 'kaplan-meier-survival',
  'sample-km-s3-censoring.csv': 'kaplan-meier-survival',
  'sample-km-s4-confidence-band.csv': 'kaplan-meier-survival',
  'sample-km-s5-tail.csv': 'kaplan-meier-survival',
  'sample-km-s6-crossing.csv': 'kaplan-meier-survival',
  'sample-km-s7-y-axis.csv': 'kaplan-meier-survival',
  'sample-km-s8-step-by-step.csv': 'kaplan-meier-survival',
  'sample-swimmer-s1-anatomy.csv': 'swimmer-plot',
  'sample-swimmer-s2-grouped-color.csv': 'swimmer-plot',
  'sample-swimmer-s3-sorting.csv': 'swimmer-plot',
  'sample-swimmer-s4-duration-of-response.csv': 'swimmer-plot',
  'sample-swimmer-s5-stop-reasons.csv': 'swimmer-plot',
  'sample-swimmer-s6-cutoff-misread.csv': 'swimmer-plot',
  'sample-swimmer-s7-too-many-vs-km.csv': 'swimmer-plot',
  'sample-swimmer-s8-steps.csv': 'swimmer-plot',
  'sample-lasagna-s1-anatomy.csv': 'lasagna-plot',
  'sample-lasagna-s2-spaghetti-vs-lasagna.csv': 'lasagna-plot',
  'sample-lasagna-s3-sorting.csv': 'lasagna-plot',
  'sample-lasagna-s4-categorical.csv': 'lasagna-plot',
  'sample-lasagna-s5-missing.csv': 'lasagna-plot',
  'sample-lasagna-s6-colormap.csv': 'lasagna-plot',
  'sample-lasagna-s7-groups-mean.csv': 'lasagna-plot',
  'sample-lasagna-s8-steps.csv': 'lasagna-plot',
  'sample-recurrence-s1-anatomy.csv': 'recurrence-plot',
  'sample-recurrence-s2-four-textures.csv': 'recurrence-plot',
  'sample-recurrence-s3-threshold.csv': 'recurrence-plot',
  'sample-recurrence-s4-embedding.csv': 'recurrence-plot',
  'sample-recurrence-s5-period-spacing.csv': 'recurrence-plot',
  'sample-recurrence-s6-stuck-block.csv': 'recurrence-plot',
  'sample-recurrence-s7-cross-recurrence.csv': 'recurrence-plot',
  'sample-recurrence-s8-steps.csv': 'recurrence-plot'
};

const samples = readdirSync(dataDir).filter((f) => f.endsWith('.csv')).sort().map((f) => ({
  file: f,
  path: `skills/what-is-the-data-saying/examples/data/${f}`,
  desc: sampleDesc[f] || '',
  pattern: samplePattern[f] || null,
  text: read(join(dataDir, f))
}));

const banner = (what) => `/* AUTO-GENERATED by web/build/build-content.mjs — do not edit.\n * Source: skills/what-is-the-data-saying/${what}\n * Plugin version: ${plugin.version}\n */\n`;

const content = {
  version: plugin.version,
  patternCount: Object.keys(patterns).length,
  readme,
  patterns
};
writeFileSync(join(outDir, 'content.js'), banner('examples/*.md') + 'window.WIDS_CONTENT = ' + JSON.stringify(content, null, 1) + ';\n');
writeFileSync(join(outDir, 'samples.js'), banner('examples/data/*.csv') + 'window.WIDS_SAMPLES = ' + JSON.stringify(samples, null, 1) + ';\n');
console.log(`content.js: ${content.patternCount} patterns; samples.js: ${samples.length} CSVs (v${plugin.version})`);
