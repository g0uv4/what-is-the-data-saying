# Pattern: ma-plot

> **圖種**：MA 圖（MA plot；亦稱平均－差值圖 Mean–Difference plot，簡寫 MD plot）
> **來源（專案維護者整理）**：`teach-viz/2026-09-29-pm-ma.md`（方法教學；正式課程）
> **定義（英文維基百科原文）**："an MA plot is an application of a Bland–Altman plot for visual representation of genomic data. The plot visualizes the differences between measurements taken in two samples, by transforming the data onto M (log ratio) and A (mean average) scales"
> **核心**：**每個點＝一個受測特徵**（基因、探針或轉錄本）；**橫軸 A＝平均表現**（微陣列是平均對數強度；RNA 定序常用平均正規化計數，橫軸多用對數刻度；愈右訊號愈亮、計數愈高）；**縱軸 M＝對數倍數變化**（log ratio，常用以 2 為底；0＝沒變、上方上調、下方下調）；RNA 定序計數資料的點雲常像漏斗或喇叭，左邊（低表現）上下散得較開、右邊（高表現）較貼近 M＝0
> **一句話**：橫軸不是基因組位置，也不是 −log10(p)；愈右表示平均表現愈高，上下才是倍數方向
> **原始文獻**：Dudoit、Yang、Callow、Speed 2002，*Statistica Sinica* 12:111–139（M、A 座標與 45° 旋轉的說明）；Yang 等人 2002，*Nucleic Acids Research* 30(4):e15。「M 是 minus、A 是 add」的口訣最早出處**未能證實**（biostatsquid 寫 "M stands for 'minus' because log(A/B) = logA-logB"，屬教學網站說法）

## When

- 雙通道微陣列、RNA 定序、蛋白質體等大量特徵的**兩條件比較**
- 已跑完差異分析的結果表：至少有平均表現（`baseMean` 或 A）與對數倍數（`log2FoldChange` 或 M）兩欄；要著色顯著點時另需 p 值或校正後 q 值
- **正規化品質檢查與差異分析診斷**：正規化後多數點應大致以 M＝0 為中心、平滑趨勢不該整條歪掉；顯著點落在高或低表現區；低計數的極端倍數是否需要收縮
- 樣本間平均－差值圖（edgeR、limma 的 `plotMD`：該樣本相對於其餘樣本平均）

## Recommend

- **主選**：MA 圖（橫軸 A、縱軸 M、畫 M＝0 參考線；顯著點依校正後 p 值或 q 值著色）
- **並陳收縮前後**：同一頁放「收縮前」「收縮後」兩張（DESeq2 中分別把 `results()` 的未收縮結果表與經 `lfcShrink` 處理後的結果表餵給 `plotMA`），檢查低表現處喇叭口是否收斂
- **並列火山圖與熱圖**：MA 圖回答「在什麼豐度層級上變」，火山圖回答「證據多強、候選排序」（`volcano-plot.md`），熱圖回答「樣本間模式」
- **互動版**：Glimma（`glimmaMA`，舊名 `glMDPlot`）
- **門檻與參數範例（均出自素材包來源；範例，不是標準）**：

| 門檻或參數 | 出現在哪裡 | 性質 |
|---|---|---|
| `alpha`＝0.1（校正後 p 值小於 0.1 著藍色） | DESeq2 `plotMA` 資料集方法預設；結果表方法優先沿用結果表記錄的 `alpha`，沒有才用 0.1 | 範例，不是標準 |
| `svalue` 門檻 0.005 | DESeq2 `plotMA`，結果表含 `svalue` 欄時改用 | 範例，不是標準 |
| `alpha`＝0.05、`lfc.cutoff`＝0.58（約 1.5 倍差異，換算為自行計算） | HBC DGE 工作坊 DESeq2 課 | 範例，不是標準 |
| padj < 0.05 且 \|LFC\| > 1 | NotchBio 頁面 | 範例，不是標準 |
| \|M\| > 1（沒有統計檢定） | biostatsquid 逐步教學的粉紅點 | 範例，不是標準 |
| 倍數門檻 ±0.5 | DESeq2 教學「倍數門檻檢定」段 | 範例，不是標準 |
| 校正後 p 值 < 0.05 且 \|M\| > 1；校正後 p 值 < 0.1 | 素材包模擬重繪圖 | 範例，不是標準 |
| 單方向差異基因約 30% 以內 TMM 仍算穩健 | Robinson 與 Oshlack 2010 | 範例，不是標準 |
| M＝0、\|M\|＝1 水平參考線 | 多數 MA 圖 | 範例，不是標準 |

