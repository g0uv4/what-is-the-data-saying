# Pattern: karyotype-ideogram

> **圖種**：核型圖／染色體帶型示意圖（Karyotype plot／Chromosome ideogram／Ideogram）
> **來源（專案維護者整理）**：`teach-viz/2026-10-02-am-karyotype.md`（方法教學；正式課程；首次正式主課）
> **亦稱**：karyogram、idiogram、示意核型（schematic karyogram）、帶型示意條；網頁與程式庫慣用拼寫 ideogram，細胞遺傳學教材亦常見 idiogram
> **核心**：把染色體畫成**示意形狀**，讓讀者在整套或單條染色體上，立刻看到長度關係、著絲點、帶型，以及異常或註解落在**哪一臂、哪一帶**；短臂 p 在上、長臂 q 在下，帶型條上可再疊區間、密度或拷貝數。
> **一句話**：這條染色體長什麼樣子、有問題的區段落在哪一臂哪一帶；不是「哪裡有關聯尖峰」（曼哈頓圖）、不是環狀多軌（Circos）。
> **誠實提醒**：圖只是溝通層；細胞遺傳學診斷仍依實驗室標準，示意色塊不能說成「已完成致病診斷」。本 repo 的練習資料與模擬圖都是虛構、數字未核。

## 八件必須釘清的事

1. **karyogram 與 idiogram 在英文維基百科是同義詞，兩者都涵蓋顯微照片與示意圖——不要寫成「karyogram＝照片、ideogram＝示意圖」。** 維基百科 Karyotype 條目寫「karyogram 或 idiogram 是核型的圖示」，再分**顯微照片核型圖**（染色、拍照，依大小與著絲點排成成對）與**示意核型圖**（設計出來的理想化圖示，通常每條染色體只畫一條染色分體）。「ideogram 專指單條或全基因體示意條」只是基因體瀏覽器與程式庫（NCBI Genome Data Viewer、Ideogram.js、UCSC 帶型軌）的**慣用分工，屬推論，不是條目明文**。最安全的分線是「照片排列」對「示意圖」。另外：英文維基百科的 **Ideogram 條目講的是文字學的「意符」**（代表一個想法或概念的符號），全文沒有染色體內容；Idiogram 會導向 Karyotype 條目，Karyotype 開頭還有提示語「Idiogram 會導向此處；不要與 ideogram 混淆」；**`Chromosome_ideogram` 這個頁面不存在（404）**——不是來源失效，染色體示意圖請看 Karyotype 條目或各工具文件。
2. **帶號與條數**：人類體細胞一般 **46 條染色體（23 對）**＝22 對常染色體加 1 對性染色體（女性 XX、男性 XY）；精子與卵子各 23 條。**帶號由著絲點往端粒遞增**：短臂 p 從著絲點往頂端是 p11、p12、p13、p21……，長臂 q 從著絲點往底端是 q11、q12、q13、q21……；所以**從頂端端粒看，p 臂最外層的帶號最大**（本 repo 虛構第 7 號：頂端 p23、底端 q41）。真實帶型還有 p11.1、7q22.1 這類亞帶（帶型解析度越高，帶號越細），本 repo 的模擬帶號只是簡化規則，**不是任何真實染色體的帶**。帶號格式出自 ISCN（國際人類細胞基因體命名系統）；ISCN 2024 的出版社摘要頁素材包測得 403，未讀（只記名稱）。
3. **著絲點三種類型只畫中央（metacentric）、亞中央（submetacentric）、近端（acrocentric）；端著絲點（telocentric，著絲點在最末端）不畫。** 依英文維基百科 Centromere 條目，人類無端著絲點染色體，人類的近端著絲點染色體是 13、14、15、21、22 號與 Y——**這兩點都只有這一個來源**，寫的時候要註明單一來源。顏色不是固定規則：Ideogram.js 與 NCBI 說明以粉色表示著絲點周圍，karyoploteR 範例圖以紅色標著絲點，**先看圖例**。
4. **畫缺失或重複時，色框只框「有變化的那一條」。** 真實的缺失或重複多半只發生在成對染色體的其中一條；不要把框同時套在成對的兩條上。缺失後該段拷貝數 1（2−1）、重複後 3（2+1）。
5. **帶型表與標註座標必須是同一個基因體版本**（GRCh37／hg19、GRCh38／hg38、T2T 等）。教學素材的實例：karyoploteR 教學站的「基因密度」兩張圖用 hg19，「Plot Genes」一張用 hg38——**同一個教學站內版本也不一樣**，所以每張圖都要自己寫版本。UCSC liftOver 鏈檔可轉換版本，但**僅限非商業使用**；本課只提到、沒有使用。
6. **授權**：Commons 的 AGeremia〈Human karyogram〉為 **CC BY-SA 3.0**（要標作者與授權，改作須以相同授權分享；素材包的點陣裁切版屬改作）；karyoploteR 教學頁與圖（Bernat Gel）頁面標 **CC BY 4.0**（要標作者與授權；套件本身 Artistic-2.0）；**IdeoViz 套件為 GPL-2**（改作後散布須採同一授權；是軟體授權，不是圖的授權）；**UCSC liftOver 鏈檔僅限非商業**；Ideogram.js 程式庫 CC0-1.0（作者 Eric Weitz）；Häggström 的帶與亞帶示意核型圖 CC0 1.0；其餘 Commons／NHGRI／美國國家癌症研究所圖標示為公眾領域或 CC0；NCBI 網頁內容屬政府製作的公眾領域，請求註明美國國家醫學圖書館（頁面內他人提供的素材可能另有著作權）；UCSC 網站與資料表可免授權使用，瀏覽器產生的圖可重複使用並請引用其論文，部分軟體商用下載需授權。素材包各圖**沒有** NC（非商業）或 ND（禁止衍生）的標示，只有 CC BY-SA 的相同方式分享與標示要求；個別圖的授權以各檔案頁為準，本 repo 不複製任何圖。
7. **數字全部是近似值**：模擬圖與練習資料裡的**染色體長度與著絲點位置是憑印象取的近似值，沒有對照官方表，數字未核**；其中 21、22 號的著絲點位置是示意取值（讓短臂畫得較短）；帶、帶號與染色深淺全部是模擬。圖上凡是刻度、Mb、帶號沒有逐項核對的，都標「數字未核」。
8. **素材包的潤稿流程說明**：素材包原定的 Gemini 潤稿步驟**沒有執行**（登入過期），文字是審稿後的原稿；已在 `ATTRIBUTION.md` 註明。

