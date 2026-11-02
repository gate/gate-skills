# Gate Futures

Supplementary product background. Use the [canonical command contract](perpetual-commands.md) for registered leaves, exact flags, units and safety variants, and [runtime rules](runtime.md) for execution. API fields in this file do not authorize direct private API calls or imply matching CLI flags.

## Scope

Gate API v4 perpetual futures. This package maps USDT-settled perpetuals; resolve `settle=usdt` explicitly. Coin-margined `btc`, `usd1`, delivery, USDC, and portfolio-only routes use separate contracts and must not be inferred from this file.

## Route / CLI

Run the complete leaf command with `--help` first. The API paths below follow the official Gate API v4 futures reference; the CLI entries follow the supplied source snapshot. Writes require the confirmation and reconciliation workflow.

| Command | Required inputs | Key return fields | Common errors |
| --- | --- | --- | --- |
| `gate-cli cex futures market contract` | `--settle`, `--contract` | contract size, leverage limits, status | contract not found |
| `gate-cli cex futures market tickers` | settle, optional contract | mark/index/last, volume | invalid settle or contract |
| `gate-cli cex futures market orderbook` | settle, contract | bids/asks | invalid depth or contract |
| `gate-cli cex futures market funding-rate` | `--settle`, `--contract` | timestamp, rate | invalid contract/settle or error envelope; validate the returned list |
| `gate-cli cex futures market insurance` | `--settle` | timestamp, balance | an `error` envelope is a failed read even when the process exits 0 |
| `gate-cli cex futures market stats` | `--settle`, `--contract` | time, open interest, liquidation metrics | an empty list is not success evidence without confirmed scope |
| `gate-cli cex futures market risk-limit-tiers` | `--settle` | tier, risk limit, max leverage | invalid settle or oversized/unbounded output |
| `gate-cli cex futures market index-constituents` | `--settle`, `--index` | exchange and constituent symbols | index name/settle error; this is a public read, not a contract filter |
| `gate-cli cex futures market liquidations` | `--settle` | time, contract, size, order size | invalid settle/contract or empty result |
| `gate-cli cex futures account get` | settle | equity, available, unrealized PnL | auth, account mode |
| `gate-cli cex futures position get` | settle, contract | size, entry, mark, leverage | position not found |
| `gate-cli cex futures position list` | settle | position list | invalid settle |
| `gate-cli cex futures account position-mode` | settle, `--mode` | account position mode | mode blocked by positions/orders; the snapshot implementation path must match the official API before a write |
| `gate-cli cex futures order get` | settle, order id | id, status, size, left, fill | order not found |
| `gate-cli cex futures order list` | settle, optional filters | order list | invalid filter |
| `gate-cli cex futures order long` | settle, contract, size | order id, status | margin, leverage, precision |
| `gate-cli cex futures order short` | settle, contract, size | order id, status | margin, leverage, precision |
| `gate-cli cex futures order add` | settle, contract, size | order id, status | Legacy/advanced leaf; verify with `--help` before use |
| `gate-cli cex futures order close` | settle, `--contract`; optional `--side`, `--size` | close order and position | no position, reduce-only conflict |
| `gate-cli cex futures order remove` | settle, `--contract`, `--size`; optional price | reduced position state | precision, position-side, or reduce-only conflict |
| `gate-cli cex futures order amend` | settle, order id, amended field | amended order | order terminal or version mismatch |
| `gate-cli cex futures order cancel` | settle, order id | cancelled id | order terminal |
| `gate-cli cex futures order batch-cancel` | settle, explicit set | cancelled ids | batch mismatch |
| `gate-cli cex futures order bbo` | settle, contract, size, direction | BBO order result | route or direction unsupported |
| `gate-cli cex futures price-trigger create` | settle, trigger fields | trigger id/status | trigger direction, TP/SL restriction |
| `gate-cli cex futures price-trigger list` | settle, optional contract | trigger list | invalid filter |
| `gate-cli cex futures price-trigger get` | settle, trigger id | trigger fields | trigger not found |
| `gate-cli cex futures price-trigger update` | settle, trigger id, mapped fields | updated trigger | TP/SL restriction |
| `gate-cli cex futures price-trigger cancel` | settle, trigger id | cancelled id | trigger terminal |
| `gate-cli cex futures price-trigger cancel-all` | settle, explicit scope | cancelled ids | missing scope |
| `gate-cli cex futures position update-leverage` | settle, contract, leverage | leverage | open position or limit conflict |
| `gate-cli cex futures position update-cross-mode` | settle, contract, mode | mode | open position or mode conflict |
| `gate-cli cex futures position update-contract-leverage` | settle, contract, leverage | leverage | Update leverage for the selected position mode; verify the leaf help before use. |
| `gate-cli cex futures trail create` | settle, contract, amount | trail id/status | verify installed flags and the SDK request; diagnostic labels alone do not block the route |
| `gate-cli cex futures trail stop` | settle, trail id/text | stopped id | verify installed flags and the SDK request; diagnostic labels alone do not block the route |
| `gate-cli cex futures trail stop-all` | settle, contract scope | stopped ids | verify installed flags and the SDK request; diagnostic labels alone do not block the route |
| `gate-cli cex futures trail list` | settle, contract/status filters | trail list | verify installed flags and the SDK request; diagnostic labels alone do not block the route |
| `gate-cli cex futures trail get` | settle, trail id | trail detail | verify installed flags and the SDK request; diagnostic labels alone do not block the route |
| `gate-cli cex futures trail update` | settle, trail id, fields | updated trail | verify installed flags and the SDK request; diagnostic labels alone do not block the route |
| `gate-cli cex futures trail log` | settle, trail id | change log | verify installed flags and the SDK request; diagnostic labels alone do not block the route |
| `gate-cli cex futures order my-trades-timerange` | settle, optional contract/from/to/limit | historical fills | invalid time range |

