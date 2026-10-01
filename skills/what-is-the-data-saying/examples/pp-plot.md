# Pattern: pp-plot

> **圖種**：P–P 圖（P–P plot；機率—機率圖，Probability–Probability plot）
> **來源（納茲教圖）**：`teach-viz/2026-10-01-pm-pp.md`（方法教學；正式課程）
> **亦稱**：英文維基百科條目首句還寫了 percent–percent plot 與 P value plot 兩個別名（"probability–probability plot or percent–percent plot or P value plot"）；「P value plot」要小心，見第 4 項
> **核心**：把兩個累積分布函數（CDF，指「數值小於等於某個值的機率」）對在一起看；可以是樣本對理論分布，也可以是樣本對樣本。**每個點的兩個座標都是 0 到 1 的累積機率**，點落在邊長為 1 的正方形裡；貼近 (0,0) 到 (1,1) 的對角線，表示兩邊的累積機率相近。
> **一句話**：同一個**數值**上，兩邊的累積機率像不像；不是 QQ 圖（同一個累積機率上，兩邊的數值像不像）。
> **對角線的說法**：英文維基百科寫母體的兩個分布相同才會落在線上，但同頁也提醒 "even samples drawn from identical distributions will not appear identical"，所以樣本只能說「大致貼線」，不能說「落在線上就相同」。

## 七件必須釘清的事

1. **P–P 是機率對機率（兩軸 0 到 1），QQ 是分位數對分位數（兩軸是數值）。** 敏感位置的差別是**定性說法，不是定理**：GeostatsGuy、reliability 文件、SAS 說明三份來源都寫 P–P 在分布中央（機率密度高處）鑑別力較好、QQ 在尾部較好；英文維基百科 P–P 條目本身**沒有**寫這一點。尾部差異在 P–P 圖上是「被壓縮、不顯眼」，**不是「看不到」**；P–P 圖兩端被迫收在 (0,0) 與 (1,1)（GeostatsGuy："low and upper tails are forced to be 0.0, 0.0 and 1.0, 1.0"）。講尾巴請並陳 QQ 圖。
2. **各來源對「哪個變數放哪個軸」不一致，圖題一定要寫。** 多數來源是橫軸理論、縱軸樣本（SAS、Statistica、Triveri、Commons 示例圖）；reliability 的半參數圖橫軸是經驗 CDF、縱軸是擬合分布；GeostatsGuy 是 X1 橫軸、X2 縱軸；Kass 講義文中沒明寫。**statsmodels 0.15.0 的 `ppplot` 軸標字面（橫軸 "Theoretical Probabilities"、縱軸 "Sample Probabilities"）與實際放的內容相反**：依原始碼與實際繪出的圖，橫軸放的是繪圖位置（預設 i/(n+1)），縱軸放的是理論分布在排序資料上的 CDF 值；傳入 `other` 時，縱軸是另一組資料的經驗累積機率，卻標成 "Probabilities of 1st Sample"，標籤與內容也不一致。素材包的 statsmodels 圖已依實際計算改正軸標。（本 repo 另在暫存虛擬環境安裝 statsmodels 0.15.0，對 `sample-pp-fictional.csv` 的 `sm` 資料集實際呼叫 `ProbPlot(...,fit=True).ppplot()` 驗證：軸標確為 "Theoretical Probabilities"（橫）與 "Sample Probabilities"（縱），但畫出的橫座標等於 i/(n+1)、縱座標等於擬合常態在排序值的 CDF，與軸標字面相反，和納茲稿一致。）換軸會讓曲線對對角線鏡射，「點在線上方」的意思反過來。本 repo 慣例：**橫軸＝參考（理論）累積機率，縱軸＝比較（樣本）累積機率**；照此寫法，點在線上方表示樣本在該數值的累積機率比參考分布高，也就是樣本偏小。
3. **NIST「Probability Plot」與 SciPy `probplot` 的軸是數值，屬 QQ 類，不是 P–P 圖。** NIST 縱軸有序觀測值、橫軸理論次序統計量中位數，頁面完全沒提 P–P 圖（「不是 P–P」是依軸語意的判斷）；SciPy 文件明寫 "should not be confused with a Q-Q or a P-P plot"。NIST QQ 頁把 quantile 解釋成「低於某值的比例」、Dataplot 頁寫 percentiles，用字容易讀成 P–P，但實際畫的軸仍是數值。**來源自己也會混名：Kass 講義圖 5 的說明文字寫 P–P，圖內標題卻寫 "QQ Plot for Front Average"**（教學稿以兩種解析度判讀一致，未用文字辨識軟體複核）。
4. **「P value plot」是 P–P 結構，不是曼哈頓圖。** Davidson 與 MacKinnon（1998，*The Manchester School* 66 卷 1 期，第 1 到 26 頁）把模擬得到的 p 值的經驗分布對名目水準畫圖，稱 "P value plot"，檢定表現正確時應貼近 45° 線——結構上等同「p 值分布對均勻分布」的 P–P 圖（這個對應是推論）。它不是把 p 值逐點畫成天際線的曼哈頓圖。
5. **繪點位置（經驗累積機率的算法）各來源不同，圖註要寫你用哪一種**：i/n（SAS 說明、Triveri 範例）、(i−0.5)/n（Kass 的變體）、i/(n+1)（Kass、英文維基百科、statsmodels 預設；statsmodels 可用參數 a 調成 (i−a)/(n+1−2a)）。**畫面不是正方形、軸超出 0 到 1，對角線在螢幕上就不是 45°**（Commons 示例圖軸範圍超出 0 到 1，紅線約 29°），務必等軸比例。
6. **授權**：GeostatsGuy 教材倉庫為 **CC BY-NC-ND 4.0（不可商用、不可改作）**；reliability 套件為 **LGPL 3.0**；Commons 上的品質特性資料 P–P 圖（作者 Jchem00，2012-04-18）為 **CC0 1.0**；NIST 網頁資訊屬公開資訊，網站請求標明出處；**其餘單張圖檔授權未逐檔確認，僅作教學示意引用，不可當作可自由再用**；標「模擬資料」者為自製。本 repo 不複製任何圖，詳見 `ATTRIBUTION.md`。
7. **素材包的潤稿流程說明**：素材包原定的 Gemini 潤稿步驟**沒有執行**（登入過期），文字是審稿後的原稿；已在 `ATTRIBUTION.md` 註明。

