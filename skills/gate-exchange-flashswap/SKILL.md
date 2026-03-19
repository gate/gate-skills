---
name: gate-exchange-flashswap
version: "2026.3.18-5"
updated: "2026-03-18"
description: Gate Flash Swap Skill for querying supported pairs, previewing quotes, and executing one-to-one, one-to-many, and many-to-one flash swap orders. Use this skill whenever you need to flash swap, convert, or exchange cryptocurrencies, preview swap quotes, check flash swap pairs, or view flash swap order history. Trigger phrases include "flash swap", "convert", "swap BTC to USDT", "buy BTC ETH SOL", "sell multiple coins", "flash swap order history", or any request involving cryptocurrency conversion.
---

# Gate Flash Swap

## General Rules
Read and follow the shared runtime rules before proceeding:
→ `exchange-runtime-rules.md`

---

Gate Flash Swap supports instant cryptocurrency conversion with three swap modes: one-to-one, one-to-many, and many-to-one. This Skill covers the full lifecycle: querying pairs, previewing quotes, executing swaps, and tracking orders.

## Trigger Conditions

This Skill is activated when the user's request matches any of the following:
- Wants to swap/convert/exchange one cryptocurrency for another
- Wants to buy multiple cryptocurrencies at once using one currency (e.g. "buy 1u BTC, 2u ETH")
- Wants to sell multiple cryptocurrencies into one target currency (e.g. "sell 1 BTC, 2 ETH for USDT")
- Asks which currencies support flash swap
- Asks about minimum/maximum swap amounts or limits
- Requests flash swap order history or specific order details
- Uses keywords: "flash swap", "convert", "quick exchange", "swap", "instant swap"

## Quick Start

Common usage examples:

1. **One-to-one swap**: "Sell 1 BTC for USDT"
2. **Buy multiple coins**: "Buy 1u BTC, 2u ETH, 3u SOL"
3. **Sell multiple coins**: "Sell 1 BTC, 2 ETH, 3 SOL for USDT"
4. **Check pairs**: "Show me flash swap supported pairs"
5. **Order history**: "Show me my flash swap orders"

## Domain Knowledge

**Flash Swap** is a quick crypto exchange service provided by Gate. Users can instantly convert one cryptocurrency to another at the real-time exchange rate without placing orders and waiting for matching.

**Swap Modes**:
- **One-to-One**: Swap a single currency for another single currency (e.g. BTC → USDT)
- **One-to-Many**: Swap one currency into multiple target currencies (e.g. USDT → BTC + ETH + SOL)
- **Many-to-One**: Swap multiple currencies into one target currency (e.g. BTC + ETH + SOL → USDT)

**Key Concepts**:
- **sell_asset / buy_asset**: The currency symbols for the sell side and buy side
- **sell_amount / buy_amount**: Specify one of them; the API calculates the other. For one-to-many, use `sell_amount` per target; for many-to-one, use `sell_amount` per source
- **quote_id**: A unique identifier returned by the preview API, required for order creation. The exact validity period is indicated by `valid_timestamp` in the response. Always check this field — do not assume a fixed duration
- **Order Status**: `1` = success, `2` = failed

**API Field Naming**:

- `cex_fc_list_fc_currency_pairs` returns **snake_case** fields: `sell_min_amount`, `sell_max_amount`, `buy_min_amount`, `buy_max_amount`, `currency_pair`, `sell_currency`, `buy_currency`
- `cex_fc_preview_fc_order_v1` and multi-currency preview APIs return **camelCase** fields in some environments (e.g. `sellMinAmount`). Always read the actual field names from the response — do not assume a fixed naming convention
- `cex_fc_list_fc_orders` and `cex_fc_get_fc_order` return snake_case: `sell_currency`, `buy_currency`, `sell_amount`, `buy_amount`, `create_time`

**Data type note**: `order_id` is returned as a **string** in API responses. `quote_id` is also a string.

**MCP Tool Inventory**:

