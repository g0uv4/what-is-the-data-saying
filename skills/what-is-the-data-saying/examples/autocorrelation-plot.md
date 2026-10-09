# Pattern: autocorrelation-plot

> **圖種**：自相關圖（autocorrelation plot）
> **來源（專案維護者整理）**：`teach-viz/2026-10-09-am-autocorr.md`（方法教學；第一次以自相關圖為主題）
> **亦稱**：英文 autocorrelation plot；別名 autocorrelogram、acf plot（autocorrelation function plot）；也常叫「自相關函數圖」。偏自相關圖＝partial autocorrelation plot／pacf plot。中文維基百科正體條目用「自我相關」「序列相關」「相關圖」；PTC Mathcad 繁體中文說明用「自相關性」「偏自相關性」；**臺灣官方規範譯名未核**（樂詞網查詢結果未能讀取）。大陸常見「自相关图」「偏自相关图」「自相关函数图」，依網路公開文章用法歸納，**未經官方名詞網站核實**
> **核心**：將單一時間序列在不同「時間差」（稱為滯後）下，計算其與自身數值的皮爾森相關係數，並將各滯後的係數繪製成棒或線；滯後 0 恆為 1，圖上通常標一條近似 95% 信心帶
> **一句話**：「隔幾步還跟自己有關」——有沒有週期、趨勢，殘差像不像白噪音。
> **誠實提醒**：本課是方法教學；模擬圖與本 repo 的練習資料都是虛構，**數字未核**。英文 correlogram 有兩種意思：時間序列棒圖＝本課的自相關圖；變數×變數色塊圖一律寫「相關矩陣」，不單獨用「相關圖」三個字。
> **潤稿狀態**：課程終稿與素材包寫明已經審稿人審核並潤稿；**沒有寫出潤稿用哪一個工具**，本稿不推測、也不另送潤稿。素材包文字依終稿整理。

## 十二件必須釘清的事

