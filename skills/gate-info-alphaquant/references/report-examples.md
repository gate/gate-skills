# Alpha Quant — Worked Example Outputs

## Example 1 — Top-10 basket, 1d, 90 bars

User: "给主流币做个 alpha 排名"

```
🔮 Alpha Quant Snapshot — 10 symbols · 1d · 90 bars
Engine: Alpha Finance AI Lab · data: Gate (free market) · 2026-07-13T07:20Z

LONG SHORTLIST (top alpha)
# | Symbol    | Alpha | MOM   | TREND | VOL   | LIQ   | MR
1 | SOL_USDT  | +1.42 | +1.6  | +1.3  | +0.4  | +1.1  | +0.2
2 | BNB_USDT  | +0.88 | +0.9  | +1.1  | +0.7  | +0.1  | +0.3
3 | BTC_USDT  | +0.61 | +0.5  | +0.8  | +1.2  | -0.2  | +0.4

SHORT SHORTLIST (weakest)
# | Symbol    | Alpha | MOM   | TREND | VOL   | LIQ   | MR
1 | DOGE_USDT | -1.55 | -1.4  | -1.2  | -0.8  | -0.6  | -1.9
2 | XRP_USDT  | -0.92 | -1.0  | -0.7  | -0.5  | -0.3  | -0.8

Weights: MOM .30 / TREND .25 / VOL .15 / LIQ .15 / MR .15
Dropped (insufficient data): none
```

Read: "SOL leads on strong momentum and a clean rising-EMA trend with volume expansion.
DOGE screens weakest — negative momentum, choppy trend, and an overbought RSI dragging its
mean-reversion guard. BTC ranks mid-pack, carried by low volatility rather than raw momentum."

## Example 2 — Custom weights

User: "只看趋势和动量，波动率别算了"

Action: set weights MOM 0.5 / TREND 0.5 / VOL 0 / LIQ 0 / MR 0, disclose the override in the
report header, recompute the composite, re-rank.

## Example 3 — Insufficient data

User: "排一下 NEWTOKEN_USDT BTC_USDT ETH_USDT"

If `NEWTOKEN_USDT` has only 12 bars:

```
Dropped (insufficient data): NEWTOKEN_USDT (12 bars < 30 minimum)
```

Rank the remaining two, but note: "Only 2 symbols ranked — cross-sectional scores are less
robust with a tiny universe; add more symbols for a stronger read."
