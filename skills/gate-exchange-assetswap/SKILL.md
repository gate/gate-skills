---
name: gate-exchange-assetswap
description: "Use this skill whenever the user wants Gate Exchange asset allocation optimization for spot holdings (list eligible assets, load config, evaluate/preview, place orders, query history). Trigger phrases include \"asset allocation optimization\", \"allocation configuration\", \"portfolio allocation\", \"rebalance spot to stablecoin\", \"Top 5 market cap allocation\", \"optimize holdings to BTC\", \"preview allocation optimization\", \"allocation optimization order list\"."
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


# Gate Exchange Asset Allocation Optimization

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only use the `gate-cli` commands explicitly listed in this skill.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

## Skill Dependencies


### gate-cli commands used

**Query operations (read-only, profile scope)**

- `cex_assetswap_list_asset_swap_assets` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)
- `cex_assetswap_get_asset_swap_config` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)
- `cex_assetswap_evaluate_asset_swap` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)
- `cex_assetswap_list_asset_swap_orders_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)
- `cex_assetswap_get_asset_swap_order_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)

**Execution operations (write, trade scope)**

- `cex_assetswap_preview_asset_swap_order_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)
- `cex_assetswap_create_asset_swap_order_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)

### Authentication

- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard for API key, secret, profiles, and defaults (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** **`gate-cli config init`** is **not** required when credentials are already supplied — e.g. **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** set on the host, or **`--api-key`** / **`--api-secret`** where supported — never ask the user to paste secrets into chat.
- API Key required: Yes
- **Permissions:** Profile (read) for listing, config, evaluation, and order queries; Trade for preview and order creation
- **Portal:** create or rotate keys outside the chat: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check

- **Required:** Gate (main) MCP with asset allocation optimization (`cex_assetswap_*`) tools enabled; **`gate-cli`** when using CLI-backed flows.
- **Install (MCP / IDE):** `gate-mcp-cursor-installer`, `gate-mcp-codex-installer`, `gate-mcp-claude-installer`, or `gate-mcp-openclaw-installer`.
- **Credentials:** When **`GATE_API_KEY`** and **`GATE_API_SECRET`** are both set (non-empty) for the host, **do not** require **`gate-cli config init`**. When **both** are unset or empty, **remind** the operator to run **`gate-cli config init`** **or** to configure **`GATE_API_KEY`** / **`GATE_API_SECRET`** in the **matching skill** from the skill library (never ask the user to paste secrets into chat).
- **Sanity check:** Before preview or order creation, confirm the runtime works (e.g. **`gate-cli --version`** or deployment-specific checks).

---

## Trigger Conditions

Activate this skill when the user wants any of the following:

- Multi-asset spot **portfolio optimization** or **rebalancing** into a **strategy** (conservative stablecoin, conviction single asset, or market-cap-weighted basket)
- To see which spot balances are **eligible** for asset allocation optimization
- **Preview** estimated execution, slippage, or risk hints before committing
- **Submit** an asset allocation optimization order after confirmation
- **Query** historical allocation optimization orders or **one order’s** status and child orders

Do **not** use this skill for: transfers between accounts or products, Launchpool or earn subscriptions, single manual spot limit/market orders without the allocation product, or dust handling below product thresholds (route to the appropriate transfer, earn, spot, or small-balance product skill instead).

---

## Data privacy and collection

- **AI interaction information**: User prompts, follow-up instructions, and tool arguments used while following this skill qualify as AI interaction data under the [Gate Privacy Policy](https://www.gate.com/legal/privacy-policy) (see §4.2.7). Do not ask for or repeat API keys, secrets, or unrelated personal data in user-visible output.
- **Data flow**: Account and trading data for this skill flow **only** through the configured **Gate (main) MCP** to **Gate Exchange APIs** via the `cex_assetswap_*` tools listed above. Do not relay the same data to undocumented third-party services, scrapers, or custom backends as part of this workflow.
- **Minimization**: Pass only parameters required by each documented MCP call (symbols, amounts, strategy fields, pagination). Do not send full chat transcripts or unrelated context fields into tool payloads.

---

## Domain Knowledge

**Product**: Asset Allocation Optimization exposes Exchange capability for restructuring multiple spot holdings into a target mix. One optimization may map to multiple internal execution legs at the order layer.

**Strategy types** (conceptual; exact enums and parameters come from `cex_assetswap_get_asset_swap_config` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)):

| Strategy | Typical targets | Meaning |
|----------|------------------|---------|
| Conservative | USDT, GUSD, USDC (examples) | Consolidate into a single stablecoin; risk-off / idle cash posture |
| Conviction ("faith") | BTC, ETH, GT (examples) | Reallocate selected spot toward target weights in the chosen asset(s); intermediate steps follow the product and API |
| Market cap | Top 2, Top 5 (examples) | Index-like exposure weighted by market cap into a basket such as BTC, ETH, SOL, BNB, XRP (actual list from API) |

**Listing rules** (for agent interpretation; product may filter server-side):

- Default presentation may exclude major reserve assets (e.g. BTC, ETH, USDT, USDC) unless the user explicitly asks to include them in the sell set.
- Only **spot available** balances participate; locked balances from earn, borrow, staking, or similar are out of scope.
- Very small balances (e.g. below roughly USD 10 equivalent) may be hidden or routed to small-balance handling; exact thresholds follow API or product rules.

**Out of scope for public skill documentation** (do not document as standard Exchange MCP capabilities):

- Banner or UI-only feature flags
- Non-standard semantic "validate and fill parameters" helpers not published as Exchange MCP

**Rate limiting**: Align with wallet or Exchange API limits when documented (example: 200 requests per 10 seconds per user or key); confirm in published API docs.

**Preview → create payload (mandatory for agents)**:

- After a successful `cex_assetswap_preview_asset_swap_order_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二), construct the `cex_assetswap_create_asset_swap_order_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) body from the preview response **`data.order`** only: for each object in **`data.order.from`** and **`data.order.to`**, emit `{ "asset": <value>, "amount": <value> }` using the preview’s **`asset`** and **`amount`** string fields (use **`amount`**, not **`amount_show`**, unless published API docs say otherwise).
- Preserve the **array order** of `to` (and `from` if multiple legs) exactly as returned in `data.order`; do not reorder symbols for convenience.
- A preview request may use **`ratio`** on `to`; the **create** call must still use the **resolved `asset` + `amount`** legs from the preview output. Creating with ratio-only `to` while omitting preview amounts often yields quote errors (for example `code: 4`).
- If the API returns additional preview-bound fields (for example top-level `usdt_evaluated_value` or `transaction_fee` inside `data`), mirror them on create **when the MCP or Exchange docs require it**; otherwise the `from` / `to` legs from preview are the primary contract.

