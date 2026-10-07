/* WIDS UI strings (zh-TW default, English optional). */
(function (root) {
  'use strict';
  var S = {
    zh: {
      title: '資料在說什麼？', subtitle: '上傳 CSV → 看欄位型態 → 依資料形狀推薦圖種（{n} 種）→ 互動繪圖 + 教學',
      lang: 'English', step1: '1. 資料', step2: '2. 欄位型態', step3: '3. 推薦圖種', step4: '4. 圖表', step5: '5. 教學',
      sample: '載入示範資料', samplePick: '— 選一個示範 CSV —', upload: '上傳 CSV 檔', paste: '或貼上 CSV 文字', parse: '解析貼上的文字',
      rows: '列', cols: '欄', delimiter: '分隔符號', preview: '資料預覽（前 8 列）', noData: '尚未載入資料。先選示範資料、上傳檔案或貼上文字。',
      colName: '欄位', colType: '型態', colMissing: '缺值', colDistinct: '相異值', colSamples: '範例值', inferred: '自動判斷',
      t_number: '數值', t_category: '類別', t_date: '日期／時間', t_boolean: '布林', t_id: '識別碼',
      showAll: '顯示全部 {n} 種（含不符合）', showEligible: '只顯示符合的', eligibleN: '符合 {n} 種 / 共 {total} 種',
      canDraw: '可繪圖', teachOnly: '教學可看，繪圖尚未支援', notEligible: '欄位不符', missingReq: '缺：', caveat: '注意：',
      fields: '需求欄位', score: '分數', renderer: '繪法', pickPattern: '在左側推薦清單點一個圖種。', pickRenderer: '其他可用繪法',
      noRenderer: '此圖種尚未支援繪圖；教學內容見「5. 教學」。可改用下列已支援的繪法先看資料：', none: '（無）', count: '計數（列數）',
      tutorial: '教學（來自 repo examples）', openGithub: '在 GitHub 看原始檔', shapeHints: '偵測到的資料形狀',
      footer: '內容來自 g0uv4/what-is-the-data-saying（MIT；教圖內容見 ATTRIBUTION）。純前端，資料不會離開你的電腦。',
      parseError: '解析失敗：', emptyCsv: 'CSV 沒有資料列。', ragged: '有 {n} 列欄位數與表頭不一致，已補空／截斷。', sampleFor: '示範：'
    },
    en: {
      title: 'What is the data saying?', subtitle: 'Upload CSV → column types → chart recommendations ({n} patterns) → interactive chart + tutorial',
      lang: '中文', step1: '1. Data', step2: '2. Column types', step3: '3. Recommended charts', step4: '4. Chart', step5: '5. Tutorial',
      sample: 'Load sample data', samplePick: '— pick a sample CSV —', upload: 'Upload CSV', paste: 'or paste CSV text', parse: 'Parse pasted text',
      rows: 'rows', cols: 'columns', delimiter: 'delimiter', preview: 'Preview (first 8 rows)', noData: 'No data yet. Load a sample, upload a file or paste text.',
      colName: 'Column', colType: 'Type', colMissing: 'Missing', colDistinct: 'Distinct', colSamples: 'Samples', inferred: 'inferred',
      t_number: 'Number', t_category: 'Category', t_date: 'Date/time', t_boolean: 'Boolean', t_id: 'Identifier',
      showAll: 'Show all {n} (incl. not matching)', showEligible: 'Only matching', eligibleN: '{n} of {total} match',
      canDraw: 'Drawable', teachOnly: 'Tutorial only — drawing not supported yet', notEligible: 'Fields do not match', missingReq: 'Missing: ', caveat: 'Caveat: ',
      fields: 'Fields', score: 'Score', renderer: 'Renderer', pickPattern: 'Pick a chart from the recommendations.', pickRenderer: 'Other renderers',
      noRenderer: 'Drawing for this pattern is not supported yet; see “5. Tutorial”. Explore the data with a supported renderer:', none: '(none)', count: 'Count (rows)',
      tutorial: 'Tutorial (from repo examples, zh-TW)', openGithub: 'View source on GitHub', shapeHints: 'Detected data shape',
      footer: 'Content from g0uv4/what-is-the-data-saying (MIT; see ATTRIBUTION). Runs fully in your browser.',
      parseError: 'Parse error: ', emptyCsv: 'CSV has no data rows.', ragged: '{n} rows had a different field count; padded/truncated.', sampleFor: 'Demo: '
    }
  };
  var lang = 'zh';
  function t(key, vars) {
    var s = (S[lang] && S[lang][key]) || S.zh[key] || key;
    if (vars) Object.keys(vars).forEach(function (k) { s = s.replace('{' + k + '}', vars[k]); });
    return s;
  }
  root.WIDS_I18N = { t: t, setLang: function (l) { lang = l === 'en' ? 'en' : 'zh'; }, getLang: function () { return lang; }, strings: S };
})(typeof self !== 'undefined' ? self : this);
