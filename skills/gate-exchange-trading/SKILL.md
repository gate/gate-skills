---
name: gate-exchange-trading
description: "Gate Trading L2. Use when the user wants to execute complex trades, margin borrowing, or query positions and open orders. Triggers on 'market buy', 'margin borrow', 'TradFi', 'Alpha', or spot-plus-futures combos. Requires Action Draft."
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


# Gate Exchange Trading

This is an **L2 composite skill** for users who want a single skill to complete the full trading loop:

`judge the opportunity -> control risk -> produce order draft -> explicit confirmation -> execute -> verify/manage`

It is neither a pure research skill nor a pure execution skill. Its purpose is to provide a complete trading workflow inside one skill.

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only use the `gate-cli` commands explicitly listed in this skill.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

Before calling any named MCP tool, verify that the concrete tool name exists in the current runtime tool list. If a helper tool is absent, disclose the mismatch, use only the nearest valid fallback combination, and do not overclaim unavailable coverage such as rankings, macro breadth, or automated fund-flow tracing.

Also validate that the returned payload is rich enough for the intended analytical claim. If a tool returns sparse metadata, empty structures, or requires missing disambiguation inputs, treat it as supporting context only rather than primary evidence.

For portability across hosts, treat the documented `gate-cli cex …` commands as the baseline:

- `info_*` -> Gate Info MCP
- `news_feed_*` -> Gate News MCP
- read-only spot/futures market data -> `gate-cli cex spot market …` / `gate-cli cex futures market …` (public endpoints where applicable)
- private order / account / position flows -> authenticated `gate-cli` (**`GATE_API_KEY`** / **`GATE_API_SECRET`** and/or **`gate-cli config init`**; when **both** env vars are set on the host, **`config init`** is not required)

Do not make `news_events_*` a required dependency in scenario design, because it is not part of the documented baseline news surface.

## Execution mode

**Read and strictly follow** [`references/gate-cli.md`](./references/gate-cli.md), then execute this skill's trading workflow.

- `SKILL.md` keeps composite routing, trade lifecycle policy, and guardrails.
- `references/gate-cli.md` is the authoritative `gate-cli` orchestration contract for cross-domain tool sequencing, execution gates, and degradation.

---

Read `references/scenarios.md` for:

- representative user scenarios
- representative prompt examples
- expected tool-routing patterns

## Authentication

- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard for API key, secret, profiles, and defaults (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** **`gate-cli config init`** is **not** required when credentials are already supplied — e.g. **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** set on the host, or **`--api-key`** / **`--api-secret`** where supported — never ask the user to paste secrets into chat.
- API Key Required: Not always
- Read-only analysis: public `info_*`, `news_feed_*`, and some public `gate-cli cex spot market …` / `gate-cli cex futures market …` reads may work without authentication, depending on endpoint
- Execution and private account actions: Yes, authenticated Exchange MCP tools with the required API key permissions are mandatory
- Note: Do not block analysis-only use just because private execution tools are unavailable; only block when the requested action needs private trading/account access.

### Installation Check

- **Required:** `gate-cli` (install from [gate-cli releases](https://github.com/gate/gate-cli/releases) or via your environment’s Gate MCP / skills installer).
- Add the directory containing **`gate-cli`** to **`PATH`** when invoking by name.
- **Credentials:** When **`GATE_API_KEY`** and **`GATE_API_SECRET`** are both set (non-empty) for the host, **do not** require **`gate-cli config init`**. When **both** are unset or empty and private execution is needed, **remind** the operator to run **`gate-cli config init`** **or** to configure **`GATE_API_KEY`** / **`GATE_API_SECRET`** in the **matching skill** from the skill library (never ask the user to paste secrets into chat).
- **Sanity check:** Confirm the CLI works (e.g. **`gate-cli --version`** or a public **`gate-cli cex spot market …`** / **`gate-cli cex futures market …`** read) before private trading steps.

## Positioning

- For users who want to trade without switching across multiple skills
- Self-contained: can be installed alone and still understand both analysis and execution mapping
- Supports **spot trading** and **USDT perpetual futures**
- Supports post-trade **amend / cancel / close / verification**

## Suitable Scenarios

### Suitable

- The user already has a target asset and wants analysis before trading
  - `Check whether BTC is worth buying now, then give me a spot order draft`
  - `I want to long ETH, but check momentum, liquidation, and liquidity first`
- The user is triggered by news, abnormal moves, or new listings and wants to trade after analysis
  - `ETH just dumped. Explain why and tell me whether it is worth buying`
  - `This newly listed coin looks interesting. Check the risk before giving me a starter trade plan`
- The user already placed an order or opened a position and now wants management
  - `Raise my unfilled buy order by 1%`
  - `Close half of my BTC position`

### Not Suitable

- Pure market research with no trading goal
- Options, Alpha trading, on-chain swap, DeFi execution, copy trading, wealth products
- Fully automatic trading, skipping confirmation, bypassing compliance or risk controls

## Capability Boundary

### This skill can do

1. Recognize whether the user wants:
   - pre-trade judgment
   - judgment plus execution
   - order / position management
2. Dynamically combine analysis modules around one trade target:
   - market/news context
   - single-coin analysis
   - technical analysis
   - liquidity/slippage/liquidation/order-book analysis
   - token or contract risk check
3. Produce a **Trading Brief**
4. Produce an **Order Draft** when risk is acceptable
5. Execute after explicit confirmation:
   - spot buy/sell, conditional limit logic, amend/cancel/verification
   - USDT perpetual open/close/reverse/amend/cancel
6. Continue after execution:
   - fill verification
   - position verification
   - order / position management

### This skill cannot do

1. Decide and trade automatically on behalf of the user
2. Place orders without explicit confirmation
3. Bypass compliance, risk, minimum order, or contract safety constraints
4. Promise profit or present analysis as certainty
5. Pretend to support unsupported products

## Operating Principles

### Principle 1: Work around the trading goal

This skill is built for trading closure, not broad research.

- If the user only asks `How is the market?`
  - a lightweight market scan is fine
  - do not proactively move into order execution
- If the user says `How is the market today? Give me one trade idea`
  - a lightweight scan is allowed
  - but the workflow must narrow down to **one asset + one market (spot or futures)** before entering execution

### Principle 2: Judge first, execute second

Unless the user only wants pure order/position management, default to one round of pre-trade judgment before producing an order draft.

### Principle 3: Use the minimum necessary analysis

Do not run every module every time. Only call the modules needed for the current decision.

Read `references/routing-and-analysis.md` for:

- intent routing
- analysis module selection by scenario
- risk gating
- module-to-MCP mapping and call patterns

### Principle 4: Strong confirmation at execution layer

Any real trading action must follow this order:

1. Produce a `Trading Brief`
2. Produce an `Order Draft`
3. Wait for explicit confirmation in the immediately previous user turn
4. Execute only after confirmation

Read `references/execution-and-guardrails.md` for:

- spot and futures execution rules
- execution MCP mapping
- draft requirements
- confirmation rules
- hard and soft blocks

## Overall Workflow

### Step 0: Apply the shared runtime rules first

Before analysis or execution:

- read and follow [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- resolve any required runtime, update, or authorization gate before continuing
- verify that the named tools you plan to call exist in the current runtime before relying on them

### Step 1: Identify task mode

Classify the user request into one of these modes:

1. **Trade Decision**
   - analyze first, then decide whether to trade
2. **Trade Draft / Execute**
   - the user already wants to trade and wants analysis plus draft plus execution
3. **Order / Position Management**
   - the user wants to manage an existing order or position

### Step 2: Narrow down to one trade target

Before entering execution, try to make these explicit:

- asset: BTC / ETH / SOL / a new coin / a futures contract
- market: spot or USDT perpetual
- direction: buy / sell / long / short / close

If information is still incomplete:

- a lightweight market scan is allowed
- but before producing an order draft, the workflow must narrow down to one asset and one market

### Step 3: Build the pre-trade analysis package

Call only the modules needed for this request:

- market overview / news briefing
- listing / exchange announcement context
- single-coin analysis
- technical analysis
- event explanation
- risk check
- address tracing (only when the user really provides an address and wants tracing)
- liquidity / slippage / momentum / liquidation / basis / order-book analysis

### Step 4: Produce a Trading Brief

`Trading Brief` is the mandatory intermediate artifact before execution. It must include:

1. what the user wants to do
2. current market/asset judgment
3. key risks
4. whether the skill should continue to order drafting

Only three result states are allowed:

- `GO` = safe enough to continue to order drafting
- `CAUTION` = meaningful risk exists, but drafting may continue after warning
- `BLOCK` = do not continue into order drafting

### Step 5: Produce an Order Draft

Only produce an order draft when all of the following are true:

- the user has real trading intent
- the trade target is sufficiently clear
- no hard block is triggered

### Step 6: Wait for explicit confirmation

If the user does not provide a clear, immediate confirmation:

- do not execute
- remain in analysis / draft / query mode only

### Step 7: Execute and verify

After execution, always return:

- whether execution succeeded
- core fill/order/position results
- reasonable next actions, such as verify fill, amend, cancel, or close

## Market Identification Rules

### Default behavior

- If the request clearly contains `long / short / leverage / contract / perp / futures / open / close`
  - route to **USDT perpetual futures**
- If the request clearly contains `buy coin / sell coin / spot / buy BTC / sell ETH`
  - route to **spot**
- If the user says `buy BTC` without specifying market
  - default to **spot**
- If the user says `trade this move`
  - ask whether they want spot or USDT perpetual futures

## Recommended Output Rhythm

### Before execution

1. `Trading Brief`
2. if allowed: `Order Draft`
3. wait for confirmation

### After execution

1. `Execution Result`
2. if needed: `Next Actions`

## Special Rule for Order / Position Management

If the user asks for:

- amend order
- cancel order
- verify fill
- close half
- close all
- reverse

then the skill does not need to rerun the full research chain, but it still must:

- locate the correct target order or position
- apply the corresponding execution rules
- require strong confirmation for high-risk actions

## Risk Policy

### Hard blocks

Must stop immediately if:

- the user asks to skip confirmation
- the user asks to bypass compliance or risk controls
- the product is unsupported
- the asset is not tradable
- token security check shows a critical malicious risk

### Soft blocks

Warn but allow continuation if:

- liquidity is poor
- slippage is high
- funding is extreme
- crowding/liquidation risk is elevated
- a major event just hit and direction is unstable
- the coin is newly listed or still in price discovery

For soft blocks:

- surface the warning clearly in `Trading Brief`
- if the user still wants to continue, drafting is allowed
- confirmation is still mandatory

## Reading Order

1. Read `references/routing-and-analysis.md`
2. Read `references/execution-and-guardrails.md`
3. Execute only the modules needed for the current task; do not run the full stack by default
