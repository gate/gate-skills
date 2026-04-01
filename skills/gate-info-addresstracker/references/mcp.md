---
name: gate-info-addresstracker-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for on-chain address profile and fund-flow tracing."
---

# Gate Address Tracker MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Address profile query
- Address transactions query
- Fund-flow tracing and summary

Out of scope:
- Trading execution and account mutation

Misroute examples:
- Token-level trend analysis without address target should route to token/on-chain research skills.

## 2. MCP Detection and Fallback

Detection:
1. Verify Gate-Info on-chain tools are available.
2. Probe with `info_onchain_get_address_info` first.

Fallback:
- If deep tools are unavailable, provide profile-only mode.
- If all tools are unavailable, return data-unavailable guidance without fabrication.

## 3. Authentication

- No API key required for these read endpoints in standard runtime.
- If runtime requires auth, request valid context before query.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

Read tools:
- `info_onchain_get_address_info`
- `info_onchain_get_address_transactions`
- `info_onchain_get_transaction`
- `info_onchain_trace_fund_flow`

Calling rules:
- Always normalize and validate address format before calls.
- Phase 1 must call address profile first.
- Phase 2 deep tracing is conditional on user intent or risk/size triggers.

## 6. Execution SOP (Non-Skippable)

1. Parse address and optional chain.
2. Call `info_onchain_get_address_info`.
3. Decide basic vs deep mode.
4. In deep mode, call transactions + fund-flow tracing.
5. Aggregate and output with explicit confidence/missing-data notes.

## 7. Output Templates

```markdown
## Address Tracking Summary
- Address: {address}
- Chain: {chain}
- Profile: {label_balance_risk_summary}
- Deep Trace: {key_flows_or_not_requested}
- Notes: {data_limits_or_missing_sections}
```

## 8. Safety and Degradation Rules

1. Never infer ownership as certainty unless explicitly labeled by source data.
2. Never fabricate fund-flow edges or transaction values.
3. Clearly mark heuristic conclusions as probabilistic.
4. Keep all operations read-only.
