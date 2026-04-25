---
name: gate-info-trendanalysis
version: "2026.4.3-1"
updated: "2026-04-03"
description: "Trend and technical analysis. Use this skill ONLY when the user's query is exclusively about technical indicators or trend analysis for one coin with no other analysis dimensions. Trigger phrases: technical analysis, K-line, RSI, MACD, trend, support, resistance. If the query ALSO mentions fundamentals, risk, news, sentiment, or any other analysis dimension, use gate-info-research instead — it handles multi-dimension queries in a single unified report."
required_credentials: []
required_env_vars: []
required_permissions: []
---

# gate-info-trendanalysis

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
→ Also read [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) for **gate-info** / **gate-news**-specific rules (tool degradation, report standards, security, routing degradation, per-skill version checks when `scripts/` is present, and legacy wrapper routing).
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.
- **Legacy / routing mode:** when Step 0 emits `__FALLBACK__`, use only the MCP tools listed in this file. When Step 0 emits `__ROUTE_CLI__`, do **not** call those MCP tools; delegate to the mapped primary skill per Step 0.

> A technicals-focused Skill. The user inputs a coin name + technical analysis intent; the system calls 4 Tools (K-line data, indicator history, multi-timeframe signals, real-time market snapshot) in parallel, then the LLM aggregates into a multi-dimensional technical analysis report.

**Trigger Scenarios**: User explicitly mentions technical analysis, K-line, indicators, trend, support/resistance, or similar keywords.

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
  and its playbook contract. Carry over the minimum context: `symbol`, plus
  optional trend-window hints if the user already supplied them.
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
GATE_SKILL_CHECK_STRICT=1 bash "$HOME/.cursor/skills/gate-info-trendanalysis/scripts/update-skill.sh" check "gate-info-trendanalysis"
```

**PowerShell:**

```powershell
$env:GATE_SKILL_CHECK_STRICT = '1'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-trendanalysis\scripts\update-skill.ps1" check "gate-info-trendanalysis"
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
GATE_SKILL_CONFIRM_TOKEN="<paste from check stdout>" bash "$HOME/.cursor/skills/gate-info-trendanalysis/scripts/update-skill.sh" apply "gate-info-trendanalysis"
```

```bash
bash "$HOME/.cursor/skills/gate-info-trendanalysis/scripts/update-skill.sh" revoke-pending "gate-info-trendanalysis"
```

```powershell
$env:GATE_SKILL_CONFIRM_TOKEN = '<paste from check stdout>'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-trendanalysis\scripts\update-skill.ps1" apply "gate-info-trendanalysis"
```

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-trendanalysis\scripts\update-skill.ps1" revoke-pending "gate-info-trendanalysis"
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

- info_marketsnapshot_get_market_snapshot
- info_markettrend_get_indicator_history
- info_markettrend_get_kline
- info_markettrend_get_technical_analysis

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
| Technical analysis | "technical analysis" "K-line" "RSI" "MACD" "Bollinger" "moving average" "support" "resistance" "trend" | Execute this Skill's full workflow |
| Comprehensive analysis (incl. fundamentals) | "analyze BTC for me" | Route to `gate-info-coinanalysis` |
| Price only | "what's BTC price" | Call `info_marketsnapshot_get_market_snapshot` directly |
| Raw K-line data only | "BTC 30-day K-line" | Call `info_markettrend_get_kline` directly — no need for full Skill |

---

## Execution Workflow

Legacy path only — this section applies when Step 0 emitted `__FALLBACK__`.

### Step 0: Multi-Dimension Intent Check

Before executing this Skill, check if the user's query involves multiple analysis dimensions:

- If the query is exclusively about technical indicators or trend analysis for one coin, proceed with this Skill.
- If the query **also** mentions fundamentals, risk, news, sentiment, or any other analysis dimension beyond technicals, route to `gate-info-research` — it handles multi-dimension queries with unified tool deduplication and coherent report aggregation.

### Step 1: Intent Recognition & Parameter Extraction

Extract from user input:
- `symbol`: Coin ticker (BTC, ETH, SOL, etc.)
- `timeframe`: Analysis timeframe (e.g., "daily" → 1d, "4-hour" → 4h; default: 1d)
- `indicators`: Specific indicators the user cares about (e.g., "RSI", "MACD"; default: all)
- `period`: K-line lookback days (default: 90)

### Step 2: Call 4 MCP Tools in Parallel

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `info_markettrend_get_kline` | `symbol={symbol}, timeframe={timeframe}, limit=90` | K-line OHLCV data (default 90 bars) | Yes |
| 1b | `info_markettrend_get_indicator_history` | `symbol={symbol}, indicators=["rsi","macd","bollinger","ma"], timeframe={timeframe}` | Technical indicator history | Yes |
| 1c | `info_markettrend_get_technical_analysis` | `symbol={symbol}` | Multi-timeframe composite signals (1h/4h/1d/1w) | Yes |
| 1d | `info_marketsnapshot_get_market_snapshot` | `symbol={symbol}, timeframe="1d", source="spot"` | Real-time market snapshot (price, volume, OI, funding rate) | Yes |

> All 4 Tools are called in parallel.

### Step 3: LLM Analysis

The LLM performs technical analysis on the raw data, completing the following reasoning:
1. Identify trend from candlestick patterns (uptrend / downtrend / sideways channel)
2. Combine indicator history to assess current position (overbought / oversold / neutral)
3. Evaluate multi-timeframe signal alignment or divergence
4. Identify key support and resistance levels

### Step 4: Output Structured Report

---

## Report Template

Legacy path only — this section applies when Step 0 emitted `__FALLBACK__`.

```markdown
## {symbol} Technical Analysis Report

