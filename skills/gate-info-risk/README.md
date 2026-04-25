# gate-info-risk

## Overview

Risk-oriented primary skill for Gate.info + Gate.news, executed via `gate-cli`. Consolidates token-contract risk, address compliance risk, and project-level incident risk into a single five-section verdict.

## Runtime requirements

- **CLI**: `gate-cli` v0.5.2 on `PATH`.
- **Shell** (optional): for `scripts/update-skill.*` only.
- **Credentials**: as required by `gate-cli` / preflight for the commands you invoke.

## Core capabilities

| Capability | Typical trigger | Playbook id |
|---|---|---|
| Token contract risk (honeypot, tax, holder concentration) | "Is PEPE safe on eth" / "is this a honeypot" | `token_risk` |
| Address compliance risk (labels, OFAC, blacklist) | "Is this address safe" / "sanctioned / OFAC" | `address_risk` |
| Project-level incident risk (exploit, depeg, regulatory) | "any security or compliance incident on {project}" | `project_risk` |

> **Address risk limitation**: `gate-cli v0.5.2` does NOT ship `info compliance check-address-risk`. Address risk is sourced from `info onchain get-address-info` labels. When those are missing the verdict is always **UNABLE_TO_ASSESS** (scope limited), never **LOW**. See [skills/gate-info-risk/references/troubleshooting.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-risk/references/troubleshooting.md).

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

Full cross-skill matrix: [skills/_shared/routing.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/routing.md).

## Acceptance criteria

1. Preflight contract followed ([skills/_shared/preflight.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/preflight.md)).
2. Every `gate-cli` command appears in `gate-cli info list` / `gate-cli news list`. `check-address-risk` is NOT called.
3. Report has all five sections in the required order (product requirements spec).
4. Missing data is labelled **scope limited** and the verdict degrades to **UNABLE_TO_ASSESS** — never upgrades to **LOW** without evidence.
5. Verdict ordering inside Section 2 is strictly high → medium → low.

## Source

- **Skill spec**: [SKILL.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-risk/SKILL.md)
- **Playbook**: [playbooks/gate-info-risk.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-info-risk.yaml)
- **References**: [references/scenarios.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-risk/references/scenarios.md), [references/cli-reference.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-risk/references/cli-reference.md), [references/troubleshooting.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-risk/references/troubleshooting.md)
- **Repository**: `gate-github-skills` (layout may mirror `gate/gate-skills`).
