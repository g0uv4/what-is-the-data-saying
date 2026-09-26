# Pattern: spiral-plot

> **圖種**：螺旋圖（Spiral plot／Time series spiral）
> **來源（納茲教圖）**：`teach-viz/2026-09-26-pm-spiral.md`（方法教學；首次正式主課）
> **亦稱**：時間序列螺旋、時間螺旋；氣候傳播常見變體叫 climate spiral／temperature spiral（氣候螺旋）；Dataviz Project 另分出 Spiral Histogram（condegram）與 Spiral Heat Map
> **核心**：把時間（或具週期的序列）排在**阿基米德螺旋**上，**一圈＝一個週期**；通常中心較早、外圈較新；**同一角度對齊同一週期位置**（每年一月都在同一條放射線上），一眼看出季節性與跨年趨勢，並把很長的序列收進單一圓形版面

## When

- 問「長期走勢怎麼變」**同時**問「哪個季節／時段年年偏高或偏低、哪一年整圈形狀異常」
- 形狀：連續、排序正確的長時間序列（日、週、月），跨度數年以上；週期長度穩定（12 個月、52 週、7 天、24 小時），能寫成「一圈＝一年，角度＝月份」這類句子
- 大眾傳播、科普的氣候／環境時間序列（氣溫異常螺旋是經典例），但要標基準期與單位

## Recommend

- **主選**：螺旋圖（一圈＝一個週期、中心較早、外圈較新、外圈標週期刻度）
- **判讀**：沿螺旋的距離＝時間；同角度的內外圈＝不同年份同一時段；垂直軌道的高度、點位或色塊顏色＝數值；外圈刻度（12 個月或 52 週）＝對齊用
- **軌道編碼（同一家族，要標清楚是哪一種）**：
  - 比振幅高峰 → **螺旋長條／condegram** 或棒棒糖
  - 看連續起伏 → **螺旋折線／面積**（氣候螺旋多屬此類，半徑同時表示氣溫異常幅度）
  - 分級強度 → **螺旋熱圖**（每圈切固定弧段著色）；仍是螺旋時間軸，不是日曆方格牆或矩陣熱圖
  - 軌道窄又要看分布 → 軌道上的地平線圖編碼（進階；spiralize 有 `spiral_horizon`）
  - **多軌螺旋**：同一螺旋疊長條、文字、地平線等軌道（spiralize 範例常見）
  - **氣候螺旋**：角度＝月份，半徑與顏色＝相對基準期的氣溫異常，常做成動畫
- **輔助圖**：要精確比較兩個時間點（「今年七月比去年七月增減多少百分比」）→ 另附兩點數值對照表或線性折線局部放大；圈數太密 → 縮減年份、拉大軌道間距或做成動畫
- **備選（何時改用哪一種）**：
  - 只看整體趨勢、不疊季節，或要精讀細微差值 → **折線圖**（`time-series-trend.md`）或表格
  - 每日一值、日曆簽到式紀錄（週 × 星期方格）→ **日曆熱力圖**（`calendar-heatmap.md`）
  - 任意兩個類別軸的交叉強度 → **矩陣熱圖**（`matrix-heatmap.md`）
  - 類別排名、少數類別比較 → 長條、棒棒糖（`lollipop-rank.md`）、**圓形長條圖**（`circular-bar.md`）
  - 封閉多軸指標形狀 → **雷達圖**（`radar-profile.md`）；扇形占比 → 南丁格爾玫瑰或圓餅家族
  - 多類別組成隨時間 → **河流圖**（`streamgraph-composition.md`）；流程或時程相依 → **甘特圖**（`gantt-schedule.md`）

## Avoid

