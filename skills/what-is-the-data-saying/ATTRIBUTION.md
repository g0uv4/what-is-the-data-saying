# ATTRIBUTION（納茲教圖來源）

本 skill **0.3.15** 的圖種啟發式、口述產出步驟與 `examples/` pattern，提炼自 **納茲 - 資料視覺**（agent id `41759b08-68d8-455a-8d45-22730ad6bd40`）的教圖與相關素材。

技能文字為摘要與可執行 checklist，**不是**教圖全文轉貼；數字案例仍以原教圖「未核」標註習慣為準。
原教圖草稿／截圖**不在這個公開 repo**。下表的路徑是作者當時的取材位置，方便內部對帳，不是給 clone 的人去開的檔。

## 主要來源目錄

| 路徑 | 用途 |
|------|------|
| `/workspace/teach-viz/` | 教圖終稿／草稿／研究筆記與截圖（主來源） |
| `/workspace/today-reports-extract/Nazh-FINAL.md` 等 | 納茲交件摘錄（如 HEB） |
| `/workspace/researcher-digest/2026-09-*` | 教圖社群卡／評論（輔助） |
| `/workspace/fox-card-study/` | 卡片敘事研究（輔助，未直接當 pattern） |
| `/home/box/agent-data/agents/41759b08-68d8-455a-8d45-22730ad6bd40/` | 納茲 profile／memory（教圖五塊格式、語氣） |

## 教圖檔 → pattern／啟發式對照

| teach-viz 檔名 | 圖種（zh-TW） | skill 落點 |
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
| 2026-09-02-am-heb-draft.md / Nazh-FINAL.md | 階層式邊捆綁 | `references/chart-heuristics.md`（HEB 列） |
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

