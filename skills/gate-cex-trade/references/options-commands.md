# Options trading

## Scope and source

Resolve the exact underlying, call/put, strike, expiry and contract identifier; read contract size, quote currency, premium precision and trading window. Quantity is the contract-defined size, not a quote budget. Use the premium price and time-in-force fields exposed by this CLI; Mark-IV order pricing is unavailable. Short options create distinct margin and exercise exposure. MMP set/reset and countdown cancellation are real supported writes; their existence does not establish an RFQ/block-trade capability. Read positions and protection settings before changing them.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `options.account.book` | `gate-cli cex options account book` | read |
| `options.account.get` | `gate-cli cex options account get` | read |
| `options.account.settlements` | `gate-cli cex options account settlements` | read |
| `options.mmp.get` | `gate-cli cex options mmp get` | read |
| `options.mmp.reset` | `gate-cli cex options mmp reset` | write |
| `options.mmp.set` | `gate-cli cex options mmp set` | write |
| `options.order.amend` | `gate-cli cex options order amend` | write |
| `options.order.cancel` | `gate-cli cex options order cancel` | write |
| `options.order.cancel-all` | `gate-cli cex options order cancel-all` | write |
| `options.order.countdown-cancel-all` | `gate-cli cex options order countdown-cancel-all` | write |
| `options.order.create` | `gate-cli cex options order create` | write |
| `options.order.get` | `gate-cli cex options order get` | read |
| `options.order.list` | `gate-cli cex options order list` | read |
| `options.position.close` | `gate-cli cex options position close` | read |
| `options.position.get` | `gate-cli cex options position get` | read |
| `options.position.list` | `gate-cli cex options position list` | read |
| `options.position.my-trades` | `gate-cli cex options position my-trades` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="options.account.book"></a>
### `gate-cli cex options account book`

Operation ID: `options.account.book`. Effect: **read**.

List options account change history

```text
gate-cli cex options account book [flags]
```

API: `GET /api/v4/options/account_book` (private).

