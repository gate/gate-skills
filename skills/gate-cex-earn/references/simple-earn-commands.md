# Simple Earn and fixed-term lending

## Scope and source

Read Uni rates, interest status, positions and records, plus fixed products, positions and history. For Uni lend, verify the exposed lend/redeem type and amount units rather than inferring direction from the command name. Fixed pre-redeem can change a position. Read positions and histories to verify subscriptions/redemptions; an accepted request is not released principal. Returns vary and principal protection is not implied. BFUSD/RWUSD are competitor products, not Gate command aliases. Do not invent post-subscription rollover settings.

Command contract: use the currently installed and registered Gate CLI command surface. Run the exact leaf with `--help` immediately before execution; its registered flags and required fields are authoritative when they differ from this reference.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Preserved user-intent semantics

- Treat a quoted Uni/fixed product rate as a product comparison, not as the user's
  received interest. For "my earnings" read interest, lending positions, or fixed
  history as applicable; do not substitute a catalogue rate.
- For Uni lending, retain the selected currency, decimal amount, `type` (`lend` or
  `redeem`), and the product-provided `min_rate`. A rate that is unsuitable for a
  lend can prevent execution; never copy it into a redemption or guess its unit.
- For a Uni position, distinguish total/lent/frozen amounts and interest status.
  A frozen amount is not an immediately available redemption balance.
- For fixed products, compare the selected product's asset, term, annual rate,
  minimum/maximum, early-redemption, reinvest, and payout terms. Subscribe only
  with the exact returned product ID and product terms. An early-redeem acceptance
  does not prove principal has been released.
- In fixed holdings, keep holding, redeemed, matured, and settled states distinct;
  use the order's returned IDs and decimal values without rounding them into a
  different amount. Present history operation type separately from principal,
  interest, and bonus amounts.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `earn.fixed.create` | `gate-cli cex earn fixed create` | write |
| `earn.fixed.history` | `gate-cli cex earn fixed history` | read |
| `earn.fixed.lends` | `gate-cli cex earn fixed lends` | read |
| `earn.fixed.pre-redeem` | `gate-cli cex earn fixed pre-redeem` | write |
| `earn.fixed.products` | `gate-cli cex earn fixed products` | read |
| `earn.uni.change` | `gate-cli cex earn uni change` | write |
| `earn.uni.interest-records` | `gate-cli cex earn uni interest-records` | read |
| `earn.uni.interest-status` | `gate-cli cex earn uni interest-status` | read |
| `earn.uni.lend` | `gate-cli cex earn uni lend` | write |
| `earn.uni.lends` | `gate-cli cex earn uni lends` | read |
| `earn.uni.rate` | `gate-cli cex earn uni rate` | read |
| `earn.uni.records` | `gate-cli cex earn uni records` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="earn.fixed.create"></a>
### `gate-cli cex earn fixed create`

