# Pattern: qq-plot

> **圖種**：QQ 圖（Q–Q plot；全名分位數－分位數圖 Quantile–Quantile plot；也寫作 QQ plot、qqplot）
> **來源（專案維護者整理）**：`teach-viz/2026-09-30-am-qq.md`（方法教學；正式課程）
> **定義**：比較兩個機率分布的分位數。把兩個分布的分位數放在同一張圖上：一批樣本對理論分布，或一批樣本對另一批樣本。**兩批資料不必成對，筆數也不必相等**（英文維基百科原句）。
> **核心**：每個點代表「同一個累積比例」在兩邊各自對應的數值；樣本對理論時常見約定是橫軸理論分位數、縱軸樣本分位數，但**不是通則**（R 的 `qqnorm` 有 `datax=TRUE`）；兩樣本比較時哪批放哪軸是作者約定（NIST 範例是第一批在縱軸）。**讀別人的圖，先看軸標題。**
> **一句話**：貼線提示分位數形狀相近，但這不是假設檢定，沒有 p 值；偏離是證據，不是證明（NIST 用字是 evidence）

## 三件必須釘清的事

1. **貼在 y = x 線上，才表示兩個分布相近；點貼在「任何一條直線」上，只表示兩者呈線性關係**（位置、尺度可以不同），不一定相同。位置差是直線上下平移，尺度差是斜率不同；**曲線彎曲才是形狀不同**（偏態、尾部厚薄）。貼線也不等於形狀相近之外的其他事都沒問題。（審稿修正）
2. **SciPy 官方文件明寫**："probplot generates a probability plot, which should not be confused with a Q-Q or a P-P plot."　所以不要把 `scipy.stats.probplot` 的圖直接叫做 QQ 圖（它畫的是機率圖，紅線是最小平方擬合線）。**qqman 的 `qq()` 只畫圖，不計算基因組膨脹係數 λ，也不畫信賴帶**（教學稿對照原始碼與說明文件確認）。**λ 沒有單一官方閾值**：估計式是 λ̂ = median(Y²) ÷ 0.456（英文維基百科 Genomic control 條目；0.456 約等於卡方一自由度的中位數，教學稿以 SciPy 自算約 0.4549）；次級來源有「1.05」與「1.10」兩種說法且互相不一致，均非官方標準或原始論文，本 pattern 不採任何單一閾值。λ 偏高也可能是多基因遺傳造成的真實訊號，不一定是壞事（PubMed 21407268 摘要："in the absence of population structure and other technical artefacts, but in the presence of polygenic inheritance, substantial genomic inflation is expected."）。
3. **圖檔授權大多不是可自由再用**：NIST、SciPy、statsmodels、ggplot2、qqman 的文件圖與 X 貼文圖，授權都未明示，素材包一律註「授權未明示，僅作教學示意引用」；Getting Genetics Done 的圖是 CC BY-NC 3.0，只能非商業使用；維基百科與 Commons 的圖須標作者與授權。本 repo 不複製任何圖檔，詳見 `ATTRIBUTION.md`。

## When

- 探索性分析：檢查樣本是否近似常態（或所指定的其他理論分布）
- 兩組量測或兩批次：檢查分布形狀、位置、尺度是否相近（筆數不必相同）
- 模型診斷：檢查線性模型殘差是否大致常態（**圖題要寫「殘差」**）
- 全基因組關聯研究（GWAS）品質管制：觀察 −log10(p) 對期望 −log10(p)，與曼哈頓圖並列
- 教學：說明偏態、厚尾、短尾在分位數座標上長什麼樣子

## Recommend

- **主選（依問題選變體）**：
  - **常態 QQ（理論 QQ）**：樣本對常態（或 t、指數等指定理論分布）。R `qqnorm`／`qqline`、ggplot2 `geom_qq`、statsmodels `qqplot`、car `qqPlot` 走這條。常態機率圖（Normal probability plot）是 QQ 機率圖對常態的特例
  - **兩樣本 QQ**：一批的分位數對另一批（NIST 經典用途）；兩批各取相同的累積比例
  - **GWAS 風格 QQ**：橫軸期望 −log10(p)、縱軸觀察 −log10(p)，紅線 y = x（qqman `qq()`：期望值為 −log10 的 `ppoints(n)`）
  - **迴歸殘差 QQ**：對殘差畫常態 QQ，檢查誤差是否大致常態
