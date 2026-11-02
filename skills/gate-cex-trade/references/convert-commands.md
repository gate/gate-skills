# Currency conversion

## Scope and source

Use the exact pair, currencies and amount mode returned by discovery. Preview the same request before creation; keep quote ID, amounts, rate, fees and expiry if the response provides them. A preview is read-only despite POST. Creation spends assets and needs a valid grant. An expired or changed quote requires a new preview and review of changed terms; do not automatically accept a worse rate. Single-currency, one-to-many, many-to-one and v1 calls have distinct models. Read order state before claiming conversion is complete.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `flash-swap.create` | `gate-cli cex flash-swap create` | write |
| `flash-swap.create-many-to-one` | `gate-cli cex flash-swap create-many-to-one` | write |
| `flash-swap.create-one-to-many` | `gate-cli cex flash-swap create-one-to-many` | write |
| `flash-swap.create-v1` | `gate-cli cex flash-swap create-v1` | write |
| `flash-swap.order` | `gate-cli cex flash-swap order` | read |
| `flash-swap.orders` | `gate-cli cex flash-swap orders` | read |
| `flash-swap.pairs` | `gate-cli cex flash-swap pairs` | read |
| `flash-swap.preview` | `gate-cli cex flash-swap preview` | read |
| `flash-swap.preview-many-to-one` | `gate-cli cex flash-swap preview-many-to-one` | read |
| `flash-swap.preview-one-to-many` | `gate-cli cex flash-swap preview-one-to-many` | read |
| `flash-swap.preview-v1` | `gate-cli cex flash-swap preview-v1` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="flash-swap.create"></a>
### `gate-cli cex flash-swap create`

Operation ID: `flash-swap.create`. Effect: **write**.

Create a flash swap order

```text
gate-cli cex flash-swap create [flags]
```

API: `POST /api/v4/flash_swap/orders` (private).

