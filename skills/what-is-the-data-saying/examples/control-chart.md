# Pattern: control-chart

> **圖種**：管制圖（Control chart；Shewhart chart；process-behavior chart）
> **來源（納茲教圖）**：`teach-viz/2026-10-04-am-control.md`（方法教學；正式課程；首次以管制圖為主題；與前一天的柏拉圖同屬「品管七大手法」系列，但圖種與用途不同）
> **亦稱**：英文別名 Shewhart chart（以 Walter A. Shewhart 命名）、process-behavior chart（流程行為圖）；中文維基百科臺灣繁體頁面寫「也稱為修哈特圖或流程行為圖」，同一頁把人名譯為「休哈特」（同頁兩種譯法不一致，照實記）。它屬於統計製程管制（Statistical Process Control，常簡稱 SPC，貼文裡常這樣寫），也是品管七大手法之一（維基百科〈Seven basic tools of quality〉清單）。
> **核心**：把製程指標依時間（或子組）順序畫出來，加上**中心線（CL）**與**上／下管制界限（UCL／LCL）**，用來判斷流程是否「統計受控」，還是出現該調查的特殊原因（special cause）。
> **一句話**：這個流程穩不穩、從什麼時候開始不穩？——它**不是**回答「做出來合不合規格」。
> **誠實提醒**：本課是方法教學，**不代替**正式的統計製程管制導入、常數表查表或軟體設定；實際計算請依公司標準作業與統計軟體說明。模擬圖與本 repo 的練習資料都是虛構，**數字未核**。
> **潤稿狀態**：素材包與教學稿都明說**沒有經過 Gemini 潤稿**（Gemini 登入失效），也沒有改用其他模型潤稿；文字是審後由人工整理的原稿。
> **縮寫（首次寫全稱）**：CL＝中心線（Center Line）；UCL＝上管制界限（Upper Control Limit）；LCL＝下管制界限（Lower Control Limit）；USL／LSL＝規格上限／下限（Upper／Lower Specification Limit）；OOC＝失控（Out Of Control）；σ 是標準差，「3σ」是離中心線三個標準差。

## 十二件必須釘清的事

