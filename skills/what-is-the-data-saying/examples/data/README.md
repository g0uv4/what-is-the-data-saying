# Demo data（虛構示意；多為 CSV，火焰圖為已收合堆疊 .txt，MA 圖、QQ 圖、Bland–Altman 圖、LocusZoom 圖、P–P 圖、核型圖、森林圖、地平線圖與柏拉圖各附一支自檢 .py，管制圖、洛倫茲曲線、馬雷圖、存活曲線、游泳圖、千層麵圖、遞迴圖、頻譜圖、自相關圖與滯後圖各附 8 組 CSV 與 8 支自檢 .py，季節子序列圖附 9 組 CSV 與 9 支自檢 .py（8 組虛構＋1 份毛納羅亞二氧化碳真實資料），季節分解圖附 5 組 CSV 與 5 支自檢 .py（5 組虛構），散布圖矩陣附 5 組 CSV 與 5 支自檢 .py（S1、S4、S5 虛構；S2 鳶尾花公有領域；S3 企鵝 CC0），泰勒圖附 5 組 CSV 與 5 支自檢 .py（S1–S5 皆為模擬範例資料，種子 20261015），週期圖附 5 組 CSV 與 5 支自檢 .py（S1–S5 皆為模擬範例資料，種子 20261016），波德圖附 5 組 CSV 與 5 支自檢 .py（S1–S5 皆為模擬範例資料，種子 20261017），霍夫默勒圖附 5 組 CSV 與 5 支自檢 .py（S1–S5 皆為模擬範例資料，種子 20261018），斜溫圖附 5 組 CSV 與 5 支自檢 .py（S1–S5 皆為模擬範例資料，種子 20261019））

來自專案維護者整理、已審的 skill pack。**非真實產業資料；數字未核。**

