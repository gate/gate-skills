---
name: gate-exchange-assets
description: "Gate multi-account asset and balance query skill. Use when the user asks to check total assets, account balance, or specific coin holdings across all accounts. Triggers on 'total assets', 'my balance', 'how many BTC do I have'. Read-only."
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


# Gate Exchange Assets Assistant

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read `./references/gate-runtime-rules.md`
- **Only use the `gate-cli` commands explicitly listed in this skill.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

## Skill Dependencies


### gate-cli commands used

**Query Operations (Read-only)**

- `gate-cli cex delivery account get`
- `gate-cli cex earn dual balance`
- `gate-cli cex earn dual orders`
- cex_earn_list_structured_orders
- `gate-cli cex futures account get`
- `gate-cli cex margin account list`
- `gate-cli cex options account get`
- `gate-cli cex spot account get`
- `gate-cli cex spot account book`
- `gate-cli cex tradfi account assets`
- `gate-cli cex unified account get`
- `gate-cli cex wallet balance total`

### Authentication
- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard for API key, secret, profiles, and defaults (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** **`gate-cli config init`** is **not** required when credentials are already supplied — e.g. **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** set on the host, or **`--api-key`** / **`--api-secret`** where supported — never ask the user to paste secrets into chat.
- API Key Required: Yes
- **Permissions:** Delivery:Read, Earn:Read, Fx:Read, Margin:Read, Options:Read, Spot:Read, Tradfi:Read, Unified:Read, Wallet:Read
- **Portal:** create or rotate keys outside the chat: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check
- **Required:** `gate-cli` (run `sh ./setup.sh` from this skill directory if missing; optional `GATE_CLI_SETUP_MODE=release`).
- Add `$HOME/.openclaw/skills/bin` to **`PATH`** if you invoke `gate-cli` by name (or the directory where [`setup.sh`](./setup.sh) installs it).
- **Credentials:** When **`GATE_API_KEY`** and **`GATE_API_SECRET`** are both set (non-empty) for the host, **do not** require **`gate-cli config init`** — that is equivalent valid config for `gate-cli`. When **both** are unset or empty, **remind** the operator to run **`gate-cli config init`** **or** to configure **`GATE_API_KEY`** / **`GATE_API_SECRET`** in the **matching skill** from the skill library (never ask the user to paste secrets into chat).
- **Sanity check:** Do not proceed with authenticated calls until the CLI behaves as expected (e.g. **`gate-cli --version`** or a read-only **`gate-cli cex ...`** command from this skill); confirm credentials resolve before mutating operations.


## Execution mode

**Read and strictly follow** [`references/gate-cli.md`](./references/gate-cli.md), then execute this skill's assets-query workflow.

- `SKILL.md` keeps intent routing and rendering rules.
- `references/gate-cli.md` is the authoritative `gate-cli` execution contract for multi-account data collection, normalization, and degraded output handling.

## Domain Knowledge

### Command mapping (`gate-cli`)

| MCP Tool | Purpose | Key Fields |
|----------|---------|------------|
| `gate-cli cex wallet balance total` | Total balance (all sub-accounts, ~1min cache) | total.amount, details (spot/futures/delivery/finance/quant/meme_box/options/payment/margin/cross_margin) |
| `gate-cli cex spot account get` | Spot balance (filter by currency) | currency, available, locked |
| `gate-cli cex unified account get` | Unified account (single/cross/portfolio margin) | balances, unified_account_total, margin_mode |
| `gate-cli cex futures account get` | Perpetual (settle=usdt or btc) | total, unrealised_pnl, available, point, bonus |
| `gate-cli cex delivery account get` | Delivery (settle=usdt) | total, unrealised_pnl, available |
| `gate-cli cex options account get` | Options | total_value, unrealised_pnl, available |
| `gate-cli cex margin account list` | Isolated margin | currency_pair, mmr, base/quote (available/locked/borrowed/interest) |
| `gate-cli cex tradfi account assets` | TradFi assets | USDx balance, margin |
| `gate-cli cex earn dual balance`, `gate-cli cex earn dual orders`, `cex_earn_list_structured_orders` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) | Finance | Flexible savings / Dual currency / Structured |
| `gate-cli cex spot account book` | Spot account book / ledger | ledger entries |

