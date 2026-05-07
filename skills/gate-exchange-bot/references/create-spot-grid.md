# Gate Bot Spot Grid — `gate-cli cex bot spot-grid create`

Manual spot grid creation contract.

## Scope

Use this command only when the user clearly wants to create a **manual spot grid** and has either already provided or is ready to provide the required parameters.

This command is the final write step. It is not a recommendation flow and not a generic education flow.

## When To Use

- "Create a BTC spot grid from 60000 to 72000 with 50 grids, arithmetic mode, 1000 USDT"
- "Use these exact spot grid parameters and create it"

## When Not To Use

- The user is still asking what range or grid count to choose
- The user wants recommendation instead of manual setup
- The user actually wants margin grid, infinite grid, futures grid, or martingale
- The user has not confirmed yet

## Required Payload

Pass the final business payload through `body` as a JSON string:

```json
{
  "body": "{\"strategy_type\":\"spot_grid\",\"market\":\"BTC_USDT\",\"create_params\":{\"money\":\"1000\",\"low_price\":\"60000\",\"high_price\":\"72000\",\"grid_num\":50,\"price_type\":0,\"trigger_price\":\"61000\",\"stop_profit\":\"75000\",\"stop_loss\":\"55000\",\"is_use_base\":false}}"
}
```

### Required fields

- `strategy_type`: fixed to `spot_grid`
- `market`
- `create_params.money`
- `create_params.low_price`
- `create_params.high_price`
- `create_params.grid_num`
- `create_params.price_type`

### Optional fields

- `create_params.trigger_price`
- `create_params.stop_profit`
- `create_params.stop_loss`
- `create_params.profit_sharing_ratio`
- `create_params.is_use_base`

### `price_type`

- `0` = arithmetic
- `1` = geometric

### Ratio normalization

If `create_params.profit_sharing_ratio` is provided, it must be a decimal ratio string.

Examples:

- `10%` -> `"0.10"`
- `5%` -> `"0.05"`

If the exact normalized value is not confirmed, do not execute the write.

## Missing Parameter Handling

If required fields are missing, do not call the command. Ask only for the missing business inputs:

1. market
2. investment amount
3. lower price
4. upper price
5. grid count
6. arithmetic vs geometric mode

Do not guess the range, grid count, or mode for the user.

## Confirmation Gate

Before execution, present a draft that includes at least:

- market
- strategy type: spot grid
- investment amount
- lower and upper price
- grid count
- arithmetic or geometric mode
- optional trigger / TP / SL / profit sharing fields

If ratio fields are present, show both forms. Example:

- `Profit sharing ratio: 10% (command payload "0.10")`

Only execute after the user explicitly confirms.

## Workflow

1. Confirm that the request is for manual spot grid creation.
2. Collect the required fields and block on any missing business input.
3. Normalize ratio fields if present.
4. Present an Action Draft with final execution parameters.
5. Execute the create command only after explicit confirmation.

## Success and Failure

Treat the write as successful only when:

- HTTP status is `200`
- response body `code = 200`

Common failure categories:

- invalid request body
- missing required fields
- invalid `grid_num`
- invalid `price_type`
- unsupported pair
- insufficient balance
- KYC or regional restriction

When the backend returns a failure, use the backend `message` faithfully.

## Guardrails

- Do not convert recommendation chats into writes.
- Do not reuse fields from other bot types.
- Do not create before confirmation.
- Do not silently accept percentage text without decimal normalization.
- Do not treat consultation questions as write approval.

## Report Template

```markdown
## Spot Grid Action Draft
- Market: {market}
- Investment: {money}
- Range: {low_price} - {high_price}
- Grid Count: {grid_num}
- Mode: {price_type_label}
- Optional Fields: {optional_summary}
- Confirmation Required: yes
```
