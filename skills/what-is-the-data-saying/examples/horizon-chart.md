# Pattern: horizon-chart

> **圖種**：地平線圖（Horizon Chart）
> **來源（納茲教圖）**：`teach-viz/2026-10-03-am-horizon.md`（方法教學；正式課程；首次以地平線圖為主題）
> **亦稱**：horizon graph；R 語言套件常寫 horizon plot。學術文章與產品文件常把 chart 與 graph 混用；圖表標題請寫完整的「地平線圖（Horizon Chart）」。
> **核心**：把「相對基準的面積圖」切成等高的色帶，再疊回同一條矮條；**用顏色層數換垂直高度**，讓很多條時間序列擠進同一個畫面。
> **口訣**：色深＝層數＝離基準的幅度；矮條高度不是真實振幅。
> **一句話**：一條序列一列、共用時間軸，沿同一條垂直線往下掃，看誰偏離基準、哪個時間點很多列一起變深。
> **誠實提醒**：本課只講「怎麼讀、怎麼畫」。範例圖與本 repo 的練習資料都是虛構或示意，**數字未核**。
> **潤稿狀態**：素材包與教學稿都明說**沒有經過 Gemini 潤稿**（Gemini 登入失效），也沒有改用其他模型潤稿；文字是審稿後由人工整理的原稿。

## 十件必須釘清的事

