---
name: gate-news-communityscan
version: "2026.3.30-5"
updated: "2026-03-30"
description: "Community sentiment via Gate-News MCP, X/Twitter-first. Use for social discussion, KOL takes, or opinion on a coin or topic. Triggers: what does the community think about ETH, Twitter or X sentiment, what are people saying, KOL opinions. Reddit, Discord, Telegram when search_ugc is available; until then label output as X/Twitter-only. Tools: news_feed_search_x, news_feed_get_social_sentiment."
---

# gate-news-communityscan

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
→ Also read [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) for **gate-info** / **gate-news**-specific rules (tool degradation, report standards, security, routing degradation, and per-skill version checks when `scripts/` is present).
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

> Community Sentiment Scan Skill (**X/Twitter focused**). Parallel calls fetch X/Twitter discussion analysis and quantitative social sentiment; LLM aggregates into a community insights report.

**Trigger Scenarios**: Community opinions, Twitter/X discussions, KOL views, social sentiment, etc.

**Per-skill updates:** This directory includes `scripts/update-skill.sh` and `scripts/update-skill.ps1`. Policy: [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) §1. The **Trigger update** steps below apply in addition to [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md); when scripts are present, use this flow for version checks before execution.

---

## Trigger update (with Execution)

**Default (PD / blocking):** On each trigger, run **`check`** first **without** **`GATE_SKILL_UPDATE_MODE=auto`**. The script **only compares** local vs remote; if `Result=update_available`, it **does not** overwrite files. **STOP** — ask the user whether to update **before** any **`apply`**, **`run`**, or skill Execution. In sandboxes (e.g. Cursor), use **full / all permissions** when later running **`apply`**. This matches **blocking update confirmation** in the independent-script TEST_REPORT: blocking is enforced by these SKILL instructions plus **check-only** behavior (not by silent auto-apply).

**Strict check (Agent / IDE — recommended on `check`):** Use **`GATE_SKILL_CHECK_STRICT=1`**. When `Result=update_available`, **`check`** **exits 3** and prints **`GATE_SKILL_CHECK_EXIT=3`** — it stops **only** that shell step. **Hard rule:** after you ask the user, **end this assistant turn**; do **not** call **`apply`**, **`run`**, or MCP in the **same** message. **`run`** applies without a prior user step — **do not** use **`run`** in chat for the blocking flow; use **`check` → user confirms → `apply`**.

### Step 1 — Check

**Install root:** `check` / `apply` read **`$DEST/SKILL.md`**. Typical **`$SKILL_ROOT`**: **`$HOME/.cursor/skills/<name>/`**, **`$HOME/.codex/skills/<name>/`**, **`$HOME/.openclaw/skills/<name>/`**, **`$HOME/.agents/skills/<name>/`**, **`$HOME/.gemini/antigravity/skills/<name>/`**. Single-arg: the script resolves **`DEST`** in that order when **`SKILL.md`** exists; otherwise **`DEST`** is `scripts/../`. Workspace-only trees need two-arg **`check`** / **`apply`** with explicit **`DEST`**.

**Bash** (blocking — no auto; example Cursor):

```bash
GATE_SKILL_CHECK_STRICT=1 bash "$HOME/.cursor/skills/gate-news-communityscan/scripts/update-skill.sh" check "gate-news-communityscan"
```

**PowerShell:**

```powershell
$env:GATE_SKILL_CHECK_STRICT = '1'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-news-communityscan\scripts\update-skill.ps1" check "gate-news-communityscan"
```

**Result semantics:** `skipped` = no action. `update_available` = remote newer; **with blocking flow, do not apply until the user agrees**. `check_failed` = could not compare — proceed with current version per [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md).

**Agent parse (stdout):** `GATE_SKILL_UPDATE_AGENT_ACTION=…`. **`BLOCK_UNTIL_USER_CONFIRMS_UPDATE`** → Step 2 before Execution. **`CONTINUE_SKILL_EXECUTION`** → no block from the check script.

### Step 2 — Confirm or Reject (blocking)

**If `update_available`:**

