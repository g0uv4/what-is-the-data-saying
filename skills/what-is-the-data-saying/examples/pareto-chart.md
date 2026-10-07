# Pattern: pareto-chart

> **圖種**：柏拉圖／帕累托圖（Pareto chart；Pareto diagram、Pareto analysis）
> **來源（納茲教圖）**：`teach-viz/2026-10-03-pm-pareto.md`（方法教學；正式課程；首次以柏拉圖為主題。原定當天下午的階層式邊捆綁圖已作廢，改教本題）
> **亦稱**：帕雷托圖、排列圖法、主次因素分析法（中文維基百科臺灣繁體頁面所列）；英文別名 Pareto diagram、Pareto analysis（ASQ 詞彙頁所列）；日文パレート図
> **核心**：把原因（類別）由大到小排成長條，再疊一條**累計百分比**折線；左軸是件數或金額，右軸是累計百分比 0–100%，一眼看出該先處理哪幾項。
> **口訣**：柱子由大到小、折線一路累計到 100%、「其他」通常放最右。
> **一句話**：一堆類別，哪幾項加起來占了大部分？先看累計線第一次到達或越過 80% 是在第幾項。
> **誠實提醒**：本課只講「怎麼讀、怎麼畫」。範例圖與本 repo 的練習資料都是虛構或示意，**數字未核**；柏拉圖只告訴你哪類多、哪類貴，不告訴你為什麼。
> **潤稿狀態**：素材包與教學稿都明說**沒有經過 Gemini 潤稿**（Gemini 登入失效），也沒有改用其他模型潤稿；文字是審稿後由人工整理的原稿。
> **撞名**：在臺灣「柏拉圖」同時是哲學家 Plato 的譯名（在 X 搜「柏拉圖」多半是談哲學家或「柏拉圖式戀愛」）；人工智慧模型排行榜常說的「Pareto 前沿」與經濟學的「帕累托最優」（Pareto efficiency）是不同概念，英文維基百科說 Pareto 法則與 Pareto 效率「只有間接關係」。

## 十一件必須釘清的事

