# Changelog — gate-info-web3

## 2026.6.22-1

- `token_onchain_social.additional_shortcut` (`+community-scan`): fixed mismapped `replaces_command_ids` — removed `news_brief` (search-news), which `+community-scan` does NOT produce. `replaces_command_ids` is now `[social_sentiment, ugc_scan]`; `news_brief` moved to `post_shortcut_optional_ids` so news headlines are no longer silently dropped on the shortcut path. Updated SKILL.md Step 2 and `_shared/cli-version-routing.md`.

## 2026.6.12-6

- `token_onchain_social`: legacy `additional_commands` use `coin: {symbol}`; `symbol_present` guard; skip news when ticker unresolved.
- `+community-scan` shortcut: `arg_enums.time-range: [1h, 24h, 7d]`.

## 2026.6.12-5

- `token_onchain_social`: `+community-scan` requires `symbol_present`; no `{symbol|{token}}` fallback on `--coin`.
- `_shared`: expanded `contract_address` predicate (Solana / base58 mint).

## 2026.6.12-4

- `token_onchain` shortcut branch: `when: contract_address` per `_shared/cli-version-routing.md`.

## 2026.6.12-3

- `protocol_platform`: align platformmetrics flags (`platform-name`, `project`, `symbol`; `get-defi-overview` uses `category` only).
- Quote `"off"` in `upstream-raw-mode` arg_enums (YAML boolean trap).

## 2026.6.12-2

- `token_onchain_social`: `inherits_shortcuts_from`; `+community-scan` uses `{symbol|{token}}` with coin_context resolution notes.

## 2026.6.12-1

- Added playbook `shortcut` for `address_tracking` (`+address-tracker`) and `token_onchain` (`+token-onchain`); `additional_shortcut` for `token_onchain_social` (`+community-scan`).
- Step 0.5 / Step 2 version-gated execution per `skills/_shared/cli-version-routing.md` (>= 0.7.6).

## 2026.4.20-1

- Initial primary skill: playbooks for address tracking, token on-chain, entity intel (web-search pending `get-entity-profile`), protocol/platform metrics, exchange reserves, liquidation heatmap, stablecoin+bridge, and token+social.
- Documented `cli_future_shortcut` for unshipped aggregate shortcuts and `trace-fund-flow` / `get-entity-profile`.
- Six-section report template aligned with `需求文档.md` §5.5.
