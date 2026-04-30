---
name: gate-exchange-earn
version: "2026.4.29-3"
updated: "2026-04-29"
description: "Gate Smart Earn (L2) via gate-cli: Simple Earn, dual products, staking, yield compare, idle-fund ideas, subscribe/redeem with confirmation. Use this skill whenever the user asks about earn APY, flexible or fixed earn, dual investment, staking rewards, positions, or earn subscribe/redeem. Trigger phrases include earn, Simple Earn, dual investment, staking, flexible earn, fixed earn, subscribe earn, redeem earn, auto renew, APY compare."
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    emoji: "📈"
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

# Gate Smart Earn Assistant

## General Rules

本 L2 Skill 遵循公共运行时规则文件：

→ [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)（Gate Skills 通用运行时规则：CLI / 凭证检查、授权验证、版本检查）

→ [gate-skills-disambiguation.md](https://github.com/gate/gate-skills/blob/master/skills/gate-skills-disambiguation.md)（L1/L2 Skill 路由消歧规则）

⚠️ STOP — You MUST read and strictly follow **both** documents above before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
- **Only use the `gate-cli` commands explicitly listed in this skill.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

---

## Regulatory and safety notices

- This skill is intended for users aged 18 or above with full civil capacity.
- Digital asset products involve significant risk and may result in partial or total loss. Yields are indicative, not guaranteed.
- The above is for informational purposes only and does not constitute investment, financial, tax, or legal advice. AI-assisted outputs are for general information only and do not constitute any representation, warranty, or guarantee by Gate.
- Users must comply with the laws and regulations of their jurisdiction. Gate operates under licenses in multiple jurisdictions; see https://www.gate.com/gategroup/legal/licenses for the Gate licenses page.
- This skill processes user prompts and queries; operational data is sent to the Gate API through `gate-cli` on the user-controlled host. Do not paste API secrets into chat.

## Skill Dependencies

- **Before any `gate-cli` invocation:** ensure `gate-cli` is installed. Let `GATE_CLI_BIN="${GATE_OPENCLAW_SKILLS_BIN:-$HOME/.openclaw/skills/bin}/gate-cli"`. If **`[ ! -x "$GATE_CLI_BIN" ]`** (and `command -v gate-cli` also fails if you rely on `PATH`), **run** `setup.sh` (e.g. `sh ./setup.sh` from this skill directory), then re-check. **Do not** continue with authenticated earn reads or writes until `gate-cli` runs successfully (e.g. `gate-cli --version`).
- **No MCP servers** are required; execution is **`gate-cli` only** for the commands listed below and in `references/gate-cli.md`.

### gate-cli commands used

**Query operations (read-only)**

- `gate-cli cex earn uni rate`
- `gate-cli cex earn uni currency`
- `gate-cli cex earn uni records`
- `gate-cli cex earn uni interest`
- `gate-cli cex earn uni interest-records`
- `gate-cli cex earn fixed products`
- `gate-cli cex earn fixed products-asset`
- `gate-cli cex earn fixed lends`
- `gate-cli cex earn dual plans`
- `gate-cli cex earn dual orders`
- `gate-cli cex earn dual balance`
- `gate-cli cex earn staking find`
- `gate-cli cex earn staking assets`
- `gate-cli cex earn staking awards`
- `gate-cli cex earn staking orders`
- `gate-cli cex spot account list`
- `gate-cli cex spot account get`
- `gate-cli info compliance check-token-security`

**Execution operations (write; Action Draft + explicit Y required)**

- `gate-cli cex earn uni lend` (with `--json` for lend/redeem semantics per CLI help)
- `gate-cli cex earn uni change` (with `--json`, e.g. auto renew)
- `gate-cli cex earn fixed create` (with `--json`)
- `gate-cli cex earn dual place`
- `gate-cli cex earn staking swap`

### Authentication

- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** when **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** are set, or **`--api-key`** / **`--api-secret`** where supported, never ask the user to paste secrets into chat.
- **Permissions:** use an API key with scopes appropriate to earn and spot balance checks (e.g. earn read/write and spot read for pre-trade balance validation). Create a dedicated, least-privilege key when possible.
- **Portal:** manage keys outside the chat: https://www.gate.com/myaccount/profile/api-key/manage

### Installation check

- **Required:** `gate-cli` (install via `setup.sh` when missing, per Skill Dependencies).
- GateClaw / OpenClaw: `setup.sh` installs to `$HOME/.openclaw/skills/bin/gate-cli` by default; add that directory to **`PATH`** if agents invoke `gate-cli` by name.
- **Sanity check:** confirm a lightweight read succeeds where applicable before writes (for example earn product listing commands after credentials resolve).

## Execution mode

Read and strictly follow `references/gate-cli.md`, then execute this skill's routing and case logic.

- `SKILL.md` holds intent routing, signal model, and the case map.
- `references/gate-cli.md` is the authoritative execution contract for `gate-cli` usage, pre-checks, confirmation gates, and degraded handling.

## Domain knowledge

### Logical capability groups (L1 alignment)

| Logical module | Role in this L2 skill |
|----------------|----------------------|
| Simple Earn (flexible/fixed) | Product discovery, rates, positions, subscribe/redeem |
| Dual-currency (dual) | Plans, orders, balances, placement |
| Staking | Discover products, positions, rewards, participate |
| Spot account (subset) | Available balance checks before subscribe flows |
| Token security (info) | Optional risk signal when comparing products for a coin |

### Four-dimensional intent signals (non-exclusive)

| Signal | Dimension | Typical triggers | CLI subset (union with others) |
|--------|-----------|------------------|--------------------------------|
| S1 | Earn products | earn, Simple Earn, dual, staking, fixed, flexible | `cex earn` product/discovery commands |
| S2 | Yield, risk, compare | APY, APR, risk, which is better, compare; **product-side** **收益** (what products or markets pay—rates, tiers, “这个产品收益怎么样”) | `dual plans`, `staking find`, `check-token-security` |
| S3 | Positions and PnL | my earn, how much earned, positions, history; **持仓** **收益** (accrued interest/rewards on **my** holdings, earn PnL and history) | `uni records`, `dual orders`, `fixed lends`, `staking orders`, `staking assets` |
| S4 | Subscribe, redeem, configure | subscribe, redeem, join, auto renew, participate | balance reads then `uni lend`, `fixed create`, `dual place`, `staking swap`, `uni change` |

**收益 keyword:** When the query contains **收益** (or close synonyms such as 收益率 in a yield sense), **split S2 vs S3 before activating both:**
- **产品收益** (product yield): asks what a **product or listing** pays or how yields compare—APY/APR, annualized rate, which option is higher. → Activate **S2 only** for this angle; **do not** activate **S3** solely from this cue.
- **持仓收益** (position / holdings yield): asks how much **the user** has earned on existing positions—accumulated interest, rewards received, “我赚了多少”, bucketed PnL. → Activate **S3 only** for this angle; **do not** activate **S2** solely from this cue.

Other signals (e.g. S1, S4) still activate from their own cues independently.

**Defaulting:** broad earn browse with little specificity activates S1+S2. Vague “how much did I earn” style queries bias toward S3. If **收益** is present but product vs 持仓 is ambiguous, prefer one short clarifying question; if a default is required, bias toward **S3** when the wording implies **my** holdings (e.g. 我 / 我的 / 累计 / 持仓) and toward **S2** when it implies **catalog or quoted rates** (e.g. 哪个 / 年化 / 产品对比).

**Execution mode:** S1/S2/S3 without S4 is research-only (fetch and summarize). If **S4** is active, use research plus **Action Draft**, then execute writes only after explicit **Y** in the immediately previous user turn.

### Out of scope (route elsewhere)

- Spot/perpetual/options **trading** execution (buy/sell on the book) → trading copilot / `gate-exchange-spot` or futures skills.
- New-listing research, listing alerts → dedicated listing/research skills.
- Broad market or single-coin **non-earn** research → market research / info research skills.
- Full account risk (liquidation, margin) unrelated to earn positions → account or unified-account skills.

### Presentation rules

- When the user asks for **separate** earn buckets (for example flexible interest vs staking rewards), present **sections per product**; do **not** merge into a single “total profit” line unless they explicitly ask for a total.
- For that style of query (including **「余币宝利息 / 质押奖励分别赚了多少」**), **default analysis/export window is the trailing ~three months**: use **`now − 90 days` through `now`** for `--from` / `--to` (Unix ms per CLI) on time-filterable reads (e.g. `uni interest-records`, `uni records`). Say the window in the reply. Use **full-history** cumulative APIs or unpaginated totals **only** if the user asks for lifetime / 全部 / 累计历史等.
- For dual and similar products, present APY in human-readable percent form when the API returns a fraction (for example multiply by 100 for display when that matches CLI output semantics); state assumptions if ambiguous.
- Do not promise fixed returns; label estimates and floating yield clearly.

## Workflow

When the user asks for any earn-related operation, follow this sequence.

### Step 1: Route intent (earn vs non-earn)

If the request is clearly **not** about earn, staking, dual, flexible/fixed savings, or idle-fund **earn** allocation, route to the appropriate non-earn skill instead of forcing earn CLI.

### Step 2: Extract parameters and activate signals

Extract where possible: `product_type` (simple / dual / staking), `currency`, `amount`, `term` or `days`, `risk_preference`, and whether the user wants a **write** (S4). If the query contains **收益**, apply the **产品收益 → S2 only / 持仓收益 → S3 only** split before merging signal CLI sets.

### Step 3: Build the CLI set

- Union CLI from each activated signal (see Domain knowledge).
- Deduplicate identical command lines with identical arguments.
- Run independent reads in parallel when safe; serialize writes to one confirmed action at a time.

### Step 4: Preflight reads and synthesis

- For writes (S4), always check **available balance** with `gate-cli cex spot account list` or `gate-cli cex spot account get` as appropriate before drafting.
- Follow `references/gate-cli.md` §2.1 (`--help` before required flags) for every leaf command.

### Step 5: Action Draft and confirmation for any write (mandatory)

Before **`gate-cli cex earn uni lend`**, **`gate-cli cex earn uni change`**, **`gate-cli cex earn fixed create`**, **`gate-cli cex earn dual place`**, or **`gate-cli cex earn staking swap`**:

1. Present an **Action Draft** (product type, currency, amount, indicative APR or terms, material risks including dual exercise/settlement risk where relevant).
2. Ask for **Y** to confirm or **N** to cancel. Treat confirmation as **single-use**; parameter or intent changes require a new draft.
3. Execute the write only after **Y** in the immediately previous user turn.
4. On failure, do **not** auto-retry writes; surface the error and suggest App/Web or corrected parameters.

### Step 6: Result and verification

- After writes, verify with the matching read commands (records, orders, lends, staking orders) when useful.
- If a read fails, degrade gracefully: state which dimension is unavailable; never fabricate balances or APY.

## Case routing map (1–15)

| Case | User intent | Core decision | Tool sequence (abbrev.) |
|------|-------------|---------------|-------------------------|
| 1 | Idle capital, low risk, best earn mix | Rank conservative products across types | Parallel: `fixed products`, `fixed products-asset`, `uni rate`, `uni currency`, `dual plans` → synthesized report |
| 2 | Compare dual vs staking for a coin | Compare APR, lock/exercise narrative, optional `check-token-security` | `dual plans` + `staking find` + optional `check-token-security` |
| 3 | Portfolio review and better products | Positions then market scan | `uni records`, `dual orders`, `fixed lends`, `staking orders` → recommendations; writes only after draft + Y |
| 4 | Staking detail and participate | Explain terms then optional `staking swap` | `staking find` + spot balance read → draft → `staking swap` after Y |
| 5 | Auto renew / roll strategy | Identify renewable rows then `uni change` if user confirms | Position reads → draft → `uni change --json` after Y |
| 6 | Flexible rate and min rate | Quote flexible parameters | `uni rate`, `uni currency` |
| 7 | Fixed products for asset sorted by yield | List and sort fixed offers | `fixed products-asset` |
| 8 | Staking discovery high yield | List and sort staking | `staking find` |
| 9 | Dual plans filter (e.g. sell-high BTC) | Filter plans by currency and product type | `dual plans` |
| 10 | Cross-type APR comparison | Side-by-side table with footnotes on methodology | `uni rate`, `uni currency`, `fixed products-asset`, `staking find` |
| 11 | Separate PnL by earn type | No cross-section totals unless asked; **default window ~last 3 months** (`--from`/`--to` ≈ 90d); lifetime only on explicit ask | Sum/fetch per bucket: `uni interest-records` (+ `uni records` if needed) with time filter for flexible; `staking awards` (paginate; filter by row timestamps if CLI has no `--from`/`--to`); `staking assets` for position snapshot; `uni interest` only for **lifetime** per-currency totals when user asks |
| 12 | Subscribe flexible (e.g. USDT) | Balance + rules then lend | spot balance + `uni currency` → draft → `uni lend --json` after Y |
| 13 | Subscribe fixed term | Pick tenor from products | `fixed products-asset` + spot balance → draft → `fixed create --json` after Y |
| 14 | Redeem flexible slice | Check redeemable then redeem | `uni records` → draft → `uni lend --json` redeem after Y |
| 15 | Dual settled history | Filter settled dual orders and summarize by currency | `dual orders`, `dual balance` |

## Judgment Logic Summary

| Condition | Action |
|-----------|--------|
| Query contains **收益** | Classify **产品收益** → **S2 only** (that angle); **持仓收益** → **S3 only** (that angle); never activate both S2 and S3 solely from the same undifferentiated 收益 mention |
| User asks for earn yields, products, or comparisons without subscribe/redeem | S1/S2/S3 only; read documented `gate-cli` commands; no writes |
| User asks to subscribe, redeem, join staking, place dual, or change auto renew | Activate S4; complete reads then **Action Draft**; **no** write without **Y** |
| User mixes trading (“market buy BTC”) with earn | Route trading to spot/trading skills; handle earn portions only if clearly separable |
| `check-token-security` returns empty or errors | Skip or label “risk data unavailable”; do not block read-only browsing solely for that |
| User wants bucketed earn PnL | Use Case 11 pattern; separate sections; **default data scope = ~last 90 days** unless user asks for all-time |
| Stale or ambiguous confirmation | Re-issue Action Draft; do not execute writes |
| Multi-step writes (e.g. redeem then subscribe) | Require **separate** confirmation per write leg |

## Report template

```markdown
## Earn Result

| Item | Value |
|------|-------|
| Scenario | {case_name} |
| Product | {product_type} |
| Currency | {currency} |
| Status | {status} |
| Key metrics | {apr_or_amounts} |

{decision_text}
```

Example `decision_text`:

- `Action Draft: Flexible USDT earn, amount 2000 USDT, indicative APR {x}%, risks: floating yield. Reply Y to confirm or N to cancel.`
- `Read-only summary: top fixed USDT terms sorted by APR (see table). No subscription executed.`
- `Not executed: available balance below requested amount.`

## Error handling

| Error type | Typical cause | Handling strategy |
|------------|---------------|-------------------|
| Insufficient balance | Not enough spot available for subscription | Show shortfall; suggest lower amount or funding |
| Product unavailable | Tenor sold out or currency unsupported | Explain; refresh product list |
| Auth or permission failure | Key missing earn or spot read scope | Stop writes; guide credential and scope fix |
| Missing confirmation | User did not send Y | Keep draft pending; reads only |
| Stale confirmation | Parameters changed since Y | Invalidate; re-draft |
| CLI partial failure | One parallel read fails | Continue other dimensions; label gaps |
| Write failure | Exchange rejects order | No auto-retry; show message; suggest App/Web |

## Safety rules

- Never call earn **write** commands without a prior **Action Draft** and explicit **Y** in the immediately previous user turn.
- Dual-currency products carry exercise/settlement risk; state that plainly before any `dual place` confirmation.
- Do not guarantee returns or imply zero risk.
- Invalidate confirmation after any material change to amount, currency, product, or side.
- Prefer `--format json` for machine parsing when the host workflow requires it (optional per operator policy).

## Cross-skill workflows

- **Fund spot then earn:** user may need spot transfer or deposit skills first if spot balance is insufficient (this skill only checks and reports).
- **Trading after redeem:** after successful redeem to spot, trading skills may apply; do not conflate order placement with earn writes.