| Tool | Type | Description |
|------|------|-------------|
| `cex_fc_preview_fc_order_v1` | Preview | One-to-one swap quote preview |
| `cex_fc_create_fc_order_v1` | Create | One-to-one swap order creation (requires `quote_id`) |
| `cex_fc_preview_fc_multi_currency_one_to_many_order` | Preview | One-to-many swap quote preview |
| `cex_fc_create_fc_multi_currency_one_to_many_order` | Create | One-to-many swap order creation |
| `cex_fc_preview_fc_multi_currency_many_to_one_order` | Preview | Many-to-one swap quote preview |
| `cex_fc_create_fc_multi_currency_many_to_one_order` | Create | Many-to-one swap order creation |
| `cex_fc_list_fc_currency_pairs` | Query | List supported flash swap pairs and limits |
| `cex_fc_list_fc_orders` | Query | Query flash swap order history |
| `cex_fc_get_fc_order` | Query | Query single flash swap order by ID |

## Workflow

### Step 1: Identify User Intent

Analyze the user's request to determine which flash swap operation to perform.

**Intent classification**:

| User Intent | Mode | Preview Tool | Create Tool |
|-------------|------|-------------|-------------|
| Swap one coin for another (e.g. "sell 1 BTC for USDT") | one-to-one | `cex_fc_preview_fc_order_v1` | `cex_fc_create_fc_order_v1` |
| One-click swap without separate confirmation (e.g. "directly swap 100 USDT to GT") | one-to-one-auto | `cex_fc_preview_fc_order_v1` → `cex_fc_create_fc_order_v1` | — |
| Buy multiple coins with one currency (e.g. "buy 1u BTC, 2u ETH") | one-to-many | `cex_fc_preview_fc_multi_currency_one_to_many_order` | `cex_fc_create_fc_multi_currency_one_to_many_order` |
| Split one currency into multiple by ratio (e.g. "split 1000 USDT, half BTC half ETH") | one-to-many-split | `cex_fc_preview_fc_multi_currency_one_to_many_order` | `cex_fc_create_fc_multi_currency_one_to_many_order` |
| Buy specific quantities of multiple coins (e.g. "buy 0.1 BTC and 1 ETH with USDT") | one-to-many-buy | `cex_fc_preview_fc_multi_currency_one_to_many_order` | `cex_fc_create_fc_multi_currency_one_to_many_order` |
| Sell multiple coins into one currency (e.g. "sell 1 BTC, 2 ETH for USDT") | many-to-one | `cex_fc_preview_fc_multi_currency_many_to_one_order` | `cex_fc_create_fc_multi_currency_many_to_one_order` |
| Consolidate all holdings of certain coins into one (e.g. "convert all my BTC, ETH, DOGE to USDT") | many-to-one-all | `cex_fc_preview_fc_multi_currency_many_to_one_order` | `cex_fc_create_fc_multi_currency_many_to_one_order` |
| Preview-only for multi-currency (e.g. "how much GT can I get for my BTC and ETH?") | many-to-one-preview | `cex_fc_preview_fc_multi_currency_many_to_one_order` | — |
| Query supported flash swap pairs | query | `cex_fc_list_fc_currency_pairs` | — |
| Query flash swap order list | query | `cex_fc_list_fc_orders` | — |
| Query single flash swap order by ID | query | `cex_fc_get_fc_order` | — |
| Verify latest order result (e.g. "did my swap succeed?") | verify-order | `cex_fc_get_fc_order` | — |

Key data to extract:
- `intent`: "one_to_one" / "one_to_one_auto" / "one_to_many" / "one_to_many_split" / "one_to_many_buy" / "many_to_one" / "many_to_one_all" / "many_to_one_preview" / "list_pairs" / "list_orders" / "get_order" / "verify_order"
- `sell_asset` / `buy_asset`: currencies involved
- `sell_amount` / `buy_amount`: amounts specified by the user

### Step 2: Pre-validate Swap Amount (before any preview)

Before calling the preview API, validate the user's amount against the pair's min/max limits to avoid unnecessary API calls.

