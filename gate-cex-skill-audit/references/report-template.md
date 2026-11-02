# Audit Report Contract

Produce the following sections in the user's language. Replace example labels with actual observations; do not leave default PASS values or fabricated execution records. Report storage/versioning follows the workspace's policy, typically `<project-root>/docs/cr/` for repository reviews.

## 1. Identity, scope, and evidence

Record target path/name, revision or content hash, selected business profile, source/package mode, requested review level, included files/shared dependencies, unread files, and runtime limits.

List the architecture baseline, standards, CLI wiki/source/export, revisions/hashes, actual access results, and discrepancies. State whether the live wiki was read. A permission-denied source and an independently reviewed export are separate facts.

## 2. Nine-dimension summary

| ID | Dimension | Status | Evidence and unresolved work |
|---|---|---|---|
| C1 | Agent Skills format | Assessed status | Metadata parsing and standard used |
| C2 | Gate architecture and file conventions | Assessed status | Selected profile, naming, file responsibilities and shared layout |
| C3 | Business lines and substantive completeness | Assessed status | Expected references/capabilities versus actual content |
| C4 | CLI completeness and correctness | Assessed status | Independent expected/actual command matrices |
| C5 | Clarity of CLI explanations | Assessed status | Parameters, units, variants, outputs and recovery |
| C6 | References and content/link integrity | Assessed status | Required local dependencies, anchors, external access |
| C7 | English, grammar and terminology | Assessed status | Full-text review and justified language exceptions |
| C8 | Financial/read-write safety and privacy | Assessed status | Authority, money, secrets, effects and recovery |
| C9 | Executable content | Assessed status | Inventory; syntax, source analysis, actual functional evidence |

Allowed statuses: `PASS`, `FAIL`, `NOT_EVALUATED`, `REQUIRES_REVIEW`, and `NOT_APPLICABLE` with a concrete reason. An optional file absent under the standard is not a failure; an expected business line missing under the approved plan is.

## 3. Reference and business coverage

| Expected file/capability | Actual file/section | CLI applicability evidence | Coverage result | Missing or incorrect content |
|---|---|---|---|---|
| Actual requirement | Observed location or missing | Independent source | Assessed result | Concrete gap |

Include every expected file of the selected profile and every uncovered required capability. Record incomplete prototypes, unlinked references, empty contracts, unsupported products, approved exclusions and unresolved scope separately.

## 4. CLI reconciliation

| Expected operation/variant | Canonical CLI / revision | Documented location | Correct inputs/outputs/access | Outcome |
|---|---|---|---|---|
| Independently established operation | Exact command and source | File:line or missing | Evidence or defect | Assessed result |

Give the expected in-scope denominator, covered numerator, exclusions and unresolved items. Do not provide a coverage percentage if the expected universe cannot be independently established. List incorrect flags, invalid combinations, missing operations, wrong units and wrong output assumptions with their actual contracts.

## 5. Findings and language edits

Each finding includes: stable ID, severity, C1-C9 category, file/line, confidence, trigger/interpretation, consequence, short evidence, minimal correction, and verification method. Missing files use their expected path and the route/profile that requires them.

- `P0`: credible unauthorized execution, asset loss, secret exposure or equivalent critical safety consequence.
- `P1`: required business/CLI gaps, false capability, materially wrong financial meaning, misleading success, or another defect preventing safe intended use.
- `P2`: wording/grammar, discoverability or maintainability issues without a demonstrated critical business consequence.
- `P3`: optional improvements; not a substitute for required corrections.

For language findings show original phrase, corrected English and why the meaning/grammar is wrong. Separately list legitimate localized examples/diagnostics with location and rationale. Do not expose secret literals while demonstrating a finding.

## 6. Executable and scenario evidence

| File/case | Intended purpose | Inspection/syntax result | Functional test and isolation | Observed result / not evaluated |
|---|---|---|---|---|
| Actual item | Verified purpose | Tool and evidence | Actual environment/trace or none | Explicit result |

Record scenario ID, level, synthetic preconditions/fixture, expected/actual ordered events, forbidden events, partial failures, cleanup and retained residual state when relevant. Designed cases are not executed cases. Syntax parsing is not functional validation; CLI contract checking is not a live trade.

## 7. Enhanced-check ledger and re-review

For each check record selected/not selected, actual status, artifact and rule revisions, evidence, limitations and affected C1-C9 dimensions. A selected required check with missing evidence makes its requested review scope incomplete. Unselected optional checks are not passed and do not block a narrower static review.

| Check | Evidence to retain when selected |
|---|---|
| Trigger accuracy | Labeled positive/near-miss cases; actual skill-load events; false triggers and missed triggers |
| Comparative effectiveness | Baseline/candidate hashes, fixed environment, per-case repeated outcomes, failures, tokens/time and unavailable metrics |
| Auditor regression | Corpus revision, actual reviewer outputs, expected findings, false positives, false negatives and inconclusive cases |
| Source/package equivalence | Trusted build mapping, full file inventory, digests, missing/extra/changed files and public-disclosure results |
| External scanner | Tool/rules/model versions, exact scope, exit/completion status, skipped files, raw redacted findings and human disposition |
| Multi-skill/host behavior | Selected skill set and host versions; routing, authorization handoff and observed permission enforcement |
| Rule freshness | Changed dependencies, applicability decisions, stale claims and required re-review cases |

For each mandatory finding keep its independent blocking decision; better style, lower token use or a scanner's score cannot offset an unsafe write or wrong contract. State precisely which artifact/version the verdict covers and which changes invalidate it.

## 8. Overall decision

- `FAIL`: at least one confirmed required-rule failure. Also retain incomplete evidence; a confirmed failure does not make the rest of the review complete.
- `INCOMPLETE`: no confirmed failure, but a required source/check for the requested review level could not be evaluated or needs unresolved review.
- `PASS`: all obligations for the stated level were assessed and passed; justified nonapplicable checks are excluded visibly.

State the requested level and separate unexecuted behavior/integration from this verdict. Include the enhanced-check ledger above; its results must not disappear into a single quality score. For command examples, static syntax/contract checking can satisfy the static level; live API execution is not required. For executable helper functionality, report unexecuted functionality as an evidence gap rather than saying it works. A requested functional-level review cannot pass with only syntax evidence.

Always report jurisdiction/service-entity legal applicability as `NOT_EVALUATED` under the current scope. This is not an overall legal, marketplace or production-release certificate. End with required fixes, remaining evidence, and the smallest safe recheck scope.
