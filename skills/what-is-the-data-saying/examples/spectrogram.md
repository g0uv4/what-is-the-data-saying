# Pattern: spectrogram

> **圖種**：頻譜圖（spectrogram）
> **來源（專案維護者整理）**：`teach-viz/2026-10-08-am-spectrogram.md`（方法教學；第一次以頻譜圖為主題）
> **亦稱**：英文 spectrogram；短時傅立葉轉換做成的時間–頻率圖。臺灣譯名還沒統一：樂詞網聲學名詞譯「聲譜圖」，電子工程名詞譯「頻譜圖」，視覺藝術名詞記載「頻譜圖；音譜圖」；寬頻／窄頻樂詞網譯「寬頻聲譜圖」「窄頻帶聲譜圖」；人工智慧術語網站寫「頻譜圖」；成功大學 2007 年碩士論文寫「傅立葉正弦時頻圖」。大陸常見「语谱图」「声谱图」「时频谱图」，中文維基條目標題「时频谱」（又稱声谱图）。**大陸所稱「频谱图」常指沒有時間軸的頻譜**（橫軸頻率、縱軸振幅），與本稿不是同一種圖；這些大陸譯名**未經官方名詞網站核實**（「術語在線」查詢頁讀不到內容）
> **核心**：把一段快速振盪的訊號切成許多很短、彼此重疊的窗，逐窗算出各頻率的功率，再依時間排開；橫軸時間、縱軸頻率、顏色代表強弱（實務上幾乎都用分貝）
> **一句話**：「什麼時間出現了哪些頻率、各有多強。」
> **誠實提醒**：本課是方法教學；模擬圖與本 repo 的練習資料都是虛構，**數字未核**。真實圖凡標「目測」都未核。本稿說的「頻譜圖」只指「時間 × 頻率 × 顏色＝能量」；整段只畫成一條「頻率 × 能量」曲線時，一律稱「頻譜（spectrum）」，不叫頻譜圖。
> **潤稿狀態**：課程終稿與素材包寫明已經審稿人審核並潤稿；**沒有寫出潤稿用哪一個工具**，本稿不推測、也不另送潤稿。素材包文字依終稿整理。

## 十二件必須釘清的事

