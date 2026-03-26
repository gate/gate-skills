# Scenarios

This document defines behavior-oriented scenario templates for 18 unified account cases.

## Global Execution Gate (Mandatory)

For every scenario that includes mutation calls (`create_unified_loan`, `set_unified_mode`, `set_user_leverage_currency_setting`, `set_unified_collateral`):
- Build and present an Action Draft first
- Require explicit confirmation from the immediately previous user turn
- Treat confirmation as single-use
- Re-confirm whenever parameters or intent change
- For multi-step flows, confirm each mutation step separately

If confirmation is missing/ambiguous/stale, do not execute any mutation call.

## Global Rendering Rules (Mandatory)

- Keep API numeric precision as returned; do not round unless the user explicitly asks.
- Do not trim/normalize decimal strings; preserve the exact API numeric string (including trailing zeros) in displayed amounts and rates.
- When timestamp fields are available, output both raw timestamp and readable local time.
- For account-overview responses, always include IMR/MMR explicitly:
  - IMR: `totalInitialMarginRate`
  - MMR: `totalMaintenanceMarginRate`
- If per-currency `balances` are displayed, include `imr` and `mmr` fields for each reported currency when present.
- Mode labels must map strictly as:
  - `classic` -> `经典现货模式`
  - `single_currency` -> `单币种保证金模式`
  - `multi_currency` -> `跨币种保证金模式`
  - `portfolio` -> `组合保证金模式`
- If account is not in unified mode or unified account is not opened, show top warning: `⚠️ 当前账户未开通统一账户功能。`

## I. Account and Mode (1-3)

## Scenario 1: Unified Account Overview
**Context**: User wants unified account equity and risk metrics.
**Prompt Examples**:
- "Check my unified account overview."
- "How much total value do I have in unified account?"
**Expected Behavior**:
1. Fetch data via `get_unified_accounts` (`currency=all` optional).
2. Calculate total equity and key margin indicators from returned account fields, including IMR/MMR (`totalInitialMarginRate` and `totalMaintenanceMarginRate`) when present.
3. If presenting per-currency balances, include each currency's `imr` and `mmr` when present.
4. Output `Unified Account Overview Report`.
5. Preserve equity precision from API (no forced rounding).
**Unexpected Behavior**:
1. Returns only one currency balance but claims it is total account value.
2. Omits key risk fields even when response includes them.
3. Triggers unrelated mutation calls in a query-only scenario.

## Scenario 2: Query Current Unified Mode
**Context**: User wants to know current unified account mode.
**Prompt Examples**:
- "What is my current unified mode?"
- "Am I in portfolio or cross-currency mode?"
**Expected Behavior**:
1. Fetch data via `get_unified_mode`.
2. Map mode value to user-readable description using fixed mapping (`classic`/`single_currency`/`multi_currency`/`portfolio`).
3. Output `Unified Mode Status Report`.
**Unexpected Behavior**:
1. Guesses mode without calling the mode query tool.
2. Uses unsupported mode labels inconsistent with API return.
3. Attempts mode mutation when user asked only to check.

## Scenario 3: Switch Unified Mode
**Context**: User wants to switch account mode.
**Prompt Examples**:
- "Switch me to portfolio mode."
- "Change my unified mode to multi-currency."
- "How do I switch unified mode?"
**Expected Behavior**:
1. Fetch data via `get_unified_mode` and compare current vs target mode.
2. Explain all four supported target modes: `经典现货模式` / `单币种保证金模式` / `跨币种保证金模式` / `组合保证金模式`.
3. Calculate impact note and build `Mode Switch Draft`.
4. After explicit confirmation, execute via `set_unified_mode` and output `Mode Switch Result Report`.
**Unexpected Behavior**:
1. Executes mode switch without confirmation.
2. Ignores current mode and submits redundant or wrong target mode.
3. Returns success without showing resulting mode.

## II. Borrow Limits and Borrowing (4-8)

## Scenario 4: Single-Currency Borrowable Query
**Context**: User wants maximum borrowable amount for one currency.
**Prompt Examples**:
- "How much BTC can I borrow?"
- "Check my USDT borrow limit."
**Expected Behavior**:
1. Fetch data via `get_unified_borrowable` (`currency=target`).
2. Calculate and normalize max borrowable amount without rounding away API precision.
3. Output `Borrowable Limit Report`.
**Unexpected Behavior**:
1. Calls wrong currency or misses required currency parameter.
2. Returns stale hardcoded limit without API response.
3. Interprets 0 as error instead of valid "currently unavailable".