1. **各函式庫的預設不同，不要寫成「多數預設鏡射」（這個說法不成立）。** 2026-10-03 逐頁核對：Cubism.js 預設 **offset**（預設 8 種顏色＝每側 4 帶；示範是綠色為正、藍色為負）；d3-horizon（vasturiano）預設 **offset**、預設 4 帶；latticeExtra 的 `horizonplot` 預設**鏡射**（低於基準的值翻到上方）、預設 3 帶；ggHoriPlot（R）的**鏡射要自己打開**（範例用單一色系、基準取最小值）；d3-horizon-chart（kmandov）的預設值素材包**沒有找到，無法證實**；Observable Plot 有示範、滑桿可選 2 到 8 帶（頁面一般抓取被擋，見查核限制）。讀別人的圖或自己選工具，先查設定。許多工具預設 3 到 4 帶，那是工具預設，不是實驗的建議（見第 2 點）。
2. **Heer 等人 CHI 2009〈Sizing the Horizon〉的實驗結論要帶著限定條件講。** 受試者是大學生與研究生：實驗一 **18** 位、實驗二 **30** 位、追加實驗 **8** 位。**只測了「比較兩個點的數值並估算差多少」**，沒有測趨勢判讀，所以不能拿來證明「看趨勢也是地平線比較好」。圖高低於約 **24 像素**時，2 帶的準確度比折線圖和不分層的鏡射圖好；圖高比較大時，作者建議用不分層的鏡射圖。固定圖高下分層會讓估算變慢、誤差變大（2 帶比折線圖平均慢約 2.05 秒）。**鏡射與 offset 的速度與準確度沒有顯著差異。** 帶數越多越慢：4 帶平均誤差約 5.64 單位，2 帶約 4.12、3 帶約 4.04；作者以 2 帶為主，**不建議 4 帶以上**，並建議圖高 6 像素以上就用 2 帶。（我另外下載論文全文檔逐項對過：18 位、30 位、追加 8 位受試者，24 像素，2.05 秒，5.64／4.12／4.04，6 像素，ACM 版權與個人或課堂用途複製的句子都在；Few 的文章我也另外讀過，Reijner 與「(and only when)」的句子都在。）
3. **「誰發明了地平線圖」各說各話，不要寫成定論。** 「Saito 等人最早」是 **Heer 論文自己的說法**（論文寫 Saito 等人以「two-tone pseudo-coloring」之名最先發展此技術，Panopticon 公司另外獨立商品化並命名；教學稿稱 Wikipedia 也這樣看）。Stephen Few 2008 年的文章（《Time on the Horizon》）寫的是：Hannes Reijner 是 Panopticon 地平線圖的**主要設計者**（原文：primarily responsible for the creation of the horizon graph），他重建的設計歷程用推測語氣（原文 must have taken），不是設計者本人的說法。Saito 2005 的全文**打不開**（DOI 只到 IEEE 轉址頁，要機器人驗證），教學稿只讀到摘要，而摘要沒有提到正負翻折或疊帶，所以「它的構造是否和今天的地平線圖完全一樣」**無法證實**。Heer、Kong、Agrawala 2009 做的是感知實驗，**不是發明者**。
4. **「要有十幾條以上才划算」是經驗法則，沒有出處**，不要當成研究結論引用。Few 的結論則是：只有在必須同時看、同時比較大量時間序列時，多付出的解讀成本才划算，並且坦承會失去連續的輪廓（他的示範是 50 條序列、全部共用同一量尺）。
5. **各列各自縮放，跨列比較顏色是常見錯誤。** 有些工具預設每列各自依自己的資料範圍決定尺度（latticeExtra 預設如此，要另外給數字才能跨格比較）；各列帶寬不同時，顏色深淺只能在同一列內比。要跨列比較，所有列共用同一個帶寬。本 repo 的練習資料示範：共用每帶 25 的量尺時，第 14 小時有 **3 台**進入外層帶；若每台改用自己最大偏離的一半當帶寬，會變成 **5 台**，多出來的兩台（machine_07 的 59.4、machine_12 的 58.0）只比基準高約 9.4 與 8.0 個百分點。
6. **矮條高度不等於真實振幅。** 振幅已被切帶疊回去，高度被刻意壓扁：2 帶時矮條高度只有原折線全距的 1/4（4 帶是 1/8）；模擬圖 S6 一帶高 0.61，只有折線全距 3.40 的約 18%。想讀精確數值，要靠游標互動或點進單條折線；地平線負責掃描，不負責對帳。
7. **顏色只看圖例。** 常見是藍正紅負（Data Viz Catalogue 部落格也這樣寫），但 Cubism 的示範是綠正藍負，Observable 與 ggHoriPlot 的範例是單一色系；圖例第一句寫「顏色深度＝層數＝幅度」，不要讓讀者把深色當成另一個類別。
8. **基準一定要寫在圖說裡，讀者才不會以為一定是 0。** 基準可以是 0、平均值、目標值、期初、滾動平均；同一份資料換基準，色帶的故事完全不同（模擬圖 S8：基準為 0 時全部是正值，基準為平均值時正負各約六成與四成）。Wikipedia 的歐洲溫室氣體示意圖（圖 R3）的基準是「相對歐洲平均」，不是「排放為 0」。要並排比較時，通常用相對起點的百分比變化，比絕對數值適合（Few 的示範就是相對首日的變化）。
9. **授權（圖與程式）**：三張 Commons 向量圖（R1–R3，作者 Alessandra Facchin）為 **CC BY-SA 4.0**，須標示作者與授權連結，改作須用相同授權；RAWGraphs 教學頁（R7）為 **CC BY-NC-SA 4.0，僅限非商業使用**；Cubism.js＝Apache 2.0、d3-horizon-chart（kmandov）與 d3-horizon（vasturiano）＝MIT、ggHoriPlot＝GPL-3、latticeExtra＝GPL-2 或 GPL-3，**以上只管程式碼，不管網頁截圖**；Heer 等人 2009 論文（R4）版權屬 ACM，個人或課堂用途可免費複製、不得為營利或商業利益散布、須附完整引用；Observable Plot 頁面（R10）**未標示授權**，無法證實可否轉載截圖；kmandov 首圖（R9）的圖片授權站方未另標；其餘網頁截圖（R5、R6、R8、R11、R12、R13）僅作教學示意。8 張模擬圖是素材包自畫的虛構資料。本 repo 不複製任何圖。
10. **別跟風景照片的「地平線」混淆，也別跟河流圖、山脊圖、熱圖搞混**（見下方鄰近圖種表）。

