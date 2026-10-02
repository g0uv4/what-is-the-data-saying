# Pattern: forest-plot

> **圖種**：森林圖（Forest Plot；別名 Blobbogram）
> **來源（納茲教圖）**：`teach-viz/2026-10-02-pm-forest.md`（方法教學；正式課程；首次以森林圖為主題）
> **亦稱**：Blobbogram（可意譯為「團塊圖」，因為方塊像一團一團的點）；也有人把名字拼成 forrest plot
> **核心**：一列一項研究；**方塊是估計、橫線是不確定性（信賴區間）、直線是沒差別（無效線）、菱形是合併結果**。方塊面積依權重，菱形中心是合併估計、菱形寬度是合併信賴區間。
> **一句話**：同一個問題的多項研究放在同一張圖，比較每項研究的估計與精確度，再看合併結果與一致性（異質性）。
> **誠實提醒**：本課只講「怎麼讀、怎麼畫」，不作任何醫療或政策結論；圖只呈現**已被納入的研究**，也不替你判斷這些研究能不能合併。本 repo 的練習資料與模擬圖都是虛構、數字未核。
> **名字的由來**：Lewis 與 Clarke 2001（*BMJ*）說「forest」指一排排線條像一片森林；同文記載 1990 年 9 月一場乳癌統合分析會議上，Richard Peto 開玩笑說名字取自乳癌研究者 Pat Forrest。「forest plot」最早何時印刷出現各來源分歧（維基百科寫 1996 年 5 月的學會海報摘要；BMJ 文則指出另有 1996 年的候選），**本 repo 不下定論**，只說「大約 1996 年前後開始有人這樣稱呼」。依權重畫方塊面積的概念「可能」由 Stephen Evans 在 1983 年提出（原文是保留語氣，照樣保留）。

## 九件必須釘清的事

