# Legacy connectivity runner

This is a retained project tool, not a transport for the six CEX skills.
Their private reads and writes use Gate CLI and their own audit protocol.

Run only against a trusted, explicitly selected stdio server. Configuration uses
the existing config.json fields; this change adds no runtime configuration keys.
A configured server is a trust boundary: remote tool descriptions or annotations
cannot prove that the server implementation is safe.

## Default scope

safe_reads.py owns the reviewed public read contract:

- cex_spot_get_spot_tickers: GET /spot/tickers, validated currency_pair/timezone.
- cex_spot_list_currency_pairs: GET /spot/currency_pairs, no arguments.

These exact names and fields were checked against the Gate public MCP schemas
and official APIv4 Spot read semantics. Unknown tools, all writes, private reads,
new fields or invalid schemas/overrides are SKIP before any tool call. A name
prefix or readOnlyHint cannot extend this catalog. Existing write overrides
are inert; they do not grant authority. Adding a tool requires a source-contract
review, tests and a code change, not a runtime bypass.

This intentionally narrows old whole-server smoke coverage. Reports must retain
the skipped denominator; a skipped tool is not verified connectivity.
The historical process exit code remains zero when individual results fail;
consume the summary/report, not that exit status, as the connectivity verdict.

## Transport and reports

stdio_client.py is the single communication boundary. It supports POSIX hosts
(macOS/Linux); other hosts fail before starting a process. It uses the existing
timeout_seconds setting (finite, >0 and <=300 seconds). Each request's monotonic
deadline includes pipe writes and the matching framed response. Initialization
and discovery have the same bounded treatment. It never retries a tool.

Each JSON frame is at most 8MiB, each exchange at most 20MiB received across
stdout/stderr, and at most 1,024 unmatched events are accepted. stderr is drained
without exposing its content. Requests are sequential, pipes are nonblocking,
and cancellation/EOF/error/timeout close and reap the owned process group.
Cleanup allows at most one second each for TERM/KILL. Exceeding a bound fails
the affected exchange; it does not fabricate an empty result or widen scope.

HTML treats peer labels and names as text and escapes them at output; report
filenames do not treat server display names as paths. Narrative model tests in
the separate legacy runner report narrative-only / NOT_EVALUATED for business
execution, even when textual order matches.

## Repeatable verification

From the repository root, use the existing unified test entries:

    python3 -B -m unittest discover -s tests -p 'test_*.py' -v
    python3 -B -m unittest discover -s tests/cex -p 'test_*.py' -v

The maintained synthetic peer and model boundary live under tests/fixtures.
They use disposable files, no real keys and no business network. Tests include
normal reads, unknown/zero-argument writes, changed schemas, deadlines, partial
frames, blocked stdin, stderr backpressure, EOF, malformed/flooded responses,
cleanup, HTML injection and ordered narrative checks. These tests are not real
MCP service or trading integration evidence.
