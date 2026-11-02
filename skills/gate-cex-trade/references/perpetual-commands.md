# Perpetual futures

## Scope and source

Read the contract, settlement currency, signed contract quantity, multiplier, minimum size, risk tiers and position mode. USDT-settled and inverse contracts have different notional and PnL rules; never reuse a linear-contract conversion for an inverse contract. A margin budget is not order notional. Use exact contract quantities or obtain the missing interpretation before execution. Single and dual-side mode, reduce-only, close semantics and auto_size must match the selected command and position. Mode, leverage, margin and risk-limit changes are writes, not preflight. Inspect open orders and resulting positions after each write. Trailing and price-trigger orders are conditional orders, not TWAP. For native chase execution, use [algorithm actions](algo-commands.md#futures-chase-execution); do not reproduce its lifecycle here.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `futures.account.book` | `gate-cli cex futures account book` | read |
| `futures.account.dual-mode` | `gate-cli cex futures account dual-mode` | write |
| `futures.account.get` | `gate-cli cex futures account get` | read |
| `futures.account.position-mode` | `gate-cli cex futures account position-mode` | write |
| `futures.order.add` | `gate-cli cex futures order add` | write |
| `futures.order.amend` | `gate-cli cex futures order amend` | write |
| `futures.order.batch-amend` | `gate-cli cex futures order batch-amend` | write |
| `futures.order.batch-cancel` | `gate-cli cex futures order batch-cancel` | write |
| `futures.order.batch-create` | `gate-cli cex futures order batch-create` | write |
| `futures.order.bbo` | `gate-cli cex futures order bbo` | write |
| `futures.order.cancel` | `gate-cli cex futures order cancel` | write |
| `futures.order.close` | `gate-cli cex futures order close` | write |
| `futures.order.countdown-cancel-all` | `gate-cli cex futures order countdown-cancel-all` | write |
| `futures.order.get` | `gate-cli cex futures order get` | read |
| `futures.order.list` | `gate-cli cex futures order list` | read |
| `futures.order.list-timerange` | `gate-cli cex futures order list-timerange` | read |
| `futures.order.long` | `gate-cli cex futures order long` | write |
| `futures.order.my-trades` | `gate-cli cex futures order my-trades` | read |
| `futures.order.my-trades-timerange` | `gate-cli cex futures order my-trades-timerange` | read |
| `futures.order.remove` | `gate-cli cex futures order remove` | write |
| `futures.order.short` | `gate-cli cex futures order short` | write |
| `futures.position.adl` | `gate-cli cex futures position adl` | read |
| `futures.position.close-history` | `gate-cli cex futures position close-history` | read |
| `futures.position.get` | `gate-cli cex futures position get` | read |
| `futures.position.get-dual` | `gate-cli cex futures position get-dual` | read |
| `futures.position.leverage` | `gate-cli cex futures position leverage` | read |
| `futures.position.liquidates` | `gate-cli cex futures position liquidates` | read |
| `futures.position.list` | `gate-cli cex futures position list` | read |
| `futures.position.list-timerange` | `gate-cli cex futures position list-timerange` | read |
| `futures.position.update-contract-leverage` | `gate-cli cex futures position update-contract-leverage` | write |
| `futures.position.update-cross-mode` | `gate-cli cex futures position update-cross-mode` | write |
| `futures.position.update-dual-cross-mode` | `gate-cli cex futures position update-dual-cross-mode` | write |
| `futures.position.update-dual-leverage` | `gate-cli cex futures position update-dual-leverage` | write |
| `futures.position.update-dual-margin` | `gate-cli cex futures position update-dual-margin` | write |
| `futures.position.update-dual-risk-limit` | `gate-cli cex futures position update-dual-risk-limit` | write |
| `futures.position.update-leverage` | `gate-cli cex futures position update-leverage` | write |
| `futures.position.update-margin` | `gate-cli cex futures position update-margin` | write |
| `futures.position.update-risk-limit` | `gate-cli cex futures position update-risk-limit` | write |
| `futures.price-trigger.cancel` | `gate-cli cex futures price-trigger cancel` | write |
| `futures.price-trigger.cancel-all` | `gate-cli cex futures price-trigger cancel-all` | write |
| `futures.price-trigger.create` | `gate-cli cex futures price-trigger create` | write |
| `futures.price-trigger.get` | `gate-cli cex futures price-trigger get` | read |
| `futures.price-trigger.list` | `gate-cli cex futures price-trigger list` | read |
| `futures.price-trigger.update` | `gate-cli cex futures price-trigger update` | write |
| `futures.trail.create` | `gate-cli cex futures trail create` | write |
| `futures.trail.get` | `gate-cli cex futures trail get` | read |
| `futures.trail.list` | `gate-cli cex futures trail list` | read |
| `futures.trail.log` | `gate-cli cex futures trail log` | read |
| `futures.trail.stop` | `gate-cli cex futures trail stop` | write |
| `futures.trail.stop-all` | `gate-cli cex futures trail stop-all` | write |
| `futures.trail.update` | `gate-cli cex futures trail update` | write |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="futures.account.book"></a>
### `gate-cli cex futures account book`

Operation ID: `futures.account.book`. Effect: **read**.

List futures account change records

```text
gate-cli cex futures account book [flags]
```

API: `GET /api/v4/futures/{settle}/account_book` (private).

Returns: [][FuturesAccountBook](models/perpetual.md#model-futuresaccountbook).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--from` | `int64` | No | `0` | Start Unix timestamp |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--to` | `int64` | No | `0` | End Unix timestamp |

<a id="futures.account.dual-mode"></a>
### `gate-cli cex futures account dual-mode`

Operation ID: `futures.account.dual-mode`. Effect: **write**.

Enable or disable dual position mode

```text
gate-cli cex futures account dual-mode [flags]
```

API: `POST /api/v4/futures/{settle}/dual_mode` (private).

Returns: [FuturesAccount](models/perpetual.md#model-futuresaccount).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--enable` | `bool` | No | `false` | Enable dual mode (omit to disable) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.account.get"></a>
### `gate-cli cex futures account get`

Operation ID: `futures.account.get`. Effect: **read**.

Get futures account details

```text
gate-cli cex futures account get [flags]
```

API: `GET /api/v4/futures/{settle}/accounts` (private).

Returns: [FuturesAccount](models/perpetual.md#model-futuresaccount).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.account.position-mode"></a>
### `gate-cli cex futures account position-mode`

Operation ID: `futures.account.position-mode`. Effect: **write**.

Set position mode (classic or cross_margin)

```text
gate-cli cex futures account position-mode [flags]
```

API: `POST /api/v4/futures/{settle}/set_position_mode` (private).

Returns: [FuturesAccount](models/perpetual.md#model-futuresaccount).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--mode` | `string` | Yes | Unset | Position mode (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.order.add"></a>
### `gate-cli cex futures order add`

Operation ID: `futures.order.add`. Effect: **write**.

Add to existing position (same direction as current position)

```text
gate-cli cex futures order add [flags]
```

API: `POST /api/v4/futures/{settle}/orders` (private).

Returns: [FuturesOrder](models/perpetual.md#model-futuresorder).

API request model(s), assembled by the command: [FuturesOrder](models/perpetual.md#model-futuresorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name, e.g. BTC_USDT (required) |
| `--price` | `string` | No | Unset | Limit price (omit for market order) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--size` | `string` | Yes | Unset | Number of contracts (required) |

<a id="futures.order.amend"></a>
### `gate-cli cex futures order amend`

Operation ID: `futures.order.amend`. Effect: **write**.

Amend a futures order

```text
gate-cli cex futures order amend [flags]
```

API: `PUT /api/v4/futures/{settle}/orders/{order_id}` (private).

Returns: [FuturesOrder](models/perpetual.md#model-futuresorder).

API request model(s), assembled by the command: [FuturesOrderAmendment](models/perpetual.md#model-futuresorderamendment). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int64` | Yes | `0` | Order ID (required) |
| `--price` | `string` | No | Unset | New order price |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--size` | `string` | No | Unset | New order size (including filled) |

<a id="futures.order.batch-amend"></a>
### `gate-cli cex futures order batch-amend`

Operation ID: `futures.order.batch-amend`. Effect: **write**.

Batch amend futures orders

```text
gate-cli cex futures order batch-amend [flags]
```

API: `POST /api/v4/futures/{settle}/batch_amend_orders` (private).

Returns: [][BatchFuturesOrder](models/perpetual.md#model-batchfuturesorder).

API request model(s), assembled by the command: [][BatchAmendOrderReq](models/perpetual.md#model-batchamendorderreq). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--orders-json` | `string` | Yes | Unset | JSON array of BatchAmendOrderReq objects (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.order.batch-cancel"></a>
### `gate-cli cex futures order batch-cancel`

Operation ID: `futures.order.batch-cancel`. Effect: **write**.

Cancel futures orders by ID list

```text
gate-cli cex futures order batch-cancel [flags]
```

API: `POST /api/v4/futures/{settle}/batch_cancel_orders` (private).

Returns: [][FutureCancelOrderResult](models/perpetual.md#model-futurecancelorderresult).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--ids` | `stringSlice` | Yes | `[]` | Order IDs to cancel (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.order.batch-create"></a>
### `gate-cli cex futures order batch-create`

Operation ID: `futures.order.batch-create`. Effect: **write**.

Batch create futures orders (JSON array)

```text
gate-cli cex futures order batch-create [flags]
```

API: `POST /api/v4/futures/{settle}/batch_orders` (private).

Returns: [][BatchFuturesOrder](models/perpetual.md#model-batchfuturesorder).

API request model(s), assembled by the command: [][FuturesOrder](models/perpetual.md#model-futuresorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--orders-json` | `string` | Yes | Unset | JSON array of FuturesOrder objects (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.order.bbo"></a>
### `gate-cli cex futures order bbo`

Operation ID: `futures.order.bbo`. Effect: **write**.

Create a best bid/offer (BBO) futures order

```text
gate-cli cex futures order bbo [flags]
```

API: `POST /api/v4/futures/{settle}/bbo_orders` (private).

Returns: [FuturesOrder](models/perpetual.md#model-futuresorder).

API request model(s), assembled by the command: [FuturesBboOrder](models/perpetual.md#model-futuresbboorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--direction` | `string` | Yes | Unset | Direction: buy or sell (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--size` | `int64` | Yes | `0` | Number of contracts, positive=buy, negative=sell (required) |

<a id="futures.order.cancel"></a>
### `gate-cli cex futures order cancel`

Operation ID: `futures.order.cancel`. Effect: **write**.

Cancel one order (--id) or all open orders (--all --contract)

```text
gate-cli cex futures order cancel [flags]
```

API: `DELETE /api/v4/futures/{settle}/orders/{order_id}` (private); `DELETE /api/v4/futures/{settle}/orders` (private).

Returns: [FuturesOrder](models/perpetual.md#model-futuresorder) or [][FuturesOrder](models/perpetual.md#model-futuresorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--all` | `bool` | No | `false` | Cancel all open orders for the contract |
| `--contract` | `string` | No | Unset | Contract name (required with --all) |
| `--id` | `int64` | No | `0` | Order ID to cancel |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.order.close"></a>
### `gate-cli cex futures order close`

Operation ID: `futures.order.close`. Effect: **write**.

Close position (full close by default, partial close with --size)

```text
gate-cli cex futures order close [flags]
```

API: `POST /api/v4/futures/{settle}/orders` (private).

Returns: [FuturesOrder](models/perpetual.md#model-futuresorder).

API request model(s), assembled by the command: [FuturesOrder](models/perpetual.md#model-futuresorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name, e.g. BTC_USDT (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--side` | `string` | No | `long` | Position side to close: long or short (relevant in dual-position mode) |
| `--size` | `string` | No | `0` | Partial close size (default 0 = full close) |

<a id="futures.order.countdown-cancel-all"></a>
### `gate-cli cex futures order countdown-cancel-all`

Operation ID: `futures.order.countdown-cancel-all`. Effect: **write**.

Set countdown to cancel all futures orders

```text
gate-cli cex futures order countdown-cancel-all [flags]
```

API: `POST /api/v4/futures/{settle}/countdown_cancel_all` (private).

Returns: [TriggerTime](models/perpetual.md#model-triggertime).

API request model(s), assembled by the command: [CountdownCancelAllFuturesTask](models/perpetual.md#model-countdowncancelallfuturestask). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Limit cancellation to this contract |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--timeout` | `int32` | Yes | `0` | Countdown in seconds (0 = cancel countdown, min 5) (required) |

<a id="futures.order.get"></a>
### `gate-cli cex futures order get`

Operation ID: `futures.order.get`. Effect: **read**.

Get a futures order by ID

```text
gate-cli cex futures order get [flags]
```

API: `GET /api/v4/futures/{settle}/orders/{order_id}` (private).

Returns: [FuturesOrder](models/perpetual.md#model-futuresorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int64` | Yes | `0` | Order ID (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.order.list"></a>
### `gate-cli cex futures order list`

Operation ID: `futures.order.list`. Effect: **read**.

List futures orders

```text
gate-cli cex futures order list [flags]
```

API: `GET /api/v4/futures/{settle}/orders` (private).

Returns: [][FuturesOrder](models/perpetual.md#model-futuresorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--limit` | `int32` | No | `20` | Number of orders to return |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--status` | `string` | No | `open` | Order status: open, finished |

<a id="futures.order.list-timerange"></a>
### `gate-cli cex futures order list-timerange`

Operation ID: `futures.order.list-timerange`. Effect: **read**.

List futures orders by time range

```text
gate-cli cex futures order list-timerange [flags]
```

API: `GET /api/v4/futures/{settle}/orders_timerange` (private).

Returns: [][FuturesOrderTimerange](models/perpetual.md#model-futuresordertimerange).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--from` | `int64` | No | `0` | Start Unix timestamp |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--to` | `int64` | No | `0` | End Unix timestamp |

<a id="futures.order.long"></a>
### `gate-cli cex futures order long`

Operation ID: `futures.order.long`. Effect: **write**.

Open or add to a long position (positive size)

```text
gate-cli cex futures order long [flags]
```

API: `POST /api/v4/futures/{settle}/orders` (private).

Returns: [FuturesOrder](models/perpetual.md#model-futuresorder).

API request model(s), assembled by the command: [FuturesOrder](models/perpetual.md#model-futuresorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name, e.g. BTC_USDT (required) |
| `--price` | `string` | No | Unset | Limit price (omit for market order) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--size` | `string` | Yes | Unset | Number of contracts (required) |

<a id="futures.order.my-trades"></a>
### `gate-cli cex futures order my-trades`

Operation ID: `futures.order.my-trades`. Effect: **read**.

List personal futures trade history

```text
gate-cli cex futures order my-trades [flags]
```

API: `GET /api/v4/futures/{settle}/my_trades` (private).

Returns: [][MyFuturesTrade](models/perpetual.md#model-myfuturestrade).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.order.my-trades-timerange"></a>
### `gate-cli cex futures order my-trades-timerange`

Operation ID: `futures.order.my-trades-timerange`. Effect: **read**.

List personal futures trade history by time range

```text
gate-cli cex futures order my-trades-timerange [flags]
```

API: `GET /api/v4/futures/{settle}/my_trades_timerange` (private).

Returns: [][MyFuturesTradeTimeRange](models/perpetual.md#model-myfuturestradetimerange).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--from` | `int64` | No | `0` | Start Unix timestamp |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--to` | `int64` | No | `0` | End Unix timestamp |

<a id="futures.order.remove"></a>
### `gate-cli cex futures order remove`

Operation ID: `futures.order.remove`. Effect: **write**.

Reduce existing position (opposite direction)

```text
gate-cli cex futures order remove [flags]
```

API: `POST /api/v4/futures/{settle}/orders` (private).

Returns: [FuturesOrder](models/perpetual.md#model-futuresorder).

API request model(s), assembled by the command: [FuturesOrder](models/perpetual.md#model-futuresorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name, e.g. BTC_USDT (required) |
| `--price` | `string` | No | Unset | Limit price (omit for market order) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--size` | `string` | Yes | Unset | Number of contracts (required) |

<a id="futures.order.short"></a>
### `gate-cli cex futures order short`

Operation ID: `futures.order.short`. Effect: **write**.

Open or add to a short position (negative size)

```text
gate-cli cex futures order short [flags]
```

API: `POST /api/v4/futures/{settle}/orders` (private).

Returns: [FuturesOrder](models/perpetual.md#model-futuresorder).

API request model(s), assembled by the command: [FuturesOrder](models/perpetual.md#model-futuresorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name, e.g. BTC_USDT (required) |
| `--price` | `string` | No | Unset | Limit price (omit for market order) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--size` | `string` | Yes | Unset | Number of contracts (required) |

<a id="futures.position.adl"></a>
### `gate-cli cex futures position adl`

Operation ID: `futures.position.adl`. Effect: **read**.

List auto-deleveraging history

```text
gate-cli cex futures position adl [flags]
```

API: `GET /api/v4/futures/{settle}/auto_deleverages` (private).

Returns: [][FuturesAutoDeleverage](models/perpetual.md#model-futuresautodeleverage).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.position.close-history"></a>
### `gate-cli cex futures position close-history`

Operation ID: `futures.position.close-history`. Effect: **read**.

List position close history

```text
gate-cli cex futures position close-history [flags]
```

API: `GET /api/v4/futures/{settle}/position_close` (private).

Returns: [][PositionClose](models/perpetual.md#model-positionclose).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--from` | `int64` | No | `0` | Start Unix timestamp |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--to` | `int64` | No | `0` | End Unix timestamp |

<a id="futures.position.get"></a>
### `gate-cli cex futures position get`

Operation ID: `futures.position.get`. Effect: **read**.

Get one-way (single-mode) position for a contract

```text
gate-cli cex futures position get [flags]
```

API: `GET /api/v4/futures/{settle}/positions/{contract}` (private).

Returns: [Position](models/perpetual.md#model-position).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name, e.g. BTC_USDT (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.position.get-dual"></a>
### `gate-cli cex futures position get-dual`

Operation ID: `futures.position.get-dual`. Effect: **read**.

Get dual-mode (hedge) position(s) for a contract

```text
gate-cli cex futures position get-dual [flags]
```

API: `GET /api/v4/futures/{settle}/dual_comp/positions/{contract}` (private).

Returns: [][Position](models/perpetual.md#model-position) or [Position](models/perpetual.md#model-position).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name, e.g. BTC_USDT (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.position.leverage"></a>
### `gate-cli cex futures position leverage`

Operation ID: `futures.position.leverage`. Effect: **read**.

Get leverage settings for a contract

```text
gate-cli cex futures position leverage [flags]
```

API: `GET /api/v4/futures/{settle}/get_leverage/{contract}` (private).

Returns: [FuturesLeverage](models/perpetual.md#model-futuresleverage).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--dual-side` | `string` | Conditional | Unset | Dual side: long, short (required for dual-position mode) |
| `--pos-margin-mode` | `string` | Conditional | Unset | Position margin mode: isolated, cross (required for split position mode) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.position.liquidates"></a>
### `gate-cli cex futures position liquidates`

Operation ID: `futures.position.liquidates`. Effect: **read**.

List personal liquidation history

```text
gate-cli cex futures position liquidates [flags]
```

API: `GET /api/v4/futures/{settle}/liquidates` (private).

Returns: [][FuturesLiquidate](models/perpetual.md#model-futuresliquidate).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.position.list"></a>
### `gate-cli cex futures position list`

Operation ID: `futures.position.list`. Effect: **read**.

List all open futures positions

```text
gate-cli cex futures position list [flags]
```

API: `GET /api/v4/futures/{settle}/positions` (private).

Returns: [][Position](models/perpetual.md#model-position).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.position.list-timerange"></a>
### `gate-cli cex futures position list-timerange`

Operation ID: `futures.position.list-timerange`. Effect: **read**.

List position history by time range

```text
gate-cli cex futures position list-timerange [flags]
```

API: `GET /api/v4/futures/{settle}/positions_timerange` (private).

Returns: [][PositionTimerange](models/perpetual.md#model-positiontimerange).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--from` | `int64` | No | `0` | Start Unix timestamp |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--to` | `int64` | No | `0` | End Unix timestamp |

<a id="futures.position.update-contract-leverage"></a>
### `gate-cli cex futures position update-contract-leverage`

Operation ID: `futures.position.update-contract-leverage`. Effect: **write**.

Update leverage for specified mode

```text
gate-cli cex futures position update-contract-leverage [flags]
```

API: `POST /api/v4/futures/{settle}/positions/{contract}/set_leverage` (private).

Returns: [Position](models/perpetual.md#model-position).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--leverage` | `string` | Yes | Unset | New leverage (required) |
| `--margin-mode` | `string` | Yes | Unset | Margin mode: isolated or cross (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.position.update-cross-mode"></a>
### `gate-cli cex futures position update-cross-mode`

Operation ID: `futures.position.update-cross-mode`. Effect: **write**.

Update one-way (single-mode) position cross/isolated margin mode

```text
gate-cli cex futures position update-cross-mode [flags]
```

API: `POST /api/v4/futures/{settle}/positions/cross_mode` (private).

Returns: [Position](models/perpetual.md#model-position).

API request model(s), assembled by the command: [FuturesPositionCrossMode](models/perpetual.md#model-futurespositioncrossmode). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--mode` | `string` | Yes | Unset | Margin mode: ISOLATED or CROSS (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.position.update-dual-cross-mode"></a>
### `gate-cli cex futures position update-dual-cross-mode`

Operation ID: `futures.position.update-dual-cross-mode`. Effect: **write**.

Update dual-mode (hedge) position cross/isolated margin mode

```text
gate-cli cex futures position update-dual-cross-mode [flags]
```

API: `POST /api/v4/futures/{settle}/dual_comp/positions/cross_mode` (private).

Returns: [][Position](models/perpetual.md#model-position).

API request model(s), assembled by the command: [UpdateDualCompPositionCrossModeRequest](models/perpetual.md#model-updatedualcomppositioncrossmoderequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--mode` | `string` | Yes | Unset | Margin mode: ISOLATED or CROSS (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.position.update-dual-leverage"></a>
### `gate-cli cex futures position update-dual-leverage`

Operation ID: `futures.position.update-dual-leverage`. Effect: **write**.

Update dual-mode (hedge) position leverage

```text
gate-cli cex futures position update-dual-leverage [flags]
```

API: `POST /api/v4/futures/{settle}/dual_comp/positions/{contract}/leverage` (private).

Returns: [][Position](models/perpetual.md#model-position).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--leverage` | `string` | Yes | Unset | New leverage (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.position.update-dual-margin"></a>
### `gate-cli cex futures position update-dual-margin`

Operation ID: `futures.position.update-dual-margin`. Effect: **write**.

Update dual-mode (hedge) position margin

```text
gate-cli cex futures position update-dual-margin [flags]
```

API: `POST /api/v4/futures/{settle}/dual_comp/positions/{contract}/margin` (private).

Returns: [][Position](models/perpetual.md#model-position).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--change` | `string` | Yes | Unset | Margin change amount (required) |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--dual-side` | `string` | Conditional | Unset | Required in dual-position mode: dual_long or dual_short; mode-query failure stops the write |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.position.update-dual-risk-limit"></a>
### `gate-cli cex futures position update-dual-risk-limit`

Operation ID: `futures.position.update-dual-risk-limit`. Effect: **write**.

Update dual-mode (hedge) position risk limit

```text
gate-cli cex futures position update-dual-risk-limit [flags]
```

API: `POST /api/v4/futures/{settle}/dual_comp/positions/{contract}/risk_limit` (private).

Returns: [][Position](models/perpetual.md#model-position).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--risk-limit` | `string` | Yes | Unset | New risk limit (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.position.update-leverage"></a>
### `gate-cli cex futures position update-leverage`

Operation ID: `futures.position.update-leverage`. Effect: **write**.

Update one-way (single-mode) position leverage

```text
gate-cli cex futures position update-leverage [flags]
```

API: `POST /api/v4/futures/{settle}/positions/{contract}/leverage` (private).

Returns: [Position](models/perpetual.md#model-position).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--cross-leverage-limit` | `string` | No | Unset | Cross margin leverage limit (cross mode only) |
| `--leverage` | `string` | Yes | Unset | New leverage (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.position.update-margin"></a>
### `gate-cli cex futures position update-margin`

Operation ID: `futures.position.update-margin`. Effect: **write**.

Update one-way (single-mode) position margin

```text
gate-cli cex futures position update-margin [flags]
```

API: `POST /api/v4/futures/{settle}/positions/{contract}/margin` (private).

Returns: [Position](models/perpetual.md#model-position).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--change` | `string` | Yes | Unset | Margin change amount (required) |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.position.update-risk-limit"></a>
### `gate-cli cex futures position update-risk-limit`

Operation ID: `futures.position.update-risk-limit`. Effect: **write**.

Update one-way (single-mode) position risk limit

```text
gate-cli cex futures position update-risk-limit [flags]
```

API: `POST /api/v4/futures/{settle}/positions/{contract}/risk_limit` (private).

Returns: [Position](models/perpetual.md#model-position).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--risk-limit` | `string` | Yes | Unset | New risk limit (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.price-trigger.cancel"></a>
### `gate-cli cex futures price-trigger cancel`

Operation ID: `futures.price-trigger.cancel`. Effect: **write**.

Cancel a price-triggered order by ID

```text
gate-cli cex futures price-trigger cancel [flags]
```

API: `DELETE /api/v4/futures/{settle}/price_orders/{order_id}` (private).

Returns: [FuturesPriceTriggeredOrder](models/perpetual.md#model-futurespricetriggeredorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int64` | Yes | `0` | Order ID (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.price-trigger.cancel-all"></a>
### `gate-cli cex futures price-trigger cancel-all`

Operation ID: `futures.price-trigger.cancel-all`. Effect: **write**.

Cancel all price-triggered orders

```text
gate-cli cex futures price-trigger cancel-all [flags]
```

API: `DELETE /api/v4/futures/{settle}/price_orders` (private).

Returns: [][FuturesPriceTriggeredOrder](models/perpetual.md#model-futurespricetriggeredorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Limit cancellation to this contract |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.price-trigger.create"></a>
### `gate-cli cex futures price-trigger create`

Operation ID: `futures.price-trigger.create`. Effect: **write**.

Create a price-triggered order

```text
gate-cli cex futures price-trigger create [flags]
```

API: `POST /api/v4/futures/{settle}/price_orders` (private).

Returns: [TriggerOrderResponse](models/perpetual.md#model-triggerorderresponse).

API request model(s), assembled by the command: [FuturesPriceTriggeredOrder](models/perpetual.md#model-futurespricetriggeredorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--price` | `string` | Yes | Unset | Order price (0 for market) (required) |
| `--price-type` | `int32` | No | `0` | Reference price type: 0=latest, 1=mark, 2=index |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--size` | `int64` | No | `0` | Signed contract size; explicitly set a nonzero size for supported conditional entry orders. Zero alone does not establish full-close semantics. |
| `--trigger-price` | `string` | Yes | Unset | Trigger price (required) |
| `--trigger-rule` | `int32` | No | `1` | Trigger condition: 1=>=, 2=<= |

<a id="futures.price-trigger.get"></a>
### `gate-cli cex futures price-trigger get`

Operation ID: `futures.price-trigger.get`. Effect: **read**.

Get a price-triggered order by ID

```text
gate-cli cex futures price-trigger get [flags]
```

API: `GET /api/v4/futures/{settle}/price_orders/{order_id}` (private).

Returns: [FuturesPriceTriggeredOrder](models/perpetual.md#model-futurespricetriggeredorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int64` | Yes | `0` | Order ID (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.price-trigger.list"></a>
### `gate-cli cex futures price-trigger list`

Operation ID: `futures.price-trigger.list`. Effect: **read**.

List price-triggered orders

```text
gate-cli cex futures price-trigger list [flags]
```

API: `GET /api/v4/futures/{settle}/price_orders` (private).

Returns: [][FuturesPriceTriggeredOrder](models/perpetual.md#model-futurespricetriggeredorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--offset` | `int32` | No | `0` | Records to skip |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--status` | `string` | No | `open` | Order status: open, finished |

<a id="futures.price-trigger.update"></a>
### `gate-cli cex futures price-trigger update`

Operation ID: `futures.price-trigger.update`. Effect: **write**.

Update a price-triggered order

```text
gate-cli cex futures price-trigger update [flags]
```

API: `PUT /api/v4/futures/{settle}/price_orders/amend/{order_id}` (private).

Returns: [TriggerOrderResponse](models/perpetual.md#model-triggerorderresponse).

API request model(s), assembled by the command: [FuturesUpdatePriceTriggeredOrder](models/perpetual.md#model-futuresupdatepricetriggeredorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--body-order-id` | `int64` | Yes | `0` | Body trigger order ID (required) |
| `--id` | `string` | Yes | Unset | Path order ID (required) |
| `--price` | `string` | No | Unset | New order price |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--size` | `int64` | No | `0` | New order size |
| `--trigger-price` | `string` | No | Unset | New trigger price |

<a id="futures.trail.create"></a>
### `gate-cli cex futures trail create`

Operation ID: `futures.trail.create`. Effect: **write**.

Create a trailing stop order

```text
gate-cli cex futures trail create [flags]
```

API: `POST /api/v4/futures/{settle}/autoorder/v1/trail/create` (private).

Returns: [CreateTrailOrderResponse](models/perpetual.md#model-createtrailorderresponse).

API request model(s), assembled by the command: [CreateTrailOrder](models/perpetual.md#model-createtrailorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--activation-price` | `string` | No | `0` | Activation price (0 = trigger immediately) |
| `--amount` | `string` | Yes | Unset | Trading quantity in contracts, positive=buy, negative=sell (required) |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--price-offset` | `string` | Yes | Unset | Callback ratio or price distance, e.g. 0.1 or 0.1% (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.trail.get"></a>
### `gate-cli cex futures trail get`

Operation ID: `futures.trail.get`. Effect: **read**.

Get a trailing stop order by ID

```text
gate-cli cex futures trail get [flags]
```

API: `GET /api/v4/futures/{settle}/autoorder/v1/trail/detail` (private).

Returns: [TrailOrderDetailResponse](models/perpetual.md#model-trailorderdetailresponse).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int64` | Yes | `0` | Order ID (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.trail.list"></a>
### `gate-cli cex futures trail list`

Operation ID: `futures.trail.list`. Effect: **read**.

List trailing stop orders

```text
gate-cli cex futures trail list [flags]
```

API: `GET /api/v4/futures/{settle}/autoorder/v1/trail/list` (private).

Returns: [TrailOrderListResponse](models/perpetual.md#model-trailorderlistresponse).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--finished` | `bool` | No | `false` | Show finished orders (default: active) |
| `--limit` | `int32` | No | `0` | Number of records per page |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.trail.log"></a>
### `gate-cli cex futures trail log`

Operation ID: `futures.trail.log`. Effect: **read**.

Get change log of a trailing stop order

```text
gate-cli cex futures trail log [flags]
```

API: `GET /api/v4/futures/{settle}/autoorder/v1/trail/change_log` (private).

Returns: [TrailOrderChangeLogResponse](models/perpetual.md#model-trailorderchangelogresponse).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int64` | Yes | `0` | Order ID (required) |
| `--limit` | `int32` | No | `0` | Number of records per page |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.trail.stop"></a>
### `gate-cli cex futures trail stop`

Operation ID: `futures.trail.stop`. Effect: **write**.

Stop a trailing stop order by ID or text

```text
gate-cli cex futures trail stop [flags]
```

API: `POST /api/v4/futures/{settle}/autoorder/v1/trail/stop` (private).

Returns: [TrailOrderResponse](models/perpetual.md#model-trailorderresponse).

API request model(s), assembled by the command: [StopTrailOrder](models/perpetual.md#model-stoptrailorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int64` | No | `0` | Order ID |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--text` | `string` | No | Unset | Custom text (used if ID not provided) |

<a id="futures.trail.stop-all"></a>
### `gate-cli cex futures trail stop-all`

Operation ID: `futures.trail.stop-all`. Effect: **write**.

Stop all trailing stop orders for a contract

```text
gate-cli cex futures trail stop-all [flags]
```

API: `POST /api/v4/futures/{settle}/autoorder/v1/trail/stop_all` (private).

Returns: [TrailOrderListResponse](models/perpetual.md#model-trailorderlistresponse).

API request model(s), assembled by the command: [StopAllTrailOrders](models/perpetual.md#model-stopalltrailorders). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Limit to this contract |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.trail.update"></a>
### `gate-cli cex futures trail update`

Operation ID: `futures.trail.update`. Effect: **write**.

Update a trailing stop order

```text
gate-cli cex futures trail update [flags]
```

API: `POST /api/v4/futures/{settle}/autoorder/v1/trail/update` (private).

Returns: [TrailOrderResponse](models/perpetual.md#model-trailorderresponse).

API request model(s), assembled by the command: [UpdateTrailOrder](models/perpetual.md#model-updatetrailorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--activation-price` | `string` | No | Unset | New activation price |
| `--amount` | `string` | No | Unset | New amount |
| `--id` | `int64` | Yes | `0` | Order ID (required) |
| `--price-offset` | `string` | No | Unset | New callback ratio or price distance |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

## Verification and recovery

Use `futures.order.get` for an order ID, `futures.position.get` or `futures.position.get-dual` for the selected mode, and `futures.price-trigger.get`/trail reads for protection objects. Check remaining position and active protection independently.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex futures account book  --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex futures account dual-mode  --format json
```

## Price-trigger protection limitation

`futures.price-trigger.create` constructs only initial contract/size/price and trigger fields. It does not expose initial `close`, `auto_size`, `reduce_only` or `tif`, although the SDK model defines them. A full close requires additional single/dual-mode fields; market execution needs compatible time-in-force. Do not use this leaf to promise a full-close, reduce-only TP/SL or market-trigger protection. Do not copy SDK-only fields into invented flags. A nonzero-size limit conditional entry still requires explicit signed size and authority, and can open exposure. Preserve an existing protection when the requested replacement cannot be expressed safely.
