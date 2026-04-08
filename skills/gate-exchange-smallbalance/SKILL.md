---
name: gate-exchange-smallbalance
version: "2026.3.20-1"
updated: "2026-03-20"
description: Gate Exchange small balance (dust) conversion to GT via wallet APIs. Use this skill whenever the user wants to list eligible dust balances, convert small balances to GT, or view small-balance conversion history. Trigger phrases include "small balance", "dust", "convert to GT", "clean up dust", "convert all small coins", "small balance history", or any request involving consolidating low-value spot holdings into GT.
---

# Gate Exchange Small Balance (Dust to GT)

## General Rules

Read and follow the shared runtime rules before proceeding:
→ `exchange-runtime-rules.md` (in parent directory `skills/`)

---

This Skill covers **small balance conversion**: listing spot holdings that qualify under the platform dust threshold, executing conversion to **GT**, and querying conversion history. Under the hood this maps to wallet routes `GET/POST /wallet/small_balance` and `GET /wallet/small_balance_history`; **agents should drive the flow via MCP tools** `cex_wallet_*` below, not by hand-crafting HTTP.

## Domain Knowledge

**Small balance conversion** batches spot (or unified account spot-side) holdings whose value is below the platform **small-balance threshold** (typically up to **100 USDT** equivalent per policy; exact limits follow API responses).

| Term | Meaning |
|------|---------|
| **Dust** | Very small leftover balances that are hard to trade as standalone orders |
| **Small balance** | Eligible currencies under the threshold that can be converted to GT in one operation |

**Characteristics**:
- Consolidates low-value assets into **GT**
- Suited for wallet cleanup; not a substitute for normal spot sells of large positions

**Account scope**: Primarily **spot** or **unified** account spot balances (per product scope).

**Payload note**: `cex_wallet_list_small_balance` and `cex_wallet_list_small_balance_history` responses may wrap rows in an **outer array** whose first element is the **list of objects** to render; if so, use that inner list. Typical row fields: list — `currency`, `available_balance`, `estimated_as_btc`, `convertible_to_gt`; history — `id`, `create_time`, `currency`, `amount`, `gt_amount` (`create_time` often Unix seconds).

**MCP Tool Inventory**:

| Tool | Type | Description |
|------|------|-------------|
| `cex_wallet_list_small_balance` | Query | List currencies eligible for small-balance conversion and estimated GT |
| `cex_wallet_convert_small_balance` | Write | Convert selected currencies or all eligible dust to GT |
| `cex_wallet_list_small_balance_history` | Query | Paginated history of small-balance conversions |

## Workflow

### Step 1: Classify User Intent

Determine whether the user wants to **list** eligible assets, **convert** to GT, **review history**, or should be **excluded** from this Skill.

**Intent routing**:

| Intent | Typical user goal | Next step |
|--------|-------------------|-----------|
| `list` | Explore what can be converted, estimated GT | Step 2 |
| `convert_selected` | Convert specific tickers to GT | Step 2 → Step 3 (interactive) |
| `convert_all` | Convert every eligible dust balance | Step 2 → Step 3 (interactive) |
| `convert_unspecified` | Wants to convert but hasn't specified which coins | Step 2 → Step 3 (interactive) |
| `history` | Past small-balance conversions | Step 4 |
| `exclude` | Sell large holdings on spot, or keep specific coins | Do not call convert; redirect or stop |

**Exclusion rules**:
- User wants to **sell high-value** spot assets at a limit/market price → guide to **spot trading**, not this Skill
- User **explicitly keeps** certain coins → do **not** include those in `currencies` and do not set `is_all: true` without clear consent

Call **no tool** in this step.

Key data to extract:
- `intent`: `list` | `convert_selected` | `convert_all` | `convert_unspecified` | `history` | `exclude`
- `currencies`: optional list of symbols (e.g. `FLOKI`, `MBLK`) for selected convert
- `is_all`: boolean when user asks to convert everything eligible
- `history_filters`: optional `currency`, `page`, `limit` for history

### Step 2: Query Eligible Small Balances

**When to call**: Always call this step when:
1. Intent is `list`
2. Intent is `convert_selected`, `convert_all`, or `convert_unspecified` (before any conversion)

Call `cex_wallet_list_small_balance` with:
- No required parameters (empty call is valid)

