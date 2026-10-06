# Pattern: swimmer-plot

> **圖種**：游泳圖（swimmer plot）
> **來源（納茲教圖）**：`teach-viz/2026-10-06-am-swimmer.md`（方法教學；正式課程；首次以游泳圖為主題）
> **亦稱**：英文 swimmer's plot、swimmer chart、swimmers plot、swim-lane plot；論文常寫「swimmer plot of time on treatment」「swimmer plot of individual responses」。**繁體中文沒有公認譯名**（多直接稱游泳圖）；中國大陸「游泳图」「泳道图」並用；日文「スイマープロット」
> **核心**：每位受試者（或每個觀察單位）畫成一條橫棒，像游泳池的一條水道；棒長＝治療（或追蹤）多久，棒上的符號標出何時開始有反應、何時惡化或停藥，棒尾箭頭＝資料截止時仍在治療
> **一句話**：「每一個人」的故事——誰撐最久、反應多早出現、維持多久、為什麼停藥、誰到截止日還在治療。屬於**個人層級的描述圖**，不是族群統計。
> **誠實提醒**：本課是方法教學；模擬圖與本 repo 的練習資料都是虛構，**數字未核**（納茲未核），不代表任何真實藥物、劑量或病人。真實圖讀數凡標「目測」都未核。
> **潤稿狀態**：素材包寫明課程終稿已經 Liora 審核，**並由 Gemini 潤稿**；素材包文字依終稿手工整理，沒有另外送 Gemini。教學資料夾的潤稿紀錄寫 2026-10-06 16:57（台北）用 gemini-3.8-flash-high 重新潤稿、比對腳本通過、手動改回原文 9 處（細節見 ATTRIBUTION）。
> **撞名**：游泳圖**不是**流程圖的**泳道圖（swimlane diagram）**——泳道圖的水道代表**分工**，不是觀察到的時間（見 R20）。Chia 等 2016 寫「swimmer (or swim-lane) plot」，中國大陸也有人把游泳圖叫「泳道图」，所以兩個名字常被混用。本 repo `kaplan-meier-survival.md` 原本寫「游泳圖（swimlane／swimmer plot）」也是混用，v0.3.29 已依本課更正。

## 十四件必須釘清的事

