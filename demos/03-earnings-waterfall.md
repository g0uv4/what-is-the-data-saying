# Demo 3 — Earnings bridge → waterfall

The CFO question: how did gross profit become operating profit? Stacked bars hide the signed steps. The skill should say **瀑布圖**.

## Paste this

```
法說會投影片。要回答：2026 H1 從毛利走到營業利益，哪一步加減最多。示意未核，單位百萬新台幣。

| 項目 | 金額_百萬TWD | 角色 |
|------|----------------|------|
| 毛利 | 820 | 起點 |
| 運費與倉儲 | -96 | 減項 |
| 廣告投放 | -140 | 減項 |
| 人員薪資 | -210 | 減項 |
| 授權金收入 | +38 | 增項 |
| 一次回沖 | +22 | 增項 |
| 營業利益 | 434 | 終點 |

請推薦圖種（資料在說什麼格式），先寫故事句，再口述怎麼畫（落地柱 vs 浮空柱、增減分色）。不要用堆疊長條或雙軸折線混充。
```

## You should hear

- **推薦：瀑布圖（waterfall / bridge）**.
- Story: 從毛利 820 到營業利益 434，中間由費用與兩筆增項橋接（未核）.
- Start / end = full-height columns; signed steps = floating columns + connectors.
- **避免：** 中間柱從 0 長起來的普通長條；跟啞鈴／子彈混同一故事.
- Self-check that 820 − 96 − 140 − 210 + 38 + 22 = 434.
- `examples/waterfall-bridge.md`. 法說會 = 少圖、大字、靜態.

## Why it wows

This is the slide that usually ships as a stacked bar. Bridge encoding is the whole point of the skill.