| 檔名 | 用途 | pack |
|------|------|------|
| `dot-density-one-to-many.csv` | 一對多點密度：縣市計數 + `dot_value` | `2026-09-21-pm-dotdensity` |
| `dot-density-one-to-one.csv` | 一對一點圖：真實經緯度落點 + 類別 | 同上 |
| `streamgraph-categories.csv` | 河流圖長表：date, category, value | `2026-09-22-am-streamgraph` |
| `streamgraph-wide.csv` | 河流圖寬表：date + 每類一欄 | 同上 |
| `population-pyramid-long.csv` | 人口金字塔長表：age_group, sex, count | `2026-09-22-pm-pyramid` |
| `population-pyramid-wide.csv` | 人口金字塔寬表：age_group, male, female | 同上 |
| `lollipop-categories.csv` | 棒棒糖：category, value | `2026-09-23-am-lollipop` |
| `sample-boxplot.csv` | 箱形：group, value（虛構，數字未核） | `2026-09-23-pm-boxplot` |
| `sample-bubble.csv` | 氣泡：entity, x, y, size, region（虛構，數字未核） | `2026-09-24-am-bubble` |
| `sample-marimekko.csv` | 馬里梅可：segment, product, value（虛構，數字未核） | `2026-09-24-pm-marimekko` |
| `sample-choropleth.csv` | 等值區域：region, region_code, population, cases, rate_per_100k（用比率上色；虛構，數字未核） | `2026-09-25-am-choropleth` |
| `sample-tilemap.csv` | 圖塊地圖：state, row, col, value_pct（每區一格、格座標不重複；虛構，數字未核） | `2026-09-25-pm-tilemap` |
| `sample-heatmap.csv` | 矩陣熱圖長格式：category, channel, sales_index（12 商品大類 × 7 通路；虛構，數字未核） | `2026-09-26-am-heatmap` |
| `sample-spiral.csv` | 螺旋圖：month, year, month_num, rentals（2017-01～2024-12 每月腳踏車租借次數，96 列；一圈＝一年；2020 異常圈；虛構，數字未核） | `2026-09-26-pm-spiral` |
| `sample-biofabric.csv` | BioFabric 邊表：source, target, relation, weight（17 節點、38 條邊；relation＝social／collaboration／reporting 當連結分組；節點前綴＝部門；虛構，數字未核） | `2026-09-27-am-biofabric` |
| `sample-flamegraph.txt` | 火焰圖**已收合堆疊純文字（非 CSV）**：每行 `根;…;葉 樣本數`，27 行、總樣本 3,626（虛構 api_server 尖峰延遲；檔內無註解，可直接餵火焰圖工具；轉階層表見 `../flame-graph.md`；虛構，數字未核） | `2026-09-27-pm-flamegraph` |
| `sample-circos-sectors.csv` | Circos 外圈扇區：sector_id, species, label, length_mb, order（甲種 3 條、乙種 3 條染色體；虛構，數字未核） | `2026-09-28-am-circos` |
| `sample-circos-track.csv` | Circos 數值軌道：sector_id, start_mb, end_mb, gene_density, repeat_level（直方圖＋熱圖軌道；虛構，數字未核） | 同上 |
| `sample-circos-links.csv` | Circos 連線：link_id, sector_a, start_a_mb, end_a_mb, sector_b, start_b_mb, end_b_mb, orientation, link_type（共線／疑似倒位／短對位；起點大於終點＝反向；虛構，數字未核） | 同上 |
| `sample-volcano-de-results.csv` | 火山圖差異分析結果：feature_id, log2_fold_change, p_value, p_adjusted_bh, neg_log10_p, neg_log10_padj, category（50 列；BH 校正在 50 列內計算；範例門檻 \|log2FC\| ≥ 1、校正後 p < 0.05 分五類；虛構，數字未核） | `2026-09-28-pm-volcano` |
| `sample-manhattan-gwas.csv` | 曼哈頓圖全基因組關聯摘要：marker_id, chromosome, position, p_value, neg_log10_p（6,427 列、22 條染色體、約 230 KB；3 個虛構峰在 3、11、17 號染色體；虛構，數字未核） | `2026-09-29-am-manhattan` |
| `sample-ma-fictional.csv` | MA 圖差異分析結果：gene_id, gene_name, base_mean, a_log2_mean, m_log2fc, m_log2fc_shrunk, lfc_se, pvalue, padj, sim_true_de（3,000 列、約 230 KB；檔頭兩行以 `#` 開頭要略過；`m_log2fc_shrunk` 是示意收縮，不是 apeglm 輸出；虛構，數字未核） | `2026-09-29-pm-ma` |
| `sample-ma-selfcheck.py` | 上一檔的自檢腳本（純標準函式庫 Python，不是資料）；見下方「自檢腳本」 | 同上 |
| `sample-qq-fictional.csv` | QQ 圖練習資料：row_id, group, value, pvalue_sim（220 列、約 6 KB；A 組近似常態 120 筆、B 組右偏 100 筆；檔頭兩行以 `#` 開頭要略過；虛構，數字未核） | `2026-09-30-am-qq` |
| `sample-qq-selfcheck.py` | 上一檔的自檢腳本（需 numpy 與 scipy，不是資料）；見下方「QQ 圖自檢腳本」，（v0.3.18 已修正讀檔方式） | 同上 |
| `sample-ba-fictional.csv` | Bland–Altman 圖練習資料：row_id, dataset, method_a, method_b（220 列、約 6 KB；dataset＝good 100 對「一致性良好」＋ fan 120 對「誤差與大小成比例」；**差值一律是方法 B 減方法 A**；檔頭兩行以 `#` 開頭要略過；虛構，數字未核） | `2026-09-30-pm-ba` |
| `sample-ba-selfcheck.py` | 上一檔的自檢腳本（需 numpy，不是資料）；見下方「Bland–Altman 自檢腳本」；以明確檔名讀 CSV，可直接在本資料夾跑 | 同上 |
| `sample-locuszoom-fictional.csv` | LocusZoom 圖（區域關聯圖）練習資料：row_id, record_type, dataset, chrom, position_bp, end_bp, neg_log10_p, ld_r2_to_index, ld_band, is_index, gene_name, strand, recomb_rate_schematic（2,306 列、約 112 KB；record_type＝variant 變異位點 2,239、gene 基因軌 11、recomb 重組率示意取樣點 56；dataset＝genome 全基因組背景 1,760 點＋第 10 號染色體 45.0–45.55 Mb 四段虛構區間 single／following／second／readcolors；檔頭兩行以 `#` 開頭要略過；虛構，數字未核） | `2026-10-01-am-locuszoom` |
| `sample-locuszoom-selfcheck.py` | 上一檔的自檢腳本（需 numpy，不是資料）；見下方「LocusZoom 自檢腳本」；以明確檔名讀 CSV，可直接在本資料夾跑 | 同上 |
| `sample-pp-fictional.csv` | P–P 圖虛構資料（1,000 列、約 30 KB；欄位 row_id, dataset, group, obs_index, value, value2；8 個 dataset：anatomy 20、good 100、heavy 200、loc 100、skew 200、two 200、resid 80、sm 100 列；檔頭**三行以 # 開頭要略過**） | 2026-10-01-pm-pp.md |
| `sample-pp-selfcheck.py` | 上一檔的自檢腳本（需 numpy 與 scipy，不是資料）；見下方「P–P 自檢腳本」；以明確檔名讀 CSV，可直接在本資料夾跑 | 同上 |
| `sample-karyotype-fictional.csv` | 核型圖／染色體帶型示意圖虛構資料（1,548 列、約 80 KB；欄位 row_id, record_type, dataset, chrom, start_bp, end_bp, name, gstain, value, chrom2, start2_bp；record_type：chrom 24、band 320、interval 5、density 631、assoc 560、link 8；檔頭**兩行以 # 開頭要略過**） | 2026-10-02-am-karyotype.md |
| `sample-karyotype-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「核型圖自檢腳本」；以明確檔名讀 CSV，可直接在本資料夾跑 | 同上 |
| `sample-forest-fictional.csv` | 森林圖虛構資料（61 列資料、約 5.5 KB、檔頭 8 行 `#` 說明；欄位 dataset, panel, study, subgroup, measure, effect, analysis_value, se, ci_lower, ci_upper, weight_fixed_pct；8 個資料集 S1–S8、10 個分析單位；**數字未核**，後 3 欄是推導欄） | `../forest-plot.md` |
| `sample-forest-selfcheck.py` | 上一檔的自檢腳本（需 numpy，有 statsmodels 才多一行交叉核對，不是資料）；見下方「森林圖自檢腳本」；以明確檔名讀 CSV，可直接在本資料夾跑 | 同上 |
| `sample-horizon-fictional.csv` | 地平線圖虛構資料（288 筆、約 13.7 KB、沒有 `#` 說明行；欄位 hour, series, cpu_percent, data_status；12 台機器 × 第 0 到 23 小時；處理器使用率虛構，**數字未核**） | `../horizon-chart.md` |
| `sample-horizon-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「地平線圖自檢腳本」；以明確檔名讀 CSV，可直接在本資料夾跑 | 同上 |
| `sample-pareto-fictional.csv` | 柏拉圖虛構資料（8 列、366 位元組、沒有 `#` 說明行；欄位 category, count, data_status；進貨驗收不合格 8 個原因，件數合計 340；**數字未核**） | `../pareto-chart.md` |
| `sample-pareto-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「柏拉圖自檢腳本」；以明確檔名讀 CSV，可直接在本資料夾跑 | 同上 |
| `sample-s1-anatomy.csv` | 管制圖虛構資料（S1 解剖；25 組；中心線 50、上界 56、下界 44（σ 設 2）；第 1 行是 `#` 說明行、第 2 行是欄位名；每列 `data_status` 都是「虛構資料，數字未核」；**數字未核**） | `../control-chart.md` |
| `sample-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「管制圖自檢腳本」 | 同上 |
| `sample-s2-out-of-control.csv` | 管制圖虛構資料（S2；20 組，left_value 與 right_value 兩欄；中心線 100、上界 109、下界 91；右欄第 15 組超界；第 1 行是 `#` 說明行、第 2 行是欄位名；每列 `data_status` 都是「虛構資料，數字未核」；**數字未核**） | `../control-chart.md` |
| `sample-s2-out-of-control-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「管制圖自檢腳本」 | 同上 |
| `sample-s3-run-same-side.csv` | 管制圖虛構資料（S3（審稿重畫的新版）；18 組；中心線 20、上界 23.6、下界 16.4；第 1–9 組連續 9 點在中心線上方；第 1 行是 `#` 說明行、第 2 行是欄位名；每列 `data_status` 都是「虛構資料，數字未核」；**數字未核**） | `../control-chart.md` |
| `sample-s3-run-same-side-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「管制圖自檢腳本」 | 同上 |
| `sample-s4-trend.csv` | 管制圖虛構資料（S4；18 組；中心線 40、上界 44.5、下界 35.5；第 1–12 組一路上升；第 1 行是 `#` 說明行、第 2 行是欄位名；每列 `data_status` 都是「虛構資料，數字未核」；**數字未核**） | `../control-chart.md` |
| `sample-s4-trend-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「管制圖自檢腳本」 | 同上 |
| `sample-s5-xbar-r.csv` | 管制圖虛構資料（S5；20 組，xbar 與 range 兩欄；X̄ 界限 8.8／10／11.2、R 界限 0.15／1.2／2.25（示意，不是係數算的）；第 1 行是 `#` 說明行、第 2 行是欄位名；每列 `data_status` 都是「虛構資料，數字未核」；**數字未核**） | `../control-chart.md` |
| `sample-s5-xbar-r-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「管制圖自檢腳本」 | 同上 |
| `sample-s6-spec-vs-control.csv` | 管制圖虛構資料（S6；24 組；管制界限 44／50／56，規格 USL 58、LSL 42；第 1 行是 `#` 說明行、第 2 行是欄位名；每列 `data_status` 都是「虛構資料，數字未核」；**數字未核**） | `../control-chart.md` |
| `sample-s6-spec-vs-control-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「管制圖自檢腳本」 | 同上 |
| `sample-s7-misread-specs.csv` | 管制圖虛構資料（S7；22 組；管制界限 44／50／56，規格 USL 60、LSL 40；第 17 組超出管制上界但仍在規格內；第 1 行是 `#` 說明行、第 2 行是欄位名；每列 `data_status` 都是「虛構資料，數字未核」；**數字未核**） | `../control-chart.md` |
| `sample-s7-misread-specs-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「管制圖自檢腳本」 | 同上 |
| `sample-s8-before-after.csv` | 管制圖虛構資料（S8；phase 欄分 before／after，各 18 組；目標 10；第 1 行是 `#` 說明行、第 2 行是欄位名；每列 `data_status` 都是「虛構資料，數字未核」；**數字未核**） | `../control-chart.md` |
| `sample-s8-before-after-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「管制圖自檢腳本」 | 同上 |
| `sample-lorenz-s1-anatomy.csv` | 洛倫茲曲線虛構資料（S1 解剖；10 戶 2、3、4、5、6、8、10、14、20、28（合計 100）；最貧 40%（前 4 戶）累計 14%；第 1 行是 `#` 說明行、第 2 行是欄位名；每列 `data_status` 都是「虛構資料，數字未核」；**數字未核**；素材包原名 `sample-s1-anatomy.csv`） | `../lorenz-curve.md` |
| `sample-lorenz-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「洛倫茲曲線資料與自檢腳本」 | 同上 |
| `sample-lorenz-s2-equal-vs-unequal.csv` | 洛倫茲曲線虛構資料（S2；group 分 more_equal（合計 105，以合計為 100%，基尼約 0.08）與 more_unequal（合計 100，基尼約 0.55），各 10 戶；第 1 行是 `#` 說明行、第 2 行是欄位名；每列 `data_status` 都是「虛構資料，數字未核」；**數字未核**；素材包原名 `sample-s2-equal-vs-unequal.csv`） | `../lorenz-curve.md` |
| `sample-lorenz-s2-equal-vs-unequal-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「洛倫茲曲線資料與自檢腳本」 | 同上 |
| `sample-lorenz-s3-gini-area.csv` | 洛倫茲曲線虛構資料（S3（審稿重畫的新版）；10 戶 2、3、4、5、7、9、12、16、20、22（合計 100）；折線下面積法基尼 0.382，乘 10／9 得 0.424；第 1 行是 `#` 說明行、第 2 行是欄位名；每列 `data_status` 都是「虛構資料，數字未核」；**數字未核**；素材包原名 `sample-s3-gini-area.csv`） | `../lorenz-curve.md` |
| `sample-lorenz-s3-gini-area-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「洛倫茲曲線資料與自檢腳本」 | 同上 |
| `sample-lorenz-s4-steps.csv` | 洛倫茲曲線虛構資料（S4；group 分 step1_unsorted（未排序，累計欄為空）與 step2_sorted（排序後，累計 20%→4%、50%→18%、90%→72%），各 10 戶；第 1 行是 `#` 說明行、第 2 行是欄位名；每列 `data_status` 都是「虛構資料，數字未核」；**數字未核**；素材包原名 `sample-s4-steps.csv`） | `../lorenz-curve.md` |
| `sample-lorenz-s4-steps-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「洛倫茲曲線資料與自檢腳本」 | 同上 |
| `sample-lorenz-s5-extremes.csv` | 洛倫茲曲線虛構資料（S5（審稿新版）；group 分 equal（人人相同，基尼 0）與 one_takes_all（一人全拿，10 戶基尼 0.90，修正後 1.0），各 10 戶；第 1 行是 `#` 說明行、第 2 行是欄位名；每列 `data_status` 都是「虛構資料，數字未核」；**數字未核**；素材包原名 `sample-s5-extremes.csv`） | `../lorenz-curve.md` |
| `sample-lorenz-s5-extremes-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「洛倫茲曲線資料與自檢腳本」 | 同上 |
| `sample-lorenz-s6-misread-pareto.csv` | 洛倫茲曲線虛構資料（S6（審稿新版）；group 分 pareto 與 lorenz；同一組 40、25、15、12、8，柏拉圖累計 40、65、80、92、100，洛倫茲累計 8、20、35、60、100；第 1 行是 `#` 說明行、第 2 行是欄位名；每列 `data_status` 都是「虛構資料，數字未核」；**數字未核**；素材包原名 `sample-s6-misread-pareto.csv`） | `../lorenz-curve.md` |
| `sample-lorenz-s6-misread-pareto-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「洛倫茲曲線資料與自檢腳本」 | 同上 |
| `sample-lorenz-s7-same-shape.csv` | 洛倫茲曲線虛構資料（S7（審稿新版）；甲、乙各 10 戶，基尼都是 0.34，曲線在 70% 處相交（都累計 45%）；第 1 行是 `#` 說明行、第 2 行是欄位名；每列 `data_status` 都是「虛構資料，數字未核」；**數字未核**；素材包原名 `sample-s7-same-shape.csv`） | `../lorenz-curve.md` |
| `sample-lorenz-s7-same-shape-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「洛倫茲曲線資料與自檢腳本」 | 同上 |
| `sample-lorenz-s8-two-groups.csv` | 洛倫茲曲線虛構資料（S8；甲、乙各 10 戶，甲基尼約 0.21、乙約 0.46，甲在第 1–9 戶全程高於乙（洛倫茲優勢）；第 1 行是 `#` 說明行、第 2 行是欄位名；每列 `data_status` 都是「虛構資料，數字未核」；**數字未核**；素材包原名 `sample-s8-two-groups.csv`） | `../lorenz-curve.md` |
| `sample-lorenz-s8-two-groups-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「洛倫茲曲線資料與自檢腳本」 | 同上 |
| `sample-marey-s1-anatomy.csv` | 馬雷圖虛構資料（S1；101 次下行、102 次上行對開，每站停 1 分鐘，每分鐘 1 公里；只交叉一次（06:24:30，21.5 公里，丁站與戊站之間）；第 1 行為 `#` 說明；數字未核） | `../marey-chart.md` |
| `sample-marey-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「馬雷圖資料與自檢腳本」 | 同上 |
| `sample-marey-s2-local-vs-express.csv` | 馬雷圖虛構資料（S2；普通車 201 次（丁站待避 3 分鐘）、快車 301 次（不停站，時速 120 公里）與不待避對照線 201-nowait；07:24:00 在丁站超車，不待避則 07:25:00、22 公里追上；第 1 行為 `#` 說明；數字未核） | `../marey-chart.md` |
| `sample-marey-s2-local-vs-express-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「馬雷圖資料與自檢腳本」 | 同上 |
| `sample-marey-s3-single-track-meet.csv` | 馬雷圖虛構資料（S3；單線雙向，402 次在戊站等 9 分鐘；08:27–08:28 同在戊站會車，不等就開（402-nowait）則 08:23:30、20.5 公里在丁站與戊站之間交叉＝衝突；第 1 行為 `#` 說明；數字未核） | `../marey-chart.md` |
| `sample-marey-s3-single-track-meet-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「馬雷圖資料與自檢腳本」 | 同上 |
| `sample-marey-s4-plan-vs-actual.csv` | 馬雷圖虛構資料（S4；同一班車的計畫線與實際線；到站晚 1、2、7、7、7 分鐘，誤點組成加起來 7 分鐘；第 1 行為 `#` 說明；數字未核） | `../marey-chart.md` |
| `sample-marey-s4-plan-vs-actual-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「馬雷圖資料與自檢腳本」 | 同上 |
| `sample-marey-s5-bus-bunching.csv` | 馬雷圖虛構資料（S5；5 輛公車、13 個站牌（每站相隔 1 公里），3 號車晚 3 分鐘出發；3→4 號車到站時刻差 5→0.2 分鐘（第 7 站 0.81 首次小於 1）；第 1 行為 `#` 說明；數字未核） | `../marey-chart.md` |
| `sample-marey-s5-bus-bunching-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「馬雷圖資料與自檢腳本」 | 同上 |
| `sample-marey-s6-misread-equal-spacing.csv` | 馬雷圖虛構資料（S6；同一班車每段時速 60 公里，站點在 0、2、4、18、20、30 公里；等距排列時丙→丁看起來最平；第 1 行為 `#` 說明；數字未核） | `../marey-chart.md` |
| `sample-marey-s6-misread-equal-spacing-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「馬雷圖資料與自檢腳本」 | 同上 |
| `sample-marey-s7-too-dense-zoom.csv` | 馬雷圖虛構資料（S7；每班車一列（不是站點長表，9 欄）：全天雙向 284 班＝普通 218＋快車 66，放大區 07:00–09:00 下行 16 班（5.6%），同時在線最多 10 班；第 1 行為 `#` 說明；數字未核） | `../marey-chart.md` |
| `sample-marey-s7-too-dense-zoom-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「馬雷圖資料與自檢腳本」 | 同上 |
| `sample-marey-s8-steps.csv` | 馬雷圖虛構資料（S8；製作步驟範例，甲到丁四站（0、6、9、20 公里），501 次下行、502 次上行；只交叉一次（10:13:30，11.5 公里）；第 1 行為 `#` 說明；數字未核） | `../marey-chart.md` |
| `sample-marey-s8-steps-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「馬雷圖資料與自檢腳本」 | 同上 |
| `sample-km-s1-anatomy.csv` | 存活曲線虛構資料（S1；單一組 30 人，中位 10.3 月；第 6／12／24 月存活 0.783／0.491／0.409；風險人數每 6 月 30、21、8、6、2、1；第 1 行為 `#` 說明；數字未核） | `../kaplan-meier-survival.md` |
| `sample-km-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫＋numpy，不是資料）；見下方「存活曲線資料與自檢腳本」 | 同上 |
| `sample-km-s2-two-groups.csv` | 存活曲線虛構資料（S2；新療法與標準療法各 100 人；中位 20.4 對 14.5 月；風險比 0.65；對數等級 P=0.0223；第 1 行為 `#` 說明；數字未核） | `../kaplan-meier-survival.md` |
| `sample-km-s2-two-groups-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫＋numpy，不是資料）；見下方「存活曲線資料與自檢腳本」 | 同上 |
| `sample-km-s3-censoring.csv` | 存活曲線虛構資料（S3；同一份 200 人三種設限處理；正確第 12 月 0.637、當事件 0.42、刪掉 0.312；中位 16.9／9.7／7.0；第 1 行為 `#` 說明；數字未核） | `../kaplan-meier-survival.md` |
| `sample-km-s3-censoring-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫＋numpy，不是資料）；見下方「存活曲線資料與自檢腳本」 | 同上 |
| `sample-km-s4-confidence-band.csv` | 存活曲線虛構資料（S4；60 人；第 6／18／30 月區間寬 0.144／0.222／0.316；第 1 行為 `#` 說明；數字未核） | `../kaplan-meier-survival.md` |
| `sample-km-s4-confidence-band-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫＋numpy，不是資料）；見下方「存活曲線資料與自檢腳本」 | 同上 |
| `sample-km-s5-tail.csv` | 存活曲線虛構資料（S5；40 人；中位 8.5 月；風險人數少於 5 自 22.2 月；末事件 27.3 月時風險 3；第 1 行為 `#` 說明；數字未核） | `../kaplan-meier-survival.md` |
| `sample-km-s5-tail-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫＋numpy，不是資料）；見下方「存活曲線資料與自檢腳本」 | 同上 |
| `sample-km-s6-crossing.csv` | 存活曲線虛構資料（S6；手術／藥物各 150 人；交叉精確 20.0 月；整段風險比 0.88，前段 1.20、後段 0.32；中位 25.7／21.4；第 1 行為 `#` 說明；數字未核） | `../kaplan-meier-survival.md` |
| `sample-km-s6-crossing-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫＋numpy，不是資料）；見下方「存活曲線資料與自檢腳本」 | 同上 |
| `sample-km-s7-y-axis.csv` | 存活曲線虛構資料（S7；甲乙各 400 人；第 24 月 0.923 對 0.888（差 3.5 百分點）；P=0.0917；第 1 行為 `#` 說明；數字未核） | `../kaplan-meier-survival.md` |
| `sample-km-s7-y-axis-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫＋numpy，不是資料）；見下方「存活曲線資料與自檢腳本」 | 同上 |
| `sample-km-s8-step-by-step.csv` | 存活曲線虛構資料（S8；8 人手算步驟；階梯 0.875→0.750→0.600→0.450→0.225；中位第 7 月；6 欄含 name；第 1 行為 `#` 說明；數字未核） | `../kaplan-meier-survival.md` |
| `sample-km-s8-step-by-step-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫＋numpy，不是資料）；見下方「存活曲線資料與自檢腳本」 | 同上 |
| `sample-swimmer-s1-anatomy.csv` | 游泳圖虛構資料（S1；20 位受試者構造示範；最長 P02 22.5 月仍在、最短 P18 1.7 月副作用；仍在 4、有緩解 9、完全緩解 3；中位 7.0；10 欄；第 1 行為 `#` 說明；數字未核） | `../swimmer-plot.md` |
| `sample-swimmer-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「游泳圖資料與自檢腳本」 | 同上 |
| `sample-swimmer-s2-grouped-color.csv` | 游泳圖虛構資料（S2；低劑量／高劑量各 10 人；中位 4.3 對 11.25 月；有緩解 2 對 7；前 10 長棒高 6 低 4；7 欄；第 1 行為 `#` 說明；數字未核） | `../swimmer-plot.md` |
| `sample-swimmer-s2-grouped-color-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「游泳圖資料與自檢腳本」 | 同上 |
| `sample-swimmer-s3-sorting.csv` | 游泳圖虛構資料（S3；依長度排序 vs 依編號排序；排序與入組月 Spearman −0.32（同分取平均名次，精確 −0.3185）；6 欄；第 1 行為 `#` 說明；數字未核） | `../swimmer-plot.md` |
| `sample-swimmer-s3-sorting-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫；有 scipy 時另交叉核對，不是資料）；見下方「游泳圖資料與自檢腳本」 | 同上 |
| `sample-swimmer-s4-duration-of-response.csv` | 游泳圖虛構資料（S4；9 位有緩解者的反應持續時間；結束於惡化 5、設限 4；最長 P13 12.2 月；9 欄；第 1 行為 `#` 說明；數字未核） | `../swimmer-plot.md` |
| `sample-swimmer-s4-duration-of-response-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「游泳圖資料與自檢腳本」 | 同上 |
| `sample-swimmer-s5-stop-reasons.csv` | 游泳圖虛構資料（S5；停止原因：惡化 13、副作用 2、退出 1、仍在 4；5 欄；第 1 行為 `#` 說明；數字未核） | `../swimmer-plot.md` |
| `sample-swimmer-s5-stop-reasons-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「游泳圖資料與自檢腳本」 | 同上 |
| `sample-swimmer-s6-cutoff-misread.csv` | 游泳圖虛構資料（S6；同一批人在第 12 月與第 24 月兩個截止日；第 12 月入組 17、仍在 11；7 欄；第 1 行為 `#` 說明；數字未核） | `../swimmer-plot.md` |
| `sample-swimmer-s6-cutoff-misread-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「游泳圖資料與自檢腳本」 | 同上 |
| `sample-swimmer-s7-too-many-vs-km.csv` | 游泳圖虛構資料（S7；150 人太多改 KM；停止 84／26／24／16、事件 134、中位 6.0；6 欄；第 1 行為 `#` 說明；數字未核） | `../swimmer-plot.md` |
| `sample-swimmer-s7-too-many-vs-km-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「游泳圖資料與自檢腳本」 | 同上 |
| `sample-swimmer-s8-steps.csv` | 游泳圖虛構資料（S8；取最早入組 6 人 P01–P06 的手繪步驟；排序 P02 22.5 → P06 2.6；9 欄；第 1 行為 `#` 說明；數字未核） | `../swimmer-plot.md` |
| `sample-swimmer-s8-steps-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「游泳圖資料與自檢腳本」 | 同上 |
| `sample-lasagna-s1-anatomy.csv` | 千層麵圖虛構資料（S1；40 人 × 12 週＝480 格長表；缺值 33（退出 4 人 21 格＋零星 12 格）；P07 第 5 週 153；第 1 行為 `#` 說明；數字未核） | `../lasagna-plot.md` |
| `sample-lasagna-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「千層麵圖資料與自檢腳本」 | 同上 |
| `sample-lasagna-s2-spaghetti-vs-lasagna.csv` | 千層麵圖虛構資料（S2；一人一列寬表；個人平均最高 P19 164.0、最低 P33 121.4；第 1 行為 `#` 說明；數字未核） | `../lasagna-plot.md` |
| `sample-lasagna-s2-spaghetti-vs-lasagna-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「千層麵圖資料與自檢腳本」 | 同上 |
| `sample-lasagna-s3-sorting.csv` | 千層麵圖虛構資料（S3；三種列排序；前 10 名介入組 2、後 10 名 9；組平均 149.7／138.8；第 1 行為 `#` 說明；數字未核） | `../lasagna-plot.md` |
| `sample-lasagna-s3-sorting-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「千層麵圖資料與自檢腳本」 | 同上 |
| `sample-lasagna-s4-categorical.csv` | 千層麵圖虛構資料（S4；教學用四級（非臨床標準）；第 1 週 0／1／5／32 缺 2、第 12 週 2／5／9／19 缺 5；第 1 行為 `#` 說明；數字未核） | `../lasagna-plot.md` |
| `sample-lasagna-s4-categorical-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「千層麵圖資料與自檢腳本」 | 同上 |
| `sample-lasagna-s5-missing.csv` | 千層麵圖虛構資料（S5；缺值留白 vs 錯誤補 0；第 12 週 140.5／122.9；第 8 週差 21.4；第 1 行為 `#` 說明；數字未核） | `../lasagna-plot.md` |
| `sample-lasagna-s5-missing-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「千層麵圖資料與自檢腳本」 | 同上 |
| `sample-lasagna-s6-colormap.csv` | 千層麵圖虛構資料（S6；彩虹 vs 單色同一排序；觀測 447 格、135–145 之間 128 格；第 1 行為 `#` 說明；數字未核） | `../lasagna-plot.md` |
| `sample-lasagna-s6-colormap-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「千層麵圖資料與自檢腳本」 | 同上 |
| `sample-lasagna-s7-groups-mean.csv` | 千層麵圖虛構資料（S7；分組面板＋每週平均；對照組 148.35 → 148.4（逢 5 進位）→ 150.2（＋1.8）、介入組 147.2 → 130.2；第 1 行為 `#` 說明；數字未核） | `../lasagna-plot.md` |
| `sample-lasagna-s7-groups-mean-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「千層麵圖資料與自檢腳本」 | 同上 |
| `sample-lasagna-s8-steps.csv` | 千層麵圖虛構資料（S8；P01、P03、P04、P06 前 4 週長表 16 列；排序 P06、P04、P01、P03；第 1 行為 `#` 說明；數字未核） | `../lasagna-plot.md` |
| `sample-lasagna-s8-steps-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「千層麵圖資料與自檢腳本」 | 同上 |
| `sample-recurrence-s1-anatomy.csv` | 遞迴圖虛構資料（S1；正弦波＋雜訊標準化 300 點；第 70／119 點 0.45／0.62、距離 0.17；ε＝0.3 遞迴率 18.8%；第 1 行為 `#` 說明；數字未核） | `../recurrence-plot.md` |
| `sample-recurrence-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「遞迴圖資料與自檢腳本」 | 同上 |
| `sample-recurrence-s2-four-textures.csv` | 遞迴圖虛構資料（S2；四面板各 300 點；遞迴率 14.1%／17.0%／14.1%／21.2%；隨機漫步決定性 79.3%；第 1 行為 `#` 說明；數字未核） | `../recurrence-plot.md` |
| `sample-recurrence-s2-four-textures-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「遞迴圖資料與自檢腳本」 | 同上 |
| `sample-recurrence-s3-threshold.csv` | 遞迴圖虛構資料（S3；同序列只換門檻；ε＝0.05／0.3／1.5 → 遞迴率 3.4%／18.8%／65.7%；第 1 行為 `#` 說明；數字未核） | `../recurrence-plot.md` |
| `sample-recurrence-s3-threshold-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「遞迴圖資料與自檢腳本」 | 同上 |
| `sample-recurrence-s4-embedding.csv` | 遞迴圖虛構資料（S4；只換嵌入；(m,τ)＝(1,1)／(2,8)／(2,15) → 19.4%／5.3%／11.3%；第 1 行為 `#` 說明；數字未核） | `../recurrence-plot.md` |
| `sample-recurrence-s4-embedding-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「遞迴圖資料與自檢腳本」 | 同上 |
| `sample-recurrence-s5-period-spacing.csv` | 遞迴圖虛構資料（S5；斜線間距＝週期；遞迴率 18.6%；高峰 50／100／150 黑格 85.2%／83.0%／84.0%；第 1 行為 `#` 說明；數字未核） | `../recurrence-plot.md` |
| `sample-recurrence-s5-period-spacing-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「遞迴圖資料與自檢腳本」 | 同上 |
| `sample-recurrence-s6-stuck-block.csv` | 遞迴圖虛構資料（S6；卡住 50 點；正常／卡住遞迴率 14.3%／16.6%；第 1 行為 `#` 說明；數字未核） | `../recurrence-plot.md` |
| `sample-recurrence-s6-stuck-block-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「遞迴圖資料與自檢腳本」 | 同上 |
| `sample-recurrence-s7-cross-recurrence.csv` | 遞迴圖虛構資料（S7；交叉遞迴圖；交叉遞迴率 19.0%；錯開 10 點 85.5%、錯開 0 點 11.0%；第 1 行為 `#` 說明；數字未核） | `../recurrence-plot.md` |
| `sample-recurrence-s7-cross-recurrence-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「遞迴圖資料與自檢腳本」 | 同上 |
| `sample-recurrence-s8-steps.csv` | 遞迴圖虛構資料（S8；8 個讀數製作步驟；平均 13.50、標準差 1.50；13 黑／49 格＝26.5%；第 1 行為 `#` 說明；數字未核） | `../recurrence-plot.md` |
| `sample-recurrence-s8-steps-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「遞迴圖資料與自檢腳本」 | 同上 |
| `sample-spectrogram-s1-anatomy.csv` | 頻譜圖虛構資料（S1；縮小版：帶限重取樣 8000→4000 赫茲、8000 列、114864 位元組；窗 256 點仍 64 毫秒、移動 64 點；窗數 122、頻率格 129、間隔 15.625 赫茲；最亮格 437.5 赫茲；1203.125 赫茲高於 −20 分貝的窗中心 0.8–1.408 秒；第 1 行為 `#` 說明、無每列 data_status；數字未核） | `../spectrogram.md` |
| `sample-spectrogram-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「頻譜圖資料與自檢腳本」 | 同上 |
| `sample-spectrogram-s2-four-patterns.csv` | 頻譜圖虛構資料（S2；縮小版：截取第 6400–9599 點、3200 列、145960 位元組；窗數 47；啁啾 1 秒最亮格 1593.75 赫茲、敲擊窗中心 1.0 秒、諧波 10 條；第 1 行為 `#` 說明；數字未核） | `../spectrogram.md` |
| `sample-spectrogram-s2-four-patterns-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「頻譜圖資料與自檢腳本」 | 同上 |
| `sample-spectrogram-s3-window-tradeoff.csv` | 頻譜圖虛構資料（S3；縮小版：截取第 0–11263 點、11264 列、164854 位元組；窗長 64／512／4096 點的窗數 701／85／8；凹陷 0.0／61.6、29.0／0.0、76.4／0.0 分貝；第 1 行為 `#` 說明；數字未核） | `../spectrogram.md` |
| `sample-spectrogram-s3-window-tradeoff-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「頻譜圖資料與自檢腳本」 | 同上 |
| `sample-spectrogram-s4-linear-vs-db.csv` | 頻譜圖虛構資料（S4；縮小版：截取第 4096–12287 點、8192 列、123619 位元組；窗數 61；−40.0 與 −60.0 分貝、線性份額 0.0001；第 1 行為 `#` 說明；數字未核） | `../spectrogram.md` |
| `sample-spectrogram-s4-linear-vs-db-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「頻譜圖資料與自檢腳本」 | 同上 |
| `sample-spectrogram-s5-linear-vs-mel.csv` | 頻譜圖虛構資料（S5；縮小版：取樣率仍 16000 赫茲、截取第 16000–28799 點、12800 列、204142 位元組；窗數 97；1000 赫茲＝1000.0 梅爾、8000 赫茲＝2840.0 梅爾；12.5%／35.2%；開頭最亮格 187.5 赫茲；第 1 行為 `#` 說明；數字未核） | `../spectrogram.md` |
| `sample-spectrogram-s5-linear-vs-mel-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「頻譜圖資料與自檢腳本」 | 同上 |
| `sample-spectrogram-s6-motor-fault.csv` | 頻譜圖虛構資料（S6；縮小版：帶限重取樣 2000→250 赫茲、15000 列、217651 位元組；窗 256 點仍 1.024 秒；窗數 116、頻率格 129、間隔約 0.977 赫茲；107.422 赫茲、中位數 −53.0、35.84 秒、最後一窗 −11.3 分貝；第 1 行為 `#` 說明；數字未核） | `../spectrogram.md` |
| `sample-spectrogram-s6-motor-fault-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「頻譜圖資料與自檢腳本」 | 同上 |
| `sample-spectrogram-s7-spectrum-vs-spectrogram.csv` | 頻譜圖虛構資料（S7；縮小版：帶限重取樣 8000→4000 赫茲、8000 列、193794 位元組；窗 256、移動 64、窗數 122；平均頻譜 400／1200 赫茲相差 0.0／0.0 分貝；第 1 行為 `#` 說明；數字未核） | `../spectrogram.md` |
| `sample-spectrogram-s7-spectrum-vs-spectrogram-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「頻譜圖資料與自檢腳本」 | 同上 |
| `sample-spectrogram-s8-steps.csv` | 頻譜圖虛構資料（S8；與素材包逐位元相同、64 列、2993 位元組；7 窗、9 格；各窗最亮 125／125／125／187.5／250／250／250 赫茲；第 4 窗 −5.6／−5.5 分貝；保留 data_status；第 1 行為 `#` 說明；數字未核） | `../spectrogram.md` |
| `sample-spectrogram-s8-steps-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「頻譜圖資料與自檢腳本」 | 同上 |
| `sample-autocorr-s1-anatomy.csv` | 自相關圖虛構資料（S1；與素材包逐位元相同、200 列、9611 位元組；n＝200、最大滯後 30；滯後 0＝1、半寬 0.1386、滯後 1／12／24＝0.759／0.838／0.787；第 1 行為 `#` 說明、每列 data_status；數字未核） | `../autocorrelation-plot.md` |
| `sample-autocorr-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「自相關圖資料與自檢腳本」 | 同上 |
| `sample-autocorr-s2-three-patterns.csv` | 自相關圖虛構資料（S2；與素材包逐位元相同、300 列、23143 位元組；白噪音／趨勢／週期 7 三欄；半寬 0.1132；第 1 行為 `#` 說明；數字未核） | `../autocorrelation-plot.md` |
| `sample-autocorr-s2-three-patterns-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「自相關圖資料與自檢腳本」 | 同上 |
| `sample-autocorr-s3-acf-pacf.csv` | 自相關圖虛構資料（S3；與素材包逐位元相同、500 列、23690 位元組；自我迴歸階 2；半寬 0.0877；偏自相關約在階 2 後進帶；第 1 行為 `#` 說明；數字未核） | `../autocorrelation-plot.md` |
| `sample-autocorr-s3-acf-pacf-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「自相關圖資料與自檢腳本」 | 同上 |
| `sample-autocorr-s4-sample-size-ci.csv` | 自相關圖虛構資料（S4；與素材包逐位元相同、1050 列、53579 位元組；三條白噪音 n＝50／200／800；半寬 0.2772／0.1386／0.0693；第 1 行為 `#` 說明；數字未核） | `../autocorrelation-plot.md` |
| `sample-autocorr-s4-sample-size-ci-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「自相關圖資料與自檢腳本」 | 同上 |
| `sample-autocorr-s5-period-spikes.csv` | 自相關圖虛構資料（S5；與素材包逐位元相同、400 列、19011 位元組；週期 7；滯後 7／14／21／28＝0.913／0.9／0.882／0.862；第 1 行為 `#` 說明；數字未核） | `../autocorrelation-plot.md` |
| `sample-autocorr-s5-period-spikes-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「自相關圖資料與自檢腳本」 | 同上 |
| `sample-autocorr-s6-nonstationary.csv` | 自相關圖虛構資料（S6；與素材包逐位元相同、300 列、18470 位元組；隨機漫步＋一階差分；未差分滯後 1／20／40＝0.971／0.498／-0.006；第 1 行為 `#` 說明；數字未核） | `../autocorrelation-plot.md` |
| `sample-autocorr-s6-nonstationary-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「自相關圖資料與自檢腳本」 | 同上 |
| `sample-autocorr-s7-two-correlograms.csv` | 自相關圖虛構資料（S7；與素材包逐位元相同、200 列、24927 位元組；左時間序列滯後 10＝0.837；右五個虛構變數甲到戊相關矩陣；第 1 行為 `#` 說明；數字未核） | `../autocorrelation-plot.md` |
| `sample-autocorr-s7-two-correlograms-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「自相關圖資料與自檢腳本」 | 同上 |
| `sample-autocorr-s8-steps.csv` | 自相關圖虛構資料（S8；與素材包逐位元相同、120 列、5755 位元組；最大滯後 24、n/4＝30；滯後 1／8／16／24＝0.576／0.799／0.752／0.693；第 1 行為 `#` 說明；數字未核） | `../autocorrelation-plot.md` |
| `sample-autocorr-s8-steps-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「自相關圖資料與自檢腳本」 | 同上 |
| `sample-lagplot-s1-anatomy.csv` | 滯後圖虛構資料（S1；與素材包逐位元相同、120 列、5527 位元組；n＝120、滯後 1、119 對；皮爾森約 0.722、自相關約 0.711；第 1 行為 `#` 說明、每列 data_status；數字未核） | `../lag-plot.md` |
| `sample-lagplot-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「滯後圖資料與自檢腳本」 | 同上 |
| `sample-lagplot-s2-six-patterns.csv` | 滯後圖虛構資料（S2；與素材包逐位元相同、200 列、24246 位元組；六格滯後 1 約 0.008／0.763／-0.705／0.81／0.755／0.985；0.763 對模型係數 0.9 是抽樣偏差；第 1 行為 `#` 說明；數字未核） | `../lag-plot.md` |
| `sample-lagplot-s2-six-patterns-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「滯後圖資料與自檢腳本」 | 同上 |
| `sample-lagplot-s3-lag-k-panels.csv` | 滯後圖虛構資料（S3；與素材包逐位元相同、144 列、7108 位元組；週期 12；皮爾森滯後 1／2／3／6／9／12 約 0.794／0.461／-0.004／-0.929／0.002／0.928；第 1 行為 `#` 說明；數字未核） | `../lag-plot.md` |
| `sample-lagplot-s3-lag-k-panels-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「滯後圖資料與自檢腳本」 | 同上 |
| `sample-lagplot-s4-vs-acf.csv` | 滯後圖虛構資料（S4；與素材包逐位元相同、30 列、1516 位元組；自相關對皮爾森：滯後 1 約 0.708 對 0.729、滯後 3 約 0.329 對 0.426、滯後 6 約 0.058 對 0.149；半寬約 0.358；第 1 行為 `#` 說明；數字未核） | `../lag-plot.md` |
| `sample-lagplot-s4-vs-acf-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「滯後圖資料與自檢腳本」 | 同上 |
| `sample-lagplot-s5-nonlinear.csv` | 滯後圖虛構資料（S5；與素材包逐位元相同、300 列、14134 位元組；滯後 1 約 -0.138；帶約 ±0.113，滯後 1–10 有 2 根在帶外；第 1 行為 `#` 說明；數字未核） | `../lag-plot.md` |
| `sample-lagplot-s5-nonlinear-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「滯後圖資料與自檢腳本」 | 同上 |
| `sample-lagplot-s6-outliers.csv` | 滯後圖虛構資料（S6；與素材包逐位元相同、150 列、9035 位元組；第 41 點約 55.2、第 102 點約 43.4；含離群值約 0.464、拿掉約 0.585；第 1 行為 `#` 說明；數字未核） | `../lag-plot.md` |
| `sample-lagplot-s6-outliers-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「滯後圖資料與自檢腳本」 | 同上 |
| `sample-lagplot-s7-scatter-lag-recurrence.csv` | 滯後圖虛構資料（S7；與素材包逐位元相同、100 列、6022 位元組；上約 0.965、中約 0.905、下黑點約 16.4%；直式上／中／下；第 1 行為 `#` 說明；數字未核） | `../lag-plot.md` |
| `sample-lagplot-s7-scatter-lag-recurrence-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「滯後圖資料與自檢腳本」 | 同上 |
| `sample-lagplot-s8-how-to.csv` | 滯後圖虛構資料（S8；與素材包逐位元相同、12 列、542 位元組；11 對；滯後 1 約 0.047（正文亦寫約 0.05）；模型係數 0.6；第 1 行為 `#` 說明；數字未核） | `../lag-plot.md` |
| `sample-lagplot-s8-how-to-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「滯後圖資料與自檢腳本」 | 同上 |
| `sample-seasonal-subseries-sim-s1-anatomy.csv` | 季節子序列圖虛構資料（S1；72 列、3694 位元組；2019–2024；7 月平均 447.4 最高、1 月 203.3 最低；第 1 行為 `#` 說明、每列 data_status；數字未核；本課沒有改檔，不宣稱與素材包逐位元相同） | `../seasonal-subseries-plot.md` |
| `sample-seasonal-subseries-sim-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「季節子序列圖資料與自檢腳本」 | 同上 |
| `sample-seasonal-subseries-sim-s2-three-views.csv` | 季節子序列圖虛構資料（S2；96 列、4881 位元組；2017–2024；6／7／8 月斜率 13.9／15.2／15.9，夏季平均斜率 15.0；版面上／中／下；第 1 行為 `#` 說明；數字未核；不宣稱與素材包逐位元相同） | `../seasonal-subseries-plot.md` |
| `sample-seasonal-subseries-sim-s2-three-views-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「季節子序列圖資料與自檢腳本」 | 同上 |
| `sample-seasonal-subseries-sim-s3-shifting-peak.csv` | 季節子序列圖虛構資料（S3；120 列、6065 位元組；7 月斜率 −1.5、9 月 +2.0；前 3 年高峰 8 月、後 3 年 9 月；第 1 行為 `#` 說明；數字未核；不宣稱與素材包逐位元相同） | `../seasonal-subseries-plot.md` |
| `sample-seasonal-subseries-sim-s3-shifting-peak-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「季節子序列圖資料與自檢腳本」 | 同上 |
| `sample-seasonal-subseries-sim-s4-trend-first.csv` | 季節子序列圖虛構資料（S4；120 列、7482 位元組；`detrended`＝扣趨勢直線；上格平均斜率約 5.9；下格高低差 10.2、6 月高、1 月低；第 1 行為 `#` 說明；數字未核；不宣稱與素材包逐位元相同） | `../seasonal-subseries-plot.md` |
| `sample-seasonal-subseries-sim-s4-trend-first-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「季節子序列圖資料與自檢腳本」 | 同上 |
| `sample-seasonal-subseries-sim-s5-no-season.csv` | 季節子序列圖虛構資料（S5；120 列、7401 位元組；純雜訊高低差 6.5、有季節 10.7；第 1 行為 `#` 說明；數字未核；不宣稱與素材包逐位元相同） | `../seasonal-subseries-plot.md` |
| `sample-seasonal-subseries-sim-s5-no-season-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「季節子序列圖資料與自檢腳本」 | 同上 |
| `sample-seasonal-subseries-sim-s6-outlier.csv` | 季節子序列圖虛構資料（S6；96 列、4883 位元組；2021 年 3 月 43.1；3 月平均含 68.8、不含 72.4，中位數 72.8；第 1 行為 `#` 說明；數字未核；不宣稱與素材包逐位元相同） | `../seasonal-subseries-plot.md` |
| `sample-seasonal-subseries-sim-s6-outlier-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「季節子序列圖資料與自檢腳本」 | 同上 |
| `sample-seasonal-subseries-sim-s7-acf-lag-subseries.csv` | 季節子序列圖虛構資料（S7；120 列、5693 位元組；自相關滯後 12／24／6＝0.752／0.701／−0.793；滯後 12 皮爾森約 0.82；半寬約 0.179；2 月高、7 月低；直式上／中／下；第 1 行為 `#` 說明；數字未核；不宣稱與素材包逐位元相同） | `../seasonal-subseries-plot.md` |
| `sample-seasonal-subseries-sim-s7-acf-lag-subseries-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「季節子序列圖資料與自檢腳本」 | 同上 |
| `sample-seasonal-subseries-sim-s8-how-to.csv` | 季節子序列圖虛構資料（S8；12 列、608 位元組；2022–2024 季資料；季平均 44.7／58.7／65.7／49.3；第 1 行為 `#` 說明；數字未核；不宣稱與素材包逐位元相同） | `../seasonal-subseries-plot.md` |
| `sample-seasonal-subseries-sim-s8-how-to-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「季節子序列圖資料與自檢腳本」 | 同上 |
| `sample-seasonal-subseries-noaa-co2-2000-2025.csv` | 季節子序列圖真實資料（毛納羅亞每月二氧化碳 2000–2025；312 列、10990 位元組；美國政府公有領域、2026-10-11 下載；2022-12 至 2023-07 初改用毛納基亞；data_status「真實資料」；圖 R15、圖 R16；本課沒有改檔，不宣稱與素材包逐位元相同） | `../seasonal-subseries-plot.md` |
| `sample-seasonal-subseries-noaa-co2-2000-2025-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「季節子序列圖資料與自檢腳本」 | 同上 |
| `sample-seasonal-decomp-sim-s1-anatomy.csv` | 季節分解圖虛構資料（S1；120 列、4858 位元組；2015–2024；殘差最大絕對值 4.4、季節 9.8；趨勢頭尾各空 6 格；有值處原始＝三成分之和；第 1 行就是表頭、沒有 `#`、沒有 data_status；數字未核；本課沒有改檔，不宣稱與素材包逐位元相同） | `../seasonal-decomposition-plot.md` |
| `sample-seasonal-decomp-sim-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「季節分解圖資料與自檢腳本」 | 同上 |
| `sample-seasonal-decomp-sim-s2-add-vs-mult.csv` | 季節分解圖虛構資料（S2；120 列、3792 位元組；加法殘差前 24／後 24 筆母體標準差 14.47／15.98，乘法 0.02／0.01；直式上／中／下；第 1 行就是表頭、沒有 `#`、沒有 data_status；數字未核；不宣稱與素材包逐位元相同） | `../seasonal-decomposition-plot.md` |
| `sample-seasonal-decomp-sim-s2-add-vs-mult-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「季節分解圖資料與自檢腳本」 | 同上 |
| `sample-seasonal-decomp-sim-s3-classical-vs-stl.csv` | 季節分解圖虛構資料（S3；120 列、3905 位元組；古典殘差標準差 5.28、STL 2.39；STL 季節窗 7 不在 CSV、自檢未核對；直式上／中／下；第 1 行就是表頭、沒有 `#`、沒有 data_status；數字未核；不宣稱與素材包逐位元相同） | `../seasonal-decomposition-plot.md` |
| `sample-seasonal-decomp-sim-s3-classical-vs-stl-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「季節分解圖資料與自檢腳本」 | 同上 |
| `sample-seasonal-decomp-sim-s4-no-season.csv` | 季節分解圖虛構資料（S4；120 列、3918 位元組；季節最大絕對值 1.29、殘差標準差 2.64；直式上／中／下；第 1 行就是表頭、沒有 `#`、沒有 data_status；數字未核；不宣稱與素材包逐位元相同） | `../seasonal-decomposition-plot.md` |
| `sample-seasonal-decomp-sim-s4-no-season-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「季節分解圖資料與自檢腳本」 | 同上 |
| `sample-seasonal-decomp-sim-s5-outlier.csv` | 季節分解圖虛構資料（S5；120 列、5973 位元組；離群值序號 62（year_frac 2020.1667）；古典殘差 51.0、STL 61.6；相對水準 100、每月 +0.5 的直線，古典趨勢鼓起最多 5.4、穩健 STL 1.1；+60 與同月份季節墊高 6.3 自檢未核對；直式上／中／下；第 1 行就是表頭、沒有 `#`、沒有 data_status；數字未核；不宣稱與素材包逐位元相同） | `../seasonal-decomposition-plot.md` |
| `sample-seasonal-decomp-sim-s5-outlier-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「季節分解圖資料與自檢腳本」 | 同上 |
| `sample-splom-sim-s1-anatomy.csv` | 散布圖矩陣虛構資料（S1；80 列、4417 位元組；甲與乙相關 0.7124228200726517，另外兩對絕對值都小於 0.1；第 1 行就是表頭、沒有 `#`、沒有 data_status；數字未核；與素材包逐位元相同） | `../scatterplot-matrix.md` |
| `sample-splom-sim-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「散布圖矩陣資料與自檢腳本」 | 同上 |
| `sample-splom-sim-s2-corr-upper.csv` | 散布圖矩陣練習資料（S2；150 列、2440 位元組；鳶尾花四個數值欄，公有領域；花瓣長與花瓣寬相關 0.962865431402796，六對裡絕對值最大；沒有品種欄；第 1 行就是表頭、沒有 `#`、沒有 data_status；課程稿圖說標未核；與素材包逐位元相同） | `../scatterplot-matrix.md` |
| `sample-splom-sim-s2-corr-upper-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「散布圖矩陣資料與自檢腳本」 | 同上 |
| `sample-splom-sim-s3-grouped-shapes.csv` | 散布圖矩陣練習資料（S3；333 列、10826 位元組；Palmer Penguins，CC0；阿德利 146、帽帶 68、巴布亞 119；巴布亞平均鰭長與平均體重最高，但仍與另外兩組重疊；品種欄沒有形狀；第 1 行就是表頭、沒有 `#`、沒有 data_status；課程稿圖說標未核；與素材包逐位元相同） | `../scatterplot-matrix.md` |
| `sample-splom-sim-s3-grouped-shapes-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「散布圖矩陣資料與自檢腳本」 | 同上 |
| `sample-splom-sim-s4-too-many-vs-heatmap.csv` | 散布圖矩陣虛構資料（S4；100 列、13687 位元組；七欄、非對角 21 對；最大絕對相關是丙與戊 0.8067857797701805；版面左／右；第 1 行就是表頭、沒有 `#`、沒有 data_status；數字未核；與素材包逐位元相同） | `../scatterplot-matrix.md` |
| `sample-splom-sim-s4-too-many-vs-heatmap-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「散布圖矩陣資料與自檢腳本」 | 同上 |
| `sample-splom-sim-s5-outlier-multicell.csv` | 散布圖矩陣虛構資料（S5；61 列、3727 位元組；離群點 (22, 4, 18) 僅一列，甲與丙高於其餘、乙低於其餘；第 1 行就是表頭、沒有 `#`、沒有 data_status；數字未核；與素材包逐位元相同） | `../scatterplot-matrix.md` |
| `sample-splom-sim-s5-outlier-multicell-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「散布圖矩陣資料與自檢腳本」 | 同上 |
| `sample-taylor-sim-s1-anatomy.csv` | 泰勒圖模擬範例資料（S1；2 列、71 位元組；觀測 std 1.0、corr 1.0、note 參考點，對自己的中心化均方根誤差 0；模型甲 1.2、0.75、note 示意，E'＝0.8；圖說的紅方是畫法，CSV 沒有顏色欄；第 1 行就是表頭、沒有 `#`、沒有 data_status；數字未核；與素材包逐位元相同） | `../taylor-diagram.md` |
| `sample-taylor-sim-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「泰勒圖資料與自檢腳本」 | 同上 |
| `sample-taylor-sim-s2-models.csv` | 泰勒圖模擬範例資料（S2；6 列、109 位元組；模型 A 的 E'＝0.3999999999999999，六點裡最小；形狀在 `marker` 欄；第 1 行就是表頭、沒有 `#`、沒有 data_status；數字未核；與素材包逐位元相同） | `../taylor-diagram.md` |
| `sample-taylor-sim-s2-models-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「泰勒圖資料與自檢腳本」 | 同上 |
| `sample-taylor-sim-s3-normalize.csv` | 泰勒圖模擬範例資料（S3；4 列、113 位元組；版面上／下：raw 雨量 3.2／0.85、raw 氣溫 1.1／0.9、norm 雨量 1.07／0.85、norm 氣溫 1.1／0.9；E' 只在正規化面板、以 s_r＝1 重算；第 1 行就是表頭、沒有 `#`、沒有 data_status；數字未核；與素材包逐位元相同） | `../taylor-diagram.md` |
| `sample-taylor-sim-s3-normalize-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「泰勒圖資料與自檢腳本」 | 同上 |
| `sample-taylor-sim-s4-crowded-vs-few.csv` | 泰勒圖模擬範例資料（S4；4 列、92 位元組；CSV 只有 few 四列，沒有圖說的 24 點；甲的 E' 最小；版面上廿四點／下四點；第 1 行就是表頭、沒有 `#`、沒有 data_status；數字未核；與素材包逐位元相同） | `../taylor-diagram.md` |
| `sample-taylor-sim-s4-crowded-vs-few-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「泰勒圖資料與自檢腳本」 | 同上 |
| `sample-taylor-sim-s5-improvement.csv` | 泰勒圖模擬範例資料（S5；2 列、53 位元組；舊版 1.35／0.6、新版 1.05／0.88，新版更靠近觀測；紅到綠的箭頭是圖說，CSV 沒有顏色欄；第 1 行就是表頭、沒有 `#`、沒有 data_status；數字未核；與素材包逐位元相同） | `../taylor-diagram.md` |
| `sample-taylor-sim-s5-improvement-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「泰勒圖資料與自檢腳本」 | 同上 |
| `sample-periodogram-sim-s1-anatomy.csv` | 週期圖模擬範例資料（S1；200 列、5224 位元組；`t_s,x`；時間 0–0.995 步 0.005；未扣平均尖峰正好 20.0 赫茲、功率 10192.720424279498；第 1 行就是表頭、沒有 `#`、沒有 data_status；模擬範例資料、數字未核；與素材包逐位元相同） | `../periodogram.md` |
| `sample-periodogram-sim-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「週期圖資料與自檢腳本」 | 同上 |
| `sample-periodogram-sim-s2-two-tones.csv` | 週期圖模擬範例資料（S2；257 列、8250 位元組；`freq_Hz,power`；高於 0.01 的局部極大是 12.109375 赫茲、0.0568727306453308 與 37.109375 赫茲、0.02650337611567428；第 1 行就是表頭、沒有 `#`、沒有 data_status；模擬範例資料、數字未核；與素材包逐位元相同） | `../periodogram.md` |
| `sample-periodogram-sim-s2-two-tones-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「週期圖資料與自檢腳本」 | 同上 |
| `sample-periodogram-sim-s3-leakage.csv` | 週期圖模擬範例資料（S3；129 列、6233 位元組；`freq_Hz,rect_dB,hann_dB`；兩種窗的尖峰都在 10.15625 赫茲、0.0 分貝；±2 格以外最高旁瓣在 11.328125 赫茲；第 1 行就是表頭、沒有 `#`、沒有 data_status；模擬範例資料、數字未核；與素材包逐位元相同） | `../periodogram.md` |
| `sample-periodogram-sim-s3-leakage-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「週期圖資料與自檢腳本」 | 同上 |
| `sample-periodogram-sim-s4-welch.csv` | 週期圖模擬範例資料（S4；129 列、3842 位元組；`freq_Hz,welch_power`；尖峰正好 25.0 赫茲、功率 0.41938521275201973；原始單段不在 CSV；第 1 行就是表頭、沒有 `#`、沒有 data_status；模擬範例資料、數字未核；與素材包逐位元相同） | `../periodogram.md` |
| `sample-periodogram-sim-s4-welch-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「週期圖資料與自檢腳本」 | 同上 |
| `sample-periodogram-sim-s5-vs-spectrogram.csv` | 週期圖模擬範例資料（S5；501 列、16554 位元組；`freq_Hz,periodogram_power`；15.0 赫茲 1.201085763474063、40.0 赫茲 1.2359419294357712；先後不在 CSV；第 1 行就是表頭、沒有 `#`、沒有 data_status；模擬範例資料、數字未核；與素材包逐位元相同） | `../periodogram.md` |
| `sample-periodogram-sim-s5-vs-spectrogram-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「週期圖資料與自檢腳本」 | 同上 |
| `sample-bode-sim-s1-anatomy.csv` | 波德圖範例資料（S1；17 列、731 位元組；`freq_Hz,gain_dB_measured,phase_deg_measured,gain_dB_theory,phase_deg_theory`；1000 赫茲理論 −3.01 分貝、−45.0 度；模擬範例資料、種子 20261017、數字未核） | `../bode-plot.md` |
| `sample-bode-sim-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「波德圖資料與自檢腳本」 | 同上 |
| `sample-bode-sim-s2-linear-vs-log.csv` | 波德圖範例資料（S2；26 列、431 位元組；`freq_Hz,gain_dB`；存檔最大 630.957 赫茲、−0.176 分貝；5000 赫茲不是一列；模擬範例資料、種子 20261017、數字未核） | `../bode-plot.md` |
| `sample-bode-sim-s2-linear-vs-log-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「波德圖資料與自檢腳本」 | 同上 |
| `sample-bode-sim-s3-order-slope.csv` | 波德圖範例資料（S3；21 列、836 位元組；`freq_Hz,gain1_dB,phase1_deg,gain2_dB,phase2_deg`；一階斜率 −19.957、二階 −40.0；模擬範例資料、種子 20261017、數字未核） | `../bode-plot.md` |
| `sample-bode-sim-s3-order-slope-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「波德圖資料與自檢腳本」 | 同上 |
| `sample-bode-sim-s4-stability-margins.csv` | 波德圖範例資料（S4；29 列、731 位元組；`freq_Hz,open_loop_gain_dB,open_loop_phase_deg`；對數內插裕度 12.074723090701836 分貝、32.732897812097804 度；密格四數不是原列；模擬範例資料、種子 20261017、數字未核） | `../bode-plot.md` |
| `sample-bode-sim-s4-stability-margins-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「波德圖資料與自檢腳本」 | 同上 |
| `sample-bode-sim-s5-signal-vs-system.csv` | 波德圖範例資料（S5；460 列、11280 位元組；`freq_Hz,input_power_dB,output_power_dB`；輸出尖峰 48.828 赫茲、−12.908 分貝；49.68 赫茲、14.02 分貝不在 CSV；模擬範例資料、種子 20261017、數字未核） | `../bode-plot.md` |
| `sample-bode-sim-s5-signal-vs-system-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「波德圖資料與自檢腳本」 | 同上 |
| `sample-hovmoller-sim-s1-anatomy.csv` | 霍夫默勒圖範例資料（S1；61 列、29670 位元組；`day` 加上經度 0 到 360、每 5 度，74 欄；脊線 3.9151242728714966 度／日，印成 3.915，記載 3.89 不是原格；全距 −2.212…0.109；模擬範例資料、種子 20261018、數字未核） | `../hovmoller-diagram.md` |
| `sample-hovmoller-sim-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「霍夫默勒圖資料與自檢腳本」 | 同上 |
| `sample-hovmoller-sim-s2-direction.csv` | 霍夫默勒圖範例資料（S2；31 列、14672 位元組；`day` 加上經度 0 到 360、每 5 度，74 欄；19 天的列最大值在經度 200，全場最大 1.948 也在 200；往東 +6、往西 −8 度／日未核對；模擬範例資料、種子 20261018、數字未核） | `../hovmoller-diagram.md` |
| `sample-hovmoller-sim-s2-direction-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「霍夫默勒圖資料與自檢腳本」 | 同上 |
| `sample-hovmoller-sim-s3-phase-group.csv` | 霍夫默勒圖範例資料（S3；51 列、32099 位元組；`day` 加上經度 0 到 360、每 4 度，92 欄；0 到 10 天、每 0.2 天，不是 51 天；群速脊線 27.990950226244344 度／日，印成 27.99；相速每天 10 度未分開追；模擬範例資料、種子 20261018、數字未核） | `../hovmoller-diagram.md` |
| `sample-hovmoller-sim-s3-phase-group-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「霍夫默勒圖資料與自檢腳本」 | 同上 |
| `sample-hovmoller-sim-s4-colormap.csv` | 霍夫默勒圖範例資料（S4；31 列、14843 位元組；`day` 加上經度 0 到 360、每 5 度，74 欄；每一天 6 次變號，波數 3；色盤名稱不在 CSV；模擬範例資料、種子 20261018、數字未核） | `../hovmoller-diagram.md` |
| `sample-hovmoller-sim-s4-colormap-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「霍夫默勒圖資料與自檢腳本」 | 同上 |
| `sample-hovmoller-sim-s5-traffic.csv` | 霍夫默勒圖範例資料（S5；61 列、17651 位元組；`minute` 加上里程 0 到 20、每 0.5 公里，42 欄；車速 14.859…100.0；高速平均 89.58560792741166，印成 89.59；低於每小時 45 公里的格子 183 個；塞車波每小時 −18 公里未核對；模擬範例資料、種子 20261018、數字未核） | `../hovmoller-diagram.md` |
| `sample-hovmoller-sim-s5-traffic-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「霍夫默勒圖資料與自檢腳本」 | 同上 |
| `sample-skewt-sim-s1-anatomy.csv` | 斜溫圖範例資料（S1；27 列、780 位元組；`pressure_hPa`、`temperature_C`、`dewpoint_C`、`wind_speed_kt`、`wind_dir_deg`；500 百帕 −5.7 度；垂直誤讀與斜角未核；風速風向未另核；模擬範例資料、種子 20261019、數字未核） | `../skew-t-log-p.md` |
| `sample-skewt-sim-s1-anatomy-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「斜溫圖資料與自檢腳本」 | 同上 |
| `sample-skewt-sim-s2-why-skew.csv` | 斜溫圖範例資料（S2；27 列、459 位元組；只有 `pressure_hPa`、`temperature_C`、`dewpoint_C`；左 0 度、右 45 度未核；模擬範例資料、種子 20261019、數字未核） | `../skew-t-log-p.md` |
| `sample-skewt-sim-s2-why-skew-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「斜溫圖資料與自檢腳本」 | 同上 |
| `sample-skewt-sim-s3-parcel-cape.csv` | 斜溫圖範例資料（S3；27 列、617 位元組；多 `surface_parcel_C`；穿越 746.8284542966692 與 162.8008773618526 百帕；2311 與 −87 焦耳／公斤未積分；950 百帕溫差 0 不是自由對流高度；模擬範例資料、種子 20261019、數字未核） | `../skew-t-log-p.md` |
| `sample-skewt-sim-s3-parcel-cape-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「斜溫圖資料與自檢腳本」 | 同上 |
| `sample-skewt-sim-s4-cloud-layers.csv` | 斜溫圖範例資料（S4；27 列、605 位元組；多 `dewpoint_depression_C`；露點差 ≤ 2.0 的連續層是 [975, 775]（9 層）與 [400, 350]（2 層）；地面露點差 2.4；是不是雲未核；模擬範例資料、種子 20261019、數字未核） | `../skew-t-log-p.md` |
| `sample-skewt-sim-s4-cloud-layers-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「斜溫圖資料與自檢腳本」 | 同上 |
| `sample-skewt-sim-s5-stable-unstable.csv` | 斜溫圖範例資料（S5；54 列、1628 位元組；`panel` 先 `stable` 再 `unstable`；穩定面板沒有正的溫度差；印成 943.99 的近地薄正差不是自由對流高度；2455 與 −74 焦耳／公斤未積分；模擬範例資料、種子 20261019、數字未核） | `../skew-t-log-p.md` |
| `sample-skewt-sim-s5-stable-unstable-selfcheck.py` | 上一檔的自檢腳本（只需 Python 標準函式庫，不是資料）；見下方「斜溫圖資料與自檢腳本」 | 同上 |

對應 pattern：`../dot-density-map.md`、`../streamgraph-composition.md`、`../population-pyramid.md`、`../lollipop-rank.md`、`../boxplot-summary.md`、`../bubble-chart.md`、`../marimekko-chart.md`、`../choropleth-map.md`、`../tile-map.md`、`../matrix-heatmap.md`、`../spiral-plot.md`、`../biofabric.md`、`../flame-graph.md`、`../circos.md`、`../volcano-plot.md`、`../manhattan-plot.md`、`../ma-plot.md`、`../qq-plot.md`、`../bland-altman.md`、`../locuszoom.md`、`../pp-plot.md`、`../karyotype-ideogram.md`、`../forest-plot.md`、`../horizon-chart.md`、`../pareto-chart.md`、`../control-chart.md`、`../lorenz-curve.md`、`../marey-chart.md`、`../kaplan-meier-survival.md`、`../swimmer-plot.md`、`../lasagna-plot.md`、`../recurrence-plot.md`、`../spectrogram.md`、`../autocorrelation-plot.md`、`../lag-plot.md`、`../seasonal-subseries-plot.md`、`../seasonal-decomposition-plot.md`、`../scatterplot-matrix.md`、`../taylor-diagram.md`、`../periodogram.md`、`../bode-plot.md`、`../hovmoller-diagram.md`、`../skew-t-log-p.md`。

## 自檢腳本 `sample-ma-selfcheck.py`

檢查 `sample-ma-fictional.csv`：共 3,000 列、`base_mean` 落在 1 至 100000、`a_log2_mean` ＝ log2(base_mean + 1)、`padj` 介於 0 與 1、|收縮後 M| ≤ |收縮前 M|、`gene_id` 不重複。只用 Python 標準函式庫（csv、math），任何 Python 3 都能跑。

腳本用相對路徑讀 CSV，所以要**先進到本資料夾**再執行（在別的資料夾執行會出現 `FileNotFoundError`，不是資料有問題）：

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-ma-selfcheck.py
```

