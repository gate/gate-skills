"""Content contracts and offline end-to-end regressions for legacy cleanup v1.

Installer cases replace only Git downloads and mcporter. Installation filtering, option
selection, copying, JSON/TOML generation and existing-user preservation are real.
The legacy --help case separately stubs the optional model-provider import.
These tests do not claim to measure an LLM's interpretation of routing prose.
"""

from collections import Counter
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "skills/gate-mcp-installer/scripts/install.sh"
DISCOVERY_URL = "https://openplatform.gateapi.io/pay-mcp-server/mcp"
SPEC = importlib.util.spec_from_file_location("skill_content_helpers", ROOT / "scripts/cex_skills.py")
HELPERS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPERS)


def local_link_errors(path, text=None):
    """Reuse the maintained Markdown parser and containment rules, including anchors."""
    errors = []
    for href in HELPERS.links(path.read_text() if text is None else text):
        destination, anchor = HELPERS.target_link(path, href)
        if destination is None:
            continue
        if not HELPERS.contained(destination, ROOT) or not destination.is_file():
            errors.append(href)
        elif anchor and anchor not in HELPERS.anchors(destination.read_text()):
            errors.append(href)
    return errors


class ContentContractTests(unittest.TestCase):
    def test_current_readme_paths_images_and_anchors_resolve(self):
        for name in ("README.md", "README_zh.md", "docs/skill-development-guide.md",
                     "skills/gate-cli-installer/README.md", "skills/gate-mcp-installer/README.md"):
            with self.subTest(document=name):
                self.assertEqual(local_link_errors(ROOT / name), [])
        for removed, kept in (
            ("openclaw-manual-install-1.png", "codex-manual-install-1.png"),
            ("codex-manual-install-4.png", "codex-manual-install-2.png"),
        ):
            self.assertFalse((ROOT / "image" / removed).exists())
            self.assertTrue((ROOT / "image" / kept).is_file())

    def test_link_checker_rejects_missing_images_anchors_and_escape(self):
        path = ROOT / "README.md"
        for link in ("image/missing-fixture.png", "README.md#missing-fixture-anchor",
                     "../outside-fixture.md", "image/%2e%2e/%2e%2e/outside-fixture.md"):
            with self.subTest(link=link):
                self.assertEqual(local_link_errors(path, f"![fixture]({link})"), [link])
        self.assertEqual(local_link_errors(path, "[public](https://example.invalid/fixture)"), [])

    def test_readme_counts_match_unique_owned_commands_not_registry_total(self):
        contract = json.loads((ROOT / "tests/cex/cli-contract.json").read_text())
        owners = {"gate-cex-" + profile for profile in contract["profiles"]}
        commands = {row["path"]: row for row in contract["commands"] if row["owner"] in owners}
        counts = Counter(row["owner"].removeprefix("gate-cex-") for row in commands.values())
        for name in ("README.md", "README_zh.md"):
            text = (ROOT / name).read_text()
            with self.subTest(document=name):
                self.assertNotIn("398", text)
                self.assertRegex(text, rf"\b{len(commands)}\b")
                for key, label in (("trade", "交易"), ("earn", "理财"), ("assets", "资产"),
                                   ("subaccount", "子账号"), ("affiliate", "返佣"), ("bot", "机器人")):
                    self.assertRegex(text, rf"(?:{key}|{label})\s+{counts[key]}\b")
                self.assertNotIn("--skill gate-market", text)
                self.assertIn("gate-cli-installer/SKILL.md", text)
                self.assertIn("gate-mcp-installer/SKILL.md", text)
                self.assertNotIn("全部 Gate Skills", text)
                self.assertNotIn("install all Gate MCP servers + Skills", text)

    def test_auditor_retains_the_approved_five_earn_products(self):
        body = (ROOT / "gate-cex-skill-audit/references/coverage-profiles.md").read_text()
        section = body.split("## gate-cex-earn\n", 1)[1].split("\n## ", 1)[0]
        references = section.split("Expected references: ", 1)[1].split("\n", 1)[0]
        self.assertEqual(set(re.findall(r"`([^`]+)`", references)), {
            "simple-earn-commands.md", "staking-commands.md", "dual-investment-commands.md",
            "auto-invest-commands.md", "collateral-loan-commands.md"})
        self.assertIn("outside this profile", section)
        self.assertNotIn("398", (ROOT / "gate-cex-skill-audit/references/cli-verification.md").read_text())

    def test_bilingual_catalog_covers_real_entries_and_uses_their_metadata_versions(self):
        """Prevent silent catalog omissions and stale duplicate version tables."""
        expected = {}
        for entry in (ROOT / "skills").glob("*/SKILL.md"):
            metadata = HELPERS.header(entry.read_text())
            version = metadata.get("version")
            if version is None and isinstance(metadata.get("metadata"), dict):
                version = metadata["metadata"].get("version")
            expected[entry.parent.name] = str(version) if version is not None else "—"
        for name, heading in (("README.md", "## Skills Overview"), ("README_zh.md", "## Skills 总览")):
            with self.subTest(document=name):
                text = (ROOT / name).read_text()
                catalog = text.split(heading, 1)[1].split("\n---", 1)[0]
                observed = {}
                for line in catalog.splitlines():
                    match = re.match(r"\| \[(gate-[a-z0-9-]+)\]", line)
                    if match:
                        self.assertNotIn(match[1], observed)
                        observed[match[1]] = line.split("|")[3].strip().strip("`")
                self.assertEqual(set(observed), set(expected))
                for skill, version in expected.items():
                    self.assertEqual(observed[skill], version, skill)
                self.assertNotRegex(text, r"(?:to|向) `main`(?: for review| 分支)")

    def test_installer_docs_preserve_product_boundaries_and_public_catalog(self):
        """Documentation must use the installed templates without promising CEX source copying."""
        cli = (ROOT / "skills/gate-cli-installer/README.md").read_text()
        mcp = (ROOT / "skills/gate-mcp-installer/README.md").read_text()
        self.assertIn("../../README.md#gate-cex-skill-20", cli)
        self.assertIn("../_shared/cex/cli-setup.md", cli)
        self.assertIn("--skill gate-info-research", cli)
        self.assertNotIn("gate-cli migrate --apply", cli)
        self.assertIn("Pay", cli)
        fragment = ROOT / "skills/gate-mcp-installer/scripts/mcp-fragments/claude/gatepay-merchant-discovery.json"
        url = json.loads(fragment.read_text())["gatepay-merchant-discovery"]["url"]
        self.assertIn(url, mcp)
        self.assertRegex(mcp, r"Neither Pay entry is\s+installed by default")

    def test_transport_only_intent_cannot_force_dex_or_bypass_product(self):
        text = (ROOT / "skills/gate-skills-disambiguation.md").read_text()
        section = text.split("### Scenario 19:", 1)[1].split("\n### Scenario ", 1)[0]
        for explicit in ("gate-cli cex", "gate-cli info", "gate-cli news", "gate-wallet",
                         "Payment/merchant-order", "insufficient to choose a domain",
                         "clarify", "Do not substitute a DEX or Pay operation"):
            self.assertIn(explicit, section)
        self.assertNotIn('Any mention of "gate-wallet", "CLI"', section)
        self.assertNotIn("Do NOT route to CEX", section)

    def test_examples_reference_existing_skills_and_preserve_cex_auditor_route(self):
        documents = [
            ROOT / "test-for-skill/test_skill.py",
            ROOT / "test-for-skill/skill-tester/SKILL.md",
            ROOT / "test-for-skill/skill-tester/README.md",
            ROOT / "test-for-skill/skill-validator/SKILL.md",
            ROOT / "test-for-skill/skill-validator/README.md",
        ]
        for path in documents:
            with self.subTest(document=path):
                text = path.read_text()
                self.assertNotRegex(text, r"gate-exchange-(?:spot|futures)\b")
                for name in re.findall(r"skills/(gate-[a-z-]+)/", text):
                    if name not in ("gate-cex-",):
                        self.assertTrue((ROOT / "skills" / name / "SKILL.md").is_file(), name)
        self.assertIn("gate-cex-skill-audit", documents[1].read_text())
        self.assertIn("gate-cex-skill-audit", documents[3].read_text())

    def test_legacy_runner_help_declares_its_legacy_input_contract(self):
        """Do not advertise current scenario layouts that the old parser cannot consume."""
        with tempfile.TemporaryDirectory(prefix="legacy-help-fixture-") as directory:
            base = Path(directory)
            # Only the optional import is mocked; --help must not construct a model client.
            (base / "anthropic.py").write_text(
                'class Anthropic:\n'
                '    def __init__(self):\n'
                '        raise AssertionError("help must not initialize a model client")\n')
            result = subprocess.run(
                [sys.executable, "-B", str(ROOT / "test-for-skill/test_skill.py"), "--help"],
                env={"PATH": os.defpath, "PYTHONPATH": str(base)}, cwd=base,
                text=True, capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("/path/to/legacy-skill", result.stdout)
            self.assertIn("not a current repository target", result.stdout)
            self.assertNotIn("gate-exchange-spot", result.stdout)


class InstallerFilterUnitTests(unittest.TestCase):
    def test_real_predicate_keeps_pay_and_rejects_new_and_old_cex_names(self):
        """Load only the side-effect-free production predicate, without installer startup."""
        match = re.search(r"^should_install_skill_source\(\) \{\n.*?^\}", INSTALLER.read_text(), re.M | re.S)
        self.assertIsNotNone(match)
        cases = {
            "": False, "gate-cex-trade": False, "gate-cex-earn": False,
            "gate-cex-future-product": False, "gate-exchange-spot": False,
            "gate-exchange-futures": False, "gate-exchange-pay-extra": False,
            "gate-exchange-pay": True, "gate-pay-x402": True, "gate-dex-market": True,
            "gate-info-coinanalysis": True, "gate-news-briefing": True, "_shared": True,
            "gate-info-space fixture": True,
        }
        for name, allowed in cases.items():
            with self.subTest(name=name):
                result = subprocess.run(
                    ["bash", "-c", match[0] + '\nshould_install_skill_source "$1"',
                     "predicate-test", name], capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0 if allowed else 1, result.stderr)


class InstallerEndToEndTests(unittest.TestCase):
    def fixture(self, platform):
        """Use documented per-client targets in child processes; never alter the host environment."""
        temporary = tempfile.TemporaryDirectory(prefix="installer-cleanup-regression-")
        self.addCleanup(temporary.cleanup)
        base = Path(temporary.name)
        source, binaries, temporary_files = base / "source", base / "bin", base / "tmp"
        binaries.mkdir()
        temporary_files.mkdir()
        excluded = {"gate-cex-trade", "gate-cex-earn", "gate-exchange-spot",
                    "gate-exchange-futures", "gate-exchange-pay-extra"}
        kept = {"gate-exchange-pay", "gate-pay-x402", "gate-dex-trade",
                "gate-info-coinanalysis", "gate-news-briefing", "_shared"}
        for name in excluded | kept:
            path = source / "skills" / name
            path.mkdir(parents=True)
            (path / "SKILL.md").write_text("synthetic source: " + name)
        registry, events = base / "registry.json", base / "events.jsonl"
        registry.write_text('{"unrelated-server": ["preserve"]}')
        peer = ROOT / "tests/fixtures/installer_host.py"
        for command in ("git", "mcporter", "npx", "gate-mcp"):
            wrapper = binaries / command
            wrapper.write_text("#!/bin/sh\nexec " + shlex.quote(sys.executable) + " -B " +
                               shlex.quote(str(peer)) + " " + command + ' "$@"\n')
            wrapper.chmod(0o755)
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node is an existing installer dependency for JSON merge")
        (binaries / "node").symlink_to(node)
        env = {
            "PATH": str(binaries) + os.pathsep + os.defpath, "TMPDIR": str(temporary_files),
            "CURSOR_USER_HOME": str(base / "cursor"), "CLAUDE_USER_HOME": str(base / "claude"),
            "CODEX_HOME": str(base / "codex"), "OPENCLAW_HOME": str(base / "openclaw"),
            "INSTALL_TEST_SOURCE": str(source), "INSTALL_TEST_REGISTRY": str(registry),
            "INSTALL_TEST_EVENTS": str(events), "PYTHONDONTWRITEBYTECODE": "1",
        }
        configs = {"cursor": base / "cursor/.cursor/mcp.json",
                   "claude": base / "claude/.claude.json",
                   "codex": base / "codex/config.toml", "openclaw": registry}
        skills = {"cursor": base / "cursor/.cursor/skills",
                  "claude": base / "claude/.claude/skills",
                  "codex": base / "codex/skills", "openclaw": base / "openclaw/skills"}
        config = configs[platform]
        config.parent.mkdir(parents=True, exist_ok=True)
        if platform == "codex":
            config.write_text('[mcp_servers.unrelated-server]\ncommand = "preserve"\n')
        elif platform != "openclaw":
            config.write_text('{"mcpServers": {"unrelated-server": {"command": "preserve"}}}')
        destination = skills[platform]
        for name in ("gate-cex-trade", "gate-exchange-spot"):
            path = destination / name
            path.mkdir(parents=True)
            (path / "keep.txt").write_text("existing user installation")
        return base, env, config, destination, excluded, kept

    def execute(self, platform, env, *arguments):
        return subprocess.run(
            ["bash", str(INSTALLER), "--platform", platform, *arguments],
            cwd=ROOT, env=env, input="\n\n", capture_output=True, text=True, timeout=20)

    def test_four_clients_keep_exchange_modes_and_install_only_non_cex_sources(self):
        """Exercise real option/merge/copy paths, including repeat runs and existing installs."""
        for platform in ("cursor", "claude", "codex", "openclaw"):
            with self.subTest(platform=platform):
                base, env, config, destination, excluded, kept = self.fixture(platform)
                options = [argument for name in ("main", "cex-public", "cex-exchange", "dex",
                                                "info", "news", "gatepay-local", "gatepay-discovery")
                           for argument in ("--mcp", name)]
                for _ in range(2):
                    result = self.execute(platform, env, *options)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                for name in kept:
                    self.assertEqual((destination / name / "SKILL.md").read_text(),
                                     "synthetic source: " + name)
                for name in excluded:
                    self.assertFalse((destination / name / "SKILL.md").exists(), name)
                for name in ("gate-cex-trade", "gate-exchange-spot"):
                    self.assertEqual((destination / name / "keep.txt").read_text(),
                                     "existing user installation")
                self.assertEqual(json.loads(Path(env["INSTALL_TEST_REGISTRY"]).read_text())
                                 ["unrelated-server"], ["preserve"])
                if platform == "openclaw":
                    servers = json.loads(config.read_text())
                    expected = {"gate", "gate-cex-pub", "gate-cex-ex"}
                    domain_servers = {"gate-dex", "gate-info", "gate-news"}
                elif platform == "codex":
                    servers = tomllib.loads(config.read_text())["mcp_servers"]
                    expected = {"Gate", "gate-cex-pub", "gate-cex-ex"}
                    domain_servers = {"gate-dex", "gate-info", "gate-news"}
                else:
                    servers = json.loads(config.read_text())["mcpServers"]
                    expected = {"Gate", "gate-cex-pub", "gate-cex-ex"}
                    domain_servers = {"Gate-Dex", "Gate-Info", "Gate-News"}
                self.assertTrue(expected | domain_servers | {
                    "gate-dex-sec", "gatepay-local-mcp", "gatepay-merchant-discovery",
                    "unrelated-server"} <= servers.keys())
                # Check the actual generated config, including mcporter's real argv shape.
                discovery = servers["gatepay-merchant-discovery"]
                actual_url = (discovery[discovery.index("--url") + 1]
                              if platform == "openclaw" else discovery["url"])
                self.assertEqual(actual_url, DISCOVERY_URL)
                events = [json.loads(line) for line in Path(env["INSTALL_TEST_EVENTS"]).read_text().splitlines()]
                self.assertTrue(any(event["command"] == "git" for event in events))
                self.assertFalse(any(event["command"] in ("npx", "gate-mcp") for event in events))
                self.assertEqual(list((base / "tmp").iterdir()), [])

    def test_discovery_only_uses_public_https_without_credentials_or_skill_download(self):
        """Keep optional discovery usable without installing payment or Exchange servers."""
        for platform in ("cursor", "claude", "codex", "openclaw"):
            with self.subTest(platform=platform):
                base, env, config, destination, _, _ = self.fixture(platform)
                result = self.execute(platform, env, "--mcp", "gatepay-discovery", "--no-skills")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                if platform == "openclaw":
                    servers = json.loads(config.read_text())
                    entry = servers["gatepay-merchant-discovery"]
                    self.assertEqual(entry, ["--url", DISCOVERY_URL])
                elif platform == "codex":
                    servers = tomllib.loads(config.read_text())["mcp_servers"]
                    self.assertEqual(servers["gatepay-merchant-discovery"]["url"], DISCOVERY_URL)
                else:
                    servers = json.loads(config.read_text())["mcpServers"]
                    self.assertEqual(servers["gatepay-merchant-discovery"]["url"], DISCOVERY_URL)
                self.assertEqual(set(servers), {"unrelated-server", "gatepay-merchant-discovery"})
                events_path = Path(env["INSTALL_TEST_EVENTS"])
                events = ([json.loads(line) for line in events_path.read_text().splitlines()]
                          if events_path.exists() else [])
                self.assertFalse(any(e["command"] in ("git", "npx", "gate-mcp") for e in events))
                self.assertEqual((destination / "gate-cex-trade/keep.txt").read_text(),
                                 "existing user installation")
                self.assertEqual(list((base / "tmp").iterdir()), [])

    def test_readme_x402_command_generates_only_the_documented_opt_in_servers(self):
        """Run the actual README command; only download/service peers are fixtures."""
        commands = []
        for name in ("README.md", "README_zh.md", "skills/gate-mcp-installer/README.md"):
            candidates = [line for line in (ROOT / name).read_text().splitlines()
                          if line.startswith("bash ") and "--mcp gatepay-local" in line
                          and "--mcp gatepay-discovery" in line and "--no-skills" in line]
            self.assertEqual(len(candidates), 1, name)
            commands.append(shlex.split(candidates[0]))
        self.assertTrue(all(argv == commands[0] for argv in commands))
        base, env, config, destination, _, _ = self.fixture("cursor")
        argv = commands[0]
        result = subprocess.run([argv[0], str(ROOT / argv[1]), *argv[2:]], cwd=ROOT,
                                env=env, input="\n\n", capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        servers = json.loads(config.read_text())["mcpServers"]
        self.assertEqual(set(servers), {"unrelated-server", "gatepay-local-mcp", "gatepay-merchant-discovery"})
        self.assertEqual(servers["gatepay-merchant-discovery"]["url"], DISCOVERY_URL)
        self.assertEqual(servers["gatepay-local-mcp"]["command"], "npx")
        self.assertFalse(Path(env["INSTALL_TEST_EVENTS"]).exists())
        self.assertEqual((destination / "gate-cex-trade/keep.txt").read_text(), "existing user installation")
        self.assertEqual(list((base / "tmp").iterdir()), [])

    def test_no_skills_does_not_clone_or_modify_existing_skill(self):
        _, env, _, destination, _, _ = self.fixture("cursor")
        result = self.execute("cursor", env, "--mcp", "cex-exchange", "--no-skills")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(Path(env["INSTALL_TEST_EVENTS"]).exists())
        self.assertEqual((destination / "gate-cex-trade/keep.txt").read_text(),
                         "existing user installation")

    def test_default_selection_keeps_legacy_pay_exchange_modes(self):
        _, env, config, destination, _, _ = self.fixture("cursor")
        result = self.execute("cursor", env)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        servers = json.loads(config.read_text())["mcpServers"]
        self.assertTrue({"Gate", "gate-cex-pub", "gate-cex-ex"} <= servers.keys())
        self.assertNotIn("gatepay-local-mcp", servers, "x402 remains opt-in")
        self.assertTrue((destination / "gate-exchange-pay/SKILL.md").is_file())
        self.assertFalse((destination / "gate-cex-earn").exists())

    def test_unknown_selection_is_rejected_before_any_external_boundary(self):
        _, env, config, _, _, _ = self.fixture("cursor")
        before = config.read_bytes()
        result = self.execute("cursor", env, "--mcp", "unknown-fixture")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unknown MCP", result.stderr)
        self.assertEqual(config.read_bytes(), before)
        self.assertFalse(Path(env["INSTALL_TEST_EVENTS"]).exists())

    def test_clone_failure_leaves_existing_skills_and_cleans_temporary_files(self):
        base, env, _, destination, _, kept = self.fixture("cursor")
        env["INSTALL_TEST_CLONE_FAIL"] = "1"
        result = self.execute("cursor", env, "--mcp", "info")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((destination / "gate-cex-trade/keep.txt").read_text(),
                         "existing user installation")
        for name in kept:
            self.assertFalse((destination / name).exists())
        self.assertEqual(list((base / "tmp").iterdir()), [])


if __name__ == "__main__":
    unittest.main()
