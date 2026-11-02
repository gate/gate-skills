"""Trade restoration regressions and offline package/stream end-to-end checks.

No business CLI is executed. Stream tests mock only the WebSocket connection;
argument parsing, subscription, response handling and JSON output remain real.
"""
import asyncio
from contextlib import redirect_stdout, redirect_stderr
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / 'skills/gate-cex-trade'


def module(name, path):
    """Load only repository-owned test/build tools, never documented CLI examples."""
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


TOOLS = module('trade_builder', ROOT / 'scripts/cex_skills.py')
CONTRACT = json.loads((ROOT / 'tests/cex/cli-contract.json').read_text())
STREAM_TESTS = module('trade_stream_cases', TARGET / 'scripts/test_futures_market_stream.py')


class TradeContractTests(unittest.TestCase):
    def test_full_source_contract_and_variants(self):
        result = TOOLS.inspect(TARGET, CONTRACT)
        self.assertEqual(result['status'], 'PASS', result)
        self.assertEqual(result['commands'], 283)
        self.assertEqual(len(list((TARGET / 'references').glob('*-commands.md'))), 13)
        self.assertEqual(len(list((TARGET / 'references/models').glob('*.md'))), 13)

    def test_localized_data_is_display_only_and_complete(self):
        # Explicitly reviewed locale data does not exempt normative Markdown from C7.
        data = json.loads((TARGET / 'references/localized-examples.json').read_text())
        self.assertEqual(set(data), {'locale', 'purpose', 'intent_examples', 'failure_messages'})
        self.assertEqual(data['locale'], 'zh-CN')
        self.assertEqual(len(data['intent_examples']), 5)
        self.assertEqual(len(data['failure_messages']), 17)
        self.assertEqual(len({x['situation'] for x in data['failure_messages']}), 17)
        for item in data['failure_messages']:
            self.assertEqual(set(item), {'situation', 'toast', 'next_step'})
            self.assertTrue(item['toast'].startswith('Toast：'))
            self.assertTrue(item['next_step'].startswith('建议后续操作：'))
        for path in TARGET.rglob('*.md'):
            self.assertNotRegex(path.read_text(), r'[\u3400-\u9fff]', str(path))

    def test_private_fallback_and_false_global_blocks_do_not_return(self):
        combined = '\n'.join(p.read_text() for p in TARGET.rglob('*.md'))
        for obsolete in ('use a compatible API executor or block', 'block every Trail CLI operation',
                         'has no `cex stock` command', 'chase is API-only',
                         'Countdown cancel is intentionally excluded', 'side=1` buy/`2` sell'):
            self.assertNotIn(obsolete, combined)
        for write in ('gate-cli cex mcl create`', 'gate-cli cex mcl repay`', 'gate-cli cex mcl collateral`'):
            self.assertNotIn(write, combined)
        handoff = (TARGET / 'references/vipfee.md').read_text()
        for requirement in ('gate-cex-earn', 'cumulative limits', 'execution status', 'unresolved', 'never repeated'):
            self.assertIn(requirement, handoff)

    def test_delivery_table_retains_all_columns(self):
        # GFM treats even inline-code pipes as column separators unless escaped.
        rows = [line for line in (TARGET / 'references/delivery.md').read_text().splitlines() if line.startswith('|')]
        import re
        widths = [len(re.split(r'(?<!\\)\|', line)) - 2 for line in rows]
        self.assertTrue(widths)
        self.assertEqual(set(widths), {4})


class TradePackageE2ETests(unittest.TestCase):
    def test_build_install_check_and_tamper_rejection(self):
        # Real builder and checker subprocess; the isolated install has no siblings.
        with tempfile.TemporaryDirectory(prefix='trade-repair-e2e-') as folder:
            base = Path(folder)
            output = base / 'build'
            TOOLS.build(ROOT, output, CONTRACT, profiles=('trade',))
            install = base / 'installed/gate-cex-trade'
            install.parent.mkdir()
            shutil.move(str(output / 'gate-cex-trade'), install)
            command = [sys.executable, '-B', str(ROOT / 'scripts/cex_skills.py'), 'check',
                       '--target', str(install), '--contract', str(ROOT / 'tests/cex/cli-contract.json'), '--package']
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertEqual(json.loads(result.stdout)['commands'], 283)
            self.assertEqual(list(install.parent.iterdir()), [install])
            self.assertFalse(list(install.rglob('*.pyc')))
            self.assertEqual(json.loads((install / 'references/localized-examples.json').read_text()),
                             json.loads((TARGET / 'references/localized-examples.json').read_text()))
            (install / 'references/spot-commands.md').unlink()
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout)['status'], 'FAIL')

    def test_parsed_stream_to_output_and_error(self):
        # Mock the wire only: validate argv -> subscribe -> receive -> exact output -> close.
        stream = STREAM_TESTS.stream
        for messages, code, status in (([STREAM_TESTS.ACK, STREAM_TESTS.DATA], 0, 'data'),
                                       ([dict(STREAM_TESTS.ACK, error={'code': 2})], 1, 'error')):
            args = stream.arguments(['--settle', 'usdt', '--channel', 'futures.tickers',
                                     '--payload', '["BTC_USDT"]', '--seconds', '1'])
            socket = STREAM_TESTS.Socket(messages)
            calls = []
            def connect(endpoint, **kwargs):
                calls.append(endpoint)
                return socket
            out = io.StringIO()
            with redirect_stdout(out):
                actual = asyncio.run(stream.observe(args, connect))
            records = [json.loads(line) for line in out.getvalue().splitlines()]
            self.assertEqual(actual, code)
            self.assertEqual(records[-1]['status'], status)
            self.assertEqual(calls, ['wss://fx-ws.gateio.ws/v4/ws/usdt'])
            self.assertEqual(socket.sent[0]['event'], 'subscribe')
            self.assertEqual(socket.sent[0]['payload'], ['BTC_USDT'])
            self.assertTrue(socket.closed)
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            stream.arguments(['--product', 'stocks', '--channel', 'stock.orders', '--payload', '["AAPL"]'])


def load_tests(loader, tests, pattern):
    """Keep the restored helper's unit/error/boundary tests in the existing CEX entry."""
    tests.addTests(loader.loadTestsFromModule(STREAM_TESTS))
    return tests
