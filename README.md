# Gate Skills

[English](README.md) | [中文](README_zh.md)

Gate Skills is an open skills marketplace that empowers AI agents with native access to gate.com's cryptocurrency ecosystem. From market analysis and derivatives monitoring to one-click MCP setup — all through natural language.

Built by gate.com. Built for the crypto community.

### One-Click Installation

Get started in seconds with our installer skills:

- **Cursor Users**: Use `gate-mcp-cursor-installer` — installs all Gate MCP servers + skills with a single command
- **OpenClaw Users**: Use `gate-mcp-openclaw-installer` — complete Gate MCP setup with interactive selection
- **Claude Code (Claude CLI) Users**: Use `gate-mcp-claude-installer` — one-click install all Gate MCP + Gate Skills
- **Codex Users**: Use `gate-mcp-codex-installer` — one-click install all Gate MCP + Gate Skills

Just say **"Help me install Gate MCP, https://github.com/gate/gate-skills"** to your AI assistant, or run the install script directly.

### Framework Compatibility

These skills are designed to work with any AI agent framework. Whether you're using Cursor, OpenClaw, or your own stack, your agents can plug into gate.com's crypto intelligence with minimal configuration.

---

## Skills Overview

| Skill | Description | Version | Status |
|-------|-------------|---------|--------|
| [gate-mcp-claude-installer](#-gate-mcp-claude-installer) | One-click installer for Gate MCP and Skills for Claude Code (Claude CLI) | `2026.3.11-1` | ✅ Active |
| [gate-mcp-codex-installer](#-gate-mcp-codex-installer) | One-click installer for Gate MCP and Skills for Codex | `2026.3.11-1` | ✅ Active |
| [gate-mcp-cursor-installer](#-gate-mcp-cursor-installer) | One-click installer for Gate MCP and Skills for Cursor | `2026.3.10-1` | ✅ Active |
| [gate-mcp-openclaw-installer](#-gate-mcp-openclaw-installer) | Complete Gate.com MCP server installer for OpenClaw | `2026.3.10-1` | ✅ Active |
| [gate-exchange-marketanalysis](#-gate-exchange-marketanalysis) | Market tape analysis: liquidity, momentum, liquidation, funding arbitrage, basis, manipulation risk, order book explainer, slippage simulation, breakout, and weekend vs weekday | `2026.3.7-1` | ✅ Active |
| [gate-exchange-futures](#-gate-exchange-futures) | USDT perpetual futures trading: open/close position, cancel/amend order | `2026.3.5-1` | ✅ Active |
| [gate-exchange-spot](#-gate-exchange-spot) | Gate spot trading: buy/sell, order management, account queries, and asset swaps | `2026.3.9-1` | ✅ Active |
| [gate-dex-market](#-gate-dex-market) | Gate DEX market data via OpenAPI: token info, K-line, rankings, security audit | `2026.3.12-1` | ✅ Active |
| [gate-dex-trade](#-gate-dex-trade) | Gate DEX trading: MCP + OpenAPI dual mode, smart routing for Swap execution | `2026.3.12-1` | ✅ Active |
| [gate-dex-wallet](#-gate-dex-wallet) | Gate DEX comprehensive wallet: authentication, assets, transfers, DApp interactions | `2026.3.10-1` | ✅ Active |
| [gate-dex-mcpmarket](#-gate-dex-mcpmarket) | Gate Wallet DEX market data: K-line, transaction stats, liquidity, token info, rankings, security audit, new token discovery | `2026.3.5-1` | ✅ Active |
| [gate-dex-mcpwallet](#-gate-dex-mcpwallet) | Gate Wallet portfolio assets and transaction history: balance, total assets, token holdings, transfer/swap history | `2026.3.6-1` | ✅ Active |
| [gate-dex-mcpswap](#-gate-dex-mcpswap) | Gate Wallet Swap/DEX trading: get quotes, execute Swap across EVM and Solana | `2026.3.6-1` | ✅ Active |
| [gate-dex-mcptransfer](#-gate-dex-mcptransfer) | Gate Wallet transfer execution: native and token transfers across EVM and Solana | `2026.3.5-1` | ✅ Active |
| [gate-dex-mcpdapp](#-gate-dex-mcpdapp) | Gate Wallet DApp interaction: connect wallet, sign messages, execute DApp transactions, ERC20 Approve | `2026.3.5-1` | ✅ Active |
| [gate-dex-mcpauth](#-gate-dex-mcpauth) | Gate Wallet authentication: Google OAuth login, session management | `2026.3.5-1` | ✅ Active |

---

## 📈 gate-exchange-marketanalysis

> **Path**: `skills/gate-exchange-marketanalysis/`

Read-only market tape analysis across ten scenarios: liquidity, momentum, liquidation, funding arbitrage, basis, manipulation risk, order book explainer, slippage simulation, K-line breakout/support–resistance, and weekend vs weekday volume comparison.

**Example Prompts**:
- `Check BTC liquidity and slippage`
- `What is the momentum of ETH?`
- `Simulate a $10K market buy on ETH`
- `Is there manipulation risk on DOGE?`
- `Compare BTC weekend vs weekday volume`

---

## 📊 gate-exchange-futures

> **Path**: `skills/gate-exchange-futures/`

USDT perpetual futures trading on Gate Exchange. Supports four operations: open position, close position, cancel order, and amend order — with pre-flight checks, margin/leverage handling, and confirmation before execution.

**Example Prompts**:
- `Long BTC 1 contract with 10x leverage`
- `Close all ETH positions`
- `Cancel my BTC buy order`
- `Change order price to 60000`

---

## 💱 gate-exchange-spot

> **Path**: `skills/gate-exchange-spot/`

Gate spot trading covering buy/sell (market & limit), smart condition-based orders, order management (amend/cancel), account queries, fill verification, and coin-to-coin swaps. All order placements require explicit user confirmation.

**Example Prompts**:
- `Buy 100 USDT worth of BTC`
- `Sell ETH when price hits 3500`
- `Cancel my unfilled BTC order and check balance`
- `Swap USDT to SOL`

---

## 📊 gate-dex-market

> **Path**: `skills/gate-dex-market/`

Gate DEX market data skill using OpenAPI mode with AK/SK authentication. Provides read-only queries for token info, K-line data, rankings, and security audits.

**Example Prompts**:
- `Get BTC token info`
- `Show me ETH K-line data`
- `What are the top trending tokens?`
- `Check security audit for this token`

---

## 🔄 gate-dex-trade

> **Path**: `skills/gate-dex-trade/`

Gate DEX trading comprehensive skill with MCP + OpenAPI dual mode support. Smart routing automatically selects the optimal trading method based on environment. Supports Swap execution across EVM and Solana.

**Example Prompts**:
- `Swap 100 USDT for ETH`
- `Exchange BNB for PEPE`
- `Get a quote for swapping SOL to USDC`
- `Buy some tokens using OpenAPI mode`

---

## 💼 gate-dex-wallet

> **Path**: `skills/gate-dex-wallet/`

Gate DEX comprehensive wallet skill. Unified entry point for authentication, asset queries, transfer execution, and DApp interactions. Routes to specific sub-modules based on user intent.

**Example Prompts**:
- `Log in to my wallet`
- `Check my wallet balance`
- `Transfer 0.1 ETH to 0x...`
- `Connect my wallet to Uniswap`
- `Sign this message`

---

## 🌐 gate-dex-mcpmarket

> **Path**: `skills/gate-dex-mcpmarket/`

Gate Wallet DEX market data — all read-only, no authentication required. Covers K-line, transaction stats, liquidity pools, token details, rankings, new token discovery, and contract security audit.

**Example Prompts**:
- `Show me the ETH K-line on the last 24h`
- `What tokens are trending on BSC?`
- `Check the security of contract 0x...`
- `List newly launched tokens on ETH`

---

## 💼 gate-dex-mcpwallet

> **Path**: `skills/gate-dex-mcpwallet/`

Gate Wallet portfolio assets and transaction history. Query balance, total assets, token holdings, wallet address, transfer history, transaction details, and Swap history. Supports EVM multi-chain and Solana.

**Example Prompts**:
- `How much ETH do I have?`
- `Check my wallet balance and total assets`
- `Show my transfer records`
- `What is my Solana wallet address?`

---

## 🔄 gate-dex-mcpswap

> **Path**: `skills/gate-dex-mcpswap/`

Gate Wallet Swap/DEX trading. Get quotes, execute Swap across EVM and Solana, and track Swap status. Includes mandatory three-step confirmation gate.

**Example Prompts**:
- `Swap 100 USDT for ETH`
- `Exchange 1 SOL for USDC`
- `Buy some PEPE with BNB`
- `Cross-chain swap ETH to Solana SOL`

---

## 💸 gate-dex-mcptransfer

> **Path**: `skills/gate-dex-mcptransfer/`

Gate Wallet transfer execution. Build transactions, sign, and broadcast. Supports EVM multi-chain and Solana native/token transfers with mandatory balance verification and confirmation gate.

**Example Prompts**:
- `Send 0.1 ETH to 0x...`
- `Transfer 100 USDT on Polygon to 0x...`
- `Send 5 SOL to my other wallet`
- `Batch transfer USDC to these addresses`

---

## 🔌 gate-dex-mcpdapp

> **Path**: `skills/gate-dex-mcpdapp/`

Gate Wallet interaction with external DApps. Connect wallet, sign messages (EIP-712/personal_sign), execute DApp transactions, and authorize ERC20 Approve. Includes security review.

**Example Prompts**:
- `Connect my wallet to Uniswap`
- `Sign this EIP-712 message`
- `Approve 1000 USDC for Aave`
- `Add ETH-USDC liquidity on Uniswap`

---

## 🔐 gate-dex-mcpauth

> **Path**: `skills/gate-dex-mcpauth/`

Gate Wallet authentication. Manage Google OAuth login, token refresh, and logout. Verifies MCP Server connection before operations.

**Example Prompts**:
- `Log in to my wallet`
- `Sign in`
- `Log out of my account`
- `Refresh my session`

---

## 🛠️ gate-mcp-cursor-installer

> **Path**: `skills/gate-mcp-cursor-installer/`

One-click installer for Gate MCP servers and Skills specifically tailored for Cursor.

**Quick Start**:
```bash
bash scripts/install.sh
```

---

## 🛠️ gate-mcp-openclaw-installer

> **Path**: `skills/gate-mcp-openclaw-installer/`

Complete Gate.com MCP server installer for OpenClaw. Supports spot/futures trading, wallet, market info, and news servers.

**Quick Start**:
```bash
./scripts/install.sh
```

---

## 🛠️ gate-mcp-claude-installer

> **Path**: `skills/gate-mcp-claude-installer/`

One-click installer for **Claude Code (Claude CLI)**: all Gate MCP servers + all Gate Skills.

**Quick Start**:
```bash
# From repo root
bash skills/gate-mcp-claude-installer/scripts/install.sh
```

Optional: `--no-skills` to install MCP only; `--mcp main --mcp dex` etc. to install selected MCPs.

---

## 🛠️ gate-mcp-codex-installer

> **Path**: `skills/gate-mcp-codex-installer/`

One-click installer for **Codex**: all Gate MCP servers + all Gate Skills.

**Quick Start**:
```bash
# From repo root
bash skills/gate-mcp-codex-installer/scripts/install.sh
```

Optional: `--no-skills` to install MCP only; `--mcp main --mcp dex` etc. to install selected MCPs.

---

## Getting Started

### Prerequisites

- An AI agent environment that supports skill loading (e.g., Cursor, OpenClaw)
- Node.js & npm

### Setup

Choose the installer skill based on your environment:

#### For Cursor Users

Use the `gate-mcp-cursor-installer` skill to install Gate MCP and Skills with one click:

```bash
# Run the install script
bash skills/gate-mcp-cursor-installer/scripts/install.sh
```

Or simply ask the AI assistant:
```
Help me install Gate MCP
```

#### For OpenClaw Users

Use the `gate-mcp-openclaw-installer` skill:

```bash
# Install all Gate MCP servers (default)
./skills/gate-mcp-openclaw-installer/scripts/install.sh

# Selective installation
./skills/gate-mcp-openclaw-installer/scripts/install.sh --select
```

#### For Claude Code (Claude CLI) Users

Use `gate-mcp-claude-installer` to install all Gate MCP and Gate Skills:

```bash
# From repo root
bash skills/gate-mcp-claude-installer/scripts/install.sh
```

MCP only: `bash skills/gate-mcp-claude-installer/scripts/install.sh --no-skills`

#### For Codex Users

Use `gate-mcp-codex-installer` to install all Gate MCP and Gate Skills:

```bash
# From repo root
bash skills/gate-mcp-codex-installer/scripts/install.sh
```

MCP only: `bash skills/gate-mcp-codex-installer/scripts/install.sh --no-skills`

### Start Using Skills

After installation, ask your AI agent any market or trading question in natural language.

---

## Skills Installation Guide

### General Skills Installation (Recommended)

1. Check whether `npx` is already installed (if not, see the appendix):

   ```bash
   npx -v
   ```

   If a version number is returned (for example, `11.8.0`), `npx` is installed.

![Check npx version](image/general-install-1.png)

2. Install skills with interactive selection:

   ```bash
   npx skills add https://github.com/gate/gate-skills
   ```
   
![Select and install skills](image/general-install-2.png)

3. Install a specific skill (example: `gate-market`):

   ```bash
   npx skills add https://github.com/gate/gate-skills --skill gate-market
   ```
   
![Install a specific skill](image/general-install-3.png)

### Install Skills in Claude CLI

#### Option 1: Natural Language Installation (Recommended)

```text
help me to install skills, github url is: https://github.com/gate/gate-skills
```

![Claude natural language installation](image/claude-install-1.png)

Installation complete.

![Claude installation complete](image/claude-install-2.png)

#### Option 2: Manual Installation

Step 1: Download the skills package (GitHub: <https://github.com/gate/gate-skills>)

Step 2: Unzip the package and copy it to `~/.claude/skills/`.

- Show hidden folders: open your user home folder, then press `Command + Shift + .` (press again to hide)
- Copy folders to target path: copy the `skills` subfolders from `gate-skills-master` into `~/.claude/skills/`
- Verify installation: run `/skills` in Claude CLI, or ask `how many skills have I installed?`

### Install Skills in Codex CLI

#### Option 1: Natural Language Installation (Recommended)

```text
help me to install skills, github url is: https://github.com/gate/gate-skills
```

![Codex natural language installation step](image/codex-nl-install-1.png)

Changes take effect after restarting Codex.

![Codex natural language installation complete](image/codex-nl-install-2.png)

#### Option 2: Terminal Installation

1. In terminal, type `/skills`, choose `1. List skills`, select `Skill Installer`, and enter `https://github.com/gate/gate-skills`

   ![Codex terminal install - open skills menu](image/codex-terminal-install-1.png)
   ![Codex terminal install - select Skill Installer](image/codex-terminal-install-2.png)
   ![Codex terminal install - input repository URL](image/codex-terminal-install-3.png)
   ![Codex terminal install - installation process](image/codex-terminal-install-4.png)

2. Verify installation: restart the terminal and run `/skills` -> `List Skills`

   ![Codex terminal install - verify installed skills](image/codex-terminal-install-5.png)

#### Option 3: Manual Installation

Step 1: Download the skills package (GitHub: <https://github.com/gate/gate-skills>)

![Codex manual install - download repository](image/codex-manual-install-1.png)

Step 2: Unzip the package and copy it to `~/.codex/skills/`.

1. Show hidden folders: open your user home folder, then press `Command + Shift + .` (press again to hide)

   ![Codex manual install - show hidden folders](image/codex-manual-install-2.png)

2. Copy folders to target path: copy all `skills` subfolders from `gate-skills-master` into `~/.codex/skills/`

   ![Codex manual install - copy skills subfolders](image/codex-manual-install-3.png)

3. Verify installation: restart the terminal and run `/skills` -> `List Skills`

   ![Codex manual install - verify installation](image/codex-manual-install-4.png)

### Install Skills in OpenClaw

#### Option 1: Install via Chat (Recommended)

In the OpenClaw chat interface (such as Telegram or Feishu), send the GitHub URL directly to the assistant, for example:

```text
Help me install this skill: https://github.com/gate/gate-skills
```

The assistant will automatically pull the repository, configure the environment, and try to load the skill.

#### Option 2: Auto-install with ClawHub (Recommended)

- Official marketplace (requires `npx`; see appendix for installation):

  ```bash
  npx clawhub@latest install gate-skills
  ```

- GitHub repository:

  ```bash
  npx clawhub@latest add https://github.com/gate/gate-skills
  ```

#### Option 3: Manual Installation

Step 1: Download the skills package (GitHub: <https://github.com/gate/gate-skills>)

![OpenClaw manual install - download repository](image/openclaw-manual-install-1.png)

Step 2: Unzip the package and copy it to `~/.openclaw/skills/`.

1. Show hidden folders: open your user home folder, then press `Command + Shift + .` (press again to hide)
2. Copy folders to target path: copy all `skills` subfolders from `gate-skills-master` into `~/.openclaw/skills/`

Step 3: Restart OpenClaw Gateway.

### Appendix: Install npx on macOS

1. Check whether `npx` is already installed:

   ```bash
   npx -v
   ```

   If a version number is returned (for example, `11.8.0`), `npx` is installed.

2. If `npx` is not installed, use one of the following methods:

   - Option 1: Install via Homebrew

     ```bash
     # Install Homebrew (official)
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

     # Install Homebrew (China mirror)
     /bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"

     # Verify Homebrew
     brew --version

     # Install Node.js (includes npx)
     brew install node

     # Verify npx
     npx -v
     ```

   - Option 2: Install Node.js from the official website (download page):
     <https://nodejs.org/en/download>

---

## Repository Structure

```
gate-github-skills/
├── README.md
├── README_zh.md
├── image/                              # Installation screenshots
└── skills/
    ├── gate-dex-market/                # DEX market data skill (OpenAPI mode)
    ├── gate-dex-trade/                 # DEX trading skill (MCP + OpenAPI dual mode)
    ├── gate-dex-wallet/                # DEX comprehensive wallet skill
    ├── gate-dex-mcpauth/               # Wallet Auth skill
    ├── gate-dex-mcpdapp/               # Wallet DApp interaction skill
    ├── gate-dex-mcpmarket/             # Wallet DEX market data skill
    ├── gate-dex-mcpswap/               # Wallet Swap/DEX trading skill
    ├── gate-dex-mcptransfer/           # Wallet Transfer execution skill
    ├── gate-dex-mcpwallet/             # Wallet Portfolio and History skill
    ├── gate-exchange-futures/          # Futures trading skill
    ├── gate-exchange-marketanalysis/   # Market tape analysis skill
    ├── gate-exchange-spot/             # Spot trading skill
    ├── gate-mcp-cursor-installer/      # Cursor MCP installer skill
    ├── gate-mcp-openclaw-installer/    # OpenClaw MCP installer skill
    ├── gate-mcp-claude-installer/      # Claude Code (Claude CLI) MCP + Skills installer
    └── gate-mcp-codex-installer/       # Codex MCP + Skills installer
```

---

## About This Repository

Each skill lives in its own folder under `skills/` and contains:

- **`SKILL.md`** — Skill definition with YAML frontmatter (name, version, description, trigger phrases) and structured instructions including routing rules and workflows.
- **`references/`** — Detailed sub-module documentation with step-by-step workflows and report templates.
- **`CHANGELOG.md`** — Version history and change log.

---

## Contribution

We welcome contributions! To add a new skill:

1. **Fork the repository** and create a new branch:
   ```bash
   git checkout -b feature/<skill-name>
   ```

2. **Create a new folder** under `skills/` containing at least a `SKILL.md` file.

3. **Follow the required format**:
   ```markdown
   ---
   name: <skill-name>
   version: "<version>"
   updated: "<YYYY-MM-DD>"
   description: A clear description of what the skill does and when to trigger it.
   ---

   # <Skill Title>

   [Add instructions, routing rules, workflows, and report templates here]
   ```

4. **Add reference documents** in a `references/` subfolder for complex sub-modules.

5. **Open a Pull Request** to `main` for review.

---

## Disclaimer

Gate Skills is an informational tool only. All outputs are provided on an "as is" and "as available" basis, without representation or warranty of any kind. It does not constitute investment, financial, trading, or any other form of advice, nor does it represent a recommendation to buy, sell, or hold any assets. All analysis is data-based and read-only — no trading operations are performed by these skills. Digital asset prices are subject to high market risk and price volatility. You are solely responsible for your investment decisions. Past performance is not a reliable predictor of future performance. Please consult an independent financial adviser prior to making any investment.
