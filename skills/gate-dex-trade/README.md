# Gate DEX Trade

> **Comprehensive Trading Skill** — MCP + OpenAPI dual modes with intelligent routing

Provides complete Swap trading capabilities through Gate DEX. Designed for AI assistants (Cursor / Claude Code / Windsurf, etc.), supports EVM multi-chain + Solana, supports cross-chain Swap.

---

## Quick Start

```bash
cd gate-dex-trade
./install.sh
```

Verify: `"Swap 100 USDT for ETH"` or `"Use OpenAPI mode to swap"`

---

## Mode Overview

| Dimension | MCP Mode | OpenAPI Mode |
|-----------|----------|-------------|
| **Connection** | Gate Wallet MCP Server | Direct AK/SK API |
| **Authentication** | mcp_token (OAuth login) | HMAC-SHA256 signature |
| **Execution** | One-shot (single call) | Step-by-step lifecycle |
| **Cross-chain** | Supported | Same-chain only |
| **Three-step Confirmation** | Mandatory | Mandatory |

---

## Trigger Keywords

- **Trading**: `swap`, `exchange`, `buy`, `sell`, `trade`, `cross-chain`
- **Queries**: `quote`, `rate`, `gas fees`, `slippage`, `transaction status`
- **Mode**: `OpenAPI mode`, `AK/SK`, `MCP mode`

---

## Routing Flow

```text
User triggers trading intent
  ↓
Explicitly specify mode?
  ├─ "OpenAPI/AK/SK" → references/openapi.md
  ├─ "MCP" → MCP mode (guide setup on failure)
  └─ Not specified → Environment detection
  ↓
Cross-chain Swap?
  ├─ Yes → Force MCP mode
  └─ No → MCP Server detection
  ↓
MCP Server available?
  ├─ Yes → references/mcp.md
  └─ No → Prompt setup + fallback to references/openapi.md
```

---

## File Architecture

```text
gate-dex-trade/
├── SKILL.md              # Pure routing layer (AI reads this first)
├── README.md             # This document (human-facing)
├── CHANGELOG.md          # Change log
├── install.sh            # Interactive installation script
└── references/
    ├── mcp.md            # MCP mode complete specification
    ├── openapi.md        # OpenAPI mode complete specification
    └── setup.md          # MCP Server setup guide (multi-platform)
```

---

## Cross-Skill Collaboration

| Source Skill | Scenario | Information Passed |
|-------------|----------|-------------------|
| `gate-dex-wallet` | Trade after viewing balance | Chain, token addresses, balance |
| `gate-dex-market` | Buy after viewing market data | Token info, price, market cap |
| `gate-dex-wallet/references/transfer.md` | Exchange remaining after transfer | Chain, tokens, wallet addresses |

---

## Related Skills

- **[gate-dex-wallet](../gate-dex-wallet/)** — Wallet (authentication, assets, transfers, DApp)
- **[gate-dex-market](../gate-dex-market/)** — Market data queries (quotes, rankings, audits)
