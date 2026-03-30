# gate-info-tokenonchain

## Overview

An AI Agent skill for **token-level on-chain analysis** (holders, activity, large transfers) via Gate-Info MCP. Calls `info_onchain_get_token_onchain` and `info_coin_get_coin_info` **in parallel**, then aggregates into a structured report. **Current limitation**: no Smart Money / `scope=smart_money` in this version — see SKILL.md **Known Limitations**. Read-only.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Holders / activity / transfers** | Scopes `holders`, `activity`, `transfers` (combine for full overview) | "ETH holder distribution" / "large transfers for SOL" |
| **Coin context** | Basic coin info alongside on-chain metrics | "On-chain analysis for BTC" |
| **Routing** | Specific **address** (0x…) → `gate-info-addresstracker`; coin fundamentals-only → `gate-info-coinanalysis` | Per SKILL.md |

### Routing

| User intent | Action |
|-------------|--------|
| Token on-chain metrics | Execute this skill with appropriate `scope` |
| Track one address | Route to `gate-info-addresstracker` |
| Smart Money (unsupported) | Inform user; run holders/activity/transfers only |
| Single-coin comprehensive fundamentals | Route to `gate-info-coinanalysis` |

### Architecture

- **Input**: Required `symbol`; optional `chain`, `scope`, `time_range` per SKILL.md.
- **Tools**: `info_onchain_get_token_onchain`, `info_coin_get_coin_info` only.
- **Output**: Report template (overview, per-scope sections, insights), **Decision Logic**, **Error Handling**, **Cross-Skill**, **Safety** — see SKILL.md.

## Documentation

- `SKILL.md` — Tools, execution workflow, report templates, Trigger update, routing.
- `references/scenarios.md` — Scenario prompts and expected behavior (for testing and QA).

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
