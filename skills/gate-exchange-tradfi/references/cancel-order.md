# Gate TradFi Cancel Order

Cancel one TradFi order per call. Use only MCP-documented tool names and parameters. **Only one tool: `cex_tradfi_delete_order`; it does not support batch** — one order per call. To cancel multiple orders, call it once for each order. Declare conditions and limits from the MCP here.

## MCP tools and parameters

| Tool | Purpose | Parameters (declare per MCP) |
| -----| --------| -----------------------------|
| `cex_tradfi_delete_order` | Cancel/delete one order | Required: order identifier (order_id). Use only parameters documented in the MCP. Does not support batch. |

- **Order id source**: The order id for `cex_tradfi_delete_order` **must** come from **`cex_tradfi_query_order_list`** (the open order list). **Do not use** the `id` or `log_id` returned by `cex_tradfi_create_tradfi_order` — those cannot be used as the cancel/delete parameter. If the user wants to cancel an order they just placed, call `cex_tradfi_query_order_list` first and use the order id from that response.
- **Conditions and limits**: Only open orders can be cancelled. **Multiple orders**: call `cex_tradfi_delete_order` once per order.

## Pre-execution confirmation

Before calling `cex_tradfi_delete_order`: **output what will be cancelled** (e.g. order_id). Ask the user to confirm. Do **not** call the tool until the user explicitly confirms.

---

## Workflow

1. Identify the order to cancel: by order_id from user, or list open orders and let user choose one (by number).
2. Build parameter set using **only MCP-documented parameters**.
3. **Output the target (order_id) to the user and ask for confirmation.** Do not call the tool until user confirms.
4. After confirmation, call `cex_tradfi_delete_order` with the order_id. For more than one order, repeat (one call per order).
5. In the response: **explain what was cancelled** (parameters sent) and the outcome. Use the Report Template below.

## Report Template

After execution, include:

- **Parameters used**: What was sent (e.g. order_id for each call).
- **Result**: Success (cancelled) or error code/message. If error, restate the sent parameters and suggest correction.

---

## Scenario 1: Cancel by order_id

**Context**: User provides an order identifier to cancel.

**Prompt Examples**:
- "Cancel order 12345"
- "Revoke order 12345"
- "Cancel my order 12345"

**Expected Behavior**:
1. Parse order_id. Output it for confirmation.
2. After confirmation, call `cex_tradfi_delete_order` with order_id.
3. Respond with parameters used and result.

**Response Template**:
```
Parameters sent:
| Order ID |
| 12345    |

Result: Order cancelled.
```

---

## Scenario 2: List orders then cancel

**Context**: User wants to cancel but does not know order_id; list open orders first.

**Prompt Examples**:
- "Cancel my order"
- "Show my orders" (then user selects which to cancel)

**Expected Behavior**:
1. Call `cex_tradfi_query_order_list` (with only MCP-documented params).
2. Show order list with numbered options. User selects one by number.
3. Map selection to order_id. Output for confirmation.
4. After confirmation, call `cex_tradfi_delete_order` with that order_id.
5. Respond with parameters used and result.
