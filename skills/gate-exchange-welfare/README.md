# gate-exchange-welfare

## Overview

Gate Exchange welfare center newcomer skill (version `2026.4.10-1`). It covers the phase-2 newcomer workflow end to end: user identity detection, newcomer task list retrieval, single task claim, newcomer reward claim, and generic completion guidance for KYC / first deposit / first trade flows. The skill must use real `gate-cli` data and current business codes; it must never invent task or reward information.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **User Type Detection** | Calls the identity endpoint before any newcomer action | "What welfare tasks can I do?" |
| **Newcomer Task List** | Returns all current newcomer tasks with real reward info and current task status | "Show my new user tasks" |
| **Single Task Claim** | Claims a selected status=`0` newcomer task, mainly the download task flow | "Claim the download task" |
| **Reward Claim** | Claims all currently claimable newcomer rewards by iterating status=`2` tasks | "Claim all my newcomer rewards" |
| **Completion Guidance** | Guides KYC / first deposit / first trade completion without fabricating thresholds | "How do I finish the first deposit task?" |
| **Restriction Fallback** | Handles old user / no-login / risk-control / task-empty / reward-edge cases | Existing user → rewards-hub guidance |

### Routing

| User Intent | Handling Method |
|-------------|-----------------|
| Query welfare / newcomer rewards / newcomer tasks | Execute this skill |
| Claim a newcomer task | Execute this skill |
| Claim newcomer rewards | Execute this skill |
| Complete identity verification task | Return generic KYC guidance |
| Complete first deposit task | Return generic deposit guidance |
| Complete first trade task | Route to `gate-exchange-trading` |
| Query asset balance | Route to `gate-exchange-assets` |

## Architecture

- **Input**: Welfare/task/reward/claim/completion intent related to the newcomer welfare center.
- **Tools**:
  - `gate-cli cex welfare identity`
  - `gate-cli cex welfare beginner-tasks`
  - `cex_welfare_claim_task` (no `gate-cli` mapping; see `gate-cli/cmd/cex/MCP_LEGACY_TOOL_RESOLUTION.md` §二)
  - `cex_welfare_claim_reward` (no `gate-cli` mapping; see `gate-cli/cmd/cex/MCP_LEGACY_TOOL_RESOLUTION.md` §二)
- **Execution model**:
  - Step 1: Identity gate
  - Step 2: Task list lookup when newcomer flow is allowed
  - Step 3: Branch into list / claim task / completion guidance / claim reward
  - Step 4: Map business `code` values and task `status` values to user-facing handling
- **Response model**: Existing-user guidance, newcomer task list, task-claim success, reward-claim summary, or generic completion guidance.

### Status Semantics

| Status | Meaning | Typical action |
|--------|---------|----------------|
| `0` | Unclaimed task | Claim task |
| `1` | Claimed / in progress | Complete the task |
| `2` | Completed, reward claimable | Claim reward |
| `3` | Reward distributing | Wait |
| `4` | Completed / settled | No further action |
| `5` | Expired | No further action |

### Scope

This skill covers:
- Existing-user / restricted-user welfare handling
- Newcomer task list lookup
- Single newcomer task claim
- Newcomer reward claim
- Generic completion guidance for KYC, deposit, and first-trade task flows

This skill does **not** cover:
- Deposit execution itself
- Trading execution itself
- Non-welfare account operations

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
