---
name: gate-info-risk
version: "2026.4.18-1"
updated: "2026-04-18"
description: "Use this skill whenever the user needs a risk- or safety-first check for a token, address, or project. Covers contract risk, address compliance labels, and project incidents via gate-cli. Triggers: is this coin safe, honeypot, sanctioned, compliance. Info primary; news auxiliary. Delegate: gate-info-research, gate-info-web3 (on-chain), gate-news-intel (events). v0.5.2; check-address-risk not shipped—use get-address-info; scope-limited if no labels."
---

# gate-info-risk

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
→ Also read [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) for **gate-info** and **gate-news** shared rules.
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

## CLI and playbook contract

1. Every CLI command MUST exist under `gate-cli v0.5.2`. This skill explicitly does NOT call `info compliance check-address-risk` (not shipped); address risk comes from `info onchain get-address-info`.
2. Call `gate-cli info …` / `gate-cli news …` only as listed in [playbooks/gate-info-risk.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-info-risk.yaml). When preflight `route` is `CLI`, do **not** call Gate MCP tools from this skill.
3. Missing data NEVER counts as "low risk". When the primary command for a chosen playbook is unavailable, the verdict is **UNABLE_TO_ASSESS** (scope limited; localized labels may appear in the user report) plus an explicit retry hint.
4. Always pass `--format json`. Required slots (`token`+`chain`, `address`+`chain`, `symbol`) must be present; if ambiguous, ask the user.
5. The report is safety-first: the verdict line comes BEFORE evidence, and high-severity items are always surfaced before medium or low.
6. No buy / sell advice. No price predictions. Use verdict bands **HIGH / MEDIUM / LOW / UNABLE_TO_ASSESS** in this skill’s logic; the final user report may localize those labels. Always include a **“what to verify next”** list.

---

## Step 0 — Preflight

Follow the shared contract in [skills/_shared/preflight.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/preflight.md) verbatim. Summary:

1. Run `gate-cli preflight --format json`; parse `.route`, `.status`, `.user_message`.
2. Branch: `CLI` → continue; `MCP_FALLBACK` → emit `__FALLBACK__` and halt; `BLOCK` → echo `user_message` and halt.
3. When `status == "ready_with_migration_warning"`, Step 3 appends one migrate hint at the very end of the report.

Do NOT run any data-collection command until Step 0 returns `route == "CLI"`.

---

<!--
Step 0.5 — Skill update check (OPT-IN, disabled by default).