## When

- 分布適配的圖形輔助：一批資料的累積形狀像不像某個**已完全指定**的參考分布（可加接受區間帶）
- 兩批**位置相近**的樣本，比較在共用數值上的累積機率
- 迴歸殘差是否大致符合假定的誤差分布（殘差診斷以 QQ 圖較常見，P–P 圖作補充）
- 可靠度與壽命資料：資料對擬合分布（reliability 文件："Fully parametric PP plots are rarely used"，兩個參數分布的 CDF 對照較少用）
- 教學：說明「中央不合」與「尾巴不合」為何要同時看 P–P 圖與 QQ 圖

## Recommend

- **主選（樣本對理論）**：橫軸＝理論 CDF 在排序值（可先標準化）的值，縱軸＝繪點位置，加 (0,0) 到 (1,1) 對角線，等軸比例；**圖註寫：理論分布名稱與參數如何得到、繪點公式、樣本數 n、哪個軸放誰**
- **資料前提**：至少一組可排序的數量（只有類別標籤不能畫）；樣本對理論時理論 CDF 必須完全指定（位置、尺度、形狀，或寫明由資料估計；Statistica："the theoretical distribution function must be completely specified"）；兩樣本法則要在一串共用數值上讀兩邊的經驗累積機率
- **變體**：
  - **兩樣本 P–P**：z 取兩批合併後的排序值，橫軸為 A 的經驗 CDF、縱軸為 B 的經驗 CDF（不用 (i−0.5)/n）；兩批位置要相近
  - **參數／半參數 P–P**（reliability 的 `PP_plot_parametric`、`PP_plot_semiparametric`）：圖題寫清是「參數對參數」還是「資料對擬合」；半參數版橫軸是經驗 CDF，與多數來源相反
  - **迴歸殘差 P–P**：圖題寫「殘差」，不要說成「原始反應變數一定常態」
  - **穩定化 P–P 圖（SP 或 S–P 圖）**：英文維基百科寫它用變異數穩定化變換，使各處偏離對角線的波動大小一致（Michael 1983，*Biometrika*；原文未開，只讀維基百科的引用資訊）；進階變體，本 pattern 不展開
- **參數與判準範例（範例，不是標準）**：