- **備選（何時改用哪一種）**：
  - 要做「變化幅度夠大且證據充分」的候選排序 → **火山圖**（`volcano-plot.md`）
  - 要看關聯訊號落在基因組哪一段 → **曼哈頓圖**（`manhattan-plot.md`）
  - 超過兩組又沒有清楚成對對比 → 先定義對比，或改用主成分分析、熱圖
  - 評估臨床兩種量測方法的一致性界限 → [**Bland–Altman 圖**](bland-altman.md)（走專文脈絡，別貼 RNA 定序 MA 圖充數）
  - 只有 p 值、沒有表現量或倍數欄 → 資料前提不足，畫不了 MA 圖
  - 任意兩欄關係 → 一般散點（`correlation-scatter.md`），不要稱為 MA 圖

## 三個必須釘清的事實

1. **`lfcShrink` 預設不改 p 值，顯著點收縮後只是被拉向零，不會消失**（**推論**，依 `plotMA` 前後只差在餵進去的結果表、收縮不動校正後 p 值推得；素材包終稿已標推論，具體以你用的收縮方法輸出欄位為準，例如含 `svalue` 欄時著色門檻另計）。所以「收縮後顯著點消失」不會自動發生；要降級極低 A 區、收縮後貼近零線的顯著點，是判讀時的決策（同樣是推論：官方文件沒有直接載明這條準則）。收縮是**有意偏向零**的估計（Love 等人 2014："The resulting MAP LFCs are biased toward zero in a manner that removes the problem of exaggerated LFCs for low counts."），不等於真值；NotchBio 說收縮後 "reveals the true pattern" 是過度宣稱。
2. **RA 圖的軸語意和 MA 圖相同**：R（對數比值）和 M 一樣放縱軸，A 放橫軸（維基百科 RA plot 條目 "R, like M, is plotted on the y-axis"）。差別只在：RA 圖是 MA 圖的**整數計數版**（"an integer-based version of an MA plot for visualizing two-condition count data"），用微小數值 ε 把「其中一組計數為零」的點納入圖中，因此呈箭頭狀。不要說 RA 圖軸語意不同。
3. **有網站把「MA 圖 vs 火山圖」比較表的火山圖軸寫反（已更正，請勿抄）**：biostatsquid 該頁比較表把火山圖橫軸寫成統計顯著性（"Statistical significance (e.g. –log10(p-value))"）、縱軸寫成 "Log2 fold change"，與主流慣例相反。正確：**火山圖橫軸是效應量（倍數變化）、縱軸是 −log10(p)**（英文維基百科火山圖條目圖說："large magnitude fold-changes (x axis) and high statistical significance (-log10 of p value, y axis)"；該條目內文也一致：−log10 p 值在縱軸、對數倍數變化在橫軸）。

## 與鄰近圖種的區別

| 圖種 | 橫軸 | 縱軸／內容 | 回答的問題 | 和 MA 圖的差別 |
|---|---|---|---|---|
| **火山圖**（`volcano-plot.md`） | 變化幅度（常用 log2 倍數變化） | 顯著性（−log10 p 值或 q 值） | 變多大、證據多強，用於候選排序 | 橫軸是效應量、縱軸是顯著性；MA 圖橫軸是平均豐度，用於診斷 |
| **曼哈頓圖**（`manhattan-plot.md`） | 基因組位置 | −log10(p) | 關聯訊號落在基因組哪一段 | MA 圖橫軸是平均表現量，不是位置 |
| **一般散點圖**（`correlation-scatter.md`） | 任意數值 | 任意數值 | 兩變數關係 | MA 圖兩軸語意固定為 A × M |
| [**Bland–Altman 圖**](bland-altman.md) | 兩種量測的平均（原尺度） | 兩種量測的差（原尺度），常畫平均差與 ±1.96 個標準差 | 兩種量測方法的一致性 | MA 圖是它在基因體資料上的應用，建立在對數尺度上（"This version of the plot is used in MA plot."；「MA 是 Bland–Altman 的對數版」為維基百科敘述，延伸解釋屬推論） |
| **RA 圖** | A：平均 | R：對數比值（和 M 一樣放縱軸） | 整數計數資料的雙條件比較 | 只用於非負整數計數，用 ε 納入單邊為零的點，呈箭頭狀（見上「三個事實」第 2 條） |
| **Circos**（`circos.md`） | 環狀多軌 | 多種軌道與連結 | 比較基因體、多軌關係 | Circos 是環狀多軌視覺化，MA 圖是診斷用散點圖 |

