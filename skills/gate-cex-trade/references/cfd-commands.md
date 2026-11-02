# CFD trading

## Scope and source

CFD volume is symbol-defined and differs from stock shares or crypto contracts. Read category, symbol contract size, volume step, trading status, account assets and positions. Pass API enum spellings explicitly: Long/Short and candle intervals 1m,15m,1h,4h,1d,7d,30d; the CLI also maps the documented legacy candle aliases below. Read existing order/position TP and SL first: omitted protections or zero can clear them, so resend unchanged protections that must remain. CFD histories start no earlier than one month ago; transaction page size is at most 50. Order-log and commission-query leaves are listed below; verify their actual flags. Order-leverage and position-history pagination flags are not established. Product funding belongs to gate-cex-assets.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

Public-release availability must be verified before using these actions. CFD uses the `cex tradfi` CLI namespace. For the requested action, verify the exact `gate-cli cex tradfi <group> <leaf> --help`, including its Usage, available command and required flags, against the action contract below. Stop only that operation if the actual TradFi leaf or necessary flags are absent or incompatible. The CFD product label does not require a separate CLI group; do not substitute a stock or another product.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `tradfi.account.assets` | `gate-cli cex tradfi account assets` | read |
| `tradfi.account.info` | `gate-cli cex tradfi account info` | read |
| `tradfi.market.categories` | `gate-cli cex tradfi market categories` | read |
| `tradfi.market.kline` | `gate-cli cex tradfi market kline` | read |
| `tradfi.market.symbol` | `gate-cli cex tradfi market symbol` | read |
| `tradfi.market.symbols` | `gate-cli cex tradfi market symbols` | read |
| `tradfi.market.ticker` | `gate-cli cex tradfi market ticker` | read |
| `tradfi.order.cancel` | `gate-cli cex tradfi order cancel` | write |
| `tradfi.order.create` | `gate-cli cex tradfi order create` | write |
| `tradfi.order.history` | `gate-cli cex tradfi order history` | read |
| `tradfi.order.list` | `gate-cli cex tradfi order list` | read |
| `tradfi.order.update` | `gate-cli cex tradfi order update` | write |
| `tradfi.position.close` | `gate-cli cex tradfi position close` | write |
| `tradfi.position.history` | `gate-cli cex tradfi position history` | read |
| `tradfi.position.list` | `gate-cli cex tradfi position list` | read |
| `tradfi.position.update` | `gate-cli cex tradfi position update` | write |
| `tradfi.market.commissions` | `gate-cli cex tradfi market commissions` | read |
| `tradfi.order.log` | `gate-cli cex tradfi order log` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="tradfi.account.assets"></a>
### `gate-cli cex tradfi account assets`

Operation ID: `tradfi.account.assets`. Effect: **read**.

Get TradFi account asset balances

```text
gate-cli cex tradfi account assets
```

API: `GET /api/v4/tradfi/users/assets` (private).

