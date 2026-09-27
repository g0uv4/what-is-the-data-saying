#!/usr/bin/env node
/*
 * Optional headless smoke test: opens web/index.html via file://, loads sample
 * CSVs, renders each supported chart, saves screenshots and fails on any
 * console error / page error.
 *
 *   npm i --no-save playwright-core     # anywhere on NODE_PATH, or set PLAYWRIGHT_CORE
 *   CHROME=/usr/bin/google-chrome node web/tests/browser/smoke.mjs [outDir]
 */
import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
const pw = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const here = dirname(fileURLToPath(import.meta.url));
const indexUrl = pathToFileURL(resolve(here, '..', '..', 'index.html')).href;
const outDir = resolve(process.argv[2] || 'wids-web-shots');
mkdirSync(outDir, { recursive: true });

const cases = [
  { name: '01-line-spiral', sample: 'sample-spiral.csv', pattern: 'time-series-trend', expect: 'canvas' },
  { name: '02-line-multiseries', sample: 'streamgraph-categories.csv', pattern: 'time-series-trend', expect: 'canvas' },
  { name: '03-line-wide', sample: 'streamgraph-wide.csv', pattern: 'time-series-trend', expect: 'canvas' },
  { name: '04-bar-sorted-lollipop', sample: 'lollipop-categories.csv', pattern: 'lollipop-rank', expect: 'canvas' },
  { name: '05-bar-sorted-choropleth', sample: 'sample-choropleth.csv', pattern: 'categorical-comparison', expect: 'canvas' },
  { name: '06-bar-grouped-marimekko', sample: 'sample-marimekko.csv', pattern: 'categorical-comparison', renderer: 'barGrouped', expect: 'canvas' },
  { name: '07-scatter-bubble', sample: 'sample-bubble.csv', pattern: 'bubble-chart', expect: 'canvas' },
  { name: '08-histogram', sample: 'sample-boxplot.csv', pattern: 'boxplot-summary', renderer: 'histogram', expect: 'canvas' },
  { name: '09-boxplot', sample: 'sample-boxplot.csv', pattern: 'boxplot-summary', expect: 'canvas' },
  { name: '10-heatmap', sample: 'sample-heatmap.csv', pattern: 'matrix-heatmap', expect: 'canvas' },
  { name: '11-pyramid-long', sample: 'population-pyramid-long.csv', pattern: 'population-pyramid', expect: 'canvas' },
  { name: '12-pyramid-wide', sample: 'population-pyramid-wide.csv', pattern: 'population-pyramid', expect: 'canvas' },
  { name: '13-adjacency-biofabric', sample: 'sample-biofabric.csv', pattern: 'adjacency-matrix', expect: 'canvas' },
  { name: '14-teach-only-biofabric', sample: 'sample-biofabric.csv', pattern: 'biofabric', expect: 'notice' },
  { name: '15-english', sample: 'sample-heatmap.csv', pattern: 'matrix-heatmap', lang: 'en', expect: 'canvas' }
];

const browser = await pw.chromium.launch({ executablePath: process.env.CHROME || '/usr/bin/google-chrome', headless: true, args: ['--allow-file-access-from-files=false'] });
const errors = [];
const results = [];
try {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  page.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') errors.push(`[${m.type()}] ${m.text()}`); });
  page.on('pageerror', (e) => errors.push('[pageerror] ' + e.message));

  // 1) Real UI flow: pick sample from the <select>
  await page.goto(indexUrl);
  await page.selectOption('#sampleSelect', 'sample-heatmap.csv');
  await page.waitForSelector('#chartHost canvas');
  const top = await page.textContent('#recList li:first-child .rec-name');
  results.push({ name: '00-ui-select', top });
  await page.screenshot({ path: `${outDir}/00-ui-select-heatmap-full.png`, fullPage: true });
  // manual type override → recommendations recompute
  await page.selectOption('#columns tbody tr:nth-child(2) select', 'id');
  await page.waitForTimeout(200);
  const topAfter = await page.textContent('#recList li:first-child .rec-name');
  results.push({ name: '00-type-override', before: top, after: topAfter });
  if (top === topAfter) errors.push('type override did not change top recommendation');
  // internal pattern link inside tutorial markdown
  await page.selectOption('#columns tbody tr:nth-child(2) select', 'category');
  const link = await page.$('#tutorial a.md-internal');
  if (link) { const target = await link.getAttribute('data-pattern'); await link.click(); await page.waitForTimeout(200); results.push({ name: '00-internal-link', target, tutorial: await page.textContent('#tutorial h1') }); }

  // 2) Each renderer via hash deep-link
  for (const c of cases) {
    const hash = `#sample=${encodeURIComponent(c.sample)}&pattern=${c.pattern}` + (c.renderer ? `&renderer=${c.renderer}` : '') + (c.lang ? `&lang=${c.lang}` : '');
    await page.goto('about:blank');
    await page.goto(indexUrl + hash);
    if (c.expect === 'canvas') await page.waitForSelector('#chartHost .chart-inner canvas', { timeout: 5000 });
    else await page.waitForSelector('#chartHead .notice', { timeout: 5000 });
    await page.waitForTimeout(400);
    const err = await page.$('#chartHost .notice.error');
    if (err) errors.push(`[${c.name}] draw error: ${await err.textContent()}`);
    const canvas = await page.$('#chartHost .chart-inner canvas');
    if (canvas) {
      const box = await canvas.boundingBox();
      // hover somewhere inside the plot to exercise tooltips
      await page.mouse.move(box.x + box.width * 0.55, box.y + box.height * 0.5);
      await page.waitForTimeout(250);
    }
    const tutH1 = await page.textContent('#tutorial h1').catch(() => null);
    await page.locator('#chartCard').screenshot({ path: `${outDir}/${c.name}.png` });
    results.push({ name: c.name, tutorial: tutH1 });
  }

  // 3) Paste flow with quotes, embedded comma, CRLF and BOM
  await page.goto(indexUrl);
  await page.click('#pasteBox summary');
  await page.fill('#pasteArea', '\uFEFFname,"note, with comma",value\r\n"A ""quoted""",x,3\r\nB,"multi\nline",5\r\n');
  await page.click('#parseBtn');
  await page.waitForSelector('#columns table');
  results.push({ name: 'paste', status: await page.textContent('#dataStatus') });
  await page.screenshot({ path: `${outDir}/16-paste-flow.png`, fullPage: false });

  // 4) Mobile layout
  await page.setViewportSize({ width: 390, height: 900 });
  await page.goto(indexUrl + '#sample=lollipop-categories.csv&pattern=lollipop-rank');
  await page.waitForSelector('#chartHost .chart-inner canvas');
  await page.screenshot({ path: `${outDir}/17-mobile.png`, fullPage: true });
} finally {
  await browser.close();
}
console.log(JSON.stringify(results, null, 1));
if (errors.length) { console.error('ERRORS:\n' + errors.join('\n')); process.exit(1); }
console.log(`OK — no console errors. Screenshots in ${outDir}`);