The script [scripts/update-skill.sh](https://github.com/gate/gate-skills/blob/master/scripts/update-skill.sh) is shipped and functional, but agents
do NOT run it as part of the normal flow (zero overhead, no token needed).
Skill authors can still invoke it manually when they want to sync SKILL.md
from upstream:

    bash "$SKILL_ROOT/scripts/update-skill.sh" check gate-info-risk

Result semantics, strict-check mode (`GATE_SKILL_CHECK_STRICT=1`) and the
auto-apply path (`GATE_SKILL_UPDATE_MODE=auto`) are documented in
[skills/_shared/update-workflow.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/update-workflow.md). To re-enable
this step inside the agent flow, delete this HTML comment wrapper so the
block becomes part of the rendered SKILL.md again.
-->

---

## Step 1 — Intent routing

Pick exactly one playbook id from [playbooks/gate-info-risk.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-info-risk.yaml):

| Playbook id    | When to pick                                                                                              | Required slots              |
|----------------|-----------------------------------------------------------------------------------------------------------|-----------------------------|
| `token_risk`   | "is this token safe", "is there a honeypot", "taxes too high", "holder concentration" — subject is a token contract. | `token`, `chain` (the `token` slot accepts ticker OR contract address) |
| `address_risk` | "is this address safe", "sanctioned / OFAC", "blacklist", "is this wallet risky".                     | `address`, `chain`          |
| `project_risk` | "compliance or incident risk for this project", "has there been a security incident on {project}", "exchange announcement risk".       | `symbol`                    |

### Slot extraction rules

- `check-token-security` takes **exactly one** of `--token` or `--address` — the CLI explicitly rejects passing both (see the CLI error message; mutually exclusive). This skill always uses `--token` because the flag is polymorphic: it accepts BOTH tickers (`USDT`) and contract addresses (`0xdAC17F...`, SPL mints, TRX mints). **Agent slot-extraction rule**: when the user mentions a contract address for a token-risk query, store that address in the `token` slot directly — do NOT create a parallel `address` slot for this playbook. Always pair with `--chain`.
- `chain` canonical form (always **send** the short id on `--chain`): `eth`, `bsc`, `polygon`, `arb`, `op`, `base`, `avax`, `solana`, `tron`, ... Accept common long-form aliases from users (`ethereum`, `arbitrum`, `optimism`, `avalanche`, `bnb`, `matic`) and normalize to the short id before calling the CLI. Response `.chain` echo is **endpoint-dependent** — sometimes short (`eth`→`eth`), sometimes long (`arb`→`arbitrum`). Parsers MUST accept both alias forms; see [skills/gate-info-risk/references/troubleshooting.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-risk/references/troubleshooting.md) (canonical alias table for input normalization and response parsing).
- `address` is a wallet. If the user asks about a token contract but passed an address, confirm which they mean.
- `symbol` for `project_risk` is the listed coin ticker; resolve ambiguous project names before calling `news` commands.
- Missing or ambiguous required slot → STOP, ask the user. Do not guess.

### Cross-skill routing at Step 1

| User signal                                                                 | Route to                            |
|-----------------------------------------------------------------------------|-------------------------------------|
| "just give me a general analysis of this coin", no safety framing           | `gate-info-research`                |
| "who is this address / what is it doing on-chain" (not risk-first)          | `gate-info-web3` |
| "why did it drop" / "community view on incident"                            | `gate-news-intel` |

---

## Step 2 — Data collection

All commands use `--format json`. Commands inside the same `parallel_group` run concurrently.

### 2.A `token_risk`

Required:

- `gate-cli info compliance check-token-security --token {token} --chain {chain} --scope full`

Optional (run in parallel with the above):

- `gate-cli info coin get-coin-info --query {symbol_or_token} --chain {chain} --scope basic` — project fundamentals for context.
- `gate-cli info onchain get-token-onchain --token {token} --chain {chain} --scope full` — holder concentration, smart-money flow.

### 2.B `address_risk`

Required:

- `gate-cli info onchain get-address-info --address {address} --chain {chain} --scope basic` — risk labels, tags, scoped balance summary.

Optional:

- `gate-cli info onchain get-address-transactions --address {address} --chain {chain} --time-range 30d --min-value-usd 100000 --limit 50` — recent large flows; helps flag mixing / exchange hopping.

> **Scope-limited rule**: `gate-cli` v0.5.2 does not expose `info compliance check-address-risk`. If `get-address-info` returns no risk labels or tags, the final verdict MUST be **UNABLE_TO_ASSESS** (localized in user output) with a note to re-check once the dedicated address-risk command ships.

### 2.C `project_risk`

Required (run in parallel):

- `gate-cli news feed search-news --coin {symbol} --limit 10 --sort-by importance --time-range 7d`
- `gate-cli news events get-latest-events --coin {symbol} --time-range 7d --limit 20` (server enum is `1h|24h|7d` — use `--start-time` / `--end-time` unix-ms for longer windows)

Optional:

- `gate-cli news feed get-exchange-announcements --coin {symbol} --limit 10` — listing / delisting / maintenance / emergency notices.

### Failure policy

- Required command failure → abort playbook, surface CLI error verbatim (trim auth), stop. No verdict is emitted.
- Optional command failure → mark the corresponding section `scope limited` in Step 3 and downgrade confidence.
- Upstream returns "not found" or empty labels → treat as data gap, NOT as low risk.

---

## Step 3 — Synthesis

The report is always 5 sections, in this order:

### Report template

```markdown
## Risk assessment — {subject}

### 1. Verdict
- **Level**: {HIGH | MEDIUM | LOW | UNABLE_TO_ASSESS} (you may localize labels in the user-facing report)
- Three short sentences: main basis + data coverage + confidence (whether scope-limited)

### 2. Core risk items
Sort strictly HIGH → MEDIUM → LOW. Each item includes:
- Risk name + taxonomy: `TECHNICAL_CONTRACT` / `ADDRESS_COMPLIANCE` / `PROJECT_LEVEL`
- Evidence (real JSON paths), e.g. `check-token-security.high_risk_list[?risk_key=="is_honeypot"].risk_value == "1"`, `check-token-security.data_analysis.top10_percent`, `get-address-info.risk_labels`
- Impact + trigger (e.g. “tax rises after holding > 7 days”)

### 3. On-chain or compliance context
{Balances / tags / labels / large flows / holder concentration / fundamentals. Sources as hit by playbook:
`info onchain get-address-info`, `info onchain get-address-transactions`, `info onchain get-token-onchain`, `info coin get-coin-info`}

### 4. Event context (if any)
{Last 7–30d news / incidents / announcements from `news feed search-news`, `news events get-latest-events`, `news feed get-exchange-announcements`. Separate **sourced facts** from **community speculation** (mark “needs confirmation” where needed).}

If the playbook did not call news commands, mark **no data**; you may suggest `gate-news-intel` for follow-up.

### 5. What to verify next
- List concrete next commands to close each gap
- If **UNABLE_TO_ASSESS**, the first bullet must tell the user to re-run `check-token-security` / `get-address-info` with the correct `{chain}`
- No buy/sell advice; no price targets
```

### Verdict rules (applied in section 1)

`check-token-security` intentionally surfaces **two type conventions** — agents must not mix them:

- **Top-level flags** (e.g. `.is_honeypot`, `.is_open_source`) are **JSON booleans** (`true` / `false`). Compare with `== true` / `== false`, NOT with `"1"` / `"0"`.
- **Nested list entries** inside `high_risk_list[]`, `middle_risk_list[]`, `low_risk_list[]`, `risky_list[]`, `attention_list[]` have `.risk_value` as **strings** (`"0"` / `"1"`). Compare with `== "1"` or cast via `tonumber`.
- **Tax fields** (`.buy_tax`, `.sell_tax`, nested `.tax_analysis.token_tax.{buy_tax,sell_tax,transfer_tax}`) are **strings** (percent without `%`). Cast with `tonumber` before numeric comparison.
- **Percent fields** under `.data_analysis` (`.top10_percent`, `.top100_percent`, `.dev_holding_percent`, `.insider_percent`, `.max_holder_percent`) are **strings**. Cast before comparing.
- Each nested entry has shape `{risk_key, risk_value, risk_level, risk_name, risk_desc}`.

| Signal (real JSON path) | Effect on verdict |
|---|---|
| `high_risk_list[?risk_key=="is_honeypot"].risk_value == "1"` (equivalently top-level `is_honeypot == true` — top-level is **boolean**, not string) | **HIGH** (immediate) |
| `high_risk_list[?risk_key=="is_high_tax"].risk_value == "1"` OR `tonumber(buy_tax) > 10` OR `tonumber(sell_tax) > 10` | At least **HIGH** |
| `middle_risk_list[?risk_key=="owner_change_balance"].risk_value == "1"` (owner can rewrite any holder's balance) | **HIGH** (immediate) |
| `middle_risk_list[?risk_key=="can_take_back_ownership"].risk_value == "1"` OR `middle_risk_list[?risk_key=="hidden_owner"].risk_value == "1"` OR `middle_risk_list[?risk_key=="self_destruct"].risk_value == "1"` | **HIGH** (immediate) |
| `middle_risk_list[?risk_key=="is_mintable"].risk_value == "1"` OR `middle_risk_list[?risk_key=="is_proxy"].risk_value == "1"` OR `middle_risk_list[?risk_key=="is_blacklisted"].risk_value == "1"` | At least **MEDIUM** |
| `high_risk_list[?risk_key=="is_open_source"].risk_value == "0"` (equivalently top-level `is_open_source == false` — **boolean** at top level) | At least **MEDIUM** |
| `tonumber(data_analysis.top10_percent) > 70` (or top-level `top10_percent`) and no lock-up evidence | At least **MEDIUM** |
| `get-address-info.risk_labels` includes `OFAC` / `sanctioned` / `mixer` / `scam` / `exchange-hack-proceeds` / `darknet` | **HIGH** (immediate) |
| `get-address-info` returns `risk_labels=[]` AND `tags=[]` | **UNABLE_TO_ASSESS** (scope limited) — do not downgrade to **LOW** |
| `holders.holder_concentration[?label=="No.1-10"].percentage > 0.5` and active large turnover in 7d (`get-token-onchain`) | Add **MEDIUM** item |
| `latest-events` has `event_type == "exploit" / "rug" / "depeg"` and `create_time` ≤ 7d | Add **MEDIUM** or **HIGH** (by severity) |
| All required commands fail | **UNABLE_TO_ASSESS** + clear retry guidance |

Optional summary shortcut: `check-token-security.risk_summary.highest_risk_level` — an aggregate `0–3` severity score from upstream (3 = honeypot-grade). When `highest_risk_level >= 3` without any flagged `risk_key`, still run through the rules above to cite the specific offending field rather than citing `risk_summary` alone.

### Migrate hint (only when Step 0 status was `ready_with_migration_warning`)

At the end of the report, append **verbatim** the migration blockquote line from [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md) (line starting with `⚙️` and `gate-cli migrate --dry-run`).

Never gate the verdict on migrate status.

---

## Cross-skill routing + Safety rules

### Routing

Follow the shared matrix in [skills/_shared/routing.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/routing.md). Risk-skill-specific follow-ups:

| Follow-up intent                                  | Target                                                           |
|---------------------------------------------------|------------------------------------------------------------------|
| "full research" / "is it worth following"                      | `gate-info-research`                   |
| "what is this address doing" / "smart money behavior"         | `gate-info-web3`                             |
| "why it dropped" / "community take on the event"                    | `gate-news-intel`                          |
| User changes chain or token and wants a new assessment                       | Re-enter the same playbook with new slots; do NOT reuse prior verdict. |

### Safety rules

Follow the shared contract in [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md). Risk-specific hardening:

1. Never say **LOW** when a required command failed or when no risk labels / security-check fields were returned; use **UNABLE_TO_ASSESS** (or localized equivalent).
2. Keep the three risk taxonomies (`TECHNICAL_CONTRACT` / `ADDRESS_COMPLIANCE` / `PROJECT_LEVEL`) strictly separate in Section 2.
3. **HIGH** items MUST appear before any **MEDIUM** or **LOW** items in Section 2.
4. No buy / sell advice. The closest allowed phrasing is “avoid / verify further” (neutral, non-prescriptive).
5. Cite the exact JSON path for every verdict-driving claim, e.g. `info compliance check-token-security.high_risk_list[?risk_key=="is_honeypot"].risk_value` or `info compliance check-token-security.data_analysis.top10_percent` — never cite a command-only hand-wave like "from check-token-security".

---

## References

| File | Load when... |
|---|---|
| [skills/gate-info-risk/references/scenarios.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-risk/references/scenarios.md) | Picking a playbook id is not obvious, or the user's prompt looks like Scenarios 4 / 5 (address risk, major-coin ambiguity). |
| [skills/gate-info-risk/references/cli-reference.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-risk/references/cli-reference.md) | You need the full flag table for `check-token-security`, `get-address-info`, `get-token-onchain`, or the auxiliary news commands. |
| [skills/gate-info-risk/references/troubleshooting.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-risk/references/troubleshooting.md) | A command failed, or `get-address-info` came back with no risk labels (the `check-address-risk` gap). |
| [skills/_shared/preflight.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/preflight.md) | Step 0 contract. |
| [skills/_shared/routing.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/routing.md) | Cross-skill routing. |
| [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md) | Safety + reporting rules. |
| [skills/_shared/update-workflow.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/update-workflow.md) | Skill update workflow. |
