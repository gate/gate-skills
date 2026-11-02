# Delivery futures

## Scope and source

Keep expiry and settlement currency explicit. Verify the dated contract, trading window, multiplier and signed contract quantity before ordering. Do not route a dated contract through perpetual commands. Match single/dual position assumptions to the actual product contract; do not assume perpetual-only flags exist here. Read leverage and risk limits before a change. Query orders, positions and settlement records separately: expiry settlement is not an order fill.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `delivery.account.book` | `gate-cli cex delivery account book` | read |
| `delivery.account.get` | `gate-cli cex delivery account get` | read |
| `delivery.order.cancel` | `gate-cli cex delivery order cancel` | write |
| `delivery.order.cancel-all` | `gate-cli cex delivery order cancel-all` | write |
| `delivery.order.create` | `gate-cli cex delivery order create` | write |
| `delivery.order.get` | `gate-cli cex delivery order get` | read |
| `delivery.order.list` | `gate-cli cex delivery order list` | read |
| `delivery.order.my-trades` | `gate-cli cex delivery order my-trades` | read |
| `delivery.position.close` | `gate-cli cex delivery position close` | read |
| `delivery.position.get` | `gate-cli cex delivery position get` | read |
| `delivery.position.liquidates` | `gate-cli cex delivery position liquidates` | read |
| `delivery.position.list` | `gate-cli cex delivery position list` | read |
| `delivery.position.settlements` | `gate-cli cex delivery position settlements` | read |
| `delivery.position.update-leverage` | `gate-cli cex delivery position update-leverage` | write |
| `delivery.position.update-margin` | `gate-cli cex delivery position update-margin` | write |
| `delivery.position.update-risk-limit` | `gate-cli cex delivery position update-risk-limit` | write |
| `delivery.price-trigger.cancel` | `gate-cli cex delivery price-trigger cancel` | write |
| `delivery.price-trigger.cancel-all` | `gate-cli cex delivery price-trigger cancel-all` | write |
| `delivery.price-trigger.create` | `gate-cli cex delivery price-trigger create` | write |
| `delivery.price-trigger.get` | `gate-cli cex delivery price-trigger get` | read |
| `delivery.price-trigger.list` | `gate-cli cex delivery price-trigger list` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="delivery.account.book"></a>
### `gate-cli cex delivery account book`

Operation ID: `delivery.account.book`. Effect: **read**.

List delivery futures account change history

```text
gate-cli cex delivery account book [flags]
```

API: `GET /api/v4/delivery/{settle}/account_book` (private).

