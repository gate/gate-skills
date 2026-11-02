---
name: gate-cex-trade
description: Route Gate CEX spot, margin, futures, options, unified account, Flash Swap, TradFi, stock, delivery, Alpha, and fee intents to the correct package reference and execution contract; state unsupported workflows instead of inferring them.
metadata:
  version: 0.1.2
  exchange: Gate
  scope: cex-trade
---

# Gate CEX trading

This is the task-level entry point for Gate CEX requests. It connects a user's intent to the package-local CLI contracts and the shared CLI execution boundary. It is a routing and safety layer; it does not add an unlisted command or turn a similar product into an equivalent one.

## Before using a tool

1. Read [runtime](references/runtime.md), [confirmation and recovery rules](references/workflows.md), and [order workflows](references/order-workflows.md), then read the canonical command reference that matches the request. Treat the official Gate API v4 documentation as authoritative for REST paths, request fields, enums, and response semantics. Treat the installed `gate-cli` source snapshot as authoritative only for the CLI command and flag surface; run the exact leaf `--help` before use. Execute registered CLI leaves using their canonical command contract. Only the bounded public market transports listed in [market rules](references/market.md) are exceptions; do not bypass a missing CLI action with a private HTTP or SDK call. If no compatible local mapping exists, render the `workflows.md` unavailable-operation toast. Trace a suspected mismatch through registration, flag parsing, handler and SDK request construction. Error-label paths alone are not wire-path evidence. Stop only the affected operation when an actual incompatibility or required capability gap is established. Source support does not prove installed-version support, online permission, regional availability or product eligibility.
2. Resolve the product and instrument. A request such as “buy BTC” is incomplete until spot, margin, futures, options, or another product is known. A read-only candidate lookup may compare CEX pairs and Alpha tokens when the asset is ambiguous; never write until the user chooses. “go long with 500 USDT” is incomplete until the product, settlement currency, amount unit, leverage, margin mode, and position side are known.
3. For a read request, use read-only operations and report the source time. For a write request, run only the product-specific preflight in `workflows.md`: order writes need rules/balance/position checks as applicable; loan and configuration writes need the current resource state and limits; countdown and account-wide actions need an explicit scope.
4. Normalize the request using the live product specification: symbol, side, order type, quantity or quote amount, price, time-in-force, reduce-only, trigger rule, settlement currency, leverage, and margin mode. Never silently convert a quote amount to contracts or base quantity.
5. Show the product-specific execution summary from `workflows.md` and ask for explicit confirmation immediately before the first write in a sequence when no active confirmation covers the unchanged operation. Include the native quantity/unit, scope, resource fields, estimated fees or margin, and any linked protection order. Reuse the active confirmation for unchanged polling, reconciliation, and declared sequence steps; obtain confirmation again only when the confirmed context changes.

## Routing

| User intent | Read first | Current route and boundary |
| --- | --- | --- |
| Chain token, new coin, meme coin, launchpad, contract address, Gate Alpha/Trenches | [Alpha commands](references/alpha-commands.md) | Use the registered Alpha CLI contract. Do not route by the words “spot account” alone; identify the asset as on-chain first. |
| Spot quote, rules, balance, buy/sell, order, fill, amend, cancel, price trigger | [Spot commands](references/spot-commands.md) | Use the registered spot CLI leaves and account/protection variants. |
| Borrow/repay, unified margin, then spot trade | [Margin commands](references/margin-commands.md) | Check account mode first. Use the local unified/margin mapping when compatible; classic isolated/cross margin remains unsupported where no local route exists. |
| USDT perpetual quote, open/close, leverage, position, order, TP/SL, conditional order | [Perpetual commands](references/perpetual-commands.md) | Use the registered futures CLI leaves. Do not extend perpetual rules to coin-margined reverse contracts, USDC, or portfolio margin. |
| Delivery contract quote, order, position, settlement, or price trigger | [Delivery commands](references/delivery-commands.md) | Use the delivery-specific API/CLI mapping and settle/contract scope. Do not reuse perpetual-only enums or assume every delivery write is enabled. |
| Options quote, account, position, order, amend, cancel, settlement, stream, MMP, or countdown cancel | [Options commands](references/options-commands.md) | Use the local options/assets mapping and verify advanced adapter leaves before execution. Block/RFQ is unmapped. |
| Market quote, chart, depth, public stream, or market analysis | [Market commands](references/market-commands.md), then [market interfaces](references/markets.md) and [public streams](references/streams.md) | Use the local market mapping for raw REST data. Public product WebSocket support is product-specific; private order/account streams are separate. |
| Unified account equity, borrowing, collateral, limits, interest, mode | [Unified commands](references/unified-commands.md) | Use the local unified/account mapping. Do not infer portfolio-account-only order or risk-model support. |
| Flash Swap quote, acceptance, status, history | [Convert commands](references/convert-commands.md) | Use the local Flash Swap contract and protocol-specific request schema. Instant conversion is not a limit Convert order. |
| CFD/TradFi quote, order, position, or close | [CFD commands](references/cfd-commands.md) | CFD uses `gate-cli cex tradfi`; verify the actual requested leaf and flags. CFD side, price type, close type, and TP/SL preservation are explicit compatibility checks. |
| Stock quote, order, position, or transaction | [Stocks commands](references/stocks-commands.md) | Use the API v4 stock contract when the local adapter exposes it. Verify the installed stock leaf and flags; ticker/history CLI gaps do not imply that public Stock WS is unavailable. |
| Spot time-slice/POV or futures strategy order | [Algorithm commands](references/algo-commands.md), then [Spot](references/spot-commands.md) or [Perpetual](references/perpetual-commands.md) | Resolve the product first, then use the mapped POV, trail, or chase endpoint. Gate's current mapping does not establish Binance TWAP/VP parity; do not emulate unsupported strategies with repeated ordinary orders. |
| VIP level, maker/taker fee, discount, or multi-collateral loan | [VIP and fees commands](references/vip-fees-commands.md) | Use the canonical fee mapping for fees. Independent MCL loans belong to `gate-cex-earn`; hand off that request, or report the missing skill. Do not equate a generic “VIP Loan” request with MCL without clarifying the product. |

