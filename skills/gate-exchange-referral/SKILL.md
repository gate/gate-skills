---
name: gate-exchange-referral
version: "2026.3.26-1"
updated: "2026-03-26"
description: "Gate invite-friends and referral campaign skill. Use when the user asks about invitation rewards, referral links, or earn-together rules. Triggers on 'invite friends', 'referral reward', 'referral link', 'earn together'."
---

# Gate Invite Friends Activity Recommendation & Rule Interpretation

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
- API Key Required: May be required, depending on runtime and whether account-specific referral data is needed
- Note: The main workflow in this skill is read-only guidance and rule interpretation. Account-scoped rebate or referral-detail queries may require authenticated Exchange MCP access in some deployments.

### Installation Check
- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), then execute this skill's recommendation/interpretation flow.

- `SKILL.md` keeps referral policy logic and decision tables.
- `references/mcp.md` is the authoritative MCP execution layer for capability boundaries, fallback behavior, and output constraints.

## Domain Knowledge

### Page Entry Points

| Page | URL |
|------|-----|
| Invite Friends (Activity Hub) | https://www.gate.com/referral |

When recommending activities, guiding users to check details, or mentioning the "Invite Friends page", always include the above URL so the user can navigate directly.

### Product Definitions

#### 1. Earn Together

- **Definition**: A limited-time invitation campaign (viral mechanism) where the inviter (M1) shares an exclusive link, the invitee (M2) registers via the link and completes tasks, and both parties receive random token rewards
- **Activity Characteristics**:
  - Time-limited: Each campaign has a clear start and end date
  - Exclusive: Only one Earn Together campaign runs at a time
  - Random rewards: Reward amounts are randomly generated within a configured range
- **How to Participate**:
  1. Inviter (M1) shares an exclusive link
  2. Invitee (M2) registers via the link
  3. M2 completes designated tasks (KYC, deposit, trading)
  4. Both parties receive random cash vouchers
- **Important Notes**:
  - Specific task requirements (deposit amount, trading volume) vary by region; please check the activity page for details
  - Rewards are subject to risk-control review and are typically distributed within 14 business days after claiming

#### 2. Help & Get Coupons

- **Definition**: Invite 2 friends to complete tasks and receive platform coupon rewards; suitable for users who want trial vouchers or discount coupons
- **How to Participate**:
  1. Share your exclusive invitation link
  2. Invite 2 new users to register
  3. New users complete the following tasks: deposit task, trading task
  4. Receive coupon rewards (e.g., 200 USDT position trial voucher; rewards may be adjusted based on actual conditions)
- **Important Notes**:
  - Assistance rewards are distributed to the Coupon Center with a 5-day validity period
  - Coupons have usage rules and expiration restrictions
  - Please check the activity page for detailed task requirements

#### 3. Super Commission

- **Definition**: A permanent invitation system that provides commission rebates based on friends' trading fees, generating continuous passive income
- **How to Participate**:
  1. Share your exclusive invitation link
  2. Friends register via the link
  3. Friends trade (Spot, Alpha, Futures, TradFi, etc.)
  4. Both you and your friends receive trading fee rebates
- **Important Notes**:
  - Commission rates vary by trading type; please check the activity page for detailed rebate rules

### Activity Constraints

- All three activities can be joined simultaneously; Earn Together is a time-limited event that opens irregularly
- Each invitee can only be invited through one invitation mode
- Referral relationships created through Super Commission cannot earn rewards from other activities; users invited through other activities cannot earn commission rebates

### Common Misconceptions

| User Question | Correct Answer |
|---------|---------|
| "Why did my friend and I receive different amounts?" | Rewards are randomly generated; the amount may differ for each invitation |
| "Are rewards credited immediately?" | Rewards are subject to risk-control review and are typically reviewed and distributed within 14 business days after the activity ends |
| "What are the specific task requirements? How much to deposit? How much to trade?" | Specific deposit amounts and trading volume requirements vary by regional policy; please check the activity page for details |

### Feature Keywords

| Keywords | Corresponding Product/Feature |
|-------|-------------|
| invite friends, referral, referral reward, invitation campaign, invite, referral, how to invite | Invite Friends Activity Recommendation |
| earn together, random reward, limited-time event | Earn Together |
| help, coupon, trial voucher, discount coupon | Help & Get Coupons |
| commission, rebate, passive income | Super Commission |
| how to earn, extra income, invitation reward | Activity Recommendation (General) |

## Workflow

When the user asks any question related to inviting friends, follow this sequence.

### Step 1: Identify Intent Type

