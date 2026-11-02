# Spot trading

## Scope and source

Use base quantities for sells and limit buys. A market buy spends quote currency through --quote. Omit --price for market orders; a limit buy needs --amount and --price. Do not invent a --type flag. Read the pair trading status, precision, minimum/maximum amount and notional limits, then the effective account balance. A market quote budget does not guarantee the received base quantity. Cancel requires exactly one of --id or --all. Preserve the order account type; do not borrow or transfer implicitly. Attached protection below does not establish native OCO/OTO/OTOCO/OPO/OPOCO guarantees. For participation-of-volume execution, use [POV actions](algo-commands.md#spot-pov-execution).

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `spot.account.book` | `gate-cli cex spot account book` | read |
| `spot.account.get` | `gate-cli cex spot account get` | read |
| `spot.account.list` | `gate-cli cex spot account list` | read |
| `spot.order.all-open` | `gate-cli cex spot order all-open` | read |
| `spot.order.amend` | `gate-cli cex spot order amend` | write |
| `spot.order.batch-amend` | `gate-cli cex spot order batch-amend` | write |
| `spot.order.batch-cancel` | `gate-cli cex spot order batch-cancel` | write |
| `spot.order.batch-create` | `gate-cli cex spot order batch-create` | write |
| `spot.order.buy` | `gate-cli cex spot order buy` | write |
| `spot.order.cancel` | `gate-cli cex spot order cancel` | write |
| `spot.order.countdown-cancel-all` | `gate-cli cex spot order countdown-cancel-all` | write |
| `spot.order.get` | `gate-cli cex spot order get` | read |
| `spot.order.list` | `gate-cli cex spot order list` | read |
| `spot.order.my-trades` | `gate-cli cex spot order my-trades` | read |
| `spot.order.sell` | `gate-cli cex spot order sell` | write |
| `spot.price-trigger.cancel` | `gate-cli cex spot price-trigger cancel` | write |
| `spot.price-trigger.cancel-all` | `gate-cli cex spot price-trigger cancel-all` | write |
| `spot.price-trigger.create` | `gate-cli cex spot price-trigger create` | write |
| `spot.price-trigger.get` | `gate-cli cex spot price-trigger get` | read |
| `spot.price-trigger.list` | `gate-cli cex spot price-trigger list` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="spot.account.book"></a>
### `gate-cli cex spot account book`

Operation ID: `spot.account.book`. Effect: **read**.

List spot account transaction history

```text
gate-cli cex spot account book [flags]
```

API: `GET /api/v4/spot/account_book` (private).

Returns: [][SpotAccountBook](models/spot.md#model-spotaccountbook).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency name |
| `--from` | `int64` | No | `0` | Start Unix timestamp (ms) |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--to` | `int64` | No | `0` | End Unix timestamp (ms) |

<a id="spot.account.get"></a>
### `gate-cli cex spot account get`

Operation ID: `spot.account.get`. Effect: **read**.

Get balance for a specific currency

```text
gate-cli cex spot account get [flags]
```

API: `GET /api/v4/spot/accounts` (private).

Returns: [][SpotAccount](models/spot.md#model-spotaccount).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | Yes | Unset | Currency symbol, e.g. BTC (required) |

<a id="spot.account.list"></a>
### `gate-cli cex spot account list`

Operation ID: `spot.account.list`. Effect: **read**.

List all spot account balances (non-zero by default)

```text
gate-cli cex spot account list [flags]
```

API: `GET /api/v4/spot/accounts` (private).

Returns: [][SpotAccount](models/spot.md#model-spotaccount).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--all` | `bool` | No | `false` | Show all currencies including zero balances |

<a id="spot.order.all-open"></a>
### `gate-cli cex spot order all-open`

Operation ID: `spot.order.all-open`. Effect: **read**.

List all open orders across all currency pairs

```text
gate-cli cex spot order all-open [flags]
```

API: `GET /api/v4/spot/open_orders` (private).

Returns: [][OpenOrders](models/spot.md#model-openorders).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--account` | `string` | No | Unset | Order account: spot, margin, unified or cross_margin; omitted uses server defaults |
| `--limit` | `int32` | No | `0` | Number of records per page |

<a id="spot.order.amend"></a>
### `gate-cli cex spot order amend`

Operation ID: `spot.order.amend`. Effect: **write**.

Amend an order (change amount or price)

```text
gate-cli cex spot order amend [flags]
```

API: `PATCH /api/v4/spot/orders/{order_id}` (private).

Returns: [Order](models/spot.md#model-order).

API request model(s), assembled by the command: [OrderPatch](models/spot.md#model-orderpatch). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--account` | `string` | No | Unset | Order account: spot, margin, unified or cross_margin; omitted uses server defaults |
| `--amount` | `string` | No | Unset | New amount |
| `--id` | `string` | Yes | Unset | Order ID (required) |
| `--pair` | `string` | Yes | Unset | Currency pair (required) |
| `--price` | `string` | No | Unset | New price |
| `--stop-loss-json` | `string` | No | Unset | Stop loss: {trigger_price,order_price}; on amend {} cancels, null/omitted keeps unchanged |
| `--stop-profit-json` | `string` | No | Unset | Take profit: {trigger_price,order_price}; on amend {} cancels, null/omitted keeps unchanged |

<a id="spot.order.batch-amend"></a>
### `gate-cli cex spot order batch-amend`

Operation ID: `spot.order.batch-amend`. Effect: **write**.

Batch amend orders

```text
gate-cli cex spot order batch-amend [flags]
```

API: `POST /api/v4/spot/amend_batch_orders` (private).

Returns: [][BatchOrder](models/spot.md#model-batchorder).

API request model(s), assembled by the command: [][BatchAmendItem](models/spot.md#model-batchamenditem). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--orders-json` | `string` | Yes | Unset | JSON array of BatchAmendItem objects (required) |

<a id="spot.order.batch-cancel"></a>
### `gate-cli cex spot order batch-cancel`

Operation ID: `spot.order.batch-cancel`. Effect: **write**.

Cancel orders by ID list

```text
gate-cli cex spot order batch-cancel [flags]
```

API: `POST /api/v4/spot/cancel_batch_orders` (private).

Returns: [][CancelOrderResult](models/spot.md#model-cancelorderresult).

API request model(s), assembled by the command: [][CancelBatchOrder](models/spot.md#model-cancelbatchorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--orders-json` | `string` | Yes | Unset | JSON array of {currency_pair, id} objects (required) |

<a id="spot.order.batch-create"></a>
### `gate-cli cex spot order batch-create`

Operation ID: `spot.order.batch-create`. Effect: **write**.

Batch place orders (JSON array of orders)

```text
gate-cli cex spot order batch-create [flags]
```

API: `POST /api/v4/spot/batch_orders` (private).

Returns: [][BatchOrder](models/spot.md#model-batchorder).

API request model(s), assembled by the command: [][Order](models/spot.md#model-order). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--orders-json` | `string` | Yes | Unset | JSON array of orders (required) |

<a id="spot.order.buy"></a>
### `gate-cli cex spot order buy`

Operation ID: `spot.order.buy`. Effect: **write**.

Place a buy order (--price for limit; --quote for market)

```text
gate-cli cex spot order buy [flags]
```

API: `POST /api/v4/spot/orders` (private).

Returns: [Order](models/spot.md#model-order).

API request model(s), assembled by the command: [Order](models/spot.md#model-order). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--account` | `string` | No | Unset | Order account: spot, margin, unified or cross_margin; omitted uses server defaults |
| `--amount` | `string` | Conditional | Unset | Amount of base currency to buy (required for limit orders) |
| `--auto-borrow` | `bool` | No | `false` | Borrow a shortfall automatically (margin, unified or cross_margin only) |
| `--auto-repay` | `bool` | No | `false` | Repay automatically for this order (unified or cross_margin only) |
| `--pair` | `string` | Yes | Unset | Currency pair, e.g. BTC_USDT (required) |
| `--price` | `string` | No | Unset | Limit price (omit for market order) |
| `--quote` | `string` | No | Unset | Amount of quote currency to spend (market buy only; e.g. --quote 10 to spend 10 USDT) |
| `--stop-loss-json` | `string` | No | Unset | Stop loss: {trigger_price,order_price}; on amend {} cancels, null/omitted keeps unchanged |
| `--stop-profit-json` | `string` | No | Unset | Take profit: {trigger_price,order_price}; on amend {} cancels, null/omitted keeps unchanged |

<a id="spot.order.cancel"></a>
### `gate-cli cex spot order cancel`

Operation ID: `spot.order.cancel`. Effect: **write**.

Cancel one order (--id) or all open orders (--all)

```text
gate-cli cex spot order cancel [flags]
```

API: `DELETE /api/v4/spot/orders/{order_id}` (private); `DELETE /api/v4/spot/orders` (private).

Returns: [Order](models/spot.md#model-order) or [][OrderCancel](models/spot.md#model-ordercancel).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--account` | `string` | No | Unset | Order account: spot, margin, unified or cross_margin; omitted uses server defaults |
| `--all` | `bool` | No | `false` | Cancel all open orders for the pair |
| `--id` | `string` | No | Unset | Order ID to cancel |
| `--pair` | `string` | Yes | Unset | Currency pair (required) |

<a id="spot.order.countdown-cancel-all"></a>
### `gate-cli cex spot order countdown-cancel-all`

Operation ID: `spot.order.countdown-cancel-all`. Effect: **write**.

Set countdown to cancel all spot orders

```text
gate-cli cex spot order countdown-cancel-all [flags]
```

API: `POST /api/v4/spot/countdown_cancel_all` (private).

Returns: [TriggerTime](models/spot.md#model-triggertime).

API request model(s), assembled by the command: [CountdownCancelAllSpotTask](models/spot.md#model-countdowncancelallspottask). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--pair` | `string` | No | Unset | Limit cancellation to this currency pair |
| `--timeout` | `int32` | Yes | `0` | Countdown in seconds (0 = cancel countdown, min 5) (required) |

<a id="spot.order.get"></a>
### `gate-cli cex spot order get`

Operation ID: `spot.order.get`. Effect: **read**.

Get an order by ID

```text
gate-cli cex spot order get [flags]
```

API: `GET /api/v4/spot/orders/{order_id}` (private).

Returns: [Order](models/spot.md#model-order).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--account` | `string` | No | Unset | Order account: spot, margin, unified or cross_margin; omitted uses server defaults |
| `--id` | `string` | Yes | Unset | Order ID (required) |
| `--pair` | `string` | Yes | Unset | Currency pair (required) |

<a id="spot.order.list"></a>
### `gate-cli cex spot order list`

Operation ID: `spot.order.list`. Effect: **read**.

List orders

```text
gate-cli cex spot order list [flags]
```

API: `GET /api/v4/spot/orders` (private).

Returns: [][Order](models/spot.md#model-order).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--account` | `string` | No | Unset | Order account: spot, margin, unified or cross_margin; omitted uses server defaults |
| `--limit` | `int32` | No | `20` | Number of orders to return |
| `--pair` | `string` | Yes | Unset | Currency pair (required) |
| `--status` | `string` | No | `open` | Order status: open, finished |

<a id="spot.order.my-trades"></a>
### `gate-cli cex spot order my-trades`

Operation ID: `spot.order.my-trades`. Effect: **read**.

List personal trading history

```text
gate-cli cex spot order my-trades [flags]
```

API: `GET /api/v4/spot/my_trades` (private).

Returns: [][Trade](models/spot.md#model-trade).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--account` | `string` | No | Unset | Order account: spot, margin, unified or cross_margin; omitted uses server defaults |
| `--from` | `int64` | No | `0` | Start Unix timestamp |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--pair` | `string` | No | Unset | Filter by currency pair |
| `--to` | `int64` | No | `0` | End Unix timestamp |

<a id="spot.order.sell"></a>
### `gate-cli cex spot order sell`

Operation ID: `spot.order.sell`. Effect: **write**.

Place a sell order (omit --price for market order)

```text
gate-cli cex spot order sell [flags]
```

API: `POST /api/v4/spot/orders` (private).

Returns: [Order](models/spot.md#model-order).

API request model(s), assembled by the command: [Order](models/spot.md#model-order). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--account` | `string` | No | Unset | Order account: spot, margin, unified or cross_margin; omitted uses server defaults |
| `--amount` | `string` | Yes | Unset | Amount to trade (required) |
| `--auto-borrow` | `bool` | No | `false` | Borrow a shortfall automatically (margin, unified or cross_margin only) |
| `--auto-repay` | `bool` | No | `false` | Repay automatically for this order (unified or cross_margin only) |
| `--pair` | `string` | Yes | Unset | Currency pair, e.g. BTC_USDT (required) |
| `--price` | `string` | No | Unset | Limit price (omit for market order) |
| `--stop-loss-json` | `string` | No | Unset | Stop loss: {trigger_price,order_price}; on amend {} cancels, null/omitted keeps unchanged |
| `--stop-profit-json` | `string` | No | Unset | Take profit: {trigger_price,order_price}; on amend {} cancels, null/omitted keeps unchanged |

<a id="spot.price-trigger.cancel"></a>
### `gate-cli cex spot price-trigger cancel`

Operation ID: `spot.price-trigger.cancel`. Effect: **write**.

Cancel a price-triggered order by ID

```text
gate-cli cex spot price-trigger cancel [flags]
```

API: `DELETE /api/v4/spot/price_orders/{order_id}` (private).

Returns: [SpotPriceTriggeredOrder](models/spot.md#model-spotpricetriggeredorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `string` | Yes | Unset | Order ID (required) |

<a id="spot.price-trigger.cancel-all"></a>
### `gate-cli cex spot price-trigger cancel-all`

Operation ID: `spot.price-trigger.cancel-all`. Effect: **write**.

Cancel all price-triggered orders

```text
gate-cli cex spot price-trigger cancel-all [flags]
```

API: `DELETE /api/v4/spot/price_orders` (private).

Returns: [][SpotPriceTriggeredOrder](models/spot.md#model-spotpricetriggeredorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--market` | `string` | No | Unset | Limit cancellation to this currency pair |

<a id="spot.price-trigger.create"></a>
### `gate-cli cex spot price-trigger create`

Operation ID: `spot.price-trigger.create`. Effect: **write**.

Create a price-triggered order

```text
gate-cli cex spot price-trigger create [flags]
```

API: `POST /api/v4/spot/price_orders` (private).

Returns: [TriggerOrderResponse](models/spot.md#model-triggerorderresponse).

API request model(s), assembled by the command: [SpotPriceTriggeredOrder](models/spot.md#model-spotpricetriggeredorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--account` | `string` | No | `normal` | Account type: normal, margin, unified |
| `--amount` | `string` | Yes | Unset | Order amount (required) |
| `--market` | `string` | Yes | Unset | Currency pair, e.g. BTC_USDT (required) |
| `--price` | `string` | Yes | Unset | Order price (required) |
| `--side` | `string` | Yes | Unset | Order side: buy or sell (required) |
| `--trigger-expiration` | `int32` | No | `86400` | Trigger expiration in seconds |
| `--trigger-price` | `string` | Yes | Unset | Trigger price (required) |
| `--trigger-rule` | `string` | No | `>=` | Trigger condition: >= or <= |

<a id="spot.price-trigger.get"></a>
### `gate-cli cex spot price-trigger get`

Operation ID: `spot.price-trigger.get`. Effect: **read**.

Get a price-triggered order by ID

```text
gate-cli cex spot price-trigger get [flags]
```

API: `GET /api/v4/spot/price_orders/{order_id}` (private).

Returns: [SpotPriceTriggeredOrder](models/spot.md#model-spotpricetriggeredorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `string` | Yes | Unset | Order ID (required) |

<a id="spot.price-trigger.list"></a>
### `gate-cli cex spot price-trigger list`

Operation ID: `spot.price-trigger.list`. Effect: **read**.

List price-triggered orders

```text
gate-cli cex spot price-trigger list [flags]
```

API: `GET /api/v4/spot/price_orders` (private).

Returns: [][SpotPriceTriggeredOrder](models/spot.md#model-spotpricetriggeredorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--market` | `string` | No | Unset | Filter by currency pair |
| `--offset` | `int32` | No | `0` | Records to skip |
| `--status` | `string` | No | `open` | Order status: open, finished |

## Verification and recovery

Use `spot.order.get` with the returned ID and pair; confirm status, finish_as, filled/left amounts and trades. Cancellation does not undo prior fills.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Order examples

These illustrate distinct user-authorized variants; they do not authorize execution. Check live limits and account state first.

```bash
# Market buy: spend exactly a 10 USDT quote budget, subject to execution and fees.
gate-cli cex spot order buy --pair BTC_USDT --quote 10 --format json
# Limit buy: request 0.001 BTC at 60000 USDT per BTC.
gate-cli cex spot order buy --pair BTC_USDT --amount 0.001 --price 60000 --format json
```

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex spot account book  --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex spot order amend --id <id> --pair <pair> --format json
```

## Installed-build capability check

Older builds may omit account-selection or automatic borrowing/repayment flags.
Verify the exact installed leaf. When supported, preserve the same explicit
account across the order lifecycle under the rules below. If a required field is
missing, stop that variant without substituting another account or transport.
Price-trigger and batch JSON actions retain their own linked account contracts.

<a id="spot-account-selection"></a>
## Account selection and borrowing

`buy`, `sell`, `amend`, `cancel`, `get`, `list`, `all-open` and `my-trades` accept
`--account spot|margin|unified|cross_margin`. Omitting it preserves the server's
existing account selection; it does not force spot. Keep the same explicit account
when reading, amending or cancelling an order. The server may ignore the deprecated
`my-trades` account filter and return records across accounts; verify each result.
Batch JSON carries account fields per item, without a shared override flag.

Creation accepts `--auto-borrow` only with explicit `margin`, `unified` or
`cross_margin`. Order-level `--auto-repay` accepts only explicit `unified` or
`cross_margin`; isolated margin uses its account-level repayment setting. Borrowing,
repayment and interest/liquidation exposure need explicit user authority. Neither a
buy instruction nor a scope grant authorizes them implicitly. For loan settings,
read [margin](margin-commands.md); do not use a collateral-loan product instead.

<a id="spot-attached-protection"></a>
## Attached take profit and stop loss

`buy`, `sell` and `amend` accept `--stop-profit-json` and `--stop-loss-json`.
A nonempty object needs a positive decimal-string `trigger_price`; optional
`order_price` is a non-negative decimal string whose execution rules belong to the
server. Reject duplicate/unknown keys, null/empty members and non-string prices.
On creation, protection requires a limit order. Buy take profit triggers above the
limit price and stop loss below; sell orders reverse those comparisons. These
fields do not establish native OCO/OTO/OTOCO guarantees.
Check minimum notional for the parent and each protective order; an eligible
parent amount alone does not guarantee that its stop loss is valid.

| Amendment input | Effect |
|---|---|
| Flag omitted or top-level JSON `null` | Preserve that protection. |
| Literal empty object `{}` | Cancel that protection explicitly. |
| Valid nonempty object | Set that protection; the server validates the current order side and price. |

Read both protections and the order's current account/state before an amendment.
The API also requires `--price` or `--amount` on a protection amendment. Include
only an explicitly authorized value; do not silently resend a value from an older
snapshot. If the user authorized only a protection change, resolve that constraint
before submitting. Then query the same order to verify the price, amount and both
protections. A cancellation is not a reversal of fills.

```text
gate-cli cex spot order buy --pair BTC_USDT --account unified --amount 0.001 --price 60000 --stop-profit-json '{"trigger_price":"66000","order_price":"65900"}' --stop-loss-json '{"trigger_price":"57000","order_price":"56900"}' --format json
# Requires authority to set the parent limit price to 60000.
gate-cli cex spot order amend --pair BTC_USDT --account unified --id 123 --price 60000 --stop-loss-json '{}' --format json
```
