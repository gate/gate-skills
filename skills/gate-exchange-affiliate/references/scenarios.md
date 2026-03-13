# Affiliate Query Scenarios

Detailed scenarios for handling various affiliate data query requests.

## Scenario 1: Basic Overview Query

**Context**: User wants to see their overall affiliate performance without specifying a time range. This is the most common query type for daily monitoring.

**Prompt Examples**:
- "Show my affiliate data"
- "My partner statistics"
- "Affiliate dashboard summary"
- "How's my referral program doing?"

**Expected Behavior**:
1. Parse query as overview type with no time specification
2. Set default time range to last 7 days
3. Call all three Partner APIs in parallel
4. Aggregate metrics from responses
5. Format and return overview report with all five core metrics
6. Include dashboard link for detailed access

## Scenario 2: Time-Range Query with Splitting

**Context**: User requests data for a period longer than 30 days, requiring the skill to split the request into multiple API calls due to the 30-day limitation per request.

**Prompt Examples**:
- "Show commission for last 60 days"
- "Trading volume for Q1 2026"
- "Last 3 months affiliate earnings"
- "Yearly affiliate performance"

**Expected Behavior**:
1. Parse time range from query
2. Check if range exceeds 30 days
3. If yes, split into 30-day segments
4. Execute API calls for each segment
5. Merge results from all segments
6. Aggregate combined data
7. Return unified report with note about splitting

## Scenario 3: Metric-Specific Query

**Context**: User wants to know a specific metric rather than a full overview, allowing for optimized API calls.

**Prompt Examples**:
- "How much commission did I earn?"
- "What's my team size?"
- "Total trading volume"
- "How many active traders?"
- "Net fees this month"

**Expected Behavior**:
1. Identify the specific metric requested
2. Determine which API(s) are needed for that metric
3. Call only the required API(s)
4. Calculate the specific metric
5. Return focused response with just that metric
6. Provide context about time range used

## Scenario 4: User-Specific Contribution

**Context**: User wants to analyze the contribution of a specific referred user, requiring filtered API calls with user_id parameter.

**Prompt Examples**:
- "UID 123456 contribution"
- "How much did user 123456 trade?"
- "Commission from UID 123456"
- "User 123456 performance last month"

**Expected Behavior**:
1. Extract user ID from query
2. Validate user ID format (must be numeric)
3. Check if user exists in subordinate list
4. If exists, call transaction and commission APIs with user_id filter
5. Calculate user-specific metrics
6. Return detailed user contribution report
7. Include user type and join date if available

## Scenario 5: Team Performance Report

**Context**: User wants a comprehensive analysis of their entire team's performance, requiring data from all APIs with extensive aggregation.

**Prompt Examples**:
- "Team performance report"
- "Full affiliate analytics"
- "Detailed partner statistics"
- "Generate monthly team report"

**Expected Behavior**:
1. Call sub_list API to get team composition
2. Call transaction_history for all trading data
3. Call commission_history for all commission data
4. Implement pagination if needed for large datasets
5. Analyze team composition (sub-agents, direct, indirect)
6. Calculate aggregate metrics and identify top performers
7. Generate comprehensive report with multiple sections
8. Include trend analysis if time range allows

## Scenario 6: Error Handling Cases

**Context**: Various error conditions that need proper handling and user-friendly error messages.

**Prompt Examples**:
- "Data for last 200 days" (exceeds limit)
- "UID 999999 contribution" (user not found)
- "My affiliate data" (when user lacks privileges)
- "User ABC123 trading" (invalid format)

**Expected Behavior**:
1. Identify the error condition
2. Return appropriate error message
3. Provide guidance for resolution
4. Suggest alternative actions where applicable
5. Include relevant links (application page, support)

## Scenario 7: Pagination Handling

**Context**: API response contains more records than the limit, requiring multiple requests to retrieve complete data.

**Prompt Examples**:
- "All transactions this month" (when >100 records)
- "Complete team list" (when >100 members)
- "Full commission history"

**Expected Behavior**:
1. Check if total > limit in initial response
2. Calculate number of pages needed
3. Make additional API calls with offset parameter
4. Combine all pages of data
5. Process complete dataset
6. Note in response that pagination was used
7. Report total records processed

## Scenario 8: Multi-Period Comparison

**Context**: User wants to compare performance across different time periods to identify trends and growth.

**Prompt Examples**:
- "Compare this week vs last week"
- "Month-over-month growth"
- "Q1 vs Q2 performance"
- "Daily average this month vs last month"

**Expected Behavior**:
1. Parse both time periods from query
2. Execute API calls for each period separately
3. Calculate metrics for both periods
4. Compute growth rates and changes
5. Format comparison report with trends
6. Highlight significant changes
7. Provide insights on performance trends

## Scenario 9: Application Guidance

**Context**: User is not yet an affiliate and wants to know how to join the program.

**Prompt Examples**:
- "How to become an affiliate?"
- "Apply for partner program"
- "Join affiliate program"
- "I want to be a Gate partner"

**Expected Behavior**:
1. Recognize application intent
2. Skip API calls (no data to query)
3. Provide clear application steps
4. Include application portal link
5. List program benefits
6. Mention requirements if applicable

## Scenario 10: Invalid Query Handling

**Context**: User query cannot be parsed or doesn't match any known pattern.

**Prompt Examples**:
- "Affiliate stuff"
- "Show me everything"
- "Data"
- Ambiguous or incomplete queries

**Expected Behavior**:
1. Acknowledge inability to parse specific intent
2. List available query types
3. Provide example queries
4. Suggest most common query (overview)
5. Offer to show default overview if user confirms