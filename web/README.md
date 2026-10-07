# web/ — 互動網頁 PoC（資料在說什麼？）

把本 repo 的 skill（`skills/what-is-the-data-saying/`）變成一個**純前端單頁**：上傳或貼上 CSV／Excel／JSON → 自動判斷欄位型態 → 依資料形狀從 **69 個圖種 pattern**（與 skill examples 同步） 推薦（排序＋理由）→ 可互動繪圖 → 顯示該圖種的教學 markdown。

- 無後端、無建置步驟即可使用：HTML / CSS / 原生 JS，普通 `<script src>`（不用 ES module、不用 `fetch` 讀本機檔），所以 **直接雙擊 `web/index.html`（file://）就能跑**。
- 第三方依賴都 vendor 在 `vendor/`（授權與版本見 `vendor/README.md`）：Chart.js 4.5.1 UMD、SheetJS Community Edition 0.20.3（Apache-2.0，自架 `xlsx.full.min.js`，來源 https://cdn.sheetjs.com/xlsx-0.20.3/package/dist/xlsx.full.min.js）。不用 CDN、不放寬 CSP `script-src`；不用日期 adapter（時間一律在 JS 內解析排序後用 category 軸）。
- 分析全部在瀏覽器內完成，資料不會離開你的電腦。帳號／權限／訪客額度（`ACCOUNTS_ENABLED`）**預設關閉**：不畫登入／升級／額度列、不呼叫權限 API、不記訪客次數、不存歷史。
- CSP `connect-src` 預設只有 `'self'`。若要把 `ACCOUNTS_ENABLED` 打開，還必須把 API origin（與 `WIDS_API_BASE` 相同）加回 `connect-src`（本機 mock 是 `http://127.0.0.1:8787` 與 `http://localhost:8787`）。
- 本資料夾不影響 plugin：`grok plugin validate .` 照樣通過；skill 檔案未改動。

## 怎麼開

1. 直接雙擊 `web/index.html`，或 `open web/index.html` / `xdg-open web/index.html`。
2. 在「1. 資料」選一個示範 CSV（來自 `examples/data/*.csv`），或上傳／貼上自己的 **CSV、Excel（.xlsx／.xls／.ods）、JSON**。CSV 先當 UTF-8 解（失敗再 Big5），逗號／分號／Tab 自動偵測；Excel 多工作表會出現下拉（預設第一張）；JSON 接受 `[{...}]` 或 `{"data":[...]}`，巢狀欄位攤平成 `a.b`。原始檔只在瀏覽器內解析，不會上傳。上限 10 MB；超過 50,000 列只留前 50,000 列並提示。
3. 「2. 欄位型態」可手動改型態，推薦會即時重算。
4. 「3. 推薦圖種」點任一圖種 → 「4. 圖表」切繪法與欄位 → 「5. 教學」看對應 pattern。

可用網址 hash 直接開到某個狀態（方便分享與自動化測試）：

```
index.html#sample=sample-heatmap.csv&pattern=matrix-heatmap
index.html#sample=sample-boxplot.csv&pattern=boxplot-summary&renderer=histogram&lang=en
```

## 重建教學內容與示範資料

`data/content.js`（`window.WIDS_CONTENT`）與 `data/samples.js`（`window.WIDS_SAMPLES`）是**產生檔，已 commit**，使用者不需要 Node。skill 的 `examples/*.md` 或 `examples/data/*.csv` 更新後重跑：

```bash
node web/build/build-content.mjs     # Node ≥ 18，無 npm 依賴；輸出可重現（無時間戳）
```

新增圖種 pattern 時：跑上面的建置，再到 `js/rules.js` 的 `RULES` 加一列（測試會檢查規則表與 `examples/*.md` 一一對應）。

## 本機連 mock 權限 API（預設關閉）

`js/config.js` 的 `ACCOUNTS_ENABLED` 預設是 `false`。11/7 上線是免費版，付費／帳號列先不上。要在本機打開帳號功能：

1. 在 `config.js` **之前**設 `window.WIDS_ACCOUNTS_ENABLED = true`（或把常數改成 `true`）。
2. 把 API origin 加回 `web/index.html` 的 CSP `connect-src`（只改旗標、CSP 沒加該 host，瀏覽器會擋 `fetch`）。

靜態頁與 mock API 要分開開（兩個 origin）。同事會在 API 端設 `CORS_ORIGIN`，必須包含靜態站的 origin。

```bash
# 終端 1：mock API（預設 http://127.0.0.1:8787）
cd web/api-mock
CORS_ORIGIN=http://127.0.0.1:4173 npm start

# 終端 2：靜態站
cd web
python3 -m http.server 4173
```

