# Pattern: recurrence-plot

> **圖種**：遞迴圖（recurrence plot，**暫譯**）
> **來源（專案維護者整理）**：`teach-viz/2026-10-07-am-recurrence.md`（方法教學；第一次以遞迴圖為主題）
> **亦稱**：英文 recurrence plot（RP）；量化側稱遞迴量化分析（recurrence quantification analysis，RQA）。中文別名：遞歸圖、復現圖、重現圖；簡體最常見「递归图」；另見成功大學 2012「逆歸圖示法」、交通大學 2020「回歸圖」——**中文譯名未統一**，本稿寫「遞迴圖（recurrence plot，暫譯）」
> **核心**：把一條時間序列的「每一個時間點」同時排在橫軸與縱軸，第 i 點和第 j 點的狀態若夠接近（距離 ≤ 門檻 ε）就在 (i, j) 塗黑，否則留白；黑白方陣用斜線、方塊、白帶呈現這條序列有沒有週期、哪裡停住、哪裡突然改變
> **一句話**：「什麼時候跟什麼時候很像」——不看數值大小本身，看有沒有回到以前的相近狀態。
> **誠實提醒**：本課是方法教學；模擬圖與本 repo 的練習資料都是虛構，**數字未核**。真實圖讀數凡標「目測」都未核。中英混名要注意：英文 recurrence（回到相近狀態）與 recursion（函式呼叫自己）中文都常稱「遞迴」。
> **潤稿狀態**：素材包寫明課程終稿已經 Liora 審核，**並由 Gemini 潤稿**；素材包文字依終稿手工整理，沒有另外送 Gemini（細節見 ATTRIBUTION）。
> **譯名限定語**：找不到以「遞迴圖」作為正式譯名的臺灣學術論文、政府／大學教材或國家教育研究院詞彙（**無法證實**）；簡體「复现图」也**找不到可靠出處、無法證實**。

## 十二件必須釘清的事

1. **怎麼讀（依序）。** 先確認兩軸都是時間（慣例向右、向上遞增；主對角線從左下到右上，自己跟自己比一定全黑）→ 看大尺度樣貌（均勻散點、平行斜線＝週期、離主對角線越遠越白＝漂移、被白帶切成幾大塊＝突變／中斷）→ 看小尺度（斜線＝相似演化持續；垂直／水平線＝狀態停住；與主對角線垂直的線＝嵌入可能不足）→ 看門檻、嵌入維度、延遲是否寫在圖上 → 需要數字時再看 RQA（遞迴率、決定性、層流性、平均斜線長度等）。
2. **歷史用限定語。** 1987 年 Eckmann、Kamphorst、Ruelle 於《歐洲物理通訊》第 4 卷提出（英文維基寫第 5 卷是錯的）；Marwan 2008 將「遞迴」想法追溯到 Poincaré 1890。原始做法半徑隨點而變、不完全對稱；今日常用固定門檻版才完全對稱。RQA 由 Zbilut 與 Webber 1992 起、1994 擴充，Marwan 等 2002 再延伸。
3. **「斜線很多／決定性高」≠ 證明有規律（S2）。** 隨機漫步決定性可達 79.3%，遠高於白雜訊 25.2%；決定性高只是「有決定性結構」的必要條件，不是充分條件——連自我迴歸過程都能算出決定性 0.6。陷阱頁明確說肉眼「幾乎不可能」判斷動態類型；不能用遞迴圖「證明」混沌。
4. **門檻隨便設，數字完全跟著走（S3、R13、R14）。** 同一序列 ε＝0.05／0.3／1.5，遞迴率從 3.4% 到 65.7%。**「遞迴率 1%–5%」是常見實務建議，但本稿找不到一手來源把它寫成一條固定區間**；約 1% 見於 Marwan 轉述 Zbilut 等 2002。一定要試幾個門檻。
5. **嵌入維度與延遲選錯會造出假結構（S4、R15）。** 維度 1 會把上升段與下降段當成同一狀態而出現交叉線；延遲剛好半週期又回到交叉線；只看決定性可能選錯設定。常見用互資訊選延遲、假近鄰法選維度。
6. **R13 圖說與畫面不符——是論文問題，不是引錯。** 論文圖說 B＝0.144，但畫面像約 50%／0.253；30%／70% 依論文內文。
7. **漂移褪色方向。** 離主對角線越遠越淡（左上角與右下角褪色），不是「右上角」。
8. **交叉遞迴圖（S7、R17）。** 比較兩條序列；**沒有「一定全黑的主對角線」**；斜線偏離多少＝兩條序列錯開多少（S7：真實時間差 10 點，錯開 10 黑格比例 85.5%、錯開 0 只有 11.0%）。
9. **pucicu＝Norbert Marwan。** X 帳號 @pucicu 已確認為 Norbert Marwan（個人檔案網址指向波茨坦氣候影響研究所個人頁）；R1 Commons 作者欄也寫 Norbert Marwan／Pucicu。
10. **非商業授權只連不嵌。** Marwan 的 recurrence-plot.tk（姓名標示－非商業性－禁止改作）與 Marwan 2007 綜述 arXiv 版（姓名標示－非商業性－相同方式分享 4.0；Marwan & Kraemer 2023 arXiv 同樣非商業）——**只放連結、不放圖**；Eckmann 1987 原文 PDF 為出版社版權，只放連結。
11. **缺座標軸、彩虹色階不是標準讀法（R3、R16）。** 先找圖例與軸標；彩虹色難辨識。R16 兩格哪條是哪條未標（未核）；R10「門檻固定在 5%」原文不清（未核）；R19 D 列門檻重複 40 可能筆誤（未核）。
12. **名稱像但不是。** 距離圖／距離矩陣熱圖是未套門檻的彩色版（R8、R16）；龐加萊圖是延遲嵌入相空間的一種投影；熱圖的列欄不一定是時間；自相似矩陣是 1970–80 年代多領域重新發明的同一類矩陣（R4）。

