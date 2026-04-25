---
name: gate-info-addresstracker
version: "2026.4.3-1"
updated: "2026-04-03"
description: "Address tracker and analysis. Use this skill whenever the user provides an on-chain address or asks to track or query an address. Trigger phrases include: track this address, who owns this address, fund flow, check address. MCP tools: info_onchain_get_address_info, info_onchain_get_address_transactions, info_onchain_trace_fund_flow."
required_credentials: []
required_env_vars: []
required_permissions: []
---

# gate-info-addresstracker

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
→ Also read [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) for **gate-info** / **gate-news**-specific rules (tool degradation, report standards, security, routing degradation, per-skill version checks when `scripts/` is present, and legacy wrapper routing).
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.
- **Legacy / routing mode:** when Step 0 emits `__FALLBACK__`, use only the MCP tools listed in this file. When Step 0 emits `__ROUTE_CLI__`, do **not** call those MCP tools; delegate to the mapped primary skill per Step 0.

> The on-chain detective Skill. The user inputs an on-chain address; the system first calls the address info Tool to get the profile, then based on user intent depth (simple query vs. fund tracing) decides whether to additionally call transaction history and fund flow tracing Tools.

**Trigger Scenarios**: User provides an on-chain address (0x... / bc1... / T... format) or explicitly expresses intent to track/query an address.

**Per-skill updates:** This directory includes `scripts/update-skill.sh` and may include `scripts/update-skill.ps1`. **ClawHub** packages uploaded to the marketplace often omit `update-skill.ps1` (upload-page restriction); **GitHub / Bitbucket** source trees keep both. Policy: [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) §1. The **Trigger update** steps below apply in addition to [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md); when scripts are present, use this flow for version checks before execution.

