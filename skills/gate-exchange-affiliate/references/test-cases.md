# Test Cases for Gate Exchange Affiliate Skill

Comprehensive test scenarios for validating the affiliate skill functionality.

## Test Case Categories

1. **Basic Queries** - Simple affiliate data requests
2. **Time-Range Queries** - Various time period requests
3. **Metric-Specific** - Individual metric queries
4. **User Analysis** - Specific user contribution queries
5. **Error Handling** - Invalid requests and edge cases
6. **Performance** - Large dataset and pagination tests

## 1. Basic Queries

### TC-1.1: Default Overview
**Input**: "Show my affiliate data"
**Expected Behavior**:
- Uses last 7 days as default time range
- Calls all three APIs (transaction_history, commission_history, sub_list)
- Returns all 5 metrics
**Validation**:
- Check time range calculation (now - 7 days)
- Verify all API calls made
- Confirm response includes all metrics

### TC-1.2: Alternative Phrasing
**Inputs**:
- "My partner statistics"
- "Affiliate dashboard"
- "Show referral performance"
**Expected**: Same as TC-1.1

## 2. Time-Range Queries

### TC-2.1: Within 30 Days
**Input**: "Commission for last 2 weeks"
**Expected Behavior**:
- Single API call per endpoint
- Time range: now - 14 days to now
**Validation**:
- No splitting occurs
- Correct timestamp calculation

### TC-2.2: Exactly 30 Days
**Input**: "Last 30 days affiliate data"
**Expected Behavior**:
- Single API call per endpoint
- Time range: now - 30 days to now

### TC-2.3: 60 Days (Requires Splitting)
**Input**: "Show commission for last 60 days"
**Expected Behavior**:
- Splits into 2 segments of 30 days each
- Makes 2 API calls per endpoint
- Merges results correctly
**Validation**:
- Verify split boundaries
- Check no data duplication
- Confirm aggregation accuracy

### TC-2.4: 180 Days (Maximum)
**Input**: "Last 180 days performance"
**Expected Behavior**:
- Splits into 6 segments of 30 days each
- Successfully processes all segments
**Validation**:
- All 6 segments processed
- Correct date boundaries

### TC-2.5: Over 180 Days (Error)
**Input**: "Show data for last 200 days"
**Expected**: Error message "Query supports maximum 180 days of historical data"

### TC-2.6: Specific Date Range
**Input**: "Affiliate data from January 1 to March 1, 2026"
**Expected Behavior**:
- Converts dates to timestamps
- Splits if necessary
- Returns data for exact period

## 3. Metric-Specific Queries

### TC-3.1: Commission Only
**Input**: "How much commission did I earn?"
**Expected Behavior**:
- Only calls commission_history API
- Returns commission amount in USDT
**Validation**:
- No unnecessary API calls
- Correct aggregation by asset

### TC-3.2: Customer Count
**Input**: "How many customers do I have?"
**Expected Behavior**:
- Only calls sub_list API
- Returns total count
**Validation**:
- Uses total field, not list length

### TC-3.3: Trading Users
**Input**: "How many active traders?"
**Expected Behavior**:
- Calls transaction_history
- Counts unique user_ids
**Validation**:
- Proper deduplication

### TC-3.4: Trading Volume
**Input**: "Total trading volume this month"
**Expected Behavior**:
- Calls transaction_history
- Sums amount field
- Groups by amount_asset

### TC-3.5: Net Fees
**Input**: "Fee contribution from my team"
**Expected Behavior**:
- Calls transaction_history
- Sums fee field
- Groups by fee_asset

## 4. User-Specific Analysis

### TC-4.1: Valid User ID
**Input**: "UID 123456 contribution"
**Expected Behavior**:
1. Checks sub_list for user existence
2. Calls transaction_history with user_id filter
3. Calls commission_history with user_id filter
4. Returns user-specific metrics

### TC-4.2: Invalid User ID Format
**Input**: "User ABC123 trading"
**Expected**: Error "Invalid UID format. UID should be numeric"

### TC-4.3: Non-Existent User
**Input**: "UID 999999999 contribution"
**Expected Behavior**:
1. Checks sub_list
2. Returns "UID not found in your referral network"

### TC-4.4: User with Time Range
**Input**: "UID 123456 commission last month"
**Expected Behavior**:
- Applies both user_id and time filters
- Returns filtered results