1. **管制界限 ≠ 規格界限，不要混畫。** 管制界限由流程自己的資料算出，描述「這個流程平常會在哪個範圍內變動」；規格界限（USL／LSL）是顧客或設計圖給的要求。維基百科明寫兩者「沒有內在關聯」（no intrinsic relationship）；NIST 手冊的說法是：管制界限用來判斷流程是否統計受控（產出是否一致），規格界限用來判斷產品能不能照預期運作。「所以管制圖上不宜混畫規格線」是教學稿作者對維基百科該句的解讀（該句原文用字不清）。模擬圖 S6 把兩種線畫在同一張圖上對照（管制界限虛線、規格界限點線，圖例要分清）。
2. **在規格內不等於沒事；受控也不等於合格。** 圖 S7（模擬）：第 17 組是 57.5，超出管制上界 56，卻仍在規格上限 60 之內；只看規格會漏掉這個訊號。「點全落在規格內也可能已經統計失控」這一半是依定義推得，**屬教學稿作者的理解，維基百科沒有直接寫**。反過來，流程可以統計受控卻仍不符規格（維基百科例子：報廢率受控但高於期望值）；受控但許多點仍越出規格，問題在流程能力或目標設定，不是把管制界限畫緊一點。NIST 對「受控」的要求更嚴：所有點都在界限之間，**而且**點的排列看起來是隨機的。
3. **判異規則有多套，看資料前先約定用哪一套；「連續同側」Western Electric 是八點、Nelson 是九點。** Western Electric 規則（西部電氣公司規則，1956 年手冊）四條區域規則：① 單點超出 3σ；② 連續 3 點中有 2 點超出 2σ（同一側）；③ 連續 5 點中有 4 點超出 1σ（同一側）；④ 連續 **8** 點落在中心線同一側。NIST 手冊另列兩條趨勢規則：連續 6 點一路上升或下降、連續 14 點上下交替（NIST 手冊 6.3.2 節同頁的「What are the WECO rules」一段，沒有獨立子頁；WECO＝Western Electric Company）。區域 A＝離中心線 2σ 到 3σ，B＝1σ 到 2σ，C＝1σ 以內。Nelson 規則（Lloyd S. Nelson，1984 年 10 月發表於《Journal of Quality Technology》）共八條：① 單點超出 3σ；② 連續 **9** 點同側；③ 連續 6 點遞增或遞減；④ 連續 14 點上下交替；⑤ 連續 3 點中有 2 點（或 3 點）超出 2σ，方向相同；⑥ 連續 5 點中有 4 點（或 5 點）超出 1σ，方向相同；⑦ 連續 15 點都在 1σ 以內；⑧ 連續 8 點都在 1σ 以外，且上下兩側都有。數點時「連續 N 點」**含起點本身**。維基百科 Control chart 條目也提醒規則集要事先說清楚。
4. **圖 S3 是 Liora 重畫的版本：9 點全部在中心線上方並全標紅。** 資料（虛構，18 組，中心線 20、上界 23.6、下界 16.4）：第 1–9 組是 20.6、20.8、20.7、21.0、20.9、21.2、21.1、20.6、20.3，第 10 組 19.8 回到中心線下方，所以連續同側**剛好 9 點**；Western Electric（要 8 點）規則在第 8 組湊滿，Nelson（要 9 點）規則在第 9 組湊滿，兩套都達標。**舊版圖 S3** 只紅標前 7 點並寫「7 consecutive points」，但資料前 9 點都在中心線上方，而 7 點本身既不構成 Western Electric（8 點）也不構成 Nelson（9 點）的任何同側訊號；Liora 重畫成 9 點全標紅，標註「9 consecutive points above CL」，終稿圖說已同步。本檔與 repo 的練習資料一律用新版。另外，Commons 圖 R6 的圖面標題寫「連續九點」並畫 9 個點，那是 Nelson 的數法，與前三張 Western Electric 規則圖（R3–R5）用的規則集不完全一致，請以上面的規則為準。
5. **「3σ ≈ 99.73% 的點落在界限內」有前提：資料近似常態，而且平均與標準差已知。** 常見採用約 3σ 界限（維基百科）。NIST 手冊指出，若分布偏斜（例如帕松分布——描述罕見事件發生次數的分布——平均 0.8 件），3σ 上界的單點誤報機率會從約 0.001 升到約 0.009（我用帕松分布重算：平均 0.8、上界 0.8＋3√0.8≈3.48，P(X≥4)≈0.0091，與 NIST 一致）；界限若只由少量資料算出，實際誤報機率可能和理論值差很多。c 圖、np 圖的 3σ 也是常態近似，不是精確機率界限。界限畫寬或畫窄，是在「假警報」和「漏掉真問題」之間取捨，NIST 也提到可改用其他機率界限（例如 0.001 機率界限）。
6. **規則越多，假警報越多。** NIST 手冊寫：只用「單點超出 3σ」平均約每 371 點誤報一次（NIST 稱這個平均等待點數為平均連串長度 Average Run Length；維基百科寫 370.4，與 1/0.0027≈370.4 吻合）；加上 Western Electric 全部規則後約每 91.75 點誤報一次（NIST 引 Champ 與 Woodall 1987 年的論文，我沒有讀該論文）。不要畫完才「挑一條剛好顯著的規則」。
7. **模擬圖的界限是預先設定的，不是由資料算出；真實流程的界限要由資料估出來，圖說要講明。** S1：設 σ＝2，點本身的標準差約 1.1，所以全擠在界限內；用這 25 點自己的平均與標準差估，界限約 46.1–52.8，比圖上的 44–56 窄。S6：用 24 點自己的標準差估界限約 44.9–55.0，與圖上的 44–56 相近但不相同。S5：X̄ 圖界限 8.8／11.2、R 圖上界 2.25、下界 0.15 都是示意，不是用 A2、D3、D4 係數算的；真實的全距圖每組 6 個以下時下界是 0（NIST 係數表 D3＝0），畫 0.15 只是示意。S8：改善後界限也是預先設定，這 18 點的標準差約 0.35，比設定的 0.7 小一半。
8. **改善後何時重算界限：找到並消除特殊原因、流程進入新的穩定態之後；不要太常改。** NIST 提醒太常改會讓圖失去「拿現在跟過去比」的用處，列出三種重算時機：再累積至少 30 個點而且流程沒有已知變動、流程發生重大改變、發生已知且可避免的異常。圖 S8（模擬）改善前後各用自己的界限（改善前中心線 12.0、上界 17.4、下界 6.6，第 6 組 18.2 超界；改善後中心線 10.0＝目標、上界 12.1、下界 7.9，沒有點超界）。與柏拉圖「處理完第一名再重畫」類似，但對照的是穩定度與變異，不是類別排名。
9. **選圖看資料型態與子組。** 計量值（用量的）：每組數個量測值、組內個數不多（NIST 說約十個以下，Minitab 說明頁寫八個以下）→ X̄–R（平均數與全距）；組內個數較多 → X̄–S（平均數與標準差）；每次只有一筆 → I–MR（個別值與移動全距，移動全距＝相鄰兩筆之間的差距）。計數值（用數的）：不良率、每組樣本數可變 → p 圖（每件只分良或不良，假設互相獨立、不良機率固定）；不良數、每組件數固定 → np 圖；缺陷數（一件上可有多處）、檢驗單位大小固定 → c 圖；每單位缺陷數、檢驗單位大小可變 → u 圖。「不良品」是整件被判不合格，「缺陷」是一件上可能有好幾處，兩者不同。前提與經驗法則：NIST 手冊引 Shewhart 的經驗法則——至少約 25 組、每組 4 個且都在受控狀態，才能說製程達到統計受控（實際依公司標準）。
10. **公式不要憑記憶寫；寫的時候連前提與來源一起寫。** 教學稿本身沒有寫公式；以下是素材包查核時對照 NIST／SEMATECH 手冊第 6 章與維基百科的結果，供補寫或回答追問：X̄–R：X̄ 圖 x̿ ± A2·R̄，R 圖上界 D4·R̄、下界 D3·R̄；I–MR：x̄ ± 2.66·MR̄（d2＝1.128，即 3/1.128），移動全距圖上界 3.267·MR̄；p 圖：p̄ ± 3√(p̄(1−p̄)/n)，各組樣本數不同時界限呈階梯狀（維基百科列三種做法：各組用自己的 n、用平均 n̄、標準化）；np 圖：n·p̄ ± 3√(n·p̄(1−p̄))；c 圖：c̄ ± 3√c̄，下界算出為負就不畫下界；u 圖：ū ± 3√(ū/nᵢ)。係數（NIST）：n＝2 時 A2 1.880、D4 3.267；n＝3 時 1.023、2.575；n＝4 時 0.729、2.282；n＝5 時 0.577、2.115；n＝7 時 A2 0.419、D3 0.076、D4 1.924；n 不大於 6 時 D3＝0。維基百科的 D4 在小數第三位略有不同（n＝2 為 3.268、n＝3 為 2.574），是四捨五入來源不同，不算錯；寫稿請選定一個來源並註明。我用 d2、d3 常數反算 A2、D3、D4，與 NIST 表一致（n＝2 的 A2 算出 1.881，NIST 寫 1.880，屬四捨五入差異）。
11. **Commons 圖的圖內數字不是本稿查證的實測。** 素材包用公式反算過三張：R7（X̄–R，n＝3）A2＝1.023、D4≈2.574 與圖面一致；R10（p 圖）p̄＝0.0246、n＝520 時上下界 0.0450／0.0042 與圖面一致（我另外用同一公式重算，相符）；R12（np 圖，每組 500 件）平均 12.45、上下界 22.90／2.00 與圖面一致（我重算相符）。**R9（個別值圖）圖面中心線 5.483、移動全距平均 0.244，依圖內資料表讀回的 20 筆算出 5.49、0.237，略有差距，可能是讀圖誤差，也可能圖內數字不一致，無法逐點證實**（這是素材包的說法，我沒有重讀圖）；R8、R9、R16 都不要拿來當計算範例。其他圖的限制：R2 的 Commons 頁面說明寫「個體管制圖，附 1、2、3 個標準差區域」，但圖上標題是 X-bar Chart for diameter，兩者不一致，只說它是帶區域色帶的管制圖；R8 的資料表有 24 欄、圖只畫 12 點，對不上；R16 的界限數字與 R9 完全相同，「應是同一張圖去掉資料表」是推測；R15 檔名是 X̄ 管制圖（Xquer Regelkarte），但圖面標籤沒有看到 X̄ 符號；R17 是 Z–MR（標準化個別值與移動全距）進階變體，本稿不展開公式；R18 是英文維基百科精選條目候選產出率的管制圖，說明非製造的流程指標也可以用，不限工廠尺寸。
12. **起源與命名只能照維基百科轉述。** 維基百科寫：Shewhart 在 1920 年代於貝爾實驗室（Bell Labs）發明管制圖；1924 年 5 月 16 日寫了一份約一頁的內部備忘錄，其中三分之一篇幅是一張簡單的圖，就是今天管制圖的雛形；後來由 W. Edwards Deming 大力推廣。備忘錄內容是引述他上司 George Edwards 的回憶，**教學稿沒有看到備忘錄原件，屬僅轉載**。維基百科 Shewhart 條目寫他 1918 年進入西部電氣公司、1925 年貝爾實驗室成立後才轉到貝爾實驗室，所以 1924 年那份備忘錄依此推算是他在西部電氣公司任職期間寫的（推算）。X 上有人說 Shewhart「1924 年 5 月發明 SPC」，那是該作者的說法。Levey–Jennings 圖是臨床實驗室常用的品管圖，畫法與 Shewhart 管制圖相近；Commons 圖 R13 的樣本只畫平均線與 ±1、±2 個標準差的線，沒有 3σ 管制界限（維基百科；僅轉載；Commons 頁面只說「用 Excel 隨機資料自製」）。

