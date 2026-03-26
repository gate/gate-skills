# Gate Claude Code One-Click Installer (MCP + Skills)

One-click installation of Gate MCP servers and all [gate-skills](https://github.com/gate/gate-skills) skills for **Claude Code (Claude CLI)**.

CEX is available as **Local** (`npx -y gate-mcp`), **Remote public** (`https://api.gatemcp.ai/mcp`, no auth), and **Remote exchange** (`https://api.gatemcp.ai/mcp/exchange`, Gate OAuth2). See [gate-mcp](https://github.com/gate/gate-mcp).

## Installation

### One-click install from this repository

```bash
# Run from the gate-skills repository root
bash skills/gate-mcp-claude-installer/scripts/install.sh
```

### Install MCP only (without gate-skills)

```bash
bash skills/gate-mcp-claude-installer/scripts/install.sh --no-skills
```

### Install specific MCPs only

```bash
# Local CEX + Dex only
bash skills/gate-mcp-claude-installer/scripts/install.sh --mcp main --mcp dex

# Remote CEX public + exchange only (no local stdio)
bash skills/gate-mcp-claude-installer/scripts/install.sh --mcp cex-public --mcp cex-exchange
```

## What Gets Installed

| Component | Description |
|-----------|-------------|
| **Gate** (`main`) | Local CEX, stdio `npx -y gate-mcp`, optional `GATE_API_KEY` / `GATE_API_SECRET` — [gate-mcp](https://github.com/gate/gate-mcp) |
| **gate-cex-pub** (`cex-public`) | `https://api.gatemcp.ai/mcp` — public market data, no auth (URL only in config) |
| **gate-cex-ex** (`cex-exchange`) | `https://api.gatemcp.ai/mcp/exchange` — private CEX tools, **Gate OAuth2** on first use |
| **Gate-Dex** (`dex`) | `https://api.gatemcp.ai/mcp/dex` (x-api-key built-in, Authorization: Bearer ${GATE_MCP_TOKEN}) |
| **Gate-Info** (`info`) | `https://api.gatemcp.ai/mcp/info` |
| **Gate-News** (`news`) | `https://api.gatemcp.ai/mcp/news` |
| **gate-skills** | Cloned from [gate-skills](https://github.com/gate/gate-skills), installs all skills under `skills/` |

## Config File Locations

- **MCP config**: `~/.claude.json` under `mcpServers` (Windows: `%USERPROFILE%\.claude.json`), merged with existing config.
- **Skills**: `~/.claude/skills/` (Windows: `%USERPROFILE%\.claude\skills`).

## Dependencies

- **Bash**: Required to run `install.sh` (built-in on macOS/Linux; use Git Bash or WSL on Windows).
- **Node.js**: Used to merge `~/.claude.json`; if Node is unavailable, the script outputs a JSON snippet for manual merging.
- **git**: Used to clone gate-skills (not required when using `--no-skills`).

## Getting API Keys & Authorization

- **Gate (main)** trading via API keys: **https://www.gate.com/myaccount/profile/api-key/manage** — set `GATE_API_KEY` and `GATE_API_SECRET` in the Gate entry `env`.
- **gate-cex-ex**: Complete **Gate OAuth2** when Claude Code prompts on first use.
- **Gate-Dex**: When a query returns authorization required, open https://web3.gate.com/ for wallet setup, then complete OAuth via the assistant link.

## After Installation

Reopen Claude Code or start a new session to load the MCP servers and skills.
