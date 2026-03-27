---
name: gate-exchange-coupon
version: "2026.3.23-1"
updated: "2026-03-23"
description: "The coupon management function of Gate Exchange: query available coupons, check coupon details, view usage rules, and trace coupon source. Use this skill whenever the user asks about their coupons, vouchers, or bonus cards on Gate Exchange. Trigger phrases include 'my coupons', 'do I have any coupons', 'coupon list', 'check my voucher', 'coupon details', 'when does my coupon expire', 'coupon rules', 'how did I get this coupon', 'coupon source'."
---

# Gate Coupon Assistant

Query and inspect coupon/voucher accounts on Gate Exchange. Supports six scenarios: list available coupons, search by coupon type, view expired/used history, view full coupon details, read usage rules, and trace coupon acquisition source.

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

### MCP Tools Used

**Query Operations (Read-only)**

- cex_coupon_get_user_coupon_detail
- cex_coupon_list_user_coupons

### Authentication
- API Key Required: Yes (see skill doc/runtime MCP deployment)
- Permissions: Coupon:Read
- Get API Key: https://www.gate.io/myaccount/profile/api-key/manage

### Installation Check
- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## Domain Knowledge

### MCP Tool Mapping


| Tool                                | Description                                                   |
| ----------------------------------- | ------------------------------------------------------------- |
| `cex_coupon_list_user_coupons`      | Fetch user coupon list (paginated, filterable by type/status) |
| `cex_coupon_get_user_coupon_detail` | Fetch full details of a single coupon                         |


### Coupon Types Reference

> **IMPORTANT — Type Translation Rule**: When displaying the coupon type, map `coupon_type` strictly to the Display Name. You may translate Display Names to match the response language, but **the mapping must be exact** — never swap or conflate two different types. Critical distinction: `position_voucher` (Position Trial Voucher) is a **position-based trial voucher** — translate as "仓位体验券" in Chinese, never as "合约体验金"; `contract_bonus` (Futures Bonus) is **futures trial funds** — translate as "合约体验金". They are completely different products.

| `coupon_type`             | Display Name                          | Description                                                                                                           |
| ------------------------- | ------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `position_voucher`        | Position Trial Voucher                | Virtual capital for opening futures positions (NOT the same as Futures Bonus). Profits can be withdrawn; the principal is reclaimed after expiry. |
| `tradfi_position_voucher` | TradFi Position Voucher               | Same concept as position voucher but applies to TradFi instruments (stocks, forex, etc.).                             |
| `contract_bonus`          | Futures Bonus                         | Trial funds usable in futures trading. Unused balance is reclaimed at expiry.                                         |
| `contract_bonus_new`      | Futures Voucher                       | Newer futures trial funds with configurable leverage and trading pair restrictions; valid for a set number of hours.   |
| `commission_rebate`       | Commission Rebate Voucher             | Rebates a percentage of actual trading fees incurred on applicable markets; reusable until the balance runs out.      |
| `hold_bonus`              | Earn Bonus                            | Trial funds for Earn products (e.g. Lend & Earn); reclaimed at expiry.                                                |
| `point`                   | Points Card                           | Platform points redeemable for rewards or used in activities.                                                         |
| `financial_rate`          | Rate Boost Voucher                    | Adds extra APR on top of the base rate for eligible Earn products, up to a capped amount.                             |
| `robot_bonus`             | Bot Bonus                             | Trial funds for trading bots (e.g. Grid, Futures Grid); runs for a fixed duration then is reclaimed.                  |
| `loss_protection_copier`  | Copy Trading Protection               | Compensates a portion of copy trading losses, subject to a maximum payout and eligible-trader restrictions.           |
| `vip_card`                | VIP Trial Card                        | Grants temporary VIP-tier fee rates and benefits for a fixed number of days after activation.                         |
| `interest_voucher`        | Margin Interest Discount Voucher      | Reduces the interest rate on isolated-margin borrowing by a set percentage, up to a maximum discount amount.          |
| `p2p`                     | P2P Discount Voucher                  | Deducts a percentage of P2P trading fees, subject to a cap and a minimum transaction size.                            |
| `cash`                    | Cash Voucher                          | Redeemable for account balance cash; credited once qualifying conditions are met.                                     |
| `crypto_loan_interest`    | Crypto Loan Interest Discount Voucher | Reduces interest on crypto-collateral loans (flexible term), subject to a maximum discount and minimum loan amount.   |
| `copy_trading`            | Copy Trading Bonus                    | Trial funds for copy trading; supports specific or all traders, with a stop-loss limit and fixed trial duration.      |
| `alpha_voucher`           | Alpha Cash Voucher                    | Cash credit usable for purchasing tokens on Gate Alpha market.                                                        |
| `etf_voucher`             | ETF Bonus                             | Trial funds for leveraged ETF trading, valid for a set number of hours on specified ETF pairs.                        |


