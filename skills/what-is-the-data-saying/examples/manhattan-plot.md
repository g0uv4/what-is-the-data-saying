# Pattern: manhattan-plot

> **圖種**：曼哈頓圖（Manhattan plot）
> **來源（納茲教圖）**：`teach-viz/2026-09-29-am-manhattan.md`（方法教學；正式課程）
> **亦稱**：全基因組關聯分析曼哈頓圖；英文固定寫法 Manhattan plot。名稱來自外形像紐約曼哈頓天際線（英文維基百科原文："It gains its name from the similarity of such a plot to the Manhattan skyline"）
> **定義（英文維基百科原文）**："In GWAS Manhattan plots, genomic coordinates are displayed along the x-axis, with the negative logarithm of the association p-value for each single nucleotide polymorphism (SNP) displayed on the y-axis, meaning that each dot on the Manhattan plot signifies an SNP." "The different colors of each block usually show the extent of each chromosome."
> **核心**：**每個點＝一個受測遺傳標記**（最常見是單核苷酸多型性 SNP）；**橫軸＝基因組位置**（先依染色體 1、2、3……由左至右，再依染色體內鹼基位置；相鄰染色體交替著色）；**縱軸＝−log10(p)**（p 愈小點愈高；p＝10⁻⁸ 對應 y＝8）；大多數點貼底、少數區段堆成尖塔，像天際線；水平線＝事先約定的門檻
> **一句話**：橫軸不是倍數變化；縱軸愈高表示 p 愈小，不是效應量本身

## When

- 全基因組關聯分析（GWAS）或高密度標記關聯掃描的摘要表：每個標記一列，至少有標記編號、染色體、位置、p 值（效應量、等位基因頻率常另附，不一定畫進基本圖）
- 要同時回答「訊號在哪一號染色體、哪一段」與「證據有多強」
- 事先約定門檻，用水平線標出過線尖塔、決定哪些區段送去 LocusZoom 圖放大
- 當全基因組導覽圖，和 QQ 圖、LocusZoom 圖（區域關聯圖）、效應量[森林圖](forest-plot.md)搭配

## Recommend

- **主選**：線性曼哈頓圖（論文主圖、簡報）
- **變體（同一家族，要標清）**：
  - **環狀曼哈頓圖**（常見於 CMplot）：染色體排成圓周、徑向高度＝−log10(p)，多圈同心可並陳多個性狀；**仍只是 −log10(p) 峰值，不是 Circos**
  - **邁阿密圖（Miami plot）**：上下兩張曼哈頓圖鏡像對照，比較兩個性狀或兩組結果（miami_generator 說明檔原文："Miami plots (which are a combination of two Manhattan plots into a single image, showing the results from two distinct group)"）；只當變體，不另開 pattern
  - **互動版**（Dash Bio `dash_bio.ManhattanPlot`；會議當場查位點，滑鼠停留看標記編號與精確 p 值）
  - **單一染色體或區域裁切**：仍是位置 × −log10(p)，視野縮小，介於總覽與完整 LocusZoom 圖之間
  - **標註策略**：只標過門檻的峰值、只標候選基因名，或只標指定位點
- **門檻範例（範例，不是標準）**：

| p 值門檻 | −log10(p) | 出現在哪裡 | 性質 |
|---|---|---|---|
| 5×10⁻⁸ | ≈7.30 | 人類全基因組關聯分析慣用的全基因組顯著門檻；qqman、manhattanly 紅線預設；Dash Bio `genomewideline_value` 預設 | 範例，不是標準（依研究設計與多重檢定策略事先約定） |
| 1×10⁻⁵ | 5 | qqman、manhattanly 的提示性門檻（藍線）預設值；**學術出處未核**，只能說是工具預設值 | 範例，不是標準 |
| 1×10⁻⁶ | 6 | CMplot 示例圖 cmplot-4_1 的實線（示例刻意設定） | 範例，不是標準 |
| 1×10⁻⁴ | 4 | CMplot 示例圖 cmplot-4_1 的虛線（示例刻意設定） | 範例，不是標準 |
| 0.05 | ≈1.30 | 火山圖對照圖的紅色虛線（是火山圖，不是曼哈頓圖） | 範例，不是標準 |

  5×10⁻⁸ 的依據：英文維基百科 Genome-wide significance 條目原文 "The most commonly accepted threshold is p < 5 × 10⁻⁸, which is based on performing a Bonferroni correction for all the independent common SNPs across the human genome."；估算依據之一是 Pe'er 等人 2008 年論文（約一百萬次獨立檢定；0.05 ÷ 1,000,000＝5×10⁻⁸，算術已核；PubMed 頁本輪打不開，見查核限制）。換算 −log10(5×10⁻⁸)≈7.30、−log10(1×10⁻⁵)＝5（算術已核）。