API request model: [request fields](models/simple-earn.md#model-fixedtermlendrequest).

Operation ID: `earn.fixed.create`. Effect: **write**.

Subscribe to a fixed-term product

```text
gate-cli cex earn fixed create [flags]
```

API: `POST /api/v4/earn/fixed-term/user/lend` (private).

Returns: [CreateEarnFixedTermLendResponse](models/simple-earn.md#model-createearnfixedtermlendresponse).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--json` | `string` | Yes | Unset | JSON body for subscription request (required) |

`--json` uses [FixedTermLendRequest](models/simple-earn.md#model-fixedtermlendrequest). Keep `product_id` and decimal `amount` from the selected product; renewal and payout fields require explicit intended terms.

<a id="earn.fixed.history"></a>
### `gate-cli cex earn fixed history`

Operation ID: `earn.fixed.history`. Effect: **read**.

List fixed-term subscription history

```text
gate-cli cex earn fixed history [flags]
```

API: `GET /api/v4/earn/fixed-term/user/history` (private).

Returns: [ListEarnFixedTermHistoryResponse](models/simple-earn.md#model-listearnfixedtermhistoryresponse).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--asset` | `string` | No | Unset | Currency |
| `--end-at` | `int32` | No | `0` | End timestamp |
| `--limit` | `int32` | No | `10` | Page size |
| `--order-id` | `string` | No | Unset | Order ID |
| `--page` | `int32` | No | `1` | Page number |
| `--product-id` | `int32` | No | `0` | Product ID |
| `--start-at` | `int32` | No | `0` | Start timestamp |
| `--type` | `string` | No | `1` | Type: 1=subscription, 2=redemption, 3=interest, 4=bonus |

<a id="earn.fixed.lends"></a>
### `gate-cli cex earn fixed lends`

Operation ID: `earn.fixed.lends`. Effect: **read**.

List fixed-term subscription orders

```text
gate-cli cex earn fixed lends [flags]
```

API: `GET /api/v4/earn/fixed-term/user/lend` (private).

Returns: [ListEarnFixedTermLendsResponse](models/simple-earn.md#model-listearnfixedtermlendsresponse).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--asset` | `string` | No | Unset | Currency |
| `--limit` | `int32` | No | `10` | Page size |
| `--order-id` | `int64` | No | `0` | Order ID |
| `--order-type` | `string` | No | `1` | Order type: 1=current, 2=historical |
| `--page` | `int32` | No | `1` | Page number |
| `--product-id` | `int32` | No | `0` | Product ID |

<a id="earn.fixed.pre-redeem"></a>
### `gate-cli cex earn fixed pre-redeem`

API request model: [request fields](models/simple-earn.md#model-earnfixedtermpredeemrequest).

Operation ID: `earn.fixed.pre-redeem`. Effect: **write**.

Early redeem a fixed-term order

```text
gate-cli cex earn fixed pre-redeem [flags]
```

API: `POST /api/v4/earn/fixed-term/user/pre-redeem` (private).

Returns: [CreateEarnFixedTermPreRedeemResponse](models/simple-earn.md#model-createearnfixedtermpreredeemresponse).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--json` | `string` | Yes | Unset | JSON body for pre-redeem request (required) |

`--json` uses [EarnFixedTermPreRedeemRequest](models/simple-earn.md#model-earnfixedtermpredeemrequest): provide the exact `order_id` string.

<a id="earn.fixed.products"></a>
### `gate-cli cex earn fixed products`

Operation ID: `earn.fixed.products`. Effect: **read**.

List fixed-term products

```text
gate-cli cex earn fixed products [flags]
```

API: `GET /api/v4/earn/fixed-term/product` (public).

Returns: [ListEarnFixedTermProductsResponse](models/simple-earn.md#model-listearnfixedtermproductsresponse).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--asset` | `string` | No | Unset | Filter by currency |
| `--limit` | `int32` | No | `10` | Page size |
| `--page` | `int32` | No | `1` | Page number |
| `--show-status` | `string` | No | Unset | Optional display status filter; `2` means visible |
| `--status` | `int32` | No | `0` | Optional product status filter; `2` means subscribable |
| `--type` | `int32` | No | `0` | Product type: 1=regular, 2=VIP |

Filter presence matters: omitting `--status` or `--show-status` preserves upstream defaults. An explicitly supplied `--status 0` or `--show-status ''` is forwarded unchanged. `2` is an example, not a default or a restriction to that value; preserve the supported service values and verify installed flags before use.

<a id="earn.uni.change"></a>
### `gate-cli cex earn uni change`

Operation ID: `earn.uni.change`. Effect: **write**.

Amend lending information

```text
gate-cli cex earn uni change [flags]
```

API: `PATCH /api/v4/earn/uni/lends` (private).

Returns: { `status`: `"ok"` }.

API request model(s), assembled by the command: [PatchUniLend](models/simple-earn.md#model-patchunilend). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--json` | `string` | Yes | Unset | JSON body for change request (required) |

<a id="earn.uni.interest-records"></a>
### `gate-cli cex earn uni interest-records`

Operation ID: `earn.uni.interest-records`. Effect: **read**.

List Uni interest/dividend records

```text
gate-cli cex earn uni interest-records [flags]
```

API: `GET /api/v4/earn/uni/interest_records` (private).

Returns: [][UniInterestRecord](models/simple-earn.md#model-uniinterestrecord).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency |
| `--from` | `int64` | No | `0` | Start timestamp |
| `--limit` | `int32` | No | `0` | Maximum items returned (max 100) |
| `--page` | `int32` | No | `0` | Page number |
| `--to` | `int64` | No | `0` | End timestamp |

<a id="earn.uni.interest-status"></a>
### `gate-cli cex earn uni interest-status`

Operation ID: `earn.uni.interest-status`. Effect: **read**.

Get Uni interest status for a currency

```text
gate-cli cex earn uni interest-status [flags]
```

API: `GET /api/v4/earn/uni/interest_status/{currency}` (private).

Returns: [UniCurrencyInterest](models/simple-earn.md#model-unicurrencyinterest).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | Yes | Unset | Currency name (required) |

<a id="earn.uni.lend"></a>
### `gate-cli cex earn uni lend`

Operation ID: `earn.uni.lend`. Effect: **write**.

Create a Uni lending order

```text
gate-cli cex earn uni lend [flags]
```

API: `POST /api/v4/earn/uni/lends` (private).

Returns: { `status`: `"ok"` }.

API request model(s), assembled by the command: [CreateUniLend](models/simple-earn.md#model-createunilend). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--json` | `string` | Yes | Unset | JSON body for lend request (required) |

<a id="earn.uni.lends"></a>
### `gate-cli cex earn uni lends`

Operation ID: `earn.uni.lends`. Effect: **read**.

List user lending orders

```text
gate-cli cex earn uni lends [flags]
```

API: `GET /api/v4/earn/uni/lends` (private).

Returns: [][UniLend](models/simple-earn.md#model-unilend).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency |
| `--limit` | `int32` | No | `0` | Maximum items returned (max 100) |
| `--page` | `int32` | No | `0` | Page number |

<a id="earn.uni.rate"></a>
### `gate-cli cex earn uni rate`

Operation ID: `earn.uni.rate`. Effect: **read**.

List estimated Uni lending rates

```text
gate-cli cex earn uni rate
```

API: `GET /api/v4/earn/uni/rate` (private).

Returns: [][UniEstimatedRate](models/simple-earn.md#model-uniestimatedrate).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="earn.uni.records"></a>
### `gate-cli cex earn uni records`

Operation ID: `earn.uni.records`. Effect: **read**.

List lending transaction records

```text
gate-cli cex earn uni records [flags]
```

API: `GET /api/v4/earn/uni/lend_records` (private).

Returns: [][UniLendRecord](models/simple-earn.md#model-unilendrecord).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency |
| `--from` | `int64` | No | `0` | Start timestamp |
| `--limit` | `int32` | No | `0` | Maximum items returned (max 100) |
| `--page` | `int32` | No | `0` | Page number |
| `--to` | `int64` | No | `0` | End timestamp |
| `--type` | `string` | No | Unset | Operation type: lend or redeem |

## Verification and recovery

Use `earn.uni.lends`/records/interest-records or `earn.fixed.lends`/history for the correct product. Check principal, available balance and pending/locked state before claiming redemption is complete.
Report quoted/estimated rates separately from distributed interest, released principal and settled balances. Never create a compensating subscription or redemption automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex earn fixed history  --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex earn fixed create --json <json> --format json
```
