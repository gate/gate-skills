# Gate Bot Infinite Grid — `gate-cli cex bot infinite-grid create`

Manual infinite grid creation contract.

## Scope

Use this command only when the user explicitly wants a **manual infinite grid** and the conversation is already at the final create step.

## Required Payload

```json
{
  "body": "{\"strategy_type\":\"infinite_grid\",\"market\":\"BTC_USDT\",\"create_params\":{\"money\":\"1000\",\"price_floor\":\"60000\",\"profit_per_grid\":\"0.015\",\"trigger_price\":\"61000\",\"stop_profit\":\"75000\",\"stop_loss\":\"55000\",\"profit_sharing_ratio\":\"0.10\"}}"
}
```

### Required fields

- `market`
- `create_params.money`
- `create_params.price_floor`
- `create_params.profit_per_grid`

### Optional fields

- `create_params.trigger_price`
- `create_params.stop_profit`
- `create_params.stop_loss`
- `create_params.profit_sharing_ratio`
- `create_params.is_use_base`

### Ratio normalization

These fields must be decimal ratio strings:

- `create_params.profit_per_grid`
- `create_params.profit_sharing_ratio`

Examples:

- `1.5%` -> `"0.015"`
- `10%` -> `"0.10"`

If the decimal form is not confirmed, do not execute the write.

### Product rule

For this skill, infinite grid does **not** require `grid_num` or `price_type`.

## Missing Parameter Handling

Ask only for missing fields:

1. market
2. investment amount
3. floor price
4. profit per grid

Do not choose the floor or target profit rate for the user.

## Confirmation Gate

Show a summary containing:

- market
- strategy type: infinite grid
- investment amount
- floor price
- profit per grid
- optional trigger / TP / SL / profit sharing fields

If percentages are present, show both forms. Example:

- `Profit per grid: 1.5% (command payload "0.015")`

## Workflow

1. Confirm that the request is for manual infinite grid creation.
2. Collect market, investment amount, floor price, and profit-per-grid.
3. Normalize ratio fields.
4. Present an Action Draft.
5. Execute only after explicit confirmation.

## Success and Failure

Success requires body `code = 200`.

Common failures:

- invalid request body
- missing required fields
- invalid profit ratio field
- unsupported pair
- insufficient balance
- KYC or regional restriction

## Guardrails

- Do not convert educational discussions into writes.
- Do not inject spot-grid or futures-grid fields into infinite grid payloads.
- Do not execute before explicit confirmation.

## Report Template

```markdown
## Infinite Grid Action Draft
- Market: {market}
- Investment: {money}
- Floor Price: {price_floor}
- Profit per Grid: {profit_per_grid_display}
- Optional Fields: {optional_summary}
```
