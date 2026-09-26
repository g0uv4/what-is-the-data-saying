# Pattern: circular-bar

> **圖種**：圓形長條圖（Circular barplot）
> **來源（納茲教圖）**：`teach-viz/2026-09-08-am-circular-bar.md`

## When

- 問「類別很多，要搶眼看高低」
- 形狀：多類別 + 一數值

## Recommend

- **主選**：圓形長條圖
- **備選**：精準差距 → 直線長條；等角面積 → 南丁格爾玫瑰

## Avoid

- 與玫瑰／雷達／旭日混淆；少數類別純裝飾
- 與螺旋圖混淆：本圖類別繞一圈就結束；連續時間捲成多圈、圈間對齊季節 → `spiral-plot.md`

## Produce checklist

- [ ] 數值=徑向棒長
- [ ] 圖注提醒精準比較弱於直線長條

鄰居 pattern：`radar-profile.md`、`spiral-plot.md`、`lollipop-rank.md`。