## When

- 一條（或幾條）具備時間順序、間隔固定的數值序列，想知道「有沒有回到以前的狀態」（心跳間隔、馬達振動、腦波、氣候代用指標、姿勢晃動）
- 想一眼看出週期、停滯、突變或漂移；比較兩條序列的同步與時間差（交叉遞迴圖）；比較兩組樣貌再用 RQA 算成數字做統計
- 資料較短、不夠平穩時也能先觀察（但仍要夠長才能算出可靠數字）
- 情境（課程稿）：工廠冷卻水泵浦馬達振動感測器，每秒一筆；想知道平常是否規律、最近有沒有卡住或突然換型態
- **不適合**：沒有時間順序；時間間隔不固定又沒辦法重新取樣；太短（只有幾十點）卻要下結論；想「證明」系統是混沌或非線性；讀者只想知道數值高低或趨勢（直接畫折線圖）

## Recommend

- **主選**：黑白遞迴圖，兩軸都是時間；上方或左邊對齊原始序列；圖上寫明序列長度、門檻 ε、嵌入維度 m、延遲 τ、距離算法與「黑＝遞迴」圖例
- **口述步驟**（素材包第 7 節）：
  1. 確認資料按時間排列、間隔固定；缺失值先決定填補或分段；單位不同則先標準化
  2. 決定要不要延遲嵌入（維度 m、延遲 τ）；常見用互資訊選延遲、假近鄰法選維度
  3. 計算每兩個狀態的距離，得到 N × N 距離表
  4. 選門檻：固定遞迴率、最大距離百分比、或大於雜訊標準差數倍；**一定要試幾個門檻**
  5. 繪製黑白方陣；標明長度、門檻、維度、延遲、距離算法與圖例；上方或左邊對齊原始序列
  6. 需要數值時再做 RQA；比較兩組時固定同一套設定
  7. 比較兩條序列用交叉遞迴圖；要「同時都回到原狀」用聯合遞迴圖
- **工具誠實**：Python 的 pyts、PyRQA；R 的 crqa；Marwan 網站另有工具列表——本 repo 未實測。S 圖由素材包自製腳本畫出（需要 numpy、matplotlib 與 Noto Sans CJK 字型）。
- **圖說建議**：寫清楚兩軸都是時間、門檻、嵌入參數、距離算法、「黑＝遞迴」；比較時寫明同一套設定；真實圖讀數標「目測，未核」；R 圖每張標作者與授權；非商業授權來源只連不嵌
- **參數與判準範例（範例，不是標準）**：

