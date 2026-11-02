# Dual investment

## Scope and source

Read plan, underlying, subscription currency, strike/target, expiry, delivery rules and reinvest setting. Settlement can return a different asset; quoted yield is not guaranteed net profit. Placement and reinvest changes are writes. Query the exact order and balance after completion. Early redemption and recommendation endpoints are outside this release.

Command contract: use the currently installed and registered Gate CLI command surface. Run the exact leaf with `--help` immediately before execution; its registered flags and required fields are authoritative when they differ from this reference.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Preserved user-intent semantics

- Classify a plan as sell-high or buy-low from its investment and exercise
  currencies; do not use a generic "earn" label that hides possible currency
  conversion at settlement. Before placing an order, show the investment currency,
  amount, target/exercise price, delivery condition, possible settlement currency,
  quoted APY, and reinvest choice.
- `apy_display` and `apy_settlement` are decimal rate fields. For user-facing
  percentages, multiply the returned decimal by 100 and append `%`; never attach
  `%` to the raw value. Quoted APY is not realised PnL or a guarantee.
- For a settlement explanation, use the exact order's exercise price, settlement
  price, settlement amount and settlement currency. State both possible outcomes
  before an order is placed; do not promise that the invested currency is returned.
- Keep order states distinct: created/pending, in position, settling, settled,
  cancelled and failed. Do not call an order settled merely because it was
  accepted. Display delivery/creation timestamps only when they answer the user's
  requested time question; they are not evidence of a result.
- For an amount/minimum question, inspect the matching available plan and its
  returned minimum before discussing eligibility. Recommendation and early
  redemption remain excluded by PD scope.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `earn.dual.balance` | `gate-cli cex earn dual balance` | read |
| `earn.dual.modify-reinvest` | `gate-cli cex earn dual modify-reinvest` | write |
| `earn.dual.orders` | `gate-cli cex earn dual orders` | read |
| `earn.dual.place` | `gate-cli cex earn dual place` | write |
| `earn.dual.plans` | `gate-cli cex earn dual plans` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="earn.dual.balance"></a>
### `gate-cli cex earn dual balance`

Operation ID: `earn.dual.balance`. Effect: **read**.

Get dual investment balance

```text
gate-cli cex earn dual balance
```

API: `GET /api/v4/earn/dual/balance` (private).

Returns: [DualGetBalance](models/dual-investment.md#model-dualgetbalance).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="earn.dual.modify-reinvest"></a>
### `gate-cli cex earn dual modify-reinvest`

Operation ID: `earn.dual.modify-reinvest`. Effect: **write**.

Modify reinvest setting of a dual investment order

```text
gate-cli cex earn dual modify-reinvest [flags]
```

API: `POST /api/v4/earn/dual/modify-order-reinvest` (private).

Returns: { `status`: `"ok"`, `order_id`: `int64`, `reinvest`: `int32` }.

API request model(s), assembled by the command: [DualModifyOrderReinvestParams](models/dual-investment.md#model-dualmodifyorderreinvestparams). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--duration` | `int64` | No | `0` | Effective duration in seconds; default 86400 (1 day) if omitted |
| `--order-id` | `int64` | Yes | `0` | Order ID (required) |
| `--status` | `int32` | Yes | `0` | 0=off, 1=on (required) |

<a id="earn.dual.orders"></a>
### `gate-cli cex earn dual orders`

Operation ID: `earn.dual.orders`. Effect: **read**.

List dual investment orders

```text
gate-cli cex earn dual orders [flags]
```

API: `GET /api/v4/earn/dual/orders` (private).

Returns: [][DualGetOrders](models/dual-investment.md#model-dualgetorders).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--from` | `int64` | No | `0` | Start settlement time |
| `--limit` | `int32` | No | `0` | Maximum number of records |
| `--page` | `int32` | No | `0` | Page number |
| `--to` | `int64` | No | `0` | End settlement time |

<a id="earn.dual.place"></a>
### `gate-cli cex earn dual place`

Operation ID: `earn.dual.place`. Effect: **write**.

Place a dual investment order

```text
gate-cli cex earn dual place [flags]
```

API: `POST /api/v4/earn/dual/orders` (private).

Returns: [PlaceDualInvestmentOrder](models/dual-investment.md#model-placedualinvestmentorder).

API request model(s), assembled by the command: [PlaceDualInvestmentOrderParams](models/dual-investment.md#model-placedualinvestmentorderparams). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--amount` | `string` | Yes | Unset | Subscription amount (required) |
| `--plan-id` | `string` | Yes | Unset | Product plan ID (required) |
| `--text` | `string` | No | Unset | Custom order ID (must start with t-) |

<a id="earn.dual.plans"></a>
### `gate-cli cex earn dual plans`

Operation ID: `earn.dual.plans`. Effect: **read**.

List dual investment plans

```text
gate-cli cex earn dual plans [flags]
```

API: `GET /api/v4/earn/dual/investment_plan` (public).

Returns: [][DualGetPlans](models/dual-investment.md#model-dualgetplans).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--plan-id` | `int64` | No | `0` | Filter by plan ID |

## Verification and recovery

Use `earn.dual.orders` and balance; check the exact plan/order, maturity, settlement asset and reinvest flag. A successful reinvest change does not place a new subscription.
Report quoted APY separately from settled amounts and realised APY. Never place a compensating dual order automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex earn dual balance  --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex earn dual modify-reinvest --order-id <order-id> --status <status> --format json
```
