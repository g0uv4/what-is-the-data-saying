# Pattern: volcano-plot

> **圖種**：火山圖（Volcano plot）
> **來源（納茲教圖）**：`teach-viz/2026-09-28-pm-volcano.md`（方法教學；正式課程）
> **亦稱**：差異表現火山圖；英文維基百科條目名 Volcano plot (statistics)（英文單說 volcano 也可能指真正的火山——讀軸比讀名字重要）
> **定義（英文維基百科原文）**："In statistics, a volcano plot is a type of scatter-plot that is used to quickly identify changes in large data sets composed of replicate data." "It plots significance versus fold-change on the y and x axes, respectively."
> **核心**：**每個點＝一個受測特徵**（基因、蛋白質、代謝物、胜肽…）；**橫軸＝效應量與方向**（多為 log2 倍數變化：右＝上調、左＝下調、近 0＝幾乎沒變）；**縱軸＝統計證據強度**（−log10 原始 p 值，或 −log10 校正後 p 值——**兩者意思不同，圖上要寫明畫哪一種**）；底部中央堆滿變化小、證據弱的點，往左上、右上長出兩翼
> **原始文獻**：Cui 與 Churchill，*Genome Biology* 2003；Li，*Journal of Bioinformatics and Computational Biology* 2012

## When

- 兩組（或一組明確對比，例：處理組對控制組）的**差異檢定結果表**：每列一個特徵，至少有特徵名、效應量（log2 倍數變化）、原始或校正後 p 值
- 特徵數量大（轉錄體、蛋白質體、代謝體、脂質體等上千到上萬個特徵）的差異篩選
- 要同時看「變化方向」「變化幅度」「證據強度」，把候選名單排出優先順序
- 教學：說明「倍數很大但 p 值很差」「p 值很小但倍數幾乎為 0」都不能只看單一指標下結論

## Recommend

- **主選**：火山圖（橫軸 log2 倍數變化、縱軸 −log10 p 值；分析前定好的門檻畫成虛線：水平＝顯著性、兩條垂直＝倍數）
- **著色**：三色（上調／下調／未過門檻）或四色（未過門檻／只過倍數／只過 p 值／兩者都過；EnhancedVolcano 預設）
- **標籤**：只標要討論的特徵（兩門檻都過、p 值最小的前幾名或指定基因），加引線避免重疊；互動版用懸停看細節
- **並列**：旁邊放 MA 圖，看表現量層級偏差
- **門檻範例（均出自來源原文；範例，不是標準）**：

| 來源 | 縱軸或門檻所用 p 值 | p 值門檻 | 倍數門檻 |
|---|---|---|---|
| MetwareBio（"Common cutoffs (example)"） | 校正後 q 值 | q < 0.05 | \|log2 倍數變化\| ≥ 1 |
| 哈佛陳曾熙公共衛生學院生物資訊核心教學 | 校正後 p 值 | < 0.05 | \|log2 倍數變化\| ≥ 0.58（約 1.5 倍） |
| Galaxy 訓練教材 | 縱軸原始 p 值、著色用偽發現率 | 偽發現率 < 0.01 | 0.58 |
| biostatsquid 教學 | 原始 p 值 | < 0.05 | \|log2 倍數變化\| > 0.6 |
| EnhancedVolcano 函式預設（以套件手冊為準） | 快速範例縱軸為原始 p 值 | pCutoff 1e-05 | FCcutoff 1 |

  上表是**範例，不是標準**：門檻要依實驗設計、樣本數、檢定力與驗證成本在分析前決定。註：EnhancedVolcano 說明文件內文寫預設倍數門檻 "log2FC is >|2|"，與手冊 FCcutoff = 1 矛盾，快速範例圖的垂直線也在 ±1，以手冊為準。

- **備選（何時改用哪一種）**：
  - 訊號落在哪條染色體、哪個區段 → **曼哈頓圖**（Manhattan plot；`manhattan-plot.md`）或區域放大圖
  - 診斷低表現量特徵的倍數估計是否不穩、收縮或正規化是否偏差 → **MA 圖**（`ma-plot.md`；NotchBio："An MA plot in RNA-seq is primarily a diagnostic view, while a volcano plot is primarily a results-summary view."）
  - 只有原始計數矩陣、還沒做檢定 → 先做差異分析；火山圖不是任意兩欄交叉探索的圖（任意兩變數 → 一般散點 `correlation-scatter.md`）
  - 超過兩組又沒有明確對比 → 按每組對比分別畫，或改用多組比較方法
  - 讀者要精確名次、靜態標籤擠成一團 → 附可排序表格或互動版
  - 要畫地形或高程 → 地圖工具，不是本圖

