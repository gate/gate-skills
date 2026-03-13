---
name: gate-exchange-flashswap
version: "2026.3.11-5"
updated: "2026-03-11"
description: Gate Flash Swap query Skill for querying supported currency pairs, validating swap limits, viewing order history, and tracking specific orders. Use this skill whenever you need to query flash swap currency pairs, check swap limits, view flash swap order history, or look up a specific flash swap order. Trigger phrases include "flash swap pairs", "flash swap orders", "flash swap limits", "query flash swap", "check swap amount", or any request involving flash swap query.
---

# Gate Flash Swap Query

## General Rules
Read and follow the shared runtime rules before proceeding:
→ [exchange-runtime-rules.md](../exchange-runtime-rules.md)

---

Query Gate Flash Swap related information, including supported currency pair lists, swap amount limits, order history, and single order details.

## Trigger Conditions

This Skill is activated when the user's request matches any of the following:
- Mentions "flash swap" combined with queries about pairs, limits, orders, or history
- Asks which currencies support flash swap or instant exchange
- Asks about minimum/maximum swap amounts or limits
- Requests flash swap order history or specific order details
- Uses keywords: "flash swap", "instant swap", "quick exchange", "swap pairs", "swap limits"

## Quick Start

Common query examples:

1. **List supported pairs**: "Show me all flash swap supported pairs"
2. **Check swap limits**: "I want to swap BTC for USDT, what is the minimum and maximum amount?"
3. **View order history**: "Show me my recent flash swap orders"

## Domain Knowledge

**Flash Swap** is a quick crypto exchange service provided by Gate. Users can instantly convert one cryptocurrency to another at the real-time exchange rate without placing orders and waiting for matching.

Key concepts:
- **Currency Pair**: A supported exchange combination for flash swap, e.g. BTC_USDT represents the exchange between BTC and USDT
- **Sell Currency**: The currency the user pays
- **Buy Currency**: The currency the user receives
- **Sell Min/Max Amount**: The minimum and maximum quantity allowed for the sell currency in a single swap
- **Buy Min/Max Amount**: The minimum and maximum quantity allowed for the buy currency in a single swap
- **Order Status**: `1` = success, `2` = failed

**API Response Field Name Mapping**:

The API returns camelCase field names. Map them to the following when extracting data:

| API Response Field | SKILL.md Field | Description |
|--------------------|----------------|-------------|
| `sellMinAmount` | sell_min_amount | Minimum sell quantity |
| `sellMaxAmount` | sell_max_amount | Maximum sell quantity |
| `buyMinAmount` | buy_min_amount | Minimum buy quantity |
| `buyMaxAmount` | buy_max_amount | Maximum buy quantity |
| `sellCurrency` | sell_currency | Sell currency symbol |
| `buyCurrency` | buy_currency | Buy currency symbol |
| `sellAmount` | sell_amount | Actual sell amount |
| `buyAmount` | buy_amount | Actual buy amount |
| `createTime` | create_time | Order creation timestamp |

**Data type note**: `order_id` is returned as a **string** in API responses, not an integer. Always treat it as a string when extracting from results.

## Workflow

### Step 1: Identify User Intent

Analyze the user's request to determine which flash swap query to perform.

**Intent classification**:

| User Intent | Action | Tool |
|-------------|--------|------|
| Query all supported flash swap pairs / check which coins can be swapped | List all currency pairs | `cex_fc_list_fc_currency_pairs` |
| Check if a specific currency supports flash swap / check min-max swap limits | Query pairs filtered by currency | `cex_fc_list_fc_currency_pairs` |
| Query flash swap order list / swap history / check order statuses | List orders | `cex_fc_list_fc_orders` |
| Query a specific flash swap order by ID / track order details | Get single order | `cex_fc_get_fc_order` |

Key data to extract:
- `intent`: "list_pairs" / "check_limits" / "list_orders" / "get_order"
- `parameters`: any filter conditions mentioned by the user (currency, status, order_id, etc.)

### Step 2: Query All Flash Swap Currency Pairs (if intent = list_pairs)

Call `cex_fc_list_fc_currency_pairs` with:
- No parameters required

**Large result set warning**: This query may return 34,000+ rows. Do NOT dump the entire list to the user. Instead:
1. Summarize the total count of available pairs
2. Show the first 20 pairs as a sample table
3. Ask the user if they want to filter by a specific currency for a more targeted result

Key data to extract:
- `currency_pairs`: full list of supported flash swap trading pairs
- `sell_currency`: available sell currencies
- `buy_currency`: available buy currencies
- Total count of available pairs

### Step 3: Validate Currency Support and Check Swap Limits (if intent = check_limits)

If the user did not specify a currency, prompt them to provide one before proceeding. Suggest popular currencies (e.g. BTC, ETH, USDT) as examples.

Call `cex_fc_list_fc_currency_pairs` with:
- `currency` (required): the currency symbol to check, e.g. "BTC", "USDT"

Key data to extract:
- `currency_pairs`: pairs containing the specified currency
- `sell_min_amount`: minimum sell quantity per swap
- `sell_max_amount`: maximum sell quantity per swap
- `buy_min_amount`: minimum buy quantity per swap
- `buy_max_amount`: maximum buy quantity per swap

If the returned list is empty, the specified currency does not support flash swap.

### Step 4: Query Flash Swap Order History (if intent = list_orders)

Before calling the API, validate the `status` parameter if provided. Only `1` (success) and `2` (failed) are valid values. If the user provides any other value, inform them that status only accepts 1 or 2, and do not proceed with the API call.

