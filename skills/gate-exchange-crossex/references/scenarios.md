# Gate CrossEx Trading Suite - Scenarios & Prompt Examples

## Scenario 1: Order Management Request

**Context**: User wants to query orders (open orders, order details, or order history).

**Prompt Examples**:
- "Show all my open orders"
- "Find my transactions in the last 90 days"

**Expected Behavior**:
1. Identify the intent as order management and route to `references/order-management.md`.
2. Extract order ID, symbol, status filter, or time range for query.


## Scenario 2: Position Query Request

**Context**: User wants to view current positions, filtered positions, or position-related risk information.

**Prompt Examples**:
- "Show all my positions"
- "Query my futures positions"
- "Do I have any margin positions open?"

**Expected Behavior**:
1. Identify the intent as position query and route to `references/position-query.md`.
2. Extract position type, exchange, symbol, and any filtering scope.
3. Query the relevant current position data, leverage, or risk-related fields.
4. Format the result clearly, highlighting symbol, direction, size, entry price, and unrealized PnL when available.
5. Return the requested position summary and surface any notable risk warnings if relevant.

## Scenario 3: History Query Request

**Context**: User wants to query historical orders, trades, positions, ledger entries, or interest records.

**Prompt Examples**:
- "Show my trade history"
- "Query BTC order history for the last 7 days"
- "Check my margin interest history"

**Expected Behavior**:
1. Identify the intent as history query and route to `references/history-query.md`.
2. Extract history type, symbol, exchange, time range, pagination inputs, and any filters.
3. Validate the requested time range and determine the appropriate history endpoint.
4. Query the historical records and organize them in reverse chronological order.
5. Return a concise history summary with key fields such as time, symbol, side, size, price, and status where applicable.