1. **怎麼讀（依序）。** 先看一列代表什麼、時間 0 是哪一天（通常一列＝一位受試者、0＝開始治療；但 R14 一列＝一次手術、R18 一列＝一組、R8 的 0＝重新治療日）→ 看排序方式 → 先數箭頭（仍在治療的人棒還會變長）→ 看符號位置（反應符號離 0 越近越早，但只會落在掃描月）→ 看反應段長度與結局 → 看終點符號（棒結束不一定是惡化）→ 看資料截止日與追蹤時間 → 看參考線與軸（參考線要對刻度、橫軸有沒有截斷）。
2. **命名由來與發明者無法證實。** **目前找到最早**以游泳圖為題的文件是 Stacey D. Phillips 2014 年 PharmaSUG（製藥業 SAS 使用者會議）論文；她把游泳圖當**既有圖種**介紹，沒有說是自己命名，所以**誰最先使用或命名無法證實**。SAS 的 Sanjay Matange 同年 6 月 22 日部落格說是聽了她的報告後寫的。「受試者平行排列像泳池水道，因此得名」只出自後來的會議論文（PharmaSUG 2019 DV-323），**僅轉載，命名由來無法證實**。
3. **沒有公認中文譯名；英文維基百科也沒有條目（素材包觀察）。** 素材包寫：英文維基百科**沒有**游泳圖條目——它測試 Swimmer_plot 頁面時是「查無此頁」（該網址本 repo 只記名、不連結、標未核）；英文 Waterfall plot 條目是頻譜分析的三維瀑布圖，Spider chart 條目轉到雷達圖，都不是腫瘤學的瀑布圖、蜘蛛圖。
4. **Chia 2016 的「常用於第一期試驗」說的是蜘蛛圖，不是游泳圖。** Chia 等 2016 說游泳圖適合「少數病人」、對免疫治療特別重要；說「第一期、第二期藥物開發中相當常見」的是 PharmaSUG 2026 DV-120。
5. **排序造成的階梯（S3）。** 同一份 20 人資料，依時長排序出現漂亮階梯，依編號（入組先後）排序就沒有；入組先後與棒長的等級相關係數＝**−0.32**（Spearman，**同長度取平均名次**；精確 −0.3185），只是微弱的「越晚入組棒越短」。棒長有同分（例如 4 位 2.0 個月），所以必須取平均名次；同分任意排名得到的值不能用。排序方式要寫在縱軸標題。
6. **資料截止日不同（S6）。** 試驗開放後第 12 個月截止：17 人入組、P18–P20 尚未入組、仍在治療 11 人、最長 P02 10.5 個月；第 24 個月截止：20 人、仍在治療 4 人、P02 22.5 個月。P13 2.2 → 14.2、P14 2.0 → 14.0、P16 1.3 → 13.3 都還在治療。**棒短可能只是追蹤不夠久。**
7. **人數太多（S7、R13）。** 150 人變成一面牆（疾病惡化 84、副作用 26、撤回同意 24、仍在治療 16）；同一份資料的 Kaplan–Meier 曲線（事件＝任何原因停藥，共 134 人）：中位 6.0 個月，第 6／12／18 個月仍在治療比例 0.433／0.202／0.061，風險人數第 0／6／12／18／24 月 150／79／28／7／0。R13 是 330 人的真實例子。超過約 50 人時改畫 Kaplan–Meier 曲線，或分面、挑子群（並寫出挑選條件）。
8. **把顏色差異當證據（S2）。** 低劑量 10 人中位 4.3 個月、高劑量 10 人中位 11.25 個月，最長前 10 條裡高劑量 6、低劑量 4——只是描述，不是「高劑量比較好」的統計證據；比較要用存活分析與檢定。
9. **把棒的結束當成惡化（S5）。** 疾病惡化 13、副作用 2（P04 12.5、P18 1.7 個月）、撤回同意 1（P06 2.6 個月）、仍在治療 4；P04 曾轉為完全緩解卻因副作用停藥。
10. **棒長＝有反應？（S1）** 最長的 P02（22.5 個月、仍在治療）列上沒有任何緩解符號。
11. **反應持續時間的設限（S4）。** 9 位有緩解者中，以疾病惡化結束 5 人、設限 4 人（仍在治療 3、副作用 1）；最長 P13 12.2 個月（設限）。
12. **參考線與標籤對不上（R6）。** 虛線標「整體無惡化存活期中位數 12.3 個月」，與論文內文一致（指這 16 人）；但依橫軸刻度量，虛線畫在**約 10.4 個月**——這是**論文原圖**的參考線和標籤對不上，不是課程引錯；讀數以論文內文為準，自己畫時參考線要對刻度。
13. **名稱叫游泳圖但其實不是（R16）；R19、R20 是對照。** R16 作者稱為「swimmer plot」，畫的卻是各就醫步驟中位天數的分組橫條圖，沒有個別病人——**反例**。R19 甘特圖（棒是**計畫**的時程）與 R20 泳道流程圖（水道是**分工**）是相近圖種對照——**三張都不是游泳圖**。先確認「一列代表什麼」。
14. **只畫有反應的人會誇大效果。** 應畫全部受試者，寫明沒惡化卻停藥的原因；圖說寫明是否畫了全部受試者。

## When

- 每人（或每個單位）一列，有共同起點（開始治療、入組、上線）、結束時間與結束原因，中間有幾個帶時間的事件
- 人數約 10 到 50 人；最常見於小樣本腫瘤藥物試驗
- 想跟瀑布圖（縮多少）、蜘蛛圖（縮的過程）一起回答「維持多久」
- 情境（課程稿）：新抗癌藥第一期劑量探索試驗，20 位晚期實體腫瘤病人分低、高兩種劑量，每 8 週做一次電腦斷層；要讓聽眾一眼看出每人治療多久、誰有反應、反應多早出現、維持多久、為什麼停藥
- **不適合**：人數上百（變成一面牆，改 Kaplan–Meier 或分面、挑子群）；組間統計推論（游泳圖是描述圖）；只畫有反應的人；非醫療用途（客戶訂閱、設備維修、員工任期、軟體支援期）道理相通，但素材包**沒有找到可開的真實案例**，只當延伸想法（未核）

## Recommend

