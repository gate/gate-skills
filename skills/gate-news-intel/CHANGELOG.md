# Changelog — gate-news-intel

## 2026.6.22-1

- `market_move_explain` (Step 2): spell out full CLI paths, esp. `gate-cli news events explain-market-move` (under `news events`, NOT `news feed`), to prevent the agent from mis-querying under `news feed`. Doc-only; playbook unchanged.

## 2026.6.12-5

- News shortcut blocks: `arg_enums.time-range: [1h, 24h, 7d]` (+brief, +event-explain, +community-scan, intel_plus_market).
- `slot_registry.time_range` documents shortcut clamp vs legacy 30d.

## 2026.6.12-4

- `intel_plus_market`: merge duplicate YAML `notes` keys (PyYAML kept only the last block; execution-order note was lost).

## 2026.6.12-3

- `event_explain`: `args_when` uses `when: event_id_present`.
- `intel_plus_market`: explicit `shortcut_block_order` and notes (news then info).

## 2026.6.12-2

- `event_explain`: `args_when` with `--event-id`; fix replaces list; keep `social_sentiment` outside shortcut replace set.
- `market_wide_intel`: explicit `+market-overview` shortcut block.
- Corrected JSON field mapping in `_shared/cli-version-routing.md`.

## 2026.6.12-1

- Added playbook shortcuts: `news +brief`, `+event-explain`, `+community-scan`; `intel_plus_market` uses `+brief` + `+coin-overview`.
- Step 0.5 reads `cli_version` from preflight JSON; `shortcuts_enabled` when >= 0.7.6.

## 2026.5.13-1

- Added `market_move_explain` playbook: leverages `gate-cli news events explain-market-move` (Tavily real-time search + internal event pool) for price-move attribution queries. Companion commands: `get-market-snapshot`, `get-orderbook`, `get-technical-analysis`, `get-coin-info`, and community (`search-x` + `get-social-sentiment`) for non-BTC.
- Added `query` slot to `slot_registry` (required for `market_move_explain`).
- Added `arg_enums` for `time-range` on `explain-market-move` (`30m / 1h / 2h / 4h / 24h`, default `2h`) per CLAUDE.md rule 9.
- Added `coin_fallback_rules` block in the playbook and SKILL.md Step 1: broad-market defaults to BTC with notice; vague references trigger a user prompt; traditional finance names pass through.
- Added dedicated 6-section Market move analysis report template in SKILL.md Step 3.
- Narrowed `event_explain` intent_keywords: "why did"/"crash"/"sharp drop" moved to `market_move_explain`; `event_explain` now covers pure event timeline/detail only.
- Added `market_move_report_sections` in playbook YAML for the 6-section template.
- Updated references: scenarios.md (Scenario 7), cli-reference.md (explain-market-move), troubleshooting.md (time_range mismatch, is_partial, companion failure, coin fallback).
- Playbook and SKILL.md versions bumped to 2026.5.13-1.

## 2026.4.20-2

- SKILL.md: added a News-intel-specific follow-up routing table in `## Cross-skill routing + Safety rules` so the three delegate targets (`gate-info-research`, `gate-info-web3`, `gate-info-risk`) are surfaced next to the report-completion stage, mirroring the other three primary skills. Fixes the asymmetry that caused `scripts/test-cross-skill-routing.py` to flag three WARNs (CSR section had no target skill references).
- No playbook execution-path changes; version bumped only to keep SKILL.md ↔ playbook `version` / `updated` consistent per CLAUDE.md rule 2.

## 2026.4.20-1

- Initial primary skill: brief, event explain, exchange listings, community intel (UGC + X + sentiment), intel + market/coin context, market-wide web + overview.
- Documented `cli_future_shortcut` for unshipped `news +*` and `info +*` aggregates.
