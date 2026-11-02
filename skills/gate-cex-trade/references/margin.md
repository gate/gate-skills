# Gate Margin

Supplementary product background. Use the [canonical command contract](margin-commands.md) for registered leaves, exact flags, units and safety variants, and [runtime rules](runtime.md) for execution. API fields in this file do not authorize direct private API calls or imply matching CLI flags.

## Scope

Margin borrowing, repayment, interest, and transferable balance. Gate's mapped execution path is unified margin plus the spot order route. There is no independent classic-margin skill in this package; do not infer isolated/cross lifecycle support from a similar endpoint name.

## Route / CLI

Use `gate-cli cex margin ... --help` for margin account/loan queries and the registered spot order CLI route for a margin trade after the account mode and borrow state are known. The reviewed spot buy/sell leaves expose `--account`, `--auto-borrow`, and `--auto-repay` (hyphenated flags). Apply the account restrictions in [spot account selection](spot-commands.md#spot-account-selection); stop if the installed version cannot express the requested account or borrowing policy. Borrow, repay, leverage, and auto-borrow writes require confirmation.

| Scenario | Endpoint / method | Required params | Optional params | Description / CLI |
| --- | --- | --- | --- | --- |
| Account state | `GET /margin/accounts` | none | `currency_pair` | Margin account state; CLI is `gate-cli cex margin account list`. |
| Account book | `GET /margin/account_book` | none | currency, currency_pair, type, from, to, page, limit | Margin ledger and interest entries. |
| Unified pairs | `GET /margin/uni/currency_pairs` | none | none | Unified borrow/trade pair rules. |
| Unified loans | `GET /margin/uni/loans` | none | currency_pair, currency, page, limit | Current loans and liabilities. Use unified loan queries. |
| Loan records | `GET /margin/uni/loan_records` | none | type, currency, currency_pair, page, limit | Historical borrow/repay records. |
| User tiers | `GET /margin/user/loan_margin_tiers` (API v4) | none | currency_pair | User-specific loan tiers. |
| Public tiers | `GET /margin/loan_margin_tiers` (API v4) | none | currency_pair | Public tier and rate limits. |
| User leverage | `POST /margin/leverage/user_market_setting` | `currency_pair`, `leverage` | none | Set current margin market leverage. |
| Transferable | `GET /margin/transferable` | currency | currency_pair | Amount that can be transferred or used. |
| Borrow/repay | `POST /margin/uni/loans` | currency, amount, currency_pair, type (`borrow` or `repay`) | `repaid_all` for full repayment | Official API supports both actions; the fallback CLI exposes only `margin uni lend` for borrow. Use `unified loan create --type repay` only for the unified-account route, not as a silent substitute for an isolated margin pair. |
| Spot trade with auto-borrow/repay | `POST /spot/orders` | pair, side, amount, type | `auto_borrow`, `auto_repay` | Use registered spot buy/sell with `--account`, `--auto-borrow`, and `--auto-repay` only for supported account combinations. Report liability changes. |

## CLI mapping

The supplied CLI exposes `gate-cli cex margin account list|book|funding|transferable`, `margin uni pairs|pair|estimate-rate|loans|lend|loan-records|interest-records|borrowable`, `margin leverage set`, `margin auto-repay get|set`, and `margin tier user|market`. `margin uni lend` is borrow-only; there is no matching `margin uni repay` leaf in this snapshot. Run the full leaf path with `--help` and preserve decimal strings exactly. Verify the actual SDK request when CLI diagnostics and the API appear to disagree; stop the affected operation if the required action cannot be expressed. Do not switch to direct API execution.

## Enums and constraints

- Account mode: `classic`, `single_currency`, `multi_currency`, `portfolio` where returned.
- Loan action: borrow or repay as exposed by the endpoint; loan type is `margin`.
- Amount is a currency amount, not a spot quote amount or futures contract count.
- Read account mode, borrowable amount, rate, existing liabilities, and transferable balance before a write.
- A failed trade after a successful borrow leaves a liability; report it and do not silently repay or retry.
- Independent classic isolated/cross margin, cross-liquidate, and negative-balance/bankruptcy repayment are not mapped here.

Any borrow, repay, or margin-trade error must use the two-line toast in `workflows.md`; keep the liability and API error in the internal report.
