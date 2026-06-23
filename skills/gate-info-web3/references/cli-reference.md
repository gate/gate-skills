# gate-info-web3 — CLI Command Reference

> Legacy leaf commands on **gate-cli v0.5.2+**. Aggregates below ship in **v0.7.6+** when `shortcuts_enabled` — see [cli-version-routing.md](../../_shared/cli-version-routing.md).

## Aggregates (>= 0.7.6)

| Command | Flags | Playbook |
|---------|-------|----------|
| `gate-cli info +address-tracker` | `--address`, `--chain`, `--min-value` (USD, default 100000) | `address_tracking` — JSON: `entity_guess`, `defi_context`, `recent_activity` |
| `gate-cli info +token-onchain` | `--symbol` (ticker) or `--address` + `--chain` (contract); see playbook `args` / `args_when` | `token_onchain` |
| `gate-cli news +community-scan` | `--coin` (ticker only; resolve via `+token-onchain` → `coin_context` when `token` is contract), `--time-range` | `token_onchain_social` |

`missing_sections` may include `trace-fund-flow` or `smart_money` — note in report.

## Info · onchain

| Command | Role in this skill |
|---------|---------------------|
| `gate-cli info onchain get-address-info` | Wallet/contract labels, balances, tags — `address_tracking` |
| `gate-cli info onchain get-address-transactions` | Large / recent transfers — `address_tracking` |
| `gate-cli info onchain get-token-onchain` | Holders, concentration, smart-money hints — `token_onchain`, `token_onchain_social` |
| `gate-cli info onchain get-transaction` | Optional: user pastes a **tx hash** (not in default playbooks — see troubleshooting) |

**Not shipped**: `trace-fund-flow`, `get-entity-profile`.

## Info · platformmetrics

| Command | Key flags | Role |
|---------|-----------|------|
| `gate-cli info platformmetrics get-defi-overview` | `--category` (default `all`) | Ecosystem DeFi overview — `protocol_platform` (optional; not per-protocol) |
| `gate-cli info platformmetrics get-platform-info` | `--platform-name` (required) | Protocol profile — `protocol_platform` |
| `gate-cli info platformmetrics get-platform-history` | `--platform-name` or `--exchange-slug` | TVL/volume/fee time series — `protocol_platform` |
| `gate-cli info platformmetrics get-yield-pools` | `--project`, `--symbol`, optional `--chain` | Lending/LP APY — `protocol_platform` |
| `gate-cli info platformmetrics search-platforms` | Resolve fuzzy protocol name → slug (verify flags) |
| `gate-cli info platformmetrics get-exchange-reserves` | CEX reserves — `exchange_reserves` |
| `gate-cli info platformmetrics get-liquidation-heatmap` | Liquidation density — `liquidation_heatmap` |
| `gate-cli info platformmetrics get-stablecoin-info` | Stablecoin market — `stablecoin_bridge` |
| `gate-cli info platformmetrics get-bridge-metrics` | Bridge rankings — `stablecoin_bridge` |

## News · feed

| Command | Role |
|---------|------|
| `gate-cli news feed web-search` | Open-web bundle for **entity_intel** |
| `gate-cli news feed search-news` | Headlines — `token_onchain_social` |
| `gate-cli news feed get-social-sentiment` | Polarity / mentions — `token_onchain_social` |
| `gate-cli news feed search-ugc` | Reddit/TG/Discord/YouTube snippets — `token_onchain_social` |

Legacy playbook paths: [playbooks/gate-info-web3.yaml](../../../playbooks/gate-info-web3.yaml).