## When

- 細胞遺傳學與臨床報告的**示意說明**：數目異常、大片段缺失或重複、易位的位置示意（診斷仍依實驗室標準，圖只是溝通層）
- 基因體瀏覽器與論文圖：用 ideogram 當「整條染色體地圖」，標出研究區間
- 教學：解釋 p、q 臂、著絲點類型、G 帶如何幫助辨認染色體
- 全基因體資料的第一層骨架（karyoploteR 風格：先畫 ideogram，再疊密度、標記、覆蓋度）
- 互動探索（Ideogram.js）：註解、熱圖、倍性、物種比較

## Recommend

- **主選（單條加標註，最貼近臨床溝通）**：畫該條染色體的帶型示意條，標 p、q、著絲點、帶號，再把報告區間以半透明色塊或側軌標上去；口頭焦點放在「單條加標註」，需要整套上下文再附縮小的全核型示意。**圖註寫：基因體版本、區間座標來源、這是示意而非病人照片**。
- **資料前提**：至少要有染色體識別與可對齊的長度或帶型座標；完整示意還要著絲點位置與分帶模式（cytoBand／ideogram 表）。帶要能從 0 鋪到全長（無縫隙、無重疊）；疊註解時需要區間起訖與基因體版本。
- **版面變體（三種不要混成一張過載圖）**：
  - **成對核型圖（示意）**：說明整套染色體的數目、大小與著絲點；各列著絲點對齊同一水平線
  - **單條帶型條加標註**：標在 p、q 與帶號上（拷貝數變異 CNV、報告區間、基因）
  - **全基因體橫向排開加資料軌**：24 列（1–22、X、Y），帶型當骨架，上方或下方疊密度、覆蓋度、標記（karyoploteR 風格）
  - **互動網頁帶型條**（Ideogram.js）：可疊註解、熱圖、倍性；多數染色體以單倍體畫出
  - **對照用顯微照片核型**：只當真實影像對照，圖題與示意圖分開寫
