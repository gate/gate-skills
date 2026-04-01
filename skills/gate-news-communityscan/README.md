# gate-news-communityscan

## Overview

An AI Agent skill for **community sentiment** via **Gate-News MCP**, **X/Twitter-first**. It runs `news_feed_search_x` and `news_feed_get_social_sentiment` **in parallel**, then the LLM synthesizes narratives, KOL themes, and quantitative sentiment. **Reddit / Discord / Telegram (UGC)** are **not** available yet — outputs must be labeled **X/Twitter only** per SKILL.md. **Read-only.**

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Community opinion** | Qualitative X discussion + optional sentiment metrics | "What does the community think about ETH" |
| **KOL / narrative scan** | Twitter/X angles and themes | "KOL views on ETF" |
| **Social sentiment** | Aggregated sentiment when `coin` is specified | "Market social sentiment" |

### Routing (when NOT to use)

| Intent | Route instead |
|--------|----------------|
| General crypto news feed | `gate-news-briefing` |
| Coin fundamentals report | `gate-info-coinanalysis` |
| Price attribution / event explain | `gate-news-eventexplain` |
| Deep research bundle | `gate-info-research` (if available) |

### Architecture

- **Input**: Optional `coin`, `topic`; `query` built for X search per SKILL.md.
- **Tools** (read-only): `news_feed_search_x`, `news_feed_get_social_sentiment`.
- **Flow**: Intent check → parameters → parallel tools → LLM aggregation (narratives vs sentiment, divergence notes). **Known limitations** (UGC offline), **Report template**, **Error Handling**, **Safety** — see `SKILL.md`.
- **MCP**: Gate-News required. **API key**: not required per SKILL.md. Install via IDE installer skills.
- **Skill updates**: `scripts/update-skill.sh` / `update-skill.ps1`; blocking update flow per `SKILL.md` and `info-news-runtime-rules.md`. Host needs **Bash** or **PowerShell** when running scripts.
- **Verification scenarios**: `references/scenarios.md`.

## Runtime prerequisites

- **Skill self-update**: **Bash** or **Windows PowerShell**; sandbox **full / all permissions** may be needed for `apply`.
- **Typical install roots**: `~/.cursor/skills/gate-news-communityscan/`, etc. — see `SKILL.md` **Trigger update**.
- **MCP**: **Gate-News** required per `SKILL.md`. No user API key for documented read-only tools.

## Outbound network & documentation

| URL / pattern | Purpose |
|---------------|---------|
| `https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md` | Runtime rules (**General Rules**). |
| `https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md` | Info/news runtime rules. |
| `https://raw.githubusercontent.com/gate/gate-skills/master/skills/<skill-name>/SKILL.md` | Version **check**. |
| `https://github.com/gate/gate-skills` | Repo references. |

X/Twitter-related tool behavior depends on **Gate-News** upstream (see `SKILL.md`).

## Data flow & privacy

- **AI interaction data**: Host LLM processes user text; **read-only** **Gate-News** tools `news_feed_search_x` and `news_feed_get_social_sentiment` per `SKILL.md`. No extra third-party endpoints beyond MCP and documented update/rules fetches.
- **Credentials**: Not required per `SKILL.md` for documented tools.
- **Minimization**: Use coin/topic/query parameters appropriate to the question.

## Age & eligibility

Social sentiment and crypto discussion: **18+**, full civil capacity. Not investment advice.

## Marketplace alignment (ClawHub / registry)

Before publishing, align **manifest** with `SKILL.md` **MCP Dependencies** (Gate-News) and this README.

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
- **Issues / feedback**: use the repository’s issue tracker for this skill package.
