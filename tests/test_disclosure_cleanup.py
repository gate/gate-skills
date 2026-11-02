"""Public-content contracts and negative fixtures; never contact a business service.

Known removed hosts are represented by digests so regressions do not republish
infrastructure names. Key/Secret examples and historical Git objects are outside
this task's user-approved scope. Installer E2E cases live in test_skill_content.
"""
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import tomllib
import unittest
from unittest import mock
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DISCOVERY_URL = "https://openplatform.gateapi.io/pay-mcp-server/mcp"
REMOVED_HOST_DIGESTS = frozenset({
    "676c9c5b810b267e7d5eb6e4f37bc40261556da1dae4b73d1c0a02d74c62b35e",
    "4fbae9d73b0114253fbc61d1d2dde31fd6280b5faf2320b647943bd96c65c3ce",
    "a6183454e4004acc09890205ee9ecfab08d519513c466b7b7d91c37cc396f846",
    "4ff05b3f0472605a04083b706ac9609e46c3d57cf30d318eeba37de5c3a1766e",
})


def disclosure_errors(body, fixture=False):
    """Return only classifications/lines, without echoing private matched values."""
    decoded = body
    for _ in range(3):
        decoded = html.unescape(unquote(decoded)).replace("\\/", "/")
    decoded = re.sub(r"\\u([a-fA-F0-9]{4})", lambda m: chr(int(m[1], 16)), decoded)
    errors = []
    for number, line in enumerate(decoded.splitlines(), 1):
        hosts = re.findall(r"(?<![\w.-])(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?![\w.-])", line)
        for host in hosts:
            host = host.lower().rstrip(".")
            if (hashlib.sha256(host.encode()).hexdigest() in REMOVED_HOST_DIGESTS
                    or (not fixture and host.endswith(".internal"))):
                errors.append(("private-host", number))
        for match in re.finditer(r"/(Users|home)/([\w.-]+)/|[A-Za-z]:[\\/]Users[\\/]([\w.-]+)[\\/]", line):
            user = match[2] or match[3]
            # Managed runtime paths and explicit synthetic test homes are not PII.
            allowed = user in {"node", "runner", "username"}
            allowed = allowed or (fixture and (user == "alice" or user.startswith("fixture")))
            if not allowed:
                errors.append(("personal-home", number))
        if re.search(r"docs/handoff/\d{4}-\d{2}-\d{2}-[^\s`]+internal-archive", line):
            errors.append(("internal-archive-locator", number))
    return sorted(set(errors))


class DisclosureRuleUnitTests(unittest.TestCase):
    """Guard normal content, encoded negatives and the explicit fixture boundary."""
    def test_public_and_generic_runtime_content_is_allowed(self):
        for text in (DISCOVERY_URL, "https://api.gatemcp.ai/mcp/exchange",
                     "~/.gate-cli/config.yaml", "/home/node/.openclaw/skills/bin", ""):
            with self.subTest(text=text):
                self.assertEqual(disclosure_errors(text), [])

    def test_plain_and_encoded_private_reference_is_rejected(self):
        for text in ("https://service.internal/mcp", "https%3A%2F%2Fservice.internal/mcp",
                     r"https:\/\/service.internal/mcp", r"https://service\u002einternal/mcp"):
            with self.subTest(text=text):
                self.assertIn(("private-host", 1), disclosure_errors(text))
        self.assertEqual(disclosure_errors("https://service.internal/mcp", fixture=True), [])

    def test_personal_home_and_archive_locator_are_rejected_without_echo(self):
        for text in ("/Users/fixture-owner/private/file", r"C:\Users\fixture-owner\private\file"):
            result = disclosure_errors(text)
            self.assertEqual(result, [("personal-home", 1)])
            self.assertNotIn("fixture-owner", repr(result))
        archive = "docs/" + "handoff/" + "2099-01-01-fixture-internal-archive/"
        self.assertEqual(disclosure_errors(archive), [("internal-archive-locator", 1)])
        self.assertEqual(disclosure_errors("/Users/fixture-owner/file", fixture=True), [])

    def test_fixture_exception_does_not_waive_a_known_removed_host(self):
        # Exercise the priority of an explicit deny over synthetic-fixture exemptions.
        host = "service.example.invalid"
        with mock.patch(__name__ + ".REMOVED_HOST_DIGESTS", {hashlib.sha256(host.encode()).hexdigest()}):
            self.assertEqual(disclosure_errors("https://" + host + "/mcp", fixture=True),
                             [("private-host", 1)])


class RepositoryDisclosureContractTests(unittest.TestCase):
    def test_current_tracked_text_has_no_confirmed_disclosure_regressions(self):
        paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
        errors = []
        for name in filter(None, paths):
            path = ROOT / name
            if not path.is_file():
                continue  # Staged deletions are intentionally absent from the current tree.
            raw = path.read_bytes()
            if raw.startswith(b"\x89PNG\r\n\x1a\n"):
                continue  # Image pixels require the separate recorded OCR/visual review.
            errors.extend((name, rule, line) for rule, line in disclosure_errors(
                raw.decode("utf-8"), fixture=name.startswith("tests/")))
        self.assertEqual(errors, [])

    def test_all_discovery_templates_match_existing_public_pay_documentation(self):
        directory = ROOT / "skills/gate-mcp-installer/scripts/mcp-fragments"
        for platform in ("claude", "cursor"):
            obj = json.loads((directory / platform / "gatepay-merchant-discovery.json").read_text())
            self.assertEqual(obj["gatepay-merchant-discovery"]["url"], DISCOVERY_URL)
        obj = tomllib.loads((directory / "codex/gatepay-merchant-discovery.toml").read_text())
        self.assertEqual(obj["mcp_servers"]["gatepay-merchant-discovery"]["url"], DISCOVERY_URL)
        entries = [line.split("|") for line in (directory / "openclaw/servers.manifest").read_text().splitlines()
                   if line.startswith("gatepay-merchant-discovery|")]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0][2], DISCOVERY_URL)
        self.assertIn('"url": "' + DISCOVERY_URL + '"', (ROOT / "skills/gate-pay-x402/SKILL.md").read_text())

    def test_optional_homepages_and_unsafe_screenshot_are_removed(self):
        for domain in ("market", "trade", "wallet"):
            text = (ROOT / f"skills/gate-dex-{domain}-cli/SKILL.md").read_text()
            self.assertNotRegex(text, r"(?m)^homepage:")
        self.assertFalse((ROOT / "image/codex-terminal-install-1.png").exists())
        for name in ("README.md", "README_zh.md"):
            self.assertNotIn("(image/codex-terminal-install-1.png)", (ROOT / name).read_text())


if __name__ == "__main__":
    unittest.main()
