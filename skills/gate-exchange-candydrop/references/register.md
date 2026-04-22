# Gate CandyDrop Register — Activity Registration

Register for CandyDrop activities.

## MCP tool and parameters

| Tool | Purpose | Required | Optional |
|------|---------|----------|----------|
| **cex_launch_register_candy_drop_v4** | Register for a CandyDrop activity | `currency` | `activity_id` |

- **cex_launch_register_candy_drop_v4**: Requires API Key authentication. State-changing write operation.
- `currency`: Token/project name (e.g. "USDT"). **Required** — the API will auto-match the nearest active activity for this token.
- `activity_id`: Activity ID. Optional — can be used together with `currency` for precise targeting.

**API request fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| currency | string | Yes | Token/project name |
| activity_id | integer | No | Activity ID (optional, used with currency) |

**API response:**

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the registration was successful |

**API error labels:**

| label | Description |
|-------|-------------|
| INVALID_PARAM_VALUE | Invalid request parameters (e.g. missing currency, invalid activity_id) |
| SERVER_ERROR | System error or activity not found |
| currency is required | Currency parameter is missing |
| Activity not found | No matching activity found for the given currency/activity_id |
| Device token is required | Registration requires device token (try from Gate app or website) |

---

## Workflow

1. **Parse parameters**: Extract `currency` (required) and optional `activity_id` from user query.
2. **Validate**: If `currency` is missing, ask the user to provide it.
3. **Optional pre-check**: Call `cex_launch_get_candy_drop_activity_rules_v4` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) to verify the activity exists and show details.
4. **Show preview**: Display registration preview with currency and activity ID (if known). Ask user to confirm.
5. **Wait for confirmation**: User must reply "confirm" to proceed or "cancel" to abort.
6. **Execute registration**: Call `cex_launch_register_candy_drop_v4` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with `currency` and optional `activity_id`.
7. **Format response**: Show success or failure message.

## Report Template

Show a preview first, then the confirmation result. Include currency and activity details.

---

## Scenario 1: Normal registration with confirmation

**Context**: User wants to register for a CandyDrop activity. The full Preview → Confirm flow is required.

**Prompt Examples**:
- "Register for CandyDrop USDT"
- "I want to register for the USDT CandyDrop activity"
- "Help me join the BTC CandyDrop"
- "Register for this candydrop activity"

**Expected Behavior**:
1. Extract: `currency` (e.g. "USDT"), optional `activity_id`.
2. If `currency` is missing, ask the user to provide it.
3. Optionally call `cex_launch_get_candy_drop_activity_rules_v4` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) to verify the activity.
4. Display registration preview and ask for confirmation.
5. On "confirm": call `cex_launch_register_candy_drop_v4` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with `currency` and optional `activity_id`.
6. Display success or error with API error label.

**Response Template**:
```
CandyDrop Registration Preview

Token: {currency}
Activity ID: {activity_id or "auto-matched by currency"}

Please reply "confirm" to proceed or "cancel" to abort.

---
(After confirmation)
Registration successful! You have registered for the {currency} CandyDrop activity. Complete the required tasks to earn rewards.
```

---

## Scenario 2: Missing parameters — clarification needed

**Context**: User expresses intent to register but does not provide the required `currency`.

**Prompt Examples**:
- "I want to join CandyDrop"
- "I want to register for a candydrop activity"
- "Help me register"

**Expected Behavior**:
1. Detect incomplete request (missing `currency`).
2. Ask the user to provide the token name.
3. Optionally suggest browsing activities first.

**Response Template**:
```
I'd like to help you register for CandyDrop! I need to know which token activity you want to join.

Please provide the token name (e.g. "USDT", "BTC", "GT").

You can also say "Show all CandyDrop activities" to browse available options first.
```