1. **怎麼讀（依序）。** 先看軸與方向（慣例：時間向右、頻率向上、0 在下方；R14、R15 頻率 0 在上，R17 左上格時間在縱軸）→ 看色條（越亮越強，還是越黑越強；0 分貝的基準是什麼、下限是多少）→ 看四種基本樣貌（S2：水平線＝持續固定音高、斜線＝頻率漸變、垂直線＝瞬間敲擊、等距水平線＝基頻加諧波）→ 看六項設定有沒有寫在圖上 → 再找新出現或消失的線，回頭對照情境。
2. **四個名詞不要混，頻率分析一律寫「三維瀑布圖」。** 頻譜沒有時間軸；頻譜圖是時間 × 頻率 × 顏色；小波量值圖（scalogram）縱軸是「尺度」，尺度越大頻率越低（R16）；三維瀑布圖（waterfall plot，暫譯；樂詞網查無此詞）資料與頻譜圖相同，只是把顏色換成高度，前方的峰會擋住後面（R17）。另外兩種同名不同物是：**財務瀑布圖**（waterfall chart，累加長條，`waterfall-bridge.md`）與**腫瘤學瀑布圖**（依變化排序的直條圖，`swimmer-plot.md` 提過）。談頻率時只寫「三維瀑布圖」。只有在明確指財務瀑布圖或腫瘤學瀑布圖時，才不必加重「三維」。
3. **歷史用限定語。** Koenig、Dunn、Lacy 1946〈The Sound Spectrograph〉《美國聲學學會期刊》18(1):19–49（同年 5 月先在美國聲學學會第 31 次會議報告；這篇的數位物件識別碼頁**無法確認、只記名、未核**）。Potter、Kopp、Green 1947《Visible Speech》（暫譯《看得見的語音》）。Gabor 1946 談時間與頻率不能同時無限精細（數位物件識別碼頁**無法確認、只記名**）：窗短則時間清楚、頻率糊；窗長則相反。梅爾刻度由 Stevens、Volkmann、Newman 1937 提出（數位物件識別碼頁**無法確認、只記名**）；現行公式「2595 × log10（1 ＋ 頻率 ÷ 700）」是後人彙整，**不是** 1937 年原文。R19 是約 1970–1990 年用來「燒」聲譜紙的 Kay Elemetrics 聲譜儀。
4. **窗越長，頻率越清楚、時間越糊（S3、R14、R15）。** 沒有一種窗長能同時分開兩者。S3（1000 與 1060 赫茲、敲擊在 1.00 與 1.02 秒；凹陷比兩峰中較低者再低 3 分貝以上才算「分得開」）：窗 8／64／512 毫秒，兩音的凹陷是 0.0／29.0／76.4 分貝，兩次敲擊的凹陷是 61.6／0.0／0.0 分貝。R14 窗長 25 毫秒、R15 同一訊號窗長 1000 毫秒，頻率軸 0 都在上方。
5. **跨過變化點的窗會混出不存在的頻率（S8）。** 64 點、取樣率 1000 赫茲，前 32 點 125 赫茲、後 32 點 250 赫茲；窗長 16 點、每次移動 8 點，7 個窗、9 個頻率格，窗中心 8、16、24、32、40、48、56 毫秒。各窗最亮依序 125、125、125、187.5、250、250、250 赫茲。第 4 窗跨過切換點，125 赫茲 −5.6 分貝、250 赫茲 −5.5 分貝，最亮反而落在中間的 187.5 赫茲。第 1 窗 125 赫茲＝0.0 分貝、250 赫茲＝−60.0 分貝；旁漏使 62.5 與 187.5 赫茲約為最大值的 0.25 倍。
6. **線性色彩看不到弱成分（S4）。** 500／1500／2500 赫茲，振幅 1／0.01／0.001。1500 赫茲的功率只有最大值的 0.0001（＝ 10^(−40／10)），線性色條上趨近 0，只看得到 500 赫茲；改成分貝才看得到 −40.0 與 −60.0 分貝（1.1 秒以後的中位數；這張下限 −100 分貝）。
7. **先看色條，也先看軸（R2、R14、R15、R17）。** Praat 預設越黑越強，與「越亮越強」相反。彩虹色盤容易把中段黃綠讀成「特別強」（本稿建議，不是定理）；比對變強變弱不要只用紅、綠（X 第 14 則就是這種差異圖）。R17 同一段口哨聲四格：左上是頻譜圖，但時間在縱軸（0–12 秒）、頻率在橫軸（0–3000 赫茲），和步驟 8 的方向相反；右上是基礎的三維瀑布圖；下面兩格是藏住被擋線條的三維瀑布圖，左下線性、右下分貝。
8. **頻率軸會改你看到的比例（S5）。** 公式 2595 × log10（1 ＋ f／700）：1000 赫茲＝1000.0 梅爾、8000 赫茲＝2840.0 梅爾。1000 赫茲以下的高度，線性軸是 12.5%（＝ 1000 ÷ 8000，所以練習檔的取樣率必須維持 16000 赫茲），梅爾軸是 35.2%。線性適合讀機械振動與諧波間距；對數適合跨好幾個數量級（鳥鳴 R7、聲景 R18）；梅爾適合語音、也常當機器學習的輸入。Audacity **目前**說明書（2026-09-02 版）預設梅爾刻度，分析機械頻率要改線性；舊版預設可能不同。
9. **只看頻譜會把先後看成同一件事（S7）。** 訊號甲前 1 秒 400 赫茲、後 1 秒 1200 赫茲；訊號乙兩音同時、振幅各約 1／√2。兩條平均頻譜在 400 與 1200 赫茲的峰值相差 0.0／0.0 分貝；頻譜圖才看得出一先一後、一同時。大陸「频谱图」常指這種沒有時間軸的頻譜，查資料時要分開（用法歸納，未核）。
10. **新亮線只告訴你「多了哪些頻率」，不說明原因（S6）。** 虛構馬達：固定線 29.5／59.0／88.5／120 赫茲；新成分落在 107.422 赫茲那一格。0–30 秒中位數 −53.0 分貝，第一個高出中位數 10 分貝的窗中心是 35.84 秒，最後一窗 −11.3 分貝。107 ÷ 29.5 ≈ 3.6，**不是整數倍**，不要推論是哪個零件。120 赫茲與電源的關係對到 Tsypkin 2013（60 赫茲供電下，感應馬達常見 2 倍電源頻率的振動；50 赫茲供電則常是 100 赫茲）——這篇的數位物件識別碼頁**無法確認、只記名**，內文依作者公開上傳的全文核過。人耳大約 20–20000 赫茲對到 MedlinePlus〈聽力檢查〉。空壓機情境的取樣率、窗長、107 赫茲都是教學示範，沒有真實案例。
11. **授權與隱私從嚴。** 頻譜圖丟掉相位，仍可能估回接近原本的聲音（Griffin & Lim 1984；數位物件識別碼頁**無法確認、只記名**），含說話內容的不要公開。**R7 是 CC BY 3.0 的錄音，要標 Justin Jansen，不是公有領域**（機器可讀欄的 Public domain 只是軟體畫的外框）。**R13**（雙中子星合併 GW170817 的啁啾）：維基共享資源寫 CC0、作者欄 LSC／Alex Nitz，與 LIGO 圖片使用政策（加州理工學院、麻省理工學院以外單位的圖，商業用途有限制）互相衝突，CC0 **無法證實**——從嚴：**只放連結、不嵌圖**。共享資源那一頁可開，所以連到頁面；兩個 LIGO 頁面是「無法確認」，只記名、不連結。
12. **原圖問題照錄不改；目測與譯名未核。** R7 檔案頁窗長寫「16348」，Audacity 2.1.2 程式碼的窗長是 2 的次方，應是 16384 的筆誤，**照錄不改**。R17 左下角殘留游標座標「86, -23.4105」（開頭被圖框切掉一截），是原圖標示問題。R20 右側刻度標到 50 且沒有單位，論文第 2.3 節寫重新取樣到 64 赫茲、頻譜圖最高 32 赫茲，50 代表什麼**無法證實**。R2／R3／R5／R9／R16 作者欄空白。R2 音節、R3 共振峰讀數、R5 揉弦、R6 音高、R8 快速脈衝、R20 深睡亮帶都是目測，未核。R7、R11 的中文鳥名、蝙蝠名未核。X 貼文數字未核；第 8 則「語音淆」文意無法證實；第 13 則是產業動態，不做投資判斷。

## When

