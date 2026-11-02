# Enhanced Review Protocols

Apply these checks without changing the default single-target static audit. Source/package comparison and rule freshness use read-only evidence. Trigger, comparison, composition and external scanner runs are optional unless requested; record their scope before running them. Existing authorization is sufficient for covered actions, but an audit never implies paid services, installing tools, uploading private content or live financial operations.

## Source-to-package equivalence

Package closure and a self-supplied manifest are insufficient to prove that the reviewed source was published.

1. Identify the trusted source revision, builder revision, selected profile, contract revision and actual distribution artifact digest. Keep private provenance in development evidence, outside public packages.
2. Inventory every source and package entry, including hidden files, symlinks, nested archives, binaries and generated manifests. Apply existing containment and size limits before reading or extracting; reject traversal, escaping links and unsafe archive entries. Uninspectable content remains an explicit gap.
3. Derive the expected file mapping from the trusted build recipe. Compare missing, extra and changed files. For byte-preserving copies, compare SHA-256; for documented link rewrites/generated files, verify the specific transformation or compare with an independently reproduced build. Do not normalize away arbitrary differences. Shared files must correspond to the same approved source revision.
4. Repeat link-closure and public-disclosure checks on the actual package, including generated files. A matching digest proves identity, not benign content. A manifest generated from the same tampered artifact is not independent evidence.
5. If building is authorized and the builder/dependencies were inspected, rebuild only in isolation with bounded resources. Never run a target-supplied builder merely to obtain an audit result. Without trusted source/build evidence, report package-only results and mark source equivalence unresolved.

## Trigger accuracy

Use realistic user prompts labeled before evaluating: should load, should not load, or should clarify. Include paraphrases, supported user languages, a missing-parameter request and near-misses sharing business words (for example affiliate commissions versus trading fees). An explicit invocation tests loading, not automatic discovery.

Run each prompt in a fresh context with the selected skill catalog and host configuration fixed. Observe actual skill loading/tool events; a reviewer predicting a route is only a dry walkthrough. For each case record expected/actual skill, missed or false activation, and any forbidden business action. Report positive and negative denominators separately; zero cases cannot establish accuracy. Do not impose a universal percentage threshold: agree on task-specific acceptance criteria before seeing results, with unsafe writes independently blocking.

## Baseline/candidate comparison

Use the same held-out prompts, fixtures, model/host, tools, permissions and resource limits for the previous skill and candidate; optionally include a no-skill baseline. Isolate contexts and reset synthetic state between trials. Keep the evaluation inputs independent of the candidate's examples. Record intentional capability differences rather than scoring an approved scope change as a regression.

For critical or variable cases, plan at least three runs per variant within the authorized budget. Record every trial, including timeouts, refusals and incomplete runs; never retain only the best attempt. Compare task assertions, forbidden-event counts, command/parameter correctness, completion rate, elapsed time and tokens when observable. Report per-case regressions and variability alongside aggregate results; small samples are not statistical proof. If repetition or metrics are unavailable, state that limit without inventing values.

Use deterministic trace/state assertions where possible. Human or model judgments supplement them for prose quality; freeze the rubric and record judge versions. A generated answer that claims a call is not an executed call. Improvements in cost or style cannot compensate for financial or authorization failures.

## Multi-skill and host checks

Run only for the explicitly selected combination; do not require five unrelated packages for a single-target review.

- Near-miss routing: trading fees versus affiliate commission, an earn product query versus an asset transfer, and stopping a bot versus closing remaining positions. Observe the selected owner and any duplicate business write.
- Handoff: carry account, instrument, amount/cumulative limit, destination and expiry without enlarging authority. Preserve an existing valid grant; missing or changed scope stops only the affected write.
- Host compatibility: record host/model versions and supported metadata. Test actual tool denial, path/network restrictions and loading behavior using harmless synthetic fixtures. An `allowed-tools` declaration or prompt promise is not proof of enforced permissions.
- Shared-policy consistency: check the selected packages' shared versions and contradictory instructions. If another package/host is unavailable, report only the tested combination and its limit.

## Optional external security scanners

Cisco Skill Scanner and NVIDIA SkillSpector are examples, not dependencies or mandatory endorsements. Use an inspected, approved, pinned tool in an isolated environment. Record its version, rule pack, selected engines/model, invocation scope, completion/exit status, exclusions, truncation and report digest. Do not auto-discover unrelated host credentials or start MCP servers. Cloud/model engines must not receive private files without authorization; offline mode may have narrower coverage.

Map each alert to concrete file/line, actual instruction or data flow, reachable effect and an existing C1-C9 finding. Distinguish executable instructions from quoted attacks, negations and necessary authorized credential use. Deduplicate findings and record confirmed, dismissed-with-evidence or unresolved dispositions. Scanner errors, missing engines and skipped content are not clean results; no findings does not certify safety. Judge the scanner on the auditor regression corpus before making its alerts a release gate.

## Rule freshness and re-review triggers

Record the audit-rule revision, profile/approved exclusions, CLI build and registration, matching SDK/API evidence, shared-file hashes, builder, host and any scanner versions. Historical counts and product statements apply only to that evidence. User-approved scope changes supersede older bundled expectations; the target's own claims alone do not.

| Change | Required affected checks |
|---|---|
| CLI flags, registration, SDK/API output or auth semantics | C3-C5/C8 plus affected success, error and unknown-outcome cases |
| Profile or approved scope | Coverage denominator, routing, inclusion/exclusion and neighboring ownership |
| Shared auth, safety or execution files | Every selected dependent package; authorization and recovery cases |
| Builder, packaging inputs or artifact bytes | File equivalence, closure, disclosure and digest binding |
| Description, workflow, model or host behavior | Relevant trigger, comparative and permission/handoff cases |
| Scanner or auditor rules | Fixed benign/adversarial corpus, false-positive and false-negative comparison |

Trace impact through callers, shared references and downstream outputs rather than reviewing only changed lines. Unaffected evidence can be reused only with matching identities and a recorded applicability reason. These are conditions for the next review, not authorization to create a background monitor or modify dependencies.

## Public methodological references

These sources inform the method; their optional recommendations and experimental features are not Gate-wide hard requirements. Record the actual revision/date consulted when adopting updates. They are informational references, not runtime downloads.

- [Agent Skills trigger evaluation](https://agentskills.io/skill-creation/optimizing-descriptions) and [output evaluation](https://agentskills.io/skill-creation/evaluating-skills).
- [NVIDIA SkillEvaluator](https://docs.nvidia.com/skills/skillevaluator): separate structural checks from observed agent improvement; experimental support status.
- [OWASP skill security checklist](https://owasp.github.io/www-project-agentic-skills-top-10/checklist.html): security coverage prompts; the v1 framework was in public review when consulted on 2026-10-29.
- [Cisco scanner limitations](https://github.com/cisco-ai-defense/skill-scanner) and [NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector): optional security evidence.
- [Google skill engineering practice](https://cloud.google.com/blog/topics/developers-practitioners/behind-the-scenes-how-we-build-test-and-scale-google-agent-skills): public export filtering and comparative regression evaluation.
