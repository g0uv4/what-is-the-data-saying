# Pattern: kaplan-meier-survival

> **圖種**：存活曲線／Kaplan–Meier 曲線（Kaplan–Meier survival curve；product-limit estimator）
> **來源（專案維護者整理）**：`teach-viz/2026-10-05-pm-km.md`（方法教學；正式課程；首次以 Kaplan–Meier 存活曲線為主題）
> **亦稱**：Kaplan–Meier plot／KM curve；乘積極限估計量（product-limit estimator）；生存曲線、存活率曲線；工程上可靠度曲線；商業上留存曲線／客戶流失分析
> **核心**：橫軸是從共同起點起算的時間，縱軸是「到這個時間點還沒發生事件的比例」；每發生一次事件曲線往下掉一階，中途離開觀察的人（設限）用短直線標記、**不讓曲線下降**
> **一句話**：這群人（零件、客戶）撐多久還會發生關心的事件？——它容許資料不完整（設限），不丟掉還沒發生事件的人。
> **誠實提醒**：本課是方法教學；模擬圖與本 repo 的練習資料都是虛構，**數字未核**（專案維護者整理時未核），不代替任何臨床試驗、可靠度報告或商業留存報表。素材包沒有實測任何軟體（R survival／survminer、Python lifelines 只列連結）。
> **潤稿狀態**：素材包與課程終稿都明說**沒有經過 Gemini 潤稿**（Gemini 登入失效），也沒有改用其他模型潤稿；課程終稿是審後由手工整理的最終文。
> **撞名**：生態學的**存活曲線（survivorship curve）**（見 R20）依相對年齡畫存活個體數（常用對數縱軸），分成晚死／平均／早死三型，**不處理設限，也不是 Kaplan–Meier**。中文維基百科目前沒有 Kaplan–Meier 專條。

## 十六件必須釘清的事

