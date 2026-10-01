# Pattern: locuszoom

> **圖種**：LocusZoom 圖（LocusZoom plot）；通稱**區域關聯圖**（regional association plot，也寫 regional plot、locus plot）。LocusZoom 是工具名，區域關聯圖是通稱；沒用這套工具的論文也會畫意圖相同的圖。本 repo 先前的鄰居範例寫作「區域放大圖」，現統一為「LocusZoom 圖（區域關聯圖）」。
> **來源（納茲教圖）**：`teach-viz/2026-10-01-am-locuszoom.md`（方法教學；正式課程）
> **名稱解讀**：Locus＝基因座（基因組上的特定區域），Zoom＝由全基因組總覽放大聚焦；此解釋屬望文生義（推論），來源沒有官方由來說明。英文維基百科**沒有**獨立的 LocusZoom 條目（該頁 404），通稱出現在 GWAS 條目的檔案 `Regional_Association_Plot.png`。
> **核心**：在全基因組關聯研究（GWAS）裡，把**某一段染色體區間**放大；**每個點＝一個變異位點**（常為單核苷酸多型性 SNP）；**橫軸＝區間內的基因組位置**（常用 Mb）；**縱軸＝−log10(p)**（越高越顯著）；各點常依與**指標變異**的連鎖不平衡（LD，白話：兩個變異位點常一起出現的程度）r² 著色；下方附基因軌，可選疊重組率曲線。
> **一句話**：曼哈頓圖找到尖塔之後的細節層，用來讀「峰有多尖、哪些點只是跟著指標變異、峰底下有哪些基因」；不是因果證明。
> **英文維基百科 GWAS 條目原文**："This type of plot is similar to the Manhattan plot in the lead section, but for a more limited section of the genome."

## 五件必須釘清的事

1. **用詞：「領先（lead）變異」或「指標變異」（index variant）；不要寫成「鉛變體」。** 「鉛變體」是把 lead 誤譯成化學元素的「鉛」，不要使用。Pruim 2010 寫預設為 "most strongly associated SNP or another user-specified SNP"；Boughton 2021 寫 lead (most significant) variant。圖上常畫成鑽石：LocusZoom.js 是**紫色鑽石**，locuszoomr 基本圖是**紅色鑽石**（加 LD 著色後也有紫色鑽石），英文維基百科示例圖是**圓點加箭頭**（沒有紫色鑽石）。
2. **領先變異不等於因果變異；一叢高 LD 的紅點「與單一關聯訊號一致，但不能證明」只有一個因果變異。** Schaid 2018 指出領先變異有相當機會不是因果變異（其模擬：各 1000 位病例與對照，勝算比 1.5、風險等位基因頻率 50% 時領先變異是因果變異的機率約 79%；勝算比 1.1、頻率 5% 時約 2.4%；數字未核）。反過來，一叢紅點也**不等於**很多個獨立發現：多個變異都顯著，可能只因都與同一個因果變異相關。**低 LD 卻仍然很高的第二個峰**值得深入檢視，但要做**條件分析**才能確認獨立，**不能直接說獨立**。
3. **LD 依賴參考面板與族群；共定位、精細定位、條件分析是三件不同的事。** r² 是向參考面板（例如 1000 Genomes 的某個族群）查出來的，不是資料自帶的固定值；LocusZoom.js 介面可選 ALL（預設）、AFR、AMR、EAS、EUR、SAS，換族群顏色會變，圖註要寫參考來源，所選面板要能代表研究樣本。三個名詞都**不是** LocusZoom 圖本身：**共定位**＝檢定兩種性狀的關聯訊號是否與同一個共享的因果變異一致（Giambartolomei 2014；該文載明高 PP4 是相關的度量，不是因果）；**精細定位**＝找出最可能影響性狀的變異，常縮成可信集合（LocusZoom.js 可顯示 95% 可信集合，但圖本身不是精細定位）；**條件分析**＝把已知變異放進模型當條件，看是否還有額外獨立訊號（Yang 2012 以摘要統計加參考樣本 LD 做近似）。
4. **顏色與單位依工具與版本而定，不看圖例不要讀圖。** Pruim 2010 圖例：r² 大於 0.8 紅、0.6 到 0.8 橙、0.4 到 0.6 綠、0.2 到 0.4 淺藍、小於 0.2 深藍，指標變異紫色；LocusZoom.js 級距相同，沒有 LD 資料的點是灰色。locuszoomr 疊上表現量數量性狀基因座（eQTL）資料的那張圖，**顏色與三角形方向代表 eQTL 效應大小與方向，不是 LD**；locuszoomr 的縱軸可改成效應量 beta（圖題要標清楚，不是 −log10(p)）。重組率曲線：LocusZoom.js 畫在右軸，單位 cM/Mb；**locuszoomr 的右軸標 "Recombination rate (%)"，單位是百分比**，兩者不同。
5. **授權**：Pruim 2010 圖 1 是 **CC BY-NC 2.5，僅限非商業使用**；英文維基百科區域關聯圖（Commons `Regional_Association_Plot.png`，作者 Sanna S 等人）**CC BY-SA 2.5**；Boughton 2021 圖 1 **CC BY 4.0**；曼哈頓對照圖（Commons `Manhattan_Plot.png`，作者 Ikram MK 等人）CC BY 2.5；以上須標作者與授權。**其餘外部圖（GitHub 截圖、locuszoomr 各圖）授權未明示，僅作教學示意引用，不可當作可自由再用**；標「模擬資料重繪」者為自製。本 repo 不複製任何圖，詳見 `ATTRIBUTION.md`。另：**PMC3605911 是病毒系統動力學論文，不是來源**；Pruim 2010 是 PMC2935401，Boughton 2021 是 PMC8479674。