通過時印一行（v0.3.16 上架前已在 python3 實跑，結束碼 0）：`OK 筆數 3000 | base_mean 1.01 ~ 99887.02 | M -4.745 ~ 5.784 | padj<0.05 筆數 197`；任一檢查不過會直接丟出 AssertionError。腳本內容與素材包版本逐位元相同，這個 pattern 的 CSV 與 .py 都未修改。

## QQ 圖自檢腳本 `sample-qq-selfcheck.py`

檢查 `sample-qq-fictional.csv`：共 220 列、`row_id` 不重複、A 組 120 筆與 B 組 100 筆、p 值介於 0 與 1（不含 0）、A 組對常態的相關係數高於 B 組且 B 組最大值離四分位參考線比 A 組遠；另輸出兩組互比的 19 組分位數配對與 −log10(p) 最大值。**需要 numpy 與 scipy**（MA 圖那支只用標準庫）。

**讀檔方式（v0.3.18 後修正）**：早期版本用 `glob.glob('*-fictional.csv')[0]` 找 CSV，資料夾裡有第二、第三個 `*-fictional.csv` 後會抓錯檔（MA 那份筆數不符，Bland–Altman 那份欄位不同，會丟 `KeyError: 'group'`）。現在腳本直接指定 `sample-qq-fictional.csv`，在 `examples/data/` 內執行即可，輸出與素材包所附完全一致：

