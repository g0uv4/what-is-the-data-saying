# Pattern: bland-altman

> **圖種**：Bland–Altman 圖（Bland–Altman plot；亦稱差值圖 Difference plot；其他領域也叫 Tukey mean-difference plot）
> **來源（納茲教圖）**：`teach-viz/2026-09-30-pm-ba.md`（方法教學；正式課程）
> **定義（英文維基百科原文）**："A Bland–Altman plot (or Bland–Altman difference plot) in analytical chemistry or biomedicine is a method of data plotting used in analyzing the agreement between two different assays."
> **核心**：兩種方法各測同一批樣本；**每個點＝一對配對量測**；**橫軸＝兩方法的平均 (A＋B)／2**；**縱軸＝兩者的差值**（**方向一定要寫在圖題**）；再畫平均差（偏差）與一致性界限（常取平均差 ± 1.96 倍差值標準差），看兩種方法差多少、差得穩不穩、能不能互相替換。橫軸用平均而不用其中一種方法，是因為差值單獨對其中一種方法作圖會有已知的統計假象（1986 年原文："a well-known statistical artefact"）。
> **原始文獻**：Bland 與 Altman 1986，*Lancet*（DOI 10.1016/S0140-6736(86)90837-8）；Bland 與 Altman 1999，*Statistical Methods in Medical Research*（DOI 10.1177/096228029900800204）；入門講解 Giavarina 2015，*Biochemia Medica* 25(2):141–151（PMC4470095）

## 五件必須釘清的事

1. **一致性界限不是信賴區間。** 界限描述「預期涵蓋約 95% 差值的區間」（差值近似常態時），是差值的分布；**平均差與兩條界限各自另有信賴區間**，表示抽樣誤差。英文維基百科（"represent a confidence interval for which most of the differences lie"）與 statsmodels 文件（"95% confidence intervals for the means of the differences"）的用語較鬆散，本 pattern 不沿用。**能不能互換，要看界限連同它們的信賴區間是否落在可接受範圍內；可接受與否是臨床或專業判斷，要事先訂好，不是統計自己決定**（Giavarina："Acceptable limits must be defined a priori, based on clinical necessity, biological considerations or other goals."）。
2. **相關係數高不等於一致；也不是「95% 的點必落在界限內」。** 1986 年原文："The use of correlation is misleading."（同一批人相關高達 0.94，仍掩蓋了兩台儀器最多相差約 80 l/min）。界限是估計值，樣本中有少數點在界限外很正常（BlandAltmanLeh 文件 20 點中 1 點在界限外："That's just what one would expect in case of normal distribution."）。
3. **差值方向各來源不一致，圖題一定要寫清**：英文維基百科寫新方法減金標準；X 原帖（ProtocolDotMed）寫 B 減 A；Giavarina 寫 A 減 B；1986 年圖 2 是大型儀器減迷你儀器、圖 3 圖上是 POS 減 OSM 但正文方向相反；BlandAltmanLeh、pingouin 是 A 減 B。方向決定平均差的正負號。**本 repo 的虛構資料一律是「方法 B 減方法 A」**。
4. **MA 圖與 Bland–Altman 圖：不要寫成同一種結構。** 英文維基百科說 MA 圖是 Bland–Altman 圖應用於基因體資料、取對數後的版本（"This version of the plot is used in MA plot."）；但用途與解讀門檻不同：本圖回答「兩種量測方法是否一致、能否互換」，MA 圖（`ma-plot.md`）回答「在什麼豐度層級上變、正規化或收縮是否異常」。實務上 DESeq2 等工具的 MA 圖橫軸是平均正規化計數，不是對數平均；「取對數／比值圖與 MA 圖的對數尺度相通」只是說對數這一步。
5. **授權**：除英文維基百科頂圖（Commons `Bland-Altman_Plot.svg`，作者 gismokater97，CC BY-SA 3.0，須標作者與授權）外，其餘外部圖（Giavarina、York／Lancet 轉載、BlandAltmanLeh、blandr、MedCalc、pingouin、statsmodels）授權都未明示，素材包一律註「授權未明示，僅作教學示意引用」，**不可當作可自由再用**；標「模擬資料重繪」者為自製。本 repo 不複製任何圖，詳見 `ATTRIBUTION.md`。另：Hanneman 2008 方法比較論文的正確編號是 **PMC2944826**。