1. **怎麼讀。** 階梯只在事件發生時往下掉，兩次事件之間是平的；設限用短直線（或十字）標在曲線上，不下降；中位存活時間＝曲線第一次降到 0.5 或以下的時間；某個時間點的存活比例＝該時間曲線的高度；圖下風險人數表告訴你「還有多少人撐著這段曲線」。
2. **為什麼叫 Kaplan–Meier（原始揭露＋轉述）。** Edward L. Kaplan 與 Paul Meier 1958 年 6 月在《美國統計學會期刊》發表〈Nonparametric estimation from incomplete observations〉。依 **Stalpers 與 Kaplan 2018**：兩人是普林斯頓數學系研究生、在 John Tukey 指導下**各自**研究，後來聽從**當時期刊編輯**的建議合併稿件。英文維基百科寫「編輯就是 Tukey」說服合併——**來源與 Stalpers 不一致，本稿與素材包不採用維基那句**（無法證實）。Kaplan 1983 年自述（僅轉載）：Meier 1952 年讀到 Greenwood 論文而開始；Kaplan 一年後在貝爾實驗室研究海底電纜中繼器真空管壽命——方法一開始就同時有醫學與工程兩個出身。
3. **被冷落十年才紅（轉述）。** Stalpers 回顧前 100 篇引用，1969 年以前平均一年約一次；1969 年 Gehan 用在癌症病人後才進入醫學文獻。《自然》2014「史上被引用最多的 100 篇論文」：Kaplan–Meier 1958 排第 11、Cox 1972 排第 24（資料擷取 2014-10-07）。各資料庫引用次數差很多（約 34k–61k），**不寫死單一資料庫的精確引用次數**。
4. **設限要正確處理（S3）。** 同一份 200 人資料：正確第 12 月存活精確 **0.637**（圖說 0.64）、把設限當事件 0.42、刪掉設限者精確 **0.312**（圖說 0.31）；中位數正確 16.9、錯誤一 9.7、錯誤二 7.0（真實設定 20 月）。兩種錯誤都嚴重低估存活。
5. **尾端不可靠（S5）。** 風險人數少於 5 人從第 **22.2** 月起（以 0.1 月步進掃描）；最後一次事件在第 **27.3** 月、當時風險人數 3，一人事件就讓曲線從 0.104 掉到 0.070；之後到第 40.6 月的平線只剩 2 人且都是設限，**不代表之後沒人再出事**。中位數 8.5 月。真實對照見 R4（aml 資料尾端）。
6. **兩線交叉不要只報一個風險比（S6）。** 交叉點精確值是第 **20.0** 月（圖說可寫「約第 20.0 月」；理論交約 20.9 月）。整段風險比 0.88（0.66–1.18）、對數等級檢定 P=0.389，看起來「沒差」；以第 20 月切開，前段 1.20、後段 0.32。中位數：手術組 25.7、藥物組 21.4 月。
7. **截斷縱軸會放大差距（S7）。** 第 24 月存活 0.923 對 0.888，只差 **3.5 個百分點**，對數等級檢定精確 P=**0.0917**（圖說 0.092）。左圖縱軸從 0.6 起，這 3.5 百分點佔縱軸高度 8.5%；右圖從 0 起只佔 3.5%。要截斷就要在圖上明講（對照 R11）。
8. **一定要看信賴區間與風險人數（S4）。** 第 6／18／30 月區間寬精確 0.144／0.222／0.316（圖說 0.14／0.22／0.32），人越少帶子越寬。常用 Greenwood 公式；KMunicate 調查建議圖下加風險人數、累計設限與事件。
9. **兩組比較要報檢定與風險比（S2）。** 中位數 20.4 對 14.5 月；風險比（新療法 ÷ 標準療法）0.65（0.45–0.94）；對數等級檢定精確 P=**0.0223**（圖說 0.022）。前 6 個月交纏，第 6.1 月以後新療法在上。
10. **解剖要對上風險人數表（S1）。** 30 人、中位數 10.3 月；第 6／12／24 月存活 0.783／0.491／0.409；風險人數第 0–30 月每 6 月：30、21、8、6、2、1。
11. **手算時：同日設限在事件之後離開（S8）。** 8 人逐步乘積：0.875→0.750→0.600→0.450→0.225；中位數第 7 月；設限者丁 4、丙 9、己 12 月。
12. **急性骨髓性白血病（aml）教科書例子（已獨立重算）。** R 套件 survival 的 aml：n=23、事件 18、設限 5；全體中位 **27** 週；維持組 **31**、未維持 **23**；對數等級檢定 P≈**0.065**（卡方約 3.40）。Liora 獨立重算一致；我用公開 Rdatasets 的 aml.csv，以手寫 Kaplan–Meier／對數等級檢定與 lifelines 各算一次，數字一致（lifelines P=0.065339、卡方 3.396）。本環境沒有安裝 R，未能直接印套件官方報表。
13. **R13 署名兩層。** Commons 作者欄寫 Our World in Data（OWID）；圖面與來源頁署名 **Saloni Dattani**——兩層都要寫。
14. **競爭風險不能用 1−KM（轉載）。** Austin 等 2016：5 年心血管死亡 43.0%（1−KM）對 36.8%（累積發生率）。有競爭風險應改畫累積發生率曲線。
15. **圖面寫「約」時，精確值以 selfcheck／素材包為準。** 例如 S3 圖說 0.64＝精確 0.637；S2 圖說 P=0.022＝精確 0.0223；S6「約第 20.0 月」＝精確就是 20.0；S7 圖說 0.092＝精確 0.0917。
16. **圖片授權與來源要逐張標。** 20 張 Commons（R1–R20）各有個別作者與授權（見最下方）；S1–S8 自繪虛構資料，數字未核。不複製圖檔，只連連結。

## When