## 與鄰近圖種的區別

| 圖種 | 橫軸 | 縱軸 | 核心問題 | 和火山圖的差別 |
|---|---|---|---|---|
| **一般散點圖**（`correlation-scatter.md`） | 任意數值變數 | 任意數值變數 | 兩變數是否相關 | 火山圖兩軸語意固定（效應量對比顯著性），不是任選兩欄 |
| **曼哈頓圖**（`manhattan-plot.md`） | 基因體座標（染色體位置） | 多為 −log10(p) | 關聯訊號落在哪個區段 | 縱軸可能相同，但橫軸是位置不是倍數；外形像城市天際線，不是向兩翼展開 |
| **MA 圖**（`ma-plot.md`；M＝對數比值，A＝平均值） | 平均表現量 | 對數倍數變化 | 變化發生在哪個表現量層級、收縮與正規化是否偏差 | 倍數在縱軸、沒有顯著性軸；偏診斷，火山圖偏結果摘要 |
| **地形等高線圖**（contour line map；repo 尚無專檔） | 地理座標 | 地理座標（高程線） | 地形高低 | 只是「火山」名稱偶合；也不同於統計等高線圖（二維密度，`contour-density.md`） |
| **Circos**（`circos.md`） | 環狀參考軸 | 同心多軌 | 沿基因體的多層訊號與對位 | 環狀多軌的比較基因體視覺化；火山圖是差異分析的優先排序圖 |

判斷口訣：**橫軸倍數＋縱軸顯著性 → 火山圖；橫軸位置 → 曼哈頓圖；橫軸平均表現量、縱軸倍數 → MA 圖；任意兩變數 → 一般散點圖；環狀多軌 → Circos。**

## Avoid

- 圖上沒寫縱軸是原始還是校正後 p 值，或縱軸標籤與實際畫的欄位不一致；縱軸畫原始 p 值、門檻卻用校正後 p 值（Galaxy、EnhancedVolcano 有此做法）時圖說沒寫明
- 把某個來源的門檻（0.05、1、0.58…）當「標準」，或分析後為了結果好看改門檻（MetwareBio 稱 "Threshold hacking"）
- 只看高度（p 值）或只看左右（倍數）下結論，忽略「倍數大但不顯著」「很顯著但倍數近 0」兩類陷阱
- 上萬個特徵只用原始 p 值篩選、沒做多重檢定校正（哈佛教學："if we test 20,000 genes for differential expression, at p < 0.05 we would expect to find 1,000 genes by chance."）
- 沒寫對比方向，讀者不知道右側「上調」是相對於誰
- 標籤貼滿全圖互相遮蔽；要精確數值時沒附表格
- 把曼哈頓圖、MA 圖或任意兩欄散點叫成火山圖；或把地形圖的「火山」搞混
- 把 EnhancedVolcano 說明文件內文的 "log2FC is >|2|" 當預設值（手冊預設 FCcutoff 1）

## Produce checklist

