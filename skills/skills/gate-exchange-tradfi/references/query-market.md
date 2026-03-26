# Query TradFi Market Data — Workflow and Scenarios

Read-only: query category list, symbol list, ticker, and symbol kline. All tools use `cex_tradfi_*` prefix. **Pass only parameters documented in the MCP for each tool.** No trading.

## Workflow

### Step 1: Identify query type

- **Category list**: User wants TradFi product categories (e.g. "TradFi categories", "category list").
- **Symbol list**: User wants the list of tradeable symbols (e.g. "symbol list", "list symbols", optionally by category).
- **Ticker(s)**: User wants price/volume for one or more symbols (e.g. "ticker for X", "price of symbol Y").
- **Symbol kline**: User wants OHLCV for a symbol over an interval (e.g. "kline for symbol X", "1d chart for Y").

### Step 2: Call tools

- **Category list**: Call `cex_tradfi_query_categories` with only MCP-documented parameters. Extract: category id, name, or fields as returned.
- **Symbol list**: Call `cex_tradfi_query_symbols` with only MCP-documented parameters (e.g. category only if the MCP defines it). Extract: symbol and other fields as returned.
- **Ticker(s)**: Call `cex_tradfi_query_symbol_ticker` with only MCP-documented parameters (e.g. symbol(s) if defined). Extract: last, 24h change, volume, etc.
- **Symbol kline**: Call `cex_tradfi_query_symbol_kline` with only MCP-documented parameters (e.g. symbol, interval, limit only if defined). Extract: timestamp, open, high, low, close, volume.

### Step 3: Format response

Use the Report Template below. If no data, report "No categories" / "No symbols" / "Symbol not found" / "No kline data" as applicable.

## Report Template

**Category list**

| Category ID / Name | Description (if any) |
|-------------------|----------------------|
| ...               | ...                  |

**Symbol list**

| Symbol   | Category | Status   |
|----------|----------|----------|
| ...      | ...      | tradeable / ... |

**Ticker(s)**

| Symbol   | Last   | 24h Change | 24h High | 24h Low | 24h Volume |
|----------|--------|------------|----------|---------|------------|
| ...      | ...    | ...%       | ...      | ...     | ...        |

**Symbol kline (summary)**

- Symbol: {symbol}
- Interval: {interval}
- From – To: {time range}
- Latest: O {open} H {high} L {low} C {close} V {volume}

(Full series can be shown as table or last N candles.)

---

## Scenario 1: Query category list

**Context**: User wants to see TradFi product category list.

**Prompt Examples**:
- "TradFi category list"
- "Query TradFi categories"
- "What categories are there"
- "List TradFi categories"

**Expected Behavior**:
1. Call `cex_tradfi_query_categories`.
2. Format as category table (id, name, or as returned).
3. If empty, reply "No categories returned."

---

## Scenario 2: List symbols

**Context**: User wants to see the list of tradeable symbols (optionally for a category).

**Prompt Examples**:
- "TradFi symbol list"
- "List symbols"
- "Symbols for category X"
- "What symbols can I trade"

**Expected Behavior**:
1. Call `cex_tradfi_query_symbols` with only the parameters documented in the MCP (e.g. category only if the MCP defines that parameter).
2. Format as symbol table (symbol, category, status).
3. If empty, reply "No symbols returned."

---

## Scenario 3: Get ticker for one or more symbols

**Context**: User wants current price and 24h stats for a symbol or symbols.

**Prompt Examples**:
- "Ticker for XAUUSD"
- "TradFi price for XAUUSD"
- "Ticker for symbol X and Y"

**Expected Behavior**:
1. Extract symbol(s) from user message; if unclear, ask which symbol(s).
2. Call `cex_tradfi_query_symbol_ticker` with the symbol(s).
3. Format as ticker table.
4. If symbol not found, reply "Symbol not found" and suggest listing symbols.

---

## Scenario 4: Get symbol kline / candlestick data

**Context**: User wants OHLCV data for a symbol (chart or analysis).

**Prompt Examples**:
- "Kline for XAUUSD 1d"
- "Candlestick 5m for symbol X"
- "Last 30 days 1d kline for XAUUSD"

**Expected Behavior**:
1. Call `cex_tradfi_query_symbol_kline` with only the parameters documented in the MCP (e.g. symbol, interval, limit only if defined).
3. Show kline summary and optionally last N candles in a table.
4. If no data, reply "No kline data for this symbol/interval."