1. **STOP** — do NOT proceed to Execution yet.
2. Inform the user (e.g. newer version available; summarize if helpful).
3. **Wait for the user’s reply** — blocking step.

   **Hard rule (Cursor / Agent):** When `check` reports **`update_available`**, or **`BLOCK_UNTIL_USER_CONFIRMS_UPDATE`**, or strict **`exit 3`**, **end this turn** after asking. **Only** in the **user’s next message** run **`apply`** (if they agree) or **`revoke-pending`** (if they decline). Do **not** chain **`apply`** in the same turn as **`check`** for this flow.

   - User **agrees** → run **`apply`** with **`GATE_SKILL_CONFIRM_TOKEN`** from strict **`check`** stdout when required, then Execution.
   - User **declines** → **`revoke-pending`**, then Execution on the current install.

**Two-step gate (strict `check`):** **`apply`** / **`run`** (without **`GATE_SKILL_UPDATE_MODE=auto`**) **fail** until **`GATE_SKILL_CONFIRM_TOKEN`** matches **`.gate-skill-apply-token`**. User decline → **`revoke-pending`**.

```bash
GATE_SKILL_CONFIRM_TOKEN="<paste from check stdout>" bash "$HOME/.cursor/skills/gate-news-communityscan/scripts/update-skill.sh" apply "gate-news-communityscan"
```

```bash
bash "$HOME/.cursor/skills/gate-news-communityscan/scripts/update-skill.sh" revoke-pending "gate-news-communityscan"
```

```powershell
$env:GATE_SKILL_CONFIRM_TOKEN = '<paste from check stdout>'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-news-communityscan\scripts\update-skill.ps1" apply "gate-news-communityscan"
```

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-news-communityscan\scripts\update-skill.ps1" revoke-pending "gate-news-communityscan"
```

**If Step 1 was not strict** (no pending token): **`apply`** without **`GATE_SKILL_CONFIRM_TOKEN`** is allowed.

**If `skipped` or `check_failed`:** no update step; proceed to Execution.

### Optional — `GATE_SKILL_UPDATE_MODE=auto`

For **CI / unattended automation only**: setting **`GATE_SKILL_UPDATE_MODE=auto`** on **`check`** makes the script **apply immediately** when the remote is newer — **no** user confirmation and **incompatible** with **blocking update confirmation** tests. Do **not** use **`auto`** on **`check`** when reproducing the blocking PD flow.

### Parameters

- **name**: Frontmatter `name` above; must match `skills/<name>/` on gate-skills.
- **Invoke**: Use **`$SKILL_ROOT/scripts/update-skill.sh`** (or `.ps1`) where **`$SKILL_ROOT/SKILL.md`** is this skill — e.g. **`~/.cursor/skills/<name>`**, **`~/.codex/skills/<name>`**, **`~/.openclaw/skills/<name>`**, **`~/.agents/skills/<name>`**, **`~/.gemini/antigravity/skills/<name>`**; do not treat **`~/.cursor`** (or any host root without **`skills/<name>/SKILL.md`**) as the install. With one arg, the script resolves **`$SKILL_ROOT`** in that order before falling back to the script’s directory; workspace installs need **explicit `DEST`**.

**Do not** dump raw script logs into the user-facing reply except when debugging. On **`check` exit 3** (strict), do not run Execution until Step 2 is resolved. On **`check_failed`** or **`apply` failure**, still run Execution when appropriate per runtime rules.

---

## Known Limitations

- **UGC platforms**: `news_social_search_ugc` (Reddit / Discord / Telegram) is **not** online. Label reports **X/Twitter only**.
- Historical sentiment trend may be single-point only depending on API.

---

## MCP Dependencies

### Required MCP Servers

| MCP Server | Status |
|------------|--------|
| Gate-News | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- news_feed_search_x (X/Twitter discussion — e.g., Grok-backed analysis per upstream)
- news_feed_get_social_sentiment

### Authentication
- API Key Required: No

### Installation Check
- Required: Gate-News
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursorinstaller`
  - Codex: `gate-mcp-codexinstaller`
  - Claude: `gate-mcp-claudeinstaller`
  - OpenClaw: `gate-mcp-openclawinstaller`

## Routing Rules