- **染色深淺欄位（UCSC cytoBand 慣例，本課僅單一來源：UCSC 軌道說明的轉載頁；UCSC 官方說明頁有機器人驗證，素材包沒有直接讀到）**：gneg（淺）、gpos25／gpos50／gpos75／gpos100（由淺到深）、acen（著絲點周圍帶）、gvar（可變區）、stalk（柄）。NCBI 說明頁的對應：黑色與深灰帶偏富含 AT 鹼基、晚複製、基因較少、屬異染色質；淺灰或白帶偏富含 CG 鹼基、早複製、基因相對較多。
- **工具範圍**：NCBI Genome Data Viewer 的 ideogram 只顯示染色體層級的組裝，鷹架或片段層級的組裝不顯示 ideogram；人類、小鼠、大鼠與果蠅的 ideogram 可顯示 Giemsa 帶型。
- **備選（何時改用哪一種）**：
  - 故事是「全基因體哪裡有關聯尖峰」→ [曼哈頓圖](manhattan-plot.md)；區間關聯細讀 → [LocusZoom 圖](locuszoom.md)
  - 多軌環狀比較或大量染色體間連線 → [Circos](circos.md)
  - 只有各染色體總長度 → 普通長條圖，不要叫核型圖
  - 樣本之間的親緣或分群階層 → 樹狀圖（本 repo 另見 `chart-heuristics.md`）
  - 解讀單張 FISH 螢光原圖 → 影像或實驗方法課，不是本圖種
- **參數與判準範例（範例，不是標準）**：

| 項目 | 數值與出處 | 性質 |
|---|---|---|
| 人類體細胞條數 | 46 條（23 對）；男性示意 22×2＋X＋Y＝46，女性示意 22×2＋XX＝46；21 號由 2 份變 3 份，整套由 46 變 47 | 範例，不是標準 |
| 著絲點位置與臂比（模擬，總長 120 單位、著絲點帶各寬 1 單位、臂長不含著絲點帶） | 著絲點在全長 50%／33%／13% 處，長臂÷短臂＝1.0／2.1／7.1，依序示意中央、亞中央、近端著絲點 | 範例，不是標準；不是 ISCN 分類門檻（素材包沒有給門檻，不代填） |
| 本 repo 練習資料的帶規則 | 著絲點兩側各一個 acen 帶（寬度＝染色體長度的 2%）；每條臂其餘的帶數＝臂長（不含 acen 帶）÷11 Mb 四捨五入、限 2 到 12 個；深淺依機率抽取（gneg 30%、gpos25 15%、gpos50 20%、gpos75 20%、gpos100 15%，相鄰兩帶不同色）；13、14、15、21、22 號短臂固定畫成一段柄與一段可變區 | 範例，不是標準；全是模擬規則 |
| 圖上長度比例（模擬圖） | 長度與 Mb 成正比，每 100 Mb 約 0.88 英寸；全基因體橫向版底部刻度 0 到 250 Mb | 範例，不是標準 |
| 假密度軌 | 每 5 Mb 一格，值為 0.05 到 1 的相對高度，沒有縱軸刻度，只能比較相對高低；karyoploteR 教學圖的窗格寬度為 10 Mb（plot.type 4）與 0.5 Mb（畫在 ideogram 上） | 範例，不是標準 |
| 長度對照（模擬資料，近似值） | 6 號約為 1 號的 68.6%、21 號約為 1 號的 18.8% | 範例，不是標準；數字未核 |
| 帶型解析度 | **不採用固定的帶數**（素材包明確不寫「幾個帶」的數字）；只示範同一條 7 號可畫較粗的帶或更細的亞帶 | — |

## 與鄰近圖種的區別