瀏覽器開 `http://127.0.0.1:4173/`：

- 頁面載入會 `GET /v1/health` 再 `GET /v1/me`，顯示訪客今日剩餘自貼（3／天）。
- 「用 GitHub 登入」走 mock OAuth（JSON callback），Bearer 存在 `localStorage` 的 `wids_token`。
- 「升級」會 `POST /v1/checkout/session` 後立刻 `POST /v1/checkout/mock-complete`，**不會打開 `checkout_url` 當網頁**。
- 已登入且有 `save_history` 時，成功分析後只 POST 摘要（`pattern_id`、`source_name`、`row_count`），絕不送原始檔。

訪客自貼次數前端記在 `wids_guest_uploads_YYYY-MM-DD`（台北日），並帶 `X-Guest-Id`；示範 CSV 不計次。API 契約與煙霧測試見 [`api-mock/README.md`](api-mock/README.md)。

### API base 與 Preview／Production CSP

預設 base 是 `http://127.0.0.1:8787`（`js/config.js` 的 `DEFAULT_API_BASE`）。覆寫方式：

1. 改 `js/config.js` 的常數（建置期／commit 進 Preview 用這條）。
2. 在 `config.js` **之前**設 `window.WIDS_API_BASE`（執行期覆寫）。

旗標打開時，Hosted／Preview／Production 要把同一個 mock origin 加進 `web/index.html` 的 CSP `connect-src`（預設只有 `'self'`）。只改 JS 常數、CSP 沒加該 host，瀏覽器會擋 `fetch`。`script-src` 仍是 `'self'`，不要為了改 base 打開 `'unsafe-inline'`。

API 端請設 `CORS_ORIGIN` 為靜態站 origin（Preview 網址或 Production 網域），並允許 `Authorization`、`X-Guest-Id`（mock 已支援）。

## 測試

```bash
node web/tests/fixtures/generate.mjs         # 重產 Excel／Big5／JSON 測試檔（已 commit，通常不必跑）
node --test web/tests/*.js web/tests/*.mjs   # CSV／Excel／JSON 解析、型態判斷、推薦規則、markdown 渲染、產生檔一致性、API client
```

選用的瀏覽器煙霧測試（headless Chromium，抓截圖並檢查 console error；需要 `playwright-core` 與本機 Chrome/Chromium，不會加入 repo 依賴）：

```bash
npm i --no-save --prefix /tmp/pw playwright-core
PLAYWRIGHT_CORE=/tmp/pw/node_modules/playwright-core CHROME=/usr/bin/google-chrome \
  node web/tests/browser/smoke.mjs /tmp/wids-shots
```

## 架構

```
web/
├── index.html              單頁；依序載入下列 script
├── css/style.css           響應式版面（≥1000px 兩欄，窄螢幕單欄）
├── vendor/                 Chart.js + SheetJS（xlsx 0.20.3 Apache-2.0）+ 授權 + 版本說明
├── data/                   產生檔：content.js（69 篇 pattern md）、samples.js（15 個示範 CSV）
├── build/build-content.mjs 產生 data/*.js
├── js/
│   ├── csv.js              自寫 CSV 解析（引號、引號內逗號／換行、""、CRLF/CR、BOM、分隔符偵測、參差列）
│   ├── input.js            本機匯入：UTF-8／Big5 CSV、JSON（攤平）、Excel／ODS（SheetJS；日期→ISO）
│   ├── types.js            欄位型態判斷：number / category / date / boolean / id；缺值、相異值、統計量
│   ├── rules.js            69 圖種規則表 + 資料形狀偵測（computeShape）+ 評分引擎
│   ├── markdown.js         極小 markdown 渲染（先跳脫 HTML；只允許 http(s)/mailto 連結）
│   ├── charts.js           繪圖器（Chart.js + 自繪 canvas）與純函式工具
│   ├── config.js           API base（預設 :8787）、ACCOUNTS_ENABLED（預設關）與 localStorage 鍵
│   ├── api.js              mock 權限 API client（旗標關或 file:// 不發請求）
│   ├── entitlement.js      訪客額度 + 帳號列（旗標關時不畫、不計次）
│   ├── i18n.js             繁中／英文字串
│   └── app.js              UI 控制（僅瀏覽器）
├── api-mock/               本機 mock 權限 API（:8787）
└── tests/                  node:test 單元測試；fixtures/ 為 Excel／Big5／JSON 樣本；browser/smoke.mjs 為選用 E2E
```

`csv.js`、`types.js`、`rules.js`、`markdown.js`、`charts.js` 都是 UMD 形式：瀏覽器掛到 `window.WIDS_*`，Node 用 `require()`，因此同一份邏輯可直接單元測試。