| 項目 | 數值與出處 | 性質 |
|---|---|---|
| 遞迴率實務建議 | 常見建議約 1%–5%，但**找不到一手來源寫成固定區間**；約 1% 見於 Marwan 轉述 Zbilut 等 2002 | 常見建議，不是標準 |
| 模擬門檻 | S1／S3／S5 ε＝0.3；S2／S6 ε＝0.25；S3 另試 0.05／1.5；S8 ε＝0.5 | 範例，不是標準 |
| 嵌入 | S1–S3、S5–S7 用 m＝1；S4 示範 (1,1)／(2,8)／(2,15)；S8 用 m＝2、τ＝1 | 範例，不是標準 |
| 距離 | 歐氏距離（維度 1 時＝差的絕對值）；遞迴＝距離 ≤ ε | 範例，不是標準 |
| 遞迴率定義 | 黑格數 ÷ 全部格數（**含**主對角線）；百分比四捨五入到小數一位 | 本包定義 |
| 模擬長度 | S1–S7 為 300 點；S8 為 8 個讀數 | 範例，不是標準 |

## 與鄰近圖種的區別

本表是素材包的概述，除標明出處者外沒有逐項查證來源。

| 圖種 | 一格（或一點）代表 | 顏色或位置代表 | 和遞迴圖的關係 |
|---|---|---|---|
| 距離圖／距離矩陣熱圖 | 時間 × 時間 | 顏色＝距離（未套門檻） | 套門檻才變黑白遞迴圖（R8、R16） |
| 龐加萊圖（Poincaré plot） | 一個時間點 | 橫＝這一拍、縱＝下一拍 | 延遲嵌入相空間的一種投影；遞迴圖是把「哪些時間點靠很近」攤平成方陣 |
| 頻譜圖（spectrogram） | 時間 × 頻率 | 顏色＝該頻率能量 | 假設週期性震盪並做頻域分解；遞迴圖不需先知道週期，斜線間距會自己告訴你 |
| 一般熱圖（[`matrix-heatmap.md`](matrix-heatmap.md)） | 列 × 欄任一表格 | 顏色＝數值 | 遞迴圖是特殊的時間×時間、二值化熱圖 |
| 千層麵圖（[`lasagna-plot.md`](lasagna-plot.md)） | 個體 × 時間 | 顏色＝該個體該時間的量測值 | 列是個體不是時間；千層麵圖看每人隨時間的值，遞迴圖看一條序列何時回到相近狀態 |
| 鄰接矩陣（[`adjacency-matrix.md`](adjacency-matrix.md)） | 節點 × 節點 | 有沒有連線 | 列與欄是同一批節點，不是時間 |
| 自相關圖 | 一個時間差 | 高度＝相關係數 | S5 右邊「每條斜線黑格比例」很像自相關，但遞迴圖還保留「是哪一段時間在重複」 |
| 折線／時序（[`time-series-trend.md`](time-series-trend.md)） | 一個時間點 | 高度＝數值 | 看數值高低與趨勢；遞迴圖看「像不像以前」 |
| 地平線圖（[`horizon-chart.md`](horizon-chart.md)） | 一條時間序列 | 把折線折疊上色 | 仍是數值隨時間的形狀，不是時間×時間的相似矩陣 |

判斷口訣：**一條等距時間序列、想看何時回到相近狀態 → 遞迴圖；想看數值高低 → 折線；很多人 × 時間的量測值 → 千層麵圖；列欄不是時間 → 一般熱圖或鄰接矩陣**。

## Avoid

