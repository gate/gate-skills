# gate-exchange-newcoin: gate-cli execution contract

> Authoritative command and gate reference for **`gate-exchange-newcoin`**. Pair with `SKILL.md` for routing; this file covers invocation order, auth, JSON preference, parallelism, and write barriers.

## 1. Binary and help discipline

- Resolve `gate-cli` per `references/gate-runtime-rules.md` (PATH, `~/.local/bin`, `~/.openclaw/skills/bin`).
- For any subcommand you have not used in-session, run `gate-cli <path> --help` before real execution to confirm required flags.
- When the CLI supports it, add **`--format json`** for machine parsing of stdout.

## 2. Deduplicated command inventory (12 leaves: 10 read + 2 write)

### 2.1 `gate-cli info` (read)

| Command | Role |
|---------|------|
| `gate-cli info coin get-coin-info` | Fundamentals / tokenomics / project facts |
| `gate-cli info compliance check-token-security` | Token security screening |
| `gate-cli info onchain get-address-info` | Address-level context when user gives **explicit** address + chain |

### 2.2 `gate-cli news` (read)

| Command | Role |
|---------|------|
| `gate-cli news feed get-exchange-announcements` | Listing / maintenance / launch-related announcements |
| `gate-cli news events get-latest-events` | Recent event feed for a coin |
| `gate-cli news feed search-news` | Keyword news search |
| `gate-cli news feed get-social-sentiment` | Social sentiment snapshot |

### 2.3 `gate-cli cex` (read + write)

| Command | Role |
|---------|------|
| `gate-cli cex launch projects` | Launch / LaunchPool style project enumeration |
| `gate-cli cex spot market ticker` | Spot ticker / tape snapshot |
| `gate-cli cex spot market orderbook` | Depth / microstructure |
| `gate-cli cex spot order buy` / `gate-cli cex spot order sell` | **Write:** spot orders |
| `gate-cli cex alpha order place` | **Write:** Alpha orders (prefer `gate-cli cex alpha order quote` upstream when building Alpha workflows) |

**Note:** Extended liquidity analytics may combine orderbook/ticker/trades or Info platform metrics in other skills; this L2 stays on the **12-leaf** minimal loop unless the user explicitly needs deeper market-structure analysis (`gate-exchange-marketanalysis`).

## 3. Authentication tiers

| Tier | Auth |
|------|------|
| `info` / `news` reads | Typically public; follow upstream README if behavior changes |
| `cex launch`, `cex spot market …` | Often public for market data; verify with `--help` |
| `cex spot order …`, `cex alpha order …` | **Requires** API credentials via `gate-cli` profile or **`GATE_API_KEY`** + **`GATE_API_SECRET`** |

Never ask users to paste API secrets into chat.

## 4. Parallel vs serial phases

**Parallel (same phase)**

- Independent reads: for example announcements + launch projects in one wave.
- Per-symbol fan-out after symbol list is known: run compliance + coin info + sentiment **per symbol** in parallel batches if the host allows.

**Serial**

- Announcement scraping **then** symbol extraction **then** per-symbol calls.
- **Writes always follow** completed read synthesis + Action Draft + **Y**.

**Never** issue writes in the same parallel batch as unrelated exploratory reads.

## 5. Action Draft (mandatory before writes)

Every **`gate-cli cex spot order`** or **`gate-cli cex alpha order place`** requires:

1. Draft showing **pair**, **side**, **order type**, **amount semantics**, **estimated** cost/proceeds, **fees**, **liquidity/slippage** caution, **new asset** risk note.
2. Wait for **`Y`** / **`N`**.
3. Execute only on **`Y`** for **that** draft.

## 6. Degradation matrix

| Failure | Behavior |
|---------|----------|
| `get-exchange-announcements` fails | Omit listing slice; label unavailable |
| Compliance empty | Continue; warn in Draft |
| Order RPC error | Surface message once; **no** automatic retry loop |
| Other read flake | Omit that dimension; avoid guessing |

## 7. External rules

Follow repository-wide guidance in **`gate-runtime-rules.md`** bundled beside this skill and the shared norms referenced from Gate skills documentation.
