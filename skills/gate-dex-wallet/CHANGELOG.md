# Changelog

All notable changes to `gate-dex-wallet` skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2026.3.14-2] - 2026-03-14

### Added

- **Auto-Update System**: Comprehensive version management and automatic updates
  - **Dynamic Version Reading**: Auto-update system now dynamically reads current skill version from SKILL.md metadata instead of hardcoded values
  - **Enhanced Update Logic**: Added support for same-version updates when remote updated date is newer than local
  - **Improved Accuracy**: Version comparison now considers both version number and updated date for comprehensive update detection
  - **Better Error Handling**: Fallback mechanisms ensure system stability when version reading fails
  - **Session-Based Checking**: Intelligent version checks only at session start with 1-hour cooldown
  - **Fresh Install Detection**: Skip version checks for recently installed skills (< 24h) for optimal first-time experience
  - **Performance Optimized**: No version checks during normal user interactions to maintain response speed
  - **Remote Source**: Updates from official Gate Skills repository on GitHub

### Enhanced

- **Auto-Update Feature Documentation**: Added comprehensive auto-update feature description in README.md
  - Performance optimization details and smart cooldown mechanisms
  - Session caching and stable operation guarantees
  - Update timing and rules clearly explained
  - User-friendly update notifications and status messages

### Technical Changes
- Added `getCurrentSkillVersion()` function for dynamic version detection
- Added `isUpdatedDateNewer()` function for date-based update comparison  
- Enhanced update conditions to support secondary criterion (updated date comparison)
- Improved update system robustness and reliability with comprehensive error handling
- Updated file list for wallet skill updates: includes all core files and references

## [2026.3.12-1] - 2026-03-12

### Added

- **CLI Command Line Module**: `references/cli.md` — gate-wallet dual-channel CLI complete specification
  - MCP channel (OAuth managed signing) + OpenAPI hybrid mode (AK/SK + MCP signing)
  - Covers authentication, asset query, transfer, swap, market data, and approval full functionality
  - Dual-channel routing rules (explicit specification / login status determination / automatic selection)
  - Hybrid Swap (`openapi-swap`) supports EVM + Solana
  - 23 common pitfalls and best practices
- **CLI Installation Script**: `install_cli.sh` — One-click installation of gate-wallet CLI
  - Detects Node.js / npm environment
  - Global installation of `gate-wallet-cli` via npm
  - Optional OpenAPI credential configuration (`~/.gate-dex-openapi/config.json`)
  - Automatic update of CLAUDE.md / AGENTS.md routing files

### Changed

- **Routing File Template**: `install.sh` generated CLAUDE.md / AGENTS.md adds CLI routing entries
- **Cross-Skill Collaboration Table**: CLI caller name in SKILL.md corrected to `gate-dex-cli`
- **npm Package Name Unification**: All files unified to use `gate-wallet-cli`

## [2026.3.11-1] - 2026-03-11

### Added

- **One-Click Installation Script**: `install.sh` supports multi-platform automatic configuration
  - Auto-detects AI platforms (Cursor, Claude Code, Codex CLI, OpenCode, OpenClaw)
  - Creates corresponding MCP configuration and Skill routing files for each platform
  - Unified configuration of `gate-wallet` MCP Server connection
- **Unified Wallet Skill Architecture**: Integrates authentication, assets, transfer, and DApp four modules into a single Skill entry point
- **Sub-function Routing System**: Organizes complete implementation specifications for each module through `references/` directory
  - `references/auth.md` — Authentication module (Google OAuth, Token management)
  - `references/transfer.md` — Wallet comprehensive (authentication, assets, transfer, DApp) module (Gas estimation, signing, broadcasting)
  - `references/dapp.md` — DApp module (wallet connection, message signing, contract interaction)
- **Asset Query Tools** (7 tools): balance, total assets, address, chain configuration, transaction history, etc.
- **Smart Route Dispatch**: Automatically routes to corresponding sub-module implementation based on user intent
- **Unified Authentication Management**: All modules share MCP token and session state
- **MCP Server Connection Detection**: First session detection + runtime error fallback
- Supports 8 chains (ETH, BSC, Polygon, Arbitrum, Optimism, Avalanche, Base, Solana)

### Changed

- **Architecture Refactoring**: From scattered 4 independent Skills (auth/wallet/transfer/dapp) integrated into a single unified Skill
- **Directory Structure**: Adopts `gate-dex-wallet/references/` pattern, referencing [gate-skills](https://github.com/gate/gate-skills/tree/master/skills/gate-exchange-futures) project architecture
- **Routing Optimization**: Main SKILL.md serves as dispatch center, sub-module specifications maintained independently

### Deprecated

- Independent `gate-dex-wallet/references/auth`, `gate-dex-wallet/references/transfer`, `gate-dex-wallet/references/dapp` Skill directories
- Cross-Skill complex routing, simplified to single Skill internal module routing