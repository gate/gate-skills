# Gate Delivery Futures

Supplementary product background. Use the [canonical command contract](delivery-commands.md) for registered leaves, exact flags, units and safety variants, and [runtime rules](runtime.md) for execution. API fields in this file do not authorize direct private API calls or imply matching CLI flags.

## Scope

Delivery futures are a separate contract family from perpetual futures. Resolve `settle` and `contract` first; do not reuse perpetual-only position, close, or strategy assumptions.

## API / CLI index

The API paths below follow the official Gate API v4 delivery family. The CLI entries identify the local adapter surface; run the exact leaf `--help` before any write. The configured CLI snapshot currently fixes `settle=usdt`; API callers must still resolve and send the intended settle value.

| Scenario | Endpoint / method | CLI leaf | Required scope |
| --- | --- | --- | --- |
| Contract, ticker, book, trades, candles | `GET /delivery/{settle}/contracts`, `/tickers`, `/order_book`, `/trades`, `/candlesticks` | `gate-cli cex delivery market contract\|contracts\|tickers\|order-book\|trades\|candlesticks` | settle; contract for contract-scoped reads |
| Insurance and risk tiers | `GET /delivery/{settle}/insurance`, `/risk_limit_tiers` | `gate-cli cex delivery market insurance\|risk-limit-tiers` | settle |
| Account and ledger | `GET /delivery/{settle}/accounts`, `/account_book` | `gate-cli cex delivery account get\|book` | settle |
| Positions and margin | `GET /delivery/{settle}/positions`, `/positions/{contract}`; `POST .../margin`, `.../leverage`, `.../risk_limit` | `gate-cli cex delivery position list\|get\|update-margin\|update-leverage\|update-risk-limit` | settle; contract for one position |
| Orders and fills | `POST /delivery/{settle}/orders`; `GET/DELETE .../orders`, `GET .../orders/{id}`, `GET .../my_trades` | `gate-cli cex delivery order create\|list\|get\|cancel\|cancel-all\|my-trades` | settle; contract and order ID as required |
| Position and settlement history | `GET /delivery/{settle}/position_close`, `/liquidates`, `/settlements` | `gate-cli cex delivery position close\|liquidates\|settlements` | settle; time/contract filters |
| Price-trigger orders | `POST/GET/DELETE /delivery/{settle}/price_orders` and `.../{id}` | `gate-cli cex delivery price-trigger create\|list\|get\|cancel\|cancel-all` | settle; explicit contract scope |

## Execution rules

- Read contract size, expiry, precision, risk tier, current position, and leverage before calculating size.
- Confirm settle, contract, signed size or close scope, price/order type, time-in-force, reduce-only/close fields, and expiry assumptions. Reconcile order status and then position size.
- Delivery order, trigger, position, and settlement resources are distinct. Do not report a trigger or accepted order as a filled close.
- If the CLI adapter path or field differs from the official delivery API, block that write and use the incompatibility toast; do not fall back to a perpetual route.
