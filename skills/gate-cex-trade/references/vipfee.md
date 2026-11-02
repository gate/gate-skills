# Gate VIP and Fees

Supplementary product background. Use the [canonical command contract](vip-fees-commands.md) for registered leaves, exact flags, units and safety variants, and [runtime rules](runtime.md) for execution. API fields in this file do not authorize direct private API calls or imply matching CLI flags.

## Scope

Read-only VIP tier, spot/futures/delivery fee, and mapped multi-collateral rate information. Fee data informs a confirmation summary; it never authorizes a trade. The `mcl` command family is a separate multi-collateral loan surface; do not equate it automatically with a VIP tier or an unspecified “VIP Loan”.

## API / CLI index

| Scenario | Endpoint / method | Required params | Optional params | Description | CLI |
| --- | --- | --- | --- | --- | --- |
| Account tier | `GET /account/detail` | none | none | VIP tier and account-level fee fields. | `gate-cli cex account detail` |
| Spot/futures fee | `GET /wallet/fee` | none | `currency_pair`, `settle` | Maker/taker fee for the selected spot/futures/delivery scope. | `gate-cli cex wallet market trade-fee` |
| Account rate limit | `GET /account/rate_limit` | none | none | Read-only API rate-limit diagnostics. | verify with `--help` |
| Multi-collateral LTV | `GET /loan/multi_collateral/ltv` | none | currency | LTV information where the account supports it. | `gate-cli cex mcl ltv` |
| Current loan rate | `GET /loan/multi_collateral/current_rate` | none | currency | Current mapped multi-collateral rate. | `gate-cli cex mcl current-rate` |
| Fixed rate | `GET /loan/multi_collateral/fixed_rate` | none | currency | Fixed-rate offer where enabled. | `gate-cli cex mcl fix-rate` |
| Loan orders | `GET /loan/multi_collateral/orders` | none | status/page | Read-only records if account supports it. | `gate-cli cex mcl orders` |
| Loan detail | `GET /loan/multi_collateral/orders/{order_id}` | order id | none | One multi-collateral loan detail. | `gate-cli cex mcl order` |
| Repay records | `GET /loan/multi_collateral/repay` | operation type | borrow currency, page, limit, time range | Repayment/liquidation records. | `gate-cli cex mcl repay-records` |
| Currency quota | `GET /loan/multi_collateral/currency_quota` | currency | none | Quota information where supported. | `gate-cli cex mcl quota` |
| Multi-collateral currencies | `GET /loan/multi_collateral/currencies` | none | none | Public supported-currency metadata. | `gate-cli cex mcl currencies` |
| Collateral records | `GET /loan/multi_collateral/mortgage` | none | page, limit, time range, currency | Historical collateral adjustments. | `gate-cli cex mcl records` |

## Enums and constraints

- Fee side: maker/taker; exact rate fields come from the response.
- Settlement: `usdt`, `btc`, or other values only when returned.
- Read fee data immediately before confirmation when the user asks for exact cost.

## Independent lending handoff

Independent MCL borrowing, repayment and collateral adjustment belong to `gate-cex-earn`. Trade retains fee, rate, LTV and risk reads only and does not execute or reproduce an MCL write workflow. Clarify an ambiguous VIP Loan product before handoff.

Carry the selected account/profile/environment, loan identity, currencies, exact decimal amounts and units, collateral action, cumulative limits, destination if relevant, expiry, unchanged authorization scope, and execution status (not started, accepted, completed, partial, or unresolved). Include prior request/loan IDs and completed steps without exposing secrets. Preserve a still-valid grant without enlarging it; changed scope needs fresh authorization. An unresolved write must be reconciled by Earn before any new mutation, never repeated as a new loan. If Earn is unavailable, stop and report the missing owner; do not execute locally.
