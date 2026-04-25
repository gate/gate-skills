# gate-info-risk — Scenarios & Prompt Examples

> Each row pins a concrete prompt to a playbook id and the expected behavior. When in doubt, load this file before picking the playbook.

## Scenario 1 — Token security check with contract + chain (English)

**Playbook**: `token_risk`

**Prompts**:
- "Is PEPE safe on eth"
- "Check honeypot risk on 0xdAC17F958D2ee523a2206206994597C13D831ec7 (ETH)"
- "Any issues with SHIB contract on bsc"

**Expected behavior**:
1. Extract `token` (symbol or contract address) + `chain`.
2. Run in parallel:
   - `gate-cli info compliance check-token-security --token {token} --chain {chain} --scope full --format json`
   - `gate-cli info coin get-coin-info --query {symbol_or_token} --chain {chain} --scope basic --format json` (optional, for context)
   - `gate-cli info onchain get-token-onchain --token {token} --chain {chain} --scope full --format json` (optional, for holder concentration + smart money)
3. Emit 5-section report. Apply verdict rules (see SKILL.md Decision thresholds).

## Scenario 2 — Token without chain (ask for chain)

**Playbook**: `token_risk`

**Prompts**:
- "Is this token safe"
- "Is PEPE safe"

**Expected behavior**:
1. Prompt: "Please specify the chain (e.g. eth, bsc, solana, base, arb, tron)". `check-token-security` requires `--chain`.
2. Do NOT call any command until `chain` is provided.

## Scenario 3 — Contract address + chain (Chinese)

**Playbook**: `token_risk`

**Prompts**:
- "Does contract 0x... on eth have risks"
- "Check if 0x... on bsc is a honeypot"

**Expected behavior**:
1. Same as Scenario 1 but `token` is taken verbatim as the contract address; do NOT attempt to infer a symbol unless `get-coin-info` returns one with non-null fields.
2. Report Section 3 (On-chain or Compliance Context) should include holder count, top-10 / top-100 ratios, and any on-chain labels.

## Scenario 4 — Address risk (scope-limited)

**Playbook**: `address_risk`

**Prompts**:
- "Is this address safe 0x..."
- "Will this address be blacklisted"
- "OFAC sanctioned?"

**Expected behavior**:
1. Extract `address` + `chain`. If chain missing, ask.
2. Run: `gate-cli info onchain get-address-info --address {address} --chain {chain} --scope basic --format json`.
3. Optional: `gate-cli info onchain get-address-transactions --address {address} --chain {chain} --time-range 30d --min-value-usd 100000 --limit 50 --format json`.
4. Derive verdict from `get-address-info.risk_labels` / `tags`:
   - Labels like `OFAC`, `sanctioned`, `mixer`, `scam`, `exchange-hack-proceeds`, `darknet` → `高风险`.
   - Labels like `heavy mixing`, `many interactions with scam` → `中风险`.
   - No labels at all + no tags → **`无法判定` (scope limited)**. Do NOT claim `低风险`.
5. Report MUST explicitly note: "gate-cli v0.5.2 does not ship `check-address-risk`; verdict is based on on-chain labels only. Retry when a dedicated address-risk command ships."

## Scenario 5 — Major coin (BTC / ETH) — guide to specify wrapped / meme

**Playbook**: `token_risk` — but gate the user first.

**Prompts**:
- "Is BTC safe"
- "Check ETH contract risk"

**Expected behavior**:
1. Inform the user: "Native assets like BTC / ETH have no contract-level risk. To check contract risks, specify a wrapped token (e.g. WBTC, stETH) or a Meme token on the target chain."
2. Do NOT call `check-token-security` for native BTC / ETH without a chain + contract.

## Scenario 6 — Project-level risk (events / compliance)

**Playbook**: `project_risk`

**Prompts**:
- "Does this project have recent compliance risks"
- "Has there been a security incident on Curve"
- "Did anything happen to LDO recently"

**Expected behavior**:
1. Extract `symbol`. Optional: `time_range` (default `7d`). Note: `get-latest-events --time-range` server enum is `1h|24h|7d` — for 30d windows fall back to `--start-time` / `--end-time` unix-ms.
2. Run in parallel:
   - `gate-cli news feed search-news --coin {symbol} --limit 10 --sort-by importance --time-range {time_range|7d} --format json`
   - `gate-cli news events get-latest-events --coin {symbol} --time-range {time_range|7d} --limit 20 --format json`
   - (optional) `gate-cli news feed get-exchange-announcements --coin {symbol} --limit 10 --format json`
3. Section 4 (Event Background) becomes the primary focus. Separate facts from community speculation (see [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md) rule 7).

## Anti-patterns

| User prompt | Do NOT route here |
|---|---|
| "Analyze PEPE" (no safety framing) | NOT `token_risk`. Route to ``gate-info-research``. |
| "Who is this address / smart money" | NOT `address_risk`. Route to ``gate-info-web3``. |
| "Why did SOL dump" | NOT `project_risk`. Route to ``gate-news-intel``. |
| "Please trade XXX" | Stop. Any trading intent is out of scope and violates safety rules. |

## Degradation rules

- **Required command fails** (`check-token-security` / `get-address-info` / `search-news`) → abort playbook, emit trimmed CLI error, do NOT emit a fake verdict.
- **Optional command fails** (`get-token-onchain`, `get-address-transactions`, `get-exchange-announcements`) → mark the corresponding section `scope limited`, lower confidence in Section 1.
- **Empty / no risk labels** on address — see Scenario 4 rule 4.
- **Preflight `MCP_FALLBACK`** — emit `__FALLBACK__`; a legacy wrapper handles it (not shipped this round).
