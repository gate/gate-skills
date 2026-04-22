# Scenarios

This document defines behavior-oriented scenario templates for gate-exchange-assets. All scenarios are **read-only** — no trading, transfer, or order placement.

---

## API Response Reference (Actual Interface)

Output templates must map to actual API response fields. Reference:

### `gate-cli cex wallet balance total` (GET /wallet/total_balance)

| Response Path | Type | Output Template Mapping |
|---------------|------|-------------------------|
| `total.amount` | string | `${total.amount}` — total asset valuation |
| `total.currency` | string | Quote currency (e.g. USDT) |
| `total.unrealised_pnl` | string? | Unrealised PnL (when total account) |
| `details` | object | Account distribution, keys: spot→Spot, futures→Futures, delivery→Delivery, finance→Finance, quant→Quant, margin→Isolated margin, cross_margin→Cross margin, meme_box→Alpha, options→Options, payment→Payment |
| `details[key].amount` | string | Per-account valuation |
| `details[key].currency` | string | Quote currency |

**AccountBalance** structure: `{ amount, currency?, unrealised_pnl?, borrowed? }`

### `gate-cli cex spot account get` (GET /spot/accounts)

| Response Field | Type | Output Mapping |
|----------------|------|----------------|
| `currency` | string | Currency |
| `available` | string | Available balance |
| `locked` | string | Locked balance |

### `gate-cli cex futures account get` (GET /futures/{settle}/accounts)

| Response Field | Type | Output Mapping |
|----------------|------|----------------|
| `total` | string | Wallet balance |
| `unrealised_pnl` | string | Unrealised PnL |
| `available` | string | Available to withdraw |
| `point` | string? | POINT (show when ≠ 0) |
| `bonus` | string? | Bonus (show when ≠ 0) |
| `bonus_offset` | string? | Position bonus (show when ≠ 0) |

### `gate-cli cex unified account get` (UnifiedAccount)

| Response Field | Type | Output Mapping |
|----------------|------|----------------|
| `unified_account_total` | string | Total assets |
| `unified_account_total_equity` | string | Account equity (cross/portfolio mode) |
| `total_margin_balance` | string | Total margin balance |
| `borrowed` | string | Total liability |
| `total_maintenance_margin_rate` | string | Maintenance margin rate (MMR) |
| `balances` | dict(currency→UnifiedBalance) | Per-currency: available, freeze, borrowed |

### `gate-cli cex options account get` (OptionsAccount)

| Response Field | Type | Output Mapping |
|----------------|------|----------------|
| `total` | string | Account balance |
| `equity` | string | Account equity |
| `available` | string | Available balance |
| `unrealised_pnl` | string | Unrealised PnL |
| `position_value` | string | Position value |

### `gate-cli cex margin account list` (MarginAccount[])

| Response Field | Type | Output Mapping |
|----------------|------|----------------|
| `currency_pair` | string | Trading pair, e.g. BTC_USDT |
| `mmr` | string | Maintenance margin rate |
| `risk` | string | Risk rate (risk mode) |
| `base` | MarginAccountCurrency | currency, available, locked, borrowed, interest |
| `quote` | MarginAccountCurrency | Same as base |

**MarginAccountCurrency**: `{ currency, available, locked, borrowed, interest }`

---

## I. Total Balance and Overview (Case 1)

### Case 1: Total Asset Query

**Trigger phrases**: "How much do I have", "Show my CEX total assets", "My account asset distribution", "Where are my assets", "Account overview", "Check my balance"

**MCP Tool**: `gate-cli cex wallet balance total` currency=USDT

**Output template**:
```
Your total CEX asset valuation is ≈ ${total.amount} USDT
🕒 Updated: {time} (UTC+8)
💰 Account distribution (details with amount>0, see API Reference for key mapping):
Spot ${details.spot.amount} | Futures ${details.futures.amount} | Delivery ${details.delivery.amount} | Finance ${details.finance.amount} | Isolated margin ${details.margin.amount} | Cross margin ${details.cross_margin.amount} | Alpha ${details.meme_box.amount} | Options ${details.options.amount} | Payment ${details.payment.amount}
```

