# Demo data（虛構示意；多為 CSV，火焰圖為已收合堆疊 .txt，MA 圖、QQ 圖、Bland–Altman 圖、LocusZoom 圖與 P–P 圖各附一支自檢 .py）

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
| `sample-ma-selfcheck.py` | 上一檔的自檢腳本（純標準函式庫 Python，不是資料）；見下方「自檢腳本」 | 同上 |
| `sample-qq-fictional.csv` | QQ 圖練習資料：row_id, group, value, pvalue_sim（220 列、約 6 KB；A 組近似常態 120 筆、B 組右偏 100 筆；檔頭兩行以 `#` 開頭要略過；虛構，數字未核） | `2026-09-30-am-qq` |
| `sample-qq-selfcheck.py` | 上一檔的自檢腳本（需 numpy 與 scipy，不是資料）；見下方「QQ 圖自檢腳本」，（v0.3.18 已修正讀檔方式） | 同上 |
| `sample-ba-fictional.csv` | Bland–Altman 圖練習資料：row_id, dataset, method_a, method_b（220 列、約 6 KB；dataset＝good 100 對「一致性良好」＋ fan 120 對「誤差與大小成比例」；**差值一律是方法 B 減方法 A**；檔頭兩行以 `#` 開頭要略過；虛構，數字未核） | `2026-09-30-pm-ba` |
| `sample-ba-selfcheck.py` | 上一檔的自檢腳本（需 numpy，不是資料）；見下方「Bland–Altman 自檢腳本」；以明確檔名讀 CSV，可直接在本資料夾跑 | 同上 |
| `sample-locuszoom-fictional.csv` | LocusZoom 圖（區域關聯圖）練習資料：row_id, record_type, dataset, chrom, position_bp, end_bp, neg_log10_p, ld_r2_to_index, ld_band, is_index, gene_name, strand, recomb_rate_schematic（2,306 列、約 112 KB；record_type＝variant 變異位點 2,239、gene 基因軌 11、recomb 重組率示意取樣點 56；dataset＝genome 全基因組背景 1,760 點＋第 10 號染色體 45.0–45.55 Mb 四段虛構區間 single／following／second／readcolors；檔頭兩行以 `#` 開頭要略過；虛構，數字未核） | `2026-10-01-am-locuszoom` |
| `sample-locuszoom-selfcheck.py` | 上一檔的自檢腳本（需 numpy，不是資料）；見下方「LocusZoom 自檢腳本」；以明確檔名讀 CSV，可直接在本資料夾跑 | 同上 |
| `sample-pp-fictional.csv` | P–P 圖虛構資料（1,000 列、約 30 KB；欄位 row_id, dataset, group, obs_index, value, value2；8 個 dataset：anatomy 20、good 100、heavy 200、loc 100、skew 200、two 200、resid 80、sm 100 列；檔頭**三行以 # 開頭要略過**） | 2026-10-01-pm-pp.md |
| `sample-pp-selfcheck.py` | 上一檔的自檢腳本（需 numpy 與 scipy，不是資料）；見下方「P–P 自檢腳本」；以明確檔名讀 CSV，可直接在本資料夾跑 | 同上 |

對應 pattern：`../dot-density-map.md`、`../streamgraph-composition.md`、`../population-pyramid.md`、`../lollipop-rank.md`、`../boxplot-summary.md`、`../bubble-chart.md`、`../marimekko-chart.md`、`../choropleth-map.md`、`../tile-map.md`、`../matrix-heatmap.md`、`../spiral-plot.md`、`../biofabric.md`、`../flame-graph.md`、`../circos.md`、`../volcano-plot.md`、`../manhattan-plot.md`、`../ma-plot.md`、`../qq-plot.md`、`../bland-altman.md`、`../locuszoom.md`、`../pp-plot.md`。

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

注意：此腳本與納茲素材包版本不再逐位元相同，唯一差別是那一行讀檔；資料與檢查邏輯未動。

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
