# ATTRIBUTION（來源與對照）

本 skill **0.3.32** 的圖種啟發式、口述產出步驟與 `examples/` pattern，由專案維護者依內部教學筆記整理，每個 pattern 附驗證資料（來源連結、授權說明，以及虛構 demo CSV 與自檢腳本）；原始筆記不在本 repo。

技能文字為摘要與可執行 checklist，**不是**教學筆記全文轉貼；數字案例沿用原筆記「未核」標註習慣。
原始筆記、草稿與截圖**不在這個公開 repo**；下表左欄只列筆記的日期與檔名，方便對照，不是可開啟的檔案。

## 教學筆記 → pattern／啟發式對照

| 教學筆記（日期與檔名） | 圖種（zh-TW） | skill 落點 |
|----------------|---------------|------------|
| 2026-08-28-am-bump-draft.md | 凹凸圖 | `examples/bump-ranking.md` |
| 2026-08-28-pm-streamgraph-draft.md | 溪流圖（非正式草稿） | 已由 2026-09-22 正式專題取代 |
| 2026-09-22-am-streamgraph.md | 河流圖（Streamgraph／ThemeRiver） | `examples/streamgraph-composition.md`；demo CSV 見 `examples/data/` |
| 2026-08-29-parallel-draft.md | 平行座標圖 | `examples/parallel-coordinates.md` |
| 2026-08-30-am-chord-draft.md | 弦圖 | `examples/chord-matrix.md` |
| 2026-08-31-am-sankey-draft.md | 桑基圖 | `examples/sankey-flow.md` |
| 2026-08-31-pm-sunburst-draft.md | 旭日圖 | `examples/sunburst-hierarchy.md` |
| 2026-09-01-am-icicle-draft.md | 冰柱圖 | `examples/hierarchy-icicle.md` |
| 2026-09-01-pm-upset-draft.md | UpSet | `examples/upset-sets.md` |
| 2026-09-02-am-heb-draft.md | 階層式邊捆綁 | `references/chart-heuristics.md`（HEB 列） |
| 2026-09-02-pm-parallel-sets.md | 平行集合圖 | heuristics（平行集合） |
| 2026-09-03-am-mosaic.md | 馬賽克圖 | `examples/mosaic-crosstab.md` |
| 2026-09-03-pm-circle-packing.md | 圓堆圖 | `examples/circle-packing.md` |
| 2026-09-03-pm-hive.md | 蜂巢圖 | heuristics（網路） |
| 2026-09-04-am-connected-scatter.md | 連接散點圖 | `examples/connected-scatter.md` |
| 2026-09-04-pm-beeswarm.md | 蜂群圖 | `examples/beeswarm-points.md` |
| 2026-09-05-am-ternary.md | 三元圖 | heuristics |
| 2026-09-05-pm-raincloud.md | 雨雲圖 | `examples/raincloud-combo.md` |
| 2026-09-06-am-treemap.md | 矩形樹狀圖 | `examples/treemap-composition.md` |
| 2026-09-06-pm-waffle.md | 華夫圖 | `examples/waffle-percent.md` |
| 2026-09-07-am-alluvial.md | 沖積圖 | `examples/alluvial-stages.md` |
| 2026-09-07-pm-dumbbell.md | 啞鈴圖 | `examples/dumbbell-gap.md` |
| 2026-09-08-am-circular-bar.md | 圓形長條圖 | `examples/circular-bar.md` |
| 2026-09-08-pm-ridgeline.md | 山脊圖 | `examples/ridgeline-density.md` |
| 2026-09-09-am-nightingale.md | 南丁格爾玫瑰圖 | heuristics（易混） |
| 2026-09-09-pm-bullet.md | 子彈圖 | `examples/bullet-kpi.md` |
| 2026-09-10-am-waterfall.md | 瀑布圖 | `examples/waterfall-bridge.md` |
| 2026-09-10-pm-funnel.md | 漏斗圖 | `examples/funnel-stages.md` |
| 2026-09-14-am-gantt.md | 甘特圖 | `examples/gantt-schedule.md` |
| 2026-09-14-pm-radar.md | 雷達圖 | `examples/radar-profile.md` |
| 2026-09-15-am-dendrogram.md | 樹狀譜系圖 | heuristics |
| 2026-09-15-pm-violin.md | 小提琴圖 | `examples/violin-distribution.md` |
| 2026-09-16-am-cartogram.md | 統計變形地圖 | `examples/cartogram-geo.md` |
| 2026-09-16-pm-voronoi.md | Voronoi 樹狀圖 | `examples/voronoi-treemap.md` |
| 2026-09-17-am-arc.md | 弧線圖 | `examples/arc-diagram.md` |
| 2026-09-17-pm-force.md | 力導向網路圖 | `examples/force-network.md` |
| 2026-09-18-am-adjacency.md | 鄰接矩陣 | `examples/adjacency-matrix.md` |
| 2026-09-18-pm-hexbin.md | 六角分箱圖 | `examples/hexbin-density.md` |
| 2026-09-19-am-contour.md | 等高線圖 | `examples/contour-density.md` |
| 2026-09-19-pm-calendar.md | 日曆熱力圖 | `examples/calendar-heatmap.md` |
| 2026-09-20-am-slope.md | 坡度圖 | `examples/slope-two-period.md` |
| 2026-09-20-pm-flowmap.md | 流量地圖 | heuristics（地理） |
| 2026-09-21-am-bubblemap.md | 比例符號地圖 | heuristics（地理） |
| 2026-09-21-pm-dotdensity.md | 點密度圖 | `examples/dot-density-map.md`；demo CSV 見 `examples/data/` |
| 2026-09-22-pm-pyramid.md | 人口金字塔 | `examples/population-pyramid.md`；demo CSV 見 `examples/data/` |
| 2026-09-23-am-lollipop.md | 棒棒糖圖 | `examples/lollipop-rank.md`；demo CSV 見 `examples/data/` |
| 2026-09-23-pm-boxplot.md | 箱形圖 | `examples/boxplot-summary.md`；demo CSV 見 `examples/data/` |
| 2026-09-24-am-bubble.md | 氣泡圖 | `examples/bubble-chart.md`；demo CSV 見 `examples/data/` |
| 2026-09-24-pm-marimekko.md | 馬里梅可圖 | `examples/marimekko-chart.md`；demo CSV 見 `examples/data/` |
| 2026-09-25-am-choropleth.md | 等值區域圖 | `examples/choropleth-map.md`；demo CSV 見 `examples/data/` |
| 2026-09-25-pm-tilemap.md | 圖塊地圖 | `examples/tile-map.md`；demo CSV 見 `examples/data/` |
| 2026-09-26-am-heatmap.md | 矩陣熱圖 | `examples/matrix-heatmap.md`（升級原通用版）；demo CSV 見 `examples/data/` |
| 2026-09-26-pm-spiral.md | 螺旋圖 | `examples/spiral-plot.md`；demo CSV 見 `examples/data/` |
| 2026-09-27-am-biofabric.md | BioFabric（生物織布圖，暫譯） | `examples/biofabric.md`；demo CSV 見 `examples/data/` |
| 2026-09-27-pm-flamegraph.md | 火焰圖 | `examples/flame-graph.md`；demo 已收合堆疊 .txt 見 `examples/data/` |
| 2026-09-28-am-circos.md | Circos（環狀多軌圖） | `examples/circos.md`；demo CSV（扇區／軌道／連線三檔）見 `examples/data/` |
| 2026-09-28-pm-volcano.md | 火山圖（Volcano plot） | `examples/volcano-plot.md`；demo CSV（原始與校正後 p 值）見 `examples/data/` |
| 2026-09-29-am-manhattan.md | 曼哈頓圖（Manhattan plot） | `examples/manhattan-plot.md`（含邁阿密圖變體）；demo CSV 見 `examples/data/` |
| 2026-09-29-pm-ma.md | MA 圖（MA plot；含 RA 圖、Bland–Altman 分界） | `examples/ma-plot.md`；demo CSV 與自檢腳本見 `examples/data/` |
| 2026-09-30-am-qq.md | QQ 圖（Q–Q plot；含 P–P 圖、Bland–Altman、LocusZoom 分界） | `examples/qq-plot.md`；demo CSV 與自檢腳本見 `examples/data/` |
| 2026-09-30-pm-ba.md | Bland–Altman 圖（Bland–Altman plot；差值圖；含 MA 圖、Gardner–Altman 圖、Passing–Bablok／Deming 迴歸分界） | `examples/bland-altman.md`；demo CSV 與自檢腳本見 `examples/data/` |
| 2026-10-01-am-locuszoom.md | LocusZoom 圖（LocusZoom plot；區域關聯圖；含曼哈頓圖、QQ 圖、精細定位／共定位／條件分析、核型圖分界） | `examples/locuszoom.md`；demo CSV 與自檢腳本見 `examples/data/` |
| 2026-10-01-pm-pp.md | P–P 圖（P–P plot；機率—機率圖；含 QQ 圖、NIST Probability Plot、SciPy `probplot`、P value plot 分界） | `examples/pp-plot.md`；demo CSV 與自檢腳本見 `examples/data/` |
| 2026-10-02-am-karyotype.md | 核型圖／染色體帶型示意圖（Karyotype plot／Chromosome ideogram／Ideogram；含曼哈頓圖、LocusZoom、Circos、樹狀圖、長條圖、FISH 分界） | `examples/karyotype-ideogram.md`；demo CSV 與自檢腳本見 `examples/data/` |
| 2026-10-02-pm-forest.md | 森林圖（Forest plot；Blobbogram；含統合分析漏斗圖〔Funnel plot〕、商業漏斗圖〔Funnel chart〕、箱形圖、啞鈴圖、Bland–Altman 分界） | `examples/forest-plot.md`；demo CSV 與自檢腳本見 `examples/data/` |
| 2026-10-03-am-horizon.md | 地平線圖（Horizon Chart；horizon graph；含折線小多圖、矩陣熱圖、河流圖、山脊圖、螺旋圖分界） | `examples/horizon-chart.md`；demo CSV 與自檢腳本見 `examples/data/` |
| 2026-10-03-pm-pareto.md | 柏拉圖（Pareto chart／帕累托圖；含一般長條圖、瀑布圖、漏斗圖、洛倫茲曲線〔相通但不同，見 `examples/lorenz-curve.md`〕、ABC 分析分界） | `examples/pareto-chart.md`；demo CSV 與自檢腳本見 `examples/data/` |
| 2026-10-04-am-control.md | 管制圖（Control chart／Shewhart chart；含折線圖、柏拉圖、直方圖、地平線圖、Levey–Jennings 圖、規格線分界） | `examples/control-chart.md`；8 組 demo CSV 與自檢腳本見 `examples/data/` |
| 2026-10-04-pm-lorenz.md | 洛倫茲曲線（Lorenz curve；含基尼係數；與柏拉圖〔相通但不同〕、折線圖、分位數圖、管制圖分界） | `examples/lorenz-curve.md`；8 組 demo CSV 與自檢腳本見 `examples/data/`（檔名加 `lorenz-` 前綴，s1 與管制圖同名） |
| 2026-10-05-am-marey.md | 馬雷圖／列車運行圖（Marey chart；與折線圖、甘特圖、表列時刻表、趨勢圖〔run chart，中文維基「运行图」轉址處〕、小多圖分界） | `examples/marey-chart.md`；8 組 demo CSV 與自檢腳本見 `examples/data/`（檔名已有 `marey` 前綴） |
| 2026-10-05-pm-km.md | 存活曲線／Kaplan–Meier（與折線圖、森林圖、累積發生率、生態學 survivorship curve、P–P／Q–Q 診斷圖分界） | `examples/kaplan-meier-survival.md`；8 組 demo CSV 與自檢腳本見 `examples/data/`（檔名已有 `km` 前綴） |
| 2026-10-06-am-swimmer.md | 游泳圖（swimmer plot；與泳道流程圖、甘特圖、腫瘤學瀑布圖／蜘蛛圖、Kaplan–Meier、事件時間線分界） | `examples/swimmer-plot.md`；8 組 demo CSV 與自檢腳本見 `examples/data/`（檔名已有 `swimmer` 前綴） |
| 2026-10-06-pm-lasagna.md | 千層麵圖（lasagna plot，暫譯；與義大利麵圖、一般熱圖、游泳圖、序列索引圖、日曆熱圖、地平線圖、鄰接矩陣分界） | `examples/lasagna-plot.md`；8 組 demo CSV 與自檢腳本見 `examples/data/`（檔名已有 `lasagna` 前綴） |
| 2026-10-07-am-recurrence.md | 遞迴圖（recurrence plot，暫譯；與一般熱圖、千層麵圖、鄰接矩陣、折線／時序、地平線圖、距離矩陣熱圖、龐加萊圖分界） | `examples/recurrence-plot.md`；8 組 demo CSV 與自檢腳本見 `examples/data/`（檔名已有 `recurrence` 前綴） |
| 2026-10-08-am-spectrogram.md | 頻譜圖（spectrogram；與頻譜、一般熱圖、千層麵圖、地平線圖、遞迴圖、小波量值圖、三維瀑布圖、財務瀑布圖、腫瘤學瀑布圖分界） | `examples/spectrogram.md`；8 組 demo CSV 與自檢腳本見 `examples/data/`（檔名已有 `spectrogram` 前綴；除 S8 外為縮小版） |