## When

- GWAS 或全基因組掃描：曼哈頓圖標出尖峰後，對該區間做細讀與出版主圖
- 比較指標變異周圍的 LD 結構（高 LD 一叢對低 LD 旁峰）
- 把關聯訊號對齊基因註解，作為候選基因討論的起點（不是因果證明）
- 教學：說明為何「一個生物學訊號」常呈現為「一叢紅點」
- 互動探索（LocusZoom.js、my.locuszoom.org）：切換區間、更換參考族群、疊加註解

## Recommend

- **主選**：經典 LocusZoom 版式——上方主面板（橫軸區間位置、縱軸 −log10(p)、依 r² 著色、標出領先變異、可畫顯著水準線），下方基因軌（與主面板共用橫軸），可選疊重組率；**圖註寫清：LD 參考面板與族群、領先變異如何選定、虛線代表什麼**
- **資料前提**：至少要有變異位點的染色體位置與 p 值（或可換算的檢定統計量）；完整版面還需要相對於領先變異的 LD（或可查詢的參考基因型面板）與基因註解來源
- **變體（同一家族，但要標清楚）**：
  - **缺 LD 色或缺基因軌的裁切圖**：不宜逕稱完整 LocusZoom 版式（locuszoomr 基本圖就沒有 LD 著色）
  - **縱軸改成效應量 beta**：圖題標清楚，不要讓讀者當成 −log10(p)
  - **疊 eQTL 效應**：顏色改代表效應，不是 LD
  - **多圖並排**（locuszoomr 可併排多個位點）：r² 圖例可能只畫在其中一張
  - **互動版**（LocusZoom.js、locuszoomr 的 plotly 版）：滑鼠停在點上看 rs 編號與 p 值
- **參數與慣例範例（範例，不是標準）**：

| 項目 | 數值與出處 | 性質 |
|---|---|---|
| LD 分級 | r² 大於 0.8 紅、0.6 到 0.8 橙、0.4 到 0.6 綠、0.2 到 0.4 淺藍、小於 0.2 深藍、領先變異紫色（Pruim 2010；LocusZoom.js 級距相同，無資料為灰） | 範例，不是標準 |
| 顯著水準虛線 | LocusZoom.js 畫在 −log10(p) 約 7.3，對應 5×10⁻⁸ 全基因組門檻；是常用慣例，不是自然法則，圖例要寫 | 範例，不是標準 |
| 區間選法 | Pruim 2010 列三種：以領先變異為中心向左右各取數百 kb、以基因名稱加兩側側翼、直接指定起訖座標；Boughton 2021 寫區間通常小於 1 Mb。「區間過大變小曼哈頓、過小切斷 LD 區塊」是經驗法則，無法證實 | 範例，不是標準 |
| LD 參考族群 | LocusZoom.js 可選 ALL（預設）、AFR、AMR、EAS、EUR、SAS | 範例，不是標準 |
| 領先變異 | 預設區間內最顯著的變異；「條件分析後改用條件後的領先變異」是常見做法，LocusZoom 文件沒寫，屬推論 | 範例，不是標準 |
| 版本（2026-10-01 查核值） | LocusZoom.js v0.14.0；locuszoomr 1.1.0（CRAN，2026-09-17） | 範例，不是標準 |

