# Gate Bot Discover — `gate-cli cex bot strategy recommend`

Recommendation contract for AIHub strategy discovery. This command is read-only and never performs bot creation by itself.

## Scope

Use this command when the user wants strategy recommendations without already supplying all core execution parameters required for a create flow.

Supported scenes:

- `top1`
- `bundle`
- `filter`
- `refresh`

## When To Use

- "Recommend a BTC spot grid"
- "What bot strategy should I use for BTC?"
- "Filter BTC strategies with max drawdown below 10%"
- "Refresh that recommendation"

## When Not To Use

- The user already provided a full grid or martingale configuration and wants to create it now
- The user wants running-strategy list, detail, or stop
- The user asks for a non-bot product such as savings, recurring buy, or manual spot/futures trading

## Query Parameters

| Parameter | Required | Notes |
|---|---|---|
| `market` | No | Trading pair such as `BTC_USDT` |
| `strategy_type` | No | Target recommendation type; `contract_martingale` is not supported as a discover target |
| `direction` | No | `buy`, `sell`, or `neutral` |
| `invest_amount` | No | Budget amount, pass through as string |
| `scene` | No | `top1`, `bundle`, `filter`, or `refresh` |
| `refresh_recommendation_id` | No | Refresh context, minimum format `strategy_type|market` |
| `limit` | No | Maximum rows for filter scene; cap at 10 |
| `max_drawdown_lte` | No | Maximum drawdown upper bound |
| `backtest_apr_gte` | No | Minimum backtest APR |

## Scene Mapping

### `top1`

Use when the user clearly specifies `strategy_type` and wants the best single recommendation.

Example:

```json
{
  "strategy_type": "spot_grid",
  "market": "BTC_USDT",
  "scene": "top1"
}
```

### `bundle`

Use when the user specifies a market but not an exact strategy type.

If the user asks for "a strategy" without a coin or pair, ask for the coin first. Recommended clarification:

`Which coin are you focused on? Popular examples are BTC or ETH.`

After the user answers, normalize the market to `{COIN}_USDT` and call `scene=bundle`.

Example:

```json
{
  "market": "BTC_USDT",
  "scene": "bundle"
}
```

### `filter`

Use when the user explicitly wants screening conditions.

Allowed screening inputs:

- `market`
- `backtest_apr_gte`
- `max_drawdown_lte`
- `limit`

Example:

```json
{
  "scene": "filter",
  "market": "BTC_USDT",
  "backtest_apr_gte": "20",
  "max_drawdown_lte": "10",
  "limit": 10
}
```

### `refresh`

Use when the user wants to refresh the previous recommendation.

Example:

```json
{
  "scene": "refresh",
  "refresh_recommendation_id": "spot_grid|BTC_USDT"
}
```

## Strategy Boundaries

Do not present these as formal discover targets:

- `contract_martingale`
- `smart-position`
- `spot-future-arbitrage`

These may be supported by product APIs but should not be represented as the standard proactive recommendation set.

The default proactive pool is:

- `spot_grid`
- `futures_grid`
- `spot_martingale`

## Workflow

1. Decide whether the request belongs to `top1`, `bundle`, `filter`, or `refresh`.
2. Ask for the target market only if it is required and still missing.
3. Execute the recommendation command with query-style parameters only.
4. Return recommendation results without performing any create action.
5. If the user chooses a recommended strategy and wants execution, switch to the correct create reference file.

`margin_grid` and `infinite_grid` are supported products but should not be treated as the default recommendation pool unless the user explicitly asks for them.

## Result Handling

- Judge success by response body `code`.
- On success, read `data.recommendations` and render the backend output faithfully.
- If the user wants to create one of the recommended strategies, switch into the corresponding create reference file.
- If the current runtime truly lacks write capability, say that the environment is missing create capability; do not misstate that recommendation flows can never continue into creation.

## Guardrails

- Do not invent unsupported filters.
- Do not pretend a create flow is part of the recommendation command.
- Do not block the natural path from recommend → confirm → create once the user chooses a strategy and provides required inputs.

## Report Template

```markdown
## Recommendation Result
- Scene: {scene}
- Market: {market}
- Strategy Scope: {strategy_scope}
- Returned Recommendations: {summary}
- Next Step: {follow_up_hint}
```
