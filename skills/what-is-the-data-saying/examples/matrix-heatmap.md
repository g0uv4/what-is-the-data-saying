# Pattern: matrix-heatmap

> **圖種**：熱力圖（Heatmap）
> **來源（納茲教圖）**：`（通用；網路有無邊見 adjacency；日活動見 calendar）`

## When

- 問「矩陣哪裡熱、相關強度」
- 形狀：類別 × 類別 + 值

## Recommend

- **主選**：熱力圖
- **備選**：相關矩陣先抽樣；日活動 → `calendar-heatmap.md`；網路邊 → `adjacency-matrix.md`

## Avoid

- 把鄰接矩陣當普通相關熱力卻不重排節點
- 彩虹色盤無序類別

## Produce checklist

- [ ] 色階單調、色盲友善
- [ ] 排軸有意義（聚類／固有序）
- [ ] 圖例寫清單位