**Main chain (mandatory order for placement)**:

1. Case 1 — list eligible assets  
2. Case 2 — get strategy and parameter configuration  
3. Case 3 — pre-trade evaluation and preview (3a optional, 3b strongly required or mandatory per product rules)  
4. Case 4 — create order after explicit user confirmation of preview  

Do **not** jump from Case 2 to Case 4 without Case 3b preview unless product rules explicitly allow it.

**Supplemental queries** (do not reorder the main chain):

- Case 5 — paginated order list  
- Case 6 — single order detail  

**Order states** (examples): configuring, completed, partially completed, failed — use API field names and values from responses.

**Tool scope summary**:

| Tool | Type | Scope |
|------|------|--------|
| `cex_assetswap_list_asset_swap_assets` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) | Read | profile |
| `cex_assetswap_get_asset_swap_config` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) | Read | profile |
| `cex_assetswap_evaluate_asset_swap` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) | Read | profile |
| `cex_assetswap_list_asset_swap_orders_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) | Read | profile |
| `cex_assetswap_get_asset_swap_order_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) | Read | profile |
| `cex_assetswap_preview_asset_swap_order_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) | Write | trade |
| `cex_assetswap_create_asset_swap_order_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) | Write | trade |

**Compliance**: Restricted regions, KYC, and disabled accounts are enforced by the API. On compliance errors, relay the message and stop; do not promise outcomes the platform does not guarantee.