- **備選（何時改用哪一種）**：
  - 要看「全基因組哪裡有峰」→ [曼哈頓圖](manhattan-plot.md)
  - p 值整體像不像期望、有沒有膨脹 → [QQ 圖](qq-plot.md)
  - 倍數對顯著性 → [火山圖](volcano-plot.md)；豐度對倍數 → [MA 圖](ma-plot.md)；兩種量測方法是否一致 → [Bland–Altman 圖](bland-altman.md)
  - 染色體形態與帶型 → 核型圖（karyotype／ideogram；repo 尚無專檔，不應稱為 LocusZoom）
  - 沒有基因組座標與關聯統計量 → 資料前提不足；只是比較任意兩欄 → [一般散點圖](correlation-scatter.md)，不應稱為區域關聯圖

## 與鄰近圖種的區別

| 圖種 | 橫軸 | 縱軸／內容 | 回答的問題 | 和 LocusZoom 圖的區別 |
|---|---|---|---|---|
| **曼哈頓圖**（`manhattan-plot.md`） | 全基因組、跨染色體位置 | −log10(p) | 全基因組哪裡有峰 | 是總覽；LocusZoom 圖是選定區間的細節層，兩者前後相接，不是同一張天際線圖 |
| **QQ 圖**（`qq-plot.md`） | 期望的 −log10(p) | 觀察的 −log10(p) | p 值分布像不像期望、有沒有膨脹 | 不是位置圖，看不出訊號在哪一段 |
| **火山圖**（`volcano-plot.md`） | 倍數 | 顯著性 | 變多大、證據多強 | 不是染色體區間座標 |
| **MA 圖／Bland–Altman 圖**（`ma-plot.md`、`bland-altman.md`） | 平均 | 倍數／差值 | 豐度與倍數；方法一致性 | 與基因組區間無關 |
| **一般散點圖**（`correlation-scatter.md`） | 任意數值 | 任意數值 | 兩變數的關係 | 本圖軸固定為區間位置對 −log10(p)，常搭配 LD 著色與基因軌 |
| Circos（`circos.md`） | 環狀參考軸 | 多軌 | 全景與連結 | 環狀多軌全景，不是單一區間的關聯放大 |
| 精細定位圖（repo 尚無專檔） | 區間內位置 | 變異是因果的機率（可信集合）等 | 最可能影響性狀的變異是哪幾個 | LocusZoom.js 可顯示 95% 可信集合，但 LocusZoom 圖本身不是精細定位 |
| 共定位圖（如 locuscomparer；repo 尚無專檔） | 區間內位置 | 兩種性狀的關聯 | 兩個訊號是否與同一個共享因果變異一致 | 說明文件載明為 GWAS 與 eQTL 共定位的視覺化；屬相近工具，不改題 |
| 核型圖（repo 尚無專檔） | 染色體 | 帶型 | 染色體長什麼樣子 | 不是關聯 p 值的區間圖 |

判斷口訣：**全基因組看哪裡有峰 → 曼哈頓圖；選定區間＋LD 著色＋基因軌 → LocusZoom 圖；p 值整體膨脹 → QQ 圖；任意兩欄 → 一般散點圖。**

## Avoid