Key data to extract:
- Row list: if the tool returns a nested array, use the **inner** array of objects (**Payload note** above)
- Each item: `currency`, `available_balance`, `estimated_as_btc`, `convertible_to_gt`
- Whether the list is **empty**

**Presentation**:
- If non-empty: summarize count, show a table with `currency`, `available_balance`, `convertible_to_gt`
- If empty: inform the user there are **no** eligible small-balance assets at this time

**For convert intents**: Store the eligible list in context for use in Step 3 validation.

### Step 3: Interactive Conversion Flow (if intent = convert_selected / convert_all / convert_unspecified)

This step enforces an **interactive flow** to ensure users make informed decisions.

#### 3.1: Validate User-Specified Currencies (if user specified tickers)

If the user specified `currencies` (e.g., "Convert FLOKI and MBLK to GT"):

1. **Check each currency against the eligible list** from Step 2:
   - If a currency **exists** in the eligible list → mark as `available`
   - If a currency **does NOT exist** in the eligible list → mark as `not_eligible`

2. **Inform the user of the validation result**:
   - For available currencies: "✅ {CURRENCY} is eligible for conversion (available: {available_balance}, estimated GT: {convertible_to_gt})"
   - For non-eligible currencies: "❌ {CURRENCY} is not in the eligible small-balance list. It may be above the threshold or not supported."

3. **If some currencies are not eligible**, ask the user:
   - "The following currencies are not eligible: {list}. Would you like to proceed with converting only the eligible ones ({eligible_list}), or would you like to review the full eligible list first?"

#### 3.2: Guide User Selection (if intent = convert_unspecified or user wants to review)

If the user has not specified which currencies to convert, or wants to review options:

1. **Show the full eligible list** with the following columns:
   - `currency` | `available_balance` | `convertible_to_gt`

2. **Ask the user to choose**:
   - "Which currencies would you like to convert? You can:"
   - "A) Select specific currencies from the list above"
   - "B) Convert all eligible currencies"
   - "Please tell me your choice (e.g., 'FLOKI and MBLK' or 'all')"

3. **Wait for user response** and extract:
   - If user specifies currencies → update `currencies` list, set `is_all: false`
   - If user says "all" → set `is_all: true`

#### 3.3: Final Confirmation

Before calling the convert API:

1. **Summarize what will be converted**:
   - For selected currencies: "You are about to convert: {currencies}. Estimated total GT: {sum of convertible_to_gt}"
   - For all eligible: "You are about to convert all {n} eligible currencies. Estimated total GT: {sum}"

2. **Warn about irreversibility**:
   - "⚠️ This operation is **irreversible**. Once converted, these assets will become GT at the current exchange rate."

3. **Ask for explicit confirmation**:
   - "Do you want to proceed? Please confirm with 'yes' or 'confirm'."

4. **Only proceed** if the user explicitly confirms.

#### 3.4: Execute Conversion

After user confirmation, call `cex_wallet_convert_small_balance` with:
- `currencies` (array of strings): e.g. `["FLOKI","MBLK"]` when converting selected tickers — use with `is_all: false`
- `is_all` (boolean): `true` to convert all eligible small balances

Key data to extract:
- `success`, `message`, and any `error_code` / error fields from the response
- On failure: exact message (e.g. balance, rate limit)

**After success**: Confirm conversion outcome in plain language; do not fabricate amounts not returned by the API.

### Step 4: Query Small Balance History (if intent = history)

Call `cex_wallet_list_small_balance_history` with:
- `currency` (optional, string): filter by converted currency
- `page` (optional, number): page index
- `limit` (optional, number): page size (default/max per API, often up to 100)

Key data to extract:
- Row list: same nested unwrap rule as list tool if applicable (**Payload note**)
- Each record: `id`, `create_time`, `currency`, `amount`, `gt_amount` — present `create_time` readably if it is Unix seconds

**Presentation**:
- Show a table with `id`, `create_time` (readable), `currency`, `amount`, `gt_amount`
- If empty, inform the user: "No conversion history found."

### Step 5: Format and Present Results

Use the **Report Template** section. For any API error, report the real code/message — never invent success.

## Error Handling