Call `cex_fc_list_fc_currency_pairs` with:
- `currency`: the sell_asset or buy_asset from the user's request

Key data to extract:
- `sell_min_amount` / `sell_max_amount`: allowed range for the sell side
- `buy_min_amount` / `buy_max_amount`: allowed range for the buy side

**Validation logic**:
- If the user's `sell_amount` < `sell_min_amount`, inform them the amount is below the minimum and do NOT proceed to preview
- If the user's `sell_amount` > `sell_max_amount`, inform them the amount exceeds the maximum
- If the pair is not found, the currency is not supported for flash swap

Skip this step if the user explicitly requests "one-click" or "direct" swap to minimize latency.

### Step 3: Preview — One-to-One Swap (if intent = one_to_one or one_to_one_auto)

Call `cex_fc_preview_fc_order_v1` with:
- `sell_asset` (required, string): asset to sell, e.g. "BTC"
- `buy_asset` (required, string): asset to buy, e.g. "USDT"
- `sell_amount` (string): amount to sell. Choose one between `sell_amount` and `buy_amount`
- `buy_amount` (string): amount to buy. Choose one between `sell_amount` and `buy_amount`

Key data to extract:
- `quote_id`: required for creating the order
- `sell_asset` / `sell_amount`: confirmed sell side
- `buy_asset` / `buy_amount`: calculated buy side
- `price`: exchange rate
- `valid_timestamp`: quote expiry time

**For one_to_one intent**: Present the preview to the user and ask for confirmation before proceeding to create.

**For one_to_one_auto intent**: The user has pre-authorized the swap by explicitly requesting "direct" or "one-click" execution. Skip the separate confirmation prompt and immediately proceed to Step 4. This is compliant with the Safety Rules as the user's direct request serves as confirmation. **However**: if the preview returns any error (code != 0), do NOT proceed to Step 4 — report the error to the user immediately.

### Step 4: Create — One-to-One Swap (after user confirms Step 3, or auto for one_to_one_auto)

**Pre-condition**: Step 3 must have returned `code == 0` with a valid `quote_id`. If Step 3 failed (any `code != 0`), do NOT execute this step. Never fabricate a `quote_id`.

Call `cex_fc_create_fc_order_v1` with body JSON string:
- `quote_id` (required, string): from preview response — must be the actual value returned by the API
- `sell_asset` (required, string): asset to sell
- `sell_amount` (required, string): amount to sell
- `buy_asset` (required, string): asset to buy
- `buy_amount` (required, string): amount to buy

Key data to extract:
- `id`: created order ID
- `status`: `1` = success, `2` = failed
- `sell_asset` / `sell_amount` / `buy_asset` / `buy_amount`: confirmed amounts
- `price`: executed rate
- `create_time`: order creation timestamp
- `error.code` / `error.message`: check for errors even when HTTP status is 200

**Order result verification**: After creating, check the `status` field:
- If `status == 1`: Inform the user the swap succeeded, show the final `buy_amount` received
- If `status == 2`: Inform the user the swap failed, suggest re-previewing and trying again
- If `error.code != 0`: Report the specific error message to the user

### Step 5: Preview — One-to-Many Swap (if intent = one_to_many, one_to_many_split, or one_to_many_buy)

**For one_to_many_split**: The user specifies a total amount and a distribution ratio (e.g. "split 1000 USDT, half BTC half ETH"). Calculate the per-target `sell_amount` before calling the API.

**For one_to_many_buy**: The user specifies target `buy_amount` per currency (e.g. "buy 0.1 BTC and 1 ETH"). Use the `buy_amount` field instead of `sell_amount` in the params array to let the API calculate the required sell amount.

Call `cex_fc_preview_fc_multi_currency_one_to_many_order` with body JSON string:
- `params` (required, array): each element contains:
  - `sell_asset` (required, string): source currency (same for all, e.g. "USDT")
  - `sell_amount` (string): amount of source currency to spend on this target
  - `buy_asset` (required, string): target currency (e.g. "BTC", "ETH")
  - `buy_amount` (string): alternative to sell_amount