1. **怎麼讀（依序）。** 先確認滯後 0＝1、橫軸是滯後、縱軸是自相關係數（兩軸都是變數名稱的是相關矩陣，不是本課圖種；S7、R16）→ 看信心帶是固定寬度 ±1.96／√n（檢驗隨機性）還是隨滯後變寬（模型識別，R17、R20；樣本越長帶越窄，S4）→ 看樣貌（全在帶內＝可能近似白噪音；緩慢衰減＝可能有趨勢、非平穩或強自我迴歸；週期倍數尖峰＝可能有季節性；正負交替＝可能振盪；S2、S5、R2–R5、R18）→ 需要時並排看偏自相關 → 回頭對照折線圖與背景知識。
2. **correlogram 有兩種意思，務必分開。**（1）時間序列自相關／偏自相關棒圖＝本課，稱為自相關圖；（2）變數×變數相關矩陣熱圖＝熱圖家族（圖 R16、圖 S7 右側）。本稿「自相關圖」只指第（1）種；第（2）種一律寫「相關矩陣」或「變數×變數相關圖」；**不單獨用「相關圖」三個字**。中文維基百科正體條目把「相關圖」列為名稱之一，那是條目用語，不是本稿圖種名。
3. **構造。** C(k)＝(1/n) Σ (x_t−μ)(x_{t+k}−μ)（t 從 1 加總至 n−k，μ 為樣本平均），r(k)＝C(k)/C(0)，r(0) 恆為 1。白噪音假設下近似 95% 信心帶 ±1.96／√n（NIST 第 1.3.3.1 節）。另有依 Bartlett 公式、假設移動平均過程、隨滯後變寬的帶，NIST 建議用於模型識別（圖 R17）。
4. **軟體預設不同，圖上要寫明。** R 的 `acf` 預設固定寬度信心帶；statsmodels `plot_acf` 與 Stata `ac` 預設依 Bartlett 公式變寬的帶。畫之前先確認產出的是哪一種。
5. **非平穩未處理就解讀「記憶很長」（S6）。** 隨機漫步的自相關滯後 1≈0.971、滯後 20≈0.498 緩慢衰減；一階差分後滯後 1≈0.004、滯後 5≈-0.014，近似白噪音。應先差分或去趨勢。
6. **短序列的尖峰當真（S4）。** n＝50 時信心半寬≈0.2772，許多尖峰只是隨機噪音；n＝200≈0.1386、n＝800≈0.0693（皆 1.96／√n）。單一尖峰略出帶，在 95% 信心帶設定下本來就可能偶爾出現（NIST 隨機資料頁提醒）；先換一段時間重畫、搭配偏自相關與背景知識。
7. **把偏自相關定階當定論（S3、R7）。** 理論上 p 階自我迴歸過程的偏自相關在滯後 p＋1 之後為 0；樣本偏自相關在階 p 後落入帶內，自我迴歸階數可能約為 p（NIST 第 6.4.4.6 節）。這只是起點：樣本係數會波動，混合模型尤其難判斷；NIST 提及近年多改用資訊準則輔助。S3（係數 0.6、−0.3，n＝500，半寬≈0.0877）：偏自相關滯後 1≈0.459、滯後 2≈-0.291、滯後 3≈-0.027、滯後 4≈-0.046，約在階 2 後進帶。
8. **最大滯後沒寫或太短。** 「不超過 n/4」只是經驗法則（多本教材歸於 Box 與 Jenkins，本稿沒有讀原書；蘇黎世聯邦理工學院 Dettling 投影片列出「約 10×log₁₀(n)」與「約 n/4」兩種）。R `acf` 預設 10×log₁₀(n)；Stata 預設取「n/2 減 2」與 40 的較小值。要觀察每週週期至少畫到滯後 14。沒有唯一標準，圖上寫明你用多少。
9. **歷史用限定語。** Box 與 Jenkins 1970《Time Series Analysis: Forecasting and Control》確立自相關圖與偏自相關圖為模型識別標準工具（NIST 引該書第 28–32、64–65 頁）。Yule 1927（第 226 卷第 267–298 頁）、Walker 1931（第 131 卷第 518–532 頁）、Quenouille 1949（第 11 卷第 1 期第 68–84 頁）書目依 Crossref 核對，**沒有讀全文**。偏自相關計算通常用 Durbin–Levinson 遞迴（Durbin 1960）。
10. **譯名限定語。** 臺灣官方規範譯名未核（樂詞網查詢結果未能讀取）。大陸用詞未經官方名詞網站核實。本稿用「自相關圖」是本次教學指定名稱。
11. **授權與「只放連結」。** 本包沒有嵌入任何非商業授權的圖。Hyndman《預測：原理與實務》線上書（未能截圖）、期刊與數位物件識別碼頁、JSTOR、軟體手冊只放連結，不複製圖片或內文。Yule 1927、Walker 1931、Quenouille 1949 三個數位物件識別碼頁**無法確認、只記名**。
12. **原圖問題照錄不改。** S7 左圖標題寫「本課的『相關圖／自相關圖』」，是圖面原有文字，本稿文字說明一律用「自相關圖」（圖沒有重畫）。R16 是維基共享資源「文章意見回饋」五項評分相關熱圖（CC BY-SA 3.0，作者 Protonk）；圖上刻意未標數字、也沒有色階。R17 來源頁未載明繪圖軟體，圖表下方註記與 Stata 官方手冊 `ac` 預設註記相同，因此**判斷為 Stata 輸出風格**（不要斷言它就是 Stata 輸出）。R12 縱軸上限截在 0.35，滯後 0 的棒（等於 1）因而被截除；不做投資判斷。R15 五個面板標題 retention(1)、(2)、(5)、(10)、(30)，來源頁未說明括號內數字。R13 僅作方法案例，不做經濟或投資判斷。

## When

- 有時間順序、間隔固定的數值序列（每日氣溫、來客數、感測器讀數、網站流量、製造殘差），想知道「隔幾步還跟自己有關」
- 檢查殘差像不像白噪音（S2 左、R2）；找週期——每日資料看 7 的倍數（可能每週循環）、每月資料看 12 的倍數（可能每年循環）（S5、R5、R6）；看趨勢或非平穩（S2 中、S6 左、R1、R4）；與偏自相關圖一起討論自我迴歸／移動平均階數（S3、R7、R10）
- 情境（課程稿，數字只是示範，不是真實測站）：社區小型氣象站每小時記錄氣溫、已連續兩個月；最近 60 天整點氣溫（約 1440 點），自相關圖最大滯後至少 48（兩天），標 ±1.96／√n 信心帶
- **不適合**：序列太短（只有幾十點，S4 左）；明顯非平穩卻未處理（先差分或去趨勢，S6）；只有類別資料或沒有時間順序；讀者只想看原始數值高低（折線圖更清楚）；把相關矩陣熱圖誤叫成自相關圖（R16、S7 右）

