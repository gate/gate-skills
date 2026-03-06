# Liquidation Anomaly Monitor

Monitor liquidation (forced closure) events across futures markets to detect abnormal liquidation spikes, directional squeezes, and pin-bar events. Produce a structured report highlighting coins with unusual liquidation activity and their market context.

## Workflow

When the user asks about liquidation activity, execute the following steps.

### Step 1: Get liquidation orders

Call `list_futures_liq_orders` with:
- `settle`: `usdt`
- `limit`: 100 (get recent liquidation records)

If the user specifies a time range, use the `from` and `to` parameters accordingly.

For a specific coin analysis, also call with `contract` parameter to filter.

Key data to extract:
- Liquidation time, contract, size, price
- Liquidation direction (long or short position being liquidated)
- Group liquidations by contract and by time window

### Step 2: Aggregate and analyze liquidation data

Group the liquidation data by contract and compute:

1. **Hourly liquidation volume**: Sum of liquidation sizes in the most recent 1-hour window
2. **Daily average liquidation volume**: Average hourly liquidation volume over the past 24 hours (or available data range)
3. **Directional breakdown**: Percentage of long liquidations vs short liquidations per contract

### Step 3: Get price context with candlesticks

For each contract showing anomalous liquidation, call `get_futures_candlesticks` with:
- `contract`: the contract identifier
- `settle`: `usdt`
- `interval`: `1h` (hourly candles)
- `limit`: 24 (last 24 hours)

Key data to extract:
- Price at time of liquidation spike
- Current price vs liquidation price (has price recovered?)
- High-low range of the candle during liquidation (wick/shadow length for pin-bar detection)
- Overall price trend context

### Step 4: Get current market state

For contracts with anomalous liquidation, call `get_futures_tickers` with:
- `contract`: the contract identifier
- `settle`: `usdt`

Key data to extract:
- Current price, mark price
- 24h volume, open interest
- Funding rate (for sentiment context)

## Judgment Logic

Apply these three checks to each contract and collect all triggered flags:

| Condition | Flag | Meaning |
|-----------|------|---------|
| 1h liquidation volume > 3x daily average hourly volume | abnormal liquidation | Liquidation spike significantly above normal levels |
| Long (or short) liquidations > 80% of total | Long Squeeze / Short Squeeze | Directional squeeze — one side being wiped out |
| Price has recovered > 50% of the drop/spike that caused liquidations | wick event | Pin-bar / wick event — price spiked to liquidate and reversed |

### Detailed judgment:

**abnormal liquidation (Abnormal Liquidation)**:
- Calculate: `hourly_liq_volume` for the most recent hour
- Calculate: `avg_hourly_liq_volume` = total liquidation volume in available data / number of hours
- If `hourly_liq_volume > 3 * avg_hourly_liq_volume` → flag

**Long Squeeze / Short Squeeze (Long/Short Squeeze)**:
- Calculate: `long_liq_pct` = long liquidation volume / total liquidation volume
- If `long_liq_pct > 80%` → flag "Long Squeeze" (Long Squeeze)
- If `short_liq_pct > 80%` (i.e., `long_liq_pct < 20%`) → flag "Short Squeeze" (Short Squeeze)

**wick event (Pin-bar / Wick Event)**:
- Identify the candle with the largest liquidation activity
- Check if the candle has a long wick: `wick_ratio = |high - low| / |open - close|`
- Check if current price has recovered: compare current price to the extreme price of that candle
- If current price recovered > 50% of the move → flag "wick event"

## Report Template

```
# Liquidation Anomaly Monitoring Report

> Monitoring time: {current_datetime}
> Data range: last 24 hours
> Settlement currency: USDT

---

## Global Overview

- Monitored contracts: {total_contracts}
- Total liquidation value: ${total_liq_value}
- Long liquidation share: {long_liq_pct}%
- Short liquidation share: {short_liq_pct}%
- Anomalous contracts: {anomaly_count}

---

## Anomalous Contract Details

### ⚠️ {rank}. {COIN}_USDT

| Metric | Value |
|------|------|
| Last 1h liquidation volume | ${hourly_liq_volume} |
| Daily average hourly liquidation volume | ${avg_hourly_liq_volume} |
| Liquidation multiple | {liq_ratio}x (vs daily average) |
| Long liquidation share | {long_pct}% |
| Short liquidation share | {short_pct}% |
| Current price | {current_price} USDT |
| Liquidation-time price | {liq_price} USDT |
| Price recovery status | {recovery_description} |

**Anomaly Flags**:
{flags with explanations}

**Market Context**:
{brief price context from candlestick data}

(Repeat for each anomalous contract, sorted by liquidation volume)

---

## Market Interpretation

{Overall market liquidation analysis:}
- Which side (long/short) is getting hurt more across the market
- Whether liquidations are concentrated in specific coins or widespread
- Correlation with price movements

---

## Risk Alerts

1. After large liquidation events, volatility can intensify; trade cautiously.
2. Wick events indicate liquidity gaps; pay attention to stop-loss setup.
3. After concentrated long/short squeezes, trend reversals may occur.
4. This analysis is based on on-chain liquidation data, for reference only, and not investment advice.
```

## Important Notes

- If no anomalous liquidation events are found, inform the user that the market liquidation activity is within normal range and provide a brief summary of overall liquidation levels.
- When the user asks about a specific coin, focus the analysis on that coin but also mention if there are broader market liquidation trends.
- Large liquidation events often cluster together — present them chronologically when relevant to show the cascade effect.
- Always provide price context — raw liquidation numbers without price reference are hard to interpret.
