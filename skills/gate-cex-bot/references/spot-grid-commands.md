# Spot, margin and infinite grids

## Scope and source

Read recommend for the exact market and strategy type, then validate the selected create model. Spot and margin grid have separate exposure; margin requires explicit borrowing/leverage authority. Infinite grid has no fixed upper exit guarantee. money, bounds, grid count and price type are product inputs, not risk controls enforced by this document. Creating a bot authorizes continuing trades; duration, budget and stop conditions must be explicit. Verify with detail/running; lifecycle actions are owned by bot-lifecycle-commands.md.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the trusted installed binary for the exact command and parameters before execution, including an existing dev build; this catalog does not establish capability availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `bot.grid.infinite` | `gate-cli cex bot grid infinite` | write |
| `bot.grid.margin` | `gate-cli cex bot grid margin` | write |
| `bot.grid.spot` | `gate-cli cex bot grid spot` | write |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="bot.grid.infinite"></a>
### `gate-cli cex bot grid infinite`

Operation ID: `bot.grid.infinite`. Effect: **write**.

CLI handler notes: Wraps PostAIHubInfiniteGridCreate. Optional fields include grid_num/price_type; required JSON keys are money, price_floor, profit_per_grid.

Create an infinite grid strategy

```text
gate-cli cex bot grid infinite [flags]
```

API: `POST /api/v4/bot/infinite-grid/create` (private).

Returns: [AiHubCreateSuccessResponse](models/spot-grid.md#model-aihubcreatesuccessresponse).

API request model(s), assembled by the command: [InfiniteGridCreateRequest](models/spot-grid.md#model-infinitegridcreaterequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `--json` | `string` | Yes | Unset | JSON body for InfiniteGridCreateRequest (required) |

<a id="bot.grid.margin"></a>
### `gate-cli cex bot grid margin`

Operation ID: `bot.grid.margin`. Effect: **write**.

CLI handler notes: Wraps PostAIHubMarginGridCreate. Required JSON shape: {strategy_type, market, create_params:{money, low_price, high_price, grid_num, price_type, leverage, direction?, ...}}

Create a margin (leverage) grid strategy

```text
gate-cli cex bot grid margin [flags]
```

API: `POST /api/v4/bot/margin-grid/create` (private).

Returns: [AiHubCreateSuccessResponse](models/spot-grid.md#model-aihubcreatesuccessresponse).

API request model(s), assembled by the command: [MarginGridCreateRequest](models/spot-grid.md#model-margingridcreaterequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `--json` | `string` | Yes | Unset | JSON body for MarginGridCreateRequest (required) |

<a id="bot.grid.spot"></a>
### `gate-cli cex bot grid spot`

Operation ID: `bot.grid.spot`. Effect: **write**.

CLI handler notes: Wraps PostAIHubSpotGridCreate. Required JSON shape: {strategy_type, market, create_params:{money, low_price, high_price, grid_num, price_type, ...}}

Create a spot grid strategy

```text
gate-cli cex bot grid spot [flags]
```

API: `POST /api/v4/bot/spot-grid/create` (private).

Returns: [AiHubCreateSuccessResponse](models/spot-grid.md#model-aihubcreatesuccessresponse).

API request model(s), assembled by the command: [SpotGridCreateRequest](models/spot-grid.md#model-spotgridcreaterequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `--json` | `string` | Yes | Unset | JSON body for SpotGridCreateRequest (required) |

## Verification and recovery

After creation, pass the returned portfolio reference and strategy type to the canonical bot lifecycle detail action. Verify running state and budget; do not submit again when the response is lost.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

Verify and stop through [bot lifecycle](bot-lifecycle-commands.md).

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex bot grid infinite --json <json> --format json
```

Grid `price_type` accepts integer 0 or 1 and `grid_num` must be at least 1. The linked model notes include the verified infinite-grid spacing mapping. For other grids, use verified product terms or an explicitly selected/recommended value rather than guessing a natural-language spacing mapping.

An agent grant expiring does not stop an already running backend strategy. If the user requires a hard deadline or cumulative spending cap that the actual creation model/backend cannot enforce, stop that variant or obtain a different explicit instruction; do not promise an automatic stop, local timer or cross-session budget control.

Apply the product-specific [Bot response contract](bot-lifecycle-commands.md#bot-response-and-route-contract); a successful submission is not proof of a completed lifecycle.

## Product workflow requirements


Follow [execution](../../_shared/cex/execution-cli.md) and [Bot confirmation gate](bot-workflows.md#bot-confirmation-gate). Each leaf takes `--json` with `strategy_type`, `market` and `create_params`.

| Product / verified leaf after `gate-cli cex bot` | Required create_params | Additional settings |
|---|---|---|
| spot_grid / `grid spot` | money, low_price, high_price, grid_num, price_type | trigger_price, stop_profit, stop_loss, is_use_base, profit_sharing_ratio |
| margin_grid / `grid margin` | money, low_price, high_price, grid_num, price_type, explicit leverage | applicable trigger/protection/base and sharing settings |
| infinite_grid / `grid infinite` | money, price_floor, profit_per_grid | applicable trigger/protection/base and sharing settings |

Amounts/prices/leverage are strings, grid_num is an integer, price_type is 0 arithmetic or 1 geometric, and is_use_base is boolean. Infinite grid takes its floor and per-grid profit directly; do not request ordinary-grid count/mode. Normalize profit_per_grid and sharing percentages once, e.g. 1.5% => "0.015". Keep price stops as prices. Show optional base-asset use and leverage/funding effects in the draft.

Example business object for `grid spot --json`:

```json
{"strategy_type":"spot_grid","market":"BTC_USDT","create_params":{"money":"1000","low_price":"60000","high_price":"72000","grid_num":50,"price_type":0,"is_use_base":false}}
```

A recommendation preview uses price_low/price_high/grid_count for ordinary spot/futures; explicitly map these to low_price/high_price/grid_num. Margin preview already uses those create keys; serialize its numeric leverage as the required string. Infinite preview uses price_floor/profit_per_grid. Complete investment and any missing mode/protection before confirmation. A recommendation does not prove sufficient funds. Preserve typed repayment advice on stop and direct the user to resolve it; do not auto-fund.

## Existing stop behavior

The ID/type stop leaf submits the existing product exit; it does not select a sell-all or keep-assets option. For spot grid, the worker cancels ordinary orders and handles any persisted stop option. Without such an option, its saved stop-operation flag determines whether to sell the remaining base asset; otherwise it does not sell all base. Therefore "default stop" alone does not establish which assets will remain. Sales may incur fees and slippage; cancellation, sales and final asset return must be verified separately, and an accepted stop does not prove any of them completed. Stopping ends the strategy's trading; restarting requires a separate action.

Before offering an executable stop draft, verify the selected instance's actual persisted exit behavior from an authoritative readback. Do not infer it from product type, user acceptance of "default", empty metrics or a previous create draft. If the current client cannot expose the saved setting, explain the missing fact and stop before confirmation/execution; use the strategy management page to inspect it. Do not manufacture a flag, silently choose an exit, or treat another confirmation as a substitute for this fact. Margin/infinite grids likewise require their verified product-specific exit and repayment facts; this spot-grid description is not evidence for those products.
