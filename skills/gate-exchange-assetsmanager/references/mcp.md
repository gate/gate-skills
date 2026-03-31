---
name: gate-exchange-assetsmanager-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for cross-account asset manager (L2): multi-account overview, risk checks, earn/alpha/rebate aggregation, and unified-account mutations."
---

# Gate Assets Manager MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Multi-account asset overview (spot/futures/margin/options/tradfi/unified/earn/alpha/rebate)
- Risk snapshots and account-health summary
- Unified-account write actions exposed in this skill

Out of scope:
- Direct spot/futures order execution
- On-chain DEX wallet operations

## 2. MCP Detection and Fallback

Detection:
1. Confirm Gate MCP is available.
2. Probe with one baseline read (`cex_wallet_get_total_balance` or `cex_unified_get_unified_accounts`).

Fallback:
- If partial modules fail, return partial report with degraded markers per module.
- If write module unavailable, keep skill in read-only mode and disclose limitation.

## 3. Authentication

- API key required for account data and mutations.
- For unified mutations, require proper permission and explicit confirmation.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

### 5.1 Portfolio aggregation (read)

- `cex_wallet_get_total_balance`
- `cex_spot_get_spot_accounts`
- `cex_margin_list_margin_accounts`
- `cex_fx_get_fx_accounts`
- `cex_fx_list_fx_positions`
- `cex_options_list_options_account`
- `cex_tradfi_query_user_assets`
- `cex_unified_get_unified_accounts`

### 5.2 Market/reference context (read)

- `cex_spot_get_spot_tickers`
- `cex_spot_get_spot_candlesticks`
- `cex_spot_get_spot_order_book`
- `cex_spot_get_spot_trades`
- `cex_fx_get_fx_tickers`
- `cex_fx_get_fx_candlesticks`
- `cex_fx_get_fx_order_book`
- `cex_fx_get_fx_trades`
- `cex_fx_get_fx_contract`
- `cex_fx_get_fx_funding_rate`
- `cex_fx_get_fx_premium_index`

### 5.3 Earn/alpha/rebate modules (read)

- `cex_alpha_list_alpha_accounts`
- `cex_alpha_list_alpha_tokens`
- `cex_alpha_list_alpha_tickers`
- `cex_alpha_list_alpha_currencies`
- `cex_earn_asset_list`
- `cex_earn_award_list`
- `cex_earn_find_coin`
- `cex_earn_get_uni_currency`
- `cex_earn_get_uni_interest`
- `cex_earn_list_uni_rate`
- `cex_earn_list_user_uni_lends`
- `cex_earn_list_dual_balance`
- `cex_earn_list_dual_orders`
- `cex_earn_list_structured_orders`
- `cex_earn_order_list`
- `cex_earn_list_uni_currencies`
- `cex_rebate_broker_commission_history`
- `cex_rebate_broker_transaction_history`
- `cex_rebate_partner_commissions_history`
- `cex_rebate_partner_transaction_history`
- `cex_rebate_partner_sub_list`
- `cex_rebate_user_info`
- `cex_rebate_user_sub_relation`

### 5.4 Ledger/risk helpers (read)

- `cex_spot_list_spot_account_book`
- `cex_fx_list_fx_liq_orders`
- `cex_unified_get_unified_mode`
- `cex_unified_get_unified_borrowable`
- `cex_unified_get_unified_transferable`
- `cex_unified_get_unified_estimate_rate`
- `cex_unified_get_user_leverage_currency_setting`
- `cex_unified_list_currency_discount_tiers`
- `cex_unified_list_unified_currencies`
- `cex_unified_list_unified_loan_records`
- `cex_unified_list_unified_loan_interest_records`

### 5.5 Mutations (write)

- `cex_unified_create_unified_loan`
- `cex_unified_set_unified_mode`
- `cex_unified_set_unified_collateral`
- `cex_unified_set_user_leverage_currency_setting`

## 6. Execution SOP (Non-Skippable)

1. Determine user target modules (portfolio only vs include risk vs include mutation).
2. Execute read modules in parallel where independent.
3. Merge data with explicit module tags and timestamps.
4. For any mutation, present action draft and require explicit confirmation.
5. Execute mutation only after confirmation; re-read relevant account state.

## 7. Output Templates

```markdown
## Assets Manager Snapshot
- Total Balance: {total_balance}
- Core Accounts: {spot/futures/margin/options/unified summary}
- Risk Flags: {imr_mmr_liquidation_signals}
- Earn/Alpha/Rebate: {module_highlights}
- Data Freshness: {timestamps}
```

```markdown
## Unified Mutation Draft
- Action: {borrow/repay/mode/collateral/leverage}
- Target: {currency_or_mode}
- Value: {amount_or_setting}
- Risk: {key_risk_note}
Reply "Confirm action" to execute.
```

## 8. Safety and Degradation Rules

1. Distinguish read aggregation from write execution clearly.
2. On partial module failure, keep successful modules and mark failed modules explicitly.
3. Never execute unified mutations without explicit immediate confirmation.
4. Keep numeric precision as returned by APIs (no silent rounding for risk fields).
5. For stale/empty modules, return "no data / unavailable" instead of inferred numbers.
