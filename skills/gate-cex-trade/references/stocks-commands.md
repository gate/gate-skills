# Stock trading

## Scope and source

This route uses the Stock API; do not label an instrument a tokenized security or offer mint/redeem without instrument evidence. Volume is the product-defined share quantity, not a USDT budget. Read symbol/exchange, lot precision, session and fee information. Market orders require market/regular/day with no price; limit orders require limit/all/day and a positive price. client-order-id is required, must not exceed 30 characters, and must be retained for reconciliation; never generate a new ID after a timeout. History is limited to three months; order history uses int32 Unix seconds. Fund transfers belong to gate-cex-assets.

The registered Stock CLI supports exchange and symbol discovery, symbol rules, fee rates, order books, account assets, transaction records, orders, and positions. It does **not** register stock ticker, K-line, market-status, category/filter, or streaming commands. Do not derive last price, market-open status, a category match, or tokenized-security eligibility from an order book or a similarly named TradFi command.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

Public-release availability must be verified before using these actions. If the exact `cex stock` command group or required flags are missing, stop this product task; a TradFi command is not an interchangeable substitute.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `stock.account.assets` | `gate-cli cex stock account assets` | read |
| `stock.account.transactions` | `gate-cli cex stock account transactions` | read |
| `stock.market.exchanges` | `gate-cli cex stock market exchanges` | read |
| [stock.market.fee-rate](vip-fees-commands.md#stock.market.fee-rate) | `gate-cli cex stock market fee-rate` | read |
| `stock.market.orderbook` | `gate-cli cex stock market orderbook` | read |
| `stock.market.symbol` | `gate-cli cex stock market symbol` | read |
| `stock.market.symbols` | `gate-cli cex stock market symbols` | read |
| `stock.order.cancel` | `gate-cli cex stock order cancel` | write |
| `stock.order.cancel-all` | `gate-cli cex stock order cancel-all` | write |
| `stock.order.create` | `gate-cli cex stock order create` | write |
| `stock.order.history` | `gate-cli cex stock order history` | read |
| `stock.order.list` | `gate-cli cex stock order list` | read |
| `stock.order.update` | `gate-cli cex stock order update` | write |
| `stock.position.close` | `gate-cli cex stock position close` | write |
| `stock.position.list` | `gate-cli cex stock position list` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

## Stock workflow constraints

Use `stock.market.exchanges`, `stock.market.symbols`, and `stock.market.symbol` for supported-instrument discovery. Before any create or update draft, read the exact symbol and validate `trade_status`, exchange, quote/settlement currency, `min_order_volume`, `max_order_volume`, `step_order_volume`, `price_precision`, and `volume_precision`. For a buy, read `stock.account.assets`; for a sell or close, also read `stock.position.list` and validate available quantity.

Ask for the exact symbol, side, share/unit volume, and order type. A limit order also needs a positive exact price. The Stock create contract has no quote-notional field, so do not convert a USD budget to shares or claim whole-share-only behavior. Apply the returned volume precision and limits instead.

Before a write, present the draft required by the shared safety/template rules: verified account/environment, symbol/exchange, side, quantity and unit, order type, limit price when applicable, session, time-in-force, target order ID when applicable, and available risk/fee evidence. Execute only with verified authorization. After an accepted create, update, cancel, or close, query the relevant order history/list and position. Submitted, partially filled, filled, cancelled, rejected, and unknown are distinct results.

For a market order, use `--price-type market --trading-session regular --time-in-force day` and omit `--price`. For a limit order, use `--price-type limit --trading-session all --time-in-force day --price <positive-price>`. A market order does not establish a pre-execution fill price, fill quantity, or market-hours state. Do not call a limit price a trigger price.

<a id="stock.account.assets"></a>
### `gate-cli cex stock account assets`

Operation ID: `stock.account.assets`. Effect: **read**.

Query stock account assets

```text
gate-cli cex stock account assets [flags]
```

API: `GET /api/v4/stock/users/assets` (private).

Returns: [UserAssetResp2](models/stocks.md#model-userassetresp2).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--pnl-calc-price` | `int32` | No | `0` | PnL price: 1=intraday, 2=extended-hours (omitted by default) |
| `--pnl-calc-type` | `int32` | No | `0` | PnL cost: 1=average, 2=diluted (omitted by default) |

<a id="stock.account.transactions"></a>
### `gate-cli cex stock account transactions`

Operation ID: `stock.account.transactions`. Effect: **read**.

Query stock transaction records

```text
gate-cli cex stock account transactions [flags]
```

API: `GET /api/v4/stock/transactions` (private).

Returns: [TransactionList2](models/stocks.md#model-transactionlist2).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--begin` | `int64` | No | `0` | Begin Unix seconds; with `--end`, the range must not exceed three months. |
| `--end` | `int64` | No | `0` | End Unix seconds; must not precede `--begin`. |
| `--ref-id` | `string` | No | Unset | Exact business reference; cannot be combined with other transaction filters. |
| `--type` | `string` | No | Unset | Transaction type, such as `buy`, `sell`, `fee`, `dividend`, `deposit`, or `withdraw`. |
| `--page` | `int32` | No | `1` | Page number. |
| `--page-size` | `int32` | No | `10` | Page size (1-500). |

This is a read-only ledger query. It can verify an observed transaction, but it does not authorize a fund transfer.

<a id="stock.market.exchanges"></a>
### `gate-cli cex stock market exchanges`

Operation ID: `stock.market.exchanges`. Effect: **read**.

List exchanges

```text
gate-cli cex stock market exchanges
```

API: `GET /api/v4/stock/exchanges` (public).

Returns: [Exchanges](models/stocks.md#model-exchanges).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

For the canonical stock fee-rate action and its exchange scope, read [VIP and fee commands](vip-fees-commands.md#stock.market.fee-rate).

<a id="stock.market.orderbook"></a>
### `gate-cli cex stock market orderbook`

Operation ID: `stock.market.orderbook`. Effect: **read**.

Query symbol order book

```text
gate-cli cex stock market orderbook [flags]
```

API: `GET /api/v4/stock/market/{symbol}/orderbook` (public).

Returns: [OrderBook2](models/stocks.md#model-orderbook2).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--symbol` | `string` | Yes | Unset | Stock symbol (required) |

<a id="stock.market.symbol"></a>
### `gate-cli cex stock market symbol`

Operation ID: `stock.market.symbol`. Effect: **read**.

Query stock symbols

```text
gate-cli cex stock market symbol [flags]
```

API: `GET /api/v4/stock/symbols/detail` (public).

Returns: [SymbolDetail](models/stocks.md#model-symboldetail).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--exchange` | `string` | No | Unset | Exchange: us,hk,kr,jp |
| `--page` | `int32` | No | `1` | Page number |
| `--page-size` | `int32` | No | `10` | Page size (1-500) |
| `--symbols` | `string` | Yes | Unset | Comma-separated symbols |

<a id="stock.market.symbols"></a>
### `gate-cli cex stock market symbols`

Operation ID: `stock.market.symbols`. Effect: **read**.

Query stock symbols

```text
gate-cli cex stock market symbols [flags]
```

API: `GET /api/v4/stock/symbols` (public).

Returns: [Symbols2](models/stocks.md#model-symbols2).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--exchange` | `string` | No | Unset | Exchange: us,hk,kr,jp |
| `--page` | `int32` | No | `1` | Page number |
| `--page-size` | `int32` | No | `10` | Page size (1-500) |
| `--symbols` | `string` | No | Unset | Comma-separated symbols |
| `--with-desc-i18n` | `bool` | No | `false` | Include translated descriptions |

<a id="stock.order.cancel"></a>
### `gate-cli cex stock order cancel`

Operation ID: `stock.order.cancel`. Effect: **write**.

Cancel one order

```text
gate-cli cex stock order cancel [flags]
```

API: `DELETE /api/v4/stock/orders/{order_id}` (private).

Returns: [DeleteOrder](models/stocks.md#model-deleteorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int64` | Yes | `0` | Order ID (required) |

<a id="stock.order.cancel-all"></a>
### `gate-cli cex stock order cancel-all`

Operation ID: `stock.order.cancel-all`. Effect: **write**.

Cancel all open stock orders

```text
gate-cli cex stock order cancel-all
```

API: `DELETE /api/v4/stock/orders` (private).

Returns: [DeleteOrder](models/stocks.md#model-deleteorder).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="stock.order.create"></a>
### `gate-cli cex stock order create`

Operation ID: `stock.order.create`. Effect: **write**.

Create one stock order (never automatically retried)

```text
gate-cli cex stock order create [flags]
```

API: `POST /api/v4/stock/orders` (private).

Returns: [CreateOrder2](models/stocks.md#model-createorder2).

API request model(s), assembled by the command: [TradFiSpotOrderRequest](models/stocks.md#model-tradfispotorderrequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--client-order-id` | `string` | Yes | Unset | Caller-supplied client order ID; required and at most 30 characters. |
| `--price` | `string` | No | Unset | Positive limit price |
| `--price-type` | `string` | No | `market` | market or limit |
| `--side` | `int32` | Yes | `0` | Side: 1=sell, 2=buy (required) |
| `--symbol` | `string` | Yes | Unset | symbol (required) |
| `--time-in-force` | `string` | No | `day` | Time in force: day |
| `--trading-session` | `string` | No | `regular` | market=regular, limit=all |
| `--volume` | `string` | Yes | Unset | volume (required) |

<a id="stock.order.history"></a>
### `gate-cli cex stock order history`

Operation ID: `stock.order.history`. Effect: **read**.

List historical orders

```text
gate-cli cex stock order history [flags]
```

API: `GET /api/v4/stock/orders/history` (private).

Returns: [OrderHistoryList2](models/stocks.md#model-orderhistorylist2).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--begin` | `int32` | No | `0` | Begin Unix seconds (int32) |
| `--end` | `int32` | No | `0` | End Unix seconds (int32) |
| `--order-ids` | `string` | No | Unset | At most 20 comma-separated IDs |
| `--page` | `int32` | No | `1` | Page number |
| `--page-size` | `int32` | No | `10` | Page size (1-500) |
| `--side` | `int32` | No | `0` | Side: 1=sell, 2=buy |
| `--symbol` | `string` | No | Unset | Filter by symbol |

<a id="stock.order.list"></a>
### `gate-cli cex stock order list`

Operation ID: `stock.order.list`. Effect: **read**.

List open orders

```text
gate-cli cex stock order list [flags]
```

API: `GET /api/v4/stock/orders` (private).

Returns: [OrderList2](models/stocks.md#model-orderlist2).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--symbol` | `string` | No | Unset | Filter by symbol |

<a id="stock.order.update"></a>
### `gate-cli cex stock order update`

Operation ID: `stock.order.update`. Effect: **write**.

Update order quantity and price

```text
gate-cli cex stock order update [flags]
```

API: `PUT /api/v4/stock/orders/{order_id}` (private).

Returns: [UpdateOrder2](models/stocks.md#model-updateorder2).

API request model(s), assembled by the command: [TradFiSpotOrderUpdateRequest](models/stocks.md#model-tradfispotorderupdaterequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int64` | Yes | `0` | Order ID (required) |
| `--price` | `string` | Yes | Unset | New positive price (required) |
| `--volume` | `string` | Yes | Unset | New positive volume (required) |

<a id="stock.position.close"></a>
### `gate-cli cex stock position close`

Operation ID: `stock.position.close`. Effect: **write**.

Close a stock position once

```text
gate-cli cex stock position close [flags]
```

API: `POST /api/v4/stock/positions/close` (private).

Returns: [ClosePosition](models/stocks.md#model-closeposition).

API request model(s), assembled by the command: [TradFiSpotClosePositionRequest](models/stocks.md#model-tradfispotclosepositionrequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--close-type` | `int32` | Yes | `0` | 1=partial, 2=all (required) |
| `--close-volume` | `string` | No | Unset | Positive volume for partial close only |
| `--symbol` | `string` | Yes | Unset | Symbol (required) |

<a id="stock.position.list"></a>
### `gate-cli cex stock position list`

Operation ID: `stock.position.list`. Effect: **read**.

List positions

```text
gate-cli cex stock position list [flags]
```

API: `GET /api/v4/stock/positions` (private).

Returns: [PositionList2](models/stocks.md#model-positionlist2).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--exchange` | `string` | No | Unset | Exchange: us,hk,kr,jp |
| `--pnl-calc-price` | `int32` | No | `0` | PnL price: 1=intraday, 2=extended-hours (omitted by default) |
| `--pnl-calc-type` | `int32` | No | `0` | PnL cost: 1=average, 2=diluted (omitted by default) |
| `--symbol` | `string` | No | Unset | Filter by symbol |

## Verification and recovery

Use `stock.order.list` and `stock.order.history` with returned order IDs, then `stock.position.list`. This baseline has no `stock order get` leaf. Preserve client-order-id but do not invent a history filter for it.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex stock account assets  --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex stock order cancel --id <id> --format json
```