## Scenario 5: Multi-Currency Borrowable Summary
**Context**: User wants borrowable limits for multiple currencies.
**Prompt Examples**:
- "Show borrowable limits for BTC, ETH, and USDT."
**Expected Behavior**:
1. Fetch data via `get_unified_borrowable` per currency (loop).
2. Calculate per-currency amounts and aggregate table/list.
3. Output `Multi-Currency Borrowable Report`.
**Unexpected Behavior**:
1. Reports only first currency and ignores others.
2. Claims batch endpoint result without real per-currency queries.
3. Mixes currencies and amounts in output mapping.

## Scenario 6: Borrow Specific Amount
**Context**: User wants to borrow a target amount of one currency.
**Prompt Examples**:
- "Borrow 200 USDT."
- "I want to borrow 0.1 BTC."
**Expected Behavior**:
1. Fetch data via `get_unified_borrowable` to validate requested amount.
2. Calculate gap vs max borrowable and build `Borrow Draft`.
3. After explicit confirmation, execute via `create_unified_loan` (`type=borrow`) and output `Borrow Result Report`.
**Unexpected Behavior**:
1. Executes borrow without pre-checking borrowable.
2. Borrows an amount above max borrowable and returns raw API failure only.
3. Executes borrow without confirmation.

## Scenario 7: Query Supported Borrow Currencies
**Context**: User asks which currencies are supported in unified lending.
**Prompt Examples**:
- "Which currencies can I borrow?"
**Expected Behavior**:
1. Fetch data via `list_unified_currencies`.
2. Calculate supported currency list summary.
3. Output `Supported Borrow Currencies Report`.
**Unexpected Behavior**:
1. Returns guessed mainstream coins only without API query.
2. Includes currencies not returned by current account scope.
3. Performs mutation actions in this read-only scenario.

## Scenario 8: Query Estimated Borrow Rate
**Context**: User asks estimated rate for borrowing one or more currencies.
**Prompt Examples**:
- "What is the estimated borrow rate for BTC?"
- "Check estimate rates for BTC and USDT."
**Expected Behavior**:
1. Fetch data via `get_unified_estimate_rate` (`currencies=[...]`).
2. Calculate/display per-currency estimated rates.
3. Output `Estimated Borrow Rate Report` with dynamic-rate disclaimer.
**Unexpected Behavior**:
1. Reports a rate but omits currency mapping.
2. Presents estimate as guaranteed fixed rate.
3. Uses unrelated historical values instead of current estimate query.

## III. Repayment and Record Queries (9-12)

## Scenario 9: Partial Repayment
**Context**: User wants to repay part of the outstanding loan.
**Prompt Examples**:
- "Repay 50 USDT."
- "Repay 0.01 BTC loan."
**Expected Behavior**:
1. Fetch data via `create_unified_loan` draft phase assumptions and validate user-provided amount.
2. Calculate repayment parameters and build `Partial Repay Draft`.
3. After explicit confirmation, execute via `create_unified_loan` (`type=repay`, `repaid_all=false`) and output `Repay Result Report`.
**Unexpected Behavior**:
1. Mistakenly sets `repaid_all=true` for partial request.
2. Executes repayment without user confirmation.
3. Returns success but omits repaid amount and currency.

## Scenario 10: Full Repayment
**Context**: User wants to repay full outstanding balance of a currency.
**Prompt Examples**:
- "Repay all my USDT loan."
- "Clear my BTC debt."
**Expected Behavior**:
1. Fetch data context from user intent and validate target currency.
2. Calculate full-repay parameters and build `Full Repay Draft`.
3. After explicit confirmation, execute via `create_unified_loan` (`type=repay`, `repaid_all=true`) and output `Full Repay Result Report`.
**Unexpected Behavior**:
1. Uses partial repayment payload for a full-repay request.
2. Proceeds when currency scope is ambiguous.
3. Executes without confirmation.

## Scenario 11: Query Loan Records
**Context**: User wants to review borrow/repay history.
**Prompt Examples**:
- "Show my unified loan records."
- "List my borrow and repay history for USDT."
**Expected Behavior**:
1. Fetch data via `list_unified_loan_records` (optional currency/time filters).
2. Calculate sorted history summary and key fields (type, amount, time).
3. Output `Loan History Report`.
**Unexpected Behavior**:
1. Returns only current balance and no history records.
2. Ignores provided filters and returns unrelated entries.
3. Triggers mutation calls in history-only request.

