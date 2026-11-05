# Repository regression tests

Run the root unit and subprocess suites with the standard unittest entry point:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
python3 -B -m unittest discover -s tests/cex -p 'test_*.py' -v
```

`cex/test_withdrawal_retirement.py` covers removal of on-chain withdrawal
submission/cancellation from the assets instructions and independent CLI
contract. It freezes the remaining 27 asset commands, checks UID-transfer
authorization/compliance safeguards, and runs the real builder and checker for
all six standalone packages. These artifact E2E tests execute no business CLI,
financial API or LLM; link rewriting, manifests, packaging and validation are
real. The historical CEX unittest entry above includes all new cases.

The root suite includes standalone Bot package tests and smoke-runner cleanup
regressions. The CEX suite remains the separate historical command/package entry.

Smoke-runner cases cover active configuration, size defaults and enum boundaries,
nested/empty schemas, missing/malformed overrides, zero-valued overrides, skips,
client exceptions and the CEX CLI-only/Pay installer boundary.

The subprocess cases exercise config loading → live or cached schema discovery →
parameter generation and overrides → stdio calls → Markdown/HTML output. They
assert exact requests, skipped calls, protocol-error reporting and early rejection
of a missing server. Only the server peer is synthetic:
`fixtures/smoke_server.py` never connects to a network or reads credentials.
Client config, schema cache, calls and reports live in disposable directories;
tests never run the maintained runner against its configured real service.

The legacy runner currently returns zero even when individual tools fail; tests
assert its failure summary and report rather than treating that exit code as a
successful connectivity result. This cleanup does not redefine that behavior.

Legacy content cleanup v1 is covered by `test_skill_content.py`:

- Parse both READMEs and the development guide for real local paths/anchors;
  reject synthetic missing images, anchors and encoded traversal.
- Derive README counts from unique owned command paths; keep cross-profile
  read reuse separate. Check the approved five-product Earn audit contract.
- Guard the documented routing boundaries and runnable non-CEX examples.
  These are content checks, not proof of LLM routing behavior.
- Unit-test the actual Bash source-filter predicate with Pay exceptions,
  new/old CEX names, empty and future-product names.
- Run the real installer for Cursor, Claude, Codex and OpenClaw twice, using
  disposable client directories. Replace only Git downloads and mcporter with
  `fixtures/installer_host.py`; use real option parsing, copying, JSON merge and
  TOML generation. Assert preserved Exchange/Pay services, excluded CEX sources,
  unchanged existing user CEX installs, unrelated configuration and cleanup.
- Exercise `--no-skills`, invalid selection and clone failure paths; run the
  legacy conversation runner's real `--help` without constructing a model client;
  its examples explicitly require the old scenario schema rather than claiming
  support for the current repository's different scenario layouts.

No real accounts, transactions, package-manager installs or business MCP calls
are made. Test-host environment variables are fixture-only; the product adds no
configuration keys. Run these cases through the root unittest command above.

The 2026-11-03 full-review repairs add formal regressions in
`test_review_repairs.py`, `test_cex_builder_boundaries.py` and
`cex/test_full_review_repairs.py`. Their contract covers the reviewed public-read
catalog (unknown tools and writes produce zero calls), the real stdio client's
normal/deadline/EOF/malformed/backpressure/cleanup paths, every HTML data sink,
ordered narrative checks and their real CLI/report path, and pre-copy builder
path rejection. Only the peer/model provider boundary is synthetic; selection,
framing, subprocess ownership, verdicts, package building/checking and reports
remain real. Narrative PASS never means business execution was observed.

Content contracts cover the one legacy fixture isolation/authorization policy,
CEX preflight scope, the approved public Trade exception and retired screenshots.
They validate files and links, not model instruction-following accuracy.
The source/package checker rejects the known obsolete Spot account-capability
denial in addition to checking the current flag tables. Its semantic guard is
specific and does not replace the agent-led full-content audit.

The retained smoke runner is now intentionally limited to the two reviewed public
reads in `test-for-skill/mcp-smoke-test/safe_reads.py`; it requires a POSIX host.
No new product configuration keys or real write-test mode are introduced.

The master disclosure cleanup is covered by `test_disclosure_cleanup.py` and the
existing four-platform installer subprocess suite in `test_skill_content.py`.
They check plain/encoded private references, personal-path and internal-archive
regressions, all shipped discovery templates against the existing public Pay
contract, and actual generated JSON/TOML/mcporter configuration. Discovery-only
and repeated full selections preserve unrelated configuration and existing CEX
installs without credentials or package-manager execution. Only Git/mcporter
boundaries are synthetic; URL selection and installation remain real.
Image pixels are covered by the separately recorded local OCR/visual review;
text tests do not claim to certify image privacy. Run both through the root
unittest entry point above. Historical commits and Key/Secret examples remain
outside this cleanup's user-approved scope.

The README catalog contracts in `test_skill_content.py` compare both languages
with all current `skills/*/SKILL.md` entries and their declared metadata versions,
and validate local links in both installer READMEs. The x402 command is extracted
from the three user-facing READMEs and executed through the actual installer;
only the established external boundaries are synthetic. It must produce exactly
the two opt-in Pay services, preserve unrelated entries and existing CEX installs,
and avoid source downloads or launching package managers.

DEX CLI usage-only contracts and wallet-installer regressions are maintained in
`test_dex_cli_usage.py`, included by the root unittest discovery command above.
Unit cases invoke the real Claude/Codex installer functions and cover route-file
creation, preserving existing guidance, repeated runs, registration fallback,
secondary check-in registration failure and invalid fixture requests. Full
installer E2E cases retain platform detection, selection, configuration and
route-file writes, and cover normal registration, client failure, help and invalid
options. They also check removed binary installers, absent download metadata and
resolvable links to the existing CLI skills.

Only vendor client registration and mcporter are synthetic, using the existing
`fixtures/installer_host.py` boundary. Child homes and project directories are
disposable; package managers, downloaders and wallet executables are guarded
fixtures that must never run. Fixture-only failure controls are not product
configuration. These tests do not claim real vendor-client compatibility or
wallet/network execution.
