---
name: gate-exchange-earn-gate-cli
version: "2026.4.29-1"
updated: "2026-04-29"
description: "gate-cli execution specification for Gate earn (Simple Earn, dual, staking): reads, writes, Action Draft gates, and degradation (aligned with gate-cli cex earn and related spot balance reads)."
---

# Gate Earn execution specification (`gate-cli`)

> Authoritative execution specification for `gate-cli cex earn` (plus listed spot balance and info reads). `SKILL.md` handles intent routing; this file defines contracts, pre-checks, and safety gates.

## 1. Scope and trigger boundaries

In scope:

- Simple Earn: flexible and fixed-term products, rates, positions, interest, subscribe/redeem, auto-renew style changes where supported by CLI
- Dual-currency: plans, orders, balances, placement
- Staking: discovery, positions, awards, orders, participation (`staking swap`)

Out of scope / route elsewhere:

- Spot order placement, futures, options → respective trading skills
- Pure on-chain DEX → DEX skills
- Non-earn market research → info or market-analysis skills

## 2. `gate-cli` availability and fallback

1. The **`gate-cli`** binary must be installed and runnable (see `SKILL.md` Skill Dependencies and `setup.sh` if needed).
2. Confirm reads work for the task (for example a product listing command) before writes.

Fallback:

- Missing `gate-cli`: install per `setup.sh`; retry reads only until credentials are valid.
- Auth failure: stop writes; follow runtime auth recovery.
- Partial API failure: continue other independent reads; label missing sections.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command:

1. **Preflight with `--help`:** Run the same command path with **`--help`** first (before other flags), e.g. `gate-cli cex earn uni lend --help`, to see required flags and JSON shape.
2. **If help lists required fields:** collect values (ask the user only for non-secret inputs such as currency, amount, tenor; never ask for API secrets in chat), then run the real invocation with every required flag.
3. **If help shows no required fields beyond auth:** run the bare command and add only optional flags needed for correct semantics.

If help is ambiguous, prefer safe read-only probes or explicit user clarification, especially before writes.

## 3. Authentication

- Configure with **`gate-cli config init`** or **`GATE_API_KEY`** / **`GATE_API_SECRET`** (or supported flags) per [gate-cli](https://github.com/gate/gate-cli).
- Writes require a key with sufficient earn and related permissions; spot **read** for balance checks before subscriptions.
- On `401` or permission errors: do not retry writes blindly; switch to guidance mode.

## 4. Command specification

### 4.1 Read commands

| Command | Purpose | Notes |
|---------|---------|-------|
| `gate-cli cex earn uni rate` | Flexible rate reference | Use with product disclaimers |
| `gate-cli cex earn uni currency` | Flexible parameters for a currency | Often needs `currency` |
| `gate-cli cex earn uni records` | Flexible positions / lend records | `--from` / `--to` (Unix ms) when listing history; Case 11 time-bounded export |
| `gate-cli cex earn uni interest` | Cumulative interest per `currency` | **Lifetime** total for that coin, not a date range; for **~last 3 months** flexible payouts use `uni interest-records` |
| `gate-cli cex earn uni interest-records` | Per-accrual flexible interest lines | **`--from` / `--to`** for window; sum `interest` per currency for period PnL (Case 11 default window ≈ 90d) |
| `gate-cli cex earn fixed products` | Fixed product catalog | |
| `gate-cli cex earn fixed products-asset` | Fixed offers for an asset | Pass asset per help |
| `gate-cli cex earn fixed lends` | User fixed positions | |
| `gate-cli cex earn dual plans` | Dual product listing | Filter by currency / side in synthesis |
| `gate-cli cex earn dual orders` | Dual order history | Settled vs open per help |
| `gate-cli cex earn dual balance` | Dual balances | Case 15 summaries |
| `gate-cli cex earn staking find` | Discover staking products | By coin if supported |
| `gate-cli cex earn staking assets` | Staking positions | |
| `gate-cli cex earn staking awards` | Staking reward history | Paginate; filter rows to the same window if API returns timestamps and no `--from`/`--to` |
| `gate-cli cex earn staking orders` | Staking order history | |
| `gate-cli cex spot account list` | Spot balances | Before subscriptions |
| `gate-cli cex spot account get` | One-coin spot balance | Requires `currency` if mandated by help |
| `gate-cli info compliance check-token-security` | Token security signal | Optional; empty result is common |

### 4.2 Write commands

| Command | Purpose | Confirmation |
|---------|---------|----------------|
| `gate-cli cex earn uni lend --json …` | Flexible lend or redeem | **Action Draft + Y** |
| `gate-cli cex earn uni change --json …` | Flexible settings (e.g. auto renew) | **Action Draft + Y** |
| `gate-cli cex earn fixed create --json …` | Open fixed subscription | **Action Draft + Y** |
| `gate-cli cex earn dual place …` | Open dual position | **Action Draft + Y** (exercise risk) |
| `gate-cli cex earn staking swap …` | Staking participate / adjust per CLI | **Action Draft + Y** |

## 5. Execution SOP (non-skippable)

### 5.1 Universal pre-check for writes

1. Confirm product still exists and tenor matches user intent (`fixed products-asset`, `uni currency`, `dual plans`, or `staking find` as appropriate).
2. Confirm **available** spot balance covers the subscription amount (`spot account list` or `spot account get`).
3. Build **Action Draft** with amounts, APR estimates, and risks.

### 5.2 Mandatory confirmation gate for writes

Before any command in §4.2:

1. Show Action Draft (product, currency, amount, indicative yield, material risks).
2. Wait for **Y** / **N**. **Y** must be in the immediately previous user turn.
3. Execute one write; treat confirmation as single-use.
4. Verify with §4.1 reads when useful.

### 5.3 Degradation

- Product query failure: skip that product line; message that some offers are temporarily unavailable.
- Write failure: no automatic retry; show error; suggest App/Web or parameter fix.

## 6. Output templates

```markdown
## Earn Action Draft
- Product: {type}
- Currency / pair context: {currency}
- Amount: {amount}
- Indicative APR or terms: {apr_or_tenor}
- Risks: {risk_notes}
Reply Y to confirm or N to cancel.
```

```markdown
## Earn Execution Result
- Status: {ok_or_failed}
- Command: {gate_cli_invocation_summary}
- Next check: {suggested_read_command}
```
