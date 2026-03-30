# Info & News Common Runtime Rules

> Shared runtime rules for all `gate-info-*` and `gate-news-*` skills.
> Each skill's SKILL.md should include: Read and follow `../info-news-runtime-rules.md` first (path relative to `skills/<skill-name>/SKILL.md`; use inline code, not a relative markdown link — Skills Hub cannot resolve repo-relative links).

---

## 1. Skill version check & update

Before execution, check whether a newer version of the current skill exists in the official Gate Skills repository:
https://github.com/gate/gate-skills

- If the skill directory contains `scripts/update-skill.sh` (or `scripts/update-skill.ps1` on Windows), run the **`check`** subcommand first **without** **`GATE_SKILL_UPDATE_MODE=auto`** for the normal **blocking** flow: the script **only compares**; when `update_available`, each skill’s **SKILL.md** instructs the agent to **ask the user** before **`apply`** (see **blocking update confirmation** in the independent-script test report). **`run`** performs check + apply in one go — **not** for that blocking flow in chat.
- Version check fetches the remote SKILL.md head via GitHub Raw URL: `https://raw.githubusercontent.com/gate/gate-skills/master/skills/{skill_name}/SKILL.md`
- **Strict `check` (recommended for agents):** **`GATE_SKILL_CHECK_STRICT=1`** on **`check`**: when `update_available`, the process **exits 3** (`GATE_SKILL_CHECK_EXIT=3`) and prints **`BLOCK_UNTIL_USER_CONFIRMS_UPDATE`**. **Two-step gate:** strict `check` prints **`GATE_SKILL_CONFIRM_TOKEN`** and writes **`.gate-skill-apply-token`**. **`apply`** / **`run`** (without auto) **refuse** (exit **2**) until **`GATE_SKILL_CONFIRM_TOKEN`** matches. User declines → **`revoke-pending <name>`**. Non-strict `check` does **not** create a token.
  - **Cursor / Agent:** After notifying the user, **end this assistant turn** before `apply` — strict `check` **exit 3** only aborts that shell step; **`apply`** in a **later** turn after the user agrees (or **`revoke-pending`** if they decline).
- **Optional — auto mode (CI / unattended only):** **`GATE_SKILL_UPDATE_MODE=auto`** on **`check`** or **`run`** applies immediately when the remote is newer — **no** user step; **incompatible** with blocking verification.
- If `skipped` (versions match) or `check_failed` (network, missing tools, etc.): proceed directly to execution.
- If update check fails or GitHub is unreachable, disclose the limitation and proceed with the current version. Never block execution due to update failure.
- Update pulls the entire skill directory from the remote repo (git clone → ZIP → tar.gz fallback), writes to a temp location first, and only overwrites after verification. Original files are preserved on failure.

---

## 2. MCP Installation Check

Before using MCP-dependent capabilities, check whether the required Gate MCP Servers are installed.

| MCP Server                   | Purpose                                                                                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| gate-info (Gate Info for AI) | Coin info, market snapshots, technical analysis, on-chain data, DeFi platform metrics, macro economic indicators, compliance checks               |
| gate-news (Gate News for AI) | News search, social sentiment, community / X sentiment, exchange announcements, event tracking                                                      |

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

### Skills Landscape

Reference list of **gate-info-skills** / **gate-news-skills** L1 scope. **Row order is not prescriptive** (no rollout or routing priority implied). Per-skill update scripts and **Trigger update** in SKILL.md should stay consistent with this landscape when syncing. **`gate-info-research`** is out of scope until a separate rollout.

**Note — extended Info/News L1 skills:** `gate-info-defianalysis`, `gate-info-macroimpact`, `gate-info-tokenonchain`, and `gate-news-communityscan` share the same runtime as other `gate-info-*` / `gate-news-*` skills. Use the same layout: `info-news-runtime-rules.md` first, optional `scripts/update-skill.*`, and **Trigger update** in SKILL.md. Official `https://github.com/gate/gate-skills` rollout may lag this repository; keep this landscape aligned when syncing.

| Package          | Skill                      | Coverage                               |
| ---------------- | -------------------------- | -------------------------------------- |
| gate-info-skills | gate-info-addresstracker   | On-chain address tracking              |
|                  | gate-info-coinanalysis     | Single-coin comprehensive analysis     |
|                  | gate-info-coincompare      | Multi-coin comparison                  |
|                  | gate-info-defianalysis     | DeFi TVL / platform / ecosystem        |
|                  | gate-info-macroimpact      | Macro indicators vs crypto linkage     |
|                  | gate-info-marketoverview   | Market-wide overview                   |
|                  | gate-info-riskcheck        | Contract security / risk assessment    |
|                  | gate-info-tokenonchain     | Token on-chain data                    |
|                  | gate-info-trendanalysis    | Trend and technical analysis           |
| gate-news-skills | gate-news-briefing         | News briefing                          |
|                  | gate-news-communityscan    | Community / X sentiment and discussion |
|                  | gate-news-eventexplain     | Event attribution and explanation      |
|                  | gate-news-listing          | Exchange listing updates               |

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