Key data to extract:
- `orders[]`: array of preview results, each containing `quote_id`, `sell_amount`, `buy_amount`, `price`, and `error`
- `total_consume_amount`: total amount of source currency consumed
- Check each order's `error.code` — if non-zero, that item failed to get a quote

Present the full preview table and highlight any failed items. Ask for confirmation.

### Step 6: Create — One-to-Many Swap (after user confirms Step 5)

**Important**: Exclude any items that failed in preview (where `error.code != 0` or `quote_id` is missing).

Call `cex_fc_create_fc_multi_currency_one_to_many_order` with body JSON string:
- `params` (required, array): each element contains:
  - `sell_asset` (required, string): source currency
  - `sell_amount` (required, string): amount to sell
  - `buy_asset` (required, string): target currency
  - `buy_amount` (required, string): amount to buy (from preview)
  - `quote_id` (string): from preview response

Key data to extract:
- `orders[]`: array of created orders, each with `id`, `status`, `error`
- `total_consume_amount`: actual total consumed
- Check each order's `error.code` for per-item failures

### Step 7: Preview — Many-to-One Swap (if intent = many_to_one, many_to_one_all, or many_to_one_preview)

**For many_to_one_all**: The user wants to consolidate all holdings of specified currencies. Before previewing, query the user's spot account balances to determine the actual amount for each currency. Filter out currencies whose balance is below the flash swap minimum amount (`sell_min_amount` from `cex_fc_list_fc_currency_pairs`).

Call `cex_fc_preview_fc_multi_currency_many_to_one_order` with body JSON string:
- `params` (required, array): each element contains:
  - `sell_asset` (required, string): source currency (e.g. "BTC", "ETH")
  - `sell_amount` (string): amount to sell
  - `buy_asset` (required, string): target currency (same for all, e.g. "USDT")
  - `buy_amount` (string): alternative to sell_amount

Key data to extract:
- `orders[]`: array of preview results with `quote_id`, `sell_amount`, `buy_amount`, `price`, `error`
- `total_acquire_amount`: total amount of target currency to receive
- Check each order's `error.code` — non-zero means that item failed

Present the full preview table and highlight any failed items.

**For many_to_one_preview**: Present the total expected `buy_amount` (sum of all successful items) and do NOT proceed to create. Inform the user this is a preview only.

**For many_to_one and many_to_one_all**: Ask for user confirmation before proceeding to create.

### Step 8: Create — Many-to-One Swap (after user confirms Step 7)

**Important**: Exclude any items that failed in preview. Including a failed item (e.g. `buy_amount: "0"`) will cause the entire request to be rejected with `code: 4`.

Call `cex_fc_create_fc_multi_currency_many_to_one_order` with body JSON string:
- `params` (required, array): each element contains:
  - `sell_asset` (required, string): source currency
  - `sell_amount` (required, string): amount to sell
  - `buy_asset` (required, string): target currency
  - `buy_amount` (required, string): amount to buy (from preview)
  - `quote_id` (string): from preview response

Key data to extract:
- `orders[]`: array of created orders with `id`, `status`, `error`
- `total_acquire_amount`: actual total received

### Step 9: Query Flash Swap Pairs (if intent = list_pairs)

Call `cex_fc_list_fc_currency_pairs` with:
- `currency` (optional, string): filter by currency symbol
- `limit` (optional, number): max items returned (default 1000)
- `page` (optional, number): page number

**Large result set warning**: Without a currency filter, this may return thousands of rows. Summarize the total count, show a sample of 20 pairs, and suggest filtering by currency.

Key data to extract:
- `items[]`: list of currency pairs with `currency_pair`, `sell_currency`, `buy_currency`, `sell_min_amount`, `sell_max_amount`, `buy_min_amount`, `buy_max_amount`

### Step 10: Query Flash Swap Order History (if intent = list_orders)

Before calling, validate the `status` parameter if provided. Only `1` (success) and `2` (failed) are valid.

