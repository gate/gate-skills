---
name: gate-exchange-collateralloan
version: "2026.3.23-1"
updated: "2026-03-23"
description: "Gate multi-collateral loan management skill. Use when the user asks to borrow crypto against collateral, create current or fixed-term loans, repay outstanding loans, add or redeem collateral, view loan orders and details, or check LTV thresholds and interest rates. Triggers on 'collateral loan', 'current loan', 'fixed loan', 'repay', 'add collateral', 'redeem collateral'."
---

# Gate Exchange Multi-Collateral Loan Skill

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
- Permissions: Mcl:Write
- Get API Key: https://www.gate.io/myaccount/profile/api-key/manage

### Installation Check
- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), then execute this skill's collateral-loan workflow.

- `SKILL.md` keeps routing and product constraints.
- `references/mcp.md` is the authoritative MCP execution layer for quota/LTV pre-checks, confirmation gates, and post-action verification.

## Trigger Conditions

This skill activates when the user asks about multi-collateral loan operations. Classify intent via **Routing Rules** (Cases 1–7). Trigger phrases include: "collateral loan", "current loan", "fixed loan", "repay", "add collateral", "redeem collateral", or equivalent in other languages.

## Workflow

### Step 1: Classify intent

Identify the user intent using Routing Rules (Cases 1–7). If required inputs are missing (order_id, currency, amount, fixed term), ask clarifying questions before proceeding.

### Step 2: Read-only requests (rates, LTV, quota, orders)

Call the corresponding MCP tool when the user asks for rates, LTV, quota, order list, or order detail.

Call `cex_mcl_list_user_currency_quota` with:
- `type`: `collateral` or `borrow`
- `currency`: comma-separated (borrow: single currency)

Call `cex_mcl_get_multi_collateral_ltv` with:
- (no params)

Call `cex_mcl_get_multi_collateral_fix_rate` with:
- (no params)

Call `cex_mcl_get_multi_collateral_current_rate` with:
- `currencies`: comma-separated currency list

Call `cex_mcl_list_multi_collateral_orders` with:
- `page`, `limit` (optional)
- `sort` (optional): `time_desc`, `ltv_asc`, `ltv_desc`
- `order_type` (optional): `current` or `fixed`

Call `cex_mcl_get_multi_collateral_order_detail` with:
- `order_id`

Key data to extract:
- LTV thresholds, fixed/current rates, quota rows, order_id, order status, collateral and borrow details

### Step 3: Create loan (current or fixed)

If current loan:
1) Build draft (collateral list + borrow currency/amount).
2) Ask for confirmation.
3) Call `cex_mcl_create_multi_collateral` with **`order`** JSON string:
```json
{
  "borrow_currency": "USDT",
  "borrow_amount": "1000",
  "collateral_currencies": [{"currency": "BTC", "amount": "0.05"}],
  "order_type": "current"
}
```

If fixed loan:
1) Call `cex_mcl_get_multi_collateral_fix_rate` (returns a **list**); **filter by borrow_currency**; take `rate_7d` or `rate_30d` as **fixed_rate** (hourly rate; pass through unchanged, do not convert or relabel as annual/daily). If no row matches, stop and inform the user that fixed rate is unavailable.
2) Build draft with fixed_type and fixed_rate (describe to user as hourly rate if showing).
3) Ask for confirmation.
4) Call `cex_mcl_create_multi_collateral` with **`order`** JSON string:
```json
{
  "borrow_currency": "USDT",
  "borrow_amount": "1000",
  "collateral_currencies": [{"currency": "ETH", "amount": "1.5"}],
  "order_type": "fixed",
  "fixed_type": "7d",
  "fixed_rate": "0.0001"
}
```
Note: `fixed_type` must be `7d` or `30d` (lowercase). `fixed_rate` is the hourly rate from the fix_rate tool — pass as-is.

### Step 4: Repay

Build draft, ask confirmation, then call `cex_mcl_repay_mcl` with **`repay_loan`** JSON string:
```json
{
  "order_id": "12345",
  "repay_items": [{"currency": "USDT", "amount": "500", "repaid_all": false}]
}
```

### Step 5: Add or redeem collateral

Build draft, ask confirmation, then call `cex_mcl_operate_multi_collateral` with **`collateral_adjust`** JSON string:
```json
{
  "order_id": "12345",
  "type": "append",
  "collaterals": [{"currency": "BTC", "amount": "0.01"}]
}
```
Use `type: "redeem"` to withdraw collateral instead.

### Step 6: Post-execution verification

After any write operation (create loan, repay, adjust collateral), call the corresponding read tool to confirm success:
- After loan creation: call `cex_mcl_get_multi_collateral_order_detail` with the returned `order_id` to verify the loan was created with correct parameters.
- After repay: call `cex_mcl_get_multi_collateral_order_detail` to confirm the updated principal/interest.
- After collateral adjustment: call `cex_mcl_get_multi_collateral_order_detail` to verify the updated collateral amounts and LTV.

## Report Template

**When asking for confirmation**:
Draft:
- Type: {current|fixed|repay|append|redeem}
- Order ID: {order_id if applicable}
- Borrow: {borrow_amount} {borrow_currency}
- Collateral: {collateral_amounts}
- Fixed term/rate: {fixed_type} / {fixed_rate} (hourly rate)

Please confirm to proceed.

**On success**:
- Summary of action and key identifiers (order_id, amounts).

**On failure**:
- Error message and next-step guidance (e.g., check currency/amount/LTV).

## Prerequisites

