# Pattern: biofabric

> **圖種**：BioFabric（生物織布圖、表格式網路圖；兩個中文名皆為暫譯，非通用定名）
> **來源（納茲教圖）**：`teach-viz/2026-09-27-am-biofabric.md`（方法教學；首次正式主課）
> **亦稱**：英文固定寫 BioFabric（專有名詞，源自開源工具名與 2012 年論文標題）；文獻有時歸入 tabular network visualization／tabular graph drawing 家族；yFiles 用例頁稱原名 Massive Sequence View（僅見於該頁，未另核原始文獻）
> **核心**：**節點＝水平線（每節點獨占一列）、邊＝垂直線段（每邊獨占一欄，連起兩個節點列）**。刻意採用正交、表格式的網路視圖來「梳開毛球」，讓每一條邊都能被個別辨識
> **出處**：William J. R. Longabaugh（Institute for Systems Biology），*Combing the hairball with BioFabric: a new approach for visualization of large networks*，BMC Bioinformatics 13:275，2012-10-27，DOI 10.1186/1471-2105-13-275

## When

- 問「這張網太密，力導向會糊成毛球；我要**每一條邊**都看得見，並比較誰跟誰的連線型態相似，或把邊依類型／條件／時間排開」
- 形狀：節點清單＋邊清單（`source, target`；有向或無向；可選邊類型、權重、時間）；中大型或高密度網路，多重關係邊、平行邊不該疊成一團
- 邊或節點有清楚的分組維度：關係類型、實驗條件、時間片段、部門、自我中心網路的距離層級
- 讀者願意學「列＝節點、欄＝邊」的讀法（初看陌生，但教得會）

## Recommend

- **主選**：BioFabric（正交織物：水平節點列＋垂直邊欄，端點用小方塊或小圓點）
- **判讀**：水平方向沿「邊的序列」瀏覽（邊愈多版面愈寬，像可橫向捲動的織物）；垂直方向是節點順序；由左上到右下的**階梯／楔形邊扇**用來比較不同節點的連線型態
- **布局與變體（同一家族，要標清楚用了哪個）**：
  - **預設布局**：從連線最多的連通元件開始廣度優先走訪，相鄰節點依度數排列；先排節點列、再排邊欄，讓邊排成階梯
  - **連通性相似布局（connectivity layout）**：連線型態相近的節點排在一起，形成連續的相似邊扇
  - **陰影連結（shadow links）**：每條邊複製一份陰影，讓兩個端點在各自的節點區都列出全部相連邊（代價：圖寬加倍）
  - **連結分組（link groups）**：邊依類型、條件或時間片段橫向分塊（例：社交｜協作｜呈報；葡萄糖｜油酸條件）
  - **節點區底色（node zone shading）**：節點區交替淺藍、淺粉底色，長距離橫向追蹤不易看錯列
  - **子集視圖／網路巡覽**：選取相鄰節點另開子集視圖，或沿列、欄逐步巡覽
- **備選（何時改用哪一種）**：
  - 節點少、邊稀疏，要空間群聚直覺 → **力導向網路**（`force-network.md`）
  - 只沿單一軸線看關係、要好標節點名 → **弧線圖**（`arc-diagram.md`）
  - 只要「有／無」或權重的對稱矩陣熱讀，不需要把邊排成可分組的欄 → **鄰接矩陣**（`adjacency-matrix.md`）
  - 故事是份額、流向或階段轉移 → **弦圖**（`chord-matrix.md`）／**桑基**（`sankey-flow.md`）／**沖積**（`alluvial-stages.md`）
  - 有可信階層＋葉連線 → 階層邊捆綁（HEB）；要比多張網、節點分配到數條軸 → 蜂巢圖（兩者目前只在 `references/chart-heuristics.md`）
  - 精確比較少數幾條邊的權重 → 排序表、長條或標數值的矩陣
  - 地理鄰近或實際路徑 → 流量地圖或節點地圖

## Avoid

