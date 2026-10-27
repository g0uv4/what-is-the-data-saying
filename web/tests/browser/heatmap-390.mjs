#!/usr/bin/env node
/*
 * Regression: the matrix heatmap page must fit a 390px-wide viewport.
 * Behavior only — document scroll width and the heatmap container box.
 *
 *   PLAYWRIGHT_CORE=/tmp/pw/node_modules/playwright-core \
 *   CHROME=/usr/bin/google-chrome node web/tests/browser/heatmap-390.mjs
 */
import { createRequire } from 'node:module';
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
const pw = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const here = dirname(fileURLToPath(import.meta.url));
const indexUrl = pathToFileURL(resolve(here, '..', '..', 'index.html')).href;
const VIEWPORT = 390;

test('matrix heatmap at 390px does not overflow the viewport', async () => {
  const browser = await pw.chromium.launch({
    executablePath: process.env.CHROME || '/usr/bin/google-chrome',
    headless: true,
    args: ['--allow-file-access-from-files=false']
  });
  try {
    const page = await browser.newPage({ viewport: { width: VIEWPORT, height: 900 }, deviceScaleFactor: 1 });
    await page.goto(indexUrl + '#sample=sample-heatmap.csv&pattern=matrix-heatmap', { waitUntil: 'load' });
    await page.waitForSelector('#chartHost .chart-inner canvas', { timeout: 8000 });
    const box = await page.evaluate(() => {
      const chart = document.querySelector('#chartHost .chart-inner');
      const r = chart.getBoundingClientRect();
      return {
        scrollWidth: document.documentElement.scrollWidth,
        innerWidth: window.innerWidth,
        chartLeft: r.left,
        chartRight: r.right
      };
    });
    assert.ok(
      box.scrollWidth <= VIEWPORT,
      'documentElement.scrollWidth ' + box.scrollWidth + ' exceeds viewport ' + VIEWPORT
    );
    assert.ok(box.chartLeft >= -0.5, 'heatmap container left ' + box.chartLeft + ' is outside the viewport');
    assert.ok(
      box.chartRight <= box.innerWidth + 0.5,
      'heatmap container right ' + box.chartRight + ' exceeds viewport ' + box.innerWidth
    );
  } finally {
    await browser.close();
  }
});
