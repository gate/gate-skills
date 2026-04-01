---
name: gate-info-coinanalysis
version: "2026.3.25-1"
updated: "2026-03-25"
description: "Single-coin comprehensive analysis skill. Use when the user asks about one coin without splitting into separate risk, news-only, or trend-only tasks. Triggers on 'analyze SOL', 'how is BTC', 'is ETH worth buying'. Do NOT use if the query adds explicit risk, multi-coin compare, or event-only why-moved — use gate-info-research."
---

# gate-info-coinanalysis

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
→ Also read [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) for **gate-info** / **gate-news**-specific rules (tool degradation, report standards, security, routing degradation, and per-skill version checks when `scripts/` is present).
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

> The most frequently used Skill. The user inputs a coin name, the system calls 5 MCP Tools in parallel to fetch fundamentals + market data + technicals + news + social sentiment, then the LLM aggregates the results into a structured analysis report.

**Trigger Scenarios**: User mentions a specific coin + keywords like analyze, how is, worth, look at, fundamentals, market analysis.

**Per-skill updates:** This directory includes `scripts/update-skill.sh` and `scripts/update-skill.ps1`. Policy: [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) §1. The **Trigger update** steps below apply in addition to [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md); when scripts are present, use this flow for version checks before execution.

---

## Trigger update (with Execution)

**Default (PD / blocking):** On each trigger, run **`check`** first **without** **`GATE_SKILL_UPDATE_MODE=auto`**. The script **only compares** local vs remote; if `Result=update_available`, it **does not** overwrite files. **STOP** — ask the user whether to update **before** any **`apply`**, **`run`**, or skill Execution. In sandboxes (e.g. Cursor), use **full / all permissions** when later running **`apply`**. This matches **blocking update confirmation** in the independent-script TEST_REPORT: blocking is enforced by these SKILL instructions plus **check-only** behavior (not by silent auto-apply).

**Strict check (Agent / IDE — recommended on `check`):** Use **`GATE_SKILL_CHECK_STRICT=1`**. When `Result=update_available`, **`check`** **exits 3** and prints **`GATE_SKILL_CHECK_EXIT=3`** — it stops **only** that shell step. **Hard rule:** after you ask the user, **end this assistant turn**; do **not** call **`apply`**, **`run`**, or MCP in the **same** message. **`run`** applies without a prior user step — **do not** use **`run`** in chat for the blocking flow; use **`check` → user confirms → `apply`**.

### Step 1 — Check

**Install root:** `check` / `apply` read **`$DEST/SKILL.md`**. Typical **`$SKILL_ROOT`**: **`$HOME/.cursor/skills/<name>/`**, **`$HOME/.codex/skills/<name>/`**, **`$HOME/.openclaw/skills/<name>/`**, **`$HOME/.agents/skills/<name>/`**, **`$HOME/.gemini/antigravity/skills/<name>/`**. Single-arg: the script resolves **`DEST`** in that order when **`SKILL.md`** exists; otherwise **`DEST`** is `scripts/../`. Workspace-only trees need two-arg **`check`** / **`apply`** with explicit **`DEST`**.

**Bash** (blocking — no auto; example Cursor):

```bash
GATE_SKILL_CHECK_STRICT=1 bash "$HOME/.cursor/skills/gate-info-coinanalysis/scripts/update-skill.sh" check "gate-info-coinanalysis"
```

**PowerShell:**

```powershell
$env:GATE_SKILL_CHECK_STRICT = '1'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-coinanalysis\scripts\update-skill.ps1" check "gate-info-coinanalysis"
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
GATE_SKILL_CONFIRM_TOKEN="<paste from check stdout>" bash "$HOME/.cursor/skills/gate-info-coinanalysis/scripts/update-skill.sh" apply "gate-info-coinanalysis"
```

```bash
bash "$HOME/.cursor/skills/gate-info-coinanalysis/scripts/update-skill.sh" revoke-pending "gate-info-coinanalysis"
```