- **故事其實是流量寬度或份額**卻硬用 BioFabric → 桑基、沖積、弦圖
- **列序、欄序隨便排**：階梯與邊扇糊掉——布局本身就是分析步驟
- **沒寫讀法**：第一次給讀者看要註明「列＝節點、垂直線＝關係」；分組、方向要有圖例
- 全圖過寬還硬塞單一螢幕，不用子集視圖、陰影連結或巡覽
- 用邊扇目測爭「誰的次數第一」→ 另附計數表
- 把呈報這類**階層邊**和協作邊混在一起解讀 → 分組分開看
- 節點少、邊稀疏也為了新穎而換成 BioFabric
- **與鄰近圖種混**：
  - 力導向：節點是點、邊朝任意方向延伸，稠密時交纏成毛球；BioFabric 節點展開成整列水平線、邊一律垂直
  - 弧線圖：節點排在單一軸線、邊畫成弧線；BioFabric 是「列 × 欄」正交織物
  - 鄰接矩陣：格子填有無或權重、讀色塊；BioFabric 仍畫「線」，只是強制正交，且邊可依語意排成連續欄位區塊
  - 階層邊捆綁：依階層把邊捆成束；BioFabric 不預設階層樹
  - 蜂巢圖：節點分配到數條軸再連線；BioFabric 只有水平節點列與垂直邊欄
  - 弦圖／桑基／沖積：講份額、流向、階段轉移；BioFabric 講「誰與誰相連、連線型態是否相似」
- 圖說寫錯：官方 Gallery 檔名含 GOT-1200 的圖**不是**影集，而是 Influential Thinkers（思想家影響關係網）
- 頁面或範例上的節點數、邊數未自行複核就當事實引用

## Produce checklist