- **備選（何時改用哪一種）**：
  - 要看「變多大、往哪邊變」的差異排序 → **火山圖**（`volcano-plot.md`）
  - 要看整體 p 值是否系統性膨脹 → **分位數－分位數圖（QQ 圖）**（`qq-plot.md`；常搭配基因組膨脹係數 λ）
  - 要看單一峰值附近的基因與連鎖不平衡 → [**LocusZoom 圖（區域關聯圖）**](locuszoom.md)
  - 沒有染色體與位置欄、只有任意兩欄數字 → 一般散點（`correlation-scatter.md`），不是曼哈頓圖
  - 只有少數事先選定的候選位點 → 表格或簡單點圖
  - 環狀多軌比較基因體故事 → **Circos**（`circos.md`）

## 與鄰近圖種的區別

| 圖種 | 橫軸 | 縱軸／內容 | 回答的問題 | 和曼哈頓圖的差別 |
|---|---|---|---|---|
| **火山圖**（`volcano-plot.md`） | 效應量（常用 log2 倍數變化） | −log10(p) | 變多大、往哪邊變、證據多強 | 縱軸相同，橫軸是效應量；外形是左右兩翼，不是天際線 |
| **一般散點圖**（`correlation-scatter.md`） | 任意數值 | 任意數值 | 兩變數關係 | 曼哈頓圖兩軸意義固定為染色體座標 × −log10(p) |
| **分位數－分位數圖（QQ 圖）**（`qq-plot.md`） | 期望 −log10(p) | 觀察 −log10(p) | 整體 p 值分佈是否校準、是否膨脹（常搭配 λ） | 不看位置；是曼哈頓圖的配套檢查圖 |
| **MA 圖**（`ma-plot.md`） | 平均表現 A | 對數倍數 M | 在什麼豐度層級上變、正規化或收縮是否異常 | 橫軸是平均表現量不是位置，沒有顯著性軸，偏診斷 |
| **Circos**（`circos.md`） | 環狀多軌 | 多種軌道與連結 | 比較基因體、多軌關係 | 環狀曼哈頓圖仍只是 −log10(p) 峰值，不是 Circos 的多軌連結故事 |
| [**LocusZoom 圖（區域關聯圖）**](locuszoom.md) | 單一區段的染色體位置 | −log10(p)，依與指標標記的 r² 著色，下方基因軌 | 峰值附近的連鎖不平衡與基因 | 曼哈頓圖找到尖塔之後的下一步，不是全基因組總覽 |
| **邁阿密圖**（變體） | 基因組位置 | 上下兩張曼哈頓圖鏡像 | 兩個性狀或兩組結果比較 | 屬曼哈頓圖變體，不另開 pattern |
| [染色體核型示意圖](karyotype-ideogram.md) | — | 染色體外觀與帶紋 | 染色體結構 | 沒有 −log10(p) 峰值，不是曼哈頓圖 |

判斷口訣：**橫軸位置＋縱軸 −log10(p) → 曼哈頓圖；橫軸倍數 → 火山圖；期望對觀察 → QQ 圖；單一區段＋r² 著色＋基因軌 → [LocusZoom 圖（區域關聯圖）](locuszoom.md)；上下鏡像兩性狀 → 邁阿密圖；環狀多軌＋連結 → Circos。**

