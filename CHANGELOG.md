# Changelog

## 0.3.20 — P–P 圖 pattern

- Add `examples/pp-plot.md` from Nazh teach-viz `2026-10-01-pm-pp.md` (approved skill pack `2026-10-01-pm-pp`; passed Liora; 方法教學). Primary name **P–P 圖**（機率—機率圖, Probability–Probability plot）. Until now it was name-only (as "repo 尚無專檔") in `qq-plot.md`, `chart-heuristics.md`, `data-shape-checks.md`, `how-to-produce.md`, `SKILL.md` and `ATTRIBUTION.md` → new pattern.
- Core lesson: both axes are cumulative probabilities (0 to 1) on a unit square; compare at the same **value**. Variants: sample vs fully specified theoretical CDF, two-sample, parametric／semi-parametric (reliability), regression-residual P–P; stabilized P–P (SP) named only.
- Seven facts pinned: (1) P–P = probability vs probability, QQ = quantile vs quantile; P–P is more sensitive mid-distribution and QQ in the tails — a **qualitative** statement from GeostatsGuy / reliability / SAS, not a theorem, and not in the Wikipedia P–P article; tail differences are "compressed", not "invisible"; (2) sources disagree on which variable goes on which axis (most: x theoretical, y sample; reliability semi-parametric and GeostatsGuy differ); **statsmodels 0.15.0 `ppplot` axis labels are reversed relative to its actual computation** — I re-verified this by installing statsmodels 0.15.0 in a scratch venv and inspecting the rendered plot data on the `sm` dataset (x = i/(n+1), y = fitted CDF, labels "Theoretical Probabilities"／"Sample Probabilities"); this repo's convention is x = theoretical, y = sample; (3) NIST "Probability Plot" and SciPy `probplot` have value-scale axes (QQ-type, not P–P); Kass lecture figure 5 caption says P–P while the figure title says QQ; (4) the "P value plot" (Davidson & MacKinnon 1998) is a P–P structure (p-value distribution vs uniform), not a Manhattan plot; (5) plotting positions i/n, (i−0.5)/n, i/(n+1) differ by source and must be stated; a non-square canvas makes the diagonal not 45° (Commons example ≈ 29°); (6) licences: GeostatsGuy CC BY-NC-ND 4.0 (non-commercial, no derivatives), reliability LGPL 3.0, Commons `wiki-pp-quality` CC0 1.0, NIST public information (credit requested), other single images not individually confirmed; (7) the pack's Gemini polish step was **not** done (login expired) — the text is the post-review original (noted in ATTRIBUTION). No images copied.
- Neighbour boundary table vs QQ, NIST Probability Plot, SciPy `probplot`, Bland–Altman, Manhattan／LocusZoom, scatter, stabilized P–P (name only). Name-only P–P mentions in `qq-plot.md` now link the new file (the "no example file" wording is removed); the QQ line "tail differences more visible on QQ — source not confirmed" now cites the three sources and is labelled qualitative. Back-links added in `bland-altman.md`, `manhattan-plot.md` and `correlation-scatter.md`.
- Heuristics / how-to / data-shape check 30 (sortable numeric data; fully specified reference CDF; plotting position and axis assignment stated; equal-axis square). Tool honesty: statsmodels 0.15.0 (modified BSD), reliability 0.9.0 (LGPL 3.0), Statistica 14.2.0 help, SAS help; other licences left blank. 23 pack sources were openable (21 linked, 2 deliberately not linked: Dataviz Project home and Python Graph Gallery home — open, but no P–P page); 3 unopenable sources (data-to-viz, R Graph Gallery, Dataviz Project QQ pages, all 404) named only, unchecked and **not** sources. X: the pack found no teaching post, none invented.
- Fictional demo CSV `sample-pp-fictional.csv` (1,000 rows, ~30 KB; three `#` header lines; 數字未核) and `sample-pp-selfcheck.py` (needs numpy + scipy; reads the CSV by explicit filename; asserts all counts and percentages); both byte-identical to the pack (`cmp`); selfcheck output matches the pack line for line. Independently recounted all figures with separate code (no pack-vs-CSV mismatch found). Note: the "all points above／below the diagonal" counts refer to **specified x-intervals** (e.g. 147 of the 200 `heavy` points), not to the whole sample.
- `examples/data/README.md`: P–P selfcheck section. `COMMERCIAL.md` pattern count 57 → 58. ATTRIBUTION cites final teach-viz + pack path, removes the "P–P has no example file" wording, and notes the skipped Gemini polish.

## 0.3.19 — LocusZoom 圖 pattern

