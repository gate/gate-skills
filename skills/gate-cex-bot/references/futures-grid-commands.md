# Futures grids

## Scope and source

Use the futures grid model with the correct settlement, direction, leverage, collateral and bounds. Verify contract units, position mode and liquidation exposure. Do not translate a spot grid request into futures. Ongoing trading needs explicit bounded authority. Query the resulting portfolio via the lifecycle contract; stopping does not imply all positions or conditional orders are closed.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the trusted installed binary for the exact command and parameters before execution, including an existing dev build; this catalog does not establish capability availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `bot.grid.futures` | `gate-cli cex bot grid futures` | write |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="bot.grid.futures"></a>
### `gate-cli cex bot grid futures`

Operation ID: `bot.grid.futures`. Effect: **write**.

CLI handler notes: Wraps PostAIHubFuturesGridCreate. Required JSON shape: {strategy_type, market, create_params:{money, low_price, high_price, grid_num, price_type, leverage, direction?, ...}}

Create a futures (contract) grid strategy

```text
gate-cli cex bot grid futures [flags]
```

API: `POST /api/v4/bot/futures-grid/create` (private).

Returns: [AiHubCreateSuccessResponse](models/futures-grid.md#model-aihubcreatesuccessresponse).

API request model(s), assembled by the command: [FuturesGridCreateRequest](models/futures-grid.md#model-futuresgridcreaterequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `--json` | `string` | Yes | Unset | JSON body for FuturesGridCreateRequest (required) |

## Verification and recovery

Use the canonical bot lifecycle detail/running reads for the returned portfolio, then inspect residual contract exposure when stopping.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

Verify and stop through [bot lifecycle](bot-lifecycle-commands.md).

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex bot grid futures --json <json> --format json
```

An agent grant expiring does not stop an already running backend strategy. If the user requires a hard deadline or cumulative spending cap that the actual creation model/backend cannot enforce, stop that variant or obtain a different explicit instruction; do not promise an automatic stop, local timer or cross-session budget control.

Apply the product-specific [Bot response contract](bot-lifecycle-commands.md#bot-response-and-route-contract); a successful submission is not proof of a completed lifecycle.

## Product workflow requirements


The verified leaf is `gate-cli cex bot grid futures --json '<business object>'`. Read [execution](../../_shared/cex/execution-cli.md) first. Outer fields: strategy_type="futures_grid", market and create_params. Required parameters: money, low_price, high_price and leverage as strings; grid_num as integer; price_type 0 arithmetic or 1 geometric. Direction is long, short or neutral. If omitted, the product's neutral default must be shown explicitly in the draft. This direction vocabulary differs from contract martingale buy/sell.

Retain optional trigger_price, stop_profit, stop_loss, is_use_base and profit_sharing_ratio if supported and selected. Convert ratio inputs once, keep price conditions as prices, and show leverage, liquidation exposure and transfers. Map recommendation price_low/price_high/grid_count to create low_price/high_price/grid_num; verify the preview's direction and leverage and collect missing fields. Apply [Bot confirmation gate](bot-workflows.md#bot-confirmation-gate), execute once, and verify the original identity/state through [lifecycle](bot-lifecycle-commands.md). Stop does not establish final settlement.
