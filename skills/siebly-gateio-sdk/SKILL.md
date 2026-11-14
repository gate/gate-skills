---
name: siebly-gateio-sdk
description: "Build, inspect, or modify Node.js and TypeScript application code for the Gate REST APIs, WebSocket streams and WebSocket API using the open-source, MIT-licensed gateio-api npm package. Use when the user is writing their own JavaScript or TypeScript integration rather than using Gate MCP or the Gate CLI."
license: MIT
metadata:
  version: 1.0.0
  author: harbourlark
---

# Siebly Gate.com JavaScript SDK (gateio-api)

Use this skill when a user asks you to write, review or fix Node.js, JavaScript or TypeScript code that talks to the Gate.com (gate.io) API v4: REST market data, account and order endpoints, public or private WebSocket streams, or order commands over the WebSocket API.

This skill does not replace the official Gate skills or Gate MCP in this repository. If the user wants natural-language trading through Gate MCP, follow those skills. If they are writing their own application code, use the `gateio-api` package documented here.

The package is open source (MIT), free, and maintained by the Siebly team. This skill is educational. It never recommends trades, assets or strategies and must not be treated as financial advice.

## Install

```bash
npm install gateio-api
```

- npm: https://www.npmjs.com/package/gateio-api
- Source and examples: https://github.com/sieblyio/gateio-api
- SDK guide: https://siebly.io/sdk/gate/javascript
- Full tutorial: https://siebly.io/sdk/gate/javascript/tutorial
- Official Gate API v4 reference: https://www.gate.com/docs/developers/apiv4/

Always install the current published version. Check the installed typings for exact method names and request shapes before writing code. Do not invent methods or a custom signing implementation.

## Clients

| Class | Use for |
| --- | --- |
| `RestClient` | All Gate API v4 REST endpoints: spot, margin, unified account, perpetual and delivery futures, options, wallet, sub-accounts, earn |
| `WebsocketClient` | Public and private WebSocket streams, with heartbeats, reconnect and resubscribe handled |
| `WebsocketAPIClient` | Promise-based order commands over the Gate WebSocket API (spot and futures) |

## Workflow

1. Identify the product (spot, unified, USDT or BTC settled futures, delivery, options) and whether the task needs only public data or private access.
2. Start with a public REST call or a public stream. Add credentials only when the task needs private endpoints.
3. Load `apiKey` and `apiSecret` from environment variables, never from chat, source files or logs. Fail fast at startup if they are missing.
4. Use `useTestnet: true` (REST and WebSocket options) with testnet keys while developing order flows. Live and testnet keys are separate.
5. Grant API keys the minimum permissions needed. Order placement never needs withdrawal permission. Encourage IP whitelisting.
6. Handle errors explicitly. Gate returns labelled errors such as `INVALID_SIGNATURE`, `REQUEST_EXPIRED` and `INVALID_KEY`: check clock sync, the key's permissions and that the right environment (live or testnet) is used.
7. For streams, wait for the subscription response before relying on data, listen for `reconnected` to resync state, and close connections on shutdown.
8. Before any code that places, amends or cancels orders, confirm with the user and prefer testnet.

## Public REST example

```ts
import { RestClient } from 'gateio-api';

const client = new RestClient();

const tickers = await client.getSpotTicker({ currency_pair: 'BTC_USDT' });
console.log(tickers[0]);
```

## Private REST example (testnet)

```ts
import { RestClient } from 'gateio-api';

const client = new RestClient({
  apiKey: process.env.GATE_API_KEY!,
  apiSecret: process.env.GATE_API_SECRET!,
  useTestnet: true,
});

const balances = await client.getSpotAccounts({ currency: 'USDT' });
console.log(balances);

const order = await client.submitSpotOrder({
  currency_pair: 'BTC_USDT',
  side: 'buy',
  type: 'limit',
  price: '10000',
  amount: '0.001',
  time_in_force: 'gtc',
});
console.log(order.id, order.status);
```

## WebSocket streams

```ts
import { WebsocketClient } from 'gateio-api';

const ws = new WebsocketClient();

ws.on('update', (data) => console.log('update', data));
ws.on('response', (data) => console.log('response', data));
ws.on('reconnected', (data) => console.log('reconnected', data?.wsKey));
ws.on('exception', (err) => console.error('ws error', err));

// Topic plus payload, routed to the spot v4 connection
ws.subscribe({ topic: 'spot.tickers', payload: ['BTC_USDT'] }, 'spotV4');
```

Connection keys include `spotV4`, `perpFuturesUSDTV4`, `perpFuturesBTCV4`, `deliveryFuturesUSDTV4`, `deliveryFuturesBTCV4`, `optionsV4` and `announcementsV4`. Private topics (for example `spot.orders`, `spot.balances`) need `apiKey` and `apiSecret` on the client; the SDK signs the subscription.

## WebSocket API orders

```ts
import { WebsocketAPIClient } from 'gateio-api';

const wsApi = new WebsocketAPIClient({
  apiKey: process.env.GATE_API_KEY!,
  apiSecret: process.env.GATE_API_SECRET!,
  useTestnet: true,
});

const res = await wsApi.submitNewSpotOrder({
  currency_pair: 'BTC_USDT',
  side: 'buy',
  type: 'limit',
  price: '10000',
  amount: '0.001',
});
console.log(res);
```

Futures equivalents include `submitNewFuturesOrder`, `cancelFuturesOrder` and `getFuturesOrders`.

## Rules

- Never print, log or commit API secrets.
- Never place live orders without the user's explicit confirmation.
- Do not describe outputs as investment advice or suggest strategies.
- Point users to the SDK guide and tutorial for longer examples rather than pasting large blocks of unverified code.