- **主選**：橫向游泳圖，依治療時長由長到短排序（縱軸標題寫明排序方式），左側標病人編號；橫軸從 0 開始；事件用符號、棒尾箭頭＝仍在治療；必要時另一段顏色標反應持續時間
- **口述步驟**（素材包第 7 節）：
  1. 定義「一列代表什麼」與時間 0
  2. 整理每人一列的表：開始、結束（或資料截止日）、結束原因、是否仍在治療，以及第一次部分緩解、完全緩解、疾病惡化、死亡等時間與分組欄（S8 ①）
  3. 決定排序：慣例依時長由長到短；也可先分組、組內排序（R6），或依劑量排序（R5）；把排序方式寫在縱軸標題（S3）
  4. 畫橫棒：橫軸從 0 開始；顏色代表組別或最佳反應，顏色不要太多（R2、S2）；人多時改細線（R12）
  5. 加事件符號與棒尾箭頭（R1、R9、S1）；需要時用另一段顏色標反應持續時間（S4）或惡化後存活（R9）
  6. 加圖例與註記：資料截止日、評估間隔、是否包含全部受試者
  7. 搭配瀑布圖、蜘蛛圖、Kaplan–Meier 曲線（R2、R3、R15）
  8. 超過約 50 人時，改畫 Kaplan–Meier 曲線或分面、挑子群（S7、R13）
- **工具誠實**：素材包列出 SAS（Phillips 2014、Matange 部落格）、R 的 swimplot 與 ggswim、JMP、Roadmap2Health 網頁工具；**ggswim 不在 CRAN（素材包觀察：CRAN 套件頁查無此頁，改從 GitHub 安裝）**；Datawrapper、Flourish 目前沒找到游泳圖範本（未核，不等於沒有）。素材包沒有說它實測了哪一套工具畫出 S 圖以外的成品；S 圖由素材包自製腳本畫出。
- **圖說建議**：寫清楚一列代表什麼、時間 0 是哪一天、排序方式、資料截止日、掃描間隔；每個符號、顏色都進圖例；寫明是否畫了全部受試者；參考線數字要和位置一致（R6）；橫軸截斷要明講（R7）；真實圖讀數標「目測，未核」；R 圖每張標作者與授權
- **參數與判準範例（範例，不是標準）**：

| 項目 | 數值與出處 | 性質 |
|---|---|---|
| 人數 | 約 10 到 50 人；超過約 50 人改 Kaplan–Meier 或分面（S7：150 人一面牆） | 範例，不是標準 |
| 排序 | 依時長由長到短；排序方式寫在縱軸標題（S3） | 範例，不是標準 |
| 掃描間隔 | 模擬設定每 2 個月掃描，緩解／惡化符號只會落在偶數月（S1）；課程情境每 8 週 | 範例，不是標準 |
| 等級相關 | 同長度取平均名次：−0.32（S3） | 範例，不是標準 |
| 模擬人數 | S1–S6 為 20 人、S7 為 150 人、S8 為 6 人，僅為示意 | 範例，不是標準 |

## 與鄰近圖種的區別

本表是素材包的概述，除標明出處者外沒有逐項查證來源。

| 圖種 | 一列是什麼 | 橫棒／線代表 | 與游泳圖的差別 |
|---|---|---|---|
| 泳道流程圖（swimlane diagram） | 一個負責單位或角色 | 流程步驟與交接 | 水道代表**分工**，不是觀察時間；名字像但完全不同（R20） |
| 甘特圖（[`gantt-schedule.md`](gantt-schedule.md)） | 一項任務 | **計畫**的工作時程 | 甘特圖的棒是預定的，游泳圖的棒是觀察到的，而且要標結束原因（R19） |
| 瀑布圖（waterfall plot，腫瘤學） | 一位受試者（直條） | 腫瘤大小最佳變化百分比 | 只看「縮多少」，沒有時間；只看瀑布圖會高估反應，應搭配游泳圖（R2、R3、R4）。≠ 財務累加瀑布圖（[`waterfall-bridge.md`](waterfall-bridge.md)） |
| 蜘蛛圖（spider plot，腫瘤學） | 一位受試者（折線） | 腫瘤大小隨時間變化 | 看「縮的過程」，人多時線會糾纏；不是雷達圖（R3） |
| Kaplan–Meier 曲線（[`kaplan-meier-survival.md`](kaplan-meier-survival.md)） | 不分列，一條族群曲線 | 仍未發生事件的比例 | 族群層級、能處理設限；人多時改用它（R15、S7） |
| 事件時間線（event timeline） | 一位受試者或一個事件 | 不良事件起訖 | Matange 2013 不良事件時間線外觀和游泳圖很像 |
| 馬雷圖（[`marey-chart.md`](marey-chart.md)） | 一班車（一條斜線） | 位置隨時間 | 縱軸是實際距離、斜率是速度；游泳圖縱軸是受試者清單、橫軸是自起點的時間 |

