# Query TradFi User Assets and MT5 Account — Workflow and Scenarios

Read-only: get user account/balance (assets) and MT5 account info. All tools use `cex_tradfi_*` prefix. **Pass only parameters documented in the MCP for each tool.** No transfers or trading.

## Workflow

### Step 1: Identify query type

- **User assets / balance**: User wants TradFi account balances (e.g. "my assets", "balance", "account").
- **MT5 account info**: User wants MT5 account details (e.g. "MT5 account", "my MT5 info", "MT5 login").

### Step 2: Call tools

- **User assets**: Call `cex_tradfi_query_user_assets` with only MCP-documented parameters. Extract: asset (or as returned by API), available, locked/total as returned.
- **MT5 account**: Call `cex_tradfi_query_mt5_account_info` with only MCP-documented parameters. Extract: account id, server, login, balance, equity, margin, or fields as returned.

### Step 3: Format response

Use the Report Template below. If the API returns empty or error, report "Unable to load assets" or "Unable to load MT5 account" and suggest checking connection or permissions.

## Report Template

**Assets / Balance**


| Asset   | Available | Locked | Total |
| ------- | --------- | ------ | ----- |
| ...     | ...       | ...    | ...   |


(If the API uses different field names, map them accordingly, e.g. "balance", "free", "used".)

**MT5 account**


| Field    | Value       |
| -------- | ----------- |
| Account  | ...         |
| Server   | ...         |
| Balance  | ...         |
| Equity   | ...         |
| Margin   | ...         |
| (others) | as returned |


---

## Scenario 1: Get account balance (user assets)

**Context**: User wants to see their TradFi account balance or assets.

**Prompt Examples**:

- "My TradFi assets"
- "Balance"
- "How much do I have"
- "Account balance"
- "My funds"

**Expected Behavior**:

1. Call `cex_tradfi_query_user_assets`.
2. Format as assets table (asset, available, locked, total).
3. If error or empty, reply "Unable to load assets" and do not retry indefinitely.
4. Do not expose API keys or secrets; only display balance data returned by the tool.

---

## Scenario 2: Get balance for a specific asset

**Context**: User asks for one asset only (e.g. USD).

**Prompt Examples**:

- "My TradFi balance"
- "How much USD do I have"

**Expected Behavior**:

1. Call `cex_tradfi_query_user_assets` with only MCP-documented parameters. If the response includes multiple assets, show the requested one or all as returned.
2. Show that asset’s available/locked/total.
3. If asset not found in response, reply "No balance for {asset}."

---

## Scenario 3: Get MT5 account info

**Context**: User wants to see their MT5 account information.

**Prompt Examples**:

- "MT5 account"
- "My MT5 info"
- "MT5 account details"
- "MT5 login"

**Expected Behavior**:

1. Call `cex_tradfi_query_mt5_account_info`.
2. Format as MT5 account table or key-value list (account, server, balance, equity, margin, etc.).
3. If error or empty, reply "Unable to load MT5 account" and suggest checking MT5 connection or permissions.
4. Do not expose passwords or sensitive credentials; only display info returned by the tool.