## Recommend

- **主選**：橫軸滯後、縱軸自相關係數的棒圖；滯後 0＝1；圖上寫明樣本長度、最大滯後、信心帶公式，以及資料是否經過差分或去除季節
- **口述步驟**（素材包第 7 節）：
  1. 確認資料。必須是一條依照時間順序排列且間隔固定的數值序列；缺失值先決定填補或分段。樣本太短（僅數十點）時，先理解信心帶會相當寬（圖 S4）
  2. 先看折線。有明顯趨勢、隨機漫步或季節性時，自相關圖會反映為「緩慢衰減」或「週期尖峰」，解讀前往往要先差分或去除季節性（圖 S6）
  3. 選最大滯後。常見經驗法則不超過 n/4；R `acf` 預設 10×log₁₀(n)；Stata 預設取「n/2 減 2」與 40 的較小值。要觀察每週週期至少畫到滯後 14。沒有唯一標準，圖上寫明你用多少
  4. 算各滯後的自相關係數。採用第 3 點的定義（或軟體預設的等價定義），確認滯後 0＝1
  5. 畫棒圖並加上信心帶。檢驗隨機性用固定寬度 ±1.96／√n；模型識別時 NIST 建議改用 Bartlett 公式隨滯後變寬的帶（圖 R17）。先確認軟體預設是哪一種，並在圖上標示
  6. 需要討論自我迴歸階數時，並排畫偏自相關圖。觀察偏自相關在第幾階之後落入帶內（圖 S3、圖 R7）；這只是起點
  7. 解讀。全在帶內＝可能近似白噪音；緩慢衰減＝可能趨勢、非平穩或強自我迴歸；週期倍數尖峰＝可能季節性；正負交替＝可能振盪。單一尖峰略出帶，在 95% 信心帶下本來就可能偶爾出現
  8. 標清楚。樣本長度、最大滯後、信心帶公式、是否差分。不要只標記含糊的「相關圖」三個字
  9. 工具。試算表、統計套件或程式庫皆可；本稿不教授操作步驟或程式碼，只要求產出「棒高代表係數、帶狀區域代表信心區間」的同一種圖表格式
- **工具誠實**：R 的 `acf`／`pacf`、pandas `autocorrelation_plot`、statsmodels `plot_acf`／`plot_pacf`、Stata `ac`／`pac` 只列連結，**本 repo 未實測**。模擬圖的畫圖腳本沒有收進來。Hyndman《預測：原理與實務》線上書自相關章無法確認，只記名、不連結。
- **參數與判準範例（範例，不是標準）**：

| 項目 | 數值與出處 | 性質 |
|---|---|---|
| 自相關係數 | r(k)＝C(k)/C(0)，C(k)＝(1/n)Σ(x_t−μ)(x_{t+k}−μ)；r(0)＝1；係數四捨五入到小數第三位 | 本包模擬圖的定義 |
| 固定寬度信心帶 | 白噪音假設下 ±1.96／√n（NIST 1.3.3.1） | 檢驗隨機性；R `acf` 預設 |
| Bartlett 變寬帶 | 移動平均假設下隨滯後變寬（NIST 建議用於模型識別） | statsmodels `plot_acf`、Stata `ac` 預設 |
| 模擬半寬 | S1 n＝200 → 0.1386；S2／S6 n＝300 → 0.1132；S3 n＝500 → 0.0877；S4 n＝50／200／800 → 0.2772／0.1386／0.0693；S5 n＝400 → 0.098；S8 n＝120 → 0.1789 | 範例，不是標準 |
| 最大滯後 | 經驗法則不超過 n/4；R 預設 10×log₁₀(n)；Stata 預設 min(n/2−2, 40) | 經驗法則；Box 與 Jenkins 原書頁碼未核 |
| 偏自相關定階 | 偏自相關在階 p 後進帶 → 自我迴歸階數可能約為 p（NIST 6.4.4.6）；只是起點 | 常見做法，不是定論 |
| 模擬種子 | 亂數種子 20261009；偏自相關用 Durbin–Levinson | 本包模擬圖 |

## 與鄰近圖種的區別

本表是素材包的概述，除標明出處者外沒有逐項查證來源。

