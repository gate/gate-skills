# Coin Deep Analysis

Generate a structured deep analysis report for a given cryptocurrency by orchestrating multiple Gate API calls, applying quantitative judgment logic, and producing a comprehensive report covering trend, liquidity, sentiment, and risk.

## Workflow

When the user asks to analyze a coin (e.g., "analyze BTC in detail"), extract the coin symbol from the user's message, then execute the following steps in order.

### Step 1: Identify the coin and trading pair

Extract the coin symbol from the user's input. Normalize it to uppercase (e.g., "btc" -> "BTC"). The default quote currency is USDT, so the trading pair is `{COIN}_USDT` (e.g., `BTC_USDT`), and the futures contract is `{COIN}_USDT` (e.g., `BTC_USDT`).

### Step 2: Call Gate API tools in sequence

Call the following 6 tools in order. If any call fails (e.g., futures contract does not exist), note it and continue with the remaining tools — do not abort the entire analysis.

#### 2.1 get_currency

Call `get_currency` with the coin symbol to retrieve basic coin information.

Key data to extract:
- Coin name, chain info
- Whether deposits and withdrawals are enabled
- Trade status

#### 2.2 get_currency_pair

Call `get_currency_pair` with `{COIN}_USDT` to get trading pair details.

Key data to extract:
- Price precision, amount precision
- Min order amount, min order value
- Trading fee tier
- Trade status

#### 2.3 get_spot_candlesticks

Call `get_spot_candlesticks` with:
- `currency_pair`: `{COIN}_USDT`
- `interval`: `1d` (daily candles)
- `limit`: 30 (last 30 days)

Key data to extract:
- Recent price trend (rising / falling / sideways)
- Current price vs 7-day and 30-day highs/lows
- Support and resistance levels (recent lows and highs)
- Daily trading volumes for volume change analysis

**Volume analysis**: Compare the most recent day's trading volume to the average of the previous 7 days. If `latest_volume / avg_7d_volume > 3.0` (i.e., 200% increase), flag as **"Abnormal Volume Spike"** (Abnormal Volume Spike).

#### 2.4 get_spot_order_book

Call `get_spot_order_book` with:
- `currency_pair`: `{COIN}_USDT`
- `limit`: 20

Key data to extract:
- Top bid and ask prices (spread)
- Total bid volume vs total ask volume
- Order book depth distribution

**Bid-Ask ratio analysis**: Calculate `total_bid_volume / total_ask_volume`. If this ratio < 0.7, flag as **"Heavy Selling Pressure"** (Heavy Selling Pressure).

#### 2.5 get_spot_trades

Call `get_spot_trades` with:
- `currency_pair`: `{COIN}_USDT`
- `limit`: 100

Key data to extract:
- Recent trade frequency and size
- Proportion of buy vs sell trades
- Any unusually large single trades (whale activity)

#### 2.6 get_futures_funding_rate

Call `get_futures_funding_rate` with:
- `contract`: `{COIN}_USDT`
- `settle`: `usdt`
- `limit`: 10

If this call fails (contract does not exist), skip the funding rate section and note "No futures contract available for this coin" in the report.

Key data to extract:
- Latest funding rate
- Funding rate trend over recent periods

**Funding rate analysis**: If the latest funding rate > 0.0005 (i.e., > 0.05%), flag as **"Long Crowding"** (Long Crowding). If the funding rate < -0.0005, note "Short Crowding" (Short Crowding) as well.

## Judgment Logic Summary

Apply these three checks and collect all triggered flags for the risk section:

| Condition | Flag | Meaning |
|-----------|------|---------|
| Latest funding rate > 0.05% (0.0005) | Long Crowding | Excessive long positioning, potential correction risk |
| Bid volume / Ask volume < 0.7 | Heavy Selling Pressure | Sell-side dominance, downward pressure |
| Latest 24h volume > 3x avg of previous 7 days | Abnormal Volume Spike | Unusual volume spike, could signal major move |

## Report Template

Generate the report in the following structure. Use the actual data obtained from the API calls. All numerical values should be formatted appropriately (e.g., prices with proper decimals, volumes with units, percentages with % sign).

```
# {COIN} Deep Analysis Report

> Analysis time: {current_datetime}
> Trading pair: {COIN}_USDT
> Data source: Gate.io

---

## 1. Basic Information

- Coin name: {name}
- Chain: {chain}
- Deposit/withdraw status: {deposit_status} / {withdraw_status}
- Trade status: {trade_status}
- Price precision: {price_precision} | Amount precision: {amount_precision}
- Min order amount: {min_amount} | Min order value: {min_value} USDT

---

## 2. Trend Analysis

### Current Price
- Latest price: {latest_price} USDT
- 24h change: {change_24h}%

### Candlestick Trend (Last 30 Days)
- 30-day high: {high_30d} USDT
- 30-day low: {low_30d} USDT
- 7-day high: {high_7d} USDT
- 7-day low: {low_7d} USDT
- Trend assessment: {trend_description}

### Key Levels
- Support: {support_level} USDT
- Resistance: {resistance_level} USDT

---

## 3. Liquidity Analysis

### Order Book Depth
- Best bid: {best_bid} | Best ask: {best_ask}
- Bid-ask spread: {spread} ({spread_pct}%)

### Bid/Ask Ratio
- Total bid volume: {total_bid_volume}
- Total ask volume: {total_ask_volume}
- Bid/ask ratio: {bid_ask_ratio}
{if bid_ask_ratio < 0.7: "⚠️ Heavy Selling Pressure: bid-side strength is weak; short-term downside pressure may remain."}

### Recent Trades
- Recent trade count: {trade_count}
- Large trade share: {large_trade_pct}%
- Aggressive buy/sell ratio: {buy_pct}% / {sell_pct}%

---

## 4. Market Sentiment

### Funding Rate
{if futures available:}
- Latest funding rate: {latest_funding_rate}%
- Recent trend: {funding_rate_trend}
{if funding_rate > 0.05%: "⚠️ Long Crowding: elevated funding raises long carry cost; watch for pullback risk."}
{if futures not available:}
- No perpetual futures contract is available for this coin; funding data unavailable.

### Volume Change
- Latest 24h volume: {latest_volume}
- Previous 7-day average volume: {avg_7d_volume}
- Volume ratio: {volume_ratio}x
{if volume_ratio > 3.0: "⚠️ Abnormal Volume Spike: volume is far above recent average; check for major catalysts."}

---

## 5. Risk Alerts

{List all triggered flags here, with brief explanation for each}

{If no flags triggered: "No obvious anomaly signals are currently detected; market state appears relatively stable."}

---

## 6. Summary and Suggestions

{Provide a brief overall assessment based on all the data above, including:}
- Overall trend outlook
- Key levels to watch
- Risk factors to be aware of
- A reminder that this is data-driven analysis, not investment advice
```

## Important Notes

- Always remind the user at the end: "This analysis is based on on-chain and exchange public data, for reference only, and not investment advice."
- If the coin symbol is not found or the trading pair does not exist, inform the user clearly and suggest checking the symbol.
- All flags (Long Crowding / Heavy Selling Pressure / Abnormal Volume Spike) should be prominently displayed in the risk section with warning icons.
- Format large numbers with appropriate units (e.g., 1.2M, 350K) for readability.
- The report should be in English by default.
