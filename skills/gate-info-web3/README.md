# gate-info-web3

## Overview

Umbrella primary skill for **Web3 / on-chain / protocol behavior** via `gate-cli`. **DeFi is only one subdomain** — this skill also covers address activity, token flows and smart-money signals, entity-style questions, exchange reserves, liquidation heatmaps, stablecoins, and bridges. The legacy name **`gate-info-defianalysis`** is a **narrow alias** for old routing; the canonical id is **`gate-info-web3`**.

## Runtime requirements

- **CLI**: `gate-cli` v0.5.2 on `PATH`.
- **Shell** (optional): `bash` / `powershell` if you run packaged `scripts/update-skill.*` manually.
- **Network**: outbound calls as required by `gate-cli` and configured credentials.

## Core capabilities

| Capability | Typical trigger | Playbook id |
|------------|-----------------|-------------|
| Address tracking / “who is this wallet” | "track this address", "who owns this wallet" | `address_tracking` |
| Token on-chain / flows / smart money on a token | "on-chain flows for ETH", "smart money on this token" | `token_onchain` |
| Named entity / desk | "what is Jump Trading doing lately" | `entity_intel` |
| Protocol TVL, yield, platform profile | "Uniswap TVL", "USDC supply yield on Aave" | `protocol_platform` |
| Exchange reserves | "exchange BTC reserves" | `exchange_reserves` |
| Liquidation heatmap | "BTC liquidation density by price" | `liquidation_heatmap` |
| Stablecoins + bridges (market structure) | "stablecoin market share", "bridge rankings" | `stablecoin_bridge` |
| On-chain + news/social in one pass | "on-chain plus community mood" | `token_onchain_social` |

Execution uses **real v0.5.2 commands** only — see [playbooks/gate-info-web3.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-info-web3.yaml). Aspirational one-shots (`+address-tracker`, `+token-onchain`, `get-entity-profile`, `trace-fund-flow`) are recorded as `cli_future_shortcut` only.

## Inputs / outputs

- **Input**: natural language + slots per playbook (`address`+`chain`, `token`+`chain`, `platform`, `exchange`+`asset`, `symbol`, `entity_query`, etc.).
- **Output**: six-section report in the user’s locale (see `SKILL.md` template for section titles).

## Routing (when NOT to use)

| Intent | Route to |
|--------|----------|
| Safety verdict, honeypot, blacklist, compliance-first | `gate-info-risk` |
| Broad research (fundamentals, macro, multi-coin) without on-chain framing | `gate-info-research` |
| Pure narrative / “why crash” / community-only | `gate-news-intel` |

Full matrix: [skills/_shared/routing.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/routing.md).

## Acceptance criteria

1. Preflight contract ([skills/_shared/preflight.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/preflight.md)).
2. Every invoked `gate-cli` subcommand appears under `gate-cli info list` / `gate-cli news list` for v0.5.2.
3. Report keeps the six headings; separates **on-chain facts** from **community / media** lines.
4. Copy does not collapse the skill into “DeFi-only”; Web3 umbrella framing is explicit when multiple subdomains appear.

## Source

- **Skill spec**: [SKILL.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-web3/SKILL.md)
- **Playbook**: [playbooks/gate-info-web3.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-info-web3.yaml)
- **References**: [skills/gate-info-web3/references/](https://github.com/gate/gate-skills/tree/master/skills/gate-info-web3/references) under this skill directory
