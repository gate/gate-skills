# Gate Alpha handoff

Supplementary product background. Use the [canonical command contract](alpha-commands.md) for registered leaves, exact flags, units and safety variants, and [runtime rules](runtime.md) for execution. API fields in this file do not authorize direct private API calls or imply matching CLI flags.

## Route

Use this local Alpha contract when the request concerns chain tokens, a contract address, Gate Alpha, Trenches, launchpad, pumpfun, Solana/Base/BSC assets, or a new on-chain coin. CEX symbols such as `BTC_USDT` remain on the spot route unless the user identifies an on-chain asset.

## API / CLI index

REST paths and response states below follow the official Gate API v4 Alpha reference. The CLI column follows the supplied snapshot and must be checked with the exact leaf `--help`.

| Scenario | API / operation | Required inputs | Optional inputs | CLI |
| --- | --- | --- | --- | --- |
| Market currencies | `GET /alpha/currencies` | none | currency, limit, page | `gate-cli cex alpha market currencies` |
| Token list/details | `GET /alpha/tokens` | none | chain, launch_platform, address, page | `gate-cli cex alpha market tokens`; the fallback CLI names `launch_platform` as `--platform`. |
| Token ticker | `GET /alpha/tickers` | none | currency, limit, page | `gate-cli cex alpha market tickers` |
| Account balances | `GET /alpha/accounts` | none | none | `gate-cli cex alpha account balances` |
| Account book | `GET /alpha/account_book` | `from` | `to`, page, limit | `gate-cli cex alpha account book` |
| Order list | `GET /alpha/orders` | none | currency, side, status, from, to, page, limit | `gate-cli cex alpha order list` |
| Order detail | `GET /alpha/order` | order id | none | `gate-cli cex alpha order get` |
| Quote | `POST /alpha/quote` | currency, side, amount, gas_mode | slippage | `gate-cli cex alpha order quote` |
| Place order | `POST /alpha/orders` | currency, side, amount, gas_mode, quote_id | slippage | `gate-cli cex alpha order place` |

## Enums and constraints

- Asset origin: CEX pair versus on-chain token. A bare short symbol such as `PEPE` is ambiguous; compare read-only candidates and ask before a write.
- `side`: `buy`, `sell`; `gas_mode`: `speed`, `custom` (custom requires slippage).
- Quote id expires after about one minute; quote before place and confirm again if it expires.
- Buy amount is USDT to spend; sell amount is the token quantity. Slippage is a percentage, not a fraction; preserve the exact fresh quote parameters.
- The confirmation must include `quote_id`, `gas_mode`, and `slippage` when custom gas mode is used. A place request without the exact fresh quote is blocked.
- Alpha order status: `0` all, `1` processing, `2` success, `3` failed, `4` cancelled, `5` buy placed/transfer pending, `6` cancelled/transfer pending.
- Token chains include `solana`, `eth`, `bsc`, `base`, `world`, `sui`, `arbitrum`, `avalanche`, `polygon`, `linea`, `optimism`, `zksync`, and `gatelayer`; launch platforms include `meteora_dbc`, `fourmeme`, `moonshot`, `pump`, `raydium_launchlab`, `letsbonk`, `gatefun`, and `virtuals` where returned.
- No dedicated Alpha kline, depth, or WebSocket route is confirmed in this skill. `alpha account book` also requires `--from` in the fallback CLI; do not issue an unbounded history query.
- The reviewed handlers call SDK `GetAlphaOrder` and `QuoteAlphaOrder`, which construct `/alpha/order` (query `order_id`) and `/alpha/quote`. Legacy `/alpha/orders/{id}` and `/alpha/orders/quote` strings in error formatting do not determine the wire path. Verify the installed command/flags and actual request mapping; do not block on an error label alone.
- Do not paste Alpha commands into the CEX spot route.