## When

- 同一批樣本或受試者上的**配對連續量測**，比較兩種方法（新儀器對舊儀器、兩種試劑、兩種演算法）
- 同一方法的重複量測（看重複性；平均差理論上應接近 0；若每位受試者重複多次，不能直接套經典公式，只取平均再畫會低估差值標準差、界限偏窄）
- 找出固定偏差、比例性偏差、扇形與離群配對
- 教學：說明為什麼相關高不等於一致

## Recommend

- **主選**：經典 Bland–Altman 圖（橫軸 (A＋B)／2、縱軸差值、紅實線＝平均差、兩條虛線＝平均差 ± 1.96 倍差值標準差、0 線；圖題寫方向）；並加上平均差與兩條界限各自的信賴區間
- **變體（依資料形狀選）**：
  - **固定偏差**：平均差離 0、點雲均勻 → 可考慮扣掉平均差校正（pingouin 文件："If there is a consistent bias, it can be adjusted for by subtracting the mean difference from the new method."）
  - **比例性偏差**：差值隨平均值傾斜 → 加差值對平均的迴歸線，改用迴歸式界限（Bland 與 Altman 1999）
  - **扇形（變異隨大小變大）**：差值散布隨平均值變寬 → 改畫**百分比差異**（差值 ÷ 兩方法平均 × 100；平均值接近 0 時不穩定）、**取對數**（反對數後界限變成比值）或迴歸式界限
  - **差值非常態**：改用差值的第 2.5 與第 97.5 百分位數（維基百科、Bland 與 Altman 1999、MedCalc 非參數法）或轉換
  - **有參考方法**時橫軸用哪個有爭議（Krouwer 2008 主張用參考方法；Bland 與 Altman 1995 主張不該用標準方法）——只說有爭議，不表態
- **參數與判準範例（範例，不是標準）**：

| 項目 | 數值與出處 | 性質 |
|---|---|---|
| 界限倍數 | 1.96 倍差值標準差（預期涵蓋約 95% 差值，前提是差值近似常態）；1986 年原文為求簡便寫 2 倍 | 範例，不是標準 |
| 平均差的標準誤 | 約 √(s²／n)；兩條界限的標準誤約 √(3s²／n)（s＝差值標準差，n＝配對數）；信賴區間用自由度 n−1 的 t 臨界值 | 範例，不是標準 |
| 樣本數 | Bland 本人建議約 100 位（"I usually recommend 100 as a good sample size"，此時界限信賴區間約 ± 0.34 倍標準差；12 位約 ± 1 倍、200 位約 ± 0.24 倍）；**是個人建議，不是公認門檻** | 範例，不是標準 |
| 可接受範圍 | **由臨床或專業事先訂定**；本 repo 練習資料為示範假設 ±8，**不是臨床標準** | 範例，不是標準 |
| 迴歸式界限係數 | MedCalc 頁面記載 2.46 | 範例，不是標準 |
| 百分位界限 | 第 2.5 與第 97.5 百分位數 | 範例，不是標準 |

- **備選（何時改用哪一種）**：
  - 只有單一方法資料，或**沒有配對**（兩批不同樣本）→ 資料前提不足，算不出每一對的差
  - 只有類別結果、沒有連續量測 → 不是本圖
  - 想看兩個獨立組的平均差與信賴區間 → **Gardner–Altman 圖**（名字相近但不是同一種；維基百科頂端提醒不要混淆；repo 尚無專檔）
  - 想用迴歸檢查兩方法的比例與固定差異 → **Passing–Bablok 迴歸**、**Deming 迴歸**（名稱對照，repo 尚無專檔）
  - 豐度與倍數 → `ma-plot.md`；倍數與顯著性 → `volcano-plot.md`；分布形狀 → `qq-plot.md`

## 與鄰近圖種的區別

