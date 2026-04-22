# Simple Earn (Uni) — Scenarios & Prompt Examples

Skill: Simple Earn (Uni) flexible. Scenarios map to **MCP tools**; for tool arguments and response see **`earn-uni-mcp-tools.md`**.

**Display rule (all Uni scenarios)**: User-facing answers must **not** include time-related fields from MCP (no dates, timestamps, or time columns). See `earn-uni-mcp-tools.md` § “User-facing output”.

| Purpose | MCP tool | Auth |
|---------|----------|------|
| Create lend or redeem | **`gate-cli cex earn uni lend`** | Yes |
| Change min rate | **`gate-cli cex earn uni change`** | Yes |
| User lend list (positions) | **`gate-cli cex earn uni lends`** | Yes |
| Single-currency total interest | **`gate-cli cex earn uni interest`** | Yes |
| Estimated APY per currency | **`gate-cli cex earn uni rate`** | No |

---

## Scenario 1: Subscribe (Lend)

**Context**: User subscribes a specified amount of a currency to Simple Earn flexible (Uni).

**Prompt Examples**:
- "Subscribe 100 USDT to Simple Earn" / "Buy 0.01 BTC into flexible earn"

**Expected Behavior**:
1. Ask for missing inputs: currency, amount.
2. If user provides `min_rate`, use it directly.
3. If user does not provide `min_rate`, call `gate-cli cex earn uni currency` to fetch the currency's flexible `min_rate` and use it as default.
4. Confirm details with the user (including the final `min_rate`).
5. Call `gate-cli cex earn uni lend` with `type: lend`.

**MCP**: `gate-cli cex earn uni lend` (see `earn-uni-mcp-tools.md` §3).

---

## Scenario 2: Redeem

**Context**: User redeems a specified amount of a currency from Simple Earn flexible.

**Prompt Examples**:
- "Redeem 100 USDT from Simple Earn" / "Redeem 0.01 BTC from flexible earn"

**Expected Behavior**:
1. Ask for missing inputs: currency, amount.
2. Confirm details with the user.
3. Call `gate-cli cex earn uni lend` with `type: redeem`.

**MCP**: `gate-cli cex earn uni lend` (see `earn-uni-mcp-tools.md` §3).

---

## Scenario 3: Single-currency position query

**Context**: Query the user's current Simple Earn flexible position for a given currency.

**Prompt Examples**:
- "My USDT Simple Earn position" / "How much BTC do I have in flexible earn?"

**Expected Behavior**:
1. Fetch data via `gate-cli cex earn uni lends`; from the returned list take **amount** (total position) for that currency.
2. No extra calculation; use the API-returned amount directly.
3. Output success: Query submitted! Your current {currency} Simple Earn position is {amount}. Failure: Query submitted! {error toast}.

**MCP** (see `earn-uni-mcp-tools.md` §4): **`gate-cli cex earn uni lends`**

---

## Scenario 4: All positions query

**Context**: Query the user's current Simple Earn flexible positions for all currencies.

**Prompt Examples**:
- "My total Simple Earn positions" / "How much do I hold in flexible earn?"

**Expected Behavior**:
1. Fetch data via `gate-cli cex earn uni lends` (no currency param) to get the full list of currencies.
2. From each record take **currency** and **amount**, format as a list.
3. Output success: Query submitted! Your current Simple Earn positions: {list currency and amount per currency}. Failure: Query submitted! {error toast}.

**MCP** (see `earn-uni-mcp-tools.md` §4): **`gate-cli cex earn uni lends`**

---

## Scenario 5: Single-currency interest query

**Context**: Query the user's cumulative interest distributed for a currency in Simple Earn flexible.

**Prompt Examples**:
- "How much USDT interest have I received?" / "My BTC interest from flexible earn"

**Expected Behavior**:
1. Fetch data via `gate-cli cex earn uni interest`; use the returned **interest** field.
2. No extra calculation; use the API-returned interest directly.
3. Output success: Query submitted! Your current {currency} Simple Earn interest distributed is {interest}. Failure: Query submitted! {error toast}.

**MCP** (see `earn-uni-mcp-tools.md` §7): **`gate-cli cex earn uni interest`**

---

## Scenario 6: Subscribe to highest APY currency

**Context**: Get the currency with the highest estimated APY and support user subscribing to it (user must confirm amount).