## Scenario 12: Query Interest Records
**Context**: User wants to review charged-interest details.
**Prompt Examples**:
- "Show my interest records."
- "How much interest did I pay on BTC loans?"
**Expected Behavior**:
1. Fetch data via `list_unified_loan_interest_records` (optional filters).
2. Calculate per-record and optional aggregate interest summary.
3. Output `Interest Records Report` with raw timestamp and readable local time.
**Unexpected Behavior**:
1. Reports loan principal records as interest records.
2. Omits rate/time fields when available.
3. Uses stale cached values instead of latest query response.

## IV. Transferability and Risk Configuration (13-18)

## Scenario 13: Single-Currency Transferable Query
**Context**: User wants maximum transferable amount for one currency.
**Prompt Examples**:
- "How much USDT can I transfer out?"
**Expected Behavior**:
1. Fetch data via `get_unified_transferable` (`currency=target`).
2. Calculate normalized max transferable amount without rounding away API precision.
3. Output `Transferable Limit Report`.
**Unexpected Behavior**:
1. Treats transferable as equal to wallet balance without risk checks.
2. Returns another currency's amount due to mapping error.
3. Executes transfer actions when user asked only for query.

## Scenario 14: Multi-Currency Transferable Summary
**Context**: User wants transferable limits for multiple currencies.
**Prompt Examples**:
- "Check transferable for BTC, ETH, USDT."
**Expected Behavior**:
1. Fetch data via `get_unified_transferable` per currency (loop).
2. Calculate per-currency transferable summary.
3. Output `Multi-Currency Transferable Report`.
**Unexpected Behavior**:
1. Uses one currency result for all rows.
2. Skips currencies with zero amount without telling user.
3. Claims unsupported batch endpoint result without per-currency verification.

## Scenario 15: Query Leverage Settings
**Context**: User wants current leverage setting for one or more currencies.
**Prompt Examples**:
- "What is my ETH leverage setting?"
- "Show leverage settings for all currencies."
**Expected Behavior**:
1. Fetch data via `get_user_leverage_currency_setting` (optional currency filter).
2. Calculate readable leverage mapping.
3. Output `Leverage Settings Report`.
**Unexpected Behavior**:
1. Returns platform max leverage instead of user setting.
2. Omits requested currency in filtered query response.
3. Performs mutation when user asked for read-only check.

## Scenario 16: Set Leverage Setting
**Context**: User wants to update leverage for a currency.
**Prompt Examples**:
- "Set ETH leverage to 5."
**Expected Behavior**:
1. Fetch current context via `get_user_leverage_currency_setting` if needed and validate target value.
2. Calculate change summary and build `Leverage Update Draft`.
3. After explicit confirmation, execute via `set_user_leverage_currency_setting` and output `Leverage Update Result Report`.
**Unexpected Behavior**:
1. Executes leverage update without confirmation.
2. Accepts clearly invalid leverage value without validation feedback.
3. Returns success without showing final leverage setting.

## Scenario 17: Set Collateral Currencies
**Context**: User wants to enable/disable specific collateral currencies.
**Prompt Examples**:
- "Enable BTC and ETH as collateral."
- "Disable SOL as collateral."
**Expected Behavior**:
1. Fetch current context if available and validate enable/disable lists.
2. Calculate resulting collateral configuration and build `Collateral Update Draft`.
3. After explicit confirmation, execute via `set_unified_collateral` and output `Collateral Update Result Report`.
4. If API returns `500`, clearly classify as backend failure and provide retry guidance.
**Unexpected Behavior**:
1. Applies opposite direction (disables requested enable list).
2. Executes without showing final enable/disable list to user.
3. Executes without confirmation.

## Scenario 18: Query Collateral Discount Tiers
**Context**: User wants risk discount tier references for collateral valuation.
**Prompt Examples**:
- "Show unified collateral discount tiers."
**Expected Behavior**:
1. Fetch data via `list_currency_discount_tiers`.
2. Calculate tier summary by currency and discount range.
3. Output `Collateral Discount Tier Report`.
**Unexpected Behavior**:
1. Returns generic risk text without tier data.
2. Mixes tier ranges between currencies.
3. Attempts unrelated configuration mutation in a query-only request.
