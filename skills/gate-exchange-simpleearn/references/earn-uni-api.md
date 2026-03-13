# Simple Earn (EarnUni) REST API and MCP Mapping

This document aligns Gate APIv4 EarnUni REST endpoints with MCP tools `cex_earn_*` for skill scenarios and MCP calls.

**Base**: APIv4, default rate limit 200r/10s. Authenticated endpoints require Gate signature (key/timestamp/sign, etc.).

---

## 1. List Simple Earn currencies

| Item | Value |
|------|-------|
| **Method** | GET |
| **Path** | `/earn/uni/currencies` |
| **MCP tool** | **cex_earn_list_uni_currencies** |
| **Auth** | No |

### Request parameters

No required path/query parameters; optional headers for auth.

### Response example (200)

```json
[
  {
    "currency": "AE",
    "min_lend_amount": "100",
    "max_lend_amount": "200000000",
    "max_rate": "0.00057",
    "min_rate": "0.000001"
  }
]
```

### Response fields

| Field | Type | Description |
|-------|------|-------------|
| currency | string | Currency name |
| min_lend_amount | string | Min lend amount (in that currency) |
| max_lend_amount | string | Max cumulative lend amount |
| max_rate | string | Max rate (hourly) |
| min_rate | string | Min rate (hourly) |

---

## 2. Get single currency details

| Item | Value |
|------|-------|
| **Method** | GET |
| **Path** | `/earn/uni/currencies/{currency}` |
| **MCP tool** | **cex_earn_get_uni_currency** |
| **Auth** | No |

### Request parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| currency | path | string | Yes | Currency |

### Response example (200)

Same structure as a single list item: `currency`, `min_lend_amount`, `max_lend_amount`, `max_rate`, `min_rate`.

---

## 3. Create lend or redeem (subscribe/redeem)

**This skill must not call this endpoint for subscribe or redeem.** The following is API reference only; do not call `cex_earn_create_uni_lend` (type: lend or redeem) at runtime.

| Item | Value |
|------|-------|
| **Method** | POST |
| **Path** | `/earn/uni/lends` |
| **MCP tool** | **cex_earn_create_uni_lend** (disabled for this skill) |
| **Auth** | Yes |

Lend: set minimum lend rate; at each whole hour the lend is confirmed and interest is applied; two minutes before/after each whole hour is settlement window—lend and redeem are not allowed. Redeem: failed lend funds return immediately; lent funds earn current hour interest; redeemed funds arrive at the next whole hour.

### Pre-call (when subscribing)

When calling **cex_earn_create_uni_lend** for subscribe (`type: lend`), first call **cex_earn_list_uni_currencies** or **cex_earn_get_uni_currency** to get **min_rate** for that currency and pass it into **cex_earn_create_uni_lend**; otherwise the lend may fail due to rate requirements.

### Request body

| Name | Type | Required | Description |
|------|------|----------|-------------|
| currency | string | Yes | Currency name |
| amount | string | Yes | Amount to lend to the pool |
| type | string | Yes | `lend` (subscribe) / `redeem` |
| min_rate | string | No | Min rate (hourly); **recommended for lend**, from list_uni_currencies / get_uni_currency; too high may cause lend failure |

### Response

204 No Content.

---

## 4. List user lend positions (flexible positions)

| Item | Value |
|------|-------|
| **Method** | GET |
| **Path** | `/earn/uni/lends` |
| **MCP tool** | **cex_earn_list_user_uni_lends** |
| **Auth** | Yes |

### Request parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| currency | query | string | No | Filter by currency |
| page | query | integer | No | Page number |
| limit | query | integer | No | Page size, default 100, max 100 |

### Response example (200)

```json
[
  {
    "currency": "BTC",
    "current_amount": "20.999992",
    "amount": "20.999992",
    "lent_amount": "0",
    "frozen_amount": "0",
    "min_rate": "0.1",
    "create_time": 1673247054000,
    "update_time": 1673247054000
  }
]
```

### Response fields

| Field | Description |
|-------|-------------|
| currency | Currency |
| amount | Total position (lend balance) |
| lent_amount | Lent amount |
| frozen_amount | Redeem requested, not yet settled |
| min_rate | Min rate |
| interest_status | interest_dividend = payout; interest_reinvest = reinvest |

---

## 5. Update user lend info (min rate)

**This skill must not call this endpoint in any form.** The following is API reference only; do not call `cex_earn_change_uni_lend` at runtime.

| Item | Value |
|------|-------|
| **Method** | PATCH |
| **Path** | `/earn/uni/lends` |
| **MCP tool** | **cex_earn_change_uni_lend** (disabled for this skill) |
| **Auth** | Yes |

Currently only supports updating min rate (hourly).

### Request body

| Name | Type | Required | Description |
|------|------|----------|-------------|
| currency | string | Yes | Currency name |
| min_rate | string | Yes | Min rate |

### Response

204 No Content.

---

## 6. List lend records (subscribe/redeem history)