## When

- 要在同一條時間軸上一次掃過**很多條**時間序列，找出誰偏離基準、哪裡出現極端、哪個時間點很多條一起變深
- 版面高度有限，每一列只能給到幾十像素（Heer 等人的實驗：圖高低於約 24 像素時，2 帶的準確度才比折線圖好）
- 關心「相對基準的偏離」多於精確數值；精確數值留給游標或點進單條折線
- 典型情境：伺服器指標、感測器、多條百分比變化的監控牆；找「同步衝擊」（部署日、流量尖峰、天氣事件）
- 形狀：長表三欄（時間、序列識別、數值）；每條序列要有同一組時間點；先決定基準

## Recommend

- **主選**：地平線圖，一列一條序列、共用時間軸；左側放序列名，圖旁放「深度＝層數＝幅度」圖例
- **步驟（口述）**：
  1. 準備長表，決定基準，圖說寫清楚基準
  2. 每條先想成「相對基準的面積圖」，算每點與基準的差；單位要能比較
  3. 選正負處理：鏡射（負值翻到基準上方，用色相分正負）或 offset（負值從條頂往下長）；實驗裡兩者差不多
  4. 決定帶數與帶寬：**帶寬＝想蓋住的最大偏離 ÷ 帶數**；要跨列比較，所有列共用同一個帶寬
  5. 切帶：差的絕對值每滿一個帶寬算一層，第 1 層最淺、最外層最深
  6. 疊回同一條矮條；越深＝離基準越遠
  7. 配色與圖例：一切以圖例為準
  8. 垂直排成小多圖、共用時間軸；沿同一條垂直線往下掃，看同步衝擊
  9. 自檢兩個問題：把色帶關掉只留矮面積，還看得清極端嗎？（看不清才值得用地平線）讀者會不會把深色當成另一個類別？
- **變體**：鏡射與 offset；共用量尺與各列各自縮放（後者跨列不可比）；2 帶與 3、4 帶（2 帶為主）；基準取 0／平均／目標／期初
- **何時改用其他圖**：
  - 只有一到三條、又要讀精確數值 → 折線或面積圖加游標，見 [`time-series-trend.md`](time-series-trend.md)
  - 圖本身夠高（約 24 像素以上）→ 折線小多圖或不分層的鏡射圖更快、準確度也不輸，見 [`small-multiples.md`](small-multiples.md)
  - 時間軸對不齊 → 失去沿同一條垂直線比較的力量
  - 主打組成占比 → 堆疊面積圖或河流圖，見 [`streamgraph-composition.md`](streamgraph-composition.md)
  - 主打分布形狀 → 山脊圖、雨雲圖、蜂群圖，見 [`ridgeline-density.md`](ridgeline-density.md)、[`raincloud-combo.md`](raincloud-combo.md)、[`beeswarm-points.md`](beeswarm-points.md)
- **參數與判準範例（範例，不是標準）**：

| 項目 | 數值與出處 | 性質 |
|---|---|---|
| 帶數 | 以 2 帶為主；3 帶準確度相近但較慢；不建議 4 帶以上；圖高 6 像素以上就用 2 帶（Heer 等人 2009） | 範例，不是標準 |
| 工具預設帶數 | Cubism 每側 4 帶（8 種顏色）、d3-horizon 4 帶、latticeExtra 3 帶、Observable 滑桿 2–8 帶 | 工具預設，不是實驗建議 |
| 圖高轉折點 | 約 24 像素（6.8 毫米，作者的 14.1 吋螢幕）以下，2 帶比折線圖準；之上建議用不分層鏡射圖 | 範例，不是標準 |
| 帶寬 | 最大偏離 ÷ 帶數；範例資料基準 50、2 帶、每帶 25（外層帶＝與基準相差超過 25） | 範例，不是標準 |
| 矮條高度 | 2 帶＝折線全距的 1/4；4 帶＝1/8（同一量尺；模擬圖 S3 高度比 8：2：1） | 範例，不是標準 |
| 序列條數 | 「十幾條以上才划算」是經驗法則，沒有出處 | 範例，不是標準 |
| 模擬圖每列高度 | 20 像素（S7，低於 24 像素轉折點；只示範畫法，不重現實驗） | 範例，不是標準 |