- [ ] 故事句是「差異候選的優先排序」；要看染色體位置 → 曼哈頓圖（`manhattan-plot.md`）；要看表現量層級偏差 → 改看或並列 MA 圖（`ma-plot.md`）
- [ ] 表：每列一個特徵；有 log2 倍數變化、原始 p 值和／或校正後 p 值（寫明校正法，例：Benjamini–Hochberg）；對比方向（誰相對於誰、誰是對照組）寫進圖說
- [ ] 縱軸選原始或校正後 p 值並寫在軸標題；門檻用的 p 值若與縱軸不同，圖說寫明
- [ ] **分析前**定好倍數與顯著性門檻（範例，不是標準），畫水平與垂直虛線；不事後改門檻
- [ ] 著色三色或四色，圖例寫門檻值
- [ ] 標籤只標要討論的特徵、加引線；互動版懸停
- [ ] 判讀順序：左上、右上兩翼 → 檢查兩類陷阱 → 才送路徑富集或實驗驗證；精確數值附表
- [ ] 圖注：「橫軸不是基因體座標；縱軸愈高代表證據愈強，不是表現量本身」
- [ ] 工具誠實（只寫素材包證實的；版本為 2026-09-28 查核值）：
  - **EnhancedVolcano**（Bioconductor；Kevin Blighe、Sharmila Rana、Myles Lewis 開發，維護者 Jared Andrews）：專為發表設計的 R 套件、四色預設；1.30.0（Bioconductor 3.23）；**GNU GPL 第 3 版**
  - **ggplot2＋ggrepel**（R）：自行組裝散點、門檻線與分類著色（biostatsquid、NotchBio、哈佛教學示範）
  - **DESeq2**（上游差異分析；`lfcThreshold` 可在檢定時設倍數門檻）、**apeglm**（繪圖前收縮倍數估計；NotchBio 建議）
  - **Plotly Python**（Dash Bio VolcanoPlot 元件，互動）；**R 語言版專頁不存在**
  - **Galaxy** 平台與訓練教材（網頁介面產生並標註前幾名或自訂基因）
  - **Orange**：研究時有火山圖圖元文件頁，今天已轉址到文件首頁（未核）
  - **Seaborn、Matplotlib**：沒有火山圖專屬範例，用一般散點自行組裝
  - 除 EnhancedVolcano 外，素材包未寫授權，不代填；R Graph Gallery、From Data to Viz、Dataviz Catalogue 沒有火山圖專頁
