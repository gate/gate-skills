# Simple Earn (Uni) — Scenarios & Prompt Examples

Skill: Simple Earn (Uni) phase one. Six cases map to **MCP tools** and REST endpoints; for request/response details see **`earn-uni-api.md`**.

| Purpose | MCP tool | REST | Auth |
|---------|----------|------|------|
| Create lend or redeem | **Do not call** (this skill does not perform subscribe/redeem) | POST /earn/uni/lends | Yes |
| User lend list (positions) | **cex_earn_list_user_uni_lends** | GET /earn/uni/lends | Yes |
| Single-currency total interest | **cex_earn_get_uni_interest** | GET /earn/uni/interests/{currency} | Yes |
| Estimated APY per currency | **cex_earn_list_uni_rate** | GET /earn/uni/rate | No |

---

## Scenario 1: Subscribe (Lend)

**Context**: User subscribes a specified amount of a currency to Simple Earn flexible (Uni).

**Prompt Examples**:
- "Subscribe 100 USDT to Simple Earn" / "Buy 0.01 BTC into flexible earn"

**Expected Behavior** (this skill in effect):
1. Do not call `cex_earn_create_uni_lend`; do not show subscribe draft.
2. Reply to user: "Simple Earn subscribe and redeem are currently not supported."

**API & MCP**: This scenario does not call POST /earn/uni/lends (cex_earn_create_uni_lend); for reference only.

---

## Scenario 2: Redeem

**Context**: User redeems a specified amount of a currency from Simple Earn flexible.

**Prompt Examples**:
- "Redeem 100 USDT from Simple Earn" / "Redeem 0.01 BTC from flexible earn"

**Expected Behavior** (this skill in effect):
1. Do not call `cex_earn_create_uni_lend`; do not show redeem draft.
2. Reply to user: "Simple Earn subscribe and redeem are currently not supported."

**API & MCP**: This scenario does not call POST /earn/uni/lends (cex_earn_create_uni_lend); for reference only.

---

## Scenario 3: Single-currency position query

**Context**: Query the user's current Simple Earn flexible position for a given currency.

**Prompt Examples**:
- "My USDT Simple Earn position" / "How much BTC do I have in flexible earn?"

**Expected Behavior**:
1. Fetch data via `cex_earn_list_user_uni_lends(currency="USDT")`; from the returned list take **amount** (total position) for that currency.
2. No extra calculation; use the API-returned amount directly.
3. Output success: Query submitted! Your current {currency} Simple Earn position is {amount}. Failure: Query submitted! {error toast}.

**API & MCP** (see `earn-uni-api.md` §4)

| Method | Path | MCP tool |
|--------|------|----------|
| GET | /earn/uni/lends | **cex_earn_list_user_uni_lends** |

---

## Scenario 4: All positions query

**Context**: Query the user's current Simple Earn flexible positions for all currencies.

**Prompt Examples**:
- "My total Simple Earn positions" / "How much do I hold in flexible earn?"

**Expected Behavior**:
1. Fetch data via `cex_earn_list_user_uni_lends()` (no currency param) to get the full list of currencies.
2. From each record take **currency** and **amount**, format as a list.
3. Output success: Query submitted! Your current Simple Earn positions: {list currency and amount per currency}. Failure: Query submitted! {error toast}.

**API & MCP** (see `earn-uni-api.md` §4)

| Method | Path | MCP tool |
|--------|------|----------|
| GET | /earn/uni/lends | **cex_earn_list_user_uni_lends** |

---

## Scenario 5: Single-currency interest query

**Context**: Query the user's cumulative interest distributed for a currency in Simple Earn flexible.

**Prompt Examples**:
- "How much USDT interest have I received?" / "My BTC interest from flexible earn"

**Expected Behavior**:
1. Fetch data via `cex_earn_get_uni_interest(currency="USDT")`; use the returned **interest** field.
2. No extra calculation; use the API-returned interest directly.
3. Output success: Query submitted! Your current {currency} Simple Earn interest distributed is {interest}. Failure: Query submitted! {error toast}.

**API & MCP** (see `earn-uni-api.md` §7)

| Method | Path | MCP tool |
|--------|------|----------|
| GET | /earn/uni/interests/{currency} | **cex_earn_get_uni_interest** |

---

## Scenario 6: Subscribe to highest APY currency

**Context**: Get the currency with the highest estimated APY and support user subscribing to it (user must confirm amount).

**Prompt Examples**:
- "Subscribe to the Simple Earn currency with highest APY" / "What's the highest APY in flexible earn? Subscribe to it"

**Expected Behavior** (this skill in effect):
1. Do not call `cex_earn_create_uni_lend` for subscribe. May call `cex_earn_list_uni_rate()` to show top APY currency and rate (read-only).
2. If user intent is subscribe or one-click subscribe, reply: "Simple Earn subscribe and redeem are currently not supported."

**API & MCP**: May use GET /earn/uni/rate for display only; do not call POST /earn/uni/lends (cex_earn_create_uni_lend).

---

## Auth failure

When any account/uni call returns 401 or 403: do not expose credentials; do not retry or rotate keys in chat. Output: **"Unable to query your orders/balance. Please configure your Gate API Key (with earn/account read permission) in MCP settings and try again."**
