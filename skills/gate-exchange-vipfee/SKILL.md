---
name: gate-exchange-vipfee
version: "2026.3.23-1"
updated: "2026-03-23"
description: "Query Gate VIP tier and trading fee rates. Use this skill whenever the user asks about their VIP level, trading fee rates, spot fees, or futures/contract fees on Gate. Trigger phrases include 'VIP level', 'trading fee', 'fee rate', 'spot fee', 'futures fee'."
---

# Gate VIP & Fee Query Assistant

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate (main) | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- cex_account_get_account_detail
- cex_wallet_get_wallet_fee

### Authentication
- API Key Required: Yes (see skill doc/runtime MCP deployment)
- Permissions: Account:Read, Wallet:Read
- Get API Key: https://www.gate.io/myaccount/profile/api-key/manage

### Installation Check
- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## Quick Start

Below are the most common prompts to get started quickly:

1. **Query VIP tier**
   > What is my VIP level?

2. **Query trading fees**
   > Show me the spot and futures trading fees.

3. **Query VIP tier and fees together**
   > Check my VIP level and trading fees.

## Domain Knowledge

### Tool Mapping by Domain

| Group | Tool Calls |
|-------|------------|
| Account / VIP tier | `cex_account_get_account_detail` |
| Trading fee rates | `cex_wallet_get_wallet_fee` |

### Key Concepts

- **VIP Tier**: Gate assigns VIP levels (VIP 0 – VIP 16) based on trading volume and asset holdings. Higher VIP tiers unlock lower fee rates.
- **Spot Fee**: The maker/taker fee rate applied to spot trading pairs.
- **Futures Fee**: The maker/taker fee rate applied to futures/contract trading, differentiated by settlement currency (BTC, USDT, USD).
- The `cex_wallet_get_wallet_fee` tool returns fee rates for both spot and futures in a single response. Use the `settle` parameter to query futures-specific fees.

### API Behavior Notes

- **Account-level pricing**: Gate fee rates are determined by the user's VIP tier. The `currency_pair` parameter does not change the returned fee values — all trading pairs share the same account-level rate.
- **`settle` parameter scope**: The `settle` parameter only affects futures fee fields (`futuresMakerFee` / `futuresTakerFee`). Spot fees (`makerFee` / `takerFee`) remain unchanged regardless of `settle`.
- **Invalid `currency_pair` handling**: The API does not return an error for non-existent trading pairs. It silently returns the default account-level fees. Do not treat a successful response as confirmation that the trading pair exists.

## Workflow

When the user asks about VIP tier or trading fees, follow this sequence.

### Step 1: Identify Query Type

Classify the request into one of these categories:

1. **VIP tier query** — user wants to know their current VIP level
2. **Fee rate query** — user wants to know spot and/or futures trading fee rates
3. **Combined query** — user wants both VIP tier and fee information

Key data to extract:
- `query_type`: "vip", "fee", or "combined"
- `currency_pair` (optional): specific trading pair for fee lookup
- `settle` (optional): futures settlement currency (BTC / USDT / USD)

### Step 2: Query VIP Tier (if needed)

If `query_type` is "vip" or "combined":

Call `cex_account_get_account_detail` with:
- No parameters required

Key data to extract:
- `vip_level`: the user's current VIP tier (e.g., VIP 0, VIP 1, etc.)

### Step 3: Query Trading Fee Rates (if needed)

If `query_type` is "fee" or "combined":

Call `cex_wallet_get_wallet_fee` with:
- `currency_pair` (optional): specify trading pair context (note: fee rates are account-level and do not vary by pair)
- `settle` (optional): futures settlement currency — affects futures fee fields only

Key data to extract:
- `maker_fee_rate`: spot maker fee rate
- `taker_fee_rate`: spot taker fee rate
- `futures_maker_fee_rate`: futures maker fee rate
- `futures_taker_fee_rate`: futures taker fee rate

### Step 4: Return Result

Format the response according to the Report Template. The API (`cex_wallet_get_wallet_fee`) always returns the full fee structure (spot + futures + delivery). Filter the output based on the user's original intent:

- If user asked about **spot fees only** → show only `makerFee` / `takerFee`
- If user asked about **futures/contract fees only** → show only `futuresMakerFee` / `futuresTakerFee`
- If user asked about **trading fees** (general) → show both spot and futures
- If user asked about **VIP only** → show only VIP level, no fee data
- If user specified a `currency_pair` → append a note in the response: "Note: The API returns account-level fee rates. The fee shown applies to all trading pairs; if the pair you specified does not exist, the result still reflects your default account fee rate."

Key data to extract:
- VIP level (if queried)
- Spot maker/taker fee rates (if queried)
- Futures maker/taker fee rates (if queried)

## Judgment Logic Summary

| Condition | Action |
|-----------|--------|
| User asks about VIP tier/level only | Call `cex_account_get_account_detail`, return VIP level |
| User asks about trading fees only | Call `cex_wallet_get_wallet_fee`, return spot and futures fee rates |
| User asks about both VIP and fees | Call both tools, return combined result |
| User specifies a trading pair | Pass `currency_pair` parameter to `cex_wallet_get_wallet_fee` |
| User specifies futures settlement currency | Pass `settle` parameter to `cex_wallet_get_wallet_fee` |
| User asks about spot fees only | Call `cex_wallet_get_wallet_fee`, return only spot fee portion |
| User asks about futures/contract fees only | Call `cex_wallet_get_wallet_fee` with `settle` parameter, return only futures fee portion |
| User specifies a `currency_pair` | Append a disclaimer that the API does not validate trading pairs; the returned fee is the account-level default and the pair may not exist |
| API returns error or empty data | Inform user of the issue and suggest checking account authentication |

## Report Template

```markdown
## Query Result

{vip_section}

{fee_section}
```

**VIP Section** (when VIP is queried):

```markdown
### VIP Tier

| Item | Value |
|------|-------|
| VIP Level | {vip_level} |
```

**Fee Section** (when fees are queried):

```markdown
### Trading Fee Rates

| Category | Maker Fee | Taker Fee |
|----------|-----------|-----------|
| Spot | {spot_maker_fee} | {spot_taker_fee} |
| Futures | {futures_maker_fee} | {futures_taker_fee} |
```

**Combined example output**:

```markdown
## Query Result

### VIP Tier

| Item | Value |
|------|-------|
| VIP Level | VIP 1 |

### Trading Fee Rates

| Category | Maker Fee | Taker Fee |
|----------|-----------|-----------|
| Spot | 0.1% | 0.1% |
| Futures (USDT) | 0.015% | 0.05% |
```

## Error Handling

| Error Type | Typical Cause | Handling Strategy |
|------------|---------------|-------------------|
| Authentication failure | API key invalid or expired | Inform user to check MCP configuration and API key validity |
| Empty response | Account data not available | Inform user the query returned no data and suggest retrying |
| Network error | MCP connection issue | Suggest user check MCP server connectivity |

## Safety Rules

- This Skill is read-only and does not perform any trading or account modification operations.
- No user confirmation is required since all operations are queries only.
- Never expose raw API keys or sensitive authentication details in responses.
