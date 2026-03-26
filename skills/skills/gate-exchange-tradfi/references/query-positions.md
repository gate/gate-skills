# Query TradFi Positions — Workflow and Scenarios

Read-only: list current positions and position history. **Pass only parameters documented in the MCP for each tool.** No open/close or modify.

## Workflow

### Step 1: Identify query type

- **Current positions**: User wants live positions (e.g. "my positions", "current holdings").
- **Position history**: User wants past positions or settlements (e.g. "position history", "past holdings").

### Step 2: Call tools

- **Current positions**: Call `cex_tradfi_query_position_list` with only MCP-documented parameters. Extract: symbol, side, size, entry price, margin, PnL if available, etc.
- **Position history**: Call `cex_tradfi_query_position_history_list` with only MCP-documented parameters (e.g. limit or time range only if defined in the MCP). Extract: same fields plus close time / settlement info.

### Step 3: Format response

Use the Report Template below. If the list is empty, report "No open positions" or "No position history" as applicable.

## Report Template

**Current positions**

| Symbol | Side | Size | Entry | Margin | Unrealized PnL | Mode |
|--------|------|------|-------|--------|----------------|------|
| ...    | ...  | ...  | ...   | ...    | ...            | ...  |

**Position history**

| Symbol | Side | Size | Entry | Close / Settle Time | Realized PnL |
|----------------|------|------|-------|---------------------|--------------|
| ...            | ...  | ...  | ...   | ...                 | ...          |

---

## Scenario 1: List current positions

**Context**: User wants to see all current TradFi positions.

**Prompt Examples**:
- "My TradFi positions"
- "Current holdings"
- "What am I holding"
- "Show my positions"

**Expected Behavior**:
1. Call `cex_tradfi_query_position_list`.
2. Format result as current-positions table.
3. If empty, reply "No open positions."

---

## Scenario 2: Position history

**Context**: User wants to see historical positions or closed positions.

**Prompt Examples**:
- "Position history"
- "My past positions"
- "Closed positions"

**Expected Behavior**:
1. Call `cex_tradfi_query_position_history_list` with only the parameters documented in the MCP.
2. Format as position history table.
3. If empty, reply "No position history."
