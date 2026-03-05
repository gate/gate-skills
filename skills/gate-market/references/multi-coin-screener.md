# Multi-Coin Screener

Screen and filter cryptocurrencies across the entire Gate.io market based on user-defined criteria. Supports dynamic filtering by volume, price change, funding rate, spread, and other metrics. Returns a ranked Top-N list with key data points.

## Workflow

When the user asks to find or filter coins (e.g., "帮我找出24h涨幅超过10%的币"), parse their criteria first, then execute the data collection and filtering pipeline.

### Step 1: Parse user criteria

Extract filtering and sorting conditions from the user's request. Common criteria include:

| Criteria Type | Examples | Data Source |
|---------------|----------|-------------|
| Price change | 涨幅 > 10%, 跌幅 > 5% | spot tickers |
| Volume | 成交量 > $1M, 成交额排名 | spot tickers |
| Funding rate | 费率 > 0.1%, 负费率 | futures funding rate |
| Price range | 价格 < $1, 价格 > $100 | spot tickers |
| Spread | 买卖价差 < 0.1% | spot tickers |
| Volume change | 放量 > 200% | spot tickers (compare) |

Determine:
- **Filter conditions**: What thresholds to apply
- **Sort field**: What to rank by (default: 24h volume descending)
- **Top N**: How many results to show (default: 20)
- **Market scope**: Spot only, futures only, or both

### Step 2: Get spot market data

Call `get_spot_tickers` without specifying a currency pair to retrieve all spot trading pairs.

Key data to extract per pair:
- Currency pair name
- Last price, highest/lowest 24h price
- 24h price change percentage
- 24h base volume, 24h quote volume (USDT)
- Highest bid, lowest ask

**Pre-filter**: Only consider `_USDT` pairs to keep results consistent and comparable. Exclude stablecoin pairs (e.g., `USDC_USDT`, `USDT_USD`).

### Step 3: Apply spot-based filters

Apply the user's criteria to filter the spot ticker data:

- **Price change filter**: Compare `change_percentage` against user threshold
- **Volume filter**: Compare `quote_volume` (USDT volume) against user threshold
- **Price filter**: Compare `last` price against user threshold
- **Spread filter**: Calculate `(lowest_ask - highest_bid) / last * 100%`

### Step 4: Enrich with futures data (if needed)

If the user's criteria involve funding rate or futures-specific metrics:

Call `get_futures_tickers` with `settle: usdt` to get all futures tickers.

Then for candidates requiring funding rate data, call `get_futures_funding_rate` with:
- `contract`: the contract identifier
- `settle`: `usdt`
- `limit`: 3 (recent rates)

Apply funding rate filters:
- **Rate filter**: Compare `|funding_rate|` against user threshold
- **Rate direction**: Positive (多头付费) vs negative (空头付费)

### Step 5: Sort and select Top N

Sort the filtered results by the user's preferred sort field. If no sort preference is given, default to 24h quote volume descending.

Select the top N results (default 20, or as specified by the user).

## Dynamic Filter Examples

Here are common user queries and how to translate them into filters:

| User Query | Filters Applied |
|------------|----------------|
| "涨幅超过10%的币" | change_pct > 10%, sort by change_pct desc |
| "成交量最大的20个币" | top 20 by quote_volume desc |
| "费率超过0.1%的币" | \|funding_rate\| > 0.1%, sort by rate desc |
| "跌了很多但量很大的币" | change_pct < -5%, quote_volume > $5M, sort by change_pct asc |
| "价格低于1美元且涨幅大的" | last < 1, change_pct > 5%, sort by change_pct desc |
| "找出放量上涨的币" | change_pct > 0, volume_ratio > 2x, sort by volume_ratio desc |

When the user's criteria are vague (e.g., "涨得多"), use reasonable defaults and explain the thresholds chosen.

## Report Template

```
# 多币种筛选结果

> 筛选时间: {current_datetime}
> 数据来源: Gate.io
> 筛选条件: {conditions_summary}
> 排序方式: {sort_description}
> 结果数量: {result_count} / {total_scanned}

---

## 筛选结果

| # | 币种 | 价格 (USDT) | 24h涨跌幅 | 24h成交额 | {extra_columns} |
|---|------|-------------|-----------|-----------|-----------------|
| 1 | {coin} | {price} | {change}% | ${volume} | {extra_data} |
| 2 | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... |

---

## 数据亮点

{Highlight notable patterns in the filtered results:}
- 板块集中度 (are the results concentrated in a sector?)
- 共性特征 (common traits among the results)
- 异常值 (outliers worth noting)

---

## 备注

- 数据为实时快照，市场变化迅速
- 筛选结果仅基于量化指标，不代表投资建议
- 如需更详细的单币分析，可以说"帮我分析一下 XXX"
```

## Important Notes

- The table columns should adapt to the user's query. If they ask about funding rates, include a funding rate column. If they ask about volume, prominently show volume data.
- For very broad queries that return too many results (e.g., "所有涨的币"), cap at a reasonable number (50) and inform the user.
- If the user's criteria are too strict and return zero results, suggest relaxing the thresholds and show the closest matches.
- Always show the filtering criteria used so the user can refine their query.
- When comparing to averages or historical values, clearly state the comparison baseline.
- Cross-reference the results with the coin deep analysis module — suggest the user can dive deeper into any specific coin from the list.
