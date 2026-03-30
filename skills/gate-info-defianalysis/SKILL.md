---
name: gate-info-defianalysis
version: "2026.3.30-6"
updated: "2026-03-30"
description: "DeFi ecosystem analysis via Gate-Info MCP. Use this skill whenever the user wants TVL rankings, protocol metrics, yield/APY, stablecoins, bridges, exchange reserves, or liquidation heatmaps. Trigger phrases include Uniswap TVL, DeFi ranking, USDC yield, bridge volume, exchange BTC reserves, liquidation density. Route coin-only fundamentals to gate-info-coinanalysis. Sub-scenario tools: info_platformmetrics_* family and info_coin_get_coin_info (exact tool names per scenario in SKILL.md)."
---

# gate-info-defianalysis

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
→ Also read [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) for **gate-info** / **gate-news**-specific rules (tool degradation, report standards, security, routing degradation, and per-skill version checks when `scripts/` is present).
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

> The DeFi Ecosystem Analysis Skill. Routes to different sub-scenarios based on user intent (overview / single platform / yield / stablecoins / bridges / reserves / liquidation), each calling one or more MCP tools.

**Trigger Scenarios**: User asks about DeFi protocols, TVL, yield rates, stablecoins, cross-chain bridges, exchange reserves, liquidation distribution, etc.

**Per-skill updates:** This directory includes `scripts/update-skill.sh` and `scripts/update-skill.ps1`. Policy: [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) §1. The **Trigger update** steps below apply in addition to [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md); when scripts are present, use this flow for version checks before execution.

---

## Trigger update (with Execution)

**Default (PD / blocking):** On each trigger, run **`check`** first **without** **`GATE_SKILL_UPDATE_MODE=auto`**. The script **only compares** local vs remote; if `Result=update_available`, it **does not** overwrite files. **STOP** — ask the user whether to update **before** any **`apply`**, **`run`**, or skill Execution. In sandboxes (e.g. Cursor), use **full / all permissions** when later running **`apply`**. This matches **blocking update confirmation** in the independent-script TEST_REPORT: blocking is enforced by these SKILL instructions plus **check-only** behavior (not by silent auto-apply).

**Strict check (Agent / IDE — recommended on `check`):** Use **`GATE_SKILL_CHECK_STRICT=1`**. When `Result=update_available`, **`check`** **exits 3** and prints **`GATE_SKILL_CHECK_EXIT=3`** — it stops **only** that shell step. **Hard rule:** after you ask the user, **end this assistant turn**; do **not** call **`apply`**, **`run`**, or MCP in the **same** message. **`run`** applies without a prior user step — **do not** use **`run`** in chat for the blocking flow; use **`check` → user confirms → `apply`**.

### Step 1 — Check

**Install root:** `check` / `apply` read **`$DEST/SKILL.md`**. Typical **`$SKILL_ROOT`**: **`$HOME/.cursor/skills/<name>/`**, **`$HOME/.codex/skills/<name>/`**, **`$HOME/.openclaw/skills/<name>/`**, **`$HOME/.agents/skills/<name>/`**, **`$HOME/.gemini/antigravity/skills/<name>/`**. Single-arg: the script resolves **`DEST`** in that order when **`SKILL.md`** exists; otherwise **`DEST`** is `scripts/../`. Workspace-only trees need two-arg **`check`** / **`apply`** with explicit **`DEST`**.

**Bash** (blocking — no auto; example Cursor):

```bash
GATE_SKILL_CHECK_STRICT=1 bash "$HOME/.cursor/skills/gate-info-defianalysis/scripts/update-skill.sh" check "gate-info-defianalysis"
```

**PowerShell:**

```powershell
$env:GATE_SKILL_CHECK_STRICT = '1'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-defianalysis\scripts\update-skill.ps1" check "gate-info-defianalysis"
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
GATE_SKILL_CONFIRM_TOKEN="<paste from check stdout>" bash "$HOME/.cursor/skills/gate-info-defianalysis/scripts/update-skill.sh" apply "gate-info-defianalysis"
```

```bash
bash "$HOME/.cursor/skills/gate-info-defianalysis/scripts/update-skill.sh" revoke-pending "gate-info-defianalysis"
```

```powershell
$env:GATE_SKILL_CONFIRM_TOKEN = '<paste from check stdout>'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-defianalysis\scripts\update-skill.ps1" apply "gate-info-defianalysis"
```

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-defianalysis\scripts\update-skill.ps1" revoke-pending "gate-info-defianalysis"
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

**Query Operations (Read-only)** — use by sub-scenario; do not call tools outside the active scenario.

