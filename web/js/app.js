/* WIDS app controller (browser only). */
(function () {
  'use strict';
  var I = window.WIDS_I18N, t = I.t;
  var IN = window.WIDS_INPUT, TY = window.WIDS_TYPES, RU = window.WIDS_RULES, MD = window.WIDS_MD, CH = window.WIDS_CHARTS;
  var API_MOD = window.WIDS_API, ENT = window.WIDS_ENTITLEMENT;
  var CONTENT = window.WIDS_CONTENT || { patterns: {} };
  var SAMPLES = window.WIDS_SAMPLES || [];
  var GH = 'https://github.com/g0uv4/what-is-the-data-saying/blob/main/skills/what-is-the-data-saying/';

  var state = { parsed: null, source: '', overrides: {}, profile: null, rec: null, pattern: null, renderer: null, preset: null, sel: {}, chart: null, showAll: false, workbook: null, sheetNames: [] };
  var api = API_MOD.createApi();
  var guestQuota = ENT.createGuestQuota();
  function accountsOn() {
    var cfg = window.WIDS_CONFIG;
    return !!(cfg && typeof cfg.accountsEnabled === 'function' && cfg.accountsEnabled());
  }
  var account = {
    accountsEnabled: accountsOn(),
    file: accountsOn() ? !api.canUseApi() : false,
    offline: true,
    me: null,
    remaining: accountsOn() ? guestQuota.remaining() : null,
    message: '',
    busy: false
  };
  var $ = function (id) { return document.getElementById(id); };

  function el(tag, attrs, text) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'class') e.className = attrs[k];
      else if (k.slice(0, 2) === 'on') e.addEventListener(k.slice(2), attrs[k]);
      else e.setAttribute(k, attrs[k]);
    });
    if (text !== undefined && text !== null) e.textContent = text;
    return e;
  }
  function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }
  function lang() { return I.getLang(); }
  function ruleName(rule) { return lang() === 'en' ? rule.en : rule.zh; }

  // ------------------------------------------------------------ static text
  function applyStatic() {
    document.documentElement.lang = lang() === 'en' ? 'en' : 'zh-Hant-TW';
    var nPat = (CONTENT && CONTENT.patternCount) || Object.keys((CONTENT && CONTENT.patterns) || {}).length || 0;
    var nRec = (RU && RU.RULES) ? RU.RULES.filter(function (r) { return !r.teachingOnly; }).length : nPat;
    Array.prototype.forEach.call(document.querySelectorAll('[data-i18n]'), function (n) {
      var key = n.getAttribute('data-i18n');
      n.textContent = (key === 'subtitle' || key === 'showAll') ? t(key, { n: nPat, r: nRec }) : t(key);
    });
    var sel = $('sampleSelect'), cur = sel.value;
    clear(sel);
    sel.appendChild(el('option', { value: '' }, t('samplePick')));
    SAMPLES.forEach(function (s) {
      var pat = s.pattern && CONTENT.patterns[s.pattern] ? CONTENT.patterns[s.pattern].name : '';
      sel.appendChild(el('option', { value: s.file }, s.file + (pat ? '（' + pat + '）' : '')));
    });
    sel.value = cur;
    refreshAccount();
  }

  // ------------------------------------------------------------ entitlement / mock API
  function accountEls() {
    return { bar: $('accountBar'), status: $('planStatus'), login: $('loginBtn'), upgrade: $('upgradeBtn'), logout: $('logoutBtn') };
  }
  function refreshAccount() {
    account.accountsEnabled = accountsOn();
    if (!account.accountsEnabled) {
      ENT.applyAccountUI(accountEls(), { accountsEnabled: false }, t);
      return;
    }
    ENT.applyAccountUI(accountEls(), account, t);
  }
  function isDemoSource(source) {
    return SAMPLES.some(function (s) { return s.file === source; });
  }
  function guestBlocked() {
    return ENT.guestUploadBlocked({
      accountsEnabled: accountsOn(),
      me: account.me,
      remaining: account.remaining
    });
  }
  function quotaMessage(err) {
    var extra = '';
    if (err && err.resetAt) extra = t('quotaReset', { at: err.resetAt });
    else if (err && err.retryAfter) extra = t('quotaRetry', { n: err.retryAfter });
    return t('quotaExceeded') + extra;
  }
  function loadMe() {
    if (!accountsOn()) {
      account.file = false;
      account.offline = true;
      account.me = null;
      account.message = '';
      refreshAccount();
      return Promise.resolve({ skipped: true });
    }
    if (!api.canUseApi()) {
      account.file = true;
      account.offline = true;
      account.me = null;
      account.remaining = guestQuota.remaining();
      refreshAccount();
      return Promise.resolve({ skipped: true });
    }
    return api.health().then(function (health) {
      if (health.skipped || !health.json || !health.json.ok) throw new Error('health failed');
      return api.me();
    }).then(function (res) {
      account.file = false;
      account.offline = false;
      account.me = res.json;
      if (account.message === t('apiOffline')) account.message = '';
      var quota = res.json && res.json.entitlement && res.json.entitlement.quota;
      var apiRem = quota ? quota.guest_uploads_remaining_today : undefined;
      guestQuota.syncFromApi(apiRem);
      account.remaining = guestQuota.effectiveRemaining(apiRem);
      refreshAccount();
      return res;
    }).catch(function () {
      account.file = false;
      account.offline = true;
      account.me = null;
      account.remaining = guestQuota.remaining();
      if (!account.message) account.message = t('apiOffline');
      refreshAccount();
    });
  }
  function maybeSaveHistory(source, parsed) {
    if (!ENT.shouldSaveHistory({
      accountsEnabled: accountsOn(),
      canUseApi: api.canUseApi(),
      file: account.file,
      offline: account.offline,
      me: account.me
    })) return Promise.resolve();
    if (!state.pattern || !parsed) return Promise.resolve();
    return api.saveHistory({
      pattern_id: state.pattern,
      source_name: source,
      row_count: parsed.rows.length
    }).then(function () {
      account.message = t('historySaved');
      refreshAccount();
    }).catch(function (err) {
      account.message = err && err.status === 429 ? quotaMessage(err) : t('historyFailed');
      refreshAccount();
    });
  }
  function afterSuccessfulLoad(source, parsed, kind) {
    if (!accountsOn()) return Promise.resolve();
    var next = Promise.resolve();
    if (kind === 'upload' && ENT.isGuest(account.me)) {
      guestQuota.increment();
      account.remaining = guestQuota.remaining();
      refreshAccount();
      if (api.canUseApi() && !account.offline) {
        next = api.consumeGuestUpload('upload').then(function (res) {
          if (res.json && typeof res.json.remaining === 'number') {
            guestQuota.syncFromApi(res.json.remaining);
            account.remaining = guestQuota.effectiveRemaining(res.json.remaining);
            refreshAccount();
          }
        }).catch(function (err) {
          if (err && err.status === 429) {
            guestQuota.syncFromApi(0);
            account.remaining = 0;
            account.message = quotaMessage(err);
            refreshAccount();
          }
        });
      }
    }
    return next.then(function () { return maybeSaveHistory(source, parsed); });
  }

  // ------------------------------------------------------------ data loading
  function hideSheetSelect() {
    var field = $('sheetField');
    if (field) field.hidden = true;
    state.workbook = null;
    state.sheetNames = [];
  }

  function fillSheetSelect(names, selected) {
    var field = $('sheetField'), sel = $('sheetSelect');
    if (!field || !sel) return;
    clear(sel);
    (names || []).forEach(function (name) {
      sel.appendChild(el('option', { value: name }, name));
    });
    sel.value = selected || (names && names[0]) || '';
    field.hidden = !(names && names.length > 1);
  }

  function formatStatus(parsed, source) {
    var delim = parsed.delimiter === '\t' ? 'TAB' : (parsed.format === 'json' || parsed.format === 'xlsx' ? '—' : '「' + parsed.delimiter + '」');
    var msg = source + ' · ' + parsed.rows.length + ' ' + t('rows') + ' × ' + parsed.headers.length + ' ' + t('cols');
    if (parsed.format === 'csv') msg += ' · ' + t('delimiter') + ' ' + delim;
    if (parsed.encoding && parsed.format === 'csv') msg += ' · ' + t('encoding') + ' ' + parsed.encoding.toUpperCase();
    if (parsed.sheetName) msg += ' · ' + t('sheet') + ' ' + parsed.sheetName;
    var rag = (parsed.warnings || []).filter(function (w) { return /^ragged:/.test(w); })[0];
    if (rag) msg += ' · ⚠ ' + t('ragged', { n: rag.split(':')[1] });
    var trunc = (parsed.warnings || []).filter(function (w) { return /^truncated:/.test(w); })[0];
    if (trunc) msg += ' · ⚠ ' + t('truncated', { total: trunc.split(':')[1] });
    return msg;
  }

  function showParseError(err) {
    var status = $('dataStatus');
    status.className = 'status error';
    var msg = err && err.message ? String(err.message) : String(err || '');
    if (/larger than 10 MB/i.test(msg)) status.textContent = t('fileTooLarge');
    else if (/unsupported/i.test(msg)) status.textContent = t('unsupportedType');
    else status.textContent = t('parseError') + msg + ' ' + t('supportedFormats');
  }

  function applyParsed(parsed, source, kind) {
    var status = $('dataStatus');
    status.className = 'status';
    if (!kind) kind = isDemoSource(source) ? 'demo' : 'upload';
    if (!parsed || !parsed.headers.length || !parsed.rows.length) {
      status.textContent = t('emptyCsv');
      status.className = 'status error';
      return false;
    }
    state.parsed = parsed;
    state.source = source;
    if (kind !== 'sheet') {
      state.overrides = {};
      state.pattern = null;
    }
    status.textContent = formatStatus(parsed, source);
    renderPreview();
    recompute(kind !== 'sheet');
    if (kind !== 'sheet') afterSuccessfulLoad(source, parsed, kind);
    return true;
  }

  function loadText(text, source, kind) {
    var status = $('dataStatus');
    status.className = 'status';
    if (!kind) kind = isDemoSource(source) ? 'demo' : 'upload';
    if (kind === 'upload' && guestBlocked()) {
      status.textContent = t('guestLimit');
      status.className = 'status error';
      return;
    }
    if (kind !== 'sheet') hideSheetSelect();
    try {
      applyParsed(IN.parseText(text), source, kind);
    } catch (e) {
      showParseError(e);
    }
  }

  function loadParsedTable(parsed, source, kind) {
    var status = $('dataStatus');
    status.className = 'status';
    if (!kind) kind = isDemoSource(source) ? 'demo' : 'upload';
    if (kind === 'upload' && guestBlocked()) {
      status.textContent = t('guestLimit');
      status.className = 'status error';
      return;
    }
    try {
      applyParsed(parsed, source, kind);
    } catch (e) {
      showParseError(e);
    }
  }

  function loadFile(file) {
    var status = $('dataStatus');
    status.className = 'status';
    if (guestBlocked()) {
      status.textContent = t('guestLimit');
      status.className = 'status error';
      return;
    }
    if (file.size > IN.MAX_BYTES) {
      status.textContent = t('fileTooLarge');
      status.className = 'status error';
      return;
    }
    hideSheetSelect();
    var rd = new FileReader();
    rd.onload = function () {
      try {
        var parsed = IN.parseFile(file.name, rd.result);
        if (parsed.workbook && parsed.sheetNames && parsed.sheetNames.length) {
          state.workbook = parsed.workbook;
          state.sheetNames = parsed.sheetNames;
          fillSheetSelect(parsed.sheetNames, parsed.sheetName);
        } else {
          hideSheetSelect();
        }
        loadParsedTable(parsed, file.name, 'upload');
      } catch (e) {
        hideSheetSelect();
        showParseError(e);
      }
    };
    rd.onerror = function () { showParseError(rd.error || new Error('read failed')); };
    rd.readAsArrayBuffer(file);
  }

  function renderPreview() {
    var host = $('preview'); clear(host);
    if (!state.parsed) return;
    host.appendChild(el('div', { class: 'muted small' }, t('preview')));
    var tb = el('table', { class: 'grid' }), thead = el('thead'), tr = el('tr');
    state.parsed.headers.forEach(function (h) { tr.appendChild(el('th', null, h)); });
    thead.appendChild(tr); tb.appendChild(thead);
    var body = el('tbody');
    state.parsed.rows.slice(0, 8).forEach(function (r) { var row = el('tr'); r.forEach(function (c) { row.appendChild(el('td', null, c)); }); body.appendChild(row); });
    tb.appendChild(body); host.appendChild(tb);
  }

  // ------------------------------------------------------------ profile + rec
  function recompute(fresh) {
    if (!state.parsed) return;
    state.profile = TY.profileTable(state.parsed, state.overrides);
    state.rec = RU.recommend(state.profile, lang());
    renderColumns();
    renderRecs();
    if (fresh || !state.pattern) {
      var top = state.rec.results.filter(function (r) { return r.eligible; })[0];
      selectPattern(top ? top.id : null);
    } else {
      selectPattern(state.pattern, state.renderer, state.preset);
    }
  }

  function renderColumns() {
    var host = $('columns'); clear(host);
    if (!state.profile) { host.appendChild(el('p', { class: 'muted' }, t('noData'))); return; }
    var tb = el('table', { class: 'grid cols' }), tr = el('tr');
    ['colName', 'colType', 'colMissing', 'colDistinct', 'colSamples'].forEach(function (k) { tr.appendChild(el('th', null, t(k))); });
    var thead = el('thead'); thead.appendChild(tr); tb.appendChild(thead);
    var body = el('tbody');
    state.profile.columns.forEach(function (c) {
      var row = el('tr');
      row.appendChild(el('td', { class: 'mono' }, c.name));
      var td = el('td'), s = el('select', { 'aria-label': c.name, class: 'type-' + c.type });
      TY.TYPES.forEach(function (ty) {
        var o = el('option', { value: ty }, t('t_' + ty) + (ty === c.inferred ? ' · ' + t('inferred') : ''));
        if (ty === c.type) o.selected = true;
        s.appendChild(o);
      });
      s.addEventListener('change', function () { state.overrides[c.name] = s.value; recompute(false); });
      td.appendChild(s);
      if (c.type === 'date' && c.granularity) td.appendChild(el('span', { class: 'muted small' }, ' ' + c.granularity));
      row.appendChild(td);
      row.appendChild(el('td', { class: c.missing ? 'warn num' : 'num' }, String(c.missing)));
      row.appendChild(el('td', { class: 'num' }, String(c.distinct)));
      row.appendChild(el('td', { class: 'samples' }, c.samples.join('、')));
      body.appendChild(row);
    });
    tb.appendChild(body); host.appendChild(tb);
  }

  function renderRecs() {
    var list = $('recList'); clear(list);
    var hints = $('shapeHints'); clear(hints);
    if (!state.rec) { $('recCount').textContent = ''; return; }
    var hk = Object.keys(state.rec.shape.hints);
    if (hk.length) {
      hints.appendChild(el('span', { class: 'muted small' }, t('shapeHints') + '：'));
      hk.forEach(function (k) { var h = RU.HINTS[k]; if (h) hints.appendChild(el('span', { class: 'hint-chip' }, lang() === 'en' ? h.en : h.zh)); });
    }
    var results = state.rec.results;
    var eligible = results.filter(function (r) { return r.eligible; });
    $('recCount').textContent = t('eligibleN', { n: eligible.length, total: results.length });
    (state.showAll ? results : eligible).forEach(function (r, i) {
      var li = el('li', { class: 'rec' + (r.eligible ? '' : ' ineligible') + (r.id === state.pattern ? ' active' : '') });
      var btn = el('button', { type: 'button', class: 'rec-btn', onclick: function () { selectPattern(r.id); } });
      var head = el('div', { class: 'rec-head' });
      head.appendChild(el('span', { class: 'rank' }, r.eligible ? String(i + 1) : '–'));
      head.appendChild(el('span', { class: 'rec-name' }, ruleName(r.rule)));
      head.appendChild(el('span', { class: 'badge ' + (r.renderable ? 'ok' : 'teach') }, r.renderable ? t('canDraw') : t('teachOnly')));
      if (r.eligible) {
        var meter = el('span', { class: 'meter', title: t('score') + ' ' + r.score });
        var fill = el('span'); fill.style.width = r.score + '%'; meter.appendChild(fill);
        head.appendChild(meter);
      }
      btn.appendChild(head);
      btn.appendChild(el('div', { class: 'rec-fields small' }, t('fields') + '：' + (lang() === 'en' ? r.rule.fields.en : r.rule.fields.zh) + ' · ' + r.id + '.md'));
      var why = el('ul', { class: 'rec-why small' });
      r.reasons.forEach(function (x) { why.appendChild(el('li', null, x)); });
      if (r.caveats.length) why.appendChild(el('li', { class: 'caveat' }, t('caveat') + r.caveats.join('、')));
      if (!r.eligible && r.missing.length) why.appendChild(el('li', { class: 'caveat' }, t('missingReq') + r.missing.join('、')));
      btn.appendChild(why);
      li.appendChild(btn);
      list.appendChild(li);
    });
  }

  // ------------------------------------------------------------ pattern + chart
  function selectPattern(id, rendererKey, preset) {
    state.pattern = id;
    renderRecsActive();
    var rule = id ? RU.byId(id) : null;
    var avail = state.profile ? CH.available(state.profile) : [];
    if (!rendererKey && rule) {
      var r0 = rule.render.filter(function (r) { return avail.indexOf(r.r) >= 0; })[0];
      if (r0) { rendererKey = r0.r; preset = r0.preset || null; }
    }
    state.sel = {};
    state.renderer = rendererKey || null; state.preset = preset || null;
    renderChartArea();
    renderTutorial(id);
  }
  function renderRecsActive() {
    var items = document.querySelectorAll('#recList .rec');
    var shown = state.rec ? (state.showAll ? state.rec.results : state.rec.results.filter(function (r) { return r.eligible; })) : [];
    Array.prototype.forEach.call(items, function (n, i) { n.classList.toggle('active', shown[i] && shown[i].id === state.pattern); });
  }

  function destroyChart() {
    if (state.chart && state.chart.destroy) { try { state.chart.destroy(); } catch (e) { /* ignore */ } }
    state.chart = null;
  }

  function renderChartArea() {
    var head = $('chartHead'), tabs = $('rendererTabs'), controls = $('controls'), host = $('chartHost');
    clear(head); clear(tabs); clear(controls); destroyChart(); clear(host);
    if (!state.profile) { host.appendChild(el('p', { class: 'muted' }, t('noData'))); return; }
    var rule = state.pattern ? RU.byId(state.pattern) : null;
    var avail = CH.available(state.profile);
    if (rule) {
      var h = el('div', { class: 'chart-title' });
      h.appendChild(el('strong', null, ruleName(rule)));
      h.appendChild(el('span', { class: 'badge ' + (rule.render.length ? 'ok' : 'teach') }, rule.render.length ? t('canDraw') : t('teachOnly')));
      head.appendChild(h);
    } else head.appendChild(el('p', { class: 'muted' }, t('pickPattern')));

    var ruleKeys = rule ? rule.render.map(function (r) { return r.r; }) : [];
    if (rule && !rule.render.length) head.appendChild(el('p', { class: 'notice' }, t('noRenderer')));
    // tabs: pattern's own renderers first, then all others available
    var ordered = ruleKeys.concat(CH.order.filter(function (k) { return ruleKeys.indexOf(k) < 0; }));
    ordered.forEach(function (k) {
      var R = CH.renderers[k];
      var ok = avail.indexOf(k) >= 0;
      var own = ruleKeys.indexOf(k) >= 0;
      var b = el('button', { type: 'button', role: 'tab', class: 'tab' + (k === state.renderer ? ' active' : '') + (own ? ' own' : ''), 'aria-selected': String(k === state.renderer) }, lang() === 'en' ? R.en : R.zh);
      if (!ok) { b.disabled = true; b.title = t('notEligible'); }
      b.addEventListener('click', function () {
        var pr = null;
        if (rule) rule.render.forEach(function (r) { if (r.r === k && r.preset) pr = r.preset; });
        selectPattern(state.pattern, k, pr);
      });
      tabs.appendChild(b);
    });
    if (!state.renderer) return;
    var R = CH.renderers[state.renderer];
    if (!state.sel.__k) { state.sel = R.auto(state.profile, state.rec.shape, state.preset); state.sel.__k = state.renderer; }
    (R.options || []).forEach(function (o) { if (state.sel[o.key] === undefined) state.sel[o.key] = o.def; });
    buildControls(R, controls);
    var meta = el('p', { class: 'muted small' }, (lang() === 'zh' ? '對應範例：' : 'Pattern file: ') + R.pattern + '.md · ' + (lang() === 'zh' ? '驗證資料：' : 'verified with: ') + R.sample);
    host.appendChild(meta);
    draw();
  }

  function buildControls(R, host) {
    var cols = state.profile.columns;
    R.fields.forEach(function (f) {
      var lab = el('label', { class: 'field' });
      lab.appendChild(el('span', null, lang() === 'en' ? f.en : f.zh));
      var s = el('select', { 'data-field': f.key });
      if (f.optional) s.appendChild(el('option', { value: '' }, t('none')));
      if (f.wide) s.appendChild(el('option', { value: '__wide__' }, lang() === 'zh' ? '（全部數值欄＝寬表多系列）' : '(all numeric columns = wide)'));
      cols.forEach(function (c) {
        if (f.types.indexOf(c.type) < 0) return;
        s.appendChild(el('option', { value: c.name }, c.name + '（' + t('t_' + c.type) + '）'));
      });
      s.value = state.sel[f.key] || '';
      s.addEventListener('change', function () { state.sel[f.key] = s.value; draw(); });
      lab.appendChild(s); host.appendChild(lab);
    });
    (R.options || []).forEach(function (o) {
      var lab = el('label', { class: 'field' });
      lab.appendChild(el('span', null, lang() === 'en' ? o.en : o.zh));
      var s = el('select', { 'data-option': o.key });
      o.choices.forEach(function (c) {
        var l = o.labels && o.labels[c] ? (lang() === 'en' ? o.labels[c].en : o.labels[c].zh) : c;
        s.appendChild(el('option', { value: c }, l));
      });
      s.value = state.sel[o.key];
      s.addEventListener('change', function () { state.sel[o.key] = s.value; draw(); });
      lab.appendChild(s); host.appendChild(lab);
    });
  }

  function draw() {
    var host = $('chartHost');
    destroyChart();
    Array.prototype.slice.call(host.children).forEach(function (n) { if (!n.classList.contains('muted')) host.removeChild(n); });
    var R = CH.renderers[state.renderer];
    var missing = R.fields.filter(function (f) { return !f.optional && !state.sel[f.key]; });
    if (missing.length) { host.appendChild(el('p', { class: 'notice' }, (lang() === 'zh' ? '請選擇：' : 'Choose: ') + missing.map(function (f) { return lang() === 'en' ? f.en : f.zh; }).join('、'))); return; }
    var box = el('div', { class: 'chart-inner' });
    host.appendChild(box);
    try {
      state.chart = R.draw(box, state.profile, state.sel);
    } catch (e) {
      box.appendChild(el('p', { class: 'notice error' }, (lang() === 'zh' ? '無法繪圖：' : 'Cannot draw: ') + e.message));
    }
  }

  // ------------------------------------------------------------ tutorial
  function resolveLink(href) {
    var h = String(href).trim();
    if (/^[a-z][a-z0-9+.-]*:/i.test(h)) return { href: h };
    var m = /^(?:\.\/)?([\w-]+)\.md(#.*)?$/.exec(h);
    if (m && CONTENT.patterns[m[1]]) return { internal: m[1] };
    // resolve relative to examples/ on GitHub
    var parts = ('examples/' + h).split('/'), out = [];
    parts.forEach(function (p) { if (p === '..') out.pop(); else if (p !== '.' && p !== '') out.push(p); });
    var path = out.join('/');
    if (path.indexOf('skills/') !== 0 && out.length && !/^(examples|references)\//.test(path)) {
      return { href: 'https://github.com/g0uv4/what-is-the-data-saying/blob/main/' + path.replace(/^(\.\.\/)+/, '') };
    }
    return { href: GH + path };
  }
  function codeLink(code) {
    var m = /^(?:\.\.\/)?(?:examples\/)?([\w-]+)\.md$/.exec(String(code).trim());
    return m && CONTENT.patterns[m[1]] ? m[1] : null;
  }
  function renderTutorial(id) {
    var art = $('tutorial'), meta = $('tutMeta');
    clear(meta); art.innerHTML = '';
    var p = id ? CONTENT.patterns[id] : null;
    if (!p) { art.appendChild(el('p', { class: 'muted' }, t('pickPattern'))); return; }
    meta.appendChild(document.createTextNode(t('tutorial') + ' · ' + p.file + ' · v' + (CONTENT.version || '') + ' · '));
    meta.appendChild(el('a', { href: GH + p.file, target: '_blank', rel: 'noopener noreferrer' }, t('openGithub')));
    art.innerHTML = MD.render(p.md, { resolveLink: resolveLink, codeLink: codeLink }); // MD.render escapes all source text
  }

  // ------------------------------------------------------------ events
  function bind() {
    $('langBtn').addEventListener('click', function () {
      I.setLang(lang() === 'zh' ? 'en' : 'zh');
      applyStatic();
      if (state.parsed) { state.rec = RU.recommend(state.profile, lang()); renderColumns(); renderRecs(); renderChartArea(); }
      else { renderColumns(); renderChartArea(); }
      renderTutorial(state.pattern);
    });
    $('sampleSelect').addEventListener('change', function (e) {
      var s = SAMPLES.filter(function (x) { return x.file === e.target.value; })[0];
      if (s) loadText(s.text, s.file, 'demo');
    });
    $('fileInput').addEventListener('change', function (e) {
      var f = e.target.files && e.target.files[0]; if (!f) return;
      $('sampleSelect').value = '';
      loadFile(f);
    });
    $('sheetSelect').addEventListener('change', function (e) {
      if (!state.workbook) return;
      var table = IN.limitRows(IN.sheetToTable(state.workbook, e.target.value));
      table.workbook = state.workbook;
      table.sheetNames = state.sheetNames;
      loadParsedTable(table, state.source, 'sheet');
    });
    $('parseBtn').addEventListener('click', function () { $('sampleSelect').value = ''; loadText($('pasteArea').value, lang() === 'zh' ? '貼上的文字' : 'pasted text', 'upload'); });
    $('loginBtn').addEventListener('click', function () {
      account.busy = true; account.message = ''; refreshAccount();
      api.loginGithub().then(function () {
        account.message = '';
        return loadMe();
      }).catch(function () {
        account.message = t('loginFailed');
      }).then(function () {
        account.busy = false;
        refreshAccount();
      });
    });
    $('upgradeBtn').addEventListener('click', function () {
      account.busy = true; account.message = ''; refreshAccount();
      api.upgrade().then(function () {
        account.message = t('upgradeOk');
        return loadMe();
      }).catch(function (err) {
        account.message = err && err.status === 429 ? quotaMessage(err) : t('upgradeFailed');
      }).then(function () {
        account.busy = false;
        refreshAccount();
      });
    });
    $('logoutBtn').addEventListener('click', function () {
      api.logout();
      account.me = null;
      account.message = '';
      loadMe();
    });
    $('showAll').addEventListener('change', function (e) { state.showAll = e.target.checked; renderRecs(); });
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a.md-internal');
      if (a) { e.preventDefault(); selectPattern(a.getAttribute('data-pattern')); $('chartCard').scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    });
  }

  function fromHash() {
    var q = {};
    String(location.hash || '').replace(/^#/, '').split('&').forEach(function (kv) { var p = kv.split('='); if (p[0]) q[decodeURIComponent(p[0])] = decodeURIComponent(p[1] || ''); });
    if (q.lang === 'en') { I.setLang('en'); applyStatic(); }
    if (q.sample) {
      var s = SAMPLES.filter(function (x) { return x.file === q.sample; })[0];
      if (s) { $('sampleSelect').value = s.file; loadText(s.text, s.file, 'demo'); }
    }
    if (q.pattern && CONTENT.patterns[q.pattern]) selectPattern(q.pattern, q.renderer && CH.renderers[q.renderer] ? q.renderer : undefined);
  }

  function stripAuthFromAddress() {
    if (typeof location === 'undefined') return;
    try {
      api.stripAuthParams(location.href, function (_state, _title, next) {
        history.replaceState(null, '', next);
      });
    } catch (e) { /* ignore */ }
  }

  function afterAuthRedirect() {
    if (typeof location === 'undefined') return Promise.resolve();
    return api.consumeAuthCodeFromSearch(location.search, location.href, function (_state, _title, next) {
      try { history.replaceState(null, '', next); } catch (e) { /* ignore */ }
    }).catch(function () {
      stripAuthFromAddress();
    });
  }

  applyStatic();
  bind();
  renderColumns();
  renderChartArea();
  renderTutorial(null);
  if (accountsOn()) {
    afterAuthRedirect().then(function () { return loadMe(); }).then(function () { fromHash(); });
  } else {
    stripAuthFromAddress();
    fromHash();
  }
  window.WIDS_APP = { state: state, loadText: loadText, loadFile: loadFile, selectPattern: selectPattern, api: api, account: account, accountsEnabled: accountsOn };
})();
