# Coin Deep Analysis

Generate a structured deep analysis report for a given cryptocurrency by orchestrating multiple Gate API calls, applying quantitative judgment logic, and producing a comprehensive report covering trend, liquidity, sentiment, and risk.

## Workflow

When the user asks to analyze a coin (e.g., "帮我分析一下 BTC"), extract the coin symbol from the user's message, then execute the following steps in order.

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

**Volume analysis**: Compare the most recent day's trading volume to the average of the previous 7 days. If `latest_volume / avg_7d_volume > 3.0` (i.e., 200% increase), flag as **"异常放量"** (Abnormal Volume Spike).

#### 2.4 get_spot_order_book

Call `get_spot_order_book` with:
- `currency_pair`: `{COIN}_USDT`
- `limit`: 20

Key data to extract:
- Top bid and ask prices (spread)
- Total bid volume vs total ask volume
- Order book depth distribution

**Bid-Ask ratio analysis**: Calculate `total_bid_volume / total_ask_volume`. If this ratio < 0.7, flag as **"卖压较重"** (Heavy Selling Pressure).

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

**Funding rate analysis**: If the latest funding rate > 0.0005 (i.e., > 0.05%), flag as **"多头拥挤"** (Long Crowding). If the funding rate < -0.0005, note "空头拥挤" (Short Crowding) as well.

## Judgment Logic Summary

Apply these three checks and collect all triggered flags for the risk section:

| Condition | Flag | Meaning |
|-----------|------|---------|
| Latest funding rate > 0.05% (0.0005) | 多头拥挤 | Excessive long positioning, potential correction risk |
| Bid volume / Ask volume < 0.7 | 卖压较重 | Sell-side dominance, downward pressure |
| Latest 24h volume > 3x avg of previous 7 days | 异常放量 | Unusual volume spike, could signal major move |

## Report Template

Generate the report in the following structure. Use the actual data obtained from the API calls. All numerical values should be formatted appropriately (e.g., prices with proper decimals, volumes with units, percentages with % sign).

```
# {COIN} 深度分析报告

> 分析时间: {current_datetime}
> 交易对: {COIN}_USDT
> 数据来源: Gate.io

---

## 一、基本信息

- 币种名称: {name}
- 所属链: {chain}
- 充提状态: {deposit_status} / {withdraw_status}
- 交易状态: {trade_status}
- 价格精度: {price_precision} | 数量精度: {amount_precision}
- 最小下单量: {min_amount} | 最小下单额: {min_value} USDT

---

## 二、走势分析

### 当前价格
- 最新价: {latest_price} USDT
- 24h 涨跌幅: {change_24h}%

### K 线趋势 (近30日)
- 30日最高: {high_30d} USDT
- 30日最低: {low_30d} USDT
- 7日最高: {high_7d} USDT
- 7日最低: {low_7d} USDT
- 趋势判断: {trend_description}

### 关键价位
- 支撑位: {support_level} USDT
- 阻力位: {resistance_level} USDT

---

## 三、流动性分析

### 盘口深度
- 买一价: {best_bid} | 卖一价: {best_ask}
- 买卖价差: {spread} ({spread_pct}%)

### 买卖盘比
- 买盘总量: {total_bid_volume}
- 卖盘总量: {total_ask_volume}
- 买卖比: {bid_ask_ratio}
{if bid_ask_ratio < 0.7: "⚠️ 卖压较重：买盘力量不足，短期可能面临下行压力"}

### 近期成交
- 近期成交笔数: {trade_count}
- 大单占比: {large_trade_pct}%
- 主买/主卖比例: {buy_pct}% / {sell_pct}%

---

## 四、市场情绪

### 资金费率
{if futures available:}
- 最新资金费率: {latest_funding_rate}%
- 近期趋势: {funding_rate_trend}
{if funding_rate > 0.05%: "⚠️ 多头拥挤：资金费率偏高，多头持仓成本上升，需警惕回调风险"}
{if futures not available:}
- 该币种暂无永续合约，无法获取资金费率数据

### 成交量变化
- 最近24h成交量: {latest_volume}
- 前7日日均成交量: {avg_7d_volume}
- 量比: {volume_ratio}x
{if volume_ratio > 3.0: "⚠️ 异常放量：成交量较近期均值大幅增加，需关注是否有重大事件驱动"}

---

## 五、风险提示

{List all triggered flags here, with brief explanation for each}

{If no flags triggered: "当前未发现明显异常信号，市场状态相对平稳。"}

---

## 六、总结与建议

{Provide a brief overall assessment based on all the data above, including:}
- Overall trend outlook
- Key levels to watch
- Risk factors to be aware of
- A reminder that this is data-driven analysis, not investment advice
```

## Important Notes

- Always remind the user at the end: "以上分析基于链上和交易所公开数据，仅供参考，不构成投资建议。"
- If the coin symbol is not found or the trading pair does not exist, inform the user clearly and suggest checking the symbol.
- All flags (多头拥挤 / 卖压较重 / 异常放量) should be prominently displayed in the risk section with warning icons.
- Format large numbers with appropriate units (e.g., 1.2M, 350K) for readability.
- The report should be in Chinese as the primary audience is Chinese-speaking users.