1. **80/20 只是經驗法則，不是定律；讀圖要看累計線第一次到達或越過 80% 的是第幾項，80% 不是門檻。** 「Pareto 法則」俗稱八二法則：大約 80% 的結果來自 20% 的原因。英文維基百科說實際可能是 90:10 或 70:30，兩個數字也不必加起來等於 100。本 repo 的練習資料（8 類、340 件）：前 3 項累計 75.3%、前 4 項累計 84.4%，所以是第 **4** 項（8 類中的 4 類＝50% 的類別，不是 20%）第一次到達 80%，而且「4 項」包含越過 80% 的那一項本身；單項占比超過 20% 的只有第 1 項（34.7%）和第 2 項（25.3%）。模擬圖 S5 對照：集中型 8 項中前 3 項就到 84.6%；平坦型要 8 項裡的 **6** 項才累計到 **80.0%**（剛好等於 80%，不是超過，所以寫「到達或越過」）。Pareto 本人常用的指數約 1.5，這時前 20% 的人約得 58% 的所得，離 80% 很遠（Persky 1992 年回顧文章，我另外開啟該 PDF 核對過這句）；維基百科 Pareto distribution 條目另引用 William H. Press 2025 年〈Pareto's Doubtful 80/20 Rule〉質疑，這篇素材包只讀到摘要與引用，僅轉載。
2. **「其他」放最右：文字出處只有 Six Sigma Material，ASQ 並沒有規定；寫「通常」，不要寫「永遠」。** Six Sigma Material 明寫「其他放右側」；實例有圖 R16（其他比第 3 台還大，仍排在最右）與圖 R6（Otros 10 比 C 的 8 大，仍排最右）。ASQ 只說零碎小項可以歸為「其他」，沒有規定位置；臺灣教學文也不是共同寫法，不要寫成「ASQ 與臺灣教學文都這樣寫」。模擬圖 S3（另一份虛構資料，總數 325）示範：「其他」36 件比瑕疵 D（30）、E（18）、F（12）都大；錯誤做法是把它插在中間第 5 位（瑕疵 D 之後，沒有依大小排序；若真的依大小排序，「其他」（36）會排在第 4 位、瑕疵 D（30）之前），累計在瑕疵 D 為 79.7%、插入「其他」後跳到 90.8%，會讓人以為「其他」是重要原因；固定放最右時，瑕疵 F 為 88.9%、最後到 100.0%。（素材包早先把錯誤那張寫成「按大小插在第 5 位」，並稱「比瑕疵 E、F 大」；納茲已於 2026-10-04 更新為上述說法，本檔已同步。）**Excel 內建的 Pareto 圖會自動把所有類別（包括「其他」）依大小重排，無法固定「其他」在最右**；要固定請改用直條加折線的組合圖，自己排好順序、自己算累計百分比。
3. **起源：有據可查的年份是 1951；1941 只出現在英文維基百科與 Lean Enterprise Institute 轉載，與 Juran 自述不一致。** Juran 1975 年的文章〈The Non-Pareto Principle; Mea Culpa〉（原刊 *Quality Progress* 1975 年 5 月；Juran Institute 存檔全文）自述：1920 年代中期起觀察到缺陷分布不均；1930 年代末在通用汽車看到 Merle Hale 做的 Pareto 模型，是他第一次接觸 Pareto 的工作；1940 年代末準備《Quality Control Handbook》第一版（1951 年出版，第 37–41 頁）時才為這個普遍現象取名「Pareto 原則」。英文維基百科的 Juran 與 Pareto principle 條目、Lean Enterprise Institute 頁面都寫 Juran「1941 年」讀到 Pareto；Juran 自述裡 1941 年 12 月是他轉任聯邦政府的時間（我開啟全文核對過），也找不到「1941 年讀到 Pareto」的原始出處。可以定論的是：Juran 把現象命名為 Pareto 原則並寫成文字，年份是 **1951 年**（構思於 1940 年代末），與 Juran Institute 指南寫的「1950 年代初」大致吻合。**「誰第一個畫出長條加累計折線的圖」無法證實。** 其他無法證實的說法：中文維基百科臺灣繁體頁面「1930 年由 Juran 首次應用於品管」（頁面沒有出處，Juran 自述也不支持）；Juran Institute 指南「Pareto 在 1895 年觀察財富分配」；「Pareto 本人寫過 80:20」。Pareto 本人的年份有書目可查：所得分配定律首見於 1896 年論文〈La courbe de la répartition de la richesse〉與 1896–97 年《Cours d'économie politique》（Persky 1992）；1897 年是《Cours》第二卷出版年；1906 年是《Manuale di economia politica》；1895 年的是另一本談需求法則的著作，不是財富分配。
4. **Juran 自己承認：手冊裡那條累計曲線應該歸給 Lorenz；但柏拉圖與洛倫茲曲線是「相通但不同」，不是同一種圖。** 同一篇 1975 年文章寫明 Pareto 的研究屬於經濟領域，把它叫做「Pareto 原則」是取錯了名字，手冊第一版的累計曲線應該歸給 Lorenz（**我核對過原文**：the cumulative curves used in Quality Control Handbook, First Edition, should have been properly identified with Lorenz）；他後來改用「關鍵少數與瑣碎多數（vital few and trivial many）」推廣。Juran 這句話的來源狀態：本檔已核對原文；[`lorenz-curve.md`](lorenz-curve.md) 對這句只是轉載本檔的說法（Lorenz 素材包 2026-10-04 下午沒有重新取原文）。**與洛倫茲曲線的關係**（以下是 Lorenz 素材包的概述，非 Juran 原文；關係式由該素材包的 selfcheck 逐點驗證，我另外用 numpy 重算，成立；兩個範例用同一套說法）：柏拉圖把**類別**依件數由大到小排，折線凹向上、落在對角線上方；洛倫茲曲線把**個體**由小到大排，兩軸都是累計百分比，曲線凸向下、落在完全平等線下方。同一組數字 40、25、15、12、8：柏拉圖累計 40、65、80、92、100（%），洛倫茲累計 8、20、35、60、100（%）；柏拉圖折線**把順序倒過來、轉半圈（以圖中心點對稱旋轉 180 度）就是洛倫茲曲線**；關係式：柏拉圖第 k 點的累計＝1−洛倫茲曲線在 1−k／n 處的累計。稱呼以圖的排法為準：類別由大到小排叫柏拉圖；個體由小到大排、兩軸都是累計百分比才叫洛倫茲曲線；不要說成同一種圖，也不要說成毫無關係。本檔練習資料（8 類，合計 340 件）：最小的 4 項合計 53 件＝15.6%（即洛倫茲曲線在 50% 處），最大的 4 項 84.4%（柏拉圖第 4 項累計），相加 100.0%。
5. **左軸最大值要設成總數，柱頂才會對上累計線第一點。** 模擬圖 S4（同一份 340 件資料）：左軸最大只設 140，第 1 根柱頂是 118/140＝84.3% 的高度，累計線第一點卻是 118/340＝34.7%，對不上；左軸最大值等於總數 340 才對齊。ASQ 要求兩軸刻度對應：左軸最大值等於全部小計的總和，左軸的一半正對右軸的 50%；臺灣 myMKC 文章也提醒折線起點應在第一根柱頂。右軸建議畫到 100%（圖 R7 的右軸畫到 120，與此不同）；右軸最大值填 100 還是 1，取決於累計百分比是用整數還是小數存放（Excel Easy 舊版做法寫 100，myMKC 寫 1）。圖 R2 沒有右側百分比軸，累計線是對著左軸畫的，建議照 ASQ 補上右軸 0–100%。
6. **Google 試算表：官方圖表類型清單沒有 Pareto，但官方沒有明文寫「沒有 Pareto」，這只是從清單推論。** 官方清單列了折線、組合、面積、直條、橫條、圓餅、散布、直方圖、瀑布圖等。Spreadsheet Point 原文寫「目前沒有獨立的 Pareto 範本選項」，Info Inspired 寫「沒有內建 Pareto 圖」，兩篇都建議用組合圖。**官方明文說法無法證實。**
7. **Excel 內建 Pareto 的版本說法：「Excel 2016 以後」來自 Excel Easy 與 2015 年的微軟部落格；Microsoft Support 頁面的適用清單列的是 Microsoft 365、2021、2024 與行動版，沒有明列 2016、2019。** 素材包沒有在真機上操作過，各步驟只核對了頁面文字。如果選的兩欄都是數字，Excel 會把它當直方圖分組，不是柏拉圖。
8. **「加權柏拉圖」「比較型柏拉圖」：ASQ 詞彙頁只列名稱、沒有定義。** 本課把加權柏拉圖用在「依件數 × 單件損失排序」、比較型用在「前後並排」，是素材包的理解；SAS 說明書有定義（柱高是加權後的次數，常見權重是修理成本或客戶損失；比較型是同一流程變數的兩張以上柏拉圖並排、座標軸一致），與本課做法相符，但只是轉載；《The Quality Toolbox》只讀到目錄。
9. **件數最多的不一定損失最大。** 練習資料加上虛構的單件損失後：依件數排第 1 的外觀刮傷（118 件），依金額降到第 4（2,360 元，占 7.9%）；第 1 名變成尺寸超差（12,900 元，占 43.1%）；依金額前 3 項（尺寸超差、數量短少、受潮，合計 24,000 元）累計 80.2%，第 3 項第一次越過 80%（前 2 項 65.2%）。「其他」400 元雖大於文件缺漏 140 元，仍固定放最右。
10. **授權（圖）**：R1–R8 來自 Wikimedia Commons，各有明確授權：R1 CC BY-SA 3.0（DanielPenfield）、R2 CC0（Zirguezi）、R3 CC BY 4.0（Peter Gladdish）、R4 CC BY 4.0（Belbury）、R5 CC BY-SA 4.0（Arcchit）、R6 CC BY-SA 3.0（FJRojkin）、**R7 CC BY-SA 3.0 與 GFDL 雙授權、作者欄空白（上傳者 Snp），作者不詳，對外使用有風險**、R8 公眾領域（Commons 標示；it:User:Biopresto）；CC BY-SA 要求標示作者、授權並以相同方式分享（R1、R5、R6、R7 須遵守），CC BY 要求標示作者與授權，CC0 無限制。**R9–R20（ASQ、Juran Institute、Lean Enterprise Institute、Six Sigma Material、Excel Easy）頁面載明版權所有，未見轉載許可，只能內部使用，不要複製**；素材包找過這些站的使用條款頁，有的頁面不存在，有的只是隱私政策，都沒有找到轉載許可，所以情況是「版權所有、未見許可」，不是「沒寫」。S1–S8 是素材包自畫的虛構模擬圖，無外部授權限制。本 repo 不複製任何圖。
11. **圖面數字一律不轉述：** R12 Juran Institute 的圖沒有顯示逐柱數字，也沒有逐柱核對，只以指南文字「18 項中前 4 項占 86%」為準（那是指南的教學舉例，不是核對過的實測資料）；R13 與 R12 的柱高逐柱相同，只是換了橫軸標題並多標一段「Awkward Zone」，**不是第二筆獨立資料**；R16 的圖說仍附有來源頁面的資料表數字，**本 repo 不引用那些頁面數字**；R15 的累計標籤、R11 的範本標題等也只作示意。

