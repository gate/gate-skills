# Gate CEX coverage and boundaries

This matrix records the current Gate API/CLI mapping used by `gate-cex-trade`. REST paths and fields follow the official [Gate API v4 documentation](https://www.gate.com/docs/developers/apiv4/en/); CLI commands and flags follow the configured CLI build. “Mapped” means documented; it does not mean credentials, permissions, path compatibility, or production execution have been tested.

| Module | Reference | Mapped coverage | Known boundary |
| --- | --- | --- | --- |
| Spot | `spot.md` | Market, account, orders, fills, amend/cancel, triggers, countdown, POV-like split create/list/get/cancel | Native OCO/OTO/SOR parity is not inferred; POV requires a compatible registered CLI leaf; missing fields do not authorize a private API fallback. |
| Futures | `futures.md` | Selected settle market, account, positions, orders, leverage/mode, triggers, batch, trail and chase autoorder contracts | Chase and Trail have registered CLI leaves; required flags must exist in the installed version. TWAP/VP is not established. |
| Delivery | `delivery.md` | Delivery market, account, positions, margin/leverage/risk, orders/fills, price triggers, liquidation and settlement history | Delivery is separate from perpetuals; the configured CLI adapter currently fixes its settle scope, so verify before writes. |
| Options | `options.md` | Market, account, positions, orders, close/reduce, streams, MMP, countdown, settlements | Advanced option CLI, block/RFQ, and market-maker block workflows require service verification. |
| Margin | `margin.md` | Unified borrow/repay, rates, liabilities, transferable, spot auto-borrow fields | No complete independent classic isolated/cross margin skill. |
| Unified | `unified.md` | Mode, account, borrowable, transferable, loans, interest, leverage, collateral, risk reads, portfolio calculator | Portfolio calculator is a read-only calculation; Delta Neutral is not order execution. Check actual SDK requests, not error-label paths; Delta Neutral, quick repayment and global leverage have registered commands. |
| Market | `market.md` | Product REST and public WebSocket routing, snapshot/resync guidance | Private stream commands are product-specific and not a generic market command. |
| Flash Swap | `flashswap.md` | Pairs, preview, quote acceptance, status/history | Not a limit Convert order; quote expiry is authoritative. |
| TradFi/CFD | `tradfi.md` | CFD symbols, ticker/kline, MT5 account, order, position, protection update, close, transaction | Check installed side/price/close enums, region, account and market availability; no blanket CFD write block. |
| Stock | `stock.md` | API v4 stock/ETF symbols, market, orders, positions, close, transactions | Verify installed [Stock commands](stocks-commands.md); do not substitute TradFi CFD. Public WS and CLI availability are separate. |
| Alpha | `alpha.md` | On-chain asset handoff and mapped Alpha CLI | No dedicated depth/kline/WS coverage confirmed. |
| VIP/fees | `vipfee.md` | Account tier and spot/futures/delivery fees; independent MCL handoff | Independent MCL belongs to gate-cex-earn; no loan execution is authorized by fee lookup. |

## Maintenance rule

When a new endpoint or CLI command is discovered, add it to the owning module's API/CLI table, include required/optional parameters and enums, and mark whether it is verified or only documented. Keep unsupported boundaries explicit instead of creating an approximate route.

Record CLI version, source, and leaf-help evidence in private test records. Do not include checkout paths, repository URLs, commit IDs, or infrastructure details in this distributable skill. Re-run leaf-help and path checks whenever the configured CLI build changes.
