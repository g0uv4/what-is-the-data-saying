# Demo 4 — Store before/after → dumbbell

Same stores, two comparable rates. People draw a slope “because two dates.” The skill should pick **啞鈴圖** for *gap per row*.

## Paste this

```
通路檢討。同一批門市，轉換率 H1 vs H2（%）。我要看誰差距最大、誰已經超車。示意未核。

| 門市 | H1轉換率_% | H2轉換率_% |
|------|------------|------------|
| 台北站前 | 3.1 | 4.8 |
| 台中中友 | 2.4 | 2.1 |
| 高雄夢時代 | 1.9 | 3.6 |
| 新竹巨城 | 2.8 | 2.9 |
| 台南南紡 | 2.2 | 1.6 |
| 桃園統領 | 1.5 | 3.0 |

這份資料該怎麼畫？請用資料在說什麼格式。請明確說為什麼不是坡度圖。軸與圖例用 zh-TW。
```

## You should hear

- **推薦：啞鈴圖（dumbbell / range plot）** — 類別列上兩個同單位數值，故事是「每列差多少」.
- **備選：** 坡度圖 if they later want 軌跡／超車 crossing as the *main* story (two vertical axes).
- **避免：** 把啞鈴畫成雙軸坡度卻說在比差距；兩端單位不同（本表沒有）.
- Sort by gap or by H2; two endpoint colors; legend locks H1／H2 and `%`.
- `examples/dumbbell-gap.md`. 未核.

## Why it wows

The mix-up (dumbbell vs slope) is a teach-viz signature. Strangers feel the pedagogy, not a generic “use a bar chart.”