## When

- 手上有一堆**類別**（問題、原因、客訴、停機機台、退貨原因、成本項目、系統當機原因），想知道「先處理哪幾項最有效」
- 想同時看兩件事：每一類有多大（左軸，件數或金額），以及前幾類加起來占多少（右軸，累計百分比）
- ASQ 的用法：問題或原因很多、想聚焦在最重要的幾項時使用；屬於品管七大手法之一（維基百科〈Seven basic tools of quality〉；石川馨 1985 的清單也列有，僅轉載自維基百科，未核原書）
- 改善之後再畫一次，看第二名是誰、整體有沒有變小
- 形狀：兩欄（類別、數量或金額）；原始資料若是一筆一列的紀錄，先彙總成「每類一列」；類別彼此不重疊；期間與用件數還是金額先決定

## Recommend

- **主選**：柏拉圖（直條由大到小，累計百分比折線，右軸 0–100%，左軸最大值＝總數）
- **步驟（口述）**：
  1. 先決定分類（類別不重疊）、期間（例如一季）、用件數還是金額（ASQ 步驟的前三項）；分類一換排名就可能跟著換
  2. 彙總成每類一列；由大到小排序，「其他」通常放最右
  3. 算累計件數與累計百分比（累計件數 ÷ 總件數）
  4. 畫直條加折線：折線放到右側座標軸，右軸 0–100%，**左軸最大值等於總數**；可加一條 80% 參考線
  5. 讀圖：折線第一次到達或越過 80% 是第幾項 → 分布夠不夠集中 → 換成金額再畫一次 → 改善後再畫一次 → 需要時往下鑽一層
