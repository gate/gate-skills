---
name: gate-news-listing
version: "2026.4.6-1"
updated: "2026-04-06"
description: "Exchange listing tracker. Use this skill whenever the user asks about exchange listing, delisting, or maintenance announcements. Trigger phrases include: any new coins listed recently, what did Binance list, new listings, delisted. MCP tools: news_feed_get_exchange_announcements, info_coin_get_coin_info, info_marketsnapshot_get_market_snapshot."
required_credentials: []
required_env_vars: []
required_permissions: []
---

# gate-news-listing

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
→ Also read [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) for **gate-info** / **gate-news**-specific rules (tool degradation, report standards, security, routing degradation, per-skill version checks when `scripts/` is present, and legacy wrapper routing).
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.
- **Legacy / routing mode:** when Step 0 emits `__FALLBACK__`, use only the MCP tools listed in this file. When Step 0 emits `__ROUTE_CLI__`, do **not** call those MCP tools; delegate to the mapped primary skill per Step 0.

> Listing radar Skill. The user queries exchange listing/delisting/maintenance announcements, the system first calls the exchange announcements Tool, then supplements high-interest coins with fundamentals and market data. The LLM aggregates everything into a structured exchange activity report.

**Trigger Scenarios**: User mentions an exchange name + listing/delisting keywords, or asks "any new coins listed recently" or "any new projects".

**Per-skill updates:** This directory includes `scripts/update-skill.sh` and may include `scripts/update-skill.ps1`. **ClawHub** packages uploaded to the marketplace often omit `update-skill.ps1` (upload-page restriction); **GitHub / Bitbucket** source trees keep both. Policy: [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) §1. The **Trigger update** steps below apply in addition to [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md); when scripts are present, use this flow for version checks before execution.