- 門檻、嵌入參數不寫在圖上；只試一個門檻（S3）
- 把「決定性高／斜線多」當成規律或混沌的證明（S2）
- 把「遞迴率 1%–5%」寫成有一手來源的固定標準
- 把漂移褪色記成「右上角」；把交叉遞迴圖當成一定有全黑主對角線
- 缺座標軸、用彩虹色階卻當標準讀法（R16）
- 把 R13 圖說 0.144 當畫面讀數（論文問題）
- 嵌入維度／延遲不檢查就下結論（S4）
- 嵌入或轉載 recurrence-plot.tk、Marwan 2007／2023 arXiv 非商業授權圖
- 寫「某人發明了遞迴圖」或把中文譯名當成已統一，而不加限定語
- 把 X 貼文當教學依據（只作連結）

## Produce checklist

- [ ] 確認資料等距、有時間順序；先標準化（單位不同時）
- [ ] 選（或明確寫「不嵌入」）維度 m 與延遲 τ；試幾個門檻 ε
- [ ] 黑白方陣；圖例「黑＝遞迴」；標長度、ε、m、τ、距離算法
- [ ] 上方或左邊對齊原始序列；比較時固定同一套設定
- [ ] 需要數字再算 RQA；交叉／聯合遞迴圖用途分清
- [ ] 歷史與譯名用限定語（暫譯；1%–5% 非一手固定區間；不能證明混沌）
- [ ] 非商業授權來源只連不嵌；R 圖標作者與授權；模擬圖標「模擬」、數字虛構

## 虛構 demo 資料

素材包沒有指定哪一份給 repo → **8 組全部收錄**（`sample-recurrence-s1-anatomy` … `sample-recurrence-s8-steps`，各 CSV＋selfcheck，共 16 檔）。檔名已有 `recurrence` 前綴，與 `examples/data/` 既有檔**無撞名**，內容與素材包 `cmp` 逐位元相同。每支 selfcheck 以明確檔名讀 CSV（`read_rows("sample-recurrence-sN-….csv")`，從腳本所在資料夾讀，無 glob），只用 Python 標準函式庫；我在 `examples/data/` 與暫存資料夾各跑一次，全部 PASS。

獨立重算（pandas／numpy，歐氏距離、含主對角線的遞迴率）與素材包、selfcheck 一致：S1 第 70／119 點 0.45／0.62、距離 0.17、遞迴率 18.8%；S2 四面板 14.1%／17.0%／14.1%／21.2%（隨機漫步決定性 79.3%、白雜訊 25.2%）；S3 ε＝0.05／0.3／1.5 → 3.4%／18.8%／65.7%；S4 (m,τ)＝(1,1)／(2,8)／(2,15) 狀態數 300／292／285、遞迴率 19.4%／5.3%／11.3%；S5 遞迴率 18.6%，斜線高峰 50／100／150 黑格比例 85.2%／83.0%／84.0%；S6 卡住 50 點，正常／卡住 14.3%／16.6%；S7 交叉遞迴率 19.0%，錯開 10 點 85.5%、錯開 0 點 11.0%；S8 平均 13.50、標準差 1.50、7 狀態、13 黑／49 格＝26.5%。**沒有發現素材包文字與 CSV 不一致。**

素材包 `draw_recurrence.py` 從暫存資料夾以 `--outdir /tmp` 重跑，8 張模擬圖與素材包逐位元相同，`export_samples.py` 匯出的 8 個 CSV 也相同；素材包 27 張圖與 `teach-viz/` 同名檔全部相同。圖檔與腳本都**沒有收進本 repo**。

## 參考連結

只連 `sources.txt` 標「可開」的網址（71 條全部連結，含 22 則 X 貼文）。打不開 0 條。以下 2 條**只記名、標未核、不連結**（網站拒絕自動連線；素材包另以 Crossref／語意學者或搜尋摘要確認存在，但不當主要依據）：

- **無法確認（2，未核）：** Fraser & Swinney 1986《物理評論 A》數位物件識別碼頁；百度百科〈递归图〉。

**歷史、方法與定義**

