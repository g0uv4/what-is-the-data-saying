/*
 * WIDS column type inference.
 * Types: 'number' | 'category' | 'date' | 'boolean' | 'id'
 * Works in browsers (window.WIDS_TYPES) and Node (module.exports).
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.WIDS_TYPES = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var TYPES = ['number', 'category', 'date', 'boolean', 'id'];
  var MISSING = { '': 1, 'na': 1, 'n/a': 1, 'null': 1, 'none': 1, 'nan': 1, '-': 1, '—': 1, '–': 1, '..': 1, '#n/a': 1, '無資料': 1 };
  var BOOL_TRUE = { 'true': 1, 'yes': 1, 'y': 1, 't': 1, '1': 1, '是': 1, '有': 1, '真': 1 };
  var BOOL_FALSE = { 'false': 1, 'no': 1, 'n': 1, 'f': 1, '0': 1, '否': 1, '無': 1, '假': 1 };
  var YEAR_NAME = /^(year|yr|yyyy|fiscal_?year|年|年度|年份|民國年)$/i;
  var ID_NAME = /(^id$|_id$|^id_|^uid$|^uuid$|^key$|編號|代碼|代號|序號|(^|_)code$|^subject$|^participant$|^patient$)/i;
  var CODE_LIKE = /^[A-Za-z]{1,4}[-_]?\d{1,8}$/;

  function isMissing(v) {
    if (v === null || v === undefined) return true;
    return MISSING.hasOwnProperty(String(v).trim().toLowerCase());
  }

  /** Parse "1,234.5", "12%", "NT$ 300", "(45)", "−3" → number, else NaN. */
  function parseNumber(v) {
    if (typeof v === 'number') return v;
    if (v === null || v === undefined) return NaN;
    var s = String(v).trim();
    if (!s) return NaN;
    var neg = false;
    if (/^\(.*\)$/.test(s)) { neg = true; s = s.slice(1, -1); }
    s = s.replace(/[\u2212\uFE63\uFF0D]/g, '-')          // unicode minus
         .replace(/^(NT\$|US\$|\$|€|£|¥|￥)\s*/i, '')
         .replace(/\s*(%|％|元|萬|円)$/, '')
         .replace(/\s+/g, '');
    if (/^[-+]?\d{1,3}(,\d{3})+(\.\d+)?$/.test(s)) s = s.replace(/,/g, '');
    if (!/^[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?$/.test(s)) return NaN;
    var n = Number(s);
    return neg ? -n : n;
  }

  function validYMD(y, m, d) {
    if (m < 1 || m > 12) return false;
    if (d < 1 || d > 31) return false;
    var dt = new Date(Date.UTC(y, m - 1, d));
    return dt.getUTCMonth() === m - 1;
  }

  /**
   * Parse a date-like string. Returns {t:ms(UTC), gran} or null.
   * gran: 'year' | 'quarter' | 'month' | 'day' | 'datetime' | 'time'
   * Plain 4-digit years are only accepted when allowYear is true.
   */
  function parseDate(v, allowYear) {
    if (v === null || v === undefined) return null;
    var s = String(v).trim();
    var m;
    if (!s) return null;
    if ((m = /^(\d{4})$/.exec(s))) {
      if (!allowYear) return null;
      var y0 = +m[1];
      return y0 >= 1800 && y0 <= 2200 ? { t: Date.UTC(y0, 0, 1), gran: 'year' } : null;
    }
    if ((m = /^(\d{4})\s*-?\s*[Qq]([1-4])$/.exec(s))) return { t: Date.UTC(+m[1], (+m[2] - 1) * 3, 1), gran: 'quarter' };
    if ((m = /^(\d{4})[-/.](\d{1,2})$/.exec(s))) {
      return validYMD(+m[1], +m[2], 1) ? { t: Date.UTC(+m[1], +m[2] - 1, 1), gran: 'month' } : null;
    }
    if ((m = /^(\d{4})年\s*(\d{1,2})月(?:\s*(\d{1,2})日)?$/.exec(s))) {
      var dd = m[3] ? +m[3] : 1;
      return validYMD(+m[1], +m[2], dd) ? { t: Date.UTC(+m[1], +m[2] - 1, dd), gran: m[3] ? 'day' : 'month' } : null;
    }
    if ((m = /^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})(?:[ T](\d{1,2}):(\d{2})(?::(\d{2})(?:\.\d+)?)?)?\s*(Z|[+-]\d{2}:?\d{2})?$/.exec(s))) {
      var y = +m[1], mo = +m[2], d = +m[3];
      if (!validYMD(y, mo, d)) return null;
      if (m[4] !== undefined) {
        var h = +m[4], mi = +m[5], se = m[6] ? +m[6] : 0;
        if (h > 23 || mi > 59 || se > 59) return null;
        return { t: Date.UTC(y, mo - 1, d, h, mi, se), gran: 'datetime' };
      }
      return { t: Date.UTC(y, mo - 1, d), gran: 'day' };
    }
    if ((m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/.exec(s))) { // US m/d/yyyy
      return validYMD(+m[3], +m[1], +m[2]) ? { t: Date.UTC(+m[3], +m[1] - 1, +m[2]), gran: 'day' } : null;
    }
    if ((m = /^(\d{1,2}):(\d{2})(?::(\d{2}))?$/.exec(s))) {
      if (+m[1] > 23 || +m[2] > 59) return null;
      return { t: Date.UTC(1970, 0, 1, +m[1], +m[2], m[3] ? +m[3] : 0), gran: 'time' };
    }
    return null;
  }

  function boolValue(v) {
    var s = String(v).trim().toLowerCase();
    if (BOOL_TRUE.hasOwnProperty(s)) return true;
    if (BOOL_FALSE.hasOwnProperty(s)) return false;
    return null;
  }

  var GRAN_ORDER = ['time', 'datetime', 'day', 'month', 'quarter', 'year'];

  /** Infer a single column. values: raw strings. */
  function inferColumn(name, values) {
    var nonMissing = [];
    var missing = 0;
    for (var i = 0; i < values.length; i++) {
      if (isMissing(values[i])) missing++; else nonMissing.push(String(values[i]).trim());
    }
    var n = nonMissing.length;
    var distinctSet = {};
    var distinct = 0;
    nonMissing.forEach(function (v) { if (!distinctSet.hasOwnProperty(v)) { distinctSet[v] = 1; distinct++; } });
    var info = { name: name, n: n, missing: missing, distinct: distinct, type: 'category', reason: '' };
    if (n === 0) { info.reason = 'all-missing'; return info; }

    // boolean
    var boolOk = nonMissing.every(function (v) { return boolValue(v) !== null; });
    var nameIsId = ID_NAME.test(name);
    if (boolOk && distinct <= 2 && !(nameIsId)) {
      // 0/1 numeric columns with only 1 distinct value are still boolean-ish; fine.
      info.type = 'boolean'; info.reason = 'two boolean-like values'; return info;
    }

    // date
    var allowYear = YEAR_NAME.test(name.trim());
    var dateOk = 0, grans = {};
    nonMissing.forEach(function (v) {
      var p = parseDate(v, allowYear);
      if (p) { dateOk++; grans[p.gran] = (grans[p.gran] || 0) + 1; }
    });
    if (dateOk / n >= 0.95) {
      var gran = Object.keys(grans).sort(function (a, b) { return grans[b] - grans[a]; })[0];
      info.type = 'date'; info.granularity = gran;
      info.reason = allowYear && gran === 'year' ? 'year-named integer column' : 'parsed as ' + gran;
      return info;
    }

    // number
    var nums = [];
    nonMissing.forEach(function (v) { var x = parseNumber(v); if (!isNaN(x)) nums.push(x); });
    if (nums.length / n >= 0.95) {
      var allInt = nums.every(function (x) { return Math.floor(x) === x; });
      if (nameIsId && allInt && distinct === n) {
        info.type = 'id'; info.reason = 'id-named unique integers'; return info;
      }
      info.type = 'number'; info.reason = 'numeric';
      info.invalid = n - nums.length;
      return info;
    }

    // text: id vs category. Id-named still needs every value distinct.
    if (distinct === n && nameIsId) {
      info.type = 'id'; info.reason = 'id-named unique text'; return info;
    }
    if (distinct === n && n >= 5 && nonMissing.every(function (v) { return CODE_LIKE.test(v); })) {
      info.type = 'id'; info.reason = 'unique code-like text'; return info;
    }
    if (distinct === n && n >= 20) {
      info.type = 'id'; info.reason = 'every value unique'; return info;
    }
    if (distinct > 50 && distinct / n > 0.8) {
      info.type = 'id'; info.reason = 'high-cardinality text'; return info;
    }
    info.type = 'category'; info.reason = 'text with repeated / few values';
    return info;
  }

  function numStats(nums) {
    if (!nums.length) return null;
    var s = nums.slice().sort(function (a, b) { return a - b; });
    var sum = 0; s.forEach(function (x) { sum += x; });
    function q(p) { var idx = (s.length - 1) * p; var lo = Math.floor(idx), hi = Math.ceil(idx); return s[lo] + (s[hi] - s[lo]) * (idx - lo); }
    return { min: s[0], max: s[s.length - 1], mean: sum / s.length, sum: sum, q1: q(0.25), median: q(0.5), q3: q(0.75), count: s.length };
  }

  /** Convert raw cell to typed value (or null when missing / unparsable). */
  function coerce(v, type, allowYear) {
    if (isMissing(v)) return null;
    switch (type) {
      case 'number': var x = parseNumber(v); return isNaN(x) ? null : x;
      case 'date': var p = parseDate(v, true); return p ? p.t : null;
      case 'boolean': var b = boolValue(v); return b === null ? String(v).trim() : b;
      default: return String(v).trim();
    }
  }

  /**
   * Build a typed table profile.
   * @param {{headers:string[], rows:string[][]}} parsed
   * @param {Object<string,string>} [overrides] column name → type
   */
  function profileTable(parsed, overrides) {
    overrides = overrides || {};
    var columns = parsed.headers.map(function (h, ci) {
      var raw = parsed.rows.map(function (r) { return r[ci]; });
      var info = inferColumn(h, raw);
      info.index = ci;
      info.inferred = info.type;
      if (overrides[h] && TYPES.indexOf(overrides[h]) >= 0) info.type = overrides[h];
      info.values = raw.map(function (v) { return coerce(v, info.type); });
      if (info.type === 'number') info.stats = numStats(info.values.filter(function (x) { return x !== null; }));
      if (info.type === 'date' && !info.granularity) info.granularity = 'day';
      var seen = {}, samples = [];
      for (var i = 0; i < raw.length && samples.length < 4; i++) {
        var s = raw[i] == null ? '' : String(raw[i]).trim();
        if (!isMissing(s) && !seen[s]) { seen[s] = 1; samples.push(s); }
      }
      info.samples = samples;
      return info;
    });
    return { columns: columns, rowCount: parsed.rows.length };
  }

  return {
    TYPES: TYPES,
    isMissing: isMissing,
    parseNumber: parseNumber,
    parseDate: parseDate,
    boolValue: boolValue,
    inferColumn: inferColumn,
    profileTable: profileTable,
    coerce: coerce,
    numStats: numStats,
    GRAN_ORDER: GRAN_ORDER
  };
});
