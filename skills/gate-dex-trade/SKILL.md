---
name: gate-dex-trade
version: "2026.3.14-2"
updated: "2026-03-14"
description: "Gate DEX trading comprehensive skill. Supports MCP and OpenAPI dual modes: MCP mode calls through gate-wallet service (requires authentication), OpenAPI mode calls directly through AK/SK. Use when users mention swap, exchange, buy, sell, quote, trade. Automatically select the most suitable calling method based on environment."
---

# Gate DEX Trade

> **Pure Routing Layer** — Environment Detection → Mode Selection → Dispatch to Complete Sub-specifications. This file contains no business logic; all trading specifications are in `references/` sub-files.

**Trigger Scenarios**: Use when users mention "swap", "exchange", "buy", "sell", "trade", "quote", "convert", "swap X for Y", "cross-chain", "Connect Gate Dex MCP", "Detect Dex MCP", "Check Gate Dex Connection", "MCP Connection Status", "Test MCP Server", and other trading-related operations.

**High Priority Triggers** (Trade-Specific): "swap", "exchange", "buy", "sell", "trade", "convert", "cross-chain", "slippage", "approve token", "transaction"

**Priority Rules**:
1. High priority triggers → Always route to Trade skill
2. Action-oriented language → Trade skill (e.g., "I want to swap", "help me buy")
3. Quote with trading context → Trade skill (e.g., "quote for buying", "swap quote")
4. Cross-chain operations → Always Trade skill (OpenAPI doesn't support cross-chain)

---

## 🎯 Multi-Skill Priority & Routing System

This skill participates in the unified priority system. See Market skill documentation for complete routing rules.

### Trade-Specific Priority Logic

**Immediate Route to Trade if:**
- Action verbs: swap, buy, sell, exchange, trade, convert
- Cross-chain context: "cross-chain swap", "bridge tokens"  
- Trading parameters: slippage, gas fee for trades, approve tokens
- Intent phrases: "I want to trade", "help me swap", "execute trade"

**Auto-Handoff Scenarios:**
1. **Pre-trade Balance Check** → Wallet skill → Return with balance → Continue trade
2. **Post-trade Verification** → Wallet skill → Show updated balances → Trade complete
3. **Market Data Context** → Market skill → Get price analysis → Return for trade decision

---

## 🐾 OpenClaw Platform Integration

### Trading-Specific MCP Patterns for OpenClaw

#### Cross-Chain Swap via mcporter
```javascript
// OpenClaw cross-chain swap example
const crossChainSwap = await CallMcpTool(
  server="mcporter",
  toolName="call_tool",
  arguments={
    server: mcpServerIdentifier,
    tool: "tx.swap",
    arguments: {
      chain_id_in: 1,    // Ethereum
      chain_id_out: 56,  // BSC
      token_in: "ETH",
      token_out: "BNB", 
      amount_in: "0.1",
      slippage: "0.005",
      mcp_token: userMcpToken
    }
  }
);
```

#### Quote Request Pattern
```javascript
// Get swap quote through mcporter
const quote = await CallMcpTool(
  server="mcporter",
  toolName="call_tool",
  arguments={
    server: mcpServerIdentifier,
    tool: "tx.quote",
    arguments: {
      chain_id_in: 1,
      token_in: "USDT",
      token_out: "ETH",
      amount_in: "1000",
      mcp_token: userMcpToken
    }
  }
);
```

#### Transaction Status Monitoring
```javascript
// Monitor swap status via mcporter
const status = await CallMcpTool(
  server="mcporter",
  toolName="call_tool",
  arguments={
    server: mcpServerIdentifier,
    tool: "tx.swap_detail",
    arguments: {
      tx_order_id: swapResult.tx_order_id,
      mcp_token: userMcpToken
    }
  }
);
```

### Token Management for Trading Operations

#### Dynamic Token Validation Before Trading
```javascript
// Check token validity before expensive trading operations
async function validateTokenBeforeTrade() {
  const tokenInfo = await validateCurrentMcpToken();
  
  if (!tokenInfo.isValid) {
    return "Please login first to execute trades. Trading requires authentication.";
  }
  
  // Verify token hasn't changed (account switch scenario)
  if (cachedMcpToken !== tokenInfo.mcp_token) {
    console.log("🔄 Account switched, refreshing trade session...");
    clearTradeCache(); // Clear any cached trade data
  }
  
  return tokenInfo;
}

// Example: Swap with token validation
async function executeSwap(swapParams) {
  const tokenInfo = await validateTokenBeforeTrade();
  if (typeof tokenInfo === 'string') return tokenInfo; // Error message
  
  const result = await callMcpToolWithValidation(
    mcpServerIdentifier,
    "tx.swap",
    {
      ...swapParams,
      // mcp_token auto-injected with fresh value
    }
  );
  
  if (!result.success && result.action === "redirect_to_auth") {
    const platform = await detectCurrentPlatform();
    const claudeHint = platform.name === "claude" ? 
      "\n💡 Claude Code users: Try restarting Claude Code if login doesn't work" : "";
    return "Session expired during trade. Please re-login and try again." + claudeHint;
  }
  
  return result;
}
```

#### Claude Code Trading Specific Issues

Trading operations are particularly sensitive to token expiration due to their multi-step nature (quote → approve → swap → monitor). Claude Code users should be aware of:

- **Long Trade Sequences**: Cross-chain swaps may take 30-60 minutes, during which tokens can expire
- **No Mid-Trade Recovery**: If token expires during a trade sequence, the entire process must restart
- **Higher Frequency Calls**: Trading makes more frequent MCP calls, increasing chance of hitting caching issues

**Recommended Workarounds**:
```text
1. Complete trades within 30 minutes of starting
2. For complex cross-chain operations, consider using CLI mode: `gate-wallet openapi-swap`
3. Keep Claude Code active during trading to prevent idle token expiration
```

---

## 🔄 Auto-Update System

### Version Check and Update (Session Start + Manual)

**Automatically check and update skill version at session initialization - skipping initial installation checks.**

#### Update Timing

1. **Session Start**: Check once when session begins (if not freshly installed)
2. **Manual Trigger**: User can manually request version check  
3. **Installation Skip**: No version check during initial skill installation (assumes latest version)
4. **Interaction Skip**: No version check during normal user interactions

#### Update Rules

1. **Version Check**: Compare local version and updated date with remote repository
2. **Update Conditions**:
   - ✅ Update: Local version < Remote version (primary criterion)
   - ✅ Update: Same version but remote updated date > local updated date (secondary criterion)
   - ❌ No Update: Remote skill doesn't exist
   - ❌ No Update: Local version ≥ Remote version AND local updated date ≥ remote updated date
3. **Error Handling**: Update failures don't affect user experience
4. **Caching**: Skip repeated checks within the same session
5. **Installation Fresh**: Skip checks if skill was just installed (assumes up-to-date)

#### Implementation Process

```javascript
// Session State Management
let sessionVersionChecked = false;
let lastCheckTimestamp = null;
let installTimestamp = null; // Track installation time
const CHECK_COOLDOWN_MS = 3600000; // 1 hour cooldown
const FRESH_INSTALL_WINDOW_MS = 86400000; // 24 hour fresh install window

// Step 1: Session-Based Version Check (with Fresh Install Detection)
async function checkSkillVersionOnSessionStart() {
  // Check if this is a fresh installation first
  if (isSkillFreshlyInstalled()) {
    console.log("🆕 Fresh installation detected, skipping version check...");
    sessionVersionChecked = true;
    return { needsUpdate: false, reason: "fresh_install" };
  }
  
  // Check cooldown time (cross-session persistence)
  const now = Date.now();
  if (lastCheckTimestamp && (now - lastCheckTimestamp) < CHECK_COOLDOWN_MS) {
    console.log("🔄 Version check on cooldown, skipping...");
    return { needsUpdate: false, reason: "cooldown_active" };
  }
  
  // Skip if already checked in this session AND within cooldown
  // This allows re-checking in same session if cooldown has passed
  if (sessionVersionChecked && lastCheckTimestamp && (now - lastCheckTimestamp) < CHECK_COOLDOWN_MS) {
    console.log("🔄 Version already checked this session (within cooldown), skipping...");
    return { needsUpdate: false, reason: "session_already_checked" };
  }
  
  const remoteUrl = "https://raw.githubusercontent.com/gate/gate-skills/master/skills/gate-dex-trade/SKILL.md";
  
  // Dynamically read current skill version and updated date
  const { localVersion, localUpdated } = getCurrentSkillVersion();
  
  try {
    // Mark as checked for this session
    sessionVersionChecked = true;
    lastCheckTimestamp = now;
    
    // Fetch remote skill metadata
    const response = await WebFetch({ url: remoteUrl });
    
    if (response.includes("---") && response.includes("version:")) {
      // Extract remote version and updated date
      const versionMatch = response.match(/version:\s*"([^"]+)"/);
      const updatedMatch = response.match(/updated:\s*"([^"]+)"/);
      const remoteVersion = versionMatch ? versionMatch[1] : null;
      const remoteUpdated = updatedMatch ? updatedMatch[1] : null;
      
      if (remoteVersion && compareVersions(localVersion, remoteVersion) < 0) {
        // Update available based on version comparison - trigger update process
        const updateResults = await performSkillUpdate(remoteVersion);
        return { 
          needsUpdate: true, 
          remoteVersion, 
          localVersion,
          remoteUpdated,
          localUpdated,
          updateResults,
          updated: true
        };
      } else if (remoteVersion === localVersion && remoteUpdated && isUpdatedDateNewer(localUpdated, remoteUpdated)) {
        // Same version but newer updated date - trigger update process
        const updateResults = await performSkillUpdate(remoteVersion);
        return { 
          needsUpdate: true, 
          remoteVersion, 
          localVersion,
          remoteUpdated,
          localUpdated,
          updateResults,
          updated: true,
          reason: "updated_date_newer"
        };
      }
    }
    
    return { needsUpdate: false, localVersion, reason: "up_to_date" };
    
  } catch (error) {
    // Update failure doesn't affect user experience
    console.warn("🔄 Skill version check failed:", error.message);
    return { needsUpdate: false, localVersion, error: error.message, reason: "check_failed" };
  }
}

// Fresh Installation Detection
function isSkillFreshlyInstalled() {
  // Check if installation is within the fresh window (24 hours)
  // This could be implemented by checking file timestamps or installation markers
  try {
    // Example: Check if SKILL.md was modified within last 24 hours
    const skillPath = "gate-dex-trade/SKILL.md";
    const stats = require('fs').statSync(skillPath);
    const now = Date.now();
    const fileAge = now - stats.mtime.getTime();
    
    return fileAge < FRESH_INSTALL_WINDOW_MS;
  } catch (error) {
    // If unable to determine, assume not fresh to be safe
    return false;
  }
}

// Get Current Skill Version from SKILL.md metadata
function getCurrentSkillVersion() {
  try {
    // Read current SKILL.md file content
    const skillContent = require('fs').readFileSync('gate-dex-trade/SKILL.md', 'utf8');
    
    // Extract version and updated from metadata
    const versionMatch = skillContent.match(/version:\s*"([^"]+)"/);
    const updatedMatch = skillContent.match(/updated:\s*"([^"]+)"/);
    
    return {
      localVersion: versionMatch ? versionMatch[1] : "2026.3.14-1", // fallback
      localUpdated: updatedMatch ? updatedMatch[1] : "2026-03-14"   // fallback
    };
  } catch (error) {
    // Fallback to default values if file reading fails
    console.warn("Failed to read current skill version, using fallback:", error.message);
    return {
      localVersion: "2026.3.14-1",
      localUpdated: "2026-03-14"
    };
  }
}

// Step 2: Version Comparison (unchanged)
function compareVersions(local, remote) {
  // Parse version format: "2026.3.14-1"
  const parseVersion = (v) => {
    const [date, build] = v.split('-');
    const [year, month, day] = date.split('.').map(Number);
    return { year, month, day, build: parseInt(build) || 0 };
  };
  
  const localParsed = parseVersion(local);
  const remoteParsed = parseVersion(remote);
  
  // Compare in order: year -> month -> day -> build
  if (localParsed.year !== remoteParsed.year) return localParsed.year - remoteParsed.year;
  if (localParsed.month !== remoteParsed.month) return localParsed.month - remoteParsed.month;
  if (localParsed.day !== remoteParsed.day) return localParsed.day - remoteParsed.day;
  return localParsed.build - remoteParsed.build;
}

// Date Comparison for updated field
function isUpdatedDateNewer(localDate, remoteDate) {
  // Parse date format: "2026-03-14"
  const parseDate = (dateStr) => {
    const [year, month, day] = dateStr.split('-').map(Number);
    return new Date(year, month - 1, day); // month is 0-indexed in Date
  };
  
  const localDateObj = parseDate(localDate);
  const remoteDateObj = parseDate(remoteDate);
  
  return remoteDateObj > localDateObj;
}

// Step 3: Manual Version Check (for user-triggered updates)
async function manualVersionCheck() {
  // Reset session flag to allow manual check
  sessionVersionChecked = false;
  return await checkSkillVersionOnSessionStart();
}

// Step 4: Perform Update (Auto-execution when available)
async function performSkillUpdate(remoteVersion) {
  const baseUrl = "https://raw.githubusercontent.com/gate/gate-skills/master/skills/gate-dex-trade";
  const filesToUpdate = [
    "SKILL.md",
    "README.md", 
    "CHANGELOG.md",
    "install.sh",
    "references/mcp.md",
    "references/openapi.md"
  ];
  
  const results = [];
  
  console.log(`🚀 Starting skill update to version ${remoteVersion}...`);
  
  for (const file of filesToUpdate) {
    try {
      const response = await WebFetch({ url: `${baseUrl}/${file}` });
      if (response && !response.includes("404") && !response.includes("Not Found")) {
        // Write the updated content to local file
        await Write({ 
          path: `gate-dex-trade/${file}`, 
          contents: response 
        });
        results.push({ file, status: "updated", size: response.length });
        console.log(`✅ Updated: ${file}`);
      } else {
        results.push({ file, status: "not_found", reason: "Remote file not accessible" });
        console.log(`⚠️ Skipped: ${file} (not found)`);
      }
    } catch (error) {
      results.push({ file, status: "failed", error: error.message });
      console.log(`❌ Failed: ${file} - ${error.message}`);
    }
  }
  
  console.log(`🎉 Skill update completed. ${results.filter(r => r.status === 'updated').length}/${results.length} files updated.`);
  return results;
}
```

#### User-Friendly Messages

**Session Start Messages**:

```markdown
🔄 **Session Started - Version Check**
- ✅ Local version: 2026.3.14-1 (checking remote...)
- 🌐 Remote repository: Connected successfully
- ⏰ Status: Up to date, no update needed

🆕 **Update Available & Applied** 
- 📦 New version: 2026.3.15-1 discovered
- 🚀 Updating skill components automatically...
  ✅ SKILL.md updated
  ✅ README.md updated  
  ✅ CHANGELOG.md updated
  ✅ install.sh updated
  ✅ references/mcp.md updated
  ✅ references/openapi.md updated
- ✨ Update completed! Now using version 2026.3.15-1

🆕 **Fresh Installation Detected**
- 💫 Skill recently installed (< 24h ago)
- 🎯 Already up-to-date, skipping version check
- ✅ All functions fully operational

⚠️ **Version Check Skipped**
- 🔄 Already checked this session (within cooldown)
- 💡 Using current version: 2026.3.14-1
- 🎯 All functions fully operational

🕐 **Check Cooldown Active**
- ⏰ Last check: 30 minutes ago
- 🔄 Next check available in: 30 minutes  
- ✅ Current version: 2026.3.14-1 (stable)

🔄 **Same Session Re-check (After 1h)**
- ⏰ Previous check was over 1 hour ago
- 🔄 Performing fresh version check...
- ✅ Result: [Up to date / Update applied]
```

#### Performance Optimizations

| Optimization | Description | Benefit |
|-------------|-------------|---------|
| **Session Flag** | `sessionVersionChecked` prevents duplicate checks | Faster interactions |
| **Fresh Install Detection** | Skip checks for recently installed skills (< 24h) | Avoid redundant updates on new installs |
| **Time Cooldown** | 1-hour minimum between checks | Reduced network requests |
| **Interaction Skip** | No checks during normal user queries | Immediate response |
| **Cache Results** | Store check results in session memory | Avoid redundant operations |

#### Manual Update Commands

Users can manually trigger version checks:

```markdown
🔧 **Manual Commands**
- "Check for skill updates" → Force version check
- "Update skill to latest" → Manual update trigger  
- "Skill version info" → Show current version status
```

**Note**: This optimized auto-update system ensures minimal performance impact while maintaining up-to-date functionality. Version checks are intelligently spaced to balance freshness with responsiveness. Fresh installations are assumed to be up-to-date and skip initial version checks for optimal first-time experience.

---

---

## Routing Flow

```text
User triggers trading intent
  ↓
Step 0: MCP Connection Detection (Enhanced Session-Level with Manual Trigger Support)
  Check for manual MCP detection keywords:
  - "Connect Gate Dex MCP", "Detect Dex MCP", "Check Gate Dex Connection" (English)
  - "Connect Gate Dex MCP", "Detect Dex MCP", "Check Gate Dex Connection" (English)
  
  If manual trigger detected → Always execute detection and display results (no caching)
  
  For business operations:
  ├─ MCP connection successful in session → Skip to Step 1 (use cached identifier)
  ├─ MCP connection failed in session → Retry detection (failures don't block retries)
  └─ First MCP operation in session → Perform MCP detection
  
  Enhanced Detection Logic:
  a) Platform Detection (OpenClaw → use mcporter, Others → direct)
  b) Server Discovery with required tools: `tx.quote`, `tx.swap`, `chain.config`
  c) Connection Verification via `chain.config` test call
  d) Smart Caching (success cached, failures allow retry for business ops)
  e) **Dynamic Token Validation**: Check for mcp_token changes before authenticated operations
  ↓
Step 1: Has user explicitly specified a mode?
  ├─ Explicitly mentions "OpenAPI" / "AK/SK" / "API Key" → Go directly to OpenAPI mode
  ├─ Explicitly mentions "MCP" / "MCP Server" → Use Step 0 MCP detection result
  └─ Not specified → Step 2
  ↓
Step 2: Is this a cross-chain swap?
  User intent involves exchanges between different chains (e.g., "swap USDT on ETH for SOL on Solana")
  ├─ Cross-chain → Must use MCP mode (OpenAPI doesn't support cross-chain), use Step 0 result
  └─ Same-chain / uncertain → Step 3
  ↓
Step 3: Mode Selection Based on Step 0 Detection
  ├─ MCP detected successfully → MCP mode (use cached server identifier)
  └─ MCP not available → Step 4
  ↓
Step 4: MCP unavailable
  ├─ User explicitly specified MCP → No fallback, show MCP Server installation guide, abort current operation
  ├─ Cross-chain Swap → No fallback (OpenAPI doesn't support cross-chain), show MCP Server installation guide, abort current operation
  └─ Same-chain Swap and user didn't specify mode → Fallback handling: inform user of MCP Server recommendation (see guide below), complete transaction using OpenAPI mode this time
```

---

## Mode Dispatch

### MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), execute according to its complete workflow.

This specification includes: MCP Server connection detection, authentication (mcp_token), MCP Resource / tool call specifications (tx.quote / tx.swap / tx.swap_detail), token address resolution, native_in/native_out judgment rules, three-step confirmation gateway (SOP), quote templates, risk warnings, cross-Skill collaboration, security rules, etc.

### OpenAPI Mode

**Read and strictly follow** [`references/openapi.md`](./references/openapi.md), execute according to its complete workflow.

This specification includes: environment detection (config file / AK/SK), HMAC-SHA256 signing, 9 Actions (chain list / Gas / quote / approve / build / sign / submit / status / history), three-step confirmation gateway (SOP), multi-chain signing strategies, error handling, etc.

**Limitation: OpenAPI mode only supports same-chain Swap, does not support cross-chain exchanges.** Cross-chain requirements must use MCP mode.

---

## Mode Comparison

| Dimension | MCP Mode | OpenAPI Mode |
|-----------|----------|-------------|
| **Connection Method** | Gate Wallet MCP Server (auto-identified by name) | Direct AK/SK API connection |
| **Authentication** | mcp_token (login authentication) | HMAC-SHA256 signature |
| **Configuration Requirements** | Configure MCP Server in MCP-compatible platform | `~/.gate-dex-openapi/config.json` |
| **Transaction Execution** | One-shot (Quote→Build→Sign→Submit single call) | Step-by-step calls (Quote → Approve → Build → Sign → Submit) |
| **Cross-chain Swap** | ✅ Supported (same-chain + cross-chain) | ❌ Only same-chain Swap |
| **Use Cases** | Wallet ecosystem integration, cross-Skill collaboration, cross-chain trading | Independent execution, same-chain trading, full pipeline control |

Both modes include three-step confirmation gateway (trading pair confirmation → quote display → signature authorization confirmation), with consistent security rules.

---

## MCP Server Installation Guide

When MCP detection fails, display the following guide to users (once only, no repeated prompts):

```
💡 We recommend installing Gate Wallet MCP Server for a better trading experience (unified authentication, One-shot execution, cross-chain Swap, wallet ecosystem integration).

Complete MCP Server configuration information:
  - Name: gate-wallet (recommended, can be customized, system auto-identifies by tool features)
  - Type: HTTP
  - URL: https://api.gatemcp.ai/mcp/dex

Please choose the corresponding configuration method based on your AI platform:

▸ Cursor
  Method A: Settings → MCP → Add new MCP server → Fill in the above information
  Method B: Edit ~/.cursor/mcp.json:
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

▸ Claude Code
  Edit ~/.claude.json (or project directory .mcp.json):
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

▸ Windsurf
  Edit ~/.codeium/windsurf/mcp_config.json:
  {
    "mcpServers": {
      "gate-dex": {
        "transport": "http",
        "serverUrl": "https://api.gatemcp.ai/mcp/dex",
        "headers": {
          "Authorization": "Bearer <your_mcp_token>"
        }
      }
    }
  }

▸ Other MCP-compatible platforms
  Add the above HTTP-type Server in the platform's MCP configuration, including authentication header configuration.

🔐 Authentication Instructions:
  - <your_mcp_token> needs to be obtained through MCP login process
  - On first use, if there's no token, MCP Server will guide you to complete OAuth authentication (supports Google OAuth or Gate OAuth)
  - Token is automatically saved after acquisition, subsequent calls will use it automatically

🔧 Connection Verification:
  After configuration is complete, you can verify the connection with:
  CallMcpTool(server="gate-dex", toolName="chain.config", arguments={"chain": "ETH"})

After installation and authentication, future transactions will automatically use MCP mode. This transaction continues with OpenAPI mode.
```

> **Server name not mandatory**: Users can configure MCP Server with any name. The routing layer auto-identifies by tool features (whether it provides `tx.quote` + `tx.swap`), not dependent on fixed names.
>
> **Platform adaptation**: When Agent displays guidance, show only the configuration method for the current runtime environment, not all. Display complete list when platform cannot be determined.
>
> **Authentication handling**: On first connection, if authentication fails, automatically guide users to complete OAuth login process (supports Google OAuth or Gate OAuth), no manual token configuration needed.

---

## Supported Chains

The actual supported chains for both modes are determined by their respective API/Resource runtime returns:
- **MCP Mode**: Get real-time support list through `swap://supported_chains` Resource
- **OpenAPI Mode**: Get real-time support list through `trade.swap.chain` interface

The following are common chain references (incomplete, for quick reference only):

| chain_id | Network Name | Native Token |
|----------|-------------|-------------|
| `1` | Ethereum | ETH |
| `56` | BNB Smart Chain | BNB |
| `137` | Polygon | POL |
| `42161` | Arbitrum One | ETH |
| `10` | Optimism | ETH |
| `43114` | Avalanche C-Chain | AVAX |
| `8453` | Base | ETH |
| `501` | Solana | SOL |
| `59144` | Linea | ETH |
| `324` | zkSync Era | ETH |
| `81457` | Blast | ETH |
| `784` | Sui | SUI |
| `195` | Tron | TRX |
| `607` | Ton | TON |
| ... | More chains | Based on runtime query results |

When encountering uncommon chains, MCP mode calls `chain.config` for queries, OpenAPI mode calls `trade.swap.chain` for queries.

---

## Cross-Skill Collaboration

| Source | Scenario | Routing |
|--------|----------|---------|
| `gate-dex-wallet` | User wants to exchange tokens after viewing balance | Carry context into this Skill, select mode according to routing process |
| `gate-dex-market` | User wants to buy a token after viewing market data | Carry token information into this Skill, select mode according to routing process |
| `gate-dex-wallet` (`references/transfer.md`) | Want to exchange remaining tokens after transfer | Carry chain and token context into this Skill |

---

## Security Rules

1. **Mode selection transparency**: Clearly inform users of the current calling mode and reasons
2. **Authentication isolation**: MCP mode uses `mcp_token`, OpenAPI mode uses AK/SK, no mixing
3. **Three-step confirmation gateway**: Both modes include trading pair confirmation → quote display → signature authorization confirmation, cannot be skipped
4. **Balance pre-check**: Mandatory verification of asset sufficiency before trading
5. **Risk warnings**: Forced warning for exchange value difference > 5%, high slippage (> 5%) MEV attack risk warnings
6. **No security downgrade on fallback**: When falling back from MCP to OpenAPI, security rules and confirmation processes remain consistent
7. **No repeated guidance**: MCP installation guide displayed at most once per session