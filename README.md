# What is the data saying（資料在說什麼）

**MIT-licensed [Grok Build](https://github.com/xai-org/grok-build) skill — v0.3.32.**

Paste a table or report. Get **which chart**, **why not the usual pie**, and **how to make it**.

The differentiator is not another chart-chooser flowchart. It is **Taiwan zh-TW teaching-grade pedagogy** plus **70 named patterns** compiled from internal teaching notes: 中文圖種名, 適不適合, 口述怎麼做.

[Install](#install-grok-build) · [30-second demo](#try-this-first) · [70 patterns](#70-named-patterns) · [License](COMMERCIAL.md) · [中文說明](#資料在說什麼)

> Star or fork if a first paste already beats your default pie.  
> Need a chart for *your* table? [Open a chart request](https://github.com/g0uv4/what-is-the-data-saying/issues/new?template=chart-request.yml).

## Install (Grok Build)

```bash
grok plugin install g0uv4/what-is-the-data-saying --trust
```

Local checkout:

```bash
git clone https://github.com/g0uv4/what-is-the-data-saying.git
cd what-is-the-data-saying
grok plugin validate .
grok plugin install . --trust
```

Then in the Grok TUI: `/what-is-the-data-saying`, or paste a table and say **「這份資料該怎麼畫」**.

```bash
grok plugin details what-is-the-data-saying
grok plugin update what-is-the-data-saying
```

## Try this first

Copy one block from [`demos/`](demos/README.md) into a new Grok chat. First-time wow cases:

| Demo | Shape | Chart you should hear |
|------|--------|------------------------|
| [Inventory tree](demos/01-inventory-icicle.md) | warehouse → category → SKU | **冰柱圖（icicle）** — not a pie |
| [Signup leak](demos/02-signup-funnel.md) | ordered stages + counts | **漏斗圖** — bottleneck named |
| [Gross → operating](demos/03-earnings-waterfall.md) | start + signed steps | **瀑布圖（bridge）** |
| [H1 vs H2 stores](demos/04-before-after-dumbbell.md) | same categories, two values | **啞鈴圖** — not a slope |
| [Two-period ranks](demos/05-two-period-slope.md) | entities × exactly two periods | **坡度圖** |

Each file is a **copy-paste prompt** plus the answer shape you can score against.

## What you get

1. **Shape check** — time / category / hierarchy / flow / geo, units, missing parents.
2. **One primary chart + 1–2 backups** — and the mix-up to avoid (icicle ≠ sankey, dumbbell ≠ slope).
3. **How to produce it** — story sentence first, then spoken steps, then a tool path.
4. **Taiwan report readers** — zh-TW titles, 新台幣 / 千元, 未核 when numbers are unchecked.

Reply format the skill always uses:

```
推薦：<中文圖種名>（英文名）— 為什麼：一句
備選：<圖型> — <何時改選>
避免：<常見誤用> — <原因>
讀者／輸出：<誰看、靜態 vs 互動>
pattern：examples/<slug>.md
```

## 70 named patterns

Full table: [`skills/what-is-the-data-saying/examples/README.md`](skills/what-is-the-data-saying/examples/README.md). Heuristics: [`references/chart-heuristics.md`](skills/what-is-the-data-saying/references/chart-heuristics.md).

Highlights: icicle / sunburst / treemap / voronoi tree · **flame graph／火焰圖**（≠ flame chart, ≠ icicle） · waterfall · funnel · dumbbell / slope / bump · **lollipop／棒棒糖** · **streamgraph／河流圖** · sankey / alluvial / chord · **circos／環狀多軌圖** · **boxplot／箱形圖** · **bubble／氣泡圖** · **marimekko／馬里梅可** · raincloud / ridgeline / beeswarm / violin · hexbin / contour · **volcano plot／火山圖**（≠ Manhattan, ≠ MA plot） · **Manhattan plot／曼哈頓圖**（+ Miami variant; ≠ volcano, ≠ QQ） · **MA plot／MA 圖**（≠ volcano; RA plot = count version） · **QQ plot／QQ 圖**（≠ P–P, ≠ probplot; y = x vs any line） · **Bland–Altman plot／Bland–Altman 圖**（≠ MA plot, ≠ correlation; limits ≠ CI） · **P–P plot／P–P 圖**（≠ QQ; probability vs probability; axes vary by source） · **Marey chart／馬雷圖／列車運行圖**（train graph, stringline, time–distance diagram; one line per vehicle, stations on the axis in real distance order so slope = speed — equal spacing breaks that; crossings mean meets or overtakes; on a single track a crossing must fall inside a station that can host a meet; ≠ line chart, ≠ Gantt chart, and the Chinese Wikipedia redirect 「运行图」 goes to run chart; attribution wording: Tufte p.31 credits Ibry, the book's first edition is 1878 and "1885" is an edition year, Sergeev 1854 is a single-source claim later than Petiet 1843 and Ibry 1847; do not use the licence-doubtful R14 image） · **Kaplan–Meier survival curve／存活曲線**（product-limit estimator; one step down per event, censoring marks do not drop the curve; median = first time S≤0.5; needs time+event/censor columns; ≠ line chart, ≠ ecological survivorship curve; do NOT adopt Wikipedia's "editor was Tukey" — use Stalpers & Kaplan 2018: graduate students under Tukey who merged on the *journal editor's* advice; AML textbook example median 27 weeks, groups 31 vs 23, log-rank P≈0.065; R13 Commons author field OWID but figure credits Saloni Dattani; crossing curves need stratified HRs; confidence bands + number-at-risk table） · **Swimmer plot／游泳圖**（one horizontal bar per subject = time on treatment; symbols for first response, CR, progression, stop reason; tail arrow = still on treatment at data cutoff; sort by duration → staircase; short bars of late enrollees are a cutoff artefact, not failure; above ~50 subjects switch to Kaplan–Meier or facets; ≠ swimlane flowchart (泳道圖), ≠ Gantt (planned vs observed), ≠ oncology waterfall/spider plot; no accepted zh-TW name, naming origin/inventor unconfirmed; Chia 2016 "commonly used in phase I" refers to the spider plot; demo S3 Spearman −0.32 with average ranks for ties; R6 dashed line labelled 12.3 months but drawn at ~10.4 by the ticks — flaw in the original figure; R16 is a counter-example, R19/R20 contrasts） · **Lasagna plot／千層麵圖（暫譯）**（heatmap special case: one row per subject, one column per shared time point, colour = value or state, missing cells marked separately; state the row ordering (S3: ordering creates patterns), single-hue scale with one fixed range, never zero-fill missing values (S5); Wicklin 2016 SAS blog: usually ≥10 px per row, not for thousands of subjects — "group first above 1,000" is NOT his statement; Swihart et al. 2010 is the commonly cited naming source, not the inventor (Peng 2008 earlier); R5 "17" is a citation superscript (paper has 174 patients); S7 figure label 148.3 but half-up value 148.4, change +1.8; R17 is a counter-example, R18–R20 contrasts; ≠ spaghetti plot, ≠ swimmer plot） · **Recurrence plot／遞迴圖（暫譯）**（binary time×time matrix: black if states at times i and j are within threshold ε; diagonal lines = recurring evolution / period, blocks = stuck, white bands = abrupt change; state ε, embedding m and delay τ on the figure — same series changes completely with different settings; DET high is necessary not sufficient for “regularity” (S2: random-walk DET 79.3% vs white-noise 25.2%); “RR 1%–5%” is common practice but no primary source states it as a fixed interval (~1% is Marwan recounting Zbilut et al. 2002); zh name provisional (Taiwan 遞迴圖 / Mainland 复现图 both unverified; also 逆歸圖示法, 回歸圖); R13 panel B caption 0.144 vs figure ~50%/0.253 is a paper flaw; pucicu = Norbert Marwan; recurrence-plot.tk and Marwan 2007 arXiv are non-commercial — link only; ≠ ordinary heatmap, ≠ lasagna, ≠ adjacency matrix） · **Spectrogram／頻譜圖**（time × frequency × colour in dB; six settings on the figure — sampling rate, window, window function, overlap, dB reference, frequency scale; longer window sharpens frequency and blurs time; linear colour hides a 0.0001 share that is −40 dB; below 1000 Hz is 12.5% of a linear axis vs 35.2% on mel; a spectrum is not a spectrogram; 三維瀑布圖 (waterfall plot) ≠ financial waterfall chart; a scalogram’s axis is scale, not frequency; R13 GW170817 licence conflict — link only; R7 is CC BY 3.0, not public domain; R7 window “16348”, R17 cursor “86, -23.4105”, and R20’s unitless “50” are recorded as-is） · **Lorenz curve／洛倫茲曲線**（with the Gini coefficient; sort units from smallest to largest and plot cumulative % of units against cumulative % of income/wealth, with the equality diagonal; always say whether the Gini has the n/(n−1) small-sample correction — 10 households, S3: 0.38 → 0.42; one person taking everything is (n−1)/n = 0.90 for 10 households, not 1; two groups can share a Gini yet have crossing curves, so do not rank them by Gini alone; related to but not the same chart as the Pareto chart: the Pareto cumulative line turned half a turn is the Lorenz curve of the same numbers） · **control chart／管制圖**（Shewhart chart; ≠ line chart, ≠ Pareto, ≠ spec limits; control limits come from process data, not from specs; the "same-side run" rule is 8 points in Western Electric but 9 in Nelson, so agree the rule set first） · **Pareto chart／柏拉圖／帕累托圖**（≠ plain bar chart, ≠ waterfall, ≠ funnel; related to but not the same chart as the Lorenz curve (the cumulative line turned half a turn is the Lorenz curve of the same numbers); cumulative-% line on a 0–100% right axis; set the left-axis max to the total; 80/20 is a rule of thumb, read at which item the line first reaches 80%; 「其他」 usually goes far right） · **horizon chart／地平線圖**（≠ streamgraph, ≠ ridgeline, ≠ heatmap; colour bands trade layers for height; write the baseline; rows are not comparable unless they share a band width） · **forest plot／森林圖**（≠ funnel plot for meta-analysis, ≠ business Funnel chart; log axis for ratio measures; square area ∝ weight） · **karyotype／ideogram plot／核型圖／染色體帶型示意圖**（≠ Manhattan, ≠ Circos; karyogram and idiogram are synonyms） · **LocusZoom plot／LocusZoom 圖**（區域關聯圖; ≠ Manhattan; lead variant ≠ causal） · **choropleth／等值區域** · **tile map／圖塊地圖** · **dot density** · **population pyramid／人口金字塔** · **BioFabric／生物織布圖** · UpSet · bullet KPI · **matrix heatmap／矩陣熱圖** · calendar heatmap · **spiral plot／螺旋圖** · cartogram.

## For teams

Earnings decks, ops dashboards, and research digests still burn analyst time on the *wrong* figure. The skill is MIT-licensed; see [`COMMERCIAL.md`](COMMERCIAL.md) for the license and how to reach the project maintainer.

## Support

| Want | Do this |
|------|---------|
| Say the skill helped | [Star](https://github.com/g0uv4/what-is-the-data-saying) or fork |
| “Which chart for *this* table?” | [New chart-request Issue](https://github.com/g0uv4/what-is-the-data-saying/issues/new?template=chart-request.yml) |

## Repo map

| Path | Role |
|------|------|
| `skills/what-is-the-data-saying/SKILL.md` | When to fire + the three-step loop |
| `references/` | Heuristics, produce-how, shape checks, Taiwan readers |
| `examples/` | 70 patterns (when / recommend / avoid / checklist) |
| `demos/` | Copy-paste first-run prompts |
| `COMMERCIAL.md` | License and how to reach the maintainer |
| `ATTRIBUTION.md` | Teaching-note → pattern mapping |

Grow it: real report → was the pick right → new `examples/<slug>.md` + ATTRIBUTION row → `grok plugin update`.

## Attribution & license

Examples and heuristics were compiled by the project maintainer from internal teaching notes (範例與啟發式由專案維護者依內部教學筆記整理), and each pattern ships with verification data. The original notes are not in this repo; this repo is an executable summary, **not** the full lesson texts. Keep [`ATTRIBUTION.md`](skills/what-is-the-data-saying/ATTRIBUTION.md) when you share.

[MIT](LICENSE) · © 2026 g0uv4 · GitHub only (no Origin).

---

## 資料在說什麼

**MIT 授權的 Grok Build skill（v0.3.32）。** 丟進一張表或一份報表，它回答兩件事：**該畫哪種圖**、**怎麼做得出來**。

和一般「圖表選擇器」的差別：對齊內部教學筆記的台灣繁體中文教學——先給中文圖種名（英文名）、適不適合、口述怎麼做，再給工具。內建 **70 個具名 pattern**，不是示意三張長條圖。

### 安裝

```bash
grok plugin install g0uv4/what-is-the-data-saying --trust
```

在 Grok TUI 輸入 `/what-is-the-data-saying`，或直接貼上資料說「這份資料該怎麼畫」。

### 先跑哪個 demo

到 [`demos/`](demos/README.md) 複製一則。庫存階層應聽到**冰柱圖**、漏斗應點名瓶頸階、損益橋應聽到**瀑布圖**、兩期同店應聽到**啞鈴圖**而不是坡度圖。

標題、軸、圖註、結論句用 **zh-TW**（營收／毛利／縣市／新台幣）；程式與變數名可用英文。數字沒核過就標「未核」。

### 給團隊

法說會投影片、營運看板、研究摘要，最常耗掉的是「畫錯圖再重做」。授權與怎麼聯絡維護者見 [`COMMERCIAL.md`](COMMERCIAL.md)。

本專案以 MIT 授權提供。想一起改或提新圖種，請開 Issue。

覺得有用就 star／fork；缺一種圖就開 [chart request](https://github.com/g0uv4/what-is-the-data-saying/issues/new?template=chart-request.yml)。
