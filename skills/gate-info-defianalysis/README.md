# gate-info-defianalysis

## Overview

An AI Agent skill for **DeFi ecosystem analysis** via Gate-Info MCP. Intent recognition routes to **sub-scenarios** (overview, single platform, yield pools, stablecoins, bridges, exchange reserves, liquidation heatmap). Each scenario calls only the tools listed for that path; **progressive loading** for bridges and stablecoins (list first, detail on follow-up). Tools are scenario-dependent — see SKILL.md. Read-only.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **DeFi overview** | Total TVL, DEX volume, fees, top protocols by TVL | "DeFi overview" / "top DeFi protocols by TVL" |
| **Platform deep-dive** | Single protocol metrics + history + native token context | "Uniswap TVL" / "Aave metrics" |
| **Yield / stablecoins / bridges / reserves / liquidation** | Yield pools, stablecoin info, bridge metrics, exchange reserves, liquidation heatmap | "USDC APY on Aave" / "BTC liquidation heatmap" |
| **Routing** | Pure coin fundamentals without DeFi → `gate-info-coinanalysis`; broad market → `gate-info-marketoverview` | Per SKILL.md Routing Rules |

### Routing

| User intent | Action |
|-------------|--------|
| DeFi / TVL / yield / stablecoins / bridges / reserves / liquidation | Execute this skill (matching sub-scenario) |
| Analyze one coin only (no DeFi focus) | Route to `gate-info-coinanalysis` |
| Overall crypto market | Route to `gate-info-marketoverview` |

### Architecture

- **Input**: User message; extract optional `platform_name`, `symbol`, `chain`, `exchange` per SKILL.md.
- **Tools**: By sub-scenario — `info_platformmetrics_*` family and `info_coin_get_coin_info` when needed; never call tools outside the active scenario.
- **Output**: Sub-scenario report templates (A–G), **Error Handling**, **Cross-Skill Routing**, **Safety** (no yield guarantees, smart-contract risk, neutrality) — see SKILL.md.

## Documentation

- `SKILL.md` — Tools, execution workflow, report templates, Trigger update, routing.
- `references/scenarios.md` — Scenario prompts and expected behavior (for testing and QA).

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