## Avoid

- 把倍數變化或效應量放上橫軸（那是火山圖）；把縱軸高度當效應量大小（縱軸是證據強度）
- 軸標題留程式變數名（例：原圖的「BPcum」「minuslog10pvalue」），或染色體從 0 起算（「ch-0」）
- 門檻線不寫數值，或事後為了好看改門檻；把某個工具預設值當「標準」
- 只看曼哈頓圖就宣布滿天峰值都是真實訊號，沒有並讀 QQ 圖檢查膨脹（整條觀察線系統性抬高 → 先排查族群分層等偏差）
- 把孤立的單一高點當可靠訊號（可靠訊號通常是一簇相鄰標記一起升高）
- 標籤塞滿整張圖互相重疊
- 把環狀曼哈頓圖叫成 Circos；把邁阿密圖當另一種主圖
- 模擬資料與真實資料不分；同一份資料同一種圖放兩張
- 引用錯論文的圖：區域關聯圖範例要來自 LocusZoom 論文本身（Pruim 等人 2010，PMC2935401）；先前誤植的 PMC3605911 是病毒系統動力學論文，與 LocusZoom 無關，**已排除**
- 原圖刻度有疑問卻不註明（例：火山圖對照圖最底刻度標為 6.68）
- 把 manhattanly 當成目前可從 CRAN 安裝的套件（已下架，見工具誠實）

## Produce checklist

- [ ] 故事句是「全基因組關聯訊號落在哪裡、多強」；不是 → 火山圖、QQ 圖或 LocusZoom 圖
- [ ] 表：標記編號、染色體、位置、p 值；性狀定義、樣本設計、多重檢定策略寫進圖說
- [ ] 縱軸 −log10(p)；若用校正後 p 值或 q 值，圖說寫明是哪一欄
- [ ] **事先**約定門檻（範例，不是標準）並畫水平線、標數值；不事後改
- [ ] 橫軸依染色體 1、2、3……排列（從 1 起算），依位置排序後累加當橫座標，相鄰染色體交替著色；軸標題寫人話（例「染色體（基因組位置）」「−log10(P)」）
- [ ] 標籤只留要討論的峰值或候選基因；互動版用滑鼠停留補細節
- [ ] 依用途選線性（論文、簡報）、環狀（多性狀並陳）或互動版（會議當場查位點）；兩性狀比較可做邁阿密圖
- [ ] 同頁並陳 QQ 圖：大部分點貼近 y＝x、只有尾端上揚，再解讀尖塔（λ 接近 1 表示沒有明顯系統性膨脹；可接受範圍各研究不同，未核）
- [ ] 鎖定尖塔後另開 [LocusZoom 圖](locuszoom.md)（區域關聯圖）看連鎖不平衡與基因軌；精確 p 值、效應量、信賴區間另附表
- [ ] 工具誠實（只寫素材包證實的；版本為 2026-09-29 查核值）：
  - **qqman**（R，Stephen Turner）：`manhattan()`、`qq()`；0.1.9；**GPL-3**；手冊原文 suggestiveline "Default -log10(1e-5)"、genomewideline "Default -log10(5e-8)"
  - **CMplot**（R，YinLiLin）：線性、環狀、多性狀、標記密度條、QQ 圖；CRAN 4.5.1（GitHub 說明檔標 4.6.0）；**GPL (≥ 2)**
  - **manhattanly**（R，Plotly 互動曼哈頓圖與 QQ 圖）：GitHub 0.3.0、MIT；**已於 2025-06-13 自 CRAN 下架**（CRAN 頁原文 "Archived on 2025-06-13 as issues were not corrected despite reminders."）——只當歷史參考，**不推薦當目前工具**；R 互動需求改評估其他方案並自行確認可安裝
  - **Dash Bio `dash_bio.ManhattanPlot`**（Python，互動；MIT）；Plotly Python 曼哈頓圖頁即用它；Plotly R 版專頁不存在
  - **Matplotlib**（Python Graph Gallery 手工拼法：散點依染色體分組、自畫門檻線）、**ggplot2**（R Graph Gallery 自訂版）、**LocusZoom**（my.locuszoom.org、statgen/locuszoom；LocusZoom 圖）、**GWASTools**（Bioconductor）、**miami_generator**（Python，邁阿密圖）：素材包未寫授權與版本，不代填