## Account and position (auth required)

| Endpoint / method | Required params | Optional params | Description |
| --- | --- | --- | --- |
| `GET /futures/{settle}/accounts` | `settle` | none | Futures account equity, available balance, and margin. |
| `GET /futures/{settle}/positions` | `settle` | `holding`, `limit`, `offset` | Current positions; side semantics depend on single/dual mode. |
| `GET /futures/{settle}/positions/{contract}` | `settle`, `contract` | none | One contract position. |
| `GET /futures/{settle}/account_book` | `settle` | `contract`, `type`, `from`, `to`, `page`, `limit` | Futures ledger and realized PnL/fee records. |
| `POST /futures/{settle}/positions/{contract}/leverage` | `settle`, `contract`, leverage | `cross_leverage_limit` | Change leverage after checking current position and limits. |
| `POST /futures/{settle}/positions/{contract}/margin` | `settle`, `contract`, `change` | none | Add or remove isolated margin where supported. |
| `POST /futures/{settle}/positions/{contract}/risk_limit` | `settle`, `contract`, risk limit | none | Update risk tier; read tiers first. |
| `POST /futures/{settle}/set_position_mode` | `settle`, `position_mode` query | none | Official API path. Set `single`, `dual`, or `dual_plus`; only when no conflicting positions/orders remain. |
| `POST /futures/{settle}/positions/cross_mode` | `settle`, `contract`, `mode` | none | Set cross/isolated margin mode where supported. |
| `GET /futures/{settle}/risk_limit_tiers` | `settle` | page, limit | Risk-limit tiers and max leverage. |

## Market Data

| Endpoint / method | Required params | Optional params | Description |
| --- | --- | --- | --- |
| `GET /futures/{settle}/contracts` | `settle` | `contract` | Contract size, multiplier, settle, status, limits. |
| `GET /futures/{settle}/tickers` | `settle` | `contract` | Last, mark, index, funding and volume summary. |
| `GET /futures/{settle}/order_book` | `settle`, `contract` | `interval`, `limit`, `with_id` | Futures order book snapshot. |
| `GET /futures/{settle}/trades` | `settle`, `contract` | `limit`, `last_id`, `from`, `to` | Recent public trades. |
| `GET /futures/{settle}/candlesticks` | `settle`, `contract`, `interval` | `from`, `to`, `limit` | OHLCV candles. |
| `GET /futures/{settle}/funding_rate` | `settle`, `contract` | limit, from, to | Funding rate history. |
| `GET /futures/{settle}/insurance` | `settle` | limit, from, to | Insurance-fund history. |
| `GET /futures/{settle}/contract_stats` | `settle` | contract, interval | Contract statistics and open interest where exposed. |
| `GET /futures/{settle}/liq_orders` | `settle` | contract, limit, from, to | Public liquidation orders. |
| `GET /futures/{settle}/index_constituents/{index}` | `settle`, `index` | none | Index constituents used by the selected futures index. |

Public market leaves must be judged from the response envelope, not only the process exit code. A `200` response that contains an `error` object (including an error envelope emitted on CLI stderr) is a failed read. An empty array from a scoped metric query, such as `contract_stats`, is not proof that the metric is supported or that the resource is empty; keep the case `NOT_EXECUTED` or classify it as `FAIL_CONTRACT` until the query scope and service response are confirmed. Use the empty/structurally invalid read toast in `workflows.md`.

## Trade (auth required)

