# Gate Spot

Supplementary product background. Use the [canonical command contract](spot-commands.md) for registered leaves, exact flags, units and safety variants, and [runtime rules](runtime.md) for execution. API fields in this file do not authorize direct private API calls or imply matching CLI flags.

## Scope

Gate API v4 spot market, account and order operations. This reference supplements the canonical command contract; private operations use the shared CLI boundary. Margin borrowing is routed through `margin.md`/`unified.md`.

## Route / CLI

Run the complete leaf command with `--help` before execution. Read commands are safe to run without a write confirmation; order, trigger, batch, and POV writes require the workflow confirmation.

| Command | Required inputs | Key return fields | Common errors |
| --- | --- | --- | --- |
| `gate-cli cex spot market currencies` | none | currency, chain, delisted state | unsupported currency |
| `gate-cli cex spot market pairs` | none | pair list | request error |
| `gate-cli cex spot market pair` | `--pair` | base, quote, precision, min/max | pair not found, market closed |
| `gate-cli cex spot market tickers` | none | last, change, high, low, base/quote volume | invalid pair |
| `gate-cli cex spot market ticker` | `--pair` | one-pair ticker | invalid pair |
| `gate-cli cex spot market orderbook` | `--pair` | asks, bids, update time | invalid depth or pair |
| `gate-cli cex spot market candlesticks` | `--pair`, interval | candles, interval | invalid interval |
| `gate-cli cex spot order list` | `--pair`, optional status | order id, status, amount, filled | invalid filter |
| `gate-cli cex spot order get` | `--id`, `--pair` | order detail | order not found |
| `gate-cli cex spot order my-trades` | optional pair | trade id, price, amount, fee | order not found |
| `gate-cli cex spot account list` | none (`--all` only in the fallback CLI) | balances | auth, insufficient permission; currency filtering is API-only |
| `gate-cli cex spot account get` | currency | one balance | auth, currency unavailable |
| `gate-cli cex spot account book` | optional currency | ledger entries | auth, invalid filter |
| `gate-cli cex spot account batch-fee` | pair list | fee map | auth, pair unavailable |
| `gate-cli cex spot order buy` (market) | pair, `--quote` | order id, status, left, filled | `--quote` is the quote-currency amount; precision, balance, market closed |
| `gate-cli cex spot order buy` (limit) | pair, `--amount`, `--price` | order id, status, left, filled | `--amount` is base-currency quantity; precision, balance, market closed |
| `gate-cli cex spot order sell` | pair, `--amount` | order id, status, left, filled | `--amount` is base-currency quantity; precision, balance, market closed |
| `gate-cli cex spot order amend` | order id or amended field | amended order fields | order not open, invalid price/amount |
| `gate-cli cex spot order batch-amend` | exact batch | per-order amended fields | batch mismatch |
| `gate-cli cex spot order cancel` | `--pair` plus id or `--all` | cancelled order id | order already terminal |
| `gate-cli cex spot order batch-cancel` | explicit set/scope | cancelled order ids | batch mismatch |
| `gate-cli cex spot order batch-create` | exact order list | per-order ids/status | one or more invalid orders |
| `gate-cli cex spot order cross-liquidate` | pair, amount, price | cross-margin liquidation fields | Not mapped by this skill; do not treat it as an ordinary spot order. |
| `gate-cli cex spot price-trigger create` | pair, trigger, order fields | trigger id, status, rule | trigger direction, scope, or precision error |
| `gate-cli cex spot price-trigger get` | trigger id | trigger fields | trigger not found |
| `gate-cli cex spot price-trigger list` | optional pair/status | trigger ids/status | invalid filter |
| `gate-cli cex spot price-trigger cancel` | trigger id | cancelled id | trigger already terminal |
| `gate-cli cex spot price-trigger cancel-all` | explicit pair/scope | cancelled ids | missing scope |
| `gate-cli cex wallet market trade-fee` | optional pair | maker/taker fee | account or pair unavailable |

## Account (auth required)

| Endpoint / method | Required params | Optional params | Description |
| --- | --- | --- | --- |
| `GET /spot/accounts` | none | `currency` | Available, locked, and total spot balances. |
| `GET /spot/account_book` | none | `currency`, `page`, `limit`, `from`, `to`, `type` | Spot ledger entries and fee/transfer records. |
| `GET /spot/fee` | none | `currency_pair` | Current pair-level maker/taker fee. |
| `GET /spot/batch_fee` | pair list | none | Fee map for several pairs. |

## General

| Endpoint / method | Required params | Optional params | Description |
| --- | --- | --- | --- |
| `GET /spot/currencies` | none | `currency` | Currency metadata and withdrawal/trading status. |
| `GET /spot/currency_pairs` | none | none | Pair rules, precision, min amount, and trading status. |
| `GET /spot/currency_pairs/{currency_pair}` | `currency_pair` path | none | One pair's live rules. |
| `GET /spot/time` | none | none | Exchange server time for request timestamp checks. |

## Market Data

| Endpoint / method | Required params | Optional params | Description |
| --- | --- | --- | --- |
| `GET /spot/tickers` | none | `currency_pair`, `timezone` | Latest ticker values. |
| `GET /spot/order_book` | `currency_pair` | `interval`, `limit`, `with_id` | Order book snapshot. Incremental reconstruction requires the product WebSocket stream. |
| `GET /spot/trades` | `currency_pair` | `limit`, `last_id`, `from`, `to` | Recent public trades. |
| `GET /spot/candlesticks` | `currency_pair`, `interval` | `from`, `to`, `limit` | OHLCV candles; the current candle can change until closed. |

