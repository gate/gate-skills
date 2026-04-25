# Info & News Common Runtime Rules

> Shared runtime rules for all `gate-info-*` and `gate-news-*` skills.
> Each skill's SKILL.md should include: Read and follow [`info-news-runtime-rules.md` on GitHub](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) first (use this URL or inline code with the same path so single-skill installs can fetch the canonical rules; avoid repo-relative links on Skills Hub).

---

## 1. Skill maintenance

Optional maintenance only:

- If the skill directory contains `scripts/update-skill.sh` (or `scripts/update-skill.ps1` on Windows), `check` may compare the installed copy with the packaged skill source used by the current install.
- In interactive sessions, ask the user before running `apply`.
- Never auto-apply updates in chat or agent-driven interactive flows.
- If `check` cannot run, continue with the currently installed version. Share maintenance details only when the user asks.
- Applying an update may modify files only inside the current skill directory under the local skills install root. It must not modify unrelated local directories.

---

## 2. MCP Installation Check

Before using MCP-dependent capabilities, check whether the required Gate MCP Servers are installed.

| MCP Server                   | Purpose                                                                           |
| ---------------------------- | --------------------------------------------------------------------------------- |
| gate-info (Gate Info for AI) | Coin info, market snapshots, technical analysis, on-chain data, compliance checks |
| gate-news (Gate News for AI) | News search, social sentiment, exchange announcements, event tracking             |

- If not installed, guide the user to the local Gate MCP installation flow for the current host IDE.
- Ask whether the user wants to install now.
- If the user agrees and the environment supports it, install the required MCP Server first, then continue the task.
- If MCP Server is installed but specific tools are unavailable, inform the user and degrade gracefully (see Section 3).

---

## 3. Legacy Wrapper Routing

Some legacy `gate-info-*` / `gate-news-*` skills may be converted into
compatibility wrappers that delegate to primary CLI skills in the separate
`gate-cli-skills` repository.

Wrapper rules:

- Run a deterministic shell probe **before** Trigger update, MCP tool selection,
  or any legacy Execution Workflow.
- The probe checks:
  1. `gate-cli` exists on `$PATH`
  2. The mapped primary skill is installed in at least one known scan root
- The probe MUST emit exactly one stdout token:
  - `__ROUTE_CLI__` → stop the legacy path and delegate to the mapped primary
    skill in `gate-cli-skills`
  - `__FALLBACK__` → continue the current legacy MCP workflow in this skill
- Do **not** invent pseudo binaries or pseudo commands (for example
  `gate-news-risk`). The CLI path is always the mapped primary skill plus real
  `gate-cli` commands documented there.
- When the wrapper emitted `__ROUTE_CLI__`, the sections below in the current
  legacy skill (`MCP Dependencies`, `Execution Workflow`, `Report Template`,
  etc.) are **not** executed.
- **Mapping:** there is no separate routing file. Each wrapper `SKILL.md`
  must inline the mapped primary skill, where to read its `SKILL.md` (e.g. a
  path under the same `skills/` tree or install root), and the minimum
  context to carry over.

---

## 4. Tool Degradation & Fault Tolerance

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

## 5. Report Output Standards

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

## 6. Security & Privacy

- Do not expose user API Keys, Secret Keys, or credentials in conversation.
- If API Key setup is needed, guide the user to configure locally:
  - Web: https://www.gate.com/zh/myaccount/profile/api-key/manage
  - App: search "API" in Gate App.
- Do not associate on-chain addresses with real-world identities (unless publicly labeled as institutional).
- Display only publicly verifiable on-chain data.
- When severe risks are detected (honeypot contracts, extremely high tax rates), risk warnings must appear prominently at the top of the report. Never downplay high-risk alerts.

---

## 7. Cross-Skill Routing

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
- **Target Skill unavailable but underlying MCP Tool exists** → call the Tool directly, return basic results, and suggest installing the full Skills package through the local Gate MCP installation flow.
- **Target Skill and Tool both unavailable** → inform the user and point them to the local Gate MCP installation flow for the current host IDE.

---

## 8. Error & Authorization Handling

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
