---
name: gate-exchange-transfer
description: "Gate Exchange same-UID internal transfer skill. Use when the user asks to move funds between their own Gate accounts. Triggers on 'transfer funds', 'move USDT to futures', 'internal transfer'."
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

Resolve **`gate-cli`** in order: **(1)** **`command -v gate-cli`** and **`gate-cli --version`** succeeds; **(2)** **`${HOME}/.local/bin/gate-cli`** if executable; **(3)** **`${HOME}/.openclaw/skills/bin/gate-cli`** if executable. Canonical rules: [`exchange-runtime-rules.md`](../exchange-runtime-rules.md) §4 (or [`gate-runtime-rules.md`](../gate-runtime-rules.md) §4).


# Gate Exchange Transfer (Internal Transfer)

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read `./references/gate-runtime-rules.md`
- **Only use the `gate-cli` commands explicitly listed in this skill.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

Execute same-UID internal transfers between Gate trading accounts: **spot**, **isolated margin**, **perpetual**, **delivery**, and **options**. Single execution endpoint: `POST /wallet/transfers` (MCP: `gate-cli cex wallet transfer create`).
**Scope (Phase 1)** 
- Supported: internal transfer only (same UID, between account types above).
- Not supported: main-to-sub, sub-to-main, sub-to-sub.

---

## Skill Dependencies


### gate-cli commands used

**Query Operations (Read-only)**

- `gate-cli cex delivery account book`
- `gate-cli cex futures account book`
- `gate-cli cex margin account book`
- `gate-cli cex options account book`
- `gate-cli cex spot account book`

**Execution Operations (Write)**

- `gate-cli cex wallet transfer create`