Canonical command references define registered actions, parameters, units and variants; order workflows compose them. Supplementary API background below cannot override these contracts or authorize another transport. Verify the installed leaf before execution.

## Completion rules

- A submitted order is not a filled order. Report the actual state: accepted, open, partially filled, filled, cancelled, rejected, or unresolved. Internal reconciliation may use `unknown`, but never expose that literal as the user-facing status.
- After any write, reconcile by the strongest available resource key: returned order/client ID for orders, liability/account state for loans, mode/leverage/collateral state for configuration, MMP state for MMP, and returned order plus balance/position for conversions. If a call times out, query first; never blindly retry a potentially accepted write.
- If the main order succeeds but a TP/SL or other protection order fails, report the live exposure and the failed protection step separately. Do not declare the whole request successful.
- For close or reduce requests, re-read the position after execution and verify that size did not increase. “Close all profitable positions” is a changing set: take a snapshot, state the markets selected, then execute and re-check.
- For reverse, close the current side and verify the close before opening the opposite side unless the product contract explicitly provides an atomic route. Report both order IDs and both final states.
- Preserve API error code, message, order ID, and the relevant request fields when recovery is needed. Every failure or blocked operation must use the two-line `workflows.md` toast format. Never expose API keys or ask the user to paste them into chat.

## Explicit boundaries

The current mapping is based on the official Gate API v4 documentation plus the installed CLI adapter and has not been treated as end-to-end production verification. Do not claim a route is tested merely because its documentation exists. Keep unsupported native spot OCO/OTO relationships (distinct from supported attached TP/SL), full independent classic-margin lifecycle, coin-margined futures, USDC, portfolio-only unified-account orders and risk models, negative-balance/bankruptcy repayment, limit Flash Convert, stock actions without a local API mapping, stock mint/redeem, unverified VIP Loan variants, block/RFQ options, account-wide kill-switch use without an explicit scope, and unverified TWAP/VP behind their documented boundaries. Delivery is a separate mapped product and must use `references/delivery.md`; do not reuse perpetual assumptions. POV and chase have registered CLI contracts; verify the installed leaves and requested flags before use. A CLI command is usable only when its exact leaf appears in `Available Commands`; parent help or a zero exit code for an unknown nested path is not evidence that the leaf exists. Do not claim an unverified CLI release or source provenance.

## Supplementary API background

- [Common workflows and confirmation rules](references/workflows.md)
- [Spot](references/spot.md) · [Margin](references/margin.md) · [Futures](references/futures.md) · [Delivery](references/delivery.md) · [Options](references/options.md)
- [Market](references/market.md) · [Unified account](references/unified.md) · [Flash Swap](references/flashswap.md)
- [TradFi / CFD](references/tradfi.md) · [Stock](references/stock.md) · [VIP fees](references/vipfee.md)
- [Alpha handoff](references/alpha.md)
- [Coverage and known gaps](references/coverage.md)


Localized user prompts and failure messages are reviewed display data in [localized examples](references/localized-examples.json); their English rules remain in [workflows](references/workflows.md).
