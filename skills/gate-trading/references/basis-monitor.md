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

- **Positive basis (期货溢价/正基差)**: Futures price > Spot price → Contango, typical in bullish markets
- **Negative basis (期货折价/负基差)**: Futures price < Spot price → Backwardation, typical in bearish or uncertain markets

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
- If recent > long-term: Basis is **走阔** (widening)
- If recent < long-term: Basis is **收窄** (narrowing)
- If roughly equal (within 10%): Basis is **稳定** (stable)

**Signal generation**:

| Condition | Signal | Implication |
|-----------|--------|-------------|
| Basis rate > 0.3% and widening | 正基差走阔 | Bullish sentiment strengthening, potential short futures arbitrage |
| Basis rate < -0.1% and widening | 负基差走阔 | Bearish sentiment strengthening, potential long futures arbitrage |
| \|z_score\| > 2 and basis narrowing | 基差回归 | Basis reverting to mean, trend may be changing |
| \|z_score\| > 3 | 基差极端偏离 | Extreme deviation, high-probability reversion opportunity |
| Basis flipped sign recently | 基差翻转 | Sentiment shift signal |

## Report Template

### Single-Coin Report

```
# {COIN} 基差分析报告

> 分析时间: {current_datetime}
> 交易对: {COIN}_USDT
> 数据来源: Gate.io

---

## 当前基差状态

| 指标 | 数值 |
|------|------|
| 现货价格 | {spot_price} USDT |
| 合约价格 | {futures_price} USDT |
| 标记价格 | {mark_price} USDT |
| 基差 | {basis} USDT |
| 基差率 | {basis_rate}% |
| 基差方向 | {正基差(溢价) / 负基差(折价)} |

---

## 历史基差分析 (近7日)

| 指标 | 数值 |
|------|------|
| 7日平均基差率 | {avg_basis_rate}% |
| 基差标准差 | {std_basis}% |
| 当前偏离度 (Z-Score) | {z_score} |
| 7日最大基差 | {max_basis}% |
| 7日最小基差 | {min_basis}% |

### 基差趋势
- 近24h均值: {recent_avg}%
- 近7日均值: {weekly_avg}%
- 趋势判断: {走阔 / 收窄 / 稳定}

---

## 信号与解读

{Generated signals based on the analysis}

**当前状态解读**:
{Interpretation of what the current basis level and trend implies about market sentiment and potential opportunities}

---

## 套利参考

{If basis presents arbitrage opportunity:}
- 套利方向: {正向套利: 买现货+空合约 / 反向套利: 卖现货+多合约}
- 当前基差收益: {basis_rate}%
- 年化参考 (假设基差维持): {annualized}%
- 执行建议: {practical considerations}

---

## 风险提示

1. 基差会随市场情绪快速变化，历史数据不代表未来走势
2. 极端行情下基差可能大幅波动，套利策略存在风险
3. 需考虑交易手续费和资金费率对套利收益的影响
4. 以上分析基于市场公开数据，仅供参考，不构成投资建议
```

### Multi-Coin Scan Report

When scanning multiple coins, use a summary table format:

```
# 全市场基差扫描报告

> 扫描时间: {current_datetime}
> 扫描范围: 全部 USDT 永续合约
> 数据来源: Gate.io

---

## 基差排行

### 正基差 Top 10 (期货溢价)

| # | 币种 | 现货价 | 合约价 | 基差率 | 趋势 | 信号 |
|---|------|--------|--------|--------|------|------|
| 1 | {coin} | {spot} | {futures} | {rate}% | {trend} | {signal} |

### 负基差 Top 10 (期货折价)

| # | 币种 | 现货价 | 合约价 | 基差率 | 趋势 | 信号 |
|---|------|--------|--------|--------|------|------|
| 1 | {coin} | {spot} | {futures} | {rate}% | {trend} | {signal} |

---

## 市场总览

- 正基差合约数: {positive_count} ({positive_pct}%)
- 负基差合约数: {negative_count} ({negative_pct}%)
- 平均基差率: {avg_rate}%
- 基差极端偏离 (|Z| > 2) 数量: {extreme_count}

## 总结

{Overall market basis sentiment interpretation}
```

## Important Notes

- Basis analysis is most meaningful for coins with sufficient liquidity in both spot and futures markets. Flag low-liquidity coins.
- The premium index from `get_futures_premium_index` provides a clean, exchange-calculated measure. Prefer it over manual spot-futures calculation when available.
- For multi-coin scans, only fetch premium index history for the top anomalies (e.g., top 5 by |basis_rate|) to avoid excessive API calls.
- Always explain the meaning of positive vs negative basis to the user, as not all users are familiar with these concepts.
- Cross-reference with funding rate — a high positive basis with high funding rate strongly suggests bullish crowding.
