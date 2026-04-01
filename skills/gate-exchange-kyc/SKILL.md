---
name: gate-exchange-kyc
version: "2026.3.23-1"
updated: "2026-03-23"
description: Guides users to the Gate KYC portal to complete identity verification. Use this skill whenever the user asks to do KYC, verify identity, find the verification page, or why they cannot withdraw. Trigger phrases include "complete KYC", "verify my identity", "where to do verification", "why can't I withdraw".
---

# KYC Portal Skill

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.


---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate (main) | ✅ Required |

### Authentication
- API Key Required: Yes (see skill doc/runtime MCP deployment)

### Installation Check
- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## Workflow

When the user asks about KYC or identity verification:

1. Provide the KYC portal URL: https://www.gate.com/myaccount/profile/kyc_home
2. Tell them to log in (if needed), open the link, and follow the on-screen steps on the portal.

If they ask about KYC status or want to submit documents in-chat, say verification is done only on the portal and direct them to the link (or to Gate support for status).

## Judgment Logic Summary

| Condition | Action |
|-----------|--------|
| User wants to do KYC, find verification page, or asks why verification / why can't withdraw | Give KYC portal URL and brief steps (log in, open link, complete on portal). |
| User asks for KYC status or tries to submit docs in-chat | Redirect to portal or Gate support; do not perform verification. |

## Report Template

```markdown
You can complete identity verification (KYC) on the official KYC portal:

**KYC portal**: https://www.gate.com/myaccount/profile/kyc_home

Log in to your Gate account, open the link above, and follow the on-screen steps. Verification is done entirely on the portal.
```
