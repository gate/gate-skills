---
name: gate-exchange-staking
description: "Gate on-chain staking skill. Use when the user asks to stake POS coins, mint, or redeem staked assets. Triggers on 'staking', 'stake ETH', 'redeem staking', 'staking rewards'."
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


# Gate Staking Query Suite

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only use the `gate-cli` commands explicitly listed in this skill.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

## Skill Dependencies


### gate-cli commands used

**Query Operations (Read-only)**

- `gate-cli cex earn staking assets`
- `gate-cli cex earn staking awards`
- `gate-cli cex earn staking find`
- `gate-cli cex earn staking orders`

**Execution Operations (Write)**

- `gate-cli cex earn staking swap`

### Authentication
- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard for API key, secret, profiles, and defaults (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** **`gate-cli config init`** is **not** required when credentials are already supplied — e.g. **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** set on the host, or **`--api-key`** / **`--api-secret`** where supported — never ask the user to paste secrets into chat.
- **Permissions:** Earn:Write
- **Portal:** create or rotate keys outside the chat: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check
- **Required:** `gate-cli` (run `sh ./setup.sh` from this skill directory if missing; optional `GATE_CLI_SETUP_MODE=release`).
- Add `$HOME/.openclaw/skills/bin` to **`PATH`** if you invoke `gate-cli` by name (or the directory where [`setup.sh`](./setup.sh) installs it).
- **Credentials:** When **`GATE_API_KEY`** and **`GATE_API_SECRET`** are both set (non-empty) for the host, **do not** require **`gate-cli config init`** — that is equivalent valid config for `gate-cli`. When **both** are unset or empty, **remind** the operator to run **`gate-cli config init`** **or** to configure **`GATE_API_KEY`** / **`GATE_API_SECRET`** in the **matching skill** from the skill library (never ask the user to paste secrets into chat).
- **Sanity check:** Do not proceed with authenticated calls until the CLI behaves as expected (e.g. **`gate-cli --version`** or a read-only **`gate-cli cex ...`** command from this skill); confirm credentials resolve before mutating operations.

## Execution mode

**Read and strictly follow** [`references/gate-cli.md`](./references/gate-cli.md), then execute this skill's staking workflow.

- `SKILL.md` keeps staking intent routing and scenario boundaries.
- `references/gate-cli.md` is the authoritative `gate-cli` execution contract for query/action separation, confirmation gates, and result verification.

## Module overview

| Module | Description | Trigger keywords |
|--------|-------------|------------------|
| **Positions** | Query staking positions, balances, available vs locked | `position`, `balance`, `staked`, `staking assets`, `holdings`, `redeemable` |
| **Rewards** | Query reward history, yesterday/monthly earnings | `reward`, `earning`, `profit`, `income`, `yesterday earnings`, `monthly earnings` |
| **Products** | Discover available staking products, APY, min amount | `products`, `available`, `APY`, `stakeable coins`, `high yield`, `flexible` |
| **Order history** | Query stake/redeem order list and pagination | `history`, `orders`, `transactions`, `staking records`, `redemption records` |
| **Stake / Redeem** | Execute stake or redeem via swap (pid required) | `stake`, `redeem`, `unstake`, `stake 100 USDT`, `redeem my ETH`, `swap staking` |

**Mint**: Treated as **immediate stake**. Route to the same Stake workflow: read `references/staking-swap.md`, resolve product (pid) and amount, then call `gate-cli cex earn staking swap` with **side=0**. For GUSD products, require the user to choose USDT or USDC and pass `coin`.

**Cancel redeem (not supported)**: When the user intends to **cancel** or **revoke** a redeem (e.g. cancel a redemption order already submitted), do not call any tool. Reply **in English** that this operation is not supported.

## Domain Knowledge

### Product types

| productType | Label | Description |
|-------------|-------|-------------|
| 0 | Certificate | Flexible staking with instant redemption (redeemPeriod = 0) |
| 1 | Lock-up | Fixed-term staking with a defined lock period (redeemPeriod > 0) |
| 2 | US Treasury Bond | Products backed by US Treasury bonds (e.g. GUSD). Users stake crypto and receive yield derived from US Treasury interest rates. Typically has a fixed or semi-fixed APR with low risk. |

### Redeemable amount calculation

The redeemable amount for a position is **not** `mortgage_amount − freeze_amount`. The correct formula is:

```
redeemable = mortgage_amount × exchangeRate
```

Where `exchangeRate` comes from `gate-cli cex earn staking find` for the same `pid` and matching `currency`. Some products have exchangeRate = 1 (e.g. USDT flexible), while others vary (e.g. liquid staking tokens).
### Dynamic exchange rate (exchangeRate ≠ 1)

When a product’s **exchange rate is not equal to 1**, it is a **dynamic-rate** product. In stake/redeem **response** data (swap result or order list): **amount** = staked/redeemed base coin quantity; **exchangeAmount** (or **exchange_amount**) = received quote/reward coin quantity.

**Display rule (English only):**
- **Stake**: Show **exchangeAmount** (what the user receives).
- **Redeem**: Show **amount** (what the user receives).
When exchangeRate = 1, either field may be omitted or shown as equal; prefer showing the single amount.

### Reward distribution

- `reward_delay_days = -1` means the reward is paid **on redeem**, not periodically.
- `interest_delay_days` indicates the delay after staking before rewards start accruing (typically 1 day / T+1).
- Multi-coin rewards: a single position can generate rewards in multiple coins (e.g. stake USDT in Compound V3, receive USDT + COMP).
### GUSD / multi-currency products (USDT or USDC)

When **staking**, **redeeming**, or **minting** GUSD (or any product whose `currency` or `mortgage_coin` is `"USDT,USDC"`):

- **Require the user to choose a coin.** Only **USDT** and **USDC** are supported.
- Prompt: e.g. "This product accepts USDT or USDC. Which do you want to use: USDT or USDC?"
- **Pass the user’s choice as the `coin` parameter** to the swap (or mint) tool. Do not call the tool until the user has selected one of the two.


### Positions: status field

When **viewing staking positions** (position/balance/holdings queries), **ignore and do not display** the `status` field. Omit it from all user-facing position output.

### Timestamps in results

**Do not display or format timestamp-related fields in any result.** Omit from user-facing output all timestamp fields (e.g. `createStamp`, `redeem_stamp`, `updateStamp`, `should_bonus_stamp`). Do not convert timestamps to dates, times, or relative time (e.g. no "YYYY-MM-DD", "HH:mm", "2 hours ago"). If a field is purely timestamp-based, do not show it.

### Number formatting

| Category | Precision | Trailing zeros | Examples |
|----------|-----------|----------------|----------|
| General amounts (mortgage_amount, freeze_amount, income_total, fee, etc.) | 8 decimals | Removed | `1.23` not `1.23000000`; `100` not `100.00000000` |
| Rate fields (estimateApr, APY, APR, exchangeRate) | 2 decimals | Retained | `5.20%` not `5.2%`; `8.00%` not `8%` |

## Routing rules

| Intent | Example phrases | Route to |
|--------|-----------------|----------|
| **Positions** | "Show my staking positions", "Check my staking assets", "What can I unstake?" | Read `references/staking-assets.md` |
| **Rewards** | "Staking rewards", "Yesterday's earnings", "Monthly earnings", "Earning records" | Read `references/staking-list.md` (Part 2: Reward List) |
| **Products** | "Available staking", "Stakeable coins", "Best APY", "Flexible only" | Read `references/staking-coins.md` |
| **Order history** | "Staking history", "Staking records", "Show redemptions", "Recent activity" | Read `references/staking-list.md` (Part 1: Order List) |
| **Stake / Redeem** | "Stake 1 BTC", "Stake 100 USDT", "Redeem my ETH", "redeem", "I want to stake", "unstake", "help me redeem" | Read `references/staking-swap.md`; use `gate-cli cex earn staking swap` with **pid** required, **side=0** (stake) or **side=1** (redeem); before stake get product list, if multiple protocols for same coin ask user to confirm |
| **Mint** | "mint", "I want to mint", "Mint", "mint GT", "help me mint" | Same as **Stake**: route to `references/staking-swap.md` and execute **stake** (side=0). Mint = immediate stake. For GUSD, require user to choose USDT or USDC and pass `coin`. |
| **Cancel redeem (not supported)** | "cancel redeem", "revoke redeem", "undo redeem", "cancel my redemption", "withdraw redeem request" | **Do not call tools.** Reply in English: Cancelling or revoking a redeem is not supported here; please use the Gate website or app if needed. I can help you query positions or order history. |
| **Unclear** | "Help with staking", "on-chain earn" | **Clarify**: positions / rewards / products / history, then route |

## Execution

### 1. Intent and parameters

- Determine module (Positions / Rewards / Products / Order history / **Stake or Redeem**) **or** whether the user intends to **mint** or **cancel a redeem**.
- **Stake / Redeem intent**: If the user wants to **execute** a stake or redeem (e.g. "stake 1 BTC", "stake 100 USDT", "redeem my ETH"), route to `references/staking-swap.md`. Follow the swap workflow: **pid is required** for `gate-cli cex earn staking swap`; use **side=0** for stake, **side=1** for redeem; before stake call `gate-cli cex earn staking find` and if multiple protocols for the same coin, list them and ask the user to confirm which product (pid) before calling the swap tool.
- **Mint intent**: If the user wants to **mint** (e.g. "mint", "I want to mint", "mint GT", "help me mint")—treat as **stake**. Route to `references/staking-swap.md` and execute the **Stake** workflow (side=0). Mint = immediate stake; same product selection, amount, and GUSD coin rule (USDT/USDC) as stake.
- **Cancel redeem intent**: If the user wants to **cancel** or **revoke** a redeem (e.g. "cancel redeem", "revoke my redemption", "undo redeem")—**do not** call any MCP tool. Reply **in English**: "Cancelling or revoking a redeem is not supported here; please use the Gate website or app if needed. I can help you query positions or order history." Then stop.
- Extract: `coin`, `pid`, `page`, `amount`; for order list also `type` (0=stake, 1=redeem); for swap always resolve or confirm `pid` before calling `gate-cli cex earn staking swap`.
- **Missing**: if user says "my staking" without specifying positions/rewards/products/history/action, ask which one or show positions by default.

### 2. Tool selection

| Module | MCP tool | Required | Optional params |
|--------|----------|----------|-----------------|
| Positions | `gate-cli cex earn staking assets` | - | `coin`, `pid` |
| Rewards | `gate-cli cex earn staking awards` | - | `coin`, `pid`, `page` |
| Products | `gate-cli cex earn staking find` | - | `cointype` |
| Order history | `gate-cli cex earn staking orders` | - | `coin`, `pid`, `type`, `page` |
| Stake / Redeem | `gate-cli cex earn staking swap` | **pid** | `amount`, **`side`** (0=stake, 1=redeem), `coin` (GUSD) |

- **Positions**: When showing redeemable amount, call **`gate-cli cex earn staking find`** (optionally with `cointype`), find the product with same **pid** and matching **currency** as each position; use that item’s **exchangeRate** (or **exchangeRateReserve** per API). Redeemable = mortgage_amount × that rate. Do not use mortgage_amount − freeze_amount.
- **Stake / Redeem**: Read `references/staking-swap.md`. **pid** is required for `gate-cli cex earn staking swap`. Use **`side`**: **0** = stake, **1** = redeem. Before stake: call `gate-cli cex earn staking find`; if multiple products (multiple pids) for that coin, list them and ask the user to confirm which product before calling the swap. Before redeem: if user did not give pid, use `gate-cli cex earn staking assets` to get positions; if multiple positions, ask user to choose pid.
- Response structures: **Positions** → array of items (pid, mortgage_coin, mortgage_amount, freeze_amount, income_total, yesterday_income / yesterday_income_multi, etc.). **Redeemable** is **not** mortgage_amount − freeze_amount; redeemable = mortgage_amount × exchange rate, where exchange rate comes from **`gate-cli cex earn staking find`** for the same **pid** and matching **currency** (coin). **Order list** → object with page, pageSize, pageCount, totalCount, list[]. **Reward list** → object with page, pageSize, pageCount, totalCount, list[] (pid, mortgage_coin, reward_coin, interest, bonus_date, etc.). **Products** → array (pid, currency, estimateApr, minStakeAmount, protocolName, redeemPeriod, productType, isDefi, currencyRewards, **exchangeRate**, etc.).
### 3. Format response

- Use the **Response Template** and field names from the reference file for the chosen module.
- Positions: show mortgage_amount, freeze_amount, **redeemable** (mortgage_amount × exchange rate; get exchange rate from **`gate-cli cex earn staking find`** for the same **pid** and matching **currency**), income_total, yesterday_income; group by coin or show per pid. Do not use mortgage_amount − freeze_amount for redeemable. Do not display or format timestamp fields (omit createStamp, updateStamp). Do not display **status** (ignore status field when showing positions).
- Rewards: show list entries with reward_coin, interest, bonus_date, pid, mortgage_coin; sum by reward_coin; use totalCount/page/pageCount when relevant. Do not display or format timestamp fields (e.g. omit should_bonus_stamp).
- Products: show protocolName, currency, estimateApr, minStakeAmount, maxStakeAmount, redeemPeriod, productType, isDefi; sort by estimateApr or filter by cointype.
- Order history: show list with coin, amount, type (0=Stake, 1=Redeem), status, pid, fee; use totalCount, page, pageCount for pagination. **Do not display or format timestamps** (omit createStamp, redeem_stamp, etc.). For **dynamic-rate** products (exchangeRate ≠ 1): for Stake show **exchange_amount**, for Redeem show **amount** (see Domain Knowledge).
- Stake / Redeem: follow `references/staking-swap.md`; confirm pid (and amount) before calling `gate-cli cex earn staking swap`; show success or error message in English. For dynamic-rate products: stake confirmation shows **exchangeAmount**, redeem shows **amount**.

## Report template

After each query, output a short standardized result consistent with the reference (e.g. positions summary, reward summary, product table, or order list). Use the exact response fields from the API (see references) so the user sees correct field names and values.

## Safety rules

### User confirmation requirement (Mandatory)

**NEVER call `gate-cli cex earn staking swap` without explicit user confirmation.** Without user confirmation, only read/query operations are allowed.

Before every stake, redeem, or mint execution:
1. Show an **Action Draft** summarizing: operation type (stake/redeem/mint), product (pid + protocolName), coin, amount, side, and key risk note (e.g. lock period, exchange rate).
2. Wait for explicit user confirmation (e.g. "Confirm", "Yes", "Go ahead").
3. Only after receiving confirmation in the immediately previous user turn, call `gate-cli cex earn staking swap`.
4. If parameters change after confirmation (amount, pid, coin), invalidate the old confirmation and re-confirm.
5. If confirmation is ambiguous, stale, or from a different context, do NOT execute — request fresh confirmation.

### Stake, redeem, and mint

- **Stake / Redeem**: Supported via `gate-cli cex earn staking swap`. Follow `references/staking-swap.md`. **pid** is required; use **side=0** (stake) or **side=1** (redeem); before stake, fetch products and if multiple protocols for the same coin, ask the user to confirm which product (pid) before calling the swap. All responses in English.
- **Mint**: Supported as **immediate stake**. When the user asks to mint, execute the **Stake** workflow: route to `references/staking-swap.md`, resolve pid and amount, call `gate-cli cex earn staking swap` with **side=0**. For GUSD, require the user to choose USDT or USDC and pass `coin`.
- **Cancel redeem**: Not supported. When the user asks to **cancel** or **revoke** a redeem (e.g. cancel a redemption order), reply **in English**: "Cancelling or revoking a redeem is not supported here; please use the Gate website or app if needed. I can help you query positions or order history." Do **not** call any tool.

### Errors

| Scenario | Action |
|----------|--------|
| Empty positions (`list` empty or totalCount 0) | "You don't have any staking positions. Browse available products to start earning." Suggest `references/staking-coins.md`. |
| No rewards yet | "No rewards found. Rewards typically start accruing 24 hours after staking." Optionally show positions from `gate-cli cex earn staking assets`. |
| Product not found / no capacity | Suggest alternatives from `gate-cli cex earn staking find` (e.g. by estimateApr). |
| API error / 401 | "Unable to fetch staking data. Please try again later." or "Please log in to view staking data." |
