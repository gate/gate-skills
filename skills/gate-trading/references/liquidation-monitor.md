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
| 1h liquidation volume > 3x daily average hourly volume | 爆仓异常 | Liquidation spike significantly above normal levels |
| Long (or short) liquidations > 80% of total | 多头清洗 / 空头清洗 | Directional squeeze — one side being wiped out |
| Price has recovered > 50% of the drop/spike that caused liquidations | 插针行情 | Pin-bar / wick event — price spiked to liquidate and reversed |

### Detailed judgment:

**爆仓异常 (Abnormal Liquidation)**:
- Calculate: `hourly_liq_volume` for the most recent hour
- Calculate: `avg_hourly_liq_volume` = total liquidation volume in available data / number of hours
- If `hourly_liq_volume > 3 * avg_hourly_liq_volume` → flag

**多头清洗 / 空头清洗 (Long/Short Squeeze)**:
- Calculate: `long_liq_pct` = long liquidation volume / total liquidation volume
- If `long_liq_pct > 80%` → flag "多头清洗" (Long Squeeze)
- If `short_liq_pct > 80%` (i.e., `long_liq_pct < 20%`) → flag "空头清洗" (Short Squeeze)

**插针行情 (Pin-bar / Wick Event)**:
- Identify the candle with the largest liquidation activity
- Check if the candle has a long wick: `wick_ratio = |high - low| / |open - close|`
- Check if current price has recovered: compare current price to the extreme price of that candle
- If current price recovered > 50% of the move → flag "插针行情"

## Report Template

```
# 爆仓异常监控报告

> 监控时间: {current_datetime}
> 数据范围: 近 24 小时
> 结算币种: USDT

---

## 全局概览

- 监控合约数: {total_contracts}
- 总爆仓金额: ${total_liq_value}
- 多头爆仓占比: {long_liq_pct}%
- 空头爆仓占比: {short_liq_pct}%
- 异常合约数: {anomaly_count}

---

## 异常合约详情

### ⚠️ {rank}. {COIN}_USDT

| 指标 | 数值 |
|------|------|
| 近1h爆仓量 | ${hourly_liq_volume} |
| 日均小时爆仓量 | ${avg_hourly_liq_volume} |
| 爆仓倍数 | {liq_ratio}x (日均) |
| 多头爆仓占比 | {long_pct}% |
| 空头爆仓占比 | {short_pct}% |
| 当前价格 | {current_price} USDT |
| 爆仓时价格 | {liq_price} USDT |
| 价格恢复情况 | {recovery_description} |

**异常标记**:
{flags with explanations}

**行情背景**:
{brief price context from candlestick data}

(Repeat for each anomalous contract, sorted by liquidation volume)

---

## 市场解读

{Overall market liquidation analysis:}
- Which side (long/short) is getting hurt more across the market
- Whether liquidations are concentrated in specific coins or widespread
- Correlation with price movements

---

## 风险提示

1. 大规模爆仓后市场波动可能加剧，需谨慎操作
2. 插针行情表明市场存在流动性缺口，需注意止损设置
3. 多头/空头集中清洗后，可能出现趋势反转
4. 以上分析基于链上清算数据，仅供参考，不构成投资建议
```

## Important Notes

- If no anomalous liquidation events are found, inform the user that the market liquidation activity is within normal range and provide a brief summary of overall liquidation levels.
- When the user asks about a specific coin, focus the analysis on that coin but also mention if there are broader market liquidation trends.
- Large liquidation events often cluster together — present them chronologically when relevant to show the cascade effect.
- Always provide price context — raw liquidation numbers without price reference are hard to interpret.
