# Basis Monitor

Monitor and analyze the spot-futures basis (price spread) for one or multiple cryptocurrencies. Evaluate current basis levels against historical averages, identify basis widening/narrowing trends, and generate signals for potential arbitrage or sentiment shifts.

## Workflow

When the user asks about basis or spot-futures spread, determine whether they want a single-coin analysis or a multi-coin scan, then execute accordingly.

### Step 1: Get spot prices

Call `get_spot_tickers` to retrieve spot market data.

- For single-coin analysis: pass `currency_pair` (e.g., `BTC_USDT`)
- For multi-coin scan: call without parameters to get all tickers, then filter to `_USDT` pairs

Key data to extract:
- Last price (spot reference price)
- 24h high/low
- 24h volume

### Step 2: Get futures prices

Call `get_futures_tickers` with:
- `settle`: `usdt`
- For single-coin: pass `contract` (e.g., `BTC_USDT`)
- For multi-coin: omit contract to get all

Key data to extract:
- Last price (futures price)
- Mark price
- Index price
- 24h volume
- Funding rate (for context)

### Step 3: Calculate current basis

For each coin with both spot and futures data:

```
basis = futures_price - spot_price
basis_rate = (futures_price - spot_price) / spot_price * 100%
```

- **Positive basis (futures premium / positive basis)**: Futures price > Spot price → Contango, typical in bullish markets
- **Negative basis (futures discount / negative basis)**: Futures price < Spot price → Backwardation, typical in bearish or uncertain markets

### Step 4: Get premium index history

For coins of interest (single-coin analysis or top anomalies in multi-coin scan), call `get_futures_premium_index` with:
- `contract`: the contract identifier
- `settle`: `usdt`
- `interval`: `1h` (hourly data points)
- `limit`: 168 (7 days of hourly data)

Key data to extract:
- Historical premium index values
- Calculate historical average basis
- Calculate standard deviation of basis
- Identify trend (widening / narrowing / stable)

### Step 5: Analyze basis deviation and trend

**Deviation analysis**:
- Calculate: `avg_basis` = mean of historical basis values
- Calculate: `std_basis` = standard deviation of historical basis values
- Calculate: `z_score = (current_basis - avg_basis) / std_basis`
- If `|z_score| > 2`: Basis is significantly deviating from historical norm

**Trend analysis**:
- Compare recent basis (last 24h average) vs longer-term basis (7-day average)
- If recent > long-term: Basis is **widening** (widening)
- If recent < long-term: Basis is **narrowing** (narrowing)
- If roughly equal (within 10%): Basis is **stable** (stable)

**Signal generation**:

| Condition | Signal | Implication |
|-----------|--------|-------------|
| Basis rate > 0.3% and widening | positive basis widening | Bullish sentiment strengthening, potential short futures arbitrage |
| Basis rate < -0.1% and widening | negative basis widening | Bearish sentiment strengthening, potential long futures arbitrage |
| \|z_score\| > 2 and basis narrowing | basis mean reversion | Basis reverting to mean, trend may be changing |
| \|z_score\| > 3 | extreme basis deviation | Extreme deviation, high-probability reversion opportunity |
| Basis flipped sign recently | basis flip | Sentiment shift signal |

## Report Template

### Single-Coin Report

```
# {COIN} Basis Analysis Report

> Analysis time: {current_datetime}
> Trading pair: {COIN}_USDT
> Data source: Gate.io

---

## Current Basis Status

| Metric | Value |
|------|------|
| Spot price | {spot_price} USDT |
| Futures price | {futures_price} USDT |
| Mark price | {mark_price} USDT |
| basis | {basis} USDT |
| Basis rate | {basis_rate}% |
| Basis direction | {positive basis (premium) / negative basis (discount)} |

---

## Historical Basis Analysis (Last 7 Days)

| Metric | Value |
|------|------|
| 7-day average basis rate | {avg_basis_rate}% |
| Basis standard deviation | {std_basis}% |
| Current deviation (Z-Score) | {z_score} |
| 7-day max basis | {max_basis}% |
| 7-day min basis | {min_basis}% |

### Basis Trend
- Last 24h average: {recent_avg}%
- Last 7d average: {weekly_avg}%
- Trend assessment: {widening / narrowing / stable}

---

## Signals and Interpretation

{Generated signals based on the analysis}

**Current State Interpretation**:
{Interpretation of what the current basis level and trend implies about market sentiment and potential opportunities}

---

## Arbitrage Reference

{If basis presents arbitrage opportunity:}
- Arbitrage direction: {forward arbitrage: buy spot + short futures / reverse arbitrage: sell spot + long futures}
- Current basis yield: {basis_rate}%
- Annualized reference (assuming basis persists): {annualized}%
- Execution suggestions: {practical considerations}

---

## Risk Alerts

1. Basis can change quickly with sentiment; history does not guarantee future moves.
2. Basis may swing sharply in extreme markets; arbitrage carries risk.
3. Include trading fees and funding impact in arbitrage returns.
4. This analysis is based on public market data, for reference only, and not investment advice.
```

### Multi-Coin Scan Report

When scanning multiple coins, use a summary table format:

```
# Full-Market Basis Scan Report

> Scan time: {current_datetime}
> Scope: all USDT perpetual contracts
> Data source: Gate.io

---

## Basis Ranking

### Top 10 Positive Basis (Futures Premium)

| # | Coin | Spot | Futures | Basis Rate | Trend | Signal |
|---|------|--------|--------|--------|------|------|
| 1 | {coin} | {spot} | {futures} | {rate}% | {trend} | {signal} |

### Top 10 Negative Basis (Futures Discount)

| # | Coin | Spot | Futures | Basis Rate | Trend | Signal |
|---|------|--------|--------|--------|------|------|
| 1 | {coin} | {spot} | {futures} | {rate}% | {trend} | {signal} |

---

## Market Overview

- Positive-basis contracts: {positive_count} ({positive_pct}%)
- Negative-basis contracts: {negative_count} ({negative_pct}%)
- Average basis rate: {avg_rate}%
- Extreme basis deviation count (|Z| > 2): {extreme_count}

## Summary

{Overall market basis sentiment interpretation}
```

## Important Notes

- Basis analysis is most meaningful for coins with sufficient liquidity in both spot and futures markets. Flag low-liquidity coins.
- The premium index from `get_futures_premium_index` provides a clean, exchange-calculated measure. Prefer it over manual spot-futures calculation when available.
- For multi-coin scans, only fetch premium index history for the top anomalies (e.g., top 5 by |basis_rate|) to avoid excessive API calls.
- Always explain the meaning of positive vs negative basis to the user, as not all users are familiar with these concepts.
- Cross-reference with funding rate — a high positive basis with high funding rate strongly suggests bullish crowding.
