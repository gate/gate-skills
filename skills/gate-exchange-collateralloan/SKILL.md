---
name: gate-exchange-collateralloan
description: "Gate multi-collateral loan management skill. Use when the user asks to borrow crypto against collateral or manage existing loans. Triggers on 'collateral loan', 'current loan', 'fixed loan', 'repay', 'add collateral', 'redeem collateral'."
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    emoji: "💱"
    os:
      - darwin
      - linux
    primaryEnv: GATE_API_KEY
    requires:
      bins:
        - gate-cli
      env:
        - GATE_API_KEY
        - GATE_API_SECRET

    install:
      - kind: download
        os:
          - linux
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_linux_amd64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (Linux x64)"
      - kind: download
        os:
          - linux
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_linux_arm64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (Linux arm64)"
      - kind: download
        os:
          - darwin
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_darwin_amd64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (macOS Intel)"
      - kind: download
        os:
          - darwin
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_darwin_arm64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (macOS Apple Silicon)"
---

### Resolving `gate-cli` (binary path)

Resolve **`gate-cli`** in order: **(1)** **`command -v gate-cli`** and **`gate-cli --version`** succeeds; **(2)** **`${HOME}/.local/bin/gate-cli`** if executable; **(3)** **`${HOME}/.openclaw/skills/bin/gate-cli`** if executable. Canonical rules: [`exchange-runtime-rules.md`](https://github.com/gate/gate-skills/blob/master/skills/exchange-runtime-rules.md) §4 (or [`gate-runtime-rules.md`](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) §4).


# Gate Exchange Multi-Collateral Loan Skill

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only use the `gate-cli` commands explicitly listed in this skill.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

## Skill Dependencies


### gate-cli commands used

**Query Operations (Read-only)**

- `gate-cli cex mcl current-rate`
- `gate-cli cex mcl fix-rate`
- `gate-cli cex mcl ltv`
- `gate-cli cex mcl order`
- `gate-cli cex mcl orders`
- `gate-cli cex mcl records`
- `gate-cli cex mcl repay-records`
- `gate-cli cex mcl quota`
- `gate-cli cex mcl collateral`

**Execution Operations (Write)**

- `gate-cli cex mcl create`
- `gate-cli cex mcl repay`

### Authentication
- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard for API key, secret, profiles, and defaults (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** **`gate-cli config init`** is **not** required when credentials are already supplied — e.g. **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** set on the host, or **`--api-key`** / **`--api-secret`** where supported — never ask the user to paste secrets into chat.
- **Permissions:** Mcl:Write
- **Portal:** create or rotate keys outside the chat: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check
- **Required:** `gate-cli` (run `sh ./setup.sh` from this skill directory if missing; optional `GATE_CLI_SETUP_MODE=release`).
- Add `$HOME/.openclaw/skills/bin` to **`PATH`** if you invoke `gate-cli` by name (or the directory where [`setup.sh`](./setup.sh) installs it).
- **Credentials:** When **`GATE_API_KEY`** and **`GATE_API_SECRET`** are both set (non-empty) for the host, **do not** require **`gate-cli config init`** — that is equivalent valid config for `gate-cli`. When **both** are unset or empty, **remind** the operator to run **`gate-cli config init`** **or** to configure **`GATE_API_KEY`** / **`GATE_API_SECRET`** in the **matching skill** from the skill library (never ask the user to paste secrets into chat).
- **Sanity check:** Do not proceed with authenticated calls until the CLI behaves as expected (e.g. **`gate-cli --version`** or a read-only **`gate-cli cex ...`** command from this skill); confirm credentials resolve before mutating operations.

## Execution mode

**Read and strictly follow** [`references/gate-cli.md`](./references/gate-cli.md), then execute this skill's collateral-loan workflow.

- `SKILL.md` keeps routing and product constraints.
- `references/gate-cli.md` is the authoritative `gate-cli` execution contract for quota/LTV pre-checks, confirmation gates, and post-action verification.

## Trigger Conditions

This skill activates when the user asks about multi-collateral loan operations. Classify intent via **Routing Rules** (Cases 1–7). Trigger phrases include: "collateral loan", "current loan", "fixed loan", "repay", "add collateral", "redeem collateral", or equivalent in other languages.

## Workflow

### Step 1: Classify intent

Identify the user intent using Routing Rules (Cases 1–7). If required inputs are missing (order_id, currency, amount, fixed term), ask clarifying questions before proceeding.

### Step 2: Read-only requests (rates, LTV, quota, orders)

Call the corresponding MCP tool when the user asks for rates, LTV, quota, order list, or order detail.

Call `gate-cli cex mcl quota` with:
- `type`: `collateral` or `borrow`
- `currency`: comma-separated (borrow: single currency)

Call `gate-cli cex mcl ltv` with:
- (no params)

Call `gate-cli cex mcl fix-rate` with:
- (no params)

Call `gate-cli cex mcl current-rate` with:
- `currencies`: comma-separated currency list

Call `gate-cli cex mcl orders` with:
- `page`, `limit` (optional)
- `sort` (optional): `time_desc`, `ltv_asc`, `ltv_desc`
- `order_type` (optional): `current` or `fixed`

Call `gate-cli cex mcl order` with:
- `order_id`

Key data to extract:
- LTV thresholds, fixed/current rates, quota rows, order_id, order status, collateral and borrow details

### Step 3: Create loan (current or fixed)

If current loan:
1) Build draft (collateral list + borrow currency/amount).
2) Ask for confirmation.
3) Call `gate-cli cex mcl create` with **`order`**: JSON string (borrow_currency, borrow_amount, collateral_currencies, order_type: current).
If fixed loan:
1) Call `gate-cli cex mcl fix-rate` (returns a **list**); **filter by borrow_currency**; take `rate_7d` or `rate_30d` as **fixed_rate** (hourly rate; pass through unchanged, do not convert or relabel as annual/daily).
2) Build draft with fixed_type and fixed_rate (describe to user as hourly rate if showing).
3) Ask for confirmation.
4) Call `gate-cli cex mcl create` with **`order`**: JSON including order_type: fixed, fixed_type `7d`/`30d`, fixed_rate.

