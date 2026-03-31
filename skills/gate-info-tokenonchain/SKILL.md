---
name: gate-info-tokenonchain
version: "2026.3.30-5"
updated: "2026-03-30"
description: "Token on-chain analysis via Gate-Info MCP: holder distribution, on-chain activity, and large or unusual transfers (scopes holders / activity / transfers). Smart Money is not available in this version. Triggers include ETH on-chain analysis, BTC holder distribution, whale movements, large transfers. Route single-address tracking to gate-info-addresstracker. Tools: info_onchain_get_token_onchain, info_coin_get_coin_info."
---

# gate-info-tokenonchain

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
→ Also read [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) for **gate-info** / **gate-news**-specific rules (tool degradation, report standards, security, routing degradation, and per-skill version checks when `scripts/` is present).
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

> Token On-Chain Analysis Skill (current version: **no Smart Money**). For token-level holder distribution, activity, and large transfers, call on-chain + basic coin info tools in parallel, then aggregate into a structured report.

**Trigger Scenarios**: User asks about token on-chain data, holder distribution, on-chain activity, large transfers, on-chain chip analysis, etc.

**Per-skill updates:** This directory includes `scripts/update-skill.sh` and `scripts/update-skill.ps1`. Policy: [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) §1. The **Trigger update** steps below apply in addition to [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md); when scripts are present, use this flow for version checks before execution.

---

## Trigger update (with Execution)

**Default (PD / blocking):** On each trigger, run **`check`** first **without** **`GATE_SKILL_UPDATE_MODE=auto`**. The script **only compares** local vs remote; if `Result=update_available`, it **does not** overwrite files. **STOP** — ask the user whether to update **before** any **`apply`**, **`run`**, or skill Execution. In sandboxes (e.g. Cursor), use **full / all permissions** when later running **`apply`**. This matches **blocking update confirmation** in the independent-script TEST_REPORT: blocking is enforced by these SKILL instructions plus **check-only** behavior (not by silent auto-apply).

**Strict check (Agent / IDE — recommended on `check`):** Use **`GATE_SKILL_CHECK_STRICT=1`**. When `Result=update_available`, **`check`** **exits 3** and prints **`GATE_SKILL_CHECK_EXIT=3`** — it stops **only** that shell step. **Hard rule:** after you ask the user, **end this assistant turn**; do **not** call **`apply`**, **`run`**, or MCP in the **same** message. **`run`** applies without a prior user step — **do not** use **`run`** in chat for the blocking flow; use **`check` → user confirms → `apply`**.

### Step 1 — Check

**Install root:** `check` / `apply` read **`$DEST/SKILL.md`**. Typical **`$SKILL_ROOT`**: **`$HOME/.cursor/skills/<name>/`**, **`$HOME/.codex/skills/<name>/`**, **`$HOME/.openclaw/skills/<name>/`**, **`$HOME/.agents/skills/<name>/`**, **`$HOME/.gemini/antigravity/skills/<name>/`**. Single-arg: the script resolves **`DEST`** in that order when **`SKILL.md`** exists; otherwise **`DEST`** is `scripts/../`. Workspace-only trees need two-arg **`check`** / **`apply`** with explicit **`DEST`**.

**Bash** (blocking — no auto; example Cursor):

```bash
GATE_SKILL_CHECK_STRICT=1 bash "$HOME/.cursor/skills/gate-info-tokenonchain/scripts/update-skill.sh" check "gate-info-tokenonchain"
```

**PowerShell:**

```powershell
$env:GATE_SKILL_CHECK_STRICT = '1'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-tokenonchain\scripts\update-skill.ps1" check "gate-info-tokenonchain"
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
GATE_SKILL_CONFIRM_TOKEN="<paste from check stdout>" bash "$HOME/.cursor/skills/gate-info-tokenonchain/scripts/update-skill.sh" apply "gate-info-tokenonchain"
```

```bash
bash "$HOME/.cursor/skills/gate-info-tokenonchain/scripts/update-skill.sh" revoke-pending "gate-info-tokenonchain"
```

```powershell
$env:GATE_SKILL_CONFIRM_TOKEN = '<paste from check stdout>'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-tokenonchain\scripts\update-skill.ps1" apply "gate-info-tokenonchain"
```

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-tokenonchain\scripts\update-skill.ps1" revoke-pending "gate-info-tokenonchain"
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

- **Smart Money**: `info_onchain_get_smart_money` and `scope=smart_money` for `info_onchain_get_token_onchain` are **not** available in this version. Inform users and use holders / activity / transfers only.
- **Entity profiling**: `info_onchain_get_entity_profile` — whale entity profiling not supported until tool is available.
- On-chain data coverage depends on upstream chain support (e.g., BlockInfo).

---

## MCP Dependencies

### Required MCP Servers

| MCP Server | Status |
|------------|--------|
| Gate-Info | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- info_onchain_get_token_onchain
- info_coin_get_coin_info

