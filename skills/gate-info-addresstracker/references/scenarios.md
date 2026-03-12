# gate-info-addresstracker — Scenarios & Prompt Examples

## Scenario 1: Address identity only (no fund tracking)

**Context**: User wants to know who an address is / basic address info, no request for transactions or fund flow.

**Prompt Examples**:
- "Who is this address 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 on eth"
- "Track this address 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
- "Check this address balance on eth"

**Expected Behavior**:
1. **Infer chain** from address prefix (0x→ETH or BSC/Arb etc., bc1/1/3→BTC, T→Tron); if unknown, ask user to specify chain. Call `info_onchain_get_address_info`(address, chain, scope=with_defi) only when supported.
2. Return **Basic** report: Address Profile, Asset Holdings, DeFi Positions (if available), PnL Summary (if available). No further tools.

## Scenario 2: Address + fund flow / recent transactions

**Context**: User explicitly asks for fund flow or recent transactions.

**Prompt Examples**:
- "Track this address 0x… and show recent fund flow"
- "Recent transactions for this address"
- "Recent transactions for this address"

**Expected Behavior**:
1. Call `info_onchain_get_address_info` first (scope=with_defi). Then call in parallel: `info_onchain_get_address_transactions` and `info_onchain_trace_fund_flow` (if available). Set **min_value_usd** by address total balance per SKILL table (e.g. <$100K → $1K/$10K; $100K–$1M → $10K/$100K; $1M–$100M → $100K/$1M; >$100M → $1M/$10M).
2. LLM aggregates into **Deep** report: Basic sections + Large Transaction History + Fund Flow Tracing + Risk Warnings. If **info_onchain_trace_fund_flow** is unavailable, note "No fund flow data" or "Fund tracing under development"; still output transaction history section.

## Scenario 3: Chain specified (English)

**Context**: User specifies chain in English.

**Prompt Examples**:
- "Who is this address on eth"
- "Track 0x… on base"

**Expected Behavior**:
1. Parse address and chain (eth, base, etc.); map to API chain param. Call `info_onchain_get_address_info` with correct chain; branch on fund-tracking need as in Scenarios 1–2. Use scope=with_defi when supported.

## Scenario 4: Auto-upgrade to Deep

**Context**: Address has labels, high balance, or risk flags — upgrade to Deep even if user did not explicitly ask for fund flow.

**Prompt Examples**:
- "Who is this address 0x…" (and API returns exchange/hacker/whale label or balance >$1M or risk_score high/medium)

**Expected Behavior**:
1. After `info_onchain_get_address_info`, if conditions for **auto-upgrade** are met (known labels, balance >$1M, or risk flags), proceed to Step 4: call `info_onchain_get_address_transactions` and `info_onchain_trace_fund_flow` in parallel with adaptive min_value_usd.
2. Output full **Deep** report including tx history and fund flow (or "Fund tracing under development" if `info_onchain_trace_fund_flow` unavailable).

## Scenario 5: Fund flow unavailable

**Context**: `info_onchain_trace_fund_flow` is not available or returns empty.

**Prompt Examples**:
- "Track this address and show fund flow"

**Expected Behavior**:
1. Call `info_onchain_get_address_info`, then `info_onchain_get_address_transactions` (with adaptive min_value_usd). Do not block on `info_onchain_trace_fund_flow`.
2. In report: show **Large Transaction History**; for Fund Flow section show "No fund flow data" or "Fund tracing under development". Still deliver address profile and transaction sections.