1. **比值類效應量（風險比 RR、勝算比 OR、危險比 HR）要先取自然對數再算，畫圖用對數軸、無效線在 1；差值類（平均差 MD、標準化平均差）用線性軸、無效線在 0。** 線性軸會扭曲：同一批模擬資料，研究 D 的風險比 2.00、區間 [1.16, 3.46]，線性軸上估計點左側長 0.84、右側長 1.46，橫線看起來不對稱；對數軸上左右各約 0.549，對稱。**看圖先看軸**：metafor 文件的預測區間示範圖橫軸是「對數風險比」，無效線在 0 不是 1。維基百科〈Forest plot〉的通用示意圖橫軸是線性刻度（1.0、2.0、3.0 等距），只拿來認識版型，不當作法。論文若只給風險比與區間，可用「(ln 上限 − ln 下限) ÷ (2 × 1.96)」反推標準誤。
2. **菱形寬度＝合併信賴區間，菱形中心＝合併估計**（左右頂點就是區間下限與上限）。菱形是**合併結果，不是第 N+1 項研究**。菱形有沒有跨過無效線，只回答「在這個信賴水準下能否排除沒差別」。隨機效應下的**預測區間**（描述「下一項新研究可能落在哪裡」）是另一條更長的細線或獨立多邊形，不是菱形，兩者意義不同。
3. **方塊的「面積」與權重成正比，不是邊長。** 本 repo 的模擬圖用「面積＝同一個常數 × 權重百分比」畫，並把圖面只留下方塊後用像素量面積：8 張圖共 73 個方塊（6＋5＋15＋12＋14＋6＋5＋10）的像素面積 ÷ 腳本標的面積，**素材包圖說的逐張範圍合起來是 0.9997–1.0015**；菱形的像素寬 ÷ 合併信賴區間寬約 1.005–1.020（抗鋸齒造成約 1–2% 誤差）。我另外重跑了素材包的 `draw_forest.py`（輸出到暫存資料夾），得到同樣範圍。（任務說明提到的 0.9994 在素材包與教學稿都找不到，以 0.9997 為準。）方塊大＝權重大＝估計較精確，**不是效果大、也不是研究品質好**；效果大小看方塊在橫軸的位置。Excel 要手動調方塊大小時「標記邊長 ∝ 權重的平方根」是本課依「面積 ∝ 權重」推導的**推論，沒有在任何來源或 Excel 官方文件核對過**（Neyeloff 等人 2012 全文沒有提到方塊依權重縮放）。
4. **DerSimonian–Laird（DL）不同於 Paule–Mandel（PM）。** Python statsmodels 的 `combine_effects` 預設的隨機效應方法是 PM 迭代法（函式簽名 `method_re='iterated'`），**不是 DL**；要把 `method_re` 設為 `'dl'` 才是 DL，且它算出的 τ² **不會截為 0**（Q 小於自由度時可能是負值，例如 S1 的 DL 原始值 −0.0064）。同一批 S5 資料：τ² 在 DL 是 **0.05965**、在預設 PM 是 **0.03435**（我用 statsmodels 0.15.0 實跑，並另以 `scipy` 自解 PM 方程式得到相同的 0.03435）；隨機效應合併風險比 DL 是 0.7189 [0.561, 0.921]、PM 是 0.7226 [0.585, 0.892]，顯示到小數兩位都是 0.72，但區間與 τ² 不同，**不要混用**，圖註寫清楚用哪一種。DerSimonian 與 Laird 1986 原論文打不開（DOI 只到出版社轉址頁），沒有逐字核過，所以**公式不能直接說成出自該論文**；Higgins 等人 2003 逐字給出 I² 定義，Neyeloff 等人 2012 逐字給出 τ² 與權重算法；Cochrane 手冊第 10 章的公式是圖片檔，素材包讀不到，不當作公式來源。
5. **I² 的讀法：分級的區間會重疊，不要硬分類。** Cochrane 手冊第 10 章給的粗略分級是 0–40% 可能不重要、30–60% 中等、50–90% 相當大、75–100% 可觀，**刻意重疊**，並強調分級可能誤導，且研究數少時 I² 本身很不穩；Higgins 等人 2003 則暫以 25%、50%、75% 作低、中、高的形容。本 repo 的 S2 資料 I²＝54.9%，剛好落在「30–60% 中等」與「50–90% 相當大」兩個區間，**只當示範，不下定性判斷**。I²＝(Q − 自由度) ÷ Q，表示研究間差異占總變異的比例，**不是效應大小**；Q 小於自由度時取 0。
6. **統合分析的漏斗圖（Funnel plot，檢查小研究是否偏向一側）與商業轉換流程的漏斗圖（Funnel chart）是兩種不同的圖，名字相近、用途完全不同，不要併成同一份範例。** 商業的那種見 [`funnel-stages.md`](funnel-stages.md)；本檔只把統合分析的漏斗圖當對照：每個點是一項研究、橫軸效應量、縱軸標準誤（越精確的越在上方），不為每項研究畫各自的信賴區間橫線，也沒有合併菱形。圖不對稱常被拿來懷疑發表偏差，但也可能來自小研究效應或其他原因。Cochrane 手冊第 13 章建議至少 10 項研究才做漏斗圖不對稱檢定；本 repo 的 S8 剛好 10 項，仍不足以判斷，僅示範版型。
7. **授權（圖）**：R5（metafor 專案站）頁尾標 **CC BY-NC-SA 4.0，僅限非商業使用**，素材包用的是縮小版，屬改作，須標示已作的變更並相同方式分享；R2（Commons〈Pre-term corticosteroid data.svg〉，Thomas Lumley，資料與程式來自 R 套件 rmeta）為 **GPL-2 的 copyleft 授權**（Commons 授權頁逐字為「版本 2」，沒有「或更新版本」），已轉成點陣圖並墊白底屬改作，正式發佈需附授權與修改聲明（GNU 官方原文頁打不開，未逐字核）；**R4、R6、R7、R8 圖本身的授權未明示**（套件本身分別為 GPL 或 MIT），僅作教學示意引用，若要正式發佈建議自畫或取得許可；R1、R3、R14 為 **CC BY-SA 3.0**（改作須相同方式分享）；R9–R13 為 **CC BY**（R9–R12 為 CC BY 4.0，R13 為 CC BY 2.0，需標作者、來源與授權）；R12（Matsukawa 等人）的 CC BY 4.0 標示**目前只有 Wikimedia Commons 一個來源可查**，出版社頁打不開，使用前請再確認；S1–S8 是素材包自製。Cochrane 手冊文字頁可讀，但頁內圖檔與公式讀不到，素材包沒有嵌 Cochrane 圖；本 repo 對 Cochrane 與各論文只連結、只轉述概念。本 repo 不複製任何圖。
8. **不是所有森林圖都有無效線或合併菱形。** 比例（敏感度、特異度、陽性預測值）沒有「沒差別」的固定位置，所以沒有無效線（R13 Kattenberg 等人 2011 的配對森林圖；方塊等大，不依權重縮放）；zEpid 的「森林圖式」效應量圖（R8）每列菱形大小一致，是各列的點估計，**不是統合分析的合併菱形**。所以**菱形的意義要看圖例**。研究設計、族群、結局定義差太多時，菱形可能把「蘋果和橘子」平均起來，這時可只畫各研究、不畫合併菱形（Cochrane 手冊第 10 章的提醒，見素材包整理）。
9. **素材包的潤稿流程說明**：素材包 `SKILL-PACK.md` 與教學稿**都沒有提到 Gemini 潤稿步驟**，無從確認是否做過；本 repo 一律視為「審稿後原稿，潤稿狀態未記載」，已在 `ATTRIBUTION.md` 註明。

