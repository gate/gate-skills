---
name: gate-info-tokenonchain
version: "2026.4.7-1"
updated: "2026-04-07"
description: "Token on-chain analysis via Gate-Info MCP: holder distribution, on-chain activity, and large or unusual transfers (scopes holders / activity / transfers). Smart Money is not available in this version. Triggers include ETH on-chain analysis, BTC holder distribution, whale movements, large transfers. Route single-address tracking to gate-info-addresstracker. Tools: info_onchain_get_token_onchain, info_coin_get_coin_info."
required_credentials: []
required_env_vars: []
required_permissions: []
---

# gate-info-tokenonchain

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read `./references/gate-runtime-rules.md`
→ Also read `./references/info-news-runtime-rules.md` for gate-info / gate-news shared rules (tool degradation, report standards, security, and output standards).
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

> Token On-Chain Analysis Skill (current version: **no Smart Money**). For token-level holder distribution, activity, and large transfers, call on-chain + basic coin info tools in parallel, then aggregate into a structured report.

**Trigger Scenarios**: User asks about token on-chain data, holder distribution, on-chain activity, large transfers, on-chain chip analysis, etc.

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
- Credentials Source: None; this skill uses read-only Gate Info / Gate News MCP access only.

### Installation Check
- Required: Gate-Info
- Install: Use the local Gate MCP installation flow for the current host IDE before continuing.
- Continue only after the required Gate MCP server is available in the current environment.

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
2. **Address privacy**: Shorten addresses (e.g., `0x1234...abcd`); do not doxx.
3. **No trading signals**: Informational only; not buy/sell advice.
4. **Exchange labels**: Best-effort; may be mislabeled.
5. **Data lag**: Note indexing delays where relevant.
6. **Smart Money**: Clearly state unavailability rather than approximating.
7. **Age & eligibility**: Intended for users **aged 18 or above** with **full civil capacity** in their jurisdiction.
8. **Data flow**: The host agent processes user prompts; this skill directs **read-only** **Gate-Info** MCP tools listed above. The LLM summarizes tool output. This skill does not invoke additional third-party data services.
