---
name: gate-mcp-cursor-installer
version: "2026.3.25-2"
updated: "2026-03-25"
description: "Installs and configures Gate MCP servers (main, CEX, DEX, Info, News) and Gate skills into Cursor IDE by writing mcp.json, merging with existing config, and verifying connectivity. Use when the user asks to set up Gate trading or research tools in Cursor. Triggers on 'install Gate MCP Cursor', 'Gate skills Cursor', 'setup Gate in Cursor'."
---

# Gate One-Click Installer (Cursor: MCP + Skills)

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they exist in the MCP server.

---

## MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), then execute this installer workflow.

- `SKILL.md` defines product scope, install behavior, and user-facing guidance.
- `references/mcp.md` is the authoritative execution layer for preflight checks, config merge policy, and install verification.

## Resources

The agent installs the following MCP servers into Cursor. All servers default to install unless the user selects a subset.

| Name | Key | Transport | Config Summary |
|------|-----|-----------|----------------|
| **Gate** | `main` | stdio | `command: npx`, `args: ["-y", "gate-mcp"]`, optional `env` for API keys |
| **gate-cex-pub** | `cex-public` | streamable-http | `url` only (no auth headers) |
| **gate-cex-ex** | `cex-exchange` | streamable-http | `url` only; Gate OAuth2 on first connect |
| **Gate-Dex** | `dex` | streamable-http | `url` + `headers` (x-api-key `MCP_AK_8W2N7Q`, Bearer) |
| **Gate-Info** | `info` | streamable-http | `url` only |
| **Gate-News** | `news` | streamable-http | `url` only |
| **gate-skills** | — | git clone | https://github.com/gate/gate-skills → `~/.cursor/skills/` |

For CEX MCP mode details (Local vs Remote Public vs Remote Exchange, tool naming differences), see [gate-mcp](https://github.com/gate/gate-mcp).

## Behavior Rules

1. **Default scope**: Install **all** MCP servers listed above + **all** gate-skills.
2. **Selectable**: The user may request only specific servers; install only those requested.
3. **Skills toggle**: Unless `--no-skills` is passed, always install all skills from the gate-skills repository.

## Installation Workflow

### Step 1 — Confirm Scope

- Ask the user which MCP servers to install. If unspecified, install all six servers plus skills.
- Confirm the target config path: `~/.cursor/mcp.json` (Windows: `%APPDATA%\Cursor\mcp.json`).

### Step 2 — Write Cursor MCP Config

Run the installer script or merge manually. The resulting `mcp.json` should look like this (all servers selected):

```jsonc
{
  "mcpServers": {
    "gate": {
      "command": "npx",
      "args": ["-y", "gate-mcp"],
      "env": { "GATE_API_KEY": "", "GATE_API_SECRET": "" }
    },
    "gate-cex-pub": {
      "url": "https://api.gatemcp.ai/mcp",
      "transport": "streamable-http"
    },
    "gate-cex-ex": {
      "url": "https://api.gatemcp.ai/mcp/exchange",
      "transport": "streamable-http"
    },
    "gate-dex": {
      "url": "<dex-endpoint>",
      "transport": "streamable-http",
      "headers": { "x-api-key": "MCP_AK_8W2N7Q", "Authorization": "Bearer <token>" }
    },
    "gate-info": {
      "url": "<info-endpoint>",
      "transport": "streamable-http"
    },
    "gate-news": {
      "url": "<news-endpoint>",
      "transport": "streamable-http"
    }
  }
}
```

- If `mcp.json` already exists, **merge** new entries into existing `mcpServers`; never overwrite unrelated servers.
- If JSON parse fails on the existing file, abort and report the error to the user.

### Step 3 — Install gate-skills

- Clone or copy all subdirectories under `skills/` from the gate-skills repo into `~/.cursor/skills/`.
- Skip this step if `--no-skills` was passed.

### Step 4 — Verify Installation

1. **Config validity**: Re-read `mcp.json` and confirm it is valid JSON with the expected `mcpServers` entries.
2. **Skills presence**: Confirm skill directories exist under `~/.cursor/skills/` (unless `--no-skills`).
3. If any check fails, report the specific failure and suggest manual remediation.

### Step 5 — Post-Install Guidance

Report the installed servers and skills, then provide next steps:

- **Restart Cursor** to activate MCP connections.
- **Gate (main) API key**: Generate at https://www.gate.com/myaccount/profile/api-key/manage and set in `env`.
- **gate-cex-ex**: Complete Gate OAuth2 when Cursor prompts on first connect.
- **Gate-Dex**: Complete wallet + OAuth setup via https://web3.gate.com/.

## Script

Use `scripts/install.sh` for one-click installation:

```bash
# Install all MCPs + skills (default)
bash scripts/install.sh

# Install specific MCPs only
bash scripts/install.sh --mcp main --mcp dex

# Install MCPs without skills
bash scripts/install.sh --no-skills
```
