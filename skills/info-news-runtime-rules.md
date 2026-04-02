# Info & News Common Runtime Rules

> Shared runtime rules for all `gate-info-*` and `gate-news-*` skills.
> Each skill's SKILL.md should include: Read and follow `../info-news-runtime-rules.md` first (path relative to `skills/<skill-name>/SKILL.md`; use inline code, not a relative markdown link — Skills Hub cannot resolve repo-relative links).

---

## 1. Skill version check & update

Before execution, check whether a newer version of the current skill exists in the official Gate Skills repository:
https://github.com/gate/gate-skills

- If the skill directory contains `scripts/update-skill.sh` (or `scripts/update-skill.ps1` on Windows), you may run the `check` subcommand to compare the local skill with the official repo.
- Version checks fetch the remote `SKILL.md` head via GitHub Raw URL: `https://raw.githubusercontent.com/gate/gate-skills/master/skills/{skill_name}/SKILL.md`
- In interactive sessions, `check` is optional maintenance. If it reports `update_available`, ask the user before running `apply`.
- Never auto-apply updates in chat or agent-driven interactive flows.
- If `check` cannot run or returns `check_failed`, continue with the currently installed version. Explain update-check details only when the user explicitly asks.
- Do not auto-download replacement updater scripts during the session. If local updater files are missing, direct users to the official repo for manual repair.
- Applying an update writes only inside the current skill directory under the local skills install root. It must not modify unrelated local directories.

---

## 2. MCP Installation Check

Before using MCP-dependent capabilities, check whether the required Gate MCP Servers are installed.

| MCP Server                   | Purpose                                                                           |
| ---------------------------- | --------------------------------------------------------------------------------- |
| gate-info (Gate Info for AI) | Coin info, market snapshots, technical analysis, on-chain data, compliance checks |
| gate-news (Gate News for AI) | News search, social sentiment, exchange announcements, event tracking             |

- If not installed, guide the user to one-click install:
  https://github.com/gate/gate-skills/tree/master/skills
- Ask whether the user wants to install now.
- If the user agrees and the environment supports it, install the required MCP Server first, then continue the task.
- If MCP Server is installed but specific tools are unavailable, inform the user and degrade gracefully (see Section 3).

---

## 3. Tool Degradation & Fault Tolerance

When an MCP Tool is unavailable or returns an error:

- A single Tool failure must NOT block the entire Skill. Skip the unavailable dimension and mark it in the report (e.g., "Data temporarily unavailable").
- If an alternative Tool exists, switch to it automatically (refer to each Skill's degradation table).

| Scenario                    | Handling                                                   |
| --------------------------- | ---------------------------------------------------------- |
| Single Tool timeout (>10s)  | Skip dimension, note "Data fetch timed out"                |
| Single Tool returns empty   | Skip dimension, note "No data available"                   |
| Single Tool returns error   | Log error, skip dimension                                  |
| All Tools fail              | Return error message, suggest user check MCP Server status |
| Tool returns malformed data | Best-effort parse; if impossible, note "Data format error" |

**Strictly forbidden**: fabricating data, substituting one Tool's data for another's, or hiding errors from the user.

---

## 4. Report Output Standards

All reports must follow these conventions:

- Use Markdown format with aligned tables.
- Prices prefixed with `$`, percentages suffixed with `%`.
- Large numbers abbreviated (e.g., $1.2B, $350M, $15.6K).
- Each report notes data source (Gate Info MCP / Gate News MCP) and data retrieval time.
- All reports involving market analysis must include a disclaimer (in the user's language). English example:
  "The above analysis is data-driven and does not constitute investment advice. Please make decisions based on your own risk tolerance."
- Do not make specific price predictions or give explicit "buy/sell" advice.
- Output language matches user's language. Technical terms (RSI, MACD, FDV) stay in English.

---

## 5. Security & Privacy

- Do not expose user API Keys, Secret Keys, or credentials in conversation.
- If API Key setup is needed, guide the user to configure locally:
  - Web: https://www.gate.com/zh/myaccount/profile/api-key/manage
  - App: search "API" in Gate App.
- Do not associate on-chain addresses with real-world identities (unless publicly labeled as institutional).
- Display only publicly verifiable on-chain data.
- When severe risks are detected (honeypot contracts, extremely high tax rates), risk warnings must appear prominently at the top of the report. Never downplay high-risk alerts.

---

## 6. Cross-Skill Routing

When user intent exceeds the current Skill's scope, proactively route to the appropriate Skill.

- Each Skill's SKILL.md defines its own Cross-Skill Routing table. Follow that table.
- Briefly explain the routing reason to the user.
- Carry over key context parameters (coin symbol, address, etc.) — do not ask the user to repeat.

### Skills Landscape (alignment priority)

Canonical **gate-info-skills** / **gate-news-skills** L1 scope, in rollout order. Per-skill update scripts and **Trigger update** in SKILL.md align to this list first. **`gate-info-research`** is out of scope until a separate rollout.

**Note — `gate-info-tokenonchain`:** Multiple L1 skills route here, but **`skills/gate-info-tokenonchain/` is not yet in the gate-skills repo**. When added, use the same layout as other L1 skills: `info-news-runtime-rules.md` + `scripts/update-skill.*` + **Trigger update**.

| Package          | Skill                    | Coverage                            |
| ---------------- | ------------------------ | ----------------------------------- |
| gate-info-skills | gate-info-coinanalysis   | Single-coin comprehensive analysis  |
|                  | gate-info-marketoverview | Market-wide overview                |
|                  | gate-info-coincompare    | Multi-coin comparison               |
|                  | gate-info-trendanalysis  | Trend and technical analysis        |
|                  | gate-info-addresstracker | On-chain address tracking           |
|                  | gate-info-tokenonchain   | Token on-chain data                 |
|                  | gate-info-riskcheck      | Contract security / risk assessment |
| gate-news-skills | gate-news-briefing       | News briefing                       |
|                  | gate-news-eventexplain   | Event attribution and explanation   |
|                  | gate-news-listing        | Exchange listing updates            |

### Routing Degradation

Before routing, check if the target Skill is available:

- **Target Skill available** → route normally.
- **Target Skill unavailable but underlying MCP Tool exists** → call the Tool directly, return basic results, and suggest installing the full Skills package.
- **Target Skill and Tool both unavailable** → inform the user and provide install link:
  https://github.com/gate/gate-skills/tree/master/skills

---

## 7. Error & Authorization Handling

When an error occurs, read documentation and try known solutions before asking the user.

| Error Type                    | Handling                                                   |
| ----------------------------- | ---------------------------------------------------------- |
| MCP Server not installed      | Guide installation (see Section 2)                         |
| MCP Server connection timeout | Suggest checking network, retry later                      |
| Tool parameter error          | Auto-correct and retry once                                |
| Rate limit                    | Inform user, wait, then auto-retry                         |
| Authorization error (401/403) | Guide user to complete API Key setup (see Section 5)       |
| Unknown error                 | Show error summary, suggest filing an issue at Gate Skills |

- Auto-retry at most 1 time, with 2-second interval.
- After retry failure, follow degradation path or inform user.