- [ ] 圖說分標真實／模擬資料、門檻值、來源；示範數字標「數字未核」
- [ ] 自檢：橫軸真的是基因組位置嗎？門檻是事先定的嗎？看過 QQ 圖了嗎？

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**，以 Python 亂數產生，不代表任何真實研究）：

- `sample-manhattan-gwas.csv` — 6,427 列、22 條染色體，約 230 KB；欄位 `marker_id, chromosome, position, p_value, neg_log10_p`。`marker_id` 為虛構編號（fk00001 起，不是真實 rs 編號）；`chromosome` 從 1 起算；`position` 為虛構鹼基位置（染色體長度只取近似值）；`neg_log10_p` 已算好，直接當縱軸。
- 放了 3 個虛構峰：3 號染色體約 62.0 百萬鹼基（最高 −log10(p)≈9.41，fk01244）、11 號約 88.5 百萬鹼基（≈8.69，fk04235）、17 號約 41.2 百萬鹼基（≈7.62，fk05644）；超過 5×10⁻⁸ 的列數分別為 17、13、8。其他染色體為均勻隨機 p 值，沒有訊號。
- 示範讀法：依 `chromosome`、`position` 排序後累加位置當橫軸，`neg_log10_p` 當縱軸，染色體交替著色，畫 7.30（5×10⁻⁸）與 5（1×10⁻⁵）兩條範例門檻線（範例，不是標準）。先看三座尖塔落在 3、11、17 號，再確認每座都是一簇相鄰點一起升高而非孤立點；再用同一欄 p 值畫 QQ 圖檢查尾端上揚。

## 參考連結（可點；皆出自素材包 sources.txt 且標可開）

- https://en.wikipedia.org/wiki/Manhattan_plot （定義原文、經典圖）
- https://en.wikipedia.org/wiki/Genome-wide_association_study 、https://en.wikipedia.org/wiki/Genome-wide_significance （5×10⁻⁸ 門檻原文）
- https://en.wikipedia.org/wiki/Q%E2%80%93Q_plot 、https://en.wikipedia.org/wiki/Genomic_control （QQ 圖、膨脹係數 λ）
- https://en.wikipedia.org/wiki/Volcano_plot_(statistics) （火山圖對照）
- https://pmc.ncbi.nlm.nih.gov/articles/PMC2935401/ （Pruim 等人 2010，LocusZoom 論文；區域關聯圖正確出處；圖 1 為 CC BY-NC，僅限非商業）
- https://my.locuszoom.org/ 、https://github.com/statgen/locuszoom
- https://github.com/pgxcentre/miami_generator （邁阿密圖）
- https://cran.r-project.org/web/packages/qqman/index.html 、https://cran.r-project.org/web/packages/qqman/vignettes/qqman.html 、https://cran.r-project.org/web/packages/qqman/qqman.pdf 、https://github.com/stephenturner/qqman
- https://github.com/YinLiLin/CMplot 、https://cran.r-project.org/web/packages/CMplot/index.html 、https://cran.r-project.org/web/packages/CMplot/CMplot.pdf
- https://cran.r-project.org/web/packages/manhattanly/index.html （CRAN 下架公告：2025-06-13）；https://github.com/sahirbhatnagar/manhattanly 、https://sahirbhatnagar.com/manhattanly/ 、https://sahirbhatnagar.github.io/manhattanly/ （歷史參考，非目前推薦）
- https://plotly.com/python/manhattan-plot/ 、https://dash.plotly.com/dash-bio/manhattanplot （Dash Bio）
- https://r-graph-gallery.com/101_Manhattan_plot.html 、https://python-graph-gallery.com/manhattan-plot-with-matplotlib/
- https://www.ebi.ac.uk/gwas/ 、https://www.ebi.ac.uk/gwas/docs/about （GWAS Catalog）
- https://www.bioconductor.org/packages/release/bioc/html/GWASTools.html
- 查核限制（未核；僅記名、不列連結）：Pe'er 等人 2008 年論文 PubMed 頁（203，需 Cookie 的驗證頁，取不到內文；引句依終稿）；Plotly R 語言曼哈頓圖頁（單數、複數網址皆 404）與 Python 複數網址（404）；Python Graph Gallery 舊曼哈頓頁、stephenturner.github.io 的 qqman 頁、Bioconductor 上的 qqman 頁、CRAN 的 CMplot 說明文件頁、manhattanly CRAN 說明文件頁（下架後不存在）（皆 404）；rdocumentation CMplot 頁（502）；From Data to Viz 曼哈頓頁、Dataviz Catalogue 曼哈頓頁與方法索引、Dataviz Project 曼哈頓頁（皆 404；終稿記 Dataviz Project 為拒絕存取，今天為 404）；英文維基百科 Miami plot、LocusZoom 條目（404，不存在）；EBI GWAS 課程曼哈頓圖頁、哈佛 Intro-to-GWAS 課程首頁與視覺化單元（404）；Getting Genetics Done 2011 年曼哈頓圖文章（可開但內容已被換成無關廣告，不當教材）
- 已排除：PMC3605911（〈Viral Phylodynamics〉，與 LocusZoom 無關）