## When

- 把同一個問題的多項研究（各自有效應量加信賴區間，或能算出）放在同一張圖，比較每項研究的估計與不確定性，再看合併結果（Lewis 與 Clarke 2001；Cochrane 手冊第 10 章）
- 看一致性：各項研究的方塊與橫線是否大致落在同一區，或四散各處（異質性）
- 看精確度與權重：橫線越短、方塊越大，代表估計越精確、在合併中分量越重
- 檢查個別研究與合併結果的信賴區間有沒有包含「沒差別」的位置
- 亞組比較（每個亞組一顆菱形，另有全部合併菱形）；迴歸模型的多個係數或各時期的估計（森林圖式排版，菱形意義看圖例）
- 一般約 5–40 列；列數更多要分頁、分區標題，或把次要資訊移到補充檔（R9 有 28 列，是列數較多的實例）

## Recommend

- **主選（標準森林圖）**：左欄研究名、中間圖、右欄數字與權重；比值用對數軸、無效線在 1；差值用線性軸、無效線在 0；軸的兩端寫清楚方向（例如「風險比小於 1：提醒組爽約較少」）；底部或角落寫 Cochran 的 Q、自由度、I²（用隨機效應時加 τ²）；**圖註寫合併方法（固定效應，或隨機效應用哪一種 τ² 估計法）**
- **資料前提**：每列一項研究，至少有研究名、效應量、信賴區間下限與上限、權重（可由標準誤算出）；比值類的效應量與區間要先取自然對數。研究只有一兩項時，合併意義有限
- **變體**：
  - **信賴區間跨不跨無效線的讀法對照**：用顏色區分區間跨過與不跨過（S2）
  - **亞組森林圖**：亞組各一顆菱形加全部合併菱形；亞組差異要用**亞組間檢定**判斷，不能只說「一組顯著、一組不顯著」（S6、R7、R10、R11）
  - **固定效應與隨機效應並列**：看權重與菱形寬度如何改變（S5）
  - **加預測區間**（隨機效應）：合併菱形下方多一條預測區間（R6）
  - **森林圖式的效應量圖**：迴歸係數或各時期的估計，菱形等大，不是合併菱形（R8）
  - **配對森林圖**：敏感度與特異度，沒有無效線（R13）
  - **森林圖與漏斗圖並列**：漏斗圖只作對照（S8、R14）
- **備選（何時改用哪一種）**：
  - 單一資料集的原始分布 → [箱形圖](boxplot-summary.md)或散點；箱子的長度不是信賴區間
  - 只有點估計、沒有不確定性（兩個時點或兩組的差距）→ [啞鈴圖](dumbbell-gap.md)或長條圖
  - 兩種測量方法的一致性 → [Bland–Altman 圖](bland-altman.md)
  - 大量項目（基因等）的倍數對顯著性 → [火山圖](volcano-plot.md)
  - 全基因體關聯尖峰 → [曼哈頓圖](manhattan-plot.md)
- **參數與判準範例（範例，不是標準）**：

| 項目 | 數值與出處 | 性質 |
|---|---|---|
| 固定效應權重與合併 | 權重＝1／標準誤²；合併估計＝權重加權平均；合併標準誤＝1／√(權重總和)；95% 區間＝合併估計 ± 1.96 × 合併標準誤（比值類再取指數） | 範例，不是標準 |
| 隨機效應（DL）步驟 | Q＝Σ權重 ×（各研究估計 − 合併估計）²；τ²＝(Q − 自由度) ÷ (Σ權重 − Σ權重² ÷ Σ權重)，小於 0 時取 0；再用 1／(標準誤² ＋ τ²) 當權重（出處 Higgins 2003、Neyeloff 2012；statsmodels 的 DL 不截為 0） | 範例，不是標準 |
| 異質性 I² | 100% × (Q − 自由度) ÷ Q，小於 0 時取 0；Cochrane 第 10 章粗略分級 0–40／30–60／50–90／75–100%（重疊）；Higgins 2003 暫以 25／50／75% 形容低、中、高 | 範例，不是標準 |
| 反推標準誤 | (ln 上限 − ln 下限) ÷ (2 × 1.96) | 範例，不是標準 |
| 方塊大小 | 面積＝同一常數 × 權重百分比（不是邊長）；隨機效應下上下兩個面板各自依自己的權重縮放 | 範例，不是標準 |
| 列數 | 一般約 5–40 列；超過約 40 列要分頁或分區 | 範例，不是標準 |
| 漏斗圖不對稱檢定的研究數 | Cochrane 第 13 章建議至少 10 項 | 範例，不是標準 |
| 顏色 | S2 示範：藍＝區間不跨過 1、橘＝跨過 1（教學配色，非慣例） | 範例，不是標準 |
| 座標範圍 | 區間超出座標範圍卻沒畫箭頭，橫線會看起來比實際短；素材包繪圖程式在這種情況直接報錯，逼你放寬座標 | 範例，不是標準 |

