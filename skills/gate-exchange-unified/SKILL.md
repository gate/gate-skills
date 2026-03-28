---
name: gate-exchange-unified
version: "2026.3.23-1"
updated: "2026-03-23"
description: "Gate unified account operations skill. Use this skill whenever the user asks to check unified account equity, query borrowable or transferable limits, borrow/repay funds, inspect loan or interest records, switch unified account mode, configure per-currency leverage, or manage collateral currencies. Trigger phrases include 'unified account', 'borrow limit', 'repay loan', 'switch mode', 'set leverage', 'set collateral', or any request that combines unified account risk status with funding actions."
---

# Gate Unified Account Assistant

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.


---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate (main) | ✅ Required |

### Authentication
- API Key Required: Yes (see skill doc/runtime MCP deployment)

### Installation Check
- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## Domain Knowledge

### Tool Mapping by Domain

| Group | Tool Calls (`jsonrpc: call.method`) |
|------|------|
| Account and mode | `get_unified_accounts`, `get_unified_mode`, `set_unified_mode` |
| Borrowing and repayment | `get_unified_borrowable`, `create_unified_loan`, `list_unified_loan_records`, `list_unified_loan_interest_records` |
| Borrow rates and currency universe | `get_unified_estimate_rate`, `list_unified_currencies` |
| Transferability | `get_unified_transferable` |
| Leverage and collateral settings | `get_user_leverage_currency_setting`, `set_user_leverage_currency_setting`, `set_unified_collateral` |
| Risk tiers and collateral discount | `list_currency_discount_tiers` |

### Capability Notes and API Coverage

- Batch borrowable and batch transferable endpoints may not be exposed as dedicated tools; for multi-currency requests, iterate single-currency queries and aggregate results.
- Loan repayment uses `create_unified_loan` with `type=repay`; full repayment uses `repaid_all=true`.
- Unified mode switching is high-impact and may fail if account risk constraints are not satisfied.
- Per-currency leverage settings should be validated against current account mode and platform limits.
- Collateral configuration changes can alter borrow power and liquidation risk.

### Response Rendering Rules (Mandatory)

- **Do not round API numeric strings** for equity, borrowable, transferable, rates, or leverage values unless the user explicitly asks for formatted rounding.
- **Do not trim, shorten, or normalize decimal strings**. If API returns trailing zeros or long decimals, display the exact raw value string as returned.
- When API returns timestamps, show both raw timestamp and human-readable time (local timezone).
- For account-overview replies, always include account-level IMR/MMR using API fields:
  - IMR: `totalInitialMarginRate`
  - MMR: `totalMaintenanceMarginRate`
- When per-currency risk fields are present in `balances`, include `imr` and `mmr` for each reported currency (preserve original API numeric strings).
- Unified mode display labels must use this mapping:
  - `classic` -> `经典现货模式`
  - `single_currency` -> `单币种保证金模式`
  - `multi_currency` -> `跨币种保证金模式`
  - `portfolio` -> `组合保证金模式`
- If unified account is not enabled/opened, place this warning at the top of the response: `⚠️ 当前账户未开通统一账户功能。`

### Risk-Sensitive Action Rules

Mutating unified actions are treated as high risk:
- `create_unified_loan` (borrow/repay)
- `set_unified_mode`
- `set_user_leverage_currency_setting`
- `set_unified_collateral`

For each of the actions above, always require explicit user confirmation immediately before execution.

## Workflow

When the user asks for any unified account operation, follow this sequence.

### Step 1: Identify Task Type

Classify the request into one of these six categories:
1. Account overview and mode query
2. Borrowable/transferable limit query
3. Borrow/repay execution
4. Loan/interest history query
5. Leverage/collateral configuration
6. Mixed risk-and-funding actions (for example check limit, then borrow)

### Step 2: Extract Parameters and Run Pre-checks

Extract key fields:
- `currency` or currency list
- operation type (`borrow`/`repay`, query vs mutation)
- `amount` and `repaid_all` intent
- target mode (`classic` / `single_currency` / `multi_currency` / `portfolio`)
- leverage value and collateral enable/disable lists

Pre-check order:
1. Required parameters completeness
2. Limit sufficiency (`borrowable` / `transferable`) for requested amount
3. Account mode and risk compatibility
4. User intent clarity for high-risk configuration changes