- 每個人（或零件、客戶）一列，至少兩個欄位——**觀察時間**（從共同起點算起）與**狀態**（1＝事件發生、0＝設限）；比較時再加**分組**
- 起點必須對每個人定義一致（確診日、簽約日、裝機日、隨機分組日）
- 情境（課程稿）：臨床試驗比較兩種療法「多久發生事件」、訂閱服務比較兩種方案多久退訂、工廠比較兩家供應商零件多久故障——而且不能把還沒發生事件的人丟掉
- **不適合**：設限跟結果有關（資訊性設限，KM 會高估存活）；有競爭風險（不能把競爭事件當普通設限）；只收已發生事件的人（與 S3「刪掉設限者」同類錯）；分組太多（五條以上前期交纏，見 R2）

## Recommend

- **主選**：Kaplan–Meier 存活曲線；兩組以上用顏色或線型區分；設限加短直線；加 95% 信賴區間帶與圖下風險人數表
- **口述步驟**（素材包第 4 節／課程稿第 6 節）：
  1. 定義起點與事件：時間從哪一天算、什麼算事件、研究何時截止
  2. 整理成兩欄（加分組欄）：觀察時間、狀態（1／0）；要比較就加組別
  3. 排序後只在事件時間計算：每個事件時間記下風險人數與事件數，存活比例乘上（1 − 事件數 ÷ 風險人數）；設限者離開後才從分母扣掉；同一天有事件也有設限，慣例是設限者在事件之後離開
  4. 畫成階梯：橫軸時間、縱軸 0 到 1；設限加短直線；每條曲線畫到該組最後一個觀察時間
  5. 加上不確定性與風險人數表：95% 信賴區間帶（常用 Greenwood）＋圖下風險人數（KMunicate 建議連累計設限與事件）
  6. 標出要讀的數字：中位數虛線、關鍵時間點存活比例；兩組比較時放對數等級檢定 P 值與風險比（含 95% 信賴區間），並寫明誰除以誰
  7. 決定畫到哪裡：尾端人太少時截掉、改淡色，或至少用風險人數表說清楚（S5）
  8. 檢查三個陷阱：交叉時不要只報一個風險比（S6）；縱軸截斷要明講（S7、R11）；有競爭風險時不要用「1 減 Kaplan–Meier」
- **工具誠實**：素材包沒有實測任何軟體。R 的 survival／survminer、Python 的 lifelines 只列連結；小資料可照 S8 手算。本 repo 驗證 aml 時另外用了 lifelines（在暫存虛擬環境安裝），不是素材包指定的步驟。
- **參數與判準範例（範例，不是標準）**：

| 項目 | 數值與出處 | 性質 |
|---|---|---|
| 中位存活時間 | 曲線第一次 ≤ 0.5 的時間（S1：10.3 月；aml：27 週） | 範例，不是標準 |
| 尾端警示 | 風險人數少於 5（S5 從 22.2 月起）或少於原始人數一成時標淡／截掉 | 範例，不是標準 |
| 交叉 | 只報一個風險比會把「先差後好」平均掉（S6：整段 0.88，前段 1.20、後段 0.32） | 範例，不是標準 |
| 縱軸 | 預設從 0 起；截斷必須明講（S7：3.5 百分點被放大成看起來很大） | 範例，不是標準 |
| 設限慣例 | 同日事件與設限：設限者在事件之後離開（S8） | 範例，不是標準 |
| 模擬圖人數 | S1＝30、S2＝200、S3＝200、S4＝60、S5＝40、S6＝300、S7＝800、S8＝8，僅為示意 | 範例，不是標準 |

## 與鄰近圖種的區別

本表是素材包的概述，除標明出處者外沒有逐項查證來源。

