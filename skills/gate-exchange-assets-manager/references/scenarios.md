# Scenarios

This document defines behaviour-oriented scenario templates for the 16 core use cases of the Account and Asset Manager L2 skill.

## Global Execution Gate (Mandatory)

**Strong confirmation · Action Draft** — For every scenario that includes write tool calls (`gate-cli cex unified loan create`, `gate-cli cex unified mode set`, `gate-cli cex unified config leverage-set`, `gate-cli cex unified config collateral`):

- Build and present an Action Draft first
- Require explicit confirmation from the immediately previous user turn
- Treat confirmation as single-use
- Re-confirm whenever parameters or intent change
- For multi-step flows, confirm each mutation step separately

**Write grading (align with SKILL.md section G)**

| Tier | Tools | Action Draft must include |
|------|-------|---------------------------|
| **Medium** | `gate-cli cex unified mode set`, `gate-cli cex unified config leverage-set`, `gate-cli cex unified config collateral` | Single confirmation plus risk disclosure; if **mode switch**, state clearly that **the mode change is irreversible** |
| **High** | `gate-cli cex unified loan create` (borrow/repay) | **Amount**, **currency**, and **interest rate** (estimated from read tools or shown by API), then user confirmation |

If confirmation is missing, ambiguous, or stale, do not execute any write tool call.

## Global Output Rules (Mandatory)

- Annotate data timestamp in every report section
- Keep API numeric precision as returned; do not round unless user explicitly asks
- When a query returns no data, use natural language "no records found" instead of listing tool names
- Liquidation prices and margin ratios are reference values; always note "subject to the exchange's actual liquidation rules"
- Asset data is limited to the user's own view and must not be leaked to other contexts

---

## I. Asset Overview (S1)

## Scenario 1: Full Account Asset Panorama
**Context**: User wants a complete view of all account balances across all sub-accounts.
**Prompt Examples**:
- "Check all my account balances."
- "How much do I have in total?"
- "Give me a full asset overview."
**Expected Behavior**:
1. Activate S1 signal.
2. Execute in parallel: `gate-cli cex wallet balance total`, `gate-cli cex spot account get`, `gate-cli cex unified account get`, `gate-cli cex futures account get`, `gate-cli cex margin account list`, `gate-cli cex options account get`, `gate-cli cex earn uni lends`, `gate-cli cex earn staking assets`, `gate-cli cex alpha account balances`, `gate-cli cex tradfi account assets`.
3. Aggregate per-account balances with percentage breakdown.
4. Output "Asset Panorama Report" with data timestamp.
5. Do not include earn interest or staking rewards (those require S3).

## Scenario 2: Transferable Limit Snapshot
**Context**: User wants to know the maximum transferable amount for a specific currency in the unified account.
**Prompt Examples**:
- "How much USDT can I transfer out of unified account?"
- "What is my transferable limit?"
**Expected Behavior**:
1. Activate S1 signal.
2. Execute in parallel: `gate-cli cex unified query transferable` (currency parameter from user), `gate-cli cex unified account get`.
3. Display transferable amount and relevant unified account equity fields.
4. Output "Transferable Limit Snapshot" with data timestamp.
5. Do not initiate any actual transfer or withdrawal operation.
6. Note: The previous "unified mode / futures-options toggle" query has been deprecated as a default scenario. `gate-cli cex unified mode get` remains in the L1 tool matrix — if the user explicitly asks about mode, it can be called independently, but it is not part of the default orchestration for this scenario.
7. On-chain withdrawal and internal transfer execution are not in scope for this skill. If user wants to initiate a transfer, route to the withdrawal/transfer capability or guide to the App.

## Scenario 3: Alpha and TradFi Balance Snapshot
**Context**: User asks about Alpha and TradFi account balances specifically.
**Prompt Examples**:
- "How much do I have in Alpha and TradFi?"
- "Show my Alpha account and TradFi balance."
**Expected Behavior**:
1. Activate S1 signal.
2. Execute in parallel: `gate-cli cex alpha account balances`, `gate-cli cex tradfi account assets`.
3. Display balances in two separate sections.
4. Note that these balances may not align with the main-site total due to independent API sources.