### Step 4: Repay

Build draft, ask confirmation, then call `gate-cli cex mcl repay` with:
- **`repay_loan`**: JSON string with `order_id` and `repay_items` [{ currency, amount, repaid_all }]

### Step 5: Add or redeem collateral

Build draft, ask confirmation, then call `gate-cli cex mcl collateral` with:
- **`collateral_adjust`**: JSON string with `order_id`, `type` (`append` | `redeem`), `collaterals` [{ currency, amount }]

## Judgment Logic Summary

- Determine case by keywords and required inputs (loan create / repay / add / redeem / list).
- Fixed loan requires fix_rate lookup; if not available, stop and inform user.
- All write operations must be confirmed before calling MCP.
- Auth failure (401/403) prompts API key configuration.

## Report Template

**When asking for confirmation**:
Draft:
- Type: {current|fixed|repay|append|redeem}
- Order ID: {order_id if applicable}
- Borrow: {borrow_amount} {borrow_currency}
- Collateral: {collateral_amounts}
- Fixed term/rate: {fixed_type} / {fixed_rate} (hourly rate)

Please confirm to proceed.

**On success**:
- Summary of action and key identifiers (order_id, amounts).
**On failure**:
- Error message and next-step guidance (e.g., check currency/amount/LTV).
## Prerequisites