- **參考線有三種畫法，圖上要註明是哪一種**（貼不貼線的判斷不同）：

| 參考線（範例，不是標準） | 意思 | 出現在哪裡 |
|---|---|---|
| y = x 線（45 度線） | 兩個分布相同時，點應落在這條線上 | NIST、維基百科、qqman |
| 通過第一與第三四分位數的線 | 不要求兩分布相同，只看形狀是否線性 | R `qqline` 預設、ggplot2 `geom_qq_line`（`line.p` 預設 c(.25,.75)）、statsmodels line="q"、car `qqPlot` |
| 擬合線 | 最小平方擬合線（SciPy `probplot` 紅線）、迴歸線（statsmodels line="r"）、標準化線（line="s"） | SciPy、statsmodels |

- **各型態怎麼讀（樣本在縱軸、理論常態在橫軸；軸換邊則方向顛倒）**：

| 型態 | 圖形 | 備註 |
|---|---|---|
| 大致貼線 | 點沿參考線分布，兩端略偏 | 只是提示，不是證明常態 |
| 右偏 | 中段貼線、右上端明顯高於線 | 「右偏」是依圖形的推論；維基百科圖說只說明顯非線性 |
| 厚尾 | 左端低於線、右端高於線（S 形） | 維基百科："S-shaped … heavier tails" |
| 短尾（如均勻） | 左端高於線、右端低於線（反向 S 形） | 維基百科常態機率圖條目寫均勻樣本 "has an S shape"，其圖把資料放在另一軸，方向相反是軸擺法不同（推論） |
| 離群值 | 少數點遠離其餘點，出現在一端 | 維基百科 Weibull 圖說："Three outliers are evident at the high end of the range." |
| 雙峰或混合分布 | **典型圖形無法證實** | 所引來源沒有描述，本 pattern 不編造 |

- **小樣本警語**：點愈少，愈難分辨隨機起伏與真正偏離常態（維基百科常態機率圖條目："With fewer points, it becomes harder to distinguish between random variability and a substantive deviation from normality."；該條目提到常態圖常只用到 7 個點）。十個以下尤其要保守
- **備選（何時改用哪一種）**：
  - 關聯訊號落在哪條染色體、哪一段 → **曼哈頓圖**（`manhattan-plot.md`）
  - 變化幅度與顯著性 → **火山圖**（`volcano-plot.md`）；豐度與倍數 → **MA 圖**（`ma-plot.md`）
  - 只想看分布輪廓、峰數、離群 → 箱形圖／小提琴／山脊／雨雲（`boxplot-summary.md`、`violin-distribution.md`、`ridgeline-density.md`、`raincloud-combo.md`）；本 repo 尚無專檔的直方圖也可
  - 兩種量測方法的一致性界限 → [**Bland–Altman 圖**](bland-altman.md)
  - 染色體局部區間細看 → [**LocusZoom 圖（區域關聯圖）**](locuszoom.md)
  - 想比較的是累積機率曲線是否重合 → [**P–P 圖**](pp-plot.md)；不要把 P–P 圖叫成 QQ 圖
  - 只有類別標籤、沒有可排序數量或 p 值 → 資料前提不夠

## 與鄰近圖種的區別

| 圖種 | 橫軸 | 縱軸／內容 | 回答的問題 | 和 QQ 圖的差別 |
|---|---|---|---|---|
| **曼哈頓圖**（`manhattan-plot.md`） | 基因組位置 | −log10(p) | 關聯訊號落在基因組哪一段 | 橫軸是位置不是期望值；兩者常並列（QQ 回答「整體有沒有偏」，曼哈頓回答「在哪裡」） |
| [**P–P 圖**](pp-plot.md) | 理論累積機率 | 經驗累積機率 | 兩條累積分布曲線是否重合 | 軸是 0 到 1 的機率，比較線是 (0,0) 到 (1,1) 的 45 度線；QQ 圖的軸是分位數實際數值。兩者常被混淆（維基百科 P–P 條目："with which it is often confused"） |
| [**Bland–Altman 圖**](bland-altman.md) | 兩種量測的平均 | 兩種量測的差 | 兩種量測方法的一致性 | 用途不同 |
| [**LocusZoom 圖（區域關聯圖）**](locuszoom.md) | 染色體局部位置 | −log10(p) 等 | 局部區間細看 | 局部關聯圖，不是分布診斷 |
| **一般散點圖**（`correlation-scatter.md`） | 任意數值 | 任意數值 | 兩變數關係 | QQ 圖的軸不是任意兩欄，而是對齊同一累積比例後的分位數 |
| **火山圖**（`volcano-plot.md`） | 倍數 | 顯著性 | 變多大、證據多強 | 不是分位數對分位數 |
| **MA 圖**（`ma-plot.md`） | 平均豐度 | 對數倍數 | 正規化或收縮是否異常 | 不是分位數對分位數 |