| 圖種 | 橫軸 | 縱軸 | 回答的問題 | 和核型圖／帶型示意圖的區別 |
|---|---|---|---|---|
| [**曼哈頓圖**](manhattan-plot.md) | 基因體位置 | −log10(p) | 全基因體哪裡有關聯尖峰 | 不畫染色體形態與帶型；帶型條只能當附帶的導航 |
| [**LocusZoom 圖**](locuszoom.md) | 一個小區間內的位置 | −log10(p) 與 LD 著色 | 單一區間的關聯與連鎖不平衡 | 細讀單一區間；核型圖負責告訴你這個區間在整條染色體哪裡 |
| [**Circos 環狀圖**](circos.md) | 染色體排成一圈 | 徑向多軌 | 多種資料與染色體間連線 | 核型圖畫形態與帶型，多為線性或成對版面；Circos 外圈的染色體示意圖也叫 ideogram，但那只是環的參考軸 |
| 樹狀圖／譜系圖 | — | — | 樣本或物種的親緣、分群 | 不是染色體圖 |
| 長條圖（只有染色體長度） | 染色體 | 長度 | 長度比較 | 沒有著絲點與帶型，不要叫核型圖 |
| FISH／顯微照片 | — | — | 真實細胞影像、探針訊號 | 本圖種是**圖示化**的核型與帶型；原始螢光照片是影像或實驗方法課 |
| 英文維基百科 Ideogram 條目 | — | — | 文字學的意符 | **不是染色體圖**，不要拿來當本圖種的條目 |
| 光譜核型（SKY 等） | — | — | 以偽彩區分染色體 | 鄰近技法，不是 G 帶；本 pattern 不改題 |

判斷口訣：**要看染色體長相、著絲點、哪一臂哪一帶 → 核型圖／帶型示意圖；位置加 −log10(p) 的尖峰 → 曼哈頓圖；單一區間的關聯 → LocusZoom；環狀多軌與連線 → Circos；只有長度 → 長條圖。**

## Avoid

- 把 karyogram 與 ideogram 切成「照片 vs 示意圖」（維基百科把兩者當同義詞）；去查英文維基百科的 Ideogram 條目找染色體圖（那是文字意符）
- 帶號順序顛倒（p 臂從著絲點往頂端遞增、q 臂從著絲點往底端遞增）
- 條數畫錯：人類體細胞一般 46 條，畫成 47 條或只畫部分卻不註明
- 把端著絲點畫成「人類少見」（依 Centromere 條目是人類沒有，且為單一來源）
- 畫缺失或重複時，把框套在成對的兩條上
- 把著絲點顏色當成固定規則（隨工具而異，先看圖例）
- 把「帶型解析度」寫成固定的帶數
- 帶型表與標註座標用不同的基因體版本（含同一份教學站內 hg19、hg38 混用而沒標）
- 拿沒有畫帶型的核型圖（例如 AGeremia 的 Human karyogram）來定位帶號
- 把性染色體同時畫 XY 與 XX 的示意圖（以「or」相連）當成同一個人的核型
- 引用圖卻漏掉授權義務（CC BY-SA 須標作者並以相同方式分享；CC BY 須標作者；GPL-2 是軟體授權）
- 把模擬圖或練習資料當成真實證據；把示意色塊直接說成「已完成致病診斷」
- 把 X 查詢 0 筆當成 X 上沒有人談（只代表這次搜尋沒有命中）

## Produce checklist

