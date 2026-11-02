# Algorithm execution boundaries

## Scope and source

Spot POV and futures chase orders are supported below. Native spot/futures TWAP and futures VP are separate, unsupported lifecycles; do not claim their execution guarantees. Ordinary limit, trigger, trailing and countdown-cancel orders are separate documented actions. Do not synthesize a timed trading loop, sign HTTP requests or use a different transport to fill the gap.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `futures.chase.create` | `gate-cli cex futures chase create` | write |
| `futures.chase.get` | `gate-cli cex futures chase get` | read |
| `futures.chase.list` | `gate-cli cex futures chase list` | read |
| `futures.chase.stop` | `gate-cli cex futures chase stop` | write |
| `futures.chase.stop-all` | `gate-cli cex futures chase stop-all` | write |
| `spot.pov.cancel` | `gate-cli cex spot pov cancel` | write |
| `spot.pov.cancel-all` | `gate-cli cex spot pov cancel-all` | write |
| `spot.pov.create` | `gate-cli cex spot pov create` | write |
| `spot.pov.get` | `gate-cli cex spot pov get` | read |
| `spot.pov.list` | `gate-cli cex spot pov list` | read |

## Invocation and parameter rules

Use separate argv values and `--format json`. The request models below define JSON fields; decimal values must remain strings. Check the applicable product permissions and user authority before each write.


<a id="futures.chase.create"></a>
### `gate-cli cex futures chase create`

Operation ID: `futures.chase.create`. Effect: **write**.

Create a chase order from SDK request JSON

```text
gate-cli cex futures chase create [flags]
```

API: `POST /api/v4/futures/{settle}/autoorder/v1/chase/create` (private).

