# gate-info-research

## Overview

Research-oriented primary skill for Gate.info + Gate.news, executed via `gate-cli`. Covers six analysis modes in one skill so the agent does not have to pick between five legacy MCP skills.

## Runtime requirements

- **CLI**: `gate-cli` v0.5.2 on `PATH` (see `gate-cli --version`).
- **Shell** (optional): `bash` or `powershell` only if you run `scripts/update-skill.sh` / `update-skill.ps1` for manual sync — not part of the default agent flow.
- **Config**: API keys / auth as required by your `gate-cli` profile (`gate-cli preflight`).

## Core capabilities

| Capability | Typical trigger | Playbook id |
|---|---|---|
| Single-coin comprehensive analysis | "analyze SOL" / "how is BTC" / "is ETH worth watching" | `single_coin` |
| Market overview | "market right now" / "how is the broad market" / "which sectors are hot" | `market_overview` |
| Multi-coin comparison | "compare BTC and ETH" / "BTC vs SOL vs ARB" | `multi_coin` |
| Trend / technical analysis | "BTC RSI" / "SOL MACD" / "price direction / TA" | `trend` |
| Macro impact | "CPI impact on markets" / "impact of NFP on BTC" | `macro` |
| Research + news synthesis | "analyze ETH with news and sentiment" | `research_plus_news` |

Every playbook uses real `gate-cli v0.5.2` lower-level commands — no aggregate `+shortcut` is assumed. See machine-readable contract in [playbooks/gate-info-research.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-info-research.yaml) and per-command flags in [skills/gate-info-research/references/cli-reference.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-research/references/cli-reference.md).

## Inputs / outputs

- **Input**: natural-language query. Required slot varies per playbook — typically one `symbol`, a list of `symbols`, or nothing (market-overview / macro).
- **Output**: six-section structured report in the user’s locale (executive summary, fundamentals, market/trend, news/sentiment, risks, watchlist — see `SKILL.md` template).

## Routing (when NOT to use)

| Intent | Route to |
|---|---|
| "Is this coin / address safe" | `gate-info-risk` |
| "Trace this address / smart money / TVL" | `gate-info-web3` |
| "Why did it crash / community take" | `gate-news-intel` |

Full cross-skill matrix: [skills/_shared/routing.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/routing.md).

## Acceptance criteria

1. Preflight contract followed ([skills/_shared/preflight.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/preflight.md)).
2. Every `gate-cli` command appears in `gate-cli info list` / `gate-cli news list`.
3. Report has all six sections in the required order (product requirements spec).
4. Missing data is labelled **no data**; it is never fabricated.

## Source

- **Skill spec**: [SKILL.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-research/SKILL.md) (this directory)
- **Playbook**: [playbooks/gate-info-research.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-info-research.yaml) (repository root)
- **References**: [references/scenarios.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-research/references/scenarios.md), [references/cli-reference.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-research/references/cli-reference.md), [references/troubleshooting.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-research/references/troubleshooting.md)
- **Repository**: `gate-github-skills` (internal); public skills often mirror `gate/gate-skills` layout.
