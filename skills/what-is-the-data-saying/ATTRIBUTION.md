# ATTRIBUTION（來源與對照）

本 skill **0.3.49** 的圖種啟發式、口述產出步驟與 `examples/` pattern，由專案維護者依內部教學筆記整理，每個 pattern 附驗證資料（來源連結、授權說明，以及虛構 demo CSV 與自檢腳本）；原始筆記不在本 repo。

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
| 2026-10-09-am-autocorr.md | 自相關圖（autocorrelation plot；與偏自相關圖、相關矩陣、折線、遞迴圖、頻譜圖、管制圖分界） | `examples/autocorrelation-plot.md`；8 組 demo CSV 與自檢腳本見 `examples/data/`（檔名已有 `autocorr` 前綴、與素材包逐位元相同；自檢改寫為只用標準函式庫） |
| 2026-10-10-am-lagplot.md | 滯後圖（lag plot；與自相關圖、一般散佈圖、遞迴圖、相連散佈圖、頻譜圖、管制圖、折線分界；「龐加萊圖」只指心率圖 R13） | `examples/lag-plot.md`；8 組 demo CSV 與自檢腳本見 `examples/data/`（檔名已有 `lagplot` 前綴、與素材包逐位元相同；自檢改寫為只用標準函式庫、預期值寫在腳本裡） |
| 2026-10-11-am-seasonal-subseries.md | 季節子序列圖（seasonal subseries plot；亦稱 cycle plot，中文「循環圖」未核；與季節圖、分月箱形圖、熱圖月曆、年×月熱圖、自相關圖、滯後圖、極座標月份圖分界；圖 R16 扣二次曲線、圖 S4 扣直線、「減當年平均」只是對照；圖 R8 是反例） | `examples/seasonal-subseries-plot.md`；9 組 demo CSV 與自檢腳本見 `examples/data/`（8 組虛構＋1 份毛納羅亞二氧化碳真實資料，美國政府公有領域；檔名已有 `seasonal-subseries` 前綴；自檢只用標準函式庫、預期值寫在腳本裡；本課沒有改這些檔，不宣稱與素材包逐位元相同） |
| 2026-10-13-am-seasonal-decomp.md | 季節分解圖（seasonal decomposition plot；亦稱古典分解圖、STL 分解圖；與季節調整後序列、季節子序列圖、季節圖、自相關圖、滯後圖分界；加法與乘法不要說成同一件事；STL 只做加法；圖 R4、圖 R5 不是四格分解圖） | `examples/seasonal-decomposition-plot.md`；5 組 demo CSV 與自檢腳本見 `examples/data/`（全是虛構；檔名已有 `seasonal-decomp` 前綴；自檢只用標準函式庫、預期值寫在腳本裡；本課沒有改這些檔，不宣稱與素材包逐位元相同） |
| 2026-10-14-am-splom.md | 散布圖矩陣（scatterplot matrix；亦稱 pairs plot，縮寫 SPLOM；與散點圖、相關熱圖、滯後圖、平行座標分界；分組要顏色加形狀，圖 R1、R2、R4 只用顏色是反例，正例是圖 S3；圖 S4 是左／右不是直式） | `examples/scatterplot-matrix.md`；5 組 demo CSV 與自檢腳本見 `examples/data/`（S1、S4、S5 虛構，種子 20261014；S2 鳶尾花四個數值欄，Anderson／Fisher，公有領域；S3 Palmer Penguins，Horst、Hill、Gorman，CC0；檔名已有 `splom` 前綴、與素材包逐位元相同；自檢只用標準函式庫、預期值寫在腳本裡）。參考圖不入庫：R1 CC BY 4.0 Nicoguaro；R2 CC BY-SA 3.0 Jackverr；R3 CC BY-SA 3.0 Philipendula；R4 CC BY-SA 4.0 Sigbert；R5 CC BY-SA 3.0 Sigbert |
| 2026-10-15-am-taylor.md | 泰勒圖（Taylor diagram；Karl E. Taylor，2001；與 Bland–Altman 圖、散點圖、散布圖矩陣、雷達圖分界；先扣平均，同時看標準差、相關與中心化均方根誤差；圖 S3、圖 S4 是上／下；圖 R3–R5 數字未核） | `examples/taylor-diagram.md`；5 組 demo CSV 與自檢腳本見 `examples/data/`（S1–S5 皆為模擬範例資料，種子 20261015；檔名已有 `taylor` 前綴、與素材包逐位元相同；自檢只用標準函式庫、預期值寫在腳本裡，中心化均方根誤差用餘弦定理）。參考圖不入庫：R1 CC BY-SA 4.0 Erectorsetkid；R2–R5 CC BY 4.0 Amina BEN SALAH |
| 2026-10-16-am-periodogram.md | 週期圖（periodogram；與頻譜圖、自相關圖、滯後圖、一般頻譜分界；整段頻率組成，尖峰對應頻率；頻率隨時間大變改頻譜圖；Welch 分段平均；圖 R2、圖 R4 數字未核；圖 R3 只作方法對照） | `examples/periodogram.md`；5 組 demo CSV 與自檢腳本見 `examples/data/`（S1–S5 皆為模擬範例資料，種子 20261016；檔名已有 `periodogram` 前綴、與素材包逐位元相同；自檢只用標準函式庫、預期值寫在腳本裡，圖 S1 的功率用純 Python 離散傅立葉轉換）。參考圖不入庫：R1 CC BY-SA 4.0 Ixfd64；R2 CC BY-SA 4.0 Warrickball；R3 CC0 Bob K；R4 CC BY 4.0 ESO／G. Anglada-Escudé；R5 CC BY-SA 4.0 Ixfd64 |
| 2026-10-17-am-bode.md | 波德圖（Bode plot；與週期圖、頻譜圖分界；畫系統的放大與延遲；共用對數頻率，上增益分貝、下相位度；圖 R3 的 f_GM 與 f_PM 對調照錄；圖 R4 數字未核） | `examples/bode-plot.md`；5 組 demo CSV 與自檢腳本見 `examples/data/`（S1–S5 皆為模擬範例資料，種子 20261017；檔名已有 `bode` 前綴）。參考圖不入庫：R1 CC BY-SA 3.0 Alejo2083；R2 CC0 Brews_ohare；R3 CC0 Sigmundg；R4 CC0 Qudusayinde；R5 CC BY-SA 3.0 Gmaxwell（上傳者） |
| 2026-10-18-am-hovmoller-polished.md | 霍夫默勒圖（Hovmöller diagram；又作霍夫穆勒圖，不當主名；與矩陣熱圖、頻譜圖、折線分界；一軸位置、一軸時間，顏色表數值；看往哪走、走多快；圖 R1 時間往上、圖 S1 往下；圖 R1 速度未核、緯度存疑；圖 R2 變數與單位未核；圖 R5 彩虹色只看走向） | `examples/hovmoller-diagram.md`；5 組 demo CSV 與自檢腳本見 `examples/data/`（S1–S5 皆為模擬範例資料，種子 20261018；檔名已有 `hovmoller` 前綴）。參考圖不入庫：R1 CC BY-SA 4.0 KIRAN S R；R2–R4 public domain US gov NOAA CPC；R5 public domain Morn PD-user-w |
| 2026-10-19-am-skewt-polished.md | 斜溫圖（Skew-T log-P diagram；課程稿沒有另給中文別名；與折線、霍夫默勒圖、地圖分界；一地一時的垂直剖面；氣壓取對數、等溫線斜 45 度；溫度沿斜線讀；兩線貼近只是可能有雲；位能要連對流抑制） | `examples/skew-t-log-p.md`；5 組 demo CSV 與自檢腳本見 `examples/data/`（S1–S5 皆為模擬範例資料，種子 20261019；檔名已有 `skewt` 前綴）。參考圖不入庫：R1 CC BY-SA 4.0 JeanBizHertzberg，懷俄明大學底圖未核，圖說必須寫「底圖未核，轉載須再確認」，整張不是已清授權；R2 CC BY-SA 4.0 TomRat；R3 public domain NOAA SPC；R4 public domain NWS；R5 public domain NWS Quad Cities |
| 2026-10-20 上午赫羅圖課程稿 | 赫羅圖（Hertzsprung–Russell diagram；顏色－星等圖是相近圖種；橫軸溫度或顏色，縱軸光度或星等；左熱右冷、上亮下暗；星等軸倒過來） | `examples/hr-diagram.md`；4 個 demo CSV 與 4 支自檢見 `examples/data/`（S1 與 S2 共用 `sample-hr-hip-s1-s2-hipparcos.csv`，依巴谷公開資料，ESA 1997 經 VizieR，17,746 列，標範例資料；S3–S5 模擬範例資料，種子 20261020、20261024、20261025；四個 CSV 都標範例資料）。參考圖不入庫：R1 CC BY-SA 2.5，署名 Richard Powell、penubag、zanhsieh，同方式分享（共享資源正體中文頁標 CC SA 1.0，本 repo 保守用 2.5）；R2 CC BY-SA 3.0 IGO ESA/Gaia/DPAC；R3 CC BY 4.0 ESO；R4 CC BY-SA 4.0 Lithopsian，「約 15,000 顆」是上傳者自己的說明，沒有論文出處，未核；R5 CC BY-SA 4.0 Meli thev |
| 2026-10-21 上午史密斯圖課程稿 | 史密斯圖（Smith chart；歸一化阻抗收進單位圓；中心匹配、左短路、右開路；上半電感、下半電容） | `examples/smith-chart.md`；3 個 demo CSV 與 3 支自檢見 `examples/data/`（S2–S5 虛構示範數字、模擬範例資料，沒有隨機種子；S4 與 S5 共用一份 CSV；S1 沒有 CSV）。參考圖不入庫：R1 CC0 Hula Hula Hula；R2 CC BY-SA 3.0，署名 Sbyrnes321，同方式分享；R3 公有領域 JoBa2282，標記歐姆數未另核；R4 CC BY-SA 3.0，署名 Sbyrnes321，同方式分享；例題圖底圖來源不明，本 repo 不使用、不連結，改以文字說明半圈導納（z=0.80+j1.40，三位小數 0.308−j0.538，|Γ| 四捨五入 0.620，Γ_y=−Γ_z） |
| 2026-10-22 上午奈奎斯特圖課程稿 | 奈奎斯特圖（Nyquist plot；開迴路 L(jω) 畫在複數平面；臨界點 −1；增益裕度在負實軸、相位裕度在單位圓） | examples/nyquist-plot.md；4 個 demo CSV 與 4 支自檢見 examples/data/（S1 與 S2 共用一份 CSV；S1–S5 模擬範例資料，沒有隨機種子）。參考圖不入庫：R3 CC BY-SA 4.0，署名 Pierre-Baptiste Steckler，同方式分享；R2 只靠紅綠，要看線位置；R4 只示意形狀；R5 字很小 |
| 2026-10-23 上午根軌跡圖課程稿 | 根軌跡圖（Root locus plot；閉迴路極點隨一個增益走；左半穩定、右半不穩定、虛軸上是等幅振盪） | examples/root-locus-plot.md；3 個 demo CSV 與 3 支自檢見 examples/data/（S1、S2 與 S3 共用一份 CSV；S1–S5 模擬範例資料，沒有隨機種子）。參考圖不入庫：R1、R2 CC BY-SA 4.0，署名 Hill.rick.c，同方式分享；R3 CC0，仍署名 Constant314，紅藍兩色的意思未核；R4 CC BY-SA 3.0，署名 AndrewDressel，課程稿用的是裁切放大版，同方式分享 |
| 2026-10-24 上午派柏圖課程稿 | 派柏圖（Piper diagram；又稱水化學三線圖；兩三角加菱形畫主要離子毫當量比例） | examples/piper-diagram.md；5 個 demo CSV 與 5 支自檢見 examples/data/（S1–S5 模擬範例資料，沒有隨機種子）。參考圖不入庫：R1、R2、R4 CC BY-SA 4.0，署名 Kvgunten、Paolopaolo714、郊外生活，同方式分享，裁白邊並縮圖；R1 另遮低對比代號框（改作）；R3 公有領域 Babakathy，仍署名，只裁極少白邊；H 區、溫泉歸屬、河水出處、4.7 未核 |
| 2026-10-25 上午尼可斯圖課程稿 | 尼可斯圖（Nichols chart；開迴路相位對增益（分貝）；霍爾圓＝閉迴路 M 圈；臨界點 −180 度、0 分貝） | examples/nichols-chart.md；5 個 demo CSV 與 5 支自檢見 examples/data/（S1–S5 模擬範例資料，沒有隨機種子，虛構轉移函數）。參考圖不入庫：R1 CC0 1.0，仍署名 Saung Tadashi，由向量圖轉成 1200×1123 點陣圖，未改內容；R2、R3 CC BY-SA 3.0，署名 Wolfch、Luca Ghio，課程稿用的是放大 2.5 倍的版本（已放大），同方式分享，看圖推讀；R3 圖上 33°、9.6 分貝，對應轉移函數無法證明 |
| 2026-10-26 上午風花圖課程稿 | 風花圖（Wind rose；又稱風玫瑰圖；扇形是風來的方向、長度是時間比例，可依風速堆疊） | examples/wind-rose.md；5 個 demo CSV 與 5 支自檢見 examples/data/（S1–S5 是本專案依愛荷華環境網機場例行天氣報告算出來的，桃園 RCTP、高雄 RCKH，2016–2025，不是虛構模擬；跑道真方位來自 OurAirports，授權註記寫公有領域）。參考圖不入庫：R1 公有領域（美國聯邦政府作品），美國農業部農業研究局，製圖 Sara West，2002，裁切後仍署名；R2、R3 CC BY 4.0，署名 Enviroware，JPEG 轉 PNG，未縮放未裁切；R4 CC BY-SA 4.0，署名 Touring Club Italiano 製圖室（與義大利國家研究委員會合作，1989–1992），裁切後放大 1.5 倍，改作仍以 CC BY-SA 4.0 釋出（同方式分享） |