Returns: [CreateChaseOrderResp](models/algo.md#model-createchaseorderresp).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--json` | `string` | Yes | Unset | CreateChaseOrderReq JSON; see the request model below |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

JSON request: [CreateChaseOrderReq](models/algo.md#model-createchaseorderreq). Read [chase rules](#futures-chase-execution) before constructing it.

<a id="futures.chase.get"></a>
### `gate-cli cex futures chase get`

Operation ID: `futures.chase.get`. Effect: **read**.

Get a chase order

```text
gate-cli cex futures chase get [flags]
```

API: `GET /api/v4/futures/{settle}/autoorder/v1/chase/detail` (private).

Returns: [GetChaseOrderDetailResp](models/algo.md#model-getchaseorderdetailresp).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `string` | Yes | Unset | Order ID |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.chase.list"></a>
### `gate-cli cex futures chase list`

Operation ID: `futures.chase.list`. Effect: **read**.

List active or finished chase orders

```text
gate-cli cex futures chase list [flags]
```

API: `GET /api/v4/futures/{settle}/autoorder/v1/chase/list` (private).

Returns: [GetChaseOrdersResp](models/algo.md#model-getchaseordersresp).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Contract name, e.g. BTC_USDT |
| `--finished` | `bool` | No | `false` | Query finished orders; requires --from and --to |
| `--from` | `int64` | No | `0` | Start Unix timestamp |
| `--hide-cancel` | `bool` | No | `false` | Hide cancelled orders |
| `--limit` | `int32` | No | `20` | Records per page, 1 to 100 |
| `--page` | `int32` | No | `1` | Page number, starting at 1 |
| `--reduce-only` | `int32` | No | `0` | 0=all, 1=reduce-only, 2=not reduce-only |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--side` | `int32` | No | `0` | 0=all, 1=long, 2=short |
| `--sort-by` | `int32` | No | `1` | 1=created, 2=finished |
| `--to` | `int64` | No | `0` | End Unix timestamp |

<a id="futures.chase.stop"></a>
### `gate-cli cex futures chase stop`

Operation ID: `futures.chase.stop`. Effect: **write**.

Stop a chase order by ID or custom text

```text
gate-cli cex futures chase stop [flags]
```

API: `POST /api/v4/futures/{settle}/autoorder/v1/chase/stop` (private).

Returns: [StopChaseOrderResp](models/algo.md#model-stopchaseorderresp).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `string` | No | Unset | Order ID |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--text` | `string` | No | Unset | text |

<a id="futures.chase.stop-all"></a>
### `gate-cli cex futures chase stop-all`

Operation ID: `futures.chase.stop-all`. Effect: **write**.

Stop all chase orders, optionally filtered by contract and margin mode

```text
gate-cli cex futures chase stop-all [flags]
```

API: `POST /api/v4/futures/{settle}/autoorder/v1/chase/stop_all` (private).

Returns: [StopAllChaseOrdersResp](models/algo.md#model-stopallchaseordersresp).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Contract name, e.g. BTC_USDT |
| `--pos-margin-mode` | `string` | No | Unset | isolated or cross |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="spot.pov.cancel"></a>
### `gate-cli cex spot pov cancel`

Operation ID: `spot.pov.cancel`. Effect: **write**.

Cancel a spot POV order

```text
gate-cli cex spot pov cancel [flags]
```

API: `DELETE /api/v4/spot/pov_orders/{order_id}` (private).

Returns: [SpotPovOrder](models/algo.md#model-spotpovorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `string` | Yes | Unset | Order ID |

<a id="spot.pov.cancel-all"></a>
### `gate-cli cex spot pov cancel-all`

Operation ID: `spot.pov.cancel-all`. Effect: **write**.

Cancel all spot POV orders; omit pair for all pairs

```text
gate-cli cex spot pov cancel-all [flags]
```

API: `DELETE /api/v4/spot/pov_orders` (private).

Returns: [][SpotPovOrder](models/algo.md#model-spotpovorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--pair` | `string` | No | Unset | Currency pair, e.g. BTC_USDT |

<a id="spot.pov.create"></a>
### `gate-cli cex spot pov create`

Operation ID: `spot.pov.create`. Effect: **write**.

Create a spot participation-of-volume order

```text
gate-cli cex spot pov create [flags]
```

API: `POST /api/v4/spot/pov_orders` (private).

Returns: [SpotPovOrder](models/algo.md#model-spotpovorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--amount` | `string` | Yes | Unset | Base currency amount as a decimal string |
| `--limit-price` | `string` | No | Unset | Limit price; omit to use the market price |
| `--pair` | `string` | Yes | Unset | Currency pair, e.g. BTC_USDT |
| `--participation-rate` | `int32` | Yes | `0` | Participation percentage: 5, 10, 20 or 40 |
| `--side` | `string` | Yes | Unset | buy or sell |
| `--text` | `string` | No | Unset | Custom ID: t- followed by at most 28 letters, digits, _, - or . |
| `--trigger-price` | `string` | No | Unset | Trigger price; omit for immediate activation |
| `--ttl` | `string` | Yes | Unset | 1h, 6h, 12h or 1d through 7d |

Request fields: [SpotPovOrderCreator](models/algo.md#model-spotpovordercreator). Read [POV rules](#spot-pov-execution).

<a id="spot.pov.get"></a>
### `gate-cli cex spot pov get`

Operation ID: `spot.pov.get`. Effect: **read**.

Get a spot POV order

```text
gate-cli cex spot pov get [flags]
```

API: `GET /api/v4/spot/pov_orders/{order_id}` (private).

Returns: [SpotPovOrder](models/algo.md#model-spotpovorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `string` | Yes | Unset | Order ID |

<a id="spot.pov.list"></a>
### `gate-cli cex spot pov list`

Operation ID: `spot.pov.list`. Effect: **read**.

List spot POV orders

```text
gate-cli cex spot pov list [flags]
```

API: `GET /api/v4/spot/pov_orders` (private).

Returns: [][SpotPovOrder](models/algo.md#model-spotpovorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--limit` | `int32` | No | `20` | Records per page, 1 to 1000 |
| `--page` | `int32` | No | `1` | Page number, 1 to 100 |
| `--pair` | `string` | No | Unset | Currency pair, e.g. BTC_USDT |
| `--side` | `string` | No | Unset | Filter by buy or sell |
| `--status` | `string` | No | `open` | open or finished |

<a id="spot-pov-execution"></a>
## Spot POV execution

Use `spot.pov.create` for a participation-of-volume order, not a timed local loop.
`--amount` is base currency on either side; `--side` is `buy` or `sell`.
`--participation-rate` is the integer percentage 5, 10, 20 or 40. TTL is `1h`,
`6h`, `12h`, or `1d` through `7d`. Optional limit/trigger prices are positive
strings; omitting them uses market pricing/immediate activation respectively.
A custom text starts with `t-` followed by 1–28 letters, digits, underscores,
hyphens or dots. A tag is not an idempotency guarantee.

Creation returns a POV ID, not proof of a fill. Poll `spot.pov.get` within the task
budget and inspect status, termination reason, then bounded spot orders/trades to
verify execution. If no unique child/fill linkage is available, report the filled
quantity unresolved; similar recent orders are not a unique match. Do not equate
the requested amount with the filled amount.
`list` takes `open`/`finished`, page 1–100 and limit 1–1000, subject to the smaller
shared read budget. Cancel one by ID. `cancel-all` without `--pair` affects all
pairs and needs that exact authority. Inspect each result and reconcile remaining
orders; cancellation does not undo executed trades. No POV amend is registered.

<a id="futures-chase-execution"></a>
## Futures chase execution

`futures.chase.create` takes [CreateChaseOrderReq](models/algo.md#model-createchaseorderreq)
as `--json`. Required fields are `contract`, a nonzero signed decimal-string
`amount` in contracts, and non-negative decimal-string `price_limit` (`"0"` for no
price limit). Positive amount buys; negative sells. Optional fields:

| Field | Rule |
|---|---|
| `offset_limit` | Positive decimal string; mutually exclusive with a nonzero `price_limit`. |
| `reduce_only` | Boolean; use true for an authorized reduction. |
| `is_dual_mode` | Boolean matching the actual position mode. |
| `price_type` | 1 best bid/ask, 2 distance from best bid/ask; omitted uses server default. |
| `price_gap_type`, `price_gap_value` | Only for type 2: required 1 absolute gap or 2 percentage, plus a positive decimal string. |
| `pos_margin_mode` | `isolated` or `cross`. |
| `position_mode` | `single`, `dual` or `dual_plus`; match actual account settings. |
| `text` | Optional custom tag; do not treat it as replay authorization. |
| `settle` | Optional; must match effective `--settle`/profile settlement. |

JSON keys are ASCII; duplicate/unknown keys and null members are rejected.
Financial decimal strings have at most 80 characters. Do not copy response-only
[ChaseOrder](models/algo.md#model-chaseorder) fields into the request.

Read contract/position/mode/available margin first. Create once; get by the returned
string ID and inspect status, fills and the current child-order reference. A zero
exit with an empty object, missing ID or mismatched ID is incomplete evidence, not
a successful lookup or execution; never resubmit to recover the missing result. Inspect
child orders through the perpetual order actions when necessary. A stopped chase
response alone does not establish zero residual exposure; re-read the chase,
current child order and position. Never replay an uncertain creation.

`list --finished` needs both `--from` and `--to` with a valid nonnegative ordered
range. The source labels them Unix timestamps without declaring a unit; establish
the service unit before a time-filtered query. Page starts at 1; limit is 1–100.
`--sort-by` is 1 created or 2 finished, `--side` is 0 all/1 long/2 short and
`--reduce-only` is 0 all/1 true/2 false. `stop` requires exactly one of `--id` or
`--text`. `stop-all` may filter contract and margin mode; without filters it stops
all chase orders for that settlement currency, requiring explicit broad authority.
The default list selects active orders explicitly. Apply the result checks in
[algorithm models](models/algo.md); a business rejection with HTTP 200 is still
a failure, and acceptance does not prove that parent or child orders completed.

```text
gate-cli cex spot pov create --pair BTC_USDT --side buy --amount 0.001 --participation-rate 10 --ttl 1h --limit-price 60000 --format json
gate-cli cex futures chase create --settle usdt --json '{"contract":"BTC_USDT","amount":"-1","price_limit":"0","reduce_only":true}' --format json
```
