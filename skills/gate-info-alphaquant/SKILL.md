---
name: gate-info-alphaquant
version: "2026.7.13-1"
updated: "2026-07-13"
description: >
  Multi-factor Alpha quant engine for Gate markets. Use this skill when the user asks for:
  cross-sectional alpha ranking, multi-factor scoring, factor analysis (momentum / volatility /
  volume / trend / mean-reversion), "which coins are strongest/weakest", "rank these tokens",
  "score BTC/ETH/SOL", relative strength screening, or a quant alpha snapshot on a basket of
  symbols. Reads free Gate market data (K-line / tickers) via Gate MCP, computes a transparent
  composite factor score, and returns a ranked long/short shortlist with per-factor breakdown.
  Read-only, no credentials required. Trigger on: 多因子, alpha 排名, 打分, 选币, 强弱排序,
  factor score, rank coins, alpha snapshot. Do NOT use for order placement (gate-exchange-trading)
  or single-coin news (gate-info-coinanalysis).
---

# Gate Info — Alpha Quant Engine

> Built by **阿尔法金融 AI 实验室 (Alpha Finance AI Lab)**. A transparent, reproducible
> multi-factor ranking engine on top of Gate's free market data. Informational only.

## What it does

Given a basket of symbols, this skill pulls recent OHLCV from Gate's free market MCP,
computes five orthogonal factors, normalizes them cross-sectionally (z-score), blends
them into one composite **Alpha Score**, and outputs a ranked long/short shortlist with a
full per-factor breakdown so the user sees *why* each coin ranks where it does.

No black box. Every score is explainable.

## When to trigger

- "给这些币做个多因子排名 / rank these coins"
- "现在哪些币最强 / 最弱" (relative strength)
- "BTC ETH SOL 打个分" (score a basket)
- "alpha 快照 / alpha snapshot"
- "选币 / 截面因子 / factor screen"

Do NOT trigger for: placing orders, single-coin deep fundamentals, news explanation.

## Inputs (collect from user, then proceed)

1. **Symbol universe** — a list of Gate spot/perp symbols (e.g. `BTC_USDT`, `ETH_USDT`, `SOL_USDT`).
   If the user gives none, default to a liquid top-10 basket and say so.
2. **Lookback window** — default `90` daily bars. Accept `30 / 60 / 90 / 180`.
3. **Timeframe** — default `1d`. Accept `4h / 1d / 1w`.

## The five factors

| Factor | Definition | Rationale |
|--------|-----------|-----------|
| **MOM** Momentum | trailing return over lookback (skip most-recent bar) | trend persistence |
| **TREND** Trend quality | % of bars above rising EMA(20) + EMA slope sign | clean vs choppy uptrend |
| **VOL** Volatility (inverted) | −1 × annualized realized vol | reward stability |
| **LIQ** Liquidity/volume thrust | recent avg quote-volume z vs its own history | participation / conviction |
| **MR** Mean-reversion guard | −1 × RSI(14) distance from 50, clipped | penalize overbought extremes |

## Workflow

1. **Resolve inputs.** Confirm symbol universe + window + timeframe. If universe missing, use default top-10 and state it. Normalize each symbol to Gate's format (`BASE_QUOTE`, e.g. `BTC_USDT`); if a symbol is not listed on Gate, drop it and report it under "Dropped" rather than failing the whole run.
2. **Fetch data.** For each symbol call Gate MCP `cex_spot_get_spot_candlesticks` (endpoint `/mcp`, no auth). Retry once on transient failure; drop symbols with insufficient bars OR that are not listed on Gate, and report them.
3. **Compute factors** per symbol (see reference `alpha-methodology.md`).
4. **Cross-sectional z-score** each factor across the universe (mean 0, std 1). Winsorize at ±3σ.
5. **Composite score** = weighted sum. Default weights: MOM 0.30, TREND 0.25, VOL 0.15, LIQ 0.15, MR 0.15. Allow user override.
6. **Rank** descending. TOP N (default 5) = long shortlist, BOTTOM N = short shortlist.
7. **Render** the report using the template below.

## Report template

```
🔮 Alpha Quant Snapshot — <N> symbols · <timeframe> · <window> bars
Engine: Alpha Finance AI Lab · data: Gate (free market) · <UTC timestamp>

LONG SHORTLIST (top alpha)
# | Symbol | Alpha | MOM | TREND | VOL | LIQ | MR
1 | ...

SHORT SHORTLIST (weakest)
# | Symbol | Alpha | MOM | TREND | VOL | LIQ | MR
...

Weights: MOM .30 / TREND .25 / VOL .15 / LIQ .15 / MR .15
Dropped (insufficient data): <list or none>
```

Then add 2-3 sentences of plain-language read (e.g. "SOL tops the basket on momentum + clean
trend; DOGE screens weakest on inverted volatility and overbought RSI").

## Guardrails

- **Read-only.** Never place or suggest a specific order. This is research, not advice.
- **No fabricated numbers.** Every figure must come from fetched data or a shown computation. If a fetch fails, say so — never invent bars.
- **Explainability first.** Always show the per-factor breakdown, never just a single opaque score.
- **State assumptions.** Default universe/weights must be disclosed when used.
- Append once: "Informational only, not investment advice. Digital assets are volatile."

## Deeper reference

- `references/alpha-methodology.md` — exact factor formulas, normalization, edge cases.
- `references/report-examples.md` — worked example outputs.

## About the Lab

Contributed by **阿尔法金融 AI 实验室 (Alpha Finance AI Lab)** — an independent contributor
focused on transparent, reproducible quant tooling for AI agents. This skill is fully open
and free to use on Gate. Feedback and PRs welcome.