```bash
cd skills/what-is-the-data-saying/examples/data && python3 sample-qq-selfcheck.py
```

注意：此腳本與專案維護者整理的素材包版本不再逐位元相同，唯一差別是那一行讀檔；資料與檢查邏輯未動。

預期輸出五行（v0.3.17 上架前實跑，結束碼 0，與素材包所附輸出完全一致）：

```
OK 筆數 220 | A 組 120 B 組 100
A 組（近似常態）對常態的相關係數 0.9890；最大值離四分位參考線 0.79
B 組（右偏）對常態的相關係數 0.9258；最大值離四分位參考線 11.92
兩組互比的 19 組分位數配對：第 1 組 (34.76, 46.34)，第 10 組 (51.46, 49.44)，第 19 組 (61.12, 56.68)
觀察 −log10(p) 最大 3.37，期望最大 2.64；p 值小於 0.001 的筆數 1
```

（實跑環境：numpy 2.2.4、scipy 1.18.1；小數位數固定，不同版本理論上可能差最後一位。）

## Bland–Altman 自檢腳本 `sample-ba-selfcheck.py`

檢查 `sample-ba-fictional.csv`：共 220 列、`row_id` 不重複、good 100 對與 fan 120 對、差值一律是方法 B 減方法 A；輸出 good 的平均差、差值標準差、一致性界限與界限外點數，平均差與兩條界限各自的 95% 信賴區間（**近似式**：平均差標準誤 ＝ s／√n，界限標準誤約 √(3s²／n)，t 臨界值固定用 1.984），以及界限連同信賴區間是否都落在**假設的**可接受範圍 ±8 內（範圍是示範假設，不是臨床標準）；fan 輸出平均差、界限，平均值較小與較大兩半的差值標準差（比值約 2，扇形），以及改看百分比差異後兩半的標準差（大致相等）。**需要 numpy**。

腳本以 `os.path.dirname(__file__)` 加明確檔名讀同資料夾的 CSV，**不搜尋檔案**，沒有 QQ 腳本的 `glob` 陷阱，在任何資料夾執行都可以；直接在本資料夾跑：

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-ba-selfcheck.py
```

預期輸出七行（v0.3.18 上架前實跑，結束碼 0，與素材包所附輸出完全一致）：

```
OK 筆數 220 | good 100 fan 120 （差值方向：方法 B 減方法 A）
good：平均差 0.703，差值標準差 2.424，一致性界限 5.454 與 -4.047，界限外 7 點
good：平均差的 95% 信賴區間 0.222 到 1.184；上界的信賴區間 4.621 到 6.286；下界的信賴區間 -4.880 到 -3.214
good：界限連同信賴區間是否都在假設的可接受範圍 ±8 內：是（範圍是假設，非臨床標準）
fan：平均差 0.583，差值標準差 5.375，一致性界限 11.118 與 -9.952
fan：平均值較小一半的差值標準差 3.391，較大一半 6.799，比值 2.01（扇形）
fan：改看百分比差異，兩半標準差 4.81 與 4.32 個百分點（大致相等）
```

**以實際計數為準**：素材包腳本註解寫 good「落在界限外的點很少（約 5%，不是 0）」，實際是 7／100＝7%；腳本沒有輸出 fan 的界限外點數，獨立重算為 5／120。本 repo 另以 numpy／scipy 獨立重算上列各數字，全部一致（以精確 t 臨界值重算 good 的信賴區間與腳本的 1.984 結果相同到小數第三位）。

## LocusZoom 自檢腳本 `sample-locuszoom-selfcheck.py`

檢查 `sample-locuszoom-fictional.csv`：共 2,306 列、`row_id` 不重複、全基因組背景點 1,760 個（染色體 1 到 22 各 80 個）；四段區間（single、following、second、readcolors）各只有一個領先變異、且它是該段最高的點；顏色等級與 r² 數值一致；輸出各區間的點數、領先變異位置與高度、其餘點最高值、超過顯著門檻（−log10(5×10⁻⁸)≈7.30）的點數與各顏色點數；第二個峰（second 區間）14 個點；readcolors 補的 3 個高處深藍點；重組率示意曲線最高處。**需要 numpy**。

腳本以 `os.path.abspath(__file__)` 加明確檔名讀同資料夾的 CSV，**不搜尋檔案**，在任何資料夾執行都可以；直接在本資料夾跑：

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-locuszoom-selfcheck.py
```

預期輸出八行（v0.3.19 上架前實跑，結束碼 0，與素材包所附輸出完全一致）：

```
OK 全檔 2306 列；全基因組背景點 1760 個（染色體 22 條，各 80 個）；基因軌 11 筆；重組率示意取樣點 56 個
single：114 個點；指標變異在 45.235 Mb、高度 9.4；其餘點最高 8.887（低於指標變異）；超過顯著門檻 17 點；顏色等級 紅 18、橙 10、綠 12、淺藍 11、深藍 62
following：121 個點；指標變異在 45.230 Mb、高度 10.0；其餘點最高 9.477（低於指標變異）；超過顯著門檻 28 點；顏色等級 紅 24、橙 10、綠 17、淺藍 7、深藍 62
second：127 個點；指標變異在 45.190 Mb、高度 9.0；其餘點最高 8.400（低於指標變異）；超過顯著門檻 17 點；顏色等級 紅 16、橙 9、綠 11、淺藍 21、深藍 69
readcolors：117 個點；指標變異在 45.230 Mb、高度 9.0；其餘點最高 8.529（低於指標變異）；超過顯著門檻 17 點；顏色等級 紅 18、橙 7、綠 16、淺藍 10、深藍 65
second：第二個峰共 14 個點，r² 都小於 0.35（深藍 8、淺藍 6），最高 8.4，仍高於顯著門檻但低於指標變異；需條件分析確認，不能直接說獨立
readcolors：高處的深藍點 3 個（高度 7.0、7.6、8.1），其中 2 個高於顯著門檻
recomb：最高 46.48 在 45.48 Mb（示意曲線，非真實資料）
```

**以實際計數為準**（本 repo 另以獨立腳本重算，全部一致），兩點要小心讀：(1)「超過顯著門檻」的點數（17／28／17／17）**包含領先變異本身**，扣掉後是 16／27／16／16；(2) `second` 那行「第二個峰共 14 個點……仍高於顯著門檻」指的是**最高點 8.4**，14 個點中只有 3 個（7.736、7.919、8.4）高於 7.30。背景點最高 3.654，沒有任何一個超過門檻。

## P–P 自檢腳本 `sample-pp-selfcheck.py`

檢查 `sample-pp-fictional.csv`：共 1,000 列、八個 dataset 的列數；`anatomy` 第 14 個排序值的橫縱座標；`good` 的最大垂直距離小於 0.07；`heavy` 標準化前後 S 形方向相反；`loc` 全部點在對角線下方；`skew` 的 P–P 與 QQ 圖尾端對照；`two` 兩批樣本；`resid` 殘差；`sm` 擬合常態後的最大垂直距離。**需要 numpy 與 scipy**。

腳本以 `os.path.abspath(__file__)` 加明確檔名讀同資料夾的 CSV，**不搜尋檔案**，在任何資料夾執行都可以；直接在本資料夾跑：

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-pp-selfcheck.py
```

預期輸出九行（v0.3.20 上架前實跑，結束碼 0，與素材包 §11 所附輸出逐行完全一致）：

```
OK 全檔 1000 列；各資料集列數：anatomy 20、good 100、heavy 200、loc 100、skew 200、two 200、resid 80、sm 100
anatomy：n=20；第 14 個排序值 z=0.69，橫座標 Φ(z)=0.754，縱座標 (14−0.5)/20=0.675；全部點到對角線的最大垂直距離 0.102
good：n=100；樣本平均 49.4、標準差 11.1；點到對角線的最大垂直距離 0.068（小於 0.07）
heavy：n=200；標準化後，橫軸 [0.05, 0.45) 的 81 個點全在對角線下方，[0.55, 0.95) 的 66 個點全在對角線上方
heavy（不標準化）：橫軸小於 0.5 的 105 個點中有 104 個在線上方；大於 0.5 的 95 個點中有 88 個在線下方（方向與標準化後相反）
loc：n=100；樣本平均 1.45；全部 100 個點都在對角線下方；橫軸 0.5 處縱軸約 0.08（沒有通過 (0.5, 0.5)）
skew：n=200；橫軸 [0.3, 0.85) 的 111 個點全在對角線上方；最大垂直距離 0.171（橫軸 0.43 處）；Q–Q 圖最右邊的點：樣本標準化值 6.19，對應的理論分位數只有 2.81
two：每批 n=100；平均數 A -0.01、B 0.03；標準差 A 1.18、B 1.88；橫軸小於 0.4 的 79 個點全在線上方；橫軸大於 0.6 的 82 個點中有 81 個在線下方、1 個剛好在線上；橫軸 0.5 處縱軸約 0.52
resid：n=80；配出的直線 y=3.19+0.73x；殘差標準差 1.05；點到對角線的最大垂直距離 0.097（小於 0.1）
sm：n=100；擬合常態平均 6.29、標準差 2.95；橫軸 [0.45, 0.85) 的 40 個點全在對角線下方（縱軸小於橫軸）；最大垂直距離 0.125
```

**以實際計數為準**（本 repo 另以獨立程式重算，自算 Φ，全部一致，未發現素材包文字與 CSV 不一致），要小心讀：「全在對角線上方／下方」只計**指定橫軸區間內**的點——`heavy` 標準化後 [0.05, 0.45) 的 81 點與 [0.55, 0.95) 的 66 點，共 147 點，不是全部 200 點；`skew` 全批 127 點在線上方、73 點在線下方，「111 點全在線上方」只指橫軸 [0.3, 0.85) 區間；`two` 橫軸大於 0.6 的 82 點中有 1 點剛好在線上。`heavy` 樣本標準差約 2.46（t 分布自由度 2，變異數無限大，數值不穩定）。示範數字標「數字未核」，不是真實資料。

## 核型圖自檢腳本 `sample-karyotype-selfcheck.py`

檢查 `sample-karyotype-fictional.csv`：共 1,548 列、`row_id` 不重複、各類列數；24 條染色體的帶從 0 鋪到全長、無縫隙無重疊，每條 2 個 acen 帶且在著絲點位置相接；柄（stalk）與可變區（gvar）的位置；深淺等級計數；p 臂與 q 臂帶號方向；第 7 號與第 5 號的帶數、長度與著絲點比例；第 5 號 q21–q23 缺失／重複的區段與依比例長度；區間 A、B、C；條數 46 與 47；著絲點類型的臂比；密度格範圍；假關聯點（門檻 7.30）與假連線。**只需 Python 標準函式庫**（不需 numpy）。

腳本以 `os.path.abspath(__file__)` 的資料夾加明確檔名讀同資料夾的 CSV，**不搜尋檔案**，在任何資料夾執行都可以；直接在本資料夾跑：

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-karyotype-selfcheck.py
```

預期輸出十三行（v0.3.21 上架前實跑，結束碼 0，與素材包 §7 所附輸出逐行完全一致）：

```
OK 全檔 1548 列；各類列數：chrom 24、band 320、interval 5、density 631、assoc 560、link 8
帶：24 條染色體共 320 個帶，每條都從 0 鋪到全長；acen 帶 48 個（每條 2 個）；stalk 5 個（13、14、15、21、22 號短臂各 1 個）；gvar 6 個（上述 5 條短臂各 1 個，加 Y 染色體長臂 1 個）；gneg 69、gpos25 46、gpos50 50、gpos75 63、gpos100 33
帶號：24 條染色體的 p 臂（由頂端端粒往下）帶號由大到小、到著絲點為 p11；q 臂（由著絲點往下）由 q11 依序變大，往端粒方向帶號都是變大
第 7 號：16 個帶（p 臂 6 個含 p11，q 臂 10 個含 q11），頂端最外層 p23、底端最外層 q41；著絲點在全長 37.7% 處
第 5 號：18 個帶，長度 181.54 Mb，著絲點在全長 26.9% 處；長臂 gpos100 的帶只有 q42；長臂第一個 gneg 帶是 q22（圖例拿它當淺色帶）
缺失／重複：第 5 號 q21、q22、q23 三個帶，73.29 到 98.56 Mb，長度 25.27 Mb；缺失後該段拷貝數 1（2−1）、重複後 3（2+1）；若依比例，缺失那一條約 156.27 Mb、重複那一條約 206.81 Mb
區間：A 20–35 Mb（在第 5 號短臂，著絲點 48.8 Mb 之前）、B 100–118 Mb、C 140–165 Mb（B、C 在長臂，且 C 的終點小於全長 181.54 Mb）
條數：男性示意 22×2＋X＋Y＝46；女性示意 22×2＋XX＝46（23 對）；21 號由 2 份變 3 份，整套由 46 變 47
著絲點類型：著絲點在全長 50%、33%、13% 處時，長臂÷短臂＝1.0、2.1、7.1
密度：631 格；最小 0.05（有 6 格剛好在下限 0.05），最大 0.977（沒有任何一格達到上限 1），平均 0.497
曼哈頓：560 個點（第 6 號 31 個、第 12 號 29 個、其餘 1–22 號各 25 個，X、Y 沒有點）；高於門檻 7.30 的共 8 個，第 6 號 5 個（位置 30.6–31.2 Mb）、第 12 號 3 個（位置 61.7–62.3 Mb），其餘染色體 0 個；其餘染色體最高只有 3.283
連線 8 條，每條連到不同的兩條染色體；21 號長度約為 1 號的 18.8%、6 號約為 1 號的 68.6%
全部檢查通過
```