> Analysis time: {timestamp} | Primary timeframe: {timeframe}

### 1. Current Market Snapshot

| Metric | Value |
|--------|-------|
| Price | ${price} |
| 24h Change | {change_24h}% |
| 24h Volume | ${volume_24h} |
| 24h High | ${high_24h} |
| 24h Low | ${low_24h} |
| Open Interest | ${oi} (if available) |
| Funding Rate | {funding_rate}% (if available) |

### 2. Trend Assessment

**Overall Trend**: {Uptrend / Downtrend / Sideways / Trend Reversal}

{Trend analysis based on candlestick patterns and MA alignment:}
- MA7 / MA25 / MA99 alignment: {Bullish / Bearish / Tangled}
- Recent candlestick patterns: {Bullish Engulfing / Doji / Hammer / etc.} (if notable)
- Volume confirmation: {Rising volume + price up (healthy) / Declining volume + price up (weak momentum) / Rising volume + price down (accelerated selling)}

### 3. Technical Indicator Details

#### RSI (14)
| Timeframe | Value | Status |
|-----------|-------|--------|
| 1h | {rsi_1h} | {Overbought/Oversold/Neutral} |
| 4h | {rsi_4h} | {Overbought/Oversold/Neutral} |
| 1d | {rsi_1d} | {Overbought/Oversold/Neutral} |

{RSI divergence analysis: any bullish/bearish divergence present?}

#### MACD
| Timeframe | DIF | DEA | Histogram | Status |
|-----------|-----|-----|-----------|--------|
| 1h | {dif} | {dea} | {histogram} | {Golden Cross/Death Cross/Above Zero/Below Zero} |
| 4h | ... | ... | ... | ... |
| 1d | ... | ... | ... | ... |

#### Bollinger Bands (20, 2)
| Metric | Value |
|--------|-------|
| Upper Band | ${upper} |
| Middle Band | ${middle} |
| Lower Band | ${lower} |
| Bandwidth | {bandwidth}% |
| Current Position | {price relative to bands + percentile} |

{Narrowing bands → breakout imminent; price touching upper band → potential pullback to middle; touching lower band → potential bounce}

### 4. Key Price Levels