**Update check — user visibility:** Technical failures during version check (missing script, sandbox, network, non-zero exit, no parseable `Result=` line) must **not** be explained to the user; continue with Execution per [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md). Only **successful** `check` / `apply` outcomes may be summarized (including **`update_available`** / strict **exit 3**, which is still a **success path** that requires user confirmation before `apply`). **Do not** auto-download `update-skill.*` from the network. **Static reference** if `.ps1` is missing: canonical scripts live in [gate/gate-skills](https://github.com/gate/gate-skills) under `skills/<name>/scripts/` (same `<name>` as frontmatter).

---

## Step 0 — Wrapper routing probe

This legacy skill is a compatibility alias for the primary CLI skill
`gate-news-intel`.

Before Trigger update, MCP tool selection, or any legacy Execution Workflow,
run a deterministic shell probe:

```bash
PRIMARY_SKILL="gate-news-intel"
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
  `https://github.com/gate/gate-skills/blob/master/skills/gate-news-intel/SKILL.md`
  and its playbook contract. Carry over the minimum context: optional `symbol`
  for coin-filtered listing queries.
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
GATE_SKILL_CHECK_STRICT=1 bash "$HOME/.cursor/skills/gate-news-listing/scripts/update-skill.sh" check "gate-news-listing"
```

**PowerShell:**

```powershell
$env:GATE_SKILL_CHECK_STRICT = '1'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-news-listing\scripts\update-skill.ps1" check "gate-news-listing"
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
GATE_SKILL_CONFIRM_TOKEN="<paste from check stdout>" bash "$HOME/.cursor/skills/gate-news-listing/scripts/update-skill.sh" apply "gate-news-listing"
```

```bash
bash "$HOME/.cursor/skills/gate-news-listing/scripts/update-skill.sh" revoke-pending "gate-news-listing"
```

```powershell
$env:GATE_SKILL_CONFIRM_TOKEN = '<paste from check stdout>'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-news-listing\scripts\update-skill.ps1" apply "gate-news-listing"
```

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-news-listing\scripts\update-skill.ps1" revoke-pending "gate-news-listing"
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
| Gate-News | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- info_coin_get_coin_info
- info_coin_get_coin_rankings
- info_marketsnapshot_get_market_snapshot
- news_feed_get_exchange_announcements

### Authentication
- API Key Required: No
- Credentials Source: None; this skill uses read-only Gate Info / Gate News MCP access only.

### Installation Check
- Required: Gate-News
- Install: Use the local Gate MCP installation flow for the current host IDE before continuing.
- Continue only after the required Gate MCP server is available in the current environment.

## Routing Rules

Legacy path only — when Step 0 emitted `__ROUTE_CLI__`, routing is delegated to
`gate-news-intel`.

| User Intent | Keywords/Pattern | Action |
|-------------|-----------------|--------|
| Query exchange listings | "what did Binance list" "any new coins on Gate" "recent new listings" | Execute this Skill's full workflow |
| Query specific coin listing info | "where is SOL listed" "when was PEPE listed on Binance" | Execute this Skill (filter by coin) |
| Query delistings/maintenance | "any coins getting delisted" "exchange maintenance announcements" | Execute this Skill (filter by announcement type) |
| News briefing | "what happened recently" | Route to `gate-news-briefing` |
| Coin analysis | "how is this new coin doing" | Route to `gate-info-coinanalysis` |
| Contract security check | "is this new coin safe" | Route to `gate-info-riskcheck` |

---

## Execution Workflow

Legacy path only — this section applies when Step 0 emitted `__FALLBACK__`.

### Step 1: Intent Recognition & Parameter Extraction

Extract from user input:
- `exchange` (optional): Exchange name (e.g., Binance, Gate, OKX, Bybit, Coinbase)
- `coin` (optional): Specific coin symbol
- `announcement_type` (optional): Announcement type (listing / delisting / maintenance)
- `limit`: Number of results, default 10

**Default Logic**:
- If no exchange specified, query all exchanges
- If no announcement type specified, default to listing
- If user mentions "delisting" or "maintenance", set the corresponding `announcement_type`

### Step 2: Call Exchange Announcements Tool

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1 | `news_feed_get_exchange_announcements` | `exchange={exchange}, coin={coin}, announcement_type={announcement_type}, limit={limit}` | Announcement list: exchange, coin, type, time, details | — |

### Step 3: Supplement Key Coins with Data (Parallel)

From Step 2 results, extract the top 3-5 newly listed coins and supplement in parallel:

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 2a | `info_coin_get_coin_info` | `query={coin_symbol}` | Project fundamentals: sector, funding, description | Yes |
| 2b | `info_marketsnapshot_get_market_snapshot` | `symbol={coin_symbol}, timeframe="1d", source="spot"` | Market data: price, change, market cap, volume | Yes |

> Only supplement data for listing-type announcements. Delisting/maintenance announcements do not need market data.

### Step 4: LLM Aggregation — Generate Report

Pass announcement data and supplementary info to the LLM to generate the exchange activity report using the template below.

---

## Report Template

Legacy path only — this section applies when Step 0 emitted `__FALLBACK__`.

```markdown
## Exchange Activity Report

> Data range: {start_time} — {end_time} | Exchange: {exchange / "All"} | Type: {type / "Listings"}

### 1. Latest Listing Announcements

| # | Exchange | Coin | Type | Listing Time | Trading Pairs |
|---|---------|------|------|-------------|---------------|
| 1 | {exchange_1} | {coin_1} | Listed | {time_1} | {pairs_1} |
| 2 | {exchange_2} | {coin_2} | Listed | {time_2} | {pairs_2} |
| ... | ... | ... | ... | ... | ... |

### 2. Featured New Coins

{Quick analysis of the top 3-5 newly listed coins}

#### {coin_1}

| Metric | Value |
|--------|-------|
| Project Description | {description} |
| Sector | {category} |
| Funding Background | {funding} |
| Current Price | ${price} |
| Post-Listing Change | {change}% |
| 24h Volume | ${volume} |
| Market Cap | ${market_cap} |

{LLM one-liner: highlights and risks to watch for this project}

#### {coin_2}
...

### 3. Delisting / Maintenance Notices (if any)

| # | Exchange | Coin | Type | Effective Date | Notes |
|---|---------|------|------|---------------|-------|
| 1 | ... | ... | Delisted | ... | ... |

### 4. Activity Summary

{LLM generates a 2-3 sentence summary based on all announcement data:}
- Most active exchange for new listings recently
- Trending listing sectors (Meme / AI / DePIN / L2, etc.)
- Notable projects and why they stand out
- Delisting/maintenance reminders (if any)

### ⚠️ Risk Warnings

- Newly listed coins experience extreme volatility — the price discovery phase carries very high risk
- Some newly listed tokens may have insufficient liquidity — watch for slippage on large trades
- It is recommended to use the "Risk Assessment" feature to check contract security before trading

> The above information is compiled from public announcements and on-chain data and does not constitute investment advice.
```

---

## Decision Logic

| Condition | Assessment |
|-----------|------------|
| New coin 24h change > +100% post-listing | Flag "Abnormal surge — chasing the pump carries extreme risk" |
| New coin 24h change < -50% post-listing | Flag "Listed at a loss — buying now requires caution" |
| 24h volume < $100K | Flag "Extremely low volume — severe liquidity shortage" |
| Multiple exchanges list the same coin simultaneously | Flag "Multi-exchange simultaneous listing — high market attention" |
| Announcement type is delisting | Flag "Upcoming delisting — please handle positions promptly" |
| Announcement type is maintenance | Flag "Deposit/withdrawal maintenance in progress — transfers temporarily unavailable" |
| Coin fundamentals show no funding info | Flag "No funding information found — additional due diligence required" |
| Announcements return empty | Inform "No relevant announcements for this time period" |
| A supplementary Tool returns empty/error | Skip detailed analysis for that coin; mark "Data unavailable" |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| Misspelled exchange name | Attempt fuzzy match, e.g., "Binance" → Binance, "OKX" → OKX |
| No matching announcements | Inform "No {type} announcements for this exchange/time period." Suggest broadening the time range or switching exchanges |
| news_feed_get_exchange_announcements timeout | Return error message; suggest trying again later |
| Coin supplementary info (coin_info / market_snapshot) fails | Skip detailed analysis for that coin; display announcement info only |
| User asks when a coin will be listed (future) | Inform "Currently only published announcements can be queried — future listing plans cannot be predicted" |
| Too many results | Default to showing the most recent 10; inform the user they can specify an exchange or time range to narrow results |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "Analyze this new coin for me" | `gate-info-coinanalysis` |
| "Is this new coin's contract safe?" | `gate-info-riskcheck` |
| "Compare a few of these new listings" | `gate-info-coincompare` |
| "Why did this coin get listed on the exchange?" | `gate-news-eventexplain` |
| "How is the overall market right now?" | `gate-info-marketoverview` |
| "On-chain data for this new coin" | `gate-info-tokenonchain` |

---

## Available Tools & Degradation Notes

| PRD-Defined Tool | Actually Available Tool | Status | Degradation Strategy |
|-----------------|----------------------|--------|---------------------|
| `news_feed_get_exchange_announcements` | `news_feed_get_exchange_announcements` | ✅ Ready | — |
| `info_coin_get_coin_rankings` | — | ❌ Not ready | Cannot list recent listings by ranking — extract coins from announcements and query individually instead |
| `info_coin_get_coin_info` | `info_coin_get_coin_info` | ✅ Ready | — |
| `info_marketsnapshot_get_market_snapshot` | `info_marketsnapshot_get_market_snapshot` | ✅ Ready | — |

---

## Safety Rules

1. **No investment advice**: Announcement analysis is based on public information and must include a "not investment advice" disclaimer
2. **No listing predictions**: Do not predict whether a coin will be listed on a specific exchange
3. **New coin risk reminder**: All reports on newly listed coins must include the "extreme volatility during initial listing" risk warning
4. **Data transparency**: Label announcement source and update time
5. **Flag missing data**: When any dimension has no data, explicitly inform the user — never fabricate data
6. **Delisting urgency**: For delisting announcements, prominently remind users to manage their positions