```powershell
$env:GATE_SKILL_CONFIRM_TOKEN = '<paste from check stdout>'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-coinanalysis\scripts\update-skill.ps1" apply "gate-info-coinanalysis"
```

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-coinanalysis\scripts\update-skill.ps1" revoke-pending "gate-info-coinanalysis"
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

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate-Info | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- info_coin_get_coin_info
- info_coin_search_coins
- info_marketsnapshot_get_market_snapshot
- info_markettrend_get_technical_analysis
- news_feed_get_social_sentiment
- news_feed_search_news

### Authentication
- API Key Required: No

### Installation Check
- Required: Gate-Info
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), then execute this skill's single-coin analysis workflow.

- `SKILL.md` keeps intent gating and final report policy.
- `references/mcp.md` is the authoritative MCP execution layer for parallel feed collection, synthesis order, and degraded handling.

## Routing Rules

| User Intent | Keywords | Action |
|-------------|----------|--------|
| Single coin comprehensive analysis | "analyze SOL" "how is BTC" "is ETH worth buying" | Execute this Skill's full workflow |
| Price only | "what's BTC price" "ETH current price" | Do NOT use this Skill — call `info_marketsnapshot_get_market_snapshot` directly |
| Multi-coin comparison | "compare BTC and ETH" | Route to `gate-info-coincompare` |
| News only | "any SOL news lately" | Route to `gate-news-briefing` |
| Technicals only | "BTC technical analysis" "what's the RSI" | Route to `gate-info-trendanalysis` |

---

## Execution Workflow

### Step 0: Multi-Dimension Intent Check

Before executing this Skill, check if the user's query involves multiple analysis dimensions:

- If the query is a standard single-coin analysis (e.g., "analyze SOL", "how is BTC"), proceed with this Skill.
- If the query **also** mentions security/risk check, event attribution, multi-coin comparison, or any other analysis dimension beyond single-coin comprehensive, route to `gate-info-research` — it handles multi-dimension queries with unified tool deduplication and coherent report aggregation.

### Step 1: Intent Recognition & Parameter Extraction

Extract from user input:
- `symbol`: Coin ticker (e.g., BTC, SOL, ETH)
- If the user mentions a project name (e.g., Solana, Uniswap), map it to the ticker symbol

If the coin cannot be identified, **ask the user to clarify the coin name** — do not guess.

### Step 2: Call 5 MCP Tools in Parallel

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `info_coin_get_coin_info` | `query={symbol}, scope="full"` | Fundamentals: project info, team, funding, sector, tokenomics, unlock schedule | Yes |
| 1b | `info_marketsnapshot_get_market_snapshot` | `symbol={symbol}, timeframe="1d", source="spot"` | Market data: price, 24h/7d change, market cap, OI, funding rate, Fear & Greed Index | Yes |
| 1c | `info_markettrend_get_technical_analysis` | `symbol={symbol}` | Technicals: multi-timeframe signals (RSI zones, MACD cross, MA alignment, support/resistance) | Yes |
| 1d | `news_feed_search_news` | `coin={symbol}, limit=5, sort_by="importance"` | News: top 5 most important recent articles | Yes |
| 1e | `news_feed_get_social_sentiment` | `coin={symbol}` | Social sentiment: Twitter KOL discussion volume, sentiment bias | Yes |

> All 5 Tools are called in parallel with no dependencies. If no news MCP is configured, call only the first 3 Gate-info tools; mark sentiment sections as "No data".

### Step 3: LLM Aggregation

Pass all 5 Tool responses to the LLM to generate a structured analysis report.

### Step 4: Output Structured Report

---

## Report Template

