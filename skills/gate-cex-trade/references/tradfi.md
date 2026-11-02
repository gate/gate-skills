# Gate TradFi

Supplementary product background. Use the [canonical command contract](cfd-commands.md) for registered leaves, exact flags, units and safety variants, and [runtime rules](runtime.md) for execution. API fields in this file do not authorize direct private API calls or imply matching CLI flags.

## Scope

Gate TradFi CFD market, MT5 account, order, position, and transaction routes. Stock API coverage is documented separately in `stock.md`. Availability depends on account and region; do not infer a complete CFD workflow from a generic symbol.

## API / CLI index

REST paths and fields follow the official Gate API v4 CFD/TradFi reference. The CLI column is supplementary; follow the canonical contract. Diagnostic paths do not establish actual SDK request paths.

| Scenario | Endpoint / method | Required params | Optional params | Description | CLI |
| --- | --- | --- | --- | --- | --- |
| Categories | `GET /tradfi/symbols/categories` | none | none | TradFi symbol categories. | `gate-cli cex tradfi market categories` |
| Symbols | `GET /tradfi/symbols` | none | none | Symbol metadata and status. | `gate-cli cex tradfi market symbols` |
| Symbol detail | `GET /tradfi/symbols/detail` | `symbols` (comma-separated, max 10) | none | Contract/market details; the current official API requires APIv4 authentication. The fallback CLI accepts one `--symbol` per call; do not pass a comma-separated list unless the installed leaf explicitly supports it. | `gate-cli cex tradfi market symbol` |
| Ticker | `GET /tradfi/symbols/{symbol}/tickers` | symbol | none | Latest quote. | `gate-cli cex tradfi market ticker` |
| Kline | `GET /tradfi/symbols/{symbol}/klines` | symbol, interval | from, to, limit | Historical candles. The CLI exposes `--type` and `--limit`; follow [market interval rules](markets.md#tradfi--cfd) for the actual API-compatible value, not an assumed conversion from a help default. | `gate-cli cex tradfi market kline` |
| MT5 account | `GET /tradfi/users/mt5-account` | none | none | MT5 account linkage/state. | `gate-cli cex tradfi account info` |
| Assets | `GET /tradfi/users/assets` | none | none | TradFi assets. | `gate-cli cex tradfi account assets` |
| Orders | `GET /tradfi/orders` | none | symbol, status, page | Open/current orders. The fallback `order list` leaf exposes no symbol/status/page filters; verify the exact help before filtering. | `gate-cli cex tradfi order list` |
| Create order | `POST /tradfi/orders` | symbol, side, volume, price_type | price, `price_tp`, `price_sl` | Create a CFD order. The official CFD contract uses `price_type=market` or `trigger`; preserve requested TP/SL fields. Do not invent a leverage field when the selected API schema does not expose one. | `gate-cli cex tradfi order create` |
| Update order | `PUT /tradfi/orders/{order_id}` | order id | price, `price_tp`, `price_sl` | Amend an open order. Before a TP/SL-only edit, read the current order and pass back its price plus the untouched protection side; omitted or `"0"` values clear that side. Re-read after the write. | `gate-cli cex tradfi order update` |
| Cancel order | `DELETE /tradfi/orders/{order_id}` | order id | none | Cancel one order. | `gate-cli cex tradfi order cancel` |
| Order history | `GET /tradfi/orders/history` | none | symbol, time/page | Historical orders. The fallback leaf exposes begin/end plus its help-listed side/symbol filters and no page flag. | `gate-cli cex tradfi order history` |
| Positions | `GET /tradfi/positions` | none | symbol | Current positions. | `gate-cli cex tradfi position list` |
| Update position | `PUT /tradfi/positions/{position_id}` | position id | `price_tp`, `price_sl` | Update protection. Read both current values first; sending neither value or `"0"` clears that side, so a one-side edit must carry the untouched side unchanged. | `gate-cli cex tradfi position update` |
| Close position | `POST /tradfi/positions/{position_id}/close` | position id, `close_type` | `close_volume` for partial | Close a CFD position; API `1` is partial and `2` is full. Verify final state. | `gate-cli cex tradfi position close` |
| Position history | `GET /tradfi/positions/history` | none | symbol, time/page | Historical positions. The fallback leaf exposes begin/end plus direction/symbol filters and no page flag. | `gate-cli cex tradfi position history` |
| Transactions | `GET /tradfi/transactions` | none | `begin_time`, `end_time`, `type`, page, page_size | Cash/trade transactions; verify SDK request construction; a legacy error label alone does not establish a different request. | `gate-cli cex tradfi account transactions` |
| Commissions | `GET /tradfi/symbols/commissions` | symbols or category | none | Symbol commission data; authentication and account eligibility remain required where specified. | `gate-cli cex tradfi market commissions` |

## API enums and CLI compatibility

- **CFD API v4 order:** `side=1` sell, `side=2` buy; `price_type=market` or `trigger`. `price_tp` and `price_sl` are optional order fields.
- **CFD API v4 close:** `close_type=1` partial (requires `close_volume`), `close_type=2` full (ignore `close_volume`).
- The reviewed CLI exposes `--side 1` sell / `2` buy and string `--price-type market` or `trigger`, matching the SDK request. Verify these exact installed flags; stop an older incompatible version, not all CFD writes.
- Kline interval is version/protocol-specific. An advertised `M1` default does not prove that the SDK converts it to `1m`; check the installed mapping and use the market contract's verified interval.
- CLI `--close-type 1` means partial and requires `--volume`; `--close-type 2` means full. Use the same native volume unit as the position.
- TradFi `volume` is the native unit returned by the symbol/position detail (for example shares, lots, or contracts). Include the unit in the confirmation summary; if the detail does not expose it, block the write.
- Transaction type: `deposit`, `withdraw`, `dividend`, `fill_negative`.
- Region/account availability and market hours can block otherwise valid requests. A requested TradFi leverage value is API/service-only until the installed CLI exposes a corresponding flag; block rather than silently omit it.
- The official transaction route is `GET /tradfi/transactions`; a legacy adapter path is compatibility evidence only and must not be treated as the API contract.
- Before a one-side TP/SL update, GET the position, preserve the other side's exact API value, and re-read after the write. If the current value or a complete update payload is unavailable, block the write.
- Stock mint/redeem, unsupported CFD actions, and unlisted order types are outside this route.