**Scenario handling**:
- **Total < 10 USDT**: Show small-asset tip; recommend [Deposit] or [Dust conversion]

**Expected behavior**:
1. Call `gate-cli cex wallet balance total` with `currency=USDT`
2. Parse `total.amount` and `details`; output account distribution (details keys: spot, futures, delivery, finance, quant, margin, cross_margin, etc.)

**Unexpected behavior**:
1. Calls trading or transfer tools
2. Returns only spot balance when user asked for total

---

## II. Specific Currency Query (Case 2)

### Case 2: Specific Currency Asset Query

**Trigger phrases**: "How many BTC do I have", "How many USDT do I have"

**MCP Tools** (concurrent queries, aggregate by currency):
- `gate-cli cex spot account get` currency={COIN} — Spot (non-unified / classic)
- `gate-cli cex unified account get` currency={COIN} — Unified (spot + USDT perpetual + options)
- `gate-cli cex futures account get` settle=usdt — USDT perpetual (non-unified)
- `gate-cli cex futures account get` settle=btc — BTC perpetual (when querying BTC)
- `gate-cli cex delivery account get` settle=usdt — Delivery
- `gate-cli cex margin account list` — Isolated margin
- `gate-cli cex earn dual balance`, `gate-cli cex earn dual orders`, `cex_earn_list_structured_orders` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二), etc.

**Output template** (aggregate from actual API response fields):
```
You hold {total_qty} {COIN} (≈ ${total_val} USDT)
🕒 Updated: {time} (UTC+8)
💰 Asset distribution:
Spot: {available} + {locked} (cex_spot returns currency, available, locked)
Trading account: {balances[COIN].available} + {freeze} (cex_unified returns UnifiedBalance)
USDT perpetual: {total} (cex_fx settle=usdt)
BTC perpetual: {total} (cex_fx settle=btc)
Isolated margin: {base.available} + {base.locked} or {quote.*} (cex_margin returns base/quote)
```

**Special handling**:
- **USDT + TradFi**: Show TradFi (USDx) separately; "TradFi account in USDx, 1:1 with USDT, not included in CEX total"
- **Voucher tokens (e.g. GTETH)**: On-chain earn voucher, cannot withdraw to chain
- **ST token**: Risk warning status, suggest checking official announcements
- **Delisted token**: Explain delisting status, suggest withdrawal
- **Delisted + ST**: Priority delisted > ST; show only one status
- **Zero balance**: "No {COIN} assets"; recommend deposit or trading as appropriate

**Expected behavior**:
1. Call all relevant MCP tools in parallel
2. Aggregate {COIN} across accounts
3. Output total quantity, USDT valuation, and distribution

**Unexpected behavior**:
1. Mixes USDx into USDT total
2. Omits account distribution
3. Places any order

---

## III. Specific Account + Currency (Case 3)

### Case 3: Specific Account Specific Currency Query

**Trigger phrases**: "How much USDT in my spot account", "How much BTC in my spot account"

**MCP Tools**:
- Non-unified / classic: `gate-cli cex spot account get` currency={COIN} → available, locked
- Unified advanced: `gate-cli cex unified account get` currency={COIN} → available, freeze, borrowed

**Output template**:
```
Your {account_name} {COIN} holdings:
🕒 Updated: {time} (UTC+8)
💰 Asset details (from actual API response):
Classic spot `gate-cli cex spot account get`: available, locked
Unified `gate-cli cex unified account get`: balances[COIN].available, freeze, borrowed
Total: available + locked (or available + freeze)
Available: {available} | Locked: {locked} (or freeze)
```

**Special handling**:
- **Unified advanced, user asks "spot"**: Inform spot merged into trading account; show trading account balance for that currency
- **Account does not support currency**: Explain why; help find currency in other accounts

**Expected behavior**:
1. Call appropriate MCP tool based on account mode
2. Return available, locked, total
3. Output structured report

**Unexpected behavior**:
1. Returns wrong account
2. Mixes unified and classic mode without clarification
3. Places any order

