# Pattern: circos

> **圖種**：Circos（環狀多軌圖）
> **來源（納茲教圖）**：`teach-viz/2026-09-28-am-circos.md`（方法教學；正式課程）
> **亦稱**：環形比較基因組視覺、圓形多軌關係圖；英文固定寫 **Circos**（同時是軟體名稱與圖種傳統；Martin Krzywinski 於 Canada's Michael Smith Genome Sciences Centre 開發）
> **核心（三層讀法）**：**環＝參考軸**（染色體、序列重疊群 contig 或任何有長度刻度的扇區排成一圈；染色體示意圖稱 ideogram；單獨的帶型示意圖見 `karyotype-ideogram.md`）→ **徑向軌道＝同一角度的多層訊號**（散點、折線、直方圖、熱圖、磚塊、文字同心疊放，同一角度＝同一位置）→ **內部連線與寬帶＝成對關係**（兩個位置之間的對應、重組、共線性；寬度、透明度、顏色表示區間大小、方向與強度）
> **出處**：Krzywinski M, Schein J, Birol I, Connors J, Gascoyne R, Horsman D, Jones SJ, Marra MA. "Circos: an information aesthetic for comparative genomics." *Genome Research* 2009;19(9):1639–1645；DOI 10.1101/gr.092759.109（DOI 與期刊頁本輪打不開，以 PubMed Central 全文為準）

## When

- 有一條（或數條）**很長、帶位置刻度的參考軸**，要同時看**沿軸的多層定量**與**軸上兩點之間的對應關係**
- 比較基因組學、腫瘤基因組相對參考基因組的變異、多位病人的結構變異熱點；染色體示意圖＋拷貝數變異／甲基化／基因密度軌道＋染色體轉位或共線性連線
- 要自動化批次產出、資料墨水比高的圓形總覽；簡報或期刊要一張圖同時看見「區段對應」與「同一位置多層同步變化」
- 形狀：三張表——扇區（id、長度、順序）＋軌道（扇區、起訖位置、數值或類別）＋連線（兩端扇區與起訖位置、方向、類型）

## Recommend

- **主選**：Circos（外圈刻度軸 → 中圈軌道 → 內圈連線）
- **變體（同一體系，要標清楚）**：

| 情況 | 建議變體 |
|---|---|
| 只看沿參考軸的分佈，沒有成對關係 | 只有多軌、中心留白 |
| 結構變異、染色體轉位、稀疏對位 | 多軌搭配細連線 |
| 大片段共線性、表格流量 | 寬帶連線（外圈仍需刻度軸，常與多軌並存） |
| 稀疏基因組中有少數熱點 | 軸斷點／局部放大（保留整條染色體上下文） |
| 矩陣資料想畫成圓形連線 | 表格轉圓形版面（官方線上表格檢視器做法；與弦圖高度重疊，交付時說清楚資料是否有位置刻度） |

- **執行期規則**：依數值改變顏色或顯示與否（例如超過門檻才著色），不改原始資料
- **備選（何時改用哪一種）**：
  - 只有「A 類流向 B 類佔多少」、沒有位置座標 → **弦圖**（`chord-matrix.md`）或**桑基**（`sankey-flow.md`）
  - 讀者要精確讀單一數值、不習慣圓形刻度 → 線性多軌圖、分面折線（`small-multiples.md`）或表格
  - 層級比例或函式呼叫堆疊 → 樹狀（`treemap-composition.md`）、**旭日**（`sunburst-hierarchy.md`）、冰柱（`hierarchy-icicle.md`）、火焰圖（`flame-graph.md`）
  - 一般網路拓撲 → `biofabric.md`、鄰接矩陣（`adjacency-matrix.md`）、**弧線圖**（`arc-diagram.md`）、力導向（`force-network.md`）

## 與鄰近圖種的區別