**Agent must not**: guarantee PnL, VIP tier level changes, or bypass eligibility rules.

---

## Workflow

### Step 1: Resolve user goal and route requests outside asset allocation optimization

Classify the request as: (A) discovery only, (B) full optimization through preview and optional order, (C) history or single-order status.

From the **user message and session context only**, infer intent and routing. Do **not** call any `cex_*` MCP tool in this step. If the user wants a **single** conventional spot order, **transfer**, **grid bot**, or **earn** action, stop using this skill and route to the appropriate Gate Exchange skill.

Key data to extract:

- `goal`: `list_only` | `evaluate_only` | `preview` | `place_order` | `order_list` | `order_detail`
- `strategy_hint`: conservative | conviction | market_cap | unknown (confirm via config)
- `symbols_or_scope`: which assets the user wants to include or exclude

### Step 2: Case 1 — List assets eligible for optimization

Call `cex_assetswap_list_asset_swap_assets` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with: parameters per MCP and API documentation (no undocumented fields).

Key data to extract:

- `eligible_assets`: symbols, available amounts, valuation hints returned by the API
- Whether the user must narrow the set for the next steps

### Step 3: Case 2 — Load configuration

Call `cex_assetswap_get_asset_swap_config` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with: no required body unless the API specifies optional filters; obtain allowed strategies, targets, limits, and precision rules.

Key data to extract:

- `allowed_strategies` and parameter shapes for TopN, target asset, and limits
- Constraints the agent must enforce when building the next request payload

### Step 4: Case 3a — Evaluation (optional)

When the user needs a quick estimate before final parameters, or while iterating on strategy choice:

Call `cex_assetswap_evaluate_asset_swap` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with: payload required by the API for the selected assets and strategy.

Key data to extract:

- `evaluation_summary`: estimated notionals or other returned metrics
- Any warnings or validation errors

### Step 5: Case 3b — Preview order (required before create in normal flow)

After the user confirms the asset set and strategy parameters:

Call `cex_assetswap_preview_asset_swap_order_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with: candidate selection and strategy fields per API docs.

Present preview outputs clearly: estimated fills, slippage or risk hints, and any server-side notices. Obtain **explicit user confirmation** after preview before Step 6.

If the market moves or the preview expires, repeat Step 5 (and Step 4 if needed) before creating an order.

Key data to extract:

- `preview_reference_fields`: any quote, token, or expiry fields required for Step 6 (follow response schema exactly)
- `create_from_legs`: copy of `data.order.from` reduced to `{ asset, amount }` per element (from preview **`amount`**, not `amount_show`)
- `create_to_legs`: copy of `data.order.to` reduced to `{ asset, amount }` per element, **same order** as preview
- `user_confirmed`: boolean — must be true to proceed

### Step 6: Case 4 — Create optimization order

Only after successful preview and explicit confirmation:

Call `cex_assetswap_create_asset_swap_order_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with: JSON body whose **`from`** is `create_from_legs` and **`to`** is `create_to_legs` from Step 5 (each leg **`asset` + `amount`** from `data.order`). Add any other preview-bound fields required by the API (for example values under `data` such as `usdt_evaluated_value` or `transaction_fee`) only when documentation or repeated failures indicate they are required. Do **not** substitute ratio-only `to` for this step when the preview already returned concrete `amount` per target asset.

Key data to extract:

- `order_id` or equivalent identifier
- Initial status and timestamps
- Next-step guidance (poll detail or show history)

