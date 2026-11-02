"""Regression contracts for the ten full-review findings; no live business calls."""
import ast
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import types
import unittest
from html.parser import HTMLParser
from unittest import mock

import test_mcp_smoke_test as smoke_tests

load_runner = smoke_tests.load_runner

ROOT = Path(__file__).resolve().parents[1]
TICKER = "cex_spot_get_spot_tickers"
PAIRS = "cex_spot_list_currency_pairs"


class SafetyAndHtmlTests(unittest.TestCase):
    """Exercise the real selection and HTML sinks, not a duplicate safety classifier."""
    @classmethod
    def setUpClass(cls):
        cls.runner = load_runner()

    def test_only_reviewed_reads_run_even_with_readonly_annotation_or_override(self):
        client = mock.Mock()
        client.call_tool.return_value = {"result": {"content": []}}
        tools = {
            PAIRS: {},
            "fixture_transfer_funds": {"annotations": {"readOnlyHint": True}},
            "get_unknown_mutating_tool": {},
            TICKER: {"arguments": {"properties": {"password": {"type": "string"}}}},
        }
        with contextlib.redirect_stdout(io.StringIO()):
            results = self.runner.run_connectivity_tests(client, tools, {
                "fixture_transfer_funds": {"params": {"amount": "0.0001"}},
            })
        client.call_tool.assert_called_once_with(PAIRS, {})
        self.assertEqual(sum(r.status == "SKIP" for r in results), 3)

    def test_read_contract_bounds_schema_and_parameters(self):
        rejection = self.runner.read_rejection
        self.assertIsNone(rejection(TICKER, {}, {"currency_pair": "BTC_USDT", "timezone": "utc0"}))
        self.assertIsNone(rejection(PAIRS, {}, {}))
        for name, schema, params in (
            ("unknown", {}, {}),
            (PAIRS, {}, {"amount": "1"}),
            (TICKER, {}, {"currency_pair": "../secret"}),
            (TICKER, {}, {"timezone": "test"}),
            (TICKER, {"required": [[]]}, {}),
            (TICKER, {"properties": {"currency_pair": {"type": "integer"}}}, {}),
            (PAIRS, {"required": ["amount"]}, {}),
            (PAIRS, {"properties": []}, {}),
            (PAIRS, None, {}),
            (TICKER, {"properties": {"timezone": {"type": "string", "enum": []}}}, {}),
            (TICKER, {"properties": {"timezone": {"type": "string", "enum": [1]}}}, {}),
            (TICKER, {"properties": {"timezone": {"type": "string", "enum": ["utc8"]}}}, {"timezone": "utc0"}),
        ):
            with self.subTest(name=name, schema=schema, params=params):
                self.assertIsNotNone(rejection(name, schema, params))

    def test_html_escapes_every_untrusted_display_sink(self):
        class Tags(HTMLParser):
            def __init__(self):
                super().__init__()
                self.tags = []
                self.attributes = []
                self.data = []
            def handle_starttag(self, tag, attrs):
                self.tags.append(tag)
                self.attributes.extend(attrs)
            def handle_data(self, data):
                self.data.append(data)
        attack = '<script>window.review=1</script><img src=x onerror=alert(1)>'
        results = [
            self.runner.TestResult(attack, attack, attack, {"input": attack}, status, attack, 1,
                                  raw_response={"status": code, "label": attack},
                                  skip_reason=attack if status == "SKIP" else None)
            for status, code in (("PASS", 500), ("PASS", 504), ("FAIL", 401), ("SKIP", 200))
        ]
        with tempfile.TemporaryDirectory(prefix="review-html-") as directory:
            path = self.runner.generate_html_report(results, attack, {}, Path(directory))
            self.assertEqual(path.parent, Path(directory))
            html = path.read_text()
        parsed = Tags()
        parsed.feed(html)
        self.assertNotIn("script", parsed.tags)
        self.assertNotIn("img", parsed.tags)
        self.assertFalse(any(k.lower().startswith("on") for k, _ in parsed.attributes))
        self.assertNotIn(attack, html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn("Show request", html)
        self.assertIn("Module Summary", html)
        self.assertTrue(any("连通 (500 服务端错误 " + attack + ")" in data for data in parsed.data))


class SmokeSafetyEndToEndTests(unittest.TestCase):
    """Retain CLI/config/schema/overrides/protocol/report; replace only the server."""
    def setUp(self):
        self.host = smoke_tests.SmokeRunnerEndToEndTests()
        self.host.setUp()
        self.addCleanup(self.host.doCleanups)

    def test_new_and_zero_argument_writes_are_not_sent(self):
        result = self.host.execute([
            {"name": PAIRS, "inputSchema": {}},
            {"name": "fixture_transfer_funds", "inputSchema": {
                "properties": {"amount": {"type": "string"}}, "required": ["amount"]},
             "annotations": {"readOnlyHint": True}},
            {"name": "get_unknown_mutation", "inputSchema": {}},
        ], overrides={"fixture_transfer_funds": {"params": {"amount": "1"}}})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Skip: 2", result.stdout)
        self.assertEqual([json.loads(x)["name"] for x in self.host.calls.read_text().splitlines()], [PAIRS])
        md, html = self.host.reports()
        self.assertIn("reviewed public read-only catalog", md)
        self.assertIn("fixture_transfer_funds", html)

    def test_changed_schema_cannot_enable_an_unreviewed_parameter(self):
        result = self.host.execute([{"name": TICKER, "inputSchema": {
            "properties": {"withdraw": {"type": "boolean"}}, "required": ["withdraw"]}}])
        self.assertEqual(result.returncode, 0)
        self.assertFalse(self.host.calls.exists())
        self.assertIn("Skip: 1", result.stdout)
        self.host.reports()


class StdioEndToEndTests(unittest.TestCase):
    """An outer guard and owned peer PID ensure a broken deadline cannot hang the suite."""
    def run_peer(self, **fault):
        with tempfile.TemporaryDirectory(prefix="bounded-stdio-") as directory:
            base = Path(directory)
            pid = base / "peer.pid"
            scenario = base / "scenario.json"
            scenario.write_text(json.dumps({
                "tools": [{"name": PAIRS, "inputSchema": {}}],
                "calls": str(base / "calls.jsonl"), "peer_pid": str(pid), **fault}))
            try:
                result = subprocess.run(
                    [sys.executable, "-B", str(ROOT / "tests/fixtures/stdio_probe.py"), str(ROOT), str(scenario)],
                    capture_output=True, text=True, timeout=5,
                    env={"PATH": os.defpath, "PYTHONDONTWRITEBYTECODE": "1"})
                self.assertEqual(result.returncode, 0, result.stderr)
                observed = json.loads(result.stdout)
                self.assertFalse(observed["running"])
                if "exited" in observed:
                    self.assertTrue(observed["exited"])
                    self.assertTrue(observed["pipes_closed"])
                self.assertLess(observed["elapsed"], 3.5)
                return observed
            finally:
                if pid.exists():
                    try:
                        os.killpg(int(pid.read_text()), signal.SIGKILL)
                    except ProcessLookupError:
                        pass

    def test_normal_response_and_stderr_backpressure(self):
        for fault in ({}, {"stderr_bytes": 1024 * 1024}, {"unmatched": 2}):
            with self.subTest(fault=fault):
                result = self.run_peer(**fault)
                self.assertNotIn("error", result)
                self.assertFalse(result["timeout"])
                self.assertEqual(result["tools"][0]["name"], PAIRS)

    def test_silence_and_partial_line_obey_deadline(self):
        for fault in ({"silence": "initialize"}, {"silence": "tools/list"},
                      {"silence": "tools/call"}, {"partial": "tools/call"}, {"pause_after_list": True}, {"wrong_id": True}):
            with self.subTest(fault=fault):
                result = self.run_peer(**fault)
                self.assertTrue(result.get("timeout") or result.get("error") == "TimeoutError")

    def test_eof_malformed_and_notification_flood_stop_and_cleanup(self):
        for fault, errors in (
            ({"eof": "tools/call"}, {"EOFError"}),
            ({"malformed": "tools/call"}, {"JSONDecodeError"}),
            ({"unmatched": 1100}, {"ValueError", "TimeoutError"}),
        ):
            with self.subTest(fault=fault):
                result = self.run_peer(**fault)
                self.assertIn(result.get("error"), errors)

    def test_request_frame_response_frame_and_exchange_byte_bounds(self):
        for fault in ({"request_bytes": 9 * 1024 * 1024},
                      {"response_bytes": 9 * 1024 * 1024},
                      {"stderr_bytes": 21 * 1024 * 1024}):
            with self.subTest(fault=fault):
                result = self.run_peer(**fault, probe_timeout=2)
                self.assertEqual(result.get("error"), "ValueError")
                self.assertIn("byte limit", result.get("detail", ""))

    def test_sequential_client_rejects_invalid_lifecycle_calls(self):
        client = load_runner().McpStdioClient("unused", [])
        with self.assertRaisesRegex(RuntimeError, "not running"):
            client.call_tool(PAIRS)
        client.process = mock.Mock()
        client._busy = True
        with self.assertRaisesRegex(RuntimeError, "concurrent"):
            client.call_tool(PAIRS)
        client.process = None  # This unit fixture never owned a real process.
        with mock.patch.object(os, "name", "nt"):
            with self.assertRaisesRegex(RuntimeError, "POSIX"):
                client.start()

    def test_reaped_peer_permission_error_cannot_skip_pipe_cleanup(self):
        client = load_runner().McpStdioClient("unused", [])
        process = mock.Mock()
        process.poll.return_value = 0
        client.process, client._selector = process, mock.Mock()
        with mock.patch.object(os, "killpg", side_effect=PermissionError):
            client.stop()
        for pipe in (process.stdin, process.stdout, process.stderr):
            pipe.close.assert_called_once()
        self.assertIsNone(client._selector)

    def test_timeout_input_is_finite_positive_and_bounded(self):
        client = load_runner().McpStdioClient
        for timeout in (0, -1, float("nan"), float("inf"), 301, "1"):
            with self.subTest(timeout=timeout):
                with self.assertRaises(ValueError):
                    client("unused", [], timeout=timeout)


class LegacyNarrativeTests(unittest.TestCase):
    """The model response is the only fake; parsing, verdict, report and CLI are real."""
    def run_case(self, text):
        spec = importlib.util.spec_from_file_location("legacy_review_runner", ROOT / "test-for-skill/test_skill.py")
        module = importlib.util.module_from_spec(spec)
        with mock.patch.dict(sys.modules, {"anthropic": types.SimpleNamespace(Anthropic=lambda: None)}):
            spec.loader.exec_module(module)
        tester = object.__new__(module.SkillTester)
        tester.verbose, tester.skill_content, tester.skill_name, tester.skill_dir = False, "fixture", "fixture", Path(".")
        tester.client = types.SimpleNamespace(messages=types.SimpleNamespace(
            create=lambda **_: types.SimpleNamespace(content=[types.SimpleNamespace(text=text)])))
        with contextlib.redirect_stdout(io.StringIO()):
            result = tester.run_scenario({"id": 1, "name": "fixture", "prompt": "synthetic",
                "expected": {"tools_in_order": ["get_quote", "create_order"], "must_ask_confirmation": True}})
        return tester, result

    def test_order_multiplicity_missing_and_forbidden_events(self):
        for events, expected in (
            (["get_quote", "create_order"], True),
            (["create_order", "get_quote"], False),
            (["get_quote", "create_order", "create_order"], False),
            (["get_quote"], False),
            (["get_quote", "create_order", "transfer"], False),
            ([], False),
        ):
            with self.subTest(events=events):
                _, result = self.run_case("\n".join("[TOOL_CALL] " + e for e in events) + "\n请确认")
                self.assertEqual(result["overall_pass"], expected)
                self.assertEqual(result["runtime_execution"], "NOT_EVALUATED")

    def test_report_cannot_claim_business_execution(self):
        tester, result = self.run_case("[TOOL_CALL] get_quote\n[TOOL_CALL] create_order\n请确认")
        with tempfile.TemporaryDirectory(prefix="narrative-report-") as directory:
            path = Path(directory) / "report.md"
            with contextlib.redirect_stdout(io.StringIO()):
                tester.generate_report([result], path)
            self.assertIn("narrative-only", path.read_text())
            self.assertIn("NOT_EVALUATED", path.read_text())


class LegacyCliEndToEndTests(unittest.TestCase):
    def test_cli_parses_scenarios_and_fails_reversed_narrative(self):
        """Only the external model package is replaced; argv/parser/verdict/report are real."""
        with tempfile.TemporaryDirectory(prefix="legacy-cli-") as directory:
            base = Path(directory)
            skill = base / "skill"
            (skill / "references").mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: fixture\n---\n# Synthetic fixture\n")
            bt = chr(96)
            (skill / "references/scenarios.md").write_text(
                f"### Scenario 1: fixture\n- User Prompt: {bt}synthetic{bt}\n"
                f"- Tools: {bt}get_quote → create_spot_order{bt}\n")
            # This module is the model-provider boundary, not the runner under test.
            (base / "anthropic.py").write_text(
                '"""Synthetic model boundary; never makes a network request."""\n'
                'from pathlib import Path\nfrom types import SimpleNamespace\n'
                'class Anthropic:\n'
                ' def __init__(self):\n'
                '  self.messages=SimpleNamespace(create=lambda **kw: SimpleNamespace(content=[SimpleNamespace(text=Path(__file__).with_name("response.txt").read_text())]))\n')
            report = base / "report.md"
            for events, code in ((["get_quote", "create_spot_order"], 0), (["create_spot_order", "get_quote"], 1)):
                (base / "response.txt").write_text("\n".join("[TOOL_CALL] " + event for event in events) + "\n请确认")
                result = subprocess.run([sys.executable, "-B", str(ROOT / "test-for-skill/test_skill.py"),
                    "--skill", str(skill), "--all", "--output", str(report)], cwd=base,
                    capture_output=True, text=True, timeout=5,
                    env={"PATH": os.defpath, "PYTHONPATH": str(base), "ANTHROPIC_API_KEY": "synthetic-only"})
                self.assertEqual(result.returncode, code, result.stdout + result.stderr)
                self.assertIn("narrative-only", report.read_text())
                self.assertIn("NOT_EVALUATED", report.read_text())


class DocumentationSafetyContracts(unittest.TestCase):
    """Guard normative entry-to-reference dependencies; these are not LLM execution tests."""
    def test_fixture_entry_and_guides_use_one_isolation_policy(self):
        base = ROOT / "test-for-skill/skill-tester"
        for relative in ("SKILL.md", "references/execution-guide.md", "references/fixture-templates.md"):
            body = (base / relative).read_text()
            self.assertIn("fixture-safety.md", body)
            self.assertNotIn("| 🧪 测试环境 | ✅ 自动执行", body)
            self.assertNotIn("确保不成交", body)
            self.assertNotIn("确保不被撮合", body)
            self.assertNotIn("标记 PASS ⚠️（Teardown 失败）", body)
        policy = (base / "references/fixture-safety.md").read_text()
        for phrase in ("BLOCKED", "Zero business writes", "Setup", "cleanup", "explicit authorization"):
            self.assertIn(phrase.lower(), policy.lower())

    def test_cex_preflight_and_public_exception_have_consistent_scope(self):
        profile = (ROOT / "gate-cex-skill-audit/references/coverage-profiles.md").read_text()
        self.assertIn("Private reads and every write", profile)
        for phrase in ("fixed GET paths", "no credentials/cookies", "no redirects",
                       "smart-position-commands.md", "futures-combo-commands.md"):
            self.assertIn(phrase, profile)
        guide = (ROOT / "docs/preflight-and-diagnostics.md").read_text()
        self.assertNotIn("All new skills MUST", guide)
        self.assertIn("never emit", guide)
        self.assertIn("Pay", guide)

    def test_stale_screenshots_removed_from_both_public_entries(self):
        stale = ("general-install-1.png", "general-install-2.png", "claude-install-1.png",
                 "claude-install-2.png", "codex-nl-install-1.png", "codex-nl-install-2.png",
                 "codex-manual-install-3.png", "codex-manual-install-4.png")
        for name in stale:
            self.assertFalse((ROOT / "image" / name).exists())
            for document in ("README.md", "README_zh.md"):
                self.assertNotIn("image/" + name, (ROOT / document).read_text())


if __name__ == "__main__":
    unittest.main()