**以實際計數為準**（本 repo 另以獨立程式〔pandas〕重算，全部一致，未發現素材包文字與 CSV 不一致），要小心讀：(1) 這是虛構資料，染色體長度與著絲點位置是憑印象取的近似值，21、22 號著絲點位置是示意取值，帶、帶號與染色深淺全是模擬，**不能當真實數據引用**；(2) 著絲點類型的臂比 1.0、2.1、7.1 是「總長 120 單位、著絲點帶各寬 1 單位、臂長不含著絲點帶」算出來的教學示意，若直接用著絲點位置算會是 1.0、2.0、6.7，它們**不是 ISCN 的分類門檻**；(3) 教學稿與素材包說每條臂其餘的帶數是臂長 ÷ 11 Mb「取整數」，實際資料是**四捨五入**（改成無條件捨去，48 條臂中有 17 條對不上）；(4) 密度最大值 0.977，沒有任何一格達到上限 1，最小值 0.05 有 6 格剛好在下限；(5) 「曼哈頓」那行的 8 個高於門檻的點都在第 6 號與第 12 號，其餘染色體最高只有 3.283。

## 森林圖自檢腳本 `sample-forest-selfcheck.py`

檢查 `sample-forest-fictional.csv`：61 列、8 個資料集、10 個分析單位，區間欄（ci_lower、ci_upper）與固定效應權重欄（weight_fixed_pct）重算相符；S1 到 S8 各自的合併估計、Q、df、I²、DL 的 τ²、區間跨不跨 1（或 0）、亞組間檢定、權重比與漏斗圖的 ±1.96 標準誤範圍。**只需 numpy**；環境裡有 statsmodels 時多一行交叉核對（以 `method_re='dl'` 對照，並列出 S5 預設 Paule–Mandel 與 DL 的 τ²），沒有就略過。

腳本以明確檔名讀同資料夾的 CSV，**不搜尋檔案**；直接在本資料夾跑：

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-forest-selfcheck.py
```

預期輸出十一行（v0.3.22 上架前實跑，結束碼 0）。以下是**有安裝 statsmodels 0.15.0** 的輸出，與素材包 §7 所附輸出逐行完全一致：

```
[CSV] 61 列、8 個資料集、10 個分析單位；區間欄與權重欄重算相符
[S1] 合併 RR 0.81 [0.70, 0.94]；Q=4.11，df=5，I²=0.0%（原始值 -21.7% 截為 0），τ²=0.000（DL 原始值 -0.0064 截為 0）；95% 區間不跨過 1 的研究 2 項、含 1 的 4 項
[S2] 前 2 項 95% 區間不含 1、後 3 項含 1；固定效應合併 RR 0.82 [0.72, 0.93]（上限 < 1）；I²=54.9%（落在 30–60% 與 50–90% 兩個重疊區間）
[S3] RR 合併 0.92 [0.76, 1.13]（含 1）；研究 D 線性軸左 0.84、右 1.46，對數軸等長；差值合併 -1.68 [-2.67, -0.70]（上限 < 0）
[S4] (a) Q=0.36，I²=0.0%，τ²=0.000，合併 0.70；(b) Q=35.43，I²=85.9%，τ²(DL)=0.138，合併 0.63；用顯示的兩位數 RR 重算 (b) 的 Q=34.75
[S5] Q=16.05，df=6，I²=62.6%，τ²(DL)=0.060（實際 0.05965）；固定 0.75 [0.66, 0.85] 寬 0.255；隨機(DL) 0.72 [0.56, 0.92] 寬 0.495（1.94 倍）；第七項權重 2.6%→7.2%
[S6] 亞組 A 0.64 [0.51, 0.79]（I²=0.0%），亞組 B 1.00 [0.83, 1.21]，全部 0.83 [0.72, 0.95]；亞組間 Q=9.68（df=1，兩種算法相同），p=0.0019→0.002
[S7] 權重 86.6／1.0／7.8／3.0／1.5（%）；最大權重研究 RR 0.96，RR 最小研究 0.35（區間 [0.12, 1.03] 含 1），權重比 84.0 倍；合併 0.92 [0.82, 1.02]（上限 > 1）
[S8] 10 項（種子 9）合併 0.76 [0.68, 0.84]，I²=0.0%；落在「合併估計 ±1.96×標準誤」之內的點 10／10（兩條虛線之間，含研究 1 本身）
[statsmodels 0.15.0] 10 個分析單位的固定效應合併值、Q、I²、τ²（method_re="dl"，DL 原始值不截斷）與本程式相符；S5 的 τ²：DL=0.05965，預設 Paule–Mandel=0.03435（不同方法，不要混用）
全部 assert 通過
```

**沒有安裝 statsmodels** 時，倒數第二行改為「[statsmodels] 未安裝，略過交叉核對（只做 numpy 重算）」，其餘十行完全相同（已用不含 statsmodels 的 Python 與 numpy 2.2.4 實測，結束碼 0）。

**以實際計數為準**（本 repo 另以獨立程式〔pandas、scipy，不用腳本的函式〕重算合併估計、Q、I²、DL 與 Paule–Mandel 的 τ²、亞組間 Q，全部一致，未發現素材包文字與 CSV 不一致），要小心讀：(1) 這是虛構資料，**數字未核，不能當真實數據引用**；(2) S4 高異質性組的 Q 是 35.43，若直接用圖上顯示的兩位數風險比重算則約 34.75，不是錯誤，是四捨五入；(3) S5 的 τ² 在 DL 是 0.05965、在 statsmodels 預設的 Paule–Mandel 是 0.03435，隨機效應合併 RR 前者 0.7189 [0.561, 0.921]、後者 0.7226 [0.585, 0.892]，兩者要分開寫；(4) S2 的 I²＝54.9% 同時落在 Cochrane 30–60% 與 50–90% 兩個重疊區間，不要硬分類；(5) S1、S4 低異質性組與 S8 的 DL τ² 原始值是負的（例如 S1 為 −0.0064），表示 Q 小於自由度，τ² 與 I² 取 0，而 statsmodels 的 DL **不截為 0**；(6) 腳本裡的 S8 漏斗圖範圍是「合併估計 ± 1.96 × 標準誤」，10 個點全在其內，10 項只是剛好達到 Cochrane 建議的下限，不足以判斷發表偏差。

## 地平線圖自檢腳本 `sample-horizon-selfcheck.py`

檢查 `sample-horizon-fictional.csv`：288 筆（12 台 × 第 0 到 23 小時）、欄位順序、每列 `data_status` 都是「虛構資料，數字未核」、每台都有 24 個時間點；基準 50 之上／之下／剛好等於的筆數與比例；外層帶（與基準相差超過 25，也就是大於 75 或小於 25）的筆數與位置；第 14 小時 3 台同步、其餘小時最多 1 台；2 帶切帶疊回的高度與矮條高度＝全距的 1/4；各列各自縮放時第 14 小時變成 5 台的對照。**只需 Python 標準函式庫**。

腳本以 `Path(__file__)` 的資料夾加明確檔名讀同資料夾的 CSV，**不搜尋檔案**；直接在本資料夾跑：

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-horizon-selfcheck.py
```

預期輸出一行（v0.3.23 上架前實跑，結束碼 0）：

```
全部檢查通過：288 筆、12 台、第 0 到 23 小時；外層帶 5 筆；第 14 小時 3 台同步；共用量尺 3 台 vs 各自縮放 5 台。
```

**以實際計數為準**（本 repo 另以獨立程式〔pandas，不用腳本的函式〕重算，全部一致，未發現素材包文字與 CSV 不一致），要小心讀：(1) 這是虛構資料，**數字未核，不能當真實數據引用**；(2) 高於 50 的有 **102** 筆（35.4%）、低於 50 的 185 筆（64.2%）、剛好等於 50 的 1 筆（0.3%，machine_07 第 3 小時）；(3) 外層帶合計 **5** 筆（約 1.7%）：第 14 小時 machine_03（92.1）、machine_06（100.0）、machine_09（89.6），以及 machine_11 第 3、4 小時（0.0、5.0）；(4) 第 14 小時進入外層帶的是 **3 台**，各自縮放時變成 5 台，多出來的 machine_07（59.4）與 machine_12（58.0）只比基準高約 9.4 與 8.0 個百分點，這是「跨列比較但尺度不同」的示範；(5) 數值範圍剛好是 0.0 到 100.0（百分比的上下限），machine_06 有一筆 100.0、machine_11 有一筆 0.0；(6) 模擬圖用的波形是 `draw_horizon.py` 內產生的，不是這份 CSV，兩者不能互相驗證。

## 柏拉圖自檢腳本 `sample-pareto-selfcheck.py`

檢查 `sample-pareto-fictional.csv`：8 列、欄位順序（category, count, data_status）、每列 `data_status` 都是「虛構資料，數字未核」、類別不重複、件數合計 340、第 1 到第 7 列由大到小且「其他」固定在最後、累計百分比最後等於 100%、第一次到達 80% 的是第幾項、8 個累計點中高於／低於／剛好等於 80% 的個數、單項占比超過 20% 的項數，以及最小 3 項合計占比。**只需 Python 標準函式庫**。

腳本以 `Path(__file__)` 的資料夾加明確檔名讀同資料夾的 CSV，**不搜尋檔案**，與其他 `*-fictional.csv` 檔名不重複；直接在本資料夾跑：

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-pareto-selfcheck.py
```

預期輸出一行（v0.3.24 上架前實跑，結束碼 0）：

```
全部檢查通過：8 列、合計 340、第 4 項首次達 80%、8 個累計點中 5 個高於 80% 且 3 個低於 80%。
```

**以實際計數為準**（本 repo 另以獨立程式〔pandas，不用腳本的函式〕重算，全部一致，未發現素材包文字與 CSV 不一致），要小心讀：(1) 這是虛構資料，**數字未核，不能當真實數據引用**；(2) 累計件數 118／204／256／287／309／323／332／340，累計百分比 34.7%／60.0%／75.3%／84.4%／90.9%／95.0%／97.6%／100.0%；(3) 第一次到達 80% 的是第 **4** 項（含越過 80% 的那一項本身），前 3 項只有 75.3%；8 個累計點中高於 80% 的 **5** 個（第 4 到第 8 項）、低於 80% 的 **3** 個（第 1 到第 3 項）、剛好等於 80% 的 0 個，不能說「全部累計點都高於 80%」；(4) 單項占比超過 20% 的只有 **2** 項（34.7%、25.3%），第 3 項是 15.3%；(5) 最小的 3 項（14、9、8 件）合計 31 件，**9.1%**；最小的 4 項 15.6%、最大的 4 項 84.4%，相加 100.0%；(6) 「其他」（8 件）剛好也是最小的一項，所以這份資料**看不出**「其他比別的類別大仍放最右」，那種情況要看模擬圖 S3 的另一份虛構資料；(7) 加權版（虛構單件損失）合計 29,910 元，依損失排序前 3 項（尺寸超差、數量短少、受潮）累計 80.2%，外觀刮傷降到第 4（7.9%）；(8) 模擬圖用的數字是素材包 `draw_pareto.py` 內寫死的，與這份 CSV 的 8 類件數相同，但 S3、S5 等圖用的是另外的虛構資料，不能用這份 CSV 驗證。

## 管制圖資料與自檢腳本 `sample-s1-…` 到 `sample-s8-…`

**收錄哪些：** 素材包 `2026-10-04-am-control` 有 8 份虛構資料（S1–S8，各對應一張模擬圖）和 8 支自檢腳本，一一對應；素材包沒有指定哪一份給 repo，也沒有合併版樣本，所以 **8 組全部收錄**（共 16 個檔，與素材包逐位元相同）。素材包的 `draw_control.py`（畫 8 張模擬圖）與 `export_samples.py`（匯出這 8 個 CSV）**沒有收**。

**檔名提醒：** 檔名是 `sample-s1-anatomy.csv` 這種，**沒有 `fictional`，也沒有 `control` 字樣**，與其他圖種的 `*-fictional.csv`、`sample-*.csv` 不重複；讀取請用**明確檔名**，不要用 `sample-*.csv` 之類的萬用字元（本資料夾還有其他圖種的 `sample-*.csv`，欄位不同）。每個 CSV 第 1 行是 `#` 開頭的說明行（pandas 用 `comment='#'`；自檢腳本會略過 `#` 行），第 2 行是欄位名。

**自檢腳本做什麼：** 每支都以 `Path(__file__)` 的資料夾加明確檔名讀同資料夾的 CSV（也可在命令列最後接另一個 CSV 檔名），只用 Python 標準函式庫，全部用 `assert`；註解寫明每個百分比、點數、「全部／高於／低於」適用的區間（第幾組到第幾組）；取整是四捨五入（逢 5 進位），不是 Python 內建 `round` 的銀行家捨入。

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-s1-anatomy-selfcheck.py
python3 sample-s3-run-same-side-selfcheck.py   # 其餘同理，共 8 支
```

預期每支輸出一行（v0.3.25 上架前實跑，結束碼 0），例如：

```
OK： sample-s3-run-same-side.csv 全部檢查通過（虛構資料，數字未核）
```

**以實際計數為準**（本 repo 另以獨立程式〔pandas／numpy，不用腳本的函式〕重算，全部一致，未發現素材包文字與 CSV 不一致），要小心讀：(1) 這是虛構資料，**數字未核，不能當真實數據引用**；(2) **界限都是預先設定的，不是由資料算出的**（S1 設 σ＝2、點的標準差約 1.1；S6 用 24 點自估界限約 44.9–55.0；S5 的 R 圖下界 0.15 只是示意，真實 D3＝0）；(3) **S3 是審稿重畫的新版**：第 1–9 組連續 9 點都在中心線上方、第 10 組（19.8）回到下方，Western Electric 的「連續 8 點」規則在第 8 組命中、Nelson 的「連續 9 點」規則在第 9 組命中；全部 18 點中高於中心線 12、低於 5、剛好等於 1（第 15 組＝20.0），所以「高於／低於」的計數要看第 1–9 組，不是全體；(4) S2 右欄只有第 15 組（110.8）超出上界 109；S7 只有第 17 組（57.5）超出管制上界 56、仍在規格上限 60 之內；S8 改善前第 6 組（18.2）超出上界 17.4，改善後沒有點超界；(5) S4 第 1–12 組嚴格遞增（38.1 到 43.2）、都沒超過上界，6 點遞增規則在第 6 組起命中；用「σ＝(UCL−CL)/3」重算，S4 的第 13 組還命中 Western Electric「連續 8 點同側」，S1、S3 第 15–18 組與 S5 的 X̄ 圖第 15、16 組命中 Nelson「連續 15 點在 1σ 以內」（預先設定的 σ 比點的實際離散大），這些素材包沒寫；(6) 模擬圖的數字就是這些 CSV（`export_samples.py` 從畫圖資料匯出），重跑 `draw_control.py` 的 8 張圖與素材包 `images/` MD5 一致。

## 洛倫茲曲線資料與自檢腳本 `sample-lorenz-s1-…` 到 `sample-lorenz-s8-…`

**收錄哪些：** 素材包 `2026-10-04-pm-lorenz` 有 8 份虛構資料（S1–S8，各對應一張模擬圖）和 8 支自檢腳本，一一對應；素材包沒有指定哪一份給 repo，也沒有合併版樣本，所以 **8 組全部收錄**（共 16 個檔）。素材包的 `draw_lorenz.py`（畫 8 張模擬圖）與 `export_samples.py`（匯出這 8 個 CSV）**沒有收**。

**檔名衝突與改名（重要）：** 素材包的原名是 `sample-s1-anatomy.csv`、`sample-s1-anatomy-selfcheck.py` 這類。其中 **s1 的兩個檔與管制圖現有檔案完全同名**（管制圖的 s2–s8 名稱雖不同，但同樣以 `sample-sN-` 開頭）。所以**洛倫茲曲線 8 組全部加 `lorenz-` 前綴**（只改檔名，不改內容），對照表：

| 素材包原名（CSV 與 `-selfcheck.py` 同） | 本 repo 檔名 |
|---|---|
| `sample-s1-anatomy` | `sample-lorenz-s1-anatomy` |
| `sample-s2-equal-vs-unequal` | `sample-lorenz-s2-equal-vs-unequal` |
| `sample-s3-gini-area` | `sample-lorenz-s3-gini-area` |
| `sample-s4-steps` | `sample-lorenz-s4-steps` |
| `sample-s5-extremes` | `sample-lorenz-s5-extremes` |
| `sample-s6-misread-pareto` | `sample-lorenz-s6-misread-pareto` |
| `sample-s7-same-shape` | `sample-lorenz-s7-same-shape` |
| `sample-s8-two-groups` | `sample-lorenz-s8-two-groups` |

自檢腳本內讀取的 CSV 檔名（`CSV_NAME`、說明文字與用法裡的檔名，每支 3 處）同步改成新名字，其餘一字未改。**可驗證：** 8 個 CSV 與素材包 `cmp` 逐位元相同；8 支自檢把 `sample-lorenz-` 還原成 `sample-` 後與素材包的檔案 `cmp` 逐位元相同。請用明確檔名，不要用 `sample-s?-*` 或 `sample-*.csv` 之類的萬用字元（會同時撈到管制圖與其他圖種的檔案）。每個 CSV 第 1 行是 `#` 開頭的說明行（pandas 用 `comment='#'`；自檢腳本會略過 `#` 行），第 2 行是欄位名 `group, label, rank, value, cum_units, cum_value_share, data_status`（素材包 SKILL-PACK 第 12 節把欄位列成六個，漏了 `data_status`，實際 CSV 是七欄）。

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-lorenz-s3-gini-area-selfcheck.py
python3 sample-lorenz-s7-same-shape-selfcheck.py   # 其餘同理，共 8 支
```

預期每支輸出一行（v0.3.26 上架前實跑，結束碼 0），例如：

```
OK： sample-lorenz-s7-same-shape.csv 全部檢查通過（虛構資料，數字未核）
```

**以實際計數為準**（本 repo 另以獨立程式〔pandas／numpy，不用腳本的函式〕重算累計份額與基尼係數，全部一致，未發現素材包文字與 CSV 不一致），要小心讀：(1) 這是虛構資料，**數字未核，不能當真實數據引用**；(2) **基尼係數一定要註明算法**：折線下面積法 S3 是 0.382，乘 n／(n−1)＝10／9 的小樣本修正後 0.424；一人全拿（S5）10 戶是 0.90，不是 1，修正後 1.0；(3) S1 的折線下面積法基尼是 0.420（修正後 0.467，素材包沒寫，別與 S3 修正後的 0.42 混淆）；(4) S2 的 more_equal 組合計 105，累計欄以合計為 100% 計算；(5) S4 的 step1_unsorted 組累計欄是空的（未排序，設計如此）；(6) S6 柏拉圖累計 40、65、80、92、100 與洛倫茲累計 8、20、35、60、100，柏拉圖第 k 點＝1−洛倫茲在 1−k／5 處，五點全成立；(7) **S7 兩組基尼都是 0.340，但曲線在 70%（前 7 戶）處相交、都累計 45%，之前（10%–60%）乙較高、之後（80%、90%）甲較高**，素材包圖面寫「約 50%～80% 之間」交叉，兩者並陳；(8) S8 甲在累計 10%–90% 每個位置都高於乙；(9) 模擬圖的數字就是這些 CSV（`export_samples.py` 從畫圖資料匯出），重跑 `draw_lorenz.py` 的 8 張圖與素材包 `images/` MD5 一致。

## 馬雷圖資料與自檢腳本 `sample-marey-s1-…` 到 `sample-marey-s8-…`

**收錄哪些：** 素材包 `2026-10-05-am-marey` 有 8 份虛構資料（S1–S8，各對應一張模擬圖）和 8 支自檢腳本，一一對應；素材包沒有指定哪一份給 repo，也沒有合併版樣本，所以 **8 組全部收錄**（共 16 個檔）。素材包的 `draw_marey.py`（畫 8 張模擬圖）與 `export_samples.py`（匯出這 8 個 CSV）**沒有收**。

**檔名：** 素材包檔名本來就有 `marey` 前綴，與本 repo `examples/data/` 既有檔案**沒有撞名**，所以**沒有改名、內容一字未改**（16 個檔與素材包 `cmp` 逐位元相同）。每支自檢以明確檔名讀 CSV（腳本內 `CSV_NAME` 加上腳本所在資料夾），沒有萬用字元；可選用命令列參數指定別的 CSV 路徑。

**CSV 格式：** 第 1 行是 `#` 開頭的說明行（虛構資料，數字未核；指向哪一張圖）；之後是表頭。S1–S6 與 S8 是站點長表，共 10 欄：`group, train, seq, station, km, arrive, depart, arrive_min, depart_min, data_status`（每班車每站一列；`arrive_min`／`depart_min` 是從某個基準時刻起算的分鐘數）。S7 每班車一列，共 9 欄：`group, train, direction, kind, stops, first_depart_min, last_arrive_min, in_zoom, data_status`。讀入時要跳過 `#` 行（例如 pandas 的 `comment='#'`）。

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-marey-s3-single-track-meet-selfcheck.py
python3 sample-marey-s7-too-dense-zoom-selfcheck.py   # 其餘同理，共 8 支
```

預期每支輸出一行（v0.3.27 上架前實跑，結束碼 0），例如：

```
OK： sample-marey-s3-single-track-meet.csv 全部檢查通過（虛構資料，數字未核）；會車 08:27 – 08:28 在戊站 ；若不等 08:23:30 20.5 公里 丁站與戊站之間
```

自檢腳本用精確分數（`Fraction`）計算，且我另以獨立程式（pandas／numpy／fractions，不用腳本的函式）重算，**全部一致，沒有發現素材包文字與 CSV 不一致**。要小心讀：(1) 這是虛構資料，**數字未核，不能當真實時刻表引用**；(2) S1 只交叉一次：06:24:30、21.5 公里；S8 只交叉一次：10:13:30、11.5 公里；兩者圖說寫「約」，而「約」值就等於精確值；(3) S2 只在 07:24:00 的丁站超車；301 次若不待避（201-nowait）則 07:25:00、22 公里追上，201 次在己站的差距是 9.5 分鐘（07:31:30 對 07:41:00）；(4) S3 的 401 次與 402 次只在戊站（08:27–08:28）重合，402 次若不等（402-nowait）就在 08:23:30、離起點 20.5 公里處交叉，落在丁站與戊站之間＝單線上的衝突；(5) S4 的七分鐘誤點：到站晚 1、2、7、7、7 分鐘，離站晚（甲到戊）0、2、4、7、7 分鐘，組成是乙站停站 +1、丙站停站 +2、甲→乙行駛 +1、丙→丁行駛 +3，合計 7，其中丙站停站加丙→丁行駛共 5 分鐘＝5／7＝71.4%；(6) **S5 的「間隔」有兩個不同的量**：圖上的 headway 是相鄰兩輛公車的到站時刻差，3→4 號車依序為 5、4.5、3.95、3.37、2.77、2.15、1.5、0.81、0.2、0.2、0.2、0.2、0.2 分鐘（第 7 站首次小於 1 分鐘，最後五站是模型規定的 0.2，不是觀測）；程式停站模型的 g 是「本車到站時刻減前車離站時刻」，兩者不同（3→4 號車 g 在第 0 站是 4.17，第 7 站起為負，停站取 0.3 分鐘下限）；4→5 號車的 headway 從 8.0 分鐘先增到最大 11.18（第 8 站）再回到 9.76，所以圖說「拉大到 9.8」只是起點對終點的比較，不是一路拉大；(7) S6 各段是 2、2、14、2、10 公里，每段時速都是 60 公里，等距排列時視覺斜率是 1／2、1／2、1／14、1／2、1／10，最平的是丙→丁；(8) S7 共 284 班＝普通 218（下行 109、上行 109）＋快車 66（33、33），放大區（07:00–09:00 下行）16 班＝普通 12＋快車 4，占 16／284＝5.6%，同時在線最多 10 班。

## 存活曲線資料與自檢腳本 `sample-km-s1-…` 到 `sample-km-s8-…`

**收錄哪些：** 素材包 `2026-10-05-pm-km` 有 8 份虛構資料（S1–S8）和 8 支自檢腳本；素材包沒有指定哪一份給 repo，所以 **8 組全部收錄**（共 16 個檔）。素材包的 `draw_km.py` 與 `export_samples.py` **沒有收**。

**檔名：** 素材包檔名本來就有 `km` 前綴，與本 repo `examples/data/` 既有檔案**沒有撞名**，所以**沒有改名、內容一字未改**（16 個檔與素材包 `cmp` 逐位元相同）。每支自檢以明確檔名讀 CSV（`CSV_NAME`＋腳本所在資料夾），沒有萬用字元；取整一律四捨五入（逢 5 進位）。

**CSV 格式：** 第 1 行是 `#` 開頭的說明行；之後是表頭。S1–S7 共 5 欄：`subject, time, event, group, data_status`。S8 共 6 欄：`subject, name, time, event, group, data_status`。`event`＝1 事件、0 設限。讀入時跳過 `#` 行。

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-km-s3-censoring-selfcheck.py
python3 sample-km-s6-crossing-selfcheck.py   # 其餘同理，共 8 支
```

預期每支輸出一行 `PASS sample-km-sN-…-selfcheck`（v0.3.28 上架前實跑，結束碼 0）。

**以實際計數為準**（本 repo 另以獨立程式重算，與 selfcheck 精確值一致，未發現素材包文字與 CSV 不一致）：(1) 虛構資料，**數字未核**；(2) 圖說「約」對應精確值見素材包第 12 節（S3 的 0.64＝0.637、S2 的 0.022＝0.0223、S6 交叉＝20.0、S7 的 0.092＝0.0917）；(3) S5 風險人數少於 5 的起點是以 0.1 月步進掃描得到的 22.2 月；(4) S6 交叉後必須看分段風險比；(5) 教科書 aml 例子（非本 CSV）中位 27 週、組別 31 對 23、對數等級 P≈0.065，已用公開資料與 lifelines 重算一致。

## 游泳圖資料與自檢腳本 `sample-swimmer-s1-…` 到 `sample-swimmer-s8-…`

**收錄哪些：** 素材包 `2026-10-06-am-swimmer` 有 8 份虛構資料（S1–S8，種子 20261026）和 8 支自檢腳本；素材包沒有指定哪一份給 repo，所以 **8 組全部收錄**（共 16 個檔）。素材包的 `draw_swimmer.py` 與 `export_samples.py` **沒有收**。

**檔名：** 素材包檔名本來就有 `swimmer` 前綴，與本 repo `examples/data/` 既有檔案**沒有撞名**，所以**沒有改名、內容一字未改**（16 個檔與素材包 `cmp` 逐位元相同）。每支自檢以明確檔名讀 CSV（`CSV_NAME`＋腳本所在資料夾，也可在命令列給檔名），沒有萬用字元；只用 Python 標準函式庫，S3 有 scipy 時另以 `spearmanr` 交叉核對、沒有就略過。

**CSV 格式：** 第 1 行是 `#` 開頭的說明行；之後是表頭，最後一欄都是 `data_status`。時間單位都是「月」。