- **沒寫週期定義或方向**：一圈代表什麼、由內而外是由早到晚還是相反，都要寫在圖上
- **把「一圈」講錯**：例如有 X 原帖寫「每一圈＝一個月」，實際是一圈＝一年、角度＝月份
- 氣候異常沒標**基準期**與單位
- 圈數過密糊成環狀色塊
- 忽略外圈弧長較長的扭曲，單憑目測圓弧距離判讀差值
- 週期不穩也硬畫 → 角度對齊失效，只剩裝飾性漩渦
- **與鄰近圖種混**：
  - 圓形長條圖／徑向長條：類別繞一圈各畫長條，通常一圈就結束；螺旋是連續時間捲成多圈、圈間對齊季節
  - 雷達圖／南丁格爾玫瑰：多變量或分類占比的封閉形狀；螺旋主軸是時間序列的週期對齊
  - 日曆熱圖／矩陣熱圖：方格排成日曆或任意行列；螺旋熱圖的方格嵌在螺旋弧段上
  - 河流圖／面積圖、甘特圖：水平線性時間軸；螺旋把過長時間軸捲起來並凸顯週期重疊
  - 地平線圖：可當螺旋軌道上的一種編碼，但本身不等於螺旋圖
- 編造工具支援：data-to-viz、Flourish、R Graph Gallery、Python Graph Gallery 本輪都**沒有**螺旋圖專頁

## Produce checklist