| User Intent | Keywords | Action |
|-------------|----------|--------|
| Community opinion on a coin | "what does community think about ETH" | Execute with `coin` |
| X/Twitter discussion | "Twitter discussion" "KOL views" | Execute (X-focused) |
| General social sentiment | "overall market sentiment" | Execute (no specific coin) |
| Reddit/Discord specific | "Reddit discussion" | Inform: X now; UGC coming |
| News only | "any crypto news" | Route to `gate-news-briefing` |
| Coin analysis | "analyze SOL" | Route to `gate-info-coinanalysis` |
| Why price moved | "why did BTC pump" | Route to `gate-news-eventexplain` |

---

## Execution Workflow

### Step 0: Multi-Dimension Intent Check

- Community/social sentiment → this Skill.
- Coin fundamentals + technicals + macro together → `gate-info-research` (if available).

### Step 1: Intent Recognition & Parameter Extraction

- `coin` (optional)
- `topic` (optional): e.g., ETF, regulation, Layer 2
- `query`: constructed from coin + topic for X search; if neither, general market social scan

### Step 2: Call MCP Tools in Parallel

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `news_feed_search_x` | `query={coin or topic}` | X discussion / narratives / KOL angles | Yes |
| 1b | `news_feed_get_social_sentiment` | `coin={coin}` if specified | Sentiment score, ratios, mention volume | Yes |

### Step 3: LLM Aggregation

- Synthesize qualitative X discussion with quantitative sentiment
- Dominant narratives and KOL themes
- Sentiment vs price alignment or divergence

---

## Report Template

```markdown
## Community Sentiment Scan: {coin or topic}

> Generated: {timestamp} | Platforms: X/Twitter only
> Note: Reddit/Discord/Telegram not yet supported.

### X/Twitter Discussion

{Summary from news_feed_search_x}

**Key Narratives**: …
**Notable KOL Views**: …

### Sentiment Metrics

| Metric | Value | Assessment |
|--------|-------|------------|
| Sentiment Score | {score} | {Bullish/Bearish/Neutral} |

### Sentiment vs Price

| Dimension | Current |
|-----------|---------|
| Social Sentiment | … |
| Price Trend (24h) | … |
| Alignment | {Aligned / Divergent} |

### Key Takeaways

{2–3 insights}

> Community sentiment is not a reliable price predictor. This does not constitute investment advice.
```

---

## Decision Logic

| Condition | Assessment |
|-----------|------------|
| Sentiment score > 70 | Strongly bullish — contrarian caution |
| Sentiment score < 30 | Strongly bearish — possible capitulation or opportunity |
| Positive ratio > 80% | Strong positive consensus — watch for reversal |
| Discussion volume > 2x 7d average | Unusual activity — possible catalyst |
| KOL opinions divided | Broken consensus — uncertainty |
| Sentiment bullish but price falling | Divergence — sentiment may lag |
| Sentiment bearish but price rising | Divergence — market defying expectations |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| `news_feed_search_x` fails | Sentiment metrics only; note X discussion unavailable |
| `news_feed_get_social_sentiment` fails | X discussion only; skip metrics |
| Both Tools fail | Return error; suggest retry |
| No X discussions for query | Broaden query; note limited data |
| User asks for Reddit/Discord | State UGC not available; X-only for now |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "Analyze this coin" | `gate-info-coinanalysis` |
| "Any news about this?" | `gate-news-briefing` |
| "Why is it pumping/dumping?" | `gate-news-eventexplain` |
| "Technical analysis?" | `gate-info-trendanalysis` |
| "On-chain data?" | `gate-info-tokenonchain` |
| "How's the overall market?" | `gate-info-marketoverview` |

---

## Safety Rules

1. **No fabricated opinions**: Only report what data supports; do not invent KOL quotes.
2. **Source attribution**: Attribute generically to KOL/community unless public figure is clearly named in data.
3. **Neutral presentation**: Show bullish and bearish views.
4. **Sentiment ≠ prediction**: State limitations clearly.
5. **Platform transparency**: Label X/Twitter-only coverage.
6. **Misinformation**: Prefer "unverified claims circulating" over stating rumors as fact.