- [ ] 先決定故事：整套數目與排列、單條加某區間、還是全基因體骨架再疊資料（三種版面不同，不要混成過載圖）
- [ ] 選定物種與基因體版本（人類 GRCh37／hg19、GRCh38／hg38、T2T 或其他物種），**帶型表與所有標註座標同一版本，寫進圖註**
- [ ] 取得帶型與著絲點：公開的 cytoBand／ideogram 表（NCBI、UCSC）或教材提供的示意帶型，標明來源；NCBI 的 ideogram 只提供染色體層級的組裝
- [ ] 畫形態層：依長度比例畫染色體條，標著絲點與 p、q；需要辨認時加 G 帶深淺；成對核型要對齊著絲點列；條數要對（46；三體則 47 並註明只畫了哪一條）
- [ ] 帶要從 0 鋪到全長；p 臂帶號由著絲點往頂端遞增，q 臂由著絲點往底端遞增；標 pter、qter（短臂、長臂的端粒端）
- [ ] 再疊註解（若需要）：區間、基因、拷貝數或密度畫在帶型上或側軌；缺失或重複的色框**只框有變化的那一條**；圖例寫「標註不等於診斷結論」
- [ ] 與照片核型分工：顯微照片負責真實細胞影像，示意 ideogram 負責帶型與區間溝通，圖題分開寫
- [ ] 解讀順序：著絲點 → p、q → 帶型地標 → 色塊區間 → 才對回報告文字或 ISCN 帶號；數目異常先數清染色體條數，再看結構異常
- [ ] 圖上刻度、Mb、帶號沒核過的標「數字未核」；示意圖註明不是病人照片
- [ ] 工具誠實（只寫素材包證實的；版本為 2026-10-02 查核值）：Ideogram.js（Eric Weitz；CC0-1.0；npm 最新版 1.53.0；人類頁面多數染色體以單倍體畫出）；karyoploteR（Bioconductor 3.23、套件版本 1.38.0、Artistic-2.0；先 `plotKaryotype` 畫 ideogram，再用 `kpLines`、`kpPoints`、`kpBars` 等疊資料；帶型預設使用預先下載的 UCSC 資料）；IdeoViz（Bioconductor，套件版本 1.48.0、GPL-2；`getIdeo` 可從 UCSC 下載帶型表；rdrr.io 文件頁顯示的是舊版 1.26.0，與現行不同）；RIdeogram（CRAN，版本 0.2.2、2020-01-20 發布、Artistic-2.0，輸出 SVG）；NCBI Genome Data Viewer 的 Ideogram View；UCSC Genome Browser 的 cytoBand、cytoBandIdeo 資料表。其他軟體授權與版本素材包未寫，不代填。

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-karyotype-fictional.csv` — 1,548 列（約 80 KB）；檔頭兩行以 `#` 開頭，讀取要略過（pandas 用 `comment='#'`）；欄位 `row_id, record_type, dataset, chrom, start_bp, end_bp, name, gstain, value, chrom2, start2_bp`。`record_type`：`chrom`（染色體；`end_bp` 為長度、`value` 為著絲點位置，單位 bp）、`band`（帶，欄位仿 UCSC cytoBand）、`interval`（標註區間：cnv 的 `value` 為拷貝數，1＝缺失、3＝重複；regions 為區間 A、B、C）、`density`（每 5 Mb 一格的假基因密度）、`assoc`（假的關聯點，`value` 為 −log10(p)）、`link`（假的連線，連到 `chrom2`、`start2_bp`）。
- 我重新計算的數字（**以實際計數為準**；與素材包檢查輸出逐項一致，素材包文字與 CSV 沒有發現不一致）：
  - 全檔 1,548 列：chrom 24、band 320、interval 5、density 631、assoc 560、link 8
  - 帶：24 條染色體每條都從 0 鋪到全長（無縫隙、無重疊）；acen 帶 48 個（每條 2 個）；stalk 5 個（13、14、15、21、22 號短臂各 1 個）；gvar 6 個（上述 5 條短臂各 1 個，加 Y 染色體長臂 1 個）；gneg 69、gpos25 46、gpos50 50、gpos75 63、gpos100 33
  - 第 7 號：16 個帶（p 臂 6 個含 p11，q 臂 10 個含 q11），頂端最外層 p23、底端最外層 q41；長度 159.35 Mb，著絲點在全長 37.7% 處
  - 第 5 號：18 個帶，長度 181.54 Mb，著絲點在全長 26.9% 處；長臂 gpos100 的帶只有 q42；長臂第一個 gneg 帶是 q22
  - 缺失／重複：第 5 號 q21、q22、q23 三個帶，73.29 到 98.56 Mb，長 25.27 Mb；缺失那一條依比例約 156.27 Mb、重複那一條約 206.81 Mb
  - 區間：A 20–35 Mb（第 5 號短臂，著絲點 48.8 Mb 之前）、B 100–118 Mb、C 140–165 Mb（B、C 在長臂，C 的終點小於全長 181.54 Mb）
  - 著絲點類型示意：50%、33%、13% 處的長臂÷短臂＝1.0、2.1、7.1（臂長不含著絲點帶；若直接用著絲點位置算會是 1.0、2.0、6.7，差在著絲點帶各寬 1 單位）
  - 密度：631 格，最小 0.05（6 格剛好在下限）、最大 0.977（沒有任何一格達到上限 1）、平均 0.497
  - 相近圖種對照用的假資料：560 個關聯點（第 6 號 31 個、第 12 號 29 個、其餘 1–22 號各 25 個，X、Y 沒有點）；高於門檻 7.30 的共 8 個（第 6 號 5 個，位置 30.6–31.2 Mb；第 12 號 3 個，位置 61.7–62.3 Mb），其餘染色體最高 3.283；連線 8 條，每條連到不同的兩條染色體
  - 提醒：素材包文字說每條臂其餘的帶數是臂長 ÷ 11 Mb「取整數」，實際資料是**四捨五入**（改成無條件捨去，48 條臂中有 17 條對不上）。以實際計數為準。
