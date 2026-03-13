# MCP Configuration for Gate Exchange Affiliate Skill

Configuration example for integrating the affiliate skill with MCP server.

## MCP Server Configuration

Add to your MCP server configuration file:

```json
{
  "mcpServers": {
    "gate": {
      "command": "npx",
      "args": ["-y", "gate-mcp"],
      "env": {
        "GATE_BASE_URL": "https://api.gateio.ws",
        "GATE_API_KEY": "your-api-key",
        "GATE_API_SECRET": "your-api-secret"
      }
    }
  }
}
```

## Required Endpoints

The MCP server must expose the following endpoints:

### Partner Endpoints (Required)
- `/rebate/partner/transaction_history`
- `/rebate/partner/commission_history`
- `/rebate/partner/sub_list`

### Deprecated Endpoints (Not Used)
- `/rebate/agency/transaction_history` ❌
- `/rebate/agency/commission_history` ❌

## Authentication

The MCP server should handle authentication using the configured API credentials and add the required `X-Gate-User-Id` header with partner privileges.

## Testing the Integration

1. **Test Partner Access**:
```bash
# Test if you have partner privileges
curl -X GET "https://api.gateio.ws/api/v4/rebate/partner/sub_list?limit=1" \
  -H "X-Gate-User-Id: YOUR_USER_ID"
```

2. **Test Time Range Query**:
```bash
# Test 7-day query
curl -X GET "https://api.gateio.ws/api/v4/rebate/partner/transaction_history" \
  -H "X-Gate-User-Id: YOUR_USER_ID" \
  -d "from=$(($(date +%s) - 604800))" \
  -d "to=$(date +%s)" \
  -d "limit=10"
```

## Environment Variables

For development/testing:

```bash
export GATE_BASE_URL="https://api.gateio.ws"
export GATE_API_KEY="your-api-key"
export GATE_API_SECRET="your-api-secret"
export GATE_USER_ID="your-user-id-with-partner-role"
```

## Error Codes to Handle

| Code | Meaning | Action |
|------|---------|--------|
| 403 | No partner privileges | User needs to apply for affiliate program |
| 400 | Invalid parameters | Check time range (max 30 days) |
| 429 | Rate limited | Implement retry with backoff |

## Rate Limits

- Default: 100 requests per minute
- Implement exponential backoff for 429 responses
- Cache `sub_list` results as they change infrequently

## Sample MCP Tool Definition

```json
{
  "name": "get_partner_commission",
  "description": "Get partner commission history",
  "inputSchema": {
    "type": "object",
    "properties": {
      "from": {
        "type": "integer",
        "description": "Start timestamp (Unix seconds)"
      },
      "to": {
        "type": "integer",
        "description": "End timestamp (Unix seconds)"
      },
      "currency": {
        "type": "string",
        "description": "Currency filter (optional)"
      },
      "user_id": {
        "type": "integer",
        "description": "Specific user ID (optional)"
      },
      "limit": {
        "type": "integer",
        "default": 100,
        "description": "Records per page"
      },
      "offset": {
        "type": "integer",
        "default": 0,
        "description": "Pagination offset"
      }
    },
    "required": ["from", "to"]
  }
}
```