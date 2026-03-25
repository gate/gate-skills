# Changelog

All notable changes to `gate-dex-trade` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2026.3.24-1] - 2026-03-24

### Changed

- **SKILL.md streamlined**: Removed Auto-Update section (now handled by `gate-runtime-rules.md` §1); removed Cross-Skill Collaboration (non-actionable); consolidated Security Rules (credential handling defers to runtime-rules §3); removed "No repeated guidance" rule
- **General Rules**: Added mandatory reference to `gate-runtime-rules.md` before any tool call


## [2026.3.19-1] - 2026-03-19

### Added

- **Balance field note** (`references/mcp.md`): `dex_wallet_get_token_list` — use `orignCoinNumber` for balance validation, not `coinNumber`

## [2026.3.18-1] - 2026-03-18

### Changed

- **SKILL.md Streamlined**: Removed verbose routing logic, multi-skill priority system, OpenClaw examples, Claude Code workarounds; converted to pure routing layer pointing to `references/`
- **MCP Tool Naming**: Restored `dex_` prefix for all tool references in mcp.md

### Fixed

- **Legacy Skill Identifiers**: Renamed `gate-dex-mcpswap` → `gate-dex-trade-mcp`, `gate-dex-opentrade` → `gate-dex-trade-openapi`
- **Cross-Reference Paths**: Replaced stale skill names (gate-dex-mcpauth, gate-dex-mcpwallet, etc.) with current file-based paths

## [2026.3.17-1] - 2026-03-17

### Fixed

- **Legacy Skill Identifiers**: Renamed `gate-dex-mcpauth` → `gate-dex-wallet/references/auth.md`, `gate-dex-mcpwallet` → `gate-dex-wallet`, `gate-dex-mcptransfer` → `gate-dex-wallet/references/transfer.md`, `gate-dex-mcpmarket` → `gate-dex-market`, `gate-dex-mcpswap` → `gate-dex-trade` in mcp.md
- **Metadata Name**: Changed mcp.md internal name from `gate-dex-mcpswap` to `gate-dex-trade-mcp`
- **OpenAPI Metadata**: Changed openapi.md internal name from `gate-dex-opentrade` to `gate-dex-trade-openapi`

## [2026.3.14-3] - 2026-03-14

### Changed

- **MCP Tool Cross-References**: Updated market tool references to use new `dex_` prefixed names
  - `token_get_coin_info` → `dex_token_get_coin_info`
  - `token_get_risk_info` → `dex_token_get_risk_info`

## [2026.3.14-2] - 2026-03-14

### Enhanced

- **Auto-Update System Upgrade**:
  - **Dynamic Version Reading**: Auto-update system now dynamically reads current skill version from SKILL.md metadata instead of hardcoded values
  - **Enhanced Update Logic**: Added support for same-version updates when remote updated date is newer than local
  - **Improved Accuracy**: Version comparison now considers both version number and updated date for comprehensive update detection
  - **Better Error Handling**: Fallback mechanisms ensure system stability when version reading fails

### Technical Changes
- Added `getCurrentSkillVersion()` function for dynamic version detection
- Added `isUpdatedDateNewer()` function for date-based update comparison
- Enhanced update conditions to support secondary criterion (updated date comparison)
- Improved update system robustness and reliability

## [2026.3.14-1] - 2026-03-14

### Enhanced

- **Authentication System Upgrade**:
  - Support for both Google OAuth and Gate OAuth dual authentication methods
  - Users can freely choose authentication method (Google account or Gate account)
  - Unified authentication process, both methods receive same functional permissions
- **URL Display Optimization**:
  - Direct display of complete clickable links when MCP returns authentication URLs
  - Removed extra decorators around URLs (quotes, brackets, etc.)
  - Ensured URLs are not escaped, users can directly copy and click to use
- **Configuration Template Enhancement**:
  - All platform configurations use complete MCP configuration templates (including Authorization header)
  - Unified `transport: "http"` configuration format
  - Optimized token placeholder descriptions
- **Security Rules Enhancement**:
  - Added proper authentication URL display rules
  - Clarified multi-authentication method support policy
  - Strengthened token confidentiality and desensitization display requirements

### Added

- Gate OAuth authentication support
- Complete MCP Server configuration template examples
- Authentication method selection instructions
- URL display standardization rules

## [2026.3.12-1] - 2026-03-12

### Changed

- **SKILL.md converted to pure routing layer**: Removed all embedded MCP business logic, SKILL.md only responsible for environment detection + mode dispatch
  - MCP mode → Read `references/mcp.md` complete specification for execution
  - OpenAPI mode → Read `references/openapi.md` complete specification for execution
- **Routing flow optimization**:
  - Added cross-chain judgment (OpenAPI doesn't support cross-chain, cross-chain must use MCP)
  - MCP Server auto-discovery by tool features (not dependent on fixed Server names)
  - When user explicitly specifies MCP but unavailable, no fallback, show installation guide
- **Multi-platform support**: MCP Server installation guide covers Cursor / Claude Code / Windsurf and other platforms, removed Cursor hard-coding

### Added

- `references/mcp.md` — MCP mode complete specification (originally embedded in SKILL.md, now independent sub-file)
- `references/README-mcp.md` — MCP mode usage instructions

### Fixed

- Supported chain list changed to runtime query, no longer hard-coded fixed numbers
- README-openapi.md file index pointing corrected (originally pointed to parent directory files)

---

## [2026.3.11-1] - 2026-03-11

### Added

- **Dual-mode architecture**: Integrated MCP and OpenAPI two trading methods into single Skill entry point
- **Intelligent routing system**: Automatically select optimal trading mode based on environment and user preferences
  - `references/openapi.md` — OpenAPI mode complete specification (AK/SK + complete lifecycle)
  - `references/README-openapi.md` — OpenAPI mode usage instructions
- **MCP trading tools** (5 tools): Quote, execution, status query, balance verification, address retrieval
- **OpenAPI trading tools** (9 tools): Chain query, Gas prices, quotes, building, signing, submission, status, etc.
- **Unified connection detection**: First session detection + runtime error fallback
- **Dual security mechanisms**: MCP three-step confirmation gateway + OpenAPI private key protection
- Multi-chain support: EVM (14 chains) + Solana + SUI + Tron + Ton

### Changed

- **Architecture upgrade**: Upgraded from single MCP Swap to MCP + OpenAPI dual-mode trading support
- **Routing optimization**: Main SKILL.md serves as intelligent dispatch center, supports automatic mode switching
- **User experience**: Automatically select most suitable trading method based on user needs and environment

---

## [2026.3.6-1] - 2026-03-06

### Added

- 5 MCP Swap tools: Quote, execution, status query, etc.
- 4 operation flows: Standard Swap, modify slippage, query status, cross-chain Swap
- Mandatory three-step confirmation gateway: Trading pair confirmation → Quote display → Signature authorization confirmation
- Exchange value difference calculation and tiered warnings (> 5% forced warning)