### Status Reference


| Status                     | Meaning                                                       |
| -------------------------- | ------------------------------------------------------------- |
| `NOT_ACTIVE`               | Pending activation                                            |
| `ACTIVATED`                | Activated                                                     |
| `TO_BE_USED`               | Available, not yet used                                       |
| `EXPIRED`                  | Expired (unused)                                              |
| `USED`                     | Used/consumed                                                 |
| `RECYCLED`                 | Recycled by platform                                          |
| `INVALID`                  | Invalidated                                                   |
| `TASK_WAIT`                | Task in progress                                              |
| `TASK_DONE`                | Task completed, reward processing                             |
| `TASK_RECEIVE_SUCCESS`     | Task reward received                                          |
| `TASK_EXPIRED`             | Task expired before completion                                |
| `TASK_START`               | Task not yet started (coupon issued, task pending activation) |
| `TASK_NOT_STARTED_EXPIRED` | Task expired before it started                                |
| `TASK_RECEIVE_FAIL`        | Task reward claim failed                                      |
| `UNKNOWN`                  | Unknown status                                                |


### `cex_coupon_list_user_coupons` Parameters


| Parameter        | Default  | Description                                                                                                     |
| ---------------- | -------- | --------------------------------------------------------------------------------------------------------------- |
| `expired`        | `0`      | `0` = valid coupons; `1` = expired/used coupons                                                                 |
| `limit`          | `20`     | Page size (1–20)                                                                                                |
| `last_id`        | `0`      | Cursor pagination: last id from previous page                                                                   |
| `expire_time`    | `0`      | Cursor pagination: `expire_time_order_by` of the last item from the previous page; used together with `last_id` |
| `order_by`       | `latest` | `latest` = by acquisition time; `expired` = by expiry asc                                                       |
| `coupon_type`    | (all)    | Filter by coupon type                                                                                           |
| `is_task_coupon` | (all)    | `0` = regular only; `1` = task coupons only                                                                     |


### `cex_coupon_get_user_coupon_detail` Parameters


| Parameter        | Required | Description                                                         |
| ---------------- | -------- | ------------------------------------------------------------------- |
| `coupon_type`    | Yes      | Coupon type string                                                  |
| `detail_id`      | Yes      | Regular coupon: `details_id` from list; Task coupon: `id` from list |
| `is_task_coupon` | No       | `0` = regular (default); `1` = task coupon                          |


## Routing Rules

Classify the user intent and route to the matching reference document:


| Intent                         | Example Phrases                                                                                                          | Route to                                                               |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| **List available coupons**     | "What coupons do I have?", "Show my available coupons", "Do I have any vouchers?", "Check my coupon balance"             | Read `references/list-coupons.md`                                      |
| **Search by coupon type**      | "Do I have a commission rebate voucher?", "Check if I have a futures bonus", "Show my VIP trial cards"                   | Read `references/list-coupons.md`                                      |
| **View coupon details**        | "Show details of my commission rebate coupon", "What are the details of this voucher?", "How much is left on my coupon?" | Read `references/coupon-detail.md`                                     |
| **View usage rules**           | "What are the rules for this coupon?", "How do I use this voucher?", "What are the terms of my futures bonus?"           | Read `references/coupon-detail.md`                                     |
| **Trace coupon source**        | "How did I get this coupon?", "Where did this voucher come from?", "What activity gave me this coupon?"                  | Read `references/coupon-detail.md`                                     |
| **Query expired/used coupons** | "Show my used coupons", "List my expired vouchers", "What coupons have I used?"                                          | Read `references/list-coupons.md`                                      |
| **Unclear**                    | "Tell me about my coupons", "coupon help"                                                                                | Clarify: ask if user wants to list all coupons or check a specific one |


## Execution

1. Identify user intent from the Routing Rules table above.
2. Load the corresponding reference document.
3. Follow the workflow in that document step by step.
4. All operations are read-only — no confirmation gate required.

## Error Handling


| Situation                        | Action                                                                                                                                         |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Coupon not found                 | Coupon record does not exist or does not belong to current user. Ask user to re-check which coupon they meant; re-fetch list to get valid IDs. |
| Invalid coupon type              | `coupon_type` is not a recognized enum value. Map user's natural language to the Coupon Types Reference table and retry.                       |
| No coupons returned              | Inform user no coupons match the query. Suggest earning coupons through tasks, activities, or referrals.                                       |
| Coupon type unrecognized by user | User mentions a vague or informal name. Clarify by listing the closest matching type names from the Coupon Types Reference.                    |


## Safety Rules

- All operations in this skill are **read-only** (query only, no writes).
- Never request or expose user API secrets in the conversation.
- Do not infer or guess coupon IDs — always obtain them from the list API first.