| Scenario | Handling |
|----------|----------|
| Empty eligible list after `cex_wallet_list_small_balance` | Friendly message: no qualifying small-balance assets |
| User-specified currency not in eligible list | Inform user which currencies are not eligible; offer to proceed with eligible ones or review full list |
| `BALANCE_NOT_ENOUGH` or balance-related failure | Explain insufficient balance; do not claim success |
| `TOO_MANY_REQUESTS` / rate limit | Ask user to retry later; respect 200 requests / 10s class limits for wallet endpoints |
| Auth / permission errors | Follow authorization guidance in `exchange-runtime-rules.md` |
| User intent is spot sell of large size | Redirect to spot trading flow, not small-balance convert |
| Missing valid convert args (neither non-empty `currencies` + `is_all: false` nor `is_all: true`) | Stop and ask user to choose tickers or confirm convert all |
| MCP / network failure | Suggest checking connectivity and retry; no fabricated results |

## Safety Rules

- **NEVER fabricate** conversion results, GT amounts, or IDs — only report API truth
- **ALWAYS confirm** before `cex_wallet_convert_small_balance`: explicit currency list **or** confirmed **convert all**, plus **irreversibility** and **rate** disclaimer (final rate at execution time)
- **Always query eligible list first** when user wants to convert — never skip to convert without showing what's available
- **Validate user-specified currencies** against the eligible list and inform user of any discrepancies
- **Do not convert** coins the user asked to **keep**
- **Do not expose** API secrets or keys
- **Display amounts** as returned by the API without arbitrary rounding
- **Risk note**: Conversion is **not reversible**; GT value fluctuates with market conditions

## Judgment Logic Summary

| Condition | Action | Tool |
|-----------|--------|------|
| User asks what dust/small balances can convert | List eligible assets | `cex_wallet_list_small_balance` |
| User wants wallet cleanup / "what can I convert" | List first, then offer convert if they proceed | `cex_wallet_list_small_balance` → interactive Step 3 |
| User specifies tickers to convert to GT | Query list → Validate currencies → Confirm → Execute | `cex_wallet_list_small_balance` → `cex_wallet_convert_small_balance` |
| User says convert all dust / all small coins | Query list → Show scope → Confirm → Execute with `is_all: true` | `cex_wallet_list_small_balance` → `cex_wallet_convert_small_balance` |
| User wants to convert but hasn't specified which | Query list → Ask user to select → Confirm → Execute | `cex_wallet_list_small_balance` → interactive selection → `cex_wallet_convert_small_balance` |
| User asks for small-balance / dust conversion history | Query history with optional filters | `cex_wallet_list_small_balance_history` |
| User wants normal spot sell of large position | Exclude; use spot trading Skill | — |
| User refuses conversion or keeps specific assets | Do not call convert | — |
| API returns error | Stop; show real error | — |

## Report Template

**Timestamp**: ISO 8601 `YYYY-MM-DD HH:mm:ss UTC` where applicable.

### Eligible Small Balances Report

```markdown
## Small Balances Eligible for GT Conversion

**Query Time**: {timestamp}

| Currency | Available | Est. BTC value | Est. GT |
|----------|-----------|----------------|---------|
| {currency} | {available_balance} | {estimated_as_btc} | {convertible_to_gt} |

**Summary**: {n} currencies eligible. (If empty: no eligible small-balance assets.)
```

### Conversion Result Report

```markdown
## Small Balance Conversion

**Time**: {timestamp}
**Mode**: {Selected currencies: ... | All eligible}

**Result**: {success / failed}
**Message**: {message}

If failed: **Code**: {error_code_if_any}
```

### History Report

```markdown
## Small Balance Conversion History

**Query Time**: {timestamp}
**Filters**: currency={currency or Any}, page={page}, limit={limit}

| ID | Time (UTC) | Currency | Amount | GT Received |
|----|--------------|----------|--------|-------------|
| {id} | {create_time — convert Unix seconds to readable time} | {currency} | {amount} | {gt_amount} |
```

### Currency Validation Report (for interactive flow)

```markdown
## Currency Validation

| Currency | Status | Available | Est. GT |
|----------|--------|-----------|---------|
| {currency} | ✅ Eligible | {available_balance} | {convertible_to_gt} |
| {currency} | ❌ Not eligible | — | — |

**Summary**: {n} of {m} specified currencies are eligible for conversion.
```