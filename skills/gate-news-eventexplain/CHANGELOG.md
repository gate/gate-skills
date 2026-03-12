# Changelog — gate-news-eventexplain

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.3.12-1] - 2026-03-12

### Added

- Skill: Event attribution and explanation. Trigger: why did X pump/dump, what caused this move. Tools: news_events_get_latest_events, info_marketsnapshot_get_market_snapshot, news_events_get_event_detail, info_onchain_get_token_onchain, news_feed_search_news. Multi-step workflow with event-found vs expand-news branch.
- SKILL.md: Workflow (Phase 1 parallel, Step 4a/4b branch), Report Template (attribution + no-event template), Reasoning Logic, Error Handling, Cross-Skill, Safety. Synced from docs/pd-vs-skills/skills/gate-news-eventexplain; tool names in underscore form.
- README.md, references/scenarios.md.

### Audit

- Read-only; no trading or order execution. No definitive causal claims; no follow-on price predictions.