Classify the request into one of the following categories:
1. Activity recommendation (user wants to know what referral activities are available)
2. Rule interpretation (user wants to understand a specific activity's rules/mechanics)
3. Activity selection advice (user has a specific need and wants the best-matching activity recommended)
4. FAQ (reward arrival time, amount differences, task requirements, etc.)
5. Data query (user wants to view activity data or reward progress)
6. Multi-activity participation rules (user wants to join multiple activities simultaneously)

### Step 2: Check Activity Status

For activity recommendation requests:
- Check whether there is an active Earn Together campaign
  - If yes → Prioritize recommending Earn Together (1 activity)
  - If no → Recommend Help & Get Coupons + Super Commission

### Step 3: Respond by Scenario

Select the corresponding response strategy based on the Case Routing Map.

### Step 4: Return Result

The response must include:
- Activity name and brief description
- Core participation steps (simplified version)
- Key notes and caveats
- Guide the user to the activity page with the direct URL (https://www.gate.com/referral) for details (if applicable)

## Case Routing Map (1-14)

### A. Activity Recommendation (1-3)

| Case | User Intent | Core Decision | Response Strategy |
|------|----------|----------|----------|
| 1 | Asks about referral activities (Earn Together is active) | Check if Earn Together is currently running → Yes | Introduce and recommend Earn Together with activity card entry |
| 2 | Asks about referral activities (Earn Together is not active) | Check if Earn Together is currently running → No | Introduce and recommend Help & Get Coupons + Super Commission |
| 3 | Asks how to invite friends / get referral link | Guide user through the operation flow | Explain: go to Invite Friends page → copy exclusive link or QR code |

### B. Rule Interpretation (4-7)

| Case | User Intent | Core Decision | Response Strategy |
|------|----------|----------|----------|
| 4 | Asks how Earn Together works | Interpret activity rules; do not recommend activity cards | Explain Earn Together participation steps, reward mechanism, and notes in detail |
| 5 | Asks how Help & Get Coupons works | Interpret activity rules; do not recommend activity cards | Explain Help & Get Coupons participation steps, reward mechanism, and notes in detail |
| 6 | Asks how Super Commission works | Interpret activity rules; do not recommend activity cards | Explain Super Commission participation steps, rebate mechanism, and notes in detail |
| 7 | Asks whether all three activities can be joined simultaneously | Interpret multi-activity participation rules | Explain simultaneous participation is allowed but referral relationship exclusivity constraints apply |

### C. Personalized Recommendation (8-10)

| Case | User Intent | Core Decision | Response Strategy |
|------|----------|----------|----------|
| 8 | Wants quick cash rewards | Match user need to the best-fitting activity | Recommend Earn Together → random cash vouchers |
| 9 | Wants trial vouchers / discount coupons | Match user need to the best-fitting activity | Recommend Help & Get Coupons → platform coupon rewards |
| 10 | Wants long-term passive income | Match user need to the best-fitting activity | Recommend Super Commission → ongoing trading fee rebates |

### D. FAQ and Boundaries (11-14)

| Case | User Intent | Core Decision | Response Strategy |
|------|----------|----------|----------|
| 11 | Asks why reward amounts differ | Address common misconception | Explain random reward generation mechanism |
| 12 | Asks when rewards will arrive | Address common misconception | Explain risk-control review process and 14-business-day timeline |
| 13 | Asks about specific task requirements (deposit/trading volume) | Guide to activity page | Explain that requirements vary by regional policy; check activity page |
| 14 | Queries activity data / reward progress | Communicate capability boundary | Inform that conversational data queries are not currently supported; redirect to Invite Friends page |

## Judgment Logic Summary

| Condition | Action |
|-----------|--------|
| User broadly asks "What referral activities are available?" | Check Earn Together status first; if active recommend Earn Together, otherwise recommend Help & Get Coupons + Super Commission |
| User asks about a specific activity's rules | Interpret the corresponding activity rules; do not recommend activity cards |
| User expresses a specific need (quick cash / coupons / long-term income) | Match and recommend the best-fitting activity |
| User asks reward-related FAQ | Use the standard answers from the Common Misconceptions table |
| User asks about activity data or progress | Inform that conversational queries are not supported; redirect to activity page |
| User asks about agent/institutional accounts | Clearly state that referral activities do not apply; redirect to business partnership contacts |
| User asks about specific deposit/trading volume requirements | Explain that requirements vary by region; redirect to activity page |
| User asks whether multiple activities can be joined simultaneously | Confirm yes, but note the referral relationship exclusivity rule |

## Report Template

```markdown
## Invite Friends Activity Recommendation

| Item | Details |
|------|---------|
| Activity Name | {activity_name} |
| Activity Type | {activity_type} |
| How to Participate | {participation_steps} |
| Reward Description | {reward_description} |
| Activity Page | https://www.gate.com/referral |

{additional_notes}
```

## Capability Boundaries

### Supported

- Activity recommendation and introduction: Recommend suitable referral activities based on user needs
- Activity comparison: Explain the differences and characteristics of the three activities
- Rule interpretation: Explain participation steps for each activity (do not recommend activity cards when interpreting rules)
- Task description: Describe task requirements (simplified version)
- FAQ answering
- Activity selection advice: Recommend the best-fitting activity based on user needs

### Not Supported

- Activity data queries (number of invitees, reward amounts, etc.) → Redirect to Invite Friends page
- Reward progress queries → Redirect to Invite Friends page
- Agent/institutional account applications → Redirect to business partnership contacts

## Error Handling

| Error Type | Typical Cause | Handling Strategy |
|----------|----------|----------|
| Earn Together status unknown | Unable to determine if an Earn Together campaign is active | Recommend Help & Get Coupons + Super Commission as fallback; inform user to check the Invite Friends page (https://www.gate.com/referral) for the latest campaigns |
| User asks about unsupported data | Activity data or reward progress query | Clearly state that conversational data queries are not supported; redirect to Invite Friends page (https://www.gate.com/referral) |
| Agent/institutional user detected | User is an agent or institutional account holder | Clearly inform that referral activities do not apply to agents/institutions; redirect to business partnership contacts |
| Region-restricted user | User IP or KYC region is on the restricted list | Inform the user that participation is not available in their region |
| Ambiguous user intent | Cannot determine which activity the user is asking about | Ask a clarifying question to narrow down intent before recommending |

## Safety Rules

- **Disclaimer**: Fake accounts, fraudulent transactions, and similar abuse are strictly prohibited; violators will be disqualified from receiving rewards
- **Identity restriction**: Agents and institutional users are not eligible for referral activities
- **Regional restriction**: Identify user IP or KYC region; if on the restricted list, inform the user that participation is not available
- Do not promise specific reward amounts (rewards are randomly generated)
- Do not bypass guidance by providing specific deposit/trading volume requirements (vary by region)
- All activity data query requests must be redirected to the Invite Friends page
