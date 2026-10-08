/*
 * WIDS CSV parser — RFC 4180-ish, no dependencies.
 * Handles: UTF-8 BOM, quoted fields, delimiters / newlines inside quotes,
 * escaped quotes (""), CRLF / LF / CR line endings, trailing newline,
 * ragged rows (padded / truncated to header length), delimiter sniffing
 * (comma, semicolon, tab).
 * Works in browsers (window.WIDS_CSV) and Node (module.exports).
 *
 * Leading '#' comments (stripLeadingComments, used by parseCSV only;
 * parseRows is unchanged):
 * 1. After the BOM is stripped, physical lines are read from the top, split on
 *    CRLF, LF, or a lone CR. The leading block is consecutive lines whose first
 *    character is '#'. Blank / whitespace-only lines inside or before that block
 *    belong to it too. The block stops at the anchor line: the first line that
 *    is non-blank and does not start with '#'.
 * 2. If there is no '#' line at the top, or there is no anchor (the file is only
 *    '#' lines and blanks), nothing is skipped. Behaviour is unchanged.
 * 3. The delimiter is opts.delimiter when that is given; otherwise it is
 *    sniffed from the anchor line alone. That same delimiter is used for the
 *    whole parse, so punctuation inside a comment cannot change the sniff.
 * 4. nf is the anchor line's field count, parseRows(anchorLine, delimiter)[0].length.
 *    The '#' lines of the block are walked top-down. The first whose field count
 *    (same delimiter, parseRows on that single line) equals nf is the header and
 *    is kept, together with everything after it. Lines before it are skipped.
 *    If no '#' line matches nf, the whole block is skipped and the anchor line
 *    is the header.
 *    Single-column exception (nf === 1): a line that is just "#" or "#" followed
 *    by whitespace (for example "# note") is a comment even though its field
 *    count is 1. A line like "#id" is still kept as the header.
 * 5. Only the top of the file is affected. A '#' that appears after the header
 *    or data has started is left alone.
 * 6. When lines were skipped, the warnings array gains "comments:<k>", where k
 *    is the number of non-blank skipped '#' lines, and the result also has
 *    skippedLines: k (0 when nothing was skipped). "empty" and "ragged:n" still
 *    apply; ragged counting ignores skipped lines.
 * Known limitation: a leading comment line that happens to contain exactly as
 * many delimiter-separated fields as the real header is treated as the header
 * (same as before this change).
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
   * Physical lines split on CRLF, LF, or a lone CR.
   * start is an index into text so the unsplit tail keeps its original endings.
   */
  function splitPhysicalLines(text) {
    var lines = [];
    var start = 0;
    var i = 0;
    var n = text.length;
    while (i < n) {
      var c = text[i];
      if (c !== '\n' && c !== '\r') { i++; continue; }
      var contentEnd = i;
      if (c === '\r' && i + 1 < n && text[i + 1] === '\n') i += 2;
      else i += 1;
      lines.push({ content: text.slice(start, contentEnd), start: start });
      start = i;
    }
    if (start < n || lines.length === 0) {
      lines.push({ content: text.slice(start), start: start });
    }
    return lines;
  }

  function fieldCount(line, delimiter) {
    var parsed = parseRows(line, delimiter);
    return parsed.length ? parsed[0].length : 0;
  }

  /**
   * Drop a leading '#' comment block. See the file header for the full rule.
   *
   * After the BOM is stripped, physical lines (CRLF / LF / lone CR) are scanned
   * from the top. The leading block is lines whose first character is '#', plus
   * blank or whitespace-only lines inside or before that block. It stops at the
   * anchor: the first non-blank line that does not start with '#'. If the top
   * has no '#' line, or the file has no anchor (only '#' lines and blanks),
   * nothing is skipped.
   * Delimiter is opts.delimiter, or else sniffed from the anchor line alone, and
   * that delimiter is used for every field count and for the caller’s parse.
   * nf is the anchor’s field count. Walking the block’s '#' lines top-down, the
   * first whose field count equals nf is kept as the header together with
   * everything after it; lines before it are skipped. If none match, the whole
   * block is skipped and the anchor is the header. When nf === 1, a line that
   * is "#" or "#" followed by whitespace (for example "# note") stays a comment;
   * "#id" can still be the header. A '#' later in the file is not touched.
   * skipped is the number of non-blank '#' lines removed (0 when nothing was
   * skipped). text is the remainder, starting at the kept header line, with the
   * original line endings preserved.
   * Known limitation: a leading comment with exactly nf delimiter-separated
   * fields is treated as the header.
   *
   * @param {string} text
   * @param {{delimiter?: string}} [opts]
   * @returns {{text: string, skipped: number, delimiter: string}}
   */
  function stripLeadingComments(text, opts) {
    opts = opts || {};
    var clean = stripBOM(String(text == null ? '' : text));
    var lines = splitPhysicalLines(clean);
    var anchorIdx = -1;
    var hasHash = false;
    var i;
    for (i = 0; i < lines.length; i++) {
      var content = lines[i].content;
      if (content.trim() === '') continue;
      if (content.charAt(0) === '#') { hasHash = true; continue; }
      anchorIdx = i;
      break;
    }
    if (!hasHash || anchorIdx < 0) {
      return {
        text: clean,
        skipped: 0,
        delimiter: opts.delimiter || sniffDelimiter(clean)
      };
    }
    var anchorLine = lines[anchorIdx].content;
    var delimiter = opts.delimiter || sniffDelimiter(anchorLine);
    var nf = fieldCount(anchorLine, delimiter);
    var headerIdx = -1;
    for (i = 0; i < anchorIdx; i++) {
      var line = lines[i].content;
      if (line.trim() === '' || line.charAt(0) !== '#') continue;
      // "# note" / "#" is prose when the data has a single column, not a header.
      if (nf === 1 && (line === '#' || /\s/.test(line.charAt(1)))) continue;
      if (fieldCount(line, delimiter) === nf) { headerIdx = i; break; }
    }
    var keepFrom = headerIdx >= 0 ? headerIdx : anchorIdx;
    var skipped = 0;
    for (i = 0; i < keepFrom; i++) {
      var skippedLine = lines[i].content;
      if (skippedLine.trim() !== '' && skippedLine.charAt(0) === '#') skipped++;
    }
    return {
      text: clean.slice(lines[keepFrom].start),
      skipped: skipped,
      delimiter: delimiter
    };
  }

  /**
   * Parse CSV text with a header row.
   * Leading '#' comment blocks are handled by stripLeadingComments.
   * @returns {{headers:string[], rows:string[][], delimiter:string, warnings:string[], skippedLines:number}}
   */
  function parseCSV(text, opts) {
    opts = opts || {};
    var stripped = stripLeadingComments(text, opts);
    var clean = stripped.text;
    var delimiter = stripped.delimiter;
    var skipped = stripped.skipped;
    var all = parseRows(clean, delimiter);
    var warnings = [];
    if (!all.length) {
      if (skipped) warnings.push('comments:' + skipped);
      warnings.push('empty');
      return { headers: [], rows: [], delimiter: delimiter, warnings: warnings, skippedLines: skipped };
    }
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
    if (skipped) warnings.push('comments:' + skipped);
    if (ragged) warnings.push('ragged:' + ragged);
    return { headers: headers, rows: rows, delimiter: delimiter, warnings: warnings, skippedLines: skipped };
  }

  return {
    parseCSV: parseCSV,
    parseRows: parseRows,
    sniffDelimiter: sniffDelimiter,
    stripBOM: stripBOM,
    stripLeadingComments: stripLeadingComments
  };
});
