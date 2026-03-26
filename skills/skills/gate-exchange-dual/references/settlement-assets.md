# Settlement & Assets — Cases 11, 12

Settlement result query and dual asset briefing.

## Available Tools

| Tool | Auth | Description |
|------|------|-------------|
| `cex_earn_list_dual_orders` | Yes | List dual investment orders. `page` and `limit` are **required**: always pass `page=1, limit=100`, then loop. `from`/`to` optional (Unix timestamps). |
| `cex_earn_list_dual_balance` | Yes | Get dual investment balance & interest stats |

> **Pagination**: `page` and `limit` are **required** — always start with `page=1, limit=100`. Loop with incrementing `page` until returned rows < `limit`. Must fetch ALL pages before drawing any conclusion.

### Global Data Formatting Rules

| Field category | Rule |
|---------------|------|
| **Any APY/rate field** (`apy`, `apy_display`, `apy_settlement`, or any other rate field from any dual tool) | Raw value — **NOT a percentage**. Example: API returns `"2.7814"` which means **278.14%**. You **MUST multiply by 100** then append `%` (i.e. `2.7814 × 100 = 278.14%`). **NEVER** display the raw value directly as a percentage (e.g. `2.7814%` is WRONG). **Sanity check**: after ×100, typical ranges are 5%–2000%. If you see values like 0.1%–20%, you forgot to multiply. Applies to all dual tools. |
| All timestamps (`delivery_time`, `create_time`, `complete_time`) | Unix timestamps (seconds). Do NOT convert to dates or display to the user — the conversion is not accurate. Omit all timestamp fields from user-facing output. |
| `status` | `INIT`→Pending, `PROCESSING`→In Position, `SETTLEMENT_SUCCESS`→Settled, `SETTLEMENT_PROCESSING`→Settling, `CANCELED`→Canceled, `FAILED`→Failed, `REFUND_SUCCESS`→Early Redemption (Completed), `REFUND_PROCESSING`→Early Redemption (Processing), `REFUND_FAILED`→Early Redemption (Failed). `REFUND_*` = early redemption, never "refund". |

> **Critical**: Do NOT display timestamp fields to the user — the conversion is not accurate.
> There is NO `type` field in order response. Derive sell-high / buy-low from `invest_currency`: crypto → Sell High; stablecoin → Buy Low.
> There is NO `instrument_name`. Filter by coin using `invest_currency` or `exercise_currency`.

## Workflow: Case 11 — Settlement Result Query

### Step 1: Parse time range and fetch ALL settled orders

If the user mentions a time period (e.g. "last month", "last week"), calculate exact `from`/`to` Unix timestamps (seconds, UTC+0). Always pass correct timestamps — do NOT ignore the time range.

Call `cex_earn_list_dual_orders` with `from`, `to`, `page=1`, `limit=100`.

> **Critical**: Complete ALL pagination (loop until returned rows < limit) before drawing any conclusions. Do NOT answer based on partial data.

After all pages are collected, if user mentions a specific coin, filter the **complete** result set locally — check if `invest_currency` or `exercise_currency` matches the coin.

### Step 2: Transform APY, then interpret and present

**First**, transform every row: `apy_display × 100` → append `%`; `apy_settlement × 100` → append `%`. E.g. raw `2.7814` → display `278.14%`.

Derive type from `invest_currency`: crypto → Sell High (Call); stablecoin → Buy Low (Put).

Explain settlement outcome:

**Sell-High (Call)**:
- `settlement_price` ≥ `exercise_price` → "Successfully sold at target price, received USDT"
- `settlement_price` < `exercise_price` → "Target price not reached, got back crypto + interest"

**Buy-Low (Put)**:
- `settlement_price` ≤ `exercise_price` → "Successfully bought at target price, received crypto"
- `settlement_price` > `exercise_price` → "Target price not reached, got back USDT + interest"

Both scenarios include principal + interest. Display: `settlement_currency`, `settlement_amount`, `settlement_price`, Realized APY (`apy_settlement × 100`%).

> `apy_display`, `apy_settlement` are raw values (NOT percentages) — multiply by 100 before appending `%`. E.g. `2.7814` → `278.14%`.
> Do NOT display timestamp fields to the user — the conversion is not accurate.

## Workflow: Case 12 — Dual Asset Briefing

### Step 1: Fetch balance

Call `cex_earn_list_dual_balance` (no parameters needed).

### Step 2: Present summary

Display total dual investment locked amounts and accumulated interest in both USDT and BTC.

## Report Template

### Settlement Result (Case 11)

```
Your Settled Dual Orders

| # | Coin Pair | Type | Invested | Target Price | Settlement Price | Result | Received | Realized APY |
|---|-----------|------|----------|--------------|------------------|--------|----------|--------------|
| 1 | {invest_currency}/{exercise_currency} | {Sell-High/Buy-Low} | {invest_amount} {invest_currency} | {exercise_price} | {settlement_price} | {Hit/Miss} | {settlement_amount} {settlement_currency} | {apy_settlement × 100}% |

Note: apy_display / apy_settlement are raw values (NOT percentages) — multiply by 100 before appending %. E.g. `2.7814` → `278.14%`.
Settlement rule: Principal + interest are always received; settlement currency depends on whether the target price was reached.
```

### Asset Briefing (Case 12)

```
Your Dual Investment Summary

• Total Locked: {user_asset_usdt} USDT / {user_asset_btc} BTC
• Total Interest Earned: {user_total_interest_usdt} USDT / {user_total_interest_btc} BTC

Dual investment is interest-guaranteed but not principal-protected, and is subject to market risks.
```

### Next Actions

- To browse new plans: see `product-query.md`