- [ ] 故事句含：要梳開哪張毛球／比較哪些節點的連線型態／哪幾類關係分塊比較
- [ ] 邊表：至少 `source, target`；有向關係保留方向；關係類型、條件、時間、權重另開欄位（官方工具常用與 Cytoscape 相同的定位字元分隔／`.sif` 風格匯入）；節點清單與邊表端點對得上
- [ ] 列序：按度數、名稱，或連通性相似；圖注寫排序依據
- [ ] 欄序：先依來源列、再依目標列排，讓邊扇呈楔形；有連結分組就先按組別排成橫向區塊
- [ ] 畫法：每節點一條水平線、每邊一條垂直線段、端點加標記；邊可比節點線深，讓連線「浮」在節點列上
- [ ] 太寬：陰影連結、節點區底色、子集視圖／巡覽，不硬塞單一螢幕
- [ ] 圖例：讀法一句話「每一列＝一個實體，每一條垂直線＝一筆關係」；連結分組名稱與顏色；節點分區（例如部門）與底色意義；有向關係的方向標記；資料來源
- [ ] 精確數值（誰的邊最多）另附計數表
- [ ] 工具誠實（只寫素材包證實的）：**BioFabric** Java 桌面版（Institute for Systems Biology；GitHub `wjrl/BioFabric`；LGPL 2.1；1.0 版 2012 年 7 月、第 2 版 Beta Release 2 於 2019-06-15）；**RBioFabric**（R；GitHub `wjrl/RBioFabric`，描述檔版本 0.3、2013-07-07、依賴 igraph、MIT；**未上架 CRAN**，須從 GitHub 安裝）；**D3BioFabric**（JavaScript／D3.js；GitHub `wjrl/D3BioFabric`）；**yFiles／yWorks**（產品說明稱 biofabric，可對節點與邊獨立排序、分組；獨立線上示範深層連結 404，以產品說明頁為準）。Dataviz Catalogue、data-to-viz、Dataviz Project 都沒有 BioFabric 專頁
- [ ] 示範數字標「數字未核」
- [ ] 自檢：節點少、邊稀疏時力導向／弧線是否已夠清楚？讀者其實要矩陣熱讀（→ 鄰接矩陣）或流量寬度（→ 桑基／沖積／弦圖）嗎？

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-biofabric.csv` — 邊表 `source, target, relation, weight`；虛構中型軟體公司員工關係網，17 個節點、38 條邊。節點前綴表示部門（Eng＝工程、Sales＝業務、Res＝研究、Mgr＝管理），可當節點列分區；`relation` 分 social（社交 8 條）、collaboration（協作 14 條）、reporting（呈報 16 條），直接當連結分組排成「社交｜協作｜呈報」三個橫向區塊；`weight` 是虛構互動強度。示範讀法：Eng_Ada 那一列在協作區塊有 6 條垂直線、社交區塊完全空白（工作綁定強、私下連結弱）；Mgr_Omar 在呈報區塊有 7 條（階層邊，與協作邊分開解讀）。要說「誰協作最多」請附計數表，不要只靠邊扇目測

## 參考連結（可點；皆出自素材包 sources.txt 第一段）

- https://biofabric.systemsbiology.net/ （官方網站：定義、Super-Quick 毛球對照、酵母蛋白質網例；License 段落）
- https://biofabric.systemsbiology.net/gallery/index.html （官方 Gallery：Les Misérables、Wikipedia 投票網、World Bank 合約、礦物元素、酵母條件比較、Influential Thinkers）
- https://biofabric.systemsbiology.net/gallery/pages/SuperQuickBioFabric.html （sources.txt 註：稿內未標狀態，研究筆記記為 200）
- https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-13-275 （Longabaugh 2012 論文）
- https://bmcbioinformatics.biomedcentral.com/counter/pdf/10.1186/1471-2105-13-275.pdf （論文 PDF）
- https://pmc.ncbi.nlm.nih.gov/articles/PMC3574047/ （PubMed Central 全文：讀法、陰影連結、連通性布局、軟體介面、子集視圖）
- https://link.springer.com/article/10.1186/1471-2105-13-275 （sources.txt 註：稿內未標狀態，研究筆記記為 200）
- https://www.yfiles.com/solutions/use-cases/biofabric-visualization （yFiles 用例：公司關係網、物流自我中心網、交易時序網；示例數字未核）
- https://github.com/wjrl/BioFabric
- https://github.com/wjrl/D3BioFabric
- https://github.com/wjrl/RBioFabric
- https://xeno.graphics/biofabric/
- https://www.visualizing.org/biofabric
- https://en.wikipedia.org/wiki/BioFabric
- https://biofabric.blogspot.com/ （sources.txt 註：稿內未標狀態，研究筆記記為 200）
- https://groups.google.com/group/biofabric-users （sources.txt 註：稿內未標狀態，研究筆記記為 200）
- https://datavizcatalogue.com/methods/network_diagram.html （一般網路圖鄰近頁，非 BioFabric 專頁；稿內未標狀態）
- https://www.data-to-viz.com/graph/network.html （一般網路圖鄰近頁，非 BioFabric 專頁；稿內未標狀態）
- 查核限制（未核內容、僅記名不列連結）：Dataviz Catalogue BioFabric 專頁 404；data-to-viz BioFabric 專頁 404；Dataviz Project 研究當下 403、複核時首頁 200 但無 BioFabric 專頁（404）；CRAN `RBioFabric` 專頁 404（未上架）；推測的 yFiles 獨立線上示範深層連結 404；GitHub 內容 API 403（改讀原始 README）

X 教學原帖：本輪查無（搜尋命中多為「bio fabric」布料商品等無關貼文；不編造）。

鄰居 pattern：`force-network.md`（點＋任意方向連線；稠密成毛球，本圖梳開）、`arc-diagram.md`（單軸節點＋弧線）、`adjacency-matrix.md`（格子填有無／權重；本圖仍畫線、邊可分組成欄塊）、`chord-matrix.md`、`sankey-flow.md`、`alluvial-stages.md`（份額／流向／階段，不是本圖的故事）、`matrix-heatmap.md`。

圖檔留在教圖／skill-pack（素材包 `images/`，稿內嵌 22 張：官方 3、論文圖 4、Gallery 8、yFiles 6、Xenographics 1），本 repo **不複製**大圖。可當範例對照的是 official-superquick（毛球 vs BioFabric）、official-yeast、pmc-fig1（讀法、子集視圖）、pmc-fig2（陰影連結）、pmc-fig3（連通性布局）、pmc-fig4（軟體介面）、gallery-LesMiz1024、gallery-WorldBankContracts2007-2013-1024、gallery-NigerDetailScreenShot-1024、gallery-Cu-Ag-Au-1200、gallery-OleateGlucoseCompare1200（條件連結分組）、gallery-thinkers（Influential Thinkers，**不是**影集）、gallery-wiki-vote-detail、gallery-SuperQuickBioFabric75（D3 示範）、yfiles-hairball（傳統毛球對照）、yfiles-example、yfiles-company（社交／協作／呈報分組，對應 demo CSV）、yfiles-logistics、yfiles-trading、yfiles-teaser、xeno-main；official-logo 只是品牌橫幅。對帳見 `ATTRIBUTION.md`。