## 與鄰近圖種的區別

| 圖種 | 它回答什麼 | 和森林圖的區別 |
|---|---|---|
| **漏斗圖（Funnel plot，統合分析）**，只作對照 | 檢查小研究是否偏向一側（發表偏差或其他原因）；每點一項研究，橫軸效應量、縱軸精確度 | 森林圖一列一項研究、看每項的估計與區間；漏斗圖畫散點、看整體是否對稱，沒有各自的信賴區間橫線與合併菱形；兩者常搭配 |
| **漏斗圖（Funnel chart，商業轉換流程）**（[`funnel-stages.md`](funnel-stages.md)） | 各步驟逐步留存或流失的人數或比例 | **名字相近、用途完全不同，不要混用、不要併檔** |
| [**箱形圖**](boxplot-summary.md) | 一組**原始資料**的分布：中位數、四分位、離群值 | 箱形圖畫資料本身的分布；森林圖畫估計值的不確定性；箱子的長度不是信賴區間 |
| [**啞鈴圖**](dumbbell-gap.md) | 兩個時點或兩組的**兩個點**之間的差距 | 只有兩點加連線，沒有信賴區間、權重、合併菱形 |
| [**Bland–Altman 圖**](bland-altman.md) | 兩種量測方法的**一致性**：差值對平均值，畫平均差與 ±1.96 個標準差的一致性界限 | 兩者都有 1.96，意義不同：Bland–Altman 的 ±1.96 標準差描述「個體差異的範圍」；森林圖的 ±1.96 標準誤描述「估計的不確定性」 |
| [**火山圖**](volcano-plot.md) | 大量項目（基因等）的倍數變化對顯著性 | 火山圖的點是大量項目、森林圖的列是少數研究；一般不併用 |
| **一般散點圖**（[`correlation-scatter.md`](correlation-scatter.md)） | 兩變數的關係 | 森林圖一軸是效應量、另一軸只是列的順序，不是兩個變數的關係 |

判斷口訣：**多項研究、每項有估計加區間、要看合併與一致性 → 森林圖；一組原始資料的分布 → 箱形圖；兩點差距 → 啞鈴圖；兩種量測方法一致性 → Bland–Altman；小研究是否偏向一側 → 漏斗圖（統合分析）；階段流失 → 漏斗圖（商業）。**

## Avoid

- 把菱形當成一項研究（它是合併結果）；把方塊大小讀成效果大小或研究品質（權重只反映精確度，不反映研究設計好壞）
- 忘記無效線的位置（比值在 1、差值在 0；對數風險比軸上在 0），把「有差別」讀反
- 比值沒用對數尺度：線性軸上 0.5 與 2 離 1 的距離不一樣，橫線左右不對稱，大於 1 的值被放大
- 「信賴區間跨過無效線＝沒有效果」：只代表在這個信賴水準下無法排除沒差別；樣本小、區間很長時常是證據不足，不是證明沒有
- 只看「有幾項研究顯著」：這是票數計算，會忽略權重與精確度
- 把 I² 當效應大小，或硬把 54.9% 這種落在重疊區間的值歸成單一類別；研究數少時 I² 很不穩
- 固定效應與隨機效應靠「哪個結果好看」選（回答的問題不同；隨機效應把 τ² 加進每項權重，小研究相對權重變大、菱形變寬；沒有異質性時兩者結果相同）；事先依問題與資料決定並說明理由
- 把 DL 和 PM 混用（statsmodels 預設是 PM；S5 的 τ² 0.05965 對 0.03435）
- 把整體菱形當成真相，無視亞組差異（S6：亞組合併值 0.64 對 1.00）
- 只看信賴區間、不看預測區間（隨機效應下，預測區間才描述下一項新研究可能落在哪裡，通常寬很多）
- 座標軸截斷信賴區間卻沒畫箭頭
- 把森林圖當成「研究都納入了」：沒被發表、沒被找到的研究看不到，要另搭配漏斗圖等檢查（至少 10 項）
- 把統合分析的漏斗圖（Funnel plot）和商業轉換的漏斗圖（Funnel chart）混為一談
- 把模擬圖或練習資料當成真實證據；把授權未明示的外部圖當可自由再用（R5 僅限非商業、R2 為 GPL-2 copyleft）
- 把 X 查詢結果當成「X 上沒有人談」