判斷口訣：**每人一條觀察到的時間軸、要看個人反應與停藥原因 → 游泳圖；看族群撐多久 → Kaplan–Meier；縮多少 → 瀑布圖；計畫時程 → 甘特圖；誰負責哪一步 → 泳道流程圖**。

## Avoid

- 把泳道流程圖（swimlane）和游泳圖混為一談
- 把依時長排序的階梯當成趨勢（S3）；排序方式不寫在縱軸
- 忽略資料截止日、把晚入組的短棒讀成效果差（S6）
- 人數上百還硬畫（S7、R13）
- 把劑量顏色差異當統計證據（S2）
- 沒有終點符號，讓讀者把副作用停藥讀成惡化（S5）
- 只畫有反應的人
- 參考線位置和標籤對不上（R6）；橫軸截斷不明講（R7）
- 看到論文標題叫 swimmer plot 就當真（R16）
- 把 Chia 2016「常用於第一期試驗」套到游泳圖（那句說的是蜘蛛圖）
- 寫「某人發明了游泳圖」或「因為像泳池水道所以叫游泳圖」而不加限定語
- 把 X 貼文當教學依據（只作連結）

## Produce checklist

- [ ] 定義一列代表什麼、時間 0、資料截止日、掃描間隔
- [ ] 每人一列：開始、結束、結束原因、是否仍在治療、事件時間、分組
- [ ] 排序方式寫在縱軸標題；橫軸從 0 開始，截斷要明講
- [ ] 每個符號、顏色進圖例；棒尾箭頭＝仍在治療
- [ ] 寫明是否畫了全部受試者；沒惡化卻停藥要標原因
- [ ] 參考線位置對刻度
- [ ] 超過約 50 人 → Kaplan–Meier 或分面、挑子群（寫挑選條件）
- [ ] 歷史與命名用限定語；不與泳道圖混用
- [ ] R 圖只連結、標作者與授權；模擬圖標「模擬」、數字虛構

## 虛構 demo 資料

素材包沒有指定哪一份給 repo → **8 組全部收錄**（`sample-swimmer-s1-anatomy` … `sample-swimmer-s8-steps`，各 CSV＋selfcheck，共 16 檔）。檔名已有 `swimmer` 前綴，與 `examples/data/` 既有檔**無撞名**，內容與素材包 `cmp` 逐位元相同。每支 selfcheck 以明確檔名讀 CSV（`CSV_NAME`＋腳本所在資料夾，無 glob），只用 Python 標準函式庫（S3 另以 scipy 交叉核對，沒有 scipy 時略過）；我在 `examples/data/` 與暫存資料夾各跑一次，全部 PASS。

獨立重算（pandas／numpy／scipy／lifelines，不用腳本的函式）與素材包、selfcheck 一致：S1 最長 P02 22.5（仍在治療、無緩解符號）、最短 P18 1.7（副作用）、仍在治療 4（P02、P13、P14、P16）、有緩解 9、完全緩解 3（P01、P03、P04）、中位 7.0、第一次緩解第 2 月 5 人／第 4 月 3 人／第 6 月 1 人；S2 中位 4.3／11.25、有緩解 2／7、前 10 條高 6 低 4；**S3 scipy `spearmanr` 與 pandas 平均名次皆為 −0.3185（→ −0.32）**；S4 惡化 5、設限 4、最長 P13 12.2；S5 13／2／1／4；S6 第 12 月入組 17、仍在治療 11 → 第 24 月 4；S7 84／26／24／16、事件 134、中位 6.0、0.433／0.202／0.061、風險人數 150／79／28／7／0；S8 排序 P02 22.5、P03 14.0、P04 12.5、P01 8.0、P05 6.0、P06 2.6。**沒有發現素材包文字與 CSV 不一致。**