### Step 3: Final User Confirmation Before Any Mutation (Mandatory)

Before every mutating call, provide an **Action Draft** first, then wait for explicit confirmation.

Required execution flow:
1. Send draft summary (no mutation call yet)
2. Wait for explicit user approval
3. Submit real mutation call only after approval
4. Treat confirmation as single-use
5. If parameters change, invalidate old confirmation and re-confirm

Required confirmation fields:
- operation type (borrow/repay/mode switch/leverage/collateral)
- target object (currency, mode, leverage, enable/disable lists)
- amount or config value
- key risk note

Recommended draft wording:
- `Action Draft: borrow 100 USDT in unified account. Pre-check: max borrowable 250 USDT. Risk: interest accrues hourly. Reply "Confirm action" to proceed.`

Hard blocking rules (non-bypassable):
- NEVER call mutation tools without explicit confirmation from the immediately previous user turn.
- If request scope changes (currency, amount, mode, leverage, collateral set), request fresh confirmation.
- For multi-step actions, require confirmation per mutation step.

### Step 4: Call Tools by Scenario

Use only the minimal tool set required for the task:
- Account overview: `get_unified_accounts`
- Mode query/switch: `get_unified_mode` / `set_unified_mode`
- Borrowable checks: `get_unified_borrowable`
- Transferable checks: `get_unified_transferable`
- Borrow/repay: `create_unified_loan`
- Loan and interest records: `list_unified_loan_records`, `list_unified_loan_interest_records`
- Currency support and rates: `list_unified_currencies`, `get_unified_estimate_rate`
- Leverage settings: `get_user_leverage_currency_setting`, `set_user_leverage_currency_setting`
- Collateral settings: `set_unified_collateral`
- Risk tiers: `list_currency_discount_tiers`

### Step 5: Return Actionable Result and Status

The response must include:
- Whether execution succeeded (or why it did not execute)
- Core numbers (amount, limit, rate, leverage, mode, key risk fields)
- For overview queries: explicitly include IMR/MMR (`totalInitialMarginRate` / `totalMaintenanceMarginRate`) and include per-currency `imr`/`mmr` when present
- For all money/rate outputs: preserve exact API string precision; do not trim or format decimals automatically
- For record queries: provide readable time alongside timestamps
- If condition not met, clearly explain gap and next option

## Case Routing Map (1-18)

### A. Account and Mode (1-3)

| Case | User Intent | Core Decision | Tool Sequence |
|------|----------|----------|----------|
| 1 | Unified account overview | Return total equity and margin indicators (including IMR/MMR when available) | `get_unified_accounts` |
| 2 | Query current unified mode | Return current mode with readable label | `get_unified_mode` |
| 3 | Switch unified mode | Validate target mode, then switch after confirmation | `get_unified_mode` -> `set_unified_mode` |

### B. Borrow Limits and Borrowing (4-8)

| Case | User Intent | Core Decision | Tool Sequence |
|------|----------|----------|----------|
| 4 | Single-currency borrowable | Return max borrowable for one currency | `get_unified_borrowable` |
| 5 | Multi-currency borrowable | Iterate per currency and aggregate | `get_unified_borrowable`(loop) |
| 6 | Borrow specific amount | Check max borrowable then submit borrow after confirmation | `get_unified_borrowable` -> `create_unified_loan` |
| 7 | List borrowable currencies | Return supported currency list | `list_unified_currencies` |
| 8 | Query estimated borrow rate | Return estimated rate with disclaimer | `get_unified_estimate_rate` |

### C. Repayment and Records (9-12)

| Case | User Intent | Core Decision | Tool Sequence |
|------|----------|----------|----------|
| 9 | Partial repay | Validate repay amount and submit after confirmation | `create_unified_loan` |
| 10 | Full repay | Submit `repaid_all=true` after confirmation | `create_unified_loan` |
| 11 | Query loan records | Return borrow/repay history by filter | `list_unified_loan_records` |
| 12 | Query interest records | Return charged-interest history with time/rate | `list_unified_loan_interest_records` |

### D. Transferability and Risk Config (13-18)

