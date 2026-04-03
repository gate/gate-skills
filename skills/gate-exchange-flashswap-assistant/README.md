# Gate Exchange Flash Swap Assistant (L2)

## Overview

An L2 skill focused on **short-path flash swap execution** on Gate: one-to-one, one-to-many, and many-to-one **instant convert** using `cex_fc_*` preview and create tools, **spot available balance** checks via `cex_spot_get_spot_accounts`, **min/max** enforcement from `cex_fc_list_fc_currency_pairs`, optional **wallet dust → GT** via `cex_wallet_*` small-balance tools, **order history** queries, and **split-over-max** batching. `SKILL.md` embeds **all 21 atomic tool-call chains** from the L2 HTML spec (parallel **P1** vs serial **→**, confirm-before-write). It does **not** replace spot order trading, deep market research, full asset audits, or account transfers.

### Core Capabilities

| Capability | Description |
|------------|-------------|
| Flash swap modes | 1:1, 1:N, N:1 with preview → Action Draft → explicit Y/N → create |
| Balance gate | Spot available read for sell-side (and USDT for 1:N) only |
| Min / max | Skip fc preview when below `sell_min_amount`; plan S6 batches when above `sell_max_amount` |
| Dust vs flash | Clear user messaging: dust convert yields **GT**, not USDT flash |
| Queries | Pair limits, order list, single order detail, optional dust history |
| Routing | Defer pure spot “buy/sell”, research, and transfers to other skills |

## Architecture

```
gate-exchange-flashswap-assistant/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── references/
    └── scenarios.md
```

## Usage Examples

```
"Flash swap 1 BTC to USDT and show the quote."
"Convert all my BTC, ETH, and DOGE to USDT via flash swap."
"Split 3000 USDT flash into BTC, ETH, and SOL with 1000 each."
"Is my PEPE balance too small for flash swap? What is the minimum?"
"Clear my wallet dust to GT after listing what is convertible."
"Did my last flash swap succeed?"
```

## Trigger Phrases

- flash swap, flash convert, instant convert, consolidate to USDT
- swap X to Y (when meaning instant convert, not limit orders)
- dust to GT, small balance convert
- flash swap history, flash minimum

## Support

- **Repository**: [bitbucket.org/gateio/gate-github-skills](https://bitbucket.org/gateio/gate-github-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
- **MCP**: Requires Gate Exchange MCP with API key; use only tools listed in `SKILL.md`.