| 圖種 | 外圈／版面的意義 | 核心問題 | 和 Circos 的差別 |
|---|---|---|---|
| **弦圖**（`chord-matrix.md`） | 類別弧段，弧長≈該類別總量比例 | 類別之間流量多少 | 通常沒有同心多軌、沒有位置刻度；大致只相當於 Circos 最內層的連線層 |
| **弧線圖**（`arc-diagram.md`） | 節點排在一條直線上，上方畫弧 | 誰和誰相連（網路拓撲） | 沒有沿刻度軸的多層軌道；是直線版面 |
| **階層邊捆綁圖**（HEB；repo 尚無專檔，見 `references/chart-heuristics.md`） | 圓周排葉節點，依階層把邊捆成束 | 階層結構下的連線走向 | 外圈是階層葉節點而非長度刻度軸；重點在拓撲與階層，不是位置對齊的多軌訊號 |
| **圓形長條圖**（`circular-bar.md`） | 每根長條占一個角度的類別 | 各類別數值大小 | 只有一層長條、沒有成對連線，也沒有長參考軸上的位置座標；可視為 Circos 一條直方圖軌道的簡化版 |
| **旭日圖**（`sunburst-hierarchy.md`） | 同心環代表階層深度，扇區角度代表占比 | 階層占比與下鑽 | 同心環是「階層」而非「同一位置的多層訊號」；沒有連線層 |

判斷口訣：**有長刻度軸＋多層軌道＋對位連線 → Circos；只有類別流量 → 弦圖；只有拓撲 → 弧線圖／階層邊捆綁；只有單層數值 → 圓形長條圖；只有階層占比 → 旭日圖。**

## Avoid

- 把只有類別流量、沒有位置刻度的資料硬做成 Circos（弦圖就夠）
- 外圈扇區沒標刻度或單位，讀者看不出「這一段是誰、從哪到哪」
- 連線全畫、不篩選也不調透明度 → 中心變成毛線球
- 同一角度的各軌道沒對齊到相同位置座標 → 讀者誤判「同位置同步變化」
- 拿圓形刻度讓讀者目測精確數值；爭議落在精確數字時另附線性多軌圖或表格
- **工具寫錯**：把 circlize、pyCirclize 的成果寫成「用官方 Circos 做的」
- **引用錯頁**：英文維基百科「Circos」條目會**重新導向到弦圖條目**，不能當 Circos 軟體或圖種專頁引用
- 把 `vigsterkr/circos` 當官方倉庫（非官方，與官方關係未證實）；`github.com/circos/circos` 不存在

## Produce checklist

- [ ] 故事句是「長參考軸＋多層訊號＋對位」；只有類別流量 → 弦圖；只有網路拓撲 → 弧線圖／力導向／BioFabric
- [ ] 扇區表：清單、長度、單位、順序與方向（順時針）；外圈標刻度與名稱
- [ ] 軌道表：「扇區＋起訖位置＋數值（或類別）」；同一角度的位置對齊；位置單位與扇區一致
- [ ] 連線表：兩端扇區與起訖位置、方向（起點大於終點＝反向）、類型，可加寬度；先篩掉過弱或過短的連線，調透明度
- [ ] 由外而內排版：染色體示意圖 → 軌道 → 連線；配色與執行期規則（不改原始資料）
- [ ] 稀疏熱點用局部放大或軸斷點，保留全軸上下文
- [ ] 輸出 PNG／SVG；期刊多用向量圖，再到繪圖軟體微調文字與圖例
- [ ] 圖旁三句讀法：環＝參考軸（扇區是誰、單位）、軌道＝同一位置的多層訊號、連線／寬帶＝對應或重組線索（顏色＝同向／反向）
- [ ] 工具誠實（只寫素材包證實的；版本為 2026-09-28 查核值，日後可能更新）：
  - **Circos 官方**：Perl 命令列工具、純文字設定檔、輸出 PNG／SVG；下載頁最新版 0.69-10；**GNU 通用公共授權條款（GPL）第 3 版**；需求頁 "You will need Perl to run Circos."
  - **circlize**（R，Zuguang Gu；Bioinformatics 2014，DOI 10.1093/bioinformatics/btu393）：CRAN 0.4.18、MIT；**同家族圓形版面實作，不是官方 Circos**
  - **pyCirclize**（Python，moshi4；matplotlib 為基礎）：原文 "pyCirclize was inspired by circlize and pyCircos."；PyPI 1.10.1、MIT；**同家族實作，不是官方 Circos**
  - **vigsterkr/circos**（GitHub）：Perl、內容與官方敘述相符的**非官方倉庫，與官方關係未證實**；素材包未寫授權
  - 官方線上表格檢視器（tableviewer）舊網址目前拒絕存取
  - Dataviz Catalogue、data-to-viz 沒有 Circos 專頁（只有弦圖頁）；Dataviz Project 拒絕存取