判斷口訣：**橫軸平均表現、縱軸對數倍數 → MA 圖；橫軸倍數、縱軸顯著性 → 火山圖；橫軸位置 → 曼哈頓圖；兩種量測方法的一致性 → [Bland–Altman 圖](bland-altman.md)；任意兩變數 → 一般散點圖。**

## Avoid

- 把橫軸當成基因組位置或 −log10(p)
- 只拿 \|M\| 大就當顯著：顏色代表的是檢定結果還是你自訂的門檻要分清（biostatsquid 的粉紅點只是 \|M\|>1，沒有統計檢定）
- 把「以 M＝0 為中心」當定律：它是「多數基因沒有差異」的假設；預期整體全面位移時，點雲不在零線上未必是錯
- 以為 `lfcShrink` 會讓顯著點消失，或把收縮後的倍數當真值
- 把火山圖的軸寫反（見上）；把 RA 圖說成軸語意不同；說 limma 廢除了 `plotMA`（實際是 `plotMD` 功能相同、參數略異，為現行文件主推）
- 對數底數不一致：教學用 `log1p`（依 R 的一般定義是自然對數，推論）卻稱 log2 倍數
- 低計數區的對角線離散條紋當成生物學訊號（低整數計數的比值只能取有限數值，推論）
- 事後為視覺效果任意改倍數門檻；把微陣列「A 愈高 \|M\| 愈大」和計數資料的漏斗形混為一談（不同資料型態）
- 模擬資料與真實資料不分；圖內留程式碼、變數名或缺軸標題（NotchBio 的圖有這些問題，本課不嵌）

## Produce checklist

- [ ] 故事句是「在什麼豐度層級上變、正規化或收縮是否異常」（診斷）；要候選排序 → 火山圖
- [ ] 表：每列一個特徵；有 A（`baseMean`、平均正規化計數或平均對數強度）與 M（`log2FoldChange`）；要著色另有 p 值或校正後 q 值；對比方向寫進圖說
- [ ] 橫軸寫明 A 是什麼、是否對數刻度；縱軸寫明 M 的底數（log2）；畫 M＝0 線；軸標題寫人話，不留程式變數名
- [ ] 顏色意義寫進圖例：檢定結果（哪一種 p 值、多少門檻）還是單純 \|M\| 門檻；門檻為範例，不是標準，事先定好
- [ ] 收縮前後並陳時，圖說寫明收縮方法（apeglm、normal、ashr）與「收縮不改 p 值（推論）」
- [ ] 讀圖順序：點雲是否大致以 M＝0 為中心 → 低 A 區喇叭口寬度 → 顯著點落在哪一段豐度 → 才送去驗證或路徑分析
- [ ] 極端倍數若集中在極低表現，優先採信經收縮或過濾後的估計；精確 q 值與倍數另附表格
- [ ] 圖注：「橫軸不是基因組位置，也不是 −log10(p)；愈右表示平均表現愈高，上下才是倍數方向」
- [ ] 工具誠實（只寫素材包證實的；版本為 2026-09-29 查核值）：
  - **DESeq2**（R，Bioconductor 1.52.0，LGPL (>= 3)）：`plotMA`、`lfcShrink`（apeglm、normal、ashr）
  - **limma**（Bioconductor，GPL (>=2)；頁面與手冊 3.68.5）：`plotMD`、`plotMA`；**edgeR**（GPL (>=2)；頁面與手冊 4.10.5）：`plotMD`，另有 `maPlot`、`plotSmear`（把倍數無限大的點「抹開」）
  - **geneplotter**（Artistic-2.0；`plotMA`，DESeq2 底層曾用）；**Glimma**（GPL-3，2.22.1；互動 `glimmaMA`，舊名 `glMDPlot`，兩者皆存在）
  - **apeglm**（GPL-2，1.34.0）、**ashr**（CRAN；授權未寫）：倍數收縮估計方法
  - **ggplot2**、**Matplotlib**：手作 MA 圖，授權素材包未寫，不代填
  - 教材授權（依終稿）：Galaxy Training、HBC 工作坊 CC BY 4.0；biostatsquid CC BY-NC-SA 4.0（非商業，第三方圖像除外）；NotchBio 頁尾 All rights reserved，不可自由再用
  - R Graph Gallery、Python Graph Gallery、From Data to Viz、Dataviz Catalogue、Dataviz Project 均無 MA 圖專頁
