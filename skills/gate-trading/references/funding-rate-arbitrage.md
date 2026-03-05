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
# 资金费率套利扫描报告

> 扫描时间: {current_datetime}
> 结算币种: USDT
> 扫描范围: 全部 USDT 永续合约
> 筛选条件: 24h成交量 > $10M, |资金费率| > 0.05%

---

## 筛选概览

- 合约总数: {total_contracts}
- 通过成交量筛选: {volume_passed}
- 通过费率筛选: {rate_passed}
- 最终候选: {final_candidates}

---

## 套利机会列表

### 🥇 {rank}. {COIN}_USDT

| 指标 | 数值 |
|------|------|
| 当前资金费率 | {funding_rate}% |
| 预估年化收益 | {annualized_return}% |
| 合约价格 | {futures_price} USDT |
| 现货价格 | {spot_price} USDT |
| 期现价差 | {basis}% |
| 24h合约成交量 | ${futures_volume} |
| 盘口深度 | 买盘 ${bid_depth} / 卖盘 ${ask_depth} |
| 套利方向 | {direction: 正向套利(做空合约+买入现货) / 反向套利(做多合约+卖出现货)} |

**风险标注**:
{risk_flags}

(Repeat for each candidate, ranked by annualized return)

---

## 风险提示

1. 资金费率会动态变化，实际收益可能低于预估年化
2. 需考虑开仓/平仓手续费、滑点成本
3. 极端行情下可能触发强平，需合理控制仓位和保证金
4. 盘口深度不足的币种，大额操作可能产生较大滑点
5. 以上分析基于实时数据，仅供参考，不构成投资建议
```

## Direction Logic

- If funding rate > 0: Longs pay shorts → **正向套利**: Short futures + Buy spot (collect funding)
- If funding rate < 0: Shorts pay longs → **反向套利**: Long futures + Sell/short spot (collect funding)

## Important Notes

- Process contracts in batches to avoid excessive API calls. If there are many candidates after the volume filter, prioritize by volume and process the top 50 first.
- Always display the arbitrage direction clearly — users need to know whether to go long or short on the futures side.
- Remind users that funding rates are dynamic and can reverse quickly.
- If no opportunities are found after filtering, clearly state that and suggest relaxing criteria or checking back later.