| 圖種 | 它回答什麼 | 和存活曲線的區別 |
|---|---|---|
| 折線圖（[`time-series-trend.md`](time-series-trend.md)） | 每個時間點一個觀察值、斜線相連 | 折線圖可上可下；存活曲線是**階梯**，只會往下或持平，兩次事件之間是平的 |
| 累積發生率曲線 | 往上畫「已經發生事件的比例」 | 沒有競爭風險時約等於 1−KM；有競爭風險時兩者不同（Austin 2016）。事件很少見時往上畫往往比較清楚 |
| 游泳圖（swimmer plot；≠ 泳道流程圖 swimlane） | 每人一條水平橫棒（像游泳池的一條水道），標治療區間、事件與截止時仍在 | 強調個別軌跡；KM 是把一群人收成族群存活比例曲線；見 [`swimmer-plot.md`](swimmer-plot.md) |
| 森林圖（[`forest-plot.md`](forest-plot.md)） | 風險比與信賴區間排成點與橫線 | **沒有時間軸**；常見搭配是 KM 看整體形狀，再用森林圖看各次族群風險比 |
| P–P 圖（[`pp-plot.md`](pp-plot.md)） | 診斷經驗分布是否符合理論 | 半參數式 P–P 可能用 KM 估經驗累積分布當一軸，但是診斷圖，不是給讀者看存活結果的圖 |
| Q–Q 圖（[`qq-plot.md`](qq-plot.md)） | 分位數對分位數的診斷 | 與存活時間分布的診斷有關，但不是 KM 曲線本身 |
| 生態學存活曲線（survivorship curve；R20） | 依相對年齡的存活個體數 | **同名不同物**：不處理設限、不是乘積極限估計 |

判斷口訣：**有觀察時間＋事件／設限、要看群體撐多久 → Kaplan–Meier；要看各研究的風險比點估計 → 森林圖；每人一條軌跡 → 游泳圖；有競爭風險 → 累積發生率，不要用 1−KM**。

## Avoid

- 把設限當事件，或直接刪掉設限者（S3）
- 把尾端平坦說成「治癒平台」（S5、R4）
- 兩線交叉只報一個風險比或一個對數等級 P 值（S6）
- 截斷縱軸卻不在圖上明講（S7、R11）
- 有競爭風險仍用 1−KM（Austin 2016）
- 寫「編輯就是 Tukey」或寫死單一資料庫的引用次數（歷史限定語）
- 把生態學 survivorship curve（R20）當成 Kaplan–Meier
- 分組太多、前期交纏卻不篩選要講的組（R2）
- 圖說只寫「約」卻不附精確值（S2／S3／S6／S7）
- 把 X 貼文當教學依據（只作連結）
- 把無法確認的全文頁（Taquet 2021、Miller 2010）當依據

## Produce checklist

- [ ] 起點、事件、截止日定義寫清楚；每人一列：觀察時間、狀態（1／0）、可選分組
- [ ] 階梯圖：事件時下降、設限短直線、每條線畫到該組最後觀察時間
- [ ] 95% 信賴區間帶（註明 Greenwood 或所用方法）＋圖下風險人數表（最好連累計設限／事件）
- [ ] 標中位數與關鍵時間點存活比例；兩組比較寫明風險比誰除以誰、P 值與區間
- [ ] 交叉時加分段結果；尾端人少標淡或截掉；縱軸若截斷必須明講
- [ ] 有競爭風險 → 改畫累積發生率，不用 1−KM
- [ ] 歷史歸屬用限定語（Stalpers 2018；不採用「編輯＝Tukey」）
- [ ] Commons 圖只連連結並標作者與授權（R13 兩層署名；R2／R11／R15 多人寫全）

## 虛構 demo 資料

素材包沒有指定哪一份給 repo → **8 組全部收錄**（`sample-km-s1-anatomy` … `sample-km-s8-step-by-step`，各 CSV＋selfcheck，共 16 檔）。檔名已有 `km` 前綴，與 `examples/data/` 既有檔**無撞名**，內容與素材包 `cmp` 逐位元相同。每支 selfcheck 以明確檔名讀 CSV（無 glob），取整一律四捨五入（逢 5 進位）；我在 `examples/data/` 與暫存資料夾各跑一次，全部 PASS。

獨立重算（pandas／numpy；aml 另用 lifelines）：與 selfcheck／素材包精確值一致——S1 中位 10.3、第 6／12／24 月 0.783／0.491／0.409；S2 中位 20.4／14.5、P=0.0223；S3 正確 0.637／刪除 0.312；S4 區間寬 0.144／0.222／0.316；S5 中位 8.5、風險<5 自 22.2 月、末事件 27.3 月；S6 交叉精確 20.0 月、中位 25.7／21.4；S7 0.923／0.888、差 3.5 百分點、P=0.0917；S8 階梯 0.875→0.750→0.600→0.450→0.225、中位第 7 月。**沒有發現素材包文字與 CSV 不一致。**

