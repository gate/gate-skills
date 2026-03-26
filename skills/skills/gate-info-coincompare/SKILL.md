---
name: gate-info-coincompare
version: "2026.3.25-1"
updated: "2026-03-25"
description: "Coin comparison. Use this skill whenever the user asks to compare two or more coins. Trigger phrases include: compare, versus, vs, which is better, difference. MCP tools: info_marketsnapshot_get_market_snapshot, info_coin_get_coin_info per coin (or batch/search when available)."
---

# gate-info-coincompare

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
→ Also read [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) for **gate-info** / **gate-news**-specific rules (tool degradation, report standards, security, routing degradation, and per-skill version checks when `scripts/` is present).
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

> Side-by-side comparison Skill. The user inputs 2-5 coins, the system calls market snapshot + fundamentals tools for each coin in parallel, and the LLM aggregates multi-dimensional data into a comparison table with overall analysis.

**Trigger Scenarios**: User mentions two or more coins + keywords like compare, versus, vs, which is better, difference, head-to-head.

**Per-skill updates:** This directory includes `scripts/update-skill.sh` and `scripts/update-skill.ps1`. Policy: [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) §1. The **Trigger update** steps below apply in addition to [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md); when scripts are present, use this flow for version checks before execution.

---

## Trigger update (with Execution)

**Default (PD / blocking):** On each trigger, run **`check`** first **without** **`GATE_SKILL_UPDATE_MODE=auto`**. The script **only compares** local vs remote; if `Result=update_available`, it **does not** overwrite files. **STOP** — ask the user whether to update **before** any **`apply`**, **`run`**, or skill Execution. In sandboxes (e.g. Cursor), use **full / all permissions** when later running **`apply`**. This matches **blocking update confirmation** in the independent-script TEST_REPORT: blocking is enforced by these SKILL instructions plus **check-only** behavior (not by silent auto-apply).

**Strict check (Agent / IDE — recommended on `check`):** Use **`GATE_SKILL_CHECK_STRICT=1`**. When `Result=update_available`, **`check`** **exits 3** and prints **`GATE_SKILL_CHECK_EXIT=3`** — it stops **only** that shell step. **Hard rule:** after you ask the user, **end this assistant turn**; do **not** call **`apply`**, **`run`**, or MCP in the **same** message. **`run`** applies without a prior user step — **do not** use **`run`** in chat for the blocking flow; use **`check` → user confirms → `apply`**.

### Step 1 — Check

**Install root:** `check` / `apply` read **`$DEST/SKILL.md`**. Typical **`$SKILL_ROOT`**: **`$HOME/.cursor/skills/<name>/`**, **`$HOME/.codex/skills/<name>/`**, **`$HOME/.openclaw/skills/<name>/`**, **`$HOME/.agents/skills/<name>/`**, **`$HOME/.gemini/antigravity/skills/<name>/`**. Single-arg: the script resolves **`DEST`** in that order when **`SKILL.md`** exists; otherwise **`DEST`** is `scripts/../`. Workspace-only trees need two-arg **`check`** / **`apply`** with explicit **`DEST`**.

**Bash** (blocking — no auto; example Cursor):

```bash
GATE_SKILL_CHECK_STRICT=1 bash "$HOME/.cursor/skills/gate-info-coincompare/scripts/update-skill.sh" check "gate-info-coincompare"
```

**PowerShell:**

```powershell
$env:GATE_SKILL_CHECK_STRICT = '1'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-coincompare\scripts\update-skill.ps1" check "gate-info-coincompare"
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
GATE_SKILL_CONFIRM_TOKEN="<paste from check stdout>" bash "$HOME/.cursor/skills/gate-info-coincompare/scripts/update-skill.sh" apply "gate-info-coincompare"
```

```bash
bash "$HOME/.cursor/skills/gate-info-coincompare/scripts/update-skill.sh" revoke-pending "gate-info-coincompare"
```

```powershell
$env:GATE_SKILL_CONFIRM_TOKEN = '<paste from check stdout>'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-coincompare\scripts\update-skill.ps1" apply "gate-info-coincompare"
```

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-coincompare\scripts\update-skill.ps1" revoke-pending "gate-info-coincompare"
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

## Routing Rules

