---
name: what-is-the-data-saying
description: >
  Given a table or report, recommend the chart and how to make it (資料在說什麼).
  Nazh-grounded Taiwan zh-TW pedagogy plus 40 named patterns. Use when the user
  pastes CSV / Excel / a table / 報表 and asks which chart, how to visualize,
  這份資料該怎麼畫, 推薦圖表, 視覺化, or runs /what-is-the-data-saying.
when-to-use: >
  A table, CSV, Excel, screenshot, or report is in the chat and they want a
  chart pick, a how-to, or zh-TW teaching (適不適合／口述怎麼做) — not a
  generic “use a bar chart.”
argument-hint: paste a table or describe the report
metadata:
  short-description: "Which chart? How to make it. 資料在說什麼"
  author: g0uv4
  version: "0.3.1"
  lineage: "納茲 - 資料視覺 teach-viz 教圖"
  license: MIT
---

# 資料在說什麼（what-is-the-data-saying）

當資料或報表進入對話時，依序做三件事：**診斷形狀 → 推薦圖型 → 協助產出**。
細節啟發式見 `references/`；可複用案例見 `examples/`；來源歸因見 `ATTRIBUTION.md`。
陌生人第一次試用的貼上稿在 plugin 根目錄 `demos/`（冰柱／漏斗／瀑布／啞鈴／坡度）。
不要把大段規則複製進回覆，點名引用檔名即可。

面向：**台灣繁體中文報表讀者**（標題、軸標、圖註、結論句用 zh-TW；程式／變數名可用 EN）。
公開使用者用英文問就英答，但圖種仍給 **中文名（英文名）**。

教學語氣對齊納茲教圖習慣：先給**中文圖種名（英文名）**、**適不適合**、**口述怎麼做**、再給工具路徑；數字未核要標「未核」。

## 工作流程

### 1. 資料形狀檢查（先做，短報）

讀取或請使用者提供樣本後，用 `references/data-shape-checks.md` 檢查並輸出精簡診斷：

- 列／欄角色（時間、類別、數值、階層、地理、網路邊、有序／無序）
- 粒度、缺失、極端值、單位是否混用
- 主問題類型：比較／趨勢／分布／相關／組成／流向／階層／多面板／排名／差距／地理

若資料不足（只有截圖、沒有數字），先說明限制，再給「假設形狀成立時」的推薦。

### 2. 推薦視覺化（給 1 主選 + 1–2 備選）

用 `references/chart-heuristics.md` 對應任務 → 圖型。回覆格式固定：

```
推薦：<中文圖種名>（英文名）— 為什麼：一句
備選：<圖型> — <何時改選>
避免：<常見誤用／易混圖種> — <原因>
讀者／輸出：<面向誰、靜態簡報 vs 可互動>
pattern：examples/<slug>.md（若有）
```

台灣報表注意事項見 `references/taiwan-report-readers.md`。

### 3. 產出視覺化

依 `references/how-to-produce.md` 與對應 `examples/` 產出要點：

1. **先寫故事句**（這張圖要回答什麼），再動手。
2. **已有程式專案** → 用專案慣用庫；**只要靜態圖** → 可重跑腳本 + png/svg；**要互動** → 標工具與資料契約。
3. **對齊已知 pattern** → 打開 `examples/` 對應檔，照「產出 checklist」做。
4. 產出一律：標單位、時間範圍、資料來源；避免 3D、雙 Y 軸（除非使用者堅持且標清楚）。
5. 教圖場合：口述步驟優先，必要時再給程式；附可點參考連結。

### 4. 成長範例庫（每次成功後）

若出現可複用的新組合，新增：

`examples/<pattern-slug>.md`

並在 `examples/README.md` 加一行；`ATTRIBUTION.md` 補來源檔名。

## 快速對照（完整表在 references/chart-heuristics.md）

| 任務 | 優先圖型（zh-TW） |
|------|------------------|
| 類別比大小 | 長條圖；類別多可考慮圓形長條 |
| 兩期／兩條件差距 | 啞鈴圖；兩期軌跡用坡度圖 |
| 時間趨勢 | 折線；多實體小多圖；組成隨時間用溪流圖 |
| 排名起伏 | 凹凸圖（bump） |
| 兩數值關係 | 散點；過密用六角分箱／等高線；雙序列演化用連接散點 |
| 分布形狀 | 小提琴／蜂群／雨雲／山脊 |
| 組成（平級） | 堆疊長條／華夫；精確值用表 |
| 階層組成 | 冰柱／旭日／矩形樹狀／圓堆／Voronoi 樹狀 |
| 從 A 變到 B 的因子 | 瀑布圖（bridge） |
| 階段漏損 | 漏斗圖 |
| 有向流量 | 桑基；階段重分組用沖積圖；成對交換用弦圖 |
| 多類別交叉 | 馬賽克／平行集合；集合交集用 UpSet |
| 網路關係 | 力導向／弧線／鄰接矩陣／蜂巢圖；有階層+葉連線用 HEB |
| 地理量 | 等值區劃圖（choropleth）；計數疏密用點密度圖；總量規模用比例符號地圖；變形用統計變形地圖 |
| KPI 對目標 | 子彈圖 |
| 專案時程 | 甘特圖 |
| 日曆活動密度 | 日曆熱力圖 |
| 多度量剖面 | 雷達（少系列）；多特徵用平行座標 |

## 回覆語氣

先給可執行推薦，再給可選細節。不要長篇理論。使用者用 zh-TW 就 zh-TW 回。教圖時給中文圖種名、適不適合、口述怎麼做。