各筆記另有同日的研究筆記與截圖，作為圖例與查證依據，未複製進 repo。

## 素材包與驗證

- 自 2026-09-21（點密度圖）起，各專題另有一份經審核的素材包（說明文件、來源清單、樣本 CSV、圖檔）。公開 repo 只收 pattern 摘要、虛構 demo CSV 與自檢腳本；圖檔不入庫，只列連結與授權。
- 每個 pattern 的來源逐條連結、圖檔授權、查核限制（打不開或無法確認的來源只記名、標未核）與數字重算結果，寫在對應的 `examples/*.md`；demo CSV、自檢腳本與檔名對照見 `examples/data/README.md`。
- 素材包附帶的繪圖產生器與匯出腳本（`draw_forest.py`、`draw_karyo.py`、`draw_horizon.py`、`draw_pareto.py`、`draw_control.py`、`draw_lorenz.py`、`draw_marey.py`、`draw_km.py`、`draw_swimmer.py`、`draw_lasagna.py`、`draw_recurrence.py`、`draw_spectrogram.py`、`draw_autocorr.py`、`draw_lagplot.py`、`draw_seasonal_subseries.py`、`draw_noaa_co2.py`、`draw_splom.py`、`export_samples.py`）**不收入本 repo**；其中部分腳本預設把圖寫進教學稿資料夾或覆寫資料檔，這也是不收的原因之一。
- 自檢腳本的輸出以實際重算為準；素材包文字與 CSV 有出入時，範例檔會註明並以實際計數為準。