- **變體**：依金額加權；改善前後並排；往下鑽（把第 1 名再拆原因，ASQ 圖 1 → 圖 2 的做法）；Wilkinson（2006，*The American Statistician* 60 卷 4 期 332–334 頁）提出替每根柱子算「接受區間」，本課不教
- **備選（何時改用哪一種）**：
  - 類別只有兩三個、或各類差不多大（平坦型）→ 一般長條圖，見 [`categorical-comparison.md`](categorical-comparison.md)、[`lollipop-rank.md`](lollipop-rank.md)；平坦型換一個分類角度再畫，常會出現「關鍵少數」（Juran Institute 的建議大意）
  - 要看趨勢 → 折線圖或管制圖（[`control-chart.md`](control-chart.md)；柏拉圖只是某段期間的快照），見 [`time-series-trend.md`](time-series-trend.md)
  - 要證明因果 → 另查原因（例如魚骨圖）
- **參數與判準範例（範例，不是標準）**：

| 項目 | 數值與出處 | 性質 |
|---|---|---|
| 參考線 | 80%（經驗法則；實際可能是 90:10 或 70:30） | 範例，不是標準 |
| 右軸 | 0–100%（ASQ 建議；圖 R7 畫到 120 與此不同） | 範例，不是標準 |
| 左軸最大值 | 等於總數；左軸的一半正對右軸的 50%（ASQ） | 範例，不是標準 |
| 累計百分比 | 累計件數 ÷ 總件數；範例四捨五入到小數 1 位 | 範例，不是標準 |
| 類別數 | 範例 8 類；ASQ 的 Excel 範本預覽最多 10 項缺陷（圖 R11） | 範例，不是標準 |
| 「其他」 | 通常放最右（文字出處僅 Six Sigma Material）；零碎小項可併成「其他」（ASQ） | 範例，不是標準 |
| 指南的舉例 | 「18 項中前 4 項占 86%」「25 道製程中有 5 道造成 65% 的報廢」（Juran Institute，用「可能會發現」的口吻，教學舉例） | 範例，不是標準 |

## 與鄰近圖種的區別

本表是素材包的概述，除標明出處者外沒有逐項查證來源。