- [ ] 示範數字標「數字未核」
- [ ] 自檢：兩軸真的是「效應量 × 顯著性」嗎？縱軸寫清楚是哪種 p 值嗎？門檻是分析前定的嗎？

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-volcano-de-results.csv` — 50 列，欄位 `feature_id, log2_fold_change, p_value, p_adjusted_bh, neg_log10_p, neg_log10_padj, category`；`FAKE001`–`FAKE050` 不對應任何真實基因；正倍數＝處理組相對控制組上調；`p_adjusted_bh` 是在這 50 列內以 Benjamini–Hochberg 法計算；`neg_log10_p`、`neg_log10_padj` 都可當縱軸。`category` 依範例門檻（|log2 倍數變化| ≥ 1、校正後 p 值 < 0.05；**範例，不是標準**）分五類：上調（過雙門檻）8、下調（過雙門檻）7、只過校正後p值門檻 12、只過倍數門檻 4、未過門檻 19。
- 示範讀法：橫軸 `log2_fold_change`、縱軸 `neg_log10_padj`，依 `category` 著色。先看兩翼（例：FAKE014、FAKE022 在右上最高，FAKE013、FAKE025 在左上）；再看陷阱——FAKE027（倍數 −3.761 但校正後 p ≈ 0.12，倍數大但不顯著）、FAKE016（校正後 p ≈ 4e-09 但倍數 −0.132，很顯著但近 0）。把縱軸換成 `neg_log10_p` 時圖說要跟著改。

## 參考連結（可點；皆出自素材包 sources.txt 且標可開）

- https://en.wikipedia.org/wiki/Volcano_plot_(statistics) （定義原文、代謝體示例圖）
- https://en.wikipedia.org/wiki/MA_plot 、https://en.wikipedia.org/wiki/Manhattan_plot （鄰近圖種定義）
- https://en.wikipedia.org/wiki/Contour_line （地形等高線；名稱偶合對照）
- https://doi.org/10.1186/gb-2003-4-4-210 、https://pubmed.ncbi.nlm.nih.gov/12702200/ 、https://europepmc.org/article/PMC/PMC154570 （Cui 與 Churchill 2003）
- https://doi.org/10.1142/S0219720012310038 （Li 2012；sources.txt 註：出版社頁需瀏覽器 cookie）、https://pubmed.ncbi.nlm.nih.gov/23075208/
- https://doi.org/10.1038/ng766 （Jin 等人 2001，維基百科條目引用；經 cookie 檢查轉址）
- https://doi.org/10.1016/j.compbiolchem.2013.02.003 （Li 等人 2014，全基因體關聯研究延伸用法）
- https://bioconductor.org/packages/release/bioc/html/EnhancedVolcano.html （版本、授權、開發者）
- https://bioconductor.org/packages/release/bioc/vignettes/EnhancedVolcano/inst/doc/EnhancedVolcano.html （說明文件第 3.1、4.2、4.5、4.11 節）
- https://bioconductor.org/packages/release/bioc/manuals/EnhancedVolcano/man/EnhancedVolcano.pdf （手冊：pCutoff 1e-05、FCcutoff 1）
- https://github.com/kevinblighe/EnhancedVolcano
- https://plotly.com/python/volcano-plot/ （Dash Bio VolcanoPlot）
- https://biostatsquid.com/volcano-plot/ 、https://biostatsquid.com/volcano-plots-r-tutorial/ 、https://biostatsquid.com/ma-plots-easy-r-tutorial/
- https://notchbio.app/blog/how-to-make-volcano-plots-ma-plots-rna-seq-r/ （火山圖 vs MA 圖）
- https://www.metwarebio.com/volcano-plot-metabolomics-proteomics-guide/ （代謝體／蛋白體；"Threshold hacking"）
- https://training.galaxyproject.org/training-material/topics/transcriptomics/tutorials/rna-seq-viz-with-volcanoplot/tutorial.html 、https://training.galaxyproject.org/training-material/topics/transcriptomics/tutorials/rna-seq-counts-to-genes/tutorial.html
- https://hbctraining.github.io/DGE_workshop/lessons/05_DGE_DESeq2_analysis2.html （MA 圖、校正後 p 值）、https://hbctraining.github.io/DGE_workshop/lessons/06_DGE_visualizing_results.html （火山圖）
- https://r-graph-gallery.com/101_Manhattan_plot.html （曼哈頓圖對照）
- https://seaborn.pydata.org/examples/index.html 、https://matplotlib.org/stable/gallery/index.html （無火山圖專屬範例）
- 查核限制（未核；僅記名、不列連結）：Plotly R 語言火山圖頁（404，頁面不存在）；Dataviz Project 火山圖頁（研究時 403、今天重測 404）；Orange 視覺化程式設計文件的火山圖圖元頁（docs.biolab.si，今天轉址到 Orange 文件首頁，原頁內容已不在）；Orange 圖元目錄火山圖頁、EnhancedVolcano 作者個人網站說明頁、R Graph Gallery／From Data to Viz／Dataviz Catalogue 火山圖或方法頁、MetwareBio 兩個舊網址（皆 404）；英文維基百科 MA 圖原圖（研究時限流未下載）

X 教學原帖：本輪查無（搜尋結果多為模板化產品宣傳與工作坊廣告；不引用、不編造）。

鄰居 pattern：`correlation-scatter.md`（任意兩變數）、`contour-density.md`（統計等高線＝二維密度，與「火山」名稱無關）、`circos.md`（環狀多軌比較基因體）、`manhattan-plot.md`（橫軸基因組位置、縱軸 −log10(p)）、`ma-plot.md`（橫軸平均表現、縱軸倍數；診斷）、`qq-plot.md`（分位數對分位數；看 p 值整體分布，不是候選排序）；地形等高線圖尚無專檔。

圖檔留在教圖／skill-pack（`/workspace/skill-packs/2026-09-28-pm-volcano/images/`，22 張，圖說用 SKILL-PACK.md 修正後版本，其中 6 張審稿更正），本 repo **不複製**大圖。火山圖範例對照：wiki-volcano-eg、bsq-slide4（解讀示意）、bsq-basic → bsq-thresholds → bsq-colour → bsq-fullplot（逐步）、enhancedvolcano-02／04／07／12、notch-volcano-labeled、metware-metabolomics、metware-proteomics、galaxy-volcanoplot、galaxy-volcanoplot_top10、plotly-thumb。對照圖：notch-what-they-show、notch-combined-volcano-ma、hbc-ma-plot（MA 圖）、wiki-manhattan-sp（曼哈頓圖）、contrast-topo-contour（地形等高線，**與統計火山圖無關**）。bsq-slide3 是情境投影片，**圖中沒有火山圖**。對帳見 `ATTRIBUTION.md`。
