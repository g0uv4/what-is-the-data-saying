# Pattern: flame-graph

> **圖種**：火焰圖（Flame Graph）
> **來源（納茲教圖）**：`teach-viz/2026-09-27-pm-flamegraph.md`（方法教學；首次正式主課）
> **亦稱**：堆疊火焰圖；英文固定寫 Flame Graph（Brendan Gregg 命名，2011 年發明、2011 年 12 月公開發布）。**Flame Chart（火焰時序圖）是不同的圖**，見下
> **核心**：對**堆疊取樣**（或等價的已收合堆疊計數）做合併：每個矩形＝一個堆疊框（函式／方法／符號名），**寬度＝該框在整份剖面樣本人口中出現的多寡**，愈寬愈「熱」；垂直＝堆疊深度；**橫軸是依函式名稱字母排序、把相同堆疊前綴合併後的人口軸，不是時間**
> **出處**：Brendan Gregg〈The Flame Graph〉，《ACM Queue》14(2)，2016，DOI 10.1145/2927299.2927301；轉載《Communications of the ACM》59(6)，2016 年 6 月，頁 48–57，DOI 10.1145/2909476

## When

- 問「CPU／記憶體／阻塞時間主要耗在哪些**呼叫路徑**、各約占多少樣本」——要同時看見葉熱點與整條祖先鏈
- 形狀：帶呼叫堆疊的取樣剖面，或已收合（folded）成「堆疊路徑 → 計數」的等價資料（每行 `根;…;葉 樣本數`）；多次樣本；符號／除錯資訊盡量齊備
- 多執行緒／多程序剖面想在一張合併圖上看總體熱路徑；優化前後、版本前後做回歸比對（差異火焰圖）

## Recommend

- **主選**：火焰圖（標準布局根在下、葉在上；頂緣「沒有再往上疊」的寬框通常就是正在佔用資源的熱點，其下方是呼叫祖先）
- **變體（同一家族，要標清楚）**：
  - **CPU 火焰圖**：on-CPU 堆疊取樣；原版顏色是**隨機暖色**（紅／橙／黃），只用來區隔相鄰框與細塔，**沒有資料意義**
  - **Memory 火焰圖**：寬度改為位元組或配置次數；示例常用綠色系示意「不是 CPU」
  - **Off-CPU 火焰圖**：執行緒不在 CPU 上時的阻塞、等待、喚醒鏈路；適合「CPU 不忙但延遲很高」
  - **Hot/Cold 火焰圖**：同圖兼看 on-CPU 與 off-CPU；官方頁說明仍屬實驗性、不易解讀
  - **Differential（差異）火焰圖**：兩份剖面相減，常用紅＝變多、藍＝變少
  - **冰柱布局（inverted／icicle layout）**：同一資料上下顛倒（根在上）；許多互動工具預設如此，以免堆疊太深時根被捲出畫面。**這仍是火焰圖，不是冰柱圖**（見下）
  - **FlameScope**：先看「秒 × 次秒偏移」熱力圖找週期／突發，再框選時段生成火焰圖
- **互動**：懸停看全名與百分比、點選水平放大、搜尋高亮並顯示累計占比
- **備選（何時改用哪一種）**：
  - 要「何時發生、順序與空隙」→ **火焰時序圖（Flame Chart）**／時間軸軌跡（Chrome 開發者工具 Performance 面板主執行緒、speedscope Time Order），或兩圖並陳
  - 一般商業階層組成（營收類別、組織預算），讀者預期冰柱／樹狀讀法 → **冰柱圖**（`hierarchy-icicle.md`）、矩形樹狀（`treemap-composition.md`）、旭日（`sunburst-hierarchy.md`）
  - 沒有堆疊、只有扁平計數表 → 長條或表格，不要假造堆疊
  - 網路誰連誰 → 力導向／弧線／鄰接矩陣／`biofabric.md`；流向與階段 → 桑基／沖積／弦圖