### Authentication
- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard for API key, secret, profiles, and defaults (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** **`gate-cli config init`** is **not** required when credentials are already supplied — e.g. **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** set on the host, or **`--api-key`** / **`--api-secret`** where supported — never ask the user to paste secrets into chat.
- API Key Required: Yes
- **Permissions:** Delivery:Read, Fx:Read, Margin:Read, Options:Read, Spot:Read, Wallet:Write
- **Portal:** create or rotate keys outside the chat: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check
- **Required:** `gate-cli` (run `sh ./setup.sh` from this skill directory if missing; optional `GATE_CLI_SETUP_MODE=release`).
- Add `$HOME/.openclaw/skills/bin` to **`PATH`** if you invoke `gate-cli` by name (or the directory where [`setup.sh`](./setup.sh) installs it).
- **Credentials:** When **`GATE_API_KEY`** and **`GATE_API_SECRET`** are both set (non-empty) for the host, **do not** require **`gate-cli config init`** — that is equivalent valid config for `gate-cli`. When **both** are unset or empty, **remind** the operator to run **`gate-cli config init`** **or** to configure **`GATE_API_KEY`** / **`GATE_API_SECRET`** in the **matching skill** from the skill library (never ask the user to paste secrets into chat).
- **Sanity check:** Do not proceed with authenticated calls until the CLI behaves as expected (e.g. **`gate-cli --version`** or a read-only **`gate-cli cex ...`** command from this skill); confirm credentials resolve before mutating operations.


## Execution mode

**Read and strictly follow** [`references/gate-cli.md`](./references/gate-cli.md), then execute this skill's transfer workflow.

- `SKILL.md` keeps transfer intent routing and account-type mapping.
- `references/gate-cli.md` is the authoritative `gate-cli` execution contract for transfer pre-check, confirmation gate, execution, and ledger verification.

## Preconditions

| Precondition | If not met |
|--------------|------------|
| User logged in | Do not call API; prompt to log in (exception flow). |
| Account mode known | Infer from context or assume classic: Spot ↔ USDT perpetual. For unified/trading account advanced mode: Trading account ↔ BTC perpetual. |
| Source balance verifiable | Call balance API for `from` account before showing draft; if unavailable, prompt user to check on web. |

---

## The Four Elements

Every internal transfer is fully specified by four elements. The assistant must resolve or infer them before showing a **Transfer Draft**.

| Element | API param | Required when | Notes |
|---------|-----------|----------------|-------|
| **From** | `from` | Always | spot \| margin \| futures \| delivery \| options |
| **To** | `to` | Always | Same enum as `from` |
| **Currency** | `currency` | Always | USDT, BTC, etc. (platform-supported). Missing → auto-complete by target (case2). |
| **Amount** | `amount` | Always | String, > 0, up to 8 decimals. Missing → ask user (case8). |

**Conditional params** 
- **margin**: `currency_pair` required (e.g. `BTC_USDT`) when `from` or `to` is `margin`. 
- **futures / delivery**: `settle` required (`usdt` \| `btc`) when `from` or `to` is `futures` or `delivery`.

---

## Public API (Phase 1)

| Endpoint | Method | Meaning | Rate limit |
|----------|--------|---------|------------|
| `/wallet/transfers` | POST | Same-UID internal transfer | 80 req/10s |

---

## Tool Mapping

| Group | Tool (`jsonrpc: call.method`) |
|-------|-------------------------------|
| Main account internal transfer | `gate-cli cex wallet transfer create` |

---

## Case Index

| Case | Scenario | Action |
|------|----------|--------|
| case1 | All four elements present | Show Transfer Draft → confirm → call API → Transfer Result Report |
| case2 | Currency missing | Auto-complete currency by target account → same as case1 |
| case3 | Transfer completed (API success) | Output Transfer Result Report + product suggestion |
| case4 | Insufficient balance | Pre-check fails; no API call; show shortfall and suggest deposit/adjust |
| case5 | Missing from/to or ambiguous intent | Show missing-info card; do not call API |
| case6 | Account mode conflict (e.g. trading account → USDT perpetual not allowed) | Explain and suggest alternative path |
| case7 | Currency vs To mismatch (e.g. USDT to BTC perpetual) | Auto-correct or prompt correction → then case1 |
| case8 | Amount missing | Ask for amount; after user provides, proceed to case1/case2 |
| case9 | User cancels or declines after draft | Acknowledge; do not call API |
| case10 | Confirmation ambiguous or stale | Re-present draft; ask for explicit "Confirm" / "Yes"; do not execute |
| case11 | Rate limit / service error | Do not retry blindly; prompt retry later or use web UI |

---

## Transfer Draft (Mandatory before execution)

Before calling `gate-cli cex wallet transfer create`, output a **Transfer Draft** and wait for explicit confirmation in the **immediately following** user turn.

**Draft contents** 
- `from` (account name) 
- `to` (account name) 
- `currency` 
- `amount` 
- If applicable: `settle` (for futures/delivery), `currency_pair` (for margin)

**Confirmation rule** 
- Treat confirmation as **single-use**. If user changes amount, currency, or direction, show a new draft and re-confirm. 
- If user does not clearly confirm (e.g. "Confirm", "Yes", "Proceed"), do **not** execute (case10).
---

## Transfer Result Report (After successful API call)

- Confirm success: e.g. "Transfer successful. {amount} {currency} has arrived in your {to account name}." 
- Optionally suggest next step by destination: Spot → spot trading; USDT perpetual → USDT-margined perpetual; etc. 
- Mention transfer history: e.g. transfer/historyV2 or equivalent MCP tool.

---

## Case Logic and Output

### case1: All four elements present

**Trigger** 
"Transfer 100 USDT from my spot account to perpetual futures account" / "Transfer 1000 USDT from spot to USDT-margined futures" / "Transfer 0.5 BTC from coin-margined to spot"

**Steps** 
1. Resolve `from`, `to`, `currency`, `amount`; add `settle` or `currency_pair` if needed. 
2. Pre-check: fetch source balance; if balance < amount → case4. 
3. Output **Transfer Draft**. 
4. Wait for explicit confirmation. 
5. Call `gate-cli cex wallet transfer create`. 
6. Output **Transfer Result Report** (case3).
**Request mapping**

| Intent | API parameter | Values |
|--------|----------------|--------|
| Source account | `from` | spot \| margin \| futures \| delivery \| options |
| Target account | `to` | spot \| margin \| futures \| delivery \| options |
| Currency | `currency` | USDT, BTC, etc. |
| Amount | `amount` | String, > 0, up to 8 decimals |
| Margin pair | `currency_pair` | Required if from/to is margin, e.g. BTC_USDT |
| Settlement | `settle` | Required if from/to is futures or delivery: usdt \| btc |

---

### case2: Currency missing, auto-complete

**Trigger** 
"Transfer 100 to my USDT-margined account" / "Transfer 500 to futures" / "Transfer 1000 to perpetual"

**Logic** 
Set `currency` by target account:

| Target account | Default currency |
|----------------|------------------|
| USDT perpetual (futures settle=usdt) | USDT |
| BTC perpetual (futures settle=btc) | BTC |
| TradFi | USDT |
| Delivery | USDT |
| Options | USDT |
| Spot / margin | Infer from context or ask |

**Steps** 
Same as case1 after `currency` is set.

**Output (draft)** 
"Detected transfer of {amount} to {to account name}. Based on account type, default currency is {currency}. Please confirm."

---

### case3: Transfer completed (API success)

**Trigger** 
User confirmed; `gate-cli cex wallet transfer create` returned success.

**Output** 
- "Transfer successful. {amount} {currency} has arrived in your {to account name}." 
- Optional: product suggestion by destination (spot / USDT perpetual / BTC perpetual / delivery / margin / TradFi / options).
- "Transfer history: transfer/historyV2" (or equivalent).
---

### case4: Insufficient balance

**Trigger** 
Pre-check: source available balance < transfer amount.

**Action** 
Do **not** call transfer API.

**Output** 
"Your {from account name} has insufficient balance (available: {available} {currency}). Please adjust the amount or deposit first."

---

### case5: Missing from/to or ambiguous intent

**Trigger** 
"Contract is about to be liquidated, transfer some funds for margin" / "Top up my futures margin" / "How do I adjust account funds"

**Logic** 
- If missing ≥ 2 of from, to, currency, amount: show **missing-info card** and ask user to provide. 
- Defaults when only one side is clear: 
 - Unified/trading account advanced mode: default from = Trading account, to = BTC perpetual. 
 - Classic: default from = Spot, to = USDT perpetual. 
- Do **not** call API until four elements are clear.

**Output** 
"I can help with margin top-up. Please specify: from account, to account, and currency (and amount if you know it)."

---

### case6: Account mode conflict

**Trigger** 
User in **trading account advanced mode** asks to transfer to USDT perpetual. In this mode, direct transfer to USDT perpetual may be disallowed (path not available).
**Output** 
"You are in trading account mode; direct transfer to USDT perpetual is not available. You can transfer to BTC perpetual (coin-margined) instead, or adjust account mode on the web."

---

### case7: Currency vs To account mismatch

**Trigger** 
"Transfer some USDT to my BTC perpetual account"

**Logic** 
BTC perpetual settles in BTC; USDT is inconsistent. 
- **Option A**: Correct to BTC amount (if user intent allows).
- **Option B**: Explain that BTC perpetual uses BTC; suggest transferring BTC or using USDT perpetual for USDT. 
- If user confirms a corrected draft (e.g. spot → BTC perpetual with BTC), proceed as case1.

**Output** 
"BTC perpetual uses BTC settlement. I've corrected the transfer to use BTC (or: please specify amount in BTC). Please confirm." Or: "For USDT, use USDT perpetual account instead."

---

### case8: Amount missing

**Trigger** 
"Transfer USDT from spot to futures" / "Move my USDT to perpetual" (no amount).
**Action** 
Ask: "How much {currency} do you want to transfer from {from} to {to}?" After user provides amount, resolve currency if still missing (case2), then proceed to case1.

---

### case9: User cancels or declines

**Trigger** 
After Transfer Draft, user says "No" / "Cancel" / "Don't do it" / "Never mind".

**Action** 
Do **not** call API. Acknowledge: "Transfer cancelled. No changes made."

---

### case10: Confirmation ambiguous or stale

**Trigger** 
After draft, user replies with something other than clear confirmation (e.g. new question, different amount, or vague "ok" in a long thread).
**Action** 
Do **not** execute. Re-present the Transfer Draft and say: "To execute this transfer, please confirm explicitly (e.g. 'Confirm' or 'Yes')."

---

### case11: Rate limit or service error

**Trigger** 
API returns `TOO_MANY_REQUESTS` or server/network error.

**Action** 
Do not retry automatically in the same turn. 
**Output** 
"Request failed (rate limit / service error). Please try again later or use the web app to transfer."

---

## Exception Flow Summary

| Exception | Handling | Block execution |
|-----------|----------|-----------------|
| Not logged in | Prompt to log in | Yes |
| Insufficient balance | Show shortfall + suggest deposit/adjust (case4) | Yes |
| Invalid account path (e.g. from/to not allowed) | Guide user to correct (case5/case6) | No, guide |
| User cancel / decline | Acknowledge (case9) | Yes |
| Confirmation missing/ambiguous | Re-present draft, ask explicit confirm (case10) | Yes |
| Rate limit / service error | Retry later or use web (case11) | Yes |
| Risk control / quota | Show clear reason | Yes |

---

## API Reference

### Request body example

```json
{
 "currency": "USDT",
 "from": "spot",
 "to": "futures",
 "amount": "100",
 "currency_pair": "",
 "settle": "usdt"
}
```

### from / to → product name

| API value | Product name |
|-----------|--------------|
| spot | Spot |
| margin | Isolated margin |
| futures | Perpetual (use `settle`) |
| delivery | Delivery |
| options | Options |

### settle (futures / delivery)

| settle | Account |
|--------|---------|
| usdt | USDT perpetual |
| btc | BTC perpetual |

### currency_pair (margin)

Required when `from` or `to` is `margin`; e.g. `BTC_USDT`.

---

## Transfer History Query

After a transfer, user may ask for history. By account type:

| Account | Query tool (if MCP provides) | Notes |
|---------|------------------------------|--------|
| Spot | `gate-cli cex spot account book` | currency, time, limit |
| Perpetual | `gate-cli cex futures account book` | settle, type=dnw |
| Delivery | `gate-cli cex delivery account book` | settle, type=dnw |
| Margin | `gate-cli cex margin account book` | currency_pair, time, limit |
| Options | `gate-cli cex options account book` | per MCP docs |

REST: Delivery GET /delivery/{settle}/account_book?type=dnw; Perpetual GET /futures/{settle}/account_book?type=dnw; Margin GET /margin/account_book.

---

## Error Codes

| Code | Meaning |
|------|---------|
| BALANCE_NOT_ENOUGH | Insufficient balance; do not retry same amount |
| TOO_MANY_REQUESTS | Rate limit; prompt retry later (case11) |
| QUOTA_NOT_ENOUGH | Quota exceeded; show message |

---

## Execution Rules (Summary)

1. **Single endpoint**: Internal transfer only via `POST /wallet/transfers` (`gate-cli cex wallet transfer create`). No main-sub in Phase 1. 
2. **Always show Transfer Draft** with from, to, currency, amount (and settle/currency_pair if needed).
3. **Require explicit confirmation** in the next user turn; single-use; re-confirm if params change. 
4. **Pre-check balance** before calling API; on insufficient balance, follow case4 and do not call. 
5. **Conditional params**: `currency_pair` for margin; `settle` for futures/delivery. 
6. **Missing currency**: case2 default table. **Missing amount**: case8 ask. 
7. **Account mode / currency mismatch**: case6 and case7; resolve or correct before executing. 
8. **On cancel or ambiguous confirm**: case9/case10; do not execute.
