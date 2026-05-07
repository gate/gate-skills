# Gate Bot Spot Martingale — `gate-cli cex bot spot-martingale create`

Manual spot martingale creation contract.

## Scope

Use this command only when the user clearly wants a **manual spot martingale** and the conversation has reached the final create step.

## Stop-Loss Rule

Spot martingale uses **`create_params.stop_loss_per_cycle`** for stop-loss behavior. Do **not** treat `stop_loss_price` as the create-time stop-loss field.

If the user only provides a stop-loss price:

1. Explain that creation requires `stop_loss_per_cycle` rather than a single fixed stop-loss price.
2. Ask the user to provide the stop-loss percentage explicitly.
3. Do **not** derive that percentage from market price, target price, or any formula.
4. If the user expressed stop-loss intent, do not enter final confirmation until `stop_loss_per_cycle` is explicitly provided.

## Required Payload

```json
{
  "body": "{\"strategy_type\":\"spot_martingale\",\"market\":\"BTC_USDT\",\"create_params\":{\"invest_amount\":\"1000\",\"price_deviation\":\"0.02\",\"max_orders\":5,\"take_profit_ratio\":\"0.015\",\"stop_loss_per_cycle\":\"0.05\",\"trigger_price\":\"90000\",\"profit_sharing_ratio\":\"0.10\"}}"
}
```

### Required fields

- `market`
- `create_params.invest_amount`
- `create_params.price_deviation`
- `create_params.max_orders`
- `create_params.take_profit_ratio`

### Conditionally required field

- `create_params.stop_loss_per_cycle` becomes mandatory if the user has expressed any stop-loss intent

### Optional fields

- `create_params.trigger_price`
- `create_params.profit_sharing_ratio`

### Ratio normalization

These must be decimal ratio strings:

- `price_deviation`
- `take_profit_ratio`
- `stop_loss_per_cycle`
- `profit_sharing_ratio`

Examples:

- `2%` -> `"0.02"`
- `1.5%` -> `"0.015"`
- `5%` -> `"0.05"`

## Missing Parameter Handling

Ask only for missing fields:

1. market
2. investment amount
3. price deviation
4. max orders
5. take-profit ratio
6. stop-loss-per-cycle if stop-loss intent exists
7. trigger price if requested

Do not choose deviation, take-profit ratio, stop-loss ratio, or max orders for the user.

## Confirmation Gate

Show a summary containing:

- market
- strategy type: spot martingale
- investment amount
- deviation ratio
- max orders
- take-profit ratio
- stop-loss-per-cycle if applicable
- trigger price / profit sharing if present

Show both user-facing percentages and normalized command payload decimals.

## Workflow

1. Confirm that the request is for manual spot martingale creation.
2. Collect required ratios and order-count fields.
3. If the user expressed stop-loss intent, require `stop_loss_per_cycle`.
4. Present an Action Draft with normalized ratio values.
5. Execute only after explicit confirmation.

## Success and Failure

Success requires body `code = 200`.

Common failure categories:

- invalid request body
- invalid ratio fields
- invalid `max_orders`
- unsupported pair
- insufficient balance
- KYC or regional restriction

## Guardrails

- Do not add `direction` or `leverage` to spot martingale create payloads.
- Do not replace `stop_loss_per_cycle` with `stop_loss_price`.
- Do not create before the user explicitly confirms.

## Report Template

```markdown
## Spot Martingale Action Draft
- Market: {market}
- Investment: {invest_amount}
- Price Deviation: {price_deviation_display}
- Max Orders: {max_orders}
- Take Profit: {take_profit_display}
- Stop Loss Per Cycle: {stop_loss_display}
- Optional Fields: {optional_summary}
```
