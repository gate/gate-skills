# Gate Info Liveroom Location — Scenarios & Prompt Examples

## Scenario 1: Single-condition — hottest BTC market analysis lives

**Context**: User wants the hottest live rooms about Bitcoin market analysis.

**Prompt Examples**:

- "我想看现在分析比特币行情最热的直播间"
- "行情分析 比特币 最热"
- "Hottest BTC market analysis live rooms"
- "What's the hottest live for BTC market analysis?"

**Expected Behavior**:

1. Map parameters: tag=Market Analysis, coin=BTC, sort=hot, limit=10.
2. Fetch data via `GET /live/gate_ai/tag_coin_live_replay?tag=Market%20Analysis&coin=BTC&sort=hot&limit=10`.
3. Build list: each item = title (live.name or video.title) + link (streaming: `https://www.gate.io/live/video/{id}?type=live`, video: `https://www.gate.io/live/video/{id}`).
4. Output list only; do not ask "how many?" or "which coin?".

---

## Scenario 2: Defaults — hottest lives (no tag or coin)

**Context**: User only says they want the hottest lives, without specifying tag or coin.

**Prompt Examples**:

- "最热的直播"
- "Hottest live rooms"
- "看看直播"

**Expected Behavior**:

1. Apply defaults: tag=empty, coin=empty, sort=hot, limit=10.
2. Fetch data via `GET /live/gate_ai/tag_coin_live_replay?sort=hot&limit=10`.
3. Return list of title + link, up to 10 items.
4. Do not ask "Which coin?" or "Which business type?".

---

## Scenario 3: Limit and coin — 5 SOL-related hottest

**Context**: User wants 5 items, SOL-related, sorted by hottest.

**Prompt Examples**:

- "给我 5 个 SOL 相关的最热直播"
- "5 SOL hottest lives"
- "SOL 相关 前5条"

**Expected Behavior**:

1. Map parameters: coin=SOL, sort=hot, limit=5; tag=empty.
2. Fetch data via `GET /live/gate_ai/tag_coin_live_replay?coin=SOL&sort=hot&limit=5`.
3. Build list of up to 5 items: title + link.
4. Output list.

---

## Scenario 4: Newest replays / latest

**Context**: User wants the newest content (sort by new).

**Prompt Examples**:

- "最新的直播"
- "Latest replays"
- "最近开的直播"

**Expected Behavior**:

1. Map parameters: sort=new, limit=10; tag and coin empty unless stated.
2. Fetch data via API with sort=new.
3. Build list: title + link; optionally label Live vs Replay.
4. Output list.

---

## Scenario 5: Restricted region

**Context**: User is in a restricted region (e.g. US, Canada, Japan).

**Expected Behavior**:

1. Do not call the API.
2. Reply that the feature is not available in their region (or similar), without returning a list.
