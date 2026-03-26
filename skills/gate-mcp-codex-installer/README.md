# Gate Codex One-Click Installer (MCP + Skills)

One-click installation of Gate MCP servers and all [gate-skills](https://github.com/gate/gate-skills) skills for **Codex**.

CEX: **Local** (`gate-mcp` stdio), **Remote public** (`/mcp`), **Remote exchange** (`/mcp/exchange` + OAuth2). See [gate-mcp](https://github.com/gate/gate-mcp).

## Installation

### One-click install from this repository

```bash
# Run from the gate-skills repository root
bash skills/gate-mcp-codex-installer/scripts/install.sh
```

### Install MCP only (without gate-skills)

```bash
bash skills/gate-mcp-codex-installer/scripts/install.sh --no-skills
```

### Install specific MCPs only

```bash
# Local + Dex
bash skills/gate-mcp-codex-installer/scripts/install.sh --mcp main --mcp dex

# Remote CEX only
bash skills/gate-mcp-codex-installer/scripts/install.sh --mcp cex-public --mcp cex-exchange
```

## What Gets Installed

| Component | Description |
|-----------|-------------|
| **Gate** (`main`) | Local CEX, `npx -y gate-mcp`, [gate-mcp](https://github.com/gate/gate-mcp) |
| **gate-cex-pub** (`cex-public`) | `https://api.gatemcp.ai/mcp` |
| **gate-cex-ex** (`cex-exchange`) | `https://api.gatemcp.ai/mcp/exchange` (OAuth2) |
| **gate-dex** | `https://api.gatemcp.ai/mcp/dex` |
| **gate-info** | `https://api.gatemcp.ai/mcp/info` |
| **gate-news** | `https://api.gatemcp.ai/mcp/news` |
| **gate-skills** | Cloned from [gate-skills](https://github.com/gate/gate-skills), installs all skills under `skills/` |

## Config File Locations

- **MCP config**: `~/.codex/config.toml` (or `$CODEX_HOME/config.toml`), merged with care (append-only for Gate tables).
- **Skills**: `$CODEX_HOME/skills/` (default `~/.codex/skills/`).

## Dependencies

- **Bash**, **Node.js** (optional for some flows), **git** for skills clone unless `--no-skills`.

## Getting API Keys & Authorization

- **Gate (main)**: https://www.gate.com/myaccount/profile/api-key/manage
- **gate-cex-ex**: Gate OAuth2 on first use in Codex.
- **gate-dex**: https://web3.gate.com/ + OAuth as needed.

## After Installation

Restart Codex to load the MCP servers and skills.
