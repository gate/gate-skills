# Tools

Small CLI utilities used by the Gate DEX Trade skill flow (for example staged swap check-in). They are optional helpers around the same HTTP contracts the MCP server uses; you can also perform these steps from your own code.

| Tool | Purpose |
|------|---------|
| [tx-checkin](./tx-checkin/) | Turn `dex_tx_swap_checkin_preview` JSON into a signed HTTP check-in call and print the API response (production gateway). |

## Environment

This tree is paired with **`gate-dex-trade`** (production). The **prebuilt** check-in binaries in `tx-checkin/` call the **production** Web3 GV API host (URL is compiled into each executable).

For the test skill package and **test** API host, use the same tool under [`../../gate-dex-trade-test/tools/`](../../gate-dex-trade-test/tools/) (sibling package under `web3_wallet_skill/`).

## Artifacts

**tx-checkin** ships **prebuilt** platform binaries only (`swap-checkin-mac`, `swap-checkin-linux`, `swap-checkin-win.exe`); see [tx-checkin/README.md](./tx-checkin/README.md).
