# Gate GitHub Skills

Gate GitHub Skills is an open skills marketplace that empowers AI agents with native access to Gate.io's cryptocurrency ecosystem. From market analysis and derivatives monitoring to one-click MCP setup — all through natural language.

Built by Gate.io. Built for the crypto community.

These skills are designed to work with any AI agent framework. Whether you're using OpenClaw, LangChain, CrewAI, or your own stack, your agents can plug into Gate.io's crypto intelligence with minimal configuration.

---

## Skills Overview

| Skill | Description | Version | Status |
|-------|-------------|---------|--------|
| [gate-exchange-market](#-gate-exchange-market) | Single-coin deep analysis & multi-coin screening | `2026.3.5-1` | ✅ Active |
| [gate-trading](#-gate-trading) | Derivatives monitoring: basis, funding rate, liquidation | `2026.3.5-1` | ✅ Active |
| [gate-mcp-installer](#-gate-mcp-installer) | One-click Gate MCP setup & configuration | `2026.3.4-1` | ✅ Active |

---

## 📊 gate-exchange-market

> **Path**: `skills/gate-exchange-market/`

Analyze cryptocurrency market data on Gate.io, covering two core modes:

| Sub-Module | What It Does |
|------------|-------------|
| **Coin Deep Analysis** | Comprehensive single-coin report covering trend, liquidity, sentiment, and risk assessment |
| **Multi-Coin Screener** | Filter and rank coins across the entire market by volume, price change, funding rate, spread, and more |

**Example Prompts**:
- `Analyze BTC in detail` / `Analyze SOL`
- `Find coins with 24h gain above 10%` / `Top coins by volume`
- `Compare ETH and SOL`

---

## 📈 gate-trading

> **Path**: `skills/gate-trading/`

Monitor trading opportunities and risks in Gate.io derivatives markets across three dimensions:

| Sub-Module | What It Does |
|------------|-------------|
| **Basis Monitor** | Spot-futures basis analysis, premium tracking, and arbitrage signals |
| **Funding Rate Arbitrage** | Full-market funding rate scan with annualized return estimates and risk annotations |
| **Liquidation Monitor** | Liquidation spike detection, directional squeeze, and pin-bar event analysis |

**Example Prompts**:
- `How is BTC basis?` / `Check BTC basis`
- `Run a funding rate arbitrage scan` / `Funding rate arbitrage opportunities`
- `Monitor liquidations` / `Show liquidation anomalies`

---

## 🔧 gate-mcp-installer

> **Path**: `skills/gate-mcp-installer/`

One-click installer and configurator for Gate MCP (mcporter). Automates the complete setup process:

1. Installs `mcporter` CLI globally via npm
2. Configures Gate MCP server with proper endpoint
3. Verifies connectivity by listing available tools
4. Provides usage examples for common queries

**Quick Start**:
```bash
bash ~/.openclaw/skills/gate-mcp-installer/scripts/install-gate-mcp.sh
```

---

## Getting Started

### Prerequisites

- An AI agent environment that supports skill loading (e.g., OpenClaw)
- Node.js & npm (for Gate MCP installation)

### Setup

1. **Install Gate MCP** — Use the `gate-mcp-installer` skill or run the install script manually:
   ```bash
   npm i -g mcporter
   mcporter config add gate https://api.gatemcp.ai/mcp --scope home
   ```

2. **Verify connectivity**:
   ```bash
   mcporter list gate --schema
   ```

3. **Start using skills** — Ask your AI agent any market or trading question in natural language.

---

## Repository Structure

```
gate-github-skills/
├── README.md
└── skills/
    ├── gate-exchange-market/    # Market intelligence skill
    │   ├── SKILL.md             # Skill definition & routing rules
    │   ├── CHANGELOG.md
    │   ├── README.md
    │   └── references/
    │       ├── coin-deep-analysis.md
    │       ├── multi-coin-screener.md
    │       └── scenarios.md
    ├── gate-trading/            # Trading intelligence skill
    │   ├── SKILL.md
    │   ├── CHANGELOG.md
    │   ├── README.md
    │   └── references/
    │       ├── basis-monitor.md
    │       ├── funding-rate-arbitrage.md
    │       ├── liquidation-monitor.md
    │       └── scenarios.md
    └── gate-mcp-installer/      # MCP setup skill
        ├── SKILL.md
        ├── CHANGELOG.md
        ├── README.md
        ├── references/
        │   └── scenarios.md
        └── scripts/
            └── install-gate-mcp.sh
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

Gate GitHub Skills is an informational tool only. All outputs are provided on an "as is" and "as available" basis, without representation or warranty of any kind. It does not constitute investment, financial, trading, or any other form of advice, nor does it represent a recommendation to buy, sell, or hold any assets. All analysis is data-based and read-only — no trading operations are performed by these skills. Digital asset prices are subject to high market risk and price volatility. You are solely responsible for your investment decisions. Past performance is not a reliable predictor of future performance. Please consult an independent financial adviser prior to making any investment.