---

## IV. Spot Account Query (Case 4)

### Case 4: Spot Account Query

**Trigger phrases**: "What's in my spot account", "Show my spot account assets"

**MCP Tools**:
- Non-unified / classic: `gate-cli cex spot account get`
- Unified advanced: `gate-cli cex unified account get`

**Output template**:
```
Your spot account total valuation is ≈ ${total_val} USDT
(Total = Σ(available+locked)×price; `gate-cli cex spot account get` has no total field, must calculate)
🕒 Updated: {time} (UTC+8)
🪙 Currency distribution (actual response fields):
{currency}: available {available}, locked {locked}
```

**Special handling**:
- **Unified advanced**: Inform spot merged into trading account; show trading account assets; "In single-currency margin mode, spot, USDT perpetual and options are unified in trading account"

**Expected behavior**:
1. Call `gate-cli cex spot account get` or `gate-cli cex unified account get` based on mode
2. Return total valuation, coin distribution (currency, available, locked)
3. Output structured report

**Unexpected behavior**:
1. Returns futures/margin when user asked for spot
2. Places any order

---

## V. Futures Account Query (Case 5)

### Case 5: Futures Account Query

**Trigger phrases**: "How much in my futures account", "Show my USDT perpetual assets", "Show my BTC perpetual assets", "Show my delivery contract assets", "Show my perpetual contract assets"

**MCP Tools**:
- USDT perpetual: `gate-cli cex futures account get` settle=usdt
- BTC perpetual: `gate-cli cex futures account get` settle=btc
- Delivery: `gate-cli cex delivery account get` settle=usdt
- Unified advanced (with USDT perpetual): `gate-cli cex unified account get`

**Field mapping**:
| Field | Display |
|-----------|---------|
| total | Wallet balance |
| unrealised_pnl | Unrealised PnL |
| available | Available to withdraw |
| point | POINT (only if ≠ 0) |
| bonus | Bonus (only if ≠ 0) |
| bonus_offset | Position bonus (only if ≠ 0) |

**Output template** (`gate-cli cex futures account get` actual response):
```
Your futures account (USDT perpetual/BTC perpetual/delivery) total valuation ≈ ${total} {USDT/BTC}
🕒 Updated: {time} (UTC+8)
Wallet: ${total} | Unrealised PnL: ${unrealised_pnl} | Available: ${available}
(when point≠0) POINT: ${point} (points only for spot and perpetual fee deduction)
(when bonus≠0) Bonus: ${bonus}
(when bonus_offset≠0) Position bonus: ${bonus_offset}
```

**Scenario handling**:
- **Non-unified, has assets**: Output as above
- **Non-unified, no futures assets**: Show futures = $0; show spot balance; recommend [Transfer]; trigger transfer card skill
- **Unified advanced, has trading account assets**: Inform USDT perpetual merged into trading account; show trading account assets; "No transfer needed, can place orders directly"; recommend [Trade]
- **Unified advanced, user asks USDT perpetual**: Show trading account available balance; prompt can place orders directly
- **Query "perpetual"**: Query and show BOTH USDT perpetual and BTC perpetual

**Expected behavior**:
1. Call `gate-cli cex futures account get` or `gate-cli cex delivery account get` as needed
2. Handle unified vs non-unified mode
3. Output structured report with field mapping

**Unexpected behavior**:
1. Calls transfer or trading tools
2. Omits POINT/bonus when non-zero
3. Shows "perpetual" without both USDT and BTC when applicable

---

## VI. Trading Account Query (Unified) (Case 6)

### Case 6: Trading Account Query

**Trigger phrases**: "How much in my trading account", "How much in my unified account"

**MCP Tool**: `gate-cli cex unified account get`

**Output by margin_mode**:

**Single-currency margin (margin_mode = "classic")**:
```
Your trading account total valuation ≈ ${unified_account_total} USDT
🕒 Updated: {time} (UTC+8)
💰 Account overview (UnifiedAccount actual fields):
Total: ${unified_account_total}
Per currency: balances[currency] → available, freeze, borrowed, cross_balance, mmr
MMR: ${total_maintenance_margin_rate}% 🟢/🟡/🔴 (>200% no risk, 130-200% medium risk, <130% high risk)
```

