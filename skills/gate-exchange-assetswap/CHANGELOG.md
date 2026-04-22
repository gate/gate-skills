# Changelog

## [2026.4.9-1] - 2026-04-09

### Fixed

- SKILL.md: **gate-skill-cr** compliance — removed undocumented `intent_routing` call from Workflow Step 1; intent classification uses user message only with no `cex_*` calls in that step (aligns with `gate-cli` allowlist in General Rules)
- SKILL.md: **Data privacy and collection** — new section declaring AI interaction data, gate-cli-only data flow to Gate Exchange APIs, and parameter minimization (Privacy Policy §4.2.7 alignment)
- SKILL.md: **Risk disclaimers** — mandatory trading risk sentence in Safety Rules and Report Template; links to Risk Disclosure and User Agreement

## [2026.4.8-6] - 2026-04-08

### Changed

- SKILL.md: documented mandatory **preview → create** construction — `cex_assetswap_create_asset_swap_order_v1` (no `gate-cli` mapping; see `gate-cli/cmd/cex/MCP_LEGACY_TOOL_RESOLUTION.md` §二) **`from` / `to`** must use **`asset` + `amount`** from `data.order` (use `amount`, preserve `to` order); ratio-only create after ratio-based preview called out as a common quote-failure pattern
- SKILL.md: Workflow Steps 5–6, Error Handling, Safety Rules, and Report Template updated for the above

## [2026.4.8-5] - 2026-04-08

### Changed

- README and `references/scenarios.md`: terminology aligned with **asset allocation optimization** (removed redundant marketing-style asset-swap / flash-swap phrasing)
- SKILL.md **Workflow**: each step uses explicit `Call \`…\` with:` lines for `gate-cli` commands (Step 1 uses logical routing only, documented inline)

## [2026.4.8-4] - 2026-04-08

### Fixed

- SKILL.md: canonical **General Rules** block (STOP line, tool guard, markdown runtime-rules link, explicit `gate-cli` allowlist) per gate-skill-cr Step 9
- SKILL.md: `description` ≤500 characters; required phrases **Use this skill whenever** and **Trigger phrases include** per skill-validator §4.1

## [2026.4.8-3] - 2026-04-08

### Changed

- SKILL.md: English-only description; terminology aligned with asset allocation optimization

## [2026.4.8-2] - 2026-04-08

### Changed

- SKILL.md: removed flash-swap wording; rate-limit wording uses Exchange API limits

## [2026.4.8-1] - 2026-04-08

### Added

- Initial Gate Exchange Asset Allocation Optimization skill
- `gate-cli` command mapping for list assets, config, evaluate, preview, create, list orders, get order
- Mandatory Case 1 to 4 ordering for placement; supplemental Case 5 and 6 for queries
- Domain knowledge: strategy types, listing rules, boundaries vs transfer, earn, spot grid, and other non-allocation products
- English scenarios for discovery, preview, place order, and order queries