- 快速振盪、成分會隨時間變的訊號（聲音、機械振動、腦波、地震波、重力波），想看「什麼時間出現哪些頻率、各多強」
- 要找新出現或消失的頻率（故障特徵、聲景裡突然的飛機或動物）；語音的共振峰、閉鎖與爆破；或要做梅爾頻譜圖當模型輸入
- 情境（課程稿，數字只是示範）：工廠空氣壓縮機馬達，固定時段、相同負載記 60 秒振動；旁邊放一張正常日、同一套設定的圖，再對某一格的時間序列加警示線
- **不適合**：變化慢、沒有振盪（營收、長期氣溫 → 折線）；取樣太稀，高於取樣率一半的頻率會折返成假的低頻；讀者要精確數值（改頻譜或加標註）；想要時間和頻率同時極精細（做不到）；只需要整段平均、不在乎先後（畫頻譜即可——但有時序時只看頻譜會誤判，S7）

## Recommend

- **主選**：橫軸時間、縱軸頻率、顏色＝分貝；時間向右、頻率向上、0 在下方；色條寫明越亮越強或越黑越強；圖說寫明六項：取樣率、窗長、窗函數、重疊、分貝基準、頻率刻度
- **口述步驟**（素材包第 7 節）：
  1. 先確認取樣率。最高可看頻率＝取樣率的一半；錄音或量測時先濾掉高於一半的成分，否則會折返成假的低頻
  2. 選窗長。頻率格間隔＝取樣率 ÷ 窗長點數。Praat 說明書：5 毫秒（預設）是寬頻、頻寬約 260 赫茲；30 毫秒是窄頻、約 43 赫茲。不確定就並排兩到三個窗長
  3. 選窗函數。一般用漢寧窗。Audacity 與 librosa 預設漢寧；SciPy 舊版頻譜圖功能預設 Tukey 窗——換工具要核對預設
  4. 決定重疊。史丹佛 CCRMA 教材寫常見 25–50%；本包模擬圖用 50% 或 75%。重疊越高越平滑，也越慢
  5. 每個窗算功率再換分貝。寫明 0 分貝的基準（本包模擬圖＝全圖最大功率；R1＝數位滿刻度）；設下限（例如 −80 分貝）。Audacity 說明書預設增益 20 分貝、範圍 80 分貝（2026-09-02 版）
  6. 選頻率軸：線性、對數或梅爾。Audacity 目前說明書預設梅爾；機械頻率改線性
  7. 選顏色：亮度單調變化（本包模擬圖是黑、紫、橘到淡黃），不建議彩虹；附色條；變強變弱不要只用紅綠
  8. 畫軸與標註：時間向右、頻率向上、0 在下；六項設定寫進圖說；關鍵線用文字或箭頭，不只靠顏色
  9. 給機器學習用時通常改畫梅爾頻譜圖。librosa 0.11.0 預設取樣率 22050 赫茲、窗長 2048 點、每次移動 512 點、漢寧窗。比對時固定同一套設定
  10. 公開前想隱私：含說話內容的頻譜圖不要隨意公開
- **工具誠實**：不寫程式可用 Audacity、Praat；寫程式可用 SciPy（官方建議改用短時傅立葉轉換 `ShortTimeFFT`，舊的 `spectrogram` 標成舊版）或 librosa。以上只列連結，**本 repo 未實測**。模擬圖的畫圖腳本沒有收進來。
- **參數與判準範例（範例，不是標準）**：

| 項目 | 數值與出處 | 性質 |
|---|---|---|
| 功率與分貝 | 週期型漢寧窗；功率＝快速傅立葉轉換結果的平方；分貝＝10 × log10（功率 ÷ 最大功率）；0 分貝＝最亮；分貝四捨五入到小數一位 | 本包模擬圖的定義 |
| 色條下限 | 一般 −80 分貝；S2 每張小圖用自己的最大值當 0 分貝；S4 下限 −100；S8 下限 −60 | 範例，不是標準 |
| 窗長取捨 | S3：8／64／512 毫秒 → 兩音凹陷 0.0／29.0／76.4 分貝，敲擊凹陷 61.6／0.0／0.0 分貝；低 3 分貝以上才算分開 | 範例，不是標準 |
| Praat | 5 毫秒寬頻、頻寬約 260 赫茲；30 毫秒窄頻、約 43 赫茲 | 說明書範例 |
| 重疊 | CCRMA：常見 25–50%；模擬圖 50% 或 75% | 常見做法，不是標準 |
| Audacity | 預設漢寧窗、增益 20 分貝、範圍 80 分貝、頻率軸預設梅爾 | 2026-09-02 說明書；舊版可能不同 |
| librosa 0.11.0 | 取樣率 22050 赫茲、窗長 2048、移動 512、漢寧窗 | 該版預設 |
| SciPy | 舊版頻譜圖預設 Tukey 窗；官方建議改 `ShortTimeFFT` | 預設會隨版本變 |
| 梅爾公式 | 2595 × log10（1 ＋ f／700）；1000 赫茲＝1000.0 梅爾、8000 赫茲＝2840.0 梅爾 | 後人彙整，不是 1937 原文 |
| 聽力範圍 | 約 20–20000 赫茲 | MedlinePlus，不是頻譜圖的軸範圍 |

## 與鄰近圖種的區別

本表是素材包的概述，除標明出處者外沒有逐項查證來源。

