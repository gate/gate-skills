# gate-info-tokenonchain

## Overview

An AI Agent skill for **token-level on-chain analysis** via **Gate-Info MCP**: **holder distribution**, **on-chain activity**, and **large/unusual transfers** (`scope`: holders / activity / transfers, combinable). It calls `info_onchain_get_token_onchain` and `info_coin_get_coin_info` **in parallel**, then aggregates into the report template in SKILL.md. **Smart Money** and related scopes are **not** available in this version — SKILL.md instructs the agent to say so clearly. **Read-only.**

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Holders** | Distribution / top-holder style on-chain view | "ETH holder distribution" |
| **Activity** | Active addresses / transaction activity | "BTC on-chain activity" |
| **Transfers** | Large or unusual transfers | "Whale movements" / "large transfers" |
| **Combined overview** | Multiple scopes in one pass | "SOL on-chain analysis" |

### Routing (when NOT to use)

| Intent | Route instead |
|--------|----------------|
| **Single address** tracking | `gate-info-addresstracker` |
| Fundamentals + technicals + news bundle | `gate-info-coinanalysis` or `gate-info-research` (if available) |
| Entity/whale profiling when not supported | Inform user; `gate-info-whaletracker` if available |

### Architecture

- **Input**: Required `symbol`; optional `chain`, `scope` (`holders` / `activity` / `transfers`; not `smart_money`), `time_range` per SKILL.md.
- **Tools** (read-only): `info_onchain_get_token_onchain`, `info_coin_get_coin_info` (`scope=basic`).
- **Flow**: Intent check → extract params → parallel tools → LLM aggregation (patterns, anomalies, no price guarantees). **Known limitations** (Smart Money, entity profiling), **Report template**, **Error Handling**, **Safety** — see `SKILL.md`.
- **MCP**: Gate-Info required. **API key**: not required per SKILL.md. Install via IDE installer skills.
- **Skill updates**: `scripts/update-skill.sh` / `update-skill.ps1`; blocking update flow per `SKILL.md` and `info-news-runtime-rules.md`. Host needs **Bash** or **PowerShell** when running scripts.
- **Verification scenarios**: `references/scenarios.md`.

## Runtime prerequisites

- **Skill self-update**: **Bash** or **Windows PowerShell**; sandboxed agents may need host-approved permissions for `apply`.
- **Typical install roots**: `~/.cursor/skills/gate-info-tokenonchain/`, etc. — see `SKILL.md` **Trigger update**.
- **MCP**: **Gate-Info** required; installer skills per `SKILL.md`. No user API key for documented read-only tools.

## Outbound network & documentation

| URL / pattern | Purpose |
|---------------|---------|
| Local file `../gate-runtime-rules.md` | Runtime rules (**General Rules**). |
| Local file `../info-news-runtime-rules.md` | Info/news runtime rules. |
| `https://raw.githubusercontent.com/gate/gate-skills/master/skills/<skill-name>/SKILL.md` | Version **check**. |
| `https://github.com/gate/gate-skills` | Repo references. |

## Data flow & privacy

- **AI interaction data**: Host agent processes prompts; **read-only** **Gate-Info** MCP calls (`info_onchain_get_token_onchain`, `info_coin_get_coin_info`) per `SKILL.md`. Outputs are LLM summaries of tool data; no undeclared third-party APIs.
- **Credentials**: Not required per `SKILL.md` for documented tools.
- **Minimization**: Pass symbol, chain, scope, and time range only as needed.

## Age & eligibility

On-chain and digital-asset topics: **18+**, full civil capacity. Informational only.

## Marketplace alignment (ClawHub / registry)

Before publishing, align **manifest** with `SKILL.md` **MCP Dependencies** (Gate-Info) and this README.

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
- **Issues / feedback**: use the repository’s issue tracker for this skill package.