| 圖種 | 它回答什麼 | 和柏拉圖的區別 |
|---|---|---|
| 一般長條圖（[`categorical-comparison.md`](categorical-comparison.md)） | 各類別的大小 | 不要求排序、沒有累計線，類別順序可依字母或時間；柏拉圖固定由大到小（「其他」通常放最右），加累計百分比折線與右軸 |
| 瀑布圖（[`waterfall-bridge.md`](waterfall-bridge.md)） | 從起點數值經一連串增減到終點數值的過程 | 柏拉圖畫各類別大小與累計占比，順序依大小；Google 試算表官方圖表清單有瀑布圖、沒有 Pareto |
| 漏斗圖（[`funnel-stages.md`](funnel-stages.md)） | 同一批對象依序過關，每一階剩多少 | 順序是流程順序，不是依大小排；與統合分析的漏斗圖更是另一回事 |
| 洛倫茲曲線（[`lorenz-curve.md`](lorenz-curve.md)；維基百科〈Lorenz curve〉） | 個體由小到大排，兩軸都是累計占比（常用於所得分配），沒有柱子 | **相通但不同**（第 4 點）：同一組數字，柏拉圖累計折線把順序倒過來、轉半圈就是洛倫茲曲線；但柏拉圖排類別、有長條、折線凹向上，洛倫茲排個體、沒有長條、曲線凸向下，不是同一種圖。Juran 自己承認手冊的累計曲線應該歸給 Lorenz（本檔已核對原文） |
| ABC 分析（維基百科〈ABC analysis〉） | 採購／存貨管理：把存貨依重要性分成 A、B、C 三類管理 | 沒有固定門檻，條目舉例「A 類＝20% 品項占 70% 年消耗價值」；它是分類管理方法，柏拉圖是畫出這個分布的圖 |
| Pareto 前沿／Pareto 效率 | 多目標取捨、資源配置 | 不同概念，與柏拉圖只有名字撞名 |

判斷口訣：**一堆類別、想知道先處理哪幾項 → 柏拉圖；只想比各類大小、不看累計 → 一般長條圖；起點到終點的增減 → 瀑布圖；依序過關的留存 → 漏斗圖。**

## Avoid

- 左軸最大值沒設成總數，柱頂與累計線第一點對不上（S4）
- 把「其他」插在中間（S3 是插在第 5 位、沒有依大小排序），累計線被墊高，讓人誤以為「其他」是重要原因（S3）；也不要寫成「永遠放最右」或「ASQ 規定」
- 把 80% 當門檻：第一次到達或越過 80% 的是第幾項要看資料，不一定是第 2 項或 20% 的類別（S1：第 4 項）
- 只看件數不看金額（S6）
- 分布本來就平坦還硬找「關鍵少數」（S5 右：要 6 項才累計到 80.0%）
- 拿它證明因果；把它當趨勢圖
- 右軸畫超過 100%（R7 畫到 120）；累計線沒有右側百分比軸（R2）
- 把 R13 當成與 R12 獨立的第二筆資料；把 R14（只有金額長條，沒有累計線）當柏拉圖；把 R17 當「未排序與排序」對照（它真正示範的是把零碎小項併成「其他」）；把 R18 當柏拉圖（它只示範「原始記錄 → 次數表」）
- 把 1941 年寫成定論；把「Juran 發明柏拉圖」寫成定論（誰先畫出長條加累計折線無法證實）
- 把 Google 試算表「沒有 Pareto」寫成官方明文
- 把 R9–R20 的圖直接放進對外文件
- 把 X 搜尋結果當成「X 上沒人談」：教學稿的 5 組搜尋找到幾則熱度不高的教學向貼文，但中文與日文查「柏拉圖」「帕累托圖」「パレート図」（排除轉貼）回來 50 筆，沒有任何一則談這張圖（多半是「柏拉圖式戀愛」與哲學家）；搜尋結果會隨時間變動

## Produce checklist