## When

- 有一個**依時間或子組順序**排列的製程或服務指標：尺寸平均、不良率、單位缺陷數、實驗室品管值、客服逾時未回覆比例，想判斷流程穩不穩、何時開始出現該調查的異常
- 情境（教學稿）：某裝配線每小時抽樣量測關鍵尺寸，或客服中心每日統計一次「逾時未回覆比例」；目的是判斷流程是否穩定，而不是一次排出「哪種不良最多」（那是柏拉圖）
- 形狀：橫軸是時間或子組序號，縱軸是選定的製程統計量；計量值常成對（X̄ 與 R）；計數值依資料型態選 p／np／c／u
- **不適合**：沒有時間順序的類別排名（用柏拉圖）；只想看分布形狀（用直方圖）；資料太少、還不知道流程是否穩定就急著畫界限

## Recommend

- **主選**：依資料型態選管制圖（見第 9 點）；固定畫中心線、上管制界限、下管制界限，點依時間順序連線
- **口述步驟**（教學稿第 6 節）：
  1. 先決定量什麼、多久取一次（例如每小時抽 5 件量尺寸、或每日不良率）；子組如何組成，會影響該用 X̄–R、X̄–S 還是 I–MR
  2. 蒐集一段「大致穩定」期間的資料；這些資料用來估計中心線與管制界限——界限來自**流程資料**，不是直接抄規格
  3. 依圖種計算統計量，畫中心線與上下管制界限（常見約 3σ；軟體或品管常數表會依樣本數給係數；下界算出為負就不畫）
  4. **事先約定判異規則**（Western Electric 或 Nelson），把點依時間順序連起來
  5. 解讀：受控則維持；失控則找特殊原因（先查人、機、料、法、環，而不是立刻把規格線畫窄一點假裝沒事）；找到並消除特殊原因、進入新穩定態後再重算界限
  6. 改善後再畫一次，對照穩定度與變異