| 圖種 | 橫軸 | 縱軸／內容 | 回答的問題 | 和 Bland–Altman 圖的差別 |
|---|---|---|---|---|
| **MA 圖**（`ma-plot.md`） | 平均豐度 | 對數倍數 | 正規化或收縮是否異常 | 維基百科：MA 圖是它應用於基因體資料、取對數後的版本；用途與解讀門檻不同，**不把兩者說成同一種圖** |
| **一般散點圖與相關係數**（`correlation-scatter.md`） | 方法 A | 方法 B | 兩變數有沒有線性關係 | 相關高不等於一致；散點圖要加 y＝x 線，但差多少不易看出，Bland–Altman 把差放到縱軸 |
| **QQ 圖**（`qq-plot.md`） | 理論或另一批的分位數 | 樣本的分位數 | 分布形狀像不像參考分布 | 看分布形狀，不是兩種量測的一致性界限；**也可用來檢查差值是否近似常態** |
| **火山圖**（`volcano-plot.md`） | 倍數 | 顯著性 | 變多大、證據多強 | 不是兩方法的差值對平均 |
| Passing–Bablok／Deming 迴歸（repo 尚無專檔） | 方法 X | 方法 Y | 穩健斜率與截距；兩變數都有誤差時的迴歸 | 迴歸式方法比較，教學稿只作名稱對照 |
| Gardner–Altman 圖（repo 尚無專檔） | 兩組 | 平均差與信賴區間 | 兩個獨立組的差 | 名字相近，不是同一種 |

判斷口訣：**配對量測、看一致性與能否互換 → Bland–Altman；平均豐度對倍數 → MA 圖；分布形狀 → QQ 圖；兩變數是否線性相關 → 一般散點圖。**

## Avoid

- 把一致性界限當成信賴區間；只報界限、不報平均差與界限的信賴區間
- 界限在可接受範圍內就說「可互換」（要連同信賴區間一起落在事先訂好的範圍內；範圍事後才發明就不成立）
- 以為相關係數高就一致；以為 95% 的點必落在界限內
- 差值方向沒寫或前後不一致（圖題、圖說、正文要一致）
- 對非常態的**差值**硬用 1.96 倍標準差（要檢查的是差值，不是量測值本身）
- 把扇形（變異隨大小改變）與比例性偏差（偏差隨大小改變，差值傾斜）混為一談；資料是扇形或傾斜，仍畫水平界限
- 平均值接近 0 時使用百分比差異；樣本太少（界限信賴區間會很寬）
- 拿它證明新方法「準確」：它只比較兩種方法彼此差多少，兩者都不是絕對正確的標準（1986 年原文："neither provides an unequivocally correct measurement"）
- 把不是 Bland–Altman 圖的圖當成它（例：Giavarina 圖 1、BlandAltmanLeh 散點圖只是「先看相關」的對照）
- 把 MA 圖與 Bland–Altman 圖寫成同一種；把模擬資料與真實資料混在一起；把授權未明示的外部圖當可自由再用

## Produce checklist

- [ ] 故事句是「兩種方法一致嗎、界限寬不寬、能不能互換」；資料是成對連續量測
- [ ] 表：一列一對配對；至少 method_a、method_b；**圖題寫差值方向**（本 repo 練習資料：方法 B 減方法 A）
- [ ] 算差值 d 與平均 m；檢查**差值**是否近似常態（直方圖、QQ 圖或常態性檢定）；是否隨大小改變
- [ ] 畫平均差線、平均差 ± 1.96 SD 兩條界限、0 線；加平均差與兩條界限各自的 95% 信賴區間（近似：平均差 SE ＝ s／√n、界限 SE ＝ √(3s²／n)）
- [ ] **事先**寫下最大可接受差（臨床或專業判斷；示範用 ±8 只是假設），再把界限連同信賴區間對照它
- [ ] 判讀四件事：平均差離 0 嗎（正負號配合方向）→ 散布隨平均值變寬嗎（扇形）→ 走勢隨平均值傾斜嗎（比例性偏差）→ 有離群配對嗎（回溯查檢體與操作，推論性建議）
- [ ] 扇形或傾斜時改畫百分比差異、取對數或迴歸式界限；圖上不留程式變數名；軸標題與單位寫清楚
- [ ] 圖注：「一致性界限描述差值的分布，不是信賴區間；能否互換看界限連同信賴區間是否在事先訂好的可接受範圍內」
- [ ] 工具誠實（只寫素材包證實的；版本為 2026-09-30 查核值）：
  - **statsmodels**（Python，0.15.0）：`mean_diff_plot`；程式 BSD-3；官方示例是兩批各 20 個隨機數（固定種子 9999），**不是真實量測**，方向為第一批減第二批
  - **pingouin**（Python，0.7.0）：`plot_blandaltman`；程式 GPL-3.0；圖上含平均差與界限的信賴區間陰影；方向 A 減 B
  - **BlandAltmanLeh**（R，CRAN 0.3.1，2015-12-23；GPL-2 或 GPL-3）：預設第一組減第二組；有含信賴區間的變體
  - **blandr**（R，CRAN 0.6.0，2024-06-09；GPL-3）：預設方法 1 減方法 2
  - **MedCalc**（商用軟體手冊頁，頁面版權 © 2026 MedCalc Software Ltd）：可選橫軸、百分比、非參數、迴歸式界限、最大可接受差
  - **Matplotlib**：素材包模擬資料重繪用，授權素材包未寫，不代填。英文維基百科另列 Analyse-it、NCSS、GraphPad Prism、StatsDirect、JASP 等支援軟體，素材包未逐一查證
  - R Graph Gallery、Python Graph Gallery、From Data to Viz、Dataviz Catalogue、Dataviz Project 均查無 Bland–Altman 專頁
