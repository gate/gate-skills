---
name: gate-info-web3
version: "2026.4.20-1"
updated: "2026-04-20"
description: "Use this skill whenever the user’s main ask is on-chain, protocol, or Web3 behavior (not a pure safety verdict). Covers address and token on-chain analysis, platform metrics, reserves, heatmaps, stablecoins, bridges; optional news/UGC. Legacy alias: gate-info-defianalysis. Delegate: gate-info-risk (safety), gate-info-research (broad research), gate-news-intel (events/sentiment). gate-cli v0.5.2; use playbook commands, not unshipped +shortcuts."
---

# gate-info-web3

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
→ Also read [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) for **gate-info** and **gate-news** shared rules (tool degradation, report standards, security, routing).
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

## CLI and playbook contract

1. **Scope naming**: Frame answers as **Web3 / on-chain / protocol behavior**. Do **not** narrow the narrative to “DeFi-only” unless the user’s question is strictly DeFi/TVL/yield. `gate-info-defianalysis` is a **legacy alias** for routing only — the canonical skill id is `gate-info-web3`.
2. Every CLI command MUST exist under **`gate-cli v0.5.2`**. Call only what appears in [playbooks/gate-info-web3.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-info-web3.yaml). When preflight `route` is `CLI`, do **not** invoke Gate MCP tools from this skill.
3. Always pass **`--format json`** on data-collection commands.
4. **Separate evidence types** in the report: label **on-chain / CLI facts** vs **community or media interpretation** (news, web search, UGC). Never present rumor as chain truth.
5. Required slots (`address`+`chain`, `token`+`chain`, `platform`, `exchange`+`asset`, `symbol`, `entity_query`) must be explicit; if ambiguous, ask — do not guess chain or contract.
6. Final user-facing reports may use the user’s locale; this `SKILL.md` stays English for discovery (see repository `CLAUDE.md` rule 1).

---

## Step 0 — Preflight

Follow [skills/_shared/preflight.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/preflight.md) verbatim:

1. Run `gate-cli preflight --format json`; parse `.route`, `.status`, `.user_message`.
2. Branch: `CLI` → continue; `MCP_FALLBACK` → emit `__FALLBACK__` and halt; `BLOCK` → echo `user_message` and halt.
3. When `status == "ready_with_migration_warning"`, Step 3 appends one migrate hint at the end of the report.

Do NOT run any `info` / `news` data call until `route == "CLI"`.

---

<!--
Step 0.5 — Skill update check (OPT-IN, disabled by default). See [skills/_shared/update-workflow.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/update-workflow.md).
-->

---

## Step 1 — Intent routing

Map the user query to **exactly one** playbook id from [playbooks/gate-info-web3.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-info-web3.yaml).

| Playbook id | When to pick | Required slots |
|-------------|----------------|----------------|
| `address_tracking` | Trace a wallet / “who is this address” / recent on-chain activity (behavior, not safety verdict). | `address`, `chain` |
| `token_onchain` | Token-level flow / holders / smart-money style signals for a **known token + chain**. | `token`, `chain` |
| `entity_intel` | Named desk / fund / entity (e.g. what a named desk is doing). | `entity_query` |
| `protocol_platform` | Protocol TVL, fees, volume, profile, history, or yield on a **named platform** (e.g. Uniswap, Aave). | `platform` |
| `exchange_reserves` | Exchange reserve / proof-of-reserves style questions for an asset. | `exchange`, `asset` |
| `liquidation_heatmap` | Perp / futures liquidation density by price (which price levels see liquidations). | `symbol` |
| `stablecoin_bridge` | Stablecoin market / peg / chain distribution, or bridge rankings — not a single-token DEX question. | — |
| `token_onchain_social` | User wants **on-chain data plus** news/sentiment/UGC in one pass. | `token`, `chain` |

### Slot extraction notes

- **`chain`**: normalize to ids the CLI accepts (`eth`, `bsc`, `arbitrum`, `base`, `solana`, ...). If missing, ask.
- **`platform`**: accept fuzzy names; if multiple matches are plausible, run `gate-cli info platformmetrics search-platforms` **only with flags verified in `gate-cli info platformmetrics search-platforms --help`**, pick one slug, then run `get-defi-overview` / `get-platform-info` / `get-yield-pools` as the playbook lists.
- **`token` vs `symbol`**: on-chain playbooks use `token` (+ `chain`); reserves / heatmap often use listed **`symbol`** (e.g. `BTC`, `USDC`).

### Cross-skill routing at Step 1