| 圖種 | 圖上一個單位代表 | 顏色或位置代表 | 和自相關圖的關係 |
|---|---|---|---|
| 自相關圖（本稿） | 一個滯後 | 棒高代表自相關係數 | — |
| 偏自相關圖（本 repo 無專檔） | 一個滯後 | 棒高代表偏自相關係數 | 常與自相關圖並列呈現；用於討論自我迴歸階數（圖 S3） |
| 相關矩陣（correlogram 另一義；[`matrix-heatmap.md`](matrix-heatmap.md)） | 變數 i × 變數 j | 顏色代表兩變數相關係數 | 兩者同名而實質相異；坐標軸為變數名稱而非滯後（圖 R16、圖 S7） |
| 遞迴圖（[`recurrence-plot.md`](recurrence-plot.md)） | 時間 i × 時間 j | 黑色代表兩時段狀態足夠相似 | 同樣可用於探查週期，但保留了「具體重複的時間區段」；自相關圖則是將所有成對時間差濃縮為單一統計係數 |
| 頻譜圖（[`spectrogram.md`](spectrogram.md)） | 時間 × 頻率 | 顏色代表能量大小 | 於頻率域觀察週期；自相關則於時間差域觀察週期。兩者可透過維納–辛欽關係建立連結（此屬進階理論，本稿不予展開） |
| 管制圖（[`control-chart.md`](control-chart.md)） | 一個時間點 | 位置代表數值大小與管制界限 | 管制圖著重於監控數值是否超出管制界限；自相關圖則檢視殘差或序列是否仍存有「隔幾步的相關」 |
| 地平線圖（[`horizon-chart.md`](horizon-chart.md)）、螺旋圖（[`spiral-plot.md`](spiral-plot.md)）、日曆熱圖（[`calendar-heatmap.md`](calendar-heatmap.md)） | 一個時間點 | 顏色或折疊層級代表數值大小 | 此三種圖表通常預先假設週期已知後進行排版；自相關圖則能由尖峰所在位置主動呈現潛在週期 |
| 折線圖（[`time-series-trend.md`](time-series-trend.md)） | 一個時間點 | 高度代表數值大小 | 觀察整體趨勢與異常值最為直接；自相關圖則是進一步分析的「結構診斷」工具 |
| 滯後圖（lag plot，未教過） | 單一點代表 (x_t, x_{t+k}) | 位置 | 僅檢視單一滯後的散佈狀況；自相關圖則將多個滯後的相關係數依序排列呈現 |

判斷口訣：**一條等距時間序列、想看隔幾步還跟自己有關 → 自相關圖；兩軸是變數名稱 → 相關矩陣；想看何時回到相近狀態、又不想先假定週期 → 遞迴圖；想看什麼時間有哪些頻率 → 頻譜圖；只想看數值高低 → 折線。**

## Avoid

- 把相關矩陣熱圖叫成自相關圖，或只標「相關圖」三個字（S7、R16）
- 非平穩未處理就解讀「記憶很長」（S6：未差分滯後 1≈0.971、滯後 20≈0.498；差分後滯後 1≈0.004）
- 把短序列的尖峰當真（S4：n＝50 半寬≈0.2772）
- 單一尖峰略出帶就說發現新週期
- 把偏自相關定階當定論（S3、R7）
- 沒確認軟體預設信心帶（R 固定寬度；statsmodels／Stata 預設 Bartlett 變寬）
- 最大滯後沒寫或太短（每週週期至少畫到滯後 14）
- 把 Yule 1927、Walker 1931、Quenouille 1949 寫成已讀全文（書目已核、全文未讀）
- 把 R17 斷言為 Stata 輸出（只寫「判斷為 Stata 輸出風格」）
- 把 X 貼文當教學依據（本次原帖 0 則，不編造）

## Produce checklist

- [ ] 確認是等間隔、有時間順序的數值序列；缺失值已決定填補或分段
- [ ] 先看折線；有趨勢或隨機漫步先差分或去趨勢，有季節先處理
- [ ] 選最大滯後並寫在圖上；滯後 0＝1
- [ ] 畫棒圖；寫明信心帶公式（固定 ±1.96／√n 或 Bartlett 變寬）與軟體預設
- [ ] 需要討論自我迴歸階數時並排偏自相關圖；定階只當起點
- [ ] 圖說：樣本長度、最大滯後、是否差分或去除季節；不要只標「相關圖」三個字
- [ ] 譯名用限定語（官方譯名未核；correlogram 第二義寫「相關矩陣」）
- [ ] 模擬圖標「模擬」、數字虛構；R 圖標作者與授權；S7 左圖標題照錄不改