- Add `examples/locuszoom.md` from Nazh teach-viz `2026-10-01-am-locuszoom.md` (approved skill pack `2026-10-01-am-locuszoom`; passed Liora; 方法教學). Primary name **LocusZoom 圖**（通稱區域關聯圖／regional association plot）. Until now it was name-only (as 區域放大圖／LocusZoom, "no example file") in `manhattan-plot.md`, `qq-plot.md`, `volcano-plot.md`, `chart-heuristics.md`, `data-shape-checks.md`, `how-to-produce.md` and `SKILL.md` → new pattern. Neighbour wording unified to 區域關聯圖.
- Core lesson: zoom into one chromosome interval after the Manhattan plot — x = position in the interval, y = −log10(p), points coloured by LD r² to the lead (index) variant, gene track below, optional recombination-rate overlay.
- Five facts pinned: (1) the zh term 「鉛變體」 is a mistranslation of "lead"; write 領先（lead）變異／指標變異; (2) the lead variant is not causal; a high-LD cluster is consistent with a single signal but does not prove it (nor does it mean many independent hits); a low-LD second peak needs **conditional analysis** before being called independent; (3) LD depends on the reference panel and population; colocalization, fine-mapping and conditional analysis are three different things, none of them is the LocusZoom plot itself; (4) colours and units depend on the tool (LocusZoom.js lead = purple diamond, locuszoomr = red diamond; locuszoomr's eQTL plot colour is eQTL effect, not LD; its right axis is Recombination rate (%) vs cM/Mb in LocusZoom.js); (5) licences: Pruim 2010 figure CC BY-NC (non-commercial only), Wikipedia regional association plot CC BY-SA 2.5, Boughton 2021 figure CC BY 4.0, everything else not explicit. PMC3605911 is a virus paper and not a source (PMC2935401 = Pruim 2010, PMC8479674 = Boughton 2021). No images copied.
- Neighbour boundary table vs Manhattan, QQ, volcano, MA／Bland–Altman, scatter, Circos, fine-mapping／colocalization／karyotype (name only). Name-only LocusZoom mentions in `manhattan-plot.md`, `qq-plot.md`, `volcano-plot.md` now link the new file (the "no example file" wording is removed); back-links added in `circos.md` and `correlation-scatter.md`.
- Heuristics / how-to / data-shape check 29 (variant position + p; lead variant and LD reference stated; gene annotation). Tool honesty: LocusZoom.js v0.14.0 (MIT per Boughton 2021, licence file not verified), locuszoomr 1.1.0 (CRAN, 2026-09-17; licence not stated in the pack), locuscomparer name only. 19 pack sources were openable (17 linked, 2 deliberately not linked: a duplicate Wikipedia `File:` page and the `locuszoom.org` https URL that the pack says only works over http); 8 unopenable sources (7 × 404, Biostars 403) named only, unchecked. X: the pack found no teaching post (0 results), none invented.
- Fictional demo CSV `sample-locuszoom-fictional.csv` (2,306 rows, ~112 KB; two `#` header lines; 數字未核) and `sample-locuszoom-selfcheck.py` (needs numpy; reads the CSV by explicit filename, runs in place); both byte-identical to the pack (`cmp`); selfcheck output matches the pack. Independently recounted all figures. Pack-vs-CSV notes: the "points above the threshold" counts (17／28／17／17) include the lead variant itself (16／27／16／16 without it), and in `second` only 3 of the 14 second-peak points exceed 7.30 (the pack's line says the peak's top point does). Actual count governs.
- `examples/data/README.md`: LocusZoom selfcheck section. `COMMERCIAL.md` pattern count 56 → 57. ATTRIBUTION cites final teach-viz + pack path and removes the "LocusZoom has no example file" wording.

## 0.3.18 — Bland–Altman 圖 pattern

- Add `examples/bland-altman.md` from Nazh teach-viz `2026-09-30-pm-ba.md` (approved skill pack `2026-09-30-pm-ba`; passed Liora; 方法教學). Primary name **Bland–Altman 圖**（差值圖／Tukey mean-difference plot）. Until now it was name-only in `ma-plot.md`, `qq-plot.md`, `chart-heuristics.md` and `how-to-produce.md` (no example file existed) → new pattern.
- Core lesson: paired measurements of the same samples by two methods; x = (A + B) / 2, y = difference (**direction must be in the title**), mean difference line plus limits of agreement (mean ± 1.96 SD of the differences; the 1986 paper used 2 SD for simplicity). Variants: fixed bias, proportional bias (regression-based limits), funnel shape (percent difference, log transform), non-normal differences (2.5th / 97.5th percentiles), repeated measures (name only with caveats).
- Five facts pinned: (1) **limits of agreement are not confidence intervals**; the mean difference and each limit have their own CIs; interchangeable only if the limits *and their CIs* lie within an a-priori acceptable range, which is a clinical / professional judgement, not a statistical one; (2) **high correlation does not mean agreement**, and it is **not** "exactly 95% of points must fall inside the limits"; (3) **difference direction differs across sources** (Wikipedia new − gold standard, X post B − A, Giavarina A − B, York figures large − mini / long − short); this repo's demo data is consistently **method B minus method A**; (4) MA plot is the log-transformed application to genomic data in spirit but has a **different purpose and reading threshold** — not written as the same structure; (5) Hanneman 2008 is **PMC2944826**; apart from the Wikipedia top image (CC BY-SA 3.0, Commons `Bland-Altman_Plot.svg`) no external image licence is explicit, so none is freely reusable. No images copied.
- Neighbour boundary table vs MA, scatter + correlation, QQ, volcano, Passing–Bablok / Deming (name + Wikipedia link only) and Gardner–Altman (name only). Name-only Bland–Altman mentions in `ma-plot.md` and `qq-plot.md` now link the new file (the "no example file" wording is removed); back-links added in `correlation-scatter.md`.
- Heuristics / how-to / data-shape check 28 (paired measurements; differences, not measurements, checked for normality; direction stated). Tool honesty: statsmodels BSD-3, pingouin GPL-3.0, BlandAltmanLeh GPL-2 or GPL-3, blandr GPL-3 (code); MedCalc manual page © 2026 MedCalc Software Ltd; Matplotlib licence left blank. 24 sources in the pack were openable (21 linked, 3 deliberately not linked: a duplicate Wikipedia `File:` page, a statsmodels image URL, a GraphPad FAQ page without Bland–Altman content); 8 unopenable sources (7 × 404, 1 × 410) named only, unchecked. X: two posts from the pack linked with a caveat (community side-evidence, not a primary source).
- Fictional demo CSV `sample-ba-fictional.csv` (220 rows, ~6 KB; two `#` header lines; 數字未核; good 100 pairs + fan 120 pairs) and `sample-ba-selfcheck.py` (needs numpy; reads the CSV by explicit filename next to the script, so it runs in place); both byte-identical to the pack (`cmp`). Selfcheck output matches the pack. Independently recounted: good n = 100, mean diff 0.703, SD 2.424, limits 5.454 / −4.047, 7 points outside (7%, the pack's script comment says "about 5%" — actual count governs); fan n = 120, mean diff 0.583, SD 5.375, limits 11.118 / −9.952, 5 points outside (not stated in the pack).
- `examples/data/README.md`: Bland–Altman selfcheck section; the `glob('*-fictional.csv')[0]` pitfall of `sample-qq-selfcheck.py` now applies to **three** `*-fictional.csv` files (it fails in place with `KeyError: 'group'` on this machine), so the copy-to-a-temp-folder recipe is now required, not optional.
- `COMMERCIAL.md` pattern count 55 → 56. ATTRIBUTION cites final teach-viz + pack path. Pattern count 55 → 56.

## 0.3.17 — QQ 圖 pattern

- Add `examples/qq-plot.md` from Nazh teach-viz `2026-09-30-am-qq.md` (approved skill pack; 方法教學); primary name **QQ 圖**（Q–Q plot／分位數－分位數圖）. No QQ example existed (only name-only mentions in Manhattan／heuristics) → new pattern.
- Core lesson: quantiles of one distribution against another (sample vs theory, or two samples; sizes need not match); axis placement is a convention — read the axis titles first. Variants: normal QQ, two-sample QQ, GWAS-style (expected vs observed −log10 p), residual QQ; normal probability plot as a special case. Three reference-line conventions (y = x, quartile line, fitted line) in a table labelled 「範例，不是標準」; shape-reading table (right skew, heavy tails S-shape, short tails reverse S, outliers; bimodal unsupported by sources, not invented); small-sample caveat.
- Three facts pinned: (1) points on y = x mean similar distributions, points on any straight line only mean a linear relationship (location／scale differ); (2) SciPy `probplot` docs say it is not a Q-Q plot, qqman `qq()` does not compute λ or draw confidence bands, λ has **no single official threshold** (1.05 and 1.10 from secondary sources disagree); high λ can be genuine polygenic signal; (3) NIST, SciPy, statsmodels, ggplot2, qqman and X figures have no explicit licence — not freely reusable; Getting Genetics Done figures are CC BY-NC (non-commercial only); Wikipedia／Commons figures need author + licence. Stated in ATTRIBUTION; no images copied.
- Neighbour boundary table vs Manhattan, P–P (name only), Bland–Altman (name only), LocusZoom (name only), scatter, volcano, MA. `manhattan-plot.md` now links QQ instead of naming it; back-links added in `volcano-plot.md`, `ma-plot.md`, `correlation-scatter.md`, `boxplot-summary.md`, `violin-distribution.md`, `ridgeline-density.md`, `raincloud-combo.md`.
- Heuristics / how-to / data-shape check 27. Tool honesty: qqman GPL-3, statsmodels BSD-3 (code), SciPy BSD, ggplot2 MIT; R qqnorm／car／Matplotlib licences left blank. Nine unopenable sources (7 × 404, Statology 202 blank, Penn State connection failure) named only, unchecked; Khan Academy page not used (site returns one generic JS-check page for every path). X: three posts from the pack linked with caveats (one infographic with "fits the line = matches" oversimplification; two self-declared AI-made) — none used as teaching material.
- Fictional demo CSV `sample-qq-fictional.csv`（220 rows, ~6 KB; two `#` header lines; 數字未核）and `sample-qq-selfcheck.py` (needs numpy + scipy). README documents a `glob('*-fictional.csv')[0]` pitfall now that `examples/data/` holds two `*-fictional.csv` files, with a safe run recipe; both files byte-identical to the pack. Pack text "about 6% carry signal" for `pvalue_sim` cannot be verified from the CSV (15 / 220 rows have p < 0.05); actual count governs.
- `COMMERCIAL.md` pattern count 54 → 55. ATTRIBUTION cites final teach-viz + pack path, removes the "QQ has no example file" wording, and fixes leftover simplified characters (入库 → 入庫, 提炼 → 提煉). Pattern count 54 → 55.

## 0.3.16 — MA 圖 pattern

- Add `examples/ma-plot.md` from Nazh teach-viz `2026-09-29-pm-ma.md` (approved skill pack; 方法教學); primary name **MA 圖**（MA plot；平均－差值圖／MD plot）. No MA example existed (only name-only mentions in volcano／heuristics) → new pattern; `ma-plot.md` does not clash with any existing file.
- Core lesson: one point per feature; x = A (mean expression), y = M (log fold change), M = 0 line; diagnostic view (normalisation, shrinkage, low-count funnel) rather than candidate ranking. "Centred on M = 0" is an assumption, not a law. Parameter table (DESeq2 `alpha` 0.1 / `svalue` 0.005, HBC 0.05 & 0.58, NotchBio, biostatsquid |M| > 1, ±0.5 threshold tests, TMM ~30%) labelled 「範例，不是標準」.
- Three facts pinned: (1) `lfcShrink` does not change p-values by default, significant points are only pulled toward zero — **labelled inference**; shrinkage is a deliberately zero-biased estimate, not the truth; (2) RA plot puts R on the y-axis like M — the difference is integer counts and the ε handling of zero-count points; (3) a website's "MA vs volcano" table wrongly says the volcano x-axis is significance (opposite to mainstream) — corrected and flagged "do not copy". Also: limma `plotMA` not removed (`plotMD` same function, different arguments).
- Neighbour boundary table vs volcano, Manhattan, scatter, Bland–Altman (name only, no file), RA plot, Circos. `volcano-plot.md` and `manhattan-plot.md` now link MA instead of naming it; `correlation-scatter.md` back-link added.
- Heuristics / how-to / data-shape check 26. Tool honesty: DESeq2 (LGPL ≥ 3), limma／edgeR (GPL ≥ 2), geneplotter (Artistic-2.0), Glimma (GPL-3), apeglm (GPL-2); other licences left blank; NotchBio all rights reserved (link only, images not used). Seven 404 sources (gallery／catalogue pages, Commons `Category:MA_plots`, rdrr `plotMA`) named only, unchecked; the only X result was workshop promo → none cited.
- Fictional demo CSV `sample-ma-fictional.csv`（3,000 rows, ~230 KB; two `#` header lines; 數字未核）and self-check script `sample-ma-selfcheck.py` (stdlib only; documented in `examples/data/README.md`; ran OK before release).
- `COMMERCIAL.md` pattern count 53 → 54. ATTRIBUTION cites final teach-viz + pack path and no longer says MA has no example file; images cited, not copied. Pattern count 53 → 54.

## 0.3.15 — 曼哈頓圖 pattern

- Add `examples/manhattan-plot.md` from Nazh teach-viz `2026-09-29-am-manhattan.md` (approved skill pack; 方法教學); primary name **曼哈頓圖**（Manhattan plot）. No Manhattan example existed → new pattern.
- Core lesson: one point per marker (SNP); x = genomic position ordered by chromosome 1, 2, 3… with alternating colours; y = −log10(p); skyline of towers; pre-agreed threshold lines. Variants: linear, circular (CMplot; still not Circos), **Miami plot** (mirrored two-trait variant, no separate pattern), interactive, single-chromosome crop. Threshold table (5×10⁻⁸, 1×10⁻⁵ tool default with unverified academic origin, CMplot demo 1×10⁻⁶／1×10⁻⁴, volcano 0.05) labelled 「範例，不是標準」.
- Neighbour boundary table vs volcano, scatter, QQ plot, Circos, regional plot (LocusZoom), Miami, karyotype ideogram. `volcano-plot.md` and `circos.md` cross-linked both ways (volcano now links Manhattan instead of naming it); QQ plot and LocusZoom named only (no files).
- Heuristics / how-to / data-shape check 25 (marker, chromosome from 1, position, p; cumulative x; QQ companion). Tool honesty: qqman (GPL-3), CMplot (GPL ≥ 2), Dash Bio ManhattanPlot (MIT); **manhattanly archived from CRAN on 2025-06-13** — historical reference only. LocusZoom source is Pruim et al. 2010 (PMC2935401); previously mis-cited PMC3605911 (a viral phylodynamics paper) excluded. Unreachable sources (Pe'er 2008 PubMed 203, Plotly R pages, gallery-site Manhattan pages, Wikipedia Miami plot／LocusZoom, etc.) named only, unchecked; no X teaching post (none invented).
- Fictional demo CSV `sample-manhattan-gwas.csv`（6,427 rows, ~230 KB, 3 fictional peaks on chr 3／11／17；數字未核）.
- `COMMERCIAL.md` pattern count 52 → 53. ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count 52 → 53.

## 0.3.14 — 火山圖 pattern

- Add `examples/volcano-plot.md` from Nazh teach-viz `2026-09-28-pm-volcano.md` (approved skill pack; 方法教學); primary name **火山圖**（Volcano plot）. No volcano example existed → new pattern.
- Core lesson: one point per feature; x = log2 fold change (direction + magnitude), y = −log10 p — raw **or** adjusted, and the plot must say which. Pre-registered threshold lines, 3- or 4-colour categories, sparse labels. Threshold table (MetwareBio, Harvard HBC, Galaxy, biostatsquid, EnhancedVolcano manual) labelled 「範例，不是標準」; EnhancedVolcano vignette ">|2|" vs manual FCcutoff 1 conflict noted (manual wins). Cui & Churchill 2003 *Genome Biology*; Li 2012 *JBCB*.
- Neighbour boundary table vs scatter (`correlation-scatter.md`), Manhattan plot, MA plot, topographic contour (name coincidence; ≠ statistical `contour-density.md`), `circos.md`; existing three cross-linked both ways, Manhattan／MA／topographic contour named only (no files).
- Heuristics / how-to / data-shape check 24 (effect size + raw／adjusted p, direction, thresholds before analysis). Tool honesty: EnhancedVolcano (Bioconductor 1.30.0, GPL v3), ggplot2 + ggrepel, DESeq2 `lfcThreshold`, apeglm, Plotly Python (no R page), Galaxy; Seaborn／Matplotlib have no dedicated example; other licences left blank. Plotly R page 404, Dataviz Project page 403→404, docs.biolab.si Orange widget page redirects to docs home — named only, unchecked. No X teaching post (none invented).
- Fictional demo CSV `sample-volcano-de-results.csv`（50 rows, raw + BH-adjusted p；數字未核）.
- `COMMERCIAL.md` pattern count 51 → 52. ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count 51 → 52.

## 0.3.13 — Circos pattern

- Add `examples/circos.md` from Nazh teach-viz `2026-09-28-am-circos.md` (approved skill pack; 方法教學); primary name **Circos**（環狀多軌圖／環形比較基因組視覺）. No Circos example existed → new pattern.
- Core lesson (three layers): ring = scaled reference axis (ideogram), radial tracks = multi-layer signals at the same angle, inner links／ribbons = paired positional relations. Variants: tracks only, tracks + thin links, ribbons, axis breaks／local zoom, table-to-circle (tableviewer; overlaps chord). Krzywinski et al., *Genome Research* 2009;19(9):1639–1645.
- Neighbour boundary table vs chord (`chord-matrix.md`), arc (`arc-diagram.md`), hierarchical edge bundling (no file; heuristics only), circular bar (`circular-bar.md`), sunburst (`sunburst-hierarchy.md`); existing four cross-linked both ways.
- Heuristics / how-to / data-shape checks (sector／track／link tables, positions within sector length, orientation). Tool honesty: Circos GPL v3 (Perl, 0.69-10); circlize (CRAN 0.4.18, MIT) and pyCirclize (PyPI 1.10.1, MIT; "inspired by circlize and pyCircos") are same-family implementations, not official; vigsterkr/circos unofficial, relation unverified. English Wikipedia "Circos" redirects to chord diagram — not cited as a Circos page. Unreachable sources named only; no X teaching post (none invented).
- Fictional demo CSVs `sample-circos-sectors.csv`, `sample-circos-track.csv`, `sample-circos-links.csv`（數字未核）.
- `COMMERCIAL.md` pattern count 50 → 51. ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count 50 → 51.

## 0.3.12 — 火焰圖 pattern

- Add `examples/flame-graph.md` from Nazh teach-viz `2026-09-27-pm-flamegraph.md` (approved skill pack; 方法教學); primary name **火焰圖**（Flame Graph；Brendan Gregg 2011）. No flame-graph example existed → new pattern.
- Core lesson: merged stack samples; width = share of sample population, height = stack depth, x-axis sorted alphabetically by frame name to maximise merging — **not time**. Variants: CPU (random warm colours, no data meaning), Memory, Off-CPU, Hot/Cold (experimental), Differential (red／blue), inverted／icicle layout, FlameScope sub-second heatmap.
- Explicit three-way boundary table: Flame Graph vs **Flame Chart**（火焰時序圖；x = time; Chrome DevTools Performance, speedscope Time Order）vs **icicle**（`hierarchy-icicle.md`; generic hierarchy composition). Plotly's "flame chart" = upward icicle alias. Icicle ↔ flame graph cross-linked both ways, not merged; also linked from sunburst／time-series.
- Heuristics / how-to / data-shape checks (folded-stack format, [unknown] frames, sampling conditions). Tool honesty: brendangregg/FlameGraph (CDDL 1.0), d3-flame-graph, speedscope, FlameScope; licences not stated in pack left blank. ACM Queue 403, wrong-DOI 404, ACM DL cookie wall, no Dataviz Catalogue／data-to-viz／Dataviz Project pages noted by name only; no X teaching post (none invented).
- Fictional demo `examples/data/sample-flamegraph.txt` (folded stacks, **not CSV**; 27 lines, 3,626 samples; 數字未核) plus a note on converting folded stacks to a path／parent／self／total table.
- Fix stale pattern count in `COMMERCIAL.md` (39 → 50). ATTRIBUTION cites final teach-viz + pack path; images (incl. SVG) cited, not copied. Pattern count 49 → 50.

## 0.3.11 — BioFabric pattern

- Add `examples/biofabric.md` from Nazh teach-viz `2026-09-27-am-biofabric.md` (approved skill pack; 方法教學); primary name **BioFabric**（生物織布圖／表格式網路圖；中文為暫譯）. No dedicated example existed (repo had `adjacency-matrix.md`, `force-network.md`, `arc-diagram.md`) → new pattern.
- Core lesson: nodes = horizontal lines (one row each), edges = vertical segments (one column each) — an orthogonal tabular view that combs the hairball so every edge is individually visible; row／column ordering is itself the analysis. Variants: default BFS／degree layout, connectivity layout, shadow links, link groups, node-zone shading, subset views／navigation. Longabaugh 2012, BMC Bioinformatics 13:275, DOI 10.1186/1471-2105-13-275.
- Neighbours cross-linked with boundaries: `force-network.md`, `arc-diagram.md`, `adjacency-matrix.md`, `chord-matrix.md` (HEB／hive plot in heuristics).
- Heuristics / how-to / data-shape checks. Tool honesty: BioFabric Java (LGPL 2.1), RBioFabric (GitHub only, not on CRAN), D3BioFabric, yFiles; no dedicated pages on Dataviz Catalogue／data-to-viz／Dataviz Project; failed URLs recorded by name only; no X teaching post (none invented). Gallery "GOT-1200" image is Influential Thinkers, not the TV series.
- Fictional demo CSV `examples/data/sample-biofabric.csv`（17 nodes, 38 edges; social／collaboration／reporting link groups；數字未核）.
- ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count 48 → 49.

## 0.3.10 — 螺旋圖 pattern

- Add `examples/spiral-plot.md` from Nazh teach-viz `2026-09-26-pm-spiral.md` (approved skill pack; 方法教學); primary name **螺旋圖**（Spiral plot／Time series spiral；climate spiral 變體）. No spiral／periodic-time-series example existed before → new pattern.
- Core lesson: time on an Archimedean spiral, one turn = one period (centre earlier, outer newer), same angle = same point in the cycle; track encodings bar／condegram, line／area, spiral heatmap, horizon; climate spiral needs baseline period + units. Pitfalls: undefined turn／direction ("one turn = one month" misreading), dense turns, outer-arc distortion, unstable periods.
- Neighbours cross-linked: `time-series-trend.md`, `calendar-heatmap.md`, `matrix-heatmap.md`, `circular-bar.md`, `radar-profile.md` (plus streamgraph／gantt mentioned).
- Heuristics / how-to / data-shape checks. Tool honesty: R spiralize, D3 community (tomshanley d3-spiral-heatmap, Condegram gist), Hawkins Climate Visuals, NASA SVS 5190; no dedicated pages on data-to-viz／Flourish／R・Python Graph Gallery. Dataviz Project 403 and spiralize COVID app timeout noted; Carlis & Konstan DOI 10.1145/288392.288399; NASA stills attributed to SVS 5383／5057 (not 5190). Two X explainer posts (one flagged for the "one turn = one month" error); no coding tutorial post (none invented).
- Fictional demo CSV `examples/data/sample-spiral.csv`（2017–2024 monthly bike rentals, 96 rows, anomalous 2020 turn；數字未核）.
- ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count 47 → 48.

## 0.3.9 — 矩陣熱圖 pattern 升級

- Upgrade `examples/matrix-heatmap.md` from Nazh teach-viz `2026-09-26-am-heatmap.md` (approved skill pack); primary name **矩陣熱圖**（Heatmap；熱力圖／色階矩陣）. A generic example already existed → upgrade in place; pattern count stays 47.
- Core lesson: two categorical／ordered axes → matrix, colour = value strength; variants annotated heatmap, clustermap (reorder + dendrogram), correlation matrix (Wilke tiles／circles), time × category. Normalise by column／row when scales differ; sequential vs diverging (midpoint) scales, avoid rainbow (Viridis／ColorBrewer); missing ≠ zero; keep fixed axis order unless clustering.
- Calendar heatmap and adjacency matrix are neighbours only (not variants); cross-links added in `calendar-heatmap.md`, `adjacency-matrix.md`, `chord-matrix.md`.
- Heuristics / how-to / data-shape checks. Tool honesty: ggplot2 `geom_tile`, lattice `levelplot` (not ggplot), base `heatmap()`, Seaborn heatmap／clustermap, Plotly, D3 Graph Gallery, Flourish Heatmaps, Highcharts; Datawrapper heatmap pages 404, Flourish how-to 404, Observable 429, D3 heatmap2_basic 404 noted. One X teaching post (clcoding). Correlation-matrix image = wilke-forensic1 (not wilke-correlations).
- Fictional demo CSV `examples/data/sample-heatmap.csv`（12 categories × 7 channels, long format；數字未核）.
- ATTRIBUTION cites final teach-viz + pack path; images cited, not copied.

## 0.3.8 — 圖塊地圖 pattern

- Add `examples/tile-map.md` from Nazh teach-viz `2026-09-25-pm-tilemap.md` (approved skill pack); primary name **圖塊地圖**（Tile map；statebins／tile grid map／格子地圖）. No dedicated example existed before (repo only had `hexbin-density.md` and `cartogram-geo.md`) → new pattern.
- Core lesson: one region = one tile, all tiles equal size; fixes choropleth large-area-low-population bias at the cost of shape／adjacency distortion. Weighted variants (Datawrapper electoral college hexagons, grid cartogram, Wikipedia mosaic cartogram, Tilegrams; tiles = population／votes) written separately and routed to `cartogram-geo.md`; cross-links with `choropleth-map.md` and `cartogram-geo.md`.
- Heuristics / how-to / data-shape checks (one tile per region, unique row/col, complete region codes, weighted tile counts sum to total). Tool honesty: statebins／geofacet／R Graph Gallery, Datawrapper square cantons + U.S. hexagons, Plotly, Tableau, D3; Observable 429 and CDC COVE 403 noted; no X teaching post this round (none invented). Cover／collage images (dw-election-hex, medium-hex, dw-swiss-compare) not cited as tile-map examples.
- Fictional demo CSV `examples/data/sample-tilemap.csv`（state+row+col+value_pct；數字未核）.
- ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count 46 → 47.

## 0.3.7 — 等值區域圖 pattern

- Add `examples/choropleth-map.md` from Nazh teach-viz `2026-09-25-am-choropleth.md` (approved skill pack); primary name **等值區域圖**（Choropleth map；分級設色圖／等值區劃圖）. No dedicated example existed before (only heuristics mentions) → new pattern.
- Core rules: normalize first (rate／per capita／per area) — never fill by totals; totals → 比例符號地圖. Separate from cartogram／比例符號／點密度／流向地圖 with when-to-switch; cross-links with `dot-density-map.md` and `cartogram-geo.md`. Classing (分位數／等距／自然斷點), sequential vs diverging, large-area-low-population bias, missing-value styling.
- Heuristics / how-to / data-shape checks (denominator present, geo codes match boundary file, missing regions ≠ 0). Tool honesty: Flourish = Projection map template; Observable old `@d3/choropleth` deprecated → `@d3/choropleth/2`; 4 verified X teaching posts.
- Fictional demo CSV `examples/data/sample-choropleth.csv`（region+population+cases+rate_per_100k；數字未核）.
- ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count 45 → 46.

## 0.3.6 — 馬里梅可圖 pattern

- Add `examples/marimekko-chart.md` from Nazh teach-viz `2026-09-24-pm-marimekko.md` (approved skill pack); primary name **馬里梅可圖**（Marimekko／Mekko；變寬堆疊長條）.
- Fold mix-ups vs 馬賽克（獨立性）／等寬堆疊／Treemap／Variwide＋軸模式（百分比 vs 絕對值）into `chart-heuristics.md` + how-to / data-shape checks (zh-TW); tool honesty: Datawrapper **無**原生 Marimekko；data-to-viz mosaic 404；Tableau 可能 403；Observable 可能 429；X 無可用教學原帖.
- Fictional demo CSV `examples/data/sample-marimekko.csv`（segment+product+value；數字未核）.
- ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count 44 → 45.

## 0.3.5 — 氣泡圖 pattern

- Add `examples/bubble-chart.md` from Nazh teach-viz `2026-09-24-am-bubble.md` (approved skill pack); primary name **氣泡圖**（Bubble chart／Bubble plot；氣泡散點圖）.
- Fold mix-ups vs bubble map／散點／連結散點／圓堆／Treemap／hexbin／等高線＋**面積≠半徑** into `chart-heuristics.md` + how-to / data-shape checks (zh-TW); tool honesty: Datawrapper＝Scatter 綁 size（無獨立 Bubble）；data-to-viz caveat/bubble、RAWGraphs、DW bubble 部落格 404；Observable 可能 429；X 無可用教學原帖.
- Fictional demo CSV `examples/data/sample-bubble.csv`（entity+x+y+size+region；數字未核）.
- ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count 43 → 44.

## 0.3.4 — 箱形圖 pattern

- Add `examples/boxplot-summary.md` from Nazh teach-viz `2026-09-23-pm-boxplot.md` (approved skill pack); primary name **箱形圖**（Box plot／Box-and-whisker；盒鬚圖）.
- Fold mix-ups vs 小提琴／雨雲／蜂群／直方／長條／誤差棒 into `chart-heuristics.md` + how-to / data-shape checks (zh-TW); tool honesty: Datawrapper **無**原生箱形；data-to-viz graph/boxplot 404；Observable 可能 429.
- Fictional demo CSV `examples/data/sample-boxplot.csv`（group+value；數字未核）.
- ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count 42 → 43.

## 0.3.3 — 人口金字塔 + 棒棒糖圖 patterns

- Add `examples/population-pyramid.md` from Nazh teach-viz `2026-09-22-pm-pyramid.md` (approved skill pack); primary name **人口金字塔**（age-sex／population pyramid）.
- Add `examples/lollipop-rank.md` from Nazh teach-viz `2026-09-23-am-lollipop.md` (approved skill pack); primary name **棒棒糖圖**（lollipop；單點＋基線細莖，勿與啞鈴混）.
- Fold mix-ups vs 長條／龍捲風／啞鈴／點圖／誤差棒 into `chart-heuristics.md` + how-to / data-shape checks (zh-TW).
- Fictional demo CSVs under `examples/data/`（金字塔長／寬表；棒棒糖類別單值；數字未核）.
- ATTRIBUTION cites final teach-viz + pack paths; images cited, not copied. Pattern count 40 → 42.

## 0.3.2 — 河流圖 pattern（正式專題）

- Upgrade `examples/streamgraph-composition.md` from draft to Nazh teach-viz `2026-09-22-am-streamgraph.md` (approved skill pack); primary name **河流圖**（亦稱溪流圖／ThemeRiver）.
- Fold mix-ups vs stacked area / ThemeRiver / ridgeline / alluvial / investment「河道」into `chart-heuristics.md` + how-to / data-shape checks (zh-TW).
- Fictional demo CSVs under `examples/data/`（長／寬表；數字未核）.
- ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count unchanged (40).

## 0.3.1 — 點密度圖 pattern

- Add `examples/dot-density-map.md` from Nazh teach-viz `2026-09-21-pm-dotdensity.md` (approved skill pack).
- Fold 點密度圖 heuristics / how-to / mix-ups into `chart-heuristics.md` and `how-to-produce.md` (zh-TW).
- Fictional demo CSVs under `examples/data/` (one-to-many / one-to-one; 數字未核).
- ATTRIBUTION + pattern count 39 → 40. Images cited, not copied.


## 0.3.0 — public launch

- Bilingual README (English lead + zh-TW) with install, demo, and conversion hooks.
- `COMMERCIAL.md` for B2B use cases (earnings decks, ops dashboards, research digests).
- Copy-paste `demos/` pack: icicle, funnel, waterfall, dumbbell, slope.
- Sharper `SKILL.md` frontmatter for first-time Grok Build users.
- Chart-request Issue template. MIT + Nazh ATTRIBUTION unchanged.
