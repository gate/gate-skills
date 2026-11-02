# Recurring investment

## Scope and source

This release supports only supported-asset discovery, the minimum investment amount, and order queries for a specified plan and execution record. Creating, updating, stopping, topping up, listing, inspecting, or reading records for a plan is intentionally excluded. Do not infer a plan's schedule, funding source, or state from an order response.

Command contract: use the currently installed and registered Gate CLI command surface. Run the exact leaf with `--help` immediately before execution; its registered flags and required fields are authoritative when they differ from this reference.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. These reads require an applicable read grant. Command existence never proves account eligibility.

## Preserved user-intent semantics and PD boundary

Auto-invest means a scheduled recurring purchase, not an immediate manual trade.
The retained reads can answer whether an asset is supported, its minimum amount,
or the result of one specified plan execution. Keep order amount, asset, market,
price, side, status, error and fund-flow fields tied to that execution record.

Plan creation, update, stop, top-up, plan list/detail, schedule/configuration and
execution-record list were explicitly removed by the current PD decision. Do not
infer a plan's cadence, next purchase, funding account, active/paused state, or
investment allocation from an order response; explain that the requested plan
capability is outside this release instead.

## Action index

| Operation ID | CLI command | Effect |
| --- | --- | --- |
| `earn.auto-invest.coins` | `gate-cli cex earn auto-invest coins` | read |
| `earn.auto-invest.min-amount` | `gate-cli cex earn auto-invest min-amount` | read |
| `earn.auto-invest.orders` | `gate-cli cex earn auto-invest orders` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Pass validated values as separate process arguments. Keep exact decimal amounts and identifiers, and bound record queries to the requested period and a limited count. `min-amount` is a read despite its POST transport.

<a id="earn.auto-invest.coins"></a>
### `gate-cli cex earn auto-invest coins`

Operation ID: `earn.auto-invest.coins`. Effect: **read**.

List currencies supporting auto-invest.

```text
gate-cli cex earn auto-invest coins [flags]
```

API: `GET /api/v4/earn/autoinvest/coins` (private).

Returns: [][AutoInvestCoinsItem](models/auto-invest.md#model-autoinvestcoinsitem).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--plan-money` | `string` | No | Unset | Pricing currency: USDT or BTC (default USDT) |

<a id="earn.auto-invest.min-amount"></a>
### `gate-cli cex earn auto-invest min-amount`

Operation ID: `earn.auto-invest.min-amount`. Effect: **read**.

Get the minimum auto-invest amount for an asset.

```text
gate-cli cex earn auto-invest min-amount [flags]
```

API: `POST /api/v4/earn/autoinvest/min_invest_amount` (private).

Returns: [AutoInvestMinInvestAmountResp](models/auto-invest.md#model-autoinvestmininvestamountresp).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--json` | `string` | Yes | Unset | JSON body using [AutoInvestMinInvestAmount](models/auto-invest.md#model-autoinvestmininvestamount) (required). |

`--json` must explicitly include `asset_type`: integer `1` for cryptocurrency or `2` for TradFi stocks, with the selected `money` and `items`. Do not infer an omitted asset family or coerce a string/boolean into an integer.

```text
gate-cli cex earn auto-invest min-amount --json '{"money":"USDT","asset_type":1,"items":[{"asset":"BTC","ratio":"1"}]}' --format json
```

The example is a read-only cryptocurrency request, not a default allocation or authority to create a recurring plan. For stocks choose `asset_type=2` and actual supported stock assets.

<a id="earn.auto-invest.orders"></a>
### `gate-cli cex earn auto-invest orders`

Operation ID: `earn.auto-invest.orders`. Effect: **read**.

List auto-invest orders for a specified plan execution record.

```text
gate-cli cex earn auto-invest orders [flags]
```

API: `GET /api/v4/earn/autoinvest/orders` (private).

Returns: [][AutoInvestOrderItem](models/auto-invest.md#model-autoinvestorderitem).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--plan-id` | `int64` | Yes | `0` | Plan ID (required) |
| `--record-id` | `int64` | Yes | `0` | Execution record ID (required) |

## Verification and recovery

These are read-only operations. If an order query is incomplete or paginated, narrow the time window or page within the shared execution budget. Do not infer that a scheduled plan is active, paused, or stopped from this result alone.

## Call template

```text
gate-cli cex earn auto-invest orders --plan-id <plan-id> --record-id <record-id> --format json
```