## 虛構 demo 資料

素材包沒有指定哪一份給 repo → **8 組全部收錄**（`sample-autocorr-s1-anatomy` … `sample-autocorr-s8-steps`，各 CSV＋selfcheck，共 16 檔）。檔名已有 `autocorr` 前綴，與 `examples/data/` 既有檔**無撞名**，8 個 CSV **與素材包逐位元相同**，沒有再縮小。8 個 CSV 合計 **178,186 位元組（約 174.0 KiB）**，單檔最大是 S4 的 53,579 位元組（約 52.3 KiB）。`draw_autocorr.py` 與 `export_samples.py` **沒有收進本 repo**。

自檢以明確檔名讀 CSV（`read_rows("sample-autocorr-sN-….csv")`，從腳本所在資料夾讀，無 glob），只用 Python 標準函式庫（自寫平均、自相關 r(k)＝C(k)/C(0)、Durbin–Levinson 偏自相關與信心半寬 1.96／√n，不靠 numpy）。我在 `examples/data/` 與暫存資料夾各跑一次，8 支都是 `RESULT: PASS`、結束碼 0（通過項數 9、12、12、11、9、11、21、10）。

| 檔 | CSV 位元組 | 列數 | 欄位 |
|---|---:|---:|---|
| S1 `sample-autocorr-s1-anatomy.csv` | 9611 | 200 | `t,x,data_status` |
| S2 `sample-autocorr-s2-three-patterns.csv` | 23143 | 300 | `t,white_noise,linear_trend,period_7,data_status` |
| S3 `sample-autocorr-s3-acf-pacf.csv` | 23690 | 500 | `t,x,data_status` |
| S4 `sample-autocorr-s4-sample-size-ci.csv` | 53579 | 1050 | `series_n,t,x,data_status` |
| S5 `sample-autocorr-s5-period-spikes.csv` | 19011 | 400 | `t,x,data_status` |
| S6 `sample-autocorr-s6-nonstationary.csv` | 18470 | 300 | `t,random_walk,diff1,data_status`（差分 299 點，t＝0 留空） |
| S7 `sample-autocorr-s7-two-correlograms.csv` | 24927 | 200 | `t,x_series,var_jia,var_yi,var_bing,var_ding,var_wu,data_status`（甲到戊） |
| S8 `sample-autocorr-s8-steps.csv` | 5755 | 120 | `t,x,data_status` |

自檢腳本位元組：S1 3336、S2 3737、S3 3585、S4 3639、S5 3293、S6 3632、S7 4054、S8 3350。

**CSV 格式：** 第 1 行是 `# 虛構資料，數字未核｜…`。之後是表頭，最後一欄 `data_status` 一律「虛構資料，數字未核」。t＝時間點編號。

**以實際計數為準**（自檢從 CSV 重算，與課程稿關鍵讀數一致）：(1) 虛構資料，**數字未核**；(2) S1 滯後 0＝1、半寬 0.1386、滯後 1／12／24＝0.759／0.838／0.787，滯後 12 是 1–30 中最大的正尖峰；(3) S2 半寬 0.1132；白噪音滯後 1／7＝-0.072／0.037，滯後 1–40 出帶 1 根；趨勢滯後 1／20＝0.962／0.787，滯後 1–20 全在帶外；週期滯後 7／14＝0.869／0.842；(4) S3 半寬 0.0877；自相關滯後 1／2／5＝0.459／-0.019／-0.086；偏自相關滯後 1–4＝0.459／-0.291／-0.027／-0.046，滯後 1、2 在帶外、3、4 在帶內；(5) S4 半寬 0.2772／0.1386／0.0693，滯後 1＝0.026／0.04／-0.025；(6) S5 半寬 0.098，滯後 7／14／21／28＝0.913／0.9／0.882／0.862；(7) S6 未差分滯後 1／20／40＝0.971／0.498／-0.006，差分後滯後 1／5＝0.004／-0.014；(8) S7 滯後 10＝0.837；甲×乙≈0.794、甲×丁≈-0.481、乙×丙≈0.584；(9) S8 半寬 0.1789，滯後 1／8／16／24＝0.576／0.799／0.752／0.693，n/4＝30。