---

## II. Risk and Margin (S2)

## Scenario 4: Margin and Liquidation Risk Check
**Context**: User wants to know if their futures positions are at risk of liquidation.
**Prompt Examples**:
- "Will I get liquidated?"
- "Is my margin sufficient?"
- "Check my margin status."
**Expected Behavior**:
1. Activate S2 signal.
2. Execute in parallel: `gate-cli cex unified account get`, `gate-cli cex futures position list`, `gate-cli cex futures market tickers`, optionally `gate-cli cex futures market funding-rate`, `gate-cli cex futures market premium`.
3. Calculate margin ratio and distance-to-liquidation per position.
4. Output risk assessment with risk level classification.
5. Include disclaimer: "Liquidation prices are reference values. Subject to the exchange's actual liquidation rules."

## Scenario 5: Position Risk Table (Liquidation Price and Unrealised PnL)
**Context**: User wants detailed position-level risk data.
**Prompt Examples**:
- "Show my liquidation prices and unrealised PnL."
- "What are my position risks?"
**Expected Behavior**:
1. Activate S2 signal.
2. Execute in parallel: `gate-cli cex futures position list`, `gate-cli cex futures market tickers`, `gate-cli cex unified account get`, optionally `gate-cli cex futures market contract`.
3. Extract liquidation price, unrealised PnL, and mark price per position.
4. Output "Position Risk Table" with per-position breakdown.

---

## III. Earn Yield Snapshots (S3)

## Scenario 6: SimpleEarn and Staking Earnings Summary
**Context**: User wants to know combined earnings from SimpleEarn and staking.
**Prompt Examples**:
- "How much have I earned from SimpleEarn and staking?"
- "Show my earn interest and staking rewards."
**Expected Behavior**:
1. Activate S3 signal.
2. Execute in parallel: `gate-cli cex earn uni lends`, `gate-cli cex earn uni interest` (SimpleEarn), `gate-cli cex earn staking assets`, `gate-cli cex earn staking awards` (Staking).
3. Aggregate SimpleEarn interest and staking rewards separately.
4. Output "Earn Yield Snapshot" with two sections (SimpleEarn / Staking).
5. Do not combine into a "total income" figure across different business lines.

---

## IV. Affiliate and Rebate (S4)

## Scenario 7: Affiliate Commission Report
**Context**: User wants a full view of their rebate and commission status. `gate-cli cex rebate user-info` may return an empty object with no ready-made cumulative rebate fields; commission detail still comes from `gate-cli cex rebate partner commissions`.
**Prompt Examples**:
- "How much commission have I earned?"
- "Show my affiliate status and commissions."
**Expected Behavior**:
1. Activate S4 signal.
2. Execute in parallel: `gate-cli cex rebate user-info`, `gate-cli cex rebate partner commissions`, `gate-cli cex rebate partner sub-list`, `gate-cli cex rebate partner transactions`.
3. If `gate-cli cex rebate user-info` is empty, still build the affiliate section from commissions history and other S4 tools. Do not conclude that there is no affiliate data.
4. Summarise recent commission rows, `commissionAsset` breakdown (often USDT and POINT), and any per-row **source** fields (for example FUTURES, SPOT, TradFi, ALPHA) as returned by the API.
5. Do **not** invent a lifetime "total rebate" in USDT or POINT unless **all** pages of `gate-cli cex rebate partner commissions` were fetched (iterate offset/limit per API until no more rows) and `commissionAmount` was summed by `commissionAsset`. If only the first page was loaded, say so and avoid fabricated totals.
6. For an official cumulative figure without full pagination, direct the user to the Gate App or Web partner or rebate center.
7. Optionally offer to continue **rebate-only** pagination and report USDT and POINT totals from history; do not mix those totals with SimpleEarn, staking, or other yield sections.
8. Where applicable, aggregate client count and activity from partner sub list and transaction history tools.
9. Output "Affiliate Commission Report" with data timestamp.