## 火焰圖 vs 火焰時序圖 vs 冰柱圖（必讀分界）

| | 火焰圖（Flame Graph，本檔） | 火焰時序圖（Flame Chart） | 冰柱圖（Icicle，`hierarchy-icicle.md`） |
|---|---|---|---|
| 橫軸 | 合併後的**樣本人口**；依函式名稱**字母排序**以最大化合併；**不是時間** | **時間順序** | 父節點寬度內依子節點**數值占比**切分（組成） |
| 合併 | 相同堆疊前綴合併成同一寬框；同一函式不同時間出現也併在一起 | 幾乎不合併，保留每次呼叫的先後與空隙 | 不是取樣合併；是階層加總（父＝子之和） |
| 資料 | 帶堆疊的取樣剖面／已收合堆疊計數 | 帶時間戳的呼叫軌跡 | 任意 parent–child／path＋非負數值 |
| 故事 | 效能熱路徑：誰最常出現在堆疊上 | 某段時間內誰先跑、跑多久、哪裡空轉 | 隸屬組成：預算、組織、檔案系統怎麼切 |
| 例 | brendangregg/FlameGraph、d3-flame-graph、speedscope Left Heavy | Chrome 開發者工具 Performance 主執行緒、speedscope Time Order | 預算／科目樹、庫存樹 |

- 火焰圖可上下顛倒成「冰柱布局」，外觀就像冰柱圖——但判斷圖種看**資料與坐標軸**，不看方向：拿任意階層加總表畫成「往上長」不會變成效能火焰圖
- Plotly 把「往上長」的 partition 方向叫 flame chart：那只是冰柱圖顛倒方向的別名，**不是**堆疊取樣火焰圖，也不是 Chrome 那種時序圖
- 有工具把時序圖誤標成 flame graph；維基百科條目也說瀏覽器開發工具內建「火焰圖」，但 Chrome 官方文件稱 Performance 主執行緒為 flame chart（x＝時間）——以官方文件與 Gregg 官方頁為準

## Avoid

- **把顏色當溫度或數值**：原版 CPU 暖色是隨機的；Memory 綠、Differential 紅／藍才是刻意色票，要看圖例
- **把橫軸當時間**：左右順序是字母排序、用來合併；同一函式不同時間出現會併成同一寬框
- **把火焰時序圖和火焰圖混稱**（Chrome 開發者工具、speedscope Time Order 是時序圖）
- **看到像冰柱就當階層組成圖**，或拿任意階層加總表硬做成「效能火焰圖」
- 只盯單一座塔：同一函式可能散在多座塔，要用搜尋累加
- 不同行為的時段（週期、突發）混在一起平均：先用次秒熱力圖挑時段
- 符號／除錯資訊不全，塔變矮或滿是 `[unknown]` 還照樣下結論
- 只看 CPU 火焰圖：CPU 塔很瘦但延遲高時補 Off-CPU 火焰圖
- 介面上的百分比、毫秒、樣本數未複核就當事實；對外用「約略占剖面樣本的一截」，精確百分比另附表與取樣條件
- 讀者無法接受「x 不是時間」又沒時間說明讀法時硬上

## Produce checklist

