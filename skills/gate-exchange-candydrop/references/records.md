# Gate CandyDrop Records — Participation History & Airdrop Records

Query CandyDrop participation (registration) history and airdrop reward distribution records.

**Authoring language:** Reference prose is **English**; user-visible text still follows `Language adaptation` in `SKILL.md`.

## MCP tools and parameters

| Tool | Purpose | Required | Optional |
|------|---------|----------|----------|
| **`gate-cli cex launch candy-drop participations`** | Query participation records | — | `currency`, `status`, `start_time`, `end_time`, `page`, `limit` |
| **`gate-cli cex launch candy-drop airdrops`** | Query airdrop records | — | `currency`, `start_time`, `end_time`, `page`, `limit` |

**IMPORTANT — Time parameter format:**
- Both endpoints accept `start_time` / `end_time` as **integer unix timestamps (seconds)**.
- See **Timestamp strategy** below for correct computation.

**IMPORTANT — `status` parameter (participation records only):**
- `ongoing`: Activity in progress
- `awaiting_draw`: Awaiting draw/lottery
- `won`: Won reward
- `not_win`: Did not win
- Omit `status` to query all records.

Both endpoints require authentication.

**API response — Participation Record (`CandyDropV4ParticipationRecord`):**

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Activity ID |
| currency | string | Token/project name |
| status | string | Record status: ongoing, awaiting_draw, won, not_win |
| register_time | string | Registration time (pre-formatted UTC string) |

Note: The API does **not** return detailed activity info. Use `currency` to identify which activity the record belongs to.

**API response — Airdrop Record (`CandyDropV4AirdropRecord`):**

| Field | Type | Description |
|-------|------|-------------|
| currency | string | Token/project name |
| airdrop_time | string | Airdrop distribution time (pre-formatted UTC string) |
| rewards | string | Airdrop reward amount (numeric string; **display with unit** — see below) |
| convert_amount | string | Auto flash-converted amount in **USDT** when applicable (may be empty). **Not shown** in user-facing airdrop record tables. |

Note: The API does **not** return which specific prize pool or task earned this reward. Use `currency` to identify the activity.

**Records tables — UTC in header (do not duplicate `(UTC)` in cells):**

- Participation **`register_time`** and airdrop **`airdrop_time`** often arrive as `YYYY-MM-DD HH:MM:SS(UTC)`.
- When the table column header already indicates UTC (e.g. `Registration Time (UTC)`, `Airdrop Time (UTC)`), **remove the trailing `(UTC)`** from each displayed value → show **`YYYY-MM-DD HH:MM:SS`** only.
- When **comparing or discarding** rows by time range (Strategy 1), parse using the same instant whether or not you strip `(UTC)` for display.

**Airdrop table — amounts MUST include units (non-skippable):**

- **`rewards`**: Always show the token amount together with that row’s `currency`, separated by one space: `{rewards} {currency}` (example: `6.000066 CAT`, `4.02032 ETH`). Do **not** output a bare number in the rewards column when presenting a table or list.
- **Flash-convert / USDT (`convert_amount`)**: Do **not** add a column or cell for this field in airdrop record replies, even if the API returns it.

---

# Part 1: Participation Records

## Timestamp strategy

The participation records API requires `start_time`/`end_time` as **integer unix timestamps (seconds)**, which LLMs often miscalculate. Use the following two strategies to avoid errors.

### Strategy 1 — Relative time including present → skip time params, single-page display

**When to use**: The user's time range **ends at or near now** — e.g. "recent", "latest", "last week", "last N days", "last month", "last 3 months".