- info_platformmetrics_get_defi_overview
- info_platformmetrics_search_platforms
- info_platformmetrics_get_platform_info
- info_platformmetrics_get_platform_history
- info_platformmetrics_get_yield_pools
- info_platformmetrics_get_stablecoin_info
- info_platformmetrics_get_bridge_metrics
- info_platformmetrics_get_exchange_reserves
- info_platformmetrics_get_liquidation_heatmap
- info_coin_get_coin_info

### Authentication
- API Key Required: No

### Installation Check
- Required: Gate-Info
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## Routing Rules

| User Intent | Keywords | Action |
|-------------|----------|--------|
| DeFi overview / TVL ranking | "DeFi overview" "TVL ranking" "top DeFi protocols" | Execute Sub-scenario A: Overview |
| Single platform deep-dive | "Uniswap TVL" "Aave metrics" "Compound info" | Execute Sub-scenario B: Platform Detail |
| Yield / APY query | "best yield" "USDC APY" "lending rates" "where to earn" | Execute Sub-scenario C: Yield Pools |
| Stablecoin analysis | "USDT market cap" "stablecoin ranking" "USDC circulation" | Execute Sub-scenario D: Stablecoins |
| Cross-chain bridge | "bridge volume" "top bridges" "cross-chain TVL" | Execute Sub-scenario E: Bridges |
| Exchange reserves | "Binance BTC reserves" "exchange reserves" "proof of reserves" | Execute Sub-scenario F: Exchange Reserves |
| Liquidation analysis | "BTC liquidation heatmap" "where are liquidations" "liquidation density" | Execute Sub-scenario G: Liquidation Heatmap |
| Coin fundamentals (no DeFi focus) | "analyze SOL" "how is BTC" | Route to `gate-info-coinanalysis` |
| Market overview | "how's the market" | Route to `gate-info-marketoverview` |

---

## Execution Workflow

### Step 0: Multi-Dimension Intent Check

- If the query is about DeFi/platform metrics, proceed with this Skill.
- If the query also involves coin fundamentals, technicals, or news beyond DeFi scope, route to `gate-info-research` (if available).

### Step 1: Intent Recognition & Parameter Extraction

Extract from user input:

- `platform_name` (optional): Protocol name (e.g., Uniswap, Aave, Lido)
- `symbol` (optional): Token/stablecoin symbol (e.g., USDC, USDT, ETH)
- `chain` (optional): Blockchain filter (e.g., Ethereum, Arbitrum)
- `exchange` (optional): Exchange name (e.g., Binance, OKX)

### Step 2: Call MCP Tools by Sub-scenario

#### Sub-scenario A: DeFi Overview

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `info_platformmetrics_get_defi_overview` | `category="all"` | Total TVL, volume, fees across DeFi/CEX/DEX | Yes |
| 1b | `info_platformmetrics_search_platforms` | `sort_by="tvl", limit=10` | Top 10 platforms by TVL | Yes |

#### Sub-scenario B: Platform Detail

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `info_platformmetrics_get_platform_info` | `platform_name={name}, scope="full"` | Full platform metrics (TVL, volume, fees, chains) | Yes |
| 1b | `info_platformmetrics_get_platform_history` | `platform_name={name}, metrics=["tvl","volume"]` | Historical trend | Yes |
| 1c | `info_coin_get_coin_info` | `query={token_symbol}` | Platform's native token info | Yes |

#### Sub-scenario C: Yield Pools

| Step | MCP Tool | Parameters | Retrieved Data |
|------|----------|------------|----------------|
| 1 | `info_platformmetrics_get_yield_pools` | `project={name}, chain={chain}, symbol={symbol}, sort_by="apy", limit=20` | Yield pool rankings with APY, TVL |

#### Sub-scenario D: Stablecoins

| Step | MCP Tool | Parameters | Retrieved Data |
|------|----------|------------|----------------|
| 1 | `info_platformmetrics_get_stablecoin_info` | `symbol={symbol}, chain={chain}, limit=10` | Stablecoin ranking or single coin detail with chain distribution |

#### Sub-scenario E: Bridges

| Step | MCP Tool | Parameters | Retrieved Data |
|------|----------|------------|----------------|
| 1 | `info_platformmetrics_get_bridge_metrics` | `bridge_name={name}, chain={chain}` | Bridge ranking or single bridge chain breakdown |

#### Sub-scenario F: Exchange Reserves

| Step | MCP Tool | Parameters | Retrieved Data |
|------|----------|------------|----------------|
| 1 | `info_platformmetrics_get_exchange_reserves` | `exchange={exchange}, asset={asset}` | Exchange on-chain reserves (BTC, ETH, etc.) |

#### Sub-scenario G: Liquidation Heatmap

