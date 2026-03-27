---
name: gate-mcp-claude-installer
version: "2026.3.25-2"
updated: "2026-03-25"
description: One-click installer for Gate MCP and all Gate Skills in Claude Code (Claude CLI). Installs Local CEX (stdio), Remote CEX public/exchange, Dex/Info/News (selectable), and all gate-skills. Default installs all MCPs + all skills.
---

# Gate One-Click Installer (Claude Code: MCP + Skills)

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.


---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate (main) | ✅ Required |
| Gate-Dex | ✅ Required |
| Gate-Info | ✅ Required |
| Gate-News | ✅ Required |

### Authentication
- API Key Required: No

### Installation Check
- Required: Gate (main), Gate-Dex, Gate-Info, Gate-News
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## CEX MCP modes (read before configuring)

Aligned with [gate-mcp](https://github.com/gate/gate-mcp) documentation:

| Mode | What it is | Auth | Typical use |
|------|------------|------|----------------|
| **Local CEX** | stdio `npx -y gate-mcp` (npm package **gate-mcp**) | Optional `GATE_API_KEY` / `GATE_API_SECRET` (public-only works without keys; set `GATE_READONLY=true` for read-only) | Full local tool surface; tool names use abbreviations (`fx`, `dc`, …) — see gate-mcp **gate-local-mcp-tools** doc |
| **Remote CEX — Public** | `https://api.gatemcp.ai/mcp` | **None** | Public market data only (~58 tools, `cex_*` names) |
| **Remote CEX — Exchange** | `https://api.gatemcp.ai/mcp/exchange` | **Gate OAuth2** (browser login) | Private trading & account (~400+ tools); **does not** duplicate the full public market-data set — use **Public** remote or Local for market queries as needed |

**Non-CEX** (same host): **Dex** (`/mcp/dex`, Google/Gate OAuth + fixed x-api-key), **Info** (`/mcp/info`), **News** (`/mcp/news`).

## Resources

| Type | Name | Endpoint / Config |
|------|------|-------------------|
| MCP | **Gate** (Local CEX, `main`) | stdio `npx -y gate-mcp`, env `GATE_API_KEY` / `GATE_API_SECRET` — [gate-mcp](https://github.com/gate/gate-mcp) |
| MCP | **gate-cex-pub** (`cex-public`) | `https://api.gatemcp.ai/mcp`, HTTP, `type`+`url` only (no headers), no auth |
| MCP | **gate-cex-ex** (`cex-exchange`) | `https://api.gatemcp.ai/mcp/exchange`, HTTP, `type`+`url` only; Gate OAuth2 on first use |
| MCP | **Gate-Dex** (`dex`) | `https://api.gatemcp.ai/mcp/dex`, fixed `x-api-key` + `Authorization: Bearer ${GATE_MCP_TOKEN}` |
| MCP | **Gate-Info** (`info`) | `https://api.gatemcp.ai/mcp/info` |
| MCP | **Gate-News** (`news`) | `https://api.gatemcp.ai/mcp/news` |
| Skills | gate-skills | https://github.com/gate/gate-skills (installs all under `skills/`) |

## Behavior Rules

1. **Default**: When the user does not specify which MCPs to install, install **all MCPs** (`main`, `cex-public`, `cex-exchange`, `dex`, `info`, `news`) + **all gate-skills**.
2. **Selectable MCPs**: Users can choose to install only specific MCPs; follow the user's selection (`--mcp` can be repeated).
3. **Skills**: Unless `--no-skills` is passed, always install **all** skills from the gate-skills repository's **skills/** directory.

## Installation Steps

### 1. Confirm User Selection (MCPs)

- If the user does not specify which MCPs → install all: `main`, `cex-public`, `cex-exchange`, `dex`, `info`, `news`.
- If the user specifies "only install xxx" → install only the specified MCPs.

### 2. Write Claude Code MCP Config

- User-level config: `~/.claude.json` (Windows: `%USERPROFILE%\.claude.json`). If using directory format, use the corresponding config under `~/.claude/`.
- If it already exists, **merge** into the existing `mcpServers`; do not overwrite other MCPs.
- Config details:
  - **Gate (main)**: stdio, `command: npx`, `args: ["-y", "gate-mcp"]`, optional `env` for API keys
  - **gate-cex-pub**: `type: http`, `url` only (remote CEX public; no extra headers)
  - **gate-cex-ex**: `type: http`, `url` for `/mcp/exchange` only; OAuth2 is completed in the client when prompted
  - **Gate-Dex**: http, `url` + `headers["x-api-key"]` = `MCP_AK_8W2N7Q` + `Authorization` = `Bearer ${GATE_MCP_TOKEN}`
  - **Gate-Info / Gate-News**: http, `url`

### 3. Install gate-skills (all)

- Pull all subdirectories under **skills/** from https://github.com/gate/gate-skills and copy them to `~/.claude/skills/` (or the corresponding directory for the current environment).
- Add `--no-skills` when using the script to install MCP only without skills.

### 4. Post-Installation Prompt

- Inform the user of the installed MCP list and "all gate-skills have been installed" (unless `--no-skills` was used).
- Prompt to reopen Claude Code or start a new session to load the MCPs.
- **Local API Key**: If **Gate (main)** is used for trading via API keys, direct the user to https://www.gate.com/myaccount/profile/api-key/manage and set `GATE_API_KEY` / `GATE_API_SECRET` in the Gate entry `env`.
- **Remote Exchange OAuth2**: If **gate-cex-ex** was installed, the user completes **Gate OAuth2** in the browser when the client prompts (scopes: `market`, `profile`, `trade`, `wallet`, `account`).
- **Gate-Dex Authorization**: If Gate-Dex was installed and a query returns an authorization required message, prompt the user to first open https://web3.gate.com/ to create or bind a wallet, then complete OAuth via the link the assistant provides.

## Script

Use the **scripts/install.sh** in this skill directory for one-click installation.

- Usage:  
  `./scripts/install.sh [--mcp main|cex-public|cex-exchange|dex|info|news] ... [--no-skills]`  
  Installs all MCPs when no `--mcp` is passed; pass multiple `--mcp` to install only specified ones; `--no-skills` installs MCP only.
- The DEX x-api-key is fixed as `MCP_AK_8W2N7Q` and written to the config.

After downloading this skill from GitHub, run from the repository root:  
`bash skills/gate-mcp-claude-installer/scripts/install.sh`  
Or (MCP only):  
`bash skills/gate-mcp-claude-installer/scripts/install.sh --no-skills`
