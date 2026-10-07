#!/usr/bin/env node
/**
 * Rebuild small ingest fixtures under web/tests/fixtures/.
 *   node web/tests/fixtures/generate.mjs
 */
import { createRequire } from 'node:module';
import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const require = createRequire(import.meta.url);
const XLSX = require('../../vendor/xlsx.full.min.js');
const here = dirname(fileURLToPath(import.meta.url));
mkdirSync(here, { recursive: true });

function writeWorkbook(path, bookType) {
  const wb = XLSX.utils.book_new();
  const sales = [
    ['date', 'product', 'value'],
    [new Date(Date.UTC(2026, 9, 7)), 'tea', 12],
    [new Date(Date.UTC(2026, 9, 8)), 'coffee', 9]
  ];
  const ws1 = XLSX.utils.aoa_to_sheet(sales, { cellDates: true });
  ws1.A2.z = 'yyyy-mm-dd';
  ws1.A3.z = 'yyyy-mm-dd';
  XLSX.utils.book_append_sheet(wb, ws1, '銷售');
  XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet([
    ['year', 'region', 'count'],
    [2024, '北', 100],
    [2025, '南', 80]
  ]), '人口');
  const out = XLSX.write(wb, { bookType: bookType, type: 'buffer' });
  writeFileSync(path, out);
}

writeWorkbook(join(here, 'dates-multisheet.xlsx'), 'xlsx');
writeWorkbook(join(here, 'dates-multisheet.xls'), 'xls');
writeWorkbook(join(here, 'dates-multisheet.ods'), 'ods');

writeFileSync(join(here, 'semicolon.csv'), 'city;temp;rain\nTaipei;28;0.2\nKaohsiung;30;1.1\n', 'utf8');

const big5Text = '產品,數量\n茶葉,3\n咖啡,5\n';
const py = spawnSync('python3', ['-c', 'import sys; sys.stdout.buffer.write(sys.stdin.read().encode("big5"))'], {
  input: Buffer.from(big5Text, 'utf8')
});
if (py.status !== 0) throw new Error(String(py.stderr || py.error));
writeFileSync(join(here, 'big5.csv'), py.stdout);

const nested = [
  { name: 'A', meta: { city: 'Taipei' }, stats: { score: 10 } },
  { name: 'B', meta: { city: 'Tainan' }, stats: { score: 8 } }
];
writeFileSync(join(here, 'nested.json'), JSON.stringify(nested, null, 2) + '\n');
writeFileSync(join(here, 'wrapped.json'), JSON.stringify({ data: nested }, null, 2) + '\n');

console.log('wrote fixtures in', here);