- [ ] 用 circlize／pyCirclize 做的圖，圖注寫「同家族實作，不是同一套程式」
- [ ] 示範數字標「數字未核」
- [ ] 自檢：拿掉外圈刻度與軌道後，是不是其實只剩弦圖？讀者需要精確數值嗎？

## 虛構 demo 資料

見 `examples/data/`（三檔皆**虛構示意，數字未核**）；情境：兩種近緣作物（甲種、乙種）全基因組組裝後的共線性比較：

- `sample-circos-sectors.csv` — 外圈扇區：`sector_id, species, label, length_mb, order`；甲種 3 條、乙種 3 條染色體（26–42 Mb）各占半圈，`order` 為順時針順序
- `sample-circos-track.csv` — 數值軌道：`sector_id, start_mb, end_mb, gene_density, repeat_level`；`gene_density`（每區間基因數）畫直方圖軌道，`repeat_level`（低／中／高）畫熱圖軌道
- `sample-circos-links.csv` — 連線：`link_id, sector_a, start_a_mb, end_a_mb, sector_b, start_b_mb, end_b_mb, orientation, link_type`；8 條，`link_type` 為共線／疑似倒位／短對位（短對位可隱藏），`orientation` 同向／反向用不同顏色；B 端起點大於終點代表反向

示範讀法：先沿外圈認出染色體身分與長度；再看寬帶是平行成束（共線）還是翻轉（L02：甲-1號 14–20 Mb ↔ 乙-1號 23→17 Mb；L07：甲-3號 16–27 Mb ↔ 乙-2號 36→31 Mb，兩條「疑似倒位」）；對 L02、L07 開局部放大，在同一角度對齊軌道，看斷點是否落在重複序列等級「高」的區段（例：甲-1號 14–21 Mb、乙-1號 16–24 Mb 皆為「高」）。L08 是短對位，可隱藏。若爭議在某區段的精確數值，另附線性多軌圖或表格。

## 參考連結（可點；皆出自素材包 sources.txt 且標「可開」）