## Produce checklist

- [ ] 故事句是「同一個問題的多項研究，估計與不確定性如何、合併後如何、彼此一致嗎」；先想清楚這些研究**能不能合併**
- [ ] 整理五個欄位：研究名、效應量、信賴區間下限、上限、權重；比值類先取自然對數再算；只有風險比與區間時用「(ln 上限 − ln 下限) ÷ (2 × 1.96)」反推標準誤
- [ ] 選合併方法並**寫進圖註**：固定效應，或隨機效應（DL 或 PM 或其他，明講；用 statsmodels 時確認 `method_re`）
- [ ] 算權重與合併；算 Q、自由度、I²（小於 0 取 0）、τ²（隨機效應時）
- [ ] 比值用對數軸、無效線在 1；差值用線性軸、無效線在 0；軸兩端寫方向
- [ ] 方塊**面積**與權重成正比；橫線畫 95% 信賴區間；菱形寬度＝合併信賴區間；左欄研究名、右欄數字與權重
- [ ] 排序（依年份或依權重）要在圖旁寫明，排序本身沒有意義
- [ ] 區間超出座標範圍時放寬座標或畫箭頭，不要默默截斷
- [ ] 有亞組就畫亞組菱形並做亞組間檢定；隨機效應時考慮加預測區間
- [ ] 解讀順序：先讀軸（比值還是差值、對數還是線性、無效線在哪）→ 每一列的位置與橫線長度 → 有沒有跨過無效線 → 菱形 → 異質性 → 最後提醒「這是示範，真實資料還要問能不能合併、有沒有漏掉沒發表的研究」
- [ ] 要查發表偏差 → 另畫漏斗圖（至少 10 項），不要把森林圖當證據
- [ ] 示範數字標「數字未核」；真實論文圖只示範讀法，不作醫療結論
- [ ] 工具誠實（只寫素材包證實的）：
  - **R**：metafor（`forest`；CRAN 標示 GPL-2 或 GPL-3）、meta（`forest`）、forestplot（吃表格欄位；CRAN 標示 GPL-2）、forestploter、survminer（臨床風險比，見 Datanovia 教學）
  - **Python**：statsmodels（`combine_effects`、`plot_forest`；預設 PM，DL 要設 `'dl'`）、zEpid（效應量圖；MIT）、Matplotlib 自畫（素材包腳本）
  - **Cochrane Review Manager（RevMan）**：官方知識庫寫明在「Graphs」分頁設定森林圖，可依研究編號、年份、權重、效應量、偏差風險排序
  - **jamovi**：MAJOR 模組是第三方模組（GPL-3.0，不是 jamovi 官方產品），說明列有基本森林圖，Coventry 大學有教學頁；另有使用者在論壇回報勝算比類的森林圖橫軸仍顯示對數值（**單一來源**）
  - **Excel**：Neyeloff 等人 2012 的做法是散佈圖（X 放效應量、Y 放列號，合併結果設為 1 放最底）加 X 方向「自訂誤差線」，Excel 把誤差線的上、下數值當成「與中心點的差距」，不是區間上下限本身（所以正值欄放「上限減估計」、負值欄放「估計減下限」——這是素材包對原文步驟的解讀）；座標軸設為對數刻度；「無效線用同樣方式再加一組資料」是推論，原文沒有逐字寫
  - **Google 試算表**：官方說明頁寫明誤差線類型只有固定值、百分比、標準差三種，沒有逐項自訂上下限，所以不能照 Excel 做法；素材包沒有實測，也不建議用它畫
  - JASP、Stata 的頁面素材包沒能打開，不寫其功能

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-forest-fictional.csv` — 61 列資料（約 5.5 KB）；檔頭 8 行以 `#` 開頭，讀取要略過（pandas 用 `comment='#'`）；欄位 `dataset, panel, study, subgroup, measure, effect, analysis_value, se, ci_lower, ci_upper, weight_fixed_pct`（前 8 欄是輸入、後 3 欄是推導欄；`analysis_value` 對 RR 是自然對數、對 MD 直接是差值；`se` 對 RR 是對數風險比的標準誤）。8 個資料集 S1–S8（對應圖 S1–S8）、10 個分析單位（S3 有風險比 RR 與差值 MD 兩批，S4 有低 low 與高 high 異質性兩批）。
- 我重新計算的數字（**以實際計數為準**；與素材包檢查輸出逐項一致，素材包文字與 CSV 沒有發現不一致；推導欄 `ci_lower`、`ci_upper`、`weight_fixed_pct` 全部重算相符）：
  - S1（6 項）：固定效應合併 RR 0.81 [0.70, 0.94]；Q＝4.11、df＝5、I²＝0.0%（原始值 −21.7% 截為 0）；DL τ² 原始值 −0.0064（截為 0）；區間不跨過 1 的 2 項（A、C）、含 1 的 4 項
  - S2（5 項）：前 2 項區間不含 1、後 3 項含 1；合併 0.82 [0.72, 0.93]；Q＝8.87、df＝4、I²＝54.9%（落在 30–60% 與 50–90% 兩個重疊區間）
  - S3：RR 一批合併 0.92 [0.76, 1.13]（含 1），研究 D 線性軸左 0.84、右 1.46（對數軸等長約 0.549）；MD 一批合併 −1.68 [−2.67, −0.70]（整個區間在 0 的左側）
  - S4：低異質性 Q＝0.36、I²＝0.0%、合併 0.70；高異質性 Q＝35.43、I²＝85.9%、DL τ²＝0.138、合併 0.63 [0.56, 0.71]；用顯示的兩位數 RR 重算高異質性的 Q 約 34.75（不是 35.43，因為圖上只顯示小數兩位）
  - S5（7 項）：Q＝16.05、df＝6、I²＝62.6%；DL τ²＝0.05965（PM＝0.03435）；固定效應 0.75 [0.66, 0.85]、對數尺度區間寬 0.255；隨機效應（DL）0.72 [0.56, 0.92]、寬 0.495（約 1.94 倍）；權重第一項 29.4%→21.5%、第二項 42.4%→22.9%、第七項 2.6%→7.2%
  - S6（6 項，兩亞組各 3）：亞組 A 合併 0.64 [0.51, 0.79]（I²＝0.0%）、亞組 B 1.00 [0.83, 1.21]、全部 0.83 [0.72, 0.95]；亞組間 Q＝9.68、df＝1、p＝0.0019（寫成 0.002；z² 與 Q 兩種寫法相同）
  - S7（5 項）：權重 86.6／1.0／7.8／3.0／1.5（%）；權重最大的「大樣本」RR 0.96、最小的「小樣本」RR 0.35（區間 [0.12, 1.03] 含 1），權重比 84.0 倍；合併 0.92 [0.82, 1.02]，區間上限略超過 1（「大樣本」「小樣本」只是示意說法，權重實際由標準誤決定）
  - S8（10 項，亂數種子 9）：合併 0.76 [0.68, 0.84]、I²＝0.0%；落在「合併估計 ± 1.96 × 標準誤」之內的點 10／10（含研究 1 本身）；權重 27.1／18.9／13.9／10.6／8.4／6.8／5.1／4.0／3.0／2.2（%）