- **解讀**：點都在管制界限內、且沒有事先約定的非隨機型態 → 傾向視為統計受控，變異多屬共同原因（common cause，流程本來就有的自然波動），通常不必急著調機；單點超界或出現規則型態（連多點同側、連續升降）→ 可能是特殊原因（special cause，額外冒出來的異常），應調查
- **參數與判準範例（範例，不是標準）**：

| 項目 | 數值與出處 | 性質 |
|---|---|---|
| 管制界限 | 常見約 3σ；99.73% 的點在界限內只在常態、獨立、參數已知時成立 | 範例，不是標準 |
| 連續同側 | Western Electric 8 點；Nelson 9 點（含起點） | 範例，不是標準 |
| 趨勢 | 連續 6 點遞增或遞減（Nelson 與 NIST 趨勢規則）；連續 14 點上下交替 | 範例，不是標準 |
| 區域規則 | 3 點中有 2 點超出 2σ；5 點中有 4 點超出 1σ（同側） | 範例，不是標準 |
| 誤報頻率 | 只用單點超 3σ 約每 371 點一次（維基百科 370.4）；加 Western Electric 全部規則約每 91.75 點一次 | 範例，不是標準 |
| 估界限的資料量 | 至少約 25 組、每組 4 個且都在受控狀態（NIST 引 Shewhart 的經驗法則）；實際依公司標準 | 範例，不是標準 |
| X̄–R 的組內個數 | 約十個以下（NIST）；八個以下（Minitab 說明頁） | 範例，不是標準 |
| 重算界限 | 再累積至少 30 個點且流程沒有已知變動、重大改變、已知且可避免的異常（NIST） | 範例，不是標準 |
| c 圖的常態近似 | 通常要平均缺陷數約 5 以上（素材包概述，未標來源） | 範例，不是標準 |

## 與鄰近圖種的區別

本表是素材包的概述，除標明出處者外沒有逐項查證來源。

| 圖種 | 它回答什麼 | 和管制圖的區別 |
|---|---|---|
| 折線圖（[`time-series-trend.md`](time-series-trend.md)） | 值隨時間的變化 | 管制圖在折線圖上加了「由流程資料算出的中心線與管制界限」與判異規則，用來判斷哪些起伏是流程固有的波動、哪些該查原因；只想看趨勢、不需要判斷「是否異常」時，折線圖就夠了 |
| 柏拉圖（[`pareto-chart.md`](pareto-chart.md)） | 某段期間各類別的排名與累計占比（橫斷面快照，問「先處理哪幾類」） | 管制圖看同一個指標隨時間穩不穩（問「流程有沒有變」）；柏拉圖稿也提醒「要看趨勢請另用折線圖或管制圖」。兩者同屬品管七大手法，用途不同 |
| 直方圖（本 repo 無專檔） | 資料分組、看分布形狀 | 不保留時間順序；管制圖保留時間順序，才看得出漂移與型態。常搭配：管制圖確認流程穩定之後，再用直方圖與規格比較 |
| 地平線圖（[`horizon-chart.md`](horizon-chart.md)） | 並排比較很多條時間序列的起伏 | 管制圖強調中心線、管制界限與判異規則 |
| Levey–Jennings 圖 | 臨床實驗室的品管圖 | 畫法與 Shewhart 管制圖相近；教學稿樣本（R13）只畫平均線與 ±1、±2 個標準差線，沒有 3σ 管制界限 |
| 規格圖（把規格線畫在趨勢圖上） | 產品合不合規格 | 規格線不是管制界限（見第 1、2 點） |