各筆記另有同日的研究筆記與截圖，作為圖例與查證依據，未複製進 repo。

## 素材包與驗證

- 自 2026-09-21（點密度圖）起，各專題另有一份經審核的素材包（說明文件、來源清單、樣本 CSV、圖檔）。公開 repo 只收 pattern 摘要、虛構 demo CSV 與自檢腳本；圖檔不入庫，只列連結與授權。
- 每個 pattern 的來源逐條連結、圖檔授權、查核限制（打不開或無法確認的來源只記名、標未核）與數字重算結果，寫在對應的 `examples/*.md`；demo CSV、自檢腳本與檔名對照見 `examples/data/README.md`。
- 素材包附帶的繪圖產生器與匯出腳本（`draw_forest.py`、`draw_karyo.py`、`draw_horizon.py`、`draw_pareto.py`、`draw_control.py`、`draw_lorenz.py`、`draw_marey.py`、`draw_km.py`、`draw_swimmer.py`、`draw_lasagna.py`、`draw_recurrence.py`、`draw_spectrogram.py`、`export_samples.py`）**不收入本 repo**；其中部分腳本預設把圖寫進教學稿資料夾或覆寫資料檔，這也是不收的原因之一。
- 自檢腳本的輸出以實際重算為準；素材包文字與 CSV 有出入時，範例檔會註明並以實際計數為準。

