# Alpha Quant v2 — Methodology Reference

Alpha158-derived factor library + IC/IR adaptive weighting. All factors are plain-arithmetic
ports of Microsoft Qlib's public Alpha158 expressions (see `alpha158-catalog.md` for the full
158). Computed per symbol on the chosen timeframe over `W` bars, then normalized
cross-sectionally across the universe and weighted by measured predictive power.

Notation: `C`=close, `O`=open, `H`=high, `L`=low, `V`=volume. `Ref(x,n)`=value n bars ago.
`Mean/Std/Max/Min(x,n)`=rolling window stat. All ratios divide by `C` to be scale-free.

## Factor formulas (the 17 used)

### Momentum
```
ROC5  = Ref(C,5)/C
ROC20 = Ref(C,20)/C
ROC60 = Ref(C,60)/C
```

### Trend quality
```
BETA20 = Slope(C,20)/C          # OLS slope of close over 20 bars, scaled
RSQR20 = Rsquare(C,20)          # R^2 of linear fit over 20 bars (0..1) — trend cleanliness
RSQR60 = Rsquare(C,60)
```

### Volatility
```
STD5  = Std(C,5)/C
STD20 = Std(C,20)/C
```

### Price structure
```
MA5   = Mean(C,5)/C
MA20  = Mean(C,20)/C
MAX20 = Max(H,20)/C
MIN20 = Min(L,20)/C
RSV20 = (C - Min(L,20)) / (Max(H,20) - Min(L,20) + 1e-12)   # stochastic position 0..1
```

### Candle / volume
```
KMID   = (C - O)/O                          # body
KSFT   = (2C - H - L)/O                      # close pressure within bar
VMA20  = Mean(V,20)/(V + 1e-12)              # volume vs its 20-bar average
CORR20 = Corr(C, log(V+1), 20)              # price-volume co-movement
```

Adding more from the 158 catalog is a drop-in: implement the expression, register it in the
factor map. No sign assumptions are baked in — direction is data-driven (below).

## Cross-sectional normalization

For each factor F, on each date t, across the universe:
```
z_F,t = clip( (F - mean_x(F)) / (std_x(F) + eps), -3, +3 )
```
(`mean_x` / `std_x` are taken across symbols at that date — the cross-section.)

## IC / IR (the core upgrade)

For each factor, measure how well its cross-section predicts the **forward H-bar return**
`r_fwd,t = C[t+H]/C[t] - 1` (default H=5):

```
IC_t = Spearman( z_F,t  ,  r_fwd,t )     # rank correlation across symbols, per date
IC   = mean_t(IC_t)                       # average information coefficient
IR   = mean_t(IC_t) / std_t(IC_t)         # information ratio — strength AND consistency
```

Require ≥10 valid dated IC observations, else fall back to equal weight (disclose it).

## Adaptive weighting

```
w_F = IR_F / Σ|IR|            # signed, normalized
```

- A factor with **negative IC** gets a **negative weight** → the engine automatically flips
  factors that are working in reverse for the current regime.
- Strong, *consistent* signals (high |IR|) dominate; noisy ones are damped.

## Composite & ranking

```
Alpha_s = Σ_F  w_F × z_F,latest(s)
```
Rank symbols by `Alpha` descending. Report per-symbol top +/− factor contributors.

## Regime read

```
mom_weight = w_ROC5 + w_ROC20 + w_ROC60
mom_weight < 0  → MEAN-REVERTING regime (past winners underperform)
mom_weight > 0  → TRENDING regime (momentum persists)
```
State this explicitly — it is the single most useful line for the user.

## Edge cases

- **Symbol not listed on Gate** → drop, list under "Dropped"; never fail the whole run.
- **< 80 bars available** → drop symbol (need history for W + IC horizon).
- **< 8 symbols** → cross-section thin; IC/IR unreliable → equal-weight fallback + note.
- **< 10 IC observations for a factor** → drop that factor from the blend.
- **NaN factor cells** → treated as 0 contribution after z-scoring; note if pervasive.
- **Determinism** → same inputs + same data snapshot → identical output. No randomness.
  Timestamp every report with the fetch time (UTC) for reproducibility.

## Honesty on magnitudes

Real single factors on a ~10-symbol crypto daily basket produce IC ≈ 0.05–0.15 and
IR ≈ 0.15–0.40. These are legitimate, non-overfit levels. Never present inflated IC or a
suspiciously smooth equity curve — the value is the *adaptive, explainable* blend, not a
fantasy number.
