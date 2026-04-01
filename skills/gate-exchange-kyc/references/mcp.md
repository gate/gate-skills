---
name: gate-exchange-kyc-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for KYC portal guidance and runtime fallback behavior."
---

# Gate KYC MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- KYC portal entry guidance
- KYC process routing and non-execution explanation

Out of scope:
- In-chat document submission
- KYC status mutation or approval actions

Misroute examples:
- If user asks to trade, transfer, or withdraw operations, route to corresponding exchange skills.

## 2. MCP Detection and Fallback

Detection:
1. Verify Gate MCP runtime availability at session start.
2. If runtime is unavailable, continue with portal-only guidance.

Fallback:
- This skill can complete with static portal guidance even without callable MCP tools.

## 3. Authentication

- API key is not required for returning the KYC portal link itself.
- If runtime policy requires authenticated context for user-specific guidance, request login first.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

No direct MCP tool invocation is required in this skill.

## 6. Execution SOP (Non-Skippable)

1. Confirm user intent is KYC or verification access.
2. Provide official portal URL: `https://www.gate.com/myaccount/profile/kyc_home`.
3. State that verification must be completed on the portal.
4. If user asks for status/doc upload in chat, redirect to portal or support.

## 7. Output Templates

```markdown
## KYC Guidance
- Portal: https://www.gate.com/myaccount/profile/kyc_home
- Steps: Log in, open portal, follow on-screen verification flow.
- Note: Verification is completed only on the official portal.
```

## 8. Safety and Degradation Rules

1. Never claim KYC is completed from chat-side actions.
2. Never request users to send sensitive identity documents in chat.
3. Use only official Gate portal/support endpoints.
4. If runtime unavailable, provide the same safe portal guidance without fabrication.
