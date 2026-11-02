# Architecture and Coverage Profiles

Baseline: the Gate CEX consolidation plan approved on 2026-10-25, updated on 2026-10-27 to include Alpha in trade and retire six agent-channel modules. Public execution uses the official Gate CLI; engineering evidence revisions do not prescribe an installed release. This file bundles the contract needed to audit one package independently. It is not a declaration that all listed capabilities exist in every CLI release.

## Shared architecture

The six business names below are distinct from this audit utility. Review only the selected business profile; do not fail it because another business skill or the auditor is not installed beside it.

- The folder name and frontmatter `name` match. `SKILL.md` handles intent, routing, common lifecycle, and boundaries.
- Product action contracts live in `references/*-commands.md`. Workflows compose actions without duplicating parameter definitions. Shared display templates define presentation, not a fictitious universal CLI response.
- Source mode uses one canonical `skills/_shared/cex/` with `preflight.md`, `cli-setup.md`, `cli-auth.md`, `execution-cli.md`, `safety.md`, and `templates.md`. Inspect those explicit dependencies within the approved source workspace.
- Package mode contains these dependencies under its own `references/_shared/cex/`; no sibling skill, personal absolute path, escaping symlink, remote instruction download, or missing source checkout is needed. Shared files link internally within their packaged directory.
- Expected source links from an entry are `../_shared/cex/...`; from product references they are `../../_shared/cex/...`. Packaged entry links become `references/_shared/cex/...`; product links become `_shared/cex/...`.
- A local `references/execution-cli.md` may be a short pointer if it resolves to the canonical contract. Independently maintained copies of installation, auth, or execution policy are a drift finding. An engineering inventory is not a substitute for product references.
- Private reads and every write use registered `gate-cli cex` commands. No MCP fallback, `info/news` execution dependency, private HTTP/SDK client, dynamic remote instruction loading, or ad hoc signer. A verified installer download is distinct from a business transport exception.
- Trade alone has an approved bounded public-market exception: fixed GET paths for futures contract statistics, futures/delivery insurance, and stock symbol metadata/orderbook; plus the bundled public WS helper. The selected API base, fixed routes, validated instruments/settlement, no credentials/cookies, no redirects, deadlines and output limits remain mandatory. Public fallback is not permission to choose an arbitrary origin/path, bypass a private CLI action, change the environment or reconstruct a verified book from raw updates. Audit the exact exception against `markets.md` and `streams.md`; do not reject it using a blanket CLI-only rule. Other profiles acquire no exception.

## gate-cex-trade

Expected product references:

`spot-commands.md`, `alpha-commands.md`, `perpetual-commands.md`, `delivery-commands.md`, `margin-commands.md`, `options-commands.md`, `stocks-commands.md`, `cfd-commands.md`, `algo-commands.md`, `convert-commands.md`, `market-commands.md`, `unified-commands.md`, `vip-fees-commands.md`.

Expected workflow: `order-workflows.md` for order changes, cancellation, protections, and position management under each applicable product contract.

Check spot market/limit orders and spending units; perpetual versus delivery, settlement and position mode; margin borrow/repay and liquidation exposure; options order/protection behavior; stock shares versus tokenized products versus CFD volume; convert quote validity; current market data, unified-account trading settings, and fees. Algorithm support requires its own independent CLI evidence; the file must not invent OCO/TWAP/VP or stream commands.

Check all nine Alpha actions: three market reads, two account reads, quote, place, get and list. Buy amount spends USDT; sell amount is base-token quantity. Check percentage slippage, custom-mode requirements, one-minute quote validity, quote/place context binding, statuses 5/6, and ambiguous-write reconciliation. Quote is a private calculation, not a trade submission. This build has no Alpha amend/cancel command.

Required algorithm coverage includes spot POV create/list/get/cancel/cancel-all and
futures chase create/list/get/stop/stop-all. Verify spot account and borrowing
selection, attached protection tri-state semantics, options full/partial close,
unified Delta-neutral/quick repayment/all-currency leverage, public RPI/ADL/all
contracts and authenticated CFD commission/log reads. See [CLI verification](cli-verification.md)
for variant checks. None of these adds a second canonical write owner.

CLI discovery seeds: `cex spot`, `alpha`, `futures`, `delivery`, `margin`, `options`, `stock`, `tradfi`, `flash-swap`, `unified`, plus relevant account/fee reads. Seeds locate evidence; they do not assign every command in a group to trading. Product-account fund transfers belong to assets, not this profile.

## gate-cex-earn

Expected references: `simple-earn-commands.md`, `staking-commands.md`, `dual-investment-commands.md`, `auto-invest-commands.md`, `collateral-loan-commands.md`.

Expected multi-step workflow: `earn-workflows.md` when subscription/redemption, rollover, loan management, or participation tasks are advertised.

