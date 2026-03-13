# Gate Exchange Affiliate Skill

Query and manage Gate Exchange affiliate/partner program data.

## Overview

This skill provides comprehensive access to Gate Exchange affiliate program data, enabling partners to track commission earnings, analyze team performance, and manage their referral network. It handles the complexity of API limitations transparently, supporting queries up to 180 days by automatically splitting requests when needed.

### Core Capabilities

| Capability | Description |
|------------|-------------|
| **Commission Tracking** | Monitor rebate earnings across different currencies with real-time data |
| **Team Analytics** | Track team size, composition, and performance metrics |
| **User Analysis** | Analyze individual referred user's contribution and trading patterns |
| **Time-Range Queries** | Support for historical data up to 180 days with automatic request splitting |
| **Application Guidance** | Step-by-step instructions for joining the affiliate program |

## Architecture

### Design Pattern
This skill follows a **Standard Architecture** pattern with structured workflow steps and clear data flow:

1. **Query Parsing Layer**: Identifies query type and extracts parameters
2. **Validation Layer**: Checks time ranges and user permissions
3. **API Integration Layer**: Calls Partner APIs with proper pagination
4. **Data Processing Layer**: Aggregates and calculates metrics
5. **Presentation Layer**: Formats responses using predefined templates

### API Integration
The skill exclusively uses Partner APIs (Agency APIs are deprecated):
- `/rebate/partner/transaction_history` - Trading records
- `/rebate/partner/commission_history` - Commission records
- `/rebate/partner/sub_list` - Subordinate list

### Time Range Handling
- **Single Request**: ≤30 days (API limitation)
- **Multi-Request**: 31-180 days (automatic splitting into 30-day segments)
- **Error**: >180 days (exceeds maximum supported range)

### Data Flow
```
User Query → Parse Intent → Validate Parameters → Call APIs → 
Aggregate Data → Format Response → Return to User
```

## Installation

1. Install the Gate MCP server if not already installed:
```bash
npm install -g gate-mcp
```

2. Configure your Gate API credentials with partner privileges

3. Load this skill in your AI assistant

## Features

- Query affiliate metrics (commission, volume, fees, customers, trading users)
- Support for time-specific queries (handles API 30-day limit automatically)
- User-specific contribution analysis
- Team performance reports with aggregated statistics
- Affiliate program application guidance

## API Limitations

- Single API request limited to 30 days
- For queries >30 days, the agent will automatically split into multiple requests
- Maximum historical data: 180 days
- Requires partner role authentication

## Example Queries

- "Show my affiliate data"
- "Commission earnings this month"
- "How many customers do I have?"
- "Team trading volume last week"
- "UID 123456 contribution"
- "Apply for affiliate program"

## Support

For issues or questions about the Gate Exchange affiliate program:
- Dashboard: https://www.gate.com/referral/affiliate
- Support: support@mail.gate.com