- **MCP Dependency**: Requires [gate-mcp](https://github.com/gate/gate-mcp) to be installed.
- **Authentication**: Order list, detail, repay, collateral, quota, and records require API key; LTV, fix rate, and current rate are public without key.
- **Disclaimer**: Loan and LTV information is for reference only and does not constitute investment advice. Understand product terms and liquidation risk before borrowing.

## Available MCP Tools

| Tool | Auth | Description | Reference |
|------|------|-------------|-----------|
| `gate-cli cex mcl fix-rate` | No | 7d/30d fixed rates (list) | `references/mcl-mcp-tools.md` |
| `gate-cli cex mcl ltv` | No | LTV thresholds | `references/mcl-mcp-tools.md` |
| `gate-cli cex mcl current-rate` | No | Current rates | `references/mcl-mcp-tools.md` |
| `gate-cli cex mcl quota` | Yes | Borrow/collateral quota | `references/mcl-mcp-tools.md` |
| `gate-cli cex mcl create` | Yes | Create loan (`order` JSON) | `references/mcl-mcp-tools.md` |
| `gate-cli cex mcl orders` | Yes | List orders | `references/mcl-mcp-tools.md` |
| `gate-cli cex mcl order` | Yes | Order detail | `references/mcl-mcp-tools.md` |
| `gate-cli cex mcl repay` | Yes | Repay (`repay_loan` JSON) | `references/mcl-mcp-tools.md` |
| `gate-cli cex mcl collateral` | Yes | Add/redeem collateral (`collateral_adjust` JSON) | `references/mcl-mcp-tools.md` |
| `gate-cli cex mcl repay-records` | Yes | Repay history | `references/mcl-mcp-tools.md` |
| `gate-cli cex mcl records` | Yes | Collateral history | `references/mcl-mcp-tools.md` |

## Routing Rules

| Case | User Intent | Signal Keywords | Action |
|------|-------------|-----------------|--------|
| 1 | Create current loan | "current loan", "pledge... borrow... (current)" | See `references/scenarios.md` Scenario 1 |
| 2 | Create fixed loan | "fixed loan", "borrow... for 7/30 days" | See `references/scenarios.md` Scenario 2 |
| 3 | Repay | "repay", "repay order..." | See `references/scenarios.md` Scenario 3 |
| 4 | Add collateral | "add collateral", "add margin" | See `references/scenarios.md` Scenario 4 |
| 5 | Redeem collateral | "redeem collateral", "reduce margin" | See `references/scenarios.md` Scenario 5 |
| 6 | List orders / order detail | "loan orders", "order detail", "my orders" | `gate-cli cex mcl orders` / `gate-cli cex mcl order` — **never include any time/date fields** in the user-facing reply (see Presentation below) |
| 7 | Auth failure (401/403) | MCP returns 401/403 | Do not expose keys; prompt user to configure Gate CEX API Key (multi-collateral loan). |

## Execution

1. Identify user intent from the Routing Rules table above.
2. For Cases 1–5: Read the corresponding scenario in `references/scenarios.md` and follow the Workflow (show order draft, then call MCP only after user confirmation).
3. For Case 6: Call list or detail tool as needed; no confirmation required for read-only. **Never show** borrow_time, maturity, due date, operate_time, create_time, repay_time, Unix timestamps, or any other time-related fields in the reply—even if the user asks for dates/times; suggest checking the Gate app or web for timing details.
4. For Case 7: Do not expose API keys or raw errors; prompt the user to set up Gate CEX API Key with multi-collateral loan permission in MCP.
5. If the user's intent is ambiguous (e.g. missing order_id, currency, or amount), ask a clarifying question before routing.

## Domain Knowledge

### Core Concepts

- **Current loan**: Flexible loan. Create via `gate-cli cex mcl create` with `order` JSON: `order_type: current`.
- **Fixed loan**: 7-day/30-day. `order` JSON must include `order_type: fixed`, **`fixed_type`**: `7d` or `30d` (lowercase), **`fixed_rate`**: **hourly interest rate** from `gate-cli cex mcl fix-rate` (use `rate_7d` or `rate_30d` for that borrow_currency; pass as-is, do not describe as annual or daily rate). Missing fixed fields may yield INVALID_PARAM_VALUE.
- **Repay**: `gate-cli cex mcl repay` with `repay_loan` JSON.
- **Add collateral**: `gate-cli cex mcl collateral`, `collateral_adjust` with `type: append`.
- **Redeem collateral**: same tool, `type: redeem`.
- **LTV**: `gate-cli cex mcl ltv` — init_ltv, alert_ltv, liquidate_ltv.

### Create Loan Flow (Case 1 & 2)

1. Parse collateral, borrow currency/amount; fixed: 7 days → **7d**, 30 days → **30d**.
2. **Current**: Optionally `gate-cli cex mcl quota` or current rate tools. On confirm: `gate-cli cex mcl create` with `order` JSON.
3. **Fixed**: `gate-cli cex mcl fix-rate`; filter list by borrow_currency; on empty or no row, stop with user message; else set **fixed_rate** = rate_7d or rate_30d (**hourly rate**; pass as-is into order JSON; do not describe as annual or daily). On confirm: `order` JSON with fixed fields.

### Repay Flow (Case 3)

1. Parse order_id and repay amount (or full).
2. Show draft; on confirm: `gate-cli cex mcl repay` with `repay_loan` JSON.

### Add / Redeem Collateral Flow (Case 4 & 5)

1. Parse order_id and collateral amount/currency.
2. Show draft; on confirm: `gate-cli cex mcl collateral` with `collateral_adjust` JSON.

### Presentation — order list / order detail (Case 6)

When the user asks to view **my collateral loan orders** or order detail:

- **No time fields**: Do not output any time or date information—omit every timestamp-style field from MCP (e.g. `borrow_time`, maturity, due time, `operate_time`, `create_time`, `repay_time`, calendar dates, Unix seconds as dates). Do not paraphrase relative timing (e.g. "expires in 3 days") computed from those fields.
- **Allowed in reply**: `order_id`, `status`, borrow side (currency, principal/interest left), collateral side (currency, amount), current LTV if present, fixed_type `7d`/`30d` as **term label only** (no calendar dates).
- **If the user asks specifically for dates/maturity**: Reply that timing is not shown here and they should open Gate (app/web) for full order schedule—still do not paste API time fields into chat.

## Safety Rules

- **Writes** (`gate-cli cex mcl create`, `gate-cli cex mcl repay`, `gate-cli cex mcl collateral`): Always require explicit confirmation and an order draft before execution.
- **No investment advice**: Present LTV/rates; user decides.
- **Sensitive data**: Never expose API keys or raw internal errors.
- **Amounts**: Reject non-positive amounts; validate order_id for repay/collateral ops.
- **Order views**: Never surface time columns, dates, or timestamp fields in order list/detail answers to the user.

## Error Handling

| Condition | Response |
|-----------|----------|
| 401/403 | "Please configure your Gate CEX API Key in MCP with multi-collateral loan permission." |
| `gate-cli cex mcl create` fails | Check `order` JSON: borrow fields; for fixed include fixed_type `7d`/`30d` and fixed_rate from fix_rate tool. |
| Wrong fixed_type | Must be **`7d`** or **`30d`**, lowercase. |
| Fix rate empty (fixed) | "Fixed rate temporarily unavailable; try later or use current loan." |
| Repay / operate fails | Check order_id, currency, amount in JSON payloads. |
| Order not found | "Order not found." / "No loan orders." |

## Prompt Examples & Scenarios

See `references/scenarios.md` for prompt examples and expected behaviors (create current/fixed, repay, add collateral, redeem collateral).