Call `cex_fc_list_fc_orders` with:
- `status` (optional, number): `1` = success, `2` = failed
- `sell_currency` (optional, string): filter by sell currency
- `buy_currency` (optional, string): filter by buy currency
- `limit` (optional, number): max records
- `page` (optional, number): page number
- `reverse` (optional, boolean): `true` for newest first (default)

Key data to extract:
- Order list with `id`, `sell_currency`, `buy_currency`, `sell_amount`, `buy_amount`, `price`, `status`, `create_time`

### Step 11: Query Single Order (if intent = get_order or verify_order)

Call `cex_fc_get_fc_order` with:
- `order_id` (required, number): the order ID to query

If the API returns 404, inform the user the order was not found.

**For verify_order**: After retrieving the order, check `status`:
- If `status == 1`: Confirm the swap succeeded, show the final `buy_amount` actually received
- If `status == 2`: Inform the user the swap failed, suggest re-previewing and placing a new order

Key data to extract:
- Full order details: `id`, `sell_currency`, `buy_currency`, `sell_amount`, `buy_amount`, `price`, `status`, `create_time`

### Step 12: Format and Present Results

Format results using the appropriate Report Template. For swap operations, always show:
1. Preview summary table with quote details
2. After creation, show order IDs, status, and any per-item errors

## Error Handling

| Error Scenario | Handling |
|----------------|----------|
| **Region/compliance restriction (code -2)** | **CRITICAL**: The API returns `{"code":-2,"message":"This service is not supported in your region"}`. This means flash swap is not available for this user's region. Immediately stop all operations, do NOT proceed to create, and inform the user: "Flash swap is not available in your region due to compliance restrictions." Do NOT fabricate any results |
| **Preview failed (any non-zero code)** | **CRITICAL**: If the preview API returns any `code != 0`, the operation has FAILED. Do NOT proceed to the create step. Do NOT fabricate a `quote_id`. Report the exact error code and message to the user. Never show "success" when the API returned an error |
| Amount below minimum (sell_amount < sell_min_amount) | Query `cex_fc_list_fc_currency_pairs` first. If below minimum, inform the user with the exact minimum and do NOT call preview |
| Amount above maximum (sell_amount > sell_max_amount) | Inform the user the amount exceeds the maximum allowed, show the limit |
| Quote expired (code 1052) | The `quote_id` has expired. Re-run the preview to get a fresh quote, then immediately create the order |
| Unable to get accurate quote (code 4 / 400001 / 400007) | These are quote-related errors from the server. `code 4` is a top-level rejection (often caused by including a failed item). `400001` and `400007` are per-item errors meaning the server cannot price this pair/amount. Suggest adjusting the amount, trying a different pair, or removing the failed item |
| Multi-currency create: entire request rejected (code 4) | Likely caused by including a preview-failed item with `buy_amount: "0"`. Remove all items where preview `error.code != 0` and retry |
| Order status == 2 (failed) | Inform the user the swap failed. Suggest re-previewing with adjusted parameters and trying again |
| Order not found (404) | The `order_id` does not exist. Suggest verifying the ID or querying the order list first |
| MCP service connection failure | Prompt user to check network or VPN, suggest retrying later |
| order_id not provided | Prompt user to provide an order ID, or use the order list query first |
| Empty query results | Inform user no data was found, suggest adjusting filters |
| Currency not supported | Inform user that the specified currency is not available for flash swap |
| Invalid status value | Status only accepts `1` (success) or `2` (failed). Reject other values before calling the API |
| Large result set (thousands of rows) | Summarize total count, show sample of 20, suggest filtering by currency |
| Balance below minimum for many_to_one_all | When consolidating all holdings, skip currencies whose balance < sell_min_amount and inform the user which were excluded |

## Safety Rules