Check product discovery, eligibility and terms, subscription/position reads, maturity/rollover choices, redemption/repayment, history, and verification where the CLI supports them. Explain variable returns, lockups, collateral/liquidation exposure, and partial completion. Binance-branded assets or mechanisms are not proof of corresponding Gate products.

CLI seeds: `cex earn` subgroups `uni`, `fixed`, `staking`, `dual`, and `auto-invest`; `cex mcl` for collateral loans. The approved scope contains these five products. Launchpool and CandyDrop are outside this profile: do not require their files, restore retired activity-center commands, or fabricate participation workflows to satisfy coverage.

## gate-cex-assets

Expected references: `balances-commands.md`, `transfers-commands.md`, `deposits-commands.md`, `withdrawals-commands.md`, `small-balance-commands.md`.

Expected workflow: `asset-workflows.md` for advertised transfers or withdrawals.

Check account/asset balances, networks and deposit addresses/history, internal/product/subaccount transfers, transfer status, withdrawal constraints/destination/tag/fees/history, and small-balance conversion. Distinguish deposits from fund transfers and submitted withdrawals from settlement. Do not silently consolidate funds or turn an asset query into trading.

CLI seeds: `cex wallet`, `cex withdrawal`, and independently identified product-account transfer operations such as stock/CFD fund movements. Fee reads may be reused as trading prerequisites; ownership follows the business action, not the command's folder alone.

## gate-cex-subaccount

Expected references: `accounts-commands.md`, `api-keys-commands.md`, `permissions-commands.md`.

Expected workflow: `subaccount-workflows.md` for advertised provisioning, key lifecycle, or permission-change tasks.

Check listing/detail, creation/lock state, mode/eligibility, key lifecycle, permission and IP restrictions, and post-change verification when supported. Differentiate a documented API-key capability from authorization to use it. Agentic OAuth does not gain key/subaccount-management rights merely because the command exists.

CLI seed: `cex sub-account` and explicitly relevant account reads. Delegate fund transfer writes to assets. Secrets must stay in the approved local credential workflow, not audit logs or chat.

## gate-cex-affiliate

Expected references: `relationships-commands.md`, `commissions-commands.md`, `statistics-commands.md`.

`affiliate-workflows.md` is expected only when the advertised tasks compose multiple actions.

Check role/relationship queries, applicable partner/broker/agency commission and transaction records, bounded history/statistics, privacy, and the exact meaning of reported rates/earnings. Do not conflate referral campaigns, relationships, applications, and paid commissions or promise future income.

CLI seed: `cex rebate`; each role and mutating application action must be verified individually. Do not classify all commission-related endpoints as writes, or every query-looking command as harmless.

## gate-cex-bot

Expected references: `spot-grid-commands.md`, `futures-grid-commands.md`, `martingale-commands.md`, `bot-lifecycle-commands.md`, `smart-position-commands.md`, and `futures-combo-commands.md`.

Expected workflow: `bot-workflows.md` for creation, running-state management, and stopping.

Check discovery/recommendations, strategy-specific creation, running/detail queries, stop semantics and resulting positions/funds. Account for infinite/margin grid and contract martingale where the CLI exposes them; a generic grid paragraph is insufficient. Explain ongoing trading exposure and the duration/limits of user authority.

CLI seed: `cex bot`. One-shot algorithm execution belongs to trade. A successful stop response does not prove that residual exposure is zero.

## Completeness decisions

For every expected reference, record present/missing, routed/reachable, substantial content/placeholder, applicable actions, CLI evidence, and outcome. A renamed file requires a newer approved mapping; similarity alone does not resolve a missing canonical file.

For every expected capability, classify it as documented and verified, implemented but undocumented, incorrectly documented, explicitly unsupported with evidence, unresolved, or excluded by an approved boundary. Inspect both reads and writes, request fields, history, lifecycle completion, and failure recovery. Empty files, unlinked files, generic descriptions, or unsupported labels without evidence do not satisfy coverage.

An unsupported product can have a substantive boundary note instead of executable examples. It must not have an active route promising execution. A target cannot exempt an implemented required capability by declaring it unsupported without independent evidence. Missing implementation belongs in the capability-gap ledger; missing documentation belongs in the skill findings.

Read-only prerequisites may appear in several skills. Each business write action has one canonical owning product reference. A single-target audit may verify its declared ownership and handoff; it cannot certify global uniqueness across five unseen packages. State that limit without requiring their installation.

Alpha is assigned to trade; do not require or recreate a seventh business skill. P2P, CrossEx, welfare, activity-center, coupon-management and Exchange Announcement are retired from agent execution. Flag callable references, obsolete module-boundary anchors and older-build/channel workarounds. Keep only concise unavailable boundaries; legitimate earn coupon fields and independent News services are not retired product actions.

Asset-swap portfolio adjustment, KYC guidance, new-coin research and referral campaigns remain outside the six profiles. Pay remains independent and its existing skills are preserved, as are all DEX skills. Historical sources are evidence, not runtime dependencies.