**How** (strictly one page at a time — NEVER auto-fetch multiple pages):
1. Do **NOT** pass `start_time`/`end_time`. Call with `page=1` only (do not pass `limit`, let the API use its default of 10).
2. The API returns records in reverse chronological order (newest first).
3. From the returned records, discard any whose `register_time` is outside the user's intended range. **Immediately display** the remaining records to the user.
4. **Check if more pages may exist**: if the number of returned records >= 10 (API default page size) and all are within range, append a prompt: "There may be more records. Reply 'next page' to continue." Then **STOP and wait for the user's reply**. Do NOT fetch page 2 on your own.
5. If returned records < 10, or the last record is older than the range start, all data has been shown — do NOT prompt for next page.

### Strategy 2 — Historical / absolute date range → use anchor table

**When to use**: The time range **does not include the present** — e.g. "last month" (meaning the previous calendar month, not the last 30 days), "February 2026", "last year", "2025-01 to 2025-06".

**How**: Look up the anchor table below and compute `start_time`/`end_time` by simple addition. Each day = `+86400`.

```
2026 monthly anchors (1st day 00:00:00 UTC):
Jan 1 = 1767225600    Jul 1 = 1782864000
Feb 1 = 1769904000    Aug 1 = 1785542400
Mar 1 = 1772323200    Sep 1 = 1788220800
Apr 1 = 1775001600    Oct 1 = 1790812800
May 1 = 1777593600    Nov 1 = 1793491200
Jun 1 = 1780272000    Dec 1 = 1796083200

2025 reference: Jan 1 = 1735689600  (subtract 31536000 from 2026 anchors for non-leap year)
```

Example: "February 2026" → `start_time=1769904000`, `end_time=1772323200` (Mar 1, exclusive).

### Decision guide

| User expression | Ends at now? | Strategy | Pass time params? |
|-----------------|-------------|----------|-------------------|
| "recent" / "latest" / "recently" | Yes | 1 | No |
| "last week" / "last 30 days" / "past month" | Yes | 1 | No |
| "last month" (= previous calendar month) | No | 2 | Yes (anchor table) |
| "February 2026" | No | 2 | Yes (anchor table) |
| "last year" | No | 2 | Yes (anchor table) |
| "2026-02-01 to 2026-03-15" | No | 2 | Yes (anchor table) |

## Workflow

1. **Determine strategy**: Check whether the user's time range includes the present moment (→ Strategy 1) or is a historical/absolute range (→ Strategy 2). See decision guide above.
2. **Parse parameters**: Extract `currency`, `status`, `page` from user query. For Strategy 2, compute `start_time`/`end_time` using the anchor table.
3. **Call tool**: Call `gate-cli cex launch candy-drop participations` with `page=1` and optional filters. Do not pass `limit` (API defaults to 10). For Strategy 1, omit time params; for Strategy 2, include them. **Fetch only ONE page per turn.**
4. **Display current page immediately**: Show records to the user (Strategy 1: after discarding out-of-range records). If there may be more records (Strategy 1: returned count >= 10 and all within range; Strategy 2: total >= already shown count), append a pagination prompt and **STOP — wait for the user to confirm before fetching the next page**.
5. **Key data to extract**: From each record: `id`, `currency`, `status`, `register_time`.
6. **Format response**: Show as table with all fields. **Strip trailing `(UTC)` from `register_time` cells** when the column header includes `(UTC)` (see **UTC in header** above). Append pagination prompt when applicable.

## Report Template

Use the **Response Template** block from the matching scenario. Show `currency`, `status`, **`register_time`** (display form per UTC-header rule), `id`.

---

## Scenario 1: Query participation records by time range

**Context**: User wants to see their CandyDrop participation history within a specific time period.

**Prompt Examples**:
- "Show my CandyDrop participation last month"
- "My CandyDrop registration records for the last month"
- "My CandyDrop registration records this year"

**Expected Behavior**:

*If Strategy 1 (range includes present):*
1. Call `gate-cli cex launch candy-drop participations` with `page=1` — do NOT pass `start_time`/`end_time` or `limit`.
2. Discard records whose `register_time` is outside the user's intended range.
3. **Immediately display** the remaining records to the user.
4. If returned count >= 10 and all are within range, append: "There may be more records. Reply 'next page' to continue." — then **STOP and wait**.