- **NEVER fabricate results**: If any API call returns an error (code != 0), you MUST report the actual error to the user. NEVER fabricate a successful response, fake order ID, fake quote_id, or fake transaction result. This is the most critical safety rule
- **NEVER proceed after preview failure**: If the preview API returns any error (code != 0, including code -2 for region restriction), you MUST stop immediately. Do NOT call the create API. Do NOT invent a quote_id (e.g. "AUTO-GT-001"). Report the error honestly
- **Always preview before creating**: Every swap must go through the preview step first. For standard flows, show the quote to the user and wait for explicit confirmation before calling the create API. For `one_to_one_auto` mode only: the user has explicitly requested a direct swap (e.g. "directly swap", "one-click"), which counts as pre-authorized confirmation — proceed to create immediately after preview without a separate confirmation prompt
- **No write operations without confirmation**: Never call any create/order API unless (a) the user has explicitly confirmed the preview result, or (b) the user explicitly requested a one-click/direct swap. Query operations (list pairs, list orders, get order) do not require confirmation
- **Exclude failed preview items**: When creating multi-currency orders, only include items that succeeded in preview (`error.code == 0`)
- **Do not expose sensitive info**: Never output API Key, Secret, or authentication tokens
- **Display amounts as-is**: Do not round or modify amounts from API responses
- **Warn on large amounts**: If the total swap amount exceeds 10,000 USDT equivalent, remind the user to double-check
- **Stale confirmation handling**: If the user confirms a previous preview, check whether the current time has exceeded the `valid_timestamp` from that preview response. If expired, automatically re-preview to get a fresh quote before creating

## Judgment Logic Summary

| Condition | Action | Tool |
|-----------|--------|------|
| User wants to swap one coin for another | Preview one-to-one, then create after confirmation | `cex_fc_preview_fc_order_v1` → `cex_fc_create_fc_order_v1` |
| User says "directly" or "one-click" swap | Preview + create automatically without separate confirmation | `cex_fc_preview_fc_order_v1` → `cex_fc_create_fc_order_v1` |
| User references a previous quote_id for confirmation | Create order using the referenced quote_id | `cex_fc_create_fc_order_v1` |
| Swap amount is suspiciously small | Pre-validate against pair min amount before preview | `cex_fc_list_fc_currency_pairs` |
| User wants to buy multiple coins with one currency | Preview one-to-many, then create | `cex_fc_preview_fc_multi_currency_one_to_many_order` → `cex_fc_create_fc_multi_currency_one_to_many_order` |
| User wants to split one currency by ratio (e.g. "half and half") | Calculate per-target sell_amount, then preview one-to-many | `cex_fc_preview_fc_multi_currency_one_to_many_order` → `cex_fc_create_fc_multi_currency_one_to_many_order` |
| User specifies buy quantities (e.g. "buy 0.1 BTC and 1 ETH") | Use buy_amount in params, preview one-to-many | `cex_fc_preview_fc_multi_currency_one_to_many_order` → `cex_fc_create_fc_multi_currency_one_to_many_order` |
| User wants to sell multiple coins into one currency | Preview many-to-one, then create | `cex_fc_preview_fc_multi_currency_many_to_one_order` → `cex_fc_create_fc_multi_currency_many_to_one_order` |
| User wants to consolidate "all" of certain holdings | Query balances, filter by min amounts, preview many-to-one, then create | `cex_fc_list_fc_currency_pairs` → `cex_fc_preview_fc_multi_currency_many_to_one_order` → `cex_fc_create_fc_multi_currency_many_to_one_order` |
| User asks "how much can I get" without wanting to execute | Preview-only many-to-one, sum buy_amounts, do NOT create | `cex_fc_preview_fc_multi_currency_many_to_one_order` |
| Preview returns items with `error.code != 0` | Warn user, exclude failed items before creating | — |
| **Preview returns code -2 (region restriction)** | **STOP immediately. Do NOT create. Inform user flash swap is not available in their region** | — |
| **Preview returns any non-zero code** | **STOP. Do NOT create. Do NOT fabricate quote_id. Report exact error to user** | — |
| Create returns code 1052 (quote expired) | Re-run preview to get fresh quote | Preview tool |
| Create returns per-item error (400001/400007) | Report which items failed, suggest adjusting amounts | — |
| Multi-currency create rejected with code 4 | Remove failed preview items and retry | Create tool |
| Order status == 2 after create | Inform user swap failed, suggest retrying | — |
| User asks "did my swap succeed?" | Query order by ID, check status field | `cex_fc_get_fc_order` |
| User asks about supported pairs or limits | Query pair list | `cex_fc_list_fc_currency_pairs` |
| User queries order history | Query order list | `cex_fc_list_fc_orders` |
| User queries specific order by ID | Query single order | `cex_fc_get_fc_order` |
| Order not found (404) | Inform user, suggest checking ID | — |
| User provides invalid status filter | Reject and inform valid values are 1 or 2 | — |