## 參考連結

只連來源清單裡標「可開」的網址（37 條全部連結）。打不開 0 條。以下 4 條**只記名、標未核、不連結**（網站拒絕自動連線或未正常回應，可能遭驗證碼阻擋；不代表頁面不存在，但不當依據。其中 3 篇的書目在 Crossref 查得到）：

- **無法確認（4，未核）：** Hyndman《預測：原理與實務》第 2 版／第 3 版線上書自相關專章（未能截圖；可能遭驗證碼阻擋）；Yule 1927 尤爾–沃克方程式原始論文數位物件識別碼頁；Walker 1931 尤爾–沃克方程式原始論文數位物件識別碼頁；Quenouille 1949 偏相關近似檢定（皇家統計學會期刊 B）數位物件識別碼頁。

**名稱、定義與工具**

- [英文維基百科〈Autocorrelation〉](https://en.wikipedia.org/wiki/Autocorrelation)
- [英文維基百科〈Correlogram〉（同時提到時間序列棒圖與相關矩陣色塊）](https://en.wikipedia.org/wiki/Correlogram)
- [英文維基百科〈Partial autocorrelation function〉](https://en.wikipedia.org/wiki/Partial_autocorrelation_function)
- [英文維基百科〈Box–Jenkins method〉](https://en.wikipedia.org/wiki/Box%E2%80%93Jenkins_method)
- [中文維基百科〈自我相關函數〉（正體）](https://zh.wikipedia.org/zh-tw/%E8%87%AA%E7%9B%B8%E5%85%B3%E5%87%BD%E6%95%B0)
- [NIST《統計方法電子手冊》1.3.3.1 Autocorrelation Plot](https://www.itl.nist.gov/div898/handbook/eda/section3/eda331.htm)
- [NIST：自相關圖—隨機資料](https://www.itl.nist.gov/div898/handbook/eda/section3/autocop1.htm)
- [NIST：自相關圖—中等自相關](https://www.itl.nist.gov/div898/handbook/eda/section3/autocop2.htm)
- [NIST：自相關圖—強自相關與自我迴歸](https://www.itl.nist.gov/div898/handbook/eda/section3/autocop3.htm)
- [NIST：自相關圖—正弦模型](https://www.itl.nist.gov/div898/handbook/eda/section3/autocop4.htm)
- [NIST《統計方法電子手冊》6.4.4.6 Box–Jenkins 模型識別](https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc446.htm)
- [NIST《統計方法電子手冊》6.4.4.6.3 偏自相關圖](https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc4463.htm)
- [R 說明頁：acf／pacf](https://search.r-project.org/R/refmans/stats/html/acf.html)
- [R 說明頁：plot.acf（信心帶種類預設值）](https://search.r-project.org/R/refmans/stats/html/plot.acf.html)
- [Stata 官方手冊：corrgram／ac／pac](https://www.stata.com/manuals/tscorrgram.pdf)
- [蘇黎世聯邦理工學院 Dettling《應用時間序列分析》2011 年課程投影片第 3 週（最大滯後經驗法則）](https://stat.ethz.ch/education/semesters/ss2011/atsa/ATSA-FS11-Slides-Week03.pdf)
- [pandas：autocorrelation_plot 說明](https://pandas.pydata.org/docs/reference/api/pandas.plotting.autocorrelation_plot.html)
- [statsmodels：plot_acf 說明](https://www.statsmodels.org/stable/generated/statsmodels.graphics.tsaplots.plot_acf.html)
- [statsmodels：plot_pacf 說明](https://www.statsmodels.org/stable/generated/statsmodels.graphics.tsaplots.plot_pacf.html)
- [Durbin 1960〈The Fitting of Time-Series Models〉JSTOR 頁](https://www.jstor.org/stable/1401322)
- [國家教育研究院樂詞網（本次讀不到查詢結果列）](https://terms.naer.edu.tw/)
- [PTC Mathcad 繁中：相關性與偏自相關性範例](https://support.ptc.com/help/mathcad/r11.0/zh_TW/PTC_Mathcad_Help/example_correlation_and_partial_autocorrelation.html)

**R 圖來源頁（只連到頁面，不嵌圖）**

- [圖 R1：NIST 樣本自相關圖（FLICKER.DAT）](https://www.itl.nist.gov/div898/handbook/eda/section3/eda331.htm)
- [圖 R2：NIST 隨機／白噪音](https://www.itl.nist.gov/div898/handbook/eda/section3/autocop1.htm)
- [圖 R3：NIST 中等自相關](https://www.itl.nist.gov/div898/handbook/eda/section3/autocop2.htm)
- [圖 R4：NIST 強自相關／自我迴歸](https://www.itl.nist.gov/div898/handbook/eda/section3/autocop3.htm)
- [圖 R5：NIST 正弦模型](https://www.itl.nist.gov/div898/handbook/eda/section3/autocop4.htm)
- [圖 R6：隱藏在噪音裡的週期約 10](https://commons.wikimedia.org/wiki/File:Acf.svg)
- [圖 R7：自相關對偏自相關（模擬自我迴歸階 3）](https://commons.wikimedia.org/wiki/File:Autocorrelation_Function_vs._Partial_Autocorrelation_Function.png)
- [圖 R8：自我迴歸階 1 樣本自相關圖](https://commons.wikimedia.org/wiki/File:Correlogram_example.png)
- [圖 R9：同一過程重複抽樣 20 次](https://commons.wikimedia.org/wiki/File:Correlogram_samples.png)
- [圖 R10：模擬自我迴歸階 3 的偏自相關](https://commons.wikimedia.org/wiki/File:Partial_Autocorrelation_Function_Graph.png)
- [圖 R11：休倫湖水深的偏自相關](https://commons.wikimedia.org/wiki/File:Partial_autocorrelation_function.png)
- [圖 R12：虛構公司 ACME Corp 三圖併排](https://commons.wikimedia.org/wiki/File:Acme_Autocorrelation.png)
- [圖 R13：美國實質人均國內生產毛額年成長的自相關（僅作方法案例）](https://commons.wikimedia.org/wiki/File:Autocorrelations_of_annual_growth_in_real_US_GDP_per_capita_since_1790.svg)
- [圖 R14：英文維基「待審建立」每月投稿數的偏自相關](https://commons.wikimedia.org/wiki/File:AfC_submissions_per_month_PACF.png)
- [圖 R15：每日留存機率的自相關](https://commons.wikimedia.org/wiki/File:Acf_retention.png)
- [圖 R16：文章意見回饋五項評分相關熱圖（correlogram 第二義）](https://commons.wikimedia.org/wiki/File:Heatmap_of_Correlation_between_Averages_in_Different_Article_Feedback_Categories.svg)
- [圖 R17：時間序列自相關圖（變數 JÜ；判斷為 Stata 輸出風格）](https://commons.wikimedia.org/wiki/File:Correlogram.png)
- [圖 R18：三種自相關樣貌示意](https://commons.wikimedia.org/wiki/File:Autocorr.svg)
- [圖 R19：自相關圖用途示意](https://commons.wikimedia.org/wiki/File:Esempioautocorr.svg)
- [圖 R20：英文維基管理員資格申請每月成功案件的自相關](https://commons.wikimedia.org/wiki/File:Autocorrelation_of_RfA.svg)

**連結統計：** 41 個網址＝可開 37＋打不開 0＋無法確認 4。來源清單檔共 48 行，其中 7 行是 `#` 說明。可開 37 條全部連結；4 條只記名未核。X 原帖 0 則，合計不含 X。

### X 貼文（只作連結，不當教學依據）

以 X 官方搜尋查詢英文「autocorrelation plot」「ACF plot」「PACF plot」「autocorrelation」「partial autocorrelation」與中文「自相關圖」「偏自相關」等關鍵詞（台北時間 2026-10-09 上午）。精確片語搜尋多次回傳 0 筆；隨後查詢工具因請求次數超過上限而暫停回應。另行使用網路搜尋（限定 x.com 與 twitter.com）以及 DuckDuckGo 進行頁面擷取，**都沒有找到可核對的原帖連結**。**因此原帖筆數＝0。** 不編造任何帳號或網址。

鄰居 pattern：`matrix-heatmap.md`（相關矩陣＝correlogram 第二義；本檔是時間序列滯後棒圖）、`recurrence-plot.md`（時間×時間的相似方陣；自相關把所有成對時間差濃縮成單一係數）、`spectrogram.md`（時間 × 頻率看週期；自相關在時間差域看週期）、`time-series-trend.md`（折線看數值高低；自相關是結構診斷）、`control-chart.md`（盯單一數值有沒有超出管制界限；自相關看殘差隔幾步還有相關）、`horizon-chart.md`、`spiral-plot.md`、`calendar-heatmap.md`（先假設週期再排版；自相關由尖峰位置呈現潛在週期）。

## 圖檔與授權（不複製，只連結）

課程稿嵌 **28** 張＝真實／示意圖 R1–R20（20 張）＋自繪模擬 S1–S8（8 張，虛構資料，數字未核）。本 repo **不複製任何圖檔**，只連到來源頁；引用時保留作者與授權。

授權以素材包 `licenses.json` 為準（R6–R20 經維基共享資源介面核對）：

- **R1–R5** 公有領域（美國政府著作，NIST／SEMATECH《統計方法電子手冊》）。R1 樣本自相關圖（FLICKER.DAT）：相鄰觀測值高度相關。R2 隨機／白噪音：滯後大於 0 之後幾乎全在帶內。R3 中等自相關。R4 強自相關／自我迴歸型。R5 正弦模型：正負尖峰交替。
- **R6** CC BY 4.0，M. W. Toews。上圖看似雜亂的 100 點，下圖自相關找出週期約 10；虛線為 95% 信心帶。
- **R7** CC BY-SA 4.0，Moon motif。左自相關緩慢下降，右偏自相關約 3 個尖峰（模擬自我迴歸階 3）。
- **R8** CC BY-SA 4.0，Dicklyon。自我迴歸階 1（相鄰相關 0.75）400 點樣本，含 95% 信心區間。
- **R9** CC BY-SA 4.0，Dicklyon。同一過程重複抽樣 20 次；整體型態相近、細部隨機波動。
- **R10** CC BY-SA 4.0，Moon motif。模擬自我迴歸階 3 的偏自相關。
- **R11** CC BY-SA 4.0，Anirudh Rao。休倫湖水深的偏自相關。
- **R12** CC0，Markm131。虛構公司 ACME Corp 252 個交易日價格，加上報酬率的自相關與偏自相關；縱軸上限截在 0.35，滯後 0 的棒被截除。來源頁未說明資料出處，僅作版面示意，不做投資判斷。
- **R13** CC BY-SA 4.0，DavidMCEddy。美國實質人均國內生產毛額年成長（1790–2021，取對數後差分）；僅作方法案例，不做經濟或投資判斷。
- **R14** CC BY-SA 4.0，Nettrom。英文維基「待審建立」每月投稿數的偏自相關，滯後 1–24。
- **R15** CC BY-SA 3.0，Junkie.dolphin。每日留存機率的自相關，五個面板 retention(1)、(2)、(5)、(10)、(30)；來源頁未說明括號內數字。
- **R16** CC BY-SA 3.0，Protonk。維基共享資源「文章意見回饋」五項評分（有可靠來源、中立、完整、易讀、整體）平均分數的相關熱圖；兩軸都是變數名稱，顏色越深相關越高，沒有數字與色階。這是 correlogram 的第二種意思，不是時間序列棒圖。
- **R17** CC BY-SA 2.5，Frank Spakowski。時間序列自相關圖（變數 JÜ，滯後 1–4），陰影為依 Bartlett 公式隨滯後變寬的 95% 信心帶。來源頁未載明軟體；圖表下方註記與 Stata 官方手冊 `ac` 預設註記相同，因此**判斷為 Stata 輸出風格**。
- **R18** 公有領域，Leitfaden。三種自相關樣貌示意（義大利文標題）：趨勢型緩慢衰減、季節型固定間隔尖峰、隨機型幾乎全在帶內。
- **R19** 公有領域，Leitfaden。自相關圖用途示意（義大利文標題）：原始序列、序列自相關、去趨勢後殘差自相關、去趨勢與季節後殘差自相關。
- **R20** CC BY-SA 3.0，Jebus989。英文維基管理員資格申請每月成功案件，分 2002–2008 與 2008–2012 兩段；藍色虛線信心界線隨滯後變寬。
- **S1–S8** 自繪模擬，虛構資料，數字未核。亂數種子 20261009；色盤藍 #0072B2／橘 #D55E00／黃 #E69F00。圖檔不入庫。**S7 左圖標題**在素材包圖面上寫「本課的『相關圖／自相關圖』」，正確讀法是自相關圖；照錄不改、沒有重畫。
