# Changelog — gate-info-risk

**Note**: Dates follow the same `YYYY.M.D-N` format the legacy `gate-info-business-skills` project uses. Bump `version` + `updated` in `SKILL.md` frontmatter and in [playbooks/gate-info-risk.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-info-risk.yaml) together when this file receives a new entry.

---

## [2026.4.18-1] - 2026-04-18 — Initial release

### Added

- **Skill**: Unified risk assessment for tokens, addresses, and project-level compliance / event risks. Replaces the legacy `gate-info-riskcheck` with three explicit playbooks (`token_risk`, `address_risk`, `project_risk`).
- **SKILL.md**: Steps 0-3 + cross-skill routing; references shared modules under [skills/_shared/](https://github.com/gate/gate-skills/tree/master/skills/_shared) for preflight, routing, report style.
- **Playbook**: [playbooks/gate-info-risk.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-info-risk.yaml) — three playbooks with real `gate-cli v0.5.2` lower-level commands.
- **References**: [references/scenarios.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-risk/references/scenarios.md), [references/cli-reference.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-risk/references/cli-reference.md), [references/troubleshooting.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-risk/references/troubleshooting.md).
- **Scripts**: `scripts/update-skill.sh`, `scripts/update-skill.ps1` — mirror of the legacy Trigger-update flow.

### CLI baseline

- Aligned to `gate-cli v0.5.2`.
- `address_risk` explicitly documents that `info compliance check-address-risk` does NOT ship in this CLI version; address risk falls back to `info onchain get-address-info` labels. Missing labels → verdict `无法判定 (scope limited)`.

### Audit

- Read-only; no trade execution.
- No buy / sell advice. Only `高风险 / 中风险 / 低风险 / 无法判定` + `建议继续核验的事项`.
- Missing data never downgrades the verdict toward `低风险`.
