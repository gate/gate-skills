---
name: gate-info-alphaquant
version: "2026.7.13-2"
updated: "2026-07-13"
description: >
  Adaptive multi-factor Alpha quant engine for Gate markets. Use this skill when the user asks for:
  cross-sectional alpha ranking, multi-factor scoring, factor analysis (momentum / volatility /
  trend-quality / price-structure / volume), "which coins are strongest/weakest", "rank these tokens",
  "score BTC/ETH/SOL", relative strength screening, or a quant alpha snapshot on a basket of
  symbols. Reads free Gate market data (K-line) via Gate MCP, computes an Alpha158-derived factor
  library, weights factors adaptively by their recent IC/IR (self-correcting to momentum vs
  mean-reversion regimes), and returns a ranked shortlist with per-factor breakdown and a regime read.
  Read-only, no credentials required. Trigger on: 多因子, alpha 排名, 打分, 选币, 强弱排序,
  factor score, rank coins, alpha snapshot. Do NOT use for order placement (gate-exchange-trading)
  or single-coin news (gate-info-coinanalysis).
---

# Gate Info — Alpha Quant Engine

> Built by **阿尔法金融 AI 实验室 (Alpha Finance AI Lab)**. A transparent, reproducible
> Built by **阿尔法金融 AI 实验室 (Alpha Finance AI Lab)**. A transparent, reproducible,
> **regime-adaptive** multi-factor ranking engine on top of Gate's free market data.
> Alpha158-derived factors, weighted by live IC/IR. Informational only.

## What it does

Given a basket of symbols, this skill pulls recent OHLCV from Gate's free market MCP,
computes a library of **Alpha158-derived factors** (ported from Microsoft Qlib's public
factor expressions), normalizes them cross-sectionally (z-score), and — critically —
**weights them adaptively by their recent IC/IR** (Information Coefficient / Information
Ratio) rather than fixed hand-picked weights. It then blends them into one composite
**Alpha Score** and outputs a ranked long/short shortlist with a full per-factor breakdown
plus a **market-regime read** (momentum vs mean-reversion), so the user sees *why* each
coin ranks where it does.

Why IC/IR weighting matters: factor efficacy flips with regime. In a mean-reverting market,
past winners underperform — a fixed "momentum = good" weight would rank backwards. By
measuring each factor's actual forward-return correlation over the lookback, the engine
**self-corrects to the current regime** and flips factor signs when the data demands it.

No black box. Every score, weight, and IC is explainable and reproducible.

## When to trigger

- "给这些币做个多因子排名 / rank these coins"
- "现在哪些币最强 / 最弱" (relative strength)
- "BTC ETH SOL 打个分" (score a basket)
- "alpha 快照 / alpha snapshot"
- "选币 / 截面因子 / factor screen"

Do NOT trigger for: placing orders, single-coin deep fundamentals, news explanation.

## Inputs (collect from user, then proceed)

1. **Symbol universe** — a list of Gate spot/perp symbols (e.g. `BTC_USDT`, `ETH_USDT`, `SOL_USDT`).
   If the user gives none, default to a liquid top-10 basket and say so. IC/IR weighting is
   more robust with **≥8 symbols**; below that, fall back to equal-weight and note it.
2. **Lookback window** — default `120` daily bars. Accept `60 / 90 / 120 / 180`.
3. **Timeframe** — default `1d`. Accept `4h / 1d / 1w`.
4. **IC horizon** — forward-return bars used to score factors. Default `5`.

## The factor library (Alpha158-derived)

Seventeen factors ported to plain arithmetic from Qlib's Alpha158 expressions, spanning five
families. Full formulas in `references/alpha-methodology.md`; the source catalog of all 158
is in `references/alpha158-catalog.md`.

| Family | Factors | Captures |
|--------|---------|----------|
| **Momentum** | ROC5, ROC20, ROC60 | multi-horizon rate of change |
| **Trend quality** | BETA20 (slope), RSQR20, RSQR60 (R² of linear fit) | how *clean* the trend is |
| **Volatility** | STD5, STD20 | realized dispersion |
| **Price structure** | MA5, MA20, MAX20, MIN20, RSV20 (stochastic) | position within range |
| **Candle / volume** | KMID, KSFT, VMA20, CORR20 (price-volume corr) | intrabar pressure + participation |