*If Strategy 2 (historical / absolute range):*
1. Compute `start_time` and `end_time` as integers using the anchor table.
2. Call `gate-cli cex launch candy-drop participations` with `start_time={timestamp}`, `end_time={timestamp}`, `page=1` — do NOT pass `limit`.
3. **Immediately display** returned records.
4. If total >= already shown count, append: "There are more records ({total} total). Reply 'next page' to continue." — then **STOP and wait**.

**Response Template**:
```
CandyDrop Participation Records ({time_period})

| Token | Status | Registration Time (UTC) |
|-------|--------|------------------------|
| {currency} | {status} | {register_time_display} |
| ... | ... | ... |

(`{register_time_display}` = strip trailing `(UTC)` when header is `Registration Time (UTC)`.)

Total: {total} records.
```

---

## Scenario 2: Query participation records by token

**Context**: User wants to see their participation details for a specific token.

**Prompt Examples**:
- "Show my USDT CandyDrop participation records"
- "What USDT CandyDrop activities have I joined?"
- "Check my BTC CandyDrop history"

**Expected Behavior**:
1. Extract token name from user query (e.g. "USDT").
2. Call `gate-cli cex launch candy-drop participations` with `currency={token}`, `page=1`.
3. For each record display: `currency`, `status`, `register_time`.

**Response Template**:
```
CandyDrop Participation Records (Token: {currency})

| Token | Status | Registration Time (UTC) |
|-------|--------|------------------------|
| {currency} | {status} | {register_time_display} |
| ... | ... | ... |

(`{register_time_display}` as in Scenario 1.)

Total: {total} records for {currency}.
```

---

## Scenario 3: Query participation records by status

**Context**: User wants to see participation records filtered by outcome status.

**Prompt Examples**:
- "Show my CandyDrop records that have won"
- "Show my won CandyDrop records"
- "Show records awaiting draw"

**Expected Behavior**:
1. Map user intent to status: won=`won`, not_win=`not_win`, ongoing=`ongoing`, awaiting_draw=`awaiting_draw`.
2. Call `gate-cli cex launch candy-drop participations` with `status={value}`, `page=1`.
3. Display filtered records.

**Response Template**:
```
CandyDrop Participation Records (Status: {status_label})

| Token | Status | Registration Time (UTC) |
|-------|--------|------------------------|
| {currency} | {status} | {register_time_display} |
| ... | ... | ... |

(`{register_time_display}` as in Scenario 1.)

Total: {total} records with status "{status_label}".
```

---

## Scenario 4: Empty participation records

**Context**: User queries participation records but has no CandyDrop registration history.

**Prompt Examples**:
- "Show my CandyDrop history" (when user has none)

**Expected Behavior**:
1. Call `gate-cli cex launch candy-drop participations`.
2. Receive empty array.
3. Suggest browsing active activities.

**Response Template**:
```
You have no CandyDrop participation records.

To get started:
- Browse active activities with "Show CandyDrop activities"
- Register for an activity with "Register for CandyDrop {token}"
```

---

# Part 2: Airdrop Records

## Workflow

1. **Determine strategy**: Same as Part 1 — check whether time range includes present (→ Strategy 1) or is historical (→ Strategy 2).
2. **Parse parameters**: Extract `currency`, `page` from user query. For Strategy 2, compute `start_time`/`end_time` using the anchor table.
3. **Call tool**: Call `gate-cli cex launch candy-drop airdrops` with `page=1` and optional filters. Do not pass `limit` (API defaults to 10). **Fetch only ONE page per turn.**
4. **Display current page immediately**: Same pagination rules as Part 1.
5. **Key data to extract**: From each record: `currency`, `airdrop_time`, `rewards`.
6. **Format response**: Show as table with those fields only. **Apply the mandatory unit rules** above for `rewards` in every cell (not raw API strings alone for amounts). **Strip trailing `(UTC)` from `airdrop_time` cells** when the column header includes `(UTC)`.