| User Intent | Keywords/Pattern | Action |
|-------------|-----------------|--------|
| Multi-coin comparison | "compare BTC and ETH" "SOL vs AVAX" "Layer2 coin comparison" | Execute this Skill's full workflow |
| Single coin analysis | "analyze SOL for me" | Route to `gate-info-coinanalysis` |
| Price only | "what's BTC price" | Call `info_marketsnapshot_get_market_snapshot` directly |
| Sector overview | "how is the DeFi sector doing" | Route to `gate-info-marketoverview` |
| Ranking list | "top 10 coins by market cap" | `info_coin_get_coin_rankings` not yet available — prompt user to list specific coins to compare |

---

## Execution Workflow

### Step 1: Intent Recognition & Parameter Extraction

Extract from user input:
- `symbols[]`: List of coins (2-5), e.g., [BTC, ETH, SOL]
- If the user mentions project names (e.g., Solana, Avalanche), map to ticker symbols
- If the user mentions a sector without specific coins (e.g., "which Layer2 coins are good"), prompt them to list 2-5 specific coins

**Limits**: Minimum 2, maximum 5. If more than 5, prompt user to narrow the scope. If only 1 coin, ask for at least one more or route to `gate-info-coinanalysis`.

### Step 2: Call 2 MCP Tools per Coin in Parallel

For each `symbol` in the list, execute in parallel:

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `info_marketsnapshot_get_market_snapshot` | `symbol={symbol}, timeframe="1d", source="spot"` | Market data: real-time price, K-line summary, market cap, FDV, Fear & Greed Index | Yes |
| 1b | `info_coin_get_coin_info` | `query={symbol}` | Fundamentals: project info, sector, funding, tokenomics | Yes |

> For 3 coins, this results in 6 parallel Tool calls with no dependencies. When `info_marketsnapshot_batch_market_snapshot` and `info_coin_search_coins` are available, prefer them; otherwise use per-coin calls above.

### Step 3 (Optional): Technical Comparison

If the user explicitly requests technical comparison, or the number of coins is 3 or fewer, optionally call in parallel:

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 2 | `info_markettrend_get_technical_analysis` | `symbol={symbol}` | Technical signals: RSI, MACD, MA alignment, support/resistance | Yes |

### Step 4: LLM Cross-Comparison Report Generation

Group all Tool responses by coin, and the LLM generates a side-by-side comparison report using the template below.

---

## Report Template

```markdown
## Coin Comparison: {symbol_1} vs {symbol_2} [vs {symbol_3} ...]

### 1. Key Metrics Comparison

| Metric | {symbol_1} | {symbol_2} | {symbol_3} |
|--------|-----------|-----------|-----------|
| Price | ${price_1} | ${price_2} | ${price_3} |
| 24h Change | {change_24h_1}% | {change_24h_2}% | {change_24h_3}% |
| 7d Change | {change_7d_1}% | {change_7d_2}% | {change_7d_3}% |
| Market Cap | ${mcap_1} | ${mcap_2} | ${mcap_3} |
| Market Cap Rank | #{rank_1} | #{rank_2} | #{rank_3} |
| FDV | ${fdv_1} | ${fdv_2} | ${fdv_3} |
| 24h Volume | ${vol_1} | ${vol_2} | ${vol_3} |
| Fear & Greed Index | {fg_1} | {fg_2} | {fg_3} |

### 2. Fundamentals Comparison

| Dimension | {symbol_1} | {symbol_2} | {symbol_3} |
|-----------|-----------|-----------|-----------|
| Sector | {category_1} | {category_2} | {category_3} |
| Total Funding | ${funding_1} | ${funding_2} | ${funding_3} |
| Key Investors | {investors_1} | {investors_2} | {investors_3} |
| Circulating Ratio | {circ_ratio_1}% | {circ_ratio_2}% | {circ_ratio_3}% |
| Upcoming Unlocks | {unlock_1} | {unlock_2} | {unlock_3} |

### 3. Technical Comparison (if available)

| Dimension | {symbol_1} | {symbol_2} | {symbol_3} |
|-----------|-----------|-----------|-----------|
| Overall Signal | {signal_1} | {signal_2} | {signal_3} |
| RSI(14) | {rsi_1} | {rsi_2} | {rsi_3} |
| MACD | {macd_1} | {macd_2} | {macd_3} |
| MA Alignment | {ma_1} | {ma_2} | {ma_3} |

### 4. Comparative Summary

{LLM generates a 3-5 sentence cross-comparison analysis covering:}
- Strengths and weaknesses of each coin across dimensions
- Which coin has stronger recent performance and which is weakening
- Whether fundamentals and market data align
- Differentiated risks to watch

### 5. Dimension-by-Dimension Winners

| Dimension | Best Performer | Weakest Performer | Notes |
|-----------|---------------|-------------------|-------|
| Short-term Gains | {best_1} | {worst_1} | ... |
| Market Cap / FDV Ratio | {best_2} | {worst_2} | ... |
| Funding Background | {best_3} | {worst_3} | ... |
| Technical Signals | {best_4} | {worst_4} | ... |

### ⚠️ Risk Warnings

{Risk differentials identified in the comparison, e.g.:}
- {symbol_x} has only {x}% circulating supply — significantly higher unlock pressure than peers
- {symbol_y} RSI is in overbought territory — higher short-term pullback risk than {symbol_z}
- {symbol_w} 24h volume is disproportionately low relative to market cap — liquidity disadvantage

> The above analysis is a data-driven side-by-side comparison and does not constitute investment advice. Please make decisions based on your own risk tolerance.
```