## 與鄰近圖種的區別

| 圖種 | 它回答什麼 | 和地平線圖的區別 |
|---|---|---|
| 折線圖／面積圖小多圖（[`small-multiples.md`](small-multiples.md)） | 每條序列的精確形狀 | 每條都要夠高才讀得準；地平線把高度壓成 1/4（2 帶）或更矮，改用色層補幅度，代價是要解碼色帶、估算較慢；圖夠高時折線圖並不輸 |
| 矩陣熱圖（[`matrix-heatmap.md`](matrix-heatmap.md)） | 一格一色的二維表 | 熱圖常看不出沿時間的形狀；地平線保留時間形狀再加色層（Wikipedia 形容地平線圖「看起來像熱圖」） |
| 河流圖（[`streamgraph-composition.md`](streamgraph-composition.md)） | 多條序列**疊成一張**，看總量與組成，基線會飄 | 地平線一條序列一列，列與列不相加，看各自相對基準的偏離 |
| 山脊圖（[`ridgeline-density.md`](ridgeline-density.md)） | 多列密度或面積微微重疊，看形狀 | 地平線把色帶摺疊起來，看相對基準的漲跌強度；Observable Plot 把地平線圖當成山脊圖與面積小多圖的替代做法 |
| 螺旋圖（[`spiral-plot.md`](spiral-plot.md)） | 週期對齊的長序列 | 地平線可當螺旋軌道上的一種編碼，本身不等於螺旋圖 |

## Avoid

- 把色深當成另一個類別，而不是更大的偏離（模擬圖 S6 誤讀 A）
- 以為矮條高度＝真實振幅（S6 誤讀 B、S7）
- 死背藍正紅負，不看圖例
- 沒寫基準，讀者以為一定是 0（R3、S8）
- 只有兩三條卻用地平線
- 跨列比較顏色，但各列尺度不同（S4）
- 把 4 帶以上當成「更精細」，忽略 Heer 等人的結果（4 帶的誤差明顯變大）
- 把 Heer 的實驗（只測兩點數值比較）當成「看趨勢也是地平線比較好」的證據
- 把「Saito 發明了地平線圖」寫成定論（那是 Heer 論文的說法；Few 把 Panopticon 的主要設計者寫成 Reijner；Saito 全文未讀到）
- 把「十幾條以上才划算」當成有出處的標準；把「多數函式庫預設鏡射」寫出來
- 與風景照片的「地平線」混淆
- 把官方自述當實驗結果：Cubism 頁面寫「把 120 像素高的面積圖壓成 30 像素會損失 75% 的解析度，地平線圖縮減垂直空間不會損失解析度」，這是官方自述，不是實驗結果
- 把 X 搜尋結果當成「X 上沒人談」：教學稿的 X 搜尋（2026-10-03 約 10:02–10:03）找不到教學向地平線圖原帖，多為 METR 的 time horizon 能力曲線或無關影視、金融用語，**未引用**，之後沒有重跑

## Produce checklist

