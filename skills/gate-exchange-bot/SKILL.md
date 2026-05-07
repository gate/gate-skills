---
name: gate-exchange-bot
version: "2026.5.6-5"
updated: "2026-05-06"
description: "Gate Exchange AI bot skill. Use this skill whenever the user wants AIHub strategy recommendation, manual spot/margin/infinite/futures grid creation, manual spot/contract martingale creation, or running strategy portfolio query and stop flows. Trigger phrases include recommend strategy, spot grid, futures grid, martingale, running bots, bot detail, and stop bot."
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    emoji: "💱"
    os:
      - darwin
      - linux
    primaryEnv: GATE_API_KEY
    requires:
      bins:
        - gate-cli
      env:
        - GATE_API_KEY
        - GATE_API_SECRET

    install:
      - kind: download
        os:
          - linux
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_linux_amd64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (Linux x64)"
      - kind: download
        os:
          - linux
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_linux_arm64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (Linux arm64)"
      - kind: download
        os:
          - darwin
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_darwin_amd64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (macOS Intel)"
      - kind: download
        os:
          - darwin
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_darwin_arm64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (macOS Apple Silicon)"
---

# Gate Exchange Bot

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.
- **Only use the `gate-cli` subcommands explicitly listed in this skill and its references.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

## Authoring Language

This skill is authored in English. End-user replies should still follow normal language adaptation.

## Skill Dependencies

### gate-cli commands used

**Query Operations (Read-only)**

- `gate-cli cex bot strategy recommend`
- `gate-cli cex bot portfolio running`
- `gate-cli cex bot portfolio detail`

**Execution Operations (Write)**

- `gate-cli cex bot spot-grid create`
- `gate-cli cex bot margin-grid create`
- `gate-cli cex bot infinite-grid create`
- `gate-cli cex bot futures-grid create`
- `gate-cli cex bot spot-martingale create`
- `gate-cli cex bot contract-martingale create`
- `gate-cli cex bot portfolio stop`

### MCP-backed command mapping

| `gate-cli` command | Backing bot capability |
|---|---|
| `gate-cli cex bot strategy recommend` | `cex_bot_get_ai_hub_strategy_recommend` |
| `gate-cli cex bot portfolio running` | `cex_bot_get_ai_hub_portfolio_running` |
| `gate-cli cex bot portfolio detail` | `cex_bot_get_ai_hub_portfolio_detail` |
| `gate-cli cex bot spot-grid create` | `cex_bot_post_ai_hub_spot_grid_create` |
| `gate-cli cex bot margin-grid create` | `cex_bot_post_ai_hub_margin_grid_create` |
| `gate-cli cex bot infinite-grid create` | `cex_bot_post_ai_hub_infinite_grid_create` |
| `gate-cli cex bot futures-grid create` | `cex_bot_post_ai_hub_futures_grid_create` |
| `gate-cli cex bot spot-martingale create` | `cex_bot_post_ai_hub_spot_martingale_create` |
| `gate-cli cex bot contract-martingale create` | `cex_bot_post_ai_hub_contract_martingale_create` |
| `gate-cli cex bot portfolio stop` | `cex_bot_post_ai_hub_portfolio_stop` |

### Authentication

- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard for API key, secret, profiles, and defaults (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** **`gate-cli config init`** is not required when credentials are already supplied — for example when **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** are set on the host, or when **`--api-key`** / **`--api-secret`** are supported. Never ask the user to paste secrets into chat.
- API Key Required: Yes
- **Permissions:** Bot:Read, Bot:Write
- **Portal:** create or rotate keys outside the chat: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check

- **Required:** `gate-cli`. Run `sh setup.sh` from this skill directory if it is missing. Optional: `GATE_CLI_SETUP_MODE=release`.
- Add `$HOME/.openclaw/skills/bin` to **`PATH`** if you invoke `gate-cli` by name.
- **Host dependencies for `setup.sh`:** `curl`, `tar`, and either `shasum` or `sha256sum`. If user-local installation fails, `setup.sh` may fall back to `sudo install` into `/usr/local/bin`.
- **Credentials:** When **`GATE_API_KEY`** and **`GATE_API_SECRET`** are both set (non-empty) for the host, do not require `gate-cli config init`. When both are unset or empty, remind the operator to run `gate-cli config init` or configure matching environment variables outside chat.
- **Sanity check:** Before any mutating call, confirm the CLI behaves as expected with a read-only probe such as `gate-cli --version` or `gate-cli cex bot strategy recommend --help`.

### Resolving `gate-cli` (binary path)

Resolve **`gate-cli`** in order: **(1)** **`command -v gate-cli`** and **`gate-cli --version`** succeeds; **(2)** **`${HOME}/.local/bin/gate-cli`** if executable; **(3)** **`${HOME}/.openclaw/skills/bin/gate-cli`** if executable. Canonical rules: [`exchange-runtime-rules.md`](https://github.com/gate/gate-skills/blob/master/skills/exchange-runtime-rules.md) §4 (or [`gate-runtime-rules.md`](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) §4).

## Execution

Read and strictly follow `references/gate-cli.md`, then execute the matched route in this `SKILL.md`.

- `SKILL.md` keeps intent routing, safety policy, and product boundaries.
- `references/gate-cli.md` is the authoritative execution contract for command probing, `body` payload handling, confirmation gates, and verification.
- `references/scenarios.md` provides scenario-style examples for review, testing, and publication completeness.

## Domain Knowledge

- Strategy recommendation is read-only and must stay separate from creation.
- Grid and martingale flows require different payload schemas and must not share fields across products.
- Running-strategy stop is always a single-strategy action; bulk stop is out of scope.
- Percentage-style business inputs must be normalized into decimal ratio strings before any write command.
- Portfolio detail and stop flows depend on an exact `strategy_id` plus the correct `strategy_type`.

## Module Overview

| Module | Description | Trigger keywords |
|--------|-------------|------------------|
| **Discover** | Recommend AIHub bot strategies by market, strategy type, filter, or refresh context | `recommend strategy`, `bundle`, `top1`, `refresh recommendation`, `filter strategy` |
| **Spot Grid** | Manual spot grid creation | `spot grid`, `manual grid` |
| **Margin Grid** | Manual margin grid creation | `margin grid` |
| **Infinite Grid** | Manual infinite grid creation | `infinite grid` |
| **Futures Grid** | Manual futures grid creation | `futures grid`, `contract grid` |
| **Spot Martingale** | Manual spot martingale creation | `spot martingale` |
| **Contract Martingale** | Manual contract martingale creation | `contract martingale`, `futures martingale` |
| **Portfolio List** | List running strategies | `running strategies`, `bots I have running`, `portfolio running` |
| **Portfolio Detail** | Query a single strategy detail | `strategy detail`, `bot detail`, `P&L detail` |
| **Portfolio Stop** | Stop one running strategy | `stop strategy`, `stop bot` |

## Routing Rules

| Intent | Example phrases | Route to |
|--------|-----------------|----------|
| **Strategy recommendation** | "Recommend a BTC strategy", "Give me a spot grid recommendation", "Refresh that recommendation" | Read `references/strategy-recommend.md` |
| **Spot grid create** | "Create a BTC spot grid from 60000 to 72000 with 50 grids and 1000 USDT" | Read `references/create-spot-grid.md` |
| **Margin grid create** | "Create a margin grid with 3x leverage and 50 grids" | Read `references/create-margin-grid.md` |
| **Infinite grid create** | "Create a BTC infinite grid with 1.5% profit per grid" | Read `references/create-infinite-grid.md` |
| **Futures grid create** | "Create a BTC futures grid with 5x leverage and neutral direction" | Read `references/create-futures-grid.md` |
| **Spot martingale create** | "Create a spot martingale that adds after a 2% drop" | Read `references/create-spot-martingale.md` |
| **Contract martingale create** | "Create a contract martingale, 5x leverage, short bias" | Read `references/create-contract-martingale.md` |
| **Running list** | "What bots do I have running?" | Read `references/list-running.md` |
| **Strategy detail** | "Show me that bot's detailed P&L" | Read `references/get-detail.md` |
| **Stop strategy** | "Stop that BTC grid bot" | Read `references/stop-strategy.md` |

## gate-cli Command Index

| # | Command | Purpose |
|---|---------|---------|
| 1 | `gate-cli cex bot strategy recommend` | Discover recommendations for `top1`, `bundle`, `filter`, or `refresh` scenes |
| 2 | `gate-cli cex bot spot-grid create` | Create a manual spot grid |
| 3 | `gate-cli cex bot margin-grid create` | Create a manual margin grid |
| 4 | `gate-cli cex bot infinite-grid create` | Create a manual infinite grid |
| 5 | `gate-cli cex bot futures-grid create` | Create a manual futures grid |
| 6 | `gate-cli cex bot spot-martingale create` | Create a manual spot martingale |
| 7 | `gate-cli cex bot contract-martingale create` | Create a manual contract martingale |
| 8 | `gate-cli cex bot portfolio running` | List running strategies |
| 9 | `gate-cli cex bot portfolio detail` | Query a single strategy detail |
| 10 | `gate-cli cex bot portfolio stop` | Stop one strategy |

## Execution Workflow

### 1. Intent classification

- Determine whether the request is **discover**, **manual create**, or **portfolio**.
- For manual create, resolve the exact bot type before reading the reference file.
- For portfolio, resolve whether the user wants **list**, **detail**, or **stop**.

### 2. Parameter discipline

- Recommendation flows use query-style parameters only.
- Create and stop flows pass the final business payload through **`body`** as a JSON string.
- Any percentage-style input must be normalized exactly as required by the matched reference document before a write command is executed.

### 3. Scenario coverage

- Use `references/scenarios.md` as the publication-facing scenario index.
- Use the module-specific reference files as the source of detailed parameter and guardrail rules.

## Safety Rules

### Confirmation

- Recommendation and read-only portfolio queries do not require confirmation.
- Every write path must first present an action draft or confirmation summary.
- Each create or stop action must be confirmed separately by the user in the immediately following turn.
- If the user does not explicitly confirm, do not execute the write command.

### Verification

- Do not judge success from HTTP `200` alone.
- Always inspect the returned payload `code`, `message`, and key `data` fields.
- If a write fails, return the backend `message` faithfully rather than inventing thresholds or hidden restrictions.

## Error Handling

- Authentication or permission failure: stop writes and direct the operator to `gate-cli config init` or host-side credential recovery.
- Missing or ambiguous business inputs: ask only for the missing fields; do not guess them.
- Invalid backend payload or business-rule rejection: surface the backend `message` and keep the flow blocked until corrected.
- Ambiguous stop target: switch to running-list selection before attempting a stop.

## Data and Privacy

- User prompts, strategy parameters, and command payloads flow through the host runtime, `gate-cli`, and Gate APIs needed for the requested bot action.
- This skill does not define any extra telemetry, analytics, or custom persistence mechanism of its own.
- Local shell history, terminal logs, or host-side audit logs may still exist depending on the operator environment.
- Never ask the user to paste API secrets into chat. Credentials should be configured via `gate-cli config init` or equivalent secure host-side environment management.

## Important Boundaries

- Do not turn education-only or consultation-only questions into writes.
- Do not guess core strategy parameters such as range, grid count, leverage, direction, martingale deviation, or stop-loss ratio.
- Bulk stop is not supported. Ambiguous stop requests must go through running-list selection and then single-strategy confirmation.
- Advanced running-strategy management beyond recommendation, create, list, detail, and single stop remains out of scope unless explicitly documented in a reference file.