- [ ] 故事句：「這一季 N 件，該先盯哪幾類」；先決定分類、期間、件數或金額
- [ ] 彙總成每類一列；由大到小排序；「其他」通常放最右（Excel 內建圖做不到，要用組合圖）
- [ ] 累計百分比 ＝ 累計件數 ÷ 總件數；右軸 0–100%；**左軸最大值＝總數**
- [ ] 80% 參考線可加，但只當參考；圖註寫期間、分類方式、件數或金額
- [ ] 解讀順序：折線第一次到達或越過 80% 是第幾項（不是第幾 %）→ 分布夠不夠集中 → 換成金額再看一次 → 改善後重畫 → 往下鑽一層
- [ ] 示範數字標「數字未核」；不放圖檔進 repo；R9–R20 不複製
- [ ] 工具誠實（只寫素材包證實的）：
  - **Excel（Excel 2016 以後，內建）**：選文字欄與數字欄 → 插入 → 插入統計圖表 → 直方圖區的 Pareto（Windows 版路徑；Mac 版是功能區的統計圖表圖示）；自動加總同名類別、由大到小排列並畫累計折線；自動重排「其他」，無法固定；版本說法見上方第 7 點
  - **Excel 舊版或 Google 試算表**：排序、算累計百分比欄，用「組合圖」把累計百分比畫成折線放到右軸；Google 官方清單無 Pareto（推論）
  - **統計軟體**：Minitab「Stat → Quality Tools → Pareto Chart」；R 的 qcc 套件 `pareto.chart` 函式（CRAN 頁標 GNU 通用公共授權）；SAS 說明書有加權與比較型定義。軟體操作細節以各家說明為準，素材包未逐一實測
  - 臺灣教學文：Ken's Blog、ResearchMFG（建議用金額呈現較易引起主管注意，單一部落格的建議）、myMKC（Excel 做法，右軸寫 1）

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-pareto-fictional.csv` — 8 列（366 位元組）；沒有 `#` 說明行，只有一行欄位名；欄位 `category, count, data_status`；8 個進貨驗收不合格原因、件數合計 340；每列 `data_status` 都寫「虛構資料，數字未核」；檔名與其他 `*-fictional.csv` 不重複。第 1–7 列由大到小，「其他」固定在第 8 列（它剛好也是最小的一項，所以這份資料看不出「其他比別人大仍放最右」，那種情況請看圖 S3 的另一份虛構資料）。
- 我用 pandas **獨立重算**的數字（以實際計數為準；與素材包、selfcheck 的敘述逐項一致，**沒有發現素材包文字與 CSV 不一致**）：
  - 件數 118／86／52／31／22／14／9／8，合計 340，類別沒有重複
  - 累計件數 118／204／256／287／309／323／332／340；累計百分比 34.7%／60.0%／75.3%／84.4%／90.9%／95.0%／97.6%／100.0%
  - 第一次到達 80%：第 4 項（84.4%；含越過 80% 的那一項本身），前 3 項只有 75.3%
  - 8 個累計點中，高於 80% 的 **5** 個（第 4 到第 8 項），低於 80% 的 **3** 個（第 1 到第 3 項），剛好等於 80% 的 0 個；不能說「全部累計點都高於 80%」
  - 單項占比超過 20% 的只有 **2** 項（第 1 項 34.7%、第 2 項 25.3%）；第 3 項 52 件是 15.3%
  - 最小的 3 項（文件缺漏 14、受潮 9、其他 8）合計 31 件，**9.1%**（不是 5%）；前 5 項累計 90.9%，兩者相加 100.0%
  - 最小的 4 項合計 53 件＝15.6%，最大的 4 項 84.4%（洛倫茲對照：最小的 4 項＝洛倫茲曲線在 50% 處，見 [`lorenz-curve.md`](lorenz-curve.md)）
  - 加權版（假設單件損失 20／150／40／30／300／10／500／50 元，虛構）：損失依序 2,360／12,900／2,080／930／6,600／140／4,500／400 元，合計 29,910 元；依損失排序為尺寸超差、數量短少、受潮、外觀刮傷、包裝破損、標示錯誤、文件缺漏，最後其他；累計 43.1%／65.2%／80.2%／88.1%／95.1%／98.2%／98.7%／100.0%
  - 我另外由繪圖腳本重算了模擬圖 S2（原始順序合計 340）、S3（總數 325；錯誤版在 D 為 79.7%、插入後 90.8%；正確版 F 為 88.9%）、S5（集中型 390、前 3 項 84.6%；平坦型 110、第 1 項 16.4%、前 6 項 80.0%）、S7（改善後 262、少 78 件、降 22.9%；改善後前 4 項 79.8%）、S8（118 件；44.1%／70.3%／87.3%／100.0%），都與教學稿相符
- 示範讀法：先看右軸是不是 0–100%、左軸最大值是不是總數 → 外觀刮傷與尺寸超差兩項就占 60.0%，到第 4 項才超過 80% → 8 類中要 4 類（一半）才到 80%，並不是 20% → 換成金額後第 1 名換人 → 這是虛構示範，不是結論。
- `sample-pareto-selfcheck.py` — 自檢腳本（只用 Python 標準函式庫；以腳本旁的**明確檔名**讀 CSV，不搜尋檔案；全部用 `assert`）；見 `examples/data/README.md`。
- 素材包另附 `draw_pareto.py`（產生 8 張模擬圖，支援 `--outdir` 與 `--force`）：**本 repo 不收**，只在 `ATTRIBUTION.md` 註明它存在於素材包。我查過：它的**預設輸出資料夾是教學稿資料夾**（已存在的檔案預設略過，加 `--force` 才覆蓋教學稿圖檔），資料是腳本內寫死的虛構數字，不讀這份 CSV；需要 numpy、matplotlib 與 Noto Sans CJK 字型。我只在暫存資料夾執行，並指定 `--outdir /tmp/…`，8 張圖與素材包 `images/` 內的模擬圖 MD5 逐一相同。

