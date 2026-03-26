# gate-news-listing — Scenarios & Prompt Examples

## Scenario 1: Recent new listings (English)

**Context**: User asks what new coins have been listed recently.

**Prompt Examples**:
- "Any new coins listed recently"
- "What did Binance list this week"
- "Recent new listings on Gate"

**Expected Behavior**:
1. Call `news_feed_get_exchange_announcements`(exchange optional, announcement_type=listing, limit=10). Extract top 3-5 newly listed coins.
2. For each selected coin, call in parallel `info_coin_get_coin_info` and `info_marketsnapshot_get_market_snapshot`(timeframe=1d, source=spot).
3. Output **Exchange Activity Report**: Latest Listing Announcements table, Featured New Coins (description, sector, funding, price, post-listing change, volume, market cap + one-liner), Delisting/Maintenance if any, Activity Summary. Include risk warnings (extreme volatility, liquidity, recommend risk check).

## Scenario 2: Specific exchange (Chinese)

**Context**: User asks about a specific exchange's new listings.

**Prompt Examples**:
- "What did Binance list"
- "What did Gate list recently"

**Expected Behavior**:
1. Extract exchange (e.g. Binance, Gate). Call `news_feed_get_exchange_announcements`(exchange=Binance, announcement_type=listing).
2. Supplement top new coins with coin_info and market_snapshot; output same 4-section report. Fuzzy-match exchange name if needed.

## Scenario 3: Delisting or maintenance

**Context**: User asks about delistings or maintenance.

**Prompt Examples**:
- "Any coins getting delisted"
- "Exchange maintenance announcements"

**Expected Behavior**:
1. Set announcement_type to delisting or maintenance. Call `news_feed_get_exchange_announcements` with that type. Do not supplement with market data for non-listing types.
2. Include Delisting/Maintenance Notices in report; prominently remind users to manage positions for delistings.

## Scenario 4: No announcements / tool failure

**Context**: No results or supplementary tool fails for a coin.

**Prompt Examples**:
- "New listings on XYZ exchange" (no data)

**Expected Behavior**:
1. If announcements return empty: inform "No relevant announcements for this time period" and suggest broadening time or exchange.
2. If coin_info or market_snapshot fails for a coin: skip detailed analysis for that coin; mark "Data unavailable"; still show announcement row.