## 尚未獨立成 pattern 的缺口

- 南丁格爾玫瑰、三元圖、樹狀譜系、蜂巢圖、HEB、流量地圖、比例符號地圖、平行集合：目前多半只在 `chart-heuristics.md`，尚無專檔 example。
- 點密度圖、河流圖、人口金字塔、棒棒糖圖、箱形圖、氣泡圖、馬里梅可圖、等值區域圖、圖塊地圖、矩陣熱圖、螺旋圖、BioFabric、火焰圖、Circos、火山圖、曼哈頓圖、MA 圖、QQ 圖、Bland–Altman 圖、LocusZoom 圖、P–P 圖、核型圖、森林圖、地平線圖、柏拉圖、管制圖、洛倫茲曲線、馬雷圖、存活曲線、游泳圖、千層麵圖、遞迴圖、頻譜圖、自相關圖、滯後圖、季節子序列圖、季節分解圖 已有專檔 example + 虛構 demo CSV；散布圖矩陣已有專檔，S1、S4、S5 是虛構 demo CSV，S2（鳶尾花，公有領域）與 S3（企鵝，CC0）是公開資料集；泰勒圖已有專檔，S1–S5 都是模擬範例 CSV；週期圖已有專檔，S1–S5 都是模擬範例 CSV，種子 20261016；波德圖已有專檔，S1–S5 都是模擬範例 CSV，種子 20261017；霍夫默勒圖已有專檔，S1–S5 都是模擬範例 CSV，種子 20261018；斜溫圖已有專檔，S1–S5 都是模擬範例 CSV，種子 20261019；赫羅圖已有專檔，4 個 CSV 都標範例資料，S1 與 S2 共用一份依巴谷公開資料（ESA 1997，經 VizieR），S3–S5 是模擬範例資料；史密斯圖已有專檔，3 個 CSV 與 3 支自檢，S2–S5 是虛構示範數字、模擬範例資料，沒有隨機種子，S4 與 S5 共用一份 CSV，S1 沒有 CSV；奈奎斯特圖已有專檔，4 個 CSV 與 4 支自檢，S1–S5 是模擬範例資料，沒有隨機種子，S1 與 S2 共用一份 CSV；根軌跡圖已有專檔，3 個 CSV 與 3 支自檢，S1–S5 是模擬範例資料，沒有隨機種子，S1、S2 與 S3 共用一份 CSV；派柏圖已有專檔，5 個 CSV 與 5 支自檢，S1–S5 是模擬範例資料，沒有隨機種子；尼可斯圖已有專檔，5 個 CSV 與 5 支自檢，S1–S5 是模擬範例資料，沒有隨機種子，虛構轉移函數；風花圖已有專檔，5 個 CSV 與 5 支自檢，S1–S5 是本專案依愛荷華環境網機場例行天氣報告算出來的（桃園 RCTP、高雄 RCKH，2016–2025），不是虛構模擬，跑道真方位來自 OurAirports、授權註記寫公有領域；其餘筆記「適合使用的範例」三小節樣本尚未全面打包。
- 社群敘事卡產線未併入本 plugin（敘事卡 ≠ 資料形狀推薦）。

## 授權與改寫

- 原始教學筆記為內部教學素材；本 skill 為 Grok Build 可執行摘要（MIT）。
- 對外分享時請保留本 ATTRIBUTION；勿宣稱教學筆記全文已開源。
- 公開上市版（0.3.x）只開 skill／pattern／demo，不開教學筆記全文。
