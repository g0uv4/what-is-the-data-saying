# Pattern: hierarchy-icicle

> **圖種**：冰柱圖（Icicle diagram）
> **來源（納茲教圖）**：`teach-viz/2026-09-01-am-icicle-draft.md`

## When

- 問「結構怎麼切、往下鑽、預算／組織／科目樹佔比」
- 形狀：階層（parent–child 或 path）+ 非負數值
- 要好標文字、層偏深

## Recommend

- **主選**：**冰柱圖（icicle）**／partition 直角版
- **備選**：旭日（緊湊總覽）；矩形樹狀（葉面積）；圓堆；Voronoi 樹狀
- **對帳**：旁掛表格（路徑 + 金額）

## Avoid

- 深階層压成單一圓餅
- 子加總 ≠ 父卻不洗資料
- 有向流量改畫冰柱（應桑基）
- 假設 Flourish 有原生冰柱（多數 Hierarchy 模板沒有）
- **與火焰圖混**：火焰圖（`flame-graph.md`）的「冰柱布局」外觀和本圖一樣，但資料是堆疊取樣、寬＝合併後的樣本占比、橫軸依函式名字母排序（不是組成切分，也不是時間）；本圖是任意階層加總的隸屬組成。拿預算／科目樹不要叫火焰圖，拿效能剖面也不要叫冰柱圖
- Plotly 把「往上長」的 partition 方向叫 flame chart：那只是本圖顛倒方向的別名，不是效能火焰圖

## Produce checklist

- [ ] 驗證階層加總（父＝子 sum）
- [ ] 層順序＝深度軸順序
- [ ] 互動：下鑽／breadcrumb；靜態限制深度
- [ ] zh-TW 節點名；單位一致
- [ ] 故事句先寫清「隸屬組成」不是流量

鄰居 pattern：`sunburst-hierarchy.md`、`treemap-composition.md`、`circle-packing.md`、`voronoi-treemap.md`、`flame-graph.md`（**不同圖種**：堆疊取樣效能熱路徑；只有冰柱布局外觀相同）、`sankey-flow.md`。
