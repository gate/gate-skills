---
name: gate-info-marketoverview
version: "2026.4.6-1"
updated: "2026-04-06"
description: "Market overview. Use this skill ONLY when the user's query is exclusively about overall market conditions with no specific coin analysis. Trigger phrases: how is the market, market overview, what is happening in crypto. If the query ALSO mentions a specific coin to analyze, risk to check, technicals to review, or any other analysis dimension, use gate-info-research instead — it handles multi-dimension queries in a single unified report."
required_credentials: []
required_env_vars: []
required_permissions: []
---

# gate-info-marketoverview

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
→ Also read [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) for **gate-info** / **gate-news**-specific rules (tool degradation, report standards, security, routing degradation, per-skill version checks when `scripts/` is present, and legacy wrapper routing).
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.
- **Legacy / routing mode:** when Step 0 emits `__FALLBACK__`, use only the MCP tools listed in this file. When Step 0 emits `__ROUTE_CLI__`, do **not** call those MCP tools; delegate to the mapped primary skill per Step 0.

> The crypto market "dashboard" Skill. The user asks about overall market conditions in a single sentence; the system calls 5 MCP Tools in parallel to fetch market-wide data + sector leaderboards + DeFi overview + recent events + macro summary, then the LLM aggregates into a market-briefing-level structured report.

**Trigger Scenarios**: User asks about overall market conditions — not about a specific coin.

**Per-skill updates:** This directory includes `scripts/update-skill.sh` and may include `scripts/update-skill.ps1`. **ClawHub** packages uploaded to the marketplace often omit `update-skill.ps1` (upload-page restriction); **GitHub / Bitbucket** source trees keep both. Policy: [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) §1. The **Trigger update** steps below apply in addition to [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md); when scripts are present, use this flow for version checks before execution.