**Cross-margin / Portfolio (margin_mode = "cross_margin" or "portfolio")**:
```
Your trading account total valuation ≈ ${unified_account_total} USDT
🕒 Updated: {time} (UTC+8)
Equity: ${unified_account_total_equity}
Total margin balance: ${total_margin_balance}
Total liability: ${borrowed}
```

**Note**: Use only "trading account" or "unified account"; never use "advanced mode", "S1/S2" or other internal terms.

**Expected behavior**:
1. Call `gate-cli cex unified account get`
2. Branch by margin_mode
3. Output structured report with MMR risk indicators

**Unexpected behavior**:
1. Uses internal terminology
2. Mixes margin modes
3. Places any order

---

## VII. Options Account Query (Case 7)

### Case 7: Options Account Query

**Trigger phrases**: "How much in my options account", "Show my options assets"

**MCP Tools**:
- Non-unified / classic: `gate-cli cex options account get`
- Unified advanced: `gate-cli cex unified account get`

**Output template** (`gate-cli cex options account get` returns OptionsAccount):
```
Your options account total valuation ≈ ${total} USDT
🕒 Updated: {time} (UTC+8)
Balance: ${total} | Equity: ${equity} | Available: ${available} | Unrealised PnL: ${unrealised_pnl} | Position value: ${position_value}
```

**Scenario handling**:
- **Non-unified, has assets**: Output as above
- **Non-unified, zero assets**: Do NOT show "options account $0"; show spot balance; recommend transfer; trigger transfer card skill
- **Unified advanced**: Show trading account balance

**Expected behavior**:
1. Call `gate-cli cex options account get` or `gate-cli cex unified account get` based on mode
2. Return available, unrealised_pnl
3. Handle zero-asset case per rules

**Unexpected behavior**:
1. Shows "options account $0" when zero
2. Omits transfer recommendation when zero
3. Places any order

---

## VIII. Finance Account Query (Case 8)

### Case 8: Finance Account Query

**Trigger phrases**: "How much in my finance account", "Show my finance account assets"

**MCP Tools**: `gate-cli cex earn dual balance`, `gate-cli cex earn dual orders`, `cex_earn_list_structured_orders` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) (Flexible savings/Dual currency/Structured)

**Output template**:
```
Your finance account total valuation ≈ ${total_val} USDT
🕒 Updated: {time} (UTC+8)
(Display actual fields from `gate-cli cex earn dual balance`, list_dual_orders, list_structured_orders; no preset structure)
```

**Expected behavior**:
1. Call `gate-cli cex earn dual balance`, `gate-cli cex earn dual orders`, `cex_earn_list_structured_orders` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)
2. Output structured report from actual API response

**Unexpected behavior**:
1. Returns spot/futures when user asked for finance
2. Places any order

---

## IX. Alpha Account Query (Case 9)

### Case 9: Alpha Account Query

**Trigger phrases**: "How much in my Alpha account", "Show my Alpha assets"

**MCP Tool**: `gate-cli cex wallet balance total` (details.meme_box for Alpha)

**Output template**:
```
Your Alpha account effective valuation ≈ ${details.meme_box.amount} USDT
🕒 Updated: {time} (UTC+8)
```

**Note**: `details.meme_box` returns only AccountBalance { amount }, no per-coin breakdown

**Expected behavior**:
1. Call `gate-cli cex wallet balance total`, use `details.meme_box.amount`
2. Output structured report

**Unexpected behavior**:
1. Calls trading or transfer tools
2. Places any order

---

## X. Isolated Margin Account Query (Case 12)

### Case 12: Isolated Margin Account Query

**Trigger phrases**: "How much in my isolated margin account", "Show my isolated margin assets"

**MCP Tool**: `gate-cli cex margin account list`

