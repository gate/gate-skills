# Alpha Quant v2 — Worked Example Outputs

## Example 1 — Top-12 basket, 1d, 120 bars, IC horizon 5

User: "给主流币做个 alpha 排名"

```
🔮 Alpha Quant Snapshot v2 — 12 symbols · 1d · 120 bars · IC horizon 5
Engine: Alpha Finance AI Lab · data: Gate (free market) · 2026-07-13T10:11Z
Regime: MEAN-REVERTING (momentum net weight negative)

Most predictive factors now (by |IR|)
Factor | IC     | IR     | weight
RSV20  | +0.109 | +0.356 | +0.13
STD5   | -0.110 | -0.309 | -0.11
CORR20 | +0.089 | +0.268 | +0.10
MAX20  | -0.087 | -0.259 | -0.09
ROC60  | -0.084 | -0.242 | -0.09
RSQR20 | -0.065 | -0.211 | -0.08

RANKING (composite alpha)
#  | Symbol    | Alpha  | top +contrib | top -contrib
1  | BNB_USDT  | +0.342 | RSV20, CORR20 | ROC60
2  | LINK_USDT | +0.291 | RSV20         | STD5
3  | LTC_USDT  | +0.276 | CORR20        | MAX20
4  | ETH_USDT  | +0.253 | RSV20         | ROC20
5  | BTC_USDT  | +0.202 | STD5(low vol) | ROC60
...
11 | DOT_USDT  | -0.486 | —             | ROC60, MAX20
12 | ADA_USDT  | -0.733 | —             | ROC20, RSQR20

Dropped (insufficient / unlisted): none
```

Read: "The book is **mean-reverting** right now — momentum (ROC) shows negative IC, so recent
laggards actually screen best and past leaders are penalized. The strongest live signals are
stochastic position (RSV20) and price-volume confirmation (CORR20), plus a low-volatility
preference (STD5 negative IC). BNB tops the basket; ADA is weakest, dragged by strong recent
momentum that the current regime punishes. Absolute IC ≈ 0.09–0.11 — modest but consistent,
as expected for a small crypto daily basket. Informational only, not investment advice."

## Example 2 — Regime flip

If the same engine is run in a **trending** market, momentum IC turns positive, ROC factors
get positive weights, `mom_weight > 0`, and the header reads `Regime: TRENDING`. The exact
same code ranks past winners at the top — no manual retuning. This automatic sign-flip is the
core value of IC/IR weighting vs fixed weights.

## Example 3 — Thin universe fallback

User: "排一下 BTC_USDT ETH_USDT SOL_USDT"

Only 3 symbols (< 8). Cross-sectional IC is unreliable, so the engine falls back to
**equal-weight z-score blend** and states: "Only 3 symbols — IC/IR weighting needs ≥8 for a
stable cross-section, so this run uses equal factor weights. Add more symbols for adaptive
weighting."
