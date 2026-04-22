---
version: v1.2.5
last_updated: 2026-04-22
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

## 2. MCP Detection & Installation

Before using MCP-dependent capabilities, detect whether the required Gate MCP is already configured.

**Detection method:**
- List available MCP tools (e.g. `tools/list` or client's MCP panel)
- If tools with `cex_` prefix exist → CEX MCP is configured
- If tools with `dex_` prefix exist → DEX MCP is configured
- If tools with `info_` / `news_` prefix exist → Info / News MCP is configured

**If required MCP is not configured:**
- Follow the deployment selection guide in Section 3 below to choose Remote MCP or Local MCP.
- Or guide the user to one-click install Gate MCP and Gate Skills:
  https://github.com/gate/gate-skills/tree/master/skills

---

## 3. MCP Deployment Selection & Authorization

Before selecting tools, follow the decision flow below to determine the correct MCP endpoint. When an authorization error occurs during use, consult the authorization details tables to guide recovery.

### CEX (`gate-exchange-*`)

CEX supports two deployment methods. **Prefer Remote MCP; fall back to Local MCP when the environment does not support OAuth.**

| | Remote MCP | Local MCP |
|------|-----------|-----------|
| **When to use** | Client supports OAuth (Cursor, Claude Desktop, Claude Code CLI, Trae, Qoder, etc.) | No OAuth support, enterprise intranet, CI/CD, or scripts |
| **Auth method** | Gate OAuth2 — requires opening a browser for login and authorization on first connect | API Key / API Secret — configure via `GATE_API_KEY` / `GATE_API_SECRET` env vars or `--api-key` / `--api-secret` args (config only, no browser needed) |
| **On auth failure** | Guide user to re-authorize via browser OAuth flow | Guide user to verify env vars or args are correctly set |
| **API Key setup** | Not needed (OAuth handles auth) | https://www.gate.com/myaccount/profile/api-key/manage |

**Agent decision flow (execute in order):**

```
1. Already configured?
   → If tools with `cex_` prefix exist in tools/list → use the existing MCP.
   → On auth error → consult the table above for recovery steps.

2. Not configured → choose deployment method:
   a. Client supports OAuth → recommend Remote MCP
   b. No OAuth / intranet / CI → recommend Local MCP

3. Guide installation:
   → Direct the user to the setup guide: https://github.com/gate/gate-mcp
   → Or suggest one-click install: https://github.com/gate/gate-skills
```

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

---

## 4. Resolving which `gate-cli` to run (`gate-exchange-*`, installers)

When invoking **`gate-cli`** from a shell or script (the command name **`gate-cli`**), resolve the executable **strictly in this order**:

1. **System / PATH:** If **`command -v gate-cli`** resolves to an executable **and** **`gate-cli --version`** exits successfully, use that binary for all documented **`gate-cli`** commands.

2. **`${HOME}/.local/bin/gate-cli`:** If step 1 does **not** yield a usable CLI, **if** this path exists **and** is executable, treat **`gate-cli`** as shorthand for invoking **`"${HOME}/.local/bin/gate-cli"`** (always use this full path in automation when PATH is unreliable).

3. **`${HOME}/.openclaw/skills/bin/gate-cli`:** If steps 1–2 do **not** yield a usable CLI, **if** this path exists **and** is executable, treat **`gate-cli`** as shorthand for **`"${HOME}/.openclaw/skills/bin/gate-cli"`**.

Do **not** assume a single global install location; agents and scripts MUST follow this detection order.

---

## 5. `gate-cli cex …` execution flow (`gate-exchange-*`)

When a workflow uses **`gate-cli cex …`** on the host (typical of `gate-exchange-*` skills), **strictly**:

1. Run **`gate-cli cex … --help`** first (same subcommand path, **`--help`** before other flags) to see if the CLI documents **required** flags or arguments.
2. **If there are required fields** (e.g. `--currency`): gather values (never API secrets in chat), then run the real command **without** `--help`, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If there are no required fields** beyond auth: run **`gate-cli cex …`** directly (add only optional flags the task still needs).

**Example:** `gate-cli cex spot account get` → `gate-cli cex spot account get --help` → if `--currency` is required, then `gate-cli cex spot account get --currency BTC`; otherwise `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, use a documented read-only call or explicit user clarification—especially before writes.