## Report Template

**Timestamp format**: All `{timestamp}` placeholders use ISO 8601 format: `YYYY-MM-DD HH:mm:ss UTC`.

### One-to-One Preview Report

```markdown
## Flash Swap Preview (One-to-One)

**Quote ID**: {quote_id}
**Valid Until**: {valid_timestamp}

| Sell | Amount | Buy | Amount | Rate |
|------|--------|-----|--------|------|
| {sell_asset} | {sell_amount} | {buy_asset} | {buy_amount} | {price} |

Proceed with this swap? (Yes/No)
```

### One-to-One Order Report

```markdown
## Flash Swap Order Created

**Order ID**: {id}
**Status**: {status_text}
**Created At**: {create_time}

| Sell | Amount | Buy | Amount | Rate |
|------|--------|-----|--------|------|
| {sell_asset} | {sell_amount} | {buy_asset} | {buy_amount} | {price} |
```

### Multi-Currency Preview Report (One-to-Many / Many-to-One)

```markdown
## Flash Swap Preview ({mode})

**Total {direction}**: {total_amount} {currency}

| # | Sell | Sell Amount | Buy | Buy Amount | Rate | Quote ID | Status |
|---|------|-------------|-----|------------|------|----------|--------|
| {n} | {sell_asset} | {sell_amount} | {buy_asset} | {buy_amount} | {price} | {quote_id} | {status} |

{failed_count} item(s) failed to get a quote and will be excluded from the order.
Proceed with {success_count} successful item(s)? (Yes/No)
```

### Multi-Currency Order Report

```markdown
## Flash Swap Orders Created ({mode})

**Total {direction}**: {total_amount} {currency}

| # | Order ID | Sell | Sell Amount | Buy | Buy Amount | Status | Error |
|---|----------|------|-------------|-----|------------|--------|-------|
| {n} | {id} | {sell_asset} | {sell_amount} | {buy_asset} | {buy_amount} | {status_text} | {error_message} |

{success_count}/{total_count} orders succeeded.
```

### Pair List Report

```markdown
## Gate Flash Swap Supported Pairs

**Query Time**: {timestamp}
**Filter**: {currency filter or "None"}

| Pair | Sell Currency | Buy Currency | Sell Min | Sell Max |
|------|---------------|--------------|----------|----------|
| {currency_pair} | {sell_currency} | {buy_currency} | {sell_min_amount} | {sell_max_amount} |

Total: {total} pairs.
```

### Order List Report

```markdown
## Gate Flash Swap Order History

**Query Time**: {timestamp}
**Filters**: Status={status}, Sell={sell_currency}, Buy={buy_currency}

| Order ID | Sell | Sell Amount | Buy | Buy Amount | Status | Created At |
|----------|------|-------------|-----|------------|--------|------------|
| {id} | {sell_currency} | {sell_amount} | {buy_currency} | {buy_amount} | {status_text} | {create_time} |

Total: {total} records.
```

### Order Detail Report

```markdown
## Gate Flash Swap Order Details

| Field | Value |
|-------|-------|
| Order ID | {id} |
| Sell Currency | {sell_currency} |
| Sell Amount | {sell_amount} |
| Buy Currency | {buy_currency} |
| Buy Amount | {buy_amount} |
| Exchange Rate | {price} |
| Status | {status_text} |
| Created At | {create_time} |
```