**Prompt Examples**:
- "Subscribe to the Simple Earn currency with highest APY" / "What's the highest APY in flexible earn? Subscribe to it"

**Expected Behavior**:
1. Call `gate-cli cex earn uni rate` to get estimated APY and find the highest currency.
2. Ask for amount 
3. If user provides `min_rate`, use it directly.
4. If user does not provide `min_rate`, call `gate-cli cex earn uni currency` for that currency and use the returned flexible `min_rate` as default.
5. Confirm details with the user (including the final `min_rate`).
6. Call `gate-cli cex earn uni lend` with `type: lend`.

**MCP**: `gate-cli cex earn uni rate` then `gate-cli cex earn uni lend` (see `earn-uni-mcp-tools.md` §11, §3).

---

## Scenario 7: Change min rate

**Context**: User changes the minimum lend rate for an existing Simple Earn position.

**Prompt Examples**:
- "Change my USDT min rate to 0.05" / "Update min_rate for BTC"

**Expected Behavior**:
1. Ask for missing inputs: currency, min_rate.
2. Confirm details with the user.
3. Call `gate-cli cex earn uni change`.

**MCP**: `gate-cli cex earn uni change` (see `earn-uni-mcp-tools.md` §5).

---

## Auth failure

When any account/uni call returns 401 or 403: do not expose credentials; do not retry or rotate keys in chat. Output: **"Unable to query your orders/balance. Please configure your Gate API Key (with earn/account read permission) in MCP settings and try again."**

---

# Fixed Earn (Fixed-term) — Scenarios & Prompt Examples

Skill: Fixed Earn. Nine cases map to **MCP tools**; for tool arguments and response see **`fixed-earn-mcp-tools.md`**.

| Purpose | MCP tool |
|---------|----------|
| List all fixed-term products | **`gate-cli cex earn fixed products`** |
| List fixed-term products by asset | **`gate-cli cex earn fixed products-asset`** |
| Create fixed-term subscribe | **`gate-cli cex earn fixed create`** |
| Pre-redeem fixed-term order | **`gate-cli cex earn fixed pre-redeem`** |
| List user fixed-term positions | **`gate-cli cex earn fixed lends`** |
| Query fixed-term history | **`gate-cli cex earn fixed history`** |

---

## Scenario 1: Query all fixed-term product list (Query all Fixed Earn products)

**Context**: User asks for all fixed-term products available for subscription in Fixed Earn. **Only return products with status=2 (subscribing) and show_status=2 (visible).**

**Prompt Examples**:
- "Which Fixed Earn products are available?" / "Which fixed-term products can I subscribe to?"

**Expected Behavior**:
1. Call `gate-cli cex earn fixed products` (gate-d-e) with **status=2 (subscribing)** and **show_status=2 (visible)**; only return products that are subscribable and visible. Paginate with `page` and `limit` as needed, and default `limit` to `10` when omitted.
2. Output: Query submitted! The Fixed Earn product list is as follows: then a table in the following format.

**Output table format**: use the table title **"Fixed Earn products"** and the following column order (consistent with the frontend):

| Currency | pid | Term (days) | Product type | Current base APY | Minimum subscription | Subscription limit | Remaining available amount | Early redemption supported | Auto-compounding supported | Maturity rollover supported |
|------|-----|----------|----------|--------------|--------------|--------------|----------------|------------------|------------------|------------------------|
| USDT | 123 | 7 | Normal | 0.25% | 1 | 100,000 | 100,000 | Yes | Yes | Yes |
| USDT | 124 | 30 | VIP | 1.33% | 0.0001 | 0.01 | 0.007 | No | Yes | Yes |

- **Product type**：type 1→Normal，2→VIP。
- **Early redemption / auto-compounding / maturity rollover**: fill Yes/No according to `pre_redeem`, `reinvest`, and `redeem_amount` (or `simple_earn`).

**MCP** (see `fixed-earn-mcp-tools.md` §1): **`gate-cli cex earn fixed products`**

---

## Scenario 2: Query fixed-term products by currency (Query all Fixed Earn products for a specific currency)

**Context**: User asks for all fixed-term products for a specific currency (e.g. USDT). **Only return products with status=2 (subscribing) and show_status=2 (visible).**

**Prompt Examples**:
- "Please check which Fixed Earn products are available for USDT" / "Which fixed-term products can I subscribe to with USDT?"