- 把領先（指標）變異當成因果變異；把「最近的基因」當成致病基因（Pruim 2010 提到距離關聯變異數百 kb 外的基因也可能有功能）
- 把一叢紅點說成「很多個獨立發現」；也不要反過來說「高 LD 就證明只有一個因果訊號」（多個因果變異彼此相關時更難拆開）
- 看到低 LD 的高處第二個峰就直接說「獨立」（要條件分析）
- 以為 LD 顏色是資料自帶的；沒寫參考面板與族群、所選面板不能代表研究樣本
- 不看顏色定義就讀圖（locuszoomr 的某張圖顏色是 eQTL 效應）；把縱軸是 beta 的圖當成 −log10(p)；把右軸 % 與 cM/Mb 當同一種單位
- 把共定位、精細定位、條件分析混為一談
- 沒說明虛線的意義（常是 5×10⁻⁸ 的慣例門檻）
- 區間太大變成小曼哈頓、太小切斷 LD 區塊（經驗法則）
- 把只有基因軌、沒有變異點的圖當成區域關聯圖（locuszoomr 有一張就只有基因軌）；把沒有 LD 色或基因軌的裁切圖當成完整 LocusZoom 版式
- 模擬資料與真實資料不分；把授權未明示或僅限非商業（Pruim 2010 的圖，CC BY-NC）的外部圖當可自由再用
- 寫成「鉛變體」

## Produce checklist

- [ ] 故事句是「這座尖塔底下是誰、旁邊的點是跟著跑還是另一個訊號」；資料是 GWAS 或全基因組掃描，且已有曼哈頓圖找出的區間
- [ ] 先完成總覽：用曼哈頓圖找出染色體與大致座標，記錄性狀、分析版本與基因組組建（例如 GRCh37 或 GRCh38）
- [ ] 選定區間（範例：領先變異左右各數百 kb、基因加側翼、直接指定座標；通常小於 1 Mb；經驗法則）
- [ ] 選定領先變異（預設區間內最顯著；若做過條件分析，改用條件後的並在圖題標清楚，屬推論）
- [ ] 表：每個變異至少有位置與 p 值（或可轉成 −log10(p) 的統計量）；缺失值與重複編號的處理先議定
- [ ] 取得 LD：向參考面板查各點對領先變異的 r²；**圖註寫參考面板與族群**，換族群顏色會變
- [ ] 畫主面板（位置對 −log10(p)，依 r² 分級著色，標出領先變異，必要時加全基因組門檻線並寫在圖例）
- [ ] 加基因軌（與主面板共用橫軸）與可選的重組率（右軸單位寫清楚：cM/Mb 或 %）
- [ ] 解讀順序：領先變異是不是最高點 → 紅／橙色一叢（與單一訊號一致，不能證明單一因果）→ 高處的藍點或第二個峰（需條件分析）→ 虛線 → 基因軌（候選假設的起點）
- [ ] 工具誠實（只寫素材包證實的；版本為 2026-10-01 查核值）：
  - **LocusZoom.js**（JavaScript，v0.14.0；程式為 MIT 授權，依 Boughton 2021，GitHub 授權檔素材包未自行驗證，且軟體授權不等於圖的授權）：網頁嵌入、平移縮放、切換 LD 參考族群、疊加 GWAS Catalog；基因軌採 GENCODE
  - **my.locuszoom.org**（現行服務；2019-10-14 推出，須用 Google 帳號上傳，附曼哈頓圖與 QQ 圖，依 Boughton 2021）與 LocalZoom；密西根大學 CSG 首頁把原版單張繪圖、批次與互動服務列為 Legacy Services（不再積極維護）；經典版（Pruim 2010）基因軌採 UCSC 基因資料
  - **locuszoomr**（R，CRAN 1.1.0，2026-09-17）：本機端繪製，Ensembl 基因軌；可加 LD、重組率、標籤，可改縱軸為 beta，可多圖並排，有 plotly 互動版（`locus_plotly`）；LD 經 LDlinkR 向 1000 Genomes 查詢，需 token；程式授權素材包未寫；CRAN 頁引用的 doi 10.1093/bioadv/vbaf006 素材包無法證實
  - **locuscomparer**（R，共定位視覺化，只記名稱並附 GitHub 連結）、**Matplotlib**（本課模擬圖重繪用）：授權素材包未寫，不代填
  - R Graph Gallery、Python Graph Gallery、From Data to Viz、Dataviz Catalogue、Dataviz Project 均查無 LocusZoom 專頁
