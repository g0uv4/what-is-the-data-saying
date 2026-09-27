/*
 * WIDS renderers. Chart.js (global `Chart`) for line / bar / scatter / histogram /
 * pyramid; hand-drawn <canvas> for box plot, matrix heatmap and adjacency matrix.
 * Pure helpers (aggregate, bins, boxStats, colour scales) are exported for Node tests.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.WIDS_CHARTS = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var PALETTE = ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f', '#edc948', '#b07aa1', '#ff9da7', '#9c755f', '#bab0ac', '#1f77b4', '#17becf'];
  var VIRIDIS = [[68, 1, 84], [59, 82, 139], [33, 145, 140], [94, 201, 98], [253, 231, 37]];
  var RDBU = [[33, 102, 172], [146, 197, 222], [247, 247, 247], [244, 165, 130], [178, 24, 43]];

  var G = typeof window !== 'undefined' ? window : {};
  function lang() { return G.WIDS_I18N ? G.WIDS_I18N.getLang() : 'zh'; }
  function L(o) { return o[lang()] || o.zh; }
  function fmt(v) {
    if (v === null || v === undefined || isNaN(v)) return '—';
    var a = Math.abs(v);
    return Number(v).toLocaleString(lang() === 'en' ? 'en-US' : 'zh-TW', { maximumFractionDigits: a >= 100 ? 0 : a >= 1 ? 2 : 4 });
  }
  function pad(n) { return n < 10 ? '0' + n : '' + n; }
  function fmtDate(t, gran) {
    var d = new Date(t);
    var y = d.getUTCFullYear(), m = d.getUTCMonth() + 1, day = d.getUTCDate();
    switch (gran) {
      case 'year': return '' + y;
      case 'quarter': return y + ' Q' + (Math.floor((m - 1) / 3) + 1);
      case 'month': return y + '-' + pad(m);
      case 'datetime': return y + '-' + pad(m) + '-' + pad(day) + ' ' + pad(d.getUTCHours()) + ':' + pad(d.getUTCMinutes());
      case 'time': return pad(d.getUTCHours()) + ':' + pad(d.getUTCMinutes());
      default: return y + '-' + pad(m) + '-' + pad(day);
    }
  }
  function colorAlpha(hex, a) {
    var n = parseInt(hex.slice(1), 16);
    return 'rgba(' + (n >> 16 & 255) + ',' + (n >> 8 & 255) + ',' + (n & 255) + ',' + a + ')';
  }
  function interp(stops, t) {
    t = Math.max(0, Math.min(1, isNaN(t) ? 0 : t));
    var p = t * (stops.length - 1), i = Math.min(stops.length - 2, Math.floor(p)), f = p - i;
    var a = stops[i], b = stops[i + 1];
    return 'rgb(' + Math.round(a[0] + (b[0] - a[0]) * f) + ',' + Math.round(a[1] + (b[1] - a[1]) * f) + ',' + Math.round(a[2] + (b[2] - a[2]) * f) + ')';
  }
  /** Colour scale: sequential viridis, or diverging RdBu around 0 when data spans 0. */
  function colorScale(min, max) {
    if (min < 0 && max > 0) {
      var m = Math.max(-min, max);
      return { diverging: true, min: -m, max: m, color: function (v) { return interp(RDBU, (v + m) / (2 * m)); } };
    }
    var span = max - min || 1;
    return { diverging: false, min: min, max: max, color: function (v) { return interp(VIRIDIS, (v - min) / span); } };
  }
  function textColorFor(rgb) {
    var m = /rgb\((\d+),(\d+),(\d+)\)/.exec(rgb); if (!m) return '#000';
    return (0.299 * m[1] + 0.587 * m[2] + 0.114 * m[3]) > 150 ? '#111' : '#fff';
  }

  // ------------------------------------------------------------ helpers
  function col(profile, name) { return profile.columns.filter(function (c) { return c.name === name; })[0] || null; }

  /** Ordered distinct keys of a column with display labels. */
  function keysOf(c, order) {
    var seen = {}, keys = [];
    c.values.forEach(function (v) { if (v !== null && !seen.hasOwnProperty(v)) { seen[v] = 1; keys.push(v); } });
    if (c.type === 'date' || c.type === 'number') keys.sort(function (a, b) { return a - b; });
    else if (order === 'alpha') keys.sort(function (a, b) { return String(a).localeCompare(String(b), 'zh-Hant'); });
    return keys;
  }
  function labelOf(c, v) {
    if (v === null || v === undefined) return '—';
    if (c.type === 'date') return fmtDate(v, c.granularity);
    if (c.type === 'boolean') return String(v);
    return c.type === 'number' ? fmt(v) : String(v);
  }

  var AGG = {
    sum: function (a) { var s = 0; a.forEach(function (x) { s += x; }); return s; },
    mean: function (a) { return a.length ? AGG.sum(a) / a.length : null; },
    count: function (a) { return a.length; },
    max: function (a) { return a.length ? Math.max.apply(null, a) : null; },
    min: function (a) { return a.length ? Math.min.apply(null, a) : null; },
    median: function (a) { if (!a.length) return null; var s = a.slice().sort(function (x, y) { return x - y; }); var m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; }
  };

  /**
   * Group rows by one or two key arrays and aggregate a value array.
   * keysA/keysB: arrays of row keys (keysB optional); values: numbers or null (null → count mode).
   * Returns map "a\u0001b" → aggregated value.
   */
  function aggregate(keysA, keysB, values, agg) {
    var buckets = {};
    for (var i = 0; i < keysA.length; i++) {
      var a = keysA[i]; if (a === null || a === undefined) continue;
      var b = keysB ? keysB[i] : ''; if (keysB && (b === null || b === undefined)) continue;
      var k = a + '\u0001' + b;
      if (!buckets[k]) buckets[k] = [];
      if (!values) buckets[k].push(1);
      else if (values[i] !== null && values[i] !== undefined) buckets[k].push(values[i]);
    }
    var fn = !values ? AGG.count : (AGG[agg] || AGG.sum);
    var out = {};
    Object.keys(buckets).forEach(function (k) { out[k] = buckets[k].length ? fn(buckets[k]) : null; });
    return out;
  }

  function quantile(sorted, p) {
    if (!sorted.length) return null;
    var idx = (sorted.length - 1) * p, lo = Math.floor(idx), hi = Math.ceil(idx);
    return sorted[lo] + (sorted[hi] - sorted[lo]) * (idx - lo);
  }
  /** Tukey box statistics (1.5 × IQR whiskers). */
  function boxStats(values) {
    var s = values.filter(function (v) { return v !== null && !isNaN(v); }).sort(function (a, b) { return a - b; });
    if (!s.length) return null;
    var q1 = quantile(s, 0.25), med = quantile(s, 0.5), q3 = quantile(s, 0.75), iqr = q3 - q1;
    var lo = q1 - 1.5 * iqr, hi = q3 + 1.5 * iqr;
    var inside = s.filter(function (v) { return v >= lo && v <= hi; });
    return { n: s.length, min: s[0], max: s[s.length - 1], q1: q1, median: med, q3: q3, iqr: iqr,
      whiskerLow: inside.length ? inside[0] : q1, whiskerHigh: inside.length ? inside[inside.length - 1] : q3,
      outliers: s.filter(function (v) { return v < lo || v > hi; }), values: s };
  }
  function niceStep(span, target) {
    var raw = span / Math.max(1, target), mag = Math.pow(10, Math.floor(Math.log10(raw || 1)));
    var r = raw / mag;
    return (r <= 1 ? 1 : r <= 2 ? 2 : r <= 2.5 ? 2.5 : r <= 5 ? 5 : 10) * mag;
  }
  /** Histogram bins: Sturges by default; edges on nice steps. */
  function bins(values, count) {
    var s = values.filter(function (v) { return v !== null && !isNaN(v); });
    if (!s.length) return [];
    var min = Math.min.apply(null, s), max = Math.max.apply(null, s);
    var k = count || Math.max(1, Math.ceil(Math.log2(s.length) + 1));
    if (min === max) return [{ x0: min, x1: max, count: s.length }];
    var step = niceStep(max - min, k);
    var start = Math.floor(min / step) * step;
    var n = Math.max(1, Math.ceil((max - start) / step + 1e-9));
    if (start + n * step <= max) n++;
    var out = [];
    for (var i = 0; i < n; i++) out.push({ x0: start + i * step, x1: start + (i + 1) * step, count: 0 });
    s.forEach(function (v) { var i = Math.min(n - 1, Math.floor((v - start) / step)); out[i].count++; });
    return out;
  }
  function niceTicks(min, max, target) {
    if (min === max) { min -= 1; max += 1; }
    var step = niceStep(max - min, target || 5);
    var t0 = Math.floor(min / step) * step, ticks = [];
    for (var v = t0; v <= max + step * 1e-6; v += step) ticks.push(+v.toFixed(10));
    if (ticks[ticks.length - 1] < max) ticks.push(+(ticks[ticks.length - 1] + step).toFixed(10));
    return ticks;
  }

  // ------------------------------------------------------------ DOM helpers
  function el(tag, attrs, text) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { if (k === 'class') e.className = attrs[k]; else e.setAttribute(k, attrs[k]); });
    if (text !== undefined) e.textContent = text;
    return e;
  }
  function chartBox(host, height) {
    var box = el('div', { class: 'chart-box' });
    box.style.height = height + 'px';
    var cv = el('canvas');
    box.appendChild(cv);
    host.appendChild(box);
    return cv;
  }
  function baseOptions(extra) {
    var o = {
      responsive: true, maintainAspectRatio: false, animation: { duration: 250 },
      plugins: { legend: { position: 'top', labels: { boxWidth: 12, usePointStyle: true } }, tooltip: { mode: 'nearest', intersect: true } }
    };
    return deepMerge(o, extra || {});
  }
  function deepMerge(a, b) {
    Object.keys(b).forEach(function (k) {
      if (b[k] && typeof b[k] === 'object' && !Array.isArray(b[k]) && a[k] && typeof a[k] === 'object') deepMerge(a[k], b[k]);
      else a[k] = b[k];
    });
    return a;
  }
  function note(host, text) { host.appendChild(el('p', { class: 'chart-note' }, text)); }
  function newChart(cv, cfg) {
    if (typeof Chart === 'undefined') throw new Error('Chart.js not loaded');
    return new Chart(cv.getContext('2d'), cfg);
  }

  // Canvas with DPR scaling + tooltip overlay. draw(ctx, w, h) returns hit regions.
  function canvasPanel(host, height, draw) {
    var wrap = el('div', { class: 'chart-box canvas-panel' });
    wrap.style.height = height + 'px';
    var cv = el('canvas');
    var tip = el('div', { class: 'canvas-tip', role: 'tooltip' });
    wrap.appendChild(cv); wrap.appendChild(tip); host.appendChild(wrap);
    var regions = [];
    function paint() {
      var w = wrap.clientWidth || 600, h = wrap.clientHeight || height;
      var dpr = window.devicePixelRatio || 1;
      cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
      cv.style.width = w + 'px'; cv.style.height = h + 'px';
      var ctx = cv.getContext('2d');
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, w, h);
      ctx.font = '12px system-ui, -apple-system, "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif';
      regions = draw(ctx, w, h) || [];
    }
    function onMove(ev) {
      var r = cv.getBoundingClientRect(), x = ev.clientX - r.left, y = ev.clientY - r.top;
      var hit = null;
      for (var i = regions.length - 1; i >= 0; i--) { var g = regions[i]; if (x >= g.x && x <= g.x + g.w && y >= g.y && y <= g.y + g.h) { hit = g; break; } }
      if (!hit) { tip.style.display = 'none'; cv.style.cursor = 'default'; return; }
      tip.innerHTML = '';
      hit.lines.forEach(function (ln, i) { var d = el('div', i === 0 ? { class: 'tip-title' } : null, ln); tip.appendChild(d); });
      tip.style.display = 'block';
      var tx = x + 14, ty = y + 14;
      if (tx + tip.offsetWidth > wrap.clientWidth) tx = x - tip.offsetWidth - 10;
      if (ty + tip.offsetHeight > wrap.clientHeight) ty = y - tip.offsetHeight - 10;
      tip.style.left = Math.max(0, tx) + 'px'; tip.style.top = Math.max(0, ty) + 'px';
      cv.style.cursor = 'crosshair';
    }
    cv.addEventListener('mousemove', onMove);
    cv.addEventListener('mouseleave', function () { tip.style.display = 'none'; });
    var ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(function () { paint(); }) : null;
    if (ro) ro.observe(wrap);
    paint();
    return { repaint: paint, destroy: function () { if (ro) ro.disconnect(); }, canvas: cv };
  }
  function legendChips(host, items, onToggle) {
    var bar = el('div', { class: 'legend-chips', role: 'group' });
    items.forEach(function (it) {
      var b = el('button', { type: 'button', class: 'chip' + (it.hidden ? ' off' : ''), 'aria-pressed': String(!it.hidden) });
      var sw = el('span', { class: 'swatch' }); sw.style.background = it.color;
      b.appendChild(sw); b.appendChild(document.createTextNode(it.label));
      b.addEventListener('click', function () { it.hidden = !it.hidden; b.classList.toggle('off', it.hidden); b.setAttribute('aria-pressed', String(!it.hidden)); onToggle(); });
      bar.appendChild(b);
    });
    host.appendChild(bar);
  }

  // ------------------------------------------------------------ field auto-pick
  function pick(profile, types, exclude, prefer) {
    exclude = exclude || [];
    var cands = profile.columns.filter(function (c) { return types.indexOf(c.type) >= 0 && exclude.indexOf(c.name) < 0; });
    if (prefer) { var p = cands.filter(function (c) { return c.name === prefer; })[0]; if (p) return p.name; }
    return cands.length ? cands[0].name : '';
  }
  function measures(profile, shape) {
    var m = (shape && shape.roles.measures) || [];
    return profile.columns.filter(function (c) { return c.type === 'number'; }).sort(function (a, b) {
      var am = m.indexOf(a.name) >= 0 ? 0 : 1, bm = m.indexOf(b.name) >= 0 ? 0 : 1;
      return am - bm;
    });
  }
  function bestMeasure(profile, shape, exclude) {
    exclude = exclude || [];
    var ms = measures(profile, shape).filter(function (c) { return exclude.indexOf(c.name) < 0; });
    var m = (shape && shape.roles.measures) || [];
    var inRole = ms.filter(function (c) { return m.indexOf(c.name) >= 0; });
    var pool = inRole.length ? inRole : ms;
    pool = pool.slice().sort(function (a, b) { return b.distinct - a.distinct; });
    // prefer a ratio column when present (geo rates), else highest-cardinality measure
    var rate = pool.filter(function (c) { return /(rate|ratio|pct|percent|率|比|%)/i.test(c.name); })[0];
    return rate ? rate.name : (pool[0] ? pool[0].name : '');
  }
  function lowCat(profile, exclude, maxDistinct) {
    exclude = exclude || [];
    var c = profile.columns.filter(function (c) { return (c.type === 'category' || c.type === 'boolean') && exclude.indexOf(c.name) < 0 && c.distinct >= 2 && c.distinct <= (maxDistinct || 12); })
      .sort(function (a, b) { return a.distinct - b.distinct; })[0];
    return c ? c.name : '';
  }

  var LABEL_TYPES = ['category', 'id', 'boolean', 'date'];
  var AGG_CHOICES = ['sum', 'mean', 'median', 'max', 'min', 'count'];
  var AGG_LABELS = { sum: { zh: '加總', en: 'sum' }, mean: { zh: '平均', en: 'mean' }, median: { zh: '中位數', en: 'median' }, max: { zh: '最大', en: 'max' }, min: { zh: '最小', en: 'min' }, count: { zh: '計數', en: 'count' } };

  // ------------------------------------------------------------ renderers
  var R = {};

  // ---- line
  R.line = {
    key: 'line', zh: '折線圖（時間序列）', en: 'Line (time series)', pattern: 'time-series-trend', sample: 'sample-spiral.csv, streamgraph-categories.csv, streamgraph-wide.csv',
    fields: [
      { key: 'x', zh: 'X（時間）', en: 'X (time)', types: ['date', 'number', 'category'] },
      { key: 'y', zh: 'Y（數值）', en: 'Y (number)', types: ['number'], wide: true },
      { key: 'series', zh: '系列（類別，可選）', en: 'Series (optional)', types: ['category', 'boolean', 'id'], optional: true }
    ],
    options: [{ key: 'agg', zh: '聚合', en: 'Aggregate', choices: AGG_CHOICES.slice(0, 5), labels: AGG_LABELS, def: 'sum' }],
    auto: function (p, s) {
      var x = pick(p, ['date'], [], s.roles.time) || pick(p, ['number']);
      var series = s.hints.multiSeries || s.hints.manySeries ? lowCat(p, [x], 60) : '';
      var y = s.hints.wideSeries && !series ? '__wide__' : bestMeasure(p, s, [x]);
      return { x: x, y: y, series: series, agg: 'sum' };
    },
    draw: function (host, p, sel) {
      var xc = col(p, sel.x); if (!xc) throw new Error('x');
      var keys = keysOf(xc), labels = keys.map(function (k) { return labelOf(xc, k); });
      var datasets = [];
      var yCols = sel.y === '__wide__' ? p.columns.filter(function (c) { return c.type === 'number' && c.name !== sel.x; }) : [col(p, sel.y)].filter(Boolean);
      if (!yCols.length) throw new Error('y');
      var sc = sel.series ? col(p, sel.series) : null;
      if (sc && sel.y !== '__wide__') {
        var agg = aggregate(xc.values, sc.values, yCols[0].values, sel.agg);
        var skeys = keysOf(sc);
        var totals = skeys.map(function (sk) { var t = 0; keys.forEach(function (k) { t += agg[k + '\u0001' + sk] || 0; }); return { sk: sk, t: t }; });
        totals.sort(function (a, b) { return b.t - a.t; });
        if (totals.length > 12) note(host, lang() === 'zh' ? '系列 ' + totals.length + ' 個，只畫總量前 12；更多請用小多圖。' : totals.length + ' series; showing top 12 by total.');
        totals.slice(0, 12).forEach(function (o, i) {
          datasets.push({ label: labelOf(sc, o.sk), data: keys.map(function (k) { var v = agg[k + '\u0001' + o.sk]; return v === undefined ? null : v; }), borderColor: PALETTE[i % PALETTE.length], backgroundColor: PALETTE[i % PALETTE.length], tension: 0.15, spanGaps: true, pointRadius: keys.length > 60 ? 0 : 3 });
        });
      } else {
        yCols.slice(0, 12).forEach(function (yc, i) {
          var agg = aggregate(xc.values, null, yc.values, sel.agg);
          datasets.push({ label: yc.name, data: keys.map(function (k) { var v = agg[k + '\u0001']; return v === undefined ? null : v; }), borderColor: PALETTE[i % PALETTE.length], backgroundColor: PALETTE[i % PALETTE.length], tension: 0.15, spanGaps: true, pointRadius: keys.length > 60 ? 0 : 3 });
        });
      }
      if (datasets.length > 3) note(host, lang() === 'zh' ? '超過 3 條線易成義大利麵：點圖例可隱藏系列。' : 'More than 3 lines gets busy: click legend items to hide.');
      return newChart(chartBox(host, 420), { type: 'line', data: { labels: labels, datasets: datasets }, options: baseOptions({
        interaction: { mode: 'index', intersect: false },
        plugins: { tooltip: { mode: 'index', intersect: false, callbacks: { label: function (c) { return c.dataset.label + '：' + fmt(c.parsed.y); } } } },
        scales: { x: { title: { display: true, text: xc.name }, ticks: { autoSkip: true, maxRotation: 0 } }, y: { title: { display: true, text: sel.y === '__wide__' ? '' : sel.y }, beginAtZero: false } }
      }) });
    }
  };

  // ---- sorted bar / lollipop
  R.barSorted = {
    key: 'barSorted', zh: '排序長條／棒棒糖', en: 'Sorted bar / lollipop', pattern: 'categorical-comparison', sample: 'lollipop-categories.csv, sample-choropleth.csv',
    fields: [
      { key: 'cat', zh: '類別', en: 'Category', types: LABEL_TYPES },
      { key: 'value', zh: '數值（空＝計數）', en: 'Value (empty = count)', types: ['number'], optional: true }
    ],
    options: [
      { key: 'agg', zh: '聚合', en: 'Aggregate', choices: AGG_CHOICES.slice(0, 5), labels: AGG_LABELS, def: 'sum' },
      { key: 'sort', zh: '排序', en: 'Sort', choices: ['desc', 'asc', 'none'], labels: { desc: { zh: '由大到小', en: 'descending' }, asc: { zh: '由小到大', en: 'ascending' }, none: { zh: '原始順序', en: 'original' } }, def: 'desc' },
      { key: 'style', zh: '樣式', en: 'Style', choices: ['bar', 'lollipop'], labels: { bar: { zh: '長條', en: 'bar' }, lollipop: { zh: '棒棒糖', en: 'lollipop' } }, def: 'bar' }
    ],
    auto: function (p, s, preset) {
      var cat = s.roles.label && col(p, s.roles.label) && col(p, s.roles.label).type === 'category' ? s.roles.label : (s.roles.geo || pick(p, ['category']) || pick(p, LABEL_TYPES));
      return { cat: cat, value: bestMeasure(p, s, [cat]), agg: 'sum', sort: 'desc', style: (preset && preset.style) || 'bar' };
    },
    draw: function (host, p, sel) {
      var cc = col(p, sel.cat); if (!cc) throw new Error('cat');
      var vc = sel.value ? col(p, sel.value) : null;
      var agg = aggregate(cc.values, null, vc ? vc.values : null, sel.agg);
      var rows = keysOf(cc).map(function (k) { return { k: k, label: labelOf(cc, k), v: agg[k + '\u0001'] }; }).filter(function (r) { return r.v !== undefined && r.v !== null; });
      if (sel.sort === 'desc') rows.sort(function (a, b) { return b.v - a.v; });
      if (sel.sort === 'asc') rows.sort(function (a, b) { return a.v - b.v; });
      var limit = 30;
      if (rows.length > limit) { note(host, lang() === 'zh' ? '類別 ' + rows.length + ' 個，只顯示前 ' + limit + '（依目前排序）。' : rows.length + ' categories; showing first ' + limit + '.'); rows = rows.slice(0, limit); }
      var maxLabel = Math.max.apply(null, rows.map(function (r) { return r.label.length; }).concat([0]));
      var horizontal = rows.length > 8 || maxLabel > 6;
      var valueLabel = vc ? (sel.agg === 'sum' ? vc.name : vc.name + '（' + L(AGG_LABELS[sel.agg]) + '）') : L({ zh: '計數', en: 'count' });
      var data = rows.map(function (r) { return r.v; });
      var lolli = sel.style === 'lollipop';
      var datasets = [{ type: 'bar', label: valueLabel, data: data, backgroundColor: lolli ? '#8a8f98' : colorAlpha(PALETTE[0], 0.85), borderColor: PALETTE[0], barThickness: lolli ? 2 : undefined, maxBarThickness: 48 }];
      if (lolli) datasets.push({ type: 'line', label: valueLabel + ' ●', data: data, showLine: false, pointRadius: 7, pointHoverRadius: 9, backgroundColor: PALETTE[1], borderColor: PALETTE[1] });
      var valueAxis = { beginAtZero: true, grace: '5%', title: { display: true, text: valueLabel } };
      var catAxis = { title: { display: true, text: cc.name }, ticks: { autoSkip: false } };
      var height = horizontal ? Math.max(260, rows.length * 26 + 80) : 400;
      return newChart(chartBox(host, height), { type: 'bar', data: { labels: rows.map(function (r) { return r.label; }), datasets: datasets }, options: baseOptions({
        indexAxis: horizontal ? 'y' : 'x',
        plugins: { legend: { display: false }, tooltip: { filter: function (item) { return !lolli || item.datasetIndex === 1; }, callbacks: { label: function (c) { return valueLabel + '：' + fmt(horizontal ? c.parsed.x : c.parsed.y); } } } },
        scales: horizontal ? { x: valueAxis, y: catAxis } : { x: catAxis, y: valueAxis }
      }) });
    }
  };

  // ---- grouped / stacked bar
  R.barGrouped = {
    key: 'barGrouped', zh: '分組／堆疊長條', en: 'Grouped / stacked bar', pattern: 'categorical-comparison', sample: 'sample-marimekko.csv, population-pyramid-long.csv',
    fields: [
      { key: 'cat', zh: '類別（軸）', en: 'Category (axis)', types: LABEL_TYPES },
      { key: 'group', zh: '分組（顏色）', en: 'Group (colour)', types: ['category', 'boolean', 'id', 'date'] },
      { key: 'value', zh: '數值（空＝計數）', en: 'Value (empty = count)', types: ['number'], optional: true }
    ],
    options: [
      { key: 'mode', zh: '模式', en: 'Mode', choices: ['grouped', 'stacked', 'percent'], labels: { grouped: { zh: '分組', en: 'grouped' }, stacked: { zh: '堆疊', en: 'stacked' }, percent: { zh: '100% 堆疊', en: '100% stacked' } }, def: 'grouped' },
      { key: 'agg', zh: '聚合', en: 'Aggregate', choices: AGG_CHOICES.slice(0, 5), labels: AGG_LABELS, def: 'sum' },
      { key: 'sort', zh: '排序', en: 'Sort', choices: ['desc', 'none'], labels: { desc: { zh: '總量由大到小', en: 'total desc' }, none: { zh: '原始順序', en: 'original' } }, def: 'desc' }
    ],
    auto: function (p, s) {
      var ct = s.roles.crossTab;
      var cat = ct ? ct[0] : lowCat(p, [], 30) || pick(p, LABEL_TYPES);
      var group = ct ? ct[1] : lowCat(p, [cat], 12);
      return { cat: cat, group: group, value: bestMeasure(p, s, [cat, group]), mode: 'grouped', agg: 'sum', sort: 'desc' };
    },
    draw: function (host, p, sel) {
      var cc = col(p, sel.cat), gc = col(p, sel.group); if (!cc || !gc) throw new Error('fields');
      var vc = sel.value ? col(p, sel.value) : null;
      var agg = aggregate(cc.values, gc.values, vc ? vc.values : null, sel.agg);
      var ck = keysOf(cc), gk = keysOf(gc).slice(0, 12);
      var totals = {}; ck.forEach(function (c) { var t = 0; gk.forEach(function (g) { t += agg[c + '\u0001' + g] || 0; }); totals[c] = t; });
      if (sel.sort === 'desc') ck.sort(function (a, b) { return totals[b] - totals[a]; });
      ck = ck.slice(0, 40);
      var pct = sel.mode === 'percent';
      var datasets = gk.map(function (g, i) {
        return { label: labelOf(gc, g), backgroundColor: PALETTE[i % PALETTE.length], data: ck.map(function (c) { var v = agg[c + '\u0001' + g]; if (v === undefined) return null; return pct ? (totals[c] ? v / totals[c] * 100 : 0) : v; }), raw: ck.map(function (c) { return agg[c + '\u0001' + g]; }) };
      });
      var stacked = sel.mode !== 'grouped';
      var horizontal = ck.length > 10;
      var vTitle = pct ? '%' : (vc ? vc.name : L({ zh: '計數', en: 'count' }));
      var vAxis = { stacked: stacked, beginAtZero: true, grace: pct ? 0 : '5%', max: pct ? 100 : undefined, title: { display: true, text: vTitle } };
      var cAxis = { stacked: stacked, title: { display: true, text: cc.name } };
      return newChart(chartBox(host, horizontal ? Math.max(300, ck.length * 28 + 90) : 420), { type: 'bar', data: { labels: ck.map(function (k) { return labelOf(cc, k); }), datasets: datasets }, options: baseOptions({
        indexAxis: horizontal ? 'y' : 'x',
        interaction: { mode: 'index', intersect: false },
        plugins: { tooltip: { mode: 'index', intersect: false, callbacks: { label: function (c) { var raw = c.dataset.raw[c.dataIndex]; return c.dataset.label + '：' + fmt(raw) + (pct ? '（' + fmt(horizontal ? c.parsed.x : c.parsed.y) + '%）' : ''); } } } },
        scales: horizontal ? { x: vAxis, y: cAxis } : { x: cAxis, y: vAxis }
      }) });
    }
  };

  // ---- scatter / bubble
  R.scatter = {
    key: 'scatter', zh: '散點／氣泡圖', en: 'Scatter / bubble', pattern: 'correlation-scatter', sample: 'sample-bubble.csv',
    fields: [
      { key: 'x', zh: 'X（數值）', en: 'X (number)', types: ['number'] },
      { key: 'y', zh: 'Y（數值）', en: 'Y (number)', types: ['number'] },
      { key: 'color', zh: '顏色分組（可選）', en: 'Colour group (optional)', types: ['category', 'boolean'], optional: true },
      { key: 'size', zh: '大小（面積映射，可選）', en: 'Size (area, optional)', types: ['number'], optional: true },
      { key: 'label', zh: '標籤（提示用，可選）', en: 'Label (tooltip, optional)', types: ['category', 'id'], optional: true }
    ],
    options: [],
    auto: function (p, s, preset) {
      var ms = measures(p, s).map(function (c) { return c.name; });
      var x = ms[0] || '', y = ms[1] || '';
      var size = '';
      if (preset && preset.useSize || s.hints.sizeVar) {
        var sz = ms.filter(function (n) { return n !== x && n !== y && /(size|pop|population|volume|weight|規模|人口)/i.test(n); })[0] || ms[2] || '';
        size = preset && preset.useSize ? sz : '';
      }
      var label = s.roles.label || pick(p, ['id', 'category']);
      var color = lowCat(p, [label], 10);
      return { x: x, y: y, color: color, size: size, label: label };
    },
    draw: function (host, p, sel) {
      var xc = col(p, sel.x), yc = col(p, sel.y); if (!xc || !yc) throw new Error('fields');
      var cc = sel.color ? col(p, sel.color) : null, sc = sel.size ? col(p, sel.size) : null, lc = sel.label ? col(p, sel.label) : null;
      var groups = cc ? keysOf(cc).slice(0, 12) : ['__all__'];
      var smax = sc && sc.stats ? Math.max(sc.stats.max, 0) : 0;
      var pts = {};
      groups.forEach(function (g) { pts[g] = []; });
      var n = p.rowCount;
      for (var i = 0; i < n; i++) {
        var x = xc.values[i], y = yc.values[i]; if (x === null || y === null) continue;
        var g = cc ? cc.values[i] : '__all__'; if (!pts[g]) continue;
        var pt = { x: x, y: y, label: lc ? lc.values[i] : null };
        if (sc) { var sv = sc.values[i]; if (sv === null || sv < 0) continue; pt.size = sv; pt.r = smax ? Math.max(2, 28 * Math.sqrt(sv / smax)) : 4; }
        pts[g].push(pt);
      }
      var datasets = groups.map(function (g, i) {
        var c = PALETTE[i % PALETTE.length];
        return { label: g === '__all__' ? yc.name : labelOf(cc, g), data: pts[g], backgroundColor: colorAlpha(c, sc ? 0.55 : 0.8), borderColor: c, pointRadius: 5, pointHoverRadius: 7 };
      });
      if (sc) note(host, lang() === 'zh' ? '氣泡面積 ∝ ' + sc.name + '（半徑取平方根，避免誇大）。' : 'Bubble area ∝ ' + sc.name + ' (radius = sqrt).');
      return newChart(chartBox(host, 440), { type: sc ? 'bubble' : 'scatter', data: { datasets: datasets }, options: baseOptions({
        plugins: { legend: { display: !!cc }, tooltip: { callbacks: { label: function (c) { var d = c.raw; return (d.label ? d.label + '｜' : '') + xc.name + ' ' + fmt(d.x) + '，' + yc.name + ' ' + fmt(d.y) + (sc ? '，' + sc.name + ' ' + fmt(d.size) : ''); } } } },
        scales: { x: { type: 'linear', title: { display: true, text: xc.name } }, y: { type: 'linear', title: { display: true, text: yc.name } } }
      }) });
    }
  };

  // ---- histogram
  R.histogram = {
    key: 'histogram', zh: '直方圖（分布初探）', en: 'Histogram', pattern: 'boxplot-summary', sample: 'sample-boxplot.csv, sample-spiral.csv',
    fields: [
      { key: 'value', zh: '數值', en: 'Value', types: ['number'] },
      { key: 'group', zh: '分組（可選）', en: 'Group (optional)', types: ['category', 'boolean'], optional: true }
    ],
    options: [{ key: 'bins', zh: '分箱數', en: 'Bins', choices: ['auto', '5', '10', '20', '30'], labels: { auto: { zh: '自動（Sturges）', en: 'auto (Sturges)' } }, def: 'auto' }],
    auto: function (p, s) { return { value: bestMeasure(p, s), group: s.hints.repeatedGroups ? (s.roles.group || '') : '', bins: 'auto' }; },
    draw: function (host, p, sel) {
      var vc = col(p, sel.value); if (!vc) throw new Error('value');
      var gc = sel.group ? col(p, sel.group) : null;
      var b = bins(vc.values, sel.bins === 'auto' ? 0 : +sel.bins);
      var labels = b.map(function (x) { return fmt(x.x0) + '–' + fmt(x.x1); });
      var datasets;
      if (gc) {
        var step = b.length ? b[0].x1 - b[0].x0 : 1, start = b.length ? b[0].x0 : 0;
        datasets = keysOf(gc).slice(0, 8).map(function (g, i) {
          var counts = b.map(function () { return 0; });
          vc.values.forEach(function (v, r) { if (v === null || gc.values[r] !== g) return; var k = Math.min(b.length - 1, Math.floor((v - start) / step)); if (k >= 0) counts[k]++; });
          return { label: labelOf(gc, g), data: counts, backgroundColor: colorAlpha(PALETTE[i % PALETTE.length], 0.75) };
        });
      } else datasets = [{ label: vc.name, data: b.map(function (x) { return x.count; }), backgroundColor: colorAlpha(PALETTE[0], 0.8) }];
      return newChart(chartBox(host, 400), { type: 'bar', data: { labels: labels, datasets: datasets }, options: baseOptions({
        plugins: { legend: { display: !!gc }, tooltip: { callbacks: { label: function (c) { return c.dataset.label + '：' + c.parsed.y + (lang() === 'zh' ? ' 筆' : ''); } } } },
        scales: { x: { stacked: !!gc, title: { display: true, text: vc.name }, grid: { display: false } }, y: { stacked: !!gc, beginAtZero: true, title: { display: true, text: lang() === 'zh' ? '筆數' : 'count' }, ticks: { precision: 0 } } },
        datasets: { bar: { categoryPercentage: 1, barPercentage: 0.96 } }
      }) });
    }
  };

  // ---- box plot (canvas)
  R.boxplot = {
    key: 'boxplot', zh: '箱形圖', en: 'Box plot', pattern: 'boxplot-summary', sample: 'sample-boxplot.csv',
    fields: [
      { key: 'group', zh: '分組（可選）', en: 'Group (optional)', types: ['category', 'boolean', 'id'], optional: true },
      { key: 'value', zh: '數值', en: 'Value', types: ['number'] }
    ],
    options: [{ key: 'points', zh: '顯示原始點', en: 'Show points', choices: ['no', 'yes'], labels: { no: { zh: '否（只點離群）', en: 'no (outliers only)' }, yes: { zh: '是（抖動）', en: 'yes (jitter)' } }, def: 'no' }],
    auto: function (p, s) { return { group: s.roles.group || lowCat(p, [], 15), value: bestMeasure(p, s), points: 'no' }; },
    draw: function (host, p, sel) {
      var vc = col(p, sel.value); if (!vc) throw new Error('value');
      var gc = sel.group ? col(p, sel.group) : null;
      var groups = (gc ? keysOf(gc).slice(0, 20) : ['__all__']).map(function (g, i) {
        var vals = vc.values.filter(function (v, r) { return v !== null && (!gc || gc.values[r] === g); });
        return { key: g, label: g === '__all__' ? vc.name : labelOf(gc, g), stats: boxStats(vals), color: PALETTE[i % PALETTE.length], hidden: false };
      }).filter(function (g) { return g.stats; });
      var panel;
      legendChips(host, groups, function () { panel.repaint(); });
      panel = canvasPanel(host, 420, function (ctx, w, h) {
        var vis = groups.filter(function (g) { return !g.hidden; });
        var regions = [];
        var m = { l: 64, r: 16, t: 16, b: 48 };
        var all = []; vis.forEach(function (g) { all.push(g.stats.min, g.stats.max); });
        if (!all.length) return regions;
        var ticks = niceTicks(Math.min.apply(null, all), Math.max.apply(null, all), 6);
        var y0 = ticks[0], y1 = ticks[ticks.length - 1];
        var Y = function (v) { return m.t + (h - m.t - m.b) * (1 - (v - y0) / (y1 - y0 || 1)); };
        ctx.strokeStyle = '#e3e6ea'; ctx.fillStyle = '#555'; ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
        ticks.forEach(function (t) { var y = Y(t); ctx.beginPath(); ctx.moveTo(m.l, y); ctx.lineTo(w - m.r, y); ctx.stroke(); ctx.fillText(fmt(t), m.l - 6, y); });
        ctx.save(); ctx.translate(14, (h - m.b + m.t) / 2); ctx.rotate(-Math.PI / 2); ctx.textAlign = 'center'; ctx.fillText(vc.name, 0, 0); ctx.restore();
        var bw = (w - m.l - m.r) / vis.length;
        vis.forEach(function (g, i) {
          var s = g.stats, cx = m.l + bw * (i + 0.5), half = Math.min(40, bw * 0.3);
          ctx.strokeStyle = '#333'; ctx.lineWidth = 1.2;
          ctx.beginPath(); ctx.moveTo(cx, Y(s.whiskerLow)); ctx.lineTo(cx, Y(s.q1)); ctx.moveTo(cx, Y(s.q3)); ctx.lineTo(cx, Y(s.whiskerHigh));
          ctx.moveTo(cx - half / 2, Y(s.whiskerLow)); ctx.lineTo(cx + half / 2, Y(s.whiskerLow)); ctx.moveTo(cx - half / 2, Y(s.whiskerHigh)); ctx.lineTo(cx + half / 2, Y(s.whiskerHigh)); ctx.stroke();
          ctx.fillStyle = colorAlpha(g.color, 0.35); ctx.fillRect(cx - half, Y(s.q3), half * 2, Y(s.q1) - Y(s.q3)); ctx.strokeRect(cx - half, Y(s.q3), half * 2, Y(s.q1) - Y(s.q3));
          ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(cx - half, Y(s.median)); ctx.lineTo(cx + half, Y(s.median)); ctx.stroke(); ctx.lineWidth = 1;
          var dots = sel.points === 'yes' ? s.values : s.outliers;
          dots.forEach(function (v, j) {
            var jx = sel.points === 'yes' ? cx + (((j * 9301 + 49297) % 233280) / 233280 - 0.5) * half * 1.4 : cx;
            var isOut = s.outliers.indexOf(v) >= 0;
            ctx.fillStyle = isOut ? '#e15759' : colorAlpha('#333333', 0.55);
            ctx.beginPath(); ctx.arc(jx, Y(v), isOut ? 3.5 : 2.5, 0, Math.PI * 2); ctx.fill();
            if (isOut) regions.push({ x: jx - 5, y: Y(v) - 5, w: 10, h: 10, lines: [g.label + (lang() === 'zh' ? '｜離群值' : ' | outlier'), fmt(v)] });
          });
          ctx.fillStyle = '#333'; ctx.textAlign = 'center'; ctx.textBaseline = 'top';
          ctx.fillText(g.label, cx, h - m.b + 8); ctx.fillStyle = '#888'; ctx.fillText('n=' + s.n, cx, h - m.b + 24);
          regions.unshift({ x: cx - half, y: Y(s.whiskerHigh), w: half * 2, h: Y(s.whiskerLow) - Y(s.whiskerHigh), lines: [g.label + '（n=' + s.n + '）',
            (lang() === 'zh' ? '最大 ' : 'max ') + fmt(s.max), 'Q3 ' + fmt(s.q3), (lang() === 'zh' ? '中位數 ' : 'median ') + fmt(s.median), 'Q1 ' + fmt(s.q1), (lang() === 'zh' ? '最小 ' : 'min ') + fmt(s.min),
            (lang() === 'zh' ? '離群 ' : 'outliers ') + (s.outliers.length ? s.outliers.map(fmt).join(', ') : '—')] });
        });
        return regions;
      });
      note(host, lang() === 'zh' ? '箱＝Q1–Q3，粗線＝中位數，鬚＝1.5×IQR 內的極值，紅點＝離群。點上方標籤可隱藏組別。' : 'Box = Q1–Q3, thick line = median, whiskers = 1.5×IQR, red = outliers. Click chips to hide groups.');
      return panel;
    }
  };

  // ---- matrix drawing shared by heatmap + adjacency
  function drawMatrix(host, M, opts) {
    // M: { rows:[label], cols:[label], cells:[[v|null]], rowTitle, colTitle, valueTitle }
    var vals = []; M.cells.forEach(function (r) { r.forEach(function (v) { if (v !== null && v !== undefined) vals.push(v); }); });
    var min = vals.length ? Math.min.apply(null, vals) : 0, max = vals.length ? Math.max.apply(null, vals) : 1;
    var scale = colorScale(opts.zeroBase && min > 0 ? 0 : min, max);
    var maxRowLabel = Math.max.apply(null, M.rows.map(function (r) { return String(r).length; }).concat([2]));
    var cellH = M.rows.length > 30 ? 14 : 28;
    var height = Math.max(200, M.rows.length * cellH + 60 + Math.min(120, 20 + Math.max.apply(null, M.cols.map(function (c) { return String(c).length; }).concat([2])) * 7));
    var legend = el('div', { class: 'color-legend' });
    var bar = el('span', { class: 'bar' });
    var stops = []; for (var i = 0; i <= 10; i++) stops.push(scale.color(scale.min + (scale.max - scale.min) * i / 10));
    bar.style.background = 'linear-gradient(to right,' + stops.join(',') + ')';
    legend.appendChild(el('span', null, fmt(scale.min))); legend.appendChild(bar); legend.appendChild(el('span', null, fmt(scale.max)));
    legend.appendChild(el('span', { class: 'muted' }, (M.valueTitle || '') + (scale.diverging ? (lang() === 'zh' ? '（發散色階，中點 0）' : ' (diverging, midpoint 0)') : (lang() === 'zh' ? '（循序色階）' : ' (sequential)'))));
    var missingSw = el('span', { class: 'swatch missing' }); legend.appendChild(missingSw); legend.appendChild(el('span', { class: 'muted' }, lang() === 'zh' ? '無資料' : 'no data'));
    host.appendChild(legend);
    return canvasPanel(host, height, function (ctx, w, h) {
      var regions = [];
      var labelW = Math.min(180, maxRowLabel * 13 + 12);
      var colLabelMax = Math.max.apply(null, M.cols.map(function (c) { return String(c).length; }).concat([2]));
      var rotate = (w - labelW - 12) / M.cols.length < colLabelMax * 13 + 8;
      var m = { l: labelW, r: 12, t: rotate ? Math.min(120, 20 + colLabelMax * 7) : 30, b: 10 };
      var cw = (w - m.l - m.r) / M.cols.length, ch = (h - m.t - m.b) / M.rows.length;
      ctx.textBaseline = 'middle';
      M.rows.forEach(function (rl, ri) {
        ctx.fillStyle = '#333'; ctx.textAlign = 'right';
        ctx.fillText(String(rl), m.l - 6, m.t + ch * (ri + 0.5));
        M.cols.forEach(function (cl, ci) {
          var v = M.cells[ri][ci], x = m.l + cw * ci, y = m.t + ch * ri;
          if (v === null || v === undefined) {
            ctx.fillStyle = '#f1f2f4'; ctx.fillRect(x + 0.5, y + 0.5, cw - 1, ch - 1);
            ctx.strokeStyle = '#d5d8dc'; ctx.beginPath(); ctx.moveTo(x + 2, y + ch - 2); ctx.lineTo(x + cw - 2, y + 2); ctx.stroke();
          } else {
            var c = scale.color(v); ctx.fillStyle = c; ctx.fillRect(x + 0.5, y + 0.5, cw - 1, ch - 1);
            if (opts.annotate && cw >= 30 && ch >= 16) { ctx.fillStyle = textColorFor(c); ctx.textAlign = 'center'; ctx.fillText(fmt(v), x + cw / 2, y + ch / 2); }
          }
          var lines = [M.rowTitle + '：' + rl, M.colTitle + '：' + cl, (M.valueTitle || '') + '：' + (v === null || v === undefined ? (lang() === 'zh' ? '無資料' : 'no data') : fmt(v))];
          if (opts.extra) { var ex = opts.extra(ri, ci); if (ex) lines.push(ex); }
          regions.push({ x: x, y: y, w: cw, h: ch, lines: lines });
        });
      });
      ctx.fillStyle = '#333';
      M.cols.forEach(function (cl, ci) {
        var x = m.l + cw * (ci + 0.5);
        ctx.save();
        if (rotate) { ctx.translate(x, m.t - 6); ctx.rotate(-Math.PI / 3); ctx.textAlign = 'left'; ctx.fillText(String(cl), 0, 0); }
        else { ctx.textAlign = 'center'; ctx.fillText(String(cl), x, m.t - 10); }
        ctx.restore();
      });
      return regions;
    });
  }

  // ---- matrix heatmap
  R.heatmap = {
    key: 'heatmap', zh: '矩陣熱圖', en: 'Matrix heatmap', pattern: 'matrix-heatmap', sample: 'sample-heatmap.csv',
    fields: [
      { key: 'row', zh: '列（類別）', en: 'Rows (category)', types: LABEL_TYPES },
      { key: 'col', zh: '欄（類別）', en: 'Columns (category)', types: LABEL_TYPES },
      { key: 'value', zh: '數值（空＝計數）', en: 'Value (empty = count)', types: ['number'], optional: true }
    ],
    options: [
      { key: 'agg', zh: '聚合', en: 'Aggregate', choices: AGG_CHOICES.slice(0, 5), labels: AGG_LABELS, def: 'mean' },
      { key: 'norm', zh: '正規化', en: 'Normalise', choices: ['none', 'row', 'col'], labels: { none: { zh: '不正規化', en: 'none' }, row: { zh: '依列（列內 %）', en: 'by row (%)' }, col: { zh: '依欄（欄內 %）', en: 'by column (%)' } }, def: 'none' },
      { key: 'order', zh: '排序', en: 'Order', choices: ['original', 'total'], labels: { original: { zh: '原始順序', en: 'original' }, total: { zh: '依總和', en: 'by total' } }, def: 'original' },
      { key: 'annotate', zh: '格內數字', en: 'Cell labels', choices: ['on', 'off'], labels: { on: { zh: '顯示', en: 'on' }, off: { zh: '隱藏', en: 'off' } }, def: 'on' }
    ],
    auto: function (p, s) {
      var ct = s.roles.crossTab || [];
      var row = ct[0] || pick(p, ['category']), c = ct[1] || pick(p, ['category'], [row]);
      return { row: row, col: c, value: bestMeasure(p, s, [row, c]), agg: 'mean', norm: 'none', order: 'original', annotate: 'on' };
    },
    draw: function (host, p, sel) {
      var rc = col(p, sel.row), cc = col(p, sel.col); if (!rc || !cc) throw new Error('fields');
      var vc = sel.value ? col(p, sel.value) : null;
      var agg = aggregate(rc.values, cc.values, vc ? vc.values : null, sel.agg);
      var rk = keysOf(rc), ck = keysOf(cc);
      var cells = rk.map(function (r) { return ck.map(function (c) { var v = agg[r + '\u0001' + c]; return v === undefined ? null : v; }); });
      if (sel.order === 'total') {
        var rt = rk.map(function (_, i) { return cells[i].reduce(function (a, v) { return a + (v || 0); }, 0); });
        var idx = rk.map(function (_, i) { return i; }).sort(function (a, b) { return rt[b] - rt[a]; });
        rk = idx.map(function (i) { return rk[i]; }); cells = idx.map(function (i) { return cells[i]; });
        var ctot = ck.map(function (_, j) { return cells.reduce(function (a, r) { return a + (r[j] || 0); }, 0); });
        var cidx = ck.map(function (_, j) { return j; }).sort(function (a, b) { return ctot[b] - ctot[a]; });
        ck = cidx.map(function (j) { return ck[j]; }); cells = cells.map(function (r) { return cidx.map(function (j) { return r[j]; }); });
      }
      var raw = cells.map(function (r) { return r.slice(); });
      if (sel.norm === 'row') cells = cells.map(function (r) { var t = r.reduce(function (a, v) { return a + (v || 0); }, 0); return r.map(function (v) { return v === null ? null : (t ? v / t * 100 : 0); }); });
      if (sel.norm === 'col') { var ct2 = ck.map(function (_, j) { return cells.reduce(function (a, r) { return a + (r[j] || 0); }, 0); }); cells = cells.map(function (r) { return r.map(function (v, j) { return v === null ? null : (ct2[j] ? v / ct2[j] * 100 : 0); }); }); }
      if (rk.length * ck.length > 2500) note(host, lang() === 'zh' ? '矩陣很大（' + rk.length + '×' + ck.length + '），建議先篩選或分群。' : 'Large matrix; consider filtering.');
      var vTitle = sel.norm !== 'none' ? '%' : (vc ? vc.name + (sel.agg !== 'sum' ? '（' + L(AGG_LABELS[sel.agg]) + '）' : '') : L({ zh: '計數', en: 'count' }));
      return drawMatrix(host, { rows: rk.map(function (k) { return labelOf(rc, k); }), cols: ck.map(function (k) { return labelOf(cc, k); }), cells: cells, rowTitle: rc.name, colTitle: cc.name, valueTitle: vTitle },
        { annotate: sel.annotate === 'on', extra: sel.norm !== 'none' ? function (ri, ci) { return (lang() === 'zh' ? '原值：' : 'raw: ') + fmt(raw[ri][ci]); } : null });
    }
  };

  // ---- adjacency matrix
  R.adjacency = {
    key: 'adjacency', zh: '鄰接矩陣', en: 'Adjacency matrix', pattern: 'adjacency-matrix', sample: 'sample-biofabric.csv',
    fields: [
      { key: 'source', zh: '來源節點', en: 'Source', types: ['category', 'id'] },
      { key: 'target', zh: '去向節點', en: 'Target', types: ['category', 'id'] },
      { key: 'weight', zh: '權重（空＝邊數）', en: 'Weight (empty = edge count)', types: ['number'], optional: true }
    ],
    options: [
      { key: 'direction', zh: '方向', en: 'Direction', choices: ['undirected', 'directed'], labels: { undirected: { zh: '無向（對稱）', en: 'undirected' }, directed: { zh: '有向', en: 'directed' } }, def: 'undirected' },
      { key: 'order', zh: '節點排序', en: 'Node order', choices: ['alpha', 'degree', 'appearance'], labels: { alpha: { zh: '名稱（同前綴成群）', en: 'name (groups prefixes)' }, degree: { zh: '連線數', en: 'degree' }, appearance: { zh: '出現順序', en: 'appearance' } }, def: 'alpha' }
    ],
    auto: function (p, s) {
      var src = s.roles.source || pick(p, ['category', 'id']), tgt = s.roles.target || pick(p, ['category', 'id'], [src]);
      return { source: src, target: tgt, weight: bestMeasure(p, s, []), direction: 'undirected', order: 'alpha' };
    },
    draw: function (host, p, sel) {
      var sc = col(p, sel.source), tc = col(p, sel.target); if (!sc || !tc) throw new Error('fields');
      var wc = sel.weight ? col(p, sel.weight) : null;
      var nodes = [], seen = {}, deg = {};
      for (var i = 0; i < p.rowCount; i++) [sc.values[i], tc.values[i]].forEach(function (v) { if (v !== null && !seen[v]) { seen[v] = 1; nodes.push(v); deg[v] = 0; } });
      var M = {}, edges = {};
      for (var r = 0; r < p.rowCount; r++) {
        var a = sc.values[r], b = tc.values[r]; if (a === null || b === null) continue;
        var w = wc ? (wc.values[r] === null ? 0 : wc.values[r]) : 1;
        deg[a]++; deg[b]++;
        var pairs = sel.direction === 'directed' ? [[a, b]] : (a === b ? [[a, b]] : [[a, b], [b, a]]);
        pairs.forEach(function (pr) { var k = pr[0] + '\u0001' + pr[1]; M[k] = (M[k] || 0) + w; edges[k] = (edges[k] || 0) + 1; });
      }
      if (sel.order === 'alpha') nodes.sort(function (x, y) { return String(x).localeCompare(String(y)); });
      if (sel.order === 'degree') nodes.sort(function (x, y) { return deg[y] - deg[x]; });
      var cells = nodes.map(function (a) { return nodes.map(function (b) { var v = M[a + '\u0001' + b]; return v === undefined ? null : v; }); });
      note(host, (lang() === 'zh' ? '節點 ' + nodes.length + '、邊 ' + p.rowCount + '。灰斜線＝無邊；' + (sel.direction === 'undirected' ? '無向：矩陣對稱。' : '有向：列＝來源、欄＝去向。') : nodes.length + ' nodes, ' + p.rowCount + ' edges. Grey = no edge.'));
      return drawMatrix(host, { rows: nodes.map(String), cols: nodes.map(String), cells: cells, rowTitle: sc.name, colTitle: tc.name, valueTitle: wc ? wc.name : (lang() === 'zh' ? '邊數' : 'edges') },
        { annotate: nodes.length <= 20, zeroBase: true, extra: function (ri, ci) { var k = nodes[ri] + '\u0001' + nodes[ci]; return edges[k] ? (lang() === 'zh' ? '邊數：' : 'edges: ') + edges[k] : null; } });
    }
  };

  // ---- population pyramid
  R.pyramid = {
    key: 'pyramid', zh: '人口金字塔', en: 'Population pyramid', pattern: 'population-pyramid', sample: 'population-pyramid-long.csv, population-pyramid-wide.csv',
    fields: [
      { key: 'age', zh: '年齡組', en: 'Age group', types: ['category', 'id'] },
      { key: 'side', zh: '側別（長表，2 值）', en: 'Side (long, 2 values)', types: ['category', 'boolean'], optional: true },
      { key: 'value', zh: '數值（長表）／左側（寬表）', en: 'Value (long) / left (wide)', types: ['number'] },
      { key: 'value2', zh: '右側（寬表）', en: 'Right (wide)', types: ['number'], optional: true }
    ],
    options: [],
    auto: function (p, s) {
      var age = s.roles.age || pick(p, ['category']);
      var side = p.columns.filter(function (c) { return c.type === 'category' && c.name !== age && c.distinct === 2; })[0];
      var ms = measures(p, s).map(function (c) { return c.name; });
      return side ? { age: age, side: side.name, value: ms[0] || '', value2: '' } : { age: age, side: '', value: ms[0] || '', value2: ms[1] || '' };
    },
    draw: function (host, p, sel) {
      var ac = col(p, sel.age); if (!ac) throw new Error('age');
      var ages = keysOf(ac).slice().sort(function (a, b) { var na = parseFloat(String(a)), nb = parseFloat(String(b)); return (isNaN(na) || isNaN(nb)) ? 0 : na - nb; });
      var names, left, right;
      if (sel.side) {
        var sc = col(p, sel.side), vc = col(p, sel.value); if (!sc || !vc) throw new Error('fields');
        var sides = keysOf(sc);
        var ordered = sides.slice().sort(function (a, b) { return /^(m|male|men|男)/i.test(String(a)) ? -1 : /^(m|male|men|男)/i.test(String(b)) ? 1 : 0; });
        var agg = aggregate(ac.values, sc.values, vc.values, 'sum');
        names = ordered.map(function (s) { return labelOf(sc, s); });
        left = ages.map(function (a) { return agg[a + '\u0001' + ordered[0]] || 0; });
        right = ages.map(function (a) { return agg[a + '\u0001' + ordered[1]] || 0; });
      } else {
        var lc = col(p, sel.value), rc = col(p, sel.value2); if (!lc || !rc) throw new Error(lang() === 'zh' ? '寬表需要左右兩個數值欄' : 'wide form needs two numeric columns');
        var la = aggregate(ac.values, null, lc.values, 'sum'), ra = aggregate(ac.values, null, rc.values, 'sum');
        names = [lc.name, rc.name];
        left = ages.map(function (a) { return la[a + '\u0001'] || 0; });
        right = ages.map(function (a) { return ra[a + '\u0001'] || 0; });
      }
      var labels = ages.map(function (a) { return labelOf(ac, a); }).reverse();
      left = left.reverse(); right = right.reverse();
      var mxRaw = Math.max.apply(null, left.concat(right)) || 1; var tk = niceTicks(0, mxRaw, 4); var mx = tk[tk.length - 1];
      return newChart(chartBox(host, Math.max(280, labels.length * 34 + 90)), { type: 'bar', data: { labels: labels, datasets: [
        { label: names[0], data: left.map(function (v) { return -v; }), backgroundColor: PALETTE[0] },
        { label: names[1], data: right, backgroundColor: PALETTE[1] }
      ] }, options: baseOptions({
        indexAxis: 'y',
        plugins: { tooltip: { callbacks: { label: function (c) { return c.dataset.label + '：' + fmt(Math.abs(c.parsed.x)); } } } },
        scales: { x: { stacked: true, min: -mx, max: mx, ticks: { callback: function (v) { return fmt(Math.abs(v)); } } }, y: { stacked: true, title: { display: true, text: ac.name } } }
      }) });
    }
  };

  var ORDER = ['line', 'barSorted', 'barGrouped', 'scatter', 'histogram', 'boxplot', 'heatmap', 'pyramid', 'adjacency'];

  /** Which renderers can work with the current columns (field requirements satisfied). */
  function available(profile) {
    return ORDER.filter(function (k) {
      var used = {};
      return R[k].fields.every(function (f) {
        if (f.optional) return true;
        var c = profile.columns.filter(function (c) { return f.types.indexOf(c.type) >= 0 && !used[c.name]; })[0];
        if (c) used[c.name] = 1;
        return !!c;
      });
    });
  }

  return {
    renderers: R, order: ORDER, available: available,
    aggregate: aggregate, boxStats: boxStats, bins: bins, niceTicks: niceTicks, colorScale: colorScale, fmtDate: fmtDate, keysOf: keysOf,
    PALETTE: PALETTE, AGG_LABELS: AGG_LABELS
  };
});