## 尚未獨立成 pattern 的缺口

- 南丁格爾玫瑰、三元圖、樹狀譜系、蜂巢圖、HEB、流量地圖、比例符號地圖、平行集合：目前多半只在 `chart-heuristics.md`，尚無專檔 example。
- 點密度圖、河流圖、人口金字塔、棒棒糖圖、箱形圖、氣泡圖、馬里梅可圖、等值區域圖、圖塊地圖、矩陣熱圖、螺旋圖、BioFabric、火焰圖、Circos、火山圖、曼哈頓圖、MA 圖、QQ 圖、Bland–Altman 圖、LocusZoom 圖、P–P 圖、核型圖、森林圖、地平線圖、柏拉圖、管制圖、洛倫茲曲線、馬雷圖、存活曲線、游泳圖、千層麵圖、遞迴圖、頻譜圖 已有專檔 example + 虛構 demo CSV；其餘筆記「適合使用的範例」三小節樣本尚未全面打包。
- 社群敘事卡產線未併入本 plugin（敘事卡 ≠ 資料形狀推薦）。

## 授權與改寫

- 原始教學筆記為內部教學素材；本 skill 為 Grok Build 可執行摘要（MIT）。
- 對外分享時請保留本 ATTRIBUTION；勿宣稱教學筆記全文已開源。
- 公開上市版（0.3.x）只開 skill／pattern／demo，不開教學筆記全文。
