# Gate Stock

Supplementary product background. Use the [canonical command contract](stocks-commands.md) for registered leaves, exact flags, units and safety variants, and [runtime rules](runtime.md) for execution. API fields in this file do not authorize direct private API calls or imply matching CLI flags.

## Scope

Gate API v4 stock and ETF trading is a separate product from TradFi CFD. The reviewed source registers `gate-cli cex stock`, including account, market, order and position leaves. Check the exact installed leaf and all requested flags; source support is not evidence of deployment or account eligibility.

## API contract

| Scenario | Endpoint / method | Required inputs | Key fields and boundary |
| --- | --- | --- | --- |
| Symbols and market metadata | `GET /stock/symbols` | none | Symbol, exchange, session, trading mode, precision, limits. Read before an order. |
| Ticker | `GET /stock/market/{symbol}/ticker` | symbol | Latest and extended-hours prices where returned. |
| Order book | `GET /stock/market/{symbol}/orderbook` | symbol | Price levels and user-order marker. |
| Candlesticks | `GET /stock/market/{symbol}/candlesticks` | symbol, interval | Public market history. |
| Open orders | `GET /stock/orders` | none | Optional symbol filter; status is an integer returned by the API. |
| Create order | `POST /stock/orders` | `symbol`, `volume`, `side`, `price_type`, `trading_session`, `time_in_force` | `side=1` sell, `side=2` buy; `price_type=market` or `limit`; `price` is required for limit orders. |
| Amend/cancel order | `PUT /stock/orders/{order_id}`, `DELETE /stock/orders/{order_id}` | order id | Re-read the order before an amend or cancel. |
| Positions | `GET /stock/positions` | none | Position quantity, available quantity, cost and P&L. |
| Close position | `POST /stock/positions/close` | `symbol`, `close_type` | `close_type=1` partial and requires `close_volume`; `close_type=2` full. |
| Transactions | `GET /stock/transactions` | none | Account and trade records; use explicit time/page filters where available. |

## Workflow boundary

Use stock session, time-in-force, price, and volume exactly as returned by the API. Do not reuse CFD `price_type=trigger`, CFD TP/SL fields, TradFi position IDs, or perpetual futures signed-size rules. Confirm symbol, exchange/session, side, native volume, price type, price, and close type. Reconcile each order by order ID and each close by the post-write position; a submitted close is not proof that the position is flat.

Private stock operations use only the registered CLI contract. Missing ticker/history CLI capabilities do not authorize a private API fallback; approved public-market exceptions remain in [market rules](market.md). Never route stock orders to `/tradfi/orders`.