「尾部差異在 QQ 圖上常比 P–P 圖更顯眼」：9/30 本課所引來源未證實；10/1 P–P 課另找到 GeostatsGuy、reliability 文件與 SAS 說明三份來源，都有類似的**定性**說法（P–P 在分布中央較有鑑別力、QQ 在尾部較有鑑別力；英文維基百科 P–P 條目本身沒寫），不是定理，詳見 [`pp-plot.md`](pp-plot.md)。

判斷口訣：**分位數對分位數 → QQ 圖；機率對機率 → P–P 圖；位置對 −log10(p) → 曼哈頓圖；任意兩欄 → 一般散點圖。**

## Avoid

- 以為點貼一條斜線就是分布相近（貼 y = x 才是）；把位置或尺度差當成彎曲
- 圖上不標參考線是哪一種
- 「點貼直線就是常態」或「點偏離就是非常態」：前者只是提示；後者要看證據強弱、樣本數與實質意義
- 一端少數點遠離其餘點，只用「非常態」一句帶過：先看是資料問題還是尾部真的較長
- 小樣本下結論；沒看軸標題就讀方向
- 把 SciPy `probplot` 直接叫 QQ 圖；說 qqman `qq()` 會給 λ 或信賴帶
- 拿單一閾值（1.05 或 1.10）判斷 λ，或把 λ 偏高一律當成品質問題
- 把 P–P 圖叫成 QQ 圖，或把曼哈頓圖當成 QQ 圖
- 殘差 QQ 圖沒寫是「殘差」，被誤讀成原始反應變數一定常態
- 圖內帶程式參數文字框、變數名、逗號小數或超出 0 到 1 的軸；模擬資料與真實資料不分
- 把授權未明示的文件圖當成可自由再用

## Produce checklist

- [ ] 故事句是「分布形狀像不像某個參考分布、兩批像不像同一種分布」（或 GWAS 的 p 值有沒有整體偏離期望）
- [ ] 選定變體並寫在圖題：常態 QQ／兩樣本 QQ／GWAS 風格／殘差 QQ（殘差要寫「殘差」）
- [ ] 理論分位數的累積比例寫清楚（例：(i − 0.5) / n；qqman 用 `ppoints(n)`）；兩樣本時兩批各取相同累積比例（例：0.05 到 0.95）
- [ ] 軸標題寫人話，標明哪個是理論或哪批樣本；不留程式變數名
- [ ] 參考線註明是 y = x、四分位線還是擬合線
- [ ] 圖注：「貼線只提示分位數形狀相近，不是證明，也不是假設檢定的 p 值」；點少時加小樣本提醒
- [ ] GWAS 風格：並陳曼哈頓圖；若報告 λ，數字另核並註明採用的判斷門檻（各教材不一，無單一官方值）；從原點附近就整條抬離時不能只當品質問題（可能是族群分層、技術偏差或多基因遺傳）；中段貼線、末端才上揚時，再對照曼哈頓圖是否有位置集中的峰值
- [ ] 殘差 QQ 兩端系統偏離：檢查資料轉換、離群點、變異數是否隨擬合值改變，必要時並陳殘差對擬合值圖（建議，屬推論）
- [ ] 工具誠實（只寫素材包證實的；版本為 2026-09-30 查核值）：
  - **qqman**（R，CRAN 0.1.9，2023-08-23；GPL-3）：`qq()`，只畫圖；引用 Turner 2018，*JOSS* 3(25):731
  - **statsmodels**（Python，0.15.0）：`qqplot`、P–P 圖；程式碼 BSD-3
  - **SciPy**（Python，1.18.0）：`probplot`（官方說明它不是 QQ 圖）；程式 BSD
  - **ggplot2**（R，4.0.3）：`geom_qq`、`geom_qq_line`；程式 MIT
  - **R `qqnorm`／`qqline`**（文件頁為 R 3.6.2 舊版）、**car `qqPlot`**、**Matplotlib**：素材包未寫授權，不代填
  - 上列文件圖片授權均**未明示**；R Graph Gallery、Python Graph Gallery、From Data to Viz、Dataviz Catalogue、Dataviz Project、Seaborn 均查無 QQ 圖專頁
