# Gate Exchange Options

## Overview

Skill for Gate options trading: place orders (market, limit, mark IV), close or reduce positions, cancel open orders, and amend open orders. All content is in English.

See `references/scenarios.md` for the scenario index and shared safety/confirmation rules.

### Core Capabilities

| Case | Description |
|------|-------------|
| **1** | Market or limit place order (buy/sell call/put; strike, expiration, size) |
| **2** | Mark IV place order (same as 1 with IV-based pricing) |
| **3** | Market or limit close/reduce position (full, half, by condition) |
| **4** | Cancel one or all open option orders |
| **5** | Amend open order (change price or size) |

## Architecture

- **Place order**: trigger phrases like "market buy 1 BTC call", "sell 1000U weekly BTC call at 70k", "open long 1 SOL weekly at market", "half of account to buy BTC 3-day call" → `references/place-order.md`.
- **Mark IV**: same plus "mark IV" / "IV order" → `references/place-order.md`.
- **Close/reduce**: "market close my BTC call", "close half of ETH put", "close when price hits 60000", "close all profitable/losing options" → `references/close-position.md`.
- **Cancel**: "cancel the BTC call order at 70k", "cancel all SOL call buy orders", "cancel all open orders" → `references/cancel-order.md`.
- **Amend**: "change my BTC call order price to XXXX", "halve the size of my SOL put/call order" → `references/amend-order.md`.

## Quick start

### Prerequisites

- Gate MCP configured and connected (options tools: `list_options_*`, `create_options_order`, `cancel_options_order`, etc.)
- Contract names follow `{underlying}-{expiration}-{strike}-{C|P}` (e.g. `BTC_USDT-20210916-50000-C`). The API accepts **size in contracts** only; when the user says base notional (e.g. "1 BTC call") or USDT (e.g. "1000U"), convert to contracts using multiplier or price_per_contract (see `references/place-order.md`). Size and price must respect `order_size_min` and `order_price_round` from the contract.

### Example prompts

- "Market buy 1 BTC call, strike at current price, expire in one week"
- "Mark IV order: buy 1 BTC call, one week expiry"
- "Market close my BTC call, expiry 03/18, strike 70000"
- "Cancel all SOL call buy orders"
- "Change my BTC call order at 70k strike, expiry 03/18, price to 0.05"