- [ ] 示範數字標「數字未核」；因果結論仍需功能與重複驗證證據，不能單靠區域圖
- [ ] 自檢：領先變異是最高點嗎？有沒有把紅點說成多個獨立發現？圖註有 LD 參考面板嗎？虛線寫了意義嗎？有沒有用「鉛變體」？

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-locuszoom-fictional.csv` — 2,306 列（約 112 KB）；檔頭兩行以 `#` 開頭，讀取要略過（pandas 用 `comment='#'`）；欄位 `row_id, record_type, dataset, chrom, position_bp, end_bp, neg_log10_p, ld_r2_to_index, ld_band, is_index, gene_name, strand, recomb_rate_schematic`。`record_type`＝`variant`（變異位點）、`gene`（基因軌，起點為 `position_bp`、終點為 `end_bp`，基因名 GENEA 等為示意，非真實基因）、`recomb`（重組率示意曲線的取樣點，**不是真實資料**）。`dataset`＝`genome`（全基因組背景：染色體 1 到 22 各 80 點，共 1,760 點）、`single`／`following`／`second`／`readcolors`（第 10 號染色體 45.0 到 45.55 Mb 的四段虛構區間，分別對應構造圖、跟隨點圖、第二個峰圖、讀顏色圖）。
- 我重新計算的數字（**以實際計數為準**；與素材包檢查輸出逐項一致）：
  - 全檔 2,306 列：variant 2,239（genome 1,760＋single 114＋following 121＋second 127＋readcolors 117）、gene 11（3＋3＋3＋2）、recomb 56（皆屬 single）；背景點最高 −log10(p) 3.654，**沒有任何背景點**超過門檻 7.30
  - `single`：領先變異 45.235 Mb、高度 9.4，其餘點最高 8.887；顏色等級 紅 18、橙 10、綠 12、淺藍 11、深藍 62
  - `following`：領先變異 45.230 Mb、高度 10.0，其餘點最高 9.477；紅 24、橙 10、綠 17、淺藍 7、深藍 62
  - `second`：領先變異 45.190 Mb、高度 9.0，其餘點最高 8.400；紅 16、橙 9、綠 11、淺藍 21、深藍 69；第二個峰（約 45.42–45.45 Mb、r² 小於 0.35、高度大於 5）共 14 點（深藍 8、淺藍 6，r² 最大 0.334），最高 8.4，**14 點中只有 3 點（7.736、7.919、8.4）高於門檻 7.30**
  - `readcolors`：領先變異 45.230 Mb、高度 9.0，其餘點最高 8.529；紅 18、橙 7、綠 16、淺藍 10、深藍 65；高處的深藍點 3 個（7.0、7.6、8.1），其中 2 個高於門檻
  - 重組率示意曲線最高 46.48，在 45.48 Mb（不在關聯峰的位置）
  - **「超過顯著門檻」的點數包含領先變異本身**：素材包輸出的 17／28／17／17，扣掉領先變異各為 16／27／16／16（`single` 的 16 點＝紅 15、橙 1）。素材包輸出沒有說明這點，另外 `second` 的輸出句「第二個峰共 14 個點……仍高於顯著門檻」指的是**最高點**，不是 14 點全部
- 示範讀法：橫軸位置（Mb）、縱軸 `neg_log10_p`，依 `ld_band` 著色（紅 r²≥0.8、橙 0.6 到 0.8、綠 0.4 到 0.6、淺藍 0.2 到 0.4、深藍 <0.2，`index` 為領先變異，每段區間恰好一個且是該段最高點），在 7.30 畫虛線，下方依 `gene` 列畫基因軌；`following` 看紅橙一叢跟在峰頂兩側；`second` 看低 LD 的第二個峰（**需條件分析確認，不能直接說獨立**）；`readcolors` 看高處的深藍點；`single` 可加 `recomb` 列疊重組率。
- `sample-locuszoom-selfcheck.py` — 自檢腳本（需 numpy；**以絕對路徑讀同資料夾的指定檔名，不搜尋檔案**；見 `examples/data/README.md`）。

## 參考連結（可點；皆出自素材包 sources.txt 且標可開）