X 教學原帖：本輪查無（搜尋結果主要是工作坊招生推廣；不引用、不編造）。

鄰居 pattern：`volcano-plot.md`（橫軸效應量）、`ma-plot.md`（橫軸平均表現、縱軸倍數；診斷）、`circos.md`（環狀多軌，≠ 環狀曼哈頓圖）、`correlation-scatter.md`（任意兩變數）；`qq-plot.md`（配套：期望對觀察 −log10(p)）；`locuszoom.md`（區域關聯圖；總覽 → 放大，前後相接）；`pp-plot.md`（機率對機率；Davidson 與 MacKinnon 的「P value plot」是 P–P 結構，≠ 曼哈頓圖）；`karyotype-ideogram.md`（染色體核型與帶型示意圖，不是關聯尖峰圖；帶型條只當導航）；邁阿密圖為本 pattern 變體；`forest-plot.md`（多項研究的效應量加信賴區間與合併菱形，不是基因組位置）。

圖檔留在教圖／skill-pack（`/workspace/skill-packs/2026-09-29-am-manhattan/images/`，21 張，圖說與終稿逐字相同），本 repo **不複製**大圖。曼哈頓圖範例對照：wiki-manhattan（真實資料；三條虛線門檻值原圖未標示，數字未核）、wiki-gwas-kidney（真實資料；紅虛線 5×10⁻⁸）、qqman-01／02／03／05（模擬資料；02 的「P」「Q」是自訂標籤示範，不是真實染色體）、rgg-chunk1／chunk3（chunk3 部分標籤重疊）、rgg-chunk7-redraw 與 pyg-01-redraw（以 Matplotlib 和模擬資料**重繪**，不是原頁面的圖；pyg 橫軸是資料列順序，不是鹼基位置）、rgg-circular、rgg-circular-multi（環狀，CMplot）、cmplot-1、cmplot-4_1（門檻 1×10⁻⁶／1×10⁻⁴ 為示例刻意設定）、manhattanly-demo（互動示範）。對照圖：qqman-09、cmplot-7（QQ 圖）、wiki-regional-locus、pmc2935401-fig1（區域關聯圖；後者出自 LocusZoom 論文圖 1，CC BY-NC 僅限非商業）、wiki-volcano-contrast（火山圖；最底刻度 6.68 疑為原圖錯誤）、wiki-gwas-illustration（概念插圖，不是曼哈頓圖）。對帳見 `ATTRIBUTION.md`。