```markdown
## {symbol} Comprehensive Analysis

### 1. Fundamentals Overview

| Metric | Value |
|--------|-------|
| Project Name | {project_name} |
| Sector | {category} |
| Market Cap Rank | #{market_cap_rank} |
| Circulating Market Cap | ${market_cap} |
| Fully Diluted Valuation | ${fdv} |
| Total Funding Raised | ${total_funding} |
| Key Investors | {investors} |

{Brief analysis of tokenomics and unlock schedule; flag any upcoming large unlocks}

### 2. Market Data & Technical Analysis

**Current Market Data**

| Metric | Value | Status |
|--------|-------|--------|
| Price | ${price} | — |
| 24h Change | {change_24h}% | {Up/Down/Sideways} |
| 7d Change | {change_7d}% | {Up/Down/Sideways} |
| 24h Volume | ${volume_24h} | {High/Low/Normal} |
| RSI(14) | {rsi} | {Overbought/Oversold/Neutral} |
| Fear & Greed Index | {fear_greed} | {Extreme Fear/Fear/Neutral/Greed/Extreme Greed} |

**Technical Signals**

{Based on info_markettrend_get_technical_analysis multi-timeframe signals, give a Bullish/Bearish/Neutral overall assessment}

- Short-term (1h/4h): {signal}
- Medium-term (1d): {signal}
- Support: ${support}
- Resistance: ${resistance}

### 3. News & Market Sentiment

**Recent Key News**

1. [{title}]({source}) — {summary} ({time})
2. ...

**Social Sentiment**

- Twitter Discussion Volume: {level}
- KOL Sentiment Bias: {Bullish/Bearish/Neutral}
- Sentiment Score: {sentiment_score}

### 4. Overall Assessment

{LLM generates a 3-5 sentence assessment covering:}
- Current market phase for this asset
- Primary drivers (fundamentals / technicals / sentiment)
- Key risks to monitor

### ⚠️ Risk Warnings

{Data-driven risk alerts, e.g.:}
- RSI overbought — elevated short-term pullback risk
- Upcoming large token unlock
- High funding rate — leveraged long crowding
- Low liquidity (if applicable)

> The above analysis is data-driven and does not constitute investment advice. Please make decisions based on your own risk tolerance.
```

---

## Decision Logic

| Condition | Assessment |
|-----------|------------|
| RSI > 70 | Flag "Overbought — elevated short-term pullback risk" |
| RSI < 30 | Flag "Oversold — potential bounce" |
| 24h volume > 7d avg volume x 2 | Flag "Significant volume surge" |
| 24h volume < 7d avg volume x 0.5 | Flag "Notable volume decline" |
| funding_rate > 0.05% | Flag "High funding rate — long crowding" |
| funding_rate < -0.05% | Flag "Negative funding rate — short crowding" |
| fear_greed > 75 | Flag "Extreme Greed — exercise caution" |
| fear_greed < 25 | Flag "Extreme Fear — potential opportunity" |
| Token unlock in next 30 days > 5% of circulating supply | Flag "Large upcoming token unlock — potential sell pressure" |
| Any Tool returns empty/error | Skip that section; note "Data unavailable" in the report |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| Coin does not exist | Prompt user to verify the coin name; suggest using `info_coin_search_coins` |
| A single Tool times out | Skip that dimension; note "This dimension is temporarily unavailable" |
| All Tools fail | Return error message; suggest the user try again later |
| User inputs multiple coins | Route to `gate-info-coincompare` |
| User inputs an address instead of a coin | Route to `gate-info-addresstracker` |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "Give me a technical analysis" | `gate-info-trendanalysis` |
| "Any recent news?" | `gate-news-briefing` |
| "What about on-chain data?" | `gate-info-tokenonchain` |
| "Is this coin safe?" | `gate-info-riskcheck` |
| "Compare XX and YY" | `gate-info-coincompare` |
| "Why is it pumping/dumping?" | `gate-news-eventexplain` |

---

## Safety Rules

1. **No investment advice**: The overall assessment is data-driven analysis and must include a "not investment advice" disclaimer
2. **No price predictions**: Do not output specific target prices or up/down predictions
3. **Data transparency**: Label data source and update time for each dimension
4. **Flag missing data**: When any dimension has no data, explicitly inform the user — never fabricate data
