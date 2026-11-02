# Gate MCP unified installer (MCP + Skills)

One script for **Cursor**, **Claude Code**, **Codex**, and **OpenClaw** (`mcporter`): installs selected Gate MCP servers and copies non-CEX skills from [gate-skills](https://github.com/gate/gate-skills).

Legacy Pay exchange transport: local stdio (`gate-mcp`), remote public (`/mcp`), remote exchange (`/mcp/exchange` + OAuth2). See [gate-mcp](https://github.com/gate/gate-mcp).

**Gate Pay** (optional): **`--mcp gatepay-local`** for x402 stdio (`npx -y gatepay-local-mcp`); **`--mcp gatepay-discovery`** for remote merchant catalog (`gatepay-merchant-discovery` → `discoveryResource`). Details: **gate-pay-x402** skill.

Merchant discovery uses the public HTTPS URL
`https://openplatform.gateapi.io/pay-mcp-server/mcp`, matching the
[Pay setup contract](../gate-pay-x402/SKILL.md). It only lists merchant resources;
payment tools run on the separately configured payment MCP. Neither Pay entry is
installed by default.

**Gate Verify (tx check-in)** uses a **second HTTP MCP** (`https://api.gatemcp.ai/mcp/dex/sec`). This installer registers it as **`gate-dex-sec`** whenever **`gate-dex`** is installed. Call MCP **`tx_checkin`** / **`/v1/tx/checkin`** with wallet **`mcp_token`** in tool args — **gate-dex-wallet** `references/tx-checkin.md`.

## Quick start

CEX business skills use the separate CLI standalone-package flow. Source copying skips `gate-cex-*` and legacy `gate-exchange-*` directories except `gate-exchange-pay`; existing installations are left in place. Exchange server configuration modes remain available for Pay.

Without `--mcp`, the default service selection is `main`, `cex-public`,
`cex-exchange`, `dex`, `info`, and `news`; selecting `dex` also installs
`gate-dex-sec`. Choose the required subset when a product does not need all of them.
For CEX packages, use the [repository CEX guide](../../README.md#gate-cex-skill-20).

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
# Gate Pay merchant discovery over HTTPS (optional)
bash skills/gate-mcp-installer/scripts/install.sh --platform cursor --mcp gatepay-discovery

# Both x402 services, without copying skills; configure the payment wallet locally.
bash skills/gate-mcp-installer/scripts/install.sh --platform cursor --mcp gatepay-local --mcp gatepay-discovery --no-skills

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
- **gatepay-merchant-discovery**: public HTTPS URL wired by installer; no payment-wallet secrets belong on this catalog entry — see [gate-pay-x402](../gate-pay-x402/SKILL.md) for **`discoveryResource`**

Restart the client after install.