### Account Name Mapping (details key → Display)

| API key | Display |
|---------|---------|
| spot | Spot account / Trading account |
| futures | Futures account (USDT perpetual) |
| delivery | Delivery contract account |
| options | Options account |
| finance | Finance account |
| quant | Quant/bot account |
| meme_box | Alpha account |
| margin | Isolated margin account |
| cross_margin | Cross margin account |
| payment | Payment account (not in total) |

### Key Rules

- **Read-only**. No trading, transfer, or order placement.
- **TradFi / payment**: USDx and payment assets are NOT included in CEX total; display separately.
- **Unified account**: When margin_mode is classic/cross_margin/portfolio, spot may be merged into "trading account". Do NOT use internal terms like "advanced mode", "S1/S2".
- **Pair format**: Futures use no-slash (BTCUSDT); spot/margin use slash (BTC/USDT).
- **Precision**: Fiat valuation 2 decimals; dust (<$0.01) show as `<$0.01`; finance yesterday PnL up to 8 decimals.

## Case Routing Map

### I. Total & Overview (Case 1)

| Case | Trigger Phrases | MCP Tool | Output |
|------|-----------------|----------|--------|
| 1 | "How much do I have", "Show my CEX total assets", "Account asset distribution", "Account overview", "Check my balance" | `gate-cli cex wallet balance total` currency=USDT | Total amount, account distribution, coin distribution; TradFi/payment listed separately if any |

### II. Specific Currency (Case 2)

| Case | Trigger Phrases | MCP Tool | Output |
|------|-----------------|----------|--------|
| 2 | "How many BTC do I have", "How many USDT do I have" | Concurrent: `gate-cli cex spot account get`, `gate-cli cex unified account get`, `gate-cli cex futures account get`, `gate-cli cex delivery account get`, `gate-cli cex margin account list`, `gate-cli cex earn dual balance`, etc. | Total {COIN} held, distribution by account |

### III. Specific Account + Currency (Case 3)

| Case | Trigger Phrases | MCP Tool | Output |
|------|-----------------|----------|--------|
| 3 | "How much USDT in my spot account", "How much BTC in my spot account" | `gate-cli cex spot account get` currency={COIN} or `gate-cli cex unified account get` currency={COIN} | Account name, total, available, locked |

### IV. Sub-Account Queries (Case 4–15)

| Case | Account | Trigger Phrases | MCP Tool |
|------|---------|-----------------|----------|
| 4 | Spot | "What's in my spot account", "Show my spot account assets" | `gate-cli cex spot account get` or `gate-cli cex unified account get` |
| 5 | Futures | "How much in futures account", "USDT perpetual", "BTC perpetual", "Delivery" | `gate-cli cex futures account get` settle=usdt/btc, `gate-cli cex delivery account get` |
| 6 | Trading (Unified) | "How much in trading account", "How much in unified account" | `gate-cli cex unified account get` |
| 7 | Options | "How much in options account", "Show my options assets" | `gate-cli cex options account get` or `gate-cli cex unified account get` |
| 8 | Finance | "How much in finance account", "Show my finance account assets" | `gate-cli cex earn dual balance`, `gate-cli cex earn dual orders`, `cex_earn_list_structured_orders` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) |
| 9 | Alpha | "How much in Alpha account", "Show my Alpha assets" | `gate-cli cex wallet balance total` details.meme_box |
| 12 | Isolated Margin | "How much in isolated margin account", "Show my isolated margin assets" | `gate-cli cex margin account list` |
| 15 | TradFi | "How much in TradFi account", "Show my TradFi assets" | `gate-cli cex tradfi account assets` |