- 示範讀法：以 S1 為例（假設情境：就診前一天提醒是否降低爽約）——先讀軸（RR、對數軸、無效線在 1）→ 研究 A（0.70）與 C（0.60）的橫線沒跨過 1，其餘四項跨過 → 菱形 0.81 [0.70, 0.94] 整顆在 1 的左側 → Q＝4.11、I²＝0.0%，彼此一致 → 最後別忘了這是模擬示範。
- `sample-forest-selfcheck.py` — 自檢腳本（只需 numpy；有安裝 statsmodels 時多做一道交叉核對；**以絕對路徑讀同資料夾的指定檔名，不搜尋檔案**，並以 `assert` 驗證權重、合併估計、Q、df、I²、τ²、區間跨不跨無效線等；見 `examples/data/README.md`）。
- 素材包另附 `draw_forest.py`（產生 8 張模擬圖，需要 numpy、scipy、matplotlib 與 Noto Sans CJK TC 字型）：**本 repo 不收**，只在 `ATTRIBUTION.md` 註明它存在於素材包。我查過：預設輸出到腳本旁的 `redraw/` 子資料夾（不會寫進 `/workspace/teach-viz/`），可用環境變數 `FOREST_OUT_PREFIX` 改路徑，沒有憑證或寫死的外部路徑；但它是繪圖用的大檔（約 40 KB），而且 repo 不放圖。

## 參考連結（可點；皆出自素材包 sources.txt 且標可開）

