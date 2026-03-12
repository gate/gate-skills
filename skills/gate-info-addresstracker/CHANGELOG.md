# Changelog — gate-info-addresstracker

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.3.12-1] - 2026-03-12

### Added

- Skill: Address tracking. Trigger: "Track this address", "Who is this address". Tools: info_onchain_get_address_info, info_onchain_get_address_transactions, info_onchain_trace_fund_flow. Flow: get_address_info first, then fund tracking if needed (parallel get_address_transactions / trace_fund_flow). Tool count: 3.
- SKILL.md: Routing, address format and scope=with_defi, adaptive threshold table, Basic/Deep Report Template, Decision Logic (risk_score/concentration/mixer/OFAC), Error Handling, Cross-Skill, Safety (privacy/labels/data source). Aligned with docs/pd-vs-skills, docs/PD_VS_SKILLS_OPTIMIZATION_SUMMARY.md.
- README.md, references/scenarios.md.

### Audit

- Read-only; no trading or order execution.