## 參考連結（可點；皆出自素材包 sources.txt 且標可開）

- 條目與詞彙：https://en.wikipedia.org/wiki/Pareto_chart 、https://zh.wikipedia.org/zh-tw/%E5%B8%95%E7%B4%AF%E6%89%98%E5%9B%BE 、https://ja.wikipedia.org/wiki/%E3%83%91%E3%83%AC%E3%83%BC%E3%83%88%E5%9B%B3 、https://en.wikipedia.org/wiki/Pareto_principle 、https://en.wikipedia.org/wiki/Joseph_M._Juran 、https://en.wikipedia.org/wiki/ABC_analysis 、https://en.wikipedia.org/wiki/Seven_basic_tools_of_quality 、https://en.wikipedia.org/wiki/Lorenz_curve
- 品管機構與一手文獻：ASQ〈What is a Pareto chart〉https://asq.org/quality-resources/pareto ；Juran 1975〈The Non-Pareto Principle; Mea Culpa〉全文 https://www.juran.com/wp-content/uploads/2021/03/The-Non-Pareto-Principle-1974.pdf 、ASQ 書目頁（全文不公開）https://asq.org/quality-progress/articles/the-nonpareto-principle-mea-culpa?id=be4b6da104c64a6d9888f7fcead5aa92 ；Juran Institute 指南 https://www.juran.com/blog/a-guide-to-the-pareto-principle-80-20-rule-pareto-analysis/ ；Persky 1992〈Pareto's Law〉http://piketty.pse.ens.fr/files/Persky1992.pdf ；Lean Enterprise Institute https://www.lean.org/lexicon-terms/pareto-chart/ ；Six Sigma Material https://www.six-sigma-material.com/Pareto-Diagram.html ；iSixSigma（為什麼「20% 原因」常常不是 20%）https://www.isixsigma.com/ask-tools-techniques/pareto-chart-20-causes-represent-80-problem-there-are-never-20usually-there-are-more-why/ ；《The Quality Toolbox》目錄 https://catdir.loc.gov/catdir/toc/ecip055/2004029947.html ；SAS 說明書（加權與比較型定義）https://www.sfu.ca/sasdoc/sashtml/qc/chap29/sect2.htm
- 試算表與軟體：Microsoft Support https://support.microsoft.com/en-us/office/create-a-pareto-chart-a1512496-6dba-4743-9ab1-df5012972856 ；Microsoft 365 部落格 2015 https://www.microsoft.com/en-us/microsoft-365/blog/2015/08/18/visualize-statistics-with-histogram-pareto-and-box-and-whisker-charts/ ；Excel Easy https://www.excel-easy.com/examples/pareto-chart.html ；Google 試算表圖表類型清單 https://support.google.com/docs/answer/190718 ；Spreadsheet Point https://spreadsheetpoint.com/how-to-make-pareto-chart-google-sheets/ ；Info Inspired https://infoinspired.com/google-docs/spreadsheet/pareto-chart-in-google-sheets/ ；Minitab https://support.minitab.com/en-us/minitab/help-and-how-to/quality-and-process-improvement/quality-tools/how-to/pareto-chart/before-you-start/overview/ ；R 套件 qcc https://cran.r-project.org/web/packages/qcc/index.html 、https://rdrr.io/cran/qcc/man/pareto.chart.html
- 臺灣教學文：https://kenddg.tw/seven-basic-tools-pareto/ 、https://www.researchmfg.com/2012/02/pareto-chart/ 、https://mymkc.com/article/content/22215
- 書目（Wilkinson 2006，*The American Statistician* 60 卷 4 期 332–334 頁）：Crossref 書目資料 https://api.crossref.org/works/10.1198/000313006X152243 （標題、期刊、卷期頁與教學稿所寫一致）
- 圖片頁與授權（Wikimedia Commons，8 個）：https://commons.wikimedia.org/wiki/File:Pareto_chart_of_titanium_investment_casting_defects.svg 、https://commons.wikimedia.org/wiki/File:Pareto_analysis.svg 、https://commons.wikimedia.org/wiki/File:Pareto_analysis_process_diagram.svg 、https://commons.wikimedia.org/wiki/File:Pareto_principle_diagram.svg 、https://commons.wikimedia.org/wiki/File:Flat_Type_Pareto.jpg 、https://commons.wikimedia.org/wiki/File:Diagrama_pareto.svg 、https://commons.wikimedia.org/wiki/File:Pareto_graphic_01.png 、https://commons.wikimedia.org/wiki/File:Diagramma-Pareto.jpg
- X 貼文（素材包逐則確認存在，內文以 X 查詢工具讀取；只作連結、不當正式教材；熱度都不高）：Excel Easy 問「哪些客訴真正造成麻煩？」並連到教學頁（最像教學的一則）https://x.com/ExcelEasy/status/2098119313882284314 ；Nielsen Sousa 的品管七大手法簡介串 https://x.com/NielsenSousa/status/2104346966725370014 ；撞名實例（談的是人工智慧模型「成本對分數」的 Pareto 前沿圖，不是柏拉圖）https://x.com/pkost0v/status/2105942401462214923 、https://x.com/HsuanMingLin/status/2105439396648612133
- 查核限制（未核；僅記名、不列連結，**不是已驗證的來源**）：Wilkinson 2006 的 DOI 連結（出版社頁，被導到沒有內文的驗證頁；2026-10-03 17:22 打不開，之後 17:23–17:26 補測 4 次相同，16:30 曾讀到摘要，時開時不開，不穩定；本 repo 只引書目資訊，書目由上方 Crossref 查證，未讀全文）。素材包 sources.txt 46 條中這是唯一標「打不開」的一條。
- 連結統計：sources.txt 46 條（去重）＝可開 45＋打不開 1。可開 45 條中 **43 條連結**（含 4 則 X 貼文）、**2 條刻意不連結**（X 上 @ainewmeth 的貼文：大意說「3 類裡的 2 類就占 80%，那是 66.7% 的類別而不是 20%，80/20 只是經驗法則」，與本課提醒一致，但附的是圖表工具網站、屬推廣性質；X 上 @account_comptte 的供應鏈貼文：數字無來源）；打不開 1 條只記名。Excel Easy 教學頁在素材包測試時（17:21、17:23、17:24）曾回「請求過多」被暫時擋下，17:25 起恢復，連續抓取容易再被擋，仍歸類為可開。

