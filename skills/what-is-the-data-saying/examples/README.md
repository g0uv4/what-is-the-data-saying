# Examples / pattern library

具名、可複用的 pattern。每個檔：**when → recommend → avoid → produce checklist**。
多數圖種提煉自納茲（資料視覺）教圖；檔內「來源」指向原始檔名（全文不在本 repo）。完整清單見 `../ATTRIBUTION.md`。
第一次安裝請先跑 plugin 根目錄 [`demos/`](../../../demos/README.md) 的五則貼上稿。

| Pattern | File | 來源教圖 |
|---------|------|----------|
| 類別比大小 | `categorical-comparison.md` | 通用 |
| 時間趨勢 | `time-series-trend.md` | 通用 |
| 兩變數相關 | `correlation-scatter.md` | 通用 |
| 矩陣熱圖（色階矩陣） | `matrix-heatmap.md` | 2026-09-26-am-heatmap.md（升級原通用版） |
| 階層冰柱 | `hierarchy-icicle.md` | 2026-09-01-am-icicle-draft.md |
| 火焰圖（堆疊取樣；≠ 火焰時序圖、≠ 冰柱） | `flame-graph.md` | 2026-09-27-pm-flamegraph.md |
| 同構多面板 | `small-multiples.md` | 通用 |
| 瀑布橋 | `waterfall-bridge.md` | 2026-09-10-am-waterfall.md |
| 漏斗階段 | `funnel-stages.md` | 2026-09-10-pm-funnel.md |
| 啞鈴差距 | `dumbbell-gap.md` | 2026-09-07-pm-dumbbell.md |
| 坡度兩期 | `slope-two-period.md` | 2026-09-20-am-slope.md |
| 凹凸排名 | `bump-ranking.md` | 2026-08-28-am-bump-draft.md |
| 河流組成（溪流圖） | `streamgraph-composition.md` | 2026-09-22-am-streamgraph.md |
| 桑基流量 | `sankey-flow.md` | 2026-08-31-am-sankey-draft.md |
| 沖積階段 | `alluvial-stages.md` | 2026-09-07-am-alluvial.md |
| 旭日階層 | `sunburst-hierarchy.md` | 2026-08-31-pm-sunburst-draft.md |
| 矩形樹狀 | `treemap-composition.md` | 2026-09-06-am-treemap.md |
| 圓堆 | `circle-packing.md` | 2026-09-03-pm-circle-packing.md |
| Voronoi 樹狀 | `voronoi-treemap.md` | 2026-09-16-pm-voronoi.md |
| 六角分箱 | `hexbin-density.md` | 2026-09-18-pm-hexbin.md |
| 等高密度 | `contour-density.md` | 2026-09-19-am-contour.md |
| 日曆熱力 | `calendar-heatmap.md` | 2026-09-19-pm-calendar.md |
| 螺旋圖（週期時間序列） | `spiral-plot.md` | 2026-09-26-pm-spiral.md |
| 小提琴分布 | `violin-distribution.md` | 2026-09-15-pm-violin.md |
| 蜂群點 | `beeswarm-points.md` | 2026-09-04-pm-beeswarm.md |
| 雨雲組合 | `raincloud-combo.md` | 2026-09-05-pm-raincloud.md |
| 山脊密度 | `ridgeline-density.md` | 2026-09-08-pm-ridgeline.md |
| 雷達剖面 | `radar-profile.md` | 2026-09-14-pm-radar.md |
| 子彈 KPI | `bullet-kpi.md` | 2026-09-09-pm-bullet.md |
| 甘特時程 | `gantt-schedule.md` | 2026-09-14-am-gantt.md |
| 華夫占比 | `waffle-percent.md` | 2026-09-06-pm-waffle.md |
| 馬賽克交叉 | `mosaic-crosstab.md` | 2026-09-03-am-mosaic.md |
| 連接散點 | `connected-scatter.md` | 2026-09-04-am-connected-scatter.md |
| 弦圖交換 | `chord-matrix.md` | 2026-08-30-am-chord-draft.md |
| Circos（環狀多軌圖） | `circos.md` | 2026-09-28-am-circos.md |
| 火山圖（差異分析） | `volcano-plot.md` | 2026-09-28-pm-volcano.md |
| 曼哈頓圖（全基因組關聯；含邁阿密圖變體） | `manhattan-plot.md` | 2026-09-29-am-manhattan.md |
| MA 圖（平均－差值圖；含 RA 圖分界） | `ma-plot.md` | 2026-09-29-pm-ma.md |
| QQ 圖（分位數對分位數；含 P–P 圖分界） | `qq-plot.md` | 2026-09-30-am-qq.md |
| P–P 圖（機率對機率；≠ QQ 圖；軸放誰各來源不一致） | `pp-plot.md` | 2026-10-01-pm-pp.md |
| 核型圖／染色體帶型示意圖（karyotype／ideogram；p、q 臂與著絲點、帶號；≠ 曼哈頓圖、≠ Circos） | `karyotype-ideogram.md` | 2026-10-02-am-karyotype.md |
| 森林圖（Forest plot；一列一項研究：方塊＝估計、橫線＝信賴區間、菱形＝合併；比值類對數軸；≠ 統合分析漏斗圖〔Funnel plot〕、≠ 商業漏斗圖〔Funnel chart〕） | `forest-plot.md` | 2026-10-02-pm-forest.md |
| 地平線圖（Horizon chart；很多條時間序列相對基準的色帶疊層；≠ 河流圖、≠ 山脊圖、≠ 熱圖；各列各自縮放跨列不可比） | `horizon-chart.md` | 2026-10-03-am-horizon.md |
| 柏拉圖（Pareto chart／帕累托圖；類別由大到小的直條＋累計百分比折線；≠ 一般長條圖、≠ 瀑布圖、≠ 漏斗圖；左軸最大值＝總數；80/20 只是經驗法則） | `pareto-chart.md` | 2026-10-03-pm-pareto.md |
| 管制圖（Control chart／Shewhart chart；時間順序的點＋中心線＋上下管制界限；≠ 折線圖、≠ 柏拉圖、≠ 規格界限；連續同側 Western Electric 8 點、Nelson 9 點） | `control-chart.md` | 2026-10-04-am-control.md |
| 洛倫茲曲線（Lorenz curve，含基尼係數；單位由小到大排序、兩軸累計百分比、附對角線；≠ 柏拉圖〔相通但不同，轉半圈關係〕、≠ 折線圖、≠ 分位數圖；基尼要註明有無小樣本修正，一人全拿 10 戶是 0.90；同基尼可曲線交叉） | `lorenz-curve.md` | 2026-10-04-pm-lorenz.md |
| 馬雷圖／列車運行圖（Marey chart；一班車一條線、站點依實際距離、斜率＝速度、交叉＝相遇或超車；≠ 折線圖、≠ 甘特圖；歷史歸屬用限定語；R14 授權存疑不用） | `marey-chart.md` | 2026-10-05-am-marey.md |
| 存活曲線／Kaplan–Meier（階梯、設限短直線、信賴區間、風險人數表；≠ 折線圖、≠ 生態學 survivorship curve；不採用「編輯＝Tukey」；aml 中位 27 週） | `kaplan-meier-survival.md` | 2026-10-05-pm-km.md |
| Bland–Altman 圖（兩種量測方法的一致性；≠ MA 圖、≠ 相關係數） | `bland-altman.md` | 2026-09-30-pm-ba.md |
| LocusZoom 圖（區域關聯圖；曼哈頓圖的區間細節層；≠ 曼哈頓圖；領先變異≠因果） | `locuszoom.md` | 2026-10-01-am-locuszoom.md |
| 力導向網路 | `force-network.md` | 2026-09-17-pm-force.md |
| 弧線圖 | `arc-diagram.md` | 2026-09-17-am-arc.md |
| 鄰接矩陣 | `adjacency-matrix.md` | 2026-09-18-am-adjacency.md |
| BioFabric（生物織布圖，暫譯） | `biofabric.md` | 2026-09-27-am-biofabric.md |
| 平行座標 | `parallel-coordinates.md` | 2026-08-29-parallel-draft.md |
| 圓形長條 | `circular-bar.md` | 2026-09-08-am-circular-bar.md |
| 統計變形地圖 | `cartogram-geo.md` | 2026-09-16-am-cartogram.md |
| 等值區域地圖 | `choropleth-map.md` | 2026-09-25-am-choropleth.md |
| 圖塊地圖 | `tile-map.md` | 2026-09-25-pm-tilemap.md |
| 點密度地圖 | `dot-density-map.md` | 2026-09-21-pm-dotdensity.md |
| 人口金字塔 | `population-pyramid.md` | 2026-09-22-pm-pyramid.md |
| 棒棒糖排名 | `lollipop-rank.md` | 2026-09-23-am-lollipop.md |
| 箱形分布摘要 | `boxplot-summary.md` | 2026-09-23-pm-boxplot.md |
| 氣泡圖（笛卡兒） | `bubble-chart.md` | 2026-09-24-am-bubble.md |
| 馬里梅可（變寬堆疊） | `marimekko-chart.md` | 2026-09-24-pm-marimekko.md |
| UpSet 集合 | `upset-sets.md` | 2026-09-01-pm-upset-draft.md |

新增 pattern：複製最接近的檔，改 slug 與本表列；保持短；補 ATTRIBUTION。