Factor **signs are NOT assumed** — each factor's direction is set by its measured IC (below).

## Workflow

1. **Resolve inputs.** Confirm symbol universe + window + timeframe. If universe missing, use default top-10 and state it. Normalize each symbol to Gate's format (`BASE_QUOTE`, e.g. `BTC_USDT`); if a symbol is not listed on Gate, drop it and report it under "Dropped" rather than failing the whole run.
2. **Fetch data.** For each symbol call Gate MCP `cex_spot_get_spot_candlesticks` (endpoint `/mcp`, no auth). Retry once on transient failure; drop symbols with insufficient bars OR that are not listed on Gate, and report them.
3. **Compute factors** per symbol across the full history panel (see `alpha-methodology.md`).
4. **Cross-sectional z-score** each factor per date across the universe (mean 0, std 1). Winsorize at ±3σ.
5. **IC/IR per factor.** For each date, compute the Spearman rank IC between the factor's
   cross-section and the forward `H`-bar return; collect the IC time series; then
   **IR = mean(IC) / std(IC)**. This measures both strength and *consistency* of the signal.
6. **Adaptive weights.** Weight each factor by its IR (sign included), normalized by Σ|IR|.
   Factors with negative IC get negative weight — the engine flips them automatically.
   If <10 valid IC observations, fall back to equal weight and disclose it.
7. **Composite score** = Σ (weight × latest cross-sectional z). Rank descending.
8. **Regime read.** If momentum factors (ROC*) carry negative net weight → mean-reverting
   regime; positive → trending. State this in plain language.
9. **Render** the report using the template below.

## Report template

```
🔮 Alpha Quant Snapshot v2 — <N> symbols · <timeframe> · <window> bars · IC horizon <H>
Engine: Alpha Finance AI Lab · data: Gate (free market) · <UTC timestamp>
Regime: <MEAN-REVERTING | TRENDING> (momentum net weight <sign>)

Most predictive factors now (by |IR|)
Factor | IC | IR | weight
RSV20  | +0.11 | +0.36 | +0.13
...

RANKING (composite alpha)
# | Symbol | Alpha | top +contributors | top −contributors
1 | BNB_USDT | +0.34 | RSV20, CORR20 | ROC60
...

Dropped (insufficient / unlisted): <list or none>
```

Then add 2-3 sentences of plain-language read, e.g. "The book is mean-reverting right now —
momentum (ROC) shows negative IC, so recent laggards screen best. BNB tops on stochastic
position and price-volume confirmation; ADA is weakest." Always state the regime and the
modest absolute IC levels honestly (real factors on a small crypto basket run IC ≈ 0.05–0.15).

## Guardrails

- **Read-only.** Never place or suggest a specific order. This is research, not advice.
- **No fabricated numbers.** Every figure must come from fetched data or a shown computation. If a fetch fails, say so — never invent bars.
- **Explainability first.** Always show the per-factor breakdown, never just a single opaque score.
- **State assumptions.** Default universe, lookback, IC horizon, and any equal-weight fallback must be disclosed when used.
- **Report IC honestly.** Show real IC/IR values; never inflate. Real factors on a small crypto basket typically show IC ≈ 0.05–0.15 — present them as-is.
- Append once: "Informational only, not investment advice. Digital assets are volatile."

## Deeper reference

- `references/alpha-methodology.md` — exact factor formulas, z-score, IC/IR weighting, edge cases.
- `references/alpha158-catalog.md` — the full 158-factor source catalog (Qlib Alpha158 expressions).
- `references/report-examples.md` — worked example outputs.

## About the Lab

Contributed by **阿尔法金融 AI 实验室 (Alpha Finance AI Lab)** — an independent contributor
focused on transparent, reproducible quant tooling for AI agents. This skill is fully open
and free to use on Gate. Feedback and PRs welcome.
