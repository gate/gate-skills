# Gate MCP unified installer (MCP + Skills)

One script for **Cursor**, **Claude Code**, **Codex**, and **OpenClaw** (`mcporter`): installs Gate MCP servers and clones [gate-skills](https://github.com/gate/gate-skills).

CEX: local stdio (`gate-mcp`), remote public (`/mcp`), remote exchange (`/mcp/exchange` + OAuth2). See [gate-mcp](https://github.com/gate/gate-mcp).

**Gate Pay** (optional): **`--mcp gatepay-local`** for x402 stdio (`npx -y gatepay-local-mcp`); **`--mcp gatepay-discovery`** for remote merchant catalog (`gatepay-merchant-discovery` → `discoveryResource`). Details: **gate-pay-x402** skill.

**Gate Verify (tx check-in)** uses a **second HTTP MCP** (`https://api.gatemcp.ai/mcp/dex/sec`). This installer registers it as **`gate-dex-sec`** whenever **`gate-dex`** is installed. Call MCP **`tx_checkin`** / **`/v1/tx/checkin`** with wallet **`mcp_token`** in tool args — **gate-dex-wallet** `references/tx-checkin.md`.

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

# Gate Pay x402 stdio (optional)
bash skills/gate-mcp-installer/scripts/install.sh --platform cursor --mcp gatepay-local
# Gate Pay merchant discovery HTTP (optional)
bash skills/gate-mcp-installer/scripts/install.sh --platform cursor --mcp gatepay-discovery

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
- **Gate Verify (tx check-in)**: **`gate-dex-sec`** MCP (installed with **gate-dex**); workflow in **gate-dex-wallet** `references/tx-checkin.md`  
- **gatepay-local-mcp**: replace placeholder **`env`** in MCP config per **gate-pay-x402** (`PLUGIN_WALLET_TOKEN`, `EVM_PRIVATE_KEY`, `SVM_PRIVATE_KEY`, …)  
- **gatepay-merchant-discovery**: URL wired by installer; no keys — see **gate-pay-x402** for **`discoveryResource`**

Restart the client after install.