- 示範讀法：先用 `chrom` 列畫出 24 條長度與著絲點，再用 `band` 列依 `gstain` 上色；`interval` 的 cnv 兩列只框第 5 號**其中一條**的 q21–q23；`density`、`assoc`、`link` 是給「疊資料軌」與「相近圖種對照」練習用的。
- `sample-karyotype-selfcheck.py` — 自檢腳本（只需 Python 標準函式庫；**以絕對路徑讀同資料夾的指定檔名，不搜尋檔案**，並以 `assert` 檢查所有列數、帶的排列規則與圖說數字；見 `examples/data/README.md`）。
- 素材包另附 `draw_karyo.py`（可重跑的九張模擬圖產生器），**本 repo 不收**：預設把圖寫進教學稿資料夾、並預設會重寫資料表（除非設環境變數 `NOBUILD`）與 `stats.json`，有路徑與覆寫資料檔的問題；只在 `ATTRIBUTION.md` 註明它存在於素材包。

## 參考連結（可點；皆出自素材包 sources.txt 且標可開）

- 條目與詞彙：https://en.wikipedia.org/wiki/Karyotype 、https://en.wikipedia.org/wiki/Idiogram （會導向 Karyotype）、https://en.wikipedia.org/wiki/Ideogram （文字意符，對照用，非本課主條）、https://en.wikipedia.org/wiki/Centromere （著絲點類型；人類無端著絲點的說法只有這一個來源）、https://www.genome.gov/genetics-glossary/Karyotype 、https://www.genome.gov/about-genomics/fact-sheets/Chromosome-Abnormalities-Fact-Sheet
- 圖片頁（作者與授權）：https://commons.wikimedia.org/wiki/File:Human_karyotype_with_bands_and_sub-bands.png 、https://commons.wikimedia.org/wiki/File:Human_karyotype_with_bands_and_sub-bands_(simple).png 、https://commons.wikimedia.org/wiki/File:Human_karyotype_diagram_showing_autosomes_and_sex_chromosomes_-_NHGRI.jpg （NHGRI 圖的出處頁 https://www.genome.gov/genetics-glossary/Y-Chromosome ）；圖庫分類 https://commons.wikimedia.org/wiki/Category:Human_karyotypes
- Ideogram.js（Eric Weitz，CC0-1.0）：https://eweitz.github.io/ideogram/ 、https://eweitz.github.io/ideogram/human.html 、https://github.com/eweitz/ideogram
- karyoploteR（Bernat Gel；教學頁 CC BY 4.0）：https://bernatgel.github.io/karyoploter_tutorial/ 、https://bioconductor.org/packages/release/bioc/html/karyoploteR.html 、https://github.com/bernatgel/karyoploteR ；教學頁示例：https://bernatgel.github.io/karyoploter_tutorial/Examples/MultipleDataTypes/MultipleDataTypes.html 、https://bernatgel.github.io/karyoploter_tutorial/Examples/GeneDensityIdeograms/GeneDensityIdeograms.html 、https://bernatgel.github.io/karyoploter_tutorial/Examples/GeneDensity/GeneDensity.html 、https://bernatgel.github.io/karyoploter_tutorial/Examples/PlotGenes/PlotGenes.html
- 其他 R 套件：IdeoViz https://rdrr.io/bioc/IdeoViz/ 、https://bioconductor.org/packages/release/bioc/html/IdeoViz.html （GPL-2）；RIdeogram https://cran.r-project.org/package=RIdeogram 、https://github.com/TickingClock1992/RIdeogram
- 瀏覽器與資料庫：NCBI Genome Data Viewer https://www.ncbi.nlm.nih.gov/gdv/ 、說明頁 https://www.ncbi.nlm.nih.gov/gdv/browser/help/ 、NCBI 政策頁 https://www.ncbi.nlm.nih.gov/home/about/policies/ ；UCSC Genome Browser https://genome.ucsc.edu/ 、https://genome.ucsc.edu/cgi-bin/hgTracks 、使用條件 https://genome.ucsc.edu/license/ 、https://genome.ucsc.edu/conditions.html
- 查核限制（未核；僅記名、不列連結）：英文維基百科的 `Chromosome_ideogram` 頁面（404，頁面不存在，是稿內已說明的事實，**不是來源失效**）；Karger 出版社的 ISCN 2024 摘要頁（403 機器人驗證）；karyoploteR 論文 Gel 與 Serra，*Bioinformatics* 2017 年第 33 卷第 19 期 3088–3090 頁的 DOI 網址（403 機器人驗證，轉址到 academic.oup.com 後被擋）。以上三項都**不是已驗證的來源**。UCSC 官方軌道說明頁與資料表頁有機器人驗證，素材包沒有直接讀到，cytoBand 欄位與值的說法只有轉載頁一個來源。
- 刻意不連結的可開頁：NCBI `https://www.ncbi.nlm.nih.gov/genome/gdv/` 與 `https://www.ncbi.nlm.nih.gov/genome/gdv/browser/help/`（兩者都只是轉址到上面已連結的 `/gdv/` 與 `/gdv/browser/help/`，重複）
- X：素材包以多輪關鍵字查 karyotype、ideogram、Ideogram.js、karyoploteR、chromosome ideogram 等教學向組合，教學向原帖 0 筆（單查 karyotype 只有與圖種無關的近日爭論貼文，未採用；另有兩次查詢被限流，未取得結果），**沒有編造連結**；0 筆只代表這次搜尋沒有命中，不等於 X 上沒有人談。

