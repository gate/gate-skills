"""Regress the retained smoke runner after retiring its disconnected fixture exporter.

Only the local synthetic peer is used. The CLI, config loading, schema discovery,
parameter generation, overrides, stdio protocol and report generation remain real.
"""

import ast
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SMOKE = ROOT / "test-for-skill/mcp-smoke-test"


def load_runner():
    """Import the local helpers without consulting host caches or starting a server."""
    spec = importlib.util.spec_from_file_location("isolated_smoke_runner", SMOKE / "run_test.py")
    module = importlib.util.module_from_spec(spec)
    with mock.patch.object(sys, "path", [str(SMOKE), *sys.path]):
        with mock.patch.dict(sys.modules):
            sys.modules.pop("auto_params", None)
            spec.loader.exec_module(module)
    return module


class SmokeCleanupUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runner = load_runner()

    def test_active_config_and_exporter_retirement(self):
        """Keep the real runner inputs while removing the disconnected export contract."""
        config = self.runner.load_config()
        self.assertTrue({"mcp_server", "cursor_mcp_config", "mcps_cache_dir",
                         "timeout_seconds", "report_dir"}.issubset(config))
        self.assertFalse({"skip_write_tools", "default_test_params", "read_prefixes",
                          "write_prefixes"} & config.keys())
        self.assertFalse(hasattr(self.runner, "classify_tool"))
        for name in ("gen_fixtures.py", "test_fixtures.json"):
            self.assertFalse((SMOKE / name).exists())
        self.assertTrue((SMOKE / "test_overrides.json").is_file())

    def test_size_default_optional_omission_and_enum_boundaries(self):
        """Removing a shadowed entry must preserve size=1 and schema enum choices."""
        for schema, expected in (
            ({"type": "integer"}, 1),
            ({"type": "integer", "enum": [0]}, 0),
            ({"type": "integer", "enum": [-2, 0]}, -2),
        ):
            with self.subTest(schema=schema):
                result = self.runner.generate_params("fixture", {
                    "properties": {"size": schema, "optional": {"type": "string"}},
                    "required": ["size"],
                })
                self.assertEqual(result, {"size": expected})
        tree = ast.parse((SMOKE / "auto_params.py").read_text())
        defaults = next(n.value for n in tree.body if isinstance(n, ast.Assign)
                        and any(isinstance(t, ast.Name) and t.id == "FIELD_DEFAULTS"
                                for t in n.targets))
        keys = [k.value for k in defaults.keys]
        self.assertEqual(len(keys), len(set(keys)), "defaults must not silently shadow a key")

    def test_empty_and_nested_schema_generation(self):
        self.assertEqual(self.runner.generate_params("fixture", {}), {})
        schema = {"arguments": {"properties": {
            "items": {"type": "array", "items": {"type": "object", "properties": {
                "size": {"type": "integer"}, "optional": {"type": "string"}},
                "required": ["size"]}}},
            "required": ["items"]}}
        self.assertEqual(self.runner.generate_params("fixture", schema), {"items": [{"size": 1}]})

    def test_override_missing_invalid_and_zero_value(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "overrides.json"
            self.assertEqual(self.runner.load_overrides(path), {})
            path.write_text("{")
            with self.assertRaises(json.JSONDecodeError):
                self.runner.load_overrides(path)
        self.assertEqual(self.runner.apply_overrides(
            "fixture", {"size": 1}, {"fixture": {"params": {"size": 0}}}), {"size": 0})

    def test_skip_and_client_exception_remain_observable(self):
        client = mock.Mock()
        client.call_tool.side_effect = RuntimeError("synthetic failure")
        with contextlib.redirect_stdout(io.StringIO()):
            results = self.runner.run_connectivity_tests(
                client, {"cex_spot_list_currency_pairs": {}, "fixture_skip": {}},
                {"fixture_skip": {"skip": True, "skip_reason": "not authorized"}})
        self.assertEqual([(r.tool_name, r.status) for r in results],
                         [("cex_spot_list_currency_pairs", "ERROR"), ("fixture_skip", "SKIP")])
        client.call_tool.assert_called_once_with("cex_spot_list_currency_pairs", {})
        self.assertIn("synthetic failure", results[0].message)

    def test_cex_stays_cli_only_while_exchange_installer_remains_for_pay(self):
        """Retiring CEX transport dependencies must not remove Pay's shared installer."""
        business = sorted((ROOT / "skills").glob("gate-cex-*"))
        self.assertEqual(len(business), 6, "the CLI-only scan must cover all six profiles")
        for directory in [*business, ROOT / "skills/_shared/cex"]:
            for path in directory.rglob("*"):
                if path.is_file():
                    self.assertNotRegex(path.read_text(), r"(?i)\bmcp\b|mcp__[a-z_]+", str(path))
        script = (ROOT / "skills/gate-mcp-installer/scripts/install.sh").read_text()
        for option in ("main)", "cex-public)", "cex-exchange)"):
            self.assertIn(option, script)
        self.assertIn("gate-exchange-pay", (ROOT / "skills/exchange-runtime-rules.md").read_text())


class SmokeRunnerEndToEndTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="smoke-runner-regression-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.runner = self.base / "runner"
        self.runner.mkdir()
        for name in ("run_test.py", "auto_params.py", "safe_reads.py", "stdio_client.py"):
            shutil.copyfile(SMOKE / name, self.runner / name)
        self.cache = self.base / "cache/user-fixture/tools"
        self.cache.mkdir(parents=True)
        self.cursor = self.base / "cursor.json"
        self.calls = self.base / "calls.jsonl"
        self.scenario = self.base / "scenario.json"
        self.server = self.base / "server.py"
        shutil.copyfile(ROOT / "tests/fixtures/smoke_server.py", self.server)
        self.config = json.loads((SMOKE / "config.json").read_text())
        self.config.update(mcp_server="fixture", cursor_mcp_config=str(self.cursor),
                           mcps_cache_dir=str(self.cache.parent.parent),
                           timeout_seconds=2, report_dir="reports")
        (self.runner / "config.json").write_text(json.dumps(self.config))
        (self.runner / "test_overrides.json").write_text("{}")
        self.cursor.write_text(json.dumps({"mcpServers": {"fixture": {
            "command": sys.executable, "args": ["-B", str(self.server), str(self.scenario)]}}}))

    def execute(self, tools, *, overrides=None, error=False):
        """Bound each full subprocess and provide no host client config or credentials."""
        self.scenario.write_text(json.dumps({"tools": tools, "calls": str(self.calls), "error": error}))
        (self.runner / "test_overrides.json").write_text(json.dumps(overrides or {}))
        return subprocess.run(
            [sys.executable, "-B", str(self.runner / "run_test.py")],
            cwd=self.base, input="", text=True, capture_output=True, timeout=15,
            env={"PATH": os.defpath, "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(self.base)})

    def reports(self):
        md = list((self.runner / "reports").glob("*.md"))
        html = list((self.runner / "reports").glob("*.html"))
        self.assertEqual(len(md), 1)
        self.assertEqual(len(html), 1)
        return md[0].read_text(), html[0].read_text()

    def test_live_discovery_defaults_override_skip_and_reports(self):
        result = self.execute([
            {"name": "cex_spot_get_spot_tickers", "inputSchema": {"properties": {
                "currency_pair": {"type": "string"}}, "required": ["currency_pair"]}},
            {"name": "fixture_skip", "inputSchema": {}},
        ], overrides={"cex_spot_get_spot_tickers": {"params": {"currency_pair": "ETH_USDT"}},
                      "fixture_skip": {"skip": True, "skip_reason": "no authorization"}})
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("Pass: 1", result.stdout)
        self.assertIn("Skip: 1", result.stdout)
        self.assertEqual([json.loads(line) for line in self.calls.read_text().splitlines()],
                         [{"name": "cex_spot_get_spot_tickers", "arguments": {"currency_pair": "ETH_USDT"}}])
        md, html = self.reports()
        for content in (md, html):
            self.assertIn("cex_spot_get_spot_tickers", content)
            self.assertIn("fixture_skip", content)
            self.assertIn("no authorization", content)

    def test_cached_schema_still_works_without_retired_fixtures(self):
        (self.cache / "cex_spot_list_currency_pairs.json").write_text(json.dumps({
            "name": "cex_spot_list_currency_pairs", "arguments": {
                "properties": {}, "required": []}}))
        result = self.execute([])
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("Using cached schemas", result.stdout)
        self.assertEqual(json.loads(self.calls.read_text()),
                         {"name": "cex_spot_list_currency_pairs", "arguments": {}})
        self.reports()

    def test_protocol_failure_is_reported_as_failure(self):
        result = self.execute([{"name": "cex_spot_list_currency_pairs", "inputSchema": {}}], error=True)
        # The existing runner communicates failed tools in its summary/report, not its exit code.
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("Fail: 1", result.stdout)
        md, _ = self.reports()
        self.assertIn("cex_spot_list_currency_pairs", md)
        self.assertIn("MCP Error", md)

    def test_missing_server_stops_before_any_call_or_report(self):
        self.cursor.write_text('{"mcpServers": {}}')
        result = self.execute([])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not found", result.stdout)
        self.assertFalse(self.calls.exists())
        self.assertFalse((self.runner / "reports").exists())


if __name__ == "__main__":
    unittest.main()
