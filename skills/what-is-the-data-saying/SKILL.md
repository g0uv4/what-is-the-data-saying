---
name: what-is-the-data-saying
description: >
  資料在說什麼：依資料形狀與閱讀任務推薦視覺化類型／做法，並協助產出圖表；
  維護可成長的 pattern 範例庫。Use when the user pastes data/reports and asks
  how to visualize, which chart to use, 這份資料該怎麼畫, 推薦圖表, 視覺化,
  資料在說什麼, or runs /what-is-the-data-saying.
when-to-use: >
  data entered the harness; report / CSV / table / Excel / 報表; ask for chart
  type, viz approach, or help producing a visualization; Taiwan Traditional
  Chinese report audience.
metadata:
  short-description: "資料視覺化推薦與產出（資料在說什麼）"
  author: g0uv4
---

# 資料在說什麼（what-is-the-data-saying）

當資料或報表進入對話時，依序做三件事：**診斷形狀 → 推薦圖型 → 協助產出**。
細節啟發式見 `references/`；可複用案例見 `examples/`。不要把大段規則複製進回覆，點名引用檔名即可。

面向：**台灣繁體中文報表讀者**（標題、軸標、圖註、結論句用 zh-TW；程式／變數名可用 EN）。

## 工作流程

### 1. 資料形狀檢查（先做，短報）

讀取或請使用者提供樣本後，用 `references/data-shape-checks.md` 檢查並輸出精簡診斷：

- 列／欄角色（時間、類別、數值、階層、地理、有序／無序）
- 粒度、缺失、極端值、單位是否混用
- 主問題類型：比較／趨勢／分布／相關／組成／流向／階層／多面板

若資料不足（只有截圖、沒有數字），先說明限制，再給「假設形狀成立時」的推薦。

### 2. 推薦視覺化（給 1 主選 + 1–2 備選）

用 `references/chart-heuristics.md` 對應任務 → 圖型。回覆格式固定：

```
推薦：<主圖型>（為什麼：一句）
備選：<圖型> — <何時改選>
避免：<常見誤用> — <原因>
讀者／輸出：<面向誰、靜態簡報 vs 可互動>
```

優先順序經驗法則（細節在 heuristics）：

| 任務 | 優先 |
|------|------|
| 少數類別比大小 | bar（水平 bar 適合長標籤） |
| 時間趨勢 | line（少系列）；過多系列 → small multiples |
| 兩數值關係 | scatter（可加 trend / 分組色） |
| 矩陣密度／相關 | heatmap |
| 階層組成 | icicle / sunburst / treemap（見 hierarchy pattern） |
| 精確查數、審核 | table（可加條件格式，不要硬畫圖） |
| 同結構多切片 | small multiples |

台灣報表注意事項見 `references/taiwan-report-readers.md`（千分位、%、YoY、財政／營運用語、投影片可讀性）。

### 3. 產出視覺化

依使用者環境選最短路徑（有現成工具就用，不要無故重寫）：

1. **已有程式專案** → 用專案慣用庫（Python: pandas + matplotlib/plotly；JS: d3/Observable/echarts；試算表：條件格式／樞紐）。
2. **只要靜態圖** → 產出可重跑腳本 + 圖檔（png/svg），軸標 zh-TW。
3. **要可互動探索** → 標明工具（Observable / Flourish / Plotly）與資料契約（欄名、型別）。
4. **對齊已知 pattern** → 打開 `examples/` 對應檔，照其「產出要點」做，並在回覆註明 pattern 名稱。

產出時一律：標單位、說明時間範圍、註記資料來源；避免 3D、雙 Y 軸（除非使用者堅持且標清楚）。

### 4. 成長範例庫（每次成功後）

若這次出現可複用的新組合（新 data shape + 圖型 + 產出要點），新增或更新：

`examples/<pattern-slug>.md`

並在 `examples/README.md` 加一行索引。Pattern 檔保持短：觸發條件、推薦、反例、產出 checklist。

## 快速對照（完整表在 references）

- **table**：審核、對帳、精確值、法規附件
- **bar**：類別比較、排序、組成（stacked 慎用）
- **line**：時間序列、事件前後
- **scatter**：相關、離群、分群
- **heat**：矩陣、日曆熱度、相關矩陣
- **icicle / partition**：階層鑽取、預算／組織樹
- **small-multiples**：多實體同尺度比較

## 回覆語氣

先給可執行推薦，再給可選細節。不要長篇理論。使用者用 zh-TW 就 zh-TW 回。