| Item | Value |
|------|-------|
| **Method** | GET |
| **Path** | `/earn/uni/lend_records` |
| **MCP tool** | **cex_earn_list_uni_lend_records** |
| **Auth** | Yes |

### Request parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| currency | query | string | No | Filter by currency |
| page | query | integer | No | Page number |
| limit | query | integer | No | Page size, default 100, max 100 |
| type | query | string | No | `lend` / `redeem` |

### Response example (200)

```json
[
  {
    "type": "lend",
    "currency": "BTC",
    "amount": "1",
    "last_wallet_amount": "0.2",
    "last_lent_amount": "0",
    "last_frozen_amount": "0",
    "create_time": 1673247054000
  }
]
```

---

## 7. Get user single-currency total interest (distributed)

| Item | Value |
|------|-------|
| **Method** | GET |
| **Path** | `/earn/uni/interests/{currency}` |
| **MCP tool** | **cex_earn_get_uni_interest** |
| **Auth** | Yes |

### Request parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| currency | path | string | Yes | Currency |

### Response example (200)

```json
{
  "currency": "AE",
  "interest": "123.345"
}
```

---

## 8. List user interest records

| Item | Value |
|------|-------|
| **Method** | GET |
| **Path** | `/earn/uni/interest_records` |
| **MCP tool** | **cex_earn_list_uni_interest_records** |
| **Auth** | Yes |

### Request parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| currency | query | string | No | Filter by currency |
| page | query | integer | No | Page number |
| limit | query | integer | No | Page size |

### Response example (200)

```json
[
  {
    "status": 1,
    "currency": "AE",
    "actual_rate": "0.0005",
    "interest": "0.05",
    "create_time": 1673247054000
  }
]
```

status: 0 = failed, 1 = success.

---

## 9. Get currency interest reinvest status

| Item | Value |
|------|-------|
| **Method** | GET |
| **Path** | `/earn/uni/interest_status/{currency}` |
| **MCP tool** | **cex_earn_get_uni_interest_status** |
| **Auth** | Yes |

### Request parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| currency | path | string | Yes | Currency |

### Response example (200)

```json
{
  "currency": "USDT",
  "interest_status": "interest_dividend"
}
```

interest_status: `interest_dividend` = payout, `interest_reinvest` = reinvest.

---

## 10. Simple Earn currency APY chart

| Item | Value |
|------|-------|
| **Method** | GET |
| **Path** | `/earn/uni/chart` |
| **MCP tool** | **cex_earn_list_uni_chart** |
| **Auth** | No |

### Request parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| from | query | integer(int64) | Yes | Start time (seconds), max range 30 days |
| to | query | integer(int64) | Yes | End time (seconds) |
| asset | query | string | Yes | Currency name |

### Response example (200)

```json
[
  { "time": 1719705600, "value": "0.01" }
]
```

value is percentage APY.

---

## 11. Currency estimated APY rate

| Item | Value |
|------|-------|
| **Method** | GET |
| **Path** | `/earn/uni/rate` |
| **MCP tool** | **cex_earn_list_uni_rate** |
| **Auth** | No |

### Request parameters

No required parameters.

### Response example (200)

```json
[
  { "currency": "USDT", "est_rate": "0.0226" }
]
```

est_rate: estimated APY (not percentage). Case 6 "subscribe to top APY currency" can use the currency with highest est_rate; this skill does not call create_uni_lend for subscribe.

---

## 12. Set interest reinvest switch (REST only, no MCP)

| Item | Value |
|------|-------|
| **Method** | PUT |
| **Path** | `/earn/uni/interest_reinvest` |
| **MCP tool** | None (REST only) |
| **Auth** | Yes |

### Request body

| Name | Type | Required | Description |
|------|------|----------|-------------|
| currency | string | Yes | Currency |
| status | boolean | Yes | true = reinvest, false = payout |

### Response

204 No Content.

---

## MCP and REST mapping

| MCP tool | Method | Path |
|----------|--------|------|
| cex_earn_list_uni_currencies | GET | /earn/uni/currencies |
| cex_earn_get_uni_currency | GET | /earn/uni/currencies/{currency} |
| cex_earn_create_uni_lend | POST | /earn/uni/lends |
| cex_earn_list_user_uni_lends | GET | /earn/uni/lends |
| cex_earn_change_uni_lend | PATCH | /earn/uni/lends (disabled for this skill) |
| cex_earn_list_uni_lend_records | GET | /earn/uni/lend_records |
| cex_earn_get_uni_interest | GET | /earn/uni/interests/{currency} |
| cex_earn_list_uni_interest_records | GET | /earn/uni/interest_records |
| cex_earn_get_uni_interest_status | GET | /earn/uni/interest_status/{currency} |
| cex_earn_list_uni_chart | GET | /earn/uni/chart |
| cex_earn_list_uni_rate | GET | /earn/uni/rate |

Scenarios and trigger phrases: **scenarios.md**. At runtime the skill uses MCP tools; this table aligns with Gate APIv4 Simple Earn (EarnUni) endpoints.