**Expected Behavior**:
1. Extract asset (e.g. USDT) from user input; if missing, ask.
2. Call `gate-cli cex earn fixed products-asset` (gate-d-e) with `asset`; if the API supports it, pass **status=2** and **show_status=2** and only return subscribing and visible products.
3. If the asset-scoped response does not include `Minimum subscription`, `Subscription limit`, `Remaining available amount`, or `Maturity rollover supported`, call the full product list with the same `asset` plus `status=2` and `show_status=2`, then use the matching product row to fill those fields.
4. Output: Query submitted! The Fixed Earn USDT product list is as follows: then the same table structure as Scenario 1.

**MCP** (see `fixed-earn-mcp-tools.md` §2): **`gate-cli cex earn fixed products-asset`**

---

## Scenario 3: Fixed-term manual subscribe (Fixed Earn manual subscription)

**Context**: User wants to subscribe a fixed amount of a currency to a fixed-term product (e.g. 7-day, 30-day). Create one fixed-term lend order.

**Prompt Examples**:
- "Subscribe 100 USDT to Fixed Earn for 7 days" / "Buy 0.01 BTC Fixed Earn for 30 days"

**Expected Behavior**:
1. Extract or ask for the currency, amount, and term (e.g. 7 days); resolve to `product_id` (e.g. via the product list by asset + lock_up_period). **Only use products with status=2 (subscribing).**
2. Call `gate-cli cex earn fixed create` (gate-d-e) with `product_id`, `amount`, `year_rate` (from product), and other required body fields.
3. Output success: Subscription submitted! You have successfully subscribed to the {amount} {currency} Fixed Earn {lock_up_period}-day product {order_id}.

**MCP** (see `fixed-earn-mcp-tools.md` §3): **`gate-cli cex earn fixed create`**

---

## Scenario 4: Fixed-term early redeem (Fixed Earn manual early redemption)

**Context**: User wants to early-redeem a fixed-term order by order_id.

**Prompt Examples**:
- "Redeem order number 123456 Fixed Earn order"

**Expected Behavior**:
1. Extract or ask: `order_id`.
2. Call `gate-cli cex earn fixed pre-redeem` (gate-d-e) with `order_id` (string).
3. Output success: Early redemption submitted! You have successfully early-redeemed the Fixed Earn {lock_up_period}-day product {order_id}; redeemed principal {principal}.

**MCP** (see `fixed-earn-mcp-tools.md` §5): **`gate-cli cex earn fixed pre-redeem`**

---

## Scenario 5: Fixed-term total positions (Fixed Earn total positions query)

**Context**: User asks for total fixed-term positions (all current orders and amounts).

**Prompt Examples**:
- "How many positions and how much amount are there in Fixed Earn?" / "What is the current total Fixed Earn position amount?"

**Expected Behavior**:
1. Call `gate-cli cex earn fixed lends` (gate-d-e) with `order_type: "1"` (current orders), `page`, and `limit`; paginate if needed.
2. Output: Query submitted! Your current Fixed Earn positions are as follows: then render the screenshot-style table below.

**Output table format** (Fixed Earn total positions, screenshot style):

| order_id | Underlying currency | Holding term (days) | Product type | Current base APY | Estimated maturity yield | Subscription time (UTC+0) | Maturity time (UTC+0) | Remaining days | Early redemption supported | Auto-compounding supported | Maturity rollover supported |
|----------|----------|------------------|----------|--------------|--------------|------------------|------------------|--------------|------------------|------------------|------------------------|
| 12366 | USDT | 7 | Normal | 0.25% | 1.6789 | 2025-3-21 18:00:56 | 2025-3-25 00:00:00 | 2 | Yes | Yes | Yes |
| 12476 | DOGE | 30 | VIP | 1.33% | 2.888 | 2025-3-21 18:00:56 | 2025-3-25 00:00:00 | 5 | No | Yes | Yes |

- **Product type**: display `product_type` as Normal / VIP, etc.
- **Subscription time and Maturity time**: UTC+0, format `YYYY-MM-DD HH:MM:SS`.
- **Remaining days**: calculated from the maturity time and the current time.
- **Early redemption / auto-compounding / maturity rollover**: fill Yes/No according to `product_info.pre_redeem`, `reinvest`, and `redeem_account` (1 → Yes, 0 → No).

**MCP** (see `fixed-earn-mcp-tools.md` §4): **`gate-cli cex earn fixed lends`**

