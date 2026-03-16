# Gate DEX Trade

> **Comprehensive Trading Skill** — MCP + OpenAPI dual modes with intelligent routing for automatic optimal trading method selection

Provides complete Swap trading capabilities through Gate DEX, covering quotes, authorization, transaction building, signing, submission, status queries, and the complete trading lifecycle. Designed for AI assistants (Cursor / Claude Code / Windsurf, etc.), supports EVM multi-chain + Solana, supports cross-chain Swap.

## 🔄 Auto-Update Feature

This skill automatically checks for updates from the [Gate Skills Repository](https://github.com/gate/gate-skills/tree/master/skills/gate-dex-trade) **only at session start or first installation**:

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

## Core Capabilities

| Capability | MCP Mode | OpenAPI Mode | Description |
|------------|----------|-------------|-------------|
| **Connection Method** | Gate Wallet MCP Server | Direct AK/SK API calls | Two call methods auto-identified |
| **Authentication** | mcp_token (unified login) | HMAC-SHA256 signature | Authentication isolation, no mixing |
| **Supported Chains** | EVM multi-chain + Solana | EVM multi-chain + Solana + SUI + Tron + Ton | Runtime dynamic support list retrieval |
| **Transaction Execution** | One-shot execution | Step-by-step lifecycle management | Different strategies for different scenarios |
| **Cross-chain Swap** | ✅ Supported | ❌ Same-chain only | Cross-chain requirements auto-route to MCP |
| **Three-step Confirmation** | ✅ Mandatory gateway | ✅ Mandatory gateway | Trading pair confirmation → Quote display → Signature authorization |

---

## Trigger Methods

- **Trading Intent**: `swap`, `exchange`, `buy`, `sell`, `trade`, `swap X for Y`, `cross-chain`
- **Quote Queries**: `quote`, `rate`, `gas fees`, `slippage`, `price impact`
- **Status Queries**: `transaction status`, `order status`, `trading history`
- **Mode Specification**: `OpenAPI mode`, `AK/SK`, `MCP mode`

---

## Intelligent Routing Flow

SKILL.md serves as pure routing layer, automatically selecting optimal mode based on environment:

```text
User triggers trading intent
  ↓
Explicitly specify mode?
  ├─ Specify "OpenAPI/AK/SK" → references/openapi.md
  ├─ Specify "MCP" → MCP mode (guide installation on failure)
  └─ Not specified → Environment detection
  ↓
Cross-chain Swap?
  ├─ Yes → Force MCP mode (OpenAPI doesn't support cross-chain)
  └─ No → MCP Server detection
  ↓
MCP Server available?
  ├─ Yes → references/mcp.md
  └─ No → Prompt MCP installation + fallback to references/openapi.md
```

---

## Operation Flow Comparison

### MCP Mode Flow

1. **Pre-checks**: MCP Server connectivity verification (`chain.config`)
2. **Authentication verification**: Confirm `mcp_token` validity, guide login if none
3. **Parameter collection**: from_token, to_token, amount, chain, slippage
4. **Supported chain verification**: Read `swap://supported_chains` Resource
5. **Balance validation**: Call `wallet.get_token_list` to verify balance and resolve addresses
6. **Get wallet addresses**: Call `wallet.get_addresses`
7. **SOP three-step confirmation**:
   - Step 1: Trading pair confirmation (Table display)
   - Step 2: Quote display (`tx.quote` + value difference check)
   - Step 3: Signature authorization confirmation
8. **One-shot execution**: `tx.swap` completes entire process in single call
9. **Status polling**: `tx.swap_detail` polling every 5s until final state

### OpenAPI Mode Flow

1. **Environment detection**: Read/create `~/.gate-dex-openapi/config.json`
2. **Credential verification**: AK/SK validity check
3. **Parameter collection**: Chain, tokens, wallet, slippage, etc.
4. **SOP three-step confirmation**:
   - Step 1: Trading pair confirmation
   - Step 2: Quote details (`trade.swap.quote` + price difference warning)
   - Step 3: Signature authorization confirmation
5. **Step-by-step execution**:
   - `trade.swap.build` build transaction
   - If approval needed: approve (EVM/Tron non-native tokens)
   - Sign transaction
   - `trade.swap.submit` submit and broadcast
6. **Status polling**: `trade.swap.status` until completion

---

## MCP Tools & Resources

### Core MCP Tools

| Tool | Function | Description |
|------|----------|-------------|
| `tx.quote` | Get Swap quote | Exchange rate, routing, Gas, price impact, authorization requirements |
| `tx.swap` | One-shot execution | Quote→Build→Sign→Submit completed in single call |
| `tx.swap_detail` | Query transaction status | Execution status and details of submitted Swap |
| `wallet.get_token_list` | Token balance query | Resolve token symbols to contract addresses |
| `wallet.get_addresses` | Wallet address retrieval | EVM / SOL addresses |

### MCP Resources

| URI | Description |
|-----|-------------|
| `swap://supported_chains` | List of Swap-supported chains (grouped by evm / solana) |

---

## OpenAPI Action Interfaces

| Action | Function | Signature Required |
|--------|----------|--------------------|
| `trade.swap.chain` | Get supported chain list | Yes |
| `trade.swap.gas` | Query Gas prices | Yes |
| `trade.swap.quote` | Get Swap quote | Yes |
| `trade.swap.approve` | Get authorization info | Yes |
| `trade.swap.build` | Build transaction | Yes |
| `trade.swap.sign` | Transaction signing | Yes |
| `trade.swap.submit` | Submit transaction | Yes |
| `trade.swap.status` | Query transaction status | Yes |
| `trade.swap.orders` | Query historical orders | Yes |

All interfaces use unified endpoint: `POST https://openapi.gateweb3.cc/api/v1/dex`, distinguished by `action` parameter.

---

## Configuration Requirements

### MCP Mode Configuration

```text
Server Name: gate-wallet (recommended, customizable)
Type: HTTP
URL: https://api.gatemcp.ai/mcp/dex

Platform configuration examples:
▸ Cursor: ~/.cursor/mcp.json
▸ Claude Code: ~/.claude.json or project .mcp.json
▸ Windsurf: ~/.codeium/windsurf/mcp_config.json
```

### OpenAPI Mode Configuration

```text
Config file: ~/.gate-dex-openapi/config.json
Endpoint: https://openapi.gateweb3.cc/api/v1/dex
Authentication: HMAC-SHA256 signature

Config structure:
{
  "api_key": "ak_****",
  "secret_key": "sk_****",
  "default_slippage": 0.005
}
```

---

## Security Mechanisms

### Authentication Security
- **MCP Mode**: mcp_token authentication, never display in plaintext, use `<mcp_token>` placeholder in examples
- **OpenAPI Mode**: Secret Key only show last 4 digits (e.g., `sk_****z4h`), full key stored in config file
- **Permission Isolation**: Recommend config directory `chmod 700`, config file `chmod 600`

### Transaction Security
- **Three-step confirmation gateway**: Trading pair confirmation → Quote display → Signature authorization confirmation, cannot be skipped
- **Risk control**: Forced warning for exchange value difference > 5%, high slippage MEV attack warnings
- **Balance pre-check**: Verify asset sufficiency and Gas token balance before trading
- **No retry on failure**: Don't auto-retry after transaction failure, display error information

### Data Security
- **Desensitized display**: account_id displayed as `acc_12...89` format
- **Config isolation**: Config files stored in user home directory, not in workspace, not tracked by git
- **No security downgrade on fallback**: Security rules remain consistent when falling back from MCP to OpenAPI

---

## Supported Blockchains

The following are common chain references, actual support list based on runtime queries:

| Chain ID | Network Name | Native Token | Type |
|----------|-------------|-------------|------|
| `1` | Ethereum | ETH | EVM |
| `56` | BNB Smart Chain | BNB | EVM |
| `137` | Polygon | POL | EVM |
| `42161` | Arbitrum One | ETH | EVM |
| `10` | Optimism | ETH | EVM |
| `8453` | Base | ETH | EVM |
| `43114` | Avalanche C-Chain | AVAX | EVM |
| `501` | Solana | SOL | Solana |
| `784` | SUI | SUI | SUI |
| `195` | Tron | TRX | Tron |
| `607` | Ton | TON | Ton |

**Dynamic Queries**:
- MCP mode: Read `swap://supported_chains` Resource
- OpenAPI mode: Call `trade.swap.chain` Action

---

## File Architecture

```text
gate-dex-trade/
├── SKILL.md                    # Pure routing layer: environment detection + mode dispatch
├── README.md                   # This document (integration guide)
├── CHANGELOG.md                # Change log
├── install.sh                  # Interactive installation script
└── references/                 # Sub-module complete specifications
    ├── mcp.md                  # MCP mode complete specification (1179 lines)
    └── openapi.md              # OpenAPI mode complete specification (1537 lines)
```

**Execution flow**: SKILL.md (routing) → references/mcp.md or openapi.md (complete specifications) → Execute according to specifications

---

## Cross-Skill Collaboration

| Source Skill | Collaboration Scenario | Information Passed |
|-------------|----------------------|-------------------|
| `gate-dex-wallet` | Exchange tokens after viewing balance | Chain, token addresses, balance context |
| `gate-dex-market` | Buy tokens after viewing market data | Token information, price, market cap data |
| `gate-dex-transfer` | Exchange remaining tokens after transfer | Chain, tokens, wallet addresses |

---

## Related Skills

- **[gate-dex-wallet](../gate-dex-wallet/)** — Wallet comprehensive (authentication, assets, transfers, DApp)
- **[gate-dex-market](../gate-dex-market/)** — Market data queries (quotes, rankings, audits)

---

## Installation & Configuration Guide

### 🚀 Method 1: One-click Installation Script (Recommended)

```bash
cd gate-dex-trade
./install.sh
```

**Features**: Auto-detect AI platforms, configure MCP Server, generate routing files, set up OpenAPI fallback

**Installation Verification**:
```text
💬 "Swap 100 USDT for ETH"
💬 "Use OpenAPI mode to swap"
```

### 🛠️ Method 2: Manual Configuration

<details>
<summary><strong>Platform Configuration Essentials</strong></summary>

**Core Steps**:
1. Configure MCP Server: `gate-dex` + `https://api.gatemcp.ai/mcp/dex`
2. Link Skills directory to platform-specific location
3. Create routing files (optional)

**Cursor**:
```bash
# ~/.cursor/mcp.json - Complete configuration template
{
  "mcpServers": {
    "gate-dex": {
      "transport": "http",
      "url": "https://api.gatemcp.ai/mcp/dex",
      "headers": {
        "Authorization": "Bearer <your_mcp_token>"
      }
    }
  }
}

# Link Skills
mkdir -p .cursor/skills
ln -s "$(pwd)/gate-dex-trade" ".cursor/skills/gate-dex-trade"
```

**Claude Code**:
```bash
# Project-level configuration - .mcp.json
{
  "mcpServers": {
    "gate-dex": {
      "type": "url",
      "url": "https://api.gatemcp.ai/mcp/dex",
      "headers": {
        "Authorization": "Bearer <your_mcp_token>"
      }
    }
  }
}

# CLAUDE.md routing file
echo '# 🔄 Swap, exchange → gate-dex-trade/SKILL.md' > CLAUDE.md
```

**Other Platforms**: Follow above format, add gate-wallet MCP Server to corresponding config files

**🔐 Authentication Instructions**:
- `<your_mcp_token>` obtained through first MCP call automatically
- When no token, will auto-guide OAuth authentication (supports Google OAuth or Gate OAuth)
- Token automatically saved and refreshed after successful authentication

</details>

### 🔧 Method 3: OpenAPI Standalone Mode

Suitable for environments without MCP support or same-chain trading only:

```bash
# Create configuration
mkdir -p ~/.gate-dex-openapi && chmod 700 ~/.gate-dex-openapi
cat > ~/.gate-dex-openapi/config.json << 'EOF'
{
  "api_key": "ak_default_demo_key",
  "secret_key": "sk_default_demo_key_PLACEHOLDER",
  "default_slippage": 0.005,
  "base_url": "https://openapi.gateweb3.cc/api/v1/dex"
}
EOF
chmod 600 ~/.gate-dex-openapi/config.json

# Link Skills (Cursor example)
mkdir -p .cursor/skills
ln -s "$(pwd)/gate-dex-trade" ".cursor/skills/gate-dex-trade"
```

**Limitations**: ❌ No cross-chain Swap support, ✅ Supports complete same-chain transaction lifecycle

---

## Verification & Troubleshooting

### 🔍 Connection Testing

**MCP Connection Diagnosis Standard Process**:
```text
# Step 1: Basic connection test
CallMcpTool(server="gate-dex", toolName="chain.config", arguments={"chain": "ETH"})

# Step 2: Tool availability verification
CallMcpTool(server="gate-dex", toolName="tx.quote", arguments={"from_token": "ETH", "to_token": "USDT", "amount": "0.1", "chain": "1"})

# Step 3: Authentication status check (if above fails)
Check if config file contains correct Authorization header
```

**OpenAPI Test**: `"Use OpenAPI mode to query supported chain list"`

### 🎯 Function Verification

```text
💬 "Check quote from ETH to USDC"
💬 "Swap USDT on ETH chain for SOL on Solana"  (cross-chain, MCP only)
```

### ❌ Connection Issue Standard Handling

| Symptom | Diagnosis | Solution |
|---------|-----------|----------|
| `MCP server not found` | Config missing | Check if mcp.json contains gate-dex config |
| `Connection refused` | Network/URL issue | Verify URL: `https://api.gatemcp.ai/mcp/dex` |
| `401 Unauthorized` | Authentication failure | 1. Check Authorization header config<br>2. Execute initial auth to get token<br>3. Verify token not expired |
| `403 Forbidden` | Insufficient permissions | Contact admin to check API permissions |
| `Tool not found: tx.quote` | Server function mismatch | Confirm connection to correct gate-wallet MCP Server |
| `Cross-chain not supported` | Using OpenAPI mode | Switch to MCP mode or use same-chain trading |

**Connection Recovery Process**:
1. **Config Check** → Confirm complete MCP configuration template
2. **Network Test** → ping/curl verify API endpoint reachability  
3. **Authentication Reset** → Clear old token, re-execute OAuth authentication (Google OAuth or Gate OAuth)
4. **Fallback Handling** → Temporarily use OpenAPI mode to complete transaction

---

## Obtaining Credentials

### 🔗 MCP Mode
- **Method**: OAuth authentication (Google OAuth or Gate OAuth), completely free
- **Features**: Unified authentication, shared rate limiting

### ⚡ OpenAPI Mode
- **Default Credentials**: Auto-available, shared rate limiting
- **Dedicated AK/SK**: Obtain from [Gate DEX Developer Platform](https://www.gatedex.com/developer), higher rate limits

**Dedicated Key Application**: Visit developer platform → Register account → Create application → Get AK/SK → Update config file