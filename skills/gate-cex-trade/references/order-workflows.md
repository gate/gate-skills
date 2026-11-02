# Order and Position Workflows

## Spot market buy

1. Resolve the exact pair and quote-currency budget. Read `spot.market.pair` in [market](market-commands.md) for precision, limits and trading status.
2. Read `spot.account.get` or list in [spot](spot-commands.md) for the intended account's available quote balance. Do not transfer or borrow implicitly.
3. Verify the grant against the selected account context, environment, pair, spending and validity period. Execute `spot.order.buy` with `--quote` and no `--amount` or `--price` for this market variant.
4. Keep the returned order ID and query `spot.order.get`; inspect fills/remaining quantity before reporting an outcome. Lost ID or an ambiguous timeout is unknown, not a reason to buy again.

## Alpha quote and trade

1. Resolve the asset's exact currency, chain, contract address and normal trading status through [Alpha](alpha-commands.md). Alpha CEX execution does not require a DEX wallet or signing flow.
2. Read Alpha balances for the selected account context. Interpret buy `--amount` as USDT spending and sell `--amount` as base-token quantity. Verify precision, funds, fees and the user's amount/slippage authority; do not transfer or borrow implicitly.
3. Call `alpha.order.quote` using the chosen currency, side, amount and gas mode. Custom mode needs the explicit percentage slippage. Quote is not placement; verify its error/limits, received range, estimated fees and one-minute validity. A missing quote ID or unresolved material term stops placement.
4. Recheck authority and quote freshness. Call `alpha.order.place` once, using the same context and quote parameters plus its `--quote-id`. A new quote or changed amount, mode or tolerance does not inherit approval for changed material terms.
5. Query `alpha.order.get` with the returned order ID. Keep processing or incomplete-transfer statuses 1, 5 and 6 distinct from completed execution. If placement timed out or lost its ID, use bounded order history/account records to reconcile uniquely; otherwise report unknown and stop. Do not requote and buy again to recover an uncertain placement.

## Amend or cancel an existing order

Read the exact order, original product/account, state and remaining quantity. Use the matching spot/perpetual/delivery/options/stock/CFD product reference. Alpha has no registered amend/cancel action; an Alpha request stops at that boundary. Check amendment fields and cancel-one versus cancel-all scope for the supported products. An amendment that races a fill can fail or partially take effect. Query again and report the observed final state; cancellation never reverses fills.

## Set leverage, open or close a position

Read contract metadata, effective position mode, existing positions/orders, current leverage and margin. Treat each setting change and trade as a separate authorized action. Use [perpetual](perpetual-commands.md), [delivery](delivery-commands.md), [margin](margin-commands.md), [options](options-commands.md), [stocks](stocks-commands.md) or [CFD](cfd-commands.md) quantities and close/reduce semantics. Re-read after each step and stop on failure; do not restore the old leverage or reverse a fill automatically.

## Maintain protection

Read the exact current trigger/trailing/order/position and both protections before changing one. Use only the selected product's supported command. For [spot attached protection](spot-commands.md#spot-attached-protection), omitted/null preserves and only an explicit empty object cancels; never convert an invalid value into cancellation. CFD omitted/zero TP or SL may clear protection: resend the unchanged protection explicitly. Treat cancel-and-replace as two writes with a possible unprotected interval; do not present it as an atomic amendment or perform it without authority. Query the resulting protection and remaining position.

## Convert or fund before trading

Follow [convert](convert-commands.md) for preview, quote review, creation and order verification. For funding, hand off the transfer to `gate-cex-assets` and wait for a verified result before trading. If the asset skill is absent, explain the missing step rather than implementing transfer writes here.

## Shared stopping rules

Read [preflight](../../_shared/cex/preflight.md), [safety](../../_shared/cex/safety.md) and [execution](../../_shared/cex/execution-cli.md). Keep the same selected account context, credentials, origin and grant throughout. Stop before a step outside verified authority, on changed material terms, or on an ambiguous write. Do not replay earlier steps or automatically compensate. A cross-skill task transfers only the required account/environment, object reference, exact amount/unit, completed state and remaining authority; never credentials.

Protection and closing guarantees depend on the selected leaf. Options order creation supports [full close and reduce-only](options-commands.md#options-position-close); its close-history query remains read-only. The perpetual trigger-creation limitation and delivery close-history boundary still apply.

## Execute a native algorithm

Read [POV or chase rules](algo-commands.md) and the relevant spot/perpetual account,
contract and existing orders. Confirm side, amount unit, price controls, lifetime
and the exact authorized stop scope. Submit once, retain the parent ID, then query
parent and relevant child orders/fills within the task budget. Stopping execution
is a separate authorized write; inspect any residual child orders and positions.
Do not synthesize TWAP/VP or replay a creation with an unknown result.
