# Gate Cursor One-Click Installer (MCP + Skills)

One-click installation of Gate MCP servers and all [gate-skills](https://github.com/gate/gate-skills) skills for Cursor.

CEX: **Local** (`npx -y gate-mcp`), **Remote public** (`/mcp`), **Remote exchange** (`/mcp/exchange` + OAuth2). See [gate-mcp](https://github.com/gate/gate-mcp).

## Installation

### One-click install from this repository

```bash
# Run from the gate-skills repository root
bash skills/gate-mcp-cursor-installer/scripts/install.sh
```

### Install MCP only (without gate-skills)

```bash
bash skills/gate-mcp-cursor-installer/scripts/install.sh --no-skills
```

### Install specific MCPs only

```bash
# Local CEX + Dex
bash skills/gate-mcp-cursor-installer/scripts/install.sh --mcp main --mcp dex

# Remote CEX public + exchange
bash skills/gate-mcp-cursor-installer/scripts/install.sh --mcp cex-public --mcp cex-exchange
```

## What Gets Installed

| Component | Description |
|-----------|-------------|
| **Gate** (`main`) | Local CEX, `npx -y gate-mcp`, [gate-mcp](https://github.com/gate/gate-mcp) |
| **gate-cex-pub** (`cex-public`) | `https://api.gatemcp.ai/mcp` — no auth (URL + transport only) |
| **gate-cex-ex** (`cex-exchange`) | `https://api.gatemcp.ai/mcp/exchange` — Gate OAuth2 |
| **Gate-Dex** | `https://api.gatemcp.ai/mcp/dex` (x-api-key + Bearer) |
| **Gate-Info** | `https://api.gatemcp.ai/mcp/info` |
| **Gate-News** | `https://api.gatemcp.ai/mcp/news` |
| **gate-skills** | Cloned from [gate-skills](https://github.com/gate/gate-skills), installs all skills under `skills/` |

## Config File Locations

- **MCP config**: `~/.cursor/mcp.json` (Windows: `%APPDATA%\Cursor\mcp.json`), merged with existing config.
- **Skills**: `~/.cursor/skills/` (Windows: `%APPDATA%\Cursor\skills`).

## Dependencies

- **Bash**: Required to run `install.sh` (built-in on macOS/Linux; use Git Bash or WSL on Windows).
- **Node.js**: Used to merge `mcp.json`; if Node is unavailable, the script outputs a JSON snippet for manual merging.
- **git**: Used to clone gate-skills (not required when using `--no-skills`).

## Getting API Keys & Authorization

- **Gate (main)**: API Key + Secret — **https://www.gate.com/myaccount/profile/api-key/manage**
- **gate-cex-ex**: OAuth2 when Cursor prompts on first connect.
- **Gate-Dex**: https://web3.gate.com/ for wallet; then OAuth via assistant link.

## After Installation

Restart Cursor to load the new MCP servers and skills.