| Endpoint / method | Required params | Optional params | Description |
| --- | --- | --- | --- |
| `POST /futures/{settle}/orders` | `settle`, `contract`, signed `size`, `price` for limit, `tif` | `reduce_only`, `close`, `text`, `is_close`, `auto_size`, `stp_*` | Create a futures order. Sign/side semantics depend on position mode. |
| `GET /futures/{settle}/orders` | `settle`, `status` | `contract`, `last_id`, `limit`, `from`, `to` | List open or historical orders. |
| `GET /futures/{settle}/orders/{order_id}` | `settle`, `order_id` | `contract` | Query one order and `finish_as`. |
| `DELETE /futures/{settle}/orders/{order_id}` | `settle`, `order_id` | `contract` | Cancel one order. |
| `DELETE /futures/{settle}/orders` | `settle`, `contract` | none | Cancel all orders in an explicit contract scope. |
| `POST /futures/{settle}/batch_orders` | `settle`, exact order list | none | Batch create; inspect each result. |
| `POST /futures/{settle}/bbo_orders` | `settle`, contract, size, direction | level | Official API BBO order; the supplied CLI exposes `futures order bbo`. |
| `PUT /futures/{settle}/orders/{order_id}` | `settle`, `order_id` | `price`, `size`, `tif` | Amend an open order. Verify endpoint/version before use. |
| `POST /futures/{settle}/batch_amend_orders` | `settle`, exact order list | per-order price/size | Batch amend. |
| `POST /futures/{settle}/batch_cancel_orders` | `settle`, exact order list or contract scope | none | Batch cancel. |
| `GET /futures/{settle}/my_trades` | `settle` | contract, order, limit, from, to | Authenticated fills. |
| `GET /futures/{settle}/orders_timerange` | `settle`, time range | contract, page, limit | Historical orders by time range. |
| `GET /futures/{settle}/my_trades_timerange` | `settle`, time range | contract, page, limit | Official API historical fills by time range. |
| `GET /futures/{settle}/position_close` | `settle` | contract, time range | Position close history. |
| `GET /futures/{settle}/liquidates` | `settle` | contract, time range | Liquidation history. |
| `GET /futures/{settle}/auto_deleverages` | `settle` | contract, time range | ADL history. |

## Conditional orders and protection

| Endpoint / method | Required params | Optional params | Description |
| --- | --- | --- | --- |
| `POST /futures/{settle}/price_orders` | `settle`, contract, trigger rule/price, execution order | `size`, `price`, `reduce_only`, `close`, `text` | Conditional open/close or TP/SL. It is not automatically linked to a position. |
| `GET /futures/{settle}/price_orders` | `settle`, `status` | contract, page, limit | List conditional orders. |
| `GET /futures/{settle}/price_orders/{order_id}` | `settle`, `order_id` | none | Query trigger order. |
| `PUT /futures/{settle}/price_orders/amend/{order_id}` | `settle`, `order_id` | trigger/order fields | Amend a condition; API v4 versions require the id in the body as well. |
| `DELETE /futures/{settle}/price_orders/{order_id}` | `settle`, `order_id` | none | Cancel one trigger. |
| `DELETE /futures/{settle}/price_orders` | `settle` | contract | Cancel all triggers in scope. |

When querying one conditional order, require a positive `order_id` and validate the returned `initial` and `trigger` objects before reconciliation. `initial.contract`, a present `initial.price` that is non-empty and parseable as a finite decimal (JSON number or decimal string), and `trigger.price` are required fields for the mapped response; validate `trigger.rule` and `trigger.price_type` when returned. An empty object or empty `initial`/`trigger` (for example, `order_id=0`) is a failed read and must use the conditional-order empty-result toast in `workflows.md`.

If a conditional-order update returns `1077/APIOrderNotSupportUpdateTouchOrder`, treat it as an API limitation, do not retry the same update, and use the unavailable-operation toast.

## Strategy / autoorder

These are futures trail/chase execution families. They are not Binance TWAP/VP equivalents and are not exposed as a standalone algorithm route.

| User intent | Gate endpoint / CLI | Required inputs | Boundary |
| --- | --- | --- | --- |
| Time-slice, TWAP, VP, or futures POV | No confirmed Gate API v4 endpoint | none | Do not emulate with repeated ordinary orders; render the unavailable-operation toast. |

