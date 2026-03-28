---
name: gate-exchange-activitycenter
version: "2026.3.23-1"
updated: "2026-03-23"
description: "Activity center for platform campaigns. Use this skill whenever the user asks about platform activities, activity recommendations, or my activities. Trigger phrases include: recommend activities, what activities, airdrop activities, trading competition, VIP activities, my activities. MCP tools: cex_activity_list_activity_types, cex_activity_list_activities, cex_activity_get_my_activity_entry."
---

# gate-exchange-activitycenter

> Activity center aggregates platform campaigns (trading competitions, airdrops, newcomer activities, referral activities, etc.), supporting activity recommendations and my activities entry.

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

**Trigger Scenarios**: User mentions "recommend activities", "what activities", "airdrop activities", "trading competition", "VIP activities", "my activities", etc.

> ⚠️ **MANDATORY RESPONSE FORMAT**: When this skill is triggered, AI responses **MUST** strictly follow the Response Templates defined in this document. Free-form responses are **FORBIDDEN**.

---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate (main) | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- cex_activity_get_my_activity_entry
- cex_activity_list_activities
- cex_activity_list_activity_types

### Authentication
- API Key Required: Yes (see skill doc/runtime MCP deployment)
- Permissions: Activity:Read
- Get API Key: https://www.gate.io/myaccount/profile/api-key/manage

### Installation Check
- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## Routing Rules

| User Intent | Keywords/Pattern | Action |
|-------------|-----------------|--------|
| Hot Recommendation | "recommend activities" "what activities" "recent activities" | Scenario 1.1 Hot Recommendation |
| Type-Based Recommendation | "airdrop activities" "trading competition" "VIP activities" "earn activities" | Scenario 1.2 Type-Based |
| Scenario-Based Recommendation | "I have GT" "futures activities" "spot activities" | Scenario 1.3 Scenario-Based |
| Search by Name | "{activity name}" "position airdrop" | Scenario 1.4 Search by Name |
| My Activities | "what activities I joined" "my activities" "enrolled activities" | Scenario 2 My Activities |
| Welfare Center/Newcomer Tasks | "claim rewards" "check-in" "newcomer tasks" | ❌ NOT applicable to this skill |

---

## MCP Tools

| MCP Tool | Purpose | action_type |
|----------|---------|-------------|
| `cex_activity_list_activity_types` | Get activity type list (id, name) for type filtering | query |
| `cex_activity_list_activities` | Query activities by hot/type/scenario/keywords | info-card |
| `cex_activity_get_my_activity_entry` | Get "My Activities" entry card | info-card |

### API Parameter Constraints

| Parameter | Constraint | Description |
|-----------|------------|-------------|
| `page_size` | **MUST be ≤ 3** | ⚠️ **HARD LIMIT**: Each request MUST NOT exceed 3 activities. Always set `page_size=3` or less. |
| `page` | Integer | Page number, default 1. |
| `recommend_type` | `hot` / `type` / `scenario` | Query mode: hot (popular), type (by type_ids), scenario (by keywords) |
| `type_ids` | String | Activity type IDs, comma-separated. Used with `recommend_type=type` |
| `keywords` | String | Search keywords for activity name. Used with `recommend_type=scenario` |

> ⚠️ **CRITICAL**: The `page_size` parameter is strictly limited to a maximum of 3. Any value greater than 3 is FORBIDDEN.

---

## Scenario 1: Activity Recommendation

### 1.1 Hot Recommendation (No Type Specified)

**Trigger**: "recommend activities" "what activities" "recent activities"

**API Call**:
```
cex_activity_list_activities?recommend_type=hot&sort_by=default&page=1&page_size=3
```

**Rules**:
- ✅ Do NOT ask for type clarification, call API directly
- ✅ Fixed `page_size=3` (maximum allowed), no pagination

---

### 1.2 Type-Based Recommendation

**Trigger**: "airdrop activities" "trading competition" "VIP activities" "earn activities"

**API Call Sequence**:
1. `cex_activity_list_activity_types` → Get type list, match user's type name (case-insensitive)
2. `cex_activity_list_activities?recommend_type=type&type_ids=matched_id1,matched_id2&sort_by=time&page_size=3`

**Keyword Extraction Examples**:
- "what airdrop activities are there" → Extract: airdrop
- "VIP activities" → Extract: VIP
- "I'm a VIP, any exclusive activities" → Extract: VIP
- "any low-risk activities" → Extract: earn

---

### 1.3 Scenario-Based Recommendation