- [ ] 故事句：「很多條序列相對基準，誰偏高、誰偏低、哪裡出現極端、哪裡同步」
- [ ] 長表三欄（時間、序列、數值）；每條序列同一組時間點；單位可比較（並排時優先用相對起點的百分比變化）
- [ ] **基準寫在圖說**；說明是 0、平均、目標、期初或滾動平均
- [ ] 帶數以 2 帶為主；帶寬＝最大偏離 ÷ 帶數；**跨列比較時所有列共用同一個帶寬**，各列各自縮放要明講「跨列不可比」
- [ ] 鏡射或 offset 二選一並寫在圖說（兩者準確度無顯著差異）；圖例第一句寫「顏色深度＝層數＝幅度」，色相方向以圖例為準
- [ ] 每列高度壓到幾十像素；共用時間軸；左側序列名；精確數字留給游標或點進單條折線
- [ ] 解讀順序：先讀圖例與基準 → 看某列某段色帶變深 → 沿同一條垂直線看是否多列同時變深（集群級事件）→ 整列幾乎只有最淺一帶可略過 → 最後提醒「矮條高度不是真實振幅」
- [ ] 示範數字標「數字未核」；不放圖檔進 repo
- [ ] 工具誠實（只寫素材包證實的）：
  - **JavaScript**：Cubism.js（Square；D3 外掛，即時儀表板；Apache 2.0；預設 offset）；d3-horizon-chart（kmandov；瀏覽器端 Canvas；MIT；預設值未找到）；d3-horizon（vasturiano；MIT；預設 offset、4 帶）；Observable Plot 有示範（2–8 帶滑桿）
  - **R**：latticeExtra `horizonplot`（GPL-2 或 GPL-3；預設鏡射、3 帶、各格各自縮放）；ggHoriPlot（Iker Rivas-González；ggplot2；GPL-3；版本 1.0.1；鏡射自己打開）。R-bloggers 有〈What is a horizon chart?〉轉載
  - **不寫程式的路線**：RAWGraphs 教學頁（約 2 分鐘影片＋專案檔；範例為 2010 到 2020 年歐洲不同產品的價格變動，數字未核；頁面授權 CC BY-NC-SA 4.0，僅限非商業）
  - **沒找到專頁**：Plotly、data-to-viz、Data Viz Project 與 Data Viz Catalogue 的 methods 頁測試時都是 404（Data Viz Catalogue 只有部落格一小節提到地平線圖，請不要寫成「有完整專頁」）；404 只代表那些路徑測試時不存在，**不能推論這些站沒有地平線圖**
  - Excel、Google 試算表的做法素材包沒有查，不寫

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-horizon-fictional.csv` — 288 筆（約 13.7 KB）；沒有 `#` 說明行，只有一行欄位名；欄位 `hour, series, cpu_percent, data_status`；12 台機器（machine_01 到 machine_12）× 第 0 到 23 小時共 24 個時間點；處理器使用率介於 0.0 到 100.0；每列 `data_status` 都寫「虛構資料，數字未核」。基準固定 50、2 帶、每帶寬 25（外層帶＝與基準相差超過 25，即大於 75 或小於 25）。
- 我用 pandas **獨立重算**的數字（以實際計數為準；與素材包、selfcheck 的敘述逐項一致，**沒有發現素材包文字與 CSV 不一致**）：
  - 288 筆、12 台、24 個小時、無重複的（台、小時）組合、無缺值
  - 高於 50 的 **102** 筆（35.4%）、低於 50 的 185 筆（64.2%）、剛好等於 50 的 1 筆（0.3%，machine_07 第 3 小時）；三者相加 288
  - 外層帶合計 **5** 筆（約 1.7%）：第 14 小時 machine_03（92.1）、machine_06（100.0）、machine_09（89.6）共 3 筆；machine_11 第 3、4 小時（0.0、5.0）共 2 筆
  - **第 14 小時 3 台**（12 台的 25%）同步進入外層帶；其餘 23 個小時每小時最多 1 台（只有第 3、4 小時各 1 台，都是 machine_11）
  - 各自縮放（每台以自己最大偏離的一半當帶寬）時，第 14 小時進入各自外層帶的是 5 台（machine_03、06、07、09、12）
  - 有第 2 帶（外層帶）的點正好是上述 5 筆；2 帶剛好蓋住最大偏離 50，疊回不丟資訊
