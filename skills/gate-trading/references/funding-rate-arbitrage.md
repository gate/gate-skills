# Funding Rate Arbitrage Scanner

Scan all futures contracts for funding rate arbitrage opportunities by cross-referencing funding rates, spot/futures price spreads, trading volume, and order book depth. Produce a ranked list of actionable opportunities with estimated annualized returns and risk annotations.

## Workflow

When the user asks about arbitrage opportunities or abnormal funding rates, execute the following steps.

### Step 1: Get all futures tickers

Call `get_futures_tickers` with `settle: usdt` to retrieve all USDT-settled perpetual contract tickers.

Key data to extract:
- Contract name, last price, mark price
- 24h trading volume (in USDT)
- Funding rate (if included in ticker)

**Pre-filter**: Only keep contracts with 24h volume > $10,000,000 (10M USDT). Low-volume contracts are not suitable for arbitrage due to execution risk and slippage.

### Step 2: Get detailed funding rates for candidates

For each contract that passes the volume filter, call `get_futures_funding_rate` with:
- `contract`: the contract identifier
- `settle`: `usdt`
- `limit`: 10

Key data to extract:
- Latest funding rate
- Funding rate trend (increasing / decreasing / stable)
- Average funding rate over recent periods

**Funding rate filter**: Only keep contracts where `|latest_funding_rate| > 0.0005` (i.e., absolute value > 0.05%). This ensures the arbitrage spread is meaningful enough to cover transaction costs.

### Step 3: Get spot tickers for comparison

Call `get_spot_tickers` for each remaining candidate's spot pair (e.g., for `BTC_USDT` contract, get `BTC_USDT` spot ticker).

Key data to extract:
- Spot last price
- 24h spot volume
- Bid/ask prices

**Basis calculation**: Compute the spot-futures price spread:
- `basis = (futures_price - spot_price) / spot_price * 100%`
- If `|basis| > 0.2%`, this is an additional positive signal — the spread amplifies the arbitrage return.

### Step 4: Check order book depth

For each remaining candidate, call `get_spot_order_book` with:
- `currency_pair`: the spot pair (e.g., `BTC_USDT`)
- `limit`: 20

Key data to extract:
- Total bid depth (top 20 levels)
- Total ask depth (top 20 levels)
- Bid-ask spread percentage

**Depth filter**: Exclude coins where the top-20 order book depth (in USDT value) is too thin to execute the arbitrage at meaningful size. A reasonable threshold: if total depth on either side < $50,000 USDT equivalent, mark as "depth insufficient" and exclude or flag with warning.

## Judgment Logic Summary

| Step | Condition | Action |
|------|-----------|--------|
| Volume filter | 24h futures volume > $10M | Keep as candidate |
| Rate filter | \|funding rate\| > 0.05% | Keep as candidate |
| Basis bonus | \|spot-futures spread\| > 0.2% | Add bonus score, higher priority |
| Depth check | Order book depth < $50K per side | Exclude or flag "low liquidity warning" |

## Scoring and Ranking

For each qualified opportunity, compute a composite score:

1. **Estimated annualized return**:
   - Funding is typically settled every 8 hours (3x daily)
   - `annualized_return = |funding_rate| * 3 * 365 * 100%`
   - Adjust if the funding settlement interval differs (check contract info)

2. **Score factors** (for ranking):
   - Higher |funding rate| → higher score
   - Larger basis spread → higher score (bonus)
   - Higher volume → higher score (better execution)
   - Deeper order book → higher score (less slippage)

3. **Sort** all qualified opportunities by estimated annualized return (descending).

## Report Template

```
# Funding Rate Arbitrage Scan Report

> Scan time: {current_datetime}
> Settlement currency: USDT
> Scope: all USDT perpetual contracts
> Filtering conditions: 24h volume > $10M, |funding rate| > 0.05%

---

## Screening Overview

- Total contracts: {total_contracts}
- Passed volume filter: {volume_passed}
- Passed rate filter: {rate_passed}
- Final candidates: {final_candidates}

---

## Arbitrage Opportunity List

### 🥇 {rank}. {COIN}_USDT

| Metric | Value |
|------|------|
| Current funding rate | {funding_rate}% |
| Estimated annualized return | {annualized_return}% |
| Futures price | {futures_price} USDT |
| Spot price | {spot_price} USDT |
| spot-futures spread | {basis}% |
| 24h futures volume | ${futures_volume} |
| Order book depth | bid ${bid_depth} / ask ${ask_depth} |
| Arbitrage direction | {direction: forward (short futures + buy spot) / reverse (long futures + sell spot)} |

**Risk Flags**:
{risk_flags}

(Repeat for each candidate, ranked by annualized return)

---

## Risk Alerts

1. Funding rates are dynamic; actual returns may be lower than estimated annualized values.
2. Include open/close fees and slippage costs.
3. Extreme markets may trigger forced liquidation; manage position size and margin carefully.
4. Thin depth can create high slippage on large orders.
5. This analysis is based on real-time data, for reference only, and not investment advice.
```

## Direction Logic

- If funding rate > 0: Longs pay shorts → **forward arbitrage**: Short futures + Buy spot (collect funding)
- If funding rate < 0: Shorts pay longs → **reverse arbitrage**: Long futures + Sell/short spot (collect funding)

## Important Notes

- Process contracts in batches to avoid excessive API calls. If there are many candidates after the volume filter, prioritize by volume and process the top 50 first.
- Always display the arbitrage direction clearly — users need to know whether to go long or short on the futures side.
- Remind users that funding rates are dynamic and can reverse quickly.
- If no opportunities are found after filtering, clearly state that and suggest relaxing criteria or checking back later.
