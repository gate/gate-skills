# gate-info-research — Troubleshooting

> Load this file when a command fails or the agent hits an edge case. Each row lists the symptom, the likely cause, and what the agent should do next — without fabricating a report.

## Preflight failures

| Symptom | Likely cause | Agent action |
|---|---|---|
| `route: "BLOCK"`, `status: "install_cli_required"` | `gate-cli` not on PATH. | Halt. Echo `user_message`. Suggest `curl -sSL https://... install.sh | sh` or the repo's install guide. |
| `route: "BLOCK"`, `status: "run_doctor_required"` | Version below minimum or config unreadable. | Halt. Echo `user_message`. Recommend `gate-cli doctor --format json`. |
| `route: "MCP_FALLBACK"` | Only legacy MCP is reachable. | Emit `__FALLBACK__`; the legacy wrapper (future round) will take over. Never pretend to answer with no data. |
| `route: "CLI"` + `status: "ready_with_migration_warning"` | Legacy Gate MCP entries still live in `~/.cursor/mcp.json` / Codex config. | **Normal** — proceed. Append one migrate hint at the end of the final report (see [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md)). |

## Slot-resolution errors

| Symptom | Cause | Fix |
|---|---|---|
| User says "Solana" but two tickers match | Ambiguous project name. | Ask: "Do you mean SOL (Solana L1) or something else?". Do NOT guess. |
| User supplies only a contract address | `get-coin-info` needs `--query` + ideally `--chain`. | Ask for `--chain` if ambiguous; if sure, set `--query-type address` (the real CLI enum is `address / auto / gate_symbol / name / project / source_id / symbol` — `contract_address` is NOT valid and will be rejected). |
| User asks about a non-crypto asset (e.g. "NVDA stock") | `info coin get-coin-info` can return equity rows. | If the playbook target is crypto research, explicitly narrow to crypto and confirm with the user. |
| `symbols[]` passed but only 1 element | `multi_coin` guard failed (len ≥ 2). | Switch to `single_coin` playbook, do NOT call `batch-market-snapshot`. |

## CLI error payloads

### `"symbol not found"` or empty `items`

- Confirm the ticker spelling. `gate-cli info coin search-coins --query <fuzzy>` can help.
- If the user asked about a very new listing, try `--ranking-type new_listing`.

### Indicator payload returns `null` for many fields (e.g. `project_info.fdv = null`)

- This is expected for some coins where upstream data is thin. Write the null-fields as `—` in Section 2 and continue. Do not abort the playbook.

### `get-kline` timeout on very fine timeframes

- Switch to a coarser `--timeframe` (`1h` / `4h` / `1d`). The Intel backend may rate-limit 1m/5s for free profiles.

### News commands return 0 items

- Switch `--time-range` from `24h` to `7d` before giving up. If still empty, mark Section 4 **no data**.

### `Authorization: ...` appears in debug output

- STOP printing the raw error to the user. Redact any `Authorization:`, `X-API-Key:`, `--api-key=`, `--api-secret=` substring first, then surface a one-line summary (see [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md) rule 6).

## Parallel-execution hiccups

| Symptom | Mitigation |
|---|---|
| One of three parallel A-group commands takes > 30s | Wait for the full group, then proceed. Do NOT cancel the fast ones; you already paid for them. |
| Two parallel commands return contradictory data (e.g. different 24h %) | Report both with source attribution; mark the inconsistency in Section 5. |
| `max-output-bytes` truncated a large payload | Re-run the specific command with `--max-output-bytes 0`. If still oversized, narrow `--scope` to `basic`. |

## Report integrity

- Never merge fact news and community views into one bullet (rule 7).
- Never use inferred price targets — the strongest allowed neutral phrasing is **stronger / softer / needs monitoring** (rule 1 in [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md)).
- If the migration hint is triggered, it MUST be the very last line of the report, not somewhere in the middle.

## Escalation

If the same failure repeats twice after the mitigations above, offer the user:

1. Run `gate-cli doctor --format json` and share the `checks[]` fail rows.
2. Re-run `gate-cli preflight` after `gate-cli migrate --apply --yes` to make sure MCP fallback is not interfering.
3. Report upstream to the `gate-cli` repo with the exact command + trimmed error.