- 示範讀法：先讀圖例與基準（50）→ 第 14 小時 machine_03、06、09 的色帶最深 → 其他 9 台在該小時沒有進外層帶，這是「3 台同步」而不是全機群 → 但若各列各自縮放，會多出 machine_07 與 machine_12 兩台（只比基準高約 8 到 9 個百分點）→ 這是跨列比較的常見錯誤。
- `sample-horizon-selfcheck.py` — 自檢腳本（只用 Python 標準函式庫；以腳本旁的**明確檔名**讀 CSV，不搜尋檔案；全部用 `assert`）；見 `examples/data/README.md`。
- 素材包另附 `draw_horizon.py`（產生 8 張模擬圖）：**本 repo 不收**，只在 `ATTRIBUTION.md` 註明它存在於素材包。我查過：它**預設把圖寫進 `/workspace/teach-viz/`**（會覆蓋教學稿圖檔），只有給第一個參數才改輸出資料夾；它不讀 CSV（資料是腳本內產生的虛構波形）；需要 numpy、matplotlib、Pillow 與 Noto Sans CJK 字型。我只在暫存資料夾執行，輸出指向 `/tmp`，8 張圖與素材包 `images/` 內的模擬圖 MD5 逐一相同。

## 參考連結（可點；皆出自素材包 sources.txt 且標可開）

- 條目與詞彙：https://en.wikipedia.org/wiki/Horizon_chart ；R-bloggers 轉載〈What is a horizon chart?〉https://www.r-bloggers.com/2022/03/what-is-a-horizon-chart/ ；Data Viz Catalogue 部落格〈Area Graphs and their Variations〉（文內一小節提到 Horizon Charts，通常正值用藍、負值用紅；**該站沒有地平線圖專頁**）https://datavizcatalogue.com/blog/area-graphs/
- 論文與文章：Heer、Kong、Agrawala，CHI 2009〈Sizing the Horizon〉論文頁 https://idl.uw.edu/papers/horizon （頁面標示 Best Paper Award）、全文檔 https://idl.cs.washington.edu/files/2009-TimeSeries-CHI.pdf ；Stephen Few 2008《Time on the Horizon》https://perceptualedge.com/articles/visual_business_intelligence/time_on_the_horizon.pdf
- 圖片頁與授權（作者 Alessandra Facchin）：https://commons.wikimedia.org/wiki/File:Horizon-chart-from-area-chart.svg 、https://commons.wikimedia.org/wiki/File:Horizon-chart_example.svg 、https://commons.wikimedia.org/wiki/File:European_greenhouse-emission_2012-2021.svg ；授權條款 https://creativecommons.org/licenses/by-sa/4.0
- 工具文件：Cubism.js https://square.github.io/cubism/ ；d3-horizon-chart（kmandov）https://kmandov.github.io/d3-horizon-chart/ （專案首圖 http://kmandov.github.io/d3-horizon-chart/img/d3-horizon-charts-lead-01.png ）；d3-horizon（vasturiano）https://github.com/vasturiano/d3-horizon ；ggHoriPlot https://cran.r-project.org/package=ggHoriPlot 、https://cran.r-project.org/web/packages/ggHoriPlot/index.html 、說明文件 https://cran.r-project.org/web/packages/ggHoriPlot/vignettes/ggHoriPlot.html 、真實資料範例 https://cran.r-project.org/web/packages/ggHoriPlot/vignettes/examples.html 、原始碼 https://github.com/rivasiker/ggHoriPlot ；latticeExtra https://cran.r-project.org/web/packages/latticeExtra/index.html 、`horizonplot` 說明頁 https://rdrr.io/cran/latticeExtra/man/horizonplot.html
- 操作教學：RAWGraphs〈How to make a horizon graph〉（CC BY-NC-SA 4.0，僅限非商業）https://rawgraphs.github.io/learning/how-to-make-a-horizon-graph/
- 查核限制（未核；僅記名、不列連結，皆**不是已驗證的來源**；素材包 sources.txt 32 條中這 10 條標「打不開」）：ACM 的 Heer 論文 DOI `10.1145/1518701.1518897`（HTTP 403，回應為驗證頁；改用上面的論文頁與全文檔）；IEEE 的 Saito 等人 2005 論文 DOI `10.1109/INFVIS.2005.1532144`（轉到 IEEE 後要機器人驗證，內文讀不到，論文內容無法證實）；Observable Plot 的 horizon 示範頁（HTTP 429 請求過多；素材包改讀公開筆記原始碼，本 repo 沒有另行開啟，頁面未標示授權）；Data Viz Project 的 `horizon-chart` 頁、data-to-viz 的 `horizon.html`、Plotly 的 `/python/horizon/`、Data Viz Catalogue 的 `methods/horizon_chart.html`（以上四個 HTTP 404）；Commons 舊檔名頁 `File:Horizon_Graph_Construction.png` 與 Commons 分類頁 `Category:Horizon_charts`（兩個 404）；作者 kjytay 個人網站的 horizon chart 文章（404；R-bloggers 轉載可開）
- 連結統計：sources.txt 32 條（去重）＝可開 22（**全部連結**，另含 kmandov 首圖的圖檔網址與 CC BY-SA 4.0 授權條款頁）＋打不開 10（只記名）；沒有「可開但刻意不連結」的網址。

