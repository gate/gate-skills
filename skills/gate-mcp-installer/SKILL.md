---
name: gate-mcp-installer
version: "2026.4.14-4"
updated: "2026-04-14"
description: "One-click installer for Gate MCP servers and gate-skills on Cursor, Claude Code, Codex, or OpenClaw/mcporter. When gate-dex is installed, also wires Gate Verify HTTP MCP as gate-dex-sec for MCP tool tx_checkin before wallet signing per gate-dex-wallet. Triggers on 'install Gate MCP', 'Gate skills', 'Gate Verify', 'tx check-in', 'setup Gate Cursor', 'Gate Claude Code', 'Gate Codex', 'OpenClaw Gate', 'mcporter Gate'."
---

# Gate MCP Installer (unified: Cursor / Claude Code / Codex / OpenClaw)

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they exist in the MCP server.

---

## MCP Dependencies

### Required MCP Servers (after install)

| MCP Server | Status |
|------------|--------|
| Gate (main) | ✅ For local CEX (stdio) |
| gate-cex-pub | ✅ Remote public |
| gate-cex-ex | ✅ Remote private (OAuth2) |
| gate-dex | ✅ DEX |
| gate-info | ✅ Info |
| gate-news | ✅ News |
| gatepay-local-mcp | ➕ Optional (Gate Pay x402 stdio; `--mcp gatepay-local`) |
| gatepay-merchant-discovery | ➕ Optional (HTTP merchant catalog / `discoveryResource`; `--mcp gatepay-discovery`) |
| Gate Verify (tx check-in) | ✅ HTTP MCP **`https://api.gatemcp.ai/mcp/dex/sec`** — merged as **`gate-dex-sec`** (Cursor / Claude / Codex / mcporter) **whenever `dex` is installed**; call **`tx_checkin`** / **`/v1/tx/checkin`** per **gate-dex-wallet** |

### Installation Check

- Run this skill’s installer script, or guide the user to run it.
- If multiple dev environments exist on one machine (e.g. Cursor + Claude Code), the script requires `--platform`.

---

## MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), then execute this installer workflow.

- `SKILL.md` — product scope, triggers, and user-facing guidance.
- `references/mcp.md` — execution SOP per platform, verification, and safety rules.

---

## Platform matrix

| Platform | MCP / transport config | Skills directory |
|----------|-------------------------|------------------|
| **Cursor** | `~/.cursor/mcp.json` (Windows: `%APPDATA%\Cursor\mcp.json`) | `~/.cursor/skills/` |
| **Claude Code** | `~/.claude.json` (`mcpServers`) | `~/.claude/skills/` |
| **Codex** | `~/.codex/config.toml` (`[mcp_servers.*]`) | `~/.codex/skills/` |
| **OpenClaw** | `mcporter` CLI (no single JSON file) | `~/.openclaw/skills/` (default) |

---

## CEX MCP modes