- [ ] 故事句含：長期走勢＋哪個週期位置反覆偏高／偏低（或哪一圈異常）
- [ ] 先確認需要「週期對齊＋長序列」；只看趨勢 → 折線
- [ ] 週期一句話寫在圖上（例如「一圈＝一年，角度＝月份」）＋方向（中心較早、外圈較新）
- [ ] 表：時間戳記排序正確、無重複；缺值處理寫明；需要時先彙總到與週期對齊的顆粒度（日 → 週／月）
- [ ] 軌道編碼四選一（長條／棒棒糖、折線／面積、螺旋熱圖色塊、地平線）並在圖注寫明
- [ ] 外圈角度刻度（月份或週次）；數值圖例（漸層色條或高度標尺，含單位）
- [ ] 氣候異常：寫基準期（例如 Hawkins 頁示例 1850–1900、NASA SVS 5190 為 1951–1980；數字未核）
- [ ] 資料來源；是否平滑或去除極端值寫一句
- [ ] 可讀性：圈數太密就縮年份、拉大圈距或做動畫；提醒讀者外圈弧長較長，精確差值看對照表或線性局部圖
- [ ] 工具誠實（只寫素材包證實的）：R `spiralize`（阿基米德螺旋專用；Gu 等，Bioinformatics 2021；軌道可放長條、折線、面積、色塊、地平線、樹）；D3 社群實作 tomshanley `d3-spiral-heatmap`、Condegram gist（非官方 Graph Gallery 專頁）；氣候螺旋範本 Ed Hawkins Climate Visuals（GIF／MP4，CC-BY 4.0）、NASA SVS 5190。data-to-viz／Flourish／R・Python Graph Gallery 無專頁
- [ ] 示範數字標「數字未核」
- [ ] 自檢：週期穩定嗎？讀者其實在比類別（→ 長條／圓形長條）、看日曆紀錄（→ 日曆熱力圖）、看任意交叉（→ 矩陣熱圖）嗎？

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-spiral.csv` — `month, year, month_num, rentals`；某城市 2017-01 至 2024-12 每月腳踏車租借次數（96 列＝8 圈 × 12 個月）。設定一圈＝一年、角度＝月份（`month_num`）、由內（2017）往外（2024）。示範讀法：一般年份夏高冬低（高峰多在 6–8 月、低谷在 1 月），年總量逐年緩增（約 71 萬 → 111 萬次）；**2020 那一圈形狀異常**——夏天沒有尖峰（7 月約 6.3 萬、為該年最低），冬天反而偏高（1 月約 8.4 萬、為該年最高）。要說「2024 年 7 月比 2023 年 7 月多幾 %」請另附對照表，不要目測螺旋。（終稿情境是逐日資料，這份先彙總到月）

## 參考連結（可點；皆出自素材包 sources.txt 第一段）

- https://datavizcatalogue.com/methods/spiral_plot.html （定義與解剖；螺旋長條示意）
- https://en.wikipedia.org/wiki/Climate_spiral （Hawkins 2016 氣候螺旋與後續延伸）
- https://en.wikipedia.org/wiki/Archimedean_spiral （sources.txt 註：稿內未標狀態，研究筆記記為 200）
- https://ed-hawkins.github.io/climate-visuals/spirals.html （全球氣溫、北極海冰螺旋；GIF／MP4，CC-BY 4.0）
- https://ed-hawkins.github.io/climate-visuals/ （sources.txt 註：稿內未標狀態，研究筆記記為 200）
- https://climatelabbook.substack.com/p/spiralling-global-temperatures （十年回顧）
- https://svs.gsfc.nasa.gov/5190/ （NASA SVS〈Climate Spiral 1880–Present〉；GISTEMP v4，基準期 1951–1980；數字未核）
- https://svs.gsfc.nasa.gov/5383 （NASA SVS〈Slow Reveal Graphs: Climate Spiral〉無標示版）
- https://svs.gsfc.nasa.gov/5057 （NASA SVS 舊版〈NASA Climate Spiral 1880–2022〉）
- https://jokergoo.github.io/spiralize/
- https://jokergoo.github.io/spiralize/articles/spiralize_intro.html （軌道編碼：長條、折線、面積、色塊、地平線）
- https://jokergoo.github.io/spiralize/articles/examples.html （ggplot2 下載量、氣溫、COVID、太陽黑子、系統發生樹）
- https://github.com/tomshanley/d3-spiral-heatmap
- https://bl.ocks.org/tomshanley/4080b28445785939b3f043b8c5b63e22 （D3 螺旋熱圖範例）
- https://gist.github.com/arpitnarechania/027e163073864ef2ac4ceb5c2c0bf616 （Condegram gist）
- https://dl.acm.org/doi/10.1145/288392.288399 （Carlis & Konstan〈Interactive Visualization of Serial Periodic Data〉，UIST 1998）
- X 解說／展示原帖（非程式教學）：https://x.com/Stellarixorine/status/2092833497723609199 （**注意**：原帖寫「每一圈＝一個月」有誤，應為一圈＝一年、角度＝月份）、https://x.com/MyZeroCarbon/status/2100623403065491568 （1880–2022 每月氣溫異常螺旋，附 NASA 連結）；本輪查無程式教學類原帖（不編造）
- 查核限制（未核內容）：https://datavizproject.com/data-type/spiral/ 、https://datavizproject.com/data-type/spiral-histogram/ 、https://datavizproject.com/data-type/spiral-heat-map/ （curl 讀取 403，Cloudflare 阻擋）；https://jokergoooo.shinyapps.io/covid19/ （spiralize COVID 互動應用，2026-09-26 查核時逾時）。另 Wikipedia 無 Spiral_plot 條目（404）、Observable condegram 等 notebook 429、原 Climate Lab Book 2016 文章無法連線、spiralize CRAN vignette 路徑 404（改用 GitHub Pages），僅記名不列為來源

鄰居 pattern：`time-series-trend.md`（線性折線；精讀差值、只看趨勢）、`calendar-heatmap.md`（日曆方格；螺旋熱圖的格子嵌在弧段上）、`matrix-heatmap.md`（任意行列交叉）、`circular-bar.md`（類別繞一圈，不是連續時間多圈）、`radar-profile.md`（多軸封閉形狀）、`streamgraph-composition.md`、`gantt-schedule.md`（線性時間軸）。

圖檔留在教圖／skill-pack（`/workspace/skill-packs/2026-09-26-pm-spiral/images/`，稿內嵌 26 張），本 repo **不複製**大圖。圖說照審稿修正版：nasa-spiral-sr 出自 NASA SVS 5383〈Slow Reveal Graphs: Climate Spiral〉無標示版、nasa-spiral-60s 出自 5057〈NASA Climate Spiral 1880–2022〉舊版（兩張都**不是** 5190）；spiralize 首頁的下載螺旋用 spiralize-ggplot2-downloads；intro-48＝沿軌道的 0 到 1 資料刻度、intro-3＝阿基米德螺旋基本曲線（圈距 d）、intro-35＝色塊（不是長條）、intro-37＝長條與依基準線分色長條、intro-38＝堆疊長條、intro-29＝折線、intro-32＝面積、intro-55＝地平線。其餘可對照 catalogue-top／catalogue-anatomy、wiki-hawkins-early-still／wiki-hawkins-2017／wiki-line-before（同資料線性折線對照）、hawkins-temp-still、hawkins-arctic-still、spiralize-example_*、spiralize-git_commit_r、spiralize-app-still、d3-spiral-heatmap。對帳見 `ATTRIBUTION.md`。
