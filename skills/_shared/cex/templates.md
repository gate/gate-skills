# Display Templates

These are presentation fields derived from verified context and CLI results. They are not a universal CLI response schema. Omit irrelevant fields; do not invent unavailable fees, fills, references, or balances.

## User-facing language

Translate verified CLI/SDK data into product language before replying. The command,
request, response, and model schemas are implementation details, not default user
content. Use a product's display mapping when it exists; otherwise report only the
business fact that is directly supported by the response.

- Do not display raw field names, JSON, CLI arguments, endpoints, model names,
  numeric enum values, or internal identifiers by default. This includes `pid`,
  `uid`, `id`, `order_id`, `status`, and raw timestamps.
- Do not display local profile names, environment variables, API origins, OAuth
  issuers, scopes, authorization URLs, tokens, or internal test-environment
  details. Say that sign-in or authorization is required or completed instead.
- A product ID or business reference may be retained for reconciliation, but show
  it only when the user asks for a receipt/debug detail or needs it for a support
  case. Prefer the product name, asset, amount, term, and observed outcome.
- Translate a documented enum to a business statement. If its meaning is absent,
  ambiguous, or does not describe the user's operation, omit the code and report
  the verified state as unknown or pending; never infer success from a number.
- Errors should state the affected action and the next safe step. Do not expose
  raw request payloads, stack traces, environment details, or trace IDs unless the
  user explicitly asks for technical diagnostics and is authorized to receive them.

Apply these rules to normal answers, action drafts, results, and errors. A user can
explicitly request raw command or API details; then provide only the minimum needed
for that request and still redact credentials and internal environment data.

## Action draft

| Field | Content |
|---|---|
| Account / environment | Generic account and environment label; never expose raw IDs, profiles, origins, or credential configuration |
| Action / product | Exact action and product; include network/destination for a transfer |
| Instrument / amount | Symbol, side, exact quantity and unit, and whether an amount is spending or received quantity |
| Price / conditions | Market/limit/trigger, price basis, protections, expiry, and applicable account/position mode |
| Costs / exposure | Available fee/slippage evidence, borrowing/leverage or lockup exposure; label estimates |
| Authorization | Existing grant reference and verified limits, or the specific missing authorization |

A complete, still-valid authorization may already permit execution. A draft alone does not create authority, and missing scope must be resolved before a write.

## Result

Report: action/product, instrument, exact amount/unit, observed state, verification source, and any remaining quantity/exposure. Use the states supported by the product: submitted, partially filled, filled, cancelled, rejected, redeemed, settled, or unknown. Do not map all successful exits to completed. Include a returned business reference only when it is useful to the user.

Distinguish CLI response fields from the final user-facing summary. Mark estimates and unknown values. Do not expose unrelated account data merely because the API returned it.

## Error or unknown outcome

Report the failed step, classified error or observed symptom, whether a write may have occurred, last reliable state/reference, reconciliation attempted, and the next safe step. Keep useful trace/request IDs when available and authorized; exclude credentials and sensitive raw diagnostics.

For an unknown write outcome, state that completion is unverified and that the request was not blindly repeated. Do not turn a missing response into a definitive rejection or success.
