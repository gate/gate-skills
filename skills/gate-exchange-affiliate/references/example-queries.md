# Example Queries and Responses

Sample queries with expected responses for testing and validation.

## 1. Basic Overview

### Query
```
"Show my affiliate data"
```

### Expected Response
```
Your affiliate data overview (last 7 days):
- Commission Amount: 1,234.56 USDT
- Trading Volume: 123,456.78 USDT  
- Net Fees: 123.45 USDT
- Customer Count: 45
- Trading Users: 28

For detailed data, visit the affiliate dashboard: https://www.gate.com/referral/affiliate
```

## 2. Time-Specific Queries

### Query: Last 30 Days
```
"Commission for last 30 days"
```

### Expected Response
```
Your affiliate data for Feb 11 - Mar 12, 2026:
- Commission Amount: 5,432.10 USDT
- Trading Volume: 543,210.00 USDT
- Net Fees: 543.21 USDT
- Customer Count: 52
- Trading Users: 41

For detailed data, visit the affiliate dashboard: https://www.gate.com/referral/affiliate
```

### Query: Last 60 Days (Requires Splitting)
```
"Show data for last 60 days"
```

### Expected Response
```
Your affiliate data for Jan 12 - Mar 12, 2026:
[Note: Data retrieved in 2 segments due to API limitations]
- Commission Amount: 10,864.20 USDT
- Trading Volume: 1,086,420.00 USDT
- Net Fees: 1,086.42 USDT
- Customer Count: 52
- Trading Users: 48

For detailed data, visit the affiliate dashboard: https://www.gate.com/referral/affiliate
```

### Query: Exceeds 180 Days
```
"Data for last 200 days"
```

### Expected Response
```
Query supports maximum 180 days of historical data.
Please adjust your time range.
```

## 3. Metric-Specific Queries

### Query: Commission Only
```
"How much commission did I earn?"
```

### Expected Response
```
Your commission amount for the last 7 days: 1,234.56 USDT

For detailed data, visit the affiliate dashboard: https://www.gate.com/referral/affiliate
```

### Query: Customer Count
```
"How many customers do I have?"
```

### Expected Response
```
Your customer count: 45

Breakdown:
- Sub-agents: 3
- Direct customers: 30
- Indirect customers: 12

For detailed data, visit the affiliate dashboard: https://www.gate.com/referral/affiliate
```

### Query: Trading Users
```
"How many active traders?"
```

### Expected Response
```
Your trading users for the last 7 days: 28

This represents unique users who have executed trades during this period.

For detailed data, visit the affiliate dashboard: https://www.gate.com/referral/affiliate
```

## 4. User-Specific Analysis

### Query: Valid User
```
"UID 123456 contribution"
```

### Expected Response
```
UID 123456 contribution (last 7 days):
- Commission Amount: 45.67 USDT
- Trading Volume: 4,567.89 USDT
- Fees: 4.57 USDT
- User Type: Direct customer
- Join Date: 2026-01-15
```

### Query: User Not Found
```
"UID 999999 contribution"
```

### Expected Response
```
UID 999999 not found in your referral network.
Please verify the user ID.
```

### Query: Invalid Format
```
"User ABC123 trading"
```

### Expected Response
```
Invalid UID format. UID should be a numeric value.
Example: UID 123456
```

## 5. Team Performance Report

### Query
```
"Generate team performance report"
```

