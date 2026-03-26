# gate-info-addresstracker

## Overview

An AI Agent skill that performs **on-chain address tracking**. **Phase 1**: always `info_onchain_get_address_info` (address, chain, **scope=with_defi** when supported). **Branch**: Basic (address info only) vs Deep (address + transactions + fund flow in parallel). **Auto-upgrade** to Deep when address has labels, high balance, or risk flags. **Address format detection**: 0x→ETH (or BSC/Arb etc.), bc1/1/3→BTC, T→Tron; prompt for chain if ambiguous. **Adaptive threshold**: min_value_usd for transactions and fund flow by balance tier (see SKILL.md). Tools: info_onchain_get_address_info, info_onchain_get_address_transactions, info_onchain_trace_fund_flow. Read-only.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Address info** | Labels, risk level, token balances, DeFi positions (scope=with_defi) | "Who is this address" / "Track this address 0x…" |
| **Fund tracking** | Transactions and fund flow; adaptive min_value_usd by balance tier | "Track this address and show recent fund flow" |
| **Basic vs Deep** | Basic = 4-section address profile; Deep = + large tx history + fund flow + risk warnings; "No data" / "Fund tracing under development" when info_onchain_trace_fund_flow unavailable | Per SKILL.md Report Template |

### Routing

| User intent | Action |
|-------------|--------|
| Address info / fund tracking | Execute this skill (Basic or Deep) |
| Token on-chain analysis | Route to `gate-info-tokenonchain` |
| Address risk check | Route to `gate-info-riskcheck` |
| Single transaction query | Call `info_onchain_get_transaction` directly |
| Entity/institution tracking | Route to `gate-info-whaletracker` |

### Architecture

- **Input**: User message with address (and optionally chain). Infer chain from prefix (0x, bc1, T) or ask.
- **Tools**: Always `info_onchain_get_address_info`(address, chain, scope=with_defi). If Deep: parallel `info_onchain_get_address_transactions` and `info_onchain_trace_fund_flow` with **adaptive min_value_usd** (balance tier → see SKILL.md table).
- **Output**: Basic report (address profile, holdings, DeFi, PnL) or Deep (+ tx history, fund flow, risk warnings). **Decision Logic** (risk_score, concentration, mixer, OFAC), **Error Handling**, **Safety** (privacy, labels, data source) — see SKILL.md.

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