| 檔 | 列數 | 欄位 |
|---|---|---|
| S1 | 20 | `subject, group, enroll_month, treatment_months, stop_reason, ongoing, first_response_month, cr_month, progression_month, data_status` |
| S2 | 20 | `subject, group, treatment_months, stop_reason, responder, ongoing, data_status` |
| S3 | 20 | `subject, enroll_month, treatment_months, row_if_sorted_by_duration, row_if_sorted_by_id, data_status` |
| S4 | 20（有緩解 9） | `subject, group, treatment_months, stop_reason, dor_start_month, dor_end_month, dor_months, dor_status, data_status` |
| S5 | 20 | `subject, group, treatment_months, stop_reason, data_status` |
| S6 | 20 | `subject, enroll_month, months_at_cutoff_12, status_at_cutoff_12, months_at_cutoff_24, status_at_cutoff_24, data_status` |
| S7 | 150 | `subject, group, treatment_months, stop_reason, event, data_status` |
| S8 | 6 | `subject, group, start_month, end_month, first_response_month, cr_month, stop_reason, ongoing, data_status` |

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-swimmer-s3-sorting-selfcheck.py
python3 sample-swimmer-s6-cutoff-misread-selfcheck.py   # 其餘同理，共 8 支
```

預期每支輸出一行 `PASS sample-swimmer-sN-…-selfcheck`（S3 另先印 `Spearman（平均名次）= -0.3185`；v0.3.29 上架前實跑，結束碼 0）。

**以實際計數為準**（本 repo 另以 pandas／numpy／scipy／lifelines 獨立重算，與 selfcheck 一致，未發現素材包文字與 CSV 不一致）：(1) 虛構資料，**數字未核**，不代表任何真實藥物或病人；(2) S1 第一次緩解第 2 月 5 人（P01、P04、P08、P10、P13）、第 4 月 3 人、第 6 月 1 人（每 2 個月評估一次）；(3) S3 排序與入組月的秩相關＝**−0.32**（scipy `spearmanr` 與 pandas `rank(method='average')` 皆 −0.3185；同分 4 個 2.0、3 個 6.0、2 個 14.0 月）——同分必須取平均名次；(4) S4 設限 4 人：P13 12.2、P04 10.5（副作用停藥）、P14 10.0、P16 9.3；(5) S6 第 12 月截止時 P13、P14、P16 棒短是因為晚入組，到第 24 月分別 14.2、14.0、13.3 月仍在治療；(6) S7 KM 第 6／12／18 月 0.433／0.202／0.061、風險人數每 6 月 150、79、28、7、0；(7) S8 用修正版圖（取最早入組 6 人）。

## 千層麵圖資料與自檢腳本 `sample-lasagna-s1-…` 到 `sample-lasagna-s8-…`

**收錄哪些：** 素材包 `2026-10-06-pm-lasagna` 有 8 份虛構資料（S1–S8，種子 20261006）和 8 支自檢腳本；素材包沒有指定哪一份給 repo，所以 **8 組全部收錄**（共 16 個檔）。素材包的 `draw_lasagna.py` 與 `export_samples.py` **沒有收**。

**檔名：** 素材包檔名本來就有 `lasagna` 前綴，與本 repo `examples/data/` 既有檔案**沒有撞名**，所以**沒有改名、內容一字未改**（16 個檔與素材包 `cmp` 逐位元相同）。每支自檢以明確檔名讀 CSV（`read_rows("sample-lasagna-sN-….csv")`，從腳本所在資料夾讀），沒有萬用字元；只用 Python 標準函式庫，以分數精確計算平均、逢 5 進位到小數一位。

**CSV 格式：** 第 1 行是 `#` 開頭的說明行；之後是表頭，最後一欄都是 `data_status`（「虛構資料，數字未核」）。收縮壓單位毫米汞柱，空白＝缺值。

| 檔 | 列數 | 欄位 |
|---|---|---|
| S1 | 480 | `subject, group, week, sbp, missing_type, highlight, data_status` |
| S2 | 40 | `subject, group, w1…w12, n_observed, person_mean, row_in_lasagna, data_status` |
| S3 | 40 | `subject, group, w1…w12, person_mean, row_A_by_id, row_B_by_mean, row_C_group_then_mean, data_status` |
| S4 | 40 | `subject, group, sbp_w1…sbp_w12, cat_w1…cat_w12, row_in_plot, data_status` |
| S5 | 480 | `subject, group, week, sbp, sbp_if_zero_filled, is_missing, data_status` |
| S6 | 40 | `row_in_plot, subject, group, w1…w12, person_mean, data_status` |
| S7 | 480 | `subject, group, row_in_group_panel, week, sbp, data_status` |
| S8 | 16 | `subject, group, week, sbp, data_status` |

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-lasagna-s5-missing-selfcheck.py
python3 sample-lasagna-s7-groups-mean-selfcheck.py   # 其餘同理，共 8 支
```

預期每支逐項印出 `PASS｜…`，最後一行 `RESULT: PASS（N 項通過、0 項失敗）`（v0.3.30 上架前實跑，結束碼 0）。

**以實際計數為準**（本 repo 另以 pandas／numpy＋分數精確平均獨立重算，與 selfcheck 一致，未發現素材包文字與 CSV 不一致）：(1) 虛構資料，**數字未核**；(2) S7 對照組第 1 週精確值 148.35（2967／20），逢 5 進位＝**148.4**、到第 12 週 150.2 變化 **＋1.8**；S7 圖上標籤顯示 148.3 是另一種進位方式，圖沒有重畫，以 148.4 為準；(3) S5 有三個每週平均落在進位邊界：第 5 週 145.95 → 146.0（無缺值，正確與補 0 相同）、補 0 第 4 週 138.95 → 139.0、補 0 第 10 週 127.25 → 127.3——課程文字與圖都沒有用到這三個值；(4) S4 的四級分法是教學簡化，不是臨床標準；(5) 中途退出：P12 第 8 週起、P15 第 7 週起（對照組），P32 第 7 週起、P34 第 9 週起（介入組）。

## 遞迴圖資料與自檢腳本 `sample-recurrence-s1-…` 到 `sample-recurrence-s8-…`

**收錄哪些：** 素材包 `2026-10-07-am-recurrence` 有 8 份虛構資料（S1–S8，種子 20261007）和 8 支自檢腳本；素材包沒有指定哪一份給 repo，所以 **8 組全部收錄**（共 16 個檔）。素材包的 `draw_recurrence.py` 與 `export_samples.py` **沒有收**。

**檔名：** 素材包檔名本來就有 `recurrence` 前綴，與本 repo `examples/data/` 既有檔案**沒有撞名**，所以**沒有改名、內容一字未改**（16 個檔與素材包 `cmp` 逐位元相同）。每支自檢以明確檔名讀 CSV（`read_rows("sample-recurrence-sN-….csv")`，從腳本所在資料夾讀），沒有萬用字元；只用 Python 標準函式庫。

**CSV 格式：** 第 1 行是 `#` 開頭的說明行；之後是表頭，最後一欄都是 `data_status`。距離為歐氏距離（維度 1 時＝差的絕對值）；遞迴＝距離 ≤ ε；遞迴率＝黑格數 ÷ 全部格數（含主對角線），百分比四捨五入到小數一位。