- [ ] 示範數字標「數字未核」
- [ ] 自檢：方向寫了嗎？界限寫成信賴區間了嗎？可接受範圍是事先訂的嗎？有沒有用相關係數當一致性證據？

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-ba-fictional.csv` — 220 列（約 6 KB）；檔頭兩行以 `#` 開頭，讀取要略過（pandas 用 `comment='#'`）；欄位 `row_id, dataset, method_a, method_b`。`dataset`＝`good`：100 對「一致性良好」的配對；`fan`：120 對「誤差與大小成比例」的配對（扇形）。**差值一律是方法 B 減方法 A**。
- 我重新計算的數字（**以實際計數為準**；與素材包檢查輸出逐項一致）：
  - `good`（n＝100）：平均差 0.703、差值標準差 2.424、界限 5.454 與 −4.047、界限外 **7 點**；平均差 95% 信賴區間 0.222 到 1.184，上界 4.621 到 6.286，下界 −4.880 到 −3.214（t 臨界值 1.984，自由度 99）；界限連同信賴區間都在**假設的**可接受範圍 ±8 內（範圍是假設，非臨床標準）；A 與 B 的相關係數約 0.997，差值與平均無明顯斜率（約 −0.007）
  - `fan`（n＝120）：平均差 0.583、差值標準差 5.375、界限 11.118 與 −9.952、界限外 **5 點**；平均值較小一半的差值標準差 3.391、較大一半 6.799（比值 2.01，扇形）；改看百分比差異，兩半標準差 4.81 與 4.32 個百分點（大致相等），百分比平均差 0.56%、界限 9.48% 與 −8.37%；A 與 B 的相關係數約 0.995（相關再高也不代表沒有扇形問題）
  - 兩組界限外點數：good 7/100＝7%、fan 5/120≈4.2%——都與「約 5%」不完全相同，正好示範「95% 是預期，不是保證」
  - 素材包檢查程式註解寫 good「落在界限外的點很少（約 5%，不是 0）」：實際是 7%（7/100），**以實際計數為準**。素材包沒有列出 fan 的界限外點數與信賴區間，上面是我自己算的（fan 平均差 95% 信賴區間 −0.389 到 1.555，t 臨界值 1.980）
- 示範讀法：橫軸 (method_a＋method_b)／2、縱軸 method_b − method_a，畫平均差線與 ± 1.96 SD 兩條虛線；`good` 應是一團均勻散開的點雲；`fan` 應呈扇形，此時改畫百分比差異再比較。圖題寫「差值＝方法 B 減方法 A」。
- `sample-ba-selfcheck.py` — 自檢腳本（需 numpy；**以絕對路徑讀同資料夾的指定檔名，不搜尋檔案，所以在任何資料夾執行都可以**；見 `examples/data/README.md`）。

## 參考連結（可點；皆出自素材包 sources.txt 且標可開）

