/* WIDS UI strings (zh-TW default, English optional). */
(function (root) {
  'use strict';
  var S = {
    zh: {
      title: '資料在說什麼？', subtitle: '上傳 CSV、Excel、JSON → 看欄位型態 → 依資料形狀推薦圖種（{n} 種）→ 互動繪圖 + 教學',
      lang: 'English', step1: '1. 資料', step2: '2. 欄位型態', step3: '3. 推薦圖種', step4: '4. 圖表', step5: '5. 教學',
      sample: '載入示範資料', samplePick: '— 選一個示範 CSV —', upload: '上傳 CSV、Excel、JSON', paste: '或貼上 CSV／JSON 文字', parse: '解析貼上的文字',
      sheet: '工作表', supportedFormats: '支援格式：CSV、Excel（.xlsx／.xls／.ods）、JSON。',
      fileTooLarge: '檔案超過 10 MB。支援格式：CSV、Excel（.xlsx／.xls／.ods）、JSON。',
      unsupportedType: '不支援這個檔案格式。支援格式：CSV、Excel（.xlsx／.xls／.ods）、JSON。',
      truncated: '列數超過 50,000（共 {total} 列），只保留前 50,000 列。',
      encoding: '編碼',
      rows: '列', cols: '欄', delimiter: '分隔符號', preview: '資料預覽（前 8 列）', noData: '尚未載入資料。先選示範資料、上傳檔案或貼上文字。',
      colName: '欄位', colType: '型態', colMissing: '缺值', colDistinct: '相異值', colSamples: '範例值', inferred: '自動判斷',
      t_number: '數值', t_category: '類別', t_date: '日期／時間', t_boolean: '布林', t_id: '識別碼',
      showAll: '顯示全部 {n} 種（含不符合）', showEligible: '只顯示符合的', eligibleN: '符合 {n} 種 / 共 {total} 種',
      canDraw: '可繪圖', teachOnly: '教學可看，繪圖尚未支援', notEligible: '欄位不符', missingReq: '缺：', caveat: '注意：',
      fields: '需求欄位', score: '分數', renderer: '繪法', pickPattern: '在左側推薦清單點一個圖種。', pickRenderer: '其他可用繪法',
      noRenderer: '此圖種尚未支援繪圖；教學內容見「5. 教學」。可改用下列已支援的繪法先看資料：', none: '（無）', count: '計數（列數）',
      tutorial: '教學（來自 repo examples）', openGithub: '在 GitHub 看原始檔', shapeHints: '偵測到的資料形狀',
      footer: '內容來自 g0uv4/what-is-the-data-saying（MIT；教圖內容見 ATTRIBUTION）。分析全部在你的瀏覽器內完成，資料不會離開你的電腦。',
      parseError: '解析失敗：', emptyCsv: '沒有資料列。支援格式：CSV、Excel（.xlsx／.xls／.ods）、JSON。', ragged: '有 {n} 列欄位數與表頭不一致，已補空／截斷。', sampleFor: '示範：',
      loginGithub: '用 GitHub 登入', upgrade: '升級', logout: '登出',
      planGuest: '訪客 · 今日剩餘自貼 {n}/{limit}', planUser: '{login} · {plan}',
      planTrial: '試用', planPro: 'Pro', planFree: '免費',
      apiOffline: '權限 API 未連上（本機請先跑 web/api-mock :8787）',
      apiOfflineFile: 'file:// 不呼叫權限 API',
      guestLimit: '訪客每日自貼已達 3 次上限。請改用示範資料，或用 GitHub 登入。',
      historySaved: '已儲存分析摘要（不含原始檔）', historyFailed: '摘要儲存失敗',
      quotaExceeded: '額度用完。', quotaReset: '重置時間：{at}', quotaRetry: '請 {n} 秒後再試。',
      upgradeOk: '已升級為 Pro', upgradeFailed: '升級失敗', loginFailed: '登入失敗', apiBusy: '處理中…'
    },
    en: {
      title: 'What is the data saying?', subtitle: 'Upload CSV, Excel, or JSON → column types → chart recommendations ({n} patterns) → interactive chart + tutorial',
      lang: '中文', step1: '1. Data', step2: '2. Column types', step3: '3. Recommended charts', step4: '4. Chart', step5: '5. Tutorial',
      sample: 'Load sample data', samplePick: '— pick a sample CSV —', upload: 'Upload CSV, Excel, JSON', paste: 'or paste CSV / JSON text', parse: 'Parse pasted text',
      sheet: 'Sheet', supportedFormats: 'Supported formats: CSV, Excel (.xlsx / .xls / .ods), JSON.',
      fileTooLarge: 'File is larger than 10 MB. Supported formats: CSV, Excel (.xlsx / .xls / .ods), JSON.',
      unsupportedType: 'This file type is not supported. Supported formats: CSV, Excel (.xlsx / .xls / .ods), JSON.',
      truncated: 'More than 50,000 rows ({total} total); keeping the first 50,000.',
      encoding: 'encoding',
      rows: 'rows', cols: 'columns', delimiter: 'delimiter', preview: 'Preview (first 8 rows)', noData: 'No data yet. Load a sample, upload a file or paste text.',
      colName: 'Column', colType: 'Type', colMissing: 'Missing', colDistinct: 'Distinct', colSamples: 'Samples', inferred: 'inferred',
      t_number: 'Number', t_category: 'Category', t_date: 'Date/time', t_boolean: 'Boolean', t_id: 'Identifier',
      showAll: 'Show all {n} (incl. not matching)', showEligible: 'Only matching', eligibleN: '{n} of {total} match',
      canDraw: 'Drawable', teachOnly: 'Tutorial only — drawing not supported yet', notEligible: 'Fields do not match', missingReq: 'Missing: ', caveat: 'Caveat: ',
      fields: 'Fields', score: 'Score', renderer: 'Renderer', pickPattern: 'Pick a chart from the recommendations.', pickRenderer: 'Other renderers',
      noRenderer: 'Drawing for this pattern is not supported yet; see “5. Tutorial”. Explore the data with a supported renderer:', none: '(none)', count: 'Count (rows)',
      tutorial: 'Tutorial (from repo examples, zh-TW)', openGithub: 'View source on GitHub', shapeHints: 'Detected data shape',
      footer: 'Content from g0uv4/what-is-the-data-saying (MIT; see ATTRIBUTION). All analysis is completed in your browser; data never leaves your computer.',
      parseError: 'Parse error: ', emptyCsv: 'No data rows. Supported formats: CSV, Excel (.xlsx / .xls / .ods), JSON.', ragged: '{n} rows had a different field count; padded/truncated.', sampleFor: 'Demo: ',
      loginGithub: 'Sign in with GitHub', upgrade: 'Upgrade', logout: 'Sign out',
      planGuest: 'Guest · self-uploads left today {n}/{limit}', planUser: '{login} · {plan}',
      planTrial: 'Trial', planPro: 'Pro', planFree: 'Free',
      apiOffline: 'Entitlement API is offline (run web/api-mock on :8787 locally)',
      apiOfflineFile: 'file:// does not call the entitlement API',
      guestLimit: 'Guest self-upload limit (3/day) reached. Use a sample, or sign in with GitHub.',
      historySaved: 'Saved analysis summary (no raw file)', historyFailed: 'Could not save summary',
      quotaExceeded: 'Quota exhausted. ', quotaReset: 'Resets at {at}', quotaRetry: 'Retry in {n}s.',
      upgradeOk: 'Upgraded to Pro', upgradeFailed: 'Upgrade failed', loginFailed: 'Sign-in failed', apiBusy: 'Working…'
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