Call `cex_fc_list_fc_orders` with:
- `status` (optional, integer): order status filter, `1` = success, `2` = failed. Must be validated before calling — only 1 or 2 are accepted
- `sell_currency` (optional, string): filter by sell currency
- `buy_currency` (optional, string): filter by buy currency
- `limit` (optional, integer): number of records per page
- `page` (optional, integer): page number

Key data to extract:
- `orders`: list of flash swap orders
- `order_id` (string): order identifier
- `sell_currency` / `buy_currency`: currencies involved
- `sell_amount` / `buy_amount`: amounts
- `price`: exchange rate
- `status`: order status (1=success, 2=failed)
- `create_time`: order creation time

### Step 5: Query Single Flash Swap Order Details (if intent = get_order)

Call `cex_fc_get_fc_order` with:
- `order_id` (required, string): the order ID to query

If the API returns a 404 error, the order does not exist. Inform the user that the specified order ID was not found, and suggest verifying the order ID or querying the order list first.

Key data to extract:
- `order_id` (string): order identifier
- `sell_currency` / `buy_currency`: currencies involved
- `sell_amount` / `buy_amount`: amounts
- `price`: exchange rate
- `status`: order status
- `create_time`: order creation time

### Step 6: Format and Present Results

Format the query results and present them to the user using the appropriate Report Template based on the intent.

Key data to extract:
- Formatted report based on the query type

## Error Handling

| Error Scenario | Handling |
|----------------|----------|
| MCP service connection failure | Prompt user to check network connection or VPN status, suggest retrying later |
| order_id not provided | Prompt user to provide an order ID, or guide them to use the order list query first |
| Empty query results | Clearly inform the user that no data was found, suggest adjusting filter conditions |
| Currency not supported for flash swap | Inform user that the specified currency is not available for flash swap |
| Currency not specified for limit check | Prompt user to specify a currency (e.g. BTC, ETH, USDT) before querying swap limits |
| Invalid status value | Status parameter only accepts `1` (success) or `2` (failed). Reject any other value before calling the API and inform the user of valid options |
| Order not found (404) | The specified `order_id` does not exist. Inform the user and suggest verifying the order ID or querying the order list first |
| Large result set (34,000+ rows) | Do not dump the entire list. Summarize total count, show a sample of 20 pairs, and suggest filtering by currency |
| Invalid parameter format | Prompt user with correct parameter format |

## Safety Rules

- This Skill only performs query operations; it does not execute any order placement or fund changes
- Must not expose user's API Key, Secret, or other sensitive information in output
- Amounts in query results should be displayed as-is without modification

## Judgment Logic Summary

| Condition | Action | Tool |
|-----------|--------|------|
| User asks which flash swap pairs are supported | Query all currency pairs | `cex_fc_list_fc_currency_pairs` |
| User asks if a specific currency can be swapped | Query pairs filtered by currency | `cex_fc_list_fc_currency_pairs` |
| User asks about min/max swap amounts or limits (currency specified) | Query pairs filtered by currency, extract limits | `cex_fc_list_fc_currency_pairs` |
| User asks about swap limits without specifying a currency | Prompt user to specify a currency before proceeding | — |
| User queries flash swap order history | Query order list | `cex_fc_list_fc_orders` |
| User provides invalid status value (not 1 or 2) | Reject and inform user that status only accepts 1 or 2 | — |
| User filters orders by status/currency | Query order list with conditions | `cex_fc_list_fc_orders` |
| User queries a specific order by ID | Query single order | `cex_fc_get_fc_order` |
| API returns 404 for order query | Inform user the order does not exist, suggest verifying the ID | — |
| Full pair list returns 34,000+ rows | Summarize count, show sample of 20, suggest currency filter | — |
| order_id missing when querying order details | Prompt user to provide order_id | — |

## Report Template

**Timestamp format**: All `{timestamp}` placeholders below use ISO 8601 format: `YYYY-MM-DD HH:mm:ss UTC` (e.g. `2026-03-11 14:30:00 UTC`). Use the current time when generating the report.

### Flash Swap Currency Pairs Report

```markdown
## Gate Flash Swap Supported Pairs

**Query Time**: {timestamp}
**Filter**: {currency filter or "None"}

| Pair | Sell Currency | Buy Currency |
|------|---------------|--------------|
| {pair} | {sell_currency} | {buy_currency} |

Total: {total} pairs.
```

### Flash Swap Currency Limit Report

```markdown
## Gate Flash Swap Limit Check

**Query Time**: {timestamp}
**Currency**: {currency}

| Pair | Sell Currency | Sell Min | Sell Max | Buy Currency | Buy Min | Buy Max |
|------|---------------|----------|----------|--------------|---------|---------|
| {pair} | {sell_currency} | {sell_min_amount} | {sell_max_amount} | {buy_currency} | {buy_min_amount} | {buy_max_amount} |

Total: {total} pairs available for {currency}.
```

### Flash Swap Order List Report

```markdown
## Gate Flash Swap Order List

**Query Time**: {timestamp}
**Filters**: Status={status}, Sell Currency={sell_currency}, Buy Currency={buy_currency}

| Order ID | Sell | Sell Amount | Buy | Buy Amount | Status | Created At |
|----------|------|-------------|-----|------------|--------|------------|
| {order_id} | {sell_currency} | {sell_amount} | {buy_currency} | {buy_amount} | {status_text} | {create_time} |

Total: {total} records.
```

### Flash Swap Order Detail Report

```markdown
## Gate Flash Swap Order Details

**Query Time**: {timestamp}

| Field | Value |
|-------|-------|
| Order ID | {order_id} |
| Sell Currency | {sell_currency} |
| Sell Amount | {sell_amount} |
| Buy Currency | {buy_currency} |
| Buy Amount | {buy_amount} |
| Exchange Rate | {price} |
| Order Status | {status_text} |
| Created At | {create_time} |
```