| 項目 | 數值與出處 | 性質 |
|---|---|---|
| 繪點位置 | i／n（SAS、Triveri）、(i−0.5)／n（Kass 變體）、i／(n+1)（Kass、維基百科、statsmodels 預設）；本 repo 模擬圖多用 (i−0.5)／n，兩樣本圖用經驗 CDF，statsmodels 圖用 i／(n+1) | 範例，不是標準 |
| 接受區間帶 | Kass 講義：以 Kolmogorov–Smirnov 檢定統計量的漸近分布做約 95% 機率帶，位置 (r−0.5)／n ± 1.36／√n；1.36 與 KS 檢定在 0.05 的漸近臨界值相符（教學稿以 SciPy 重算得 1.358） | 範例，不是標準 |
| 對角線的判讀 | 貼線＝兩邊累積機率相近；通過 (0.5, 0.5)＝兩邊中位數相同（維基百科）；S 形＝資料可能需要轉換（Statistica）；貼邊走＝位置差太遠、幾乎不重疊（維基百科） | 範例，不是標準 |
| 本 repo 練習資料的「貼線」數字 | 近似常態 n＝100 時最大垂直距離 0.068（小於 0.07）；殘差 n＝80 時 0.097（小於 0.1）——只是虛構資料的實測值，不是判準 | 範例，不是標準 |

- **備選（何時改用哪一種）**：
  - 要講尾部離群、厚尾多誇張、分位數數值差多少 → [QQ 圖](qq-plot.md)
  - 兩分布位置差極遠、幾乎不重疊 → 先對齊位置（P–P 圖會變貼邊折線）
  - 理論分布參數未指定 → 先估計，或先用 QQ 圖協助定參數
  - 兩種量測方法的一致性 → [Bland–Altman 圖](bland-altman.md)
  - 豐度對倍數 → [MA 圖](ma-plot.md)；倍數對顯著性 → [火山圖](volcano-plot.md)；基因組位置對 −log10(p) → [曼哈頓圖](manhattan-plot.md)或 [LocusZoom 圖](locuszoom.md)
  - 只是比較任意兩欄 → [一般散點圖](correlation-scatter.md)

## 與鄰近圖種的區別

| 圖種 | 橫軸 | 縱軸 | 回答的問題 | 和 P–P 圖的區別 |
|---|---|---|---|---|
| **QQ 圖**（`qq-plot.md`） | 理論（或樣本 A）的分位數，單位是數值 | 樣本（或樣本 B）的分位數，單位是數值 | 同一個累積機率上，兩邊的數值像不像 | 軸是數值；位置與尺度改變時仍保持直線（SAS 說明）；尾部較敏感（定性說法）；P–P 不保持位置與尺度 |
| NIST「Probability Plot」 | 理論次序統計量中位數（數值） | 有序觀測值（數值） | 資料像不像某個分布 | 兩軸都是數值，屬 QQ 或常態機率圖一類，**不是 P–P 圖**，不要混名 |
| SciPy `probplot` | 理論分位數 | 有序資料 | 同上 | 文件明說不要與 Q-Q 或 P-P 圖混淆 |
| **Bland–Altman 圖**（`bland-altman.md`） | 兩方法平均值 | 兩方法差值 | 兩種量測方法的一致性 | 不是累積機率 |
| **曼哈頓圖**（`manhattan-plot.md`）／**LocusZoom 圖**（`locuszoom.md`） | 基因組位置 | −log10(p) | 訊號落在哪裡 | 不是累積機率；「P value plot」是 P–P 結構，不是曼哈頓圖 |
| **一般散點圖**（`correlation-scatter.md`） | 任意數量 | 任意數量 | 兩個變數的關係 | 本圖的軸固定為兩個累積機率（0 到 1） |
| 穩定化 P–P 圖（repo 尚無專檔） | 同 P–P | 同 P–P（變異數穩定化） | 各處偏離波動大小一致 | 同家族進階變體，本 pattern 不改題 |

判斷口訣：**同一個數值上比累積機率 → P–P 圖；同一個累積機率上比數值 → QQ 圖；軸是數值的「Probability Plot」→ 不是 P–P 圖。**

## Avoid

