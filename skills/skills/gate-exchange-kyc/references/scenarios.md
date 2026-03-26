# Scenarios

## Scenario 1: User wants to do KYC or find verification page

**Context**: User wants to complete KYC or find where to verify identity on Gate.

**Prompt Examples**:
- "I want to complete KYC"
- "Where can I do verification?"
- "How do I verify my identity?"
- "Why can't I withdraw?"

**Expected Behavior**:
1. Provide KYC portal URL: https://www.gate.com/myaccount/profile/kyc_home
2. Tell user to log in, open the link, and follow the on-screen steps on the portal.

---

## Scenario 2: User asks for KYC status or tries to submit docs in-chat

**Context**: User asks about KYC application status or expects to submit documents in the chat.

**Prompt Examples**:
- "What's my KYC status?"
- "Can you verify my ID?"
- "Submit my KYC documents here"

**Expected Behavior**:
1. Say verification is done only on the KYC portal (or direct to Gate support for status).
2. Provide KYC portal URL and tell user to complete verification there; do not accept or process documents in-chat.
