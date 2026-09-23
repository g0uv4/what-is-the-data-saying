# What is the data saying（資料在說什麼）

**Open-core [Grok Build](https://github.com/xai-org/grok-build) skill — v0.3.3.**

Paste a table or report. Get **which chart**, **why not the usual pie**, and **how to make it**.

The differentiator is not another chart-chooser flowchart. It is **Nazh-grounded Taiwan zh-TW pedagogy** plus **42 named patterns** from real teach-viz lessons: 中文圖種名, 適不適合, 口述怎麼做.

[Install](#install-grok-build) · [30-second demo](#try-this-first) · [42 patterns](#42-named-patterns) · [Teams](COMMERCIAL.md) · [中文說明](#資料在說什麼)

> Star or fork if a first paste already beats your default pie.  
> Need a chart for *your* table? [Open a chart request](https://github.com/g0uv4/what-is-the-data-saying/issues/new?template=chart-request.yml).

## Install (Grok Build)

```bash
grok plugin install g0uv4/what-is-the-data-saying --trust
```

Local checkout:

```bash
git clone https://github.com/g0uv4/what-is-the-data-saying.git
cd what-is-the-data-saying
grok plugin validate .
grok plugin install . --trust
```

Then in the Grok TUI: `/what-is-the-data-saying`, or paste a table and say **「這份資料該怎麼畫」**.

```bash
grok plugin details what-is-the-data-saying
grok plugin update what-is-the-data-saying
```

## Try this first

Copy one block from [`demos/`](demos/README.md) into a new Grok chat. First-time wow cases:

| Demo | Shape | Chart you should hear |
|------|--------|------------------------|
| [Inventory tree](demos/01-inventory-icicle.md) | warehouse → category → SKU | **冰柱圖（icicle）** — not a pie |
| [Signup leak](demos/02-signup-funnel.md) | ordered stages + counts | **漏斗圖** — bottleneck named |
| [Gross → operating](demos/03-earnings-waterfall.md) | start + signed steps | **瀑布圖（bridge）** |
| [H1 vs H2 stores](demos/04-before-after-dumbbell.md) | same categories, two values | **啞鈴圖** — not a slope |
| [Two-period ranks](demos/05-two-period-slope.md) | entities × exactly two periods | **坡度圖** |

Each file is a **copy-paste prompt** plus the answer shape you can score against.

## What you get

1. **Shape check** — time / category / hierarchy / flow / geo, units, missing parents.
2. **One primary chart + 1–2 backups** — and the mix-up to avoid (icicle ≠ sankey, dumbbell ≠ slope).
3. **How to produce it** — story sentence first, then spoken steps, then a tool path.
4. **Taiwan report readers** — zh-TW titles, 新台幣 / 千元, 未核 when numbers are unchecked.

Reply format the skill always uses:

```
推薦：<中文圖種名>（英文名）— 為什麼：一句
備選：<圖型> — <何時改選>
避免：<常見誤用> — <原因>
讀者／輸出：<誰看、靜態 vs 互動>
pattern：examples/<slug>.md
```

## 42 named patterns

Full table: [`skills/what-is-the-data-saying/examples/README.md`](skills/what-is-the-data-saying/examples/README.md). Heuristics: [`references/chart-heuristics.md`](skills/what-is-the-data-saying/references/chart-heuristics.md).

Highlights: icicle / sunburst / treemap / voronoi tree · waterfall · funnel · dumbbell / slope / bump · **lollipop／棒棒糖** · **streamgraph／河流圖** · sankey / alluvial / chord · raincloud / ridgeline / beeswarm · hexbin / contour · **dot density** · **population pyramid／人口金字塔** · UpSet · bullet KPI · calendar heatmap · cartogram.

## For teams (hours, not a paywall)

Earnings decks, ops dashboards, and research digests still burn analyst time on the *wrong* figure. See [`COMMERCIAL.md`](COMMERCIAL.md) for B2B cases and what a custom pack looks like.

The **core skill stays MIT**. No hosted login wall.

## Support & custom work

| Want | Do this |
|------|---------|
| Say the skill helped | [Star](https://github.com/g0uv4/what-is-the-data-saying) or fork |
| “Which chart for *this* table?” | [New chart-request Issue](https://github.com/g0uv4/what-is-the-data-saying/issues/new?template=chart-request.yml) |
| Custom viz / skill packs / training | Open an Issue and mention **`0xsaghm`** — no invented email, no fake checkout |
| Sponsor | GitHub Sponsors on `g0uv4` is a **placeholder** until that page is enabled. Star or an Issue is the real signal today |

## Repo map

| Path | Role |
|------|------|
| `skills/what-is-the-data-saying/SKILL.md` | When to fire + the three-step loop |
| `references/` | Heuristics, produce-how, shape checks, Taiwan readers |
| `examples/` | 42 patterns (when / recommend / avoid / checklist) |
| `demos/` | Copy-paste first-run prompts |
| `COMMERCIAL.md` | Team use cases |
| `ATTRIBUTION.md` | Nazh teach-viz mapping |

Grow it: real report → was the pick right → new `examples/<slug>.md` + ATTRIBUTION row → `grok plugin update`.

## Attribution & license

Pedagogy and pattern names come from **納茲 - 資料視覺** teach-viz lessons. This repo is an executable summary, **not** the full lesson texts. Keep [`ATTRIBUTION.md`](skills/what-is-the-data-saying/ATTRIBUTION.md) when you share.

[MIT](LICENSE) · © 2026 g0uv4 · GitHub only (no Origin).

---

## 資料在說什麼

**開源核心的 Grok Build skill（v0.3.3）。** 丟進一張表或一份報表，它回答兩件事：**該畫哪種圖**、**怎麼做得出來**。

和一般「圖表選擇器」的差別：對齊納茲教圖的台灣繁體中文教學——先給中文圖種名（英文名）、適不適合、口述怎麼做，再給工具。內建 **42 個具名 pattern**，不是示意三張長條圖。

### 安裝

```bash
grok plugin install g0uv4/what-is-the-data-saying --trust
```

在 Grok TUI 輸入 `/what-is-the-data-saying`，或直接貼上資料說「這份資料該怎麼畫」。

### 先跑哪個 demo

到 [`demos/`](demos/README.md) 複製一則。庫存階層應聽到**冰柱圖**、漏斗應點名瓶頸階、損益橋應聽到**瀑布圖**、兩期同店應聽到**啞鈴圖**而不是坡度圖。

標題、軸、圖註、結論句用 **zh-TW**（營收／毛利／縣市／新台幣）；程式與變數名可用英文。數字沒核過就標「未核」。

### 給團隊／想做客製

法說會投影片、營運看板、研究摘要，最常耗掉的是「畫錯圖再重做」。用途與工時見 [`COMMERCIAL.md`](COMMERCIAL.md)。

核心不收費。客製圖、產業 skill pack、內訓：開 Issue 並提到 **`0xsaghm`**。不要寄信到這個 repo 裡不存在的信箱。GitHub Sponsors 僅預留，頁面沒開之前請用星標或 Issue。

覺得有用就 star／fork；缺一種圖就開 [chart request](https://github.com/g0uv4/what-is-the-data-saying/issues/new?template=chart-request.yml)。
