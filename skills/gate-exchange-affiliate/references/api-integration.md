# API Integration Guide

Technical reference for integrating with Gate Exchange Partner Rebate APIs.

## Authentication

All requests require the `X-Gate-User-Id` header with partner privileges.

```http
X-Gate-User-Id: {user_id_with_partner_role}
```

## Base URL

Production: `https://api.gateio.ws/api/v4`

## Endpoints

### 1. Partner Transaction History

Get trading records of referred users.

**Endpoint**: `GET /rebate/partner/transaction_history`

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| currency_pair | string | No | Trading pair (e.g., "BTC_USDT") |
| user_id | integer | No | Specific user ID |
| from | integer | Yes | Start timestamp (Unix seconds) |
| to | integer | Yes | End timestamp (Unix seconds) |
| limit | integer | No | Records per page (default: 100) |
| offset | integer | No | Pagination offset (default: 0) |

**Response**:
```json
{
  "total": 150,
  "list": [
    {
      "transaction_time": 1709280000,
      "user_id": 123456,
      "group_name": "VIP1",
      "fee": "10.5",
      "fee_asset": "USDT",
      "currency_pair": "BTC_USDT",
      "amount": "10000",
      "amount_asset": "USDT",
      "source": "SPOT"
    }
  ]
}
```

**Source Values**:
- `SPOT`: Spot trading
- `FUTURES`: Futures trading

### 2. Partner Commission History

Get commission records from referred users.

**Endpoint**: `GET /rebate/partner/commission_history`

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| currency | string | No | Currency filter (e.g., "USDT") |
| user_id | integer | No | Specific user ID |
| from | integer | Yes | Start timestamp (Unix seconds) |
| to | integer | Yes | End timestamp (Unix seconds) |
| limit | integer | No | Records per page (default: 100) |
| offset | integer | No | Pagination offset (default: 0) |

**Response**:
```json
{
  "total": 75,
  "list": [
    {
      "commission_time": 1709280000,
      "user_id": 123456,
      "group_name": "VIP1",
      "commission_amount": "5.25",
      "commission_asset": "USDT",
      "source": "SPOT"
    }
  ]
}
```

### 3. Partner Subordinate List

Get list of all referred users (subordinates).

**Endpoint**: `GET /rebate/partner/sub_list`

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | integer | No | Filter by specific user ID |
| limit | integer | No | Records per page (default: 100) |
| offset | integer | No | Pagination offset (default: 0) |

**Response**:
```json
{
  "total": 45,
  "list": [
    {
      "user_id": 123456,
      "user_join_time": 1709280000,
      "type": 3
    }
  ]
}
```

**Type Values**:
- `1`: Sub-agent
- `2`: Indirect customer
- `3`: Direct customer

## Time Handling

### Important Constraints

1. **30-Day Limit**: Each API request can query maximum 30 days
2. **180-Day History**: System supports maximum 180 days of historical data
3. **Timestamp Format**: Unix timestamp in seconds (not milliseconds)

### Time Range Splitting Algorithm

For queries exceeding 30 days:

```javascript
function splitTimeRange(fromTimestamp, toTimestamp) {
  const MAX_DAYS = 30;
  const MAX_SECONDS = MAX_DAYS * 86400;
  const segments = [];
  
  let currentFrom = fromTimestamp;
  
  while (currentFrom < toTimestamp) {
    const currentTo = Math.min(currentFrom + MAX_SECONDS, toTimestamp);
    segments.push({
      from: currentFrom,
      to: currentTo
    });
    currentFrom = currentTo;
  }
  
  return segments;
}

// Example: 60-day query
const from = 1704067200; // 2024-01-01
const to = 1709251200;   // 2024-03-01

const segments = splitTimeRange(from, to);
// Result: [
//   { from: 1704067200, to: 1706659200 }, // Jan 1-31
//   { from: 1706659200, to: 1709251200 }  // Jan 31-Mar 1
// ]
```

## Pagination

### Complete Data Retrieval

```javascript
async function fetchAllData(endpoint, params) {
  const limit = 100;
  let offset = 0;
  let allData = [];
  let hasMore = true;
  
  while (hasMore) {
    const response = await fetch(`${endpoint}?${new URLSearchParams({
      ...params,
      limit,
      offset
    })}`);
    
    const data = await response.json();
    allData = allData.concat(data.list);
    
    // Check if more data exists
    hasMore = data.list.length === limit && offset + limit < data.total;
    offset += limit;
  }
  
  return allData;
}
```

## Data Aggregation

### Commission Aggregation by Asset

```javascript
function aggregateCommission(commissionList) {
  const aggregated = {};
  
  commissionList.forEach(item => {
    const asset = item.commission_asset;
    const amount = parseFloat(item.commission_amount);
    
    if (!aggregated[asset]) {
      aggregated[asset] = 0;
    }
    aggregated[asset] += amount;
  });
  
  return aggregated;
}
```

### Trading Volume Calculation

```javascript
function calculateTradingVolume(transactionList) {
  const volumes = {};
  
  transactionList.forEach(item => {
    const asset = item.amount_asset;
    const amount = parseFloat(item.amount);
    
    if (!volumes[asset]) {
      volumes[asset] = 0;
    }
    volumes[asset] += amount;
  });
  
  return volumes;
}
```

### Unique User Count

```javascript
function countUniqueUsers(transactionList) {
  const uniqueUsers = new Set();
  
  transactionList.forEach(item => {
    uniqueUsers.add(item.user_id);
  });
  
  return uniqueUsers.size;
}
```

## Error Handling

### Common Error Codes

| Code | Description | User Message |
|------|-------------|--------------|
| 403 | No partner privileges | "Your account does not have affiliate privileges" |
| 400 | Invalid time range | "Time range exceeds 30 days per request" |
| 404 | User not found | "User ID not found in your referral network" |
| 429 | Rate limit exceeded | "Too many requests, please try again later" |

### Error Response Format

```json
{
  "label": "INVALID_TIME_RANGE",
  "message": "Time range cannot exceed 30 days"
}
```

### Handling Strategy

```javascript
async function safeAPICall(endpoint, params) {
  try {
    const response = await fetch(endpoint, {
      headers: {
        'X-Gate-User-Id': userId
      },
      params
    });
    
    if (!response.ok) {
      const error = await response.json();
      
      switch (response.status) {
        case 403:
          throw new Error('Not an affiliate. Apply at: https://www.gate.com/referral/affiliate');
        case 400:
          if (error.label === 'INVALID_TIME_RANGE') {
            // Implement automatic splitting
            return handleTimeRangeSplit(endpoint, params);
          }
          throw new Error(error.message);
        case 404:
          throw new Error('User not found in your referral network');
        case 429:
          // Implement retry with backoff
          await sleep(5000);
          return safeAPICall(endpoint, params);
        default:
          throw new Error(`API Error: ${error.message}`);
      }
    }
    
    return response.json();
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
}
```

## Rate Limiting

- Default: 100 requests per minute
- Implement exponential backoff for 429 responses
- Use batch requests where possible
- Cache sub_list results (changes infrequently)

## Best Practices

1. **Parallel Requests**: When fetching multiple metrics, use parallel requests
2. **Efficient Pagination**: Use appropriate limit values (100 recommended)
3. **Time Zone Handling**: Always work in UTC timestamps
4. **Number Precision**: Maintain precision for cryptocurrency amounts
5. **Error Recovery**: Implement retry logic for transient failures
6. **Response Caching**: Cache sub_list for session duration
7. **Validation**: Validate all parameters before API calls