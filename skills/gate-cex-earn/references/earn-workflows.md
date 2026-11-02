# Earn and Loan Workflows

## Subscribe or redeem

Select [Simple Earn/fixed](simple-earn-commands.md), [staking](staking-commands.md) or [dual investment](dual-investment-commands.md). Read product terms, eligibility/quota, currency, principal, lockup/maturity and current position. Clarify settlement currency, reinvest and early-redemption effects. Check funds and authority, execute the exact action, then read the matching position/order/history and released balance. Do not treat acceptance as completed redemption or automatically move principal to another product.

## Inspect recurring investment

Use [auto-invest](auto-invest-commands.md) only to inspect supported assets, minimum investment amounts, and orders for a specified plan and execution record. Creating, changing, funding, stopping, or querying an individual plan is outside this release; do not use a removed CLI leaf or substitute another integration.

## Manage a collateral loan

Use [collateral loans](collateral-loan-commands.md) to read the exact debt, collateral and LTV. Obtain authority for loan/collateral/repayment amounts and any liquidation exposure. Submit the selected action and verify order and repayment records, remaining interest/debt and collateral. Do not auto-refinance or add collateral after failure.

## Cross-product holdings and earnings

For requests such as "my Earn positions" or "how much have I earned", first split
the request into product holdings (S3) and quoted product yields (S2). Query every
in-scope product that has a retained matching read command, show the result in
separate product sections, and identify products without a retained matching read.
There is no aggregate CLI endpoint in this release. Do not merge rewards, interest
and principal into a single total unless the user explicitly asks and each returned
field has a compatible unit and time window.

## Shared stopping rules

Read [preflight](../../_shared/cex/preflight.md), [safety](../../_shared/cex/safety.md) and [execution](../../_shared/cex/execution-cli.md). Keep the same selected account context, credentials, origin and grant throughout. Stop before a step outside verified authority, on changed material terms, or on an ambiguous write. Do not replay earlier steps or automatically compensate. A cross-skill task transfers only the required account/environment, object reference, exact amount/unit, completed state and remaining authority; never credentials.
