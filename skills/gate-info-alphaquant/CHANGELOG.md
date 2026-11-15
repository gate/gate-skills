# Changelog — gate-info-alphaquant

## 2026.7.13-2 (2026-07-13)

- **Major upgrade to v2: Alpha158 factor library + IC/IR adaptive weighting.**
- Expanded from 5 hand-picked factors to 17 factors ported from Microsoft Qlib's public
  Alpha158 expressions (momentum / trend-quality / volatility / price-structure / candle-volume).
- Replaced fixed hand-tuned weights with **data-driven IC/IR weighting**: each factor is
  weighted by its Information Ratio (mean IC / std IC) over the lookback, sign included.
  Factors with negative IC are automatically flipped.
- Added **market-regime read** (momentum vs mean-reversion) derived from net momentum weight.
- Added `references/alpha158-catalog.md` (full 158-factor source catalog).
- Report template now shows most-predictive factors by |IR|, per-symbol contributors, and regime.
- Equal-weight fallback for thin universes (<8 symbols) or <10 IC observations.
- Validated live on Gate (ccxt) with a 12-symbol basket; correctly detected a mean-reverting
  regime (negative momentum IC) that v1's fixed weights would have ranked backwards.

## 2026.7.13-1 (2026-07-13)

- Initial release by Alpha Finance AI Lab (阿尔法金融 AI 实验室).
- Five-factor cross-sectional alpha engine: MOM, TREND, VOL (inv), LIQ, MR.
- Reads free Gate market data via Gate MCP `/mcp` (no credentials).
- Transparent per-factor breakdown + long/short shortlist.
- Read-only, informational; guardrails against fabricated numbers and order advice.