| Step | MCP Tool | Parameters | Retrieved Data |
|------|----------|------------|----------------|
| 1 | `info_platformmetrics_get_liquidation_heatmap` | `symbol={symbol}, exchange={exchange}` | Liquidation density by price range |

### Step 3: LLM Aggregation

Generate sub-scenario-specific analysis. For overview, provide market context; for detail, provide competitive positioning; for yield, highlight risk/reward.

### Step 4: Progressive Loading (Bridges & Stablecoins)

For Bridges and Stablecoins, use a list-first, detail-on-demand pattern:

1. **First call** (no `bridge_name` / narrow `symbol`): ranking list — summary without full chain breakdown.
2. **Second call** (user follow-up): specific `bridge_name` or `symbol` — full chain-level details.

---

## Report Template

### Template A: DeFi Overview

```markdown
## DeFi Ecosystem Overview

> Generated: {timestamp}

### Market Summary

| Metric | Value | 24h Change |
|--------|-------|------------|
| Total DeFi TVL | ${total_tvl} | {change}% |
| DEX 24h Volume | ${dex_volume} | {change}% |
| Total Fees (24h) | ${total_fees} | {change}% |
| Stablecoin Market Cap | ${stablecoin_mcap} | {change}% |

### Top 10 Protocols by TVL

| Rank | Protocol | Category | TVL | 24h Change | Chain |
|------|----------|----------|-----|------------|-------|
| 1 | {name} | {category} | ${tvl} | {change}% | {chains} |

### Analysis

{LLM assessment: DeFi market trend, capital flows, notable shifts}

> Data sourced from Gate Info MCP. Does not constitute investment advice.
```

### Template B: Platform Detail

```markdown
## {platform_name} Deep Dive

> Generated: {timestamp}

### Key Metrics

| Metric | Value | Rank |
|--------|-------|------|
| TVL | ${tvl} | #{rank} |
| 24h Volume | ${volume} | — |
| 24h Fees | ${fees} | — |

### TVL Trend

{Describe trend from historical data}

### Token Info ({symbol})

| Metric | Value |
|--------|-------|
| Price | ${price} |
| Market Cap | ${market_cap} |
| FDV | ${fdv} |

### Analysis

{LLM competitive analysis}

> Data sourced from Gate Info MCP. Does not constitute investment advice.
```

### Templates C–G (Yield / Stablecoin / Bridge / Reserve / Liquidation)

- Summary metrics at top
- Ranked table of data
- 2–3 sentence LLM analysis
- Standard disclaimer

---

## Decision Logic

| Condition | Assessment / next step |
|-----------|-------------------------|
| Generic DeFi market, TVL leaderboard, or “top protocols” | Sub-scenario A (Overview) |
| User names a specific protocol (Uniswap, Aave, …) | Sub-scenario B (Platform detail) |
| Yield, APY, lending, “where to earn” | Sub-scenario C (Yield pools) |
| Stablecoins, peg, circulation, ranking | Sub-scenario D; use progressive loading per Step 4 |
| Bridges, cross-chain TVL, bridge volume | Sub-scenario E; list-first, detail on follow-up |
| Exchange reserves, PoR, “exchange BTC holdings” | Sub-scenario F |
| Liquidations, heatmap, density by price | Sub-scenario G |
| Ambiguous intent | Ask one clarifying question or default to A |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| Platform name not found | Suggest similar platform names; ask user to verify |
| Single Tool fails | Skip that section; note "Data temporarily unavailable" |
| All Tools fail | Return error; suggest user try again later |
| No yield pools match criteria | Broaden search (remove chain/symbol filter); inform user |
| Exchange not supported | List supported exchanges; ask user to choose another |
| Symbol not recognized | Try matching via `info_coin_get_coin_info`; ask user if unclear |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "Analyze the token" | `gate-info-coinanalysis` |
| "Technical analysis of the token" | `gate-info-trendanalysis` |
| "Is this protocol safe?" | `gate-info-riskcheck` |
| "On-chain data for the token" | `gate-info-tokenonchain` |
| "Any news about this protocol?" | `gate-news-briefing` |
| "How does macro affect DeFi?" | `gate-info-macroimpact` |
| "How's the market overall?" | `gate-info-marketoverview` |

---

## Safety Rules

1. **No yield guarantees**: APY/yield data is historical and subject to change; state clearly that past rates do not guarantee future returns.
2. **Smart contract risk**: When showing yield pools or protocols, note that DeFi carries smart contract risk.
3. **No endorsement**: Listing a protocol does not constitute an endorsement; maintain neutrality.
4. **Reserve disclaimers**: Exchange reserve data is on-chain observable but may not reflect total assets.
5. **Liquidation data**: Liquidation heatmaps show estimated levels, not guaranteed triggers.
6. **Data transparency**: Label data source, update frequency, and known limitations.