- [ ] 示範數字標「數字未核」
- [ ] 自檢：橫軸是平均表現嗎？縱軸是對數倍數嗎？顏色是檢定結果嗎？是否把「以零為中心」當成了定律？

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-ma-fictional.csv` — 3,000 列（約 230 KB）；檔頭兩行以 `#` 開頭，讀取要略過（pandas 用 `comment='#'`）；欄位 `gene_id, gene_name, base_mean, a_log2_mean, m_log2fc, m_log2fc_shrunk, lfc_se, pvalue, padj, sim_true_de`。基因名 `fakegene1…` 不是真實基因；`base_mean` 約 1 至 10⁵（對數刻度均勻）；`a_log2_mean` ＝ log2(base_mean + 1)；`m_log2fc` 是收縮前的虛構倍數；`m_log2fc_shrunk` 是**示意收縮**（低計數者被拉向零，**不是 apeglm 的輸出**）；`lfc_se` 計數愈低愈大；`padj` 為在 3,000 個虛構 p 值上做 Benjamini–Hochberg 校正；`sim_true_de` 標示產生資料時是否放入真實差異。
- 我重新數過：padj < 0.05 共 197 列、padj < 0.1 共 218 列；\|m_log2fc\| > 1 共 324 列，其中 padj < 0.05 且 \|M\| > 1 共 150 列；`sim_true_de`＝1 共 328 列（約 11%；素材包寫「約 12%」，以實際計數為準）；base_mean < 10 的 621 列 M 標準差約 0.98，base_mean > 1000 的 1,156 列約 0.58（低表現處散得較開，即喇叭口）。
- 示範讀法：橫軸 `a_log2_mean`（或 log10(base_mean)），縱軸 `m_log2fc` 或 `m_log2fc_shrunk`，padj < 0.1 的點著色，畫 M＝0 線（門檻為範例，不是標準）。先畫收縮前再畫收縮後，比較低 A 區的極端點；注意示意收縮只動 M、不動 padj，兩張圖的著色點是同一批。同一份資料也可畫火山圖（縱軸 −log10 padj），對照兩張圖各回答什麼。
- `sample-ma-selfcheck.py` — 自檢腳本（見 `examples/data/README.md`）。

## 參考連結（可點；皆出自素材包 sources.txt 且標可開）