鄰居 pattern：`manhattan-plot.md`（全基因體關聯尖峰；帶型條只當導航）、`locuszoom.md`（區間細讀；核型圖告訴你區間在整條染色體哪裡）、`circos.md`（環狀多軌；外圈染色體示意圖也稱 ideogram）、`correlation-scatter.md`（任意兩變數）、`pp-plot.md`（不相關，僅供區分）；樹狀圖、光譜核型（SKY）、互動 Ideogram.js 實作細節尚無專檔。

圖檔留在教圖／skill-pack（素材包 `images/`，28 張，圖說與教學稿逐字相同），本 repo **不複製**任何圖。可對照的圖：wiki-karyotype-page（維基百科 Karyotype 條目截圖，內含 Dmonlrd〈How to read a Karyotype〉，CC BY-SA 4.0）、wiki-bands-subbands-thumb（Häggström，CC0 1.0；圖上刻度數字未核）、wiki-karyogram-crop（AGeremia，CC BY-SA 3.0，**屬改作須相同授權分享**；**沒有畫帶型**，不能定位帶號）、wiki-human-karyotype（Häggström 與 Olson，公眾領域；性染色體同時畫 XY 與 XX 並用「or」相連，**不是同一個人的核型**；Commons 檔案說明寫「男性核型」，與圖內不一致，以圖為準）、wiki-comparison-styles（同一條 7 號畫兩種帶型解析度）、wiki-translocation-deletion（46,XY,t(1;3)(p21;q21),del(9)(q22)；光譜核型偽彩，**不是 G 帶**，解析度低）、wiki-nhgri-diagram、wiki-trisomy21（21 三體；原檔副檔名 .jpg、實際內容是 PNG）；模擬資料重繪九張 sim-anatomy／sim-single-ideo-labels／sim-read-legend／sim-normal-vs-cnv／sim-ideo-vs-photo／sim-horizontal-tracks／sim-aneuploidy／sim-centromere-types／sim-neighbor-contrast（皆**虛構、數字未核**；sim-normal-vs-cnv 為了標出位置，把缺失那一條畫成中間留空、與完整的一條等高，真實缺失會讓兩端接起來、染色體變短；sim-ideo-vs-photo 右側是自繪的抽象「照片式核型」，不是真的顯微照片）；Ideogram.js 七張 ideogram-js-overview／human／mouse／collinear（四個腦癌樣本的表現量熱圖，顯示 1p 與 19q 缺失，**不是 G 帶判讀範例**）／heatmap／ploidy／rearrangements（**三倍體香蕉基因體，不是人類**）；karyoploteR 四張 kp-multiple-data（資料全是亂數假資料）／kp-gene-density-on-ideogram（hg19）／kp-gene-density（教學頁刻意不畫帶型，**這張沒有帶型**；hg19）／kp-plot-genes（hg38；圖上 11 個基因，程式列的 12 個符號中 AKT 沒有被資料庫傳回）。除 CC0、公眾領域、CC BY 或 CC BY-SA 明示者外，授權以各檔案頁為準。對帳見 `ATTRIBUTION.md`。
