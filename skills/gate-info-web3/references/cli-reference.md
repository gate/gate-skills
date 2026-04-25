# gate-info-web3 — CLI Command Reference

> Commands this skill may invoke — verify flags with `gate-cli info <group> <cmd> --help` / `gate-cli news feed <cmd> --help` on **gate-cli v0.5.2**. Always pass `--format json` for data collection.

## Info · onchain

| Command | Role in this skill |
|---------|---------------------|
| `gate-cli info onchain get-address-info` | Wallet/contract labels, balances, tags — `address_tracking` |
| `gate-cli info onchain get-address-transactions` | Large / recent transfers — `address_tracking` |
| `gate-cli info onchain get-token-onchain` | Holders, concentration, smart-money hints — `token_onchain`, `token_onchain_social` |
| `gate-cli info onchain get-transaction` | Optional: user pastes a **tx hash** (not in default playbooks — see troubleshooting) |

**Not in v0.5.2 inventory (do not call)**: `trace-fund-flow`, `get-entity-profile` — see playbook `cli_future_shortcut`.

## Info · platformmetrics

| Command | Role |
|---------|------|
| `gate-cli info platformmetrics get-defi-overview` | Protocol snapshot — `protocol_platform` |
| `gate-cli info platformmetrics get-platform-info` | Protocol profile — `protocol_platform` |
| `gate-cli info platformmetrics get-platform-history` | TVL/volume/fee time series — `protocol_platform` |
| `gate-cli info platformmetrics get-yield-pools` | Lending/LP APY — `protocol_platform` |
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

## Aggregates (do not use as hard dependency)

Documented only under `cli_future_shortcut` in [playbooks/gate-info-web3.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-info-web3.yaml): `info +address-tracker`, `info +token-onchain`, `news +brief`, `news +community-scan`.
