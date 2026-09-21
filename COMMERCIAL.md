# Commercial use（團隊怎麼省分析師工時）

Open-core：核心 skill（推薦圖種 + 口述怎麼做 + 39 patterns）保持 MIT。
這份文件只講**誰會省時間、什麼可以另外談**——不設付費牆。

## Who this is for

| Team | Pain today | What this skill replaces | Hours it usually eats |
|------|------------|--------------------------|------------------------|
| **IR / earnings decks** | Slide owners default to pie + dual-axis; CFOs then ask “從毛利怎麼走到營業利益？” | Waterfall, slope, dumbbell, bullet KPI — with a one-line takeaway | 0.5–2 days per deck rewriting the wrong chart |
| **Ops / supply-chain dashboards** | Inventory and org trees get smashed into one pie; funnel stages get mixed units | Icicle / treemap for hierarchy; funnel with conversion rates and a named bottleneck | Recurring weekly “why doesn’t this match the table?” threads |
| **Research / digest writers** | Every brief reinvents “which chart?” from muscle memory | 39 named patterns + mix-up table (icicle ≠ sankey, dumbbell ≠ slope) | 30–90 min per figure, plus review loops |
| **Consulting / client workshops** | Junior staff cannot defend why *this* chart, not a nightingale rose | zh-TW teaching format: 中文圖種名, 適不適合, 口述怎麼做 | Training time + rework after the client meeting |
| **Product / growth** | Signup → paid is drawn as a pretty funnel even when later stages exceed earlier ones | Shape checks catch broken funnels before they hit the exec Slack | False-alarm fire drills |

Numbers above are **planning ranges, not audited case studies**. Label any live client figure as 未核 until you check it.

## Offers (talk, don’t click a fake checkout)

The core stays free. If you want someone to sit with your data:

1. **Custom viz** — one messy workbook → a defendable figure + takeaway sentence.
2. **Skill packs** — extra patterns for your industry (bank subjects, hospital pathways, public-budget trees).
3. **Training** — a short workshop: Taiwan report readers, mix-up charts, “story sentence first.”

**Contact (no invented email or payment link):**

- Open a GitHub Issue with the `chart-request` template, or
- Mention **`0xsaghm`** on the Issue.

GitHub Sponsors on `g0uv4` is a **placeholder** until that page is actually enabled. Do not treat a 404 Sponsors URL as a payment method.

## What we will not do

- Paywall the 39 patterns or the recommendation loop.
- Send you a Stripe / PayPal link from this repo.
- Claim Origin, Cloudflare Access, or a hosted SaaS is required to use the skill.

## How to evaluate in one afternoon

1. Install: `grok plugin install g0uv4/what-is-the-data-saying --trust`
2. Paste any prompt in [`demos/`](demos/README.md).
3. Ask the skill to defend 適不適合 against a pie or dual-axis default.
4. If that already saved a slide review, star the repo — then open an Issue if you want a pack built for your tables.