- [ ] 示範數字標「數字未核」
- [ ] 自檢：貼的是 y = x 還是任意直線？參考線畫法有註明嗎？有沒有把 P–P 圖或機率圖叫成 QQ 圖？

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-qq-fictional.csv` — 220 列（約 6 KB）；檔頭兩行以 `#` 開頭，讀取要略過（pandas 用 `comment='#'`）；欄位 `row_id, group, value, pvalue_sim`。`group` A 為近似常態的虛構數值（120 筆）、B 為右偏的虛構數值（100 筆）；`value` 為虛構單位；`pvalue_sim` 為虛構 p 值，供練習「觀察對期望 −log10 p 值」的 QQ 圖。
- 我重新計算的數字（**以實際計數為準**）：A 組 120 筆，範圍 26.35–72.96，平均 49.84、標準差 8.52，偏態約 −0.43；B 組 100 筆，範圍 44.92–70.12，中位數 49.44、平均 50.35，偏態約 1.97（右偏）；`row_id` 220 個不重複；`pvalue_sim` 介於 0.00042 與 0.987，p < 0.05 共 15 列、< 0.01 共 4 列、< 0.001 共 1 列、< 0.0001 共 0 列。與素材包檢查輸出一致（A 組對常態相關係數 0.9890、B 組 0.9258，B 組最大值離四分位參考線 11.92 遠大於 A 組 0.79；觀察 −log10(p) 最大 3.37、期望最大 2.64）。
- 素材包文字說 `pvalue_sim`「約 6% 帶訊號」：CSV 沒有訊號旗標欄，無法重數；只能說 p < 0.05 的列占 15 / 220 ≈ 6.8%（其中含虛無假設下本來就會出現的約 5%），所以「約 6% 帶訊號」**無法由 CSV 驗證**，以實際計數為準。
- 示範讀法：組 A 或組 B 排序後，對 (i − 0.5) / n 的常態分位數作圖，畫通過第一與第三四分位數的參考線（範例，不是標準）；A 組貼線、B 組右上端明顯高於線；兩組互比時各取相同累積比例（例：0.05 到 0.95 共 19 組）畫兩樣本 QQ；`pvalue_sim` 排序後橫軸放期望 −log10(p)、縱軸放觀察 −log10(p)，畫 y = x（虛構資料 p 值太少，尾端只有一列 < 0.001，別過度解讀）。
- `sample-qq-selfcheck.py` — 自檢腳本（需 numpy 與 scipy；**跑法與一個陷阱**見 `examples/data/README.md`）。

## 參考連結（可點；皆出自素材包 sources.txt 且標可開）

