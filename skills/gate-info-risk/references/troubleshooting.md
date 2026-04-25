# gate-info-risk — Troubleshooting

> Load this file when a risk-assessment command fails or an edge case appears. Risk skills MUST NOT fall back to "Low Risk" when they don't know — the correct fallback is `Unable to determine (scope limited)`.

## Preflight failures

Same as `gate-info-research troubleshooting`. See also [skills/_shared/preflight.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/preflight.md).

## The `check-address-risk` gap (address_risk only)

| Symptom | Cause | Agent action |
|---|---|---|
| Agent "wants" to call `info compliance check-address-risk` | That command does NOT exist in `gate-cli v0.5.2`. | Use `info onchain get-address-info` + `get-address-transactions` only. Never fabricate a call. |
| `get-address-info` returns no `risk_labels` and no `tags` | Address is not labelled by upstream, OR address is too new, OR upstream data is thin. | Verdict = `无法判定 (scope limited)`. Recommend retry after `check-address-risk` ships upstream. |
| User insists on a pass/fail verdict | Risk assessment rules. | Re-state the scope-limited caveat. Offer to list the raw label fields verbatim. Do NOT emit `低风险` just to satisfy the ask. |

## Slot-resolution errors

| Symptom | Cause | Fix |
|---|---|---|
| `check-token-security` returns `"chain required"` error | `--chain` was missing or mistyped. | Ask the user for the correct chain id and canonicalize per the alias table below before passing to `--chain`. |

<a id="chain-aliases"></a>

### Chain aliases

**Input convention**: the skill sends the **short id** on `--chain` (`eth`, `bsc`, `arb`, ...). The CLI also accepts long-form aliases on input (`ethereum`, `bnb`, `arbitrum`, ...), so user-supplied long forms must be normalized to the short id before invocation.

**Response parsing contract**: the response `.chain` echo is **endpoint- and chain-dependent** — do NOT assume a fixed short-vs-long shape. Observed (dev build):

| Input `--chain` | Observed response `.chain` | Observed on endpoint |
|---|---|---|
| `eth`      | `eth`       | `check-token-security` (USDT-ETH) |
| `arb`      | `arbitrum`  | `check-token-security` (ARB-on-Arbitrum) |
| `bsc`      | `bsc`       | `check-token-security` (CAKE-on-BSC) |

Because the echo is per-endpoint, **parsers MUST accept both alias forms** when reading `.chain`. Use a normalization map (below) on read, don't hard-code a single expected spelling.

### Canonical alias table (for BOTH input normalization and response parsing)

| Canonical short id (send on `--chain`) | Long-form aliases (accept as user input AND as response `.chain` echo) |
|---|---|
| `eth`      | `ethereum` |
| `bsc`      | `bnb`, `binance-smart-chain` |
| `polygon`  | `matic` |
| `arb`      | `arbitrum` |
| `op`       | `optimism` |
| `base`     | — |
| `avax`     | `avalanche` |
| `solana`   | `sol` |
| `tron`     | `trx` |

### Other slot-resolution errors

| Symptom | Cause | Fix |
|---|---|---|
| User provides an EOA wallet but asks about a token | Slot mismatch — an EOA is not a token contract. | Clarify: "Did you mean a wallet address (`address_risk`) or a token contract (`token_risk`)?" Do NOT silently pick one. |
| User provides just a ticker for `token_risk` | `--token` works with a ticker on some chains, but resolving to the correct contract is ambiguous when a ticker exists on many chains (USDT on eth / tron / bsc / ...). | Ask for `--chain`; if user is unsure, offer to enumerate top chains for that ticker via `info coin get-coin-info --query {ticker}`. |
| User supplies a mixed-case address (`0xAbC...`) | EVM addresses are checksum-case-sensitive in some UIs but lower-cased on Gate upstream. | Pass as-is; both case forms are accepted. |

## CLI error payloads

### `check-token-security` returns `risky_list: null, attention_list: null`

Normal for clean tokens. Combine with `high_risk_list` values: if all entries have `risk_value: "0"` (with the benign `is_open_source: "1"` exception), the token has no flagged issues at the contract layer. Proceed to verdict rules in SKILL.md.

### `check-token-security.data_analysis.top10_percent > 70` but token is a major stablecoin

Stablecoins (USDT, USDC, DAI) are structurally concentrated in issuer treasuries + exchange hot wallets + bridge locker contracts. Note the concentration as `TECHNICAL_CONTRACT` risk item but do NOT upgrade the verdict to `高风险` solely on this.

### `get-address-info` succeeds with populated `tags` but no `risk_labels`

Tags alone are informational (e.g. `exchange deposit`, `contract router`), not risk-bearing. Verdict remains `无法判定` unless `tags` include risk-bearing terms (`mixer deposit`, `sanctioned entity`, ...).

### `get-token-onchain` fails with `"upstream timeout"`

Optional command; mark Section 3 (On-chain or Compliance Context) partial and continue. Do NOT retry more than once inside the same turn.

### `Authorization: Bearer ...` leaks into error output

Stop. Redact everything after `Authorization:`, `Bearer `, `X-API-Key:`, `--api-key=`, `--api-secret=`. Surface only the one-line summary.

## Report-integrity rules

- **Section ordering**: 1 Conclusion -> 2 Core Risks (High -> Medium -> Low) -> 3 On-chain / Compliance Context -> 4 Event Background -> 5 Suggested Follow-ups. Never reorder.
- **Risk classification tag**: every Section-2 bullet MUST carry one of `TECHNICAL_CONTRACT` / `ADDRESS_COMPLIANCE` / `PROJECT_LEVEL`. No unclassified bullets.
- **Scope-limited marker**: when any optional command failed, append ` (scope limited)` to the verdict and state which dimension is missing in Section 3.
- **No buy / sell advice**. Closest allowed language: `建议避开 / 建议进一步核验`.

## Escalation

After two repeated failures on the same command:

1. Run `gate-cli doctor --format json`; inspect `checks[] | select(.status=="fail")`.
2. Check `GATE_INTEL_INFO_MCP_URL` env — connectivity issues on the compliance endpoint show up here.
3. If still stuck, downgrade the playbook (e.g. from `token_risk` full to basic: drop `get-token-onchain` and return `check-token-security` only) and clearly state the reduced scope in Section 1.
