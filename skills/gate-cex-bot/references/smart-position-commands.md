# Smart position

Before any creation or stop, apply the [Bot confirmation gate](bot-workflows.md#bot-confirmation-gate), even with complete parameters or an existing grant.

External type smart_position; internal type smart-position is not the CLI payload enum. Use `gate-cli cex bot smart-position create --json` with the [verified candidate](compatibility.md); check its actual leaf help before execution.

Creation business object uses strategy_type and create_params: begin_money_amount and begin_money_currency="USDT"; asset_info with 2–10 unique assets and rate strings totaling 1. Rates use two decimal places and minimum 0.01. Require exactly one of period (product interval) or threshold (positive ratio below 1, up to four decimals). Retain optional positive stop_profit/stop_loss, is_use_base and selected close_flag (0 return assets, 1 market-close). Show any documented effective default in the draft; do not infer an entire portfolio from a market. BTC recommendations must include the exact BTC asset, with other assets allowed; BTC3L is not BTC.

Stopping requires an explicit choice:

| stop_mode | Behavior |
|---|---|
| market | Existing controlled market-close retries; residual assets may be returned |
| limit | One selected price expression and positive expiration seconds, optional slip ratio; expiration cancels and returns assets, without switching to market |
| no_close | Return the current assets without closing |

Limit stop_options contain price (string), expiration (positive integer seconds) and optional slip (decimal string, 0.001–0.05, up to six decimals); 1% becomes "0.01", not a JSON number. No per-member prices or implicit stop choice. The backend atomically saves the accepted choice and stop signal, rejects a conflicting later choice and preserves an identical request's deadline/counters. Present [the complete stop draft](../../_shared/cex/templates.md) before confirmation. Historical details retain configuration; missing cash/asset quantities remain unknown or partial rather than zero.

Example creation business object (fill and confirm the user's complete draft before sending):

```json
{"strategy_type":"smart_position","create_params":{"begin_money_amount":"100","begin_money_currency":"USDT","asset_info":[{"asset":"BTC","rate":"0.50"},{"asset":"ETH","rate":"0.50"}],"period":"1h","close_flag":0}}
```

Use `gate-cli cex bot stop --strategy-id '<id>' --strategy-type smart_position --stop-mode <market|limit|no_close>`. For limit only, add `--stop-options '{"price":"100.000000000000000001","expiration":600}'`, optionally including the selected slip. The quoted price is an example, not a live quote or default. Show the selected mode and every option in the draft and verify authority for that exact choice; clarify missing or changed scope before execution. Market/no_close omit stop-options; do not send an empty object or substitute a different mode when validation refuses the request.

<a id="bot.smart-position.create"></a>
### `gate-cli cex bot smart-position create`

Operation ID: `bot.smart-position.create`. Effect: **write**.

Create smart_position: USDT amount, 2–10 asset/rate entries; exactly one period (1m–28d) or threshold; optional close_flag (0/1)

```text
gate-cli cex bot smart-position create [flags]
```

API: `POST /api/v4/bot/smart-position/create` (private).

Returns: [AiHubCreateSuccessResponse](models/spot-grid.md#model-aihubcreatesuccessresponse).

API request model: [SmartPositionCreateRequest](models/portfolios.md#model-smartpositioncreaterequest).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `--json` | `string` | Yes | Unset | Typed JSON request with strategy_type and create_params; amounts and rates are strings |
