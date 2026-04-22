# Fixed Earn (Fixed-term) — `gate-cli` Tools Reference

`gate-cli` tools only. No REST paths or methods; use this document for skill behavior and tool arguments.

**Scope**: Simple Earn **fixed-term** (Fixed Earn). For flexible (Uni), see `references/earn-uni-mcp-tools.md`.

---

## 1. `gate-cli cex earn fixed products`

**Auth**: No

List all fixed-term products (paginated). Use only products with **status=2 (subscribing)** and **show_status=2 (visible)** when showing subscribable products.

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| page | number | Yes | Page number |
| limit | number | Yes | Page size, default 10 if omitted |
| asset | string | No | Currency filter, e.g. USDT |
| type | number | No | 1=normal, 2=vip |
| status | number | No | Pass **2** for subscribable list |
| show_status | string | No | Pass **2** for visible list |

### Response (key fields)

`data.list`: array of products (id, name, asset, lock_up_period, min_lend_amount, user_max_lend_amount, total_lend_amount, year_rate, type, status, pre_redeem, reinvest, redeem_account, fixed_earn_bonus_info, etc.). `data.count` / `data.total`: total count.

### Output table (product list)

When displaying, use title **"Fixed Earn products"** and columns:

| Currency | pid | Term (days) | Product type | Current base APY | Minimum subscription | Subscription limit | Remaining available amount | Early redemption supported | Auto-compounding supported | Maturity rollover supported |
|----------|-----|-------------|--------------|------------------|----------------------|--------------------|----------------------------|----------------------------|----------------------------|-----------------------------|

- **Product type**: type 1 Normal, 2 VIP.
- **Early redemption / auto-compounding / maturity rollover**: from pre_redeem, reinvest, redeem_account (1 Yes, 0 No). If asset-scoped response omits some fields, fill from full product list for same asset.

---

## 2. `gate-cli cex earn fixed products-asset`

**Auth**: No

List fixed-term products for one currency.

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| asset | string | Yes | Currency, e.g. USDT, BTC |
| type | string | No | "" or "1" normal, "2" vip, "0" all |

### Response (key fields)

`data.list`: products for that asset, ordered by lock_up_period ascending. If asset-scoped response omits min_lend_amount, user_max_lend_amount, user_max_lend_volume, or redeem_account, fetch full product list (same asset, status=2, show_status=2) and fill from matching row.

---

## 3. `gate-cli cex earn fixed create`

**Auth**: Yes

Create fixed-term subscribe (lend). Use only products with **status=2 (subscribing)** from the product list; product_id and year_rate must come from a status=2 product.

### Arguments (body)

| Name | Type | Required | Description |
|------|------|----------|-------------|
| product_id | integer | Yes | Product id from list (status=2) |
| amount | string | Yes | Subscribe amount |
| year_rate | string | Yes | Product year rate (from product) |
| reinvest_status | integer | No | Reinvest option |
| redeem_account_type | integer | No | Redeem account type |
| financial_rate_id | integer | No | Coupon id; 0 if none |
| sub_business | integer | No | Sub-business id |

### Response

Empty `{}` on success.

---

## 4. `gate-cli cex earn fixed lends`

**Auth**: Yes

List user fixed-term orders (current or history) or single order detail.

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| order_type | string | Yes | 1=current orders, 2=history orders |
| page | number | Yes | Page number |
| limit | number | Yes | Page size, default 10 |
| product_id | number | No | Filter by product |
| order_id | number | No | Filter by order (single-order detail) |
| asset | string | No | Filter by currency |
| sub_business | number | No | Sub business type |
| business_filter | string | No | JSON array, e.g. [{"business":1,"sub_business":0}] |

### Response (key fields)

`data.list`: lend orders (order_id may be int64; use int64 in parsers). `data.total`: count.

### Output table (positions)

Use columns:

| order_id | Underlying currency | Holding term (days) | Product type | Current base APY | Estimated maturity yield | Subscription time (UTC+0) | Maturity time (UTC+0) | Remaining days | Early redemption supported | Auto-compounding supported | Maturity rollover supported |
|----------|---------------------|---------------------|--------------|------------------|--------------------------|---------------------------|------------------------|---------------|----------------------------|----------------------------|-----------------------------|

- **Product type**: product_type 1 Normal, 2 VIP.
- **Remaining days**: max(0, ceil((redeem_at - now) / 86400)); show 0 or "Expired" when expired.
- **Early / auto-compounding / rollover**: from product_info.pre_redeem, reinvest, redeem_account (1 Yes, 0 No).

Single-order detail: same table, one row.

---

## 5. `gate-cli cex earn fixed pre-redeem`

**Auth**: Yes

Early redeem (or at maturity) a fixed-term order.

### Arguments (body)

| Name | Type | Required | Description |
|------|------|----------|-------------|
| order_id | string | Yes | Order id to redeem, e.g. "5862478785" |

### Response

Empty `{}` on success.

---

## 6. `gate-cli cex earn fixed history`

**Auth**: Yes

Fixed Earn transaction history (subscribe, redeem, interest, extra bonus).

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| type | string | Yes | "1" subscribe, "2" redeem, "3" interest, "4" extra bonus |
| page | string | Yes | Page number |
| limit | string | Yes | Page size, default 10 |
| product_id | integer | No | Filter by product |
| order_id | string | No | Filter by order |
| asset | string | No | Filter by currency |
| start_at | integer | No | Start timestamp (seconds) |
| end_at | integer | No | End timestamp (seconds) |
| sub_business | integer | No | Sub-business |
| business_filter | string | No | "1" normal, "2" vip |

### Response (key fields)

`data.list`: records with order_id, asset, amount, type, lock_up_period, create_time, etc. `data.total`: count.

### Output table (history)

| order_id | Operation time | Operation type | Underlying currency | Amount | Term (days) |
|----------|----------------|----------------|---------------------|--------|-------------|

- **Operation type**: type 1 subscribe, 2 redeem, 3 interest, 4 extra bonus.
- **Amount**: principal for subscribe/redeem, interest amount for interest.
- **Operation time**: create_time as YYYY-MM-DD HH:MM.

---

## Tool summary (fixed-term)

| `gate-cli` tool | Auth | Use in skill |
|----------|------|--------------|
| `gate-cli cex earn fixed products` | No | Browse all products, filters |
| `gate-cli cex earn fixed products-asset` | No | Products for one currency |
| `gate-cli cex earn fixed create` | Yes | Subscribe to fixed product |
| `gate-cli cex earn fixed lends` | Yes | Current/history orders, single order detail |
| `gate-cli cex earn fixed pre-redeem` | Yes | Early redeem order |
| `gate-cli cex earn fixed history` | Yes | Subscribe/redeem/interest/bonus history |

**Note**: Response parsing must use **int64** for order_id to avoid unmarshal errors for large IDs.

Scenarios and prompt examples: `references/scenarios.md`.
