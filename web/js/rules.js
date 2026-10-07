/*
 * WIDS recommendation rules — data-driven table for all patterns (69 as of v0.3.31).
 * Derived from skills/what-is-the-data-saying/references/chart-heuristics.md
 * (決策表 + 形狀 → 圖捷徑) and data-shape-checks.md (欄位角色 + 結構探測).
 *
 * Each rule:
 *   id        pattern slug (= examples/<id>.md)
 *   zh / en   chart name
 *   requires  min/max column counts by type. 'label' = category|id.
 *   need      hints that must ALL hold ('a|b' = either). Each met need +NEED_BONUS.
 *   prefer    bonus hints (+PREFER_BONUS each)
 *   avoid     penalty hints (−AVOID_PENALTY each), shown as caveats
 *   base      prior (simple, direct charts first — "優先選能直接回答問題的最簡單圖")
 *   fields    zh / en description of the required field combination
 *   why       zh / en one-line rationale (from the heuristics tables)
 *   render    [] of { r: rendererKey, preset?: {...} } — empty = teaching only
 *
 * Works in browsers (window.WIDS_RULES) and Node (module.exports).
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.WIDS_RULES = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var NEED_BONUS = 20, PREFER_BONUS = 10, AVOID_PENALTY = 15;

  // ---------------------------------------------------------------- hints
  // Labels used to explain a recommendation.
  var HINTS = {
    time:               { zh: '有日期／時間欄', en: 'has a date/time column' },
    longSeries:         { zh: '時間點 ≥ 24 個（長序列）', en: '≥ 24 time points (long series)' },
    cycle:              { zh: '長序列且跨多個穩定週期', en: 'long series spanning several stable cycles' },
    daily:              { zh: '每日一值、日數 ≥ 60', en: 'daily values, ≥ 60 days' },
    multiSeries:        { zh: '時間 + 少數系列（2–8）', en: 'time + few series (2–8)' },
    manySeries:         { zh: '時間 + 多系列（> 8）', en: 'time + many series (> 8)' },
    wideSeries:         { zh: '寬表：多個同尺度數值欄當系列', en: 'wide table: several same-scale numeric series' },
    rankOverTime:       { zh: '時間 + 實體 + 可排名度量', en: 'time + entity + rankable measure' },
    compositionOverTime:{ zh: '時間 + 類別 + 非負量（組成隨時間）', en: 'time + category + non-negative amount' },
    oneRowPerCat:       { zh: '一個類別一列 + 數值', en: 'one row per category + value' },
    fewCats:            { zh: '類別少（≤ 6）', en: 'few categories (≤ 6)' },
    manyCats:           { zh: '類別多（> 12）', en: 'many categories (> 12)' },
    repeatedGroups:     { zh: '每組多筆觀測（類別 + 連續數值）', en: 'several observations per group' },
    bigGroups:          { zh: '每組樣本 ≥ 15', en: '≥ 15 observations per group' },
    smallN:             { zh: '總筆數不多（≤ 300），每點可見', en: 'small n (≤ 300), every point visible' },
    crossTab:           { zh: '類別 × 類別 → 一個值（可樞紐成矩陣）', en: 'category × category → value (pivotable)' },
    bigMatrix:          { zh: '矩陣格數 ≥ 20', en: '≥ 20 matrix cells' },
    smallCross:         { zh: '外層 3–8 × 內層 3–7', en: 'outer 3–8 × inner 3–7' },
    twoCats:            { zh: '兩個低基數類別欄（≤ 8）', en: 'two low-cardinality category columns' },
    multiCatStages:     { zh: '≥ 3 個低基數類別欄（階段）', en: '≥ 3 low-cardinality category columns' },
    noNumeric:          { zh: '沒有數值欄（以計數為值）', en: 'no numeric column (counts)' },
    nonNegative:        { zh: '數值全非負', en: 'all values non-negative' },
    signed:             { zh: '數值有正有負', en: 'signed values' },
    sameUnitPair:       { zh: '兩個同尺度數值欄', en: 'two same-scale numeric columns' },
    twoPeriods:         { zh: '恰好兩期', en: 'exactly two periods' },
    ageGroup:           { zh: '可排序年齡組', en: 'ordered age groups' },
    twoSides:           { zh: '雙側度量（例：男／女）', en: 'two-sided measure (e.g. male/female)' },
    geo:                { zh: '地理區塊欄（一區一列）', en: 'geographic unit column (one row per unit)' },
    latlon:             { zh: '經緯度欄', en: 'lat/lon columns' },
    ratio:              { zh: '已正規化的比率欄', en: 'normalised rate column' },
    countLike:          { zh: '可數計數欄（人口、件數）', en: 'countable totals (population, cases)' },
    gridRowCol:         { zh: '有 row / col 格座標', en: 'row / col grid coordinates' },
    network:            { zh: '來源／去向（節點 + 邊）', en: 'source / target (nodes + edges)' },
    flow:               { zh: '來源 → 去向 + 流量', en: 'source → target + amount' },
    denseNetwork:       { zh: '邊多或稠密（≥ 30 邊或邊／節點 ≥ 1.5）', en: 'dense network (≥ 30 edges or edges/node ≥ 1.5)' },
    smallNetwork:       { zh: '節點 ≤ 30', en: '≤ 30 nodes' },
    edgeGroups:         { zh: '邊有類型／條件欄可分組', en: 'edges have a type/condition column' },
    squareExchange:     { zh: '來源與去向是同一組節點（方陣交換）', en: 'same node set on both ends (square exchange)' },
    hierarchy:          { zh: '階層（父子／路徑／巢狀類別）', en: 'hierarchy (parent/child, path, nested categories)' },
    deepHierarchy:      { zh: '階層深度 ≥ 3（可往下鑽）', en: 'hierarchy depth ≥ 3 (drill-down)' },
    delta:              { zh: '有符號增減量', en: 'signed increments' },
    waterfallBridge:    { zh: '起點＋有號增減＝終點（橋）', en: 'start + signed steps = end (bridge)' },
    stages:             { zh: '有序階段（漏斗）', en: 'ordered stages (funnel)' },
    monotoneStages:     { zh: '有序階段且通過量單調不增', en: 'ordered stages with monotone non-increasing counts' },
    pairedPeriods:      { zh: '恰好兩期／兩條件的同單位欄', en: 'exactly two same-unit period/condition columns' },
    target:             { zh: '有目標／預算欄', en: 'has target / budget column' },
    startEnd:           { zh: '開始 + 結束日期', en: 'start + end dates' },
    sets:               { zh: '≥ 3 個布林欄（集合成員）', en: '≥ 3 boolean membership columns' },
    manyNumeric:        { zh: '≥ 3 個連續數值欄', en: '≥ 3 continuous numeric columns' },
    fewRows:            { zh: '實體少（≤ 5 列）', en: 'few entities (≤ 5 rows)' },
    sizeVar:            { zh: '第三個非負數值可當大小', en: 'a third non-negative measure for size' },
    sizeNamed:          { zh: '有規模欄（size／人口）', en: 'a size-like column (size / population)' },
    dense:              { zh: '點很多（≥ 500 列）', en: 'many points (≥ 500 rows)' },
    partOfWhole:        { zh: '少數類別的占比（加總≈100%）', en: 'shares of a whole (sum ≈ 100%)' }
  };

  // ---------------------------------------------------------------- rules
  function R(id, zh, en, o) { o.id = id; o.zh = zh; o.en = en; o.render = o.render || []; o.need = o.need || []; o.prefer = o.prefer || []; o.avoid = o.avoid || []; return o; }

  var RULES = [
    R('categorical-comparison', '長條圖（排序／分組／堆疊）', 'Bar chart (sorted / grouped / stacked)', {
      requires: { label: [1], measure: [1] }, base: 60,
      prefer: ['oneRowPerCat', 'fewCats', 'crossTab'], avoid: ['manyCats', 'time', 'bigMatrix', 'network', 'geo', 'hierarchy', 'monotoneStages', 'waterfallBridge'],
      fields: { zh: '1 類別 + 1 數值（可先聚合）；第二類別 → 分組／堆疊', en: '1 category + 1 number; 2nd category → grouped/stacked' },
      why: { zh: '少數類別比大小，最直接的是排序長條', en: 'Comparing a few categories: sorted bars are most direct' },
      render: [{ r: 'barSorted' }, { r: 'barGrouped' }] }),
    R('time-series-trend', '折線圖', 'Line chart', {
      requires: { date: [1], measure: [1] }, base: 62,
      prefer: ['multiSeries', 'wideSeries'], avoid: ['manySeries'],
      fields: { zh: '1 時間 + 1 數值（+ ≤ 3 系列）', en: '1 time + 1 number (+ ≤ 3 series)' },
      why: { zh: '時間 + 數值 + 少系列 → 折線', en: 'Time + number + few series → line' },
      render: [{ r: 'line' }] }),
    R('correlation-scatter', '散點圖', 'Scatter plot', {
      requires: { measure: [2] }, base: 56,
      prefer: ['smallN'], avoid: ['dense', 'wideSeries'],
      fields: { zh: '2 數值（+ 類別上色）', en: '2 numbers (+ category colour)' },
      why: { zh: '兩數值關係 → 散點', en: 'Two numeric variables → scatter' },
      render: [{ r: 'scatter' }] }),
    R('matrix-heatmap', '矩陣熱圖', 'Matrix heatmap', {
      requires: { label: [2], measure: [1] }, base: 40, need: ['crossTab'],
      prefer: ['bigMatrix'], avoid: ['network'],
      fields: { zh: '列類別 + 欄類別 + 1 數值（長格式或寬表）', en: 'row category + column category + number' },
      why: { zh: '類別 × 類別 + 值 → 看哪裡熱／冷', en: 'Category × category + value → where is hot/cold' },
      render: [{ r: 'heatmap' }] }),
    R('hierarchy-icicle', '冰柱圖', 'Icicle chart', {
      requires: { label: [1], measure: [1] }, base: 42, need: ['hierarchy'],
      prefer: ['deepHierarchy', 'nonNegative'],
      fields: { zh: '父子／路徑（或巢狀類別）+ 數值', en: 'parent/child or path + number' },
      why: { zh: '階層組成、要標籤 → 冰柱', en: 'Labelled hierarchy composition → icicle' } }),
    R('small-multiples', '小多圖', 'Small multiples', {
      requires: { date: [1], label: [1], measure: [1] }, base: 36, need: ['manySeries'],
      fields: { zh: '時間 + 實體（> 8）+ 數值', en: 'time + many entities + number' },
      why: { zh: '多實體時間趨勢 → 同尺度小多圖，避免義大利麵', en: 'Many entities over time → aligned small multiples' } }),
    R('waterfall-bridge', '瀑布圖', 'Waterfall chart', {
      requires: { label: [1], measure: [1] }, base: 38, need: ['waterfallBridge'],
      prefer: ['delta', 'oneRowPerCat'],
      fields: { zh: '起點 + 一串有符號增減 + 終點', en: 'start + signed steps + end' },
      why: { zh: '從 A 到 B 的因子橋 → 瀑布', en: 'Bridge from A to B → waterfall' } }),
    R('funnel-stages', '漏斗圖', 'Funnel chart', {
      requires: { label: [1], measure: [1] }, base: 38, need: ['monotoneStages'],
      prefer: ['oneRowPerCat', 'countLike'],
      fields: { zh: '有序階段 + 通過量（單調不增）', en: 'ordered stages + monotone non-increasing count' },
      why: { zh: '階段漏損／轉換率 → 漏斗', en: 'Stage drop-off → funnel' } }),
    R('dumbbell-gap', '啞鈴圖', 'Dumbbell chart', {
      requires: { label: [1], measure: [2] }, base: 34, need: ['sameUnitPair', 'oneRowPerCat'],
      prefer: ['twoPeriods', 'pairedPeriods'],
      fields: { zh: '類別 + 兩個同單位數值', en: 'category + two same-unit numbers' },
      why: { zh: '兩期／兩條件差距 → 啞鈴', en: 'Gap between two conditions → dumbbell' } }),
    R('slope-two-period', '坡度圖', 'Slope chart', {
      requires: { label: [1], measure: [1] }, base: 32, need: ['twoPeriods'],
      avoid: ['pairedPeriods'],
      fields: { zh: '實體 + 恰好兩期數值', en: 'entity + exactly two periods' },
      why: { zh: '兩期軌跡交錯 → 坡度圖', en: 'Two-period crossings → slope chart' } }),
    R('bump-ranking', '凹凸圖', 'Bump chart', {
      requires: { date: [1], label: [1], measure: [1] }, base: 30, need: ['rankOverTime'],
      fields: { zh: '時間 + 實體 + 可排名度量', en: 'time + entity + rankable measure' },
      why: { zh: '名次隨時間 → 凹凸圖', en: 'Rank over time → bump chart' } }),
    R('streamgraph-composition', '河流圖（溪流圖）', 'Streamgraph', {
      requires: { date: [1], measure: [1] }, base: 36, need: ['compositionOverTime'],
      fields: { zh: '時間 + 類別 + 非負量（長表或寬表）', en: 'time + category + non-negative amount' },
      why: { zh: '組成隨時間、要整體流動感 → 河流圖', en: 'Composition over time with flow → streamgraph' } }),
    R('sankey-flow', '桑基圖', 'Sankey diagram', {
      requires: { label: [2], measure: [1] }, base: 32, need: ['flow'],
      fields: { zh: '來源 + 去向 + 非負流量', en: 'source + target + non-negative amount' },
      why: { zh: '有向流量 → 桑基', en: 'Directed flow → Sankey' } }),
    R('alluvial-stages', '沖積圖', 'Alluvial diagram', {
      requires: { category: [3] }, base: 24, need: ['multiCatStages'],
      fields: { zh: '≥ 3 個有序階段類別欄（+ 計數）', en: '≥ 3 stage category columns (+ count)' },
      why: { zh: '有序階段重分組 → 沖積', en: 'Regrouping across ordered stages → alluvial' } }),
    R('sunburst-hierarchy', '旭日圖', 'Sunburst', {
      requires: { label: [1], measure: [1] }, base: 30, need: ['hierarchy'],
      prefer: ['deepHierarchy'],
      fields: { zh: '父子／路徑 + 數值', en: 'parent/child or path + number' },
      why: { zh: '階層組成、緊湊總覽 → 旭日', en: 'Compact hierarchy overview → sunburst' } }),
    R('treemap-composition', '矩形樹狀圖', 'Treemap', {
      requires: { label: [1], measure: [1] }, base: 26, need: ['nonNegative'],
      prefer: ['hierarchy', 'deepHierarchy', 'manyCats'], avoid: ['time'],
      fields: { zh: '（階層）類別 + 非負數值', en: '(hierarchical) category + non-negative number' },
      why: { zh: '階層／組成、鋪滿面積 → treemap', en: 'Space-filling composition → treemap' } }),
    R('circle-packing', '圓堆圖', 'Circle packing', {
      requires: { label: [1], measure: [1] }, base: 24, need: ['hierarchy'],
      fields: { zh: '父子／路徑 + 數值', en: 'parent/child or path + number' },
      why: { zh: '階層嵌套圓 → 圓堆', en: 'Nested circles for hierarchy → circle packing' } }),
    R('voronoi-treemap', 'Voronoi 樹狀圖', 'Voronoi treemap', {
      requires: { label: [1], measure: [1] }, base: 20, need: ['hierarchy'],
      fields: { zh: '父子／路徑 + 數值', en: 'parent/child or path + number' },
      why: { zh: '凸多邊形鋪滿的階層 → Voronoi 樹狀', en: 'Convex-cell hierarchy → Voronoi treemap' } }),
    R('hexbin-density', '六角分箱圖', 'Hexbin', {
      requires: { measure: [2] }, base: 30, need: ['dense'],
      fields: { zh: '2 數值（大量點）', en: '2 numbers, many points' },
      why: { zh: '散點過密 → 六角分箱', en: 'Overplotted scatter → hexbin' } }),
    R('contour-density', '等高密度圖', 'Contour density', {
      requires: { measure: [2] }, base: 28, need: ['dense'],
      fields: { zh: '2 數值（大量點）', en: '2 numbers, many points' },
      why: { zh: '散點過密 → 等高線', en: 'Overplotted scatter → contour' } }),
    R('calendar-heatmap', '日曆熱力圖', 'Calendar heatmap', {
      requires: { date: [1], measure: [1] }, base: 34, need: ['daily'],
      fields: { zh: '日期（每日一值）+ 數值', en: 'daily date + number' },
      why: { zh: '每日一值、看哪幾天忙 → 日曆熱力', en: 'One value per day → calendar heatmap' } }),
    R('spiral-plot', '螺旋圖', 'Spiral plot', {
      requires: { date: [1], measure: [1] }, base: 36, need: ['cycle'],
      fields: { zh: '連續時間（數年以上）+ 數值，週期穩定', en: 'multi-year time + number with stable cycle' },
      why: { zh: '長序列＋穩定週期 → 一圈＝一週期的螺旋', en: 'Long series with stable cycle → spiral (one turn = one cycle)' } }),
    R('violin-distribution', '小提琴圖', 'Violin plot', {
      requires: { label: [1], measure: [1] }, base: 36, need: ['repeatedGroups'],
      prefer: ['bigGroups'], avoid: ['network'],
      fields: { zh: '分組類別 + 連續數值（每組多筆）', en: 'group + continuous number (many per group)' },
      why: { zh: '要看密度／雙峰 → 小提琴', en: 'Density / bimodality → violin' } }),
    R('beeswarm-points', '蜂群圖', 'Beeswarm', {
      requires: { label: [1], measure: [1] }, base: 35, need: ['repeatedGroups'],
      prefer: ['smallN'], avoid: ['network', 'dense'],
      fields: { zh: '分組類別 + 連續數值（每點可見）', en: 'group + number, every point shown' },
      why: { zh: '要個體點 → 蜂群', en: 'Show every observation → beeswarm' } }),
    R('raincloud-combo', '雨雲圖', 'Raincloud plot', {
      requires: { label: [1], measure: [1] }, base: 32, need: ['repeatedGroups'],
      prefer: ['fewCats'], avoid: ['network'],
      fields: { zh: '少數分組 + 連續數值', en: 'few groups + continuous number' },
      why: { zh: '少組、雲＋雨＋傘 → 雨雲', en: 'Few groups, cloud + rain + box → raincloud' } }),
    R('ridgeline-density', '山脊圖', 'Ridgeline plot', {
      requires: { label: [1], measure: [1] }, base: 28, need: ['repeatedGroups'],
      prefer: ['bigGroups'], avoid: ['fewCats', 'network'],
      fields: { zh: '多組（≥ 5）+ 連續數值', en: 'many groups (≥ 5) + number' },
      why: { zh: '多組密度漂移 → 山脊', en: 'Density drift across many groups → ridgeline' } }),
    R('radar-profile', '雷達圖', 'Radar chart', {
      requires: { label: [1], measure: [3] }, base: 26, need: ['manyNumeric'],
      prefer: ['fewRows'],
      fields: { zh: '實體（≤ 3）+ 多個同尺度度量', en: 'entities (≤ 3) + several measures' },
      why: { zh: '少度量、要比外形 → 雷達（系列 ≤ 2–3）', en: 'Profile shape of few series → radar' } }),
    R('bullet-kpi', '子彈圖', 'Bullet graph', {
      requires: { measure: [2] }, base: 34, need: ['target'],
      fields: { zh: '實際 + 目標（+ 質性區間）', en: 'actual + target (+ ranges)' },
      why: { zh: 'KPI 實際 vs 目標 → 子彈圖', en: 'KPI actual vs target → bullet' } }),
    R('gantt-schedule', '甘特圖', 'Gantt chart', {
      requires: { date: [2] }, base: 40, need: ['startEnd'],
      fields: { zh: '任務 + 開始 + 結束', en: 'task + start + end' },
      why: { zh: '專案時程 → 甘特', en: 'Project schedule → Gantt' } }),
    R('waffle-percent', '華夫圖', 'Waffle chart', {
      requires: { label: [1], measure: [1] }, base: 30, need: ['partOfWhole'],
      avoid: ['hierarchy'],
      fields: { zh: '少數類別 + 占比（加總 100%）', en: 'few categories + shares (sum 100%)' },
      why: { zh: '平級組成、少塊 → 華夫', en: 'Flat composition, few parts → waffle' } }),
    R('mosaic-crosstab', '馬賽克圖', 'Mosaic plot', {
      requires: { category: [2] }, base: 28, need: ['twoCats'],
      prefer: ['noNumeric', 'crossTab'], avoid: ['network'],
      fields: { zh: '兩個類別（+ 計數）', en: 'two categories (+ count)' },
      why: { zh: '交叉表／獨立性 → 馬賽克', en: 'Cross-tab / independence → mosaic' } }),
    R('connected-scatter', '連接散點圖', 'Connected scatter', {
      requires: { date: [1], measure: [2] }, base: 28, need: ['time'],
      fields: { zh: '2 數值 + 時間（只決定連線順序）', en: '2 numbers + time as path order' },
      why: { zh: '雙序列一起演化 → 連接散點', en: 'Two series evolving together → connected scatter' } }),
    R('chord-matrix', '弦圖', 'Chord diagram', {
      requires: { label: [2], measure: [1] }, base: 24, need: ['network'],
      prefer: ['squareExchange'],
      fields: { zh: '來源 + 去向（同一組節點）+ 交換量', en: 'source + target (same set) + amount' },
      why: { zh: '成對雙向交換 → 弦圖', en: 'Pairwise exchange → chord' } }),
    R('force-network', '力導向網路圖', 'Force-directed network', {
      requires: { label: [2] }, base: 34, need: ['network'],
      prefer: ['smallNetwork'], avoid: ['denseNetwork'],
      fields: { zh: '節點 + 邊（source, target）', en: 'nodes + edges (source, target)' },
      why: { zh: '網路誰連誰 → 力導向', en: 'Who connects to whom → force layout' } }),
    R('arc-diagram', '弧線圖', 'Arc diagram', {
      requires: { label: [2] }, base: 30, need: ['network'],
      prefer: ['smallNetwork'],
      fields: { zh: '節點 + 邊（節點要可讀標籤）', en: 'nodes + edges, readable labels' },
      why: { zh: '要可讀節點標籤 → 弧線圖', en: 'Readable node labels → arc diagram' } }),
    R('adjacency-matrix', '鄰接矩陣', 'Adjacency matrix', {
      requires: { label: [2] }, base: 33, need: ['network'],
      prefer: ['denseNetwork'],
      fields: { zh: 'source + target（+ 權重）', en: 'source + target (+ weight)' },
      why: { zh: '節點 × 節點有無邊，可重排看團', en: 'Node × node presence; reorder to see clusters' },
      render: [{ r: 'adjacency' }] }),
    R('biofabric', 'BioFabric（生物織布圖）', 'BioFabric', {
      requires: { label: [2] }, base: 30, need: ['network'],
      prefer: ['denseNetwork', 'edgeGroups'],
      fields: { zh: 'source + target（+ 關係類型／條件／時間）', en: 'source + target (+ relation / condition / time)' },
      why: { zh: '稠密網路、每條邊都要可辨識 → BioFabric', en: 'Dense network, every edge legible → BioFabric' } }),
    R('parallel-coordinates', '平行座標圖', 'Parallel coordinates', {
      requires: { measure: [3] }, base: 28, need: ['manyNumeric'],
      fields: { zh: '≥ 3 連續數值（+ 類別上色）', en: '≥ 3 numbers (+ category colour)' },
      why: { zh: '多連續特徵剖面 → 平行座標', en: 'Multivariate profiles → parallel coordinates' } }),
    R('circular-bar', '圓形長條圖', 'Circular bar chart', {
      requires: { label: [1], measure: [1] }, base: 26, need: ['oneRowPerCat'],
      prefer: ['manyCats'], avoid: ['fewCats'],
      fields: { zh: '多類別 + 1 數值', en: 'many categories + number' },
      why: { zh: '類別很多、要搶眼排序 → 圓形長條', en: 'Many categories, eye-catching → circular bar' } }),
    R('cartogram-geo', '統計變形地圖', 'Cartogram', {
      requires: { label: [1], measure: [1] }, base: 24, need: ['geo'],
      prefer: ['countLike'],
      fields: { zh: '地理區塊 + 總量（面積＝資料量）', en: 'geo unit + total (area = value)' },
      why: { zh: '面積＝資料量 → 統計變形地圖', en: 'Area = value → cartogram' } }),
    R('choropleth-map', '等值區域圖', 'Choropleth map', {
      requires: { label: [1], measure: [1] }, base: 56, need: ['geo'],
      prefer: ['ratio'], avoid: ['gridRowCol', '!ratio', 'pairedPeriods', 'twoPeriods'],
      fields: { zh: '地理區塊（代碼）+ 已正規化比率', en: 'geo unit (code) + normalised rate' },
      why: { zh: '地理比率 → 等值區域（先正規化）', en: 'Geographic rate → choropleth (normalise first)' } }),
    R('tile-map', '圖塊地圖', 'Tile map', {
      requires: { label: [1], measure: [1] }, base: 30, need: ['geo'],
      prefer: ['gridRowCol', 'gridRowCol', 'ratio'],
      fields: { zh: '地理區塊 + row/col 格座標 + 值', en: 'geo unit + row/col grid + value' },
      why: { zh: '各區同等權重、怕大區搶眼 → 圖塊地圖', en: 'Equal weight per region → tile map' } }),
    R('dot-density-map', '點密度地圖', 'Dot density map', {
      requires: { number: [1] }, base: 45, need: ['geo|latlon'],
      prefer: ['latlon', 'countLike'],
      fields: { zh: '地理區塊 + 計數（一對多）或經緯度（一對一）', en: 'geo unit + count, or lat/lon points' },
      why: { zh: '計數疏密／叢集 → 點密度', en: 'Count density / clusters → dot density' } }),
    R('population-pyramid', '人口金字塔', 'Population pyramid', {
      requires: { label: [1], measure: [1] }, base: 45, need: ['ageGroup', 'twoSides'],
      fields: { zh: '年齡組 + 雙側（性別）+ 人數／占比', en: 'age group + two sides + count' },
      why: { zh: '年齡 × 雙側結構輪廓 → 人口金字塔', en: 'Age × two-sided profile → pyramid' },
      render: [{ r: 'pyramid' }] }),
    R('lollipop-rank', '棒棒糖圖', 'Lollipop chart', {
      requires: { label: [1], measure: [1] }, base: 52, need: ['oneRowPerCat'],
      prefer: ['fewCats'], avoid: ['time', 'geo', 'deepHierarchy', 'monotoneStages', 'waterfallBridge'],
      fields: { zh: '1 類別 + 1 數值（一類一列）', en: '1 category + 1 number (one row each)' },
      why: { zh: '同長條任務、高值齊頭時減墨水 → 棒棒糖', en: 'Same task as bars, less ink → lollipop' },
      render: [{ r: 'barSorted', preset: { style: 'lollipop' } }] }),
    R('boxplot-summary', '箱形圖', 'Box plot', {
      requires: { label: [1], measure: [1] }, base: 44, need: ['repeatedGroups'],
      prefer: ['fewCats'], avoid: ['network'],
      fields: { zh: '分組類別 + 連續數值（每組多筆）', en: 'group + continuous number (many per group)' },
      why: { zh: '多組比中位數／IQR／離群 → 箱形圖', en: 'Compare median / IQR / outliers → box plot' },
      render: [{ r: 'boxplot' }, { r: 'histogram' }] }),
    R('bubble-chart', '氣泡圖', 'Bubble chart', {
      requires: { measure: [3] }, base: 42, need: ['sizeVar'],
      prefer: ['sizeNamed', 'smallN'], avoid: ['dense', 'geo'],
      fields: { zh: 'X 數值 + Y 數值 + 非負大小（面積映射）', en: 'x + y + non-negative size (area)' },
      why: { zh: '2 數值 + 第三量級 → 氣泡（面積映射）', en: '2 numbers + a size measure → bubble' },
      render: [{ r: 'scatter', preset: { useSize: true } }] }),
    R('marimekko-chart', '馬里梅可圖', 'Marimekko chart', {
      requires: { label: [2], measure: [1] }, base: 28, need: ['crossTab', 'nonNegative'],
      prefer: ['smallCross'], avoid: ['bigMatrix'],
      fields: { zh: '外層區隔 + 內層組成 + 可加總量', en: 'outer segment + inner component + additive amount' },
      why: { zh: '區隔規模 + 區內組成 → 馬里梅可', en: 'Segment size + inner mix → Marimekko' } }),
    R('upset-sets', 'UpSet 集合圖', 'UpSet plot', {
      requires: { boolean: [3] }, base: 36, need: ['sets'],
      fields: { zh: '元素 + 多個布林成員欄', en: 'element + several boolean membership columns' },
      why: { zh: '多集合交集 → UpSet（不要一堆 Venn）', en: 'Many set intersections → UpSet' } }),
    R('flame-graph', '火焰圖', 'Flame graph', {
      requires: { label: [1], measure: [1] }, base: 18, need: ['hierarchy'],
      prefer: ['nonNegative'], avoid: ['time', 'geo'],
      fields: { zh: '呼叫堆疊路徑（或階層）+ 樣本計數', en: 'call-stack path (or hierarchy) + sample counts' },
      why: { zh: '剖面熱路徑 → 火焰圖（教學）', en: 'Profile hot paths → flame graph (teach)' } }),
    R('circos', 'Circos 環狀多軌', 'Circos', {
      requires: { label: [2], measure: [1] }, base: 16, need: ['network'],
      prefer: ['denseNetwork'], avoid: ['time'],
      fields: { zh: '扇區／軌道／連線（多表）', en: 'sectors / tracks / links (multi-table)' },
      why: { zh: '長軸多軌 + 區間對應 → Circos（教學）', en: 'Long axis + multi-track + links → Circos (teach)' } }),
    R('volcano-plot', '火山圖', 'Volcano plot', {
      requires: { measure: [2] }, base: 20, need: ['dense'],
      prefer: ['manyNumeric'], avoid: ['time', 'geo', 'network'],
      fields: { zh: '效應量（如 log2FC）+ 顯著性（−log10 p）', en: 'effect size (e.g. log2FC) + significance (−log10 p)' },
      why: { zh: '大量特徵差異篩選 → 火山圖（教學）', en: 'Many-feature DE screen → volcano (teach)' } }),
    R('manhattan-plot', '曼哈頓圖', 'Manhattan plot', {
      requires: { label: [1], measure: [1] }, base: 18, need: ['dense'],
      prefer: ['manyCats'], avoid: ['network', 'geo'],
      fields: { zh: '染色體／位置 + p 值（全基因組摘要）', en: 'chromosome/position + p-values (GWAS summary)' },
      why: { zh: '全基因組關聯掃描 → 曼哈頓圖（教學）', en: 'GWAS scan → Manhattan (teach)' } }),
    R('ma-plot', 'MA 圖', 'MA plot', {
      requires: { measure: [2] }, base: 20, need: ['sameUnitPair'],
      prefer: ['dense', 'manyNumeric'], avoid: ['time', 'geo'],
      fields: { zh: '平均表現 A + 對數倍數 M（兩條件）', en: 'mean expression A + log-fold M (two conditions)' },
      why: { zh: '兩條件大量特徵比較 → MA 圖（教學）', en: 'Two-condition feature compare → MA (teach)' } }),
    R('qq-plot', 'QQ 圖', 'Q–Q plot', {
      requires: { measure: [1] }, base: 22, need: ['repeatedGroups|smallN'],
      prefer: ['fewCats'], avoid: ['time', 'network', 'geo'],
      fields: { zh: '連續數值（對理論分位或兩組）', en: 'continuous values (vs theoretical or two samples)' },
      why: { zh: '分布形狀／常態檢查 → QQ 圖（教學）', en: 'Distribution shape check → Q–Q (teach)' } }),
    R('bland-altman', 'Bland–Altman 圖', 'Bland–Altman plot', {
      requires: { measure: [2] }, base: 22, need: ['sameUnitPair'],
      prefer: ['smallN'], avoid: ['dense', 'time', 'geo', 'sizeVar'],
      fields: { zh: '同批配對的兩種量測方法', en: 'paired measurements from two methods' },
      why: { zh: '兩方法一致性 → Bland–Altman（教學）', en: 'Method agreement → Bland–Altman (teach)' } }),
    R('locuszoom', 'LocusZoom 圖', 'LocusZoom plot', {
      requires: { measure: [1], label: [1] }, base: 16, need: ['dense'],
      prefer: ['manyNumeric'], avoid: ['network', 'geo'],
      fields: { zh: '區間內標記位置 + 關聯強度（+ LD）', en: 'regional markers + association (+ LD)' },
      why: { zh: '曼哈頓尖峰區間細讀 → LocusZoom（教學）', en: 'Zoom a GWAS peak → LocusZoom (teach)' } }),
    R('pp-plot', 'P–P 圖', 'P–P plot', {
      requires: { measure: [1] }, base: 18, need: ['repeatedGroups|smallN'],
      prefer: ['fewCats'], avoid: ['time', 'network', 'geo'],
      fields: { zh: '樣本累積機率 vs 指定參考分布', en: 'empirical CDF vs a fully specified reference' },
      why: { zh: '分布適配輔助 → P–P 圖（教學）', en: 'Distribution fit aid → P–P (teach)' } }),
    R('karyotype-ideogram', '核型／染色體帶型圖', 'Karyotype / ideogram', {
      requires: { label: [1], measure: [1] }, base: 14, need: ['manyCats|dense'],
      prefer: ['nonNegative'], avoid: ['time', 'network'],
      fields: { zh: '染色體／帶型區間 + 註記', en: 'chromosome / band intervals + annotations' },
      why: { zh: '染色體地圖示意 → 核型圖（教學）', en: 'Chromosome map → ideogram (teach)' } }),
    R('forest-plot', '森林圖', 'Forest plot', {
      requires: { label: [1], measure: [1] }, base: 24, need: ['oneRowPerCat'],
      prefer: ['fewCats', 'fewRows'], avoid: ['time', 'geo', 'network', 'crossTab'],
      fields: { zh: '研究／項目 + 效應量（+ 信賴區間）', en: 'study/item + effect (+ CI)' },
      why: { zh: '多項研究效應＋區間 → 森林圖（教學）', en: 'Study effects + CIs → forest (teach)' } }),
    R('horizon-chart', '地平線圖', 'Horizon chart', {
      requires: { date: [1], label: [1], measure: [1] }, base: 22, need: ['manySeries|multiSeries'],
      prefer: ['longSeries'], avoid: ['network', 'geo'],
      fields: { zh: '時間 + 多序列 + 相對基準的數值', en: 'time + many series + values vs a baseline' },
      why: { zh: '很多條時間序列緊湊比較 → 地平線圖（教學）', en: 'Many dense time series → horizon (teach)' } }),
    R('pareto-chart', '柏拉圖', 'Pareto chart', {
      requires: { label: [1], measure: [1] }, base: 28, need: ['oneRowPerCat', 'nonNegative'],
      prefer: ['fewCats', 'manyCats'], avoid: ['time', 'geo', 'network', 'signed', 'hierarchy', 'monotoneStages'],
      fields: { zh: '類別 + 件數／金額（一類一列）', en: 'category + count/amount (one row each)' },
      why: { zh: '聚焦少數主因 → 柏拉圖（教學）', en: 'Focus vital few → Pareto (teach)' } }),
    R('control-chart', '管制圖', 'Control chart', {
      requires: { measure: [1] }, base: 24, need: ['time|longSeries'],
      prefer: ['smallN'], avoid: ['network', 'geo', 'crossTab'],
      fields: { zh: '時間／子組序 + 製程統計量（+ 管制界限）', en: 'time/subgroup order + process statistic (+ limits)' },
      why: { zh: '流程穩定性／異常偵測 → 管制圖（教學）', en: 'Process stability → control chart (teach)' } }),
    R('lorenz-curve', '洛倫茲曲線', 'Lorenz curve', {
      requires: { measure: [1] }, base: 20, need: ['nonNegative', 'oneRowPerCat|smallN'],
      prefer: ['fewCats'], avoid: ['time', 'network', 'geo', 'signed', 'hierarchy', 'monotoneStages'],
      fields: { zh: '單位 + 非負可累計量（所得／財富等）', en: 'units + non-negative accumulable amounts' },
      why: { zh: '分配不均（含基尼）→ 洛倫茲（教學）', en: 'Inequality (+ Gini) → Lorenz (teach)' } }),
    R('marey-chart', '馬雷圖／列車運行圖', 'Marey chart', {
      requires: { label: [1], measure: [1] }, base: 16, need: ['time|startEnd'],
      prefer: ['multiSeries'], avoid: ['geo', 'network', 'crossTab'],
      fields: { zh: '路線站點距離 + 車次時刻', en: 'route distance + vehicle timestamps' },
      why: { zh: '時間－距離營運 → 馬雷圖（教學）', en: 'Time–distance ops → Marey (teach)' } }),
    R('kaplan-meier-survival', 'Kaplan–Meier 存活曲線', 'Kaplan–Meier curve', {
      requires: { measure: [1] }, base: 22, need: ['smallN|repeatedGroups'],
      prefer: ['fewCats'], avoid: ['geo', 'network', 'crossTab'],
      fields: { zh: '觀察時間 + 事件／設限狀態（+ 分組）', en: 'time-to-event + censor status (+ group)' },
      why: { zh: '含設限的存活／流失 → KM 曲線（教學）', en: 'Survival with censoring → KM (teach)' } }),
    R('swimmer-plot', '游泳圖', 'Swimmer plot', {
      requires: { label: [1], measure: [1] }, base: 18, need: ['startEnd|smallN'],
      prefer: ['fewCats', 'fewRows'], avoid: ['dense', 'network', 'geo', 'crossTab'],
      fields: { zh: '個體 + 治療／觀察時段 + 事件標記', en: 'subject + on-treatment span + event marks' },
      why: { zh: '小樣本療程時間線 → 游泳圖（教學）', en: 'Small-n treatment timelines → swimmer (teach)' } }),
    R('lasagna-plot', '千層麵圖', 'Lasagna plot', {
      requires: { label: [2], measure: [1] }, base: 20, need: ['crossTab'],
      prefer: ['bigMatrix', 'time'], avoid: ['network', 'geo'],
      fields: { zh: '個體 × 固定時間點的長表熱圖', en: 'subject × fixed time grid (long heatmap)' },
      why: { zh: '多人同期序列總覽 → 千層麵圖（教學）', en: 'Many subjects × time → lasagna (teach)' } }),
    R('recurrence-plot', '遞迴圖', 'Recurrence plot', {
      requires: { measure: [1] }, base: 16, need: ['longSeries|time'],
      prefer: ['smallN'], avoid: ['network', 'geo', 'crossTab'],
      fields: { zh: '等間隔時間序列（狀態是否重現）', en: 'evenly spaced series (state recurrence)' },
      why: { zh: '狀態是否回到從前 → 遞迴圖（教學）', en: 'State recurrence → recurrence plot (teach)' } })

  ];

  // ---------------------------------------------------------------- shape
  var RX = {
    geo: /(county|state|province|region|country|city|district|town|zip|postal|iso|geo|prefecture|縣市|城市|區域|地區|省|州|鄉|鎮|行政區|郵遞|國家|縣)/i,
    geoStore: /(門市|店面|店鋪|超商|分行|據點|stores?|shops?)/i,
    geoValue: /(市|縣|區|省|州|鄉|鎮)$/,
    lat: /^(lat|latitude|緯度)$/i,
    lon: /^(lon|lng|long|longitude|經度)$/i,
    ratio: /(rate|ratio|pct|percent|share|per_?\d|per.?capita|率|比|占比|佔比|%|％|每)/i,
    count: /(count|population|pop|cases|total|number|num_|人口|件數|人數|戶數|數量)/i,
    source: /^(source|src|from|origin|起點|來源|出發|起)$/i,
    target: /^(target|tgt|to|dest|destination|終點|去向|目的|迄)$/i,
    hierarchy: /(parent|child|path|level|lvl|tier|層|科目|上層|父|子)/i,
    delta: /(change|delta|diff|increment|impact|contribution|增減|變動|差額|增量|貢獻)/i,
    stage: /(stage|step|phase|funnel|階段|步驟|漏斗|流程)/i,
    stageValue: /(曝光|點擊|瀏覽|造訪|落地|開通|付費|續約|加入購物車|結帳|購買|註冊|訪問|visit|impression|click|signup|sign.?up|cart|checkout|purchase|lead|trial)/i,
    targetName: /(target|goal|budget|plan|quota|目標|預算|計畫|標準)/i,
    start: /(start|begin|from|開始|起始|起)/i,
    end: /(end|finish|until|due|結束|完成|截止|迄)/i,
    age: /(age|年齡|歲)/i,
    ageValue: /^(\d+\s*[-~–—至]\s*\d+|\d+\s*\+|\d+\s*歲.*|\d+\s*(以上|以下)|under\s*\d+|\d+\s*and\s*over)$/i,
    sides: /^(male|female|men|women|m|f|男|女|男性|女性|left|right)$/i,
    period: /^(\d{4}|fy\s?\d{2,4}|before|after|pre|post|前|後|去年|今年|base|baseline|current|previous|prior|q[1-4]|h[12]|上半年|下半年|上期|下期)/i,
    size: /(size|pop|population|volume|weight|規模|人口|大小|量體)/i,
    grid: { row: /^(row|r|列)$/i, col: /^(col|column|c|欄|行)$/i },
    cycleCol: /^(month_?num|month|weekday|dow|hour|week|週|星期|月份|小時)$/i
  };

  function uniq(arr) { var s = {}, out = []; arr.forEach(function (v) { if (v !== null && v !== undefined && !s.hasOwnProperty(v)) { s[v] = 1; out.push(v); } }); return out; }
  function median(xs) { var s = xs.filter(function (x) { return x !== null; }).sort(function (a, b) { return a - b; }); if (!s.length) return 0; var m = Math.floor(s.length / 2); return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; }

  function prefixKey(cols, row, lastIdx) {
    var key = '', i, v;
    for (i = 0; i <= lastIdx; i++) {
      v = cols[i].values[row];
      if (v === null || v === undefined) return null;
      key += (i ? '\u0001' : '') + String(v);
    }
    return key;
  }

  function uniquePrefixCounts(cols, rows) {
    var counts = [], d, r, key, seen, n;
    for (d = 0; d < cols.length; d++) {
      seen = {}; n = 0;
      for (r = 0; r < rows; r++) {
        key = prefixKey(cols, r, d);
        if (key === null) continue;
        if (!seen.hasOwnProperty(key)) { seen[key] = 1; n++; }
      }
      counts.push(n);
    }
    return counts;
  }

  function valueNestedPair(coarse, fine, rows) {
    if (!coarse || !fine || fine.distinct < 2 || coarse.distinct < 2) return false;
    if (fine.distinct <= coarse.distinct) return false;
    var map = {}, r, fv, cv;
    for (r = 0; r < rows; r++) {
      fv = fine.values[r]; cv = coarse.values[r];
      if (fv === null || cv === null) continue;
      if (map.hasOwnProperty(fv) && map[fv] !== cv) return false;
      map[fv] = cv;
    }
    return Object.keys(map).length >= 2;
  }

  /**
   * True nested drill-down: original column order, distinct ≥ 2 only.
   * Every adjacent step must refine, branch, and have unique child→parent
   * when the child is keyed by its full prefix path (so the same leaf label
   * may appear under two parents). Sparsity alone never qualifies.
   */
  function detectHierarchyPath(cols, rows) {
    if (!cols || cols.length < 2 || rows < 2) return null;
    cols = cols.filter(function (c) { return c.distinct >= 2; });
    if (cols.length < 2) return null;
    var prefixes = uniquePrefixCounts(cols, rows);
    var i, r, parent, child, map, parentKids, branched, kidCount;
    branched = false;
    for (i = 1; i < cols.length; i++) {
      if (prefixes[i] <= prefixes[i - 1]) return null;
      map = {};
      parentKids = {};
      for (r = 0; r < rows; r++) {
        parent = prefixKey(cols, r, i - 1);
        child = prefixKey(cols, r, i);
        if (parent === null || child === null) continue;
        if (map.hasOwnProperty(child) && map[child] !== parent) return null;
        map[child] = parent;
        if (!parentKids[parent]) parentKids[parent] = {};
        parentKids[parent][child] = 1;
      }
      if (Object.keys(map).length < 2) return null;
      for (parent in parentKids) {
        if (!Object.prototype.hasOwnProperty.call(parentKids, parent)) continue;
        kidCount = 0;
        for (child in parentKids[parent]) {
          if (Object.prototype.hasOwnProperty.call(parentKids[parent], child)) kidCount++;
        }
        if (kidCount >= 2) branched = true;
      }
    }
    if (!branched) return null;
    var depth = cols.length;
    if (depth >= 3) {
      return { names: cols.map(function (c) { return c.name; }), depth: depth };
    }
    if (valueNestedPair(cols[0], cols[1], rows) && cols[1].distinct < rows) {
      return { names: cols.map(function (c) { return c.name; }), depth: 2 };
    }
    return null;
  }

  function detectWaterfallBridge(measure, rows) {
    if (!measure || rows < 4) return false;
    var vals = [], i, v;
    for (i = 0; i < rows; i++) {
      v = measure.values[i];
      if (v === null || v === undefined) return false;
      vals.push(v);
    }
    var first = vals[0], last = vals[vals.length - 1];
    if (!(first > 0 && last > 0)) return false;
    var midSum = 0, hasNeg = false;
    for (i = 1; i < vals.length - 1; i++) {
      midSum += vals[i];
      if (vals[i] < 0) hasNeg = true;
    }
    if (!hasNeg) return false;
    var tol = Math.max(0.51, Math.abs(first) * 0.005);
    return Math.abs(first + midSum - last) <= tol;
  }

  function isMonotoneNonIncreasing(measure, rows) {
    if (!measure || rows < 3) return false;
    var prev = null, i, v;
    for (i = 0; i < rows; i++) {
      v = measure.values[i];
      if (v === null || v === undefined) return false;
      if (prev !== null && v > prev + 1e-9) return false;
      prev = v;
    }
    return measure.values[0] > measure.values[rows - 1];
  }

  /**
   * Compute shape features from a WIDS_TYPES.profileTable() result.
   * Returns { counts, rows, hints:{name:true}, roles:{...} }.
   */
  function computeShape(profile) {
    var cols = profile.columns;
    var rows = profile.rowCount;
    var by = function (t) { return cols.filter(function (c) { return c.type === t; }); };
    var num = by('number'), cat = by('category'), date = by('date'), bool = by('boolean'), ids = by('id');
    var labels = cat.concat(ids);
    var counts = { number: num.length, measure: 0, category: cat.length, date: date.length, boolean: bool.length, id: ids.length, label: labels.length };
    var h = {};
    var roles = {};

    var gridRow = num.filter(function (c) { return RX.grid.row.test(c.name); })[0];
    var gridCol = num.filter(function (c) { return RX.grid.col.test(c.name); })[0];
    if (gridRow && gridCol) { h.gridRowCol = true; }
    var lat = num.filter(function (c) { return RX.lat.test(c.name); })[0];
    var lon = num.filter(function (c) { return RX.lon.test(c.name); })[0];
    if (lat && lon) h.latlon = true;
    // "measure" numerics exclude coordinates / grid / cycle helpers
    var measures = num.filter(function (c) { return c !== gridRow && c !== gridCol && c !== lat && c !== lon && !RX.cycleCol.test(c.name); });
    roles.measures = measures.map(function (c) { return c.name; });
    counts.measure = measures.length;
    var allNonNeg = measures.length > 0 && measures.every(function (c) { return !c.stats || c.stats.min >= 0; });
    if (allNonNeg) h.nonNegative = true;
    if (measures.some(function (c) { return c.stats && c.stats.min < 0 && c.stats.max > 0; })) h.signed = true;

    // time
    var mainDate = date.slice().sort(function (a, b) { return b.distinct - a.distinct; })[0];
    if (mainDate) {
      h.time = true;
      roles.time = mainDate.name;
      var d = mainDate.distinct, g = mainDate.granularity;
      if (d >= 24) h.longSeries = true;
      if (g === 'day' && d >= 60) h.daily = true;
      if (h.longSeries && ((g === 'month' && d >= 36) || (g === 'day' && d >= 730) || ((g === 'datetime' || g === 'time') && d >= 72))) h.cycle = true;
      if (d === 2) h.twoPeriods = true;
    }

    // categories sorted by cardinality
    var catsByCard = cat.filter(function (c) { return c.distinct >= 2; }).sort(function (a, b) { return a.distinct - b.distinct; });
    var uniqueLabel = labels.filter(function (c) { return c.distinct === rows && rows >= 2 && c.missing === 0; })[0];
    if (uniqueLabel && measures.length >= 1) { h.oneRowPerCat = true; roles.label = uniqueLabel.name; }
    var primaryCat = uniqueLabel && uniqueLabel.type === 'category' ? uniqueLabel : catsByCard[0];
    if (primaryCat) {
      roles.category = primaryCat.name;
      if (primaryCat.distinct <= 6) h.fewCats = true;
      if (primaryCat.distinct > 12) h.manyCats = true;
    }

    if (mainDate && measures.length) {
      var seriesCat = catsByCard[0];
      if (seriesCat) {
        if (seriesCat.distinct >= 2 && seriesCat.distinct <= 8) h.multiSeries = true;
        if (seriesCat.distinct > 8) h.manySeries = true;
        if (seriesCat.distinct >= 3 && mainDate.distinct >= 3) h.rankOverTime = true;
        if (allNonNeg && seriesCat.distinct >= 2 && seriesCat.distinct <= 12) h.compositionOverTime = true;
      }
      if (measures.length >= 2 && measures.length <= 12) {
        var meds = measures.map(function (c) { return Math.abs(c.stats ? c.stats.median : 0) || 1e-9; });
        var ratio = Math.max.apply(null, meds) / Math.min.apply(null, meds);
        if (ratio <= 10) {
          h.wideSeries = true;
          if (!seriesCat && allNonNeg) h.compositionOverTime = true;
        }
      }
    }

    // cross tab (two category columns + value)
    if (catsByCard.length >= 2 && measures.length >= 1) {
      var a = catsByCard[0], b = catsByCard[1];
      var pairs = {};
      for (var i = 0; i < rows; i++) pairs[a.values[i] + '\u0001' + b.values[i]] = 1;
      var nPairs = Object.keys(pairs).length;
      var cells = a.distinct * b.distinct;
      if (nPairs / rows >= 0.8 && nPairs / cells >= 0.5) {
        h.crossTab = true;
        roles.crossTab = [b.name, a.name];
        if (cells >= 20) h.bigMatrix = true;
        if (a.distinct >= 3 && a.distinct <= 8 && b.distinct >= 3 && b.distinct <= 8) h.smallCross = true;
      }
    }
    var lowCats = catsByCard.filter(function (c) { return c.distinct <= 8; });
    if (lowCats.length >= 2) h.twoCats = true;
    if (lowCats.length >= 3) h.multiCatStages = true;
    if (measures.length === 0) h.noNumeric = true;

    // repeated groups → distribution
    if (measures.length >= 1 && !h.crossTab) {
      var grp = catsByCard.filter(function (c) { return c.distinct <= 15 && rows / c.distinct >= 3; })[0];
      var isSeries = false;
      if (grp && mainDate) {
        var dp = {};
        for (var k = 0; k < rows; k++) dp[mainDate.values[k] + '\u0001' + grp.values[k]] = 1;
        isSeries = Object.keys(dp).length / rows >= 0.8;
      }
      if (grp && !isSeries) {
        h.repeatedGroups = true; roles.group = grp.name;
        if (rows / grp.distinct >= 15) h.bigGroups = true;
      }
    }
    if (rows <= 300) h.smallN = true;
    if (rows >= 500 && measures.length >= 2) h.dense = true;
    if (rows <= 5) h.fewRows = true;

    // two same-scale numerics
    if (measures.length >= 2) {
      for (var x = 0; x < measures.length && !h.sameUnitPair; x++) {
        for (var y = x + 1; y < measures.length; y++) {
          var m1 = Math.abs(measures[x].stats ? measures[x].stats.median : 0), m2 = Math.abs(measures[y].stats ? measures[y].stats.median : 0);
          if (m1 > 0 && m2 > 0 && Math.max(m1, m2) / Math.min(m1, m2) <= 3) { h.sameUnitPair = true; roles.pair = [measures[x].name, measures[y].name]; break; }
        }
      }
      var periodCols = measures.filter(function (c) { return RX.period.test(c.name.trim()); });
      if (periodCols.length === 2) {
        h.twoPeriods = true;
        if (h.sameUnitPair) h.pairedPeriods = true;
      }
    }
    if (h.twoPeriods && !labels.length) delete h.twoPeriods;

    // age × two sides
    var ageCol = labels.filter(function (c) {
      if (RX.age.test(c.name)) return true;
      var vals = uniq(c.values);
      return vals.length >= 3 && vals.filter(function (v) { return RX.ageValue.test(String(v).trim()); }).length / vals.length >= 0.6;
    })[0];
    if (ageCol) { h.ageGroup = true; roles.age = ageCol.name; }
    var sideCat = cat.filter(function (c) { return c !== ageCol && c.distinct === 2; })[0];
    var sideNums = measures.filter(function (c) { return RX.sides.test(c.name.trim()); });
    if ((ageCol && sideCat) || sideNums.length === 2) h.twoSides = true;

    // geo
    var geoCol = labels.filter(function (c) {
      if (RX.geoStore.test(c.name)) return false;
      var perUnit = c.distinct >= 0.8 * rows;
      var vals = uniq(c.values);
      var valueGeo = vals.length >= 2 && vals.filter(function (v) { return RX.geoValue.test(String(v)); }).length / vals.length >= 0.6;
      return perUnit && (RX.geo.test(c.name) || valueGeo);
    })[0];
    if (geoCol && measures.length) { h.geo = true; roles.geo = geoCol.name; }
    if (measures.some(function (c) { return RX.ratio.test(c.name); })) h.ratio = true;
    if (measures.some(function (c) { return RX.count.test(c.name); })) h.countLike = true;

    // network
    var src = labels.filter(function (c) { return RX.source.test(c.name.trim()); })[0];
    var tgt = labels.filter(function (c) { return RX.target.test(c.name.trim()); })[0];
    var overlap = 0;
    if (!(src && tgt) && labels.length >= 2) {
      for (var p = 0; p < labels.length && !(src && tgt); p++) {
        for (var q = p + 1; q < labels.length; q++) {
          var A = uniq(labels[p].values), B = uniq(labels[q].values);
          if (A.length < 3 || B.length < 3) continue;
          var setB = {}; B.forEach(function (v) { setB[v] = 1; });
          var inter = A.filter(function (v) { return setB[v]; }).length;
          if (inter / Math.min(A.length, B.length) >= 0.5) { src = labels[p]; tgt = labels[q]; break; }
        }
      }
    }
    if (src && tgt && src !== tgt) {
      h.network = true;
      roles.source = src.name; roles.target = tgt.name;
      var sv = uniq(src.values), tv = uniq(tgt.values);
      var setT = {}; tv.forEach(function (v) { setT[v] = 1; });
      overlap = sv.filter(function (v) { return setT[v]; }).length / Math.min(sv.length, tv.length);
      var nodes = uniq(sv.concat(tv)).length;
      roles.nodes = nodes;
      if (rows >= 30 || rows / nodes >= 1.5) h.denseNetwork = true;
      if (nodes <= 30) h.smallNetwork = true;
      if (overlap >= 0.8) h.squareExchange = true;
      if (measures.length >= 1 && allNonNeg) h.flow = true;
      if (cat.some(function (c) { return c !== src && c !== tgt && c.distinct >= 2 && c.distinct <= 8; })) h.edgeGroups = true;
      // a network is not a cross-tab / distribution
      delete h.crossTab; delete h.repeatedGroups; delete h.bigGroups; delete h.bigMatrix; delete h.smallCross;
    }

    // hierarchy: named parent/path, unique child→parent, or multi-column drill-down
    var hierCols = cat.filter(function (c) { return c.distinct >= 2; });
    var path = !h.network ? detectHierarchyPath(hierCols, rows) : null;
    if (labels.some(function (c) { return RX.hierarchy.test(c.name); }) ||
        labels.some(function (c) { var v = uniq(c.values); return v.length >= 3 && v.filter(function (s) { return /\s[/>›]\s|\//.test(String(s)); }).length / v.length >= 0.6; })) {
      h.hierarchy = true;
    }
    if (path) {
      h.hierarchy = true;
      roles.hierarchy = path.names;
      roles.hierarchyDepth = path.depth;
      if (path.depth >= 3) h.deepHierarchy = true;
    } else if (!h.hierarchy && catsByCard.length >= 2 && !h.network) {
      // nested categories: every finer value maps to exactly one coarser value
      for (var ci = 0; ci < catsByCard.length && !h.hierarchy; ci++) {
        for (var cj = ci + 1; cj < catsByCard.length; cj++) {
          var coarse = catsByCard[ci], fine = catsByCard[cj];
          if (fine.distinct < 2 || coarse.distinct < 2) continue;
          if (fine.distinct <= coarse.distinct || fine.distinct >= rows) continue;
          var map = {}, ok = true;
          for (var r = 0; r < rows && ok; r++) {
            var fv = fine.values[r], cv = coarse.values[r];
            if (fv === null || cv === null) continue;
            if (map.hasOwnProperty(fv) && map[fv] !== cv) ok = false; else map[fv] = cv;
          }
          if (ok) { h.hierarchy = true; roles.hierarchy = [coarse.name, fine.name]; break; }
        }
      }
    }
    // Only a real nested path (not a name-token match) drops distribution hints
    if (path) {
      delete h.repeatedGroups; delete h.bigGroups; delete h.multiCatStages;
      if (!h.ageGroup) delete h.twoSides;
    }

    // misc
    if (measures.some(function (c) { return RX.delta.test(c.name); }) || (h.signed && h.oneRowPerCat)) h.delta = true;
    if (measures.length && detectWaterfallBridge(measures[0], rows)) h.waterfallBridge = true;
    var stageCol = labels.filter(function (c) {
      if (RX.stage.test(c.name)) return true;
      var v = uniq(c.values);
      return v.length >= 3 && v.filter(function (s) { return RX.stageValue.test(String(s)); }).length / v.length >= 0.5;
    })[0];
    if (stageCol && measures.length) {
      h.stages = true;
      if (isMonotoneNonIncreasing(measures[0], rows)) h.monotoneStages = true;
    }
    if (measures.some(function (c) { return RX.targetName.test(c.name); }) && measures.length >= 2) h.target = true;
    var startCol = date.filter(function (c) { return RX.start.test(c.name); })[0];
    var endCol = date.filter(function (c) { return c !== startCol && RX.end.test(c.name); })[0];
    if (startCol && endCol) h.startEnd = true;
    if (bool.length >= 3) h.sets = true;
    if (measures.length >= 3) h.manyNumeric = true;
    if (measures.length >= 3) {
      var sizeCand = measures.filter(function (c) { return c.stats && c.stats.min >= 0; });
      if (sizeCand.length >= 1) h.sizeVar = true;
      if (measures.some(function (c) { return RX.size.test(c.name); })) h.sizeNamed = true;
    }
    if (h.oneRowPerCat && allNonNeg && primaryCat && primaryCat.distinct >= 2 && primaryCat.distinct <= 10) {
      var m0 = measures[0];
      var sum = m0.stats ? m0.stats.sum : 0;
      if (Math.abs(sum - 100) <= 1.5 || Math.abs(sum - 1) <= 0.015) h.partOfWhole = true;
    }

    return { counts: counts, rows: rows, hints: h, roles: roles };
  }

  // ---------------------------------------------------------------- engine
  function meetsRequires(rule, counts) {
    var miss = [];
    Object.keys(rule.requires || {}).forEach(function (k) {
      var rng = rule.requires[k];
      var have = counts[k] || 0;
      if (have < rng[0] || (rng[1] !== undefined && have > rng[1])) miss.push(k + '≥' + rng[0]);
    });
    return miss;
  }

  function hintOk(expr, hints) {
    return expr.split('|').some(function (k) { return k.charAt(0) === '!' ? !hints[k.slice(1)] : !!hints[k]; });
  }

  function hintLabel(expr, lang) {
    return expr.split('|').map(function (k) {
      if (k.charAt(0) === '!') { var b = HINTS[k.slice(1)]; return (lang === 'zh' ? '沒有：' : 'lacks: ') + (b ? b[lang] : k); }
      return HINTS[k] ? HINTS[k][lang] : k; }).join(lang === 'zh' ? ' 或 ' : ' or ');
  }

  /**
   * Evaluate all rules against a shape.
   * @returns array of { rule, score, eligible, reasons[], caveats[], missing[] } sorted by score desc.
   */
  function evaluate(shape, lang) {
    lang = lang === 'en' ? 'en' : 'zh';
    var out = RULES.map(function (rule, idx) {
      var missing = meetsRequires(rule, shape.counts);
      var needMissing = rule.need.filter(function (n) { return !hintOk(n, shape.hints); });
      var eligible = !missing.length && !needMissing.length;
      var score = rule.base;
      var reasons = [rule.why[lang]];
      var caveats = [];
      if (eligible) {
        rule.need.forEach(function (n) { score += NEED_BONUS; reasons.push('✓ ' + hintLabel(n, lang)); });
        rule.prefer.forEach(function (n) { if (hintOk(n, shape.hints)) { score += PREFER_BONUS; if (reasons.indexOf('+ ' + hintLabel(n, lang)) < 0) reasons.push('+ ' + hintLabel(n, lang)); } });
        rule.avoid.forEach(function (n) { if (hintOk(n, shape.hints)) { score -= AVOID_PENALTY; caveats.push(hintLabel(n, lang)); } });
      } else {
        score = 0;
      }
      return {
        rule: rule, id: rule.id, score: Math.max(0, Math.min(100, score)), eligible: eligible,
        reasons: reasons, caveats: caveats,
        missing: missing.concat(needMissing.map(function (n) { return hintLabel(n, lang); })),
        renderable: rule.render.length > 0, order: idx
      };
    });
    out.sort(function (a, b) {
      if (a.eligible !== b.eligible) return a.eligible ? -1 : 1;
      if (b.score !== a.score) return b.score - a.score;
      return a.order - b.order;
    });
    return out;
  }

  function recommend(profile, lang) {
    var shape = computeShape(profile);
    return { shape: shape, results: evaluate(shape, lang) };
  }

  function byId(id) { return RULES.filter(function (r) { return r.id === id; })[0] || null; }

  return { RULES: RULES, HINTS: HINTS, computeShape: computeShape, evaluate: evaluate, recommend: recommend, byId: byId };
});