---

## Scenario 6: Single fixed-term order detail (Fixed Earn single position detail query)

**Context**: User asks for details of one fixed-term order by order_id.

**Prompt Examples**:
- "Please check Fixed Earn order number 123456" / "What is the current status of Fixed Earn order number 5556?"

**Expected Behavior**:
1. Extract or ask: `order_id`.
2. Call `gate-cli cex earn fixed lends` (gate-d-e) with `order_type: "1"`, `order_id`, `page`, `limit`.
3. Output: Query submitted! Your Fixed Earn position {order_id} is as follows: then render the same screenshot-style table, using the Scenario 5 column layout for the matching order.

**MCP** (see `fixed-earn-mcp-tools.md` §4): **`gate-cli cex earn fixed lends`**

---

## Scenario 7: Fixed-term history (Fixed Earn history records query)

**Context**: User asks for fixed-term wealth management history in a time range (subscribe / redeem / interest). Obtain user's history for the period; subscribe/redeem/interest.

**Prompt Examples**:
- "Please check the last 3 months of fixed-term subscription records"
- "Fixed-term redemption order records from 2025/1/1 to 2025/12/31"
- "Please check the last month of fixed-term interest records"

**Expected Behavior**:
1. Parse or ask time range (e.g. last 3 months, or start_at/end_at). Query the Fixed Earn transaction history via MCP; paginate or merge types as needed.
2. Call `gate-cli cex earn fixed history` with `type` (1=subscribe, 2=redeem, 3=interest, 4=extra bonus) and optionally `start_at`, `end_at`; may call multiple types and merge, or paginate.
3. Output: **Query submitted! The Fixed Earn records are as follows** (if querying by time range, append "{start time} to {end time}"), then a table in the following format.

**Output table format** (Fixed Earn records; subscribe/redeem/interest/extra bonus all use this table):

| order_id | Operation time | Operation type | Underlying currency | Amount | Term (days) |
|----------|--------------|----------|--------------|------|--------------|
| 123445 | 2025-01-01 00:00 | subscribe | USDT | 100.123 | 7 |
| 123445 | 2025-01-01 00:00 | redeem | USDT | 100.123 | 30 |
| 123445 | 2025-01-01 00:00 | interest | USDT | 0.8 | 30 |

- **Operation type**：subscribe(type=1) / redeem(type=2) / interest(type=3) / extra bonus(type=4)。
- **Amount**: corresponds to the interface field **amount** (principal for subscribe/redeem, interest amount for interest).
- **Term (days)**: corresponds to `lock_up_period`. The last N fixed-term subscribe/redeem/interest records all use the 6 columns above.

**API response fields → table columns**:

| Table column | API field | Description |
|--------|----------|------|
| order_id | **order_id** | Order ID, use the API `order_id` field; fall back to `id` if it is not returned |
| Operation time | create_time | `YYYY-MM-DD HH:MM` |
| Operation type | type | 1 subscribe / 2 redeem / 3 interest / 4 extra bonus |
| Underlying currency | asset | Currency |
| Amount | **amount** | principal for subscribe/redeem, interest amount for interest |
| Term (days) | **lock_up_period** | Term (days) |

**MCP** (see `fixed-earn-mcp-tools.md` §6): **`gate-cli cex earn fixed history`**

---

## Scenario 8: Compliance / region restriction (region-based order restrictions)

**Context**: User asks whether they can subscribe in their region or which regions are supported. Fixed Earn has region restrictions; subscription may be blocked for restricted regions.

**Prompt Examples**:
- "Can I subscribe in {region}?" / "Which regions does Fixed Earn support?"

**Expected Behavior**:
1. Do not perform subscribe; if user attempts subscribe in a restricted region, the create-order API will return a compliance error.
2. Return the standard compliance error message to the user.

**Output**: (return the specific error code information) Due to compliance restrictions, your region is not currently supported.

---

## Scenario 9: Compliance check failure (compliance validation failure)

**Context**: User reports that subscription failed with a compliance/region check error. Explain and return the same error message.

**Prompt Examples**:
- "Why does the compliance check fail?" / "My Fixed Earn subscription failed and it says compliance validation did not pass."

**Expected Behavior**:
1. Do not retry or expose internal logic; return the API error code/message when available.
2. Output the standard compliance message.

**Output**: (return the specific error code information) Due to compliance restrictions, your region is not currently supported.
