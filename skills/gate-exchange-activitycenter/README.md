# gate-exchange-activitycenter

## Overview

Activity center aggregation platform for Gate Exchange campaigns. **Step 1**: Identify user intent (hot/type/scenario/name recommendation or my activities). **Step 2**: Call appropriate API (`cex_activity_list_activities` for recommendations, `cex_activity_get_my_activity_entry` for my activities). **Step 3**: Return activity cards. Use when user asks about platform activities, activity recommendations, or my activities. Read-only.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Hot Recommendation** | Recommend popular activities without type specification | "recommend activities" / "what activities" |
| **Type-Based Recommendation** | Filter activities by type (airdrop, trading competition, VIP) | "airdrop activities" / "trading competition" |
| **Scenario-Based Recommendation** | Find activities by asset or scenario | "I have GT, what activities can I join" |
| **Search by Name** | Find specific activity by name/keywords | "help me find position airdrop" |
| **My Activities** | Show entry to user's enrolled activities | "my activities" / "what activities I joined" |

### Routing

| User Intent | Action |
|-------------|--------|
| Activity recommendation (hot/type/scenario/name) | Execute Scenario 1.x |
| My activities | Execute Scenario 2 |
| Welfare center / Daily check-in | Route to welfare skill (NOT this skill) |

## Architecture

- **Input**: User intent (recommendation type, activity type, keywords)
- **Tools**: 
  - `cex_activity_list_activity_types` — Get type list for filtering
  - `cex_activity_list_activities` — Query activities by hot/type/scenario/keywords
  - `cex_activity_get_my_activity_entry` — Get "My Activities" entry
- **Output**: Activity cards. **Decision Logic** (type matching), **Error Handling**, **Safety** (no investment advice) — see SKILL.md.

### Key Rules

1. **Fixed page_size=3**: All activity list queries use `page_size=3`, no pagination
2. **No Type Clarification**: For hot recommendation, call API directly without asking user
3. **Type Matching**: Case-insensitive matching for activity types

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