Returns: [][DeliveryAccountBook](models/delivery.md#model-deliveryaccountbook).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--type` | `string` | No | Unset | Change type filter |

<a id="delivery.account.get"></a>
### `gate-cli cex delivery account get`

Operation ID: `delivery.account.get`. Effect: **read**.

Get delivery futures account information

```text
gate-cli cex delivery account get
```

API: `GET /api/v4/delivery/{settle}/accounts` (private).

Returns: [DeliveryAccount](models/delivery.md#model-deliveryaccount).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="delivery.order.cancel"></a>
### `gate-cli cex delivery order cancel`

Operation ID: `delivery.order.cancel`. Effect: **write**.

Cancel a single delivery futures order

```text
gate-cli cex delivery order cancel [flags]
```

API: `DELETE /api/v4/delivery/{settle}/orders/{order_id}` (private).

Returns: [DeliveryOrder](models/delivery.md#model-deliveryorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `string` | Yes | Unset | Order ID (required) |

<a id="delivery.order.cancel-all"></a>
### `gate-cli cex delivery order cancel-all`

Operation ID: `delivery.order.cancel-all`. Effect: **write**.

Cancel all open delivery orders for a contract

```text
gate-cli cex delivery order cancel-all [flags]
```

API: `DELETE /api/v4/delivery/{settle}/orders` (private).

Returns: [][DeliveryOrder](models/delivery.md#model-deliveryorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Futures contract name (required) |
| `--side` | `string` | No | Unset | Filter by side: ask or bid |

<a id="delivery.order.create"></a>
### `gate-cli cex delivery order create`

Operation ID: `delivery.order.create`. Effect: **write**.

Create a delivery futures order

```text
gate-cli cex delivery order create [flags]
```

API: `POST /api/v4/delivery/{settle}/orders` (private).

Returns: [DeliveryOrder](models/delivery.md#model-deliveryorder).

API request model(s), assembled by the command: [DeliveryOrder](models/delivery.md#model-deliveryorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Futures contract name (required) |
| `--price` | `string` | No | Unset | Order price (0 for market order) |
| `--size` | `int64` | Yes | `0` | Order size, positive for buy, negative for sell (required) |
| `--tif` | `string` | No | Unset | Time in force: gtc, ioc, poc, fok |

<a id="delivery.order.get"></a>
### `gate-cli cex delivery order get`

Operation ID: `delivery.order.get`. Effect: **read**.

Get details of a delivery futures order

```text
gate-cli cex delivery order get [flags]
```

API: `GET /api/v4/delivery/{settle}/orders/{order_id}` (private).

Returns: [DeliveryOrder](models/delivery.md#model-deliveryorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `string` | Yes | Unset | Order ID (required) |

<a id="delivery.order.list"></a>
### `gate-cli cex delivery order list`

Operation ID: `delivery.order.list`. Effect: **read**.

List delivery futures orders

```text
gate-cli cex delivery order list [flags]
```

API: `GET /api/v4/delivery/{settle}/orders` (private).

Returns: [][DeliveryOrder](models/delivery.md#model-deliveryorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--offset` | `int32` | No | `0` | Number of records to skip |
| `--status` | `string` | Yes | `open` | Order status: open or finished (required) |

<a id="delivery.order.my-trades"></a>
### `gate-cli cex delivery order my-trades`

Operation ID: `delivery.order.my-trades`. Effect: **read**.

List personal delivery futures trading records

```text
gate-cli cex delivery order my-trades [flags]
```

API: `GET /api/v4/delivery/{settle}/my_trades` (private).

Returns: [][DeliveryMyTrade](models/delivery.md#model-deliverymytrade).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--limit` | `int32` | No | `0` | Number of records to return |

<a id="delivery.position.close"></a>
### `gate-cli cex delivery position close`

Operation ID: `delivery.position.close`. Effect: **read**.

List position close history

```text
gate-cli cex delivery position close [flags]
```

API: `GET /api/v4/delivery/{settle}/position_close` (private).

Returns: [][DeliveryPositionClose](models/delivery.md#model-deliverypositionclose).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--limit` | `int32` | No | `0` | Number of records to return |

<a id="delivery.position.get"></a>
### `gate-cli cex delivery position get`

Operation ID: `delivery.position.get`. Effect: **read**.

Get details of a delivery position

```text
gate-cli cex delivery position get [flags]
```

API: `GET /api/v4/delivery/{settle}/positions/{contract}` (private).

Returns: [DeliveryPosition](models/delivery.md#model-deliveryposition).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Futures contract name (required) |

<a id="delivery.position.liquidates"></a>
### `gate-cli cex delivery position liquidates`

Operation ID: `delivery.position.liquidates`. Effect: **read**.

List liquidation history

```text
gate-cli cex delivery position liquidates [flags]
```

API: `GET /api/v4/delivery/{settle}/liquidates` (private).

Returns: [][DeliveryLiquidate](models/delivery.md#model-deliveryliquidate).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--limit` | `int32` | No | `0` | Number of records to return |

<a id="delivery.position.list"></a>
### `gate-cli cex delivery position list`

Operation ID: `delivery.position.list`. Effect: **read**.

List all delivery positions

```text
gate-cli cex delivery position list
```

API: `GET /api/v4/delivery/{settle}/positions` (private).

Returns: [][DeliveryPosition](models/delivery.md#model-deliveryposition).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="delivery.position.settlements"></a>
### `gate-cli cex delivery position settlements`

Operation ID: `delivery.position.settlements`. Effect: **read**.

List settlement records

```text
gate-cli cex delivery position settlements [flags]
```

API: `GET /api/v4/delivery/{settle}/settlements` (private).

Returns: [][DeliverySettlement](models/delivery.md#model-deliverysettlement).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--limit` | `int32` | No | `0` | Number of records to return |

<a id="delivery.position.update-leverage"></a>
### `gate-cli cex delivery position update-leverage`

Operation ID: `delivery.position.update-leverage`. Effect: **write**.

Update delivery position leverage

```text
gate-cli cex delivery position update-leverage [flags]
```

API: `POST /api/v4/delivery/{settle}/positions/{contract}/leverage` (private).

Returns: [DeliveryPosition](models/delivery.md#model-deliveryposition).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Futures contract name (required) |
| `--leverage` | `string` | Yes | Unset | New leverage value (required) |

<a id="delivery.position.update-margin"></a>
### `gate-cli cex delivery position update-margin`

Operation ID: `delivery.position.update-margin`. Effect: **write**.

Update delivery position margin

```text
gate-cli cex delivery position update-margin [flags]
```

API: `POST /api/v4/delivery/{settle}/positions/{contract}/margin` (private).

Returns: [DeliveryPosition](models/delivery.md#model-deliveryposition).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--change` | `string` | Yes | Unset | Margin change amount (required) |
| `--contract` | `string` | Yes | Unset | Futures contract name (required) |

<a id="delivery.position.update-risk-limit"></a>
### `gate-cli cex delivery position update-risk-limit`

Operation ID: `delivery.position.update-risk-limit`. Effect: **write**.

Update delivery position risk limit

```text
gate-cli cex delivery position update-risk-limit [flags]
```

API: `POST /api/v4/delivery/{settle}/positions/{contract}/risk_limit` (private).

Returns: [DeliveryPosition](models/delivery.md#model-deliveryposition).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Futures contract name (required) |
| `--risk-limit` | `string` | Yes | Unset | New risk limit value (required) |

<a id="delivery.price-trigger.cancel"></a>
### `gate-cli cex delivery price-trigger cancel`

Operation ID: `delivery.price-trigger.cancel`. Effect: **write**.

Cancel a single price-triggered delivery order

```text
gate-cli cex delivery price-trigger cancel [flags]
```

API: `DELETE /api/v4/delivery/{settle}/price_orders/{order_id}` (private).

Returns: [FuturesPriceTriggeredOrder](models/delivery.md#model-futurespricetriggeredorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `string` | Yes | Unset | Order ID (required) |

<a id="delivery.price-trigger.cancel-all"></a>
### `gate-cli cex delivery price-trigger cancel-all`

Operation ID: `delivery.price-trigger.cancel-all`. Effect: **write**.

Cancel all price-triggered delivery orders for a contract

```text
gate-cli cex delivery price-trigger cancel-all [flags]
```

API: `DELETE /api/v4/delivery/{settle}/price_orders` (private).

Returns: [][FuturesPriceTriggeredOrder](models/delivery.md#model-futurespricetriggeredorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Futures contract name (required) |

<a id="delivery.price-trigger.create"></a>
### `gate-cli cex delivery price-trigger create`

Operation ID: `delivery.price-trigger.create`. Effect: **write**.

Create a price-triggered delivery order

```text
gate-cli cex delivery price-trigger create [flags]
```

API: `POST /api/v4/delivery/{settle}/price_orders` (private).

Returns: [TriggerOrderResponse](models/delivery.md#model-triggerorderresponse).

API request model(s), assembled by the command: [FuturesPriceTriggeredOrder](models/delivery.md#model-futurespricetriggeredorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Futures contract name (required) |
| `--order-price` | `string` | No | Unset | Order price (0 for market) |
| `--size` | `int64` | Yes | `0` | Order size (required) |
| `--trigger-price` | `string` | Yes | Unset | Trigger price (required) |

<a id="delivery.price-trigger.get"></a>
### `gate-cli cex delivery price-trigger get`

Operation ID: `delivery.price-trigger.get`. Effect: **read**.

Get details of a price-triggered delivery order

```text
gate-cli cex delivery price-trigger get [flags]
```

API: `GET /api/v4/delivery/{settle}/price_orders/{order_id}` (private).

Returns: [FuturesPriceTriggeredOrder](models/delivery.md#model-futurespricetriggeredorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `string` | Yes | Unset | Order ID (required) |

<a id="delivery.price-trigger.list"></a>
### `gate-cli cex delivery price-trigger list`

Operation ID: `delivery.price-trigger.list`. Effect: **read**.

List price-triggered delivery orders

```text
gate-cli cex delivery price-trigger list [flags]
```

API: `GET /api/v4/delivery/{settle}/price_orders` (private).

Returns: [][FuturesPriceTriggeredOrder](models/delivery.md#model-futurespricetriggeredorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--offset` | `int32` | No | `0` | Number of records to skip |
| `--status` | `string` | Yes | `open` | Order status: open or finished (required) |

## Verification and recovery

Use `delivery.order.get`, `delivery.position.get` and, at expiry, `delivery.position.settlements`. The relevant settlement read can lag order acceptance.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex delivery account book  --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex delivery order cancel --id <id> --format json
```

## Settlement limitation

The delivery handler fixes settlement to `usdt` (`cmd/cex/delivery/market.go:getSettle`); this command tree has no delivery `--settle` flag. Non-USDT delivery execution is unsupported by this skill contract, even if APIv4 supports it. Do not substitute perpetual commands.

## Close-history distinction

`delivery.position.close` reads closed-position history; it does not close a live position. Closing through an opposite signed order must use the real order contract and current position. This CLI does not expose every SDK reduce-only/close field; do not promise an atomic reduce-only/full-close behavior that the selected leaf cannot express. An explicitly requested offsetting order can create new exposure if state changes. Stop when the requested safety guarantee cannot be represented.