## Scenario 8: Affiliate Identity and Relationship Snapshot
**Context**: User wants to know their affiliate role and client relationships without commission details.
**Prompt Examples**:
- "Am I an affiliate or a partner?"
- "Show my client relationships."
**Expected Behavior**:
1. Activate S4 signal.
2. Execute in parallel: `gate-cli cex rebate user-info`, `gate-cli cex rebate sub-relation`, `gate-cli cex rebate partner sub-list`.
3. Display role, relationship structure, and client count.
4. Do not call commission history unless explicitly requested.

---

## V. Write Operations (S5)

## Scenario 9: Borrow Execution
**Context**: User wants to borrow a specific amount from the unified account.
**Prompt Examples**:
- "Borrow 500 USDT."
- "I want to borrow some USDT from unified account."
**Expected Behavior**:
1. Activate S5 signal.
2. Execute in parallel: `gate-cli cex unified query borrowable` (currency=USDT), `gate-cli cex unified account get`, `gate-cli cex unified query estimate-rate`.
3. Display borrowable limit and estimated rate. **Rate semantics:** `gate-cli cex unified query estimate-rate` returns **hourly** estimated borrow rates (per currency); state "hourly" in user-facing text — do not label the raw value as annual APR unless converted and marked reference-only.
4. Generate **high-risk** Action Draft: operation=borrow, currency=USDT, amount=500 (or max if exceeded), rate=estimated **hourly** rate, risk="interest accrues hourly" (amount + currency + rate are mandatory fields).
5. Wait for explicit user confirmation.
6. After confirmation, execute `gate-cli cex unified loan create` (type=borrow, currency=USDT, amount=confirmed amount).
7. Output "Borrow Result Report".
8. Note: If user subsequently requests to open a position with borrowed funds, route to the trading copilot skill.

## Scenario 10: Add Margin / Set Collateral
**Context**: User wants to add margin to a futures position by setting collateral.
**Prompt Examples**:
- "Add margin to my futures position."
- "Set BTC as collateral in unified account."
**Expected Behavior**:
1. Activate S2 + S1 + S5 signals.
2. Phase 1 parallel read: `gate-cli cex unified account get`, `gate-cli cex spot account get`, `gate-cli cex futures position list`.
3. Evaluate available balance and position risk.
4. Generate Action Draft with collateral change details and risk note.
5. Wait for explicit user confirmation.
6. After confirmation, execute `gate-cli cex unified config collateral`.
7. Output execution result.

---

## VI. Multi-Signal Composite Scenarios

## Scenario 11: Asset Overview Plus Risk Check (S1 + S2)
**Context**: User wants both asset balances and margin/position risk in one query.
**Prompt Examples**:
- "How much do I have and will I get liquidated?"
- "Show my total assets and check futures risk."
**Expected Behavior**:
1. Activate S1 + S2 signals.
2. Execute all S1 and S2 tools in parallel (deduplicated).
3. Output structured report with S1 (asset panorama) and S2 (risk assessment) as separate sections.
4. Do not include earn interest (S3) unless explicitly asked.
5. Present factual data only; do not produce "health scores" or "risk ratings" beyond the data.
6. **Prohibited outputs**: Do not generate account "health" ratings, asset analysis/attribution, or implied PnL conclusions. When the user's phrasing omits "all accounts", still pull the full S1 scope. Do not include earn/staking yields (if also requested, activate S3 separately or split into a follow-up query).

## Scenario 12: Earn and Affiliate Snapshots (S3 + S4)
**Context**: User wants SimpleEarn/staking earnings and affiliate commissions in one query. If `gate-cli cex rebate user-info` is empty, the affiliate block still uses `gate-cli cex rebate partner commissions` per Scenario 7 rules.
**Prompt Examples**:
- "How much have I earned from SimpleEarn, staking, and affiliates?"
- "Show earnings and commissions separately."
**Expected Behavior**:
1. Activate S3 + S4 signals.
2. Execute all S3 and S4 tools in parallel.
3. Output three sections: SimpleEarn / Staking / Affiliate, each with independent data.
4. Do not combine into a "total income" or "total ledger" figure.
5. **Prohibited outputs**: Do not sum across sections; do not use phrases like "total income", "total ledger", or "PnL reconciliation". Each section reports only its own snapshot. Does not include futures PnL or cross-business-line calibration.
6. For S4, apply the same pagination and no-fabricated-total rules as Scenario 7 when reporting USDT or POINT rebate aggregates.

