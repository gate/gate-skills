# Gate Unified Account

Supplementary product background. Use the [canonical command contract](unified-commands.md) for registered leaves, exact flags, units and safety variants, and [runtime rules](runtime.md) for execution. API fields in this file do not authorize direct private API calls or imply matching CLI flags.

## Scope

Unified account mode, borrowable/transferable balances, loans, interest, leverage, collateral, and risk configuration. Unified account orders still route to spot/futures/options references.

## API / CLI index

REST paths and request fields follow the official Gate API v4 unified-account reference. The CLI column follows the configured source snapshot; verify actual SDK request construction; error-label strings alone are not compatibility blockers.

| Scenario | Endpoint / method | Required params | Optional params | Description | CLI |
| --- | --- | --- | --- | --- | --- |
| Account | `GET /unified/accounts` | none | `currency`, `sub_uid` | Equity, balances, and risk fields. | `gate-cli cex unified account get` |
| Mode | `GET /unified/unified_mode` | none | none | Current account mode. | `gate-cli cex unified mode get` |
| Set mode | `PUT /unified/unified_mode` | `mode` (`classic`, `multi_currency`, `portfolio`, `single_currency`) | none | Change account mode after checking positions/liabilities. | `gate-cli cex unified mode set --mode` |
| Borrowable | `GET /unified/borrowable` | `currency` | none | Borrowable amount and limits. | `gate-cli cex unified query borrowable` |
| Batch borrowable | `GET /unified/batch_borrowable` | currencies array (max 10) | none | Official API batch borrowable query. | `gate-cli cex unified query borrowable-list` |
| Transferable | `GET /unified/transferable` | `currency` | none | Transferable amount. | `gate-cli cex unified query transferable` |
| Estimate rate | `GET /unified/estimate_rate` | currencies array (max 10) | none | Estimated hourly borrow rate. | `gate-cli cex unified query estimate-rate` |
| Currencies | `GET /unified/currencies` | none | `currency` | Collateral/borrow currency configuration. | `gate-cli cex unified account currencies` |
| Loans | `GET /unified/loans` | none | currency, type (`platform` or `margin`), page, limit | Current loan liabilities. | `gate-cli cex unified loan list` |
| Borrow/repay | `POST /unified/loans` | currency, type (`borrow` or `repay`), amount | `repaid_all`, text | Borrow or repay; read liability after the write. | `gate-cli cex unified loan create --currency --amount --type` |
| Loan records | `GET /unified/loan_records` | none | type (`borrow` or `repay`), currency, page, limit | Historical loan operations. | `gate-cli cex unified loan records` |
| Interest records | `GET /unified/interest_records` | none | currency, page, limit, from, to, type | Accrued/paid interest. | `gate-cli cex unified loan interest` |
| User leverage | `GET /unified/leverage/user_currency_setting` | none | currency | Per-currency leverage setting. | `gate-cli cex unified config leverage-get` |
| Set leverage | `POST /unified/leverage/user_currency_setting` | currency, leverage | none | Update per-currency leverage. | `gate-cli cex unified config leverage-set` |
| Discount tiers | `GET /unified/currency_discount_tiers` | none | none | Currency discount tiers. | `gate-cli cex unified config discount-tiers` |
| Collateral | `POST /unified/collateral_currencies` | `collateral_type` (`0` all or `1` custom) | `enable_list`, `disable_list` | Add/remove collateral currencies. | `gate-cli cex unified config collateral` |
| Risk units | `GET /unified/risk_units` | none | currency | Unified risk-unit data. | `gate-cli cex unified risk units` |
| Loan margin tiers | `GET /unified/loan_margin_tiers` | none | none | Public loan margin tiers. | `gate-cli cex unified config loan-tiers` |
| User leverage | `POST /unified/leverage/user_setting` | leverage | none | Global borrowed-currency leverage. | `gate-cli cex unified config leverage-set-all` |
| Currency leverage config | `GET /unified/leverage/user_currency_config` | currency | none | Per-currency leverage limits. | `gate-cli cex unified config leverage-config` |
| Historical loan rate | `GET /unified/history_loan_rate` | currency | tier, page, limit | Historical rate tiers. | verify with `--help` |
| Estimated quick repayment | `GET /unified/estimated_quick_repayment` | none | none | Preview before quick repayment. | `gate-cli cex unified loan quick-estimate` |
| Quick repayment | `POST /unified/quick_repayment` | `debt_currencies`, `available_currencies` | none | Repay supported liabilities quickly. | `gate-cli cex unified loan quick-repay` |
| Portfolio calculator | `POST /unified/portfolio_calculator` | calculator input | none | Portfolio-only calculation; no order side effect. | `gate-cli cex unified risk calculate --input <json>` |
| Delta neutral | `GET/POST /unified/delta_neutral` | product input for writes | enable/state | Configuration read/write; not order execution. | `gate-cli cex unified config delta-neutral-get` / `delta-neutral-set --enabled` |

## Enums and constraints

- `mode`: `classic`, `single_currency`, `multi_currency`, `portfolio`.
- Loan action/type: `borrow`, `repay`; loan type: `platform`, `margin`.
- Leverage and amounts: preserve decimal strings; do not round through floating-point arithmetic.
- Account mode changes are writes and can be blocked by open positions or liabilities.
- Read mode, balances, borrowable, rate, liabilities, interest, and transferable amount before a write.
- Portfolio calculator and Delta Neutral are not order execution.

- `collateral_type`: `0` all collateral currencies, `1` custom list.
- Quick repayment uses debt and available currency arrays; read the estimate endpoint before submitting.
- The reviewed SDK builds `/unified/batch_borrowable` and `/unified/collateral_currencies`. Legacy `/unified/borrowable_list` or `/unified/collateral` error labels are not wire paths. Verify installed leaves, parameters and account permissions separately.
- `unified loan quick-estimate` and `quick-repay` are registered; currency selections are not spend caps. Verify liabilities, balances and authority before repayment. `unified config leverage-set-all` may partially apply: inspect failures and re-read each currency, never replay the whole write. See the canonical safety variants.
- `risk calculate` maps to the official portfolio calculator and is a read-only calculation; it does not change positions, margin, or orders.
