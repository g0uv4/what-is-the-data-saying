# What is the data saying（資料在說什麼）

**MIT-licensed [Grok Build](https://github.com/xai-org/grok-build) skill — v0.3.42.**

Paste a table or report. Get **which chart**, **why not the usual pie**, and **how to make it**.

The differentiator is not another chart-chooser flowchart. It is **Taiwan zh-TW teaching-grade pedagogy** plus **80 named patterns** compiled from internal teaching notes: 中文圖種名, 適不適合, 口述怎麼做.

[Install](#install-grok-build) · [30-second demo](#try-this-first) · [80 patterns](#80-named-patterns) · [License](COMMERCIAL.md) · [中文說明](#資料在說什麼)

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

## 80 named patterns

Full table: [`skills/what-is-the-data-saying/examples/README.md`](skills/what-is-the-data-saying/examples/README.md). Heuristics: [`references/chart-heuristics.md`](skills/what-is-the-data-saying/references/chart-heuristics.md).

Highlights: icicle / sunburst / treemap / voronoi tree · **flame graph／火焰圖**（≠ flame chart, ≠ icicle） · waterfall · funnel · dumbbell / slope / bump · **lollipop／棒棒糖** · **streamgraph／河流圖** · sankey / alluvial / chord · **circos／環狀多軌圖** · **boxplot／箱形圖** · **bubble／氣泡圖** · **marimekko／馬里梅可** · raincloud / ridgeline / beeswarm / violin · hexbin / contour · **volcano plot／火山圖**（≠ Manhattan, ≠ MA plot） · **Manhattan plot／曼哈頓圖**（+ Miami variant; ≠ volcano, ≠ QQ） · **MA plot／MA 圖**（≠ volcano; RA plot = count version） · **QQ plot／QQ 圖**（≠ P–P, ≠ probplot; y = x vs any line） · **Bland–Altman plot／Bland–Altman 圖**（≠ MA plot, ≠ correlation; limits ≠ CI） · **P–P plot／P–P 圖**（≠ QQ; probability vs probability; axes vary by source） · **Marey chart／馬雷圖／列車運行圖**（train graph, stringline, time–distance diagram; one line per vehicle, stations on the axis in real distance order so slope = speed — equal spacing breaks that; crossings mean meets or overtakes; on a single track a crossing must fall inside a station that can host a meet; ≠ line chart, ≠ Gantt chart, and the Chinese Wikipedia redirect 「运行图」 goes to run chart; attribution wording: Tufte p.31 credits Ibry, the book's first edition is 1878 and "1885" is an edition year, Sergeev 1854 is a single-source claim later than Petiet 1843 and Ibry 1847; do not use the licence-doubtful R14 image） · **Kaplan–Meier survival curve／存活曲線**（product-limit estimator; one step down per event, censoring marks do not drop the curve; median = first time S≤0.5; needs time+event/censor columns; ≠ line chart, ≠ ecological survivorship curve; do NOT adopt Wikipedia's "editor was Tukey" — use Stalpers & Kaplan 2018: graduate students under Tukey who merged on the *journal editor's* advice; AML textbook example median 27 weeks, groups 31 vs 23, log-rank P≈0.065; R13 Commons author field OWID but figure credits Saloni Dattani; crossing curves need stratified HRs; confidence bands + number-at-risk table） · **Swimmer plot／游泳圖**（one horizontal bar per subject = time on treatment; symbols for first response, CR, progression, stop reason; tail arrow = still on treatment at data cutoff; sort by duration → staircase; short bars of late enrollees are a cutoff artefact, not failure; above ~50 subjects switch to Kaplan–Meier or facets; ≠ swimlane flowchart (泳道圖), ≠ Gantt (planned vs observed), ≠ oncology waterfall/spider plot; no accepted zh-TW name, naming origin/inventor unconfirmed; Chia 2016 "commonly used in phase I" refers to the spider plot; demo S3 Spearman −0.32 with average ranks for ties; R6 dashed line labelled 12.3 months but drawn at ~10.4 by the ticks — flaw in the original figure; R16 is a counter-example, R19/R20 contrasts） · **Lasagna plot／千層麵圖（暫譯）**（heatmap special case: one row per subject, one column per shared time point, colour = value or state, missing cells marked separately; state the row ordering (S3: ordering creates patterns), single-hue scale with one fixed range, never zero-fill missing values (S5); Wicklin 2016 SAS blog: usually ≥10 px per row, not for thousands of subjects — "group first above 1,000" is NOT his statement; Swihart et al. 2010 is the commonly cited naming source, not the inventor (Peng 2008 earlier); R5 "17" is a citation superscript (paper has 174 patients); S7 figure label 148.3 but half-up value 148.4, change +1.8; R17 is a counter-example, R18–R20 contrasts; ≠ spaghetti plot, ≠ swimmer plot） · **Recurrence plot／遞迴圖（暫譯）**（binary time×time matrix: black if states at times i and j are within threshold ε; diagonal lines = recurring evolution / period, blocks = stuck, white bands = abrupt change; state ε, embedding m and delay τ on the figure — same series changes completely with different settings; DET high is necessary not sufficient for “regularity” (S2: random-walk DET 79.3% vs white-noise 25.2%); “RR 1%–5%” is common practice but no primary source states it as a fixed interval (~1% is Marwan recounting Zbilut et al. 2002); zh name provisional (Taiwan 遞迴圖 / Mainland 复现图 both unverified; also 逆歸圖示法, 回歸圖); R13 panel B caption 0.144 vs figure ~50%/0.253 is a paper flaw; pucicu = Norbert Marwan; recurrence-plot.tk and Marwan 2007 arXiv are non-commercial — link only; ≠ ordinary heatmap, ≠ lasagna, ≠ adjacency matrix） · **Spectrogram／頻譜圖**（time × frequency × colour in dB; six settings on the figure — sampling rate, window, window function, overlap, dB reference, frequency scale; longer window sharpens frequency and blurs time; linear colour hides a 0.0001 share that is −40 dB; below 1000 Hz is 12.5% of a linear axis vs 35.2% on mel; a spectrum is not a spectrogram; 三維瀑布圖 (waterfall plot) ≠ financial waterfall chart; a scalogram’s axis is scale, not frequency; R13 GW170817 licence conflict — link only; R7 is CC BY 3.0, not public domain; R7 window “16348”, R17 cursor “86, -23.4105”, and R20’s unitless “50” are recorded as-is） · **Autocorrelation plot／自相關圖**（lag 0 = 1; x = lag, y = coefficient; ±1.96/√n fixed band vs Bartlett widening band; R `acf` default fixed width, statsmodels `plot_acf` and Stata `ac` default Bartlett; slow decay = trend/non-stationary → difference first; spikes at multiples of 7/12 = possible season; PACF cut-off suggests AR order only as a starting point; short series spikes are noise; correlogram has two meanings — the variable×variable one is 「相關矩陣」 (correlation matrix heatmap), not this chart; R16 is the Wikimedia Commons Article Feedback five-rating correlation heatmap, CC BY-SA 3.0, credit Protonk; R17 is described as 「判斷為 Stata 輸出風格」） · **Lag plot／滯後圖**（square scatter: x = the value k steps ago, y = the value now, same scale, plus the diagonal; n points give n−k pairs; a cloud ≈ near-random, along the diagonal = positive autocorrelation, an ellipse or ring = a period, a curve = nonlinear structure one autocorrelation bar hides; Pearson on the pairs is roughly the k-th bar but not the same definition; S2 sample correlation 0.763 vs model coefficient 0.9 is sampling bias（抽樣偏差）, not a miscalculation; correlation near 0 is not “no relationship”; a trend or random walk can look like strong memory — detrend first; one outlier shows up as four diamonds (S6); S7 is vertical only, 上／中／下; 「龐加萊圖」 only for the heart-rate chart R13, and R12 stays English “Poincaré map”; a grid (R10) or a filled square (R8) is not dependence; Taiwan official name unverified; mainland 「滞后图」 is quoted only） · **Seasonal subseries plot／季節子序列圖**（also cycle plot — Chinese 「循環圖」 official name unverified; `monthplot` / `month_plot` / `quarter_plot` / `cycleplot` are function names, not another chart; monthly → 12 panels, quarterly → 4, day-of-week → 7; each panel is one season position across years as a small line plus a horizontal mean, shared y-axis; mean-line height = which month is high or low, within-panel slope = whether that month itself is changing; the autocorrelation plot and the lag plot only answer “is there seasonality?”; a seasonal plot — one full line per year — is not this chart; S2 is top/middle/bottom only, S7 is vertical only（上／中／下）; three detrend methods are not the same figure — R16 subtracts a quadratic fit on Mauna Loa monthly CO2 2000–2025 (May ≈ +3.15 ppm, Sep ≈ −3.35, Oct −3.34 almost the same; lesson “高低約 6.5”, selfcheck of the unrounded difference then rounded = 6.51), S4 subtracts a linear trend (within-panel slopes ≈ 0, range 10.2, June high, January low), and “subtract that year’s 12-month mean” is only a comparison on the same CO2 file (May ≈ +2.87, Sep ≈ −2.88, range ≈ 5.7), not R16 and not S4; the deseasonalized column’s May ≈ 2.99 → 3.27 / Sep ≈ −3.32 → −3.44 is a separate description, cause unverified, and the selfcheck does not check it; R1 was already linearly detrended by the NIST/SEMATECH handbook (US government public domain); R15 is the undetrended counterexample, each panel’s mean slope ≈ 2.29 ppm/year; R8 is a counterexample — S&P 500 1985–2024 monthly percent changes in polar coordinates, no within-panel year path, Wikimedia Commons CC BY-SA 4.0, RCraig09, not investment advice; NOAA GML Mauna Loa CO2 is US government public domain, downloaded 2026-10-11 (observations paused Dec 2022–early Jul 2023; values from Mauna Kea); figure numbers R1, R8, R15, R16, S1–S8 are not renumbered; “at least 4–5 years” is practical advice, 查無文獻; Taiwan official name unverified; mainland 「季节子序列图」 is quoted only） · **Seasonal decomposition plot／季節分解圖**（aliases by algorithm, not other charts: classical decomposition plot／古典分解圖, STL decomposition plot／STL 分解圖 — Seasonal and Trend decomposition using Loess; `seasonal_decompose` / `STL` / `decompose` / `stl` are function names, not another chart; a seasonally adjusted series is one line and is not this chart; vertical panels share one time axis, usually observed → trend → seasonal → residual; compare each panel’s scale first; additive: observed = trend + seasonal + residual; multiplicative: observed = trend × seasonal × residual; monthly period 12, quarterly 4, weekday 7; classical moving average leaves the first and last 6 months without trend or residual (S1); amplitude growing with the level → multiplicative (S2: additive residual SD of the first/last 24 months 14.47/15.98 vs multiplicative 0.02/0.01); a changing season or an outlier → robust STL (S3 residual SD 5.28 classical vs 2.39 STL; S5 classical trend bulge at most 5.4 vs robust STL 1.1); no real season still draws a seasonal panel — do not trust it when the residual is larger (S4: seasonal max abs 1.29 vs residual SD 2.64); STL is additive only, log first for a multiplicative reading; not X-11 / SEATS / X-13ARIMA-SEATS; R4’s main line is the seasonally adjusted series plus a small seasonal inset, R5 is the seasonal component only — neither is the four-panel chart; S2–S5 are vertical only（上／中／下）; figure numbers R1–R5, S1–S5 are not renumbered; R1 Wikimedia Commons CC BY 4.0 Heredia Roberto, R2 CC BY-SA 4.0 EpochFail, R3 CC BY-SA 3.0 Junkie.dolphin, R4 CC0 Ldecola, R5 NASA public domain; Taiwan official name unverified; mainland 「季节分解」 is quoted only） · **Scatterplot matrix／散布圖矩陣**（also pairs plot, SPLOM; `pairplot` / `scatter_matrix` / `pairs` are function names, not other charts; about 3–4 numeric variables, diagonal = histogram or density, other cells = points, upper triangle may show Pearson correlations; one pair → correlation scatter; coefficients only or too many columns → correlation heatmap, then redraw 3–4 columns; same series lagged k → lag plot; many features and one profile per row → parallel coordinates; groups need color AND shape — R1, R2 and R4 are iris and distinguish groups by color only, which violates that rule; R2 uses the same square for every group; R4 colors are spectral-cluster labels, not the original species; the correct demo is S3, Palmer Penguins CC0, circle / square / triangle plus color, and the CSV has 品種, not a shape column; 巴布亞 sits toward the upper right on flipper length × body mass but the ranges overlap — say 偏右上; S1 n=80, corr(甲,乙)≈0.7124228200726517; S2 petal length/width r≈0.962865431402796; S4 is left/right, 7 variables, max |off-diagonal| r≈0.8067857797701805 for 丙–戊; S5 n=61, outlier (22, 4, 18) leaves the cloud in several cells at once; S1/S4/S5 fictional, seed 20261014; S2 iris public domain; figure numbers R1–R5, S1–S5 not renumbered; R5’s nine scagnostics are not something to compute; R3 abbreviations unverified; Taiwan official name unverified — the lesson recorded no lookup, so this repo did not look one up; no png copied; `draw_splom.py` is named in the materials note and is not included） · **Taylor diagram／泰勒圖**（Karl E. Taylor, 2001; polar semicircle of standard deviation, correlation, and centered RMSE after the mean is removed; observation on the x-axis; different units are divided by the observation standard deviation so the observation sits at radius 1; shape plus color plus labels, and a revision is drawn as an arrow; mean bias alone is Bland–Altman — this diagram subtracts the mean first and does not show mean bias; too many models is the S4 counter-example; S3 is top/bottom, raw vs normalized, and centered RMSE is computed only on the normalized panel with s_r = 1; S4 is top/bottom, twenty-four points over four, but the CSV has only the four-point panel and the selfcheck did not verify those 24; S1 model 甲 std 1.2, corr 0.75, centered RMSE 0.8, CSV note 示意 while the figure caption says a red square; S2 model A centered RMSE 0.3999999999999999 and the closest of six; S5 the new version is closer than the old; S1–S5 are simulated example data, seed 20261015, numbers unverified; R3–R5 numbers stay 未核; R2’s lesson caption does not say 數字未核, the materials note does, and neither was remeasured; figure numbers R1–R5, S1–S5 not renumbered; Taiwan official name unverified — the lesson recorded no lookup, so this repo did not look one up; the lesson recorded no other spelling, so none is quoted; no png copied; a drawing script named in the materials note was not copied and its filename is not repeated here） · **Periodogram／週期圖**（whole-series estimate of power spectral density: x = frequency, y = power, peaks = frequencies; frequency changing over time is a spectrogram — window length, STFT and dB stay in examples/spectrogram.md; autocorrelation looks at lag; a single-segment periodogram’s noise does not shrink just because the series is longer, so average with Welch; Hann lowers sidelobes versus a rectangular window when the true frequency is off-bin; S1 CSV n=200 peaks at exactly 20.0 Hz, raw power 10192.720424279498, the sim note’s n=1024 peak 19.922 is not in the file; S2 nearest bins 12.109375 Hz power 0.0568727306453308 and 37.109375 Hz power 0.02650337611567428; S3 both windows peak at 10.15625 Hz and 0.0 dB, Hann sidelobe outside ±2 bins is −34.20898840629693 dB versus rectangular −17.019584057359197 dB, both at 11.328125 Hz; S4 Welch peak 25.0 Hz power 0.41938521275201973, raw panel not in the CSV; S5 peaks at 15.0 Hz power 1.201085763474063 and 40.0 Hz power 1.2359419294357712, time order is not in the CSV; R2 and R4 numbers stay 數字未核; R3 is a method comparison only, the page marks a mirror-image dispute; S1–S5 simulated example data, seed 20261016; Taiwan official name unverified — the lesson recorded no lookup; no png copied; a drawing script named in the materials note was not copied and its filename is not repeated here） · **Bode plot／波德圖**（shared log frequency; gain in dB on top, phase in degrees below; system amplification and delay when input and output can be compared; a signal’s frequencies are a periodogram, frequency vs time is a spectrogram; linear axis crowds the corners; control loops need both margins; R3 f_GM and f_PM labels stay swapped; R4 ~5 kHz and ~30° stay 數字未核; S1–S5 simulated example data, seed 20261017; Taiwan official name unverified; no png） · **Hovmöller diagram／霍夫默勒圖**（also 霍夫穆勒圖, not the primary name; position × time colour grid; read which way it moves and how fast; mark time up or down before a slope — R1 up, S1 down; time downward: down-right is east; frequency-over-time is a spectrogram, a general matrix is a matrix heatmap; one place is a line chart; S1 ridge 3.9151242728714966 °/day, printed 3.915, recorded about 3.89; equatorial conversion printed 5.04 m/s; do not apply 111.2 km per degree at high latitude without the cosine; S3 group-speed ridge printed 27.99 °/day against recorded 28, phase speed 10 °/day is not a separate CSV track; S2 +6 and −8 °/day, S5 −18 km/h, and S4 colormap names stay unchecked; R1 speeds 未核 and latitude doubtful; R2 variable and unit 未核; R5 is a rainbow, direction only; S1–S5 simulated example data, seed 20261018; Taiwan official name unverified — the lesson recorded no lookup; published 1949; no png） · **Skew-T log-P diagram／斜溫圖**（log pressure, isotherms skewed 45°; read temperature along the slant; one place, one time, a vertical profile of stability, possible cloud, and thunderstorm potential; ground values only → line chart; many places and times → Hovmöller; many stations → a map; a 2° dewpoint gap is an experience threshold, 未核, and close lines mean possible cloud; CAPE is read with CIN; joule integrals stay unchecked; S1 at 500 hPa is −5.7°C; R1 CC BY-SA 4.0 JeanBizHertzberg, Wyoming base map 未核 — say 「底圖未核，轉載須再確認」, the whole figure is not license-cleared; R2 CC BY-SA 4.0 TomRat, a schematic; R3 public domain NOAA SPC; R4 public domain NWS; R5 public domain NWS Quad Cities; S1–S5 are 範例資料, seed 20261019; Taiwan official name 未核, the lesson recorded no lookup; Chinese Wikipedia is 〈斜溫圖〉; no png; the drawing-script filename is not written） · **Lorenz curve／洛倫茲曲線**（with the Gini coefficient; sort units from smallest to largest and plot cumulative % of units against cumulative % of income/wealth, with the equality diagonal; always say whether the Gini has the n/(n−1) small-sample correction — 10 households, S3: 0.38 → 0.42; one person taking everything is (n−1)/n = 0.90 for 10 households, not 1; two groups can share a Gini yet have crossing curves, so do not rank them by Gini alone; related to but not the same chart as the Pareto chart: the Pareto cumulative line turned half a turn is the Lorenz curve of the same numbers） · **control chart／管制圖**（Shewhart chart; ≠ line chart, ≠ Pareto, ≠ spec limits; control limits come from process data, not from specs; the "same-side run" rule is 8 points in Western Electric but 9 in Nelson, so agree the rule set first） · **Pareto chart／柏拉圖／帕累托圖**（≠ plain bar chart, ≠ waterfall, ≠ funnel; related to but not the same chart as the Lorenz curve (the cumulative line turned half a turn is the Lorenz curve of the same numbers); cumulative-% line on a 0–100% right axis; set the left-axis max to the total; 80/20 is a rule of thumb, read at which item the line first reaches 80%; 「其他」 usually goes far right） · **horizon chart／地平線圖**（≠ streamgraph, ≠ ridgeline, ≠ heatmap; colour bands trade layers for height; write the baseline; rows are not comparable unless they share a band width） · **forest plot／森林圖**（≠ funnel plot for meta-analysis, ≠ business Funnel chart; log axis for ratio measures; square area ∝ weight） · **karyotype／ideogram plot／核型圖／染色體帶型示意圖**（≠ Manhattan, ≠ Circos; karyogram and idiogram are synonyms） · **LocusZoom plot／LocusZoom 圖**（區域關聯圖; ≠ Manhattan; lead variant ≠ causal） · **choropleth／等值區域** · **tile map／圖塊地圖** · **dot density** · **population pyramid／人口金字塔** · **BioFabric／生物織布圖** · UpSet · bullet KPI · **matrix heatmap／矩陣熱圖** · calendar heatmap · **spiral plot／螺旋圖** · cartogram.

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
| `examples/` | 80 patterns (when / recommend / avoid / checklist) |
| `demos/` | Copy-paste first-run prompts |
| `COMMERCIAL.md` | License and how to reach the maintainer |
| `ATTRIBUTION.md` | Teaching-note → pattern mapping |

Grow it: real report → was the pick right → new `examples/<slug>.md` + ATTRIBUTION row → `grok plugin update`.

## Attribution & license

Examples and heuristics were compiled by the project maintainer from internal teaching notes (範例與啟發式由專案維護者依內部教學筆記整理), and each pattern ships with verification data. The original notes are not in this repo; this repo is an executable summary, **not** the full lesson texts. Keep [`ATTRIBUTION.md`](skills/what-is-the-data-saying/ATTRIBUTION.md) when you share.

[MIT](LICENSE) · © 2026 g0uv4 · GitHub only (no Origin).

---

## 資料在說什麼

**MIT 授權的 Grok Build skill（v0.3.42）。** 丟進一張表或一份報表，它回答兩件事：**該畫哪種圖**、**怎麼做得出來**。

和一般「圖表選擇器」的差別：對齊內部教學筆記的台灣繁體中文教學——先給中文圖種名（英文名）、適不適合、口述怎麼做，再給工具。內建 **80 個具名 pattern**，不是示意三張長條圖。

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