鄰居 pattern：`small-multiples.md`（折線小多圖；圖夠高時不輸地平線）、`time-series-trend.md`（單條折線加游標）、`matrix-heatmap.md`（一格一色）、`streamgraph-composition.md`（組成疊加、基線漂移）、`ridgeline-density.md`（形狀重疊）、`spiral-plot.md`（地平線可當螺旋軌道上的編碼）；Heer 論文與 Few 文章的實驗與設計討論只在本檔轉述；`control-chart.md`（管制圖：單一指標的中心線、管制界限與判異規則；本檔擅長並排比較很多條序列）、`lasagna-plot.md`（千層麵圖：每列一格一色而非折疊折線；Wicklin 2025 認為汽油價格用千層麵圖更好讀）。

圖檔留在教圖／skill-pack（`/workspace/skill-packs/2026-10-03-am-horizon/images/`，21 張＝13 張真實／示意圖加 8 張模擬圖，圖說與教學稿逐字相同；教學稿原規劃的第 14 張真實圖〔Data Viz Catalogue 部落格截圖〕因沒拍到 Horizon 小節而未採用，所以是 21 張，不是 22 張），本 repo **不複製**任何圖。可對照的圖：R1 構造五步圖（CC BY-SA 4.0）、R2 Commons 多序列例圖（13 列、2010–2020 年；CC BY-SA 4.0）、R3 歐洲 29 國溫室氣體相對歐洲平均（含冰島、挪威、瑞士；CC BY-SA 4.0；基準是歐洲平均）、R4 Heer 論文第 1 圖（ACM 版權，僅教學示意）、R5 IDL 論文頁截圖、R6 Cubism 落地頁（綠正藍負）、R7 RAWGraphs 教學頁（CC BY-NC-SA 4.0 僅限非商業）、R8 kmandov 專案頁首（只拍到頁首，沒有實際圖表）、R9 kmandov 手繪風首圖（授權站方未標）、R10 Observable Plot 畫廊頁（未標授權）、R11 ggHoriPlot CRAN 頁、R12 ggHoriPlot 真實資料範例頁（單一桃色系、基準取最小值）、R13 latticeExtra 說明頁；模擬圖 S1 構造四步、S2 鏡射與 offset（圖內底註寫明各工具預設）、S3 2 帶與 4 帶（高度比 8：2：1）、S4 十二列監控牆（各列各自縮放）、S5 正負色帶與圖例、S6 常見誤讀、S7 每列 20 像素的折線小多圖與地平線、S8 基準選擇（圖內底註的「絕對股價」意思是「絕對數值」，與投資無關）；皆**模擬資料**、數字未核。對帳見 `ATTRIBUTION.md`。
