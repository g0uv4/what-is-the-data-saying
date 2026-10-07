/*
 * WIDS local file / paste ingest: CSV (UTF-8 then Big5), JSON, Excel/ODS.
 * Converts every format to the same {headers, rows, delimiter, warnings} table
 * as WIDS_CSV.parseCSV. Never uploads the raw file.
 * Works in browsers (window.WIDS_INPUT) and Node (module.exports).
 */
(function (root, factory) {
  var csv, xlsx;
  if (typeof module === 'object' && module.exports) {
    csv = require('./csv.js');
    try { xlsx = require('../vendor/xlsx.full.min.js'); } catch (err) { xlsx = null; }
    module.exports = factory(csv, xlsx);
  } else {
    root.WIDS_INPUT = factory(root.WIDS_CSV, root.XLSX);
  }
})(typeof self !== 'undefined' ? self : this, function (CSV, XLSX) {
  'use strict';

  var MAX_BYTES = 10 * 1024 * 1024;
  var MAX_ROWS = 50000;
  var SPREADSHEET_EXT = { xlsx: 1, xls: 1, ods: 1 };
  var CSV_EXT = { csv: 1, tsv: 1, txt: 1 };
  var UNSUPPORTED_EXT = {
    pdf: 1, parquet: 1, png: 1, jpg: 1, jpeg: 1, gif: 1, webp: 1, html: 1,
    htm: 1, svg: 1, zip: 1, doc: 1, docx: 1, ppt: 1, pptx: 1
  };

  function getXLSX() {
    if (XLSX) return XLSX;
    var g = typeof globalThis !== 'undefined' ? globalThis : (typeof self !== 'undefined' ? self : {});
    if (g.XLSX) return g.XLSX;
    throw new Error('SheetJS is not loaded');
  }

  function toU8(buffer) {
    if (!buffer) return new Uint8Array(0);
    if (buffer instanceof Uint8Array) return buffer;
    if (typeof Buffer !== 'undefined' && Buffer.isBuffer && Buffer.isBuffer(buffer)) {
      return new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength);
    }
    if (buffer instanceof ArrayBuffer) return new Uint8Array(buffer);
    if (ArrayBuffer.isView(buffer)) {
      return new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength);
    }
    throw new Error('expected binary data');
  }

  function extOf(name) {
    var m = /\.([A-Za-z0-9]+)$/.exec(String(name || ''));
    return m ? m[1].toLowerCase() : '';
  }

  function stripBOM(text) {
    return CSV.stripBOM(String(text == null ? '' : text));
  }

  function looksLikeJSON(text) {
    var s = stripBOM(text).replace(/^\uFEFF/, '').replace(/^[\s\u00a0]+/, '');
    return s.charAt(0) === '{' || s.charAt(0) === '[';
  }

  function decodeBytes(buffer) {
    var bytes = toU8(buffer);
    var utfStart = 0;
    if (bytes.length >= 3 && bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf) {
      utfStart = 3;
    }
    try {
      var utf = new TextDecoder('utf-8', { fatal: true }).decode(bytes.subarray(utfStart));
      return { text: stripBOM(utf), encoding: 'utf-8' };
    } catch (err) {
      try {
        var big5 = new TextDecoder('big5').decode(bytes);
        return { text: stripBOM(big5), encoding: 'big5' };
      } catch (err2) {
        throw new Error('could not decode text as UTF-8 or Big5');
      }
    }
  }

  function uniqueHeaders(headers) {
    var seen = {};
    return headers.map(function (h, idx) {
      h = String(h == null ? '' : h).trim();
      if (h === '') h = 'col_' + (idx + 1);
      if (!seen[h]) { seen[h] = 1; return h; }
      seen[h] += 1;
      return h + '_' + seen[h];
    });
  }

  function rowsFromAoa(aoa) {
    var warnings = [];
    var lines = (aoa || []).filter(function (r) {
      return r && r.some(function (c) { return String(c == null ? '' : c).trim() !== ''; });
    });
    if (!lines.length) return { headers: [], rows: [], delimiter: ',', warnings: ['empty'] };
    var headers = uniqueHeaders(lines[0]);
    var ragged = 0;
    var rows = lines.slice(1).map(function (r) {
      if (r.length !== headers.length) ragged += 1;
      var out = r.slice(0, headers.length);
      while (out.length < headers.length) out.push('');
      return out.map(function (c) { return c == null ? '' : String(c); });
    });
    if (ragged) warnings.push('ragged:' + ragged);
    return { headers: headers, rows: rows, delimiter: ',', warnings: warnings };
  }

  function limitRows(parsed) {
    parsed = parsed || { headers: [], rows: [], delimiter: ',', warnings: [] };
    parsed.warnings = parsed.warnings ? parsed.warnings.slice() : [];
    var n = parsed.rows ? parsed.rows.length : 0;
    if (n > MAX_ROWS) {
      parsed.rows = parsed.rows.slice(0, MAX_ROWS);
      parsed.warnings.push('truncated:' + n);
      parsed.truncatedFrom = n;
    }
    return parsed;
  }

  function pad2(n) {
    return n < 10 ? '0' + n : String(n);
  }

  function partsToISO(p) {
    if (!p) return '';
    var date = p.y + '-' + pad2(p.m) + '-' + pad2(p.d);
    if (p.H || p.M || p.S) return date + 'T' + pad2(p.H) + ':' + pad2(p.M) + ':' + pad2(p.S);
    return date;
  }

  function serialToISO(serial) {
    var X = getXLSX();
    if (!X.SSF || typeof X.SSF.parse_date_code !== 'function') return '';
    var parts = X.SSF.parse_date_code(serial);
    return parts ? partsToISO(parts) : '';
  }

  function isDateNumFmt(fmt) {
    if (fmt == null || fmt === '') return false;
    if (typeof fmt === 'number') {
      return (fmt >= 14 && fmt <= 22) || (fmt >= 27 && fmt <= 36) || (fmt >= 45 && fmt <= 47)
        || (fmt >= 50 && fmt <= 58) || fmt === 165 || fmt === 166;
    }
    var s = String(fmt);
    if (!s || /^general$/i.test(s)) return false;
    var unquoted = s.replace(/\\./g, '').replace(/"[^"]*"/g, '').replace(/\[[^\]]*\]/g, '');
    return /[yY]/.test(unquoted) || (/[mM]/.test(unquoted) && /[dD]/.test(unquoted));
  }

  function cellToText(cell) {
    if (!cell) return '';
    if (cell.t === 'z' || cell.t === 'e') return '';
    if (typeof cell.v === 'number' && (cell.t === 'd' || (cell.t === 'n' && isDateNumFmt(cell.z)))) {
      return serialToISO(cell.v);
    }
    if (cell.t === 'd') {
      if (typeof cell.v === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(cell.v.trim())) return cell.v.trim();
      if (cell.w && /^\d{4}-\d{2}-\d{2}$/.test(String(cell.w).trim())) return String(cell.w).trim();
      return '';
    }
    if (cell.t === 'n') {
      if (cell.v == null) return '';
      return String(cell.v);
    }
    if (cell.t === 'b') return cell.v ? 'true' : 'false';
    if (cell.v == null) return '';
    return String(cell.v);
  }

  function sheetToTable(workbook, sheetName) {
    var X = getXLSX();
    var name = sheetName || (workbook.SheetNames && workbook.SheetNames[0]) || '';
    var ws = workbook.Sheets && workbook.Sheets[name];
    if (!ws) return { headers: [], rows: [], delimiter: ',', warnings: ['empty'], sheetName: name };
    var ref = ws['!ref'];
    var aoa = [];
    if (ref) {
      var range = X.utils.decode_range(ref);
      var r, c, row, addr;
      for (r = range.s.r; r <= range.e.r; r++) {
        row = [];
        for (c = range.s.c; c <= range.e.c; c++) {
          addr = X.utils.encode_cell({ r: r, c: c });
          row.push(cellToText(ws[addr]));
        }
        aoa.push(row);
      }
    }
    var table = rowsFromAoa(aoa);
    table.sheetName = name;
    table.sheetNames = workbook.SheetNames ? workbook.SheetNames.slice() : [name];
    table.format = 'xlsx';
    table.delimiter = ',';
    return table;
  }

  function readWorkbook(buffer) {
    var X = getXLSX();
    return X.read(toU8(buffer), { type: 'array', cellDates: false, cellNF: true });
  }

  function flattenValue(value, prefix, out) {
    if (value === null || value === undefined) {
      if (prefix) out[prefix] = '';
      return;
    }
    if (Array.isArray(value)) {
      var allScalar = value.every(function (x) { return x === null || typeof x !== 'object'; });
      if (allScalar) {
        out[prefix] = value.map(function (x) { return x == null ? '' : String(x); }).join(',');
        return;
      }
      value.forEach(function (item, i) {
        flattenValue(item, prefix ? prefix + '.' + i : String(i), out);
      });
      return;
    }
    if (typeof value === 'object') {
      var keys = Object.keys(value);
      if (!keys.length) {
        if (prefix) out[prefix] = '';
        return;
      }
      keys.forEach(function (k) {
        flattenValue(value[k], prefix ? prefix + '.' + k : k, out);
      });
      return;
    }
    out[prefix] = String(value);
  }

  function recordsToTable(records) {
    if (!records || !records.length) {
      return { headers: [], rows: [], delimiter: ',', warnings: ['empty'], format: 'json' };
    }
    if (Array.isArray(records[0]) && records.every(function (r) { return Array.isArray(r); })) {
      var table = rowsFromAoa(records);
      table.format = 'json';
      return table;
    }
    var maps = records.map(function (rec) {
      var obj = rec;
      if (rec === null || typeof rec !== 'object') obj = { value: rec };
      else if (Array.isArray(rec)) {
        obj = {};
        rec.forEach(function (v, i) { obj[String(i)] = v; });
      }
      var flat = {};
      flattenValue(obj, '', flat);
      return flat;
    });
    var seen = {};
    var headers = [];
    maps.forEach(function (m) {
      Object.keys(m).forEach(function (k) {
        if (!k) return;
        if (!seen[k]) { seen[k] = 1; headers.push(k); }
      });
    });
    headers = uniqueHeaders(headers);
    var rows = maps.map(function (m) {
      return headers.map(function (h) { return Object.prototype.hasOwnProperty.call(m, h) ? String(m[h]) : ''; });
    });
    return { headers: headers, rows: rows, delimiter: ',', warnings: [], format: 'json' };
  }

  function extractRecords(value) {
    if (Array.isArray(value)) return value;
    if (value && typeof value === 'object' && Array.isArray(value.data)) return value.data;
    throw new Error('JSON must be an array of objects or {"data":[...]}');
  }

  function parseJSON(text) {
    var clean = stripBOM(text).trim();
    var value;
    try {
      value = JSON.parse(clean);
    } catch (err) {
      throw new Error('invalid JSON');
    }
    return limitRows(recordsToTable(extractRecords(value)));
  }

  function parseCSVBytes(buffer) {
    var dec = decodeBytes(buffer);
    var parsed = CSV.parseCSV(dec.text);
    parsed.format = 'csv';
    parsed.encoding = dec.encoding;
    return limitRows(parsed);
  }

  function parseText(text) {
    if (looksLikeJSON(text)) return parseJSON(text);
    var parsed = CSV.parseCSV(text);
    parsed.format = 'csv';
    parsed.encoding = 'utf-8';
    return limitRows(parsed);
  }

  function detectFormat(name, buffer) {
    var ext = extOf(name);
    if (SPREADSHEET_EXT[ext]) return ext;
    if (ext === 'json') return 'json';
    if (CSV_EXT[ext]) return 'csv';
    if (UNSUPPORTED_EXT[ext]) return 'unsupported';
    var bytes = buffer ? toU8(buffer) : new Uint8Array(0);
    if (bytes.length >= 4 && bytes[0] === 0x50 && bytes[1] === 0x4b && (bytes[2] === 0x03 || bytes[2] === 0x05 || bytes[2] === 0x07)) {
      return 'xlsx';
    }
    if (bytes.length >= 8 && bytes[0] === 0xd0 && bytes[1] === 0xcf && bytes[2] === 0x11 && bytes[3] === 0xe0) {
      return 'xls';
    }
    try {
      var dec = decodeBytes(bytes);
      if (looksLikeJSON(dec.text)) return 'json';
    } catch (err) { /* treat as csv */ }
    return 'csv';
  }

  function parseSpreadsheet(buffer, preferredSheet) {
    var wb = readWorkbook(buffer);
    var name = preferredSheet && wb.SheetNames.indexOf(preferredSheet) >= 0
      ? preferredSheet
      : (wb.SheetNames[0] || '');
    var table = sheetToTable(wb, name);
    table.workbook = wb;
    table.sheetNames = wb.SheetNames.slice();
    table.sheetName = name;
    table.format = 'xlsx';
    return limitRows(table);
  }

  function parseFile(name, buffer) {
    var hinted = buffer && typeof buffer.byteLength === 'number' ? buffer.byteLength : 0;
    if (hinted > MAX_BYTES) throw new Error('file larger than 10 MB');
    var bytes = toU8(buffer);
    if (bytes.byteLength > MAX_BYTES) throw new Error('file larger than 10 MB');
    var fmt = detectFormat(name, bytes);
    if (fmt === 'unsupported') throw new Error('unsupported file type');
    if (SPREADSHEET_EXT[fmt] || fmt === 'xlsx' || fmt === 'xls' || fmt === 'ods') {
      return parseSpreadsheet(bytes);
    }
    if (fmt === 'json') {
      var jsonDec = decodeBytes(bytes);
      var jsonTable = parseJSON(jsonDec.text);
      jsonTable.encoding = jsonDec.encoding;
      return jsonTable;
    }
    return parseCSVBytes(bytes);
  }

  return {
    MAX_BYTES: MAX_BYTES,
    MAX_ROWS: MAX_ROWS,
    stripBOM: stripBOM,
    looksLikeJSON: looksLikeJSON,
    decodeBytes: decodeBytes,
    detectFormat: detectFormat,
    parseJSON: parseJSON,
    parseText: parseText,
    parseFile: parseFile,
    parseSpreadsheet: parseSpreadsheet,
    sheetToTable: sheetToTable,
    limitRows: limitRows,
    cellToText: cellToText,
    serialToISO: serialToISO
  };
});
