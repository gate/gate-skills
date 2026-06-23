# gate-info-risk

## Overview

Risk-oriented primary skill for Gate.info + Gate.news, executed via `gate-cli`. Consolidates token-contract risk, address compliance risk, and project-level incident risk into a single five-section verdict.

**CLI paths**: legacy leaf commands align to **v0.5.2+**. For `token_risk`, **`info +token-risk`** (v0.7.6+) replaces `check-token-security` + basic `get-coin-info` when `shortcuts_enabled`; optional `get-token-onchain` still runs via `post_shortcut_optional_ids`. `address_risk` does **not** use `+address-tracker` or unshipped `check-address-risk`.

## Runtime requirements

- **CLI**: `gate-cli` on `PATH` — v0.5.2+ for legacy; **v0.7.6+** recommended for `token_risk` shortcut.
- **Shell** (optional): for `scripts/update-skill.*` only.
- **Credentials**: as required by `gate-cli` / preflight for the commands you invoke.

## Core capabilities

| Capability | Typical trigger | Playbook id | Shortcut (>= 0.7.6) |
|---|---|---|---|
| Token contract risk (honeypot, tax, holder concentration) | "Is PEPE safe on eth" / "is this a honeypot" | `token_risk` | `info +token-risk` |
| Address compliance risk (labels, OFAC, blacklist) | "Is this address safe" / "sanctioned / OFAC" | `address_risk` | — (legacy `get-address-info` only) |
| Project-level incident risk (exploit, depeg, regulatory) | "any security or compliance incident on {project}" | `project_risk` | — |

> **Address risk limitation**: `gate-cli` does NOT ship `info compliance check-address-risk`. Address risk is sourced from `info onchain get-address-info` labels. When those are missing the verdict is always **UNABLE_TO_ASSESS** (scope limited), never **LOW**. See [references/troubleshooting.md](references/troubleshooting.md).

> **`token_risk` shortcut**: ticker → `--symbol`; contract → `--address` + `--chain` via playbook `args_when` (`contract_address` predicate in [skills/_shared/cli-version-routing.md](../_shared/cli-version-routing.md)). Native coins without a resolvable contract may fail the shortcut — fall back to legacy or ask for a wrapped token address.

## Inputs / outputs

- **Input**: natural-language query. Required slots:
  - `token_risk` → `token` (contract or ticker) + `chain`
  - `address_risk` → `address` + `chain`
  - `project_risk` → `symbol`
- **Output**: five-section structured report in the user’s locale; Section 1 states **HIGH / MEDIUM / LOW / UNABLE_TO_ASSESS** (may be localized in the user-facing report).

## Routing (when NOT to use)

| Intent | Route to |
|---|---|
| "Give me a general analysis of {coin}" (no safety framing) | `gate-info-research` |
| "Trace this address / smart money behavior" (not risk-first) | `gate-info-web3` |
| "Why did it drop / community view on the incident" | `gate-news-intel` |

Full cross-skill matrix: [skills/_shared/routing.md](../_shared/routing.md).

## Acceptance criteria

1. Preflight contract followed ([skills/_shared/preflight.md](../_shared/preflight.md)); Step 0.5 sets `shortcuts_enabled` when `cli_version >= 0.7.6`.
2. Every legacy `gate-cli` command appears in `gate-cli info list` / `gate-cli news list`. `check-address-risk` and `+address-tracker` are NOT called from this skill.
3. Report has all five sections in the required order (product requirements spec).
4. Missing data is labelled **scope limited** and the verdict degrades to **UNABLE_TO_ASSESS** — never upgrades to **LOW** without evidence.
5. Verdict ordering inside Section 2 is strictly high → medium → low.

## Source

- **Skill spec**: [SKILL.md](SKILL.md)
- **Playbook**: [playbooks/gate-info-risk.yaml](../../playbooks/gate-info-risk.yaml)
- **Shortcuts**: [skills/_shared/cli-version-routing.md](../_shared/cli-version-routing.md)
- **References**: [references/scenarios.md](references/scenarios.md), [references/cli-reference.md](references/cli-reference.md), [references/troubleshooting.md](references/troubleshooting.md)