Returns: [UserAssetResp](models/cfd.md#model-userassetresp).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="tradfi.account.info"></a>
### `gate-cli cex tradfi account info`

Operation ID: `tradfi.account.info`. Effect: **read**.

Get MT5 account information

```text
gate-cli cex tradfi account info
```

API: `GET /api/v4/tradfi/users/mt5-account` (private).

Returns: [Mt5Account](models/cfd.md#model-mt5account).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="tradfi.market.categories"></a>
### `gate-cli cex tradfi market categories`

Operation ID: `tradfi.market.categories`. Effect: **read**.

List all TradFi symbol categories

```text
gate-cli cex tradfi market categories
```

API: `GET /api/v4/tradfi/symbols/categories` (public).

Returns: [Categories](models/cfd.md#model-categories).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="tradfi.market.kline"></a>
### `gate-cli cex tradfi market kline`

Operation ID: `tradfi.market.kline`. Effect: **read**.

Get candlestick data for a TradFi symbol

```text
gate-cli cex tradfi market kline [flags]
```

API: `GET /api/v4/tradfi/symbols/{symbol}/klines` (public).

Returns: [Klines](models/cfd.md#model-klines).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--limit` | `int32` | No | `100` | Number of candlesticks to return |
| `--symbol` | `string` | Yes | Unset | Symbol name, e.g. XAUUSD (required) |
| `--type` | `string` | No | `1m` | API intervals: `1m`, `15m`, `1h`, `4h`, `1d`, `7d`, `30d`; CLI also accepts legacy aliases `M1`, `M15`, `H1`, `H4`, `D1` |

Translate the user's requested period to an API interval: one hour is `1h`, four hours is `4h`. The CLI defaults to `1m` and maps `M1/M15/H1/H4/D1` to `1m/15m/1h/4h/1d` before sending `kline_type`; the API itself accepts only API intervals. Prefer explicit API intervals for clarity. Five-minute and thirty-minute candles (`M5/M30`) are not supported; explain that limit without silently substituting another period.

```bash
gate-cli cex tradfi market kline --symbol XAUUSD --type 1h --limit 100 --format json
```

<a id="tradfi.market.symbol"></a>
### `gate-cli cex tradfi market symbol`

Operation ID: `tradfi.market.symbol`. Effect: **read**.

Get details for a TradFi symbol

```text
gate-cli cex tradfi market symbol [flags]
```

API: `GET /api/v4/tradfi/symbols/detail` (private).

Returns: [ContractDetail](models/cfd.md#model-contractdetail).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--symbol` | `string` | Yes | Unset | Symbol name, e.g. XAUUSD (required) |

<a id="tradfi.market.symbols"></a>
### `gate-cli cex tradfi market symbols`

Operation ID: `tradfi.market.symbols`. Effect: **read**.

List all TradFi symbols

```text
gate-cli cex tradfi market symbols
```

API: `GET /api/v4/tradfi/symbols` (public).

Returns: [Symbols](models/cfd.md#model-symbols).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="tradfi.market.ticker"></a>
### `gate-cli cex tradfi market ticker`

Operation ID: `tradfi.market.ticker`. Effect: **read**.

Get ticker for a TradFi symbol

```text
gate-cli cex tradfi market ticker [flags]
```

API: `GET /api/v4/tradfi/symbols/{symbol}/tickers` (public).

Returns: [TradFiTicker](models/cfd.md#model-tradfiticker).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--symbol` | `string` | Yes | Unset | Symbol name, e.g. XAUUSD (required) |

<a id="tradfi.order.cancel"></a>
### `gate-cli cex tradfi order cancel`

Operation ID: `tradfi.order.cancel`. Effect: **write**.

Cancel a TradFi order

```text
gate-cli cex tradfi order cancel [flags]
```

API: `DELETE /api/v4/tradfi/orders/{order_id}` (private).

Returns: `map[string]any`.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int64` | Yes | `0` | Order ID (required) |

<a id="tradfi.order.create"></a>
### `gate-cli cex tradfi order create`

Operation ID: `tradfi.order.create`. Effect: **write**.

Create a TradFi order

```text
gate-cli cex tradfi order create [flags]
```

API: `POST /api/v4/tradfi/orders` (private).

Returns: [CreateOrder2](models/cfd.md#model-createorder2).

API request model(s), assembled by the command: [TradFiOrderRequest](models/cfd.md#model-tradfiorderrequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--price` | `string` | No | `0` | Order price (use 0 for market orders) |
| `--price-type` | `string` | No | `market` | Price type: market or trigger |
| `--side` | `int32` | Yes | `0` | Order side: 1=sell, 2=buy (required) |
| `--sl` | `string` | No | Unset | Stop-loss price |
| `--symbol` | `string` | Yes | Unset | Symbol name, e.g. XAUUSD (required) |
| `--tp` | `string` | No | Unset | Take-profit price |
| `--volume` | `string` | Yes | Unset | Order volume (required) |

<a id="tradfi.order.history"></a>
### `gate-cli cex tradfi order history`

Operation ID: `tradfi.order.history`. Effect: **read**.

List TradFi order history

```text
gate-cli cex tradfi order history [flags]
```

API: `GET /api/v4/tradfi/orders/history` (private).

Returns: [OrderHistoryList](models/cfd.md#model-orderhistorylist).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--begin` | `int64` | No | `0` | Begin timestamp (Unix seconds) |
| `--end` | `int64` | No | `0` | End timestamp (Unix seconds) |
| `--side` | `int32` | No | `0` | Filter by side: 1=sell, 2=buy |
| `--symbol` | `string` | No | Unset | Filter by symbol |

<a id="tradfi.order.list"></a>
### `gate-cli cex tradfi order list`

Operation ID: `tradfi.order.list`. Effect: **read**.

List open TradFi orders

```text
gate-cli cex tradfi order list
```

API: `GET /api/v4/tradfi/orders` (private).

Returns: [OrderList](models/cfd.md#model-orderlist).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="tradfi.order.update"></a>
### `gate-cli cex tradfi order update`

Operation ID: `tradfi.order.update`. Effect: **write**.

Update a TradFi order (price, TP, SL)

```text
gate-cli cex tradfi order update [flags]
```

API: `PUT /api/v4/tradfi/orders/{order_id}` (private).

Returns: [UpdateOrder](models/cfd.md#model-updateorder).

API request model(s), assembled by the command: [TradFiOrderUpdateRequest](models/cfd.md#model-tradfiorderupdaterequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int64` | Yes | `0` | Order ID (required) |
| `--price` | `string` | Yes | Unset | New price (required) |
| `--sl` | `string` | No | Unset | New stop-loss price |
| `--tp` | `string` | No | Unset | New take-profit price |

<a id="tradfi.position.close"></a>
### `gate-cli cex tradfi position close`

Operation ID: `tradfi.position.close`. Effect: **write**.

Close a TradFi position

```text
gate-cli cex tradfi position close [flags]
```

API: `POST /api/v4/tradfi/positions/{position_id}/close` (private).

Returns: [DeletePosition](models/cfd.md#model-deleteposition).

API request model(s), assembled by the command: [TradFiClosePositionRequest](models/cfd.md#model-tradficlosepositionrequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--close-type` | `int32` | Yes | `0` | Close type: 1=partial close, 2=full close (required) |
| `--id` | `int64` | Yes | `0` | Position ID (required) |
| `--volume` | `string` | Conditional | Unset | Volume for partial close (required when close-type=1) |

<a id="tradfi.position.history"></a>
### `gate-cli cex tradfi position history`

Operation ID: `tradfi.position.history`. Effect: **read**.

List TradFi position close history

```text
gate-cli cex tradfi position history [flags]
```

API: `GET /api/v4/tradfi/positions/history` (private).

Returns: [PositionHistoryList](models/cfd.md#model-positionhistorylist).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--begin` | `int64` | No | `0` | Begin timestamp (Unix seconds) |
| `--direction` | `string` | No | Unset | Filter by position direction: long, short |
| `--end` | `int64` | No | `0` | End timestamp (Unix seconds) |
| `--symbol` | `string` | No | Unset | Filter by symbol |

<a id="tradfi.position.list"></a>
### `gate-cli cex tradfi position list`

Operation ID: `tradfi.position.list`. Effect: **read**.

List open TradFi positions

```text
gate-cli cex tradfi position list
```

API: `GET /api/v4/tradfi/positions` (private).

Returns: [PositionList](models/cfd.md#model-positionlist).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="tradfi.position.update"></a>
### `gate-cli cex tradfi position update`

Operation ID: `tradfi.position.update`. Effect: **write**.

Update take-profit and/or stop-loss for a position

```text
gate-cli cex tradfi position update [flags]
```

API: `PUT /api/v4/tradfi/positions/{position_id}` (private).

Returns: [UpdatePosition](models/cfd.md#model-updateposition).

API request model(s), assembled by the command: [TradFiPositionUpdateRequest](models/cfd.md#model-tradfipositionupdaterequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int64` | Yes | `0` | Position ID (required) |
| `--sl` | `string` | No | Unset | New stop-loss price |
| `--tp` | `string` | No | Unset | New take-profit price |

## Verification and recovery

Use `tradfi.order.list`/history and `tradfi.position.list`/history for the returned object. Verify both TP and SL after updates. Preserve raw business code/message and data; envelope timestamp is milliseconds, while candle t is seconds.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex tradfi account assets  --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex tradfi order cancel --id <id> --format json
```

<a id="tradfi.market.commissions"></a>
### `gate-cli cex tradfi market commissions`

Operation ID: `tradfi.market.commissions`. Effect: **read**.

Query authenticated TradFi symbol commissions

```text
gate-cli cex tradfi market commissions [flags]
```

API: `GET /api/v4/tradfi/symbols/commissions` (private).

Returns: [SymbolCommissions](models/cfd.md#model-symbolcommissions).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--category-code` | `string` | No | Unset | Optional category code |
| `--symbols` | `string` | No | Unset | Comma-separated symbols; omitted to use server defaults |

<a id="tradfi.order.log"></a>
### `gate-cli cex tradfi order log`

Operation ID: `tradfi.order.log`. Effect: **read**.

Get a TradFi order log entry

```text
gate-cli cex tradfi order log [flags]
```

API: `GET /api/v4/tradfi/orders/log/{log_id}` (private).

Returns: [OrderLog](models/cfd.md#model-orderlog).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--log-id` | `int64` | Yes | `0` | Positive log ID |

<a id="cfd-commissions-and-order-logs"></a>
## Commissions and order logs

`tradfi.market.commissions` is an authenticated CFD fee-schedule query. It accepts
optional comma-separated `--symbols` and `--category-code`; narrow the requested
set. `data.list` contains symbol, category and fee per lot as a decimal string.
This is a trading cost, not affiliate commission earnings; do not route it to the
rebate skill or infer a universal maker/taker rate.

`tradfi.order.log --log-id` requires a positive exact int64 log ID. Keep `log_id`
and `order_id` distinct; obtain the log reference from the relevant order/history
record instead of substituting an unrelated order ID. Inspect the returned symbol,
side, volume, price and state. A log alone is not proof of a completed position
change; reconcile the order, trades and position. Responses use the CFD timestamp
and `data` envelope shown in [models](models/cfd.md).