- [ ] 故事句是「熱路徑／樣本人口」，不是「時間順序」；要問第幾毫秒誰先跑 → 火焰時序圖
- [ ] 取得帶堆疊的剖面（例：Linux perf／eBPF、DTrace、產品化剖析器、語言執行環境取樣器）；取樣頻率與時長蓋住關心的負載；符號齊備
- [ ] 收合堆疊：每次樣本 → 「根;…;葉 計數」一行，同一路徑計數加總
- [ ] 布局：標準火焰（根在下）或冰柱布局（根在上），或讓讀者切換；圖注寫明
- [ ] 色票：CPU 隨機暖色（註明無資料意義）／Memory 綠色系／Differential 紅＝增加、藍＝減少／混合模式依語言分色（例：Netflix Java in Flames 綠＝Java、黃＝C++、紅＝系統）
- [ ] 互動：懸停全名與百分比、點選水平放大、搜尋累計占比
- [ ] （可選）負載有週期或突發 → FlameScope 類次秒熱力圖先挑時段
- [ ] 解讀順序：最寬頂緣葉框 → 往祖先讀誰呼叫它 → 搜尋累加同名函式 → 與計數表對帳
- [ ] 圖旁一句讀法：「寬＝合併後的樣本占比，高＝堆疊深度，橫向不是時間；同一函式在不同時間出現會被併成同一個寬框」
- [ ] 取樣條件（剖析器、頻率、時長、時段）寫進圖注
- [ ] 工具誠實（只寫素材包證實的）：`brendangregg/FlameGraph`（`flamegraph.pl` 等，輸出互動 SVG；檔頭 CDDL 1.0，版權 2011 Brendan Gregg 與 Joyent）；`spiermar/d3-flame-graph`（D3 互動版）；speedscope（Jamie Wong；Time Order／Left Heavy／Sandwich）；FlameScope（Netflix）；Chrome 開發者工具 Performance 只作火焰時序圖對照。後三者與 d3-flame-graph 的授權素材包未寫，不代填。Dataviz Catalogue、data-to-viz、Dataviz Project 無專頁
- [ ] 示範數字標「數字未核」
- [ ] 自檢：讀者會不會把橫軸讀成時間、把顏色讀成溫度？資料真的是堆疊樣本，還是其實是一般階層組成（→ 冰柱）？

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-flamegraph.txt` — **已收合堆疊（folded stacks）純文字，不是 CSV**：每行 `函式;函式;…;函式 樣本數`，共 27 行、總樣本 3,626；情境是虛構 API 後端伺服器 `api_server` 尖峰延遲。檔內不加註解，可直接餵給火焰圖工具（例：`flamegraph.pl`、speedscope）。示範讀法：最寬熱路徑是 `main → event_loop → handle_request → route_dispatch → orders_handler → serialize_response → json_encode → escape_string → utf8_validate`；葉框 `utf8_validate` 1,342 樣本（約 37%），`orders_handler` 底下的 `serialize_response` 整支 2,335 樣本（約六成多）；另有資料庫讀取、驗證、寫回應、背景工作、`gc_thread` 等較窄的塔。`escape_string` 也出現在 `users_handler` 那座塔——用搜尋才會累加到

**轉成階層表（若要餵冰柱／樹狀工具或對帳）**：每行最後一個空白前是路徑、後面是計數。以 `;` 切路徑 → 每行得到一個葉節點的 **self 樣本數**；把路徑的每個前綴都當成一個節點，節點的 **total 樣本數**＝所有以它為前綴的行計數加總（例：`…;serialize_response` total＝它底下 5 行相加 2,335）。可整理成 `path, parent, name, self, total` 表，`total` 當寬度。注意：這樣畫出來的是「堆疊樣本的階層表」，意義仍是效能樣本占比，不會因此變成一般組成用的冰柱圖；而一般商業階層表反過來也不能當成效能火焰圖。

## 參考連結（可點；皆出自素材包 sources.txt 第一段）

- https://www.brendangregg.com/flamegraphs.html （官方總頁：x＝堆疊剖面人口、常依字母排序、不是時間；區分 Icicle 與 Flame Chart）
- https://www.brendangregg.com/FlameGraphs/cpuflamegraphs.html
- https://www.brendangregg.com/FlameGraphs/memoryflamegraphs.html
- https://www.brendangregg.com/FlameGraphs/offcpuflamegraphs.html
- https://www.brendangregg.com/FlameGraphs/hotcoldflamegraphs.html
- https://www.brendangregg.com/blog/2014-11-09/differential-flame-graphs.html
- https://corpaul.github.io/flamegraphdiff/ （差異火焰圖三圖對照）
- https://www.brendangregg.com/flamescope.html
- https://www.brendangregg.com/blog/2018-11-08/flamescope-pattern-recognition.html （sources.txt 註：稿內未標狀態，研究筆記記為 200）
- https://www.brendangregg.com/Articles/Netflix_FlameScope_20180404.pdf （sources.txt 註：稿內未標狀態，研究筆記記為 200）
- https://github.com/Netflix/flamescope
- https://medium.com/netflix-techblog/netflix-flamescope-a57ca19d47bb
- https://github.com/brendangregg/FlameGraph
- https://github.com/spiermar/d3-flame-graph
- https://github.com/jlfwong/speedscope
- https://www.speedscope.app/ （Time Order＝時序圖讀法；Left Heavy＝火焰圖讀法；Sandwich）
- https://cacm.acm.org/magazines/2016/6/202665-the-flame-graph/fulltext （CACM 轉載；會轉址到下一條）
- https://cacm.acm.org/practice/the-flame-graph/ （上一條的轉址目標；sources.txt 註：稿內未單獨標狀態）
- https://cacm.acm.org/research/the-flame-graph/
- https://netflixtechblog.com/java-in-flames-e763b3d32166 （Java 混合模式火焰圖）
- https://developer.chrome.com/docs/devtools/performance/reference （對照：Performance 面板 flame chart，x＝時間）
- https://en.wikipedia.org/wiki/Flame_graph （注意：條目稱瀏覽器開發工具內建火焰圖一句不採用，見上）
- 查核限制（未核內容、僅記名不列連結）：ACM Queue〈The Flame Graph〉原文頁與附圖下載 403（未讀）；錯誤 DOI 路徑 `10.1145/2927301` 的 ACM 數位圖書館頁 404；正確 DOI 10.1145/2927299.2927301 的 ACM 數位圖書館頁只回 cookie 檢查頁（未讀全文）；Dataviz Catalogue、data-to-viz、Dataviz Project 無火焰圖專頁（404）；Gregg 部落格若干舊式連字號日期網址 404（一律改用斜線日期路徑）；官方站 CPU 混合模式示例點陣圖 404（研究時改用對應 SVG）

X 教學原帖：本輪查無（含限定 Brendan Gregg 帳號的查詢；不編造）。

鄰居 pattern：`hierarchy-icicle.md`（**不同圖種**：一般階層組成；火焰圖的冰柱布局只是方向相同）、`sunburst-hierarchy.md`、`treemap-composition.md`、`circle-packing.md`（階層份額形狀，非堆疊取樣）、`time-series-trend.md`（要時間順序時的線性對照；時序呼叫看火焰時序圖）、`matrix-heatmap.md`（FlameScope 的次秒熱力圖屬時間 × 次秒矩陣）、`sankey-flow.md`、`biofabric.md`（流向／網路，不是呼叫堆疊）。

圖檔留在教圖／skill-pack（`/workspace/skill-packs/2026-09-27-pm-flamegraph/images/`，稿內嵌 23 張，其中 1 張 SVG），本 repo **不複製**大圖。火焰圖範例對照：bg-cpu-mysql-crop、bg-cpu-bash、bg-cpu-mysql-filt、bg-example-perf.svg（CPU）；bg-mem-faultpages、bg-mem-mallocbytes（Memory 綠色系）；bg-offcpu-mysqld、bg-offcpu-wakeup（Off-CPU）；bg-hotcold-kernel（Hot/Cold；bg-hotcold-figure 是執行緒狀態轉換說明圖，不是火焰圖）；bg-diff-rm、bg-diff-corpaul（差異）；d3-screenshot；speedscope-leftheavy；netflix-java-hero（混合模式分色）；wiki-mediawiki-1280。**時序圖對照（不是火焰圖）**：chrome-flame-chart、speedscope-timeorder。文字剖面對照：bg-cpu-bash-profile、bg-cpu-mysql-stacks。FlameScope 次秒熱力圖：flamescope-heatmap-annotated、flamescope-02-annotated、flamescope-pattern-montage。對帳見 `ATTRIBUTION.md`。
