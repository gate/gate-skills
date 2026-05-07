# Gate Bot Margin Grid — `gate-cli cex bot margin-grid create`

Manual margin grid creation contract.

## Scope

Use this command only when the user clearly wants a **manual margin grid** and the conversation has already reached the final execution step.

## Required Payload

```json
{
  "body": "{\"strategy_type\":\"margin_grid\",\"market\":\"BTC_USDT\",\"create_params\":{\"money\":\"1000\",\"low_price\":\"60000\",\"high_price\":\"72000\",\"grid_num\":50,\"price_type\":0,\"leverage\":\"3\",\"trigger_price\":\"61000\",\"stop_profit\":\"75000\",\"stop_loss\":\"55000\",\"profit_sharing_ratio\":\"0.10\"}}"
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
- `leverage` is required
- `direction` is not a mandatory prerequisite and must not be treated as the field that decides actual product direction

### Ratio normalization

`create_params.profit_sharing_ratio` must be passed as a decimal ratio string.

Example:

- `10%` -> `"0.10"`

If the normalized decimal is not confirmed, do not execute the write.

## Missing Parameter Handling

If required parameters are missing, ask only for the missing fields:

1. market
2. investment amount
3. lower price
4. upper price
5. grid count
6. arithmetic vs geometric mode
7. leverage

Do not auto-complete the trading range, grid count, leverage, or direction for the user.

## Confirmation Gate

Before execution, show a summary containing:

- market
- strategy type: margin grid
- investment amount
- lower / upper price
- grid count
- arithmetic / geometric mode
- leverage
- optional trigger / TP / SL / profit sharing fields

If the user provided percentages, keep the readable percentage and also show the normalized command payload form.

## Workflow

1. Confirm that the request is for manual margin grid creation.
2. Collect the required market, range, grid, and leverage fields.
3. Normalize any ratio fields.
4. Present an Action Draft.
5. Execute the create command only after explicit confirmation.

## Success and Failure

Success requires:

- HTTP `200`
- body `code = 200`

Failure examples:

- invalid request body
- missing required fields
- invalid `grid_num`
- invalid `price_type`
- invalid `leverage`
- unsupported pair
- insufficient balance
- minimum investment not met
- KYC or regional restriction

Use the backend `message` directly when possible.

## Guardrails

- Do not mix recommendation and create in one write step.
- Do not create before explicit confirmation.
- Do not pass percentage text directly as an integer or percent string.
- Do not route running-strategy management here.

## Report Template

```markdown
## Margin Grid Action Draft
- Market: {market}
- Investment: {money}
- Range: {low_price} - {high_price}
- Grid Count: {grid_num}
- Mode: {price_type_label}
- Leverage: {leverage}
- Optional Fields: {optional_summary}
```