- https://en.wikipedia.org/wiki/Q%E2%80%93Q_plot （定義、四張範例圖）；相關條目：https://en.wikipedia.org/wiki/Normal_probability_plot 、https://en.wikipedia.org/wiki/P%E2%80%93P_plot 、https://en.wikipedia.org/wiki/Probability_plot 、https://en.wikipedia.org/wiki/Quantile 、https://en.wikipedia.org/wiki/Genomic_control （λ 估計式）
- Commons 圖片頁（作者與授權）：https://commons.wikimedia.org/wiki/File:Normal_normal_qq.svg 、https://commons.wikimedia.org/wiki/File:Normal_exponential_qq.svg 、https://commons.wikimedia.org/wiki/File:Weibull_qq.svg （CC BY-SA 3.0，作者 Skbkekas）；https://commons.wikimedia.org/wiki/File:Ohio_temps_qq.svg （CC BY 3.0，Skbkekas）；https://commons.wikimedia.org/wiki/File:Normprob.png 、https://commons.wikimedia.org/wiki/File:Normexpprob.png 、https://commons.wikimedia.org/wiki/File:Normunifprob.png （CC BY 3.0，Visnut）
- https://www.itl.nist.gov/div898/handbook/eda/section3/qqplot.htm 、https://www.itl.nist.gov/div898/handbook/eda/section3/probplot.htm （NIST 工程統計手冊；圖授權未明示）
- https://www.rdocumentation.org/packages/stats/versions/3.6.2/topics/qqnorm （R `qqnorm`／`qqline`）、https://rdrr.io/cran/car/man/qqPlot.html
- https://ggplot2.tidyverse.org/reference/geom_qq.html 、https://www.statsmodels.org/stable/generated/statsmodels.graphics.gofplots.qqplot.html 、https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.probplot.html
- https://cran.r-project.org/web/packages/qqman/qqman.pdf 、https://cran.r-project.org/web/packages/qqman/vignettes/qqman.html 、https://github.com/stephenturner/qqman
- https://gettinggeneticsdone.blogspot.com/2011/04/annotated-manhattan-plots-and-qq-plots.html （2011 年舊文；**內容與圖為 CC BY-NC 3.0，只能非商業使用**；頁首 2014 年更新說舊程式碼大概已不能用）
- X 貼文（素材包引用，皆非正式教材）：https://x.com/JuanluCaba_Unex/status/2101026577265942957 （分位數概念資訊圖，示意數字未核；「貼線就等於吻合」過度簡化，引用要加保留）；https://x.com/ChenDavie_AI/status/2096453843773255847 、https://x.com/ChenDavie_AI/status/2096453848022053246 （貼文自標以人工智慧製作、附圖為人工智慧生成示意圖，不作正式教材，只留連結）
- 查核限制（未核；僅記名、不列連結）：R Graph Gallery `quantile-quantile-plot.html`、Python Graph Gallery `quantile-quantile-plot/`、From Data to Viz `graph/qq.html`、Dataviz Catalogue `methods/qq_plot.html`、Dataviz Project `data-type/quantile-quantile-plot/`、Commons `Category:Q-Q_plots`、Seaborn `seaborn.qqplot`（以上 7 條 404）；Statology `q-q-plot`（202，回應近乎空白，不可用）；賓州州立大學 STAT 462 `node/123`（000，連線失敗）。另 Khan Academy 該篇雖回 200，但該站對任何路徑都回同一個要求啟用網頁腳本的驗證頁，文章是否存在無法證實，不作為來源、不列連結
- 已對照但素材包未列網址的次級來源：MetricGate、grGWAS 文件對 λ 閾值的說法（互相不一致，非官方標準）；不引用、不連結

鄰居 pattern：`manhattan-plot.md`（配套：位置 × −log10(p)）、`volcano-plot.md`、`ma-plot.md`、`correlation-scatter.md`（任意兩變數）、`violin-distribution.md`、`boxplot-summary.md`、`ridgeline-density.md`、`raincloud-combo.md`（分布輪廓的其他看法）、`bland-altman.md`（兩種量測方法的一致性；QQ 圖可用來檢查差值是否近似常態）、`locuszoom.md`（局部區間細看，不是分布診斷）、`pp-plot.md`（機率對機率；最容易混）；直方圖尚無專檔；`forest-plot.md`（多項研究的效應量與合併；統合分析的漏斗圖與 QQ 圖不是同一種診斷）、`kaplan-meier-survival.md`（存活時間診斷有時用 Q–Q；KM 曲線是群體存活估計，不是分位數診斷圖）。

圖檔留在教圖／skill-pack（素材包 `images/`，25 張，圖說與教學稿逐字相同），本 repo **不複製**任何圖。可對照的圖：wiki-normal-normal／wiki-normal-exp／wiki-weibull／wiki-ohio-temps（維基百科，需標作者與授權；ohio-temps 是兩樣本 QQ，不是對理論分布）、wiki-normprob／wiki-normexpprob／wiki-normunifprob（常態機率圖）、sim-anatomy-normal／sim-right-skew／sim-heavy-tails／sim-short-tails／sim-ref-lines／sim-gwas-inflation／sim-gwas-early-lift／sim-residual-qq（皆為**模擬資料重繪**；sim-residual-qq 顯示的是非常態殘差；gwas 兩張的 λ 約 1.08 與 1.30 是模擬值、數字未核、不是判斷門檻）、nist-qqplot、qqman-qq-basic／qqman-qq-titled、statsmodels-02（兩樣本 QQ）、scipy-probplot-note（**機率圖，不是 QQ 圖**）、ggplot2-geom-qq-1-note／2-note、x-juanlu（皆授權未明示，僅作教學示意引用）；對照圖：statsmodels-03（P–P 圖）、contrast-manhattan-qqman（曼哈頓圖，不是 QQ 圖）。對帳見 `ATTRIBUTION.md`。
