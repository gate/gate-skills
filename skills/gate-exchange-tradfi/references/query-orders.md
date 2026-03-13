# Query TradFi Orders — Workflow and Scenarios

Read-only: list order list and order history. No create/cancel/amend. **Use only parameters documented in the Gate TradFi MCP for each tool; do not pass unsupported parameters.**

## Workflow

### Step 1: Identify query type

- **Order list (open orders)**: User wants current open orders (e.g. "my open orders", "list orders").
- **Order history**: User wants past orders (e.g. "order history", "recent filled/cancelled orders").

### Step 2: Call tools

- **Order list (open orders)**: Call `cex_tradfi_query_order_list` with only the parameters defined in the MCP for this tool. Extract: symbol, side, size, price, status, time, and other fields as returned.
- **Order history**: Call `cex_tradfi_query_order_history_list` with only the parameters defined in the MCP for this tool. Extract: same fields; indicate filled/cancelled where available.

### Step 3: Format response

Use the Report Template below. If the list is empty, report "No open orders" or "No orders in history" as applicable.

## Report Template

**Order list / Open orders**


| Symbol | Side | Size | Price | Status | Time (UTC) |
| ------ | ---- | ---- | ----- | ------ | ---------- |
| ...    | ...  | ...  | ...   | ...    | ...        |


**Order history**


| Symbol | Side | Size | Price | Filled | Status | Time |
| ------ | ---- | ---- | ----- | ------ | ------ | ---- |
| ...    | ...  | ...  | ...   | ...    | ...    | ...  |


---

## Scenario 1: List open orders

**Context**: User wants to see current open TradFi orders.

**Prompt Examples**:

- "Show my TradFi open orders"
- "List my orders"
- "What orders do I have open"

**Expected Behavior**:

1. Call `cex_tradfi_query_order_list` with only the parameters supported by the MCP for this tool.
2. Format result as order list table.
3. If empty, reply "No open orders."

---

## Scenario 2: Order history

**Context**: User wants to see past orders (filled or cancelled).

**Prompt Examples**:

- "TradFi order history"
- "My recent orders"
- "Show filled orders"

**Expected Behavior**:

1. Call `cex_tradfi_query_order_history_list` with only the parameters documented in the MCP for this tool.
2. Format as order history table.
3. If empty, reply "No orders in history."