**Update check — user visibility:** Technical failures during version check (missing script, sandbox, network, non-zero exit, no parseable `Result=` line) must **not** be explained to the user; continue with Execution per [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md). Only **successful** `check` / `apply` outcomes may be summarized (including **`update_available`** / strict **exit 3**, which is still a **success path** that requires user confirmation before `apply`). **Do not** auto-download `update-skill.*` from the network. **Static reference** if `.ps1` is missing: canonical scripts live in [gate/gate-skills](https://github.com/gate/gate-skills) under `skills/<name>/scripts/` (same `<name>` as frontmatter).

---

## Step 0 — Wrapper routing probe

This legacy skill is a compatibility alias for the primary CLI skill
`gate-info-research`.

Before Trigger update, MCP tool selection, or any legacy Execution Workflow,
run a deterministic shell probe:

```bash
PRIMARY_SKILL="gate-info-research"
HAS_PRIMARY=0
for root in \
  "$HOME/.cursor/skills" \
  "$HOME/.codex/skills" \
  "$HOME/.openclaw/skills" \
  "$HOME/.agents/skills" \
  "$HOME/.gemini/antigravity/skills"
do
  if [ -f "$root/$PRIMARY_SKILL/SKILL.md" ]; then
    HAS_PRIMARY=1
    break
  fi
done

if command -v gate-cli >/dev/null 2>&1 && [ "$HAS_PRIMARY" = "1" ]; then
  echo "__ROUTE_CLI__"
else
  echo "__FALLBACK__"
fi
```

Interpretation:

- `__ROUTE_CLI__` → stop here. Do **not** run Trigger update or the legacy MCP
  sections below. Follow
  `https://github.com/gate/gate-skills/blob/master/skills/gate-info-research/SKILL.md`
  and its playbook contract. Carry over the minimum context: no required slots;
  the primary skill should pick `market_overview`.
- `__FALLBACK__` → continue with Trigger update and the legacy MCP workflow in
  this file.

---

## Trigger update (with Execution)

**Default (PD / blocking):** On each trigger, run **`check`** first **without** **`GATE_SKILL_UPDATE_MODE=auto`**. The script **only compares** local vs remote; if `Result=update_available`, it **does not** overwrite files. **STOP** — ask the user whether to update **before** any **`apply`**, **`run`**, or skill Execution. In sandboxes (e.g. Cursor), use **full / all permissions** when later running **`apply`**. This matches **blocking update confirmation** in the independent-script TEST_REPORT: blocking is enforced by these SKILL instructions plus **check-only** behavior (not by silent auto-apply).

**Strict check (Agent / IDE — recommended on `check`):** Use **`GATE_SKILL_CHECK_STRICT=1`**. When `Result=update_available`, **`check`** **exits 3** and prints **`GATE_SKILL_CHECK_EXIT=3`** — it stops **only** that shell step. **Hard rule:** after you ask the user, **end this assistant turn**; do **not** call **`apply`**, **`run`**, or MCP in the **same** message. **`run`** applies without a prior user step — **do not** use **`run`** in chat for the blocking flow; use **`check` → user confirms → `apply`**.

### Step 1 — Check

**Install root:** `check` / `apply` read **`$DEST/SKILL.md`**. Typical **`$SKILL_ROOT`**: **`$HOME/.cursor/skills/<name>/`**, **`$HOME/.codex/skills/<name>/`**, **`$HOME/.openclaw/skills/<name>/`**, **`$HOME/.agents/skills/<name>/`**, **`$HOME/.gemini/antigravity/skills/<name>/`**. Single-arg: the script resolves **`DEST`** in that order when **`SKILL.md`** exists; otherwise **`DEST`** is `scripts/../`. Workspace-only trees need two-arg **`check`** / **`apply`** with explicit **`DEST`**.

**Agent selection rules** (run **at most one** of the fenced examples below; choose by OS and files under `$SKILL_ROOT/scripts/`):
- **macOS / Linux / WSL / Git Bash:** If `update-skill.sh` exists → use **only** the **Bash** example.
- **Windows (native PowerShell):** If `update-skill.ps1` exists → use **only** the **PowerShell** example.
- **Windows without `.ps1`** (typical ClawHub install): If only `update-skill.sh` exists → try **WSL** or **Git Bash** (`bash`) using the **same command shape** as the Bash example. If bash is unavailable or execution fails → **skip Step 1** silently (no script stderr or “version check failed” message to the user); proceed to Execution.
- **Neither script exists:** Skip Step 1 silently; proceed to Execution. Do **not** invent `GATE_SKILL_CONFIRM_TOKEN` or run `apply` / `revoke-pending`.

**Bash** (blocking — no auto; example Cursor):

```bash
GATE_SKILL_CHECK_STRICT=1 bash "$HOME/.cursor/skills/gate-info-marketoverview/scripts/update-skill.sh" check "gate-info-marketoverview"
```

**PowerShell:**

```powershell
$env:GATE_SKILL_CHECK_STRICT = '1'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-marketoverview\scripts\update-skill.ps1" check "gate-info-marketoverview"
```

**Result semantics:** `skipped` = no action. `update_available` = remote newer; **with blocking flow, do not apply until the user agrees**. `check_failed` = could not compare — proceed with current version per [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md); **do not** surface technical check failure details to the user.

**Agent parse (stdout):** `GATE_SKILL_UPDATE_AGENT_ACTION=…`. **`BLOCK_UNTIL_USER_CONFIRMS_UPDATE`** → Step 2 before Execution. **`CONTINUE_SKILL_EXECUTION`** → no block from the check script.

### Step 2 — Confirm or Reject (blocking)

**Runtime:** Use the **same** shell family for Step 2 as for Step 1 (Bash vs PowerShell). If Step 1 was **skipped**, do **not** run `apply` or `revoke-pending`.

**If `update_available`:**

1. **STOP** — do NOT proceed to Execution yet.
2. Inform the user (e.g. newer version available; summarize if helpful).
3. **Wait for the user’s reply** — blocking step.

   **Hard rule (Cursor / Agent):** When `check` reports **`update_available`**, or **`BLOCK_UNTIL_USER_CONFIRMS_UPDATE`**, or strict **`exit 3`**, **end this turn** after asking. **Only** in the **user’s next message** run **`apply`** (if they agree) or **`revoke-pending`** (if they decline). Do **not** chain **`apply`** in the same turn as **`check`** for this flow.

   - User **agrees** → run **`apply`** with **`GATE_SKILL_CONFIRM_TOKEN`** from strict **`check`** stdout when required, then Execution.
   - User **declines** → **`revoke-pending`**, then Execution on the current install.

**Two-step gate (strict `check`):** **`apply`** / **`run`** (without **`GATE_SKILL_UPDATE_MODE=auto`**) **fail** until **`GATE_SKILL_CONFIRM_TOKEN`** matches **`.gate-skill-apply-token`**. User decline → **`revoke-pending`**.

```bash
GATE_SKILL_CONFIRM_TOKEN="<paste from check stdout>" bash "$HOME/.cursor/skills/gate-info-marketoverview/scripts/update-skill.sh" apply "gate-info-marketoverview"
```

```bash
bash "$HOME/.cursor/skills/gate-info-marketoverview/scripts/update-skill.sh" revoke-pending "gate-info-marketoverview"
```

```powershell
$env:GATE_SKILL_CONFIRM_TOKEN = '<paste from check stdout>'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-marketoverview\scripts\update-skill.ps1" apply "gate-info-marketoverview"
```

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-marketoverview\scripts\update-skill.ps1" revoke-pending "gate-info-marketoverview"
```

**If Step 1 was not strict** (no pending token): **`apply`** without **`GATE_SKILL_CONFIRM_TOKEN`** is allowed.

**If `skipped` or `check_failed`:** no update step; proceed to Execution.

### Optional — `GATE_SKILL_UPDATE_MODE=auto`

For **CI / unattended automation only**: setting **`GATE_SKILL_UPDATE_MODE=auto`** on **`check`** makes the script **apply immediately** when the remote is newer — **no** user confirmation and **incompatible** with **blocking update confirmation** tests. Do **not** use **`auto`** on **`check`** when reproducing the blocking PD flow.

### Parameters

- **name**: Frontmatter `name` above; must match `skills/<name>/` on gate-skills.
- **Invoke**: Use **`$SKILL_ROOT/scripts/update-skill.sh`** (or `.ps1`) where **`$SKILL_ROOT/SKILL.md`** is this skill — e.g. **`~/.cursor/skills/<name>`**, **`~/.codex/skills/<name>`**, **`~/.openclaw/skills/<name>`**, **`~/.agents/skills/<name>`**, **`~/.gemini/antigravity/skills/<name>`**; do not treat **`~/.cursor`** (or any host root without **`skills/<name>/SKILL.md`**) as the install. With one arg, the script resolves **`$SKILL_ROOT`** in that order before falling back to the script’s directory; workspace installs need **explicit `DEST`**. **Two-arg `check` / `apply` / `revoke-pending`:** canonical order is **absolute `DEST` (skill root) first**, then **`name`**; **`update-skill.sh` / `update-skill.ps1` auto-swap** when only one normalized path contains `SKILL.md` (e.g. agent passes `name` then path).
- **ClawHub vs full tree:** Installs without `update-skill.ps1` may copy it from [gate/gate-skills](https://github.com/gate/gate-skills) under `skills/<name>/scripts/` (**manual** only; agents must **not** auto-download).

**Do not** dump raw script logs into the user-facing reply except when debugging. On **`check` exit 3** (strict), do not run Execution until Step 2 is resolved. On **`check_failed`** or **`apply` failure**, still run Execution when appropriate per runtime rules.

---

## MCP Dependencies

Legacy path only — this section applies when Step 0 emitted `__FALLBACK__`.

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate-Info | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- info_coin_get_coin_rankings
- info_macro_get_macro_summary
- info_marketsnapshot_get_market_overview
- info_marketsnapshot_get_market_snapshot
- info_platformmetrics_get_defi_overview
- news_events_get_latest_events

### Authentication
- API Key Required: No
- Credentials Source: None; this skill uses read-only Gate Info / Gate News MCP access only.

### Installation Check
- Required: Gate-Info
- Install: Use the local Gate MCP installation flow for the current host IDE before continuing.
- Continue only after the required Gate MCP server is available in the current environment.

## Routing Rules

Legacy path only — when Step 0 emitted `__ROUTE_CLI__`, routing is delegated to
`gate-info-research`.

| User Intent | Keywords | Action |
|-------------|----------|--------|
| Market overview | "how's the market" "market overview" "what's happening in crypto" "are we up or down today" | Execute this Skill's full workflow |
| Single coin analysis | "how is BTC" "analyze ETH" | Route to `gate-info-coinanalysis` |
| News only | "what's happening" | Route to `gate-news-briefing` |
| DeFi deep-dive | "which DeFi protocol is best" "TVL rankings" | Route to `gate-info-defianalysis` |
| Macro deep-dive | "how's the jobs report" "any economic data today" | Route to `gate-info-macroimpact` |

---

## Execution Workflow

Legacy path only — this section applies when Step 0 emitted `__FALLBACK__`.

### Step 0: Multi-Dimension Intent Check

Before executing this Skill, check if the user's query involves multiple analysis dimensions:

- If the query is exclusively about overall market conditions with no specific coin to deep-dive, proceed with this Skill.
- If the query **also** mentions a specific coin to analyze, risk to check, technicals to review, or any other analysis dimension beyond market overview, route to `gate-info-research` — it handles multi-dimension queries with unified tool deduplication and coherent report aggregation.

### Step 1: Intent Recognition

Confirm the user is asking about overall market conditions (not a single coin). Optionally extract:
- `time_context`: e.g., "today", "this week", "recently" (affects news/event time range)

### Step 2: Call 5 MCP Tools in Parallel

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `info_marketsnapshot_get_market_overview` | (none) | Full market: total market cap, 24h volume, BTC dominance, Fear & Greed Index, gainer/loser ratio | Yes |
| 1b | `info_coin_get_coin_rankings` | `ranking_type="gainers", time_range="24h", limit=5` | Top 5 gainers | Yes |
| 1c | `info_platformmetrics_get_defi_overview` | `category="all"` | DeFi total TVL, DEX 24h volume, stablecoin total market cap | Yes |
| 1d | `news_events_get_latest_events` | `time_range="24h", limit=5` | Major events in the past 24h | Yes |
| 1e | `info_macro_get_macro_summary` | (none) | Macro snapshot (DXY, rates, CPI trend) | Yes |

> All 5 Tools are called in parallel with no dependencies. If a tool is not available, omit that call and mark the corresponding report section as "No data". If `info_marketsnapshot_get_market_overview` is not available, use `info_marketsnapshot_get_market_snapshot` for BTC/ETH as fallback.

### Step 2b: Optional Supplementary Calls

| Condition | Supplementary Tool | Parameters | Purpose |
|-----------|--------------------|------------|---------|
| User asks about "this week" or needs trend context | `info_coin_get_coin_rankings` | `ranking_type="losers", time_range="24h", limit=5` | Add top losers |
| User is interested in sector rotation | `info_coin_get_coin_rankings` | `ranking_type="hot", limit=10` | Trending coins |

### Step 3: LLM Aggregation

---

## Report Template

Legacy path only — this section applies when Step 0 emitted `__FALLBACK__`.

```markdown
## Crypto Market Overview

> Data as of: {timestamp}

### 1. Market Summary

| Metric | Current Value | 24h Change |
|--------|--------------|------------|
| Total Market Cap | ${total_market_cap} | {change}% |
| 24h Volume | ${total_volume_24h} | {change}% |
| BTC Dominance | {btc_dominance}% | {change}pp |
| Fear & Greed Index | {fear_greed_index} | {Extreme Fear/Fear/Neutral/Greed/Extreme Greed} |
| Gainer/Loser Ratio | {gainers}/{losers} | {Bulls/Bears/Balanced} |

**Market Status**: {One-sentence description of the current market state based on the above metrics}

### 2. Sectors & Leaderboard

**24h Top Gainers**

| Rank | Coin | Price | 24h Change |
|------|------|-------|------------|
| 1 | {symbol} | ${price} | +{change}% |
| 2 | ... | ... | ... |

**24h Top Losers** (if data available)

| Rank | Coin | Price | 24h Change |
|------|------|-------|------------|
| 1 | {symbol} | ${price} | {change}% |
| 2 | ... | ... | ... |

{If the leaderboards show sector patterns (e.g., L2s rallying, Memes dumping), flag sector rotation}

### 3. DeFi Overview

| Metric | Value | Change |
|--------|-------|--------|
| DeFi Total TVL | ${defi_tvl} | {change}% |
| DEX 24h Volume | ${dex_volume} | {change}% |
| Stablecoin Total Market Cap | ${stablecoin_cap} | {change}% |

### 4. Recent Major Events

1. 🔴/🟡/🟢 [{event_title}] — {event_summary} ({time})
2. ...

> 🔴 = High impact, 🟡 = Medium impact, 🟢 = Low impact

### 5. Macro Environment

| Metric | Value | Trend |
|--------|-------|-------|
| US Dollar Index (DXY) | {dxy} | {Rising/Falling/Sideways} |
| 10Y Treasury Yield | {yield_10y}% | {Rising/Falling} |
| Fed Funds Rate | {fed_rate}% | {Hiking/Cutting/Paused} |

{If there are upcoming macro events (NFP, CPI, FOMC), briefly mention potential market impact}

### 6. Overall Assessment

{LLM generates a 3-5 sentence assessment:}
- Current market phase (bull / bear / sideways / recovery)
- Primary drivers
- Key risks or opportunities to watch

> The above analysis is data-driven and does not constitute investment advice.
```

---

## Decision Logic

| Condition | Label/Assessment |
|-----------|-----------------|
| fear_greed > 75 | "Extreme Greed — exercise caution at highs" |
| fear_greed < 25 | "Extreme Fear — potential opportunity amid panic" |
| BTC dominance > 55% and most altcoins declining | "Capital rotating back to BTC — altcoins under pressure" |
| BTC dominance declining + most altcoins rising | "Potential altcoin season" |
| Gainer/Loser ratio > 3:1 | "Broad-based rally — bulls in control" |
| Gainer/Loser ratio < 1:3 | "Broad-based decline — bears in control" |
| DeFi TVL 7d change > +10% | "Significant capital inflow into DeFi" |
| Stablecoin market cap rising | "Off-exchange capital flowing in — bullish signal" |
| Any Tool returns empty/error | Skip that section; note "Data unavailable" |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| get_market_overview or core snapshot fails | Return degraded version showing only available sections; or use get_market_snapshot for BTC/ETH as fallback |
| Macro data unavailable | Skip "Macro Environment" section; note "Macro data temporarily unavailable" |
| Event data unavailable | Skip "Recent Major Events" section |
| All Tools fail | Return error message; suggest the user try again later |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "How is BTC?" / clicks on a specific coin | `gate-info-coinanalysis` |
| "Why did XX pump?" | `gate-news-eventexplain` |
| "Any recent news?" | `gate-news-briefing` |
| "DeFi details" | `gate-info-defianalysis` |
| "Macro data impact" | `gate-info-macroimpact` |
| "Give me a BTC technical analysis" | `gate-info-trendanalysis` |

---

## Safety Rules

1. **No investment advice**: Market assessments are data-driven; must include a "not investment advice" disclaimer
2. **No trend predictions**: Do not output "tomorrow will go up/down" style predictions
3. **Data transparency**: Label data source and update time
4. **Flag missing data**: When any section has no data, explicitly state it — never fabricate data
5. **Avoid emotional language**: Use objective, neutral language to describe market conditions
