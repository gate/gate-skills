---
name: gate-exchange-kyc
version: "2026.3.18-2"
updated: "2026-03-18"
description: Guides users to the Gate KYC portal to complete identity verification. Use this skill whenever the user asks to do KYC, verify identity, find the verification page, or why they cannot withdraw. Trigger phrases include "complete KYC", "verify my identity", "where to do verification", "why can't I withdraw".
---

# KYC Portal Skill

## General Rules
Read and follow [`exchange-runtime-rules.md`](https://github.com/gate/gate-skills/blob/master/skills/exchange-runtime-rules.md) first.

Guides users to the Gate KYC portal. This skill only provides the link and brief instructions; it does not perform verification.

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
