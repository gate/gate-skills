import asyncio
import importlib.util
import json
import io
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location('stream', Path(__file__).with_name('futures-market-stream.py'))
stream = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(stream)
CHANNEL = 'futures.tickers'
ACK = {'channel': CHANNEL, 'event': 'subscribe', 'result': {'status': 'success'}}
DATA = {'channel': CHANNEL, 'event': 'update', 'result': [{'contract': 'BTC_USDT', 'size': '0.125'}]}


class Socket:
    def __init__(self, messages):
        self.messages = iter(messages)
        self.sent = []
        self.closed = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        self.closed = True

    async def send(self, message):
        self.sent.append(json.loads(message))

    async def recv(self):
        message = next(self.messages, None)
        if isinstance(message, Exception):
            raise message
        if message is None:
            await asyncio.sleep(10)
        return message if isinstance(message, str) else json.dumps(message)


class Tests(unittest.IsolatedAsyncioTestCase):
    def args(self, **kwargs):
        args = stream.arguments(['--settle', 'usdt', '--channel', CHANNEL,
                                 '--payload', '["BTC_USDT"]'])
        args.seconds = 0.03
        for k, v in kwargs.items():
            setattr(args, k, v)
        return args

    async def run_stream(self, sockets, **kwargs):
        calls, records = [], []
        def connect(url, **options):
            calls.append((url, options))
            return sockets[len(calls) - 1]
        code = await stream.observe(self.args(**kwargs), connect, records.append)
        return code, records, calls

    async def test_exact_numeric_output(self):
        raw = ('{"channel":"futures.tickers","event":"update","result":'
               '{"price":0.10000000000000001,"size":1.234567890123456789e-20,'
               '"large":123456789012345678901234567890,"text":"0.10000000000000001"}}')
        code, records, _ = await self.run_stream([Socket([ACK, raw])])
        self.assertEqual(code, 0)
        rendered = io.StringIO()
        with redirect_stdout(rendered):
            stream.observe.__globals__['output'](next(r for r in records if r['type'] == 'message'))
        decoded = json.loads(rendered.getvalue(), parse_float=Decimal)['message']['result']
        self.assertEqual(decoded['price'], Decimal('0.10000000000000001'))
        self.assertEqual(decoded['size'], Decimal('1.234567890123456789e-20'))
        self.assertEqual(decoded['large'], 123456789012345678901234567890)
        self.assertIsInstance(decoded['text'], str)
        self.assertIn('"price":0.10000000000000001', rendered.getvalue())

    async def test_nonfinite_json_rejected_without_data(self):
        for constant in ('NaN', 'Infinity', '-Infinity', '1e999999999999999999999999999999999999999999999'):
            raw = '{"channel":"futures.tickers","event":"update","result":{"price":' + constant + '}}'
            code, records, _ = await self.run_stream([Socket([ACK, raw])])
            self.assertEqual(code, 1)
            self.assertEqual(records[-1]['status'], 'error')
            self.assertEqual(records[-1]['updates'], 0)
            self.assertFalse(any(r['type'] == 'message' for r in records))

    async def test_server_error_decimal_keeps_error_status(self):
        raw = '{"channel":"futures.tickers","error":{"price":0.10000000000000001}}'
        code, records, _ = await self.run_stream([Socket([raw])])
        self.assertEqual(code, 1)
        self.assertIn('0.10000000000000001', records[-1]['error'])

    def test_delivery_obu_levels_are_product_specific(self):
        def parse(product, payload):
            return stream.arguments(['--product', product, '--settle', 'usdt',
                                     '--channel', 'futures.obu', '--payload', json.dumps(payload)])
        for depth in ('20', '100'):
            self.assertEqual(parse('delivery', ['ob.BTC_USDT_20261225.' + depth]).product, 'delivery')
        for payload in (['ob.BTC_USDT_20261225.400'], ['ob.BTC_USDT_20261225.20', 'ob.BTC_USDT_20261225.400'],
                        ['ob.BTC_USDT_20261225.100.extra']):
            with self.assertRaises(SystemExit), redirect_stdout(io.StringIO()):
                parse('delivery', payload)
        self.assertEqual(parse('perpetual', ['ob.BTC_USDT.400']).product, 'perpetual')

    async def test_unsupported_dependency_fails_explicitly(self):
        from unittest.mock import patch
        records = []
        with patch('websockets.__version__', '14.2'):
            code = await stream.observe(self.args(), emit=records.append)
        self.assertEqual(code, 1)
        self.assertIn('websockets>=15', records[-1]['error'])

    async def test_ack_only_is_not_data(self):
        code, records, _ = await self.run_stream([Socket([ACK])])
        self.assertEqual(code, 0)
        self.assertEqual(records[-1]['status'], 'ack_only')
        self.assertEqual(records[-1]['updates'], 0)

    async def test_data_before_ack_decimal_and_output_cap(self):
        ws = Socket([DATA, ACK, DATA, DATA])
        code, records, calls = await self.run_stream([ws], max_messages=1)
        self.assertEqual(code, 0)
        self.assertEqual(records[-1]['updates'], 3)
        samples = [r for r in records if r['type'] == 'message']
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0]['message'], DATA)
        self.assertEqual(calls[0][1]['additional_headers'], {'X-Gate-Size-Decimal': '1'})
        self.assertEqual(calls[0][0], 'wss://fx-ws.gateio.ws/v4/ws/usdt')
        self.assertTrue(ws.closed)

    async def test_empty_and_unrelated_are_not_business(self):
        empty = dict(DATA, result=[])
        other = dict(DATA, channel='futures.trades')
        _, records, _ = await self.run_stream([Socket([ACK, empty, other])])
        self.assertEqual(records[-1]['updates'], 0)
        self.assertEqual(records[-1]['empty_updates'], 1)

    async def test_subscription_error_no_retry(self):
        error = dict(ACK, error={'code': 2, 'message': 'bad payload'})
        code, records, calls = await self.run_stream([Socket([error])])
        self.assertEqual(code, 1)
        self.assertEqual(records[-1]['status'], 'error')
        self.assertEqual(len(calls), 1)

    async def test_global_error_and_bad_json_are_errors(self):
        for message in ({'error': {'code': 2, 'message': 'rejected'}}, ['not', 'an', 'object']):
            code, records, calls = await self.run_stream([Socket([message])])
            self.assertEqual(code, 1)
            self.assertEqual(records[-1]['status'], 'error')
            self.assertEqual(len(calls), 1)

    async def test_reconnect_clears_ack_and_resubscribes(self):
        first, second = Socket([ACK, DATA, OSError('closed')]), Socket([])
        code, records, calls = await self.run_stream([first, second])
        self.assertEqual(code, 1)
        self.assertEqual(len(calls), 2)
        self.assertEqual(first.sent[0], second.sent[0])
        self.assertFalse(records[-1]['connections'][1]['ack'])
        self.assertEqual(records[-1]['status'], 'no_confirmation')
        self.assertTrue(first.closed and second.closed)

    async def test_upgrade_reconnect_is_bounded(self):
        upgrade = {'channel': 'futures.system', 'event': 'update', 'result': {'type': 'upgrade'}}
        code, records, calls = await self.run_stream([Socket([upgrade]), Socket([upgrade])])
        self.assertEqual(code, 1)
        self.assertEqual(len(calls), 2)
        self.assertEqual(records[-1]['status'], 'error')

    async def test_no_ack_with_data_is_unconfirmed(self):
        code, records, _ = await self.run_stream([Socket([DATA])])
        self.assertEqual(code, 1)
        self.assertEqual(records[-1]['status'], 'data_without_ack')

    def test_invalid_arguments(self):
        invalid = [('--channel', 'futures.orders'), ('--settle', 'evil'),
                   ('--payload', '{}'), ('--payload', '["x\\n"]'),
                   ('--seconds', 'nan'), ('--seconds', '61'), ('--max-messages', '0')]
        import contextlib
        import io
        for key, value in invalid:
            with self.subTest(key=key, value=value), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    stream.arguments(['--settle', 'usdt', '--channel', CHANNEL,
                                      '--payload', '["BTC_USDT"]', key, value])


    def public_args(self, product, channel, payload, settle=None):
        argv = ['--product', product, '--channel', channel, '--payload', json.dumps(payload)]
        if settle:
            argv += ['--settle', settle]
        args = stream.arguments(argv)
        args.seconds = 0.03
        return args

    def test_public_product_routes(self):
        cases = [
            ('spot', 'spot.tickers', ['BTC_USDT'], None, 'wss://api.gateio.ws/ws/v4/'),
            ('leverage', 'spot.tickers', ['BTC_USDT'], None, 'wss://api.gateio.ws/ws/v4/'),
            ('perpetual', CHANNEL, ['BTC_USDT'], 'usd1', 'wss://fx-ws.gateio.ws/v4/ws/usd1'),
            ('delivery', CHANNEL, ['BTC_USDT_20261030'], 'usdt', 'wss://fx-ws.gateio.ws/v4/ws/delivery/usdt'),
            ('options', 'options.ul_tickers', ['BTC_USDT'], None, 'wss://op-ws.gateio.live/v4/ws'),
            ('stocks', 'stock.tickers', {'markets': ['AAPL']}, None, 'wss://fx-ws.gateio.ws/v4/ws/stock'),
            ('cfd', 'tradfi.tickers', {'markets': ['XAUUSD']}, None, 'wss://fx-ws.gateio.ws/v4/ws/tradfi'),
        ]
        for product, channel, payload, settle, endpoint in cases:
            with self.subTest(product=product):
                args = self.public_args(product, channel, payload, settle)
                self.assertEqual(args.endpoint, endpoint)
                self.assertEqual(args.payload, payload)

    def test_public_scope_and_schema_rejections(self):
        import contextlib
        import io
        cases = [
            ('stocks', 'futures.tickers', ['BTC_USDT'], None),
            ('stocks', 'stock.orders', ['AAPL'], None),
            ('stocks', 'stock.tickers', ['AAPL'], None),
            ('stocks', 'stock.tickers', {'markets': ['AAPL'], 'auth': 'secret'}, None),
            ('stocks', 'stock.tickers', {'markets': []}, None),
            ('stocks', 'stock.tickers', {'markets': ['AAPL']}, 'usdt'),
            ('delivery', CHANNEL, ['BTC_USDT_20261030'], 'usd1'),
            ('delivery', CHANNEL, ['BTC_USD_20261225'], 'btc'),
            ('perpetual', CHANNEL, ['BTC_USDT'], None),
            ('options', 'options.orders', ['BTC_USDT'], None),
            ('options', 'options.ul_tickers', {'underlyings': ['BTC_USDT']}, None),
            ('options', 'options.contract_candlesticks', {'underlyings': ['BTC_USDT']}, None),
            ('options', 'options.contract_tickers', {'underlyings': ['BTC_USDT'], 'auth': {}}, None),
            ('options', 'options.contracts', {'underlyings': ['BTC_USDT'] * 21}, None),
        ]
        for args in cases:
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.public_args(*args)

    def test_option_scoped_objects(self):
        for channel, payload in [
            ('options.contract_tickers', {'underlyings': ['BTC_USDT'], 'change_from': 'utc0'}),
            ('options.contract_candlesticks', {'underlyings': ['BTC_USDT'], 'interval': '1m'}),
            ('options.settlements', {'contracts': ['BTC_USDT-20261030-80000-C']}),
        ]:
            self.assertEqual(self.public_args('options', channel, payload).payload, payload)

    async def test_stock_alias_preserves_raw_and_is_stock_only(self):
        alias = {'channel': 'tspot.tickers', 'event': 'update', 'result': [{'symbol': 'AAPL', 'last_price': '300', 'status_code': 3}]}
        records, calls = [], []
        args = self.public_args('stocks', 'stock.tickers', {'markets': ['AAPL']})
        ws = Socket([alias, dict(ACK, channel='stock.tickers')])
        def connect(endpoint, **kwargs):
            calls.append(endpoint)
            return ws
        code = await stream.observe(args, connect, records.append)
        self.assertEqual(code, 0)
        self.assertEqual(records[-1]['updates'], 1)
        self.assertEqual(records[-1]['product'], 'stocks')
        self.assertEqual(records[-1]['environment'], 'production')
        self.assertEqual(next(r['message'] for r in records if r['type'] == 'message'), alias)
        self.assertEqual(calls, ['wss://fx-ws.gateio.ws/v4/ws/stock'])
        _, old_records, _ = await self.run_stream([Socket([ACK, alias])])
        self.assertEqual(old_records[-1]['updates'], 0)


if __name__ == '__main__':
    unittest.main()