Returns: [][OptionsAccountBook](models/options.md#model-optionsaccountbook).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--from` | `int64` | No | `0` | Start Unix timestamp |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--offset` | `int32` | No | `0` | Number of records to skip |
| `--to` | `int64` | No | `0` | End Unix timestamp |
| `--type` | `string` | No | Unset | Change type filter |

<a id="options.account.get"></a>
### `gate-cli cex options account get`

Operation ID: `options.account.get`. Effect: **read**.

Get options account information

```text
gate-cli cex options account get
```

API: `GET /api/v4/options/accounts` (private).

Returns: [OptionsAccount](models/options.md#model-optionsaccount).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="options.account.settlements"></a>
### `gate-cli cex options account settlements`

Operation ID: `options.account.settlements`. Effect: **read**.

List personal settlement history

```text
gate-cli cex options account settlements [flags]
```

API: `GET /api/v4/options/my_settlements` (private).

Returns: [][OptionsMySettlements](models/options.md#model-optionsmysettlements).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--underlying` | `string` | Yes | Unset | Underlying name (required) |

<a id="options.mmp.get"></a>
### `gate-cli cex options mmp get`

Operation ID: `options.mmp.get`. Effect: **read**.

Query MMP settings

```text
gate-cli cex options mmp get [flags]
```

API: `GET /api/v4/options/mmp` (private).

Returns: [][OptionsMmp](models/options.md#model-optionsmmp).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--underlying` | `string` | No | Unset | Filter by underlying |

<a id="options.mmp.reset"></a>
### `gate-cli cex options mmp reset`

Operation ID: `options.mmp.reset`. Effect: **write**.

Reset MMP (unfreeze)

```text
gate-cli cex options mmp reset [flags]
```

API: `POST /api/v4/options/mmp/reset` (private).

Returns: [OptionsMmp](models/options.md#model-optionsmmp).

API request model(s), assembled by the command: [OptionsMmpReset](models/options.md#model-optionsmmpreset). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--underlying` | `string` | Yes | Unset | Underlying name (required) |

<a id="options.mmp.set"></a>
### `gate-cli cex options mmp set`

Operation ID: `options.mmp.set`. Effect: **write**.

Set MMP configuration

```text
gate-cli cex options mmp set [flags]
```

API: `POST /api/v4/options/mmp` (private).

Returns: [OptionsMmp](models/options.md#model-optionsmmp).

API request model(s), assembled by the command: [OptionsMmp](models/options.md#model-optionsmmp). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--delta-limit` | `string` | Yes | Unset | Net delta upper limit (required) |
| `--frozen-period` | `int32` | Yes | `0` | Freeze duration in milliseconds (required) |
| `--qty-limit` | `string` | Yes | Unset | Trading volume upper limit (required) |
| `--underlying` | `string` | Yes | Unset | Underlying name (required) |
| `--window` | `int32` | Yes | `0` | Time window in milliseconds (required) |

<a id="options.order.amend"></a>
### `gate-cli cex options order amend`

Operation ID: `options.order.amend`. Effect: **write**.

Amend an options order

```text
gate-cli cex options order amend [flags]
```

API: `PUT /api/v4/options/orders/{order_id}` (private).

Returns: [OptionsOrder](models/options.md#model-optionsorder).

API request model(s), assembled by the command: [AmendOptionsOrderRequest](models/options.md#model-amendoptionsorderrequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Options contract name (required) |
| `--id` | `int64` | Yes | `0` | Order ID (required) |
| `--price` | `string` | Yes | Unset | New price (required) |
| `--size` | `int64` | No | `0` | New size |

<a id="options.order.cancel"></a>
### `gate-cli cex options order cancel`

Operation ID: `options.order.cancel`. Effect: **write**.

Cancel a single options order

```text
gate-cli cex options order cancel [flags]
```

API: `DELETE /api/v4/options/orders/{order_id}` (private).

Returns: [OptionsOrder](models/options.md#model-optionsorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int64` | Yes | `0` | Order ID (required) |

<a id="options.order.cancel-all"></a>
### `gate-cli cex options order cancel-all`

Operation ID: `options.order.cancel-all`. Effect: **write**.

Cancel all open options orders

```text
gate-cli cex options order cancel-all [flags]
```

API: `DELETE /api/v4/options/orders` (private).

Returns: [][OptionsOrder](models/options.md#model-optionsorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--side` | `string` | No | Unset | Filter by side: ask or bid |
| `--underlying` | `string` | No | Unset | Filter by underlying |

<a id="options.order.countdown-cancel-all"></a>
### `gate-cli cex options order countdown-cancel-all`

Operation ID: `options.order.countdown-cancel-all`. Effect: **write**.

Countdown to cancel all options orders

```text
gate-cli cex options order countdown-cancel-all [flags]
```

API: `POST /api/v4/options/countdown_cancel_all` (private).

Returns: [TriggerTime](models/options.md#model-triggertime).

API request model(s), assembled by the command: [CountdownCancelAllOptionsTask](models/options.md#model-countdowncancelalloptionstask). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--timeout` | `int32` | Yes | `0` | Countdown timeout in seconds (required); 0 to cancel the countdown |
| `--underlying` | `string` | No | Unset | Filter by underlying |

<a id="options.order.create"></a>
### `gate-cli cex options order create`

Operation ID: `options.order.create`. Effect: **write**.

Create an options order

```text
gate-cli cex options order create [flags]
```

API: `POST /api/v4/options/orders` (private).

Returns: [OptionsOrder](models/options.md#model-optionsorder).

API request model(s), assembled by the command: [OptionsOrder](models/options.md#model-optionsorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--close` | `bool` | No | `false` | Close the full position; requires --size 0 |
| `--contract` | `string` | Yes | Unset | Options contract name (required) |
| `--price` | `string` | No | Unset | Order price (0 for market order with ioc) |
| `--reduce-only` | `bool` | No | `false` | Only reduce an existing position; signed --size specifies the partial close |
| `--size` | `int64` | Yes | `0` | Order size, positive for buy, negative for sell (required) |
| `--tif` | `string` | No | Unset | Time in force: gtc, ioc, poc, fok |

<a id="options.order.get"></a>
### `gate-cli cex options order get`

Operation ID: `options.order.get`. Effect: **read**.

Get details of an options order

```text
gate-cli cex options order get [flags]
```

API: `GET /api/v4/options/orders/{order_id}` (private).

Returns: [OptionsOrder](models/options.md#model-optionsorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int64` | Yes | `0` | Order ID (required) |

<a id="options.order.list"></a>
### `gate-cli cex options order list`

Operation ID: `options.order.list`. Effect: **read**.

List options orders

```text
gate-cli cex options order list [flags]
```

API: `GET /api/v4/options/orders` (private).

Returns: [][OptionsOrder](models/options.md#model-optionsorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--offset` | `int32` | No | `0` | Number of records to skip |
| `--status` | `string` | Yes | `open` | Order status: open or finished (required) |
| `--underlying` | `string` | No | Unset | Filter by underlying |

<a id="options.position.close"></a>
### `gate-cli cex options position close`

Operation ID: `options.position.close`. Effect: **read**.

List position close history for an underlying

```text
gate-cli cex options position close [flags]
```

API: `GET /api/v4/options/position_close` (private).

Returns: [][OptionsPositionClose](models/options.md#model-optionspositionclose).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--underlying` | `string` | Yes | Unset | Underlying name (required) |

<a id="options.position.get"></a>
### `gate-cli cex options position get`

Operation ID: `options.position.get`. Effect: **read**.

Get details of an options position

```text
gate-cli cex options position get [flags]
```

API: `GET /api/v4/options/positions/{contract}` (private).

Returns: [OptionsPosition](models/options.md#model-optionsposition).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Options contract name (required) |

<a id="options.position.list"></a>
### `gate-cli cex options position list`

Operation ID: `options.position.list`. Effect: **read**.

List options positions

```text
gate-cli cex options position list [flags]
```

API: `GET /api/v4/options/positions` (private).

Returns: [][OptionsPosition](models/options.md#model-optionsposition).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--underlying` | `string` | No | Unset | Filter by underlying |

<a id="options.position.my-trades"></a>
### `gate-cli cex options position my-trades`

Operation ID: `options.position.my-trades`. Effect: **read**.

List personal options trading records

```text
gate-cli cex options position my-trades [flags]
```

API: `GET /api/v4/options/my_trades` (private).

Returns: [][OptionsMyTrade](models/options.md#model-optionsmytrade).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--offset` | `int32` | No | `0` | Number of records to skip |
| `--underlying` | `string` | Yes | Unset | Underlying name (required) |

## Verification and recovery

Use `options.order.get`, `options.position.get` and `options.mmp.get` as applicable. Inspect fills and remaining exposure; a successful MMP reset is not a fill or a closed position.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex options account book  --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex options mmp reset --underlying <underlying> --format json
```

<a id="options-position-close"></a>
## Position close and close history

`options.position.close` is a read-only close-history query. To close a live
position, first read the exact current position, signed size and pending orders.
Use `options.order.create --close --size 0` for a full close. For a partial close,
use nonzero opposite-signed contract size with `--reduce-only`; never approximate
a guaranteed reduction with an unguarded opposite order. Prices are premium
strings; price `0` needs `--tif ioc` for market execution. Do not claim a guaranteed
execution price or fill. Preserve exact int64 size; no float conversion.

After submission, inspect the order and position; acceptance is not a completed
close. A timeout or lost ID requires reconciliation, not a replacement order.
`--close` with nonzero size and zero size without `--close` are invalid. These flags
apply to order creation, not to amendments or the history command.

```text
gate-cli cex options order create --contract BTC_USDT-20261225-60000-C --close --size 0 --price 0 --tif ioc --format json
gate-cli cex options order create --contract BTC_USDT-20261225-60000-C --reduce-only --size -1 --price 0 --tif ioc --format json
```