### Authentication
- API Key Required: No

### Installation Check
- Required: Gate-Info
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursorinstaller`
  - Codex: `gate-mcp-codexinstaller`
  - Claude: `gate-mcp-claudeinstaller`
  - OpenClaw: `gate-mcp-openclawinstaller`

## Routing Rules

| User Intent | Keywords | Action |
|-------------|----------|--------|
| Token holder distribution | "ETH holders" "BTC holding distribution" "top holders" | Execute with `scope=holders` |
| On-chain activity | "on-chain activity" "active addresses" "transaction count" | Execute with `scope=activity` |
| Large transfers | "large transfers" "whale movements" "unusual transfers" | Execute with `scope=transfers` |
| Full on-chain overview | "on-chain analysis for SOL" "ETH on-chain data" | Execute with `holders,activity,transfers` |
| Smart Money (not yet supported) | "smart money buying" | Inform user; run available scopes only |
| Specific address query | "track this address 0x..." | Route to `gate-info-addresstracker` |
| Coin fundamentals | "analyze SOL" | Route to `gate-info-coinanalysis` |
| Whale entity tracking | "what is Jump Trading doing" | Route to `gate-info-whaletracker` if available, else inform |

---

## Execution Workflow

### Step 0: Multi-Dimension Intent Check

- Token-level on-chain → this Skill.
- Specific address (not token) → `gate-info-addresstracker`.
- Fundamentals + technicals + news together → `gate-info-research` (if available).

### Step 1: Intent Recognition & Parameter Extraction

- `symbol` (required): Token ticker (e.g., BTC, ETH, SOL)
- `chain` (optional): e.g., eth, sol, bsc
- `scope`: one or more of `holders`, `activity`, `transfers` (`smart_money` — not available)
- `time_range` (optional): default 24h for transfers/activity

### Step 2: Call MCP Tools in Parallel

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `info_onchain_get_token_onchain` | `symbol, chain, scope, time_range` | Holder / activity / transfer data per scope | Yes |
| 1b | `info_coin_get_coin_info` | `query={symbol}, scope="basic"` | Basic coin context | Yes |

### Step 3: LLM Aggregation

- Contextualize on-chain data with coin info
- Identify patterns and anomalies
- Avoid speculative price predictions

---

## Report Template

```markdown
## {symbol} On-Chain Analysis

> Generated: {timestamp} | Chain: {chain or "All supported chains"}
> Note: Smart Money analysis not yet available in this version.

### Token Overview

| Metric | Value |
|--------|-------|
| Token | {symbol} ({name}) |
| Market Cap | ${market_cap} |
| Circulating Supply | {circulating_supply} |

### Holder Distribution (if scope includes holders)

{Tables + LLM concentration assessment}

### On-Chain Activity (if scope includes activity)

{Metrics + LLM trend assessment}

### Large Transfers (if scope includes transfers)

{Table + LLM flow assessment}

### On-Chain Health Score

{Dimensions scored /10 + overall}

### Key Insights

{2–3 data-driven bullets}

> On-chain data does not predict future prices. This does not constitute investment advice.
```

---

## Decision Logic

| Condition | Assessment |
|-----------|------------|
| Top 10 holder concentration > 70% | High concentration risk |
| Top 10 holder concentration < 30% | Well-distributed holder base |
| Active addresses declining > 20% WoW | Declining network activity |
| Active addresses growing > 30% WoW | Strong activity growth |
| Large transfers to exchange addresses | Potential sell pressure |
| Large transfers from exchange addresses | Potential accumulation |
| User asks about Smart Money | State not available; offer holders/activity/transfers |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| Token not found on-chain | Check via `info_coin_get_coin_info`; suggest symbol/chain |
| `info_onchain_get_token_onchain` fails | Show coin info only; note on-chain unavailable |
| `info_coin_get_coin_info` fails | Show on-chain data without market context |
| Scope returns empty | Skip section; note no data for scope |
| Chain not supported | List supported chains; ask user |
| Both Tools fail | Return error; suggest retry later |
| User requests `smart_money` | Inform not available; offer other scopes |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "Analyze this coin" | `gate-info-coinanalysis` |
| "Track this address" | `gate-info-addresstracker` |
| "Is this token safe?" | `gate-info-riskcheck` |
| "Technical analysis?" | `gate-info-trendanalysis` |
| "Any news?" | `gate-news-briefing` |
| "What does the community think?" | `gate-news-communityscan` |
| "DeFi data for this?" | `gate-info-defianalysis` |

---

## Safety Rules

1. **No fabricated on-chain data**: Only report MCP-returned data.
2. **Address privacy**: Shorten addresses (e.g., `0x1234…abcd`); do not doxx.
3. **No trading signals**: Informational only; not buy/sell advice.
4. **Exchange labels**: Best-effort; may be mislabeled.
5. **Data lag**: Note indexing delays where relevant.
6. **Smart Money**: Clearly state unavailability rather than approximating.