### Expected Response
```
=== Team Performance Report (Mar 6 - Mar 12, 2026) ===

📊 Team Overview
- Total Members: 45 (Sub-agents: 3, Direct: 30, Indirect: 12)
- Active Users: 28 (62.2%)
- New Members: 2

💰 Trading Data
- Total Volume: 123,456.78 USDT
- Total Fees: 123.45 USDT
- Average Volume per User: 4,409.17 USDT

🏆 Commission Data
- Total Commission: 1,234.56 USDT
- Spot Commission: 864.19 USDT (70%)
- Futures Commission: 370.37 USDT (30%)

👑 Top 5 Contributors
1. UID 123456 - Volume 12,345.67 USDT / Commission 123.45 USDT
2. UID 234567 - Volume 10,234.56 USDT / Commission 102.34 USDT
3. UID 345678 - Volume 8,123.45 USDT / Commission 81.23 USDT
4. UID 456789 - Volume 6,012.34 USDT / Commission 60.12 USDT
5. UID 567890 - Volume 4,901.23 USDT / Commission 49.01 USDT

📈 Trend Analysis
- Volume increased 15% from previous period
- Active user rate improved by 5%
- Average commission per user: 44.09 USDT
```

## 6. Application Guidance

### Query
```
"How to become an affiliate?"
```

### Expected Response
```
You can apply to become a Gate Exchange affiliate and earn commission from referred users' trading.

Application Process:
1. Open the affiliate application page
2. Fill in application information
3. Submit application
4. Wait for platform review

Application Portal: https://www.gate.com/referral/affiliate

Benefits:
- Earn commission from referred users
- Access to marketing materials
- Dedicated support team
- Performance analytics dashboard

Requirements:
- Valid Gate Exchange account
- KYC verification completed
- Meet minimum trading volume requirements

For more information, visit the affiliate program page or contact support@mail.gate.com
```

## 7. Error Scenarios

### Not an Affiliate
```
Query: "Show my affiliate data"
Response: "Your account does not have affiliate privileges. 
To become an affiliate, please apply at: https://www.gate.com/referral/affiliate"
```

### No Data Available
```
Query: "Commission for January 2026"
Response: "No data found for January 2026.
Please check if you have referred users with trading activity during this period."
```

### Sub-account Restriction
```
Query: "My affiliate earnings"
Response: "Sub-accounts cannot query affiliate data.
Please use your main account."
```

## 8. Comparison Queries

### Query
```
"Compare this week vs last week"
```

### Expected Response
```
Performance Comparison: This Week vs Last Week

Metric          | Last Week    | This Week    | Change
----------------|--------------|--------------|--------
Commission      | 1,000.00 USDT| 1,234.56 USDT| +23.5% ↑
Trading Volume  | 100,000 USDT | 123,456 USDT | +23.5% ↑
Net Fees        | 100.00 USDT  | 123.45 USDT  | +23.5% ↑
Trading Users   | 25           | 28           | +12.0% ↑
New Customers   | 3            | 5            | +66.7% ↑

Key Insights:
- Strong growth in all metrics
- User acquisition improving
- Average volume per user stable
```

## 9. Multi-Currency Handling

### Query
```
"Commission breakdown by currency"
```

### Expected Response
```
Commission by Currency (last 7 days):
- USDT: 1,000.00
- BTC: 0.0123
- ETH: 0.456

Total (USDT equivalent): 1,234.56 USDT

Note: Non-USDT amounts converted at current market rates
```

## 10. Date Range Variations

### Query: Specific Dates
```
"Affiliate data from March 1 to March 10, 2026"
```

### Expected Response
```
Your affiliate data for Mar 1 - Mar 10, 2026:
- Commission Amount: 890.12 USDT
- Trading Volume: 89,012.34 USDT
- Net Fees: 89.01 USDT
- Customer Count: 45
- Trading Users: 23
```

### Query: Month Name
```
"February commission"
```

### Expected Response
```
Your affiliate data for February 2026:
- Commission Amount: 4,567.89 USDT
- Trading Volume: 456,789.00 USDT
- Net Fees: 456.78 USDT
- Customer Count: 43
- Trading Users: 38
```

### Query: Quarter
```
"Q1 2026 performance"
```

### Expected Response
```
Your affiliate data for Q1 2026 (Jan 1 - Mar 31):
[Note: Data retrieved in 3 segments due to API limitations]
- Commission Amount: 15,432.10 USDT
- Trading Volume: 1,543,210.00 USDT
- Net Fees: 1,543.21 USDT
- Customer Count: 52
- Trading Users: 49
```