---

## Decision Logic

| Condition | Assessment |
|-----------|------------|
| 24h change difference > 10% between coins | Flag "Significant short-term performance divergence" |
| FDV/Market Cap ratio for one coin > 2x others | Flag "Relatively elevated FDV — higher unlock risk" |
| Circulating ratio < 30% | Flag "Low circulating ratio — future sell pressure risk" |
| 24h volume / market cap < 1% | Flag "Low liquidity — slippage risk for large trades" |
| RSI difference > 30 (one overbought, another oversold) | Flag "Technicals in opposite states — evaluate separately" |
| Any Tool returns empty/error | Mark corresponding column as "Data unavailable"; display remaining coins normally |
| Two coins are from entirely different sectors | Remind user: "Cross-sector comparison is for reference only — core value drivers differ significantly" |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| A coin does not exist | Note the name may be incorrect; exclude it and continue comparing the rest |
| Only 1 coin provided | Route to `gate-info-coinanalysis` (single coin analysis) |
| More than 5 coins provided | Prompt user to narrow down to 5 or fewer, or suggest comparing in batches |
| A coin's Tool times out | Skip that coin's dimension; mark as "Temporarily unavailable" in the table |
| All Tools fail | Return error message; suggest the user try again later |
| User inputs an address | Route to `gate-info-addresstracker` |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "Give me a deep dive on SOL" | `gate-info-coinanalysis` |
| "Show me SOL technicals in detail" | `gate-info-trendanalysis` |
| "Any recent news for these coins?" | `gate-news-briefing` |
| "Is SOL's contract safe?" | `gate-info-riskcheck` |
| "Why did ETH pump but SOL didn't?" | `gate-news-eventexplain` |
| "How about on-chain data comparison?" | `gate-info-tokenonchain` |

---

## Available Tools & Degradation Notes

| PRD-Defined Tool | Actually Available Tool | Status | Degradation Strategy |
|-----------------|-------------------------|--------|----------------------|
| `info_marketsnapshot_batch_market_snapshot` | `info_marketsnapshot_get_market_snapshot` | Degraded | Call `get_market_snapshot` per coin in parallel — no speed impact |
| `info_coin_search_coins` | `info_coin_get_coin_info` | Degraded | Use `get_coin_info` with symbol query as substitute |
| `info_markettrend_get_technical_analysis` | `info_markettrend_get_technical_analysis` | ✅ Ready | — |

---

## Safety Rules

1. **No investment advice**: Comparative analysis is data-driven and must include a "not investment advice" disclaimer
2. **No ranking recommendations**: Do not output conclusions like "buy A instead of B" — only present data differences
3. **No price predictions**: Do not output specific target prices or up/down predictions
4. **Data transparency**: Label data source and update time for each dimension
5. **Flag missing data**: When any dimension has no data, explicitly mark "Data unavailable" — never fabricate data
6. **Cross-sector reminder**: When compared coins belong to different sectors, remind the user of fundamental logic differences
