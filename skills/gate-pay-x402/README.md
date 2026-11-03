# Gate Pay protected HTTP payment skill

`gate-pay-x402` guides agents through paid HTTP resources using the local stdio package
`gatepay-local-mcp`.

It is the agent-side orchestration and safety layer for a protected HTTP request: probe the
resource, identify x402 or MPP, show the price, obtain payment consent, use the selected local
payment method, retry the resource, and report whether access was actually obtained. It is not a
merchant service, wallet, or general Gate Exchange trading skill.

## Scope

- Probe merchant requests with `x402_place_order`.
- Complete wallet-signed x402 flows.
- Complete Gate Pay centralized flows through the local MCP OAuth/helper tools.
- Run Base + USDC MPP sessions, including normal HTTP settlement and optional on-chain teardown.
- Configure Quick Wallet, plugin wallet, or local private-key signing without exposing secrets in
  chat.
- Use an optional, separate discovery MCP to find payable resources when the user has no URL.

## Gate Exchange boundary

Use this skill when the task starts from a protected resource URL or requires x402/MPP protocol
handling and merchant-resource retry through `gatepay-local-mcp`.

Route to `gate-exchange-pay` when the user explicitly chooses Gate Exchange/Gate account balance,
an upstream checkout already has the structured inputs for `cex_pay_create_ai_order_pay`, and the
task is the direct charge/receipt rather than protected-URL negotiation.

Do not switch between local and Exchange payment tool families silently for one charge.

## Runtime

The current package exposes MCP tools only; there is no business CLI. Tool names, required fields,
enums, and argument types come from each live MCP `inputSchema`. The skill documents the 12 tools
exposed by the current public registry.

## Install

Prerequisites: a Skill-capable host, Node.js, and `npx`.

Install this Skill from the public repository:

```bash
npx skills add https://github.com/gate/gate-skills --skill gate-pay-x402
```

Register the required local payment MCP in the host's MCP configuration:

```json
{
  "command": "npx",
  "args": ["-y", "gatepay-local-mcp"],
  "env": {}
}
```

Optionally register the public merchant-discovery MCP when users need to find a payable service
without already having its URL:

```json
{
  "url": "https://openplatform.gateapi.io/pay-mcp-server/mcp",
  "transport": "streamable-http"
}
```

Keep the two servers separate. Configure payment credentials only on `gatepay-local-mcp`:

- Quick Wallet: no private-key environment variable; authenticate through the MCP tool.
- Plugin wallet: set `PLUGIN_WALLET_TOKEN` locally.
- Local private key for x402: the current implementation requires both `EVM_PRIVATE_KEY` and
  `SVM_PRIVATE_KEY` to mark the mode ready.
- Local private key for MPP/Base: `EVM_PRIVATE_KEY` is required; `SVM_PRIVATE_KEY` is not.

Never paste keys or full tokens into chat. Restart the host after changing MCP configuration, then
verify that `x402_place_order` is available. Discovery is ready when its live tool list exposes a
catalog tool such as `discoveryResource`.

## Use

Ask the agent in natural language. It will probe first and request confirmation after displaying
the payment details. Example prompts:

```text
Use Quick Wallet to access https://api.example.com/paid-report.
Configure my local-private-key wallet for x402 payments.
Find a payable weather API, show me the price, and ask before paying.
Use this MPP endpoint with a maximum deposit of 2 USDC.
```

For a direct structured charge from Gate account balance, use `gate-exchange-pay` instead.

## Files

```text
gate-pay-x402/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── references/
    └── scenarios.md
```

`SKILL.md` contains runtime routing and safety rules. `references/scenarios.md` contains regression
cases for x402, MPP, centralized payment, Gate Exchange routing, wallet setup, discovery, and
untrusted merchant content.