判斷口訣：**要判斷流程穩不穩、何時開始不穩 → 管制圖；只看趨勢 → 折線圖；各類別誰最多 → 柏拉圖；合不合規格 → 規格線，另畫。**

## Avoid

- 把規格界限當管制界限，或把兩者混畫（S6、S7）；以為「在規格內就沒事」或「受控＝合格」
- 混用規則集的點數：「連續同側」Western Electric 8 點、Nelson 9 點；看完圖才挑一條剛好顯著的規則
- 標紅的點數與圖說、規則不一致（舊版 S3 的教訓：標 7 點、寫 7 點，卻不構成任何同側訊號）
- 把預設界限畫得像由資料算出的；真實流程的界限要由資料估出來，圖說要講明是「由流程資料算出」還是「預先設定的示意值」
- 改善後不重算界限，或太常改界限
- 把「3σ ≈ 99.73%／0.27% 誤報」當保證（偏斜資料、少量資料、c 圖 np 圖的常態近似都會偏離）
- 下界算出是負數還硬畫（c 圖缺陷數少時，NIST：不畫下界）
- p 圖界限畫成直線（各組樣本數不同時呈階梯狀，R10；樣本數固定的 np 圖界限才是兩條直線，R12）
- 拿 Commons 圖的圖內數字當實測或計算範例（R8、R9、R16 尤其不要）
- 資料太少、還不知道流程是否穩定就急著畫界限
- 把 X 貼文當教學依據：它們只是個人說法

## Produce checklist

- [ ] 故事句：「這個指標穩不穩、何時開始不穩」；先決定量什麼、多久取一次、子組怎麼組成
- [ ] 依資料型態選圖種（X̄–R、X̄–S、I–MR、p、np、c、u）
- [ ] 中心線、UCL、LCL 與規格線（若要畫）用不同線型與顏色，圖例標名稱（教學稿 S6：管制界限虛線、規格界限點線）；縮寫 CL、UCL、LCL、USL、LSL、OOC 在圖說或圖例旁給全稱
- [ ] 圖說寫清楚界限來源（由流程資料算出，或預先設定的示意值）與用哪一套判異規則；點數怎麼數要寫清楚，例如「第 1–9 組共 9 點在中心線上方，含第 1 點本身」
- [ ] 標紅的點和圖說一致，只標觸發訊號的點或要說明的型態；標註文字、陰影範圍與圖說同步
- [ ] 橫軸是時間或子組序號；縱軸是選定的統計量；計量值成對畫（X̄ 與 R）
- [ ] 模擬圖標模擬、圖說結尾寫「數字虛構」；圖面文字不是中文時，圖說只描述圖面可見內容並註明語言，與頁面說明不一致時只說兩者不一致
- [ ] 工具誠實：素材包只引用 Minitab 的 Xbar-R 與 I-MR 說明頁（取其選圖條件）、品管常數表與軟體會給係數這種泛稱；**沒有實測任何軟體**，Excel、Google 試算表、Python、R 等的管制圖做法素材包都沒有查，這裡不寫。QI Macros、iSixSigma 是商業教學頁，只列連結。
- [ ] 不放 Commons 圖進對外文件，除非逐張標作者與授權（見下方圖檔段）

## 虛構 demo 資料

素材包沒有指定哪一份給 repo，也沒有「合併版」樣本；它的八份虛構資料各自對應一張模擬圖（S1–S8）、各附一支自檢腳本，所以本 repo **八組成對收錄**到 `examples/data/`（共 8 個 CSV＋8 支 selfcheck，與素材包逐位元相同）。**注意：檔名是 `sample-s1-anatomy.csv` 這類，沒有 `fictional` 字樣，也沒有「control」字樣**——它們都是管制圖的資料，說明見 `examples/data/README.md`；讀取請用**明確檔名**，不要用 `sample-*.csv` 之類的萬用字元（本資料夾還有其他圖種的 `sample-*.csv`）。每個 CSV 第一行是 `#` 開頭的說明行（pandas 用 `comment='#'`），第二行是欄位名，每列 `data_status` 都寫「虛構資料，數字未核」。

| 檔案 | 對應圖 | 內容 |
|---|---|---|
| `sample-s1-anatomy.csv` | S1 解剖 | 25 組；CL 50、UCL 56、LCL 44（σ 設 2） |
| `sample-s2-out-of-control.csv` | S2 | 20 組，左右兩欄；CL 100、UCL 109、LCL 91 |
| `sample-s3-run-same-side.csv` | S3（Liora 新版） | 18 組；CL 20、UCL 23.6、LCL 16.4 |
| `sample-s4-trend.csv` | S4 | 18 組；CL 40、UCL 44.5、LCL 35.5 |
| `sample-s5-xbar-r.csv` | S5 | 20 組，xbar 與 range 兩欄；X̄ 界限 8.8／10／11.2，R 界限 0.15／1.2／2.25 |
| `sample-s6-spec-vs-control.csv` | S6 | 24 組；管制界限 44／50／56，規格 USL 58、LSL 42 |
| `sample-s7-misread-specs.csv` | S7 | 22 組；管制界限 44／50／56，規格 USL 60、LSL 40 |
| `sample-s8-before-after.csv` | S8 | `phase` 欄分 before／after，各 18 組；目標 10 |

