# Asset Movement Workflows

## Read balances or deposit information

Use [balances](balances-commands.md) for the requested account/currency only. For a deposit, use [deposits](deposits-commands.md) to resolve chain, address/tag, status and history. Do not claim the address query initiated or completed a deposit.

## Transfer between accounts or products

Use [transfers](transfers-commands.md). Confirm the selected account context, source/destination and subaccount UID if any, currency, exact amount/unit and permission. Check available/transferable balance and product availability. Preserve a supported stable reference, invoke once, then query transfer status or product transactions. Only a verified transfer result permits the next cross-skill trade. No unique reference means an ambiguous result remains unknown; do not sweep funds or replay.

## Read withdrawal history and status

Use [withdrawal queries](withdrawals-commands.md) to read existing withdrawal history and status within the requested account/currency and time window. Query results do not initiate a transfer or prove settlement. For UID transfer history, use [deposit records](deposits-commands.md).

## Convert small balances

Use [small balances](small-balance-commands.md) to inspect eligibility and conversion terms. Confirm the exact currency set; convert once and verify history plus resulting balances. Handle partial outcomes individually without replaying successful currencies.

## Shared stopping rules

Read [preflight](../../_shared/cex/preflight.md), [safety](../../_shared/cex/safety.md) and [execution](../../_shared/cex/execution-cli.md). Keep the same selected account context, credentials, origin and grant throughout. Stop before a step outside verified authority, on changed material terms, or on an ambiguous write. Do not replay earlier steps or automatically compensate. A cross-skill task transfers only the required account/environment, object reference, exact amount/unit, completed state and remaining authority; never credentials.
