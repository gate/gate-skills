# gate-exchange-activitycenter — Scenarios & Prompt Examples

## Scenario 1.1: Hot Recommendation

**Context**: User asks for popular or recommended activities without specifying type.

**Prompt Examples**:
- "Recommend some activities"
- "What activities are available"
- "Any hot activities recently"

**Expected Behavior**:
1. Call `cex_activity_list_activities?recommend_type=hot&sort_by=default&page=1&page_size=3`
2. Output: Activity cards with brief intro "Here are the current hot activities. Click the card to view details or sign up."

---

## Scenario 1.2: Type-Based Recommendation

**Context**: User asks for activities of a specific type.

**Prompt Examples**:
- "Any airdrop activities"
- "What trading competitions are there"
- "VIP activities"
- "I'm a VIP, any exclusive activities"

**Expected Behavior**:
1. Call `cex_activity_list_activity_types` to get type list
2. Match user's type name (case-insensitive): "airdrop" -> type_id, "VIP" -> type_id
3. Call `cex_activity_list_activities?recommend_type=type&type_ids=[matched_ids]&sort_by=time&page_size=3`
4. Output: Activity cards with "Filtered [type] activities for you. Click the card to view details and how to participate."

---

## Scenario 1.3: Scenario-Based Recommendation

**Context**: User asks for activities based on asset or behavior.

**Prompt Examples**:
- "I have GT, what activities can I join"
- "I often trade futures, any activities for me"
- "Any activities for spot trading"

**Expected Behavior**:
1. Extract scenario/asset keywords: "GT", "futures", "spot"
2. If mappable to type: Call `cex_activity_list_activity_types` then `cex_activity_list_activities` with `type_ids`
3. If scenario-based: Call `cex_activity_list_activities?recommend_type=scenario&keywords=["GT"]&page_size=3`
4. Output: Activity cards with "Filtered activities related to [scenario/asset] for you. Click the card to view participation requirements and rewards."

---

## Scenario 1.4: Search by Name

**Context**: User provides specific activity name or keywords.

**Prompt Examples**:
- "Help me find position airdrop phase 10"
- "Where is VIP exclusive activity"

**Expected Behavior**:
1. Extract keywords: "position airdrop", "VIP exclusive"
2. Call `cex_activity_list_activities?keywords=["position airdrop"]&page_size=3`
3. If results found: Output cards with "Based on your keywords, I found some possible activities. If you didn't find what you're looking for, you can provide a more complete activity name."
4. If no results: Use "No Results" template

---

## Scenario 2: My Activities

**Context**: User wants to see their enrolled activities.

**Prompt Examples**:
- "What activities have I joined"
- "My activities"
- "Activities I signed up for"

**Expected Behavior**:
1. Call `cex_activity_get_my_activity_entry`
2. Output: Entry card with "Click [My Activities] to view your enrolled and ongoing activities."

---

## Scenario 2.5: Show Query Process

**Context**: User asks to see the query process or wants to understand how activities are retrieved.

**Prompt Examples**:
- "Show me the query process"
- "How do you find these activities"
- "Explain the search steps"

**Expected Behavior**:
1. Show step-by-step query process with API calls
2. Display intermediate results (type list, matched type IDs)
3. Show final filtered results with explanation

**Example Output Format**:
```
## Step 1: Query Activity Type List
Call cex_activity_list_activity_types to get all activity types...
[Display type list table]

## Step 2: Match Target Type
Found Trading type ID = 4

## Step 3: Filter Activities
Filter activities with type_id = 4 from the activity list...
[Display filtered results table]

## Query Process Summary
[Display flow diagram]
```

---

## Scenario 3: No Activities Found (Recommendation)

**Context**: Activity recommendation returns empty results.

**Prompt Examples**:
- "Any Alpha activities" (no Alpha activities currently)

**Expected Behavior**:
1. Call `cex_activity_list_activities` with type filter
2. Response: empty list
3. Output "No Results" template:

```
Currently no Alpha activities are in progress. You can:
- Check the activity center regularly, new activities will be displayed as soon as they launch
- Tell me other activity types you're interested in (e.g., trading, earn, VIP exclusive), and I can filter for you
```

**FORBIDDEN**: "Filtered Alpha activities for you, click to view details" (when no results)