| 圖種 | 一格（或一點）代表 | 顏色或位置代表 | 和頻譜圖的關係 |
|---|---|---|---|
| 頻譜圖（本稿） | 一個時間窗 × 一個頻率格 | 顏色＝分貝 | — |
| 頻譜（spectrum；本 repo 無專檔） | 一個頻率 | 高度＝能量 | 把頻譜圖沿時間平均壓成一條線，就看不出先後（S7） |
| 一般熱圖（[`matrix-heatmap.md`](matrix-heatmap.md)） | 列 × 欄任一表格 | 顏色＝數值 | 頻譜圖是熱圖的一種：列＝頻率、欄＝時間窗；格子是算出來的，而且要先取捨窗長 |
| 千層麵圖（[`lasagna-plot.md`](lasagna-plot.md)） | 一個對象 × 一個時間點 | 顏色＝數值 | 千層麵圖每列是個體，列序可以重排；頻譜圖每列是頻率，順序固定 |
| 地平線圖（[`horizon-chart.md`](horizon-chart.md)） | 一個時間點 | 折疊色帶＝數值 | 地平線圖填的是單一序列的數值；頻譜圖先拆成許多頻率再上色 |
| 遞迴圖（[`recurrence-plot.md`](recurrence-plot.md)） | 時間 × 時間 | 黑＝兩個時間點的狀態夠近 | 兩者都能找週期。頻譜圖把週期變成頻率（週期＝1 ÷ 頻率），但要先選窗長；遞迴圖不必先知道週期 |
| 日曆熱圖（[`calendar-heatmap.md`](calendar-heatmap.md)）、螺旋圖（[`spiral-plot.md`](spiral-plot.md)） | 一天或一個時間點 | 顏色＝數值 | 先假設週期已知（週、年）再排版；頻譜圖把各頻率攤開，讓讀者自己找週期 |
| 河流圖（[`streamgraph-composition.md`](streamgraph-composition.md)；課程稿稱串流圖） | 一個時間點 × 一個類別 | 厚度＝數量 | 都在看成分隨時間變。河流圖的類別是人定的、用厚度；頻譜圖的「類別」是連續頻率、用顏色 |
| 管制圖（[`control-chart.md`](control-chart.md)） | 一個時間點 | 位置＝數值，另加管制界限 | 管制圖盯單一數值；頻譜圖盯每一個頻率（S6 那種新亮線） |
| 等高線圖（[`contour-density.md`](contour-density.md)） | 兩軸上的座標 | 等值線 | 都是用兩軸呈現第三個量；頻譜圖用連續顏色，等高線用線 |
| 小波量值圖（scalogram；無專檔） | 一個時間 × 一個尺度 | 顏色＝強度 | 低頻用長窗、高頻用短窗；縱軸不是頻率（R16） |
| 三維瀑布圖（waterfall plot，暫譯；無專檔） | 一個時間窗的整條頻譜 | 高度＝能量 | 資料與頻譜圖相同，改成立體堆疊；前面的峰會擋住後面（R17） |
| 財務瀑布圖（[`waterfall-bridge.md`](waterfall-bridge.md)） | 一個增減項目 | 浮動直條＝貢獻 | 同名不同物，不是頻率分析 |
| 腫瘤學瀑布圖（見 [`swimmer-plot.md`](swimmer-plot.md)） | 一位病人 | 排序直條＝腫瘤變化 | 同名不同物，不是頻率分析 |

判斷口訣：**快速振盪、想看什麼時間有哪些頻率 → 頻譜圖；只想要整段平均 → 頻譜；列是人、欄是時間 → 千層麵圖；想看何時回到相近狀態、又不想先假定週期 → 遞迴圖；頻率分析的立體堆疊 → 三維瀑布圖，不要寫成財務瀑布圖。**

## Avoid

- 把頻譜叫成頻譜圖，或把大陸「频谱图」當成有時間軸（S7）
- 只試一個窗長；用跨過變化點的窗去讀「當時的頻率」（S3、S8）
- 用線性色彩呈現落差很大的聲音（S4）；不寫 0 分貝的基準
- 不看色條就假設越亮越強（R2）；用彩虹色盤；變強變弱只用紅綠
- 沒看軸就把頻率 0 當成在下方、時間當成在橫軸（R14、R15、R17）
- 把小波量值圖的尺度讀成頻率（R16）
- 把三維瀑布圖、財務瀑布圖、腫瘤學瀑布圖當成同一種圖
- 用新亮線推論是哪個零件（S6：107 ÷ 29.5 ≈ 3.6，不是整數倍）
- 把含說話內容的頻譜圖公開（Griffin & Lim 1984，出處頁未核）
- 把 R7 當成公有領域；嵌入或轉載 R13（授權衝突，只連不嵌）
- 改掉原圖筆誤（R7「16348」、R17「86, -23.4105」、R20 刻度 50）
- 把梅爾公式說成 1937 年原文；把 X 貼文當教學依據（只作連結）

## Produce checklist

- [ ] 確認是等間隔的時間域訊號，取樣率已知；高於一半的頻率已先濾掉
- [ ] 選窗長（必要時並排兩到三個）、窗函數、重疊；頻率軸選線性／對數／梅爾
- [ ] 功率換分貝，寫明 0 分貝基準與下限；色條方向寫明；不用彩虹、不只用紅綠
- [ ] 時間向右、頻率向上、0 在下（若故意反過來，圖說要寫）
- [ ] 圖說六項：取樣率、窗長、窗函數、重疊、分貝基準、頻率刻度；關鍵線用文字或箭頭
- [ ] 比較時固定同一套設定；新頻率只報「多了哪一格」，不推論零件
- [ ] 譯名用限定語（大陸「频谱图」常指頻譜、未核；三維瀑布圖是暫譯）
- [ ] R7 標 CC BY 3.0、Justin Jansen；R13 只連不嵌；原圖筆誤照錄；模擬圖標「模擬」、數字虛構