- 條目與詞彙：https://en.wikipedia.org/wiki/Forest_plot 、https://en.wikipedia.org/wiki/Funnel_plot 、https://en.wikipedia.org/wiki/Meta-analysis 、https://en.wikipedia.org/wiki/Bland%E2%80%93Altman_plot 、https://en.wikipedia.org/wiki/Box_plot
- 圖片頁（作者與授權）：https://commons.wikimedia.org/wiki/Category:Forest_plots 、https://commons.wikimedia.org/wiki/File:Generic_forest_plot.png 、https://commons.wikimedia.org/wiki/File:Pre-term_corticosteroid_data.svg 、https://commons.wikimedia.org/wiki/File:Forestplot01.jpg 、https://commons.wikimedia.org/wiki/File:Example_of_a_symmetrical_funnel_plot_created_with_MetaXL_Sept_2015.jpg 、https://commons.wikimedia.org/wiki/File:Forest_plots_for_positive_predictive_values_for_comparing_the_performance_of_digital_rectal_examination_and_prostate-specific_antigen_as_a_screening_test_for_prostate_cancer.jpg （Matsukawa 等人圖頁，CC BY 4.0 目前僅此單一來源）
- 方法與論文：Lewis 與 Clarke 2001（BMJ）https://www.bmj.com/content/322/7300/1479 、https://pmc.ncbi.nlm.nih.gov/articles/PMC1120528/ ；Cochrane 手冊 https://training.cochrane.org/handbook/current/chapter-10 、https://training.cochrane.org/handbook/current/chapter-13 （會轉到 cochrane.org 網域；頁內公式與圖是圖片檔，打不開）；Higgins 等人 2003 https://pmc.ncbi.nlm.nih.gov/articles/PMC192859/ ；Neyeloff 等人 2012（PubMed Central 版）https://pmc.ncbi.nlm.nih.gov/articles/PMC3296675/
- 真實案例（只示範讀法，不作醫療結論）：Naito 等人 2023 https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0280308 ；Schumann 等人（PubMed Central 版）https://pmc.ncbi.nlm.nih.gov/articles/PMC8891239/ ；Kattenberg 等人 2011 https://pmc.ncbi.nlm.nih.gov/articles/PMC3228868/
- 套件與工具文件：https://www.metafor-project.org/doku.php/plots:forest_plot 、https://wviechtb.github.io/metafor/reference/forest.rma.html 、https://cran.r-project.org/package=meta 、https://search.r-project.org/CRAN/refmans/meta/html/forest.meta.html 、https://cran.r-project.org/package=forestplot 、https://cran.r-project.org/web/packages/forestplot/vignettes/forestplot.html 、https://cran.r-project.org/package=forestploter 、https://www.datanovia.com/learn/pharma-clinical/04-tlf-generation/forest-plot-survminer 、https://www.statsmodels.org/stable/generated/statsmodels.stats.meta_analysis.CombineResults.plot_forest.html 、https://www.statsmodels.org/stable/generated/statsmodels.stats.meta_analysis.combine_effects.html 、https://zepid.readthedocs.io/en/latest/Graphics.html 、https://github.com/pzivich/zEpid
- 軟體操作：RevMan 知識庫 https://documentation.cochrane.org/revman-kb/manual-input-analyses-259686817.html 、https://documentation.cochrane.org/revman-kb/report-analysis-results-142314014.html ；jamovi MAJOR 模組（第三方）https://github.com/kylehamilton/MAJOR ；Coventry 大學 jamovi 教學 https://sigmacoventry.github.io/website/Jamovi/Meta-Analysis-of-Continuous-Outcomes-Using-Jamovi_readability.html ；Google 文件編輯器說明（誤差線）https://support.google.com/docs/answer/9085344
- X 貼文（素材包逐則確認存在；素材包只讀到貼文標題與摘要；只作連結、不當正式教材）：https://x.com/datanovia/status/2100577727585661267 （survminer 與 ggplot2 的可執行教學，連到上面的 Datanovia 頁；教學向，最貼近；其中危險比 1.64〔0.74–3.60，跨過 1〕為作者數字，未另行驗算）、https://x.com/CleverAcademy_/status/2102442802135351320 （「How to read a forest plot in 30 seconds」，宣傳式簡述）、https://x.com/rafaelglezm/status/2105552773328850972 （心臟科醫師兼統計編輯評論：比值估計值在橫軸應用對數尺度，信賴區間才會對稱；評論，與對數尺度直接相關）
- 查核限制（未核；僅記名、不列連結，皆**不是已驗證的來源**）：Springer 的 Schumann 等人出版社頁（回 200 但只有瀏覽器驗證頁 Client Challenge）、BioMed Central 的 Neyeloff 2012 官網頁（轉到 Springer 後同樣只有驗證頁）、European Urology Oncology 的 Matsukawa 出版社頁（導向 cookie 錯誤頁）、Matsukawa 論文的 DOI 與 DerSimonian 與 Laird 1986 原論文的 DOI（兩個都只到 Elsevier 轉址頁，讀不到內文）、cochrane.org 的手冊總覽頁 `learn/courses-and-resources/handbook`（404）、statsmodels 的 `meta-analysis.html`、Stata 的 `meta.html`、jamovi 的 `library.html`（以上三個是猜的網址，404，不作為來源）、`jasp-stats.org`（HTTP 202，只有自動轉向驗證頁 sgcaptcha 的空白頁，不當證據）。
- 刻意不連結的可開頁：X 貼文 `lddcmumbai/status/2104896874318864676`（診所帳號推廣一支「Forest plot Interpretation made easy」影片，素材包沒看影片內容；宣傳式）與 `nadeemshafique/status/2103558773919064200`（宣布 Medium 文章〈Before the Forest Plot: Four Decisions That Make a Meta-Analysis Trustworthy〉，只有標題可確認，文章內文未讀，連結中的作者帳號與發文帳號名稱不同，不當作可信的教學來源）
- X：素材包找到 5 則貼文（教學向以 Datanovia 那則最完整，其餘為宣傳式簡述或評論）；X 搜尋有數量與排序限制，**不能由此推論「X 上沒人談森林圖」**，沒有編造連結