- **MCP Dependency**: Requires [gate-mcp](https://github.com/gate/gate-mcp) to be installed.
- **Authentication**: Order list, detail, repay, collateral, quota, and records require API key; LTV, fix rate, and current rate are public without key.
- **Disclaimer**: Loan and LTV information is for reference only and does not constitute investment advice. Understand product terms and liquidation risk before borrowing.

## Available MCP Tools

| Tool | Auth | Description | Reference |
|------|------|-------------|-----------|
| `cex_mcl_get_multi_collateral_fix_rate` | No | 7d/30d fixed rates (list) | `references/mcl-mcp-tools.md` |
| `cex_mcl_get_multi_collateral_ltv` | No | LTV thresholds | `references/mcl-mcp-tools.md` |
| `cex_mcl_get_multi_collateral_current_rate` | No | Current rates | `references/mcl-mcp-tools.md` |
| `cex_mcl_list_user_currency_quota` | Yes | Borrow/collateral quota | `references/mcl-mcp-tools.md` |
| `cex_mcl_create_multi_collateral` | Yes | Create loan (`order` JSON) | `references/mcl-mcp-tools.md` |
| `cex_mcl_list_multi_collateral_orders` | Yes | List orders | `references/mcl-mcp-tools.md` |
| `cex_mcl_get_multi_collateral_order_detail` | Yes | Order detail | `references/mcl-mcp-tools.md` |
| `cex_mcl_repay_mcl` | Yes | Repay (`repay_loan` JSON) | `references/mcl-mcp-tools.md` |
| `cex_mcl_operate_multi_collateral` | Yes | Add/redeem collateral (`collateral_adjust` JSON) | `references/mcl-mcp-tools.md` |
| `cex_mcl_list_multi_repay_records` | Yes | Repay history | `references/mcl-mcp-tools.md` |
| `cex_mcl_list_multi_collateral_records` | Yes | Collateral history | `references/mcl-mcp-tools.md` |

## Routing Rules

| Case | User Intent | Signal Keywords | Action |
|------|-------------|-----------------|--------|
| 1 | Create current loan | "current loan", "pledge ... borrow ... (current)" | See `references/scenarios.md` Scenario 1 |
| 2 | Create fixed loan | "fixed loan", "borrow ... for 7/30 days" | See `references/scenarios.md` Scenario 2 |
| 3 | Repay | "repay", "repay order ..." | See `references/scenarios.md` Scenario 3 |
| 4 | Add collateral | "add collateral", "add margin" | See `references/scenarios.md` Scenario 4 |
| 5 | Redeem collateral | "redeem collateral", "reduce margin" | See `references/scenarios.md` Scenario 5 |
| 6 | List orders / order detail | "loan orders", "order detail", "my orders" | `cex_mcl_list_multi_collateral_orders` / `cex_mcl_get_multi_collateral_order_detail` — **never include any time/date fields** in the user-facing reply (see Presentation below) |
| 7 | Auth failure (401/403) | MCP returns 401/403 | Do not expose keys; prompt user to configure Gate CEX API Key (multi-collateral loan). |

## Domain Knowledge

- **Current loan**: Flexible-term loan with `order_type: current`.
- **Fixed loan**: 7-day or 30-day term. Requires `fixed_type` (`7d`/`30d` lowercase) and `fixed_rate` (hourly rate from fix_rate tool, passed as-is — never describe as annual or daily). Missing fixed fields yield INVALID_PARAM_VALUE.
- **LTV thresholds**: Retrieved via `cex_mcl_get_multi_collateral_ltv` — includes init_ltv, alert_ltv, and liquidate_ltv.

### Presentation — order list / order detail (Case 6)

When displaying loan orders or order detail:

- **No time fields**: Omit every timestamp-style field from MCP responses (`borrow_time`, maturity, `operate_time`, `create_time`, `repay_time`, Unix timestamps, calendar dates). Do not compute relative timing (e.g. "expires in 3 days").
- **Allowed in reply**: `order_id`, `status`, borrow side (currency, principal/interest left), collateral side (currency, amount), current LTV if present, `fixed_type` as term label only.
- **If the user asks for dates/maturity**: Reply that timing is not shown here and suggest checking the Gate app or web for the full order schedule.

## Safety Rules

- **Writes** (`cex_mcl_create_multi_collateral`, `cex_mcl_repay_mcl`, `cex_mcl_operate_multi_collateral`): Always require explicit confirmation and an order draft before execution.
- **No investment advice**: Present LTV/rates; user decides.
- **Sensitive data**: Never expose API keys or raw internal errors.
- **Amounts**: Reject non-positive amounts; validate order_id for repay/collateral ops.
- **Order views**: Never surface time columns, dates, or timestamp fields in order list/detail answers to the user.

## Error Handling

| Condition | Response |
|-----------|----------|
| 401/403 | "Please configure your Gate CEX API Key in MCP with multi-collateral loan permission." |
| `cex_mcl_create_multi_collateral` fails | Check `order` JSON: borrow fields; for fixed include fixed_type `7d`/`30d` and fixed_rate from fix_rate tool. |
| Wrong fixed_type | Must be **`7d`** or **`30d`**, lowercase. |
| Fix rate empty (fixed) | "Fixed rate temporarily unavailable; try later or use current loan." |
| Repay / operate fails | Check order_id, currency, amount in JSON payloads. |
| Order not found | "Order not found." / "No loan orders." |

## Prompt Examples & Scenarios

See `references/scenarios.md` for prompt examples and expected behaviors (create current/fixed, repay, add collateral, redeem collateral).