**Output template** (`gate-cli cex margin account list` returns MarginAccount[], no total per item, aggregate base+quote per pair):
```
Your isolated margin account total valuation ≈ ${total_val} USDT
(Total = Σ base+quote value per pair; API has no total field)
🕒 Updated: {time} (UTC+8)
📊 Pair position details (actual response fields):
① {currency_pair}
{base.currency}: available ${base.available} | borrowed ${base.borrowed} | locked ${base.locked} | interest ${base.interest}
{quote.currency}: available ${quote.available} | borrowed ${quote.borrowed} | locked ${quote.locked} | interest ${quote.interest}
MMR: ${mmr}% 🟢/🟡/🔴 (>200% no risk, 130-200% medium risk, <130% high risk)
(when account_type=risk show risk rate; when account_type=mmr show mmr)
```

**Expected behavior**:
1. Call `gate-cli cex margin account list`
2. Return per-pair base/quote details with MMR
3. Output structured report

**Unexpected behavior**:
1. Returns spot/futures when user asked for margin
2. Omits MMR or risk indicator
3. Places any order

---

## XI. TradFi Account Query (Case 15)

### Case 15: TradFi Account Query

**Trigger phrases**: "How much in my TradFi account", "Show my TradFi assets"

**MCP Tool**: `gate-cli cex tradfi account assets`

**Output template**:
```
Your TradFi account details:
(Display actual fields from `gate-cli cex tradfi account assets`, common: net value, balance, unrealised PnL, margin, available margin, margin ratio, etc., in USDx)
⚠ Note: TradFi account is in USDx, 1:1 with USDT, not included in CEX total valuation.
```

**Note**:
- USDx assets must be physically isolated from crypto assets; never mix into USDT calculation
- AI transfer card is NOT supported for TradFi

**Expected behavior**:
1. Call `gate-cli cex tradfi account assets`
2. Return all fields in USDx
3. Always include disclaimer

**Unexpected behavior**:
1. Mixes USDx into USDT total
2. Omits disclaimer
3. Suggests AI transfer for TradFi

---

## XII. Account Book and Ledger (Legacy 5–7)

### Scenario 5: Account Book for Coin

**Context**: User wants ledger/account book for a currency.
**Prompt examples**: "Show my BTC account book.", "What changes happened to my ETH?"
**MCP Tool**: `gate-cli cex spot account book` currency=X
**Expected**: Return recent ledger entries (actual API fields: id, timestamp, currency, change, total, balance, type, etc.).

### Scenario 6: Ledger + Current Balance

**Context**: User wants both ledger flow and current balance.
**Prompt examples**: "Check recent BTC account book and tell me how much BTC I have now."
**MCP Tools**: `gate-cli cex spot account book` + `gate-cli cex spot account get`
**Expected**: Summarize recent changes and reconcile to current balance.

### Scenario 7: Recent Account Activity

**Context**: User wants summary of recent account activity.
**Prompt examples**: "What's my recent account activity?"
**MCP Tool**: `gate-cli cex spot account book` for major currencies
**Expected**: Summarize recent buy/sell/fee/transfer effects.

---

## XIII. Recommendation Engine (Single Button Per Response)

| Priority | Trigger | Recommended Action | Reference Phrase |
|----------|---------|-------------------|------------------|
| P1 (Risk) | Unified MMR > 80% or margin risk > 85% | [Transfer] or [Close position] | "⚠ Your trading account risk is high, consider adding margin" |
| P2 (Efficiency) | Spot/trading USDT ratio > 90% and no orders | [Finance] | "Idle funds detected, deposit to earn flexible interest" |
| P3 (Trading) | Query specific currency and today volatility > 5% | [Trade {COIN}/USDT] | — |
| P4 (Default) | — | [View account details] | — |

---

## XIV. Transfer Path Restrictions

- **Core rule**: Funds can only move between [any account] ↔ [spot/trading account]; cannot transfer directly between two non-spot accounts.
- **Supported for transfer**: Spot/trading, USDT perpetual, BTC perpetual, delivery, options, isolated margin, TradFi
- **NOT supported for AI transfer card**: Payment account (→ guide to App Pay mode)
