# Multi-Coin Screener

Screen and filter cryptocurrencies across the entire Gate.io market based on user-defined criteria. Supports dynamic filtering by volume, price change, funding rate, spread, and other metrics. Returns a ranked Top-N list with key data points.

## Workflow

When the user asks to find or filter coins (e.g., "help me find24hcoins with gain above 10%"), parse their criteria first, then execute the data collection and filtering pipeline.

### Step 1: Parse user criteria

Extract filtering and sorting conditions from the user's request. Common criteria include:

| Criteria Type | Examples | Data Source |
|---------------|----------|-------------|
| Price change | gain > 10%, drop > 5% | spot tickers |
| Volume | volume > $1M, turnover rank | spot tickers |
| Funding rate | rate > 0.1%, negative rate | futures funding rate |
| Price range | price < $1, price > $100 | spot tickers |
| Spread | bid-ask spread < 0.1% | spot tickers |
| Volume change | volume expansion > 200% | spot tickers (compare) |

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
- **Rate direction**: Positive (longs pay) vs negative (shorts pay)

### Step 5: Sort and select Top N

Sort the filtered results by the user's preferred sort field. If no sort preference is given, default to 24h quote volume descending.

Select the top N results (default 20, or as specified by the user).

## Dynamic Filter Examples

Here are common user queries and how to translate them into filters:

| User Query | Filters Applied |
|------------|----------------|
| "coins with gain above 10%" | change_pct > 10%, sort by change_pct desc |
| "top 20 coins by volume" | top 20 by quote_volume desc |
| "coins with funding rate above 0.1%" | \|funding_rate\| > 0.1%, sort by rate desc |
| "coins down a lot but with huge volume" | change_pct < -5%, quote_volume > $5M, sort by change_pct asc |
| "coins under $1 with strong gains" | last < 1, change_pct > 5%, sort by change_pct desc |
| "find coins rising with volume expansion" | change_pct > 0, volume_ratio > 2x, sort by volume_ratio desc |

When the user's criteria are vague (e.g., "strong gainers"), use reasonable defaults and explain the thresholds chosen.

## Report Template

```
# Multi-Coin Screening Results

> Screening time: {current_datetime}
> Data source: Gate.io
> Screening conditions: {conditions_summary}
> Sorting method: {sort_description}
> Result count: {result_count} / {total_scanned}

---

## Screening Results

| # | Coin | Price (USDT) | 24h Change | 24h Turnover | {extra_columns} |
|---|------|-------------|-----------|-----------|-----------------|
| 1 | {coin} | {price} | {change}% | ${volume} | {extra_data} |
| 2 | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... |

---

## Data Highlights

{Highlight notable patterns in the filtered results:}
- Sector concentration (are the results concentrated in a sector?)
- Common traits (common traits among the results)
- Outliers (outliers worth noting)

---

## Notes

- Data is a real-time snapshot; markets can change quickly.
- Screening results are based on quantitative indicators only and are not investment advice.
- For deeper single-coin analysis, say "analyze XXX in detail".
```

## Important Notes

- The table columns should adapt to the user's query. If they ask about funding rates, include a funding rate column. If they ask about volume, prominently show volume data.
- For very broad queries that return too many results (e.g., "all rising coins"), cap at a reasonable number (50) and inform the user.
- If the user's criteria are too strict and return zero results, suggest relaxing the thresholds and show the closest matches.
- Always show the filtering criteria used so the user can refine their query.
- When comparing to averages or historical values, clearly state the comparison baseline.
- Cross-reference the results with the coin deep analysis module — suggest the user can dive deeper into any specific coin from the list.
