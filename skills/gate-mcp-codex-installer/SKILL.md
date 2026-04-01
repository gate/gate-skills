---
name: gate-mcp-codex-installer
version: "2026.3.25-2"
updated: "2026-03-25"
description: "Gate MCP and Gate skills installer for Codex. Use when the user asks to add Gate MCP or skills to Codex. Triggers on 'install Gate MCP Codex', 'Gate skills Codex', 'setup Gate Codex'."
---

# Gate One-Click Installer (Codex: MCP + Skills)

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

## MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), then execute this installer workflow.

- `SKILL.md` keeps product scope, install behavior, and user-facing guidance.
- `references/mcp.md` is the authoritative execution layer for preflight checks, config merge safety, and install verification steps.

## CEX MCP modes

See [gate-mcp](https://github.com/gate/gate-mcp): **Local** = stdio `gate-mcp` with API keys; **Remote Public** = `https://api.gatemcp.ai/mcp` (no auth); **Remote Exchange** = `https://api.gatemcp.ai/mcp/exchange` (Gate OAuth2). Dex/Info/News are separate endpoints on the same host.

## Resources

| Type | Name | Endpoint / Config |
|------|------|-------------------|
| MCP | **Gate** (`main`) | stdio `command = "npx"`, `args = ["-y", "gate-mcp"]`, optional `env` for keys |
| MCP | **gate-cex-pub** (`cex-public`) | `url = "https://api.gatemcp.ai/mcp"` |
| MCP | **gate-cex-ex** (`cex-exchange`) | `url = "https://api.gatemcp.ai/mcp/exchange"` (OAuth2 in client) |
| MCP | **gate-dex** (`dex`) | `https://api.gatemcp.ai/mcp/dex`, `http_headers` x-api-key + Bearer token |
| MCP | **gate-info** (`info`) | `https://api.gatemcp.ai/mcp/info` |
| MCP | **gate-news** (`news`) | `https://api.gatemcp.ai/mcp/news` |
| Skills | gate-skills | https://github.com/gate/gate-skills (installs all under `skills/`) |

## Behavior Rules

1. **Default**: When the user does not specify which MCPs to install, install **all MCPs** (`main`, `cex-public`, `cex-exchange`, `dex`, `info`, `news`) + **all gate-skills**.
2. **Selectable MCPs**: Users can choose to install only specific MCPs; follow the user's selection.
3. **Skills**: Unless `--no-skills` is passed, always install **all** skills from the gate-skills repository's **skills/** directory.

## Installation Steps

### 1. Confirm User Selection (MCPs)

- If the user does not specify which MCPs → install all: `main`, `cex-public`, `cex-exchange`, `dex`, `info`, `news`.
- If the user specifies "only install xxx" → install only the specified MCPs.

### 2. Write Codex MCP Config

- User-level config: `~/.codex/config.toml` (or `$CODEX_HOME/config.toml`). Creates the file and writes `[mcp_servers]` with corresponding tables if it does not exist.
- If it already exists, **merge**: only append Gate MCP sections that don't already exist; do not overwrite existing config.
- Config details:
  - **Gate (main)**: stdio, `command` / `args` / optional `env` for `GATE_API_KEY` / `GATE_API_SECRET`
  - **gate-cex-pub / gate-cex-ex**: `url` as above (no `http_headers` for remote CEX)
  - **gate-dex**: `url` + `http_headers` for x-api-key and Bearer
  - **gate-info / gate-news**: `url`

### 3. Install gate-skills (all)

- Pull all subdirectories under **skills/** from https://github.com/gate/gate-skills and copy them to `$CODEX_HOME/skills/` (default `~/.codex/skills/`).
- Add `--no-skills` when using the script to install MCP only without skills.

### 4. Post-Installation Prompt

- Inform the user of the installed MCP list and "all gate-skills have been installed" (unless --no-skills was used).
- Prompt to restart Codex to load MCP servers and skills.
- **Local API Key**: For **Gate (main)** trading via API keys → https://www.gate.com/myaccount/profile/api-key/manage
- **gate-cex-ex**: Complete **Gate OAuth2** when Codex prompts on first use.
- **Gate-Dex**: If auth required, open https://web3.gate.com/ for wallet, then complete OAuth via the assistant link.

## Script

Use the **scripts/install.sh** in this skill directory for one-click installation.

- Usage:  
  `./scripts/install.sh [--mcp main|cex-public|cex-exchange|dex|info|news] ... [--no-skills]`  
  Installs all MCPs when no `--mcp` is passed; pass multiple `--mcp` to install only specified ones; `--no-skills` installs MCP only.
- The DEX x-api-key is fixed as `MCP_AK_8W2N7Q` and written to config.toml.

After downloading this skill from GitHub, run from the repository root:  
`bash skills/gate-mcp-codex-installer/scripts/install.sh`  
Or (MCP only):  
`bash skills/gate-mcp-codex-installer/scripts/install.sh --no-skills`