| 檔 | 列數 | 欄位 |
|---|---|---|
| S1 | 300 | `t, z_value, data_status`（t＝0–299） |
| S2 | 1200 | `panel, t, z_value, data_status` |
| S3 | 300 | `t, z_value, data_status` |
| S4 | 300 | `t, z_value, data_status` |
| S5 | 300 | `t, z_value, data_status` |
| S6 | 300 | `t, z_normal, z_stuck, in_stuck_window, data_status` |
| S7 | 300 | `t, series_a, series_b, data_status` |
| S8 | 8 | `point, raw, z, state_dim1, state_dim2, data_status` |

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-recurrence-s3-threshold-selfcheck.py
python3 sample-recurrence-s7-cross-recurrence-selfcheck.py   # 其餘同理，共 8 支
```

預期每支逐項印出 `PASS｜…`，最後一行 `RESULT: PASS（N 項通過、0 項失敗）`（v0.3.31 上架前實跑，結束碼 0）。

**以實際計數為準**（本 repo 另以 pandas／numpy 獨立重算，與 selfcheck 一致，未發現素材包文字與 CSV 不一致）：(1) 虛構資料，**數字未核**；(2) S1 第 70／119 點（0-based index）四捨五入到小數兩位為 0.45／0.62，距離 0.17 ≤ ε＝0.3；(3) S2 隨機漫步決定性 79.3% > 白雜訊 25.2%——決定性高不是規律的充分條件；(4) S3 同一序列三個門檻遞迴率 3.4%／18.8%／65.7%；(5) S5 斜線高峰落在 50／100／150（週期 50 的倍數）；(6) S7 真實時間差 10 點，錯開 10 的對角線黑格比例 85.5%、錯開 0 只有 11.0%；(7) S8 平均 13.50、母體標準差 1.50，m＝2、τ＝1、ε＝0.5 時 7 狀態、13／49＝26.5%。

## 頻譜圖資料與自檢腳本 `sample-spectrogram-s1-…` 到 `sample-spectrogram-s8-…`

**收錄哪些：** 素材包 `2026-10-08-am-spectrogram` 有 8 份虛構時間域訊號（S1–S8，各對應一張模擬圖）和 8 支自檢腳本；素材包沒有指定哪一份給 repo，所以 **8 組全部收錄**（共 16 個檔）。素材包的 `draw_spectrogram.py`（畫模擬圖）與 `export_samples.py`（匯出 CSV）**沒有收**。

**檔名：** 素材包檔名本來就有 `spectrogram` 前綴，與本 repo `examples/data/` 既有檔案**沒有撞名**，所以**沒有改名**。S1–S7 是縮小版，**不是**與素材包逐位元相同；**S8 與素材包逐位元相同**（`cmp` 核過）。每支自檢以明確檔名讀 CSV（`read_cols("sample-spectrogram-sN-….csv")`，從腳本所在資料夾讀），沒有萬用字元；只用 Python 標準函式庫（自寫週期型漢寧窗與基數 2 的快速傅立葉轉換，不靠 numpy）。

**縮小方式：** 素材包 8 個 CSV 合計 12,452,663 位元組（約 12.5 MB；S6 單獨 5,916,292 位元組，約 5.9 MB）。本 repo 的 8 個 CSV 合計 **1,167,877 位元組（約 1140.5 KiB）**，單檔最大是 S6 的 217,651 位元組（約 212.5 KiB，不到 220 KB）。帶限重取樣＝整段做快速傅立葉轉換、丟掉新奈奎斯特頻率以上的成分、再反轉換（等於理想低通），然後每隔若干點留一點。截取的檔保留原取樣點編號。

| 檔 | 列數 | CSV 位元組 | 縮小方式與設定 |
|---|---:|---:|---|
| S1 `sample-spectrogram-s1-anatomy.csv` | 8000 | 114864 | 帶限重取樣 8000→4000 赫茲（每 2 點留 1 點，整段）。窗 256 點（仍是 64 毫秒）、移動 64 點（16 毫秒）。窗數仍 122、頻率格間隔仍 15.625 赫茲；頻率格 257→129。欄位 `sample,x` |
| S2 `sample-spectrogram-s2-four-patterns.csv` | 3200 | 145960 | 取樣率仍 8000 赫茲，截取第 6400–9599 點（0.8–1.2 秒）。窗數 47（全長是 247）。欄位 `sample,pure_1000hz,chirp_200_3000hz,click_1s,harmonics_300hz` |
| S3 `sample-spectrogram-s3-window-tradeoff.csv` | 11264 | 164854 | 取樣率仍 8000 赫茲，截取第 0–11263 點（0–1.408 秒）。窗長 64／512／4096 點的窗數是 701／85／8。凹陷算法用到的窗都還在，所以凹陷分貝與全長相同。欄位 `sample,x` |
| S4 `sample-spectrogram-s4-linear-vs-db.csv` | 8192 | 123619 | 取樣率仍 8000 赫茲，截取第 4096–12287 點（0.512–1.536 秒）。窗數 61。欄位 `sample,x` |
| S5 `sample-spectrogram-s5-linear-vs-mel.csv` | 12800 | 204142 | 取樣率**維持 16000 赫茲**（12.5%＝1000 ÷ 8000 靠它），截取第 16000–28799 點（1.0–1.8 秒）。窗數 97。全長的「開頭基頻約 150 赫茲」在這段變成「截取起點約 200 赫茲（150 ＋ 100 × 1.0 ÷ 2）；300 赫茲以下最亮格是 187.5 赫茲」。欄位 `sample,x` |
| S6 `sample-spectrogram-s6-motor-fault.csv` | 15000 | 217651 | 帶限重取樣 2000→250 赫茲（先去掉 125 赫茲以上，每 8 點留 1 點）。窗 256 點（仍是 1.024 秒）、移動 128 點。窗數仍 116、頻率格間隔仍約 0.977 赫茲；頻率格 1025→129。欄位 `sample,x` |
| S7 `sample-spectrogram-s7-spectrum-vs-spectrogram.csv` | 8000 | 193794 | 帶限重取樣 8000→4000 赫茲。窗 256 點、移動 64 點，窗數 122。欄位 `sample,signal_a,signal_b` |
| S8 `sample-spectrogram-s8-steps.csv` | 64 | 2993 | **與素材包逐位元相同**，沒有再縮小。欄位 `sample,x,data_status` |

自檢腳本位元組：S1 4961、S2 5570、S3 6251、S4 4902、S5 5584、S6 5358、S7 5725、S8 5420。

**CSV 格式：** 第 1 行是 `# 虛構資料，數字未核｜…`。S1–S7 **沒有**每列的 `data_status` 欄（列數上千，虛構標記放在第 1 行；跟較早的 MA 圖、LocusZoom 樣本把標記放在檔頭的做法相同）。S8 仍保留 `data_status`。縮小後的訊號值以約 6 位有效數字寫入（不補尾端的 0，所以有的格子看起來不到 6 位）；S8 是未縮小的正弦取樣，位數較多（例如 √2／2 寫成 0.707106781187）。

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-spectrogram-s1-anatomy-selfcheck.py
python3 sample-spectrogram-s6-motor-fault-selfcheck.py   # 其餘同理，共 8 支
```

預期每支逐項印出 `PASS｜…`，最後一行 `RESULT: PASS（N 項通過、0 項失敗）`（**v0.3.32 上架前實跑，結束碼 0**）。實跑通過項數：S1 10、S2 11、S3 22、S4 8、S5 11、S6 15、S7 9、S8 14。

**以實際計數為準**（自檢從縮小檔重算，課程稿的關鍵讀數不變；只有格子數，以及 S5 的開頭基頻檢查，跟全長訊號不同。沒有另外用獨立程式重算頻譜，也沒有重跑沒有收進本 repo 的 `draw_spectrogram.py`／`export_samples.py`）：(1) 虛構資料，**數字未核**；(2) S1 最亮格 437.5 赫茲，1203.125 赫茲那一格高於 −20 分貝的窗中心是 0.8–1.408 秒；(3) S2 啁啾在 1 秒最亮格 1593.75 赫茲（理論 1600），敲擊最亮窗中心 1.0 秒，諧波 10 條；(4) S3 窗 8／64／512 毫秒的凹陷是 0.0／61.6、29.0／0.0、76.4／0.0 分貝；(5) S4 −40.0 與 −60.0 分貝、線性份額 0.0001；(6) S5 自檢印 `開頭 8 窗基頻 187.5 赫茲（理論 200，差不到兩格）`，不是全長訊號的約 150 赫茲；另確認 1.2–1.6 秒、5000–7000 赫茲的嘶聲比其他時間亮 6 分貝以上（實跑差距 8.6 分貝）；1000 赫茲＝1000.0 梅爾、8000 赫茲＝2840.0 梅爾，1000 赫茲以下高度線性 12.5%、梅爾 35.2%；(7) S6 固定線 29.5／59.0／88.5／120 赫茲，新成分落在 107.422 赫茲；0–30 秒中位數 −53.0 分貝，第一個高出中位數 10 分貝的窗中心是 35.84 秒，最後一窗 −11.3 分貝；107 ÷ 29.5 ≈ 3.6，不是整數倍；(8) S7 兩條平均頻譜在 400 與 1200 赫茲相差 0.0／0.0 分貝；(9) S8 各窗最亮 125／125／125／187.5／250／250／250 赫茲，第 4 窗 −5.6／−5.5 分貝、最亮 187.5 赫茲。

## 自相關圖資料與自檢腳本 `sample-autocorr-s1-…` 到 `sample-autocorr-s8-…`

**收錄哪些：** 素材包 `2026-10-09-am-autocorr` 有 8 份虛構資料（S1–S8，各對應一張模擬圖）和 8 支自檢腳本；素材包沒有指定哪一份給 repo，所以 **8 組全部收錄**（共 16 個檔）。素材包的 `draw_autocorr.py`（畫模擬圖）與 `export_samples.py`（匯出 CSV）**沒有收**。

**檔名：** 素材包檔名本來就有 `autocorr` 前綴，與本 repo `examples/data/` 既有檔案**沒有撞名**，所以**沒有改名**。8 個 CSV **全部與素材包逐位元相同**（`cmp` 核過），沒有再縮小。每支自檢以明確檔名讀 CSV（`read_rows("sample-autocorr-sN-….csv")`，從腳本所在資料夾讀），沒有萬用字元；只用 Python 標準函式庫（自寫平均、自相關 r(k)＝C(k)/C(0)、Durbin–Levinson 偏自相關與信心半寬 1.96／√n，不靠 numpy）。素材包自檢需要 numpy，本 repo 改寫為只用標準函式庫，檢查項目、預期值、四捨五入與訊息與素材包相同。

**沒有縮小：** 8 個 CSV 合計 **178,186 位元組（約 174.0 KiB）**，單檔最大是 S4 的 53,579 位元組（約 52.3 KiB）。

| 檔 | 列數 | CSV 位元組 | 欄位 |
|---|---:|---:|---|
| S1 `sample-autocorr-s1-anatomy.csv` | 200 | 9611 | `t,x,data_status` |
| S2 `sample-autocorr-s2-three-patterns.csv` | 300 | 23143 | `t,white_noise,linear_trend,period_7,data_status` |
| S3 `sample-autocorr-s3-acf-pacf.csv` | 500 | 23690 | `t,x,data_status` |
| S4 `sample-autocorr-s4-sample-size-ci.csv` | 1050 | 53579 | `series_n,t,x,data_status` |
| S5 `sample-autocorr-s5-period-spikes.csv` | 400 | 19011 | `t,x,data_status` |
| S6 `sample-autocorr-s6-nonstationary.csv` | 300 | 18470 | `t,random_walk,diff1,data_status`（差分 299 點，t＝0 留空） |
| S7 `sample-autocorr-s7-two-correlograms.csv` | 200 | 24927 | `t,x_series,var_jia,var_yi,var_bing,var_ding,var_wu,data_status` |
| S8 `sample-autocorr-s8-steps.csv` | 120 | 5755 | `t,x,data_status` |

自檢腳本位元組：S1 3336、S2 3737、S3 3585、S4 3639、S5 3293、S6 3632、S7 4054、S8 3350。

**CSV 格式：** 第 1 行是 `# 虛構資料，數字未核｜…`。之後是表頭，最後一欄都是 `data_status`（「虛構資料，數字未核」）。t＝時間點編號。讀入時要跳過 `#` 行。

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-autocorr-s1-anatomy-selfcheck.py
python3 sample-autocorr-s6-nonstationary-selfcheck.py   # 其餘同理，共 8 支
```

預期每支逐項印出 `PASS｜…`，最後一行 `RESULT: PASS（N 項通過、0 項失敗）`（**v0.3.33 上架前實跑，結束碼 0**）。實跑通過項數：S1 9、S2 12、S3 12、S4 11、S5 9、S6 11、S7 21、S8 10。在 `examples/data/` 與暫存資料夾各跑一次都通過；與素材包 numpy 版通過項數相同。

**以實際計數為準**（自檢從 CSV 重算，與課程稿關鍵讀數一致。沒有重跑沒有收進本 repo 的 `draw_autocorr.py`／`export_samples.py`）：(1) 虛構資料，**數字未核**；(2) S1 滯後 0＝1、半寬 0.1386、滯後 1／12／24＝0.759／0.838／0.787，滯後 12 是 1–30 中最大的正尖峰；(3) S2 半寬 0.1132；白噪音滯後 1／7＝-0.072／0.037，滯後 1–40 出帶 1 根（「至多 3 根」）；趨勢滯後 1／20＝0.962／0.787，滯後 1–20 全在帶外；週期滯後 7／14＝0.869／0.842；(4) S3 半寬 0.0877；自相關滯後 1／2／5＝0.459／-0.019／-0.086；偏自相關滯後 1–4＝0.459／-0.291／-0.027／-0.046，滯後 1、2 在帶外、3、4 在帶內；(5) S4 半寬 0.2772／0.1386／0.0693，滯後 1＝0.026／0.04／-0.025；(6) S5 半寬 0.098，滯後 7／14／21／28＝0.913／0.9／0.882／0.862；(7) S6 未差分滯後 1／20／40＝0.971／0.498／-0.006，差分後滯後 1／5＝0.004／-0.014；(8) S7 滯後 10＝0.837；甲×乙≈0.794、甲×丁≈-0.481、乙×丙≈0.584；(9) S8 半寬 0.1789，滯後 1／8／16／24＝0.576／0.799／0.752／0.693，n/4＝30。

## 滯後圖資料與自檢腳本 `sample-lagplot-s1-…` 到 `sample-lagplot-s8-…`

**收錄哪些：** 素材包 `2026-10-10-am-lagplot` 有 8 份虛構資料（S1–S8，各對應一張模擬圖）和 8 支自檢腳本；素材包沒有指定哪一份給 repo，所以 **8 組全部收錄**（共 16 個檔）。素材包的 `draw_lagplot.py`（畫模擬圖）、`export_samples.py`（匯出 CSV）與 `sim_facts.json`（預期值）**沒有收**。

**檔名：** 素材包檔名本來就有 `lagplot` 前綴，與本 repo `examples/data/` 既有檔案**沒有撞名**，所以**沒有改名**。8 個 CSV **全部與素材包逐位元相同**（`cmp` 核過），沒有再縮小。每支自檢以明確檔名讀 CSV（`read_rows` 一類的讀檔，從腳本所在資料夾讀），沒有萬用字元；只用 Python 標準函式庫（自寫平均、滯後 k 的皮爾森相關與自相關，不靠 numpy）。素材包自檢需要 numpy，並從 `sim_facts.json` 讀預期值；本 repo 改寫為只用標準函式庫，**預期值寫在腳本裡**。

**沒有縮小：** 8 個 CSV 合計 **68,130 位元組（約 66.5 KiB）**，單檔最大是 S2 的 24,246 位元組（約 23.7 KiB）。

| 檔 | 列數 | CSV 位元組 | 欄位 |
|---|---:|---:|---|
| S1 `sample-lagplot-s1-anatomy.csv` | 120 | 5527 | `t,y,data_status` |
| S2 `sample-lagplot-s2-six-patterns.csv` | 200 | 24246 | `t,white_noise,ar_pos_0p9,ar_neg,period12,trend_noise,random_walk,data_status`（未標準化原值；圖上已標準化） |
| S3 `sample-lagplot-s3-lag-k-panels.csv` | 144 | 7108 | `t,month,y,data_status` |
| S4 `sample-lagplot-s4-vs-acf.csv` | 30 | 1516 | `t,y,data_status` |
| S5 `sample-lagplot-s5-nonlinear.csv` | 300 | 14134 | `t,y,data_status` |
| S6 `sample-lagplot-s6-outliers.csv` | 150 | 9035 | `t,y_with_outliers,y_without,data_status` |
| S7 `sample-lagplot-s7-scatter-lag-recurrence.csv` | 100 | 6022 | `day,temp_c,cups,data_status` |
| S8 `sample-lagplot-s8-how-to.csv` | 12 | 542 | `t,y,data_status` |

自檢腳本位元組：S1 2328、S2 2388、S3 2421、S4 2375、S5 2371、S6 1992、S7 2433、S8 2025。

**CSV 格式：** 第 1 行是 `# 虛構資料，數字未核｜…`。之後是表頭，最後一欄都是 `data_status`（「虛構資料，數字未核」）。讀入時要跳過 `#` 行。列數是資料列（`wc -l` 再扣說明行與表頭）。

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-lagplot-s1-anatomy-selfcheck.py
python3 sample-lagplot-s5-nonlinear-selfcheck.py   # 其餘同理，共 8 支
```

預期每支逐項印出 `PASS｜…`，最後一行 `RESULT: PASS（N 項通過、0 項失敗）`（**v0.3.34 上架前實跑，結束碼 0**）。實跑通過項數：S1 6、S2 9、S3 15、S4 16、S5 6、S6 5、S7 6、S8 5。

**以實際計數為準**（自檢從 CSV 重算，與課程稿關鍵讀數一致。沒有重跑沒有收進本 repo 的 `draw_lagplot.py`／`export_samples.py`，也沒有收 `sim_facts.json`）：(1) 虛構資料，**數字未核**；(2) 圖 S1 滯後 1 皮爾森約 0.722、自相關約 0.711，119 對；(3) 圖 S2 六格滯後 1 約 0.008／0.763／-0.705／0.81／0.755／0.985；其中 0.763 對模型係數 0.9 是抽樣偏差（估計偏誤下 200 點平均約 0.88，其餘為這組亂數的樣本誤差）；(4) 圖 S3 皮爾森滯後 1／2／3／6／9／12 約 0.794／0.461／-0.004／-0.929／0.002／0.928，自相關滯後 6／12 約 -0.901／0.862；(5) 圖 S4 自相關對皮爾森：滯後 1 約 0.708 對 0.729、滯後 3 約 0.329 對 0.426、滯後 6 約 0.058 對 0.149，半寬約 0.358；(6) 圖 S5 滯後 1 約 -0.138，帶約 ±0.113，滯後 1–10 有 2 根在帶外；(7) 圖 S6 含離群值約 0.464、拿掉約 0.585；(8) 圖 S7 上約 0.965、中約 0.905、下黑點約 16.4%（相差不超過 1°C；直式上／中／下）；(9) 圖 S8 11 對，滯後 1 約 0.047（正文亦寫約 0.05），模型係數 0.6。

## 季節子序列圖資料與自檢腳本 `sample-seasonal-subseries-sim-s1-…` 到 `sample-seasonal-subseries-noaa-co2-2000-2025`

**收錄哪些：** 素材包 `2026-10-11-am-seasonal-subseries` 有 8 份虛構資料（S1–S8，各對應一張模擬圖）、1 份毛納羅亞二氧化碳真實資料（圖 R15、圖 R16）和 9 支自檢腳本；素材包沒有指定哪一份給 repo，所以 **9 組全部收錄**（共 18 個檔）。素材包的 `draw_seasonal_subseries.py`（畫模擬圖）、`draw_noaa_co2.py`（重繪二氧化碳）與 `export_samples.py`（匯出 CSV）**沒有收**。

**檔名：** 素材包檔名本來就有 `seasonal-subseries` 前綴，與本 repo `examples/data/` 既有檔案**沒有撞名**，所以**沒有改名**。本課**沒有改這些檔**，也**不宣稱與素材包逐位元相同**（沒有做 `cmp`）。每支自檢以明確檔名讀 CSV（從腳本所在資料夾讀），沒有萬用字元；只用 Python 標準函式庫（`csv`、`math`、`os`、`sys`；一次與二次趨勢用自寫的最小平方，不靠 numpy）。預期值寫在腳本裡。

**沒有縮小：** 9 個 CSV 合計 **51,697 位元組（約 50.5 KiB）**。其中 8 個虛構檔合計 40,707 位元組（約 39.8 KiB），單檔最大是 S4 的 7,482 位元組（約 7.3 KiB）；真實二氧化碳檔 10,990 位元組（約 10.7 KiB）。都小於 25 萬位元組。模擬圖重畫種子 20261011。

| 檔 | 列數 | CSV 位元組 | 欄位 |
|---|---:|---:|---|
| S1 `sample-seasonal-subseries-sim-s1-anatomy.csv` | 72 | 3694 | `year,month,value,data_status` |
| S2 `sample-seasonal-subseries-sim-s2-three-views.csv` | 96 | 4881 | `year,month,value,data_status` |
| S3 `sample-seasonal-subseries-sim-s3-shifting-peak.csv` | 120 | 6065 | `year,month,value,data_status` |
| S4 `sample-seasonal-subseries-sim-s4-trend-first.csv` | 120 | 7482 | `year,month,value,detrended,data_status`（`detrended`＝扣趨勢直線） |
| S5 `sample-seasonal-subseries-sim-s5-no-season.csv` | 120 | 7401 | `year,month,noise_only,with_season,data_status` |
| S6 `sample-seasonal-subseries-sim-s6-outlier.csv` | 96 | 4883 | `year,month,value,data_status` |
| S7 `sample-seasonal-subseries-sim-s7-acf-lag-subseries.csv` | 120 | 5693 | `year,month,value,data_status` |
| S8 `sample-seasonal-subseries-sim-s8-how-to.csv` | 12 | 608 | `year,quarter,value,data_status` |
| 二氧化碳 `sample-seasonal-subseries-noaa-co2-2000-2025.csv` | 312 | 10990 | `year,month,average_ppm,deseasonalized_ppm,data_status`（圖 R15、圖 R16；真實資料） |

自檢腳本位元組：S1 2653、S2 3763、S3 3663、S4 4745、S5 2257、S6 2437、S7 2848、S8 2232、二氧化碳檔 5015。

**CSV 格式：** 虛構檔第 1 行是 `# 虛構資料，數字未核｜…`，最後一欄 `data_status` 一律「虛構資料，數字未核」。二氧化碳檔第 1 行標明真實資料、海洋暨大氣總署、2026-10-11 下載，以及 2022-12 至 2023-07 初改用毛納基亞；`data_status` 為「真實資料」。讀入時要跳過 `#` 行。列數是資料列（`wc -l` 再扣說明行與表頭）。

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-seasonal-subseries-sim-s1-anatomy-selfcheck.py
python3 sample-seasonal-subseries-noaa-co2-2000-2025-selfcheck.py   # 其餘同理，共 9 支
```

預期每支逐項印出 `PASS｜…`，最後一行 `RESULT: PASS（N 項通過、0 項失敗）`（**v0.3.35 上架前實跑，結束碼 0**）。實跑通過項數：S1 6、S2 5、S3 6、S4 7、S5 5、S6 6、S7 7、S8 5、二氧化碳檔 8。

**以實際計數為準**（自檢從 CSV 重算，與課程稿關鍵讀數一致。沒有重跑沒有收進本 repo 的 `draw_seasonal_subseries.py`／`draw_noaa_co2.py`／`export_samples.py`。本課沒有改這些檔，不宣稱與素材包逐位元相同）：(1) 虛構檔**數字未核**；二氧化碳檔是美國政府公開資料，不是虛構；(2) 圖 S1 的 7 月平均 447.4、1 月 203.3，72 點；(3) 圖 S2 的 6／7／8 月斜率 13.9／15.2／15.9，夏季平均斜率 15.0（版面上／中／下）；(4) 圖 S3 的 7 月斜率 −1.5、9 月 +2.0，前 3 年高峰 8 月、後 3 年 9 月；(5) 圖 S4 的 `detrended` 欄等於扣趨勢直線，原始各格平均斜率 5.9，去趨勢後高低差 10.2、高峰 6 月、低谷 1 月；(6) 圖 S5 純雜訊高低差 6.5、有季節 10.7；(7) 圖 S6 的 2021 年 3 月為 43.1，3 月平均含 68.8、不含 72.4，中位數 72.8；(8) 圖 S7 自相關滯後 12／24／6 為 0.752／0.701／−0.793，滯後 12 皮爾森相關四捨五入到小數第三位為 0.82，半寬 0.179，120 點（直式上／中／下）；(9) 圖 S8 季平均 44.7／58.7／65.7／49.3；(10) 圖 R15 各格平均斜率 2.29 ppm／年（未去趨勢的反例）；(11) 圖 R16 扣二次趨勢後 5 月最高、9 月最低，未舍入高低差四捨五入為 6.51，5 月 +3.15、9 月 −3.35、10 月 −3.34；(12) 「減當年平均」對照是 5 月 +2.87、9 月 −2.88，自檢有核對，**不是**圖 R16、也不是圖 S4 的做法。去季節欄那組 2.99 → 3.27、−3.32 → −3.44 **沒有**寫進自檢，原因未核，不要拿去改寫圖 R16 的 +3.15／−3.35。圖 R1 是手冊事先扣過直線，不是這份 CSV 的二次曲線，也不是 +2.87／−2.88。

## 季節分解圖資料與自檢腳本 `sample-seasonal-decomp-sim-s1-…` 到 `sample-seasonal-decomp-sim-s5-outlier`

**收錄哪些：** 素材包 `2026-10-13-am-seasonal-decomp` 有 5 份虛構資料（S1–S5，各對應一張模擬圖）和 5 支自檢腳本；素材包沒有指定哪一份給 repo，所以 **5 組全部收錄**（共 10 個檔）。課程沒有點名畫圖腳本，本 repo 也沒有收。

**檔名：** 素材包檔名本來就有 `seasonal-decomp` 前綴，與本 repo `examples/data/` 既有檔案**沒有撞名**，所以**沒有改名**。本節**沒有改這些檔**，也**不宣稱與素材包逐位元相同**（沒有做 `cmp`）。每支自檢以明確檔名讀 CSV（從腳本所在資料夾讀），沒有萬用字元；只用 Python 標準函式庫（`csv`、`math`、`os`、`sys`；母體標準差除以 n，不靠 numpy）。預期值寫在腳本裡。

**沒有縮小：** 5 個 CSV 合計 **22,446 位元組（約 21.9 KiB）**，單檔最大是 S5 的 5,973 位元組（約 5.8 KiB）。都小於 25 萬位元組。模擬圖重畫種子 20261013。

| 檔 | 列數 | CSV 位元組 | 欄位 |
|---|---:|---:|---|
| S1 `sample-seasonal-decomp-sim-s1-anatomy.csv` | 120 | 4858 | `year_frac,observed,trend,seasonal,resid` |
| S2 `sample-seasonal-decomp-sim-s2-add-vs-mult.csv` | 120 | 3792 | `year_frac,observed,add_resid,mult_resid` |
| S3 `sample-seasonal-decomp-sim-s3-classical-vs-stl.csv` | 120 | 3905 | `year_frac,observed,classical_resid,stl_resid` |
| S4 `sample-seasonal-decomp-sim-s4-no-season.csv` | 120 | 3918 | `year_frac,observed,seasonal,resid` |
| S5 `sample-seasonal-decomp-sim-s5-outlier.csv` | 120 | 5973 | `year_frac,observed,classical_trend,stl_trend,classical_resid,stl_resid` |

自檢腳本位元組：S1 2824、S2 2515、S3 2432、S4 2342、S5 2965。

**CSV 格式：** 第 1 行就是表頭（**沒有** `#` 說明行），也**沒有** `data_status` 欄——與季節子序列圖那批練習檔不同。空格＝古典分解頭尾算不到的趨勢或殘差。`year_frac` 從 2015.0 到 2024.9167（2015–2024 共 120 個月）。列數是資料列（`wc -l` 再扣表頭，所以 `wc -l` 是 121）。

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-seasonal-decomp-sim-s1-anatomy-selfcheck.py
python3 sample-seasonal-decomp-sim-s5-outlier-selfcheck.py   # 其餘同理，共 5 支
```

預期每支逐項印出 `PASS｜…`，最後一行 `RESULT: PASS（N 項通過、0 項失敗）`（課程稿記載在 `examples/data/` 實跑，結束碼 0）。實跑通過項數：S1 9、S2 7、S3 7、S4 7、S5 10。

**以實際計數為準**（自檢從 CSV 重算，與課程稿關鍵讀數一致。課程沒有點名畫圖腳本，本 repo 也沒有重跑。本節沒有改這些檔，不宣稱與素材包逐位元相同）：(1) 虛構檔**數字未核**；(2) 圖 S1 殘差最大絕對值 4.4、季節 9.8，趨勢頭尾各空 6 格，有值處原始＝三成分之和；(3) 圖 S2 加法殘差去掉空值後前 24／後 24 筆母體標準差（除以 n）14.47／15.98，乘法 0.02／0.01（直式上／中／下）；(4) 圖 S3 古典殘差標準差 5.28、STL 2.39；STL 季節窗 7 是課程稿記載，CSV 沒有這欄，**自檢未核對**；(5) 圖 S4 季節最大絕對值 1.29、殘差標準差 2.64，殘差比季節大，季節格不可信；(6) 圖 S5 離群值序號 62（`year_frac` 2020.1667），古典殘差 51.0、STL 61.6；相對產生過程直線（水準 100、每月 +0.5），古典趨勢鼓起最多 5.4、穩健 STL 1.1。模擬記載的離群值 +60、同月份古典季節墊高 6.3 **沒有**寫進自檢（S5 CSV 沒有季節欄）。古典分解至少兩個完整週期、月資料少於 24 筆不要用古典，是課程稿轉述 statsmodels 0.15.0 文件，**本 repo 未實測**。圖 S2–S5 只有直式上／中／下。圖號維持 R1–R5、S1–S5，不重排。

## 散布圖矩陣資料與自檢腳本 `sample-splom-sim-s1-…` 到 `sample-splom-sim-s5-outlier-multicell`

**收錄哪些：** 素材包有 5 份練習資料（S1–S5，各對應一張模擬圖）和本 repo 另寫的 5 支自檢腳本；**5 組全部收錄**（共 10 個檔）。課程稿沒有點名畫圖腳本。素材包說明點名 `draw_splom.py`，該腳本不在這次對到的檔案裡，本 repo **沒有收**。

**檔名：** 素材包檔名本來就有 `splom` 前綴，與本 repo `examples/data/` 既有檔案**沒有撞名**，所以**沒有改名**。本節**沒有改這些 CSV**。複製後以 `cmp` 核對，**與素材包逐位元相同**。每支自檢以明確檔名讀 CSV（從腳本所在資料夾讀），沒有萬用字元；只用 Python 標準函式庫（`csv`、`math`、`os`、`sys`；皮爾森相關自寫，不靠 numpy、pandas）。預期值寫在腳本裡。

**沒有縮小：** 5 個 CSV 合計 **35,097 位元組（約 34.3 KiB）**，單檔最大是 S4 的 13,687 位元組（約 13.4 KiB）。都小於 25 萬位元組。模擬圖種子 20261014（S2、S3 的數字來自公開資料集，不是這顆種子造出來的）。

| 檔 | 列數 | CSV 位元組 | 欄位 |
|---|---:|---:|---|
| S1 `sample-splom-sim-s1-anatomy.csv` | 80 | 4417 | `變數甲,變數乙,變數丙` |
| S2 `sample-splom-sim-s2-corr-upper.csv` | 150 | 2440 | `萼片長,萼片寬,花瓣長,花瓣寬` |
| S3 `sample-splom-sim-s3-grouped-shapes.csv` | 333 | 10826 | `嘴峰長,嘴峰深,鰭長,體重,品種` |
| S4 `sample-splom-sim-s4-too-many-vs-heatmap.csv` | 100 | 13687 | `甲,乙,丙,丁,戊,己,庚` |
| S5 `sample-splom-sim-s5-outlier-multicell.csv` | 61 | 3727 | `變數甲,變數乙,變數丙,標記` |

自檢腳本位元組：S1 2579、S2 2519、S3 3261、S4 2464、S5 2091。

**CSV 格式：** 第 1 行就是表頭（**沒有** `#` 說明行），也**沒有** `data_status` 欄。列數是資料列（`wc -l` 再扣表頭）。S1、S4、S5 是虛構。S2 是鳶尾花四個數值欄（公有領域，Anderson／Fisher）。S3 是企鵝四個測量加品種（Palmer Penguins，CC0，Horst、Hill、Gorman）。

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-splom-sim-s1-anatomy-selfcheck.py
python3 sample-splom-sim-s5-outlier-multicell-selfcheck.py   # 其餘同理，共 5 支
```

預期每支逐項印出 `PASS｜…`，最後一行 `RESULT: PASS（N 項通過、0 項失敗）`（在 `examples/data/` 實跑，結束碼 0）。實跑通過項數：S1 9、S2 8、S3 10、S4 8、S5 9。

**以實際計數為準**（自檢從 CSV 重算。本節沒有改這些 CSV，與素材包逐位元相同。沒有重跑 `draw_splom.py`，本 repo 也沒有收這個腳本，也沒有收 png）：(1) 圖 S1 虛構，n＝80，甲與乙相關 0.7124228200726517，另外兩對絕對值都小於 0.1；(2) 圖 S2 花瓣長與花瓣寬 0.962865431402796，且是六對裡絕對值最大的一對（公有領域鳶尾花；課程稿圖說「約零點九六（未核）」）；(3) 圖 S3 n＝333、三個品種（阿德利 146、帽帶 68、巴布亞 119）；巴布亞平均鰭長與平均體重最高，鰭長與體重都仍與另外兩組有重疊（偏右上，不是完全分開）；圓、方、三角是畫圖時加上的，CSV 沒有形狀欄；(4) 圖 S4 七欄、100 列、非對角 21 對，最大絕對相關 0.8067857797701805，落在丙與戊；版面左／右；(5) 圖 S5 n＝61，離群點 (22, 4, 18) 僅一列，且在三個變數上都離開其餘 60 列。圖 R1、R2、R4 只用顏色區分組別，不符合顏色加形狀；正例是圖 S3。圖號維持 R1–R5、S1–S5，不重排。

## 泰勒圖資料與自檢腳本 `sample-taylor-sim-s1-…` 到 `sample-taylor-sim-s5-improvement`

**收錄哪些：** 素材包有 5 份練習資料（S1–S5，各對應一張模擬圖）和本 repo 另寫的 5 支自檢腳本；**5 組全部收錄**（共 10 個檔）。S1–S5 都是模擬範例資料。課程稿沒有點名畫圖腳本。素材包另有一支繪製模擬圖的腳本，公開檔不寫它的檔名，本 repo **沒有收**，也沒有收 png。

**檔名：** 素材包檔名本來就有 `taylor` 前綴，與本 repo `examples/data/` 既有檔案**沒有撞名**，所以**沒有改名**。本節**沒有改這些 CSV**。複製後以 `cmp` 核對，**與素材包逐位元相同**。每支自檢以明確檔名讀 CSV（從腳本所在資料夾讀），沒有萬用字元；只用 Python 標準函式庫（`csv`、`math`、`os`、`sys`；中心化均方根誤差用餘弦定理自寫，E'² = s_r² + s_m² − 2 s_r s_m R，不靠 numpy）。預期值寫在腳本裡。練習檔的 s_r 取 1：圖 S1 的觀測標準差就是 1.0；圖 S2、圖 S4 的 few、圖 S5，以及圖 S3 的正規化面板，都用 s_r＝1。圖 S3 的原始雨量不拿 s_r＝1 去算。

**沒有縮小：** 5 個 CSV 合計 **438 位元組（約 0.43 KiB）**，單檔最大是 S3 的 113 位元組。都小於 25 萬位元組。模擬圖種子 20261015。浮水印是「模擬｜範例數字未核（虛構資料）」。

| 檔 | 列數 | CSV 位元組 | 欄位 |
|---|---:|---:|---|
| S1 `sample-taylor-sim-s1-anatomy.csv` | 2 | 71 | `id,std,corr,note` |
| S2 `sample-taylor-sim-s2-models.csv` | 6 | 109 | `model,std,corr,marker` |
| S3 `sample-taylor-sim-s3-normalize.csv` | 4 | 113 | `panel,var,std_or_norm,corr` |
| S4 `sample-taylor-sim-s4-crowded-vs-few.csv` | 4 | 92 | `panel,id,std,corr` |
| S5 `sample-taylor-sim-s5-improvement.csv` | 2 | 53 | `version,std,corr` |

自檢腳本位元組：S1 2742、S2 2863、S3 3390、S4 2766、S5 2681。

**CSV 格式：** 第 1 行就是表頭（**沒有** `#` 說明行），也**沒有** `data_status` 欄。列數是資料列（`wc -l` 再扣表頭）。S1–S5 都是模擬範例資料，數字未核。圖 S4 的 CSV 只有 few 四列；圖說的 24 點不在檔內，自檢未核對。

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-taylor-sim-s1-anatomy-selfcheck.py
python3 sample-taylor-sim-s5-improvement-selfcheck.py   # 其餘同理，共 5 支
```

預期每支逐項印出 `PASS｜…`，最後一行 `RESULT: PASS（N 項通過、0 項失敗）`（在 `examples/data/` 實跑，結束碼 0）。實跑通過項數：S1 9、S2 10、S3 11、S4 10、S5 10。

**以實際計數為準**（自檢從 CSV 重算。本節沒有改這些 CSV，與素材包逐位元相同。素材包點名的繪圖腳本沒有收，公開檔不寫檔名，也沒有重跑，也沒有收 png）：(1) 圖 S1 模擬範例，觀測 std 1.0、corr 1.0、note「參考點」，對自己的 E'＝0；模型甲 1.2／0.75、note「示意」，E'＝0.8；圖說的紅方是畫法；(2) 圖 S2 模型 A 的 E'＝0.3999999999999999，且是六點裡最小（不是先寫成 0.4）；(3) 圖 S3 版面上／下；同一變數的相關不變；氣溫的數值不變、雨量變了；正規化後面版以 s_r＝1 重算，雨量 E'＝0.5708765190476832、氣溫 0.4795831523312717；原始雨量不用 s_r＝1；(4) 圖 S4 版面上廿四點／下四點；CSV 只有 few 四列，甲的 E'＝0.3784177585684897 最小，乙正好 0.75；24 點自檢未核對；(5) 圖 S5 舊版 E'＝1.0965856099730655、新版 0.5044799302251775，新版更靠近（標準差更靠近 1，相關也較高）；紅到綠的箭頭是圖說，CSV 沒有顏色欄。圖 R3、R4、R5 數字未核。圖 R2 的課程稿圖說沒寫這四字，授權註記另寫數字未核，不從圖上量。圖號維持 R1–R5、S1–S5，不重排。

## 週期圖資料與自檢腳本 `sample-periodogram-sim-s1-…` 到 `sample-periodogram-sim-s5-vs-spectrogram`

**收錄哪些：** 素材包有 5 份練習資料（S1–S5，各對應一張模擬圖）和本 repo 另寫的 5 支自檢腳本；**5 組全部收錄**（共 10 個檔）。S1–S5 都是模擬範例資料。課程稿沒有點名畫圖腳本。素材包另有一支繪製模擬圖的腳本，公開檔不寫它的檔名，本 repo **沒有收**，也沒有收 png。

**檔名：** 素材包檔名本來就有 `periodogram` 前綴，與本 repo `examples/data/` 既有檔案**沒有撞名**，所以**沒有改名**。本節**沒有改這些 CSV**。複製後以 `cmp` 核對，**與素材包逐位元相同**。每支自檢以明確檔名讀 CSV（從腳本所在資料夾讀），沒有萬用字元。只用 Python 標準函式庫：圖 S1 用 `csv`、`math`、`os`、`sys`，功率是純 Python 離散傅立葉轉換的 |X|²，**沒有除以點數**，不靠 numpy；圖 S2–S5 只用 `csv`、`os`、`sys`（檔已經是頻譜，不再做轉換，也不重做短時傅立葉轉換）。預期值寫在腳本裡。

**沒有縮小：** 5 個 CSV 合計 **40103 位元組（約 39.16 KiB）**，單檔最大是 S5 的 16554 位元組。都小於 25 萬位元組。模擬圖種子 20261016。浮水印是「模擬｜範例數字未核（虛構資料）」。

| 檔 | 列數 | CSV 位元組 | 欄位 |
|---|---:|---:|---|
| S1 `sample-periodogram-sim-s1-anatomy.csv` | 200 | 5224 | `t_s,x` |
| S2 `sample-periodogram-sim-s2-two-tones.csv` | 257 | 8250 | `freq_Hz,power` |
| S3 `sample-periodogram-sim-s3-leakage.csv` | 129 | 6233 | `freq_Hz,rect_dB,hann_dB` |
| S4 `sample-periodogram-sim-s4-welch.csv` | 129 | 3842 | `freq_Hz,welch_power` |
| S5 `sample-periodogram-sim-s5-vs-spectrogram.csv` | 501 | 16554 | `freq_Hz,periodogram_power` |

自檢腳本位元組：S1 3899、S2 2767、S3 3530、S4 2654、S5 2804。

**CSV 格式：** 第 1 行就是表頭（**沒有** `#` 說明行），也**沒有** `data_status` 欄。列數是資料列（`wc -l` 再扣表頭）。S1–S5 都是模擬範例資料，數字未核。圖 S1 的模擬記載 n＝1024、尖峰 19.922 赫茲不在這份 CSV。圖 S4 的原始單段不在 CSV。圖 S5 的先後不在 CSV。

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-periodogram-sim-s1-anatomy-selfcheck.py
python3 sample-periodogram-sim-s5-vs-spectrogram-selfcheck.py   # 其餘同理，共 5 支
```

預期每支逐項印出 `PASS｜…`，最後一行 `RESULT: PASS（N 項通過、0 項失敗）`（在 `examples/data/` 實跑，結束碼 0）。實跑通過項數：S1 13、S2 10、S3 11、S4 10、S5 10。

**以實際計數為準**（自檢從 CSV 重算。本節沒有改這些 CSV，與素材包逐位元相同。課程稿沒有點名畫圖腳本。素材包點名的繪圖腳本沒有收，公開檔不寫檔名，也沒有重跑，也沒有收 png）：(1) 圖 S1 這份檔 200 點，尖峰正好 20.0 赫茲；未扣平均功率 10192.720424279498，扣平均 10192.720424279489，對稱漢寧後 2351.9007398023687；n＝1024 與 19.922 赫茲不在檔內；(2) 圖 S2 高於 0.01 的局部極大只有 12.109375 赫茲（0.0568727306453308）與 37.109375 赫茲（0.02650337611567428），前者較高；12.01 與 37.01 不是存檔的列；(3) 圖 S3 兩種窗的尖峰都在 10.15625 赫茲、0.0 分貝；±2 格以外最高旁瓣都在 11.328125 赫茲，矩形 −17.019584057359197、漢寧 −34.20898840629693，124 格裡矩形較高的有 98 格；(4) 圖 S4 Welch 尖峰正好 25.0 赫茲、功率 0.41938521275201973，而且高於其餘每一格；原始單段不在檔內；(5) 圖 S5 15.0 赫茲 1.201085763474063、40.0 赫茲 1.2359419294357712 是兩個主要尖峰；先後不在檔內。圖 R2、圖 R4 數字未核。圖 R1 的課程稿寫約 30 與 50 赫茲，不從圖上重測。圖 R3 只作單段對 Welch 的方法對照，來源頁標右半為鏡像。圖號維持 R1–R5、S1–S5，不重排。窗長、短時傅立葉轉換與分貝見頻譜圖，不在本節重講。

## 波德圖資料與自檢腳本 `sample-bode-sim-s1-…` 到 `sample-bode-sim-s5-signal-vs-system`

5 組範例資料 CSV 與 5 支自檢已在本目錄（共 10 檔）。S1–S5 都是模擬範例資料，種子 20261017，浮水印「模擬｜範例數字未核（虛構資料）」，數字未核。檔名已有 `bode` 前綴。CSV 與素材包逐位元相同（`cmp`）。合計 14009 位元組（約 13.68 KiB），最大是 S5 的 11280。第 1 行就是表頭，沒有 `#`，沒有 `data_status`。自檢只用 `csv`、`math`、`os`、`sys`，不靠 numpy。通過項數 S1 11、S2 12、S3 14、S4 14、S5 12。腳本位元組 3261、3154、3846、3821、3371。沒有收 png。