**Update check — user visibility:** Technical failures during version check (missing script, sandbox, network, non-zero exit, no parseable `Result=` line) must **not** be explained to the user; continue with Execution per [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md). Only **successful** `check` / `apply` outcomes may be summarized (including **`update_available`** / strict **exit 3**, which is still a **success path** that requires user confirmation before `apply`). **Do not** auto-download `update-skill.*` from the network. **Static reference** if `.ps1` is missing: canonical scripts live in [gate/gate-skills](https://github.com/gate/gate-skills) under `skills/<name>/scripts/` (same `<name>` as frontmatter).

---

## Step 0 — Wrapper routing probe

This legacy skill is a compatibility alias for the primary CLI skill
`gate-info-web3`.

Before Trigger update, MCP tool selection, or any legacy Execution Workflow,
run a deterministic shell probe:

```bash
PRIMARY_SKILL="gate-info-web3"
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
  `https://github.com/gate/gate-skills/blob/master/skills/gate-info-web3/SKILL.md`
  and its playbook contract. Carry over the minimum context: `address` and
  `chain`.
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
GATE_SKILL_CHECK_STRICT=1 bash "$HOME/.cursor/skills/gate-info-addresstracker/scripts/update-skill.sh" check "gate-info-addresstracker"
```

**PowerShell:**

```powershell
$env:GATE_SKILL_CHECK_STRICT = '1'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-addresstracker\scripts\update-skill.ps1" check "gate-info-addresstracker"
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
GATE_SKILL_CONFIRM_TOKEN="<paste from check stdout>" bash "$HOME/.cursor/skills/gate-info-addresstracker/scripts/update-skill.sh" apply "gate-info-addresstracker"
```

```bash
bash "$HOME/.cursor/skills/gate-info-addresstracker/scripts/update-skill.sh" revoke-pending "gate-info-addresstracker"
```

```powershell
$env:GATE_SKILL_CONFIRM_TOKEN = '<paste from check stdout>'
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-addresstracker\scripts\update-skill.ps1" apply "gate-info-addresstracker"
```

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\gate-info-addresstracker\scripts\update-skill.ps1" revoke-pending "gate-info-addresstracker"
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

- info_onchain_get_address_info
- info_onchain_get_address_transactions
- info_onchain_get_transaction
- info_onchain_trace_fund_flow

### Authentication
- API Key Required: No
- Credentials Source: None; this skill uses read-only Gate Info / Gate News MCP access only.

### Installation Check
- Required: Gate-Info
- Install: Use the local Gate MCP installation flow for the current host IDE before continuing.
- Continue only after the required Gate MCP server is available in the current environment.

## Routing Rules

Legacy path only — when Step 0 emitted `__ROUTE_CLI__`, routing is delegated to
`gate-info-web3`.

| User Intent | Keywords/Pattern | Action |
|-------------|-----------------|--------|
| Query address info | "who owns this address" "check 0x..." | Execute this Skill (Basic Mode) |
| Track fund flow | "track" "fund flow" "where did this money go" | Execute this Skill (Deep Tracking Mode) |
| Token on-chain analysis | "ETH chip analysis" "what are smart money buying" | Route to `gate-info-tokenonchain` |
| Address risk check | "is this address safe" "is this a blacklisted address" | Route to `gate-info-riskcheck` |
| Single transaction query | "what is this transaction" "decode this tx" | Call `info_onchain_get_transaction` directly |
| Entity/institution tracking | "Jump Trading holdings" "this institution's address" | Route to `gate-info-whaletracker` |

---

## Execution Workflow

Legacy path only — this section applies when Step 0 emitted `__FALLBACK__`.

### Step 1: Intent Recognition & Parameter Extraction

Extract from user input:
- `address`: On-chain address (auto-detect format)
- `chain` (optional): Chain type (ETH/BSC/TRX/BTC, etc. — can be auto-inferred from address format)
- `intent_depth`: User intent depth
  - `basic` — just asking "who is this" / "how much do they hold"
  - `deep` — requesting "track funds" / "show transactions" / "where did the money go"

**Automatic Address Format Detection**:

| Address Prefix | Inferred Chain |
|---------------|----------------|
| `0x` | Ethereum (default; could also be BSC/Polygon/Arbitrum or other EVM chains) |
| `bc1` / `1` / `3` | Bitcoin |
| `T` | Tron |
| Other | Prompt user to specify the chain |

### Step 2: Phase 1 — Address Profile (Required)

| Step | MCP Tool | Parameters | Retrieved Data |
|------|----------|------------|----------------|
| 1 | `info_onchain_get_address_info` | `address={address}, chain={chain}, scope="with_defi"` | Address profile: balance, labels, risk score, DeFi positions, PnL |

### Step 3: Decision Branch

```
get_address_info response
    │
    ├── User only wants a simple query (intent_depth = basic)
    │   └── → Output address profile report directly (skip to Step 5)
    │
    └── User requests deep tracking (intent_depth = deep)
        └── → Proceed to Step 4 parallel calls
```

**Conditions for automatic upgrade to deep mode**:
- Address has known labels (e.g., exchange, hacker, whale) → likely worth investigating
- Address balance > $1M
- Address has risk flags

### Step 4: Phase 2 — Deep Tracking (Conditionally Triggered)

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 2a | `info_onchain_get_address_transactions` | `address={address}, chain={chain}, min_value_usd=10000, limit=20` | Large transactions (> $10k) | Yes |
| 2b | `info_onchain_trace_fund_flow` | `start_address={address}, chain={chain}, depth=3, min_value_usd=100000` | Fund flow tracing (3-level depth, > $100k) | Yes |

> Both Tools called in parallel. `min_value_usd` thresholds are adaptively adjusted based on address size.

**Adaptive Threshold Logic**:

| Address Total Balance | `info_onchain_get_address_transactions` min_value | `info_onchain_trace_fund_flow` min_value |
|----------------------|--------------------------------------------------|-----------------------------------------|
| < $100K | $1,000 | $10,000 |
| $100K – $1M | $10,000 | $100,000 |
| $1M – $100M | $100,000 | $1,000,000 |
| > $100M | $1,000,000 | $10,000,000 |

### Step 5: LLM Aggregation

---

## Report Template

Legacy path only — this section applies when Step 0 emitted `__FALLBACK__`.

### Basic Mode

```markdown
## Address Analysis Report

> Address: `{address}`
> Chain: {chain}
> Query time: {timestamp}

### 1. Address Profile

| Metric | Value |
|--------|-------|
| Address Label | {label} (e.g., Exchange Hot Wallet / Whale / Unknown / Hacker-linked) |
| Risk Score | {risk_score}/100 ({Low Risk/Medium Risk/High Risk}) |
| First Transaction | {first_tx_time} |
| Total Transactions | {tx_count} |
| Current Balance | ${total_balance_usd} |

### 2. Asset Holdings

| Token | Amount | Value (USD) | Share |
|-------|--------|-------------|-------|
| {token_1} | {amount} | ${value} | {pct}% |
| {token_2} | ... | ... | ... |
| ... | ... | ... | ... |

**Holding Characteristics**: {LLM analyzes the holding structure, e.g., "Highly concentrated in ETH", "Diversified across multiple DeFi tokens", "Possible market maker"}

### 3. DeFi Positions (if available)

| Protocol | Type | Amount | Status |
|----------|------|--------|--------|
| {protocol} | {Lending/LP/Staking} | ${value} | {Healthy/Near Liquidation} |
| ... | ... | ... | ... |

### 4. PnL Summary (if available)

| Metric | Value |
|--------|-------|
| Realized PnL | ${realized_pnl} |
| Unrealized PnL | ${unrealized_pnl} |
| Win Rate | {win_rate}% |
```

### Deep Tracking Mode (appended to Basic Mode)

```markdown
### 5. Large Transaction History

> Filter: Amount > ${min_value_usd} | Most recent {count} transactions

| Time | Type | Amount | Counterparty | Counterparty Label |
|------|------|--------|--------------|-------------------|
| {time} | {In/Out/Contract Interaction} | ${value} | `{counterparty}` | {label/unknown} |
| ... | ... | ... | ... | ... |

**Transaction Pattern Analysis**:
{LLM analyzes transaction records and identifies patterns:}
- Frequent interactions with an exchange → likely depositing/withdrawing
- Large one-way outflows → possibly liquidating
- Interacting with many new addresses → possibly dispersing funds
- Regular fixed-amount transfers → possibly payroll/OTC

### 6. Fund Flow Tracing

> Trace depth: {depth} levels | Minimum amount: ${min_value_usd}

```
{address} (origin)
  ├── ${amount} → {addr_1} ({label_1})
  │     ├── ${amount} → {addr_1a} ({label})
  │     └── ${amount} → {addr_1b} ({label})
  ├── ${amount} → {addr_2} ({label_2})
  │     └── ${amount} → {addr_2a} ({label})
  └── ${amount} → {addr_3} ({label_3})
```

**Fund Flow Analysis**:
{LLM analysis based on tracing results:}
- Ultimate destination of funds (exchange? mixer? DeFi protocol?)
- Any suspicious patterns (split transfers, circular transfers, obfuscation paths)
- Associated known entities

### ⚠️ Risk Warnings

{If the address has risk flags, prominently display:}
- ⚠️ This address is flagged as: {risk_label}
- ⚠️ Associated addresses involved in: {risk_detail}
```

---

## Decision Logic

| Condition | Assessment |
|-----------|------------|
| risk_score > 70 | High-risk address — warn user to exercise caution |
| risk_score 40-70 | Medium risk — note some risk factors present |
| risk_score < 40 | Low risk |
| Holding concentration > 80% in a single token | Flag "Highly concentrated holding" |
| DeFi lending health factor < 1.2 | Near liquidation |
| Large outflow in past 24h > 50% of total balance | Flag "Recent large outflow" |
| Fund flow includes mixer addresses | Flag "Mixer involvement — high risk" |
| Fund flow includes OFAC-sanctioned addresses | Flag "Associated with sanctioned address" |
| trace_fund_flow returns empty | Possibly a new address or no large-enough transactions — handle normally |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| Invalid address format | Prompt user to check the format; provide correct format examples |
| Cannot identify chain | Prompt user to specify the chain ("Which chain is this address on? ETH/BSC/TRX/BTC...") |
| `info_onchain_get_address_info` returns empty | Address may be new or have no on-chain activity; inform the user |
| `info_onchain_trace_fund_flow` unavailable (P1 phase) | Inform user "Fund tracing is still under development"; show transaction history only |
| `info_onchain_get_address_transactions` timeout | Reduce limit and retry, or show address profile only |
| All Tools fail | Return error message; suggest the user try again later |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "Is this address safe?" | `gate-info-riskcheck` |
| "On-chain data for this token" | `gate-info-tokenonchain` |
| "Which institution owns this address?" | `gate-info-whaletracker` |
| "Analyze XX coin for me" | `gate-info-coinanalysis` |
| "Why was there a large outflow?" | `gate-news-eventexplain` |

---

## Safety Rules

1. **Privacy protection**: Do not link on-chain addresses to specific natural persons (unless publicly labeled as institutional addresses)
2. **Clear risk warnings**: High-risk addresses must have prominent, unmistakable risk labels with reasons
3. **No definitive characterization**: Do not use terms like "criminal address" or "dirty money" — use objective language like "flagged as high risk" or "associated with suspicious activity"
4. **Data source transparency**: Label data sources (BlockInfo / Nansen / Arkham) must be attributed
5. **Flag missing data**: Fund tracing rolls out in phases; when unavailable, explicitly state it
6. **Do not encourage stalking**: If a user attempts to track many personal addresses for harassment purposes, prompt responsible use
