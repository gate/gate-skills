---
name: gate-exchange-newcoin
version: "2026.4.29-1"
updated: "2026-04-29"
description: "New listing DD and event radar via gate-cli (info/news/cex): listings, fundamentals, risk, sentiment, tape, LaunchPool calendar; optional first spot/Alpha order after Action Draft + Y/N. Use this skill whenever the user asks about new listings, pre-listing research, launchpool, rug checks, or a first buy on a new asset. Trigger phrases include 'new listing', 'due diligence new coin', 'launchpool calendar', 'listing announcement', 'is it a rug', 'first buy spot'."
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    emoji: "🆕"
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

# New Coin Due Diligence and Event Radar (New Coin Radar)

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read `./references/gate-runtime-rules.md`
- **Only use the `gate-cli` commands explicitly listed in this skill.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

---

## Skill Dependencies

- **Before any `gate-cli` invocation:** ensure `gate-cli` is installed. Let `GATE_CLI_BIN="${GATE_OPENCLAW_SKILLS_BIN:-$HOME/.openclaw/skills/bin}/gate-cli"`. If **`[ ! -x "$GATE_CLI_BIN" ]`** (and `command -v gate-cli` also fails if you rely on `PATH`), **run** [`setup.sh`](./setup.sh) (e.g. `sh ./setup.sh` from this skill directory), then re-check.
- **No MCP servers** are required for this skill; execution is **`gate-cli` only** (see published mapping: [gate-cli](https://github.com/gate/gate-cli)).

### gate-cli commands used (deduplicated minimal set)

**Query operations (read-only)**

- `gate-cli info coin get-coin-info`
- `gate-cli info compliance check-token-security`
- `gate-cli info onchain get-address-info` (when the user supplies an explicit on-chain address and chain context)
- `gate-cli news feed get-exchange-announcements`
- `gate-cli news events get-latest-events`
- `gate-cli news feed search-news`
- `gate-cli news feed get-social-sentiment`
- `gate-cli cex launch projects`
- `gate-cli cex spot market ticker`
- `gate-cli cex spot market orderbook`

**Execution operations (write; API credentials required)**

- `gate-cli cex spot order buy` / `gate-cli cex spot order sell`
- `gate-cli cex alpha order place` (for Alpha market workflows; prefer `gate-cli cex alpha order quote` first when available per [`gate-cli` Alpha docs](https://github.com/gate/gate-cli))

### Authentication

- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** **`gate-cli config init`** is **not** required when credentials are already supplied — e.g. **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** set — never ask the user to paste secrets into chat.
- **Permissions:** Read flows use public `info` / `news` CLI paths; **`cex` market reads** typically do not require keys; **order placement** requires **`Spot:Write`** (spot) and appropriate Alpha permissions for **`cex alpha`** writes.
- **Portal:** create or rotate keys outside the chat: https://www.gate.com/myaccount/profile/api-key/manage

### Installation check

- **Required:** `gate-cli` (install via [`setup.sh`](./setup.sh) when missing).
- **Sanity check:** Confirm `gate-cli --version` before relying on scripted flows.

## Execution mode

**Read and strictly follow** [`references/gate-cli.md`](./references/gate-cli.md), then execute routing, signal detection (S1–S5), and confirmation gates in this file.

- `SKILL.md` holds intent routing, signal definitions, Action Draft rules, and degradation policy.
- `references/gate-cli.md` is the authoritative execution contract for flags, parallelism, JSON output preference, and write gates.

## Domain knowledge

### Scope and routing

| Topic | Route here | Route elsewhere |
|-------|----------------|-----------------|
| New listings, upcoming listing research, LaunchPool calendars, first-order new coin context | This skill | — |
| Mature large-cap research / broad market research without new-coin framing | — | `gate-info-research` or single-dimension `gate-info-*` |
| Routine spot trading without new-listing angle | — | `gate-exchange-spot` |
| DEX on-chain swap | — | DEX wallet / trade skills |

### Research signals (S1–S4) and execution signal (S5)

| Signal | Dimension | Typical triggers | CLI subset |
|--------|-------------|-------------------|------------|
| S1 | New listing / calendar | listing, launchpool, new coin on exchange | `gate-cli news feed get-exchange-announcements`, `gate-cli cex launch projects` |
| S2 | Fundamentals / DD | diligence, tokenomics, project background | `gate-cli info coin get-coin-info`, `gate-cli news feed search-news` |
| S3 | Risk / safety | rug, honeypot, scam, contract safety | `gate-cli info compliance check-token-security`, optional `gate-cli info onchain get-address-info` |
| S4 | Heat / events / tape | pump, news, sentiment, tape | `gate-cli news events get-latest-events`, `gate-cli news feed get-social-sentiment`, `gate-cli cex spot market ticker`, `gate-cli cex spot market orderbook` |
| S5 | First-order execution (write) | **`buy_intent=true`** orthogonal to S1–S4 | **`gate-cli cex spot order buy|sell`**, **`gate-cli cex alpha order place`** only after Action Draft **and** user **Y** |

**`buy_intent` rules**

- **`true`:** User expresses a trading mandate (buy, sell, place order, market/limit, first fill, etc.) for spot or Alpha in a new-coin context.
- **`false`:** Pure research, comparison, calendar, or risk opinion with no order mandate.
- **Ambiguous execution:** If intent is true but **symbol**, **pair**, or **size** is missing, ask clarifying questions; **do not** call write CLIs until parameters match the draft and the user confirms **Y**.

### Fallback activation

- If the query names a **symbol** but no signal matches: default **S2** (fundamentals).
- If the query is generic “what is new” without a symbol: default **S1 + S4** (listings + heat).

### Parallelism

- **Parallel:** Commands that do not depend on each other’s stdout (within the same read phase).
- **Serial:** Extract symbols from announcements **then** per-symbol fan-out; **never** parallelize write CLIs with unrelated reads in the same confirmation round.
- Prefer **`--format json`** on supported subcommands when parsing structured fields.

## Workflow

### Step 1: Intent gate

Confirm the user is in **new coin / listing / launch / DD / first-order** context. If the request is clearly **only** mature-cap spot trading with no new-listing angle, prefer **`gate-exchange-spot`**.

### Step 2: Extract parameters and signals

Extract:

- `symbol[]` (0..N)
- `time_range` (default **24h** where applicable)
- **`buy_intent`** (bool)
- Activated signals **S1–S4** (independent toggles)
- **S5** iff **`buy_intent=true`**

Apply fallback rules when no signal would otherwise activate.

### Step 3: Assemble read-phase CLI set

Compute **CLI set = union** of CLIs for all activated **S1–S4** branches; **deduplicate**. Run read phase **before** any write.

### Step 4: Synthesize

Merge outputs; **do not** fabricate missing fields. If sources disagree, present **separate bullets** instead of a single contradictory sentence. Include mandatory **informational disclaimer** (not investment advice; see **Report Template**).

### Step 5: Execution branch (S5 only)

If **`buy_intent=false`:** deliver structured research only.

If **`buy_intent=true`:**

1. Ensure minimum research for safety: at least **S3** plus **one of S2/S4** when data is available; if the user insists on minimal execution, document elevated risk in the Action Draft.
2. Produce **Action Draft** (pair, side, type, amount semantics, estimated price/cost, fees, liquidity/slippage warning, new-asset risk note).
3. Wait for explicit **Y** / **N** on **that** draft **only**.
4. On **Y**, call **`gate-cli cex spot order buy|sell`** or **`gate-cli cex alpha order place`** as documented. **Never** place orders without step 2–3.
5. On failure: **do not auto-retry** writes; surface error text and suggest App/Web follow-up.

## Case routing map

| # | User intent (summary) | Signals | Read-phase focus | Write |
|---|----------------------|---------|------------------|-------|
| 1 | Screen recent listings for safer, hotter candidates | S1, S2, S3; S5 only after explicit buy | Announcements + news search; per symbol compliance + coin info + sentiment | Spot/Alpha after Y |
| 2 | Pre-listing diligence for a named asset | S1, S2 | Announcements search + coin info + compliance | No |
| 3 | Sharp move: scam check and chase decision | S3, S2, S1, S4, S5 | Events + compliance + coin info; optional address tools | Spot/Alpha after Y |
| 4 | Weekly launchpool / launch calendar with risk labels | S1, S2 | Launch announcements + `cex launch projects`; per-project coin + compliance | No |
| 5 | Sector narrative coin: fundamentals + tape + optional buy | S2, S1, S4, S5 | Coin info + news + ticker (+ orderbook if needed) | Spot/Alpha after Y |
| 6 | Monitor listing tape and place first limit | S1, S4, S5 | Announcements + ticker (poll responsibly); draft limit | Spot/Alpha after Y |

## Judgment logic summary

| Condition | Action |
|-----------|--------|
| Mature-cap only, no listing context | Route away from this skill |
| `buy_intent=false` | Read-only union of S1–S4; **no** `cex` order CLIs |
| `buy_intent=true` | Complete read synthesis **then** Action Draft **then** **Y** **then** write CLIs |
| User said “should I buy?” without order verbs | Treat as **`buy_intent=false`** until they issue an order mandate |
| Missing symbol for execution | Ask; **block** writes |
| Conflicting CLI results | Split conclusions; label unknowns |
| Write failure | Report once; no silent retry |

## Report template

```markdown
## New Coin Radar Report

**Disclaimer:** This output is for informational purposes only and does not constitute investment, financial, tax, or legal advice. Digital asset trading involves significant risk and may result in partial or total loss. AI-assisted outputs are for general information only and do not constitute any representation, warranty, or guarantee by Gate.

### Signals activated
- S1 .. S4: ...
- buy_intent: ...

### Findings
- Listings / calendar: ...
- Fundamentals: ...
- Risk / compliance: ...
- Events / sentiment / tape: ...

### Decision support (not advice)
- ...

### Action Draft (only if buy_intent=true)
- Order type, pair, amount, estimated price/fee, risk notes
- Confirm with **Y** to proceed or **N** to cancel

### Execution result (only after Y)
- Status: ...
```

## Error handling

| Error type | Handling |
|------------|----------|
| Announcement CLI unavailable | Skip listing dimension; state data gap |
| Compliance empty / partial | Keep going; flag “risk data incomplete” in Draft |
| Order rejected | Show error; suggest parameter fix; **no** auto-retry |
| Missing confirmation | Reads only |

## Safety rules

- **No** write without Action Draft + **Y** in the immediately prior turn for **that** draft.
- **No** skipping liquidity/volatility warning for new listings.
- Single-use confirmation: parameter change **invalidates** prior **Y**.
- This skill is intended for users **aged 18+** with full civil capacity.

## Privacy

- Prompts and trade instructions may be processed by the host AI and sent to Gate APIs through **`gate-cli`** per your environment. Do not paste secrets into chat.

## Cross-skill workflows

- **Deep spot management** after first fill: hand off to **`gate-exchange-spot`** for amendments, triggers, and full position workflow.
- **Pure research** without execution: can use **`gate-info-research`** when the query is broad multi-dimension research not specific to listings.