另有同日前綴之 `*-research.md`、截圖檔（png/jpg）作為教圖研究與圖例依據，未逐一複製進 repo。
點密度圖另經已審 skill pack `/workspace/skill-packs/2026-09-21-pm-dotdensity/`（SKILL-PACK.md、sources.txt、images/）；公開 repo 只收 pattern 摘要與虛構 demo CSV，大圖不入库。
河流圖另經已審 skill pack `/workspace/skill-packs/2026-09-22-am-streamgraph/`（SKILL-PACK.md、sources.txt、sample CSVs、images/ 共 13 張）；公開 repo 只收 pattern 摘要與虛構 demo CSV，大圖不入库（對帳可看 pack `images/`）。
人口金字塔另經已審 skill pack `/workspace/skill-packs/2026-09-22-pm-pyramid/`（SKILL-PACK.md、sources.txt、sample CSVs、images/ 約 19 張）；公開 repo 只收 pattern 摘要與虛構 demo CSV，大圖不入库。
棒棒糖圖另經已審 skill pack `/workspace/skill-packs/2026-09-23-am-lollipop/`（SKILL-PACK.md、sources.txt、sample CSV、images/；稿內嵌約 24 張）；公開 repo 只收 pattern 摘要與虛構 demo CSV，大圖不入库。
箱形圖另經已審 skill pack `/workspace/skill-packs/2026-09-23-pm-boxplot/`（SKILL-PACK.md、sources.txt、sample CSV、images/；稿內嵌約 24 張）；公開 repo 只收 pattern 摘要與虛構 demo CSV，大圖不入库。
氣泡圖另經已審 skill pack `/workspace/skill-packs/2026-09-24-am-bubble/`（SKILL-PACK.md、sources.txt、sample CSV、images/；稿內嵌約 24 張）；公開 repo 只收 pattern 摘要與虛構 demo CSV，大圖不入库。
馬里梅可圖另經已審 skill pack `/workspace/skill-packs/2026-09-24-pm-marimekko/`（SKILL-PACK.md、sources.txt、sample CSV、images/；稿內嵌約 23 張）；公開 repo 只收 pattern 摘要與虛構 demo CSV，大圖不入库。
等值區域圖另經已審 skill pack `/workspace/skill-packs/2026-09-25-am-choropleth/`（SKILL-PACK.md、sources.txt 25 條、sample CSV、images/；稿內嵌 24 張）；公開 repo 只收 pattern 摘要與虛構 demo CSV，大圖不入库。來源含 Dataviz Catalogue／Dataviz Project／data-to-viz／Wikipedia／Claus Wilke／Datawrapper（部落格、Academy、產品頁）／ColorBrewer／Flourish／D3・R・Python Graph Gallery／Plotly／Observable（舊 `@d3/choropleth` 已停用，引用新版 `@d3/choropleth/2`），以及 4 則已核 X 教學原帖（Africa_DataHub、World_Data_A、tableaupublic、JoachimSchork）；逐條連結見 `examples/choropleth-map.md`。
圖塊地圖另經已審 skill pack `/workspace/skill-packs/2026-09-25-pm-tilemap/`（SKILL-PACK.md、sources.txt 23 條、sample CSV、images/；稿內嵌 24 張）；公開 repo 只收 pattern 摘要與虛構 demo CSV，大圖不入库。來源含 Claus Wilke／NPR Visuals／Datawrapper（部落格、地圖總覽）／Wikipedia Cartogram／Pitch Tilegrams／statebins（GitHub、CRAN）／geofacet／R Graph Gallery／Bill Mill／d3kit-gridmap／Medium（Plotly）／tamasszabo.org（Tableau）／Flourish／data-to-viz／ColorBrewer；Observable 429、CDC COVE 403 列為查核限制；本輪 X 查無教學原帖。封面／拼貼圖（dw-election-hex、medium-hex、dw-swiss-compare）不當圖塊地圖範例；逐條連結見 `examples/tile-map.md`。
矩陣熱圖另經已審 skill pack `/workspace/skill-packs/2026-09-26-am-heatmap/`（SKILL-PACK.md、sources.txt 23 條、sample CSV、images/；稿內嵌 24 張），升級原本通用版 `examples/matrix-heatmap.md`（pattern 數不變）；公開 repo 只收 pattern 摘要與虛構 demo CSV，大圖不入库。來源含 Dataviz Catalogue／Dataviz Project／data-to-viz／Wikipedia／Claus Wilke／ColorBrewer／Datawrapper 色階文／Flourish（Heatmaps 頁、範本）／D3・R・Python Graph Gallery／Seaborn／Plotly／Highcharts，以及 1 則 X 教學原帖（clcoding）；Datawrapper 熱圖專頁與部落格 404、Flourish 操作教學 404、Observable `@d3/heatmap` 429、D3 `heatmap2_basic` 404 列為查核限制。相關矩陣範例圖用 wilke-forensic1（不用 wilke-correlations 散點示意）；`levelplot` 歸 lattice；Flourish 三張 PNG 已由素材作者重新存檔。日曆熱力圖與鄰接矩陣只列為鄰近圖種。逐條連結見 `examples/matrix-heatmap.md`。
螺旋圖另經已審 skill pack `/workspace/skill-packs/2026-09-26-pm-spiral/`（SKILL-PACK.md、sources.txt 22 條正式來源＋失敗項對照、sample CSV、images/；稿內嵌 26 張）；公開 repo 只收 pattern 摘要與虛構 demo CSV，大圖不入库。來源含 Dataviz Catalogue／Wikipedia（Climate spiral、Archimedean spiral）／Ed Hawkins Climate Visuals（CC-BY 4.0）與 Climate Lab Book Substack／NASA SVS 5190・5383・5057／spiralize（首頁、入門、範例集）／tomshanley d3-spiral-heatmap（GitHub、bl.ocks）／Condegram gist／Carlis & Konstan UIST 1998（DOI 10.1145/288392.288399），以及 2 則 X 解說原帖（Stellarixorine 的「一圈＝一個月」有誤、已註明；MyZeroCarbon）；Dataviz Project 403、spiralize COVID 互動應用逾時列為查核限制，本輪查無程式教學類 X 原帖。圖說照審稿修正版（NASA 無標示版與舊版靜幀分屬 5383、5057，非 5190；spiralize 入門圖逐張更正）。逐條連結見 `examples/spiral-plot.md`。
BioFabric 另經已審 skill pack `/workspace/skill-packs/2026-09-27-am-biofabric/`（SKILL-PACK.md、sources.txt 第一段 18 條可開來源＋第二段失敗項對照、sample CSV、images/；稿內嵌 22 張）；公開 repo 只收 pattern 摘要與虛構 demo CSV，大圖不入库。來源含 BioFabric 官方網站與 Gallery（Institute for Systems Biology）／Longabaugh 2012 BMC Bioinformatics 論文（DOI 10.1186/1471-2105-13-275；BMC、PDF、PubMed Central、Springer）／yFiles 用例頁／GitHub wjrl（BioFabric、D3BioFabric、RBioFabric）／Xenographics／visualizing.org／Wikipedia／官方部落格與使用者群組／Dataviz Catalogue 與 data-to-viz 的一般網路圖頁（非 BioFabric 專頁）；Dataviz Catalogue、data-to-viz、Dataviz Project 無 BioFabric 專頁，CRAN RBioFabric 404、yFiles 線上示範深層連結 404、GitHub 內容 API 403 列為查核限制（只記名稱）；本輪 X 查無教學原帖。中文名「生物織布圖／表格式網路圖」為暫譯；Gallery 的 GOT-1200 圖是 Influential Thinkers，不是影集。逐條連結見 `examples/biofabric.md`。
火焰圖另經已審 skill pack `/workspace/skill-packs/2026-09-27-pm-flamegraph/`（SKILL-PACK.md、sources.txt 第一段 22 條可開來源＋第二段失敗項對照、sample 已收合堆疊 .txt、images/；稿內嵌 23 張含 1 張 SVG）；公開 repo 只收 pattern 摘要與虛構 demo 資料，大圖不入库。來源含 Brendan Gregg 官方站（總頁、CPU／Memory／Off-CPU／Hot-Cold、差異火焰圖、FlameScope 頁與部落格、Netflix FlameScope PDF）／GitHub（brendangregg/FlameGraph、spiermar/d3-flame-graph、jlfwong/speedscope、Netflix/flamescope）／speedscope.app／CACM〈The Flame Graph〉（DOI 10.1145/2909476；原刊 ACM Queue DOI 10.1145/2927299.2927301）／Netflix Tech Blog（Java in Flames、FlameScope）／Chrome 開發者工具 Performance 文件（火焰時序圖對照）／Wikipedia／flamegraphdiff；ACM Queue 原文與附圖 403、錯誤 DOI 路徑 404、ACM 數位圖書館 cookie 檢查頁、Dataviz Catalogue／data-to-viz／Dataviz Project 無專頁、舊式部落格網址與官方 CPU 混合模式點陣圖 404 列為查核限制（只記名稱）；本輪 X 查無教學原帖。火焰圖與火焰時序圖、冰柱圖分開寫，與 `examples/hierarchy-icicle.md` 雙向互連、不合併。逐條連結見 `examples/flame-graph.md`。
Circos 另經已審 skill pack `/workspace/skill-packs/2026-09-28-am-circos/`（SKILL-PACK.md、sources.txt 每行標可否打開、三個 sample CSV、images/ 22 張，圖說用 Liora 修正後版本）；公開 repo 只收 pattern 摘要與虛構 demo CSV，大圖不入库。來源含 circos.ca 官方站（首頁、圖庫、樣品、媒體與文獻採用例、導覽、指南、教學、文件、軟體下載與需求頁）／Krzywinski 等 2009 *Genome Research* 論文（PubMed Central、PubMed、Crossref）／PHSA 新聞稿／circlize（論文 DOI、線上專書、CRAN）／pyCirclize（GitHub、文件、PyPI）／vigsterkr/circos（非官方倉庫，與官方關係未證實）／Dataviz Catalogue 與 data-to-viz 弦圖頁／英文維基百科弦圖條目（「Circos」條目會轉到弦圖，不當 Circos 專頁）。授權：Circos 為 GPL 第 3 版；circlize、pyCirclize 為 MIT（同家族實作，非官方版；pyCirclize 原文「inspired by circlize and pyCircos」）。期刊頁與論文 DOI 登入轉址迴圈、github.com/circos/circos 404、Dataviz Project 403、mkweb.bcgsc.ca 舊網址與舊表格檢視器 403 列為查核限制（只記名稱）；本輪 X 查無可用教學原帖。階層邊捆綁尚無專檔，只在 heuristics 寫分界。逐條連結見 `examples/circos.md`。
火山圖另經已審 skill pack `/workspace/skill-packs/2026-09-28-pm-volcano/`（SKILL-PACK.md、sources.txt 50 條每行標狀態、sample CSV 50 列含原始與校正後 p 值、images/ 22 張，圖說用 Liora 修正後版本）；公開 repo 只收 pattern 摘要與虛構 demo CSV，大圖不入库。來源含英文維基百科（火山圖、MA 圖、曼哈頓圖、等高線條目）／Cui 與 Churchill 2003 *Genome Biology*（DOI、PubMed、Europe PMC）／Li 2012 *JBCB*（DOI、PubMed）／Jin 等 2001 *Nat Genet*、Li 等 2014（DOI）／EnhancedVolcano（Bioconductor 套件頁、說明文件、手冊、GitHub；GPL 第 3 版）／Plotly Python 火山圖頁／biostatsquid、NotchBio、MetwareBio、Galaxy 訓練教材、哈佛生物資訊核心教學／R Graph Gallery 曼哈頓圖頁／Seaborn、Matplotlib 範例索引（無火山圖專屬範例）。門檻表標「範例，不是標準」；EnhancedVolcano 說明文件內文 ">|2|" 與手冊 FCcutoff 1 矛盾，以手冊為準。Plotly R 語言火山圖頁 404、Dataviz Project 火山圖頁（研究時 403、今天 404）、docs.biolab.si Orange 火山圖圖元頁（轉址到文件首頁）及其他 404 網址列為查核限制（只記名稱、未核）；本輪 X 查無可用教學原帖。MA 圖、地形等高線圖尚無專檔，只寫分界；曼哈頓圖已於 0.3.15 補專檔（`examples/manhattan-plot.md`）。逐條連結見 `examples/volcano-plot.md`。
曼哈頓圖另經已審 skill pack `/workspace/skill-packs/2026-09-29-am-manhattan/`（SKILL-PACK.md、sources.txt 55 條每行標狀態碼、sample CSV 6,427 列含 3 個虛構峰、images/ 21 張，圖說與終稿逐字相同）；公開 repo 只收 pattern 摘要與虛構 demo CSV，大圖不入库。來源含英文維基百科（Manhattan plot、Genome-wide association study、Genome-wide significance、Q–Q plot、Genomic control、火山圖條目）／Pruim 等 2010 LocusZoom 論文（PMC2935401；先前誤植的 PMC3605911 為病毒系統動力學論文，已排除）／my.locuszoom.org、statgen/locuszoom／miami_generator（邁阿密圖）／qqman（CRAN 頁、說明文件、手冊、GitHub；GPL-3）／CMplot（GitHub、CRAN 頁、手冊；GPL (≥ 2)）／manhattanly（GitHub、作者網站；MIT；**2025-06-13 已自 CRAN 下架**，CRAN 頁只當下架證據，不推薦為目前工具）／Plotly Python 曼哈頓圖頁與 Dash Bio（MIT）／R Graph Gallery、Python Graph Gallery／EBI GWAS Catalog／GWASTools。門檻表標「範例，不是標準」；1×10⁻⁵ 只是工具預設值、學術出處未核。Pe'er 等 2008 PubMed 頁（203 驗證頁）、Plotly R 頁與複數網址、From Data to Viz／Dataviz Catalogue／Dataviz Project 曼哈頓頁、維基百科 Miami plot／LocusZoom 條目等 404／502 網址及內容被換成廣告的 Getting Genetics Done 文章列為查核限制（只記名稱、未核）；本輪 X 查無可用教學原帖。QQ 圖、區域放大圖（LocusZoom）尚無專檔，只寫分界。逐條連結見 `examples/manhattan-plot.md`。

## 尚未獨立成 pattern 的缺口（可請 Liora／納茲補）

- 南丁格爾玫瑰、三元圖、樹狀譜系、蜂巢圖、HEB、地平線圖、流量地圖、比例符號地圖、平行集合：目前多半只在 `chart-heuristics.md`，尚無專檔 example。
- 點密度圖、河流圖、人口金字塔、棒棒糖圖、箱形圖、氣泡圖、馬里梅可圖、等值區域圖、圖塊地圖、矩陣熱圖、螺旋圖、BioFabric、火焰圖、Circos、火山圖、曼哈頓圖 已有專檔 example + 虛構 demo CSV；其餘教圖「適合使用的範例」三小節樣本尚未全面打包。
- X 社群卡 skill／fox-card 產線未併入本 plugin（敘事卡 ≠ 資料形狀推薦）。

## 授權與改寫

- 原教圖為內部教學素材；本 skill 為 Grok Build 可執行摘要（MIT）。
- 對外分享時請保留本 ATTRIBUTION；勿宣稱教圖全文已開源。
- 公開上市版（0.3.x）只開 skill／pattern／demo，不開 teach-viz 全文。
