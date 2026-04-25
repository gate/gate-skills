# Shared Report & Safety Style

> Applies to every primary skill in `gate-cli-skills`. These rules are hard constraints — violations break the trust contract with end users and may mislead them financially.

## Priority tagging (when writing SKILL.md step text)

Reuse the OKX-style three-tier priority when you need to emphasize a rule inside a skill body:

1. **CRITICAL** — absolute prohibition; bypass causes data loss, security incident, or legal exposure.
2. **REQUIRED** — mandatory step; skipping breaks functionality.
3. **RECOMMENDED** — best practice; deviation allowed with reason.

## Universal safety rules

1. **No buy / sell advice.** For research, the strongest allowed neutral phrasing is **stronger / softer / needs monitoring** (or equivalent in the user’s locale). For risk, use verdict bands **HIGH / MEDIUM / LOW / UNABLE_TO_ASSESS** (localized in user output if needed) plus a short **what to verify next** list — never prescriptive buy/sell language.
2. **No specific price predictions.** You may cite support / resistance from `info markettrend get-technical-analysis` verbatim; you MUST NOT output targets like "SOL will reach $120".
3. **No fabricated data.** Every numeric or categorical value in the report MUST trace back to a command you actually ran in Step 2. If the data is missing, mark that subsection **no data** or **scope limited** — never fill with inference.
4. **Missing data never lowers risk.** For risk-oriented answers, missing fields ⇒ **UNABLE_TO_ASSESS** (or localized equivalent), never **LOW** without evidence.
5. **Cite the source command per claim.** At section level (research) or bullet level (risk), footnote the exact command. For example: `(Source: info marketsnapshot get-market-snapshot.realtime.last)`.
6. **Never echo secrets.** Even if `--debug` or verbose output contains `--api-key`, `--api-secret`, `GATE_API_KEY`, or any `Authorization:` header, you MUST redact before surfacing to the user.
7. **Separate fact events from community views.** News and events go in one paragraph; social / UGC / X / Reddit commentary goes in another. Never merge them into a single "news says" bullet.
8. **English frontmatter only.** YAML fields in SKILL.md stay English for reliable discovery; user-facing answers follow the user's locale.

## Report structures (per primary skill)

- `gate-info-research` — **6 sections**: Summary / Fundamentals and Market Position / Trend Analysis / Recent News and Sentiment / Risk Warnings / Watchlist.
- `gate-info-risk` — **5 sections**: Risk Conclusion / Core Risks / On-chain or Compliance Context / Event Background (if any) / Suggested Follow-ups.

Section count and order are fixed per each primary skill’s `SKILL.md` report template. Do not rename or reorder.

## Migrate hint (Step 3 tail)

When Step 0 returned `status == "ready_with_migration_warning"`, append this ONE line at the very end of the final report:

> ⚙️ Detected legacy Gate MCP config, recommended to run `gate-cli migrate --dry-run` to clean up.

Never gate the main report on this hint. Never put it in the middle of a section.

## Error surface rule

When a required command fails:

1. Trim `Authorization:`, `X-API-Key:`, and any `--api-key=` substrings from the raw output.
2. Quote the trimmed one-line error verbatim.
3. Tell the user exactly which slot or argument to retry (e.g. "Please provide a valid `--chain` (like eth / bsc / solana / tron)").
4. Do NOT fabricate a partial report to "save face".