- 不寫哪個軸放誰（各來源不一致，換軸會鏡射、「線上方」意思反過來）
- 照 statsmodels `ppplot` 的軸標字面讀圖
- 位置或尺度沒對齊就畫（P–P 不保持位置與尺度；樣本整體偏大時，點整片落在對角線一側、不通過 (0.5, 0.5)）
- 只靠 P–P 圖下「尾部沒問題」的結論（兩端被迫收在 (0,0) 與 (1,1)）；把「看不到尾部」說成事實（正確說法是「被壓縮、不顯眼」）
- 把「大致貼線」說成「相同」；以圖形適配取代正式的適配度檢定
- 畫面不是正方形、軸超出 0 到 1（對角線不是 45°）；繪點公式不寫
- 把 NIST「Probability Plot」或 SciPy `probplot` 叫成 P–P 圖；把 P–P 與 QQ 當同一種圖
- 兩樣本位置差太遠還硬畫（曲線貼邊走，資訊量很低）
- 把「P value plot」當成曼哈頓圖
- 把模擬圖當成真實證據；把授權未明示、CC BY-NC-ND 或 LGPL 的外部圖當可自由再用
- 把敏感位置的差別寫成定理

## Produce checklist

- [ ] 故事句是「這批數的累積形狀像不像參考分布／兩批在共用數值上的累積機率像不像」；先說清楚比較對象（樣本對理論，或樣本 A 對樣本 B）
- [ ] 整理資料：去掉或標註缺值；確認是可排序的連續（或近似連續）數量；記 n
- [ ] （樣本對理論）指定或估計參數並寫進圖題；參數不完整就不要硬叫「對該分布的 P–P 圖」
- [ ] 排序並算經驗累積（繪點位置），**圖註寫公式**
- [ ] 算參考側累積機率（代入理論 CDF；兩樣本法則改為在共用數值 z 上讀兩邊的經驗 CDF）
- [ ] 畫在邊長為 1 的正方形：兩軸 0 到 1、對角線 (0,0)–(1,1)、**等軸比例**；**哪個軸放誰寫進圖題**
- [ ] 解讀順序：是否貼線 → 彎曲落在哪一段機率 → 是否過 (0.5, 0.5) → 是否貼邊（位置差太遠）→ 再決定要不要並陳 QQ 圖看尾巴
- [ ] 要講尾巴、離群、分位數數值差 → 並陳 QQ 圖；兩張不要互相冒名
- [ ] 工具誠實（只寫素材包證實的；版本為 2026-10-01 查核值）：
  - **statsmodels**（Python，0.15.0）：`ProbPlot.ppplot`（與 `qqplot`、`probplot` 同一個物件）；文件頁的示例圖只有 Q–Q 與 `probplot`，**沒有任何 P–P 示例圖**；軸標與實際內容相反（見第 2 項）；程式為修改版 BSD 授權
  - **reliability**（Python，文件版本 0.9.0）：`PP_plot_parametric`、`PP_plot_semiparametric`；套件 LGPL 3.0；半參數版橫軸是經驗 CDF；文件寫 "If the fitted distribution is a good fit the PP plot will follow the 45 degree diagonal line"
  - **TIBCO Statistica**（14.2.0 說明頁）：觀測 CDF 對理論 CDF，理論參數必須完整指定
  - **SAS**（說明頁）：P–P 在機率密度高的區域較有鑑別力；位置或尺度改變，P–P 的線性不會保持
  - **James Triveri 教學文**（Python／SciPy）：理論百分位在橫軸、經驗百分位在縱軸；範例用 i／n 並先標準化；頁內嵌圖素材包未存檔，未核
  - **GeostatsGuy 教材**（Python）：兩批樣本 P–P；教材 CC BY-NC-ND 4.0
  - **Matplotlib、numpy、scipy**：素材包模擬圖用；授權素材包未寫（statsmodels 以外），不代填
  - data-to-viz、R Graph Gallery、Dataviz Project 的 QQ 專頁查無（404），Python Graph Gallery 首頁可開但沒有 P–P 專頁——不是來源