### 推薦規則怎麼算

`rules.js` 的 `RULES` 是資料驅動的規則表，每列對應一個 `examples/<id>.md`，依據 `references/chart-heuristics.md`（決策表、形狀 → 圖捷徑、易混圖種）與 `references/data-shape-checks.md`（欄位角色、結構探測）整理：

| 欄位 | 意義 |
|------|------|
| `requires` | 各型態欄位數下限（`label` = 類別或識別碼；`measure` = 扣掉經緯度、格座標、週期輔助欄後的數值欄） |
| `need` | 必須成立的形狀訊號（例：`crossTab`、`network`、`geo\|latlon`），每項 +20 |
| `prefer` | 加分訊號，每項 +10 |
| `avoid` | 扣分訊號（−15），同時顯示為「注意」；可寫 `!ratio` 表示「沒有比率欄」 |
| `base` | 先驗分數：越直接、越常用的圖越高（「優先選能直接回答問題的最簡單圖」） |
| `fields` / `why` | 需求欄位組合與理由（中英） |
| `render` | 可用繪圖器；空陣列 = 「教學可看，繪圖尚未支援」 |

形狀訊號（`computeShape`）包含：時間長度與週期、每日資料、系列數、寬表、類別 × 類別可樞紐、每組多筆（分布）、一類一列、同尺度數值對、兩期、年齡組 × 雙側、地理欄（一區一列）、經緯度、比率欄、row/col 格座標、source/target 網路（稠密度、邊分組、方陣）、巢狀類別階層、有號增減、漏斗階段、目標欄、開始／結束日期、布林集合欄、多數值欄、第三量級大小欄、大量點等。

## 已支援（端到端可繪）的圖種

| 繪圖器 | 對應 pattern | 互動 | 驗證用示範 CSV |
|--------|--------------|------|----------------|
| 折線圖（時間序列；長表多系列或寬表） | `time-series-trend.md` | 提示、欄位／系列／聚合選擇、圖例切換 | `sample-spiral.csv`、`streamgraph-categories.csv`、`streamgraph-wide.csv` |
| 排序長條／棒棒糖（預設由大到小） | `categorical-comparison.md`、`lollipop-rank.md` | 提示、排序、聚合、樣式 | `lollipop-categories.csv`、`sample-choropleth.csv` |
| 分組／堆疊／100% 堆疊長條 | `categorical-comparison.md` | 提示、模式切換、圖例切換 | `sample-marimekko.csv`、`population-pyramid-long.csv` |
| 散點／氣泡（顏色分組、面積映射大小） | `correlation-scatter.md`、`bubble-chart.md` | 提示（含標籤）、圖例切換 | `sample-bubble.csv` |
| 直方圖（分布初探，可分組） | `boxplot-summary.md`（輔助） | 提示、分箱數、圖例切換 | `sample-boxplot.csv` |
| 箱形圖（canvas 自繪，Tukey 1.5×IQR） | `boxplot-summary.md` | 提示、組別切換、顯示原始點 | `sample-boxplot.csv` |
| 矩陣熱圖（canvas 自繪；循序／發散色階） | `matrix-heatmap.md` | 提示、聚合、依列／欄正規化、排序、格內數字 | `sample-heatmap.csv` |
| 人口金字塔（長表或寬表） | `population-pyramid.md` | 提示、圖例切換 | `population-pyramid-long.csv`、`population-pyramid-wide.csv` |
| 鄰接矩陣（canvas 自繪） | `adjacency-matrix.md` | 提示、有向／無向、節點排序 | `sample-biofabric.csv` |

其餘 40 種仍會依資料形狀被推薦，並標示「教學可看，繪圖尚未支援」。

## 已知限制

- 檔案在瀏覽器內讀取：CSV 先 UTF-8（`TextDecoder` fatal），失敗再 Big5。Excel 日期會轉成 ISO（`2026-10-07`），不會留下序號。單檔上限 10 MB；超過 50,000 列只保留前 50,000 列。不支援 Parquet、PDF、圖片 OCR、Google 試算表連結。
- 時間軸為 category 軸：不等距時間點會等距排列。
- 日期判斷支援 ISO（`YYYY-MM[-DD][ HH:mm]`）、`YYYY/MM/DD`、`YYYYQn`、`YYYY年M月[D日]`、`M/D/YYYY`、`HH:mm`；年欄需欄名像 `year`／`年`。
- 推薦是啟發式規則，不理解欄位語意；以欄名關鍵字補足（geo、source/target、stage…），可手動改型態修正。
- 教學 markdown 目前只有繁中原文。
