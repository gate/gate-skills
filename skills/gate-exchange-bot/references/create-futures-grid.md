# Gate Bot Futures Grid — `gate-cli cex bot futures-grid create`

Manual futures grid creation contract.

## Scope

Use this command only when the user clearly wants a **manual futures grid** and is ready for final execution.

## Required Payload

```json
{
  "body": "{\"strategy_type\":\"futures_grid\",\"market\":\"BTC_USDT\",\"create_params\":{\"money\":\"1000\",\"low_price\":\"60000\",\"high_price\":\"72000\",\"grid_num\":50,\"price_type\":0,\"leverage\":\"5\",\"direction\":\"neutral\",\"trigger_price\":\"61000\",\"stop_profit\":\"75000\",\"stop_loss\":\"55000\",\"profit_sharing_ratio\":\"0.10\"}}"
}
```

### Required fields

- `market`
- `create_params.money`
- `create_params.low_price`
- `create_params.high_price`
- `create_params.grid_num`
- `create_params.price_type`
- `create_params.leverage`

### Optional fields

- `create_params.direction`
- `create_params.trigger_price`
- `create_params.stop_profit`
- `create_params.stop_loss`
- `create_params.profit_sharing_ratio`
- `create_params.is_use_base`

### Value rules

- `price_type`: `0` arithmetic, `1` geometric
- `direction`: `long`, `short`, or `neutral`
- If direction is omitted, the product defaults to neutral behavior

### Ratio normalization

`create_params.profit_sharing_ratio` must be a decimal ratio string.

Example:

- `10%` -> `"0.10"`

## Missing Parameter Handling

Ask only for missing fields:

1. market
2. investment amount
3. lower price
4. upper price
5. grid count
6. arithmetic vs geometric mode
7. leverage
8. direction if the user wants it explicit

Do not decide the range, leverage, or direction on the user's behalf.

## Confirmation Gate

Before execution, show:

- market
- strategy type: futures grid
- investment amount
- lower / upper price
- grid count
- arithmetic / geometric mode
- leverage
- direction: long / short / neutral
- optional trigger / TP / SL / profit sharing fields

If a ratio field is present, show both the user-facing percentage and the decimal command payload.

## Workflow

1. Confirm that the request is for manual futures grid creation.
2. Collect range, grid, leverage, and optional direction fields.
3. Normalize ratio fields.
4. Present an Action Draft.
5. Execute only after explicit confirmation.

## Success and Failure

Success requires response body `code = 200`.

Common failure categories:

- invalid request body
- invalid `grid_num`
- invalid `price_type`
- invalid `direction`
- invalid `leverage`
- unsupported pair
- insufficient balance
- leverage out of range
- KYC or regional restriction

## Guardrails

- Do not mix futures grid with spot, margin, or martingale payloads.
- Do not write `direction` as `buy` / `sell`; use `long` / `short` / `neutral`.
- Do not execute before explicit confirmation.
- Do not translate consultation about leverage or risk into write approval.

## Report Template

```markdown
## Futures Grid Action Draft
- Market: {market}
- Investment: {money}
- Range: {low_price} - {high_price}
- Grid Count: {grid_num}
- Mode: {price_type_label}
- Leverage: {leverage}
- Direction: {direction}
- Optional Fields: {optional_summary}
```