我用 pandas／numpy **獨立重算**了界限、中心線、超界點與判異規則命中（以實際計數為準；與素材包敘述、selfcheck 逐項一致，**沒有發現素材包文字與 CSV 不一致**）：

- **S1**：25 點；高於中心線 10、低於 15、等於 0；沒有點超界；標準差（n−1）1.119；自估界限 46.1–52.8；落在 48–52 的 23 點；範圍 47.3–51.9
- **S2**：左圖 20 點沒有超界；右圖只有第 15 組（110.8）超出上界 109
- **S3**：第 1–9 組都高於中心線、第 10 組（19.8）低於；起始連續同側 9 點；Western Electric「連續 8 點」規則命中在第 8、9 組，Nelson「連續 9 點」命中在第 9 組；沒有點超界；全部 18 點中高於中心線 12、低於 5、剛好等於 1（第 15 組＝20.0），所以只看全體「高於／低於」計數會誤導，要看第 1–9 組
- **S4**：第 1–12 組嚴格遞增（38.1 → 43.2），都沒有超過上界；連續 6 點遞增的規則第 6 組起命中（第 6 到第 12 組）
- **S5**：X̄ 與 R 都沒有點超界；R 最小值 0.993，下界 0.15 是示意；各欄的界限都是常數
- **S6**：24 點，沒有超出管制界限，也沒有超出規格；自估界限 44.9–55.0
- **S7**：只有第 17 組（57.5）超出管制上界 56，仍在規格上限 60 內；沒有點超出規格
- **S8**：改善前第 6 組（18.2）超出上界 17.4，目標 10；改善後沒有點超界，標準差 0.353（設定 σ 為 0.7）
- **我另外觀察到、素材包沒寫的**：用「σ＝(UCL−CL)/3」當設定值重算全部區域規則，S4 除了趨勢規則外，第 13 組也命中 Western Electric「連續 8 點同側」（第 6–13 組都高於中心線 40），第 12、13 組命中「5 點中有 4 點超出 1σ」；S1、S3 在第 15 到 18 組、S5 的 X̄ 圖在第 15、16 組命中 Nelson 規則 7（連續 15 點都在 1σ 以內），因為預先設定的 σ 比點的實際離散大。這些圖只用來示範單一現象，不是在說「這份資料只命中一條規則」。
- **圖與腳本的實跑**：selfcheck 8 支都在暫存資料夾實跑，結束碼 0、各輸出一行「OK」；`draw_control.py` 預設輸出到**它自己旁邊的 `out/`**（不會寫進 teach-viz），我只在暫存資料夾執行並用 `--outdir /tmp/…` 指定輸出，8 張模擬圖與素材包 `images/` MD5 逐一相同（含新版 S3）；`export_samples.py` 預設寫回它自己所在的資料夾，我用 `--outdir /tmp/…` 實跑，匯出的 8 個 CSV 與素材包的逐位元相同。兩支腳本**本 repo 不收**，只在 `ATTRIBUTION.md` 註明。

## 參考連結（可點；皆出自素材包 sources.txt 且標可開）

