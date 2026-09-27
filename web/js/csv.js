/*
 * WIDS CSV parser — RFC 4180-ish, no dependencies.
 * Handles: UTF-8 BOM, quoted fields, delimiters / newlines inside quotes,
 * escaped quotes (""), CRLF / LF / CR line endings, trailing newline,
 * ragged rows (padded / truncated to header length), delimiter sniffing
 * (comma, semicolon, tab).
 * Works in browsers (window.WIDS_CSV) and Node (module.exports).
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.WIDS_CSV = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  function stripBOM(text) {
    return text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;
  }

  /** Guess delimiter from the first logical line (outside quotes). */
  function sniffDelimiter(text) {
    var counts = { ',': 0, ';': 0, '\t': 0 };
    var inQ = false;
    for (var i = 0; i < text.length && i < 20000; i++) {
      var c = text[i];
      if (c === '"') inQ = !inQ;
      else if (!inQ && (c === '\n' || c === '\r')) break;
      else if (!inQ && counts.hasOwnProperty(c)) counts[c]++;
    }
    var best = ',';
    if (counts['\t'] > counts[best]) best = '\t';
    if (counts[';'] > counts[best]) best = ';';
    return best;
  }

  /** Tokenise into array of rows (arrays of strings). */
  function parseRows(text, delimiter) {
    text = stripBOM(String(text == null ? '' : text));
    var d = delimiter || sniffDelimiter(text);
    var rows = [];
    var row = [];
    var field = '';
    var inQuotes = false;
    var fieldStarted = false; // distinguishes "" (empty quoted) from nothing
    var i = 0;
    var n = text.length;
    while (i < n) {
      var c = text[i];
      if (inQuotes) {
        if (c === '"') {
          if (text[i + 1] === '"') { field += '"'; i += 2; continue; }
          inQuotes = false; i++; continue;
        }
        field += c; i++; continue;
      }
      if (c === '"' && !fieldStarted && field === '') {
        inQuotes = true; fieldStarted = true; i++; continue;
      }
      if (c === d) {
        row.push(field); field = ''; fieldStarted = false; i++; continue;
      }
      if (c === '\r' || c === '\n') {
        row.push(field); field = ''; fieldStarted = false;
        rows.push(row); row = [];
        if (c === '\r' && text[i + 1] === '\n') i += 2; else i++;
        continue;
      }
      field += c; fieldStarted = true; i++;
    }
    if (field !== '' || fieldStarted || row.length) { row.push(field); rows.push(row); }
    // drop fully blank lines
    return rows.filter(function (r) { return !(r.length === 1 && r[0].trim() === ''); });
  }

  /**
   * Parse CSV text with a header row.
   * @returns {{headers:string[], rows:string[][], delimiter:string, warnings:string[]}}
   */
  function parseCSV(text, opts) {
    opts = opts || {};
    var clean = stripBOM(String(text == null ? '' : text));
    var delimiter = opts.delimiter || sniffDelimiter(clean);
    var all = parseRows(clean, delimiter);
    var warnings = [];
    if (!all.length) return { headers: [], rows: [], delimiter: delimiter, warnings: ['empty'] };
    var headers = all[0].map(function (h, idx) {
      h = String(h).trim();
      return h === '' ? 'col_' + (idx + 1) : h;
    });
    // de-duplicate header names
    var seen = {};
    headers = headers.map(function (h) {
      if (!seen[h]) { seen[h] = 1; return h; }
      seen[h]++; return h + '_' + seen[h];
    });
    var ragged = 0;
    var rows = all.slice(1).map(function (r) {
      if (r.length !== headers.length) ragged++;
      var out = r.slice(0, headers.length);
      while (out.length < headers.length) out.push('');
      return out;
    });
    if (ragged) warnings.push('ragged:' + ragged);
    return { headers: headers, rows: rows, delimiter: delimiter, warnings: warnings };
  }

  return { parseCSV: parseCSV, parseRows: parseRows, sniffDelimiter: sniffDelimiter, stripBOM: stripBOM };
});
