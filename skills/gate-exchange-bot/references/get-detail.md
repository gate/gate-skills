# Gate Bot Portfolio Detail — `gate-cli cex bot portfolio detail`

Single-strategy detail query contract.

## Scope

Use this command to inspect one exact running strategy.

## Required Query Parameters

- `strategy_id`
- `strategy_type`

Both are required. `strategy_type` must not be omitted because it is used by the backend to route the detail request correctly.

## When To Use

- "Show detail for strategy 123456"
- "How is my ETH martingale performing?"
- "Show detailed P&L for that bot"

## When Not To Use

- The user only wants a running list
- The user wants to stop a strategy
- The target strategy is still ambiguous

## Success and Failure

Success requires body `code = 200`.

Key fields:

- `data.strategy_id`
- `data.strategy_type`
- `data.market`
- `data.status`
- `data.base_info`
- `data.metrics`
- `data.position`
- `data.stop_supported`

Common failures:

- invalid `strategy_id`
- invalid `strategy_type`
- strategy detail not found

## Guardrails

- Do not omit `strategy_type`.
- Do not guess the target from a list unless the user has already confirmed a unique strategy.

## Workflow

1. Confirm that both `strategy_id` and `strategy_type` are known.
2. Execute the detail query.
3. Return base info, metrics, and position context from the backend response.
4. If the user wants to stop the strategy next, switch into the stop workflow instead of doing it implicitly.

## Report Template

```markdown
## Strategy Detail
- Strategy ID: {strategy_id}
- Strategy Type: {strategy_type}
- Market: {market}
- Status: {status}
- Metrics: {metrics_summary}
- Position: {position_summary}
```