- [ ] 示範數字標「數字未核」；圖形適配不能代替正式的適配度檢定（reliability 文件：圖形結果常常難以分辨，所以才用量化的適配指標）
- [ ] 自檢：軸寫了誰放哪嗎？繪點公式寫了嗎？等軸嗎？有沒有把 NIST／probplot 叫成 P–P？尾巴的結論有並陳 QQ 圖嗎？

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-pp-fictional.csv` — 1,000 列（約 30 KB）；檔頭三行以 `#` 開頭，讀取要略過（pandas 用 `comment='#'`）；欄位 `row_id, dataset, group, obs_index, value, value2`。`dataset`＝`anatomy`（座標系解剖，n＝20，標準常態）、`good`（近似常態，n＝100，平均 50、標準差 10）、`heavy`（厚尾，n＝200，t 分布自由度 2）、`loc`（位置未對齊，n＝100，平均 1.3）、`skew`（右偏，n＝200，對數常態）、`two`（兩樣本，`group` 為 A 或 B，各 n＝100）、`resid`（迴歸殘差用，n＝80，`value`＝x、`value2`＝y）、`sm`（statsmodels 示例，n＝100，gamma 形狀 6）；`obs_index` 是該資料集內的原始抽樣順序（尚未排序）。
- 我重新計算的數字（**以實際計數為準**；與素材包檢查輸出逐項一致，素材包文字與 CSV 沒有發現不一致）：
  - 全檔 1,000 列：anatomy 20、good 100、heavy 200、loc 100、skew 200、two 200（A、B 各 100）、resid 80、sm 100
  - `anatomy`：第 14 個排序值 z＝0.69，橫座標 Φ(z)＝0.754，縱座標 (14−0.5)/20＝0.675；20 點到對角線的最大垂直距離 0.102
  - `good`：樣本平均 49.4、標準差 11.1；標準化後最大垂直距離 0.068
  - `heavy`：樣本標準差約 2.46（t 分布自由度 2 變異數無限大，不穩定）；標準化後，橫軸 [0.05, 0.45) 的 81 點全在對角線下方、[0.55, 0.95) 的 66 點全在上方；**不標準化**直接代入標準常態 CDF 時方向相反：橫軸小於 0.5 的 105 點中 104 點在線上方、大於 0.5 的 95 點中 88 點在線下方（所以標準化與否要寫在圖註）
  - `loc`：樣本平均 1.45；100 點全在對角線下方；橫軸 0.5 處縱軸約 0.08，沒有通過 (0.5, 0.5)
  - `skew`：橫軸 [0.3, 0.85) 的 111 點全在對角線上方；最大垂直距離 0.171（橫軸 0.43 處）；QQ 圖最右邊的點標準化值 6.19，對應理論分位數只有 2.81
  - `two`：平均數 A −0.01、B 0.03；標準差 A 1.18、B 1.88；橫軸小於 0.4 的 79 點全在線上方；橫軸大於 0.6 的 82 點中 81 點在線下方、1 點剛好在線上；橫軸 0.5 處縱軸約 0.52
  - `resid`：配出的直線 y＝3.19＋0.73x；殘差標準差 1.05；最大垂直距離 0.097
  - `sm`：擬合常態平均 6.29、標準差 2.95；橫軸 [0.45, 0.85) 的 40 點全在對角線下方；最大垂直距離 0.125
  - 提醒：上列「全在線上方／下方」的點數是**指定橫軸區間內**的點，不是整批資料（例如 `heavy` 的 200 點只數了其中 147 點；`skew` 全批 127 點在線上方、73 點在線下方）
- 示範讀法：橫軸理論 CDF、縱軸 (i−0.5)/n，畫對角線與等軸；`good` 貼線，`heavy` 標準化後呈 S 形（但厚尾的差異要在 QQ 圖上看），`loc` 整片落在線下方，`skew` 中段高於線，`two` 呈 S 形（B 較分散）。
- `sample-pp-selfcheck.py` — 自檢腳本（需 numpy 與 scipy；**以絕對路徑讀同資料夾的指定檔名，不搜尋檔案**，並以 `assert` 檢查所有點數與百分比；見 `examples/data/README.md`）。

## 參考連結（可點；皆出自素材包 sources.txt 且標可開）

