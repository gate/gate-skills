---
name: gate-exchange-referral
version: "2026.3.26-1"
updated: "2026-03-26"
description: "Gate invite-friends and referral campaign skill. Recommends referral activities, explains participation rules for Earn Together, Help & Get Coupons, and Super Commission, and answers reward FAQs. Use when the user asks about invitation rewards, referral links, commission rebates, or earn-together rules. Triggers on 'invite friends', 'referral reward', 'referral link', 'earn together', 'commission rebate'."
---

# Gate Invite Friends Activity Recommendation & Rule Interpretation

## General Rules

⚠️ STOP — Read and strictly follow the shared runtime rules before proceeding.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they exist in the MCP server.

---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate (main) | ✅ Required |

### Authentication
- API key may be required depending on runtime. The primary workflow is read-only guidance; account-scoped rebate queries may require authenticated Exchange MCP access.

### Installation Check
- Required: Gate (main)
- Install via IDE-specific installer skill: `gate-mcp-cursor-installer`, `gate-mcp-codex-installer`, `gate-mcp-claude-installer`, or `gate-mcp-openclaw-installer`.

## MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), then execute this skill's recommendation/interpretation flow.

- `SKILL.md` keeps referral policy logic and decision tables.
- `references/mcp.md` is the authoritative MCP execution layer for capability boundaries, fallback behavior, and output constraints.

## Domain Knowledge

**Referral page URL (use in all responses that reference the activity page):** https://www.gate.com/referral

### Programs Overview

| Program | Type | Reward | Duration |
|---------|------|--------|----------|
| **Earn Together** | Limited-time campaign | Random cash vouchers for both inviter and invitee | Time-limited; one campaign at a time |
| **Help & Get Coupons** | Ongoing | Platform coupon rewards (e.g., 200 USDT trial voucher, 5-day validity) | Ongoing |
| **Super Commission** | Permanent | Trading fee rebates (Spot, Alpha, Futures, TradFi) | Permanent; passive income |

For detailed product definitions, participation steps, and reward mechanics, see [`references/product-definitions.md`](./references/product-definitions.md) (or the Product Definitions section in `references/scenarios.md`).

### Activity Constraints

- All three programs can be joined simultaneously; Earn Together opens irregularly.
- Each invitee can only be linked through **one** invitation mode.
- **Exclusivity rule:** Referral relationships created through Super Commission cannot earn rewards from other activities, and vice versa.

## Workflow

When the user asks any question related to inviting friends, follow this sequence.

### Step 1: Classify Intent

Determine which category the request falls into:

| Category | Examples |
|----------|---------|
| **A. Activity recommendation** | "What referral activities are available?" |
| **B. Rule interpretation** | "How does Earn Together work?" |
| **C. Personalized recommendation** | "I want quick cash" / "I want passive income" |
| **D. FAQ** | Reward timing, amount differences, task requirements |
| **E. Data query** | "How many people have I invited?" |
| **F. Multi-activity rules** | "Can I join all three?" |

### Step 2: Route and Respond

**A. Activity Recommendation:**
1. Check whether an Earn Together campaign is currently active.
2. If active → recommend Earn Together only. If not active → recommend Help & Get Coupons + Super Commission.
3. For "how to get referral link" → explain: visit the Invite Friends page → copy exclusive link or QR code.

**B. Rule Interpretation:**
- Explain the requested program's participation steps, reward mechanism, and caveats in detail.
- Do **not** recommend activity cards when interpreting rules.
- See [`references/scenarios.md`](./references/scenarios.md) for expected behavior per scenario.

**C. Personalized Recommendation:**

| User Need | Recommend | Rationale |
|-----------|-----------|-----------|
| Quick cash rewards | Earn Together (if active), else Help & Get Coupons | Random cash vouchers on task completion |
| Trial vouchers / coupons | Help & Get Coupons | Platform coupon rewards after inviting 2 friends |
| Long-term passive income | Super Commission | Ongoing trading fee rebates, permanently effective |

**D. FAQ:**

| Question | Answer |
|----------|--------|
| "Why different reward amounts?" | Rewards are randomly generated; amounts vary per invitation. |
| "When will rewards arrive?" | Subject to risk-control review; typically distributed within 14 business days after campaign ends. |
| "What are the deposit/trading requirements?" | Requirements vary by region. Check the activity page for details. |

**E. Data Query:**
- Inform the user that conversational data queries are not supported. Redirect to the Invite Friends page.

**F. Multi-activity Rules:**
- Confirm all three can be joined simultaneously, but emphasize the exclusivity constraint.

### Step 3: Format Response

Every response must include:
1. Activity name and brief description
2. Core participation steps (simplified)
3. Key caveats (regional variation, risk-control review, reward randomness)
4. Direct link to the referral page when applicable

For detailed scenario routing (Cases 1–14) and expected/unexpected behaviors, see [`references/scenarios.md`](./references/scenarios.md).

## Report Template

```markdown
## Referral Guidance

| Item | Details |
|------|---------|
| Recommended Program | {program_name} |
| Why | {fit_reason} |
| How to Participate | {participation_steps} |
| Key Notes | {constraints_and_timeline} |
| Activity Page | https://www.gate.com/referral |
```

## Capability Boundaries

**Supported:** Activity recommendation, program comparison, rule interpretation, task description (simplified), FAQ answering, personalized activity selection.

**Not supported:**
- Activity data queries (invitee count, reward amounts) → redirect to Invite Friends page
- Reward progress queries → redirect to Invite Friends page
- Agent/institutional account applications → redirect to business partnership contacts

## Error Handling

| Error Type | Handling Strategy |
|------------|-------------------|
| Earn Together status unknown | Default to recommending Help & Get Coupons + Super Commission; direct user to the referral page for latest campaigns |
| Unsupported data query | State conversational queries are not supported; redirect to referral page |
| Agent/institutional user | Inform referral activities do not apply; redirect to business partnership contacts |
| Region-restricted user | Inform participation is not available in their region |
| Ambiguous intent | Ask a clarifying question before recommending |

## Safety Rules

- Fake accounts and fraudulent transactions are strictly prohibited; violators lose reward eligibility.
- Agents and institutional users are not eligible for referral activities.
- Identify user region; if restricted, inform the user participation is unavailable.
- Never promise specific reward amounts (rewards are randomly generated).
- Never provide specific deposit/trading volume requirements (vary by region); redirect to the activity page.
- All activity data query requests must be redirected to the Invite Friends page.