- 通稱與相關條目：https://en.wikipedia.org/wiki/Genome-wide_association_study 、https://en.wikipedia.org/wiki/Manhattan_plot
- 圖片頁（作者與授權）：https://commons.wikimedia.org/wiki/File:Regional_Association_Plot.png （CC BY-SA 2.5）、https://commons.wikimedia.org/wiki/File:Manhattan_Plot.png （CC BY 2.5）
- 論文：https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2935401/ 與 https://doi.org/10.1093/bioinformatics/btq419 （Pruim 等 2010，LocusZoom 經典版；圖 1 為 CC BY-NC 2.5，僅限非商業）；https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8479674/ 與 https://doi.org/10.1093/bioinformatics/btab186 （Boughton 等 2021，LocusZoom.js；圖 1 為 CC BY 4.0）
- 工具：https://my.locuszoom.org/ 、https://csg.sph.umich.edu/locuszoom/ 、https://github.com/statgen/locuszoom 、https://statgen.github.io/locuszoom/ 、https://statgen.github.io/locuszoom/docs/guides/index.html ；https://cran.r-project.org/web/packages/locuszoomr/vignettes/locuszoomr.html 、https://cran.r-project.org/web/packages/locuszoomr/index.html 、https://github.com/myles-lewis/locuszoomr ；共定位相近工具 https://github.com/boxiangliu/locuscomparer
- 查核限制（未核；僅記名、不列連結）：英文維基百科 `LocusZoom` 條目（404，不存在）、`locuszoom.org`（https 連線被對方中斷，素材包測得 000；改用 http 同名網址可開，素材包未另列）、Dataviz Catalogue `methods/locuszoom.html`、From Data to Viz `graph/locuszoom.html`、R Graph Gallery `locuszoom.html`、Python Graph Gallery `locuszoom/`、Dataviz Project `data-type/locuszoom/`、LocusZoom.js 文件站 `examples/` 頁（以上 404）；Biostars `p/103057/`（403）
- 刻意不連結的可開頁：英文維基百科 `File:Regional_Association_Plot.png`（與 Commons 圖片頁重複）
- 論文原文僅引述、素材包未列連結：Schaid 等 2018（Nat Rev Genet 19:491–504）、Giambartolomei 等 2014（PLoS Genet 10(5):e1004383）、Yang 等 2012（Nat Genet 44:369–375）；Bentham 2015（GCST003156）為 locuszoomr 說明文件範例資料的出處
- X：素材包以多種關鍵字查 LocusZoom、"regional association plot"、"locus zoom" GWAS，結果皆為 0 筆，**找不到教學向原帖，沒有編造連結**

鄰居 pattern：`manhattan-plot.md`（前後相接：總覽 → 放大）、`qq-plot.md`、`volcano-plot.md`、`ma-plot.md`、`bland-altman.md`、`correlation-scatter.md`、`circos.md`；精細定位圖、共定位圖、核型圖尚無專檔。

圖檔留在教圖／skill-pack（`/workspace/skill-packs/2026-10-01-am-locuszoom/images/`，20 張，圖說與教學稿逐字相同），本 repo **不複製**任何圖。可對照的圖：wiki-Regional_Association_Plot（CC BY-SA 2.5；第 19 號染色體；指標變異為圓點加箭頭，圖內另有未附圖例的方塊、倒三角）、pmc2010-btq419f1（Pruim 2010 圖 1，CC BY-NC 2.5 僅限非商業；圖內 "nonsyn"、"utr" 縮寫未定義）、pmc2021-lzjs-btab186f1（CC BY 4.0；裁切後未附 r² 圖例）、github-standard-association（LocusZoom.js 截圖，授權未明示）、locuszoomr-v01（無 LD 著色）／v02／v03（右軸單位 %）／v07（縱軸是 beta）／v12／v04（**只有基因軌，不是區域關聯圖**）／v06（顏色是 eQTL 效應，**不是 LD**）／v08／v13（互動版截圖）、sim-anatomy／sim-manhattan-vs-region／sim-following-ld／sim-second-peak-lowld／sim-read-ld-colors／sim-recomb-overlay（皆**模擬資料重繪**，數字未核；「跟隨」是本課教學比喻，非來源術語；重組率為示意曲線）、wiki-manhattan-contrast（真正的曼哈頓圖，CC BY 2.5）。除上列明示授權者外皆授權未明示，僅作教學示意引用。對帳見 `ATTRIBUTION.md`。