| Endpoint / method | Required params | Optional params / enum | Description |
| --- | --- | --- | --- |
| `POST /futures/{settle}/autoorder/v1/trail/create` | `contract`, `amount` | `activation_price` (0=immediate), `is_gte`, `price_type`, `price_offset`, `reduce_only`, `position_related`, `text`, `pos_margin_mode`, `position_mode` | Create a trailing autoorder. |
| `POST /futures/{settle}/autoorder/v1/trail/stop` | `id` or text | none | Stop one trail autoorder. |
| `POST /futures/{settle}/autoorder/v1/trail/stop_all` | `contract` | `related_position` | Stop all trail autoorders in scope. |
| `GET /futures/{settle}/autoorder/v1/trail/list` | `settle` | contract, is_finished, time/page/sort filters | List trail orders. |
| `GET /futures/{settle}/autoorder/v1/trail/detail` | `id` | none | Query one trail order. |
| `POST /futures/{settle}/autoorder/v1/trail/update` | `id` | amount, activation_price, price_offset | Update a trail order where enabled. |
| `GET /futures/{settle}/autoorder/v1/trail/change_log` | `id` | none | Query trail changes. |
| `POST /futures/{settle}/autoorder/v1/chase/create` | `contract`, `amount`, exactly one of `price_limit` or `offset_limit` | `settle`, `reduce_only`, `text`, `is_dual_mode`, `price_type`, `price_gap_type`, `price_gap_value`, `pos_margin_mode`, `position_mode` | Create a chase autoorder; positive amount buys and negative amount sells. |
| `POST /futures/{settle}/autoorder/v1/chase/stop` | `id`, `text`, `settle` | none | Stop one chase autoorder. |
| `POST /futures/{settle}/autoorder/v1/chase/stop_all` | `contract` | none | Stop all chase autoorders in scope. |
| `GET /futures/{settle}/autoorder/v1/chase/list` | `settle`, `sort_by` (1 created, 2 finished) | contract, is_finished, time/page/side/reduce_only filters | List chase autoorders. |
| `GET /futures/{settle}/autoorder/v1/chase/detail` | `id` | none | Query one chase autoorder. |

The reviewed Trail handlers call SDK methods constructing `/futures/{settle}/autoorder/v1/trail/*`. Legacy `/trail_orders*` error labels do not establish wire-path incompatibility. Check each installed leaf and required flag. Trail create still lacks `reduce_only`, `position_related`, and client `text` flags in the reviewed contract: stop a protection intent requiring them, while independently supported Trail reads or ordinary intents remain available. Chase has five registered leaves in [algorithm commands](algo-commands.md); verify their JSON fields and price guard. Do not approximate either family with repeated ordinary orders.

## Enums

- `settle`: execution route requires `usdt`; `btc` and `usd1` are discovery-only unless another skill explicitly supports them.
- `tif`: `gtc`, `ioc`, `fok`, `poc` where supported.
- `status`: `open`, `finished`; cancellation is represented by `finish_as=cancelled` where returned.
- `finish_as`: product-specific values such as `filled`, `cancelled`, `liquidated`, `ioc`, `auto_deleveraged`, `reduce_only`, `position_closed`.
- `margin mode`: API values `cross`, `isolated`; the installed futures position CLI expects `CROSS` or `ISOLATED`.
- `position mode`: `single`, `dual`, `dual_plus`.
- Trail `price_type`: `1` latest, `2` index, `3` mark. Chase `price_type`: `1` best bid/ask, `2` distance. Chase `price_gap_type`: `1` absolute, `2` percentage.
- Price-trigger CLI enums: `--trigger-rule 1` is `>=`, `2` is `<=`; `--price-type 0` is latest, `1` is mark, `2` is index. These values are for `price-trigger` only and must not be reused for trail/chase.
- Trail direction: `is_gte=true` is an upward trigger and `false` is downward; trail `amount` is positive for buy and negative for sell. Chase amount uses the same positive-buy/negative-sell convention.

## Constraints

- Read contract multiplier, size precision, risk tiers, settle, current position mode, and leverage before calculating a size.
- Closing/reversing must verify the position after the close leg; never infer a flat position from an accepted order.
- TP/SL, conditional, trail, and chase state are separate from position state. Report them separately.
- A protection intent (TP/SL, conditional close, or trailing protection) is executable only when the selected route exposes the required `reduce_only`, `close`, or `position_related` field. The configured CLI snapshot may omit some of these fields; stop the affected operation if the registered CLI cannot express them; never switch to a private API executor.
- The configured `futures order long|short` leaves may expose only contract, size, price, and settle. API v4 also supports fields such as `tif`, `reduce_only`, `close`, client text, and STP where the selected executor exposes them. Do not turn a CLI field omission into a product-level unsupported claim.
- `futures account position-mode` accepts `--mode`; the reviewed handler calls the SDK request for `/futures/{settle}/set_position_mode`. A legacy `/position_mode` diagnostic label does not prove a wire mismatch. Check installed capability, conflicting positions/orders, permission and resulting mode before reporting success.
- The fallback `futures order my-trades-timerange` leaf is available, while the official API path is `/futures/{settle}/my_trades_timerange`; preserve the official path in API calls and verify the CLI adapter before relying on it.
