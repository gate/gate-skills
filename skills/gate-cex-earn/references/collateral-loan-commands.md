# Multi-collateral loans

## Scope and source

Read exact debt, collateral, orders, records and LTV. Confirm loan currency, exact debt/collateral amounts, term and repayment source. Creation, collateral modification and repayment affect funds and liquidation exposure. Query the exact order plus repayment records after writes; do not automatically add collateral, renew, liquidate or convert assets. Currency catalog, quote and quota endpoints are outside this release. Margin/unified trading loans remain owned by gate-cex-trade.

Command contract: use the currently installed and registered Gate CLI command surface. Run the exact leaf with `--help` immediately before execution; its registered flags and required fields are authoritative when they differ from this reference.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Preserved user-intent semantics and PD boundary

- An MCL order must retain its exact order type, borrowed currency/amount,
  collateral currencies/amounts, LTV, outstanding principal and outstanding
  interest. LTV is a risk threshold, not a quote, balance, or assurance that
  liquidation cannot occur.
- For add collateral use `type=append`; for a collateral withdrawal use
  `type=redeem`. Never reverse the direction or submit a compensating adjustment
  after a rejection. For repayment, report principal and interest separately and
  reconcile the exact order afterward.
- A fixed loan needs its verified fixed term and rate; a current loan must not be
  silently substituted for it. The currency catalogue, rate and quota reads were
  removed by PD. Therefore, when a fixed-rate request lacks an already verified
  rate/term, do not guess or place it; hand off to the official product interface.
- Keep loan states distinct, especially lending, repaying, liquidating, finished,
  and liquidated/closed. A write response is not evidence that collateral was
  returned or that debt is cleared.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `mcl.collateral` | `gate-cli cex mcl collateral` | write |
| `mcl.create` | `gate-cli cex mcl create` | write |
| `mcl.ltv` | `gate-cli cex mcl ltv` | read |
| `mcl.order` | `gate-cli cex mcl order` | read |
| `mcl.orders` | `gate-cli cex mcl orders` | read |
| `mcl.records` | `gate-cli cex mcl records` | read |
| `mcl.repay` | `gate-cli cex mcl repay` | write |
| `mcl.repay-records` | `gate-cli cex mcl repay-records` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="mcl.collateral"></a>
### `gate-cli cex mcl collateral`

Operation ID: `mcl.collateral`. Effect: **write**.

Adjust collateral (append or redeem)

```text
gate-cli cex mcl collateral [flags]
```

API: `POST /api/v4/loan/multi_collateral/mortgage` (private).

Returns: [CollateralAdjustRes](models/collateral-loan.md#model-collateraladjustres).

API request model(s), assembled by the command: [CollateralAdjust](models/collateral-loan.md#model-collateraladjust). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--json` | `string` | Yes | Unset | JSON body for CollateralAdjust (required) |

<a id="mcl.create"></a>
### `gate-cli cex mcl create`

Operation ID: `mcl.create`. Effect: **write**.

Create a multi-collateral loan order

```text
gate-cli cex mcl create [flags]
```

API: `POST /api/v4/loan/multi_collateral/orders` (private).

Returns: [OrderResp](models/collateral-loan.md#model-orderresp).

API request model(s), assembled by the command: [CreateMultiCollateralOrder](models/collateral-loan.md#model-createmulticollateralorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--json` | `string` | Yes | Unset | JSON body for CreateMultiCollateralOrder (required) |

<a id="mcl.ltv"></a>
### `gate-cli cex mcl ltv`

Operation ID: `mcl.ltv`. Effect: **read**.

Get multi-collateral LTV (public)

```text
gate-cli cex mcl ltv
```

API: `GET /api/v4/loan/multi_collateral/ltv` (public).

Returns: [CollateralLtv](models/collateral-loan.md#model-collateralltv).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="mcl.order"></a>
### `gate-cli cex mcl order`

Operation ID: `mcl.order`. Effect: **read**.

Get multi-collateral order detail

```text
gate-cli cex mcl order [flags]
```

API: `GET /api/v4/loan/multi_collateral/orders/{order_id}` (private).

Returns: [MultiCollateralOrder](models/collateral-loan.md#model-multicollateralorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `string` | Yes | Unset | Order ID (required) |

<a id="mcl.orders"></a>
### `gate-cli cex mcl orders`

Operation ID: `mcl.orders`. Effect: **read**.

List multi-collateral loan orders

```text
gate-cli cex mcl orders [flags]
```

API: `GET /api/v4/loan/multi_collateral/orders` (private).

Returns: [][MultiCollateralOrder](models/collateral-loan.md#model-multicollateralorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--limit` | `int32` | No | `0` | Maximum number of records |
| `--order-type` | `string` | No | Unset | Order type: current or fixed |
| `--page` | `int32` | No | `0` | Page number |
| `--sort` | `string` | No | Unset | Sort type: time_desc, ltv_asc, ltv_desc |

<a id="mcl.records"></a>
### `gate-cli cex mcl records`

Operation ID: `mcl.records`. Effect: **read**.

List collateral adjustment records

```text
gate-cli cex mcl records [flags]
```

API: `GET /api/v4/loan/multi_collateral/mortgage` (private).

Returns: [][MultiCollateralRecord](models/collateral-loan.md#model-multicollateralrecord).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--collateral-currency` | `string` | No | Unset | Filter by collateral currency |
| `--from` | `int64` | No | `0` | Start timestamp |
| `--limit` | `int32` | No | `0` | Maximum number of records |
| `--page` | `int32` | No | `0` | Page number |
| `--to` | `int64` | No | `0` | End timestamp |

<a id="mcl.repay"></a>
### `gate-cli cex mcl repay`

Operation ID: `mcl.repay`. Effect: **write**.

Repay a multi-collateral loan

```text
gate-cli cex mcl repay [flags]
```

API: `POST /api/v4/loan/multi_collateral/repay` (private).

Returns: [MultiRepayResp](models/collateral-loan.md#model-multirepayresp).

API request model(s), assembled by the command: [RepayMultiLoan](models/collateral-loan.md#model-repaymultiloan). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--json` | `string` | Yes | Unset | JSON body for RepayMultiLoan (required) |

<a id="mcl.repay-records"></a>
### `gate-cli cex mcl repay-records`

Operation ID: `mcl.repay-records`. Effect: **read**.

List multi-collateral repayment records

```text
gate-cli cex mcl repay-records [flags]
```

API: `GET /api/v4/loan/multi_collateral/repay` (private).

Returns: [][MultiRepayRecord](models/collateral-loan.md#model-multirepayrecord).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--borrow-currency` | `string` | No | Unset | Filter by borrowed currency |
| `--from` | `int64` | No | `0` | Start timestamp |
| `--limit` | `int32` | No | `0` | Maximum number of records |
| `--page` | `int32` | No | `0` | Page number |
| `--to` | `int64` | No | `0` | End timestamp |
| `--type` | `string` | Yes | Unset | Operation type: repay or liquidate (required) |

## Verification and recovery

Use `mcl.order`, orders, records and repay-records; check remaining principal, interest, collateral and LTV. If reconciliation is ambiguous, do not repeat repayment.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex mcl orders --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex mcl collateral --json <json> --format json
```