鄰居 pattern：`boxplot-summary.md`（原始資料的分布；箱子長度不是信賴區間）、`dumbbell-gap.md`（兩點差距、無信賴區間）、`bland-altman.md`（兩者都有 1.96，意義不同）、`volcano-plot.md`（大量項目的倍數對顯著性）、`manhattan-plot.md`（基因組位置對 −log10(p)；「效應量森林圖」常與它搭配）、`funnel-stages.md`（名字相近但完全不同：商業轉換流程的 Funnel chart）、`correlation-scatter.md`（兩變數關係）；統合分析的漏斗圖（Funnel plot）只作本檔的對照，不另立專檔。

圖檔留在教圖／skill-pack（`/workspace/skill-packs/2026-10-02-pm-forest/images/`，22 張＝14 張真實／示意圖加 8 張模擬圖，圖說與教學稿逐字相同），本 repo **不複製**任何圖。編號依素材包圖例清單（`SKILL-PACK.md` 第 5 行寫「圖 R12 已移除」，但同檔圖例清單的 R12 是 Matsukawa 圖、影像檔也在，兩者矛盾，這裡以圖例清單與檔案為準）。可對照的圖：R1 wikipedia-generic-forest-plot（CC BY-SA 3.0；**橫軸是線性**，示意）、R2 wikipedia-preterm-corticosteroid（GPL-2；轉點陣屬改作；合併勝算比約 0.53）、R3 commons-forestplot01（CC BY-SA 3.0；極簡四列加菱形）、R4 metafor-doc-arrangement（授權未明示；版面參數解剖，**沒有權重欄**）、R5 metafor-wiki-forest-plot（**CC BY-NC-SA 4.0 僅限非商業**；縮小版；卡介苗資料集 13 項，圖底隨機效應合併 RR 0.49 [0.34, 0.70]，Q＝152.23、df＝12、I²＝92.2%、τ²＝0.31，該圖用 REML 估 τ²，不是 DL；用 DL 重算 τ²＝0.309、I²＝92.1%、合併同為 0.49〔以上為素材包讀數與重算，本 repo 沒有該資料集，未獨立重算〕）、R6 metafor-doc-prediction-interval（授權未明示；對數風險比軸、無效線在 0；合併 −0.71 [−1.07, −0.36]、預測區間 [−1.87, 0.44] 跨過 0）、R7 forestplot-vignette-subgroups（授權未明示；**虛構示範資料**，人名研究名）、R8 zepid-effect-measure-plot（授權未明示；縮小版；菱形等大，**不是合併菱形**；已發表論文資料）、R9 commons-social-isolation-hr（CC BY 4.0；28 列，合併 HR 1.33 [1.26, 1.41]、I²＝76%、Q＝112.51、df＝27）、R10 commons-social-isolation-by-tool（CC BY 4.0；依測量工具的亞組）、R11 commons-concurrent-training-explosive-strength（CC BY 4.0；標準化平均差，18 項分兩亞組〔13＋5〕，整體 −0.28 [−0.48, −0.08]）、R12 commons-dre-psa-ppv（CC BY 4.0，**單一來源**；六個面板各自隨機效應合併，效果量是比例；解析度低）、R13 pmc-malaria-rdt-fig3（CC BY 2.0；配對森林圖，方塊等大、**沒有無效線**；解析度低）、R14 commons-funnel-symmetric-metaxl（CC BY-SA 3.0；**這是漏斗圖，不是森林圖**，只作對照，檔名叫對稱但仍有數個點在漏斗之外）；模擬資料自畫八張 S1 anatomy／S2 crossing-null／S3 log-vs-linear／S4 heterogeneity／S5 fixed-vs-random／S6 subgroups／S7 misread-square-size／S8 with-funnel（皆**模擬資料**、數字未核）。對帳見 `ATTRIBUTION.md`。
