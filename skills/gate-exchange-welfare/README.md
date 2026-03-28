# gate-exchange-welfare

## Overview

Gate Exchange welfare center new user task Skill (version 2026.3.18-6, with updated MCP tools integration). Triggered when users ask about welfare benefits, new user rewards, or available tasks. **Core Logic**: Call interface to determine user identity (new vs existing) then branch processing—existing users receive direct guidance text (redirect to Web/App); new users call task query interface to return all new user onboarding tasks, displaying task title, subtitle, reward content, and action button text, with restriction condition prompts. Read-only operations, does not execute task claiming or reward distribution.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **User Type Detection** | Call interface to identify if user is new, determines subsequent branching | Any welfare/task query triggers this |
| **Existing User Guidance** | Existing users don't see new user tasks, unified guidance to Web/App welfare center | "What welfare do I have" → existing user → return guidance link |
| **New User Task List** | Return complete new user onboarding tasks: title, subtitle, rewards, action buttons | "What new user rewards are available" → new user → show task cards |
| **Exception Fallback** | Interface timeout / empty task list / not logged in / various user identity restrictions, all have corresponding fallback text | Risk control user → contact customer service prompt |

### Routing

| User Intent | Handling Method |
|-------------|-----------------|
| Query welfare / rewards / tasks | Execute this Skill |
| Query new user benefits / new user tasks | Execute this Skill |
| Want to complete "First Deposit" task | Route to deposit / funding Skill |
| Want to complete "First Trade" task | Route to `gate-exchange-spot` |
| Want to complete "Identity Verification" task | Guide to Web / App to complete KYC |
| Query asset balance | Route to `gate-exchange-assets` |

## Architecture

- **Input**: User asks about welfare, tasks, rewards related content, no additional parameters needed (user identity automatically retrieved by MCP tools).
- **Tools**:
  - Step 1: `cex_welfare_get_user_identity` (User type determination interface) → Check if current user qualifies for new user benefits. Returns code=0 indicating qualification, or specific error codes (1001=existing user, 1002=risk control, 1003=sub-account, 1004=agent, 1005=market maker, 1006=enterprise, 1008=not logged in)
  - Step 2 (new users only): `cex_welfare_get_beginner_task_list` (Query beginner guidance task list) → Get beginner guidance task list, including registration tasks (type=10) and guidance tasks (type=11), each task contains reward information, completion status and task description
- **Output**: Existing user guidance text / New user task card list + restriction condition prompts. Detailed response templates, exception handling, cross-Skill integration rules see SKILL.md; complete scenario examples see references/scenarios.md.

### Scope

This Skill covers the following scenarios:
- Case 1: Existing user query → Guide to Web / App
- Case 2: New user query → Show new user task list
- Exception handling: Covers all user identity restrictions and system exception situations (error codes 1001-1008)

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