| Type | Price | Basis |
|------|-------|-------|
| Strong Resistance | ${resistance_1} | {Previous high / MA99 / Upper Bollinger / Round number} |
| Weak Resistance | ${resistance_2} | ... |
| Weak Support | ${support_1} | ... |
| Strong Support | ${support_2} | {Previous low / MA99 / Lower Bollinger / Volume profile cluster} |

### 5. Multi-Timeframe Signal Summary

| Timeframe | Composite Signal | Bullish Indicators | Bearish Indicators |
|-----------|-----------------|--------------------|--------------------|
| 1h | {Strong Buy/Buy/Neutral/Sell/Strong Sell} | {count} | {count} |
| 4h | ... | ... | ... |
| 1d | ... | ... | ... |
| 1w | ... | ... | ... |

**Signal Consistency**: {Are multi-timeframe signals aligned? e.g., "Short-term bearish but medium/long-term bullish — divergence present"}

### 6. Overall Technical Assessment

{LLM generates a comprehensive assessment:}
- Current trend strength evaluation
- Short-term (1-3 day) likely direction
- Medium-term (1-2 week) likely direction
- Key observation: a break above ${resistance_1} opens upside; a break below ${support_2} signals trend weakening

### Risk Warnings

{Data-driven risk alerts}

> Technical analysis is based on historical data and cannot predict future price movements. This does not constitute investment advice.
```

---

## Decision Logic

| Condition | Assessment |
|-----------|------------|
| RSI > 70 (multi-timeframe consistent) | "Multi-timeframe RSI overbought — high pullback probability" |
| RSI < 30 (multi-timeframe consistent) | "Multi-timeframe RSI oversold — high bounce probability" |
| MACD daily golden cross + 4h golden cross | "MACD multi-timeframe golden cross confirmed — bullish signal" |
| MACD daily death cross + 4h death cross | "MACD multi-timeframe death cross confirmed — bearish signal" |
| Bollinger bandwidth < 5% | "Extreme Bollinger squeeze — breakout imminent" |
| Price breaks above upper Bollinger | "Short-term overextended — potential pullback to middle band" |
| MA7 > MA25 > MA99 | "Bullish MA alignment" |
| MA7 < MA25 < MA99 | "Bearish MA alignment" |
| 3 consecutive days of rising volume + price up | "Rising volume rally — healthy trend" |
| Declining volume + price up | "Low-volume rally — watch for weakening momentum" |
| Short-term vs medium/long-term signals diverge | Flag "Bull/bear divergence — awaiting directional resolution" |
| funding_rate > 0.1% | "Extreme long crowding in futures — risk of long squeeze" |
| Any Tool returns empty/error | Skip that indicator analysis; note "Data unavailable" |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| Coin does not exist | Prompt user to verify the coin name |
| info_markettrend_get_kline insufficient data | Reduce lookback period or switch to larger timeframe; note limited data |
| info_markettrend_get_technical_analysis fails | Derive signals from K-line and indicator history manually; label "Composite signal manually derived" |
| info_markettrend_get_indicator_history partial indicators missing | Display available indicators; note missing ones as "temporarily unavailable" |
| All Tools fail | Return error message; suggest the user try again later |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "What about fundamentals?" / "Full analysis" | `gate-info-coinanalysis` |
| "Why is it pumping/dumping?" | `gate-news-eventexplain` |
| "On-chain chip analysis" | `gate-info-tokenonchain` |
| "Compare XX and YY" | `gate-info-coincompare` |
| "Recent news?" | `gate-news-briefing` |

---

## Safety Rules

1. **No trading advice**: Do not output "recommend going long/short" or "buy at XX"
2. **No specific price predictions**: Do not output "will rise to XX tomorrow" or "target price XX"
3. **Acknowledge limitations**: Clearly state that technical analysis is based on historical data and may fail
4. **Data transparency**: Label K-line data range and indicator parameter settings
5. **Flag missing data**: When indicators are unavailable, explicitly state it — never fabricate values
