# Perpetual Futures Public WebSocket

Official protocol: https://www.gate.com/docs/developers/futures/ws/zh_CN/
Endpoint: `wss://fx-ws.gateio.ws/v4/ws/{btc|usdt|usd1}`. Use the requested
settlement and a canonical perpetual contract returned by contract metadata.
This page describes Perpetual only; use [streams.md](streams.md) for the other
product routes and the shared helper. No API key, account login or trading operations are needed.

## Execution

Use the bounded [subscription helper](../scripts/futures-market-stream.py)
with Python >=3.11 and an existing `websockets>=15`. Missing dependencies are
reported; the helper never installs packages or changes credentials/config.
For example, from the repository root (resolve paths against the installed
skill directory elsewhere):

```sh
python3 skills/gate-cex-trade/scripts/futures-market-stream.py \
  --settle usdt --channel futures.tickers --payload '["BTC_USDT"]' --seconds 12
```

`--settle`, `--channel` and `--payload` are required. Payload is a JSON array
of 1–20 strings, each 1–128 characters, without control characters. Use the
channel-specific schema below; the server validates instrument/parameter
availability. The helper only accepts the 13 listed public channels and fixed
production endpoints. It always requests `X-Gate-Size-Decimal: 1` so decimal
contract sizes aren't rounded down. User-supplied headers/URLs/auth are absent.

`--seconds` is the total connection/observation/retry budget, 1–60 seconds
(default 12); closing may take up to 2 additional seconds. This is bounded
observation, not a permanent background subscription. `--max-messages` limits
raw business samples to 1–100 (default 10); subsequent updates are still counted
until the budget expires. Each sample retains server fields and a separate
`received_at`. Keep larger output in a temporary evidence file.

## Public channels and payloads

F below means a concrete canonical contract, e.g. BTC_USDT for USDT settlement;
examples are schemas, not a default product or instrument selection policy.

| Channel | Payload | Data |
| --- | --- | --- |
| `futures.tickers` | `[F]` | Latest/mark/index prices and ticker statistics |
| `futures.trades` | `[F]` | Public executions; distinguish internal takeover trades (`is_internal`) |
| `futures.book_ticker` | `[F]` | Best bid/ask, not full depth |
| `futures.order_book` | `[F,"20","0"]` | Periodic limited-depth full snapshots (`event=all`); allowed depths 1/5/10/20/50/100, accuracy 0 |
| `futures.order_book_update` | `[F,"100ms","20"]` | Raw U/u depth updates; depths 20/50/100; 20ms only allows depth 20 |
| `futures.obu` | `["ob.BTC_USDT.400"]` | V2 full/incremental messages; stream name embeds the selected contract |
| `futures.rpi_order_book` | `[F,"20","0"]` | RPI full snapshots; same schema as order_book |
| `futures.rpi_obu` | `["rpi_ob.BTC_USDT.400"]` | RPI V2 messages; use its own full/incremental semantics |
| `futures.candlesticks` | `["1m",F]` | OHLC and volume updates; `w` identifies window closure |
| `futures.contract_stats` | `[F,"1m"]` | OI, long/short and taker statistics; second parameter is the statistics window |
| `futures.public_liquidates` | `[F]` | Public liquidation events, not personal liquidations |
| `futures.contract_info` | `[F]` | Contract information changes |
| `futures.adl_warning` | `[F]` | Market ADL risk warnings; all-normal subscriptions may only return ACK |

Candle intervals: `10s/1m/5m/15m/30m/1h/4h/8h/1d/7d`.
Statistics windows: `1m/5m/15m/30m/1h/4h/8h/1d/3d/7d`.
For multi-contract payloads and special selectors, follow the official channel
schema; do not apply the simple `[F]` form to depth, OBU or candle channels.
Keep contract sizes/decimal strings unchanged and obtain the contract multiplier
before expressing base-asset quantities. Price types and timestamps remain distinct.

## Evidence, errors and recovery

Output is JSON Lines: `start`, `ack`, bounded raw `message` samples,
`disconnect` when applicable, and `summary` with per-connection counts.

- `data`: last connection confirmed subscription and supplied nonempty business
  `result` objects/arrays. This proves receipt, not independent correctness of
  every field. Inspect the target contract, server time and fields you need.
- `ack_only`: confirmed subscription, no nonempty business payload within the
  budget. Exit 0 means the observation completed, not that business data was
  verified. Low-frequency events can legitimately remain ACK-only.
- `data_without_ack` / `no_confirmation`: business receipt without subscription
  confirmation / no confirmation and no data; both exit nonzero.
- `error`: server rejection, malformed message, protocol/network error or exhausted
  retry budget; exits nonzero. Never replace missing fields with invented values.

Business data may precede ACK. Empty results do not count as verified data.
WS ping/pong is enabled. Abnormal disconnects or the official `futures.system`
upgrade notification trigger at most one reconnect within the same total budget;
the helper resubscribes and resets connection confirmation, retaining separate
evidence for both connections. More failures stop explicitly. No credentials,
cache, database or local account configuration is read.

## Raw depth is not a reconstructed order book

The helper does not build a local book: `order_book_rebuilt` is always false.
For `order_book_update`, callers needing a current book must buffer increments,
obtain the existing public REST order_book with `with_id=true` and a limit equal
to subscribed depth, then bridge `U <= snapshot_id+1 <= u`. Skip stale updates;
a sequence gap requires a fresh snapshot. Sizes replace previous values; zero
removes a level. Empty bid/ask updates still advance sequence/time. Handle the
`full` flag as a replacement rather than an ordinary delta. OBU uses its own
stream/full layout; do not blindly reuse another channel's parser.

After disconnect, discard the old local book and rebuild from new evidence.
Successful resubscription does not prove sequence continuity, book rebuilding,
or recovery of events missed during downtime. Stock-specific ticker/K-line capabilities and their history boundaries are
documented in [streams.md](streams.md#stocks).