`draw_km.py`／`export_samples.py` **未收進本 repo**（見 ATTRIBUTION）。我從暫存資料夾以 `--outdir /tmp` 重跑：8 張模擬 PNG 與 8 個匯出 CSV 皆與素材包逐位元相同；素材包 `images/` 28 張與 `teach-viz/` 同名檔亦全部相同。

## 參考連結

以下只連 `sources.txt` 標「可開」的網址（72 條全部連結）。2 條「無法確認」只記名、標未核、**不當依據**（不連結）：

- **無法確認（未核，不連結）：** Taquet 等 2021《刺胳針精神醫學》全文頁（網站一直轉址，讀不到正文）；Miller 等 2010《腫瘤學期刊》DOI 頁（出版社拒絕存取）。R10／R15 的 Commons 圖頁仍可開並已連結，但原論文全文不當依據。

**百科與方法（可開）：**
- https://en.wikipedia.org/wiki/Kaplan%E2%80%93Meier_estimator
- https://ja.wikipedia.org/wiki/%E3%82%AB%E3%83%97%E3%83%A9%E3%83%B3%EF%BC%9D%E3%83%9E%E3%82%A4%E3%83%A4%E3%83%BC%E6%8E%A8%E5%AE%9A%E9%87%8F
- https://en.wikipedia.org/wiki/Survival_analysis
- https://zh.wikipedia.org/wiki/%E5%88%A0%E5%A4%B1
- https://zh.wikipedia.org/wiki/%E9%A3%8E%E9%99%A9%E6%AF%94
- https://en.wikipedia.org/wiki/Censoring_(statistics)
- https://en.wikipedia.org/wiki/Logrank_test
- https://en.wikipedia.org/wiki/Proportional_hazards_model
- https://en.wikipedia.org/wiki/Survivorship_curve
- https://en.wikipedia.org/wiki/Edward_L._Kaplan
- https://en.wikipedia.org/wiki/Paul_Meier_(statistician)

**論文與指引（可開）：**
- https://doi.org/10.2307/2281868 （Kaplan–Meier 1958）
- https://www.tandfonline.com/doi/full/10.1080/17498430.2018.1450055 （Stalpers 與 Kaplan 2018）
- https://www.nature.com/news/the-top-100-papers-1.16224
- https://pmc.ncbi.nlm.nih.gov/articles/PMC3932959/ （Rich 等 2010）
- https://pmc.ncbi.nlm.nih.gov/articles/PMC6773317/ （Morris 等 2019 KMunicate）
- https://doi.org/10.1016/S0140-6736(02)08594-X （Pocock 等 2002）
- https://pmc.ncbi.nlm.nih.gov/articles/PMC2394578/ （Pocock 等 2008）
- https://pmc.ncbi.nlm.nih.gov/articles/PMC4741409/ （Austin 等 2016）
- https://www.bmj.com/content/349/bmj.g5608
- https://www.bmj.com/content/372/bmj.n579
- https://pmc.ncbi.nlm.nih.gov/articles/PMC3148547/ （Elaimy 等 2011，R2 出處）

**資料與工具（可開）：**
- https://CRAN.R-project.org/package=survival
- https://lifelines.readthedocs.io/en/latest/Survival%20analysis%20with%20lifelines.html
- https://lifelines.readthedocs.io/en/latest/Survival%20Analysis%20intro.html
- https://rpkgs.datanovia.com/survminer/reference/ggsurvplot.html
- https://www.datanovia.com/learn/biostatistics/survival-analysis/kaplan-meier-estimation
- https://ourworldindata.org/childhood-leukemia-treatment-history
- https://meta.wikimedia.org/wiki/Research:Measuring_User_Search_Satisfaction
- https://www.databricks.com/blog/2021/02/24/solution-accelerator-telco-customer-churn-predictor.html
- https://blog.longwin.com.tw/2019/01/news-taiwan-startup-company-live-analysis-2019/
- https://www.plurk.com/p/ni2xmt
- https://youtu.be/W5tDrP2mGLA

