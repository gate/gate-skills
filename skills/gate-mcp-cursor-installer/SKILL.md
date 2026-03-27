---
name: gate-mcp-cursor-installer
version: "2026.3.25-2"
updated: "2026-03-25"
description: One-click installer for Gate MCP and Skills in Cursor. Installs Local CEX (stdio), Remote CEX public/exchange, Dex/Info/News (selectable), and all gate-skills. Default installs all MCPs + all skills.
---

# Gate One-Click Installer (Cursor: MCP + Skills)

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

## CEX MCP modes

See [gate-mcp](https://github.com/gate/gate-mcp): **Local** = stdio `npx -y gate-mcp` (API keys); **Remote Public** = `https://api.gatemcp.ai/mcp` (no auth); **Remote Exchange** = `https://api.gatemcp.ai/mcp/exchange` (Gate OAuth2). Tool naming differs between Local (abbrev) and Remote (`cex_*`); use each server's `tools/list`.

## Resources

| Type | Name | Endpoint / Config |
|------|------|-------------------|
| MCP | **Gate** (`main`) | `command: npx`, `args: ["-y", "gate-mcp"]`, optional `env` |
| MCP | **gate-cex-pub** (`cex-public`) | `url` + `transport: streamable-http` only (no headers) |
| MCP | **gate-cex-ex** (`cex-exchange`) | `url` + `transport: streamable-http` only; OAuth2 when prompted |
| MCP | **Gate-Dex** (`dex`) | `url`, `transport: streamable-http`, x-api-key + Bearer |
| MCP | **Gate-Info** (`info`) | `url`, `transport: streamable-http` |
| MCP | **Gate-News** (`news`) | `url`, `transport: streamable-http` |
| Skills | gate-skills | https://github.com/gate/gate-skills (installs all under `skills/`) |

## Behavior Rules

1. **Default**: When the user does not specify which MCPs to install, install **all MCPs** (`main`, `cex-public`, `cex-exchange`, `dex`, `info`, `news`) + **all gate-skills**.
2. **Selectable MCPs**: Users can choose to install only specific MCPs; follow the user's selection.
3. **Skills**: Unless `--no-skills` is passed, always install **all** skills from the gate-skills repository's **skills/** directory.

## Installation Steps

### 1. Confirm User Selection (MCPs)

- If the user does not specify which MCPs → install all: `main`, `cex-public`, `cex-exchange`, `dex`, `info`, `news`.
- If the user specifies "only install xxx" → install only the specified MCPs.

### 2. Write Cursor MCP Config

- Config file: `~/.cursor/mcp.json` (Windows: `%APPDATA%\Cursor\mcp.json`).
- If it already exists, **merge** into the existing `mcpServers`; do not overwrite other MCPs.
- Config details:
  - **Gate (main)**: `command` / `args` / optional `env`
  - **gate-cex-pub / gate-cex-ex**: `url` + `transport: streamable-http` only (no headers)
  - **Gate-Dex**: `url` + `transport` + `headers` for x-api-key and Bearer
  - **Gate-Info / Gate-News**: `url` + `transport: streamable-http`

### 3. Install gate-skills (all)

- Pull all subdirectories under **skills/** from https://github.com/gate/gate-skills and copy them to `~/.cursor/skills/` (or the corresponding directory for the current environment).
- Add `--no-skills` when using the script to install MCP only without skills.

### 4. Post-Installation Prompt

- Inform the user of the installed MCP list and "all gate-skills have been installed" (unless --no-skills was used).
- Prompt to restart Cursor.
- **Local API Key**: For **Gate (main)** → https://www.gate.com/myaccount/profile/api-key/manage
- **gate-cex-ex**: Complete **Gate OAuth2** when Cursor prompts on first connect.
- **Gate-Dex**: Wallet + OAuth guidance as in [gate-mcp](https://github.com/gate/gate-mcp) (https://web3.gate.com/).

## Script

Use the **scripts/install.sh** in this skill directory for one-click installation.

- Usage:  
  `./scripts/install.sh [--mcp main|cex-public|cex-exchange|dex|info|news] ... [--no-skills]`  
  Installs all MCPs when no `--mcp` is passed; pass multiple `--mcp` to install only specified ones; `--no-skills` installs MCP only.
- The DEX x-api-key is fixed as `MCP_AK_8W2N7Q` and written to mcp.json.

After downloading this skill from GitHub, run from the repository root:  
`bash scripts/install.sh`  
Or (MCP only):  
`bash scripts/install.sh --no-skills`
