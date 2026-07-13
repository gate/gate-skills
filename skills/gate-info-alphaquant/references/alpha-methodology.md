# Alpha Quant — Methodology Reference

Exact formulas for the five factors. All computed per symbol on the chosen timeframe over
`W` bars, then cross-sectionally normalized across the universe.

Notation: `C[t]` = close, `V[t]` = quote volume, `t=0` most recent bar.

## 1. MOM — Momentum

Trailing return, skipping the most recent bar to reduce microstructure noise:

```
MOM_raw = C[1] / C[W-1] - 1
```

Use `C[1]` (not `C[0]`) as the near leg. Longer window → slower signal.

## 2. TREND — Trend quality

Combine EMA-slope sign and above-EMA fraction:

```
ema = EMA(C, span=20)
above_frac = mean( C[t] > ema[t]  for t in 0..W-1 )      # 0..1
slope_sign = sign( ema[0] - ema[min(20, W-1)] )          # -1/0/+1
TREND_raw  = above_frac * slope_sign
```

Rewards symbols that spend most bars above a *rising* EMA; punishes choppy/declining.

## 3. VOL — Volatility (inverted)

Annualized realized volatility of log returns, negated so lower vol scores higher:

```
r[t]      = ln(C[t] / C[t+1])
sigma     = std(r) * sqrt(bars_per_year)   # 365 for 1d, 365*6 for 4h, 52 for 1w
VOL_raw   = -sigma
```

## 4. LIQ — Liquidity / volume thrust

Recent participation vs the symbol's own history (self-referential z, then used raw
before cross-sectional z):

```
v_recent  = mean(V[0..9])       # last 10 bars
v_base    = mean(V[10..W-1])
LIQ_raw   = (v_recent - v_base) / (std(V[10..W-1]) + eps)
```

Captures volume expansion / conviction.

## 5. MR — Mean-reversion guard

Penalize overbought extremes using RSI(14) distance from neutral 50:

```
rsi       = RSI(C, 14)[0]
MR_raw    = -(abs(rsi - 50) if rsi > 70 or rsi < 30 else 0) / 50
```

Only bites at extremes; neutral in the normal 30–70 band.

## Cross-sectional normalization

For each factor F across the universe:

```
z_F = (F_raw - mean(F_raw)) / (std(F_raw) + eps)
z_F = clip(z_F, -3, +3)          # winsorize
```

## Composite

```
Alpha = 0.30*z_MOM + 0.25*z_TREND + 0.15*z_VOL + 0.15*z_LIQ + 0.15*z_MR
```

Weights are user-overridable. Rank descending.

## Edge cases

- **Symbol not listed on Gate** → drop symbol, list under "Dropped" with reason (e.g. `TON_USDT (not listed on Gate)`). Never fail the whole run for one bad symbol.
- **< 30 bars available** → drop symbol, list under "Dropped".
- **Single-symbol universe** → cross-sectional z undefined; return raw factors + a note that ranking needs ≥3 symbols.
- **Zero-volume bars** → forward-fill volume; if >30% zero, drop symbol.
- **NaN / gaps** → linear-interpolate ≤2 consecutive gaps, else drop.
- **MR silent in neutral regimes** → the mean-reversion guard is 0 for every symbol whose RSI(14) sits in the 30–70 band. This is by design: MR only penalizes true overbought/oversold extremes. In a calm, range-bound market MR contributes nothing and the composite is effectively driven by MOM/TREND/VOL/LIQ. Note this in the report when MR is zero across the board.

## Determinism

Same inputs + same data snapshot → identical output. No randomness. Timestamp every report
with the data fetch time (UTC) so results are reproducible and auditable.
