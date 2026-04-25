# Gate DEX Market

> **Comprehensive Market Data Skill** — Dual-mode MCP + OpenAPI with intelligent routing for optimal call selection

Provides complete market data query capabilities through Gate DEX, supporting K-line charts, token information, security audits, rankings, and more.

## 🔄 Auto-Update Feature

This skill automatically checks for updates from the [Gate Skills Repository](https://github.com/gate/gate-skills/tree/master/skills/gate-dex-market) **only at session start or first installation**:

- ⚡ **Performance Optimized**: Only checks once per session (no interaction delays)
- 🕐 **Smart Cooldown**: 1-hour minimum between version checks
- ✅ **Session Caching**: Skip repeated checks within the same session
- 🛡️ **Stable Operation**: Update failures never interrupt normal functionality  
- 🔍 **Version Tracking**: Current version displayed at session start
- 🌐 **Remote Source**: Official Gate Skills repository on GitHub

**Update Timing**:
- 🚀 **Session Start**: Check once when session begins
- 📦 **First Install**: Check during initial skill installation  
- 🔧 **Manual Trigger**: User can request "check for updates"
- ❌ **Never**: During normal user interactions (for performance)

**Update Rules**:
- 📈 Update: Local version < Remote version
- ⏭️ Skip: Remote skill doesn't exist or Local version ≥ Remote  
- 💡 User-friendly notifications for all update statuses

---

## 🎯 Core Modes

| Mode | Connection Method | Features | Use Cases |
|------|------------------|----------|-----------|
| 🔗 **MCP Mode** | gate-dex MCP Server | No credentials required, high integration | Wallet collaboration, unified sessions |
| ⚡ **OpenAPI Mode** | Direct AK/SK calls | Independent & fast, feature-rich | Independent queries, lightweight scenarios |

---

## 🚀 Quick Installation

### Option 1: Auto Install Script (Recommended)

```bash
# Run market data specialized install script
./gate-dex-market/install.sh
```

Script features:
- 🔍 Auto-detect AI platforms and configure
- 📈 Optimize market data Skill loading order
- 📊 Configure MCP + OpenAPI dual-mode support
- 🎯 Generate market data prioritized routing files

### Option 2: Manual Configuration

Detailed configuration methods see [Root README.md](https://github.com/gate/gate-skills/blob/master/README.md).

---

## 🚀 Quick Usage

### Trigger Keywords

- **Market Data**: `K-line`, `quotes`, `price trends`, `trading volume`
- **Token Information**: `token details`, `holder analysis`, `new token discovery`
- **Security Audit**: `token security`, `risk check`, `honeypot detection`
- **Rankings**: `gainers list`, `volume ranking`, `trending tokens`

### Example Conversations

```text
💬 "Show me the K-line chart for USDT on ETH"    → Auto-select best mode
💬 "Latest token security audit report"          → Security risk analysis  
💬 "Today's top gaining tokens ranking"          → Rankings query
```

---

## 📁 File Structure

```text
gate-dex-market/
├── README.md              # This document
├── SKILL.md               # Agent dual-mode routing specification
├── CHANGELOG.md           # Change log
└── references/            # Sub-module reference docs
    ├── mcp.md             # 🔗 MCP mode detailed specification
    └── openapi.md         # ⚡ OpenAPI mode detailed specification
```

**MCP Mode** detailed specification see `references/mcp.md`.
**OpenAPI Mode** detailed specification see `references/openapi.md`.

---

## 🔧 Prerequisites

**MCP Mode**:
- Server Name: `gate-dex`
- URL: `https://api.gatemcp.ai/mcp/dex`

**OpenAPI Mode**:
- Config file: `~/.gate-dex-openapi/config.json`
- Endpoint: `https://openapi.gateweb3.cc/api/v1/dex`

Detailed configuration methods see [Root README.md](https://github.com/gate/gate-skills/blob/master/README.md).

---

## 🔗 Related Skills

- [gate-dex-wallet](https://github.com/gate/gate-skills/tree/master/skills/gate-dex-wallet) — Wallet comprehensive (auth, assets, transfer, DApp)
- [gate-dex-trade](https://github.com/gate/gate-skills/tree/master/skills/gate-dex-trade) — Trading execution