## Trade (auth required)

| Endpoint / method | Required params | Optional params | Description |
| --- | --- | --- | --- |
| `POST /spot/orders` | `currency_pair`, `side`, `amount`, `type` | `price`, `time_in_force`, `text`, `account`, `auto_borrow`, `auto_repay`, `stp_*` | Create a limit or market order. Keep base/quote amount semantics from the pair rules. |
| `GET /spot/orders` | `status` (open or finished) | `currency_pair`, `page`, `limit`, `from`, `to` | List open or historical orders by status. |
| `GET /spot/open_orders` | none | `currency_pair` | List all open orders grouped by pair. |
| `GET /spot/orders/{order_id}` | `order_id`, `currency_pair` | none | Query one order and remaining/fill state. |
| `DELETE /spot/orders/{order_id}` | `order_id`, `currency_pair` | none | Cancel one open order. |
| `DELETE /spot/orders` | `currency_pair` | `side`, `account` | Batch cancel in an explicit pair/scope. |
| `POST /spot/cancel_batch_orders` | exact order id list | none | Batch cancel with per-order results. |
| `PATCH /spot/orders/{order_id}` | `order_id`, `currency_pair` | `amount`, `price`, `amend_text` | Amend an open order where the installed skill exposes it. Verify the response; this is not cancel-and-replace. |
| `POST /spot/amend_batch_orders` | exact order list | per-order amount/price/text | Batch amend. Confirm the exact list and inspect per-order result. |
| `GET /spot/my_trades` | `currency_pair` | `order_id`, `limit`, `page`, `from`, `to` | Authenticated fills. |
| `POST /spot/price_orders` | pair, trigger rule, trigger price, order body | `price`, `amount`, `side`, `text` | Create a conditional spot order. It is not a native OCO/OTO relationship. |
| `GET /spot/price_orders` | `status` | pair, page, limit | List conditional orders. |
| `GET /spot/price_orders/{order_id}` | `order_id` | none | Query one conditional order. |
| `DELETE /spot/price_orders/{order_id}` | `order_id` | none | Cancel one conditional order. |

For a specific spot conditional-order lookup, require a positive `order_id` and validate the spot response shape before reconciliation: `market` must be non-empty, `trigger.price` and `trigger.rule` must be present, and `put.side` and `put.amount` must be present. An empty object or missing required fields is a failed read and must use the conditional-order empty-result toast in `workflows.md`; do not apply the futures `initial.*` schema to a spot response.

## Strategy / split and POV

These endpoints belong to the spot route. They are POV-like execution, not Binance TWAP/VP parity. No mapped endpoint should be simulated with repeated ordinary orders.

| User intent | Gate endpoint / CLI | Required inputs | Boundary |
| --- | --- | --- | --- |
| TWAP or VP | No confirmed Gate API v4 endpoint | none | Use the unavailable-operation toast; do not emulate with repeated ordinary orders. |

| Endpoint / method | Required params | Optional params / enum | Description |
| --- | --- | --- | --- |
| `POST /spot/pov_orders` | `currency_pair`, `side`, `amount`, `participation_rate`, `ttl` | `participation_rate`: `5`, `10`, `20`, `40`; `ttl`: `1h`, `6h`, `12h`, `1d`…`7d`; `limit_price`, `trigger_price`, `text` (`t-` prefix) | Create a POV-like split order. Amount remains the native spot amount. |
| `GET /spot/pov_orders` | `status` | `currency_pair`, `side`, `page`, `limit` | List POV orders. `status`: `open` or `finished`. |
| `GET /spot/pov_orders/{order_id}` | `order_id` | none | Query one POV order. |
| `DELETE /spot/pov_orders/{order_id}` | `order_id` | none | Cancel one POV order. |
| `DELETE /spot/pov_orders` | none | `currency_pair` | Cancel POV orders in an explicit pair scope. |

## Enums

- `side`: `buy`, `sell`.
- `type`: `limit`, `market`.
- `time_in_force`: `gtc`, `ioc`, `fok`, `poc` where supported by the pair/order type.
- `account`: `spot`, `margin`, `unified`.
- Spot trigger status: `open`, `cancelled`, `finish`, `failed`, `expired`.
- `status`: `open`, `closed`, `cancelled`, `finished` (the API may expose product-specific terminal names).
- `trigger rule`: `>=` or `<=` against the configured reference price.
- POV status: `CREATED`, `CANCELING`, `RUNNING`, `COMPLETED`, `EXPIRED`, `TERMINATED`.

## Constraints

- Read pair rules before converting quote amount, base amount, or price precision.
- The configured CLI snapshot exposes market-buy `--quote` (quote currency), limit-buy `--amount` plus `--price` (base currency), and sell `--amount` (base currency). API v4 also supports fields such as `time_in_force`, `account`, `auto_borrow`, `auto_repay`, and STP where the selected route exposes them. If the CLI leaf omits a requested field, stop that operation; do not switch to a private API executor or describe the whole product capability as absent.
- Do not claim Gate spot has Binance SOR/OCO/OTO/OTOCO parity from a price trigger or POV endpoint.
- POV has five registered CLI leaves in [algorithm commands](algo-commands.md). Verify the installed leaf, JSON fields, native amount, interval, duration and price limits against that contract. Missing required capabilities stop the operation; never simulate it with repeated ordinary orders.
- `gate-cli` names above are documented routes; run the exact leaf command with `--help` before use. Margin/unified trades must not silently fall back to ordinary spot when the selected executor cannot express the account or auto-borrow/repay fields.
