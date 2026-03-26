# Multi-Collateral Loan — Scenarios & Prompt Examples

Skill maps write/read flows to **MCP tools** only. Arguments and JSON shapes: **`mcl-mcp-tools.md`**.

| Purpose | MCP tool | Auth |
|---------|----------|------|
| Create current/fixed loan | **cex_mcl_create_multi_collateral** (`order` JSON) | Yes |
| Repay | **cex_mcl_repay_multi_collateral_loan** (`repay_loan` JSON) | Yes |
| Add / redeem collateral | **cex_mcl_operate_multi_collateral** (`collateral_adjust` JSON) | Yes |
| List orders | **cex_mcl_list_multi_collateral_orders** | Yes |
| Order detail | **cex_mcl_get_multi_collateral_order_detail** | Yes |
| Quota / LTV / fix rate / current rate | **cex_mcl_list_user_currency_quota**, **cex_mcl_get_multi_collateral_ltv**, **cex_mcl_get_multi_collateral_fix_rate**, **cex_mcl_get_multi_collateral_current_rate** | Mixed |

---

## Scenario 1: Create current loan order

**Context**: User creates a **current** (flexible) multi-collateral loan: pledge collateral, borrow at variable rate.

**Prompt Examples**:
- "Pledge 100 USDT, borrow 7000 DOGE (current loan)"
- "Collateral 50 USDT, current borrow DOGE"

**Expected Behavior**:
1. Optionally call `cex_mcl_list_user_currency_quota` or `cex_mcl_get_multi_collateral_current_rate` to validate. Parse collateral and borrow (amount + currency).
2. Show draft. After user confirms, call `cex_mcl_create_multi_collateral` with **`order`** JSON: borrow_currency, borrow_amount, collateral_currencies (if any), order_type: current.
3. On success: loan created message with order_id. On failure: show error guidance.

**Tester**: User Prompt: `Pledge 100 USDT, borrow 7000 DOGE (current loan)` | Tools: optional quota → **cex_mcl_create_multi_collateral**

**MCP steps**

| Step | MCP tool |
|------|----------|
| 1 (optional) | **cex_mcl_list_user_currency_quota** |
| 2 | **cex_mcl_create_multi_collateral** |

---

## Scenario 2: Create fixed loan order

**Context**: User creates a **fixed**-term loan (7 or 30 days).

**Prompt Examples**:
- "Pledge 0.01 BTC, borrow 100 USDT for 7 days"
- "Collateral ETH, borrow USDT 30 days"

**Expected Behavior**:
1. Parse term: **7 days → fixed_type `7d`**, **30 days → `30d`** (lowercase).
2. Call `cex_mcl_get_multi_collateral_fix_rate`. Response is a **list**. **Filter** by borrow_currency. If empty or no row: stop; user message (no submit).
3. Set **fixed_rate** from `rate_7d` or `rate_30d` (**hourly interest rate**; pass as-is; do not convert or describe as annual/daily). Show draft; on confirm call `cex_mcl_create_multi_collateral` with **`order`** JSON: order_type fixed, fixed_type, fixed_rate, borrow_currency, borrow_amount, collateral_currencies.
4. On success/failure: same pattern as Scenario 1.

**Tester**: User Prompt: `Pledge 0.01 BTC, borrow 100 USDT for 7 days` | Tools: **cex_mcl_get_multi_collateral_fix_rate** → **cex_mcl_create_multi_collateral**

**MCP steps**

| Step | MCP tool |
|------|----------|
| 1 (optional) | **cex_mcl_list_user_currency_quota** |
| 2 | **cex_mcl_get_multi_collateral_fix_rate** |
| 3 | **cex_mcl_create_multi_collateral** |

---

## Scenario 3: Repay

**Context**: User repays part or all of a loan order.

**Prompt Examples**:
- "Repay order 123456 in full"
- "Order 123456 repay 1000 USDT"

**Expected Behavior**:
1. Parse order_id and amount (or full). Show draft; on confirm call `cex_mcl_repay_multi_collateral_loan` with **`repay_loan`** JSON (order_id, repay_items).
2. Success/failure user messages.

**Tester**: User Prompt: `Order 123456 repay 1000 USDT` | **cex_mcl_repay_multi_collateral_loan**

**MCP**: **cex_mcl_repay_multi_collateral_loan**

---

## Scenario 4: Add collateral

**Context**: User **adds** collateral to an order.

**Prompt Examples**:
- "Order 123456 add margin 100 USDT"
- "Order 123456 add collateral 0.01 ETH"

**Expected Behavior**:
1. Parse order_id, amount, currency. Show draft; on confirm call `cex_mcl_operate_multi_collateral` with **`collateral_adjust`** JSON: type append, collaterals array.
2. Success/failure messages.

**Tester**: User Prompt: `Order 123456 add margin 100 USDT` | **cex_mcl_operate_multi_collateral**

**MCP**: **cex_mcl_operate_multi_collateral**

---

## Scenario 5: Redeem collateral

**Context**: User **redeems** (reduces) collateral.

**Prompt Examples**:
- "Order 123456 redeem margin 100 USDT"
- "Order 123456 reduce collateral 0.01 ETH"

**Expected Behavior**:
1. Parse order_id, amount, currency. Show draft; on confirm call `cex_mcl_operate_multi_collateral` with **`collateral_adjust`** JSON: type redeem.
2. Success/failure messages.

**Tester**: User Prompt: `Order 123456 redeem margin 100 USDT` | **cex_mcl_operate_multi_collateral**

**MCP**: **cex_mcl_operate_multi_collateral**

---

## Scenario 6: List or view my orders (no time fields)

**Context**: User views collateral loan orders or one order detail (e.g. "我的订单", "loan orders").

**Prompt Examples**:
- "Show my multi-collateral loan orders"
- "Order detail for 123456"

**Expected Behavior**:
1. Call `cex_mcl_list_multi_collateral_orders` and/or `cex_mcl_get_multi_collateral_order_detail`.
2. Summarize **order_id, status, borrow amounts/currencies, collateral amounts/currencies, LTV** (and fixed term as **7d/30d label only** if fixed—no calendar dates).
3. **Strip all time-related fields** from the user-facing answer: no borrow_time, maturity, due date, operate_time, create_time, repay_time, Unix timestamps, or natural-language dates derived from those fields. If the user asks for timing, direct them to Gate app/web; do not echo API timestamps.

**MCP**: **cex_mcl_list_multi_collateral_orders**, **cex_mcl_get_multi_collateral_order_detail**

---

## Auth failure

On 401/403: do not expose credentials. Output: **"Unable to perform collateral loan operations. Please configure your Gate API Key (multi-collateral loan permission) in MCP settings and try again."**
