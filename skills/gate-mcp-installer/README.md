# Gate MCP unified installer (MCP + Skills)

One script for **Cursor**, **Claude Code**, **Codex**, and **OpenClaw** (`mcporter`): installs Gate MCP servers and clones [gate-skills](https://github.com/gate/gate-skills).

CEX: local stdio (`gate-mcp`), remote public (`/mcp`), remote exchange (`/mcp/exchange` + OAuth2). See [gate-mcp](https://github.com/gate/gate-mcp).

## Quick start

```bash
bash skills/gate-mcp-installer/scripts/install.sh
```

If several clients are installed, pick one:

```bash
bash skills/gate-mcp-installer/scripts/install.sh --platform cursor
```

## Common options

```bash
# MCP only
bash skills/gate-mcp-installer/scripts/install.sh --no-skills

# Subset
bash skills/gate-mcp-installer/scripts/install.sh --mcp main --mcp cex-public

# OpenClaw interactive (single server)
bash skills/gate-mcp-installer/scripts/install.sh --platform openclaw --select
```

## Paths

| Platform | MCP | Skills |
|----------|-----|--------|
| Cursor | `~/.cursor/mcp.json` | `~/.cursor/skills/` |
| Claude | `~/.claude.json` | `~/.claude/skills/` |
| Codex | `~/.codex/config.toml` | `~/.codex/skills/` |
| OpenClaw | `mcporter` | `~/.openclaw/skills/` |

Windows Cursor: `%APPDATA%\Cursor\mcp.json` and `...\skills`.

## Dependencies

- **bash**, **git** (for skills; skip with `--no-skills`)
- **Node.js** + **npx** for JSON merge (Cursor/Claude) and for local `gate-mcp`
- **mcporter** for OpenClaw (`npm install -g mcporter`)

## Keys & OAuth

- **Gate (main)**: https://www.gate.com/myaccount/profile/api-key/manage  
- **gate-cex-ex**: OAuth in IDE; OpenClaw: `mcporter auth gate-cex-ex`  
- **gate-dex**: https://web3.gate.com/ + OAuth when tools require it  

Restart the client after install.