- https://en.wikipedia.org/wiki/Bland%E2%80%93Altman_plot （定義原文）；相關條目：https://en.wikipedia.org/wiki/MA_plot 、https://en.wikipedia.org/wiki/Estimation_statistics （Gardner–Altman 圖）、https://en.wikipedia.org/wiki/Passing%E2%80%93Bablok_regression 、https://en.wikipedia.org/wiki/Deming_regression
- 頂圖圖片頁（作者與授權）：https://commons.wikimedia.org/wiki/File:Bland-Altman_Plot.svg ；圖庫分類：https://commons.wikimedia.org/wiki/Category:Bland%E2%80%93Altman_plots
- 原始論文與轉載：https://doi.org/10.1016/S0140-6736(86)90837-8 （1986 年 Lancet）、https://www-users.york.ac.uk/~mb55/meas/ba.htm 、https://www-users.york.ac.uk/~mb55/meas/ba.pdf （York 大學 Martin Bland 頁的轉載，經 Lancet 授權轉載，頁面未寫可自由再用）；https://doi.org/10.1177/096228029900800204 （1999 年）；https://www-users.york.ac.uk/~mb55/meas/sizemeth.htm （樣本數說明，頁面最後更新 2004-01-12）
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4470095/ （Giavarina 2015；開放取用，版權屬克羅埃西亞醫學生化學會，未找到創用 CC 聲明）
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2944826/ （Hanneman 2008，方法比較文獻；正確編號 PMC2944826）
- https://www.medcalc.org/manual/bland-altman-plot.php
- https://www.statsmodels.org/stable/generated/statsmodels.graphics.agreement.mean_diff_plot.html 、https://pingouin-stats.org/generated/pingouin.plot_blandaltman.html
- https://cran.r-project.org/web/packages/BlandAltmanLeh/vignettes/Intro.html 、https://cran.r-project.org/web/packages/blandr/vignettes/introduction.html
- X 貼文（社群旁證，不是學術原始論文，帳號背景無法證實；方向 B 減 A 與 Giavarina 的 A 減 B 相反）：https://x.com/ProtocolDotMed/status/2103866656384749777 、https://x.com/ProtocolDotMed/status/2103867012711841941 （第二則附「在合適假設下」的前提）
- 查核限制（未核；僅記名、不列連結）：From Data to Viz `graph/blandaltman.html`、Dataviz Catalogue `methods/bland_altman_plot.html`、R Graph Gallery `bland-altman-plot.html`、Python Graph Gallery `bland-altman-plot/`、Dataviz Project `data-type/bland-altman-plot/`、datanovia 的 Bland–Altman 教學頁、Commons 單數分類 `Category:Bland–Altman_plot`（以上 404）；STHDA 的 GGally Bland–Altman 頁（410，已永久移除）
- 刻意不連結的可開頁：GraphPad `faqid/1790`（內容是 "Choosing a statistical test"，沒有 Bland–Altman 內容，教學稿未採用）、`statsmodels` 的示例圖檔網址與英文維基百科 `File:` 頁（圖檔／重複頁）

鄰居 pattern：`ma-plot.md`（對數尺度相通但用途不同）、`qq-plot.md`（檢查差值是否近似常態）、`pp-plot.md`（機率對機率；≠ 一致性圖）、`correlation-scatter.md`（相關不等於一致）、`volcano-plot.md`；Gardner–Altman 圖、Passing–Bablok 與 Deming 迴歸尚無專檔。

圖檔留在教圖／skill-pack（`/workspace/skill-packs/2026-09-30-pm-ba/images/`，27 張，圖說與教學稿逐字相同），本 repo **不複製**任何圖。可對照的圖：wikipedia-top（CC BY-SA 3.0；圖上只寫 difference、沒標方向）、sim-anatomy／sim-good-agreement／sim-fixed-bias／sim-proportional-fan／sim-percent-diff／sim-proportional-bias-slope／sim-vs-identity-scatter／sim-ma-log-compare（皆**模擬資料重繪**，方向 B 減 A；圖上數字為模擬值、數字未核；sim-good-agreement 的 ±8 綠帶是假設，不是臨床標準；sim-ma-log-compare 只示範「取對數」這一步，不代表兩圖是同一種圖）、york-ba2／ba3-note／ba4（1986 年；ba2、ba4 界限用 2 倍標準差；ba3 圖上 POS 減 OSM，與正文方向相反）、giavarina-f1（**不是** Bland–Altman 圖）／f2／f3／f5／f6／f7／f8（A 減 B；f2、f3 尚未畫界限）、pingouin-plot-note、baleh-01（**散點圖，不是** Bland–Altman 圖）／02／04-note／05-note、blandr-01、medcalc-loa-full（改過圖內縮寫）、statsmodels-example（隨機數，不是真實量測）。皆授權未明示，僅作教學示意引用（除 wikipedia-top 外）。對帳見 `ATTRIBUTION.md`。