**S8 一律用修正版**（`…-sim-s8-steps-fixed.png`，圖標題為「取編號最前、也就是最早入組的 6 位受試者 P01–P06」）。素材包 `draw_swimmer.py` 直接輸出這個修正版檔名；我從暫存資料夾以 `--outdir /tmp` 重跑，8 張模擬圖（含 S8 修正版）與素材包逐位元相同，匯出的 8 個 CSV 也相同；素材包 28 張圖與 `teach-viz/` 同名檔全部相同。圖檔與腳本都**沒有收進本 repo**。

## 參考連結

只連 `sources.txt` 標「可開」的網址（75 條全部連結，含 19 則 X 貼文）。以下 6 條**只記名、標未核、不連結**：

- **打不開（2，未核）：** 英文維基百科 Swimmer plot 頁、CRAN 的 ggswim 套件頁。這兩個只用來說明素材包測試時看到「英文維基百科沒有游泳圖條目」「ggswim 不在 CRAN」，**不當內容來源**。
- **無法確認（4，未核，不當依據）：** PhUSE 2025 DV08、PharmaSUG 2025 DV-337（網址無法解析）、fx361 簡體中文文章〈肿瘤临床试验中泳道图的SAS实现〉、Mercier 2019《製藥統計》（網站拒絕自動檢查）。不代表頁面不存在。

**方法、歷史與文獻**