## 5. Error Handling

### TC-5.1: Not an Affiliate
**Scenario**: API returns 403
**Expected**: "Your account does not have affiliate privileges. Apply at: https://www.gate.com/referral/affiliate"

### TC-5.2: No Data Available
**Scenario**: APIs return empty lists
**Expected**: Shows metrics as 0, not error

### TC-5.3: Partial Data
**Scenario**: User has commissions but no transactions
**Expected**: Shows available data, 0 for missing metrics

### TC-5.4: API Timeout
**Scenario**: API request times out
**Expected**: Retry with backoff, then user-friendly error

### TC-5.5: Invalid Time Range Format
**Input**: "Data for tomorrow"
**Expected**: Error or clarification request

## 6. Performance Tests

### TC-6.1: Large Dataset Pagination
**Scenario**: User has 500+ transactions
**Expected Behavior**:
- Properly paginates through all pages
- Maintains performance
- Correct aggregation

### TC-6.2: Concurrent Requests
**Scenario**: Multiple metrics requested
**Expected Behavior**:
- Uses parallel API calls
- Faster than sequential

### TC-6.3: Cache Utilization
**Scenario**: Multiple queries in same session
**Expected Behavior**:
- sub_list cached after first call
- Subsequent queries faster

## 7. Team Performance Report

### TC-7.1: Complete Report
**Input**: "Generate team performance report"
**Expected Behavior**:
1. Calls all three APIs
2. Implements pagination if needed
3. Generates comprehensive report with:
   - Team composition breakdown
   - Active user percentage
   - Trading/commission analytics
   - Top contributors

### TC-7.2: Report with Time Range
**Input**: "Team report for Q1 2026"
**Expected Behavior**:
- Splits Q1 into appropriate segments
- Generates report for specific period

## 8. Application Guidance

### TC-8.1: Application Query
**Input**: "How to become an affiliate?"
**Expected Behavior**:
- No API calls
- Returns application instructions
- Includes application URL

### TC-8.2: Application Status
**Input**: "Check my affiliate application"
**Expected**: Guidance to check application status page

## 9. Edge Cases

### TC-9.1: Leap Year Handling
**Input**: "Data for February 2024"
**Expected**: Correctly handles 29 days

### TC-9.2: Daylight Saving Time
**Scenario**: Query spans DST change
**Expected**: Correct timestamp handling

### TC-9.3: Multiple Currencies
**Scenario**: Commission in BTC, ETH, USDT
**Expected**: Groups by currency or converts to USDT

### TC-9.4: Zero Values
**Scenario**: User with 0 commission
**Expected**: Shows "0.00 USDT" not empty

## 10. Validation Checklist

For each test case, verify:

- [ ] Correct API endpoints called
- [ ] Proper parameter formatting
- [ ] Time range calculations accurate
- [ ] Pagination handled correctly
- [ ] Results aggregated properly
- [ ] Error messages user-friendly
- [ ] Response time acceptable
- [ ] Memory usage reasonable
- [ ] No data duplication
- [ ] Formatting consistent

## Test Data Requirements

### Mock User Profiles

1. **New Affiliate**: 0-5 referrals, minimal data
2. **Active Affiliate**: 20-50 referrals, regular activity
3. **Power Affiliate**: 100+ referrals, high volume
4. **Mixed Types**: Sub-agents, direct, indirect customers

### Mock Time Periods

- Current day (partial data)
- Complete weeks
- Complete months
- Spanning months
- Historical (>30 days ago)

## Automated Testing

```javascript
// Example test runner
async function runTestSuite() {
  const testCases = [
    { id: 'TC-1.1', input: 'Show my affiliate data', validate: validateOverview },
    { id: 'TC-2.3', input: 'Last 60 days', validate: validateSplitting },
    // ... more test cases
  ];
  
  for (const test of testCases) {
    try {
      const result = await processQuery(test.input);
      const passed = await test.validate(result);
      console.log(`${test.id}: ${passed ? 'PASS' : 'FAIL'}`);
    } catch (error) {
      console.log(`${test.id}: ERROR - ${error.message}`);
    }
  }
}
```

## Success Criteria

- All basic queries return correct metrics
- Time splitting works for 30-180 day ranges
- Error messages are clear and actionable
- Performance acceptable for large datasets
- No data loss during aggregation
- Consistent formatting across responses