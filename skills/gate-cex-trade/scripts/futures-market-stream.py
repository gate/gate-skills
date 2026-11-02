#!/usr/bin/env python3
"""Compatibility entry for existing perpetual subscriptions."""
import asyncio
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('public_market_stream', Path(__file__).with_name('public-market-stream.py'))
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)
arguments, observe = core.arguments, core.observe

if __name__ == '__main__':
    try:
        raise SystemExit(asyncio.run(observe(arguments())))
    except KeyboardInterrupt:
        raise SystemExit(130)
