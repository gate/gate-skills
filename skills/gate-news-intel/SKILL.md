---
name: gate-news-intel
version: "2026.4.20-2"
updated: "2026-04-20"
description: "Use this skill whenever the user’s main ask is news, events, listings, or social/UGC. Primary gate-cli news (optional info for market context). Covers briefings, event explain, exchange announcements, UGC X/Reddit/YouTube, sentiment. Triggers: what happened, why crash, new listings, community take. Delegate: gate-info-research (research-first), gate-info-web3 (on-chain), gate-info-risk (safety). v0.5.2; do not use unshipped +brief +event-explain +community-scan +market +coin shortcuts."
---

# gate-news-intel

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
→ Also read [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) for **gate-info** and **gate-news** shared rules.
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

## CLI and playbook contract

1. **Primary boundary**: **news, events, announcements, and social/UGC intelligence**. Optional **`info`** calls appear only in playbooks that explicitly add market or coin background (`intel_plus_market`, `market_wide_intel`).
2. Every command MUST exist under **`gate-cli v0.5.2`**. Call only what is listed in [playbooks/gate-news-intel.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-news-intel.yaml). When preflight `route` is `CLI`, do **not** use Gate MCP from this skill.
3. Always pass **`--format json`** on data-collection commands.
4. **Separate fact from opinion**: label **facts** (dated events, official announcements, news wires) vs **community / UGC / X / social** (always cite source type: UGC, X, Reddit, YouTube, sentiment index).
5. **Synthesis order (PRD 5.6.7)**:
   - **“Why did it drop / crash?”** → causal **event chain first** (Section 2), then optionally market/coin background (Section 4).
   - **“How does the community see ...?”** → **Section 3 (community / UGC / X / sentiment) before** broad market overview (Section 4).
6. Final user-facing reports may use the user’s locale; this `SKILL.md` stays English for discovery (repository `CLAUDE.md` rule 1).

---

## Step 0 — Preflight

Follow [skills/_shared/preflight.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/preflight.md) verbatim:

1. Run `gate-cli preflight --format json`; parse `.route`, `.status`, `.user_message`.
2. Branch: `CLI` → continue; `MCP_FALLBACK` → emit `__FALLBACK__` and halt (legacy MCP fallback is outside this repo’s primary skills); `BLOCK` → echo `user_message` and halt.
3. When `status == "ready_with_migration_warning"`, remember it — Step 3 appends one migrate hint at the end of the report.

Do NOT run `news` / `info` data collection until `route == "CLI"`.

---

## Step 1 — Intent routing

Map the user query to **exactly one** playbook id from [playbooks/gate-news-intel.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-news-intel.yaml).

| Playbook id | When to pick | Required slots |
|-------------|----------------|----------------|
| `news_brief` | Headlines / “what happened recently” **with a named asset** | `symbol` |
| `event_explain` | “Why did it drop / crash / event explanation / cause” | `symbol` |
| `exchange_listings` | Listings, delistings, maintenance, **announcements** | — |
| `community_intel` | “Community take”, Reddit, YouTube, X, social / sentiment (social-first) | `symbol` |
| `intel_plus_market` | User wants **news + market or coin background** | `symbol` |
| `market_wide_intel` | Broad “what is happening in crypto” **without** a ticker | — |

### Slot extraction

- `symbol`: ticker (`BTC`, `ETH`, ...). Ask if missing when the playbook requires it.
- `time_range`: `24h` / `7d` / `30d`. Defaults: `24h` for brief/sentiment; `7d` for UGC/X.
- `event_id`: only when the user references a concrete event for `get-event-detail`.
- `topic_query`: for `market_wide_intel` web search.

### Cross-skill routing at Step 1

| User signal | Route to |
|-------------|----------|
| “Is it safe / honeypot / blacklist” | `gate-info-risk` (primary) |
| “Trace this address / on-chain / TVL / reserves” | `gate-info-web3` (primary) |
| “Analyze this coin / fundamentals / technicals / macro” (research-first) | `gate-info-research` (primary) |

