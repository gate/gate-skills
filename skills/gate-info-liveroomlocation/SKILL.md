---
name: gate-info-liveroomlocation
version: "2026.3.23-1"
updated: "2026-03-23"
description: "Gate live stream and replay listing skill. Use when the user asks to find live rooms or replays by tag, coin, or sort. Triggers on 'live room list', '最热直播', 'replay list', 'SOL live stream'."
required_credentials: []
required_env_vars: []
required_permissions: []
---

# Gate Info Liveroom Location — Live & Replay Listing

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.


---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate-Info | ✅ Required |

### Authentication
- API Key Required: No
- Credentials Source: None; this skill uses read-only Gate Info / Gate News MCP access only.

### Installation Check
- Required: Gate-Info
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), then execute this skill's live/replay listing workflow.

- `SKILL.md` keeps intent mapping, product behavior, and response semantics.
- `references/mcp.md` is the authoritative MCP execution layer for parameter extraction, single-endpoint calls, and degradation handling.

## Workflow

When the user asks about live rooms or replays (by business type, coin, hottest/newest, or count), execute the following steps.

### Step 1: Parse intent and map parameters

From natural language, extract and map to API parameters:

- **tag**: Market Analysis | Hot Topics | Blockchain | Others | empty (all). Default: empty.
- **coin**: Coin symbol (e.g. BTC, SOL) or empty (all). Default: empty.
- **sort**: `hot` (hottest) | `new` (newest). Default: `hot`.
- **limit**: Integer 1–10. Default: 10.

Key mapping rules:

| User phrase (examples) | Param | Value |
|------------------------|--------|--------|
| 行情分析, 市场分析, Market Analysis | tag | Market Analysis |
| 热门话题, Hot Topics | tag | Hot Topics |
| 区块链, Blockchain | tag | Blockchain |
| 其他, Others | tag | Others |
| Not mentioned | tag | empty |
| Bitcoin, BTC, SOL, ETH, 比特币 | coin | BTC, SOL, etc. |
| Not mentioned | coin | empty |
| 最热, 热门, 按热度, hottest | sort | hot |
| 最新, 最近, newest | sort | new |
| Not mentioned | sort | hot |
| 前5条, 给我3个, 10个 | limit | 5, 3, 10 |
| Not mentioned | limit | 10 |

**Do not** ask the user "how many?" or "which coin?" when they did not specify; apply defaults.

### Step 2: Call the API

Call `GET /live/gate_ai/tag_coin_live_replay` with query parameters:

- `tag`: string (optional)
- `coin`: string (optional)
- `sort`: `hot` | `new` (optional, default hot)
- `limit`: integer (optional, default 10, max 10)

Key data to extract from response:

- `data.list`: array of items, each with `content_type` (`"streaming"` or `"video"`), and either `live` (with `id`, `name`) or `video` (with `id`, `title`).

**Pre-filter**: If the user is in a restricted region (US, Canada, Japan, or other Gate-restricted regions), do **not** call the API; reply that the feature is not available in their region.

### Step 3: Build list output

For each item in `data.list`:

- **Title**: `live.name` when `content_type === "streaming"`, else `video.title` when `content_type === "video"`.
- **Link**:
  - `content_type === "streaming"`: `https://www.gate.io/live/video/{live.id}?type=live`
  - `content_type === "video"`: `https://www.gate.io/live/video/{video.id}`

Output a list of lines: each line = **title** + **link**. Optionally label "Live" or "Replay". Do not add extra fields (e.g. likes, duration) unless required by product.

## Judgment Logic Summary

| Condition | Signal | Meaning |
|-----------|--------|---------|
| User in restricted region | Block | Do not call API; reply that the feature is not available in their region |
| tag / coin / sort / limit not mentioned | Use default | tag=empty, coin=empty, sort=hot, limit=10 |
| content_type === "streaming" | Live | Use live.name; link with `?type=live` |
| content_type === "video" | Replay | Use video.title; link without type |
| Empty list or API error | No list | Reply with a short message; do not fabricate a list |

## Report Template

- **List format**: One line per item: `[Live/Replay] Title — <link>`.
- **Disclaimer** (if needed): Gate live and replay content is provided by creators; it does not constitute investment or viewing advice; the platform only provides display and filtering.

## Single API only

Use only `GET /live/gate_ai/tag_coin_live_replay`. Do not combine or mention other live or video APIs.