**Commons 圖頁（可開，R1–R20；使用時必須標作者與授權）：**
- https://commons.wikimedia.org/wiki/File:Km_plot.svg （R1；CC0；Rw251）
- https://commons.wikimedia.org/wiki/File:Kaplan-Meier_curve_Tumor_Volume_Size.png （R2；CC BY-SA 2.0；作者九人寫全：Elaimy AL、Mackay AR、Lamoreaux WT、Fairbanks RK、Demakas JJ、Cooke BS、Peressini BJ、Holbrook JT、Lee CM）
- https://commons.wikimedia.org/wiki/File:Kaplan-Meier-sample-plot.svg （R3；CC0；Accountalive）
- https://commons.wikimedia.org/wiki/File:KM_plot_AML_survival.svg （R4；CC BY-SA 4.0；Michaelg2015）
- https://commons.wikimedia.org/wiki/File:Kaplan-Meier_by_treatment_in_AML.svg （R5；CC BY-SA 4.0；Michaelg2015）
- https://commons.wikimedia.org/wiki/File:Kaplan-Meier_curve_for_aml_with_confidence_bounds.svg （R6；CC BY-SA 4.0；Michaelg2015）
- https://commons.wikimedia.org/wiki/File:Aml_data_set_sorted_by_survival_time.png （R7；CC BY-SA 4.0；Michaelg2015）
- https://commons.wikimedia.org/wiki/File:Based_on_Collett_Fig_2.3.svg （R8；CC BY-SA 4.0；Michaelg2015；Commons 檔名依 Collett，書名頁面未載）
- https://commons.wikimedia.org/wiki/File:Survival_function_2_median_survival.svg （R9；CC BY-SA 4.0；Michaelg2015；平滑理論曲線，讀中位數方法相同）
- https://commons.wikimedia.org/wiki/File:CTCKaplanMeier.JPG （R10；CC BY 3.0；Miller 等；原論文 DOI 無法確認）
- https://commons.wikimedia.org/wiki/File:B.1.1.7_mortality_study_results.jpg （R11；CC BY 4.0；Challen 等六人寫全）
- https://commons.wikimedia.org/wiki/File:Kaplan-Meier_Survival_curves.png （R12；CC BY-SA 4.0；Amisffs）
- https://commons.wikimedia.org/wiki/File:Childhood-leukemia-survival-curves-cog-trials.png （R13；CC BY 4.0；Commons 作者欄＝OWID，圖面與來源頁署名 Saloni Dattani）
- https://commons.wikimedia.org/wiki/File:Estimaci%C3%B3_de_Kaplan-Meier_de_la_superviv%C3%A8ncia_de_malalts_amb_sida.svg （R14；CC BY-SA 3.0；Pep Roca）
- https://commons.wikimedia.org/wiki/File:Incidence_of_major_neurological_or_psychiatric_outcomes_in_the_6_months_after_COVID-19.jpg （R15；CC BY 4.0；Taquet 等五人；全文頁無法確認）
- https://commons.wikimedia.org/wiki/File:Cancer_in_Cowden_Syndrome.jpg （R16；公有領域；Stk11）
- https://commons.wikimedia.org/wiki/File:Courbe_survie_locotracteurs_Kaplan_Meier.svg （R17；CC BY-SA 3.0；Cdang）
- https://commons.wikimedia.org/wiki/File:Survival_page-visit-km-curve.png （R18；CC BY-SA 3.0；MPopov）
- https://commons.wikimedia.org/wiki/File:SDoC_baseline_-_Survival_curve_of_search_results_dwell_time_on_Commons.png （R19；CC BY-SA 4.0；CXie）
- https://commons.wikimedia.org/wiki/File:%E7%94%9F%E5%AD%98%E6%9B%B2%E7%B7%9A.svg （R20；CC0；生態學存活曲線，勿與 KM 混淆）