## Scenario 13: Emergency Margin Add (S2 + S1 + S5)
**Context**: User's futures position is near liquidation and they want to evaluate options and add margin.
**Prompt Examples**:
- "I am about to get liquidated, how much free spot balance do I have? Can I add margin or borrow?"
**Expected Behavior**:
1. Activate S2 + S1 + S5 signals.
2. Phase 1 parallel: S2 tools (position risk), S1 tools (spot balance), S5 read tools (borrowable, rate).
3. Evaluate: distance to liquidation + available spot balance + borrowable limit.
4. Generate Action Draft for add-margin or borrow operation.
5. Wait for explicit user confirmation.
6. After confirmation, execute the appropriate write tool.
7. Output combined risk assessment and execution result.

---

## VII. Inquiry-Only Scenarios (Read-Only, No S5)

## Scenario 14: Borrowable Limit Inquiry (No Execution)
**Context**: User wants to know how much they can borrow but explicitly does not want to execute.
**Prompt Examples**:
- "How much USDT can I borrow? Don't borrow yet."
- "What is the estimated borrow rate? Just checking."
**Expected Behavior**:
1. Activate S1 signal (inquiry subset), NOT S5.
2. Execute in parallel: `gate-cli cex unified query borrowable`, `gate-cli cex unified query estimate-rate`, `gate-cli cex unified account get`.
3. Display borrowable limit and estimated rate. **`gate-cli cex unified query estimate-rate`** values are **hourly** estimated borrow rates per currency (not annualized APR by default).
4. Do not generate Action Draft or enter write flow.
5. If user later says "go ahead and borrow", then activate S5 (Scenario 9).
6. Signal note: This scenario does NOT activate S5 (S5 is reserved for queries with execution intent — see Routing Rules). This is pure read mode; no Action Draft, no `create_loan` call. User wanting to actually borrow should use Scenario 9.

## Scenario 15: Per-Currency Leverage Setting Query
**Context**: User wants to check current leverage setting for a specific currency.
**Prompt Examples**:
- "What is my USDT leverage setting in unified account?"
- "Show my per-currency leverage configuration."
**Expected Behavior**:
1. Activate S1 signal.
2. Execute: `gate-cli cex unified config leverage-get` (currency parameter), `gate-cli cex unified account get`.
3. Display current leverage setting.
4. Note that modifying leverage requires explicit write operation with confirmation (S5).

## Scenario 16: Rebate USDT and POINT Totals With Empty user_info
**Context**: User asks for total partner commission in USDT and POINT but `gate-cli cex rebate user-info` returned an empty object, so there is no single API field for cumulative rebate. The user wants accurate totals from history or is okay with pagination.
**Prompt Examples**:
- "My rebate user info is empty. How much USDT and POINT commission did I get in total?"
- "Pull all pages of my partner commissions and sum USDT and POINT only."
**Expected Behavior**:
1. Activate S4 signal.
2. Call `gate-cli cex rebate partner commissions` with limit per page as supported by the API (for example 100) and offset 0, then repeat with increasing offset until the response returns no rows or fewer than one full page.
3. Sum `commissionAmount` separately for `commissionAsset` USDT and POINT (and other assets only if the user asked for them).
4. If the user stops early or the session does not finish all pages, report partial sums and state clearly that totals are incomplete; do not present incomplete sums as lifetime totals.
5. Remind the user that the Gate App or Web partner or rebate center shows official cumulative figures.
6. Do not add these rebate totals to earn or staking figures in the same breath.
