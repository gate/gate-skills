# Changelog

All notable changes to the Gate Exchange CandyDrop skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [2026.4.14-1] - 2026-04-14

### Changed
- **Airdrop records** user-facing tables: **omit** the flash-convert **USDT** column (`convert_amount`); show **Project (currency)**, **Airdrop Time (UTC)**, and **Airdrop Rewards** (`{rewards} {currency}`) only (`references/records.md`, `SKILL.md`, `references/gate-cli.md`).

## [2026.4.13-5] - 2026-04-13

### Changed
- **Skill authoring language**: Instructions standardized to **English** per Gate skill guidelines; added explicit note that **end-user replies** still follow `Language adaptation` in `SKILL.md`. Chinese strings in `references/activities.md` task-type table are labeled as **zh-CN example labels** only.
- Removed Chinese instructional/examples from skill prose (`SKILL.md`, `activities.md`, `records.md`); `CHANGELOG` history bullets normalized to English.

## [2026.4.13-4] - 2026-04-13

### Changed
- **`tradfi`** display: show **`TradFi`** only (no extra parenthetical suffix).
- **Activity list** intents: **direct answer** — title + table; **no** long preamble, field lectures, or pasting the task-type mapping table (`references/activities.md` → *Activity list — answer directly*).

## [2026.4.13-3] - 2026-04-13

### Changed
- Activity list **`rule_name`**: require **contextual translation** for end users (see mapping table in `references/activities.md`); query params for `rule_name` filters stay API tokens.

## [2026.4.13-2] - 2026-04-13

### Changed
- Records tables: when the column header already includes **`(UTC)`**, **omit the trailing `(UTC)`** on each time cell (`register_time`, `airdrop_time`) — display **`YYYY-MM-DD HH:MM:SS`** only (see `SKILL.md` and `references/records.md`).

## [2026.4.13-1] - 2026-04-13

### Changed
- Airdrop records output: **`rewards` must be shown with the row token** (`{rewards} {currency}`); **`convert_amount`** shown as **`{value} USDT`** when present, otherwise **`--`** (see `references/records.md`).

## [2026.4.9-1] - 2026-04-09

### Added
- Initial release of Gate Exchange CandyDrop skill
- Browse CandyDrop activities with filtering (status, token, task type, registration status)
- View activity rules with prize pool and task details
- Register for CandyDrop activities with Preview-Confirm flow
- Query task completion progress for enrolled activities
- Query participation records (registration history) by time, token, and status
- Query airdrop records (reward distribution history) by time and token
- Compliance error handling for region restrictions
- 17 scenarios across 5 sub-modules
- Support for 6 `gate-cli` commands from gate-dev (public) and g-d-x (authenticated) services
- Timestamp strategy for records queries (Strategy 1: relative time, Strategy 2: anchor table)
- Dual-parameter resolution (currency vs activity_id)
