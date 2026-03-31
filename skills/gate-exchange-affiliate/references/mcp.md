---
name: gate-exchange-affiliate-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for affiliate/partner analytics: eligibility, application status, partner commission/transaction/sub-user reports."
---

# Gate Affiliate MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Partner eligibility/application status queries
- Partner commission and transaction history
- Partner subordinate/user relationship reports

Out of scope:
- Direct application submission workflows not exposed in this skill

## 2. MCP Detection and Fallback

Detection:
1. Verify rebate/partner endpoints are available.
2. Probe `cex_rebate_get_partner_eligibility`.

Fallback:
- If history endpoints fail, return eligibility/status only.

## 3. Authentication

- API key required with partner/rebate permissions.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

- `cex_rebate_get_partner_eligibility`
- `cex_rebate_get_partner_application_recent`
- `cex_rebate_partner_commissions_history`
- `cex_rebate_partner_transaction_history`
- `cex_rebate_partner_sub_list`

## 6. Execution SOP (Non-Skippable)

1. Classify intent: eligibility/application vs commission/transaction analytics.
2. Normalize time range (respect endpoint constraints).
3. Fetch minimal required endpoints.
4. Aggregate into partner report with key KPIs.

## 7. Output Templates

```markdown
## Affiliate Partner Snapshot
- Eligibility: {eligible_or_not}
- Application Status: {recent_application_state}
- Commission: {commission_summary}
- Transactions: {transaction_summary}
- Subordinate Stats: {sub_list_summary}
```

## 8. Safety and Degradation Rules

1. Respect endpoint time-range limitations and disclose truncation.
2. Do not fabricate partner metrics when no data is returned.
3. Keep user-level data privacy boundaries in summaries.
4. If permission is insufficient, report required role clearly.
5. Keep outputs read-only.