- 條目與定義：https://en.wikipedia.org/wiki/Control_chart 、https://zh.wikipedia.org/zh-tw/%E7%AE%A1%E5%88%B6%E5%9C%96 、https://en.wikipedia.org/wiki/Statistical_process_control 、https://zh.wikipedia.org/zh-tw/%E7%B5%B1%E8%A8%88%E8%A3%BD%E7%A8%8B%E7%AE%A1%E5%88%B6 、https://en.wikipedia.org/wiki/Walter_A._Shewhart 、https://en.wikipedia.org/wiki/Seven_basic_tools_of_quality 、https://en.wikipedia.org/wiki/Common_cause_and_special_cause_(statistics) 、https://en.wikipedia.org/wiki/Levey%E2%80%93Jennings_chart
- 判異規則：https://en.wikipedia.org/wiki/Western_Electric_rules 、https://en.wikipedia.org/wiki/Nelson_rules
- 圖種條目：https://en.wikipedia.org/wiki/X%CC%84_and_R_chart 、https://en.wikipedia.org/wiki/P-chart 、https://en.wikipedia.org/wiki/Np-chart 、https://en.wikipedia.org/wiki/C-chart 、https://en.wikipedia.org/wiki/U-chart
- NIST／SEMATECH 統計方法電子手冊：6.3.1 https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc31.htm 、6.3.2（含 Western Electric 規則）https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm 、6.3.2.1 https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc321.htm 、6.3.3.1 https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc331.htm 、6.3.3.2 https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc332.htm
- 業界與軟體說明（商業站，圖與文字多半版權所有，只列連結）：iSixSigma https://www.isixsigma.com/tools-templates/control-charts/a-guide-to-control-charts/ ；Minitab X̄–R https://support.minitab.com/en-us/minitab/help-and-how-to/quality-and-process-improvement/control-charts/how-to/variables-charts-for-subgroups/xbar-r-chart/before-you-start/overview/ ；Minitab I-MR https://support.minitab.com/en-us/minitab/help-and-how-to/quality-and-process-improvement/control-charts/how-to/variables-charts-for-individuals/i-mr-chart/before-you-start/overview/ ；QI Macros https://www.qimacros.com/control-chart/
- 臺灣教學文（ResearchMFG）：繪製步驟 https://www.researchmfg.com/2016/05/control-chart-create/ 、判讀 https://www.researchmfg.com/2016/05/control-chart-judgment/ 、製程在控的特徵 https://www.researchmfg.com/2016/05/quality-under-control/
- 圖庫分類：https://commons.wikimedia.org/wiki/Category:Control_charts
- Commons 圖片頁（18 個，授權與作者見下方圖檔段）：https://commons.wikimedia.org/wiki/File:ControlChart.svg 、https://commons.wikimedia.org/wiki/File:Control_Chart_with_Zones.png 、https://commons.wikimedia.org/wiki/File:Rule_1_-_Western_electric_control_chart.svg 、https://commons.wikimedia.org/wiki/File:Rule_2_-_Western_electric_control_chart.svg 、https://commons.wikimedia.org/wiki/File:Rule_3_-_Western_electric_control_chart.svg 、https://commons.wikimedia.org/wiki/File:Rule_4_-_Western_electric_control_chart.svg 、https://commons.wikimedia.org/wiki/File:XBarR_Chart.jpg 、https://commons.wikimedia.org/wiki/File:XBarS_Chart.jpg 、https://commons.wikimedia.org/wiki/File:IMR_Chart.jpeg 、https://commons.wikimedia.org/wiki/File:PChart.jpg 、https://commons.wikimedia.org/wiki/File:Np_control_chart.svg 、https://commons.wikimedia.org/wiki/File:Npchart.JPG 、https://commons.wikimedia.org/wiki/File:Levy-Jennings_SampleChart.png 、https://commons.wikimedia.org/wiki/File:Control_Chart_(tr).png 、https://commons.wikimedia.org/wiki/File:Xquer_Regelkarte.svg 、https://commons.wikimedia.org/wiki/File:Diagram_Kontrol.JPG 、https://commons.wikimedia.org/wiki/File:Grafik_ZMR.JPG 、https://commons.wikimedia.org/wiki/File:En.wp_Featured_Article_Candidates_FAC_yield_control_chart.png
- X 貼文（6 則，素材包用命令列只看得到網頁外框，內文是用 X 官方查詢工具讀回，標「可開」；**只作連結、不當教學依據**，貼文只是個人說法）：見下方 X 段
- 查核限制（**未核；僅記名、不列連結，不是已驗證的來源**）：(1) ASQ「What is a Control Chart」頁面——納茲測試時網站拒絕存取，審稿複測與素材包稍後的命令列測試都能開，但狀態不穩定，素材包依審後稿標「打不開」，教學稿所有主張都不靠它；(2) Six Sigma Material 的「Control Chart」頁面——頁面不存在（網站回覆查無此網址），無法引用；(3) NIST 手冊結尾為 e 的「6.3.2.e」那一頁——NIST 手冊沒有這頁，網址回應碼雖為 200，卻被導回 NIST 資訊技術實驗室首頁，內容與管制圖無關，所以 Western Electric 規則改引 6.3.2 節。
- 連結統計：sources.txt 55 條（去重）＝可開 52＋打不開 3。可開 52 條**全部連結**（含 6 則 X 貼文；沒有刻意不連結的可開網址）；打不開 3 條只記名、未核。

## X 的情況

查詢時間：納茲約 2026-10-04 10:06–10:07（台北）；審稿約 10:30 前後逐則用貼文編號讀回原文，並重跑中文查詢。**繁體中文：用「管制圖」加 SPC、Shewhart、製程、品管等關鍵字查，0 筆**；只用「管制圖」一詞查，有 1 則 2026-09-02 的實務經驗貼文（談在關鍵原料的來料檢驗用過「移動平均管制圖」，客戶稽核時被稱讚），不是教學帖：https://x.com/shareefvan/status/2095179715741122819 。**英文與日文：約 5 則提及 Shewhart／管制圖／管制界限的原帖，但沒有找到可當逐步教學主案例的長帖**，下列僅列原帖（日期為台北時間），不編造教學內容；這不代表 X 上沒有人談，只代表當時的查詢結果。

1. Neil Pettinger（@kurtstat），2026-09-22 21:02：談 Intentional SPC 課程（給想有目的地使用統計製程管制的醫療分析師）與 Shewhart 1924——說 Shewhart 在 1924 年 5 月「發明 SPC」，是作者的說法。https://x.com/kurtstat/status/2102382994770014295
2. @ScotFreeLife，2026-09-11 05:25（世界標準時間 9 月 10 日晚上）：提及 Shewhart 1920 年代發明管制圖、Deming 推廣；後半談即時遙測資料，帶行銷口吻。https://x.com/ScotFreeLife/status/2098160922649088451
3. @ainewmeth，2026-09-09 21:07：提及 control chart／SPC／capability，也提到量具（量測用的工具）要可信。https://x.com/ainewmeth/status/2097673265812799497
4. @logiglish21，2026-09-07 17:24：日文帖，區分「管理限界」（control limit）與「規格限界」（specification limit）。https://x.com/logiglish21/status/2096892361456734420
5. @aftonone，2026-10-02 23:37：回覆建議查 Western Electric rules／SPC charts；這是對別人貼文的回覆，原貼文的上下文沒有讀，**脈絡無法證實**。https://x.com/aftonone/status/2106046039941664899

要寫「圖怎麼畫、規則怎麼記」，仍以維基百科、NIST 手冊、ResearchMFG 與本稿的 Commons 圖／模擬圖為主。

鄰居 pattern：`time-series-trend.md`（只看趨勢、不判斷異常時用折線）、`pareto-chart.md`（類別排名與累計占比；管制圖看同一指標隨時間穩不穩）、`horizon-chart.md`（並排比較很多條時間序列的起伏）、`small-multiples.md`（多條序列各畫一張管制圖時的排法）；直方圖、Levey–Jennings 圖只在本檔說明邊界，不另立專檔、`lorenz-curve.md`（洛倫茲曲線：分配形狀的橫斷面比較，不判斷流程穩不穩）、`marey-chart.md`（馬雷圖：列車運行圖；中文維基「运行图」轉址到趨勢圖 run chart，兩者不同）、`kaplan-meier-survival.md`（存活／留存的時間到事件分析；管制圖是流程是否受控）。

圖檔留在教圖／skill-pack（`/workspace/skill-packs/2026-10-04-am-control/images/`，26 張＝18 張真實／示意圖加 8 張模擬圖，與終稿使用的檔案 MD5 逐一一致），本 repo **不複製**任何圖，只列連結與授權；對帳見 `ATTRIBUTION.md`。**Commons 圖 R1–R18 各有個別作者與授權，我另外查了每個 Commons 頁面的授權欄，與素材包相符**；使用時必須標作者與授權：CC BY-SA 要標示作者與授權、衍生作品用同樣授權；GFDL（GNU 自由文件授權）通常要求附授權全文或連結；公眾領域可自由使用。向量圖（SVG）以 Commons 提供的縮圖（PNG）存檔，除此之外沒有修改；R14 本地檔是縮圖，與 Commons 原檔不同。對外轉載前建議再確認各授權的要求。

- R1 管制圖基本結構：DanielPenfield（頁面署名原上傳者），公眾領域
- R2 帶區域色帶：NeilP777，CC BY-SA 4.0
- R3–R6 Western Electric 規則 1–4：GMcGlinn、Richard Argentieri，CC BY-SA 3.0（R6 圖面寫連續九點，見上面第 4 點）
- R7 X̄–R、R8 X̄–S、R9 I–MR、R10 p 圖、R12 np 圖（樣本數固定 500）、R16 I–MR（只有圖）、R17 Z–MR：Andreas Sihono，GFDL
- R11 np 圖（過程自午夜起約 1.5σ 漂移）：DanielPenfield，CC BY-SA 3.0
- R13 Levey–Jennings 圖：Dr. F.C. Turner，公眾領域
- R14 土耳其文版：原圖 DanielPenfield，改作 DeeMusil、Anerka，CC BY-SA 3.0
- R15 德文版（Xquer Regelkarte）：原圖 DanielPenfield，德文版衍生 WikipediaMaster，公眾領域
- R18 英文維基百科精選條目候選產出率：Grondemar，CC BY-SA 4.0
- S1 解剖、S2 受控 vs 一點超界、S3 連續同側（新版）、S4 連續上升、S5 X̄–R 成對、S6 管制界限 vs 規格界限、S7 常見誤讀、S8 改善前後：素材包自畫的**模擬圖**，虛構資料、數字未核，無外部授權限制，右下角有浮水印「模擬｜範例數字未核（虛構資料）」
- 版權所有、未見轉載許可的圖：本包 26 張**沒有**這一類；但 ASQ、iSixSigma、Minitab、QI Macros、ResearchMFG 等商業教學頁的圖與文字多半版權所有，素材包只放連結、沒有下載它們的圖；若日後要用，先查使用條款，否則只能內部用。
