# gate-info-defianalysis

## Overview

An AI Agent skill for **DeFi ecosystem analysis** via **Gate-Info MCP**. It routes user intent into sub-scenarios (overview, single platform, yield pools, stablecoins, bridges, exchange reserves, liquidation heatmap), calls the documented `info_platformmetrics_*` tools (and `info_coin_get_coin_info` where needed) in parallel where applicable, then the LLM produces a structured report. **Read-only.** Coin-only fundamentals without a DeFi angle belong in `gate-info-coinanalysis`.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **DeFi overview** | Total TVL/volume/fees context and top platforms by TVL | "DeFi overview" / "TVL ranking" |
| **Platform deep-dive** | Full metrics + history + native token context | "Uniswap TVL" / "Aave metrics" |
| **Yield pools** | APY/TVL-ranked pools with risk framing | "USDC yield" / "best lending APY" |
| **Stablecoins & bridges** | Rankings first; detail-on-demand on follow-up | "USDT market cap" / "bridge volume" |
| **Exchange reserves** | On-chain reserve-style metrics per exchange/asset | "Binance BTC reserves" |
| **Liquidation heatmap** | Density by price range | "BTC liquidation heatmap" |

### Routing (when NOT to use)

| Intent | Route instead |
|--------|----------------|
| Single-coin fundamentals only (no DeFi focus) | `gate-info-coinanalysis` |
| Broad market snapshot | `gate-info-marketoverview` |
| Macro + crypto | `gate-info-macroimpact` |
| Research bundle (if available) | `gate-info-research` |

### Architecture

- **Input**: Optional `platform_name`, `symbol`, `chain`, `exchange` extracted per SKILL.md.
- **Tools** (only as listed in SKILL.md): `info_platformmetrics_get_defi_overview`, `info_platformmetrics_search_platforms`, `info_platformmetrics_get_platform_info`, `info_platformmetrics_get_platform_history`, `info_platformmetrics_get_yield_pools`, `info_platformmetrics_get_stablecoin_info`, `info_platformmetrics_get_bridge_metrics`, `info_platformmetrics_get_exchange_reserves`, `info_platformmetrics_get_liquidation_heatmap`, `info_coin_get_coin_info`.
- **Flow**: Intent → sub-scenario (A–G) → parallel MCP calls → LLM aggregation; bridges/stablecoins use list-first, detail-on-demand. **Report templates**, **Decision Logic**, **Error Handling**, **Cross-Skill Routing**, **Safety Rules** — see `SKILL.md`.
- **MCP**: Gate-Info required. **API key**: not required per SKILL.md. Install via IDE installer skills (`gate-mcp-cursor-installer`, etc.).
- **Skill updates**: `scripts/update-skill.sh` / `update-skill.ps1` compare local vs remote; blocking `check` / user confirm / `apply` per `SKILL.md` and `info-news-runtime-rules.md`. Host needs **Bash** (macOS/Linux/WSL/Git Bash) or **PowerShell** (Windows) when running scripts.
- **Verification scenarios**: `references/scenarios.md` (happy path, degradation, routing).

## Runtime prerequisites

- **Skill self-update** (`check` / `apply` in `SKILL.md`): the host must provide **Bash 3+** (macOS, Linux, WSL, Git Bash) **or** **Windows PowerShell** (execution policy may need bypass for `scripts/update-skill.ps1`). Sandboxed agents (e.g. Cursor) usually need **full / all permissions** to run `apply` when syncing from remote.
- **Typical install roots** (examples): `~/.cursor/skills/gate-info-defianalysis/`, `~/.codex/skills/gate-info-defianalysis/`, `~/.openclaw/skills/gate-info-defianalysis/` — see `SKILL.md` **Trigger update**.
- **MCP**: **Gate-Info** required; install via IDE installer skills. No user API key is required for the documented read-only tools per `SKILL.md`.

## Outbound network & documentation

Agents may retrieve documentation or version metadata over HTTPS. Review against corporate policy:

| URL / pattern | Purpose |
|---------------|---------|
| `https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md` | Shared runtime rules (**General Rules**). |
| `https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md` | Info/news runtime rules (version check UX, MCP install, degradation). |
| `https://raw.githubusercontent.com/gate/gate-skills/master/skills/<skill-name>/SKILL.md` | `update-skill` **check** compares local vs remote skill head. |
| `https://github.com/gate/gate-skills` | Canonical repo / skill tree references in runtime rules. |

The `apply` path in `update-skill` scripts may use `git`, `curl`, or archives as described in `info-news-runtime-rules.md` §1.

## Data flow & privacy

- **AI interaction data**: User prompts are processed by the host LLM/agent. This skill instructs **read-only** MCP calls to **Gate-Info** only (tools listed in `SKILL.md`). Responses combine tool output with model text; no extra third-party analytics endpoints are added by this skill’s documented workflow.
- **Credentials**: No API key is required for the documented tools per `SKILL.md`; any secrets live in the user’s MCP/host configuration.
- **Minimization**: Pass only parameters needed for the active sub-scenario (symbol, chain, limits, exchange names).

## Age & eligibility

Content covers **digital assets and DeFi**. Intended for users **aged 18 or above** with **full civil capacity** in their jurisdiction. Do not use for minors or as personalized investment advice.

## Marketplace alignment (ClawHub / registry)

Before publishing to a marketplace, reconcile **registry manifest** fields (required credentials, MCP scopes) with `SKILL.md` **MCP Dependencies** / **Authentication** and this README so listing metadata matches actual runtime needs.

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
- **Issues / feedback**: use the repository’s issue tracker for this skill package.
