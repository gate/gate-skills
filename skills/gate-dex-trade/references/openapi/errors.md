# OpenAPI: Error Handling

> Load on any API error (`code != 0`). Display English message as-is, attach suggestions.

---

## General Errors (Auth / Signature / Rate Limit)

| Code | Handling |
|------|----------|
| 10001-10005 | Check API call implementation. Confirm 4 required headers are complete. |
| 10008 | Signature mismatch. Check SK correct? JSON compact (no spaces)? Path = `/api/v1/dex`? |
| 10101 | Timestamp > 30s offset. Check system clock. |
| 10103 | AK/SK invalid. Use "update AK/SK" to reconfigure. |
| 10111-10113 | IP whitelist issue. Custom AK/SK: add IP at https://web3.gate.com/zh/api-config. Default credentials have no restriction. |
| 10121 | X-Request-Id format invalid. Must be standard UUIDv4. |
| 10122 | **Auto retry**: New X-Request-Id, retry immediately. Max 3 retries. No user notification. |
| 10131-10133 | Rate limited. Default = 2 QPS. **Auto retry**: Wait 2s, max 2 retries. |

## Quote Errors

| Code | Handling |
|------|----------|
| 31101 | Amount exceeds max. Reduce and retry. |
| 31102 | Amount below min. Increase and retry. |
| 31104 | Trading pair not found. Check contract addresses. |
| 31105 / 31503 | Insufficient liquidity. Reduce amount or retry later. |
| 31106 | Quantity too small. Input larger amount. |
| 31108 | Token not supported. |
| 31109 | Price impact too large. Suggest caution or reduce amount. |
| 31111 | Gas exceeds output. Not cost-effective. Increase amount or use cheaper chain. |
| 31112 | Cross-chain not supported. Use Gate MCP: https://github.com/gate/gate-mcp |

## Build / Submit Errors

| Code | Handling |
|------|----------|
| 31500 / 31600 | Parameter error. Display message field details. |
| 31501 | Insufficient balance. Check token + gas. |
| 31502 | Slippage too low. Increase slippage. |
| 31504 | Token has freeze permission. Account may be frozen. |
| 31601 | order_id expired or signature failed. **Auto re-quote** (with SOP confirmation). |
| 31701 | No history records. |

## Auto Retry Summary

| Code | Action | Max Retries |
|------|--------|-------------|
| 10122 | New X-Request-Id, retry immediately | 3 |
| 10131-10133 | Wait 2s, retry | 2 |
| 31601 | Re-start from quote (with SOP) | 1 |
