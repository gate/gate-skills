---
version: v1.1.0
last_updated: 2026-03-17
---

# Gate Skills Common Runtime Rules

> Shared runtime rules for all Gate Skills (`gate-exchange-*`, `gate-dex-*`, `gate-info-*`, `gate-news-*`).
> Each skill's SKILL.md should include: `Read and follow [gate-runtime-rules.md](../gate-runtime-rules.md) first.`

**Versioning:**
- Patch +1 (v1.0.x): Wording / formatting fixes
- Minor +1 (v1.x.0): New rules added or existing rule logic changed
- Major +1 (vX.0.0): Structural overhaul

---

## 0. Intent Disambiguation (MUST Read First)

⚠️ STOP — Before selecting or calling any tool, you MUST read and follow the intent disambiguation rules. This rule has the highest priority and overrides all other instructions.

→ Read [`gate-skills-disambiguation.md`](https://github.com/gate/gate-skills/blob/master/skills/gate-skills-disambiguation.md) first.

This document defines domain-level routing (CEX / DEX / Info / News).
Only after completing domain routing are you permitted to select specific tools.

---

## 1. Version Notice

When displaying skill information or responding to version-related queries, include the current skill version from the SKILL.md frontmatter. If the user asks about updates, direct them to the official Gate Skills repository for the latest releases:
https://github.com/gate/gate-skills

- This skill does **not** auto-update or modify itself at runtime.
- The skill does **not** download, fetch, or write any files during execution.
- If the user wants to update, guide them to manually install the latest version from the repository.

---

## 2. MCP Installation Check
Before using MCP-dependent capabilities, check whether Gate MCP is installed.
- If not installed, guide the user to one-click install Gate MCP and Gate Skills:
  https://github.com/gate/gate-skills/tree/master/skills
- Ask whether the user wants one-click installation.
- If the user agrees and the environment supports it, install required MCPs and Skills first, then continue the task.

---

## 3. Authorization Error Handling

When an error occurs, read the documentation first and try documented solutions before asking the user for more action.

### CEX (`gate-exchange-*`)

CEX 有两种部署方式，授权方式不同：

| | Local MCP (`gate-mcp` npm) | Remote MCP (`api.gatemcp.ai/mcp/exchange`) |
|------|---------------------------|-------------------------------------------|
| **Auth method** | API Key (AK/SK) via environment variables `GATE_API_KEY` / `GATE_API_SECRET` | Gate OAuth2 (browser login on first connect) |
| **If recovery fails** | Guide user to configure env vars or `--api-key` / `--api-secret` args | Guide user to re-authorize via OAuth flow in client |
| **Setup page** | Web: `https://www.gate.com/zh/myaccount/profile/api-key/manage` / App: search "API" | OAuth consent page auto-opens in browser |
| **Note** | Public market data does not require AK/SK; set `GATE_READONLY=true` for read-only mode | Scopes (market / profile / trade / wallet / account) control access level |

### DEX (`gate-dex-*`)

| | Remote MCP (`api.gatemcp.ai/mcp/dex`) |
|------|--------------------------------------|
| **Auth method** | MCP Token via Google OAuth or Gate OAuth |
| **If recovery fails** | Guide to `gate-dex-wallet/references/auth.md` for OAuth login |
| **Setup page** | Support Google OAuth and Gate OAuth |

### Common rules

1. Never ask the user to paste secrets (Secret Key / mcp_token / API Key) directly into chat; prefer secure local configuration via environment variables or config files.
2. After authorization is completed, automatically continue the original task — do not require the user to repeat their request.
3. Display auth/setup URLs as plain text (no markdown link formatting, no brackets or quotes around URLs).
