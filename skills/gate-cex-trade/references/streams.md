# Public Market WebSocket Interfaces

Use [public-market-stream.py](../scripts/public-market-stream.py) for bounded
public subscriptions. Python >=3.11 and an existing websockets>=15 are required;
the helper never installs dependencies, configures accounts or performs trades.
The existing futures-market-stream.py command remains compatible with perpetual
subscriptions. Alpha has no confirmed dedicated WS: use labeled REST polling.

## Execution and environment

From the repository root, for example:

```sh
python3 skills/gate-cex-trade/scripts/public-market-stream.py \
  --product spot --channel spot.tickers --payload '["BTC_USDT"]' --seconds 12
python3 skills/gate-cex-trade/scripts/public-market-stream.py \
  --product stocks --channel stock.tickers --payload '{"markets":["AAPL"]}' --seconds 12
```

Resolve the script relative to the installed resources elsewhere. Select the
product and canonical instrument from the user's context and metadata. Do not
invent a dated contract or substitute a stock with a same-name CFD.

All endpoints below are **production public WS**. Results label `environment`
as `production`. When the user requests a testing environment or the current
REST session uses a custom base, do not silently substitute these production
feeds or combine them with testing REST data. If no matching WS endpoint is
configured/documented, disclose that the requested environment is unavailable;
use production only when the user chooses it. Then validate instruments with
a per-command production REST override as described in
[REST environment rules](markets.md#rest-environment-and-compatibility-reads). The helper does not accept arbitrary
URLs or infer a testing WS address from GATE_BASE_URL.

| --product | Endpoint | Protocol | --settle |
| --- | --- | --- | --- |
| spot | `wss://api.gateio.ws/ws/v4/` | Spot v4 | Not applicable |
| leverage | Same as Spot | Spot shared market prices | Not applicable |
| perpetual | `wss://fx-ws.gateio.ws/v4/ws/{settle}` | Futures v4 | Required: btc/usdt/usd1 |
| delivery | `wss://fx-ws.gateio.ws/v4/ws/delivery/usdt` | Delivery v4 | Required: usdt |
| options | `wss://op-ws.gateio.live/v4/ws` | Options v4 | Not applicable |
| stocks | `wss://fx-ws.gateio.ws/v4/ws/stock` | Stock v1 | Not applicable |
| cfd | `wss://fx-ws.gateio.ws/v4/ws/tradfi` | TradFi v1 | Not applicable |

One invocation selects one public channel. Arrays contain 1–20 nonempty strings,
each <=128 characters without control characters. Object payloads are accepted
only for the documented ticker or option schemas below, with <=20 total symbol
strings and <=8KiB encoded payload. Unknown/private channels and object fields
are rejected. Do not supply credentials or private subscriptions.

`--seconds` is a 1–60 second total budget including connection and at most one
reconnect (default 12). Closing may take up to 2 extra seconds. `--max-messages`
limits retained raw business samples to 1–100 (default 10); remaining updates
are counted until time expires. This is bounded observation, not a background
service. WS ping/pong, 1MiB messages and queue size 16 bound resource use.

## Spot and Leverage

P denotes a metadata-validated pair. Leverage uses these same public prices;
account margin modes do not create separate price streams.

| Channel | Payload |
| --- | --- |
| spot.tickers / spot.trades / spot.book_ticker | `[P]` |
| spot.order_book | `[P,"20","100ms"]` |
| spot.order_book_update | `[P,"100ms"]` |
| spot.obu | `["ob.BTC_USDT.50"]` (embed the selected pair) |
| spot.rpi_order_book | `[P,"20","100ms"]` |
| spot.rpi_obu | `["rpi_ob.BTC_USDT.50"]` (embed the selected pair) |
| spot.candlesticks | `["1m",P]` |

Trade/size units are base-asset quantities. Ticker latest price is not BBO.
Candles retain server `t` and closure `w`; an open bar can change. RPI/OBU use
their own layouts and reset semantics, not a generic full-depth assumption.

## Perpetual and Delivery

[Perpetual channel parameters and units](futures-streams.md) cover 13 public
channels. The shared helper accepts `--product perpetual` with those payloads;
the old entry without --product retains perpetual behavior.

Delivery currently supports only USDT settlement: the BTC WS address returned
HTTP 404 in the 2026-10-29 retest and is rejected before connecting.
Delivery supports the following seven channels on its own dated-contract endpoint:

| Channel | Payload (D is a returned dated contract) |
| --- | --- |
| futures.tickers / futures.trades / futures.book_ticker | `[D]` |
| futures.order_book | `[D,"20","0"]` |
| futures.order_book_update | `[D,"100ms","20"]` |
| futures.obu | `["ob.<dated-contract>.100"]` or `["ob.<dated-contract>.20"]` |
| futures.candlesticks | `["1m",D]` |

Delivery OBU accepts only levels 20 and 100; the helper rejects other levels
before connecting. Perpetual OBU has its own supported levels.
Preserve settlement, expiry and contract multipliers. A futures.* channel name
does not make a Delivery contract a perpetual. Decimal sizes are requested with
X-Gate-Size-Decimal:1 for both products. Unsupported intervals/depths or contracts
are errors; do not silently change the user's expiry or settlement.

## Options

O is a returned full option contract, U is its returned underlying, e.g. BTC_USDT.

| Channel | Array payload |
| --- | --- |
| options.contract_tickers / options.trades / options.mark_prices | `[O]` |
| options.settlements / options.contracts / options.book_ticker | `[O]` |
| options.ul_tickers / options.ul_trades / options.ul_price | `[U]` |
| options.contract_candlesticks | `["1m",O]` |
| options.ul_candlesticks | `["1m",U]` |
| options.order_book | `[O,"20","0"]` |
| options.order_book_update | `[O,"100ms","20"]` |

The seven contract-scoped channels other than order_book/order_book_update also
accept objects: `{"underlyings":["BTC_USDT"]}` and/or `{"contracts":[O]}`.
At least one list must be nonempty. contract_candlesticks objects additionally
require `"interval":"1m"`; contract_tickers alone permits `"change_from"`
with 24h/utc0/utc8. Server expansion limits apply; report limit errors rather
than retrying wider subscriptions. Underlying channels use their array form.

Distinguish premium, IV, mark, bid/ask and underlying prices. Low activity may
produce ACK without trades or new candles. Settlement events are not a history
query; use REST for past expirations rather than substituting current prices.

## Stocks

| Channel | Payload |
| --- | --- |
| stock.tickers | `{"markets":["AAPL"]}` |
| stock.orderbooks | `["AAPL"]` |
| stock.kline | `["1m","AAPL","false"]` |

Ticker requires the object schema, unlike depth/candles. Keep symbol, exchange,
quote_currency, last_price and status_code from the actual result. On the stock
endpoint only, the helper accepts `tspot.tickers` as a ticker compatibility alias
and retains its original channel in evidence. A server update can precede ACK.

| status_code | Session meaning |
| --- | --- |
| 1 / 2 / 3 / 4 | Pre-market / post-market / regular / closed |
| 5 / 6 | US gt_lp / Hong Kong or Korea gt_lp session |

Keep unknown codes raw. `status=open` alone is insufficient to identify regular
hours; do not infer Gate's session from a conventional market clock. Order-book
bid/ask is not a substitute for last trade. Missing sizes remain unknown.

stock.kline interval examples: 1m/5m/15m/30m/1h/4h/1d/1w/1M/30d. The optional
third argument is string true/false; use true for US extended hours only when
requested. This is incremental subscription, not historical from/to retrieval.
For a request about **today**, compare bar.t to the exchange-local trading date
(e.g. America/New_York for US stocks), state actual bar dates, window and closure,
and keep server event time separate from receipt time. An old bar or no update
means today's data was not obtained; never call it today's complete K-line set.
A short successful live subscription does not supply the rest of today's history.

## CFD / TradFi

| Channel | Payload |
| --- | --- |
| tradfi.tickers | `{"markets":["XAUUSD"]}` |
| tradfi.order_book | `["XAUUSD"]` |
| tradfi.candlesticks | `["1m","XAUUSD"]` |

The order_book channel supplies BBO, not full L2 depth. Preserve each server time
unit and the selected public symbol. Do not use a same-name CFD for a stock query.
For REST kline, prefer the API-compatible interval documented in markets.md.
The CLI defaults to `1m` and maps `M1/M15/H1/H4/D1` to `1m/15m/1h/4h/1d`.
This CLI mapping does not apply to WS payloads; use the documented WS intervals.

## Alpha

No dedicated public Alpha WS is confirmed. Use the public REST interfaces in
[markets.md](markets.md#alpha) and label polling as snapshots, not a live stream.

## Evidence and depth continuity

JSON Lines output contains start/ack/message/disconnect/summary, selected product,
production endpoint, raw server fields, separate receipt time and per-connection
ACK/update counts. `data` means last connection confirmed the subscription and
provided a nonempty object/array; independently inspect instrument/time/fields.
`ack_only` exits 0 but only confirms subscription, not business receipt.
`data_without_ack`, `no_confirmation`, `error` exit nonzero. Empty result does
not count as business data. Preserve unknown/zero fields, decimal strings and
large integers and numeric decimal precision, retaining JSON numbers as numbers.
Nonfinite NaN/Infinity values are invalid JSON and fail the observation;
distinguish server errors from legitimate no-event windows.

At most one abnormal-disconnect/upgrade recovery resubscribes within the same
budget; old ACKs do not confirm the new connection. Raw depth is not a local
book: order_book_rebuilt is always false. If a caller needs a reconstructed book,
use the product's validated REST snapshot and incremental sequence/reset rules;
a gap or disconnect invalidates the old book. Do not call raw incremental
receipt or successful resubscription a verified book rebuild.

## Official sources

- [Spot](https://www.gate.com/docs/developers/apiv4/ws/en/)
- [Perpetual](https://www.gate.com/docs/developers/futures/ws/zh_CN/)
- [Delivery](https://www.gate.com/docs/developers/delivery/ws/en/)
- [Options](https://www.gate.com/docs/developers/options/ws/en/)
- [Stocks](https://www.gate.com/docs/developers/stock/ws/en/)
- [CFD](https://www.gate.com/docs/developers/cfd/ws/en/)