## 虛構 demo 資料

素材包的 8 組時間域訊號合計 12,452,663 位元組（約 12.5 MB；S6 單獨 5,916,292 位元組，約 5.9 MB）。本 repo **沒有**收原始長度，收的是縮小版：`sample-spectrogram-s1-anatomy` … `sample-spectrogram-s8-steps`，各 CSV＋selfcheck，共 16 檔。檔名已有 `spectrogram` 前綴，與 `examples/data/` 既有檔**無撞名**。8 個 CSV 合計 **1,167,877 位元組（約 1140.5 KiB）**，單檔最大是 S6 的 217,651 位元組（約 212.5 KiB，不到 220 KB）。`draw_spectrogram.py` 與 `export_samples.py` **沒有收進本 repo**。

縮小後，課程稿裡 S1–S8 的關鍵讀數仍由自檢重算出來（只有格子數，以及 S5 的開頭基頻檢查，跟全長訊號不同，見下表）。自檢以明確檔名讀 CSV（`read_cols("sample-spectrogram-sN-….csv")`，從腳本所在資料夾讀，無 glob），只用 Python 標準函式庫（自寫週期型漢寧窗與基數 2 的快速傅立葉轉換，不靠 numpy）。我在 `examples/data/` 與暫存資料夾各跑一次，8 支都是 `RESULT: PASS`、結束碼 0（通過項數 10、11、22、8、11、15、9、14）。

縮小方式（帶限重取樣＝整段做快速傅立葉轉換、丟掉新奈奎斯特頻率以上的成分、再反轉換，等於理想低通，然後每隔若干點留一點）：

| 檔 | CSV 位元組 | 列數 | 縮小方式與設定 |
|---|---:|---:|---|
| S1 `sample-spectrogram-s1-anatomy.csv` | 114864 | 8000 | 帶限重取樣 8000→4000 赫茲（每 2 點留 1 點，整段）。窗 256 點（仍是 64 毫秒）、移動 64 點（16 毫秒）。窗數仍 122、頻率格間隔仍 15.625 赫茲；頻率格 257→129。欄位 `sample,x` |
| S2 `sample-spectrogram-s2-four-patterns.csv` | 145960 | 3200 | 取樣率仍 8000 赫茲，截取第 6400–9599 點（0.8–1.2 秒），**保留原取樣點編號**。窗數 47（全長是 247）。欄位 `sample,pure_1000hz,chirp_200_3000hz,click_1s,harmonics_300hz` |
| S3 `sample-spectrogram-s3-window-tradeoff.csv` | 164854 | 11264 | 取樣率仍 8000 赫茲，截取第 0–11263 點（0–1.408 秒）。窗長 64／512／4096 點的窗數是 701／85／8。凹陷算法用到的窗都還在，所以凹陷分貝與全長相同。欄位 `sample,x` |
| S4 `sample-spectrogram-s4-linear-vs-db.csv` | 123619 | 8192 | 截取第 4096–12287 點（0.512–1.536 秒），保留原編號。窗數 61。欄位 `sample,x` |
| S5 `sample-spectrogram-s5-linear-vs-mel.csv` | 204142 | 12800 | 取樣率**維持 16000 赫茲**（12.5%＝1000 ÷ 8000 靠它），截取第 16000–28799 點（1.0–1.8 秒），保留原編號。窗數 97。全長的「開頭基頻約 150 赫茲」在這段變成「截取起點約 200 赫茲（150 ＋ 100 × 1.0 ÷ 2）；300 赫茲以下最亮格是 187.5 赫茲」。欄位 `sample,x` |
| S6 `sample-spectrogram-s6-motor-fault.csv` | 217651 | 15000 | 帶限重取樣 2000→250 赫茲（先去掉 125 赫茲以上，每 8 點留 1 點）。窗 256 點（仍是 1.024 秒）、移動 128 點。窗數仍 116、頻率格間隔仍約 0.977 赫茲；頻率格 1025→129。欄位 `sample,x` |
| S7 `sample-spectrogram-s7-spectrum-vs-spectrogram.csv` | 193794 | 8000 | 帶限重取樣 8000→4000 赫茲。窗 256 點、移動 64 點，窗數 122。欄位 `sample,signal_a,signal_b` |
| S8 `sample-spectrogram-s8-steps.csv` | 2993 | 64 | **與素材包逐位元相同**，沒有再縮小。欄位 `sample,x,data_status` |

自檢腳本位元組：S1 4961、S2 5570、S3 6251、S4 4902、S5 5584、S6 5358、S7 5725、S8 5420。

**CSV 格式：** 第 1 行是 `# 虛構資料，數字未核｜…`。S1–S7 **沒有**每列的 `data_status` 欄（列數上千，虛構標記放在第 1 行；跟較早的 MA 圖、LocusZoom 樣本把標記放在檔頭的做法相同）。S8 仍保留 `data_status`。縮小後的訊號值以約 6 位有效數字寫入（不補尾端的 0，所以有的格子看起來不到 6 位）；S8 是未縮小的正弦取樣，位數較多（例如 √2／2 寫成 0.707106781187）。

