# Gate TradFi Close Position

Close a TradFi position (full or partial). Use only MCP-documented tool names and parameters. **Full close (全部平仓): do not pass size or close_volume** — the tool closes the entire position without that parameter. For partial close, pass close size/close_volume per MCP.

## MCP tools and parameters

| Tool | Purpose | Parameters (declare per MCP) |
| -----| --------| -----------------------------|
| `cex_tradfi_close_position` | Close position | **Full close**: position identifier (symbol or position_id) only; **do not pass size or close_volume**. **Partial close**: position identifier and close size/close_volume (per MCP). Do not pass parameters not documented in the MCP. |

- **Full close**: **Do not pass size or close_volume**; the tool closes the whole position. Use only position identifier (e.g. symbol or position_id).
- **Partial close**: Pass close size or close_volume per MCP; it must not exceed current position size. Value constraints (size step, min/max) must follow MCP or API rules.
- **Position identification**: Use only the identifier the MCP documents. Current positions from `cex_tradfi_query_position_list`.

## Pre-execution confirmation

Before calling `cex_tradfi_close_position`: **output all parameters** that will be sent (e.g. symbol for full close, or symbol + close size for partial). Ask the user to confirm. Do **not** call the tool until the user explicitly confirms.

---

## Workflow

1. Identify the position to close (symbol or position_id from user or from `cex_tradfi_query_position_list`).
2. **Full close**: Build params with position identifier only; **do not pass size or close_volume**. **Partial close**: Determine close size (e.g. user says "close half" or "close 0.05"); validate against current position and MCP; pass close size/close_volume per MCP.
3. Build parameter set using **only MCP-documented parameters**.
4. **Output the full parameter set to the user and ask for confirmation.** Do not call the tool until user confirms.
5. After confirmation, call `cex_tradfi_close_position`.
6. In the response: **explain the parameters that were used** and the outcome (e.g. closed size, realized PnL if returned). Use the Report Template below.

## Report Template

After execution, include:

- **Parameters used**: What was sent (e.g. symbol only for full close; symbol + close size for partial).
- **Result**: Success (position closed or reduced; realized PnL if available) or error code/message. If error, restate the sent parameters and suggest correction.

---

## Scenario 1: Full close (全部平仓)

**Context**: User wants to close the entire position for a symbol. **Do not pass size or close_volume** — full close uses position identifier only.

**Prompt Examples**:
- "Close EURUSD position"
- "Close all EURUSD"
- "Flat EURUSD"
- "Close my EURUSD"

**Expected Behavior**:
1. Resolve position (e.g. via `cex_tradfi_query_position_list`). Confirm it exists.
2. Build params: **position identifier (symbol or position_id) only**; do **not** pass size or close_volume. Output for confirmation.
3. After confirmation, call `cex_tradfi_close_position`.
4. Respond with parameters used and result.

**Response Template**:
```
Parameters sent:
| Symbol  | (full close — no size/close_volume) |
| EURUSD  | —                                  |

Result: Position closed. Realised PnL: … (if returned by MCP).
```

---

## Scenario 2: Partial close

**Context**: User wants to close part of the position. Pass close size or close_volume per MCP.

**Prompt Examples**:
- "Close 0.05 EURUSD"
- "Close half of my EURUSD position"
- "Reduce EURUSD by 0.05"

**Expected Behavior**:
1. Resolve position and current size. Compute close size (e.g. half or user-specified amount). Validate against position size and MCP limits.
2. Build params: position identifier and **close size/close_volume** (per MCP). Output for confirmation.
3. After confirmation, call `cex_tradfi_close_position`.
4. Respond with parameters used and result (remaining position if available).
