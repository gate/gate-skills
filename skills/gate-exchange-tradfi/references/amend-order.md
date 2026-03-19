# Gate TradFi Amend Order

Amend an existing TradFi order: **price** and/or **take-profit / stop-loss price** only. **Size is not supported** by `cex_tradfi_update_order`. Use only MCP-documented tool names and parameters.

## MCP tools and parameters

| Tool | Purpose | Parameters (declare per MCP) |
| -----| --------| -----------------------------|
| `cex_tradfi_update_order` | Amend one order | Supports **price** and **take-profit / stop-loss price** only. **Does not support changing size.** Required/optional from MCP: order_id, and at least one of new price, take-profit price, stop-loss price. Do not pass size or parameters not documented in the MCP. |

- **Conditions and limits**: Only open orders can be amended. Value constraints (price step, etc.) must follow MCP or API rules. **Do not pass or prompt for size** — the tool does not support it.
- **Order id source**: The order id for `cex_tradfi_update_order` **must** come from **`cex_tradfi_query_order_list`** (the open order list). **Do not use** the `id` or `log_id` returned by `cex_tradfi_create_tradfi_order` — those cannot be used for amend. Resolve from `cex_tradfi_query_order_list` if user refers to order by position or description.

## Pre-execution confirmation

Before calling `cex_tradfi_update_order`: **output all parameters** that will be sent (e.g. order_id, new price, take-profit price, stop-loss price). Show before/after if available. Ask the user to confirm. Do **not** call the tool until the user explicitly confirms.

---

## Workflow

1. Identify the order to amend (from user-provided order_id or by listing open orders and letting user choose).
2. Determine what to change per user message: **price** and/or **take-profit price** and/or **stop-loss price** only. If the user asks to change size, tell them the tool does not support changing size.
3. Build parameter set using **only MCP-documented parameters** (no size).
4. **Output the full parameter set (and before/after) to the user and ask for confirmation.** Do not call the tool until user confirms.
5. After confirmation, call `cex_tradfi_update_order`.
6. In the response: **explain the parameters that were used** and the outcome (success or error). Use the Report Template below.

## Report Template

After execution, include:

- **Parameters used**: What was sent (e.g. order_id, new price, take-profit, stop-loss).
- **Result**: Success (updated order state) or error code/message. If error, restate the sent parameters and suggest correction.

---

## Scenario 1: Amend price

**Context**: User wants to change the limit price of an open order.

**Prompt Examples**:
- "Amend order 12345 price to 1.0600"
- "Change order price to 1.06"
- "Update my EURUSD order price to 1.0600"

**Expected Behavior**:
1. Resolve order (by order_id or from list). Get current price.
2. Build params: order_id, new price. Output for confirmation.
3. After confirmation, call `cex_tradfi_update_order`.
4. Respond with parameters used and result.

**Response Template**:
```
Parameters sent:
| Order ID | New price |
| 12345    | 1.0600    |

Result: Order amended. Price updated to 1.0600.
```

---

## Scenario 2: Amend take-profit or stop-loss price

**Context**: User wants to change take-profit and/or stop-loss price for an open order.

**Prompt Examples**:
- "Amend order 12345 take-profit to 1.07"
- "Change stop-loss to 1.04 for order 12345"
- "Update order 12345 take-profit 1.07 stop-loss 1.04"

**Expected Behavior**:
1. Resolve order. Build params: order_id, and take-profit price and/or stop-loss price (per MCP). Output for confirmation.
2. After confirmation, call `cex_tradfi_update_order`.
3. Respond with parameters used and result.

**Note**: If the user asks to change **size**, reply that `cex_tradfi_update_order` does not support changing size; only price and take-profit/stop-loss price can be amended.
