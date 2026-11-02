# Futures combo

Before any creation or stop, apply the [Bot confirmation gate](bot-workflows.md#bot-confirmation-gate), even with complete parameters or an existing grant.

External type futures_combo; internal futures-combo remains server owned. No official recommendation exists. Use `gate-cli cex bot futures-combo create --json` with the [verified candidate](compatibility.md), after checking actual leaf help.

Creation business object uses strategy_type and create_params. Supply 2–10 unique asset_info entries with market, side buy/sell and rate strings totaling 1; each rate is 0.01–1 in steps of 0.01. Use explicit integer leverage 1–100, additionally constrained by each live market; begin_money_currency="USDT" and positive begin_money_amount; exactly one of period or threshold. Supported periods are 30m, 1h, 4h, 8h, 12h, 1d, 3d, 7d, 14d and 28d. threshold is a ratio from 0.01 to 0.50. Optional stop_profit is a ratio from 0.01 to 100 (1%–10000%); stop_loss is 0.01–0.99 (1%–99%). Explicit null disables these optional stop conditions in this product. Collect selected stop_profit/stop_loss ratios if wanted. Preserve every contract, direction and weight. Product validation owns market eligibility, supported weight precision, leverage constraints, fee/funding requirements and minimum investment; surface its refusals rather than inventing limits.

The dedicated lifecycle owns account allocation, deposits, task dispatch, recovery and settlement. A failure after allocation retains the original ID. Query that instance and its existing financial facts; do not create again or replay a transfer. Per-leg details carry amount/value units, side and target weight. Ended instances retain the saved composition without reading a released subaccount.

Stop uses the existing whole-portfolio close and settlement workflow; custom rebalance exit modes do not apply. Draft the full close, cancellation, residual exposure and settlement implications, then confirm once. Stop acceptance, trading completion, final-refund fact, settlement, empty account and account release are separate facts. Report only observed phases; a stopped status alone is not funds-arrived evidence.

Example creation business object (confirm the user's complete draft before sending):

```json
{"strategy_type":"futures_combo","create_params":{"begin_money_amount":"100","begin_money_currency":"USDT","asset_info":[{"market":"BTC_USDT","side":"buy","rate":"0.50"},{"market":"ETH_USDT","side":"sell","rate":"0.50"}],"period":"1h","leverage":2}}
```

Stop exactly one confirmed instance with `gate-cli cex bot stop --strategy-id '<id>' --strategy-type futures_combo`, without smart-position stop-mode/options. Read back the same ID with `detail` before claiming any lifecycle or financial completion.

<a id="bot.futures-combo.create"></a>
### `gate-cli cex bot futures-combo create`

Operation ID: `bot.futures-combo.create`. Effect: **write**.

Create futures_combo: USDT amount, 2–10 market/side/rate entries, leverage; exactly one period or threshold; optional stop_profit/stop_loss

```text
gate-cli cex bot futures-combo create [flags]
```

API: `POST /api/v4/bot/futures-combo/create` (private).

Returns: [AiHubCreateSuccessResponse](models/spot-grid.md#model-aihubcreatesuccessresponse).

API request model: [FuturesComboCreateRequest](models/portfolios.md#model-futurescombocreaterequest).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `--json` | `string` | Yes | Unset | Typed JSON request with strategy_type and create_params; amounts and rates are strings |
