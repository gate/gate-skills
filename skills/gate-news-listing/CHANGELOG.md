# Changelog — gate-news-listing

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.3.12-1] - 2026-03-12

### Added

- Skill: Exchange listing tracker. Trigger: any new coins listed recently, what did Binance list, new listings, delisting/maintenance. Tools: news_feed_get_exchange_announcements, info_coin_get_coin_info, info_marketsnapshot_get_market_snapshot. Two-step workflow: announcements then supplement top coins.
- SKILL.md: Workflow (announcements → supplement in parallel), Report Template (4 sections + risk warnings), Decision Logic, Error Handling, Available Tools & Degradation Notes, Safety. Synced from docs/pd-vs-skills/skills/gate-news-listing; tool names in underscore form.
- README.md, references/scenarios.md.

### Audit

- Read-only. No listing predictions; new-coin volatility risk reminder; delisting urgency reminder.