See [gate-mcp](https://github.com/gate/gate-mcp):

| Mode | What | Auth |
|------|------|------|
| **Local CEX** | stdio `npx -y gate-mcp` (or global `gate-mcp`) | Optional `GATE_API_KEY` / `GATE_API_SECRET` |
| **Remote public** | `https://api.gatemcp.ai/mcp` | None |
| **Remote exchange** | `https://api.gatemcp.ai/mcp/exchange` | Gate OAuth2 in client / `mcporter auth gate-cex-ex` |

**Non-CEX** (same host): Dex (`/mcp/dex`), Info (`/mcp/info`), News (`/mcp/news`). Dex uses fixed `x-api-key` `MCP_AK_8W2N7Q` + Bearer `${GATE_MCP_TOKEN}` where applicable.

---

## Tx check-in (Gate Verify / GV)

Gate Verify is a **second HTTP MCP** on the same host as remote DEX, used only for signing check-in:

| Role | Install surface |
|------|------------------|
| Wallet / DEX tools | **`gate-dex`** → `https://api.gatemcp.ai/mcp/dex` (headers per fragment) |
| Gate Verify | **`gate-dex-sec`** → `https://api.gatemcp.ai/mcp/dex/sec` (URL-only / `streamable-http`; **no** wallet HTTP headers on this entry) |

This installer **adds the Verify MCP whenever `--mcp dex` is included** (default full install includes it). Agents call **`tx_checkin`** or **`/v1/tx/checkin`** on the Verify server with **`authorization`** = the same **`mcp_token`** as wallet MCP tool args — see [gate-dex-wallet `references/tx-checkin.md`](https://github.com/gate/gate-skills/blob/master/skills/gate-dex-wallet/references/tx-checkin.md). Staged swap specifics: **gate-dex-trade** skill.

---

## Resources

| Type | Name | Notes |
|------|------|--------|
| MCP | **Gate** (`main`) | stdio; prefer global `gate-mcp` when installed |
| MCP | **gate-cex-pub** | HTTP remote public |
| MCP | **gate-cex-ex** | HTTP remote private + OAuth2 |
| MCP | **gate-dex** | HTTP + headers |
| MCP | **gate-dex-sec** | HTTP `https://api.gatemcp.ai/mcp/dex/sec`; **`tx_checkin`** before signing — bundled with **`dex`** install |
| MCP | **gate-info** / **gate-news** | HTTP |
| MCP | **gatepay-local-mcp** | stdio `npx -y gatepay-local-mcp`; wallet **`env`** per **gate-pay-x402** |
| MCP | **gatepay-merchant-discovery** | HTTP `http://dev.halftrust.xyz/pay-mcp-server/mcp`; catalog only (**gate-pay-x402**) |
| Skill | **gate-dex-wallet** | Routing for Verify MCP + wallet flows — `references/tx-checkin.md` |
| Skills | gate-skills | https://github.com/gate/gate-skills |

---

## Behavior rules

1. **Default**: Install **all six** trading MCP surfaces + **Gate Verify** (bundled with **`dex`**) + **all gate-skills** unless the user opts out. **Gate Pay** MCPs are **not** included by default: add **`--mcp gatepay-local`** (x402 stdio) and/or **`--mcp gatepay-discovery`** (remote merchant catalog) when needed. Omitting **`dex`** also omits the Verify MCP entry.
2. **Selectable**: `--mcp main|cex-public|cex-exchange|dex|info|news|gatepay-local|gatepay-discovery` (repeatable).
3. **Skills**: `--no-skills` installs MCP configuration only.
4. **OpenClaw**: `--select` / `-s` keeps the interactive single-server menu (mcporter legacy UX).

---

## Installer script

Path: **`skills/gate-mcp-installer/scripts/install.sh`**

```bash
# Auto-detect when only one environment matches
bash skills/gate-mcp-installer/scripts/install.sh

# Force platform (required if multiple clients detected)
bash skills/gate-mcp-installer/scripts/install.sh --platform cursor
bash skills/gate-mcp-installer/scripts/install.sh --platform claude
bash skills/gate-mcp-installer/scripts/install.sh --platform codex
bash skills/gate-mcp-installer/scripts/install.sh --platform openclaw

# Subset of MCPs
bash skills/gate-mcp-installer/scripts/install.sh --platform cursor --mcp main --mcp dex

# Gate Pay x402 (stdio) alongside trading MCPs
bash skills/gate-mcp-installer/scripts/install.sh --platform cursor --mcp gatepay-local
# With --mcp main, the script prompts for GATE_API_KEY (CEX local MCP only); gatepay-local-mcp env is separate (gate-pay-x402).
bash skills/gate-mcp-installer/scripts/install.sh --platform cursor --mcp main --mcp gatepay-local

# Gate Pay merchant discovery (HTTP; discoveryResource) — often paired with gatepay-local
bash skills/gate-mcp-installer/scripts/install.sh --platform cursor --mcp gatepay-discovery
bash skills/gate-mcp-installer/scripts/install.sh --platform cursor --mcp gatepay-local --mcp gatepay-discovery --no-skills

# MCP only
bash skills/gate-mcp-installer/scripts/install.sh --no-skills

# OpenClaw interactive pick
bash skills/gate-mcp-installer/scripts/install.sh --platform openclaw --select
```

---

## OpenClaw quick commands (mcporter)

```bash
mcporter list gate-cex-pub
mcporter call gate-info.list_tickers currency_pair=BTC_USDT
mcporter call gate-news.list_news
mcporter call gate.list_spot_accounts
mcporter auth gate-cex-ex
mcporter call gate-dex.list_balances
```

---

## Post-install (all platforms)

- **Restart** the IDE / client (or new session) so MCP lists reload.
- **API Key**: https://www.gate.com/myaccount/profile/api-key/manage for local `Gate (main)` trading.
- **gate-cex-ex**: OAuth2 when the client prompts; OpenClaw: `mcporter auth gate-cex-ex`.
- **gate-dex**: https://web3.gate.com/ for wallet; complete OAuth if tools require it.
- **Gate Verify (`gate-dex-sec`)**: merged with **`dex`**; before signing or **`dex_tx_x402_fetch`**, call **`tx_checkin`** / **`/v1/tx/checkin`** on this MCP with **`authorization`** = wallet **`mcp_token`** (tool argument, not copied HTTP headers) — **gate-dex-wallet** [`references/tx-checkin.md`](https://github.com/gate/gate-skills/blob/master/skills/gate-dex-wallet/references/tx-checkin.md).
- **gatepay-local-mcp**: stdio Gate Pay x402; set **`env`** placeholders in the client config to real values only locally — see **gate-pay-x402** (`PLUGIN_WALLET_TOKEN`, **`EVM_PRIVATE_KEY`**, **`SVM_PRIVATE_KEY`**, optional **`PAYMENT_METHOD_PRIORITY`**).
- **gatepay-merchant-discovery**: remote URL only (no secrets in installer); lists payable resources — confirm tool name (**`discoveryResource`**) in the live tool list (**gate-pay-x402**). If connect fails, adjust **`transport`** in JSON per your host (fragment uses `streamable-http` like other Gate HTTP MCPs).

---

## Supersedes

This skill replaces: `gate-mcp-cursor-installer`, `gate-mcp-claude-installer`, `gate-mcp-codex-installer`, `gate-mcp-openclaw-installer`. Those directories may retain short redirect stubs for backwards compatibility.
