# Gate Options

Supplementary product background. Use the [canonical command contract](options-commands.md) for registered leaves, exact flags, units and safety variants, and [runtime rules](runtime.md) for execution. API fields in this file do not authorize direct private API calls or imply matching CLI flags.

## Scope

Gate options market, account, order, position, stream, MMP, settlement, and position-close records. This file merges the ordinary order route with the three option supplements. A documented endpoint without a compatible registered CLI leaf (or an explicitly approved public market transport) is read-only reference material until that executor is verified.

## Route / CLI

Run each leaf command with `--help` before use. The API paths below follow the official Gate API v4 options reference; the CLI entries follow the supplied source snapshot. Core order create/cancel/amend and any MMP, account-wide cancel, or settlement action require the workflow confirmation.

| Command | Required inputs | Key return fields | Common errors |
| --- | --- | --- | --- |
| `gate-cli cex options market underlyings` | optional filter | underlying names | unsupported underlying |
| `gate-cli cex options market expirations` | `--underlying` | expiry list | invalid underlying |
| `gate-cli cex options market contracts` | `--underlying`, optional expiry | contract list and multiplier | invalid underlying/expiry |
| `gate-cli cex options market contract` | `--contract` | multiplier, strike, call/put, order limits | contract not found |
| `gate-cli cex options market order-book` | contract | asks, bids, timestamp | invalid depth |
| `gate-cli cex options market tickers` | `--underlying` | mark, bid/ask, IV, volume | no market data |
| `gate-cli cex options account get` | none | equity, available, margin | auth or account unavailable |
| `gate-cli cex options position list` | optional underlying | size, entry, mark, PnL | contract filter error |
| `gate-cli cex options position my-trades` | `--underlying` | trade id, price, size, fee | invalid underlying or contract |
| `gate-cli cex options order list` | `--status` (`open` or `finished`) | order id, status, left, fill | invalid filter |
| `gate-cli cex options order create` | `--contract`, `--size` | `--price`, `--tif` | `price=0` plus IOC is the mapped market form; the reviewed CLI exposes `--close` and `--reduce-only`; full close uses `--close --size 0`, partial close uses signed nonzero `--size` with `--reduce-only`. MMP and mark-IV order fields still require installed flag support |
| `gate-cli cex options order cancel` | order id | cancelled id | order terminal |
| `gate-cli cex options order cancel-all` | explicit filters or confirmed scope | cancelled ids | scope missing |
| `gate-cli cex options order amend` | `--contract`, `--id`, `--price` | `--size` | order not open |
| `gate-cli cex options mmp get` | none; optional `--underlying` | MMP state | underlying not found |
| `gate-cli cex options mmp set` | `--underlying`, window, frozen period, qty/delta limits | MMP config | invalid range or permission |
| `gate-cli cex options mmp reset` | `--underlying` | reset state | no frozen state |
| `gate-cli cex options account settlements` | `--underlying` | account settlement records | invalid underlying |
| `gate-cli cex options market settlements` | `--underlying` | public settlement history | invalid filter |
| `gate-cli cex options market settlement` | `--underlying`, `--contract`, `--at` | settlement at time | contract/time not found |
| `gate-cli cex options position close` | `--underlying`, optional contract | position-close history | read-only; does not close a live position |
| `gate-cli cex options market underlying-tickers` | `--underlying` | underlying index/valuation ticker | unsupported underlying |
| `gate-cli cex options market underlying-candlesticks` | `--underlying` | interval, limit | unsupported underlying or interval |
| Public streams | product-specific channel/payload | bounded observation | Use [public streams](streams.md#options); private subscriptions are excluded from the helper. |

## Market Data

| Endpoint / method | Required params | Optional params | Description |
| --- | --- | --- | --- |
| `GET /options/underlyings` | none | none | List option underlyings. |
| `GET /options/expirations` | `underlying` | none | Expirations for an underlying. |
| `GET /options/contracts` | `underlying` | `expiration`, page, limit | Contracts filtered by underlying/expiry. |
| `GET /options/contracts/{contract}` | `contract` | none | Contract multiplier, strike, call/put and order limits. |
| `GET /options/tickers` | `underlying` | none | Option ticker and mark/IV data. |
| `GET /options/order_book` | `contract` | `interval`, `limit` | Option order-book snapshot. |
| `GET /options/trades` | `contract` | limit, from, to | Public option trades. |
| `GET /options/candlesticks` | `contract`, `interval` | from, to, limit | Option candles where the endpoint is enabled. |
| `GET /options/underlying/tickers/{underlying}` | `underlying` path | none | Official API underlying ticker used for option valuation. |
| `GET /options/underlying/candlesticks` | `underlying`, `interval` | from, to, limit | Official API underlying candles. |

## Account and positions (auth required)

| Endpoint / method | Required params | Optional params | Description |
| --- | --- | --- | --- |
| `GET /options/accounts` | none | none | Option account equity, available margin, and balance. |
| `GET /options/account_book` | none | `currency`, `from`, `to`, `page`, `limit` | Option account ledger. |
| `GET /options/positions` | none | `underlying` | Current option positions. |
| `GET /options/positions/{contract}` | `contract` | none | One contract's position and size. |
| `GET /options/my_trades` | `underlying` | `contract`, `limit`, `offset`, `from`, `to` | Authenticated fills. |

## Trade (auth required)

| Endpoint / method | Required params | Optional params | Description |
| --- | --- | --- | --- |
| `POST /options/orders` | `contract`, `size` | `price`, `tif`, `iceberg`, `text`, `reduce_only`, `close`, `mmp`, mark-IV fields | Place an option order. `price=0` plus IOC is the mapped market form where supported; size is integer contracts. |
| `GET /options/orders` | `status` | `underlying`, `contract`, `limit`, `offset`, `from`, `to` | List open or historical option orders. |
| `GET /options/orders/{order_id}` | `order_id` | none | Query one order. |
| `PUT /options/orders/{order_id}` | `order_id`, `contract`, `price`, `size` | none | Amend an open order. |
| `DELETE /options/orders/{order_id}` | `order_id` | none | Cancel one order. |
| `DELETE /options/orders` | explicit filter or confirmed account-wide scope | `underlying`, `contract`, `side` | Cancel matching option orders. If filters are omitted it is account-wide; require an explicit user scope before calling. |

## Streams

Use the public channel and payload tables in [public streams](streams.md#options), including contract versus underlying subscriptions, object scopes, candle intervals and recovery. The bounded helper is an approved public-only exception; a missing CLI watcher does not block it. Do not add a generic settle field or reuse futures payloads. ACK alone does not prove market data receipt; preserve server timestamps and exact numbers.

Private order, position and fill subscriptions are not authorized by the public helper. Without a registered, verified private CLI operation, stop that subscription; a documented API channel or available credentials do not authorize a custom WS client.

## MMP and kill switch (auth required)

| Endpoint / method | Required params | Optional params | Description |
| --- | --- | --- | --- |
| `GET /options/mmp` | none | `underlying` | Read MMP configuration and state; specify an underlying when possible. |
| `POST /options/mmp` | `underlying`, `window`, `frozen_period`, `qty_limit`, `delta_limit` | `mmp` fields supported by the service | Set MMP protection. `window`/`frozen_period` are milliseconds; quantity/delta limits are positive values. |
| `POST /options/mmp/reset` | `underlying` | none | Reset the frozen MMP state. It does not restore orders that were already cancelled. |
| `POST /options/orders` | `mmp=true` plus normal order fields | none | Mark an option order as MMP protected when the account supports it. |

MMP is separate from the account-wide cancel endpoint. Read current state before changing it and confirm the exact underlying and thresholds.

## Settlements and position close

| Endpoint / method | Required params | Optional params | Description |
| --- | --- | --- | --- |
| `GET /options/settlements` | `underlying` | `contract`, `from`, `to`, `limit`, `offset` | Public settlement history. |
| `GET /options/settlements/{contract}` | `underlying`, `contract`, `at` | none | Public settlement data for one contract/time. |
| `GET /options/my_settlements` | `underlying` | `contract`, `from`, `to`, `limit`, `offset` | Authenticated settlement records for the account. |
| `GET /options/position_close` | `underlying` | `contract` | Read-only position-close records. |
| `POST /options/orders` with full-close fields | `contract`, `close=true`, `size=0` where supported | `price`, `tif`, `text` | Full close; verify the position after the order reaches a terminal state. |
| `POST /options/orders` with reduce-only fields | `contract`, signed `size`, `reduce_only=true` | `price`, `tif`, `text` | Partial close; contract size must not exceed the live position. |

## Contract and size normalization

Contract names use `{underlying}-{expiration}-{strike}-{C|P}`. Read the contract multiplier and `order_size_min` before converting a user notional. For base notional, `contracts = floor(base_amount / multiplier)`; for a USDT notional, use the current `price_per_contract` and floor to an integer. Round price to the contract precision and reject a result below the minimum size. State the conversion in the confirmation summary; never silently round up.

## Enums

- Option kind: `C`, `P` or `call`, `put` as returned by the contract response.
- `order_type`: market, limit, and mark-IV form exposed by the installed API.
- `tif`: `gtc`, `ioc`, `poc`.
- `status`: `open`, `finished`; cancellation is represented by `finish_as=cancelled` where returned.
- `finish_as`: `filled`, `cancelled`, `liquidated`, `ioc`, `auto_deleveraged`, `reduce_only`, `position_closed`, `reduce_out`, `mmp_cancelled` where returned.
- `side`: buy/sell or the signed size convention returned by the API.
- `mmp`: `true` or `false`.
- MMP `window`: `0` disables or `1`–`5000` milliseconds; `frozen_period=0` means persistent freeze.

## Constraints

- Current CLI covers market lookup, account, positions, trades, list/create/cancel/amend, MMP, settlement history, and position-close history. `position close` is read-only; if `order create --help` does not expose `--close` or `--reduce-only`, active option close is unavailable and must use the toast workflow. Stream watcher commands are not mapped; verify any proposed watcher with `--help`.
- The snapshot CLI does expose underlying ticker and candlestick leaves, but the API paths remain the official singular `/options/underlying/...` paths above. Do not rewrite them to a guessed plural path.
- Block trade, RFQ, and market-maker block workflows are not mapped by this skill.
- Do not treat a settlement record or position-close record as proof that a live position is flat; re-read `/options/positions/{contract}`.

> WebSocket channel names and payload schemas differ between Gate options deployments. The current market reference uses `wss://op-ws.gateio.live/v4/ws`; before subscribing, verify the live service's channel schema and use REST snapshot/resync after reconnect. Do not infer a private stream from a public channel.

For deployments that still expose legacy names, ticker subscriptions may be `options.tickers` instead of `options.contract_tickers`/`options.ul_tickers`; confirm the channel list returned by the live options WebSocket before subscribing.