- [Phillips 2014，PharmaSUG DG07〈Swimmer Plot〉](https://pharmasug.org/proceedings/2014/DG/PharmaSUG-2014-DG07.pdf)
- [Chia 等 2016《美國國家癌症研究所期刊》](https://pmc.ncbi.nlm.nih.gov/articles/PMC5017943/)
- [最早一篇：2015《臨床癌症研究》](https://pmc.ncbi.nlm.nih.gov/articles/PMC4470734/)
- [Masuoka 2025 改良游泳圖](https://pmc.ncbi.nlm.nih.gov/articles/PMC12414822/)
- [《美國醫學會雜誌網路開放版》2019 瀑布圖目測偏差](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2733434)
- [Shao 2014《美國國家癌症研究所期刊》瀑布圖評論](https://doi.org/10.1093/jnci/dju331)
- [Huang、Chen、Sun 2023（瀑布圖的統計解讀）](https://ascopubs.org/doi/abs/10.1200/CCI.23.00132)
- [歐洲生物醫學文獻資料庫（Europe PMC）搜尋「swimmer plot」](https://europepmc.org/search?query=%22swimmer%20plot%22%20OR%20%22swimmer%20plots%22)

**軟體與教學（SAS／R／JMP／線上工具）**

- [Matange 2014，SAS 部落格〈Swimmer Plot〉](https://blogs.sas.com/content/graphicallyspeaking/2014/06/22/swimmer-plot/)
- [Matange 2018，SAS 部落格〈瀑布圖與游泳圖合併〉](https://blogs.sas.com/content/graphicallyspeaking/2018/05/13/a-combined-waterfall-and-swimmer-plot/)
- [Matange 2013，SAS 部落格〈不良事件時間線〉](http://blogs.sas.com/content/graphicallyspeaking/2013/01/30/ae-timeline-by-name/)
- [SAS 全球論壇 2016 論文 SAS4321](https://support.sas.com/resources/papers/proceedings16/SAS4321-2016.pdf)
- [Matange、Heath，SAS 全球論壇 2019 論文 3143](https://support.sas.com/resources/papers/proceedings19/3143-2019.pdf)
- [SAS Visual Analytics 畫游泳圖（2022-09-30）](https://blogs.sas.com/content/sgf/2022/09/30/how-to-draw-a-swimmer-plot-in-sas-visual-analytics/)
- [PharmaSUG 2019 DV-323〈Fine-tuning your swimmer plot〉](https://pharmasug.org/proceedings/2019/DV/PharmaSUG-2019-DV-323.pdf)
- [PharmaSUG 2026 DV-120〈Swimmer Plots – Some Practical Advice〉](https://pharmasug.org/proceedings/2026/DV/PharmaSUG-2026-DV-120.pdf)
- [Miclaus 2018，JMP 講稿（瀑布圖、蜘蛛圖、游泳圖）](https://community.jmp.com/kvoqx44227/attachments/kvoqx44227/abstracts/1585/1/Miclaus_TumorResponse_US2018.pdf)
- [R 套件 swimplot（R 語言官方套件庫 CRAN）](https://CRAN.R-project.org/package=swimplot)
- [swimplot 說明文件](https://cran.r-project.org/web/packages/swimplot/vignettes/Introduction.to.swimplot.html)
- [ggswim 套件文件](https://chop-cgtinformatics.github.io/ggswim/)
- [ggswim GitHub 頁](https://github.com/CHOP-CGTInformatics/ggswim/)
- [R Consortium 2025-06-22 介紹文](https://r-consortium.org/posts/swimmer-plots-with-ggswim/)
- [Boehringer Ingelheim dv.swimmerplot 文件](https://boehringer-ingelheim.github.io/dv.swimmerplot/articles/dv-swimmerplot.html)
- [Roadmap2Health 線上游泳圖工具](https://roadmap2health.io/berdapps/swimmer/)
- [Miller Lab 2020-02-09 游泳圖文章](https://themillerlab.io/posts/swimmer_plots/)
- [Kat Hoffman 部落格：多變數治療時間線](https://www.khstats.com/blog/trt-timelines/multiple-vars/)
- [Steven Monda：從游泳圖還原個別病人資料](https://stevenmonda.github.io/KM-NMIBC/)
- [unionclin（簡體中文「游泳图」）](https://www.unionclin.com/News/322.html?page=9)

**相近圖種名詞（英文維基百科）**

- [英文維基百科：Swimlane（泳道流程圖）](https://en.wikipedia.org/wiki/Swim_lane)
- [英文維基百科：Gantt chart](https://en.wikipedia.org/wiki/Gantt_chart)
- [英文維基百科：Waterfall plot（三維頻譜瀑布圖，非腫瘤學）](https://en.wikipedia.org/wiki/Waterfall_plot)
- [英文維基百科：Spider chart（轉到雷達圖，非腫瘤學）](https://en.wikipedia.org/wiki/Spider_chart)
- [英文維基百科：Kaplan–Meier estimator](https://en.wikipedia.org/wiki/Kaplan%E2%80%93Meier_estimator)

**R 圖來源論文與圖檔頁**

- [R1 來源：Falkenhorst 等 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13596059/)
- [R2 來源：Yang 等 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13585213/)
- [R3 來源：Fan 等 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13503353/)
- [R4 來源：Waguespack 等 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13452024/)
- [R5 來源：Boklan 等 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12428389/)
- [R6 來源：Duca 等 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439513/)
- [R7 來源：Licata 等 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13564716/)
- [R8 來源：Ch'en 等 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13510987/)
- [R9 來源：Frumin Edri 等 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13609104/)
- [R10 來源：Tahara 等 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12896801/)
- [R11 來源：Cupertino Bérgomi 等 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12952609/)
- [R12 來源：Kuzukiran Kocatas 等 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13366725/)
- [R13 來源：Neola 等 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13395094/)
- [R14 來源：Nishida 等 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12941371/)
- [R15 來源：Bryan 等 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12005870/)
- [R16 來源：Malik 等 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13239896/)
- [R17、R18 來源：Agel 等 2026（PubMed Central）](https://pmc.ncbi.nlm.nih.gov/articles/PMC13298933/)
- [R17、R18 來源：Agel 等 2026（數位物件識別碼頁）](https://doi.org/10.1371/journal.pone.0352327)
- [R19 來源：維基共享資源 Pert example gantt chart](https://commons.wikimedia.org/wiki/File:Pert_example_gantt_chart.gif)
- [R20 來源：維基共享資源 Approvals](https://commons.wikimedia.org/wiki/File:Approvals.svg)

**授權條款**

- [授權條款 CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- [授權條款 CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)
- [授權條款 CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)

**連結統計：** sources.txt 81 個網址（去重；檔案共 88 行，另有 7 行 `#` 說明）＝可開 75＋打不開 2＋無法確認 4。可開 75 條全部連結（其中 X 貼文 19 條）；6 條只記名未核。

### X 貼文（只作連結，不當教學依據）

以 X 官方搜尋（2012 年起）再以官方貼文讀取逐則讀回 **19 則**：英文 14、日文 5；**繁體中文談游泳圖的原始貼文 0 筆**（繁中「游泳圖」只有游泳照片與插畫，「泳道圖」指流程圖泳道）。貼文數字一律未核，僅轉載。

1. [@tmprowell（顯示名稱 Tatiana Prowell, MD）](https://x.com/tmprowell/status/1178302919935975424)
2. [@tnewsomdavis](https://x.com/tnewsomdavis/status/1665824020640456706)
3. [@Dr_AmerZeidan](https://x.com/Dr_AmerZeidan/status/1271802483527028739)
4. [@Myeloma_Doc（顯示名稱 Robert Z. Orlowski）](https://x.com/Myeloma_Doc/status/1746931243239768288)
5. [@Hieflo23](https://x.com/Hieflo23/status/955343636622970880)
6. [@dgermain21](https://x.com/dgermain21/status/1620806383800033280)
7. [@ChandrakanthMv](https://x.com/ChandrakanthMv/status/2057676027275730999)
8. [@JackWestMD（顯示名稱 H. Jack West）](https://x.com/JackWestMD/status/1869760606578028729)
9. [@StephenVLiu](https://x.com/StephenVLiu/status/1355830895354269697)
10. [@monda_steven](https://x.com/monda_steven/status/1992939510007767357)
11. [@kat_hoffman_](https://x.com/kat_hoffman_/status/1535237421058727942)
12. [@MRXblogs（Annie Pettit）](https://x.com/MRXblogs/status/508876209430605824)
13. [@fedenichetti](https://x.com/fedenichetti/status/1720002435580633256)
14. [@acmoorephd（顯示名稱 Amy C. Moore）](https://x.com/acmoorephd/status/1532797852438581248)
15. [@sasyupi（日文）](https://x.com/sasyupi/status/1493467978742235136)
16. [@m0370（日文）](https://x.com/m0370/status/1254387774322425857)
17. [@PPubmed（EMUYN 広報，日文）](https://x.com/PPubmed/status/1856284270521921867)
18. [@sasyupi（日文）](https://x.com/sasyupi/status/1706976735869489609)
19. [@ShingoHatakeya1（日文）](https://x.com/ShingoHatakeya1/status/1564983091894005764)

鄰居 pattern：`kaplan-meier-survival.md`（族群層級存活曲線；人多時改用它，R15 示範兩者並排）、`gantt-schedule.md`（棒是計畫時程，不是觀察時間；R19 對照）、`marey-chart.md`（一條線是一班車的位置隨時間）、`time-series-trend.md`（單一指標隨時間）、`small-multiples.md`（人多時依組別分面）、`waterfall-bridge.md`（財務累加瀑布圖；腫瘤學瀑布圖不同，見上表）、`forest-plot.md`（次族群風險比點估計，沒有個人軌跡）。

## 圖檔與授權（不複製，只連結）

28 張＝真實／示意圖 R1–R20＋自繪模擬 S1–S8（虛構資料，數字未核；S8 為修正版）。**本 repo 不散佈圖檔，只連到來源頁；引用時保留作者與授權。**

- **R1–R18：** PubMed Central 開放取用論文，素材包標 **CC BY 4.0**（PubMed Central 文章頁或 Europe PMC 全文標示核對）；使用時必須標作者與出處（作者全名見素材包第 13 節與課程圖說）。我另以 Europe PMC REST API（2026-10-06，台北）查 R1–R18 的 17 篇來源論文（R17、R18 同一篇）：`license` 欄位全部是「cc by」（API 不給版本號，「4.0」依素材包）；Chia 2016 在 API 沒有授權欄、Masuoka 2025 為「cc by-nc-nd」，與素材包一致。
- **R19：** 維基共享資源，CC BY-SA 3.0，Dbsheajr（改作需用相同授權）；**R20：** 維基共享資源，CC0 1.0，Paul Kerr。我用 Commons API（2026-10-06，台北）查到 R19 授權簡稱 CC BY-SA 3.0、作者欄「Dbsheajr at English Wikipedia」、日期 2006-07-23；R20 CC0、Paul Kerr、2012-09-23，與素材包相符。
- **R16 是反例、R19／R20 是相近圖種對照**，都不是游泳圖；使用時保留這個標示。
- **只放連結、不轉存：** Chia 等 2016（保留所有權利）、Masuoka 2025（CC BY-NC-ND，禁止改作）。
- **目測未核：** R1 最長約 7.5 年、R2 約 43 個月、R3 約 25 個月、R11 約 65 個月、R12 約 190 天；R6 虛線位置約 10.4 個月（標籤 12.3 個月，以論文內文為準）。