Returns: [FlashSwapOrder](models/convert.md#model-flashswaporder).

API request model(s), assembled by the command: [FlashSwapOrderRequest](models/convert.md#model-flashswaporderrequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--buy-amount` | `string` | Yes | Unset | Amount to buy (required) |
| `--buy-currency` | `string` | Yes | Unset | Currency to buy (required) |
| `--preview-id` | `string` | Yes | Unset | Preview result ID (required) |
| `--sell-amount` | `string` | Yes | Unset | Amount to sell (required) |
| `--sell-currency` | `string` | Yes | Unset | Currency to sell (required) |

<a id="flash-swap.create-many-to-one"></a>
### `gate-cli cex flash-swap create-many-to-one`

Operation ID: `flash-swap.create-many-to-one`. Effect: **write**.

Create a multi-currency many-to-one flash swap order

```text
gate-cli cex flash-swap create-many-to-one [flags]
```

API: `POST /api/v4/flash_swap/multi-currency/many-to-one/order/create` (private).

Returns: [FlashSwapMultiCurrencyManyToOneOrderCreateResp](models/convert.md#model-flashswapmulticurrencymanytooneordercreateresp).

API request model(s), assembled by the command: [FlashSwapMultiCurrencyManyToOneOrderCreateReq](models/convert.md#model-flashswapmulticurrencymanytooneordercreatereq). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--json` | `string` | Yes | Unset | JSON body for create params (required) |

<a id="flash-swap.create-one-to-many"></a>
### `gate-cli cex flash-swap create-one-to-many`

Operation ID: `flash-swap.create-one-to-many`. Effect: **write**.

Create a multi-currency one-to-many flash swap order

```text
gate-cli cex flash-swap create-one-to-many [flags]
```

API: `POST /api/v4/flash_swap/multi-currency/one-to-many/order/create` (private).

Returns: [FlashSwapMultiCurrencyOneToManyOrderCreateResp](models/convert.md#model-flashswapmulticurrencyonetomanyordercreateresp).

API request model(s), assembled by the command: [FlashSwapMultiCurrencyOneToManyOrderCreateReq](models/convert.md#model-flashswapmulticurrencyonetomanyordercreatereq). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--json` | `string` | Yes | Unset | JSON body for create params (required) |

<a id="flash-swap.create-v1"></a>
### `gate-cli cex flash-swap create-v1`

Operation ID: `flash-swap.create-v1`. Effect: **write**.

Create a flash swap order (v1)

```text
gate-cli cex flash-swap create-v1 [flags]
```

API: `POST /api/v4/flash_swap/order/create` (private).

Returns: [FlashSwapOrderCreateResp](models/convert.md#model-flashswapordercreateresp).

API request model(s), assembled by the command: [FlashSwapOrderCreateReq](models/convert.md#model-flashswapordercreatereq). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--json` | `string` | Yes | Unset | JSON body for FlashSwapOrderCreateReq (required) |

<a id="flash-swap.order"></a>
### `gate-cli cex flash-swap order`

Operation ID: `flash-swap.order`. Effect: **read**.

Get a flash swap order by ID

```text
gate-cli cex flash-swap order [flags]
```

API: `GET /api/v4/flash_swap/orders/{order_id}` (private).

Returns: [FlashSwapOrder](models/convert.md#model-flashswaporder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int32` | Yes | `0` | Order ID (required) |

<a id="flash-swap.orders"></a>
### `gate-cli cex flash-swap orders`

Operation ID: `flash-swap.orders`. Effect: **read**.

List flash swap orders

```text
gate-cli cex flash-swap orders [flags]
```

API: `GET /api/v4/flash_swap/orders` (private).

Returns: [][FlashSwapOrder](models/convert.md#model-flashswaporder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--buy-currency` | `string` | No | Unset | Currency bought |
| `--limit` | `int32` | No | `0` | Maximum number of records |
| `--page` | `int32` | No | `1` | Page number |
| `--sell-currency` | `string` | No | Unset | Currency sold |
| `--status` | `int32` | No | `0` | Order status: 1=success, 2=failed |

<a id="flash-swap.pairs"></a>
### `gate-cli cex flash-swap pairs`

Operation ID: `flash-swap.pairs`. Effect: **read**.

List all supported currency pairs in flash swap (public)

```text
gate-cli cex flash-swap pairs [flags]
```

API: `GET /api/v4/flash_swap/currency_pairs` (public).

Returns: [][FlashSwapCurrencyPair](models/convert.md#model-flashswapcurrencypair).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency name |
| `--limit` | `int32` | No | `0` | Maximum number of items returned |
| `--page` | `int32` | No | `1` | Page number |

<a id="flash-swap.preview"></a>
### `gate-cli cex flash-swap preview`

Operation ID: `flash-swap.preview`. Effect: **read**.

Preview a flash swap order

```text
gate-cli cex flash-swap preview [flags]
```

API: `POST /api/v4/flash_swap/orders/preview` (private).

Returns: [FlashSwapOrderPreview](models/convert.md#model-flashswaporderpreview).

API request model(s), assembled by the command: [FlashSwapPreviewRequest](models/convert.md#model-flashswappreviewrequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--buy-amount` | `string` | No | Unset | Amount to buy (either sell-amount or buy-amount) |
| `--buy-currency` | `string` | Yes | Unset | Currency to buy (required) |
| `--sell-amount` | `string` | No | Unset | Amount to sell (either sell-amount or buy-amount) |
| `--sell-currency` | `string` | Yes | Unset | Currency to sell (required) |

<a id="flash-swap.preview-many-to-one"></a>
### `gate-cli cex flash-swap preview-many-to-one`

Operation ID: `flash-swap.preview-many-to-one`. Effect: **read**.

Preview a multi-currency many-to-one flash swap order

```text
gate-cli cex flash-swap preview-many-to-one [flags]
```

API: `POST /api/v4/flash_swap/multi-currency/many-to-one/order/preview` (private).

Returns: [FlashSwapMultiCurrencyManyToOneOrderPreviewResp](models/convert.md#model-flashswapmulticurrencymanytooneorderpreviewresp).

API request model(s), assembled by the command: [FlashSwapMultiCurrencyManyToOneOrderPreviewReq](models/convert.md#model-flashswapmulticurrencymanytooneorderpreviewreq). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--json` | `string` | Yes | Unset | JSON body for preview params (required) |

<a id="flash-swap.preview-one-to-many"></a>
### `gate-cli cex flash-swap preview-one-to-many`

Operation ID: `flash-swap.preview-one-to-many`. Effect: **read**.

Preview a multi-currency one-to-many flash swap order

```text
gate-cli cex flash-swap preview-one-to-many [flags]
```

API: `POST /api/v4/flash_swap/multi-currency/one-to-many/order/preview` (private).

Returns: [FlashSwapMultiCurrencyOneToManyOrderPreviewResp](models/convert.md#model-flashswapmulticurrencyonetomanyorderpreviewresp).

API request model(s), assembled by the command: [FlashSwapMultiCurrencyOneToManyOrderPreviewReq](models/convert.md#model-flashswapmulticurrencyonetomanyorderpreviewreq). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--json` | `string` | Yes | Unset | JSON body for preview params (required) |

<a id="flash-swap.preview-v1"></a>
### `gate-cli cex flash-swap preview-v1`

Operation ID: `flash-swap.preview-v1`. Effect: **read**.

Preview a flash swap order (v1, one-to-one)

```text
gate-cli cex flash-swap preview-v1 [flags]
```

API: `GET /api/v4/flash_swap/order/preview` (private).

Returns: [FlashSwapOrderPreviewResp](models/convert.md#model-flashswaporderpreviewresp).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--buy-amount` | `string` | No | Unset | Buy amount (either sell-amount or buy-amount) |
| `--buy-asset` | `string` | Yes | Unset | Currency to buy (required) |
| `--sell-amount` | `string` | No | Unset | Sell amount (either sell-amount or buy-amount) |
| `--sell-asset` | `string` | Yes | Unset | Currency to sell (required) |

## Verification and recovery

Use `flash-swap.order` with the returned order reference and inspect the conversion status, spent/received amounts and fee fields actually returned. Preview does not spend funds.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex flash-swap order --id <id> --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex flash-swap create --buy-amount <buy-amount> --buy-currency <buy-currency> --preview-id <preview-id> --sell-amount <sell-amount> --sell-currency <sell-currency> --format json
```
