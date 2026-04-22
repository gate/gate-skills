# Multi-Collateral Loan — `gate-cli` Tools Reference

`gate-cli` tools only. No REST paths or HTTP methods; use this document for arguments and behavior. Scenarios: **`scenarios.md`**.

---

## 1. `gate-cli cex mcl fix-rate`

**Auth**: No

Returns a **list** of `{ currency, rate_7d, rate_30d }` per borrow currency. **`rate_7d` and `rate_30d` are hourly interest rates.** For fixed-term orders, **filter by `borrow_currency`**, then use `rate_7d` (term `7d`) or `rate_30d` (term `30d`) as **`fixed_rate`** (hourly rate) inside **`gate-cli cex mcl create`** `order` JSON.

### Arguments

None.

### AI usage

- **fixed_rate is an hourly interest rate.** Use `rate_7d` or `rate_30d` from the response as the `fixed_rate` value in the create-order `order` JSON; do not convert to annual or daily, and do not describe it to the user as anything other than hourly rate when displaying.
- Empty or missing row for a currency means fixed-term borrow is not supported for that currency.

---

## 2. `gate-cli cex mcl create`

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

## 3. `gate-cli cex mcl orders`

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

## 4. `gate-cli cex mcl order`

**Auth**: Yes

### Arguments

| Name | Type | Required |
|------|------|----------|
| order_id | string | Yes |

Response shape aligns with a single order from the list API (borrow/collateral breakdown, LTV, status, and may include timestamp fields).

**User-facing display (skill rule)**: When summarizing detail for the user, **omit every time/timestamp/maturity field**; same allowed fields as list (§3). Do not output dates even if the user asks—point to Gate app/web for schedule.

---

## 5. `gate-cli cex mcl repay`

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

## 6. `gate-cli cex mcl collateral`

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

## 7. `gate-cli cex mcl repay-records`

**Auth**: Yes

### Arguments

| Name | Required | Description |
|------|----------|-------------|
| type | Yes | `repay` or `liquidate` |
| borrow_currency | No | Filter |
| page, limit | No | Pagination |
| from, to | No | Unix seconds |

---

## 8. `gate-cli cex mcl records`

**Auth**: Yes

Collateral append/redeem history.

### Arguments

| Name | Required | Description |
|------|----------|-------------|
| page, limit | No | Pagination |
| from, to | No | Unix seconds |
| collateral_currency | No | Filter |

---

## 9. `gate-cli cex mcl ltv`

**Auth**: No

Global LTV thresholds: `init_ltv`, `alert_ltv`, `liquidate_ltv`.

### Arguments

None.

---

## 10. `gate-cli cex mcl quota`

**Auth**: Yes

Per-currency borrow or collateral quota.

### Arguments

| Name | Required | Description |
|------|----------|-------------|
| type | Yes | `collateral` or `borrow` |
| currency | Yes | Comma-separated; borrow allows one currency |

---

## 11. `gate-cli cex mcl current-rate`

**Auth**: No

Current (flexible) borrow rates for listed currencies.

### Arguments

| Name | Required | Description |
|------|----------|-------------|
| currencies | Yes | Comma-separated, max 100 |
| vip_level | No | Defaults if omitted |

---

## Tool summary

| `gate-cli` tool | Auth | Use |
|----------|------|-----|
| `gate-cli cex mcl fix-rate` | No | Fixed rates list; filter by borrow currency |
| `gate-cli cex mcl create` | Yes | New current/fixed loan (`order` JSON) |
| `gate-cli cex mcl orders` | Yes | List orders |
| `gate-cli cex mcl order` | Yes | One order |
| `gate-cli cex mcl repay` | Yes | Repay (`repay_loan` JSON) |
| `gate-cli cex mcl collateral` | Yes | Add/redeem collateral (`collateral_adjust` JSON) |
| `gate-cli cex mcl repay-records` | Yes | Repay history |
| `gate-cli cex mcl records` | Yes | Collateral history |
| `gate-cli cex mcl ltv` | No | LTV thresholds |
| `gate-cli cex mcl quota` | Yes | Quota |
| `gate-cli cex mcl current-rate` | No | Flexible rates |
