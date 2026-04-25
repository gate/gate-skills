---
name: gate-exchange-dual
description: "Gate dual investment skill. Use when the user asks about dual currency products, target price settlement, or placing dual orders. Triggers on 'dual investment', 'dual currency', 'target price', 'exercise price', 'dual orders', 'dual balance', 'sell-high', 'buy-low', 'place dual order', 'subscribe dual'."
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


# Gate Exchange Dual Investment Skill

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read `./references/gate-runtime-rules.md`
- **Only use the `gate-cli` commands explicitly listed in this skill.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

## Skill Dependencies


### gate-cli commands used

**Query Operations (Read-only)**

- `gate-cli cex earn dual balance`
- `gate-cli cex earn dual plans`
- `gate-cli cex earn dual orders`

**Execution Operations (Write)**

- `gate-cli cex earn dual place`

### Authentication
- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard for API key, secret, profiles, and defaults (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** **`gate-cli config init`** is **not** required when credentials are already supplied — e.g. **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** set on the host, or **`--api-key`** / **`--api-secret`** where supported — never ask the user to paste secrets into chat.
- API Key Required: Yes
- **Permissions:** Earn:Write
- **Portal:** create or rotate keys outside the chat: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check
- **Required:** `gate-cli` (run `sh ./setup.sh` from this skill directory if missing; optional `GATE_CLI_SETUP_MODE=release`).
- Add `$HOME/.openclaw/skills/bin` to **`PATH`** if you invoke `gate-cli` by name (or the directory where [`setup.sh`](./setup.sh) installs it).
- **Credentials:** When **`GATE_API_KEY`** and **`GATE_API_SECRET`** are both set (non-empty) for the host, **do not** require **`gate-cli config init`** — that is equivalent valid config for `gate-cli`. When **both** are unset or empty, **remind** the operator to run **`gate-cli config init`** **or** to configure **`GATE_API_KEY`** / **`GATE_API_SECRET`** in the **matching skill** from the skill library (never ask the user to paste secrets into chat).
- **Sanity check:** Do not proceed with authenticated calls until the CLI behaves as expected (e.g. **`gate-cli --version`** or a read-only **`gate-cli cex ...`** command from this skill); confirm credentials resolve before mutating operations.

## Execution mode

**Read and strictly follow** [`references/gate-cli.md`](./references/gate-cli.md), then execute this skill's dual-investment workflow.

- `SKILL.md` keeps routing and product semantics.
- `references/gate-cli.md` is the authoritative `gate-cli` execution contract for plan lookup, confirmation-gated placement, and order verification.

## Prerequisites

- **MCP Dependency**: Requires [gate-mcp](https://github.com/gate/gate-mcp) to be installed.
- **Authentication**: All endpoints require API key authentication.
- **Risk Disclaimer**: Always append: _"This information is for reference only and does not constitute investment advice. Dual investment is not principal-protected. You may receive settlement in a different currency than your investment. Please understand the product terms before investing."_

## Available MCP Tools

| Tool | Auth | Description |
|------|------|-------------|
| `gate-cli cex earn dual plans` | Yes | List available dual investment plans (optional param: plan_id) |
| `gate-cli cex earn dual orders` | Yes | List dual investment orders. **`page` and `limit` are required**: always pass `page=1, limit=100`. Optional: `from`, `to`. **MUST loop all pages (increment page until returned rows < limit) before drawing any conclusion.** |
| `gate-cli cex earn dual balance` | Yes | Get dual investment balance & interest stats |
| `gate-cli cex earn dual place` | Yes | Place a dual investment order. Params: `plan_id` (required), `amount` (required), `text` (optional, must start with `t-`, max 28 bytes after prefix, alphanumeric/`_`/`-`/`.` only). |

## Routing Rules

| Case | User Intent | Signal Keywords | Action |
|------|-------------|----------------|--------|
| 1 | Browse dual product list | "dual products", "sell-high / buy-low options" | See `references/product-query.md` |
| 3 | Product details | "min investment", "BTC sell-high" | See `references/product-query.md` (filter locally by currency; show matching plans, skip min amount) |
| 4 | Settlement simulation | "what happens at delivery", "if price reaches X" | See `references/product-query.md` (simulation) |
| 5 | Position summary (ongoing) | "how much locked", "active positions" | See `references/product-query.md` (ongoing + balance) |
| 6 | Settlement records | "settlement records", "got crypto or USDT", "last month orders" | See `references/product-query.md` (settled) |
| 7 | Sell-high order (invest crypto) | "sell high for me", "sell high with BTC", "sell high order" | See `references/subscription.md` |
| 8 | Buy-low order (invest stablecoin) | "buy low for me", "buy low BTC with USDT", "buy low order" | See `references/subscription.md` |
| 9 | Amount eligibility for order | "can I buy", "is 5000U enough" | See `references/subscription.md` |
| 10 | Min purchase check for order | "minimum to buy", "can I buy dual with 50U" | See `references/subscription.md` |
| 11 | Settlement result query | "what did I receive", "settlement result" | See `references/settlement-assets.md` (settlement) |
| 12 | Dual asset briefing | "dual balance", "total locked" | See `references/settlement-assets.md` (balance) |
| 13 | Currency conversion risk | "will I lose principal", "risk", "principal-protected?" | Domain Knowledge (no API) |
| 14 | Missed gains explanation | "did I lose money", "missed gains", "price surged" | Domain Knowledge (no API) |
| 15 | Restricted region | "can I buy dual in [region]", "which regions supported" | See `references/subscription.md` (compliance) |
| 17 | Compliance check failure | "subscription failed", "compliance check not passed" | See `references/subscription.md` (compliance) |

## Execution

1. Identify user intent from the Routing Rules table above.
2. For Cases 1–6, 11–12: Read the corresponding sub-module document in `references/` and follow the Workflow.
3. For Cases 7–10: Read `references/subscription.md` and follow the order placement Workflow.
4. For Cases 15, 17: Read `references/subscription.md` and follow the compliance handling Workflow. These cases are triggered by `gate-cli cex earn dual place` error responses or by the user asking about region restrictions.
5. For Cases 13–14: Answer directly using Domain Knowledge below (no API call needed).
6. If the user's intent is ambiguous, ask a clarifying question before routing.

## Domain Knowledge

### Core Concepts

- **Sell High (Call)**: User invests crypto, target price above current price. If settlement price ≥ target price → receive USDT (principal × target price × (1 + interest)); if settlement price < target price → get back crypto + interest.
- **Buy Low (Put)**: User invests stablecoins, target price below current price. If settlement price ≤ target price → receive crypto; if settlement price > target price → get back USDT + interest.
- **Target Price**: The price that determines settlement outcome at delivery. Gate official term.
- **Settlement Price**: Market price of the underlying asset at delivery time, compared against target price.
- **Interest-guaranteed, not principal-protected**: Principal + interest are always received, but the settlement currency may change due to price movement.
- The closer the target price is to the current price, the higher the APY, but also the higher the probability of currency conversion.
- Once placed, dual investment orders cannot be cancelled. Settlement is automatic at delivery time.
- **Order type derivation**: `gate-cli cex earn dual orders` has NO `type` field. Derive from `invest_currency`: crypto (BTC, ETH...) → Sell High (Call); stablecoin (USDT) → Buy Low (Put). Filter by coin using `invest_currency` or `exercise_currency` — there is NO `instrument_name`.
- **Order status values**: `INIT` (Pending), `PROCESSING` (In Position), `SETTLEMENT_SUCCESS` (Settled), `SETTLEMENT_PROCESSING` (Settling), `CANCELED` (Canceled), `FAILED` (Failed), `REFUND_SUCCESS` / `REFUND_PROCESSING` / `REFUND_FAILED` → display as "Early Redemption", never "Refund". Early-redeemed orders have zero yield.

### Settlement Rules (Gate Examples)

**Sell High**: Invest 1 BTC, target price 20,000 USDT, 31 days, 100% APY
- Settlement price < 20,000 → payout = 1 × (1 + 100%/365×31) = **1.0849 BTC**
- Settlement price ≥ 20,000 → payout = 1 × 20,000 × (1 + 100%/365×31) = **21,698.63 USDT**

**Buy Low**: Invest 20,000 USDT, target price 20,000 USDT, 31 days, 100% APY
- Settlement price ≤ 20,000 → payout = 20,000/20,000 × (1 + 100%/365×31) = **1.0849 BTC**
- Settlement price > 20,000 → payout = 20,000 × (1 + 100%/365×31) = **21,698.63 USDT**

### Risk FAQ (Cases 13–14)

**Q: Will I lose principal? (Case 13)**
A: Interest-guaranteed, not principal-protected. You always receive principal + interest, but the settlement currency may change. Sell-high may return crypto instead of USDT; buy-low may return USDT instead of crypto. The closer the target price to the current price, the higher the yield but also the higher the conversion risk.

**Q: I sold high on BTC and it surged — did I lose money? (Case 14)**
A: When settlement price ≥ target price, you successfully sell at the target price and receive USDT, but miss gains above the target price. When settlement price < target price, you get back crypto + interest. This product suits sideways or mildly bullish markets; in strong bull markets you may "miss out" on excess gains.

## Safety Rules

- **Timestamp fields (CRITICAL)**: All time fields (`delivery_time`, `create_time`, `complete_time`, `delivery_timest`) are Unix timestamps (seconds). Do NOT convert them to dates or display them to the user in any form. This includes: (1) Do NOT show timestamps as table columns. (2) Do NOT convert timestamps to dates and use them as section headers or grouping labels (e.g. "Delivery Time: 2026-03-17"). (3) Do NOT mention delivery dates in order confirmations. Simply omit all time-related information from user-facing output.
- **APY display (CRITICAL — applies to ALL dual tools)**: Any APY/rate field (`apy`, `apy_display`, `apy_settlement`, `apyDisplay`, or any other rate field) returned by any dual investment tool is a **raw value — NOT a percentage**. You **MUST multiply by 100** then append `%` for display. **NEVER** display the raw value directly as a percentage. Common mistake: values like `1.1343` or `16.133` look like percentages but they are NOT — `1.1343` → **113.43%**, `16.133` → **1613.3%**. Another example: `0.0619` → **6.19%**, `2.7814` → **278.14%**. Use the raw value only in settlement formulas. This rule applies to ALL dual tools (`gate-cli cex earn dual plans`, `gate-cli cex earn dual orders`, `gate-cli cex earn dual balance`, etc.).
- **APY sanity check (MANDATORY before responding)**: After formatting ALL APY values, scan every value in your output. Typical correct ranges after ×100: crypto sell-high plans → 10%–2000%; stablecoin buy-low plans → 5%–1800%. **If you see any APY displayed as 0.05%–20% (single or low-double digits), you almost certainly forgot to multiply by 100. STOP, go back, and recompute ALL APY values before responding.** For example, if a raw value is `19.9378`, the correct display is `1993.78%` — NOT `19.94%`.
- **No investment advice**: Do not recommend specific plans or predict prices. Present data and let the user decide.
- **Non-principal-protected**: Always clearly communicate that dual investment is NOT principal-protected and the user may receive a different currency.
- **Order placement confirmation**: Before calling `gate-cli cex earn dual place`, MUST show the user the full order details (plan, amount, target price, APY, settlement scenarios) and get **explicit user confirmation**. NEVER place an order without confirmation.
- **Sensitive data**: Never expose API keys, internal endpoint URLs, or raw error traces to the user.

## Error Handling

| Condition | Response |
|-----------|----------|
| Auth endpoint returns "not login" | "Please log in to your Gate account first." |
| `gate-cli cex earn dual plans` returns empty | "No dual investment plans available at the moment." |
| `gate-cli cex earn dual orders` returns empty | "No dual investment orders found for the specified criteria." |
| `gate-cli cex earn dual place` returns region restriction error | See Case 15 in `references/subscription.md` |
| `gate-cli cex earn dual place` returns other compliance error | See Case 17 in `references/subscription.md` |
| `gate-cli cex earn dual place` returns insufficient balance | "Insufficient balance. Please ensure your account has enough funds and try again." |
| `gate-cli cex earn dual place` returns other failure | Display the error message returned by the API to the user. |

## Prompt Examples & Scenarios

See `references/scenarios.md` for full prompt examples and expected behaviors covering all 17 cases.