- [Eckmann、Kamphorst、Ruelle 1987 原文全文（可攜式文件格式 PDF，放在 Eckmann 於日內瓦大學的個人網頁）](https://fiteoweb.unige.ch/~eckmannj/ps_files/recurrenceplots.pdf)
- [Eckmann 等 1987 出版社數位物件識別碼（DOI）頁](https://doi.org/10.1209/0295-5075/4/9/004)
- [Marwan 的遞迴圖網站首頁（recurrence-plot.tk）](https://www.recurrence-plot.tk/)
- [同站〈遞迴圖一覽〉：大尺度樣貌與小尺度結構](https://www.recurrence-plot.tk/glance.php)
- [同站〈遞迴量化分析〉各項指標定義](https://www.recurrence-plot.tk/rqa.php)
- [同站〈如何避開遞迴圖分析的陷阱〉](https://www.recurrence-plot.tk/pitfalls.php)
- [同站〈遞迴圖的各種變體〉](https://www.recurrence-plot.tk/variations.php)
- [Marwan 網站〈交叉遞迴圖〉頁（crps.php）](https://www.recurrence-plot.tk/crps.php)
- [Marwan、Romano、Thiel、Kurths 2007 綜述〈Recurrence Plots for the Analysis of Complex Systems〉arXiv 版](https://arxiv.org/abs/2501.13933)
- [同上綜述《物理報告》（Physics Reports）438:237–329 數位物件識別碼頁](https://doi.org/10.1016/j.physrep.2006.11.001)
- [Marwan 2008〈遞迴圖歷史回顧〉arXiv 版（圖 R5、R6 來源）](https://arxiv.org/abs/1709.09971)
- [同上《歐洲物理期刊特刊》164:3–12 數位物件識別碼頁](https://doi.org/10.1140/epjst/e2008-00829-1)
- [Marwan & Kraemer 2023〈動態系統遞迴分析的趨勢〉arXiv 版](https://arxiv.org/abs/2409.04110)
- [同上《歐洲物理期刊特刊》232:5–27 數位物件識別碼頁](https://doi.org/10.1140/epjs/s11734-022-00739-8)
- [Marwan 2011〈如何避開遞迴圖資料分析的潛在陷阱〉《國際分岔與混沌期刊》21(4):1003–1017](https://doi.org/10.1142/S0218127411029008)
- [Zbilut & Webber 1992《物理快報 A》171:199–203（遞迴量化分析起點）](https://doi.org/10.1016/0375-9601(92)90426-M)
- [Webber & Zbilut 1994《應用生理學期刊》76:965–973](https://doi.org/10.1152/jappl.1994.76.2.965)
- [Trulla、Giuliani、Zbilut、Webber 1996《物理快報 A》223:255–260](https://doi.org/10.1016/S0375-9601(96)00741-4)
- [Marwan & Kurths 2002 交叉遞迴圖《物理快報 A》302:299–307](https://doi.org/10.1016/S0375-9601(02)01170-2)
- [Romano、Thiel、Kurths、von Bloh 2004〈多變量遞迴圖〉《物理快報 A》330:214–223（聯合遞迴圖）](https://doi.org/10.1016/j.physleta.2004.07.066)
- [Takens 1981〈偵測亂流中的奇異吸子〉（延遲嵌入定理）](https://doi.org/10.1007/BFb0091924)
- [英文維基百科〈Recurrence plot〉](https://en.wikipedia.org/wiki/Recurrence_plot)
- [英文維基百科〈Recurrence quantification analysis〉](https://en.wikipedia.org/wiki/Recurrence_quantification_analysis)
- [日文維基百科〈リカレンスプロット〉](https://ja.wikipedia.org/wiki/リカレンスプロット)
- [德文維基百科〈Rekurrenzplot〉](https://de.wikipedia.org/wiki/Rekurrenzplot)
- [中文維基百科〈混沌理論〉臺灣正體頁（寫「遞迴圖」）](https://zh.wikipedia.org/zh-tw/混沌理论)

**簡體中文與工具**

- [《物理學報》2014〈癫痫脑电自动检测方法〉（簡體用「递归图」）](https://wulixb.iphy.ac.cn/cn/article/pdf/preview/10.7498/aps.63.050506.pdf)
- [《西安交通大學學報》2017〈人体步态复杂度的递归图和递归定量分析研究〉](https://zkxb.xjtu.edu.cn/zh/article/doi/10.7652/xjtuxb201710008/)
- [數學天地網〈重现图〉（MathWorld 中文翻譯站）](https://mathworld.net.cn/RecurrencePlot.html)
- [Python 套件 pyts 的 RecurrencePlot 說明頁](https://pyts.readthedocs.io/en/stable/generated/pyts.image.RecurrencePlot.html)
- [Python 套件 PyRQA（PyPI 頁）](https://pypi.org/project/PyRQA/)
- [R 套件 crqa（CRAN 頁）](https://cran.r-project.org/package=crqa)

**R 圖來源（Commons、PMC）**

- [圖 R1 來源：維基共享資源 Rp examples740.gif](https://commons.wikimedia.org/wiki/File:Rp_examples740.gif)
- [圖 R2 來源：維基共享資源 Rp soi.gif](https://commons.wikimedia.org/wiki/File:Rp_soi.gif)
- [圖 R3 來源：維基共享資源（數學產生的混沌序列）](https://commons.wikimedia.org/wiki/File:Recurrence_plot_of_mathematicaly_generated_chaos.jpg)
- [圖 R4 來源：維基共享資源 Junejoetal ssm eccv08.jpg](https://commons.wikimedia.org/wiki/File:Junejoetal_ssm_eccv08.jpg)
- [R7 來源：Dimitriev 等 2020 心算壓力心跳間隔（PMC7026015）](https://pmc.ncbi.nlm.nih.gov/articles/PMC7026015/)
- [R8 來源：Mathunjwa 等 2022 心電圖心律不整（PMC8877903）](https://pmc.ncbi.nlm.nih.gov/articles/PMC8877903/)
- [R9 來源：Zhao 等 2019 胎兒心率（PMC6422985）](https://pmc.ncbi.nlm.nih.gov/articles/PMC6422985/)
- [R10 來源：Kobel 等 2023 姿勢晃動（PMC10415033）](https://pmc.ncbi.nlm.nih.gov/articles/PMC10415033/)
- [R11 來源：Rousseau 等 2023 石筍氧同位素（PMC10739820）](https://pmc.ncbi.nlm.nih.gov/articles/PMC10739820/)
- [Kecik 等](https://pmc.ncbi.nlm.nih.gov/articles/PMC9457464/)
- [Petrauskiene 等](https://pmc.ncbi.nlm.nih.gov/articles/PMC9693566/)
- [R14 來源：Großekathöfer 等 2017 自閉症三門檻（PMC5311048）](https://pmc.ncbi.nlm.nih.gov/articles/PMC5311048/)
- [R15 來源：He 等 2025 渦激振動延遲（PMC12527018）](https://pmc.ncbi.nlm.nih.gov/articles/PMC12527018/)
- [圖 R16 來源：Inglada-Perez 2020（PMC7767038）](https://pmc.ncbi.nlm.nih.gov/articles/PMC7767038/)
- [R17 來源：Scheer 等 2025 交叉遞迴圖雙人同步（PMC12543173）](https://pmc.ncbi.nlm.nih.gov/articles/PMC12543173/)
- [圖 R18 來源：Zaitouny 等 2022（PMC9032846）](https://pmc.ncbi.nlm.nih.gov/articles/PMC9032846/)
- [圖 R19 來源：Zheng 等 2024（PMC11202180）](https://pmc.ncbi.nlm.nih.gov/articles/PMC11202180/)

**連結統計：** sources.txt 73 個網址（去重；檔案共 79 行，另有 6 行 `#` 說明）＝可開 71＋打不開 0＋無法確認 2。可開 71 條全部連結（其中 X 貼文 22 條）；2 條只記名未核。

### X 貼文（只作連結，不當教學依據）

以 X 官方搜尋再以官方貼文讀取逐則讀回 **22 則，全部英文**；**中文、日文談時間序列遞迴圖的原始貼文 0 筆**。數字一律未核，僅轉載。@pucicu 已確認為 Norbert Marwan。

1. [@QFinancePapers](https://x.com/QFinancePapers/status/96389070258831361)
2. [@LeeCarlsonMath](https://x.com/LeeCarlsonMath/status/96542132852105217)
3. [@antmandan](https://x.com/antmandan/status/211587714875785216)
4. [@UCCAPCenter](https://x.com/UCCAPCenter/status/269138674397089792)
5. [@fusaroli](https://x.com/fusaroli/status/621351758560907264)
6. [@pucicu](https://x.com/pucicu/status/640849298058559488)
7. [@ASHAJournals](https://x.com/ASHAJournals/status/805774480362573824)
8. [@FranciscoICMC](https://x.com/FranciscoICMC/status/817036973009489921)
9. [@AIP_Publishing](https://x.com/AIP_Publishing/status/836705110331912192)
10. [@FrontPsychol](https://x.com/FrontPsychol/status/1069815573494681600)
11. [@recurrenceplot](https://x.com/recurrenceplot/status/1080501352890056704)
12. [@AndrejSpiridon4](https://x.com/AndrejSpiridon4/status/1394605279153737735)
13. [@matej__v](https://x.com/matej__v/status/1399307406719455239)
14. [@EricLeonardis](https://x.com/EricLeonardis/status/1457644158026280960)
15. [@karlbooklover](https://x.com/karlbooklover/status/1525899707180060673)
16. [@pucicu](https://x.com/pucicu/status/1613940255773671425)
17. [@AmSocBiomech](https://x.com/AmSocBiomech/status/1820539802359640470)
18. [@SignalPapers](https://x.com/SignalPapers/status/1897586723690787130)
19. [@predict_addict](https://x.com/predict_addict/status/1946238601617944970)
20. [@ninadaithal](https://x.com/ninadaithal/status/2001238825876775367)
21. [@AndrejSpiridon4](https://x.com/AndrejSpiridon4/status/2072558094828105739)
22. [@FrontPhysiol](https://x.com/FrontPhysiol/status/2100187627437899798)

鄰居 pattern：`matrix-heatmap.md`（一般熱圖；遞迴圖是時間×時間的二值化特例）、`lasagna-plot.md`（列＝個體、欄＝時間的量測色帶；遞迴圖兩軸都是時間）、`adjacency-matrix.md`（列欄是節點不是時間）、`time-series-trend.md`（看數值高低與趨勢；遞迴圖看「像不像以前」）、`horizon-chart.md`（折疊折線看多條序列形狀）。

## 圖檔與授權（不複製，只連結）

27 張＝真實／示意圖 R1–R19＋自繪模擬 S1–S8（虛構資料，數字未核）。**本 repo 不散佈圖檔，只連到來源頁；引用時保留作者與授權。**

- **R1–R4（Commons）：** R1 四種典型樣貌，CC BY-SA 3.0，Norbert Marwan／Pucicu；R2 南方振盪指數，CC BY-SA 3.0（機器可讀作者欄空白，檔案頁描述為 Norbert Marwan，未核）；R3 數學產生的混沌序列，公有領域，Lakinekaki；R4 高爾夫揮杆自相似矩陣，CC BY-SA 3.0，Ijunejo。我用 Commons API（2026-10-07，台北）查到 R1 CC BY-SA 3.0／Norbert Marwan／Pucicu／2006-10-10、R2 CC BY-SA 3.0、R3 Public domain／Lakinekaki、R4 CC BY-SA 3.0／Ijunejo／2008-10，與素材包相符。
- **R5、R6：** Marwan 2008 arXiv（1709.09971），創用 CC 姓名標示 4.0。
- **R7–R19：** PubMed Central，素材包標創用 CC 姓名標示 4.0。我另以 Europe PMC REST API（2026-10-07，台北）查 R7–R19 的 13 篇來源論文：`license` 欄位全部是「cc by」（API 不給版本號，「4.0」依素材包）。
- **只放連結、不轉存（非商業／版權）：** recurrence-plot.tk（姓名標示－非商業性－禁止改作）；Marwan 2007 綜述 arXiv 版與 Marwan & Kraemer 2023 arXiv 版（非商業）；Eckmann 1987 原文 PDF（出版社版權）。
- **R13 是論文圖說與畫面不符的實例**（圖說 B＝0.144，畫面像約 50%／0.253），不是引錯；使用時保留這個標示。
