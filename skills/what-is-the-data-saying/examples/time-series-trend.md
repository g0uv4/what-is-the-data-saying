# Pattern: time-series-trend

> **圖種**：折線圖（Line chart）
> **來源（專案維護者整理）**：`（通用；對照 teach-viz 溪流／凹凸／坡度等時間教圖）`

## When

- 問「怎麼變、事件前後」
- 形狀：時間 + 數值（+ 少許系列）

## Recommend

- **主選**：折線圖（≤3 系列）
- **備選**：多實體 → 小多圖；長序列＋穩定週期、要同時看季節對齊與跨年趨勢 → 螺旋圖 `spiral-plot.md`（精讀差值仍回折線）；組成河（河流圖）→ `streamgraph-composition.md`；兩期 only → `slope-two-period.md`

## Avoid

- 單圖重疊 20+ 線
- 用每日長條塞滿密日資料

## Produce checklist

- [ ] 時間軸解析度與故事一致
- [ ] 系列過多改小多圖或篩選
- [ ] 標事件註記（若有）
- [ ] 單位／來源 zh-TW

鄰居 pattern：`flame-graph.md`（效能剖面：火焰圖橫軸不是時間；要呼叫的時間順序看火焰時序圖）、`spiral-plot.md`（把長時間軸捲成一圈＝一個週期）、`streamgraph-composition.md`、`slope-two-period.md`、`small-multiples.md`；`horizon-chart.md`（地平線圖：很多條對齊時間軸又要壓在矮列裡掃相對基準的偏離）；`pareto-chart.md`（柏拉圖只是某段期間的快照、看不出趨勢；要看趨勢用本檔的折線）；`control-chart.md`（管制圖：在折線上加中心線、管制界限與判異規則，判斷流程穩不穩；只看趨勢用本檔）、`lorenz-curve.md`（洛倫茲曲線：橫軸是排序後的名次比例、不是時間，不是趨勢線）、`marey-chart.md`（馬雷圖：一條線是一班車的位置隨時間變化、縱軸是實際距離，不是單一指標的走勢）、`kaplan-meier-survival.md`（存活曲線是只降不升的階梯，設限不下降；不是一般可上可下的折線）、`swimmer-plot.md`（游泳圖：一人一條時間棒的個人層級描述，不是單一指標走勢）、`lasagna-plot.md`（千層麵圖：很多個體同一組時間點的色帶；要精準讀值仍回折線）、`recurrence-plot.md`（遞迴圖：看何時回到相近狀態，不是數值高低本身）、`autocorrelation-plot.md`（自相關圖：結構診斷「隔幾步還跟自己有關」，不是數值高低本身）、`lag-plot.md`（滯後圖：知道前 k 步能不能猜現在、關係是什麼形狀；拿掉時間軸，簡報仍以折線為主）。