**連結統計：** sources.txt 74 條網址（檔案共 81 行，含 7 行 `#` 說明）＝可開 72＋無法確認 2＋打不開 0。可開 72 條全部連結；無法確認 2 條只記名未核。我另外用 Commons API（2026-10-05，台北）逐張查了 20 個檔案頁的授權簡稱與作者欄，與素材包相符：R1、R3、R20＝CC0；R2＝CC BY-SA 2.0（作者九人與素材包一致）；R4–R9＝CC BY-SA 4.0／Michaelg2015；R10＝CC BY 3.0／Miller 等；R11＝CC BY 4.0／Challen 等；R12＝CC BY-SA 4.0／Amisffs；R13＝CC BY 4.0、API 作者欄＝OWID（與素材包「Commons 作者欄寫 OWID、圖面署名 Saloni Dattani」一致，我沒有重讀圖面）；R14＝CC BY-SA 3.0／Pep Roca；R15＝CC BY 4.0／Taquet 等五人；R16＝公有領域／Stk11；R17＝CC BY-SA 3.0／Cdang；R18＝CC BY-SA 3.0／MPopov；R19＝CC BY-SA 4.0／CXie。

### X 貼文（只作連結，不當教學依據）

繁體中文談 Kaplan–Meier 方法的專帖：**0** 則。原帖共 **19** 則（含 2 則繁中只用「存活分析／存活曲線」一詞、內容不是 KM 方法）。審稿以 X 官方貼文讀取在台北時間 2026-10-05 下午逐則讀回；數字一律未核，僅轉載。

- https://x.com/planet4589/status/1894551338043736473
- https://x.com/planet4589/status/1791172709168316530
- https://x.com/ChandrakanthMv/status/2055874538588823604
- https://x.com/igakuhenyu_lab/status/2086930252237099217
- https://x.com/ProtocolDotMed/status/2093969120169742502
- https://x.com/ProtocolDotMed/status/2103505522762858777
- https://x.com/CathLabAH/status/2103567610872725898
- https://x.com/jasonryanmd/status/2056915048258257215
- https://x.com/dhughesPharmD/status/1575446266485555202
- https://x.com/BBiostatistics/status/2023544151988695058
- https://x.com/TheLancetNeuro/status/676699007750643712
- https://x.com/VPrasadMDMPH/status/1716620353978749075
- https://x.com/tsung/status/1088232469093060608
- https://x.com/ly2314/status/1176686252986441728
- https://x.com/LeopolisDream/status/1575870068985982977
- https://x.com/pash22/status/949039035024101377
- https://x.com/kentalog1127/status/1956679835432165648
- https://x.com/ShingoHatakeya1/status/1979092619767509434
- https://x.com/theosanderson/status/1357806104412114954

鄰居 pattern：`forest-plot.md`（風險比與信賴區間的點估計，沒有時間軸；常與 KM 搭配）、`time-series-trend.md`（一般折線可上可下；KM 是只降不升的階梯）、`pp-plot.md`／`qq-plot.md`（診斷圖，可能用到 KM 估經驗分布，但不是給讀者看存活結果）、`control-chart.md`（流程是否受控；與存活時間分析不同）、`marey-chart.md`（移動物體沿路線的時刻，不是事件發生時間的群體估計）、`swimmer-plot.md`（游泳圖：每人一條觀察到的治療棒；人多時改用 KM）。

## 圖檔與授權（不複製，只連結）

28 張＝Commons 真實／示意圖 R1–R20（各有個別作者與授權）＋自繪模擬 S1–S8（虛構資料，數字未核）。**不把圖檔散佈進本 repo。** R2／R11／R15 多人作者必須寫全；R13 必須同時寫 Commons 作者欄 OWID 與圖面署名 Saloni Dattani；R8 書名頁面未載；R10／R15 原論文全文無法確認、Commons 頁仍可連。部分真實圖目測讀數（R2、R14、R19 等）標目測未核。