- https://en.wikipedia.org/wiki/MA_plot （定義原文、正規化前後經典圖）
- https://en.wikipedia.org/wiki/Bland%E2%80%93Altman_plot 、https://en.wikipedia.org/wiki/RA_plot （鄰近圖種）
- https://en.wikipedia.org/wiki/Volcano_plot_(statistics) 、https://en.wikipedia.org/wiki/Manhattan_plot 、https://en.wikipedia.org/wiki/Scatter_plot
- https://commons.wikimedia.org/wiki/Category:MA_plot 、https://commons.wikimedia.org/wiki/File:MaPlot-edgeR.smear-wikipedia.png （edgeR smear 圖檔說明頁）
- https://www3.stat.sinica.edu.tw/statistica/j12n1/j12n16/j12n16.htm （Dudoit 等人 2002）
- https://pmc.ncbi.nlm.nih.gov/articles/PMC100354/ （Yang 等人 2002）
- https://pmc.ncbi.nlm.nih.gov/articles/PMC4402510/ （Ritchie 等人 2015，limma）
- https://pmc.ncbi.nlm.nih.gov/articles/PMC4302049/ （Love 等人 2014，DESeq2）
- https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html 、https://www.bioconductor.org/packages/release/bioc/html/DESeq2.html 、https://bioconductor.org/packages/release/bioc/manuals/DESeq2/man/DESeq2.pdf
- https://rdrr.io/bioc/geneplotter/man/plotMA.html （rdrr.io 為第三方快照）
- https://www.bioconductor.org/packages/release/bioc/html/limma.html 、https://rdrr.io/bioc/limma/man/plotMD.html 、https://bioconductor.org/packages/release/bioc/manuals/limma/man/limma.pdf 、https://bioconductor.org/packages/release/bioc/vignettes/limma/inst/doc/usersguide.pdf
- https://www.bioconductor.org/packages/release/bioc/html/edgeR.html 、https://rdrr.io/bioc/edgeR/man/plotMD.html 、https://bioconductor.org/packages/release/bioc/manuals/edgeR/man/edgeR.pdf 、https://bioconductor.org/packages/release/bioc/vignettes/edgeR/inst/doc/edgeRUsersGuide.pdf
- https://bioconductor.org/packages/release/bioc/html/Glimma.html
- https://biostatsquid.com/how-to-interpret-ma-plots/ 、https://biostatsquid.com/ma-plots-easy-r-tutorial/ （**注意其比較表把火山圖軸寫反，勿抄**）
- https://notchbio.app/blog/how-to-make-volcano-plots-ma-plots-rna-seq-r/ （火山圖 vs MA 圖；"reveals the true pattern" 為過度宣稱；站方保留所有權利，本課不嵌其圖）
- https://hbctraining.github.io/DGE_workshop/lessons/05_DGE_DESeq2_analysis2.html
- https://training.galaxyproject.org/training-material/topics/transcriptomics/tutorials/rna-seq-counts-to-genes/tutorial.html
- 查核限制（未核；僅記名、不列連結）：R Graph Gallery `ma-plot.html`、Python Graph Gallery `ma-plot/`、From Data to Viz `graph/ma.html`、Dataviz Catalogue `methods/ma_plot.html`、Dataviz Project `data-type/ma-plot/`、Wikimedia Commons `Category:MA_plots`（複數）、rdrr.io 的 `limma/man/plotMA.html`（以上 7 條皆 404；終稿只以路徑名稱提及，不作為來源）

X 教學原帖：素材包指出以 MA plot、plotMA、DESeq2、tutorial 等關鍵字檢索，只找到 OmicsLogic 工作坊招生貼文，沒有可當教材的原帖；不引用、不編造。

鄰居 pattern：`volcano-plot.md`（橫軸效應量、縱軸顯著性；候選排序）、`manhattan-plot.md`（橫軸基因組位置）、`correlation-scatter.md`（任意兩變數）、`circos.md`（環狀多軌）、`qq-plot.md`（分位數對分位數；不看倍數）、`bland-altman.md`（兩種量測方法的一致性；用途不同，不是同一種圖）；RA 圖為 MA 圖的整數計數版，於本 pattern 內說明。

圖檔留在教圖／skill-pack（素材包 `images/`，24 張，圖說與終稿逐字相同），本 repo **不複製**大圖。可對照的圖：wiki-pre-norm-672／wiki-post-norm-672（微陣列正規化前後，真實資料，公有領域）、sim-anatomy、sim-classic-funnel、sim-pre-norm-bias、sim-post-norm、sim-shrink-before-after、sim-lfc-threshold-tests、sim-volcano-ma-side（皆為**模擬資料重繪**，數值僅供示意）、bsq-interpret-02／03（示意，資料來源頁面未說明）、bsq-r-02／03（airway 真實資料；粉紅只是 \|M\|>1，M 與 A 是 log1p，非 log2）、deseq2-01（未收縮）／deseq2-extra-02（apeglm 收縮後）／deseq2-02（三種收縮並排）、hbc-ma-unshrunken／hbc-ma-plot（收縮前後）、wiki-edger-smear、galaxy-mdsampleLA／LE、galaxy-mdvolplot_basalpregnant-basallactate（MD 圖與火山圖並排）；對照圖：contrast-bland-altman（原尺度，不是對數）、contrast-ra-orange（RA 圖，橫軸 A、縱軸 R）。對帳見 `ATTRIBUTION.md`。