**Trigger**: "I have GT, what activities can I join" "futures activities"

**API Call**:
- If mappable to type: Use `recommend_type=type` with `type_ids`
- If scenario/asset: Use `recommend_type=scenario` with `keywords`

```
cex_activity_list_activities?recommend_type=scenario&keywords=GT&page_size=3
```

---

### 1.4 Search by Name

**Trigger**: "help me find position airdrop" "where is VIP exclusive activity" "find test activity"

**API Call**:
```
cex_activity_list_activities?recommend_type=scenario&keywords=test_activity&page=1&page_size=3
```

**Parameter Notes**:
- Use `recommend_type=scenario` with `keywords` for name search
- `keywords` is the activity name or partial name to search
- ⚠️ **Language Conversion**: If user input contains non-English text, translate keywords to English before passing to the `keywords` parameter

**Response Template** (when results found):
> Based on your keywords, I found some possible activities. If you didn't find the activity you're looking for, you can provide a more complete activity name, or click more activities to explore more hot activities.

---

## Scenario 2: My Activities

**Trigger**: "what activities I joined" "my activities" "enrolled activities"

**API Call**:
```
cex_activity_get_my_activity_entry
```

**Rules**:
- ✅ Only show entry card, guide user to click and jump
- ✅ Apply URL Processing Rules (see above) to the `url` field
- ❌ Do NOT filter activity list in this API

---

## Decision Logic

| Condition | Action |
|-----------|--------|
| User asks for hot/recommended activities | Call `cex_activity_list_activities` with `recommend_type=hot` directly |
| User specifies activity type | First call `cex_activity_list_activity_types`, then `cex_activity_list_activities` with `recommend_type=type&type_ids=xxx` |
| User mentions asset/scenario (GT, futures) | Use `recommend_type=scenario` with `keywords` |
| User searches by activity name | Use `recommend_type=scenario` with `keywords={activity_name}` |
| User asks "my activities" | Call `cex_activity_get_my_activity_entry` |
| Activity list returns empty | Use "No Results" template, do NOT use "filtered for you..." |

---

## URL Processing Rules

All activity URLs returned by API must be processed before displaying to users:

| URL Pattern | Processing | Example |
|-------------|------------|---------|
| Relative path (starts with `/`) | Prepend `https://www.gate.com` | `/competition/xxx` → `https://www.gate.com/competition/xxx` |
| Already has host (starts with `http://` or `https://`) | Keep as-is, no modification | `https://www.gate.com/campaigns/xxx` → `https://www.gate.com/campaigns/xxx` |

**Why relative paths?** API returns relative paths for flexibility:
- Multi-language support: Frontend can dynamically add language prefix (`/zh/`, `/en/`, `/ja/`)
- Multi-environment deployment: Different domains for test/staging/production
- Client flexibility: Web, App, H5 can handle links differently

**Display Format**: Always use clickable Markdown link: `[{activity_title}]({processed_url})`

---

## Activity Response Field Specification

For all activity recommendation scenarios (1.1, 1.2, 1.3, 1.4), the response MUST only include the following fields:

| API Field | Display Label | Processing Rule |
|-----------|---------------|-----------------|
| `master_one_line` | Activity Title | Display as-is |
| `url` | Activity Link | Apply URL Processing Rules (prepend `https://www.gate.com` for relative paths) |
| `type_name` | Activity Type | Display the `type_name` value directly (NOT `type_id`) |

**Response Format Example**:

| Activity Title | Activity Type | Activity Link |
|----------------|---------------|---------------|
| Traditional Assets Limited Edition Event | Traditional Assets | [View Details](https://www.gate.com/campaigns/cheney_alpha152) |

**Rules**:
- ✅ Only display the 3 fields listed above
- ✅ Use `type_name` for activity type (NOT `type_id`)
- ✅ Process URLs according to URL Processing Rules
- ❌ Do NOT display other fields like `id`, `type_id`, `hot`, `img`, `competition_name`, `start_at`, `end_at`, etc.

---

## Response Templates

> ⚠️ **MANDATORY**: AI responses **MUST** strictly follow these templates. Free-form or custom responses are **FORBIDDEN**.

### Template Compliance Rules

1. **REQUIRED**: Every response MUST use the exact template structure defined below
2. **REQUIRED**: Include the intro text + activity table + follow-up prompt
3. **FORBIDDEN**: Adding extra commentary, explanations, or custom formatting
4. **FORBIDDEN**: Omitting any part of the template structure

### Activity Recommendation (Has Results)

| Scenario | Intro Text (MUST use exactly) |
|----------|-------------------------------|
| Hot (1.1) | Here are the current hot activities: |
| By Type (1.2) | Filtered [type] activities for you: |
| By Scenario (1.3) | Filtered activities related to [scenario/asset] for you: |
| By Name (1.4) | Based on your keywords, I found some possible activities: |

**Required Response Structure**:
```
{Intro Text from table above}

| Activity Title | Activity Type | Activity Link |
|----------------|---------------|---------------|
| {master_one_line} | {type_name} | [View Details]({processed_url}) |
| ... | ... | ... |

{Follow-up Prompt - see below}
```

**Follow-up Prompts by Scenario**:
| Scenario | Follow-up Prompt (MUST include) |
|----------|--------------------------------|
| Hot (1.1) | Click the link to view details or sign up. Need activities of a specific type? |
| By Type (1.2) | Click the link to view details and how to participate. |
| By Scenario (1.3) | Click the link to view participation requirements and rewards. |
| By Name (1.4) | If you didn't find what you're looking for, provide a more complete activity name. |

### My Activities Template (Scenario 2)

**Required Response Structure**:
```
Click [My Events]({processed_url}) to view your enrolled and ongoing activities.

In "My Events" you can:
- View activity progress
- Claim activity rewards
- Track activity status
```

### No Results Template

**Required Response Structure**:
```
Currently no [type/keyword] activities are in progress. You can:
- Check the activity center regularly, new activities will be displayed as soon as they launch
- Tell me other activity types you're interested in (e.g., trading, earn, VIP exclusive), and I can filter for you
```

---

## Error Handling

| Error Type | Response Template |
|------------|-------------------|
| API timeout/failure | Unable to load activities at the moment, please try again later. |
| No matching activities | Use "No Results" template |
| 401 Unauthorized | Session expired, please log in again to view activities. |
| 400 Bad Request | Unable to process your request. Please try a different search term. |
| 429 Rate Limited | Too many requests. Please wait a moment and try again. |
| 500 Server Error | Service temporarily unavailable. Please try again later. |
| Network Error | Network connection issue. Please check your connection and try again. |

---

## Safety Rules

1. **No investment advice**: Activity rewards are platform benefits, not investment guidance
2. **No data fabrication**: Only show data returned by backend
3. **Compliance check**: Do not show activities unavailable in user's region
4. **No internal exposure**: Never mention technical details to users, including:
   - API names (e.g., `cex_activity_list_activities`)
   - Parameter names (e.g., `recommend_type`, `type_ids`)
   - Internal IDs (e.g., `type_id=34`, `id=1499`)
   - Error codes or technical error messages
   - Example of **BAD** response: "No Alpha type activities found (type_id=34)"
   - Example of **GOOD** response: "Currently no Alpha activities are in progress"

---

## Data Integrity Rules

> ⚠️ **MANDATORY**: These rules MUST be followed for ALL data processing and display.

### 1. Never Guess Data
- ❌ **FORBIDDEN**: Guessing, estimating, or fabricating any data values
- ❌ **FORBIDDEN**: Making assumptions about timestamps, numbers, or any computed values
- ✅ **REQUIRED**: Only display data exactly as returned by API
- ✅ **REQUIRED**: If data is missing or unclear, state "Data unavailable" instead of guessing

### 2. Self-Verification Mechanism
Before displaying any processed data, perform self-check:

| Data Type | Verification Method |
|-----------|---------------------|
| Timestamps | Verify conversion result is reasonable (year, month, day within expected range) |
| URLs | Verify URL format is valid after processing |
| Numbers | Verify numeric values match API response exactly |
| Type names | Verify `type_name` exists in API response, do NOT derive from `type_id` |

### 3. Proactive Validation (Not Reactive Correction)
- ✅ **REQUIRED**: Validate data BEFORE presenting to user
- ✅ **REQUIRED**: Double-check time-sensitive information (timestamps, dates)
- ❌ **FORBIDDEN**: Wait for user to point out errors
- ❌ **FORBIDDEN**: Display data first and correct later

### 4. Error Handling for Data Issues
If data validation fails:
1. Do NOT display the problematic data
2. Show a safe fallback message: "Some data is temporarily unavailable"
3. Log the issue internally (do NOT expose to user)

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "I want to buy crypto" | Trading skill |
| "I want to stake" | Launchpool/Earn skill |
| "Welfare center" "check-in" | Welfare center skill (NOT this skill) |

---

## Additional References

For detailed scenarios and examples, see `references/scenarios.md`