- https://circos.ca/ （官方首頁：定義、四格樣品、基因組／非基因組拼圖、表格檢視器縮圖牆；sources.txt 註：工作機需略過憑證驗證）
- https://circos.ca/images/ 、https://circos.ca/images/gallery/ 、https://circos.ca/images/samples/
- https://circos.ca/images/features/ （媒體採用例：American Scientist、紐約時報、Condé Nast Portfolio）
- https://circos.ca/images/published/ （科學文獻採用例）
- https://circos.ca/intro/genomic_data/ 、https://circos.ca/intro/general_data/ （基因組／非基因組應用；汽車顧客流向圖）
- https://circos.ca/intro/features/ （功能總覽 A–T、刻度變換）
- https://circos.ca/guide/genomic/ 、https://circos.ca/guide/tables/ 、https://circos.ca/guide/visual/
- https://circos.ca/tutorials/ 、https://circos.ca/tutorials/images/ （第 5 單元連線、第 6 單元二維軌道、第 8 單元實作範例）
- https://circos.ca/documentation/
- https://circos.ca/software/ 、https://circos.ca/software/download/ （GPL 第 3 版、版本 0.69-10）、https://circos.ca/software/requirements/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC2752132/ （論文全文與圖 5、6、7）
- https://pubmed.ncbi.nlm.nih.gov/19541911/ 、https://api.crossref.org/works/10.1101/gr.092759.109 （書目）
- https://www.phsa.ca/genomic-innovation-benefits-people-planet （基因組科學中心沿革）
- https://doi.org/10.1093/bioinformatics/btu393 （circlize 論文）
- https://jokergoo.github.io/circlize_book/book/ 、https://cran.r-project.org/web/packages/circlize/index.html
- https://github.com/moshi4/pyCirclize 、https://moshi4.github.io/pyCirclize/ 、https://pypi.org/project/pyCirclize/
- https://github.com/vigsterkr/circos （**非官方倉庫，與官方關係未證實**）
- https://datavizcatalogue.com/methods/chord_diagram.html 、https://www.data-to-viz.com/graph/chord.html （弦圖頁，非 Circos 專頁；Dataviz Catalogue 把 Circos 列為繪圖工具）
- https://en.wikipedia.org/wiki/Chord_diagram_(information_visualization) （英文維基百科弦圖條目；英文「Circos」條目 https://en.wikipedia.org/wiki/Circos 會重新導向到這裡，**不是** Circos 專頁，只可當「外界常把 Circos 與弦圖混為一談」的旁證）
- 查核限制（打不開，未核、僅記名不列連結）：*Genome Research* 期刊官方頁與論文 DOI（登入轉址迴圈）；`github.com/circos/circos`（404，不存在）；Dataviz Project 首頁與弦圖頁（403）；論文腳註中的舊官方網址 mkweb.bcgsc.ca/circos 與舊版線上表格檢視器（403）；Dataviz Catalogue 圓形網路試探頁、data-to-viz 圓形版面試探頁（404）；Dataviz Catalogue、data-to-viz 沒有 Circos 專頁

X 教學原帖：本輪查無可用教學原帖（搜尋結果多為工具閒聊、「Circos 風格」弦圖推廣或新工具發表；不編造）。

鄰居 pattern：`chord-matrix.md`（只有類別流量）、`arc-diagram.md`（直線版面拓撲）、`circular-bar.md`（單層類別長條）、`sunburst-hierarchy.md`（同心環＝階層）、`sankey-flow.md`、`biofabric.md`、`adjacency-matrix.md`、`force-network.md`、`hierarchy-icicle.md`、`flame-graph.md`、`volcano-plot.md`（同屬基因體學常見圖，但火山圖是差異分析的優先排序散點）、`manhattan-plot.md`（環狀曼哈頓圖只是 −log10(p) 峰值，不是 Circos 多軌連結）、`locuszoom.md`（單一染色體區間的關聯放大，不是環狀多軌全景）、`karyotype-ideogram.md`（染色體形態與帶型的線性或成對示意，不是環狀多軌）；階層邊捆綁尚無專檔。

圖檔留在教圖／skill-pack（素材包 `images/`，22 張，圖說用 SKILL-PACK.md 修正後版本），本 repo **不複製**大圖。可當範例對照的是 official-sample-panel（四格：細連線、寬帶、多軌加扇出、只有多軌）、plottypes（元件 A–T）、official-panel-genomic、official-panel-general（非基因組：購車、化學反應性、約會趨勢）、official-panel-tableviewer、pmc-1639fig5／6／7（拷貝數多軌、區段拉出、連續刻度放大）、guide-conservation、sample-large-23／24、tut-tutorial-05-01／06-01／08-01、globalscale（刻度變換）、official-rules（執行期規則）、feature-americanscientist、feature-nyt-epigenome、conde-nast（Krzywinski 與 John Grimwade 合作設計，**不是** 23andMe 製作）、car-purchase；pycirclize-pyCirclize_gallery 與 circlize-examples 要標「同家族實作，不是官方 Circos」。對帳見 `ATTRIBUTION.md`。
