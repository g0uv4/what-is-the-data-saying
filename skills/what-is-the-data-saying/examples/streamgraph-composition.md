# Pattern: streamgraph-composition

> **圖種**：河流圖（Streamgraph／ThemeRiver）
> **來源（納茲教圖）**：`teach-viz/2026-09-22-am-streamgraph.md`（正式專題；取代草稿 `2026-08-28-pm-streamgraph-draft.md`）
> **亦稱**：溪流圖、stream graph、ThemeRiver、trend river

## When

- 問「多個非負組成隨時間怎麼一起起伏」——整體河道寬窄、各層厚度消長、季節／週期峰谷
- 敘事重點是**巨觀流動感與相對份額**，不是單點精確讀值
- 類別適中（約五～七層；長尾併「其他」）；互動懸停可補精確數值

## Recommend

- **主選**：河流圖（堆疊面積 + 浮動中心線／wiggle-minimizing offset）
  - **ThemeRiver 變體**：剪影大致對稱於中央軸
  - **Streamgraph（Byron＋Wattenberg）**：能量／晃動最佳化基準線與排序，邊界更平穩
  - **百分比展開（expand／100% stack）**：看相對占比而非絕對量（外觀仍可像河）
- **備選**：單一層精準走勢 → 折線／小多圖；貼零看總量累加 → **堆疊面積圖**；階段重分組流向 → 沖積／桑基

## Avoid

- 指望用縱軸當刻度尺讀單一層絕對高度（基準線浮動）
- 負值當主軸（常見工具會忽略負值）；比率／人均當厚度主編碼
- 類別過多、層帶糊成一團；與**山脊線**（上下錯開密度）混淆
- 與**沖積／桑基**混淆（那些是節點轉移流向，不是連續時間厚度河）
- 中文投資用語「河流圖／本益比河道」——與本圖種無關，勿混入案例
- 把貼齊 y＝0 的堆疊面積**假裝**成河流圖（近親，但基準線不同）

## Produce checklist

- [ ] 故事句含：整體起伏／層帶消長（不是「讀出某月某層精確值」）
- [ ] 資料：可排序時間 + 類別 + **非負**度量；長表（date, category, value）或寬表（date + 每類一欄）
- [ ] 先畫貼零堆疊面積對照總量與排序，再切 stream／ThemeRiver／wiggle
- [ ] 類別數可控；微小類合併「其他」；相鄰層色差夠
- [ ] 圖例：時間單位、類別色票、是否對稱中軸／百分比展開；示範數標「數字未核」
- [ ] 工具誠實：Flourish area→streamgraph（寬表）、RAWGraphs Streamgraph、ECharts ThemeRiver；Datawrapper 無原生一鍵
- [ ] 自檢：還原貼零後若敘事仍成立且讀者要精準讀高 → 改堆疊面積或折線；有關鍵負值 → 勿硬套

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `streamgraph-categories.csv` — 長表（date, category, value）
- `streamgraph-wide.csv` — 寬表（date + A/B/C 欄）

## 參考連結（可點；教圖已核狀態）

- https://datavizcatalogue.com/methods/stream_graph.html
- https://datavizproject.com/data-type/stream-graph/
- https://www.data-to-viz.com/graph/streamgraph.html （舊 `stream.html`＝404）
- https://en.wikipedia.org/wiki/Streamgraph （獨立 ThemeRiver 條目＝404）
- https://leebyron.com/streamgraph/ ／論文 PDF／DOI 10.1109/TVCG.2008.166
- https://flourish.studio/blog/streamgraphs/ ／ help article 67
- https://rawgraphs.io/learning/how-to-make-a-streamgraph/
- https://echarts.apache.org/examples/en/index.html#chart-type-themeRiver

圖檔與截圖留在教圖／skill-pack（`/workspace/skill-packs/2026-09-22-am-streamgraph/images/`），本 repo **不複製**大圖；對帳見 `ATTRIBUTION.md`。
