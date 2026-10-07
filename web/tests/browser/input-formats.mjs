#!/usr/bin/env node
/*
 * Optional headless check: file:// upload of Excel / JSON / Big5 / semicolon CSV.
 *   PLAYWRIGHT_CORE=/tmp/pw/node_modules/playwright-core CHROME=/usr/bin/google-chrome \
 *     node web/tests/browser/input-formats.mjs [outDir]
 */
import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
const pw = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const here = dirname(fileURLToPath(import.meta.url));
const webRoot = resolve(here, '..', '..');
const indexUrl = pathToFileURL(resolve(webRoot, 'index.html')).href;
const fixtures = resolve(webRoot, 'tests', 'fixtures');
const outDir = resolve(process.argv[2] || 'wids-input-shots');
mkdirSync(outDir, { recursive: true });

const browser = await pw.chromium.launch({
  executablePath: process.env.CHROME || '/usr/bin/google-chrome',
  headless: true,
  args: ['--allow-file-access-from-files=false']
});
const errors = [];
const requests = [];
const results = [];

async function expectChart(page, name) {
  await page.waitForSelector('#recList li:first-child .rec-name', { timeout: 8000 });
  const rec = await page.textContent('#recList li:first-child .rec-name');
  const status = await page.textContent('#dataStatus');
  const canvas = await page.$('#chartHost .chart-inner canvas');
  if (!rec) errors.push(`[${name}] no recommendation`);
  results.push({ name, rec, status, canvas: !!canvas });
  await page.locator('#dataCard').screenshot({ path: `${outDir}/${name}.png` });
}

try {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const page = await ctx.newPage();
  page.on('console', (m) => { if (m.type() === 'error') errors.push(`[console] ${m.text()}`); });
  page.on('pageerror', (e) => errors.push('[pageerror] ' + e.message));
  page.on('request', (req) => {
    const url = req.url();
    requests.push(url);
    if (/8787|\/v1\//.test(url)) errors.push('[network] file:// called API ' + url);
  });

  await page.goto(indexUrl);
  await page.setInputFiles('#fileInput', resolve(fixtures, 'dates-multisheet.xlsx'));
  await expectChart(page, 'xlsx-sales');
  const sheetVisible = await page.isVisible('#sheetSelect');
  const sheetOpts = await page.$$eval('#sheetSelect option', (opts) => opts.map((o) => o.value));
  results.push({ name: 'sheet-dropdown', visible: sheetVisible, options: sheetOpts });
  if (!sheetVisible) errors.push('sheet dropdown hidden for multi-sheet xlsx');
  if (sheetOpts.join() !== '銷售,人口') errors.push('sheet options: ' + sheetOpts.join());
  await page.selectOption('#sheetSelect', '人口');
  await page.waitForFunction(() => document.querySelector('#dataStatus')?.textContent.includes('人口'));
  await expectChart(page, 'xlsx-sheet2');

  await page.setInputFiles('#fileInput', resolve(fixtures, 'nested.json'));
  await expectChart(page, 'json-nested');
  const cols = await page.$$eval('#preview th', (ths) => ths.map((th) => th.textContent));
  if (!cols.includes('meta.city')) errors.push('nested JSON did not flatten meta.city: ' + cols.join());

  await page.setInputFiles('#fileInput', resolve(fixtures, 'big5.csv'));
  await expectChart(page, 'csv-big5');
  const big5Status = await page.textContent('#dataStatus');
  if (!/產品|BIG5|茶葉/.test(big5Status + (await page.textContent('#preview')))) {
    errors.push('Big5 CSV did not show Chinese headers');
  }

  await page.setInputFiles('#fileInput', resolve(fixtures, 'semicolon.csv'));
  await expectChart(page, 'csv-semicolon');

  await page.goto(indexUrl);
  await page.click('#pasteBox summary');
  await page.fill('#pasteArea', JSON.stringify({ data: [{ name: 'X', meta: { city: 'Keelung' } }] }));
  await page.click('#parseBtn');
  await expectChart(page, 'paste-json');
  const pasteCols = await page.$$eval('#preview th', (ths) => ths.map((th) => th.textContent));
  if (!pasteCols.includes('meta.city')) errors.push('paste JSON did not flatten: ' + pasteCols.join());

  results.push({ name: 'file-protocol-requests', requests });
} finally {
  await browser.close();
}

console.log(JSON.stringify(results, null, 2));
if (errors.length) {
  console.error('ERRORS:\n' + errors.join('\n'));
  process.exit(1);
}
console.log('OK — uploads rendered recommendations; file:// made no API calls.');