### Step 7: Case 5 — List orders (supplemental)

When the user asks for recent history:

Call `cex_assetswap_list_asset_swap_orders_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with: pagination parameters per API (for example recent months as defined by product).

Key data to extract:

- `orders[]`: identifiers, statuses, created times
- Pagination cursors or flags if present

### Step 8: Case 6 — Order detail (supplemental)

When the user supplies an order id or picks one from a list:

Call `cex_assetswap_get_asset_swap_order_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with: `order_id` string per MCP and API documentation.

Key data to extract:

- Aggregate status and per-child order states if returned
- Amounts consumed and received as returned by the API

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Preview expired or price invalid | Re-run `cex_assetswap_preview_asset_swap_order_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) (and evaluation if needed); explain briefly |
| Create returns quote error after successful preview | Confirm create body uses **`asset` + `amount`** from `data.order.from` / `data.order.to` (preview order preserved); re-preview and retry; avoid ratio-only `to` if preview returned amounts |
| Insufficient available balance | Stop create; ask user to free balance or adjust selection |
| Rate limit | Back off and retry later; show the API message |
| Compliance or region block | Stop; relay compliance message; do not retry with workarounds |
| Partial completion | Report actual status from `cex_assetswap_get_asset_swap_order_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二); no guaranteed completion time |

---

## Safety Rules

- **Trading risk**: Digital asset trading involves significant risk and may result in partial or total loss of your investment. See the [Gate Risk Disclosure](https://www.gate.com/legal/risk-disclosure) and [User Agreement](https://www.gate.com/legal/user-agreement).
- Never call `cex_assetswap_create_asset_swap_order_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) without a successful preview and clear user confirmation of preview contents, except where the user’s own explicit one-shot authorization is defined by runtime rules for this product (default: require confirmation).
- Never build the create payload with ratio-only target legs when the preview response already includes **`data.order.to`** entries with **`amount`**; use those **`asset` + `amount`** pairs (and matching `from` legs) for create.
- Never fabricate order IDs, preview tokens, or success when the API returned an error.
- Display rates and amounts as estimates until execution; final settlement is authoritative.
- Do not expose API keys or secrets in user-visible output.

---

## Judgment Logic Summary

| Condition | Action |
|-----------|--------|
| User wants eligible spot assets for portfolio optimization | Case 1 only (`cex_assetswap_list_asset_swap_assets` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)) |
| User needs strategy options or limits | Case 2 (`cex_assetswap_get_asset_swap_config` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)) |
| User wants a quick estimate | Case 3a (`cex_assetswap_evaluate_asset_swap` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)) |
| User is ready to see executable preview | Case 3b (`cex_assetswap_preview_asset_swap_order_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)) |
| User confirmed preview | Case 4 (`cex_assetswap_create_asset_swap_order_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)) |
| User asks for past optimizations | Case 5 (`cex_assetswap_list_asset_swap_orders_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)) |
| User asks for one order’s progress | Case 6 (`cex_assetswap_get_asset_swap_order_v1` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)) |
| User wants single spot order or grid bot | Route out of this skill |
| Preview failed or expired | Re-preview; do not create |

---

## Report Template

```markdown
## Asset allocation optimization

**Goal**: {list | evaluate | preview | order placed | history | detail}

**Eligible assets (summary)**: {N} items, {optional total valuation if API provides}

**Strategy**: {conservative | conviction | market_cap | from API}

**Preview** (if run):
- Key figures: {from API}
- Create legs (if placing order): {`from`/`to` as `asset`+`amount` from `data.order`}
- Risk or slippage notes: {from API}

**Order** (if created):
- Order ID: {id}
- Status: {status}

**History / detail** (if queried):
- {table or bullet list from API}

**Disclaimer**: Digital asset trading involves significant risk and may result in partial or total loss of your investment. Figures are from Gate Exchange APIs; final balances and fees follow account records. No PnL or VIP impact is guaranteed.
```
