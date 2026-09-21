# Pattern: streamgraph-composition

> **圖種**：溪流圖（Streamgraph）
> **來源（納茲教圖）**：`teach-viz/2026-08-28-pm-streamgraph-draft.md`

## When

- 問「整體組成隨時間如何起伏」
- 形狀：時間 + 類別 + 非負度量

## Recommend

- **主選**：溪流圖（stack + wiggle/center offset）
- **備選**：單層精準走勢 → 折線／小多圖；有序階段重分組 → 沖積

## Avoid

- 指望精確讀 Y 刻度
- 類別過多；與沖積圖混淆

## Produce checklist

- [ ] 非負值；類別少到可追
- [ ] 標來源；互動補數值
