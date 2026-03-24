# Gate Exchange Account and Asset Manager

## Overview

An L2 composite skill that orchestrates 58 deduplicated MCP tool calls (54 read + 4 write) across 7 L1 skills to provide a unified entry point for account and asset management, margin and liquidation risk assessment, earn yield snapshots, affiliate commission queries, and unified-account write operations.

The skill uses a 5-dimension signal overlay routing system (S1 Assets, S2 Risk, S3 Earn, S4 Affiliate, S5 Write Operations) that detects multiple intents from a single user query and assembles the minimal tool set needed, with full deduplication and parallel execution.

### Core Capabilities

| Capability | Signal | Description |
|------------|--------|-------------|
| Multi-account asset panorama | S1 | Query balances across spot, unified, futures, margin, options, Alpha, TradFi, SimpleEarn, and staking accounts |
| Margin and liquidation risk assessment | S2 | Evaluate margin ratios, liquidation prices, unrealised PnL, and funding rates for futures positions |
| Earn yield snapshots | S3 | View current SimpleEarn and staking positions with accrued interest and rewards |
| Affiliate and rebate queries | S4 | Check rebate status, partner commissions, client relationships, and transaction history. If `cex_rebate_user_info` is empty, use `cex_rebate_partner_commissions_history` (full pagination required for exact lifetime USDT/POINT sums; see SKILL.md Domain Knowledge) |
| Unified account write operations | S5 | Execute borrowing, set collateral currencies, configure per-currency leverage, and switch account modes with mandatory confirmation |

### Key Design Principles

- **Signal overlay, not single-intent classification**: Multiple dimensions can activate simultaneously from one query
- **Read-first, write-gated**: All write operations require explicit Action Draft and user confirmation
- **Tool deduplication**: Same tool + same parameters execute once across overlapping dimensions
- **Graceful degradation**: Individual tool failures do not block other dimensions from returning results

## Execution Guardrail (Mandatory)

**Strong confirmation · Action Draft** — Before any write operation (`cex_unified_create_unified_loan`, `cex_unified_set_unified_mode`, `cex_unified_set_user_leverage_currency_setting`, `cex_unified_set_unified_collateral`), the assistant must:

1. Generate an **Action Draft** with operation type, target, parameters, estimated impact, and risk note
2. Apply **write grading**: medium-risk (mode / leverage / collateral) = single confirmation + risk disclosure (**mode switch: state that the change is irreversible**); high-risk (borrow/repay) = draft must list **amount, currency, and interest rate** before confirmation
3. Wait for explicit user confirmation
4. Execute only after confirmation; treat confirmation as single-use
5. Re-confirm if any parameter changes

Without explicit confirmation, stay in read-only mode.

## Architecture

```
gate-exchange-assets-manager/
├── SKILL.md              # L2 routing skill with 5-dimension signal system
├── README.md             # This file
├── CHANGELOG.md          # Version history
└── references/
    └── scenarios.md      # 16 behaviour-oriented scenario templates
```

### L1 Skill Dependencies

| L1 Skill | Tool Count | Role |
|----------|------------|------|
| gate-exchange-assets | 11 | Multi-account balance queries |
| gate-exchange-unified | 14 | Unified account operations (read + write) |
| gate-exchange-simpleearn | 5 | SimpleEarn position and interest queries |
| gate-exchange-staking | 4 | Staking position and reward queries |
| gate-exchange-marketanalysis | 12 | Market data for risk assessment context |
| gate-exchange-affiliate | 7 | Rebate and commission queries |
| gate-exchange-alpha | 4 | Alpha account queries |

## Usage Examples

```
"Check all my account balances."
"Will I get liquidated? Check my margin."
"How much have I earned from SimpleEarn and staking?"
"What is my affiliate commission status?"
"How much USDT can I borrow? Don't borrow yet, just check."
"Borrow 500 USDT from unified account."
"Add margin to my futures position."
"Show my total assets and futures risk together."
```

## Trigger Phrases

- total assets / account balance / asset overview / how much do I have
- margin check / liquidation risk / will I get liquidated / position risk
- earn interest / staking rewards / SimpleEarn yield / earn snapshot
- affiliate / rebate / commission / partner status
- borrow USDT / add margin / set collateral / switch mode / set leverage

## Prerequisites

- Requires Gate MCP server configured and connected with valid authentication (OAuth2 or API Key).
- All 58 MCP tools require API Key authentication; the skill processes only the authenticated user's own data.

## Support

- GitHub Issues: https://github.com/gate/gate-skills/issues
- Gate Help Center: https://www.gate.com/help