鄰居 pattern：`categorical-comparison.md`（一般長條圖：不排序、無累計線）、`lollipop-rank.md`（排名；各類差不多大時）、`waterfall-bridge.md`（起點到終點的增減）、`funnel-stages.md`（依序過關的留存）、`time-series-trend.md`（要看趨勢時）、`control-chart.md`（管制圖：看同一指標隨時間穩不穩）、`lorenz-curve.md`（洛倫茲曲線：個體由小到大的累計，與柏拉圖相通但不同）；ABC 分析只在本檔說明邊界，不另立專檔。

圖檔留在教圖／skill-pack（素材包 `images/`，28 張＝20 張真實／示意圖加 8 張模擬圖，圖說與教學稿逐字相同，檔案與終稿使用的檔案 MD5 逐一一致；R3、R4 原為透明底，已鋪白），本 repo **不複製**任何圖。可對照的圖：R1 鈦合金鑄造缺陷柏拉圖（CC BY-SA 3.0）、R2 引擎過熱（CC0；六個原因、合計 71；沒有右軸）、R3 四步驟流程圖（CC BY 4.0）、R4 Pareto 法則示意（CC BY 4.0）、R5 房型柏拉圖（CC BY-SA 4.0）、R6 西班牙文資料表（CC BY-SA 3.0）、R7 日文標示（CC BY-SA 3.0／GFDL、作者不詳；右軸畫到 120）、R8 義大利文標示（公眾領域）；R9 ASQ 圖 1 五類客訴、R10 ASQ 圖 2 拆成六類、R11 ASQ Excel 範本、R12 Juran 關鍵少數、R13 Juran 尷尬區、R14 Juran 每單位成本長條、R15 Lean Enterprise Institute 咖啡服務、R16 Six Sigma Material 停機時數、R17 併成「其他」放最右的長條、R18 原始記錄到次數表、R19 Excel Easy 內建 Pareto（餐廳客訴 10 類）、R20 Excel Easy 組合圖（皆為版權所有、未見轉載許可、只能內部使用）；模擬圖 S1 構造、S2 做法三步、S3「其他」放哪、S4 軸對齊、S5 集中型對平坦型、S6 加權、S7 改善前後、S8 往下鑽（皆**模擬資料**、數字未核，右下角有浮水印）。對帳見 `ATTRIBUTION.md`。