### V. Account Book (Legacy 5–7)

| Case | Intent | MCP Tool |
|------|--------|----------|
| 5 | Account book for coin | `gate-cli cex spot account book` |
| 6 | Ledger + current balance | `gate-cli cex spot account book` → `gate-cli cex spot account get` |
| 7 | Recent activity | `gate-cli cex spot account book` |

## Special Scenario Handling

| Scenario | Handling |
|----------|----------|
| Total < 10 USDT | Show small-asset tip; recommend [Deposit] or [Dust conversion] |
| Unified account migration | "Your account is upgrading to unified account, asset data may be incomplete, please retry in ~5 minutes" |
| Dust (>10 dust coins) | "~${total_val} dust across {N} currencies" → [Dust conversion] |
| API timeout/error | "Data fetch error, please retry later" → [Refresh] |
| Account/coin balance = 0 | Do NOT show "your xx account is 0"; skip that item |
| USDT + TradFi | Show TradFi (USDx) separately; "TradFi in USDx, 1:1 with USDT, not in CEX total" |
| GTETH / voucher tokens | Explain: On-chain earn voucher, cannot withdraw to chain |
| ST token | Risk warning, suggest checking official announcements |
| Delisted token | Explain delisting, suggest withdrawal |
| Unified account, user asks "spot" | Inform spot merged into trading account; show trading account balance |

## Output Templates

**Case 1 – Total Balance:**
```
Your total CEX asset valuation ≈ ${total.amount} USDT
🕒 Updated: {time} (UTC+8)
💰 Account distribution: details keys (spot/futures/delivery etc.) amount, show only amount > 0
```

**Case 2 – Specific Currency:**
```
You hold {total_qty} {COIN} (≈ ${total_val} USDT)
🕒 Updated: {time} (UTC+8)
💰 Asset distribution: {account}: {qty} {COIN}, ≈ ${val} ({pct}%)
```

**Case 15 – TradFi:**
```
Your TradFi account details:
Net value: {net_value} USDx | Balance: {balance} USDx | Unrealised PnL: {unrealised_pnl} USDx
Margin: {margin} USDx | Available margin: {available_margin} USDx | Margin ratio: {ratio}% (max 999+%)
⚠ TradFi account in USDx, 1:1 with USDT, not in CEX total valuation.
```

## Acceptance Test Queries (Validation)

| Scenario | Query |
|----------|-------|
| Total balance – normal | How much do I have? |
| Total balance – overview | Show my CEX total assets |
| Total balance – small (<10U) | My account asset distribution |
| Specific currency – normal | How many BTC do I have? |
| Specific currency – zero | How much DOGE do I have? |
| Specific account+currency | How much USDT in my spot account? |
| Spot account | What's in my spot account? |
| Futures – with assets | How much in futures account |
| Futures – USDT+BTC perpetual | Show my perpetual contract assets |
| Futures – no assets | Show my USDT perpetual assets |
| Trading account | How much in trading account |
| Options | Show my options assets |
| Alpha | How much in Alpha account |
| Isolated margin | Show my isolated margin assets |
| TradFi | How much in TradFi account |

## Cross-Skill Workflows

- **Before trading**: User asks "Can I buy 100U BTC?" → This skill: `gate-cli cex spot account get` currency=USDT → Route to `gate-exchange-spot` if sufficient.
- **After transfer**: Route to this skill for updated balance when user asks.
- **Transfer card**: When futures/options = 0, recommend [Transfer] and trigger transfer skill.

## Safety Rules

- **Read-only only**. Never call create_order, cancel_order, create_transfer, or any write operation.
- If user intent includes trading, transfer, or order placement → route to appropriate skill.
- Always clarify currency and scope (spot vs all wallets) when ambiguous.

For detailed scenario templates and edge cases, see [references/scenarios.md](references/scenarios.md).