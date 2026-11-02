#!/usr/bin/env python3
"""Bounded public market JSON subscriptions; no local order book."""
import argparse
import asyncio
import json
import math
import re
from decimal import Decimal, DecimalException
import time

FUTURES = tuple('futures.' + name for name in (
    'tickers', 'trades', 'book_ticker', 'order_book', 'order_book_update',
    'obu', 'rpi_order_book', 'rpi_obu', 'candlesticks', 'contract_stats',
    'public_liquidates', 'contract_info', 'adl_warning',
))
SPOT = tuple('spot.' + name for name in (
    'tickers', 'trades', 'book_ticker', 'order_book', 'order_book_update',
    'obu', 'rpi_order_book', 'rpi_obu', 'candlesticks',
))
OPTIONS = tuple('options.' + name for name in (
    'contract_tickers', 'ul_tickers', 'trades', 'ul_trades', 'ul_price',
    'mark_prices', 'settlements', 'contracts', 'contract_candlesticks',
    'ul_candlesticks', 'book_ticker', 'order_book', 'order_book_update',
))
OPTION_SCOPES = {'options.' + name for name in (
    'contract_tickers', 'contract_candlesticks', 'book_ticker', 'trades',
    'mark_prices', 'contracts', 'settlements',
)}
PRODUCTS = {
    'spot': ('wss://api.gateio.ws/ws/v4/', SPOT),
    'leverage': ('wss://api.gateio.ws/ws/v4/', SPOT),
    'perpetual': ('wss://fx-ws.gateio.ws/v4/ws/{settle}', FUTURES),
    'delivery': ('wss://fx-ws.gateio.ws/v4/ws/delivery/{settle}', tuple(
        'futures.' + name for name in ('tickers', 'trades', 'book_ticker', 'order_book', 'order_book_update', 'obu', 'candlesticks'))),
    'options': ('wss://op-ws.gateio.live/v4/ws', OPTIONS),
    'stocks': ('wss://fx-ws.gateio.ws/v4/ws/stock', ('stock.tickers', 'stock.orderbooks', 'stock.kline')),
    'cfd': ('wss://fx-ws.gateio.ws/v4/ws/tradfi', ('tradfi.tickers', 'tradfi.order_book', 'tradfi.candlesticks')),
}
CHANNELS = tuple(sorted({channel for _, channels in PRODUCTS.values() for channel in channels}))


def short_string(value):
    return isinstance(value, str) and 1 <= len(value) <= 128 and all(ord(c) >= 32 and ord(c) != 127 for c in value)


def string_list(value):
    return isinstance(value, list) and 1 <= len(value) <= 20 and all(short_string(x) for x in value)


def valid_payload(channel, payload):
    if channel in ('stock.tickers', 'tradfi.tickers'):
        return isinstance(payload, dict) and set(payload) == {'markets'} and string_list(payload['markets'])
    if isinstance(payload, list):
        return string_list(payload)
    if not isinstance(payload, dict) or channel not in OPTION_SCOPES:
        return False
    allowed = {'underlyings', 'contracts'}
    if channel == 'options.contract_tickers':
        allowed.add('change_from')
    if channel == 'options.contract_candlesticks':
        allowed.add('interval')
        if not short_string(payload.get('interval')):
            return False
    if not set(payload) <= allowed:
        return False
    scopes = [payload[k] for k in ('underlyings', 'contracts') if k in payload]
    if not scopes or not all(isinstance(v, list) and all(short_string(x) for x in v) for v in scopes):
        return False
    if not 1 <= sum(len(v) for v in scopes) <= 20:
        return False
    return 'change_from' not in payload or payload['change_from'] in ('24h', 'utc0', 'utc8')


def arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--product', choices=tuple(PRODUCTS), default='perpetual')
    parser.add_argument('--settle', choices=('btc', 'usdt', 'usd1'))
    parser.add_argument('--channel', required=True, choices=CHANNELS)
    parser.add_argument('--payload', required=True, help='Channel-specific JSON string array or documented object')
    parser.add_argument('--seconds', type=float, default=12, help='Total budget, including connection/retry (1–60)')
    parser.add_argument('--max-messages', type=int, default=10, help='Maximum raw business samples (1–100)')
    args = parser.parse_args(argv)
    if args.channel not in PRODUCTS[args.product][1]:
        parser.error('channel is not public/supported for the selected product')
    if args.product in ('perpetual', 'delivery'):
        if not args.settle or args.product == 'delivery' and args.settle != 'usdt':
            parser.error('perpetual requires btc/usdt/usd1 settlement; delivery supports only usdt')
    elif args.settle:
        parser.error('--settle does not apply to this product')
    try:
        args.payload = json.loads(args.payload)
    except ValueError:
        parser.error('--payload must be valid channel-specific JSON')
    if not valid_payload(args.channel, args.payload) or len(json.dumps(args.payload).encode()) > 8192:
        parser.error('invalid channel payload; use documented object keys or 1–20 short strings, each <=128 characters')
    if args.product == 'delivery' and args.channel == 'futures.obu' and not all(
            re.fullmatch(r'ob\.[A-Za-z0-9_]+\.(20|100)', item) for item in args.payload):
        parser.error('delivery OBU requires ob.<contract>.20 or ob.<contract>.100')
    if not math.isfinite(args.seconds) or not 1 <= args.seconds <= 60:
        parser.error('--seconds must be finite and between 1 and 60')
    if not 1 <= args.max_messages <= 100:
        parser.error('--max-messages must be between 1 and 100')
    args.endpoint = PRODUCTS[args.product][0].format(settle=args.settle)
    return args


def reject_constant(value):
    raise ValueError('Invalid JSON constant: ' + value)


def exact_json(value):
    """Keep server decimal numbers exact and numeric in emitted JSON."""
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError('Nonfinite JSON number')
        return str(value)
    if isinstance(value, dict):
        return '{' + ','.join(json.dumps(k, ensure_ascii=False) + ':' + exact_json(v)
                              for k, v in value.items()) + '}'
    if isinstance(value, list):
        return '[' + ','.join(exact_json(v) for v in value) + ']'
    return json.dumps(value, ensure_ascii=False, allow_nan=False)


def output(record):
    print(exact_json(record), flush=True)


class Reconnect(Exception):
    pass


async def observe(args, connect=None, emit=output):
    try:
        import websockets
        if int(websockets.__version__.split('.')[0]) < 15:
            raise ImportError('websockets>=15 required for explicit proxy control')
        from websockets.asyncio.client import connect as ws_connect
        from websockets.exceptions import ConnectionClosed, WebSocketException
    except ImportError:
        emit({'type': 'summary', 'status': 'error', 'error': 'Python websockets>=15 is required; no dependency was installed'})
        return 1
    connect = connect or ws_connect
    endpoint = args.endpoint
    start = time.monotonic()
    deadline = start + args.seconds
    connections, samples, error = [], 0, None
    emit({'type': 'start', 'product': args.product, 'environment': 'production', 'endpoint': endpoint, 'channel': args.channel,
          'payload': args.payload, 'budget_seconds': args.seconds,
          'order_book_rebuilt': False})
    try:
        async with asyncio.timeout(args.seconds):
            for attempt in range(2):
                state = {'connection': attempt + 1, 'ack': False, 'updates': 0, 'empty_updates': 0}
                connections.append(state)
                try:
                    async with connect(endpoint, additional_headers=({'X-Gate-Size-Decimal': '1'} if args.product in ('perpetual', 'delivery') else None),
                                       open_timeout=min(10, max(0.01, deadline - time.monotonic())),
                                       close_timeout=2, ping_interval=10, ping_timeout=10,
                                       max_size=1024 * 1024, max_queue=16, proxy=None) as ws:
                        await ws.send(json.dumps({'time': int(time.time()), 'channel': args.channel,
                                                  'event': 'subscribe', 'payload': args.payload}))
                        while True:
                            message = json.loads(await ws.recv(), parse_float=Decimal, parse_constant=reject_constant)
                            if not isinstance(message, dict):
                                raise ValueError('Expected a JSON object')
                            channel, event = message.get('channel'), message.get('event')
                            # Recognize the production Stock alias only on its own endpoint.
                            if args.product == 'stocks' and args.channel == 'stock.tickers' and channel == 'tspot.tickers':
                                channel = 'stock.tickers'
                            result = message.get('result')
                            if channel == 'futures.system' and event == 'update' and isinstance(result, dict) and result.get('type') == 'upgrade':
                                raise Reconnect('server upgrade')
                            if channel not in (None, args.channel):
                                continue
                            if message.get('error') is not None:
                                raise ValueError('Subscription/server error: ' + exact_json(message['error']))
                            if channel != args.channel:
                                continue
                            if event == 'subscribe':
                                if not isinstance(result, dict) or result.get('status') != 'success':
                                    raise ValueError('Subscription was not confirmed successful')
                                state['ack'] = True
                                emit({'type': 'ack', 'connection': attempt + 1, 'message': message})
                            elif event in ('update', 'all'):
                                if not isinstance(result, (dict, list)):
                                    raise ValueError('Business result must be a JSON object or array')
                                if not result:
                                    state['empty_updates'] += 1
                                    continue
                                state['updates'] += 1
                                if samples < args.max_messages:
                                    emit({'type': 'message', 'connection': attempt + 1,
                                          'received_at': time.time(), 'message': message})
                                    samples += 1
                except (OSError, ConnectionClosed, Reconnect) as exc:
                    state['disconnect'] = str(exc)
                    emit({'type': 'disconnect', 'connection': attempt + 1, 'reason': str(exc)})
                    if attempt == 1:
                        raise ValueError('Reconnect budget exhausted: ' + str(exc)) from exc
    except TimeoutError:
        pass
    except (ValueError, DecimalException, RecursionError, OSError, WebSocketException) as exc:
        error = str(exc)
    except asyncio.CancelledError:
        error = 'interrupted'
    # The last connection must establish its own evidence; an old ACK cannot confirm it.
    last = connections[-1] if connections else {'ack': False, 'updates': 0}
    status = ('data' if last['updates'] else 'ack_only') if last['ack'] else (
        'data_without_ack' if last['updates'] else 'no_confirmation')
    if error:
        status = 'error'
    emit({'type': 'summary', 'product': args.product, 'environment': 'production', 'status': status, 'error': error,
          'endpoint': endpoint, 'channel': args.channel, 'payload': args.payload,
          'elapsed_seconds': round(time.monotonic() - start, 3),
          'updates': sum(c['updates'] for c in connections),
          'empty_updates': sum(c['empty_updates'] for c in connections),
          'samples': samples, 'connections': connections, 'order_book_rebuilt': False})
    return 0 if status in ('data', 'ack_only') else 1


if __name__ == '__main__':
    try:
        raise SystemExit(asyncio.run(observe(arguments())))
    except KeyboardInterrupt:
        raise SystemExit(130)
