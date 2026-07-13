# Changelog — gate-info-alphaquant

## 2026.7.13-1 (2026-07-13)

- Initial release by Alpha Finance AI Lab (阿尔法金融 AI 实验室).
- Five-factor cross-sectional alpha engine: MOM, TREND, VOL (inv), LIQ, MR.
- Reads free Gate market data via Gate MCP `/mcp` (no credentials).
- Transparent per-factor breakdown + long/short shortlist.
- User-overridable factor weights; configurable universe / window / timeframe.
- Read-only, informational; guardrails against fabricated numbers and order advice.
