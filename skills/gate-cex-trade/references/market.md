# Gate Market Data

## Scope

Read-only market discovery and public streams for Gate spot, leverage, futures, options, stocks, and TradFi. Product order/account operations remain in product references. Public streams do not authorize private writes.

## Public market interfaces

Read [market interfaces](markets.md) for product parameters, units and bounded
public compatibility reads, and [public streams](streams.md) for the optional
bounded WebSocket helper. Alpha uses REST only; no dedicated Alpha WS is
confirmed. For public market reads only, the bounded helper and fixed compatibility GETs
listed there are explicit exceptions to the shared CLI-only transport rule.
They do not permit generic HTTP clients, signing, private data or writes.
Trading, account and private-stream routes remain product-specific.

Cross-product subscriptions use separate product endpoints and channel-specific payloads; there is no unified WS endpoint. [Public streams](streams.md) preserves the full channel catalog, Stock ticker alias handling, ACK-versus-data distinction and product recovery rules.

## Product routing

| Product | REST market family | Public WebSocket channels | CLI read route |
| --- | --- | --- | --- |
| Spot | `/spot/currencies`, `/spot/currency_pairs`, `/spot/tickers`, `/spot/order_book`, `/spot/trades`, `/spot/candlesticks` | `spot.tickers`, `spot.book_ticker`, `spot.order_book`, `spot.order_book_update`, `spot.trades`, `spot.candlesticks` | `gate-cli cex spot market currencies`, `currency`, `pairs`, `pair`, `ticker`, `tickers`, `orderbook`, `candlesticks` |
| Leverage | Spot market endpoints plus margin rules | Reuses spot public streams | `gate-cli cex spot market ticker / orderbook / candlesticks` after margin mode is resolved |
| Perpetual futures | `/futures/{settle}/contracts`, `/tickers`, `/order_book`, `/trades`, `/candlesticks`, funding/liquidation families | `futures.tickers`, `futures.book_ticker`, `futures.order_book_update`, `futures.trades`, `futures.candlesticks` | `gate-cli cex futures market contract`, `tickers`, `orderbook` |
| Delivery futures | `/delivery/{settle}/contracts`, `/tickers`, `/order_book`, `/trades`, `/candlesticks`, insurance/risk families | Product-specific delivery channels | `gate-cli cex delivery market contracts`, `contract`, `tickers`, `order-book`, `trades`, `candlesticks` |
| Options | `/options/underlyings`, `/expirations`, `/contracts`, `/tickers`, `/order_book`, `/trades`, `/candlesticks` | `options.contract_tickers`, `options.ul_tickers`, `options.trades`, `options.order_book_update` | `gate-cli cex options market underlyings`, `expirations`, `contracts`, `contract`, `tickers`, `order-book` |
| TradFi/CFD | `/tradfi/symbols`, `/tradfi/symbols/categories`, `/tradfi/symbols/detail`, `/tradfi/symbols/{symbol}/tickers`, `/tradfi/symbols/{symbol}/klines` | Product-specific; symbol-detail reads may require APIv4 authentication | `gate-cli cex tradfi market categories`, `symbols`, `symbol`, `ticker`, `kline` |
| Stock/ETF | `/stock/symbols`, `/stock/market/{symbol}/ticker`, `/stock/market/{symbol}/orderbook`, `/stock/market/{symbol}/candlesticks` | Product-specific; do not assume CEX stream parity | Verify installed stock leaves; see [compatibility reads](markets.md#stock-read-compatibility) |
| Alpha | Alpha REST market routes | No dedicated Alpha kline/depth/WS route confirmed | `gate-cli cex alpha market currencies`, `tokens`, `tickers` |

## REST index

| Scenario | Endpoint / method | Required params | Optional params | Description |
| --- | --- | --- | --- | --- |
| Pair/contract rules | product `GET /spot/currency_pairs` or `GET /futures/{settle}/contracts` | product and settle where applicable | symbol/contract | Precision, multiplier, status, min/max. |
| Ticker | `GET /spot/tickers`, `GET /futures/{settle}/tickers`, `GET /options/tickers` | product context | symbol/contract | Last, mark/index where provided, volume. |
| Depth | product `GET /spot/order_book`, `GET /futures/{settle}/order_book`, or `GET /options/order_book` | symbol/contract | interval, limit, with_id | Snapshot; sequence continuity requires WebSocket. |
| Trades | product `GET /spot/trades`, `GET /futures/{settle}/trades`, or `GET /options/trades` | symbol/contract | limit, from, to | Public recent trades. |
| Candles | product `GET /spot/candlesticks`, `GET /futures/{settle}/candlesticks`, or `GET /options/candlesticks` | symbol/contract, interval | from, to, limit | Current candle is mutable until closed. |
| Funding/liquidation | futures `GET /futures/{settle}/funding_rate`, `GET /futures/{settle}/liq_orders` | settle, contract or settle | time/page filters | Futures-only public risk data. |

## WebSocket recovery

- Use the product's documented v4 WebSocket URL and settle context.
- For incremental depth, fetch a REST snapshot, subscribe, apply sequence ranges, and rebuild after a gap.
- Record source time and interval in analysis output. Do not treat stale ticker data as an execution quote.
- On reconnect, resubscribe and re-snapshot. The helper emits raw updates and never claims a rebuilt order book; private channels are outside its scope.

## Enums and constraints

- Candle intervals use values returned by the product API; do not assume all products share every interval.
- Incremental depth uses sequence fields `U`/`u` where present.
- Futures settle values include `usdt`, `btc`, and only values returned by the installed route.
- Market analysis is read-only. Run `--help` before adding filters; no private order/account stream or write command belongs here.