| 檔 | 列數 | CSV 位元組 | 欄位 |
|---|---:|---:|---|
| S1 `sample-bode-sim-s1-anatomy.csv` | 17 | 731 | `freq_Hz,gain_dB_measured,phase_deg_measured,gain_dB_theory,phase_deg_theory` |
| S2 `sample-bode-sim-s2-linear-vs-log.csv` | 26 | 431 | `freq_Hz,gain_dB` |
| S3 `sample-bode-sim-s3-order-slope.csv` | 21 | 836 | `freq_Hz,gain1_dB,phase1_deg,gain2_dB,phase2_deg` |
| S4 `sample-bode-sim-s4-stability-margins.csv` | 29 | 731 | `freq_Hz,open_loop_gain_dB,open_loop_phase_deg` |
| S5 `sample-bode-sim-s5-signal-vs-system.csv` | 460 | 11280 | `freq_Hz,input_power_dB,output_power_dB` |

自檢：`sample-bode-sim-s1-anatomy-selfcheck.py`、`sample-bode-sim-s2-linear-vs-log-selfcheck.py`、`sample-bode-sim-s3-order-slope-selfcheck.py`、`sample-bode-sim-s4-stability-margins-selfcheck.py`、`sample-bode-sim-s5-signal-vs-system-selfcheck.py`。圖 S2 的 5000 赫茲不是一列；圖 S4 密格 2.052 赫茲、4.468 赫茲、12.02 分貝、32.67 度不是原列；圖 S5 的 49.68 赫茲、14.02 分貝不在 CSV。圖 R3 的 f_GM 與 f_PM 對調照錄。圖 R4 約 5 千赫茲、約 30 度數字未核。

## 霍夫默勒圖資料與自檢腳本 `sample-hovmoller-sim-s1-…` 到 `sample-hovmoller-sim-s5-traffic`

5 組範例資料 CSV 與 5 支自檢已在本目錄（共 10 檔）。S1–S5 都是模擬範例資料，種子 20261018，浮水印「模擬｜範例數字未核（虛構資料）」，數字未核。檔名已有 `hovmoller` 前綴。合計 108935 位元組（約 106.38 KiB），最大是 S3 的 32099。都小於 25 萬位元組。第 1 行就是表頭，沒有 `#`，沒有 `data_status`。寬表：時間為列、位置為欄。0 度與 360 度是同一條經線，斜率與變號先去掉尾欄。自檢只用 `csv`、`math`、`os`、`sys`，不靠 numpy。通過項數 S1 9、S2 9、S3 8、S4 8、S5 10。腳本位元組 3948、4123、3940、4006、3679。沒有收 png。

| 檔 | 列數 | CSV 位元組 | 欄位 |
|---|---:|---:|---|
| S1 `sample-hovmoller-sim-s1-anatomy.csv` | 61 | 29670 | `day` 加上經度 0 到 360、每 5 度（74 欄） |
| S2 `sample-hovmoller-sim-s2-direction.csv` | 31 | 14672 | `day` 加上經度 0 到 360、每 5 度（74 欄） |
| S3 `sample-hovmoller-sim-s3-phase-group.csv` | 51 | 32099 | `day` 加上經度 0 到 360、每 4 度（92 欄） |
| S4 `sample-hovmoller-sim-s4-colormap.csv` | 31 | 14843 | `day` 加上經度 0 到 360、每 5 度（74 欄） |
| S5 `sample-hovmoller-sim-s5-traffic.csv` | 61 | 17651 | `minute` 加上里程 0 到 20、每 0.5 公里（42 欄） |

自檢：`sample-hovmoller-sim-s1-anatomy-selfcheck.py`、`sample-hovmoller-sim-s2-direction-selfcheck.py`、`sample-hovmoller-sim-s3-phase-group-selfcheck.py`、`sample-hovmoller-sim-s4-colormap-selfcheck.py`、`sample-hovmoller-sim-s5-traffic-selfcheck.py`。圖 S1 脊線 3.9151242728714966 度／日（印 3.915；記載 3.89 不是原格）；赤道附近換算印成 5.04 公尺每秒。圖 S2 的 +6 與 −8 度／日未核對。圖 S3 群速印成 27.99，相速每天 10 度未分開追。圖 S4 色盤名稱不在 CSV。圖 S5 塞車波每小時 −18 公里未核對。圖 R1 時間往上、圖 S1 往下。高緯不要把 111.2 公里直接套上。圖 R1 速度未核、緯度存疑。圖 R2 變數與單位未核。圖 R5 彩虹色只看走向。

## 斜溫圖資料與自檢腳本 `sample-skewt-sim-s1-…` 到 `sample-skewt-sim-s5-stable-unstable`

5 組範例資料 CSV 與 5 支自檢已在本目錄（共 10 檔）。S1–S5 都是模擬範例資料，種子 20261019，浮水印「模擬｜範例數字未核（虛構資料）」，數字未核。檔名已有 `skewt` 前綴。合計 4089 位元組（約 3.99 KiB），最大是 S5 的 1628。都小於 25 萬位元組。第 1 行就是表頭，沒有 `#`，沒有 `data_status`。氣壓 1000 到 100 百帕、嚴格遞減：1000–700 每 25 百帕，700–200 每 50 百帕，200–100 每 25 百帕，共 27 層。圖 S5 先 27 列 `stable`，再 27 列 `unstable`。自檢只用 `csv`、`math`、`os`、`sys`，不靠 numpy。通過項數 S1 10、S2 7、S3 17、S4 10、S5 24。腳本位元組 4194、2952、6255、3854、8554。沒有收 png。

| 檔 | 列數 | CSV 位元組 | 欄位 |
|---|---:|---:|---|
| S1 `sample-skewt-sim-s1-anatomy.csv` | 27 | 780 | `pressure_hPa`、`temperature_C`、`dewpoint_C`、`wind_speed_kt`、`wind_dir_deg` |
| S2 `sample-skewt-sim-s2-why-skew.csv` | 27 | 459 | `pressure_hPa`、`temperature_C`、`dewpoint_C` |
| S3 `sample-skewt-sim-s3-parcel-cape.csv` | 27 | 617 | `pressure_hPa`、`temperature_C`、`dewpoint_C`、`surface_parcel_C` |
| S4 `sample-skewt-sim-s4-cloud-layers.csv` | 27 | 605 | `pressure_hPa`、`temperature_C`、`dewpoint_C`、`dewpoint_depression_C` |
| S5 `sample-skewt-sim-s5-stable-unstable.csv` | 54 | 1628 | `panel`、`pressure_hPa`、`temperature_C`、`dewpoint_C`、`surface_parcel_C` |

自檢：`sample-skewt-sim-s1-anatomy-selfcheck.py`、`sample-skewt-sim-s2-why-skew-selfcheck.py`、`sample-skewt-sim-s3-parcel-cape-selfcheck.py`、`sample-skewt-sim-s4-cloud-layers-selfcheck.py`、`sample-skewt-sim-s5-stable-unstable-selfcheck.py`。圖 S1 的 500 百帕是 −5.7 度；垂直誤讀與斜角未核；風速風向未另核。圖 S2 的 0 度與 45 度未核。圖 S3 穿越 746.8284542966692 與 162.8008773618526 百帕；2311 與 −87 未積分；950 百帕溫差 0 不是自由對流高度。圖 S4 的層是 [975, 775]（9 層）與 [400, 350]（2 層）；地面露點差 2.4；是不是雲未核；2 度是經驗門檻、各家不一、未核。圖 S5 穩定面板沒有正的溫度差；印成 943.99 的近地薄正差不是自由對流高度；不穩定面板自由對流高度附近是 756.1733601325386 百帕、平衡高度附近是 164.00229547459637 百帕；2455 與 −74 未積分。圖 R1 是 CC BY-SA 4.0 JeanBizHertzberg，底圖未核，必須寫「底圖未核，轉載須再確認」，整張不是已清授權。圖 R2 是 CC BY-SA 4.0 TomRat。圖 R3 公有領域 NOAA SPC。圖 R4 公有領域 NWS。圖 R5 公有領域 NWS Quad Cities。

