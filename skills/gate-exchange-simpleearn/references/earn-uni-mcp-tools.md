# Simple Earn Flexible (Uni) — MCP Tools Reference

MCP tools only. No REST paths or methods; use this document for skill behavior and tool arguments.

**Scope**: Simple Earn **flexible** (Uni) only. For fixed-term, see `references/fixed-earn-mcp-tools.md`.

### User-facing output (flexible Uni)

When presenting flexible Uni results to the user, **strip or omit every time-display field** from MCP responses (e.g. `time`, `create_time`, `update_time`, `timestamp`, settlement instants, history row times). Tables and prose must not include date/time columns or “at HH:MM” style facts unless the user explicitly asks for timing. Chart tools: do not print time-indexed series; at most state the latest estimated APY (or decline to show a timeline).

---

## 1. cex_earn_list_uni_rate

**Auth**: No

Estimated annualized rate per flexible currency. Use this to enumerate currencies with APY and to pick the highest-APY currency. For **min_lend_amount**, **min_rate**, and lend limits, call **`cex_earn_get_uni_currency`** for each currency you care about (this tool does not return full lend constraints).

### Arguments

None required.

### Response (key fields)

Array of objects (typical): `currency`, estimated rate / APY fields as returned by MCP. Sort by rate to implement "subscribe to highest APY", then call **`cex_earn_get_uni_currency`** on the chosen currency before subscribe.

---

## 2. cex_earn_get_uni_currency

**Auth**: No

Single-currency flexible details (for subscribe min_rate).

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| currency | string | Yes | Currency, e.g. USDT, ETH |

### Response (key fields)

Same as one list item: `currency`, `min_lend_amount`, `max_lend_amount`, `max_rate`, `min_rate`.

**Pre-call**: When subscribing, call this (or list) to get `min_rate` and pass it into `cex_earn_create_uni_lend`; otherwise the lend may fail.

---

## 3. cex_earn_create_uni_lend

**Auth**: Yes

Create lend (subscribe) or redeem.

### Arguments (body)

| Name | Type | Required | Description |
|------|------|----------|-------------|
| currency | string | Yes | Currency name |
| amount | string | Yes | Amount to lend or redeem |
| type | string | Yes | `lend` (subscribe) or `redeem` |
| min_rate | string | No | Min hourly rate; **recommended for lend** (from get_uni_currency). Too high may cause lend failure. |

### Behavior (agent use; do not echo clock/time detail to the user unless they ask)

- **lend**: Whole-hour confirmation/settlement; brief window around each hour when lend/redeem may be rejected—explain generically on failure (“temporarily unavailable, retry shortly”) without quoting times.
- **redeem**: Redeemed funds settle on the next cycle; failed lend funds return immediately.

---

## 4. cex_earn_list_user_uni_lends

**Auth**: Yes

User flexible positions (optional filter by currency).

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| currency | string | No | Filter by currency |
| page | integer | No | Page number |
| limit | integer | No | Page size, default 100, max 100 |

### Response (key fields per item)

| Field | Description |
|-------|-------------|
| currency | Currency |
| amount | Total position (lend balance) |
| lent_amount | Lent amount |
| frozen_amount | Redeem requested, not yet settled |
| min_rate | Min rate |
| interest_status | interest_dividend = payout; interest_reinvest = reinvest |

---

## 5. cex_earn_change_uni_lend

**Auth**: Yes

Update user lend min rate (hourly) for a currency.

### Arguments (body)

| Name | Type | Required | Description |
|------|------|----------|-------------|
| currency | string | Yes | Currency name |
| min_rate | string | Yes | New min rate |

---

## 6. cex_earn_list_uni_lend_records

**Auth**: Yes

Subscribe/redeem history.

**User-facing**: Show type, currency, amount only—**no** operation time or timestamp columns.

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| currency | string | No | Filter by currency |
| page | integer | No | Page number |
| limit | integer | No | Page size, default 100, max 100 |
| type | string | No | `lend` or `redeem` |

---

## 7. cex_earn_get_uni_interest

**Auth**: Yes

Single-currency cumulative interest (distributed).

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| currency | string | Yes | Currency |

### Response (key fields)

| Field | Type | Description |
|-------|------|-------------|
| currency | string | Currency |
| interest | string | Cumulative interest |

---

## 8. cex_earn_list_uni_interest_records

**Auth**: Yes

User interest records.

**User-facing**: Show currency and amount (and type if applicable)—**no** credited-at / period time fields.

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| currency | string | No | Filter by currency |
| page | integer | No | Page number |
| limit | integer | No | Page size |

---

## 9. cex_earn_get_uni_interest_status

**Auth**: Yes

Currency interest reinvest switch (payout vs reinvest).

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| currency | string | Yes | Currency |

### Response (key fields)

| Field | Description |
|-------|-------------|
| interest_status | interest_dividend = payout; interest_reinvest = reinvest |

---

## 10. cex_earn_list_uni_chart

**Auth**: No

Simple Earn currency APY chart (time series).

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| asset | string | Yes | Currency name |
| from | integer (int64) | Yes | Start time (seconds), max range 30 days |
| to | integer (int64) | Yes | End time (seconds) |

### Response

Array of `{ "time": number, "value": "string" }`; value is percentage APY. **Do not show `time` or a dated series to the user**; optionally report only the latest `value` as current estimated APY for that asset.

---

## 11. cex_earn_list_uni_rate

**Auth**: No

Estimated APY per currency (for “top APY” and display).

### Arguments

None required.

### Response (key fields)

Array of `{ "currency": string, "est_rate": string }`. `est_rate` is estimated APY (not percentage). Use the currency with highest `est_rate` for “subscribe to top APY”; confirm amount and call `cex_earn_create_uni_lend` after user confirmation.

---

## Tool summary (flexible)

| MCP tool | Auth | Use in skill |
|----------|------|--------------|
| cex_earn_list_uni_rate | No | APY per currency; top APY + currency list |
| cex_earn_get_uni_currency | No | Single-currency min_rate / limits for subscribe |
| cex_earn_create_uni_lend | Yes | Subscribe (lend) or redeem |
| cex_earn_list_user_uni_lends | Yes | Positions (single or all) |
| cex_earn_change_uni_lend | Yes | Change min rate |
| cex_earn_list_uni_lend_records | Yes | Lend/redeem history |
| cex_earn_get_uni_interest | Yes | Single-currency cumulative interest |
| cex_earn_list_uni_interest_records | Yes | Interest records |
| cex_earn_get_uni_interest_status | Yes | Reinvest status |
| cex_earn_list_uni_chart | No | APY chart |

Scenarios and prompt examples: `references/scenarios.md`.