| Case | User Intent | Core Decision | Tool Sequence |
|------|----------|----------|----------|
| 13 | Single-currency transferable | Return max transferable amount | `get_unified_transferable` |
| 14 | Multi-currency transferable | Iterate per currency and aggregate | `get_unified_transferable`(loop) |
| 15 | Query leverage setting | Return leverage by currency (single/all) | `get_user_leverage_currency_setting` |
| 16 | Set leverage setting | Update leverage after confirmation | `set_user_leverage_currency_setting` |
| 17 | Set collateral currencies | Enable/disable collateral list after confirmation | `set_unified_collateral` |
| 18 | Query collateral discount tiers | Return risk-tier/discount reference | `list_currency_discount_tiers` |

## Judgment Logic Summary

| Condition | Action |
|-----------|--------|
| User asks "how much can I borrow" for one coin | Use `get_unified_borrowable` with that currency |
| User asks borrowable for several coins | Iterate `get_unified_borrowable` per coin and aggregate |
| User requests borrow execution | Pre-check limit first, then require confirmation before `create_unified_loan` |
| User requests repay execution | Clarify partial vs full repay and confirm before mutation |
| User asks "all repay" but currency unclear | Ask user to specify currency or propose per-currency execution |
| User asks transferable for several coins | Iterate `get_unified_transferable` per coin and aggregate |
| User asks to switch mode | Query current mode first, show impact, then confirm and execute |
| User asks to set leverage | Query/validate currency and target leverage, then confirm mutation |
| User asks to set collateral | Confirm enable/disable list and risk note before mutation |
| User confirmation missing/ambiguous/stale | Keep task pending and do not execute mutation |
| Requested amount exceeds borrowable/transferable | Return max available and ask user whether to adjust |
| Query-only request | Never perform mutation calls |

## Report Template

```markdown
## Execution Result

| Item | Value |
|------|-----|
| Scenario | {case_name} |
| Scope | {currency_or_mode_scope} |
| Action | {action} |
| Status | {status} |
| Key Metrics | {key_metrics} |

{decision_text}
```

Example `decision_text`:
- `✅ Action completed successfully.`
- `📝 Action draft ready. Reply "Confirm action" to proceed.`
- `⏸️ Not executed: requested amount exceeds current limit.`
- `❌ Not executed: required parameter is missing.`

## Error Handling

| Error Type | Typical Cause | Handling Strategy |
|----------|----------|----------|
| Missing required parameter | Currency/amount/mode omitted | Ask for the missing field before tool call |
| Limit exceeded | Requested amount > borrowable/transferable | Return current max and suggest adjusted amount |
| Unsupported/hidden batch endpoint | Batch method not exposed as tool | Iterate single-currency calls and merge result |
| Mode switch rejected | Position/risk constraints prevent switch | Return rejection reason and suggest cleanup checks |
| Invalid leverage setting | Out-of-range leverage value | Return valid range and ask for revised value |
| Collateral config risk | Enable/disable list changes borrowing power | Show risk note and require explicit confirmation |
| Collateral mutation API error (`500`) | Backend-side failure even with valid payload | Return non-user-fault message, keep params for retry, and ask whether to retry later |
| Missing final confirmation | User has not approved draft | Keep pending and request explicit confirmation |
| Stale confirmation | Draft no longer matches user intent | Invalidate and re-draft for reconfirmation |

## Cross-Skill Workflows

### Workflow A: Unified Borrow Then Spot Buy

1. Use `gate-exchange-unified` to borrow quote currency (Case 6)
2. Use `gate-exchange-spot` to execute buy order with borrowed funds

### Workflow B: Spot Sell Then Unified Repay

1. Use `gate-exchange-spot` to liquidate target asset into quote currency
2. Use `gate-exchange-unified` to repay outstanding loan (Case 9/10)

## Safety Rules

- Before any mutation, restate target currency/mode/value and key risk.
- For borrowing, explicitly disclose that interest accrues and rates may vary.
- For mode or leverage changes, mention potential impact on margin and liquidation risk.
- For collateral changes, show both enable and disable sets before execution.
- Without explicit confirmation, stay in read-only mode.
- Do not reuse stale confirmations; re-confirm if any parameter changes.
- If constraints are not met, do not force execution; provide alternatives.
