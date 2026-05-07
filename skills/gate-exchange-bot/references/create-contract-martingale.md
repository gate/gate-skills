# Gate Bot Contract Martingale — `gate-cli cex bot contract-martingale create`

Manual contract martingale creation contract.

## Scope

Use this command only when the user clearly wants a **manual contract martingale** and the conversation is ready for the final create call.

## Required Payload

```json
{
  "body": "{\"strategy_type\":\"contract_martingale\",\"market\":\"BTC_USDT\",\"create_params\":{\"invest_amount\":\"1000\",\"price_deviation\":\"0.02\",\"max_orders\":5,\"take_profit_ratio\":\"0.015\",\"direction\":\"sell\",\"leverage\":\"5\",\"stop_loss_price\":\"75000\",\"profit_sharing_ratio\":\"0.10\"}}"
}
```

### Required fields

- `market`
- `create_params.invest_amount`
- `create_params.price_deviation`
- `create_params.max_orders`
- `create_params.take_profit_ratio`
- `create_params.direction`
- `create_params.leverage`

### Optional fields

- `create_params.stop_loss_price`
- `create_params.profit_sharing_ratio`

### Direction rule

Allowed values:

- `buy`
- `sell`

Do not use:

- `long`
- `short`
- `neutral`

### Ratio normalization

These fields must be decimal ratio strings:

- `price_deviation`
- `take_profit_ratio`
- `profit_sharing_ratio`

Examples:

- `2%` -> `"0.02"`
- `1.5%` -> `"0.015"`
- `10%` -> `"0.10"`

## Missing Parameter Handling

Ask only for missing fields:

1. market
2. investment amount
3. price deviation
4. max orders
5. take-profit ratio
6. direction
7. leverage

Do not choose direction, leverage, or risk parameters for the user.

## Confirmation Gate

Before execution, show:

- market
- strategy type: contract martingale
- investment amount
- direction
- leverage
- deviation ratio
- max orders
- take-profit ratio
- optional stop-loss price / profit sharing

If ratios are present, show both the readable percentage and the normalized decimal payload.

## Workflow

1. Confirm that the request is for manual contract martingale creation.
2. Collect market, direction, leverage, and ratio fields.
3. Normalize ratio values.
4. Present an Action Draft.
5. Execute only after explicit confirmation.

## Success and Failure

Success requires body `code = 200`.

Common failure categories:

- invalid request body
- invalid ratio fields
- invalid `max_orders`
- invalid `direction`
- invalid `leverage`
- unsupported pair
- insufficient balance
- KYC or regional restriction

## Guardrails

- Do not write `direction` as `long`, `short`, or `neutral`.
- Do not mix grid fields into contract martingale payloads.
- Do not create before explicit confirmation.

## Report Template

```markdown
## Contract Martingale Action Draft
- Market: {market}
- Investment: {invest_amount}
- Direction: {direction}
- Leverage: {leverage}
- Price Deviation: {price_deviation_display}
- Max Orders: {max_orders}
- Take Profit: {take_profit_display}
- Optional Fields: {optional_summary}
```
