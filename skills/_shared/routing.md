# Shared Cross-Skill Routing

> Every primary skill in `gate-cli-skills` consults this table during Step 1 (intent routing). Delegate to the target skill instead of answering when the user's intent matches a row.

## Primary skills (target state = 4)

| Skill id | Purpose | Shipped |
|---|---|---|
| `gate-info-research` | Research / analysis (single coin, market, multi-coin, trend, macro, research + news) | yes |
| `gate-info-risk` | Token / address / project-level risk assessment | yes |
| `gate-info-web3` | Web3 / on-chain / protocol behavior (whale, smart money, entity profiling, TVL, bridges, reserves, heatmaps; DeFi is one subdomain) | yes |
| `gate-news-intel` | News / events / exchange announcements / UGC / X / Reddit / YouTube / social sentiment | yes |

## Routing table (decision signals first)

| User signal examples | Route to |
|---|---|
| "analyze SOL", "how is BTC", "is ETH worth watching", "compare BTC and ETH", "BTC RSI", "impact of NFP on BTC" | `gate-info-research` |
| "is this token safe", "honeypot?", "is the contract safe", "is this address safe", "will it be blacklisted", "project compliance risk" | `gate-info-risk` |
| "trace this address", "who is this address", "smart money", "whale", "TVL of Uniswap", "exchange reserves", "liquidation heatmap" | `gate-info-web3` |
| "why did it crash", "what happened recently", "social sentiment", "what does Reddit think", "YouTube", "community view", "X/Twitter narrative", "new listings", "exchange announcements" | `gate-news-intel` |

## Per-skill cross-delegation rules (within the shipped four)

### Inside `gate-info-research`, delegate to `gate-info-risk` when the user asks:

- Is `{coin|contract|address}` safe?
- Does `{token}` have a honeypot / tax?
- How is the compliance for this address / project?

### Inside `gate-info-research`, delegate to `gate-info-web3` when the user asks:

- Trace / explain a **wallet address** or **on-chain behavior** (not a coin research report).
- Smart money, whale flows, protocol TVL, reserves, liquidation heatmap as the **main** ask.

### Inside `gate-info-research`, delegate to `gate-news-intel` when the user asks:

- Why did `{coin}` crash / dump **as a news–event question** (not macro TA research).
- Latest headlines, community sentiment, Reddit / YouTube / X narrative as the **main** ask.

### Inside `gate-info-risk`, delegate to `gate-info-research` when the user asks:

- Give me a general analysis of `{coin}`.
- What's `{coin}`'s fundamentals / technicals without any risk framing?
- Is this coin worth watching?

### Inside `gate-info-risk`, delegate to `gate-info-web3` when the user asks:

- Who is this address / what did it do on-chain **without** a safety-first verdict framing.

### Inside `gate-info-risk`, delegate to `gate-news-intel` when the user asks:

- Why did it drop / **community narrative** on the incident (not a risk verdict).

### Inside `gate-info-web3`, delegate to `gate-info-risk` when the user asks:

- Safety, honeypot, blacklist, sanctions, "will it be blacklisted" as the **primary** goal.

### Inside `gate-info-web3`, delegate to `gate-info-research` when the user asks:

- Broad investment-style research, macro, or multi-coin comparison **without** on-chain/protocol as the focus.

### Inside `gate-info-web3`, delegate to `gate-news-intel` when the user asks:

- Pure **event / sentiment / media** questions with **no** on-chain/protocol framing.

### Inside `gate-news-intel`, delegate to `gate-info-research` when the user asks:

- Full **research report** (fundamentals, TA, macro, multi-coin compare) **without** news/community as the focus.

### Inside `gate-news-intel`, delegate to `gate-info-web3` when the user asks:

- Address tracing, on-chain flows, protocol / DeFi metrics as the **primary** ask.

### Inside `gate-news-intel`, delegate to `gate-info-risk` when the user asks:

- Is it safe / honeypot / blacklist **as the primary** question.

## Anti-pattern

Do NOT "merge" the other skill's scope into the current report by quietly calling commands from its playbook. Delegation is an explicit handoff, not a silent fan-out.