**以實際計數為準**（自檢從縮小檔重算，與上列關鍵讀數一致；沒有改課程稿的數字）：(1) 虛構資料，**數字未核**；(2) S1 最亮格 437.5 赫茲，1203.125 赫茲那一格高於 −20 分貝的窗中心是 0.8–1.408 秒；(3) S2 啁啾在 1 秒最亮格 1593.75 赫茲（理論 1600），敲擊最亮窗中心 1.0 秒，諧波 10 條；(4) S5 自檢另確認 1.2–1.6 秒、5000–7000 赫茲的嘶聲比其他時間亮 6 分貝以上（實跑差距 8.6 分貝）；開頭 8 窗最亮是 187.5 赫茲，不是全長訊號的約 150 赫茲；(5) S8 第 4 窗 −5.6／−5.5 分貝，最亮 187.5 赫茲。

## 參考連結

只連來源清單裡標「可開」的網址（67 條全部連結，含 22 則 X 貼文）。打不開 0 條。以下 9 條**只記名、標未核、不連結**（網站拒絕自動連線、持續轉址或無法連線；不代表頁面不存在，但不當依據。其中 7 篇的書目在 Crossref 查得到）：

- **無法確認（9，未核）：** Koenig、Dunn、Lacy 1946〈The Sound Spectrograph〉數位物件識別碼頁；Gabor 1946〈Theory of communication〉數位物件識別碼頁；Stevens、Volkmann、Newman 1937 梅爾刻度原文數位物件識別碼頁；Harris 1978〈談窗函數〉數位物件識別碼頁；Griffin & Lim 1984 數位物件識別碼頁；Abbott 等 2016《物理評論快報》116:061102 數位物件識別碼頁（R12 的論文頁）；Tsypkin 2013 數位物件識別碼頁；LIGO 圖片頁（雙中子星合併 GW170817 頻譜圖的原始出處）；LIGO 圖片使用政策頁。

**名稱、定義與工具**

