# Multi-Collateral Loan — MCP Tools Reference

MCP tools only. No REST paths or HTTP methods; use this document for arguments and behavior. Scenarios: **`scenarios.md`**.

---

## 1. cex_mcl_get_multi_collateral_fix_rate

**Auth**: No

Returns a **list** of `{ currency, rate_7d, rate_30d }` per borrow currency. **`rate_7d` and `rate_30d` are hourly interest rates.** For fixed-term orders, **filter by `borrow_currency`**, then use `rate_7d` (term `7d`) or `rate_30d` (term `30d`) as **`fixed_rate`** (hourly rate) inside **`cex_mcl_create_multi_collateral`** `order` JSON.

### Arguments

None.

### AI usage

- **fixed_rate is an hourly interest rate.** Use `rate_7d` or `rate_30d` from the response as the `fixed_rate` value in the create-order `order` JSON; do not convert to annual or daily, and do not describe it to the user as anything other than hourly rate when displaying.
- Empty or missing row for a currency means fixed-term borrow is not supported for that currency.

---

## 2. cex_mcl_create_multi_collateral

**Auth**: Yes

Create a **current** or **fixed** multi-collateral loan. **User confirmation required** before call.

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| order | string | Yes | JSON string: CreateMultiCollateralOrder |

### order JSON (typical fields)

| Field | Required | Description |
|-------|----------|-------------|
| borrow_currency | Yes | Borrow currency (e.g. USDT) |
| borrow_amount | Yes | Amount (decimal string) |
| collateral_currencies | No | Array of `{ currency, amount }` |
| order_type | No | `current` or `fixed`; default current |
| fixed_type | If fixed | `7d` or `30d` (lowercase) |
| fixed_rate | If fixed | **Hourly interest rate** from §1 (rate_7d or rate_30d for that currency); do not convert or describe as annual/daily |
| auto_renew, auto_repay | No | Booleans for fixed |

---

## 3. cex_mcl_list_multi_collateral_orders

**Auth**: Yes

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| page | number | No | Page number |
| limit | number | No | Page size |
| sort | string | No | `time_desc`, `ltv_asc`, `ltv_desc` |
| order_type | string | No | `current` or `fixed`; defaults to current if omitted |

**User-facing display**: List responses may include time fields in JSON—**never** include any time/date/timestamp/maturity in the reply to the user; only order_id, status, amounts, collateral, LTV, term label (7d/30d) without calendar dates.

---

## 4. cex_mcl_get_multi_collateral_order_detail

**Auth**: Yes

### Arguments

| Name | Type | Required |
|------|------|----------|
| order_id | string | Yes |

Response shape aligns with a single order from the list API (borrow/collateral breakdown, LTV, status, and may include timestamp fields).

**User-facing display (skill rule)**: When summarizing detail for the user, **omit every time/timestamp/maturity field**; same allowed fields as list (§3). Do not output dates even if the user asks—point to Gate app/web for schedule.

---

## 5. cex_mcl_repay_multi_collateral_loan

**Auth**: Yes

Partial or full repay. **User confirmation required**.

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| repay_loan | string | Yes | JSON string: RepayMultiLoan |

### repay_loan JSON (typical)

| Field | Description |
|-------|-------------|
| order_id | Loan order id |
| repay_items | Array of `{ currency, amount, repaid_all }` |

---

## 6. cex_mcl_operate_multi_collateral

**Auth**: Yes

Add or withdraw collateral. **User confirmation required**.

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| collateral_adjust | string | Yes | JSON string: CollateralAdjust |

### collateral_adjust JSON (typical)

| Field | Description |
|-------|-------------|
| order_id | Loan order id |
| type | `append` (add) or `redeem` (reduce) |
| collaterals | Array of `{ currency, amount }` |

---

## 7. cex_mcl_list_multi_repay_records

**Auth**: Yes

### Arguments

| Name | Required | Description |
|------|----------|-------------|
| type | Yes | `repay` or `liquidate` |
| borrow_currency | No | Filter |
| page, limit | No | Pagination |
| from, to | No | Unix seconds |

---

## 8. cex_mcl_list_multi_collateral_records

**Auth**: Yes

Collateral append/redeem history.

### Arguments

| Name | Required | Description |
|------|----------|-------------|
| page, limit | No | Pagination |
| from, to | No | Unix seconds |
| collateral_currency | No | Filter |

---

## 9. cex_mcl_get_multi_collateral_ltv

**Auth**: No

Global LTV thresholds: `init_ltv`, `alert_ltv`, `liquidate_ltv`.

### Arguments

None.

---

## 10. cex_mcl_list_user_currency_quota

**Auth**: Yes

Per-currency borrow or collateral quota.

### Arguments

| Name | Required | Description |
|------|----------|-------------|
| type | Yes | `collateral` or `borrow` |
| currency | Yes | Comma-separated; borrow allows one currency |

---

## 11. cex_mcl_get_multi_collateral_current_rate

**Auth**: No

Current (flexible) borrow rates for listed currencies.

### Arguments

| Name | Required | Description |
|------|----------|-------------|
| currencies | Yes | Comma-separated, max 100 |
| vip_level | No | Defaults if omitted |

---

## Tool summary

| MCP tool | Auth | Use |
|----------|------|-----|
| cex_mcl_get_multi_collateral_fix_rate | No | Fixed rates list; filter by borrow currency |
| cex_mcl_create_multi_collateral | Yes | New current/fixed loan (`order` JSON) |
| cex_mcl_list_multi_collateral_orders | Yes | List orders |
| cex_mcl_get_multi_collateral_order_detail | Yes | One order |
| cex_mcl_repay_multi_collateral_loan | Yes | Repay (`repay_loan` JSON) |
| cex_mcl_operate_multi_collateral | Yes | Add/redeem collateral (`collateral_adjust` JSON) |
| cex_mcl_list_multi_repay_records | Yes | Repay history |
| cex_mcl_list_multi_collateral_records | Yes | Collateral history |
| cex_mcl_get_multi_collateral_ltv | No | LTV thresholds |
| cex_mcl_list_user_currency_quota | Yes | Quota |
| cex_mcl_get_multi_collateral_current_rate | No | Flexible rates |
