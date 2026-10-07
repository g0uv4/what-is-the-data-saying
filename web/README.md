# web/ — 互動網頁 PoC（資料在說什麼？）

把本 repo 的 skill（`skills/what-is-the-data-saying/`）變成一個**純前端單頁**：上傳或貼上 CSV → 自動判斷欄位型態 → 依資料形狀從 **69 個圖種 pattern**（與 skill examples 同步） 推薦（排序＋理由）→ 可互動繪圖 → 顯示該圖種的教學 markdown。

- 無後端、無建置步驟即可使用：HTML / CSS / 原生 JS，普通 `<script src>`（不用 ES module、不用 `fetch` 讀本機檔），所以 **直接雙擊 `web/index.html`（file://）就能跑**。
- 唯一第三方依賴：Chart.js 4.5.1 UMD，已 vendor 在 `vendor/`（授權與版本見 `vendor/README.md`）。不用 CDN、不用日期 adapter（時間一律在 JS 內解析排序後用 category 軸）。
- 資料只在瀏覽器內處理，不會上傳；頁面有 CSP（`connect-src 'none'`）。
- 本資料夾不影響 plugin：`grok plugin validate .` 照樣通過；skill 檔案未改動。

## 怎麼開

1. 直接雙擊 `web/index.html`，或 `open web/index.html` / `xdg-open web/index.html`。
2. 在「1. 資料」選一個示範 CSV（來自 `examples/data/*.csv`），或上傳／貼上自己的 CSV（UTF-8；逗號、分號、Tab 自動偵測）。
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

## 測試

```bash
node --test web/tests/               # CSV 解析、型態判斷、推薦規則、markdown 渲染、產生檔一致性
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
├── vendor/                 chart.umd.min.js + 授權 + 版本說明
├── data/                   產生檔：content.js（69 篇 pattern md）、samples.js（15 個示範 CSV）
├── build/build-content.mjs 產生 data/*.js
├── js/
│   ├── csv.js              自寫 CSV 解析（引號、引號內逗號／換行、""、CRLF/CR、BOM、分隔符偵測、參差列）
│   ├── types.js            欄位型態判斷：number / category / date / boolean / id；缺值、相異值、統計量
│   ├── rules.js            69 圖種規則表 + 資料形狀偵測（computeShape）+ 評分引擎
│   ├── markdown.js         極小 markdown 渲染（先跳脫 HTML；只允許 http(s)/mailto 連結）
│   ├── charts.js           繪圖器（Chart.js + 自繪 canvas）與純函式工具
│   ├── i18n.js             繁中／英文字串
│   └── app.js              UI 控制（僅瀏覽器）
└── tests/                  node:test 單元測試；browser/smoke.mjs 為選用 E2E
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

- 檔案以 UTF-8 讀取；Big5 CSV 需先轉碼。整份資料在記憶體中處理，建議 ≤ 數萬列。
- 時間軸為 category 軸：不等距時間點會等距排列。
- 日期判斷支援 ISO（`YYYY-MM[-DD][ HH:mm]`）、`YYYY/MM/DD`、`YYYYQn`、`YYYY年M月[D日]`、`M/D/YYYY`、`HH:mm`；年欄需欄名像 `year`／`年`。
- 推薦是啟發式規則，不理解欄位語意；以欄名關鍵字補足（geo、source/target、stage…），可手動改型態修正。
- 教學 markdown 目前只有繁中原文。
