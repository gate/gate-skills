# Spot and contract martingale

## Scope and source

Keep spot and contract creation models separate. Explain the multiplier/addition sequence, maximum additions, total possible spend, leverage and loss exposure before creation. A larger later order is not covered by a smaller one-off trade grant. Require enforceable strategy limits from the actual model/backend; missing limits stop the proposed autonomous task. Use detail/running/stop through the lifecycle contract.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the trusted installed binary for the exact command and parameters before execution, including an existing dev build; this catalog does not establish capability availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `bot.martingale.contract` | `gate-cli cex bot martingale contract` | write |
| `bot.martingale.spot` | `gate-cli cex bot martingale spot` | write |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="bot.martingale.contract"></a>
### `gate-cli cex bot martingale contract`

Operation ID: `bot.martingale.contract`. Effect: **write**.

Fixed stop-loss prices require a supported stop_loss_price_type of last, index or mark.
Check the installed command and request model; if either field cannot be preserved, keep the action unexecuted.

Create a contract martingale strategy

```text
gate-cli cex bot martingale contract [flags]
```

API: `POST /api/v4/bot/contract-martingale/create` (private).

Returns: [AiHubCreateSuccessResponse](models/martingale.md#model-aihubcreatesuccessresponse).

API request model(s), assembled by the command: [ContractMartingaleCreateRequest](models/martingale.md#model-contractmartingalecreaterequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `--json` | `string` | Yes | Unset | JSON body for ContractMartingaleCreateRequest (required) |

<a id="bot.martingale.spot"></a>
### `gate-cli cex bot martingale spot`

Operation ID: `bot.martingale.spot`. Effect: **write**.

CLI handler notes: Wraps PostAIHubSpotMartingaleCreate.

Request contract: stop-loss is expressed via create_params.stop_loss_per_cycle
(per-round ratio); the legacy create_params.stop_loss_price is no longer
mapped on this path. Optional create_params.trigger_price is also accepted.

Create a spot martingale strategy

```text
gate-cli cex bot martingale spot [flags]
```

API: `POST /api/v4/bot/spot-martingale/create` (private).

Returns: [AiHubCreateSuccessResponse](models/martingale.md#model-aihubcreatesuccessresponse).

API request model(s), assembled by the command: [SpotMartingaleCreateRequest](models/martingale.md#model-spotmartingalecreaterequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `--json` | `string` | Yes | Unset | JSON body for SpotMartingaleCreateRequest (required) |

## Verification and recovery

Use lifecycle detail/running for the exact strategy type and portfolio reference. Verify actual sequence/limits, committed funds and exposure rather than describing the strategy as risk-free.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

Verify and stop through [bot lifecycle](bot-lifecycle-commands.md).

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex bot martingale contract --json <json> --format json
```

An agent grant expiring does not stop an already running backend strategy. If the user requires a hard deadline or cumulative spending cap that the actual creation model/backend cannot enforce, stop that variant or obtain a different explicit instruction; do not promise an automatic stop, local timer or cross-session budget control.

Apply the product-specific [Bot response contract](bot-lifecycle-commands.md#bot-response-and-route-contract); a successful submission is not proof of a completed lifecycle.

## Product workflow requirements


Read [execution](../../_shared/cex/execution-cli.md) and [Bot confirmation gate](bot-workflows.md#bot-confirmation-gate). Verified leaves take `--json` business objects with strategy_type, market and create_params.

## Spot martingale

Use `gate-cli cex bot martingale spot`. Type spot_martingale. Required: invest_amount, price_deviation and take_profit_ratio strings; max_orders integer. max_orders means maximum additional entries excluding the first. Ask whether an ambiguous total-order count includes the first; do not silently change it. Optional trigger_price is a price, stop_loss_per_cycle a per-cycle ratio, and profit_sharing_ratio a ratio.

For requested protection, require a positive supported per-cycle stop-loss ratio. Zero/negative values disable protection and cannot fulfill that intent. A fixed stop price cannot be silently converted to a per-cycle ratio; explain the product boundary and ask for a supported explicit choice. Convert 2% to "0.02" once. A recommendation's frequency/max_orders must retain the same additional-entry meaning; select only create fields supported by this contract, not every preview property.

## Contract martingale

Use `gate-cli cex bot martingale contract` with the [verified candidate](compatibility.md) after checking actual leaf help. Type contract_martingale. Required: invest_amount, price_deviation and take_profit_ratio strings; max_orders integer; direction buy or sell; explicit leverage string. max_orders still excludes the first entry.

For fixed stop_loss_price, collect stop_loss_price_type last, index or mark and persist both. Missing basis blocks execution; do not choose a default. No fixed-price intent requires no such question. SDK v7.2.167 preserves both fields; use them together in the direct create_params object. A different installed binary must prove the same capability before use.

The backend, using the existing complete-ladder margin formula, current contract multiplier/step, owner fee, leverage, direction and add count, derives a downward-quantized first size and rechecks the full budget. The Agent does not copy that algorithm, increase investment, lower adds or promise affordability from a recommendation. If the minimum viable size exceeds budget, show the refusal and ask for a newly reviewed choice. Contract martingale has no official recommendation flow.