- [英文維基百科〈Spectrogram〉](https://en.wikipedia.org/wiki/Spectrogram)
- [英文維基百科〈Short-time Fourier transform〉（短時傅立葉轉換）](https://en.wikipedia.org/wiki/Short-time_Fourier_transform)
- [英文維基百科〈Mel scale〉（梅爾刻度）](https://en.wikipedia.org/wiki/Mel_scale)
- [英文維基百科〈Formant〉（共振峰）](https://en.wikipedia.org/wiki/Formant)
- [英文維基百科〈Waterfall plot〉（三維瀑布圖）](https://en.wikipedia.org/wiki/Waterfall_plot)
- [中文維基百科〈时频谱〉（簡體頁，又稱声谱图）](https://zh.wikipedia.org/wiki/%E6%97%B6%E9%A2%91%E8%B0%B1)
- [國家教育研究院樂詞網：spectrogram 各領域譯名](https://terms.naer.edu.tw/search/?match_type=phrase&query_field=title&query_term=spectrogram&query_op=)
- [人工智慧術語網站 aiterms.tw〈spectrogram〉](https://aiterms.tw/terms/spectrogram)
- [臺灣博碩士論文知識加值系統：成功大學 2007（寫「傅立葉正弦時頻圖」）](https://ndltd.ncl.edu.tw/handle/18733076855061725787)
- [SciPy 舊版頻譜圖函式說明（官方標為舊版）](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html)
- [SciPy 短時傅立葉轉換 `ShortTimeFFT`（官方建議改用這個）](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.ShortTimeFFT.html)
- [librosa 0.11.0 梅爾頻譜圖說明](https://librosa.org/doc/0.11.0/generated/librosa.feature.melspectrogram.html)
- [Praat：把聲音轉成頻譜圖的設定](https://www.fon.hum.uva.nl/praat/manual/Sound__To_Spectrogram___.html)
- [Praat Intro 3.2：寬頻與窄頻](https://www.fon.hum.uva.nl/praat/manual/Intro_3_2__Configuring_the_spectrogram.html)
- [Audacity 使用手冊：頻譜圖檢視](https://manual.audacityteam.org/man/spectrogram_view.html)
- [Audacity 使用手冊：頻譜圖設定（預設值）](https://manual.audacityteam.org/man/spectrogram_settings.html)
- [史丹佛 CCRMA，Julius O. Smith〈Spectrograms〉](https://ccrma.stanford.edu/~jos/mdft/Spectrograms.html)
- [西門菲莎大學聲音研究手冊〈Spectrograph〉](https://www.sfu.ca/sonic-studio-webdav/handbook/Spectrograph.html)

**會議、書與可核對的出處**

- [1946 年美國聲學學會第 31 次會議議程（PDF）](https://languagelog.ldc.upenn.edu/myl/SpectrographSession1946.pdf)
- [Google 圖書：Potter、Kopp、Green 1947《Visible Speech》](https://books.google.com/books?id=j3Q0AAAAIAAJ)
- [美國地質調查局：地震測站 24 小時頻譜圖](https://earthquake.usgs.gov/monitoring/spectrograms/24hr/)
- [Audacity 2.1.2 程式碼：窗長為 2 的次方（R7「16348」筆誤的對照）](https://github.com/audacity/audacity/blob/Audacity-2.1.2/src/prefs/SpectrogramSettings.cpp)
- [MedlinePlus〈聽力檢查〉：人耳約 20–20000 赫茲](https://medlineplus.gov/ency/article/003341.htm)
- [R20 來源：Li 等 2022（PMC9141573）](https://pmc.ncbi.nlm.nih.gov/articles/PMC9141573/)
- [Melcón 等 2012《公共科學圖書館：綜合》（R10 來源論文）](https://doi.org/10.1371/journal.pone.0032681)
- [Seong、Kim、Kim 2024 軸承故障（PMC10857163）](https://pmc.ncbi.nlm.nih.gov/articles/PMC10857163/)

**R 圖來源頁（只連到頁面，不嵌圖）**

- [圖 R1：十九世紀語音「nineteenth century」](https://commons.wikimedia.org/wiki/File:Spectrogram-19thC.png)
- [圖 R2：Praat 畫的「ta ta ta」](https://commons.wikimedia.org/wiki/File:Praat-spectrogram-tatata.png)
- [圖 R3：母音 [i]、[u]、[ɑ] 的共振峰](https://commons.wikimedia.org/wiki/File:Spectrogram_-iua-.png)
- [圖 R4：同一句話的波形與頻譜圖](https://commons.wikimedia.org/wiki/File:Spectrogram_-_It_Rains_a_Lot_in_Portland.png)
- [圖 R5：小提琴](https://commons.wikimedia.org/wiki/File:Spectrogram_of_violin.png)
- [圖 R6：大山雀鳴唱](https://commons.wikimedia.org/wiki/File:Parus_major_sonagram.jpg)
- [圖 R7：歌鶯鳴唱（中文俗名未核；錄音 CC BY 3.0，不是公有領域）](https://commons.wikimedia.org/wiki/File:Hippolais_polyglotta_song_spectrogram.png)
- [圖 R8：海豚哨音與喀聲](https://commons.wikimedia.org/wiki/File:Dolphin1.jpg)
- [圖 R9：座頭鯨的歌](https://commons.wikimedia.org/wiki/File:Humpback_song_spectrogram.png)
- [圖 R10：藍鯨叫聲與中頻主動聲納](https://commons.wikimedia.org/wiki/File:Example_of_Blue_Whales%27_D_calls_in_presence_of_MFA_sonar_-_Melc%C3%B3n_et_al._2012.png)
- [圖 R11：北棕蝠回聲定位（中文俗名未核）](https://commons.wikimedia.org/wiki/File:Eptesicu_nilssonii_echolocation_call.PNG)
- [圖 R12：第一次偵測到的重力波 GW150914](https://commons.wikimedia.org/wiki/File:LIGO_measurement_of_gravitational_waves.svg)
- [維基共享資源頁：雙中子星合併 GW170817 的重力波頻譜圖（只放連結、不嵌圖）](https://commons.wikimedia.org/wiki/File:GW170817_Gravitational_Wave_Chirp_Spectrogram.jpg)
- [圖 R14：窗長 25 毫秒](https://commons.wikimedia.org/wiki/File:STFT_colored_spectrogram_25ms.png)
- [圖 R15：同一訊號、窗長 1000 毫秒](https://commons.wikimedia.org/wiki/File:STFT_colored_spectrogram_1000ms.png)
- [圖 R16：小波量值圖（對照，不是頻譜圖）](https://commons.wikimedia.org/wiki/File:Scaleogram.png)
- [圖 R17：口哨聲的頻譜圖與三維瀑布圖](https://commons.wikimedia.org/wiki/File:Waterfall_plot_of_a_whistle.png)
- [圖 R18：雷尼爾山聲景](https://commons.wikimedia.org/wiki/File:Mount_Rainier_soundscape.jpg)
- [圖 R19：Kay Elemetrics 聲譜儀](https://commons.wikimedia.org/wiki/File:Sonagraphe.jpg)

**連結統計：** 76 個網址＝可開 67＋打不開 0＋無法確認 9。來源清單檔共 83 行，其中 7 行是 `#` 說明。可開 67 條全部連結（其中 X 貼文 22 條）；9 條只記名未核。

### X 貼文（只作連結，不當教學依據）

以 X 官方搜尋再以官方貼文讀取逐則讀回 **22 則**（英文 14、中文 6〔簡體 1、繁體 5〕、日文 2）；**沒有翻完所有頁**。數字一律未核，僅轉載。第 8 則原文另有「語音淆」，文意無法證實。第 13 則（BigVGAN 第二版）是產業動態，不做投資判斷。第 11 則的 89%、第 13 則的速度、第 22 則的赫茲數都未核。

1. [@Bob_Baxley](https://x.com/Bob_Baxley/status/697977115019448320)
2. [@keunwoochoi](https://x.com/keunwoochoi/status/1054374286155227139)
3. [@MacaulayLibrary](https://x.com/MacaulayLibrary/status/1077262701682929664)
4. [@TDataScience](https://x.com/TDataScience/status/1163624692357443586)
5. [@CosmicInglewood](https://x.com/CosmicInglewood/status/1251903111557378049)
6. [@museumsvictoria](https://x.com/museumsvictoria/status/1324124702294437888)
7. [@ailemon_me](https://x.com/ailemon_me/status/1368792397111459840)
8. [@mkpoli](https://x.com/mkpoli/status/1458261268775649281)
9. [@JenishRudani](https://x.com/JenishRudani/status/1553672973575262209)
10. [@reminous_](https://x.com/reminous_/status/1575445057993609216)
11. [@aimedadviser](https://x.com/aimedadviser/status/1612993351292440577)
12. [@yifever](https://x.com/yifever/status/1737516889239351737)
13. [@reach_vb](https://x.com/reach_vb/status/1813181163126587830)
14. [@harlos0517](https://x.com/harlos0517/status/1933280829754781789)
15. [@AnushkaSharad](https://x.com/AnushkaSharad/status/1937719650457997373)
16. [@may_natSakura](https://x.com/may_natSakura/status/2052298863843987556)
17. [@yujiroyonetsu](https://x.com/yujiroyonetsu/status/2098667176186216788)
18. [@SoundPapers](https://x.com/SoundPapers/status/2100072606703448200)
19. [@rohit3a](https://x.com/rohit3a/status/2102475769079541827)
20. [@momi_au](https://x.com/momi_au/status/2104080859980767518)
21. [@kcimc](https://x.com/kcimc/status/2105081448160227678)
22. [@AnimalBattStats](https://x.com/AnimalBattStats/status/2105687005401137322)

鄰居 pattern：`matrix-heatmap.md`（一般熱圖；頻譜圖是頻率 × 時間窗的特例，格子是算出來的）、`lasagna-plot.md`（列＝個體、可以重排；頻譜圖列＝頻率、不能調）、`horizon-chart.md`（單一數值的折疊色帶）、`recurrence-plot.md`（時間 × 時間的相似方陣；不必先知道週期）、`calendar-heatmap.md`、`spiral-plot.md`（先假設週期再排版）、`streamgraph-composition.md`（人定類別、用厚度）、`control-chart.md`（盯單一數值）、`contour-density.md`（等值線，不是連續色）、`waterfall-bridge.md`（財務瀑布圖，不是三維瀑布圖）、`swimmer-plot.md`（提及腫瘤學瀑布圖，也不是三維瀑布圖）。

## 圖檔與授權（不複製，只連結）

課程稿嵌 **27** 張＝真實／示意圖 R1–R12、R14–R20（19 張）＋自繪模擬 S1–S8（8 張，虛構資料，數字未核）。**R13 不嵌圖。** 本 repo **不複製任何圖檔**，只連到來源頁；引用時保留作者與授權。

授權以 2026-10-08（台北）用維基共享資源 API 與 Europe PMC REST API 重查的結果為準，與素材包一致：

- **R1** 公有領域，Aquegg（男聲 “nineteenth century”；0 分貝基準是數位滿刻度）。
- **R2** CC BY-SA 3.0，作者欄空白（無法證實）。Praat 灰階，越黑越強。
- **R3** CC BY 2.0，作者欄空白（無法證實）。共振峰讀數是目測，未核。
- **R4** CC BY 2.0，Aaron Parecki。
- **R5** CC BY-SA 3.0，作者欄空白（無法證實）。揉弦是目測，未核。
- **R6** CC BY-SA 3.0，Maxime Metzmacher（素材包另記錄音者 Chantal Dengis）。音高是目測，未核。
- **R7** **錄音 CC BY 3.0，標示 Justin Jansen；不是公有領域。** 機器可讀欄的 Public domain 只涵蓋軟體畫的外框，檔案頁寫錄音是 CC BY 3.0，從嚴整張依 CC BY 3.0。窗長「16348」照錄（應為 16384 的筆誤）。中文鳥名未核；對數刻度。
- **R8** CC BY-SA 3.0，Spyrogumas。快速脈衝是目測，未核。
- **R9** CC BY-SA 3.0，作者欄空白（無法證實）。
- **R10** 共享資源標 CC BY 2.5，期刊標 CC BY 4.0；Melcón 等 2012。
- **R11** CC BY-SA 3.0，Rauno Kalda。中文蝙蝠名未核。
- **R12** CC BY 3.0，Abbott 等（LIGO Scientific Collaboration 與 Virgo）；事件 GW150914。論文的數位物件識別碼頁無法確認，只記名。
- **R13 只放連結、不嵌圖。** 共享資源寫 CC0、作者欄 LSC／Alex Nitz，與 LIGO 圖片使用政策衝突，CC0 無法證實。共享資源頁可開（見上方連結）；LIGO 圖片頁與使用政策頁無法確認，只記名、不連結。
- **R14、R15** CC BY-SA 3.0，Alessio Damato。窗長 25 毫秒對 1000 毫秒；頻率 0 在上方；彩虹色。
- **R16** 公有領域，作者欄空白（無法證實）。小波量值圖，縱軸是尺度 1–30，不是頻率。
- **R17** CC BY-SA 3.0，Greglocock。四格：頻譜圖（時間在縱軸）加三張三維瀑布圖。左下角「86, -23.4105」照錄。
- **R18** 公有領域，美國國家公園管理局（National Park Service），2019 年雷尼爾山聲景；三列、0–20 分鐘，對數刻度標 40／400／4000 赫茲。
- **R19** CC BY-SA 3.0，Maxime Metzmacher。Kay Elemetrics 聲譜儀。
- **R20** Europe PMC 的 `license` 欄是 “cc by”（版本 4.0 依素材包）；Li 等 2022，PMC9141573。右側刻度 50 無單位，與論文最高 32 赫茲對不上，照錄；深睡亮帶是目測，未核。
- **S1–S8** 自繪模擬，虛構資料，數字未核。色盤黑、紫、橘到淡黃；分貝定義見上表。圖檔不入庫。
