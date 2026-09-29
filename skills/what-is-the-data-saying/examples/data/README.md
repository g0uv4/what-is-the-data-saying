# Demo data（虛構示意；多為 CSV，火焰圖為已收合堆疊 .txt，MA 圖另附一支自檢 .py）

來自納茲已審 skill pack。**非真實產業資料；數字未核。**

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
| `sample-ma-selfcheck.py` | 上一檔的自檢腳本（純標準庫 Python，不是資料）；見下方「自檢腳本」 | 同上 |

對應 pattern：`../dot-density-map.md`、`../streamgraph-composition.md`、`../population-pyramid.md`、`../lollipop-rank.md`、`../boxplot-summary.md`、`../bubble-chart.md`、`../marimekko-chart.md`、`../choropleth-map.md`、`../tile-map.md`、`../matrix-heatmap.md`、`../spiral-plot.md`、`../biofabric.md`、`../flame-graph.md`、`../circos.md`、`../volcano-plot.md`、`../manhattan-plot.md`、`../ma-plot.md`。

## 自檢腳本 `sample-ma-selfcheck.py`

檢查 `sample-ma-fictional.csv`：共 3,000 列、`base_mean` 落在 1 至 100000、`a_log2_mean` ＝ log2(base_mean + 1)、`padj` 介於 0 與 1、|收縮後 M| ≤ |收縮前 M|、`gene_id` 不重複。只用 Python 標準庫（csv、math），任何 Python 3 都能跑。

腳本用相對路徑讀 CSV，所以要**先進到本資料夾**再執行：

```bash
cd skills/what-is-the-data-saying/examples/data
python3 sample-ma-selfcheck.py
```

通過時印一行（v0.3.16 上架前已在 python3 實跑，結束碼 0）：`OK 筆數 3000 | base_mean 1.01 ~ 99887.02 | M -4.745 ~ 5.784 | padj<0.05 筆數 197`；任一檢查不過會直接丟出 AssertionError。腳本內容與素材包版本逐位元相同，這個 pattern 的 CSV 與 .py 都未修改。
