# Gate TradFi Modify Position

Modify an existing TradFi position: **take-profit and/or stop-loss price only**. **Other fields (e.g. leverage, margin mode) are not supported** by `cex_tradfi_update_position`. Use only MCP-documented tool names and parameters.

## MCP tools and parameters

| Tool | Purpose | Parameters (declare per MCP) |
| -----| --------| -----------------------------|
| `cex_tradfi_update_position` | Modify position | Supports **take-profit price** and **stop-loss price** only. **Does not support leverage, margin mode, or other fields.** Required/optional from MCP: position identifier (symbol or position_id), and take-profit price and/or stop-loss price. Do not pass parameters not documented in the MCP. |

- **Conditions and limits**: Only existing positions can be modified. Value constraints for take-profit/stop-loss must follow MCP or API rules. **Do not pass or prompt for leverage, margin mode, or other fields** — the tool does not support them.
- **Position identification**: Use only the identifier the MCP documents. Current positions can be listed via `cex_tradfi_query_position_list`.

## Pre-execution confirmation

Before calling `cex_tradfi_update_position`: **output all parameters** that will be sent (e.g. symbol or position_id, take-profit price, stop-loss price). Ask the user to confirm. Do **not** call the tool until the user explicitly confirms.

---

## Workflow

1. Identify the position to modify (symbol or position_id from user or from `cex_tradfi_query_position_list`).
2. Determine what to change per user message: **take-profit price** and/or **stop-loss price** only. If the user asks to change leverage, margin mode, or anything else, tell them the tool only supports take-profit and stop-loss price.
3. Build parameter set using **only MCP-documented parameters**.
4. **Output the full parameter set to the user and ask for confirmation.** Do not call the tool until user confirms.
5. After confirmation, call `cex_tradfi_update_position`.
6. In the response: **explain the parameters that were used** and the outcome. Use the Report Template below.

## Report Template

After execution, include:

- **Parameters used**: What was sent (e.g. symbol/position_id, take-profit price, stop-loss price).
- **Result**: Success (position updated) or error code/message. If error, restate the sent parameters and suggest correction.

---

## Scenario 1: Set or change take-profit price

**Context**: User wants to set or change the take-profit price for an open position.

**Prompt Examples**:
- "Set take-profit to 1.08 for my EURUSD position"
- "Modify position EURUSD take-profit 1.08"
- "Change take-profit to 1.08"

**Expected Behavior**:
1. Resolve position (symbol or position_id). Build params: position identifier, take-profit price. Output for confirmation.
2. After confirmation, call `cex_tradfi_update_position`.
3. Respond with parameters used and result.

**Response Template**:
```
Parameters sent:
| Symbol | Take-profit price |
| EURUSD | 1.08              |

Result: Position modified. Take-profit set to 1.08.
```

---

## Scenario 2: Set or change stop-loss price

**Context**: User wants to set or change the stop-loss price for an open position.

**Prompt Examples**:
- "Set stop-loss to 1.03 for EURUSD"
- "Modify position stop-loss 1.03"
- "Change stop-loss to 1.03"

**Expected Behavior**:
1. Resolve position. Build params: position identifier, stop-loss price. Output for confirmation.
2. After confirmation, call `cex_tradfi_update_position`.
3. Respond with parameters used and result.

---

## Scenario 3: Set or change both take-profit and stop-loss

**Context**: User wants to set or change both take-profit and stop-loss for a position.

**Prompt Examples**:
- "Set take-profit 1.08 and stop-loss 1.03 for EURUSD"
- "Modify position EURUSD take-profit 1.08 stop-loss 1.03"

**Expected Behavior**:
1. Build params: position identifier, take-profit price, stop-loss price. Output for confirmation.
2. After confirmation, call `cex_tradfi_update_position`.
3. Respond with parameters used and result.

**Note**: If the user asks to change **leverage**, **margin mode**, or any other field, reply that `cex_tradfi_update_position` only supports take-profit and stop-loss price; other modifications are not supported.
