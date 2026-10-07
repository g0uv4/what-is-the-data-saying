'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const web = path.join(__dirname, '..');

test('index.html links favicon.svg inside head', () => {
  const html = fs.readFileSync(path.join(web, 'index.html'), 'utf8');
  const headStart = html.indexOf('<head>');
  const headEnd = html.indexOf('</head>');
  assert.ok(headStart >= 0 && headEnd > headStart);
  const head = html.slice(headStart, headEnd);
  assert.match(head, /<link rel="icon" href="favicon\.svg">/);
});

test('favicon.svg is a local geometric icon', () => {
  const svgPath = path.join(web, 'favicon.svg');
  assert.ok(fs.existsSync(svgPath));
  const svg = fs.readFileSync(svgPath, 'utf8');
  assert.match(svg, /<svg\b/);
  assert.match(svg, /\bviewBox\s*=/);
  assert.doesNotMatch(svg, /<text\b/i);
  assert.doesNotMatch(svg, /<image\b/i);
  assert.doesNotMatch(svg, /<script\b/i);
  assert.doesNotMatch(svg, /href\s*=/i);
  const withoutNs = svg.split('xmlns="http://www.w3.org/2000/svg"').join('');
  assert.equal(withoutNs.includes('http'), false);
});

test('favicon.ico has an ICO header and three images', () => {
  const icoPath = path.join(web, 'favicon.ico');
  assert.ok(fs.existsSync(icoPath));
  const ico = fs.readFileSync(icoPath);
  assert.ok(ico.length >= 6);
  assert.deepEqual([...ico.subarray(0, 4)], [0x00, 0x00, 0x01, 0x00]);
  assert.equal(ico.readUInt16LE(4), 3);
});