---

## Step 2 — Data collection

Execute the chosen playbook. Same `parallel_group` → concurrent; wait between groups.

**Shortcut fallbacks (not executed as literal commands)** — use the YAML command blocks; see `cli_future_shortcut` in the playbook for `+brief`, `+event-explain`, `+community-scan`, `+market-overview`, `+coin-overview`.

**`exchange_listings`**: base invocation uses `limit` + `format` only; if the user supplied `symbol`, add `--coin {symbol}` when the CLI supports it (`get-exchange-announcements --help`).

**`event_explain`**: call `get-event-detail` **only** when `event_id` is known; otherwise omit that command.

**Info failures**: In `intel_plus_market`, `market_overview` / `coin_info` / `market_snapshot` / `technical_analysis` are **optional** — if they fail, still deliver the **news-led** report (PRD 5.6.8).

---

## Step 3 — Synthesis

Produce **five sections**, in this order:

### Report template

```markdown
## Intel briefing — {subject}

### 1. Event / news takeaway
- 3–5 bullets; separate **verified facts** from **unconfirmed** items

### 2. Key facts and timeline
- Time-ordered, verifiable items from `search-news` / `get-latest-events` / `get-event-detail` where used

### 3. Community / UGC / X / Reddit / YouTube
- **Must** cover, when the playbook includes them: UGC (`search-ugc`), X (`search-x`), and sentiment where applicable (`get-social-sentiment`)
- Label every bullet with **source type** (e.g. UGC / X / sentiment index) — do not state opinion as on-chain fact

### 4. Market or coin background (if any)
- Only when the playbook includes `info` or `get-market-overview` in `market_wide_intel`; if not used, state **no extra market context**

### 5. Conclusion and what to watch
- Not investment advice; list follow-up items

> This report is based on public data and tool output; it is not investment advice.
```

### Migrate hint

If Step 0 had `ready_with_migration_warning`, append **verbatim** the migration blockquote line from [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md) (line starting with `⚙️`).

---

## Cross-skill routing + Safety rules

### Routing

Follow [skills/_shared/routing.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/routing.md). Do not absorb **research / web3 / risk** primary intents into this skill. News-intel-specific follow-ups (after the briefing is delivered and the user asks a follow-up):

| Follow-up intent | Target |
|------------------|--------|
| "deeper research on this coin" / "is it worth attention" / "fundamentals / technicals / macro" | `gate-info-research` |
| "address from the event" / "what is on-chain" / "protocol TVL / reserves / smart money" | `gate-info-web3` |
| "is this token safe" / "honeypot" / "blacklist" / "compliance" | `gate-info-risk` |
| User changes `symbol` or time window and wants the same class of intel | Re-enter the same playbook with the new slots |

### Safety rules

Follow [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md). News-intel-specific:

1. No buy/sell advice; no price targets.
2. **Community and UGC are first-class** in Section 3 (not footnotes) when `community_intel` or relevant commands in other playbooks fire.
3. Never fabricate events or quotes — if empty, mark **no data**.

---

## References

| File | Load when... |
|------|------------|
| [skills/gate-news-intel/references/scenarios.md](https://github.com/gate/gate-skills/blob/master/skills/gate-news-intel/references/scenarios.md) | Picking among brief / event / community / listings / market-wide. |
| [skills/gate-news-intel/references/cli-reference.md](https://github.com/gate/gate-skills/blob/master/skills/gate-news-intel/references/cli-reference.md) | Flag tables for `news` and optional `info` commands. |
| [skills/gate-news-intel/references/troubleshooting.md](https://github.com/gate/gate-skills/blob/master/skills/gate-news-intel/references/troubleshooting.md) | Optional flags, `get-exchange-announcements` filters, empty `event_id`. |
| [skills/_shared/preflight.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/preflight.md) | Step 0. |
| [skills/_shared/routing.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/routing.md) | Cross-skill matrix. |
| [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md) | Shared report rules. |