| User signal | Route to |
|-------------|----------|
| Safety / honeypot / blacklist / compliance **verdict** (safety-first) | `gate-info-risk` (primary) |
| General research, fundamentals, macro, multi-coin compare **without** on-chain/protocol framing | `gate-info-research` (primary) |
| Pure “why did it move”, “community narrative”, **no** on-chain ask | `gate-news-intel` (primary) |

---

## Step 2 — Data collection

Execute the chosen playbook. Commands in the same `parallel_group` may run concurrently; wait for the group before the next. **Only** use commands defined in the playbook YAML (plus the optional `search-platforms` pre-check for fuzzy `platform` names when Step 1 says so).

### Execution substitutes (v0.5.2)

- **`info +address-tracker` / `info +token-onchain`**: **not** relied upon. Use the **`address_tracking`** and **`token_onchain`** command blocks in the YAML (see `cli_future_shortcut` there for aspirational one-liners).
- **`info onchain trace-fund-flow`** and **`info onchain get-entity-profile`**: **not** in the v0.5.2 inventory documented in `docs/gate-cli-commands-summary.md`. Use **`get-address-info` + `get-address-transactions`** for flows; use **`news feed web-search`** for entity-style questions until `get-entity-profile` exists.
- **News aggregates (`news +brief`, `news +community-scan`)**: use **`search-news`**, **`get-social-sentiment`**, **`search-ugc`** as in `token_onchain_social`.

### Failure policy

- Required command fails → abort, surface CLI error, no fabricated section.
- Optional command fails → mark the matching subsection as **no data** in Step 3.
- News/web search may be partial or opinion-heavy — tag those lines as **community / media**, not as on-chain facts.

---

## Step 3 — Synthesis

Produce **exactly six sections**, in this order (section titles in the final user report may be localized; structure is fixed):

### Report template

```markdown
## Web3 intel — {subject}

### 1. Subject and executive takeaways
- Objects (address / token / protocol / exchange / entity / theme)
- 1–3 neutral bullets; separate **on-chain verifiable** vs **needs confirmation**

### 2. On-chain activity (core)
- Recent interaction types, large transfers, label-based identity hints — **only** from on-chain / `info onchain` commands

### 3. Flows, positioning, smart money, entity read
- Flow and holder / positioning structure (`get-address-transactions`, `get-token-onchain`)
- Smart-money or whale-style signals (from token-onchain data)
- Entity questions: if `web-search` is used, mark as **second-hand** narrative

### 4. Protocol or platform metrics (if relevant)
- Scale (TVL, volume, fees), direction of change, pools or assets that matter (`platformmetrics` commands)

### 5. Community or news context (if relevant)
- Only when the playbook includes news / web-search: short factual + tone summary; **keep separate** from sections 2–3

### 6. Risks and watchlist
- Data gaps, follow-up on-chain signals, **non-advice** watch items

> This report is based on public data and tool output; it is not investment advice.
```

### Migrate hint (only if Step 0 had `ready_with_migration_warning`)

Append **verbatim** the migration blockquote line from [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md) (the line starting with `⚙️` and `gate-cli migrate --dry-run`), same as other primary skills.

---

## Cross-skill routing + Safety rules

### Routing

Follow [skills/_shared/routing.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/routing.md). Web3-specific reminders:

| Follow-up intent | Target |
|------------------|--------|
| “Is it safe / honeypot / sanctioned?” | `gate-info-risk` (primary) |
| “Full research report / worth buying?” (no on-chain focus) | `gate-info-research` (primary) |
| “Why pump/dump / Twitter drama only” | `gate-news-intel` (primary) |

### Safety rules

Follow [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md). Web3-specific:

1. No buy/sell recommendations; no price targets.
2. Do not treat **empty** on-chain data as proof of safety — that belongs in **risk** skill.
3. When **web-search** or **UGC** is used, prefix interpretive lines with **media / community** so they are not confused with chain state.

---

## References

| File | Load when... |
|------|----------------|
| [skills/gate-info-web3/references/scenarios.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-web3/references/scenarios.md) | Choosing among address / token / protocol / reserves / heatmap playbooks. |
| [skills/gate-info-web3/references/cli-reference.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-web3/references/cli-reference.md) | Flag tables and verified `platformmetrics` / `onchain` / `news` flags. |
| [skills/gate-info-web3/references/troubleshooting.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-web3/references/troubleshooting.md) | Shortcut gaps, `search-platforms` discovery, optional `get-transaction` for a pasted tx hash. |
| [skills/_shared/preflight.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/preflight.md) | Step 0. |
| [skills/_shared/routing.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/routing.md) | Cross-skill matrix. |
| [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md) | Shared report rules. |
