# gate-info-macroimpact

## Overview

An AI Agent skill for **macro-driven crypto context** using **Gate-Info** and **Gate-News** MCP. On macro-related questions (CPI, NFP, Fed, rates, economic calendar), it runs **economic calendar**, **macro indicator or summary**, **related news**, and **market snapshot** for a correlated coin (default BTC) **in parallel**, then the LLM outputs a structured correlation analysis. **Read-only.**

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Macro impact** | Link releases/events to crypto price narrative | "CPI and BTC" / "Fed meeting impact" |
| **Calendar mode** | Upcoming macro events in a window | "Any macro data today" |
| **Indicator mode** | Latest/previous/forecast-style framing when data exists | "What's the latest CPI" |
| **Four-pillar fetch** | Calendar + indicator (or macro summary) + news + market snapshot | Per SKILL.md parallel table |

### Routing (when NOT to use)

| Intent | Route instead |
|--------|----------------|
| Pure coin analysis (no macro angle) | `gate-info-coinanalysis` |
| Market-wide overview | `gate-info-marketoverview` |
| General crypto headlines | `gate-news-briefing` |
| Attribution / "why did price move" | `gate-news-eventexplain` |
| Price/technicals-only | `gate-info-trendanalysis` or coin analysis skill |

### Architecture

- **Input**: `event_keyword`, optional `coin`, `time_range` per SKILL.md; if the macro event cannot be identified, clarify with the user.
- **Tools** (read-only): `info_macro_get_economic_calendar`, `info_macro_get_macro_indicator`, `info_macro_get_macro_summary` (when no specific indicator), `news_feed_search_news`, `info_marketsnapshot_get_market_snapshot`.
- **Flow**: Intent check → parameter extraction → parallel MCP → LLM aggregation (surprise vs forecast, correlation, news context). **Report template**, **Decision Logic**, **Error Handling**, **Safety** — see `SKILL.md`.
- **MCP**: Gate-Info + Gate-News required. **API key**: not required per SKILL.md. Install via IDE installer skills.
- **Skill updates**: `scripts/update-skill.sh` / `update-skill.ps1`; blocking update flow per `SKILL.md` and `info-news-runtime-rules.md`. Host needs **Bash** or **PowerShell** when running scripts.
- **Verification scenarios**: `references/scenarios.md`.

## Runtime prerequisites

- **Skill self-update**: **Bash 3+** or **Windows PowerShell** for `scripts/update-skill.sh` / `update-skill.ps1`; sandboxed agents may need host-approved permissions for `apply`.
- **Typical install roots**: `~/.cursor/skills/gate-info-macroimpact/`, `~/.codex/skills/gate-info-macroimpact/`, etc. — see `SKILL.md` **Trigger update**.
- **MCP**: **Gate-Info** and **Gate-News** required per `SKILL.md`; install via IDE installer skills. No user API key required for documented read-only tools.

## Outbound network & documentation

| URL / pattern | Purpose |
|---------------|---------|
| Local file `../gate-runtime-rules.md` | Runtime rules (**General Rules**). |
| Local file `../info-news-runtime-rules.md` | Info/news runtime rules. |
| `https://raw.githubusercontent.com/gate/gate-skills/master/skills/<skill-name>/SKILL.md` | Version **check** vs remote `SKILL.md`. |
| `https://github.com/gate/gate-skills` | Repo / install references. |

`apply` may use `git` / `curl` / archives per `info-news-runtime-rules.md` §1.

## Data flow & privacy

- **AI interaction data**: Host LLM/agent processes user text; this skill directs **read-only** MCP calls to **Gate-Info** and **Gate-News** only (named tools in `SKILL.md`). No additional third-party data brokers are specified beyond MCP and documented update flows.
- **Credentials**: None required for documented tools per `SKILL.md`; host MCP config may add its own auth.
- **Minimization**: Use only calendar/indicator/news/snapshot parameters required for the query.

## Age & eligibility

Macro and crypto market content is for users **18+** with **full civil capacity**. Not personalized investment, tax, or legal advice.

## Marketplace alignment (ClawHub / registry)

Before publishing, align **manifest** credentials and MCP declarations with `SKILL.md` and this README (requires both Gate-Info and Gate-News).

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
- **Issues / feedback**: use the repository’s issue tracker for this skill package.