## Report Template

Use the **Response Template** block from the matching scenario. Show `currency`, **`airdrop_time`** (display form per UTC-header rule), and **display-formatted** `{rewards} {currency}` per the unit rules.

---

## Scenario 5: Query airdrop records by time range

**Context**: User wants to see their CandyDrop airdrop rewards within a specific time period.

**Prompt Examples**:
- "Show my CandyDrop airdrop rewards this month"
- "What CandyDrop airdrops have I received recently?"
- "My CandyDrop airdrop history"

**Expected Behavior**:

*If Strategy 1 (range includes present):*
1. Call `gate-cli cex launch candy-drop airdrops` with `page=1` — do NOT pass `start_time`/`end_time` or `limit`.
2. Discard records whose `airdrop_time` is outside the user's intended range.
3. **Immediately display** the remaining records.
4. If returned count >= 10 and all within range, append: "There may be more records. Reply 'next page' to continue." — then **STOP and wait**.

*If Strategy 2 (historical / absolute range):*
1. Compute `start_time` and `end_time` as integers using the anchor table.
2. Call `gate-cli cex launch candy-drop airdrops` with `start_time={timestamp}`, `end_time={timestamp}`, `page=1` — do NOT pass `limit`.
3. **Immediately display** returned records.
4. If total >= already shown count, append: "There are more records ({total} total). Reply 'next page' to continue." — then **STOP and wait**.

**Response Template**:
```
CandyDrop Airdrop Records ({time_period})

| Project | Airdrop Time (UTC) | Airdrop Rewards |
|---------|-------------------|-----------------|
| {currency} | {airdrop_time_display} | {rewards} {currency} |
| ... | ... | ... |

(`{airdrop_time_display}` = `YYYY-MM-DD HH:MM:SS` with trailing `(UTC)` removed when header already says UTC.)

Showing {current_count} records.
{If more records may exist:} There may be more records. Reply "next page" to continue.
```

---

## Scenario 6: Query airdrop records by token

**Context**: User wants to see airdrop rewards for a specific token.

**Prompt Examples**:
- "Show my USDT CandyDrop airdrop details"
- "How much USDT CandyDrop airdrop did I receive?"
- "Check my BTC CandyDrop airdrops"

**Expected Behavior**:
1. Extract token name from user query (e.g. "USDT").
2. Call `gate-cli cex launch candy-drop airdrops` with `currency={token}`, `page=1`.
3. For each record display: `currency`, `airdrop_time`, and **`{rewards} {currency}`** (with units).

**Response Template**:
```
CandyDrop Airdrop Records (Token: {currency})

| Airdrop Time (UTC) | Airdrop Rewards |
|-------------------|-----------------|
| {airdrop_time_display} | {rewards} {currency} |
| ... | ... |

(`{airdrop_time_display}` as in Scenario 5.)

Showing {current_count} records for {currency}.
{If total >= current_count:} There are more records. Reply "next page" to continue.
```

---

## Scenario 7: Empty airdrop records

**Context**: User queries airdrop records but has no CandyDrop airdrop history.

**Prompt Examples**:
- "Show my CandyDrop airdrop rewards" (when user has none)

**Expected Behavior**:
1. Call `gate-cli cex launch candy-drop airdrops` with `page=1`.
2. Receive empty array.
3. Explain reward distribution timing and suggest participation.

**Response Template**:
```
No airdrop rewards found.

Rewards are typically distributed after the activity ends and tasks are completed. If you have registered for active activities, please complete the required tasks and check back after the activity concludes.

To start earning:
- Browse active activities with "Show CandyDrop activities"
- Register for an activity with "Register for CandyDrop {token}"
- Check your task progress with "My CandyDrop task progress"
```
