# Pattern: cartogram-geo

> **圖種**：統計變形地圖（Cartogram）
> **來源（納茲教圖）**：`teach-viz/2026-09-16-am-cartogram.md`

## When

- 問「地理區塊資料量用面積說話」
- 形狀：每區一列 + 數值

## Recommend

- **主選**：統計變形地圖
- **備選**：比率填色 → choropleth（`choropleth-map.md`）；點總量 → bubble map；每區等權重、一區一格等大 → 圖塊地圖（`tile-map.md`）
- **加權六角／方塊**（格數＝人口或選舉人票：Datawrapper electoral college hexagons、grid cartogram、鑲嵌式面積變形地圖、Tilegrams）屬本家族，不是等大圖塊地圖；對照見 `tile-map.md`

## Avoid

- 以為土地面積；缺值變零塊

## Produce checklist

- [ ] 故事句：面積＝資料不是土地
- [ ] 並排真實邊界對照