- 條目與通稱：https://en.wikipedia.org/wiki/P%E2%80%93P_plot 、https://en.wikipedia.org/wiki/Q%E2%80%93Q_plot 、https://en.wikipedia.org/wiki/Probability_plot
- 圖片頁（作者與授權）：https://commons.wikimedia.org/wiki/File:Probability-Probability_plot,_quality_characteristic_data.png （CC0 1.0）；圖庫分類 https://commons.wikimedia.org/wiki/Category:Probability_plots
- 教材與文件：https://geostatsguy.github.io/GeostatsPyDemos_Book/GeostatsPy_QQ.html （授權檔 https://raw.githubusercontent.com/GeostatsGuy/GeostatsPyDemos_Book/main/LICENSE ）；https://reliability.readthedocs.io/en/stable/Probability-Probability%20plots.html （授權檔 https://raw.githubusercontent.com/MatthewReid854/reliability/master/LICENSE ）；https://www.statsmodels.org/stable/generated/statsmodels.graphics.gofplots.ProbPlot.html ；https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.probplot.html
- 講義與說明：https://www.stat.cmu.edu/~kass/tspp/08notes/qq.pdf （Kass，卡內基美隆大學）；https://docs.tibco.com/pub/dsc-stat/14.2.0/doc/html/UserGuide/6-working-with-graphs/probability-probability-plots-a.htm ；https://www.sfu.ca/sasdoc/sashtml/qc/chap8/sect9.htm 與 http://www.sfu.ca/sasdoc/sashtml/qc/chap8/sect8.htm （SAS 說明）；https://www.jtrive.com/posts/gof-python-scipy/gof-python-scipy.html
- NIST（對照，不是 P–P）：https://itl.nist.gov/div898/handbook/eda/section3/probplot.htm 、https://itl.nist.gov/div898/handbook/eda/section3/qqplot.htm 、https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/probplot.htm ；NIST 版權頁 https://www.nist.gov/oism/copyrights
- P value plot 出處：https://russell-davidson.research.mcgill.ca/articles/gmn-euro.pdf （Davidson 與 MacKinnon 論文）
- 查核限制（未核；僅記名、不列連結）：From Data to Viz `graph/qq.html`、R Graph Gallery `qq-plot.html`、Dataviz Project `data-type/qq-plot/`（以上 404，找不到 QQ 或 P–P 專頁，**不是來源**）
- 刻意不連結的可開頁：Dataviz Project 首頁與 Python Graph Gallery 首頁（可開，但沒有 P–P 專頁，不當來源）
- X：素材包以多輪關鍵字查 P–P、PP plot、probability-probability（含與 QQ 並陳、教學與適配關鍵詞），教學向原帖 0 筆，**沒有編造連結**
- 論文原文僅引述、素材包未列連結：Michael 1983（*Biometrika* 70 卷 1 期，第 11 到 17 頁；穩定化 P–P 圖）

鄰居 pattern：`qq-plot.md`（分位數對分位數；最容易混）、`bland-altman.md`、`manhattan-plot.md`、`locuszoom.md`、`volcano-plot.md`、`ma-plot.md`、`correlation-scatter.md`；穩定化 P–P 圖尚無專檔。

圖檔留在教圖／skill-pack（`/workspace/skill-packs/2026-10-01-pm-pp/images/`，21 張，圖說與教學稿逐字相同），本 repo **不複製**任何圖。可對照的圖：wiki-pp-quality（CC0；軸超出 0 到 1、紅線約 29°）、sim-unit-square-anatomy／sim-anatomy-good-fit／sim-heavy-tails／sim-location-mismatch／sim-pp-vs-qq-skew／sim-two-sample-pp／sim-residual-pp／sim-statsmodels-ppplot（皆**模擬資料**，數字未核；statsmodels 圖軸標已依實際計算改正，橫軸 i/(n+1)、縱軸擬合 CDF，與本 repo 慣例互換）、geostats-PP_calc／notebook-pp／interactive_PP（CC BY-NC-ND 4.0；互動儀表板兩個軸標題都用了反函數記號 F⁻¹(x) 卻接 "Cumulative Probability"，記號與文字不一致，以文字與刻度為準）、reliability-ppparametric（圖中沒有對角線也沒有圖例）／ppsemiparam（經驗放橫軸，與多數來源相反）、對照用的 QQ 類圖 geostats-QQ_calc／notebook-qq／QQ_equal／interactive_QQ 與 reliability-qqparametric／qqsemiparam（**不是 P–P 圖**）、nist-probplot（軸是數值，**不是嚴格 P–P 圖**）。授權見上；除 CC0 的 wiki-pp-quality 外，單張圖檔授權皆未逐檔確認，僅作教學示意引用。對帳見 `ATTRIBUTION.md`。
