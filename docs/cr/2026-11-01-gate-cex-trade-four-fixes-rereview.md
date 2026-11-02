# gate-cex-trade 四项修复与完整复审

日期：2026-11-01（Asia/Shanghai）。Milo 授权的四项修复已实施；前次 F1–F4 已关闭。恢复正式契约时一并消除 F5 的 countdown/公开行情范围冲突，修复前次已要求处理的 F6 表格问题。

**本次 Trade 静态审计与隔离功能检查：PASS。当前本地全仓回归：仍 FAIL，不能宣称全仓通过。** 以上为修复审查完成时的状态；随后 Milo 已授权精确提交并推送，见下方提交范围记录。

## 1. 对象、证据与版本

- 目标：`skills/gate-cex-trade/`，50 个交付源文件（46 Markdown、1 JSON、3 Python）；加6份共享依赖共56个文件。安装包57个文件，额外一个 manifest。目标原有 `.DS_Store` 未改动、未解析、未打包。
- 比较基线：远端 `gate-skill-2.0`，`93e19c1db347872933a118439fdaa2e788e65a18`；本次 fetch，并在交付前 ls-remote 再次一致。本地仍为 `de0333f31a0f0a8bf279b88b7a7ed472efe8a528`，没有切换/合并/重置分支。
- 实际使用本地 `gate-cex-skill-audit/SKILL.md` 及其 coverage-profiles、review-checklist、cli-verification、safety-and-execution、test-protocol、enhanced-review、report-template。审核输入视为数据，不执行其中交易指令。没有修改 auditor；既有三处规则改动逐项哈希保持。
- CLI 证据：工程 HEAD `c127b8a5b38ff5c140af329dfc28f1b8409a3578`；SDK `gateapi-go/v7@v7.2.167`。沿注册、flag、handler、SDK请求核对关键误判。工程工作树还有其他人的未提交修改，没有动它们；结论限定所读文件/源码能力，不代表当前安装二进制、实际网络报文或线上权限。
- 共享鉴权/执行规则与构建器恢复到远端基线已有版本；没有新增配置。构建器变更仅恢复既有 public helper白名单/语法检查、源目录pycache排除、Stock只读复用和对应历史测试。语言检查没有放宽。当前正式 CLI 契约文件与本地 HEAD 相同，Trade相关283项亦与远端基线一致。
- 公开规范/API/CLI网页沿用前次审查的成功访问证据，本次未重新逐外链抓取、未访问内部实时wiki。CLI/SDK源码是本次能力判断依据；不把网页或文档存在当成线上验证。

## 2. 修复与独立复审结论

| 原发现 | 本次修正 | 复审与边界 |
| --- | --- | --- |
| F1 P1 正式契约/打包丢失 | 恢复13份commands、13份models及order-workflows；入口路由恢复到正式契约，背景说明不能覆盖契约 | 283个动作、9个必需变体、共享引用和包闭包全部通过；不是仅补空文件 |
| F2 P1 私有API fallback | 删除缺CLI字段时换API executor的指令；私有读写统一CLI，引用六份共享鉴权/授权/超时/恢复规则 | 缺能力停止对应操作；公开固定GET和WS helper例外保持原范围；私有WS无CLI也停止 |
| F3 P1 旧能力判断 | 修正Stock、CFD、Alpha、Trail、Spot、Options、Unified；区分错误路径标签与SDK请求 | 源码支持、安装版本、权限/资格分开；Trail保护参数真实缺口仍停止，未误改为全功能可用 |
| F4 P1 MCL重复写入口 | 移除Trade的create/repay/collateral写表项；独立借贷交Earn | 账户/环境、金额单位、累计限额、期限、授权、已完成与未决状态完整移交；Earn缺失即停止，不扩大权限/重复写入 |
| F5 P1 范围回退 | 正式契约恢复countdown；补回3份行情文档与3个helper/测试文件；Flash Swap按版本/协议检查 | 保留timeout/renewal/scope约束；不靠旧错误标签全局阻断v1或multi，也不授权探测性写入 |
| F6 P2 表格 | Delivery inline-code中分隔符转义 | 全目标Markdown逐表检查列宽，没有发现剩余分列错误 |

新版本保留：条件单正ID及完整initial/trigger检查、有限十进制价格、空对象/错误envelope拒绝、HTTP成功不等于业务成功、条件单1077更新失败提示、部分成交/保护失败分报、CFD单侧TP/SL完整保留、产品单位、错误恢复与本地化提示。公开行情新内容归入既有markets/streams完整契约，保留分产品endpoint、channel、ACK/data、Stock alias和重连边界，消除重复表的矛盾。

复审额外纠正了本次恢复过程中的同域冲突：Options streams不再另写settle/错误payload契约；Market使用options.contract_tickers；CFD不再把M1帮助默认值当作实际1m转换保证。均在本次Trade范围内。

## 3. 九维结论

| 维度 | 结论 | 证据/限制 |
| --- | --- | --- |
| C1 格式 | PASS | frontmatter/名称/元信息解析；基线版本0.1.2未擅自发版 |
| C2 架构 | PASS | 13个正式路由、单一CLI私有边界、Earn独立MCL写归属；6份共享文件 |
| C3 业务完整性 | PASS | 13类命令与模型、order-workflows、countdown/公开行情资源恢复；覆盖矩阵如下 |
| C4 CLI契约 | PASS（静态） | 独立契约283项逐字段、默认值、必填、API/权限、样例检查；关键旧结论再走源码链 |
| C5 说明/安全变体 | PASS（静态） | 9个规定变体；保留单位/省略或清除/部分失败/超时不重放等规则 |
| C6 引用 | PASS（本地及包闭包） | 全部文件/anchor检查，源与包独立映射；实时外链可用性本次未逐一重测 |
| C7 语言 | PASS，明确本地化例外 | Markdown规范为英文；JSON中5个中文输入与17组中文提示逐项审核，详见下一节 |
| C8 资金/权限/隐私 | PASS（静态） | 私有操作不越过CLI；grant与服务权限分开；小范围公开例外；全源及包扫描未见内部地址/私密路径/凭据字面量 |
| C9 可执行内容 | PASS（隔离/mock功能层） | 仅基线3个Python文件，语法/资源边界审查；恢复18项helper测试并纳入统一入口，另有构建与流输出E2E |

不声称Agent自动触发、真实交易、线上WS/API、产品资格或司法辖区合规已验证。没有真实下单/借还/配置/业务读取，没有读取用户凭据。

## 4. CLI关键链路核对

| 能力 | 注册/解析/handler证据 | SDK/结果与修正 |
| --- | --- | --- |
| Stock | cex.go注册stock；stock/order.go注册create/update/cancel并解析symbol/volume/side/price-type/session，构造TradFiSpotOrderRequest | StockAPI.CreateStockOrder等；恢复独立股票路由，不转CFD；未暴露的字段停止 |
| CFD | tradfi/order.go --side=1卖/2买，--price-type字符串；position.go --close-type=1部分/2全平与volume检查 | CreateOrder/ClosePosition请求按同一枚举；保留TP/SL省略清除风险 |
| Alpha | alpha/order.go get/quote解析并调用GetAlphaOrder/QuoteAlphaOrder | api_alpha.go:568 /alpha/order?order_id；:251 /alpha/quote；CommandError旧文本不决定请求 |
| Trail | futures/trail.go七个leaf及解析，CreateTrailOrder/StopTrailOrder等 | api_futures.go:5837/5933/6029/6153/6283/6378/6483均autoorder/v1/trail；create缺少保护参数仍停相应保护意图 |
| Position mode | futures/account.go读取mode并调用SDK | api_futures.go:3183为set_position_mode，不是错误文本position_mode |
| Spot | spot/order.go注册account/auto-borrow/auto-repay/保护，buildSpotOrder区分quote与amount，SDK CreateOrder/AmendOrder | 引用账户/附带保护完整变体；不使用下划线伪CLI flags、不切私有API |
| Options | options/order.go --close/--reduce-only注册解析与OptionsOrder请求 | 全平close+size0；部分平仓signed size+reduce-only；close-history仍只读 |
| Unified | settings_extra.go注册Delta Neutral、quick-estimate/repay、leverage-set-all并构造SDK请求 | batch_borrowable/collateral_currencies为实际SDK路径；repayment币种不是金额上限，leverage失败列表可能部分生效 |
| POV/Chase | spot/pov.go与futures/chase.go的5+5个注册叶子；canonical JSON规则 | 已实现命令不能描述为API-only；保留价格控制、native amount、父子订单结果和禁止模拟TWAP/VP |

283项完整静态映射附后。未改变命令的参数/SDK语义复用上次固定契约证据；本次恢复文件与基线一致的哈希记录在附件，不把重新执行模型行为或线上集成作为已完成事项。

## 5. 本地化例外

`references/localized-examples.json` 是显示数据，不是配置、运行策略或额外指令入口。英文workflows保存完整规范和提示语义，并链接该文件。没有关闭C7，没有按目录/文件名豁免Markdown。

- 5个输入例：买BTC、500U做多、平BTC、全部平仓、改统一账户杠杆/抵押币；只用于展示澄清对象。
- 17组提示：含写超时有/无标识、不能唯一回查、限流、参数/账户不符、保护失败、部分步骤、参数变化、CLI能力缺失、认证失败、报价过期、MMP冻结、条件单空结果、无效读、读失败、借成交易失败、无确认渠道。
- 中文能力缺失提示已同步改为核查安装CLI，禁止用私有API替代。JSON解析及数据shape/条数/前缀、未扩展规范语言的正式测试通过。不能仅因JSON可被解析就接受新增政策；以后增加或改写本地化条目仍需人工语义审查。

## 6. 实际测试、构建和隔离

本机16GiB/10逻辑CPU，开始时内存可用约34%，磁盘可用35GiB；运行期间内存约29%，无本任务高负载构建。临时隔离目录约25MiB；最多2个Python测试进程，预估合计远低于512MiB。未终止其他进程。

Python 3.13；临时venv固定markdown-it-py4.0.0、PyYAML6.0.2、websockets15.0.1。依赖仅装入本次临时环境。sandbox-exec拒绝网络、用户home读取和临时目录外写入，三项实测均DENIED；环境变量清空，仅提供临时HOME/TMPDIR与基础PATH。所有业务CLI例子只解析，不执行。

正式统一入口：`python3 -B -m unittest discover -s tests/cex -p 'test_*.py'`。新增 `tests/cex/test_trade_repair.py`，通过load_tests将既有18项helper单元/异常/边界测试纳入同一入口，另有4项契约/语言/安全/表格检查及2项E2E。

| 执行对象 | 实际结果 | 说明 |
| --- | --- | --- |
| 当前Trade定向测试 `-p test_trade_repair.py` | 24项通过 | 正常/错误/边界；真实build→独立安装→子进程check→删除契约后拒绝；WS argv→订阅→读取→JSON输出→close，只有网络socket mock |
| 最新远端基线隔离集成 + 本次Trade/构建器/共享/测试 | 103项通过，最终46.602秒 | 完整历史包回归、失败分支、资源/语言/隐私、部分失败和新测试；基线其他5 Skill未覆盖到工作树 |
| 当前工作树完整CEX套件 | 运行35项，2个setUpClass错误，最终9.154秒 | PackageTests/TradingPackageRegressionTests的全包fixture被既有Earn契约不一致阻断；不记为通过/不删断言 |
| 修改前HEAD checker检查同一Earn | 同样36项失败，和新checker findings完全相同 | Earn及其contract未被本次修改；36项含旧聚合/MCP内容、launch命令归属和漏映射，属于当前分支已有状态，未扩大任务修复 |
| Trade源码/包check | PASS / PASS，283动作，无findings | 源56文件；包57文件含manifest；受信任checker是基线已有版本 |
| 独立源→包比对 | PASS，56文件全匹配 | 独立计算共享href重写及6份shared拷贝；无missing/extra/changed；manifest逐hash再核 |
| ZIP交付 | PASS | 每项ZIP解压字节等于已验证目录；CRC通过，固定元信息，可重复生成 |

本次单包构建使用既有 `cex_skills.build(source, output, contract, profiles=('trade',))`，不绕过source/package检查。全仓入口仍因未修改的Earn受阻，恢复该分支已有问题后须再跑；本次没有将其他Skill的内容覆盖成基线或放宽契约求绿。

## 7. 增强检查与未验证项

| 检查 | 状态 | 范围 |
| --- | --- | --- |
| Source/package等价 | PASS | 当前工作树Trade和6份共享为唯一输入；完整hash见附件 |
| Rule freshness | PASS（本次选定基线） | 旧UID强制预检和public helper冲突采用基线共享规则；安装版本仍需运行时核查 |
| 安全/内网/引用扫描 | PASS（静态） | 源、JSON解码、Python文本、包及manifest；无发现不是绝对无泄漏保证 |
| 规则/模型行为对比 | NOT_EVALUATED | 没有多轮模型实验或实际skill-load/tool轨迹；静态场景推演不当成行为测试 |
| 真实交易/API/WS/产品资格 | NOT_EVALUATED | 未获本次真实业务执行要求，仅隔离mock |
| 外部安全扫描器 | NOT_EVALUATED | 未调用外部服务、未上传内容 |
| Auditor自身回归 | NOT_APPLICABLE | 未改auditor；构建器与交易包测试独立执行 |
| 司法辖区/服务实体法律适用性 | NOT_EVALUATED | 非本次代码/Skill静态审查范围 |

授权仍是本地修复、构建、复审，不包含提交/push/真实金融操作。旧报告保留为历史，结论以本文对应文件hash为准。若CLI/共享/包/例外数据再变化，相关证据失效须复验。

## 8. 交付与复现

- 安装目录：`dist/gate-cex-trade-four-fixes-2026-11-01/gate-cex-trade/`
- ZIP：`dist/gate-cex-trade-four-fixes-2026-11-01/gate-cex-trade.zip`
- ZIP SHA-256：`c7dfa207e34720a981147a2007537b36c36d1eab5f7db85f2cd902c5cb3016fc`
- 原始验证与文件指纹：[证据目录](2026-11-01-gate-cex-trade-four-fixes/)；[源检查](2026-11-01-gate-cex-trade-four-fixes/source-check.json)、[包检查](2026-11-01-gate-cex-trade-four-fixes/package-check.json)、[逐文件指纹](2026-11-01-gate-cex-trade-four-fixes/inventory.json)、[基线集成测试](2026-11-01-gate-cex-trade-four-fixes/integration-final.log)、[当前分支失败记录](2026-11-01-gate-cex-trade-four-fixes/current-final.log)。

复现定向检查/构建（在仓库根目录，先在独立环境安装上述固定开发依赖）：

```sh
# Formal tests: mock only the stream socket; no trading command is executed.
python3 -B -m unittest discover -s tests/cex -p 'test_trade_repair.py'
# Check the current source without constructing any API client.
python3 -B scripts/cex_skills.py check --target skills/gate-cex-trade --contract tests/cex/cli-contract.json
```

```python
# Select only Trade using the existing canonical builder; output must not exist.
import json
from pathlib import Path
from scripts.cex_skills import build
build(Path.cwd(), Path('dist/trade-recheck').absolute(),
      json.loads(Path('tests/cex/cli-contract.json').read_text()), profiles=('trade',))
```

隔离基线回归重现：只读导出上述固定remote SHA的skills/scripts/tests到新目录，再覆盖本次Trade、共享、builder及两份测试文件；保留该基线其他5个Skill与其完整contract，运行统一入口。此操作没有更改工作树分支。基线以外的当前分支历史差异不能据此声称已通过。

## 附录A：13类覆盖

| 正式引用 | 适用动作数 | 结论 |
| --- | --- | --- |
| algo-commands.md | 10 | PASS |
| alpha-commands.md | 9 | PASS |
| cfd-commands.md | 18 | PASS |
| convert-commands.md | 11 | PASS |
| delivery-commands.md | 21 | PASS |
| margin-commands.md | 26 | PASS |
| market-commands.md | 51 | PASS |
| options-commands.md | 17 | PASS |
| perpetual-commands.md | 51 | PASS |
| spot-commands.md | 20 | PASS |
| stocks-commands.md | 14 | PASS |
| unified-commands.md | 28 | PASS |
| vip-fees-commands.md | 7 | PASS |

分母283=282个Trade所有者动作+1个Assets所有者的Stock transactions只读复用；不共享写归属。

## 附录B：逐动作契约矩阵

| 命令 | 正式位置 | 参数/API/权限/说明检查 |
| --- | --- | --- |
| `gate-cli cex account debit-fee get` | vip-fees-commands.md:30 | PASS（静态） |
| `gate-cli cex account debit-fee set` | vip-fees-commands.md:47 | PASS（静态） |
| `gate-cli cex account detail` | unified-commands.md:51 | PASS（静态） |
| `gate-cli cex account rate-limit` | vip-fees-commands.md:68 | PASS（静态） |
| `gate-cli cex account stp add-users` | unified-commands.md:68 | PASS（静态） |
| `gate-cli cex account stp create` | unified-commands.md:88 | PASS（静态） |
| `gate-cli cex account stp list` | unified-commands.md:109 | PASS（静态） |
| `gate-cli cex account stp remove-user` | unified-commands.md:128 | PASS（静态） |
| `gate-cli cex account stp users` | unified-commands.md:148 | PASS（静态） |
| `gate-cli cex alpha account balances` | alpha-commands.md:34 | PASS（静态） |
| `gate-cli cex alpha account book` | alpha-commands.md:51 | PASS（静态） |
| `gate-cli cex alpha market currencies` | alpha-commands.md:73 | PASS（静态） |
| `gate-cli cex alpha market tickers` | alpha-commands.md:94 | PASS（静态） |
| `gate-cli cex alpha market tokens` | alpha-commands.md:115 | PASS（静态） |
| `gate-cli cex alpha order get` | alpha-commands.md:139 | PASS（静态） |
| `gate-cli cex alpha order list` | alpha-commands.md:160 | PASS（静态） |
| `gate-cli cex alpha order place` | alpha-commands.md:187 | PASS（静态） |
| `gate-cli cex alpha order quote` | alpha-commands.md:213 | PASS（静态） |
| `gate-cli cex delivery account book` | delivery-commands.md:44 | PASS（静态） |
| `gate-cli cex delivery account get` | delivery-commands.md:64 | PASS（静态） |
| `gate-cli cex delivery market candlesticks` | market-commands.md:74 | PASS（静态） |
| `gate-cli cex delivery market contract` | market-commands.md:95 | PASS（静态） |
| `gate-cli cex delivery market contracts` | market-commands.md:114 | PASS（静态） |
| `gate-cli cex delivery market insurance` | market-commands.md:131 | PASS（静态） |
| `gate-cli cex delivery market order-book` | market-commands.md:150 | PASS（静态） |
| `gate-cli cex delivery market risk-limit-tiers` | market-commands.md:170 | PASS（静态） |
| `gate-cli cex delivery market tickers` | market-commands.md:189 | PASS（静态） |
| `gate-cli cex delivery market trades` | market-commands.md:208 | PASS（静态） |
| `gate-cli cex delivery order cancel` | delivery-commands.md:81 | PASS（静态） |
| `gate-cli cex delivery order cancel-all` | delivery-commands.md:100 | PASS（静态） |
| `gate-cli cex delivery order create` | delivery-commands.md:120 | PASS（静态） |
| `gate-cli cex delivery order get` | delivery-commands.md:144 | PASS（静态） |
| `gate-cli cex delivery order list` | delivery-commands.md:163 | PASS（静态） |
| `gate-cli cex delivery order my-trades` | delivery-commands.md:185 | PASS（静态） |
| `gate-cli cex delivery position close` | delivery-commands.md:205 | PASS（静态） |
| `gate-cli cex delivery position get` | delivery-commands.md:225 | PASS（静态） |
| `gate-cli cex delivery position liquidates` | delivery-commands.md:244 | PASS（静态） |
| `gate-cli cex delivery position list` | delivery-commands.md:264 | PASS（静态） |
| `gate-cli cex delivery position settlements` | delivery-commands.md:281 | PASS（静态） |
| `gate-cli cex delivery position update-leverage` | delivery-commands.md:301 | PASS（静态） |
| `gate-cli cex delivery position update-margin` | delivery-commands.md:321 | PASS（静态） |
| `gate-cli cex delivery position update-risk-limit` | delivery-commands.md:341 | PASS（静态） |
| `gate-cli cex delivery price-trigger cancel` | delivery-commands.md:361 | PASS（静态） |
| `gate-cli cex delivery price-trigger cancel-all` | delivery-commands.md:380 | PASS（静态） |
| `gate-cli cex delivery price-trigger create` | delivery-commands.md:399 | PASS（静态） |
| `gate-cli cex delivery price-trigger get` | delivery-commands.md:423 | PASS（静态） |
| `gate-cli cex delivery price-trigger list` | delivery-commands.md:442 | PASS（静态） |
| `gate-cli cex flash-swap create` | convert-commands.md:34 | PASS（静态） |
| `gate-cli cex flash-swap create-many-to-one` | convert-commands.md:59 | PASS（静态） |
| `gate-cli cex flash-swap create-one-to-many` | convert-commands.md:80 | PASS（静态） |
| `gate-cli cex flash-swap create-v1` | convert-commands.md:101 | PASS（静态） |
| `gate-cli cex flash-swap order` | convert-commands.md:122 | PASS（静态） |
| `gate-cli cex flash-swap orders` | convert-commands.md:141 | PASS（静态） |
| `gate-cli cex flash-swap pairs` | convert-commands.md:164 | PASS（静态） |
| `gate-cli cex flash-swap preview` | convert-commands.md:185 | PASS（静态） |
| `gate-cli cex flash-swap preview-many-to-one` | convert-commands.md:209 | PASS（静态） |
| `gate-cli cex flash-swap preview-one-to-many` | convert-commands.md:230 | PASS（静态） |
| `gate-cli cex flash-swap preview-v1` | convert-commands.md:251 | PASS（静态） |
| `gate-cli cex futures account book` | perpetual-commands.md:74 | PASS（静态） |
| `gate-cli cex futures account dual-mode` | perpetual-commands.md:97 | PASS（静态） |
| `gate-cli cex futures account fee` | vip-fees-commands.md:85 | PASS（静态） |
| `gate-cli cex futures account get` | perpetual-commands.md:117 | PASS（静态） |
| `gate-cli cex futures account position-mode` | perpetual-commands.md:136 | PASS（静态） |
| `gate-cli cex futures chase create` | algo-commands.md:32 | PASS（静态） |
| `gate-cli cex futures chase get` | algo-commands.md:54 | PASS（静态） |
| `gate-cli cex futures chase list` | algo-commands.md:74 | PASS（静态） |
| `gate-cli cex futures chase stop` | algo-commands.md:103 | PASS（静态） |
| `gate-cli cex futures chase stop-all` | algo-commands.md:124 | PASS（静态） |
| `gate-cli cex futures market adl-risk-states` | market-commands.md:1023 | PASS（静态） |
| `gate-cli cex futures market batch-funding-rates` | market-commands.md:228 | PASS（静态） |
| `gate-cli cex futures market candlesticks` | market-commands.md:250 | PASS（静态） |
| `gate-cli cex futures market contract` | market-commands.md:272 | PASS（静态） |
| `gate-cli cex futures market contracts` | market-commands.md:292 | PASS（静态） |
| `gate-cli cex futures market contracts-all` | market-commands.md:1042 | PASS（静态） |
| `gate-cli cex futures market funding-rate` | market-commands.md:313 | PASS（静态） |
| `gate-cli cex futures market index-constituents` | market-commands.md:334 | PASS（静态） |
| `gate-cli cex futures market insurance` | market-commands.md:354 | PASS（静态） |
| `gate-cli cex futures market liquidations` | market-commands.md:374 | PASS（静态） |
| `gate-cli cex futures market orderbook` | market-commands.md:395 | PASS（静态） |
| `gate-cli cex futures market premium` | market-commands.md:416 | PASS（静态） |
| `gate-cli cex futures market risk-limit-table` | market-commands.md:438 | PASS（静态） |
| `gate-cli cex futures market risk-limit-tiers` | market-commands.md:457 | PASS（静态） |
| `gate-cli cex futures market rpi-orderbook` | market-commands.md:1063 | PASS（静态） |
| `gate-cli cex futures market stats` | market-commands.md:478 | PASS（静态） |
| `gate-cli cex futures market ticker` | market-commands.md:500 | PASS（静态） |
| `gate-cli cex futures market tickers` | market-commands.md:520 | PASS（静态） |
| `gate-cli cex futures market trades` | market-commands.md:539 | PASS（静态） |
| `gate-cli cex futures order add` | perpetual-commands.md:156 | PASS（静态） |
| `gate-cli cex futures order amend` | perpetual-commands.md:180 | PASS（静态） |
| `gate-cli cex futures order batch-amend` | perpetual-commands.md:204 | PASS（静态） |
| `gate-cli cex futures order batch-cancel` | perpetual-commands.md:226 | PASS（静态） |
| `gate-cli cex futures order batch-create` | perpetual-commands.md:246 | PASS（静态） |
| `gate-cli cex futures order bbo` | perpetual-commands.md:268 | PASS（静态） |
| `gate-cli cex futures order cancel` | perpetual-commands.md:292 | PASS（静态） |
| `gate-cli cex futures order close` | perpetual-commands.md:314 | PASS（静态） |
| `gate-cli cex futures order countdown-cancel-all` | perpetual-commands.md:338 | PASS（静态） |
| `gate-cli cex futures order get` | perpetual-commands.md:361 | PASS（静态） |
| `gate-cli cex futures order list` | perpetual-commands.md:381 | PASS（静态） |
| `gate-cli cex futures order list-timerange` | perpetual-commands.md:403 | PASS（静态） |
| `gate-cli cex futures order long` | perpetual-commands.md:426 | PASS（静态） |
| `gate-cli cex futures order my-trades` | perpetual-commands.md:450 | PASS（静态） |
| `gate-cli cex futures order my-trades-timerange` | perpetual-commands.md:471 | PASS（静态） |
| `gate-cli cex futures order remove` | perpetual-commands.md:494 | PASS（静态） |
| `gate-cli cex futures order short` | perpetual-commands.md:518 | PASS（静态） |
| `gate-cli cex futures position adl` | perpetual-commands.md:542 | PASS（静态） |
| `gate-cli cex futures position close-history` | perpetual-commands.md:563 | PASS（静态） |
| `gate-cli cex futures position get` | perpetual-commands.md:586 | PASS（静态） |
| `gate-cli cex futures position get-dual` | perpetual-commands.md:606 | PASS（静态） |
| `gate-cli cex futures position leverage` | perpetual-commands.md:626 | PASS（静态） |
| `gate-cli cex futures position liquidates` | perpetual-commands.md:648 | PASS（静态） |
| `gate-cli cex futures position list` | perpetual-commands.md:669 | PASS（静态） |
| `gate-cli cex futures position list-timerange` | perpetual-commands.md:688 | PASS（静态） |
| `gate-cli cex futures position update-contract-leverage` | perpetual-commands.md:711 | PASS（静态） |
| `gate-cli cex futures position update-cross-mode` | perpetual-commands.md:733 | PASS（静态） |
| `gate-cli cex futures position update-dual-cross-mode` | perpetual-commands.md:756 | PASS（静态） |
| `gate-cli cex futures position update-dual-leverage` | perpetual-commands.md:779 | PASS（静态） |
| `gate-cli cex futures position update-dual-margin` | perpetual-commands.md:800 | PASS（静态） |
| `gate-cli cex futures position update-dual-risk-limit` | perpetual-commands.md:822 | PASS（静态） |
| `gate-cli cex futures position update-leverage` | perpetual-commands.md:843 | PASS（静态） |
| `gate-cli cex futures position update-margin` | perpetual-commands.md:865 | PASS（静态） |
| `gate-cli cex futures position update-risk-limit` | perpetual-commands.md:886 | PASS（静态） |
| `gate-cli cex futures price-trigger cancel` | perpetual-commands.md:907 | PASS（静态） |
| `gate-cli cex futures price-trigger cancel-all` | perpetual-commands.md:927 | PASS（静态） |
| `gate-cli cex futures price-trigger create` | perpetual-commands.md:947 | PASS（静态） |
| `gate-cli cex futures price-trigger get` | perpetual-commands.md:974 | PASS（静态） |
| `gate-cli cex futures price-trigger list` | perpetual-commands.md:994 | PASS（静态） |
| `gate-cli cex futures price-trigger update` | perpetual-commands.md:1017 | PASS（静态） |
| `gate-cli cex futures trail create` | perpetual-commands.md:1043 | PASS（静态） |
| `gate-cli cex futures trail get` | perpetual-commands.md:1068 | PASS（静态） |
| `gate-cli cex futures trail list` | perpetual-commands.md:1088 | PASS（静态） |
| `gate-cli cex futures trail log` | perpetual-commands.md:1110 | PASS（静态） |
| `gate-cli cex futures trail stop` | perpetual-commands.md:1131 | PASS（静态） |
| `gate-cli cex futures trail stop-all` | perpetual-commands.md:1154 | PASS（静态） |
| `gate-cli cex futures trail update` | perpetual-commands.md:1176 | PASS（静态） |
| `gate-cli cex margin account book` | margin-commands.md:49 | PASS（静态） |
| `gate-cli cex margin account funding` | margin-commands.md:74 | PASS（静态） |
| `gate-cli cex margin account list` | margin-commands.md:93 | PASS（静态） |
| `gate-cli cex margin account transferable` | margin-commands.md:112 | PASS（静态） |
| `gate-cli cex margin account user-info` | margin-commands.md:132 | PASS（静态） |
| `gate-cli cex margin auto-repay get` | margin-commands.md:151 | PASS（静态） |
| `gate-cli cex margin auto-repay set` | margin-commands.md:168 | PASS（静态） |
| `gate-cli cex margin cross loans` | margin-commands.md:187 | PASS（静态） |
| `gate-cli cex margin cross repayments` | margin-commands.md:209 | PASS（静态） |
| `gate-cli cex margin leverage set` | margin-commands.md:230 | PASS（静态） |
| `gate-cli cex margin tier market` | margin-commands.md:252 | PASS（静态） |
| `gate-cli cex margin tier user` | margin-commands.md:271 | PASS（静态） |
| `gate-cli cex margin uni borrowable` | margin-commands.md:290 | PASS（静态） |
| `gate-cli cex margin uni estimate-rate` | margin-commands.md:310 | PASS（静态） |
| `gate-cli cex margin uni interest-records` | margin-commands.md:329 | PASS（静态） |
| `gate-cli cex margin uni lend` | margin-commands.md:353 | PASS（静态） |
| `gate-cli cex margin uni loan-records` | margin-commands.md:377 | PASS（静态） |
| `gate-cli cex margin uni loans` | margin-commands.md:400 | PASS（静态） |
| `gate-cli cex margin uni pair` | margin-commands.md:422 | PASS（静态） |
| `gate-cli cex margin uni pairs` | margin-commands.md:441 | PASS（静态） |
| `gate-cli cex options account book` | options-commands.md:40 | PASS（静态） |
| `gate-cli cex options account get` | options-commands.md:63 | PASS（静态） |
| `gate-cli cex options account settlements` | options-commands.md:80 | PASS（静态） |
| `gate-cli cex options market candlesticks` | market-commands.md:560 | PASS（静态） |
| `gate-cli cex options market contract` | market-commands.md:581 | PASS（静态） |
| `gate-cli cex options market contracts` | market-commands.md:600 | PASS（静态） |
| `gate-cli cex options market expirations` | market-commands.md:620 | PASS（静态） |
| `gate-cli cex options market order-book` | market-commands.md:639 | PASS（静态） |
| `gate-cli cex options market settlement` | market-commands.md:660 | PASS（静态） |
| `gate-cli cex options market settlements` | market-commands.md:681 | PASS（静态） |
| `gate-cli cex options market tickers` | market-commands.md:700 | PASS（静态） |
| `gate-cli cex options market trades` | market-commands.md:719 | PASS（静态） |
| `gate-cli cex options market underlying-candlesticks` | market-commands.md:739 | PASS（静态） |
| `gate-cli cex options market underlying-tickers` | market-commands.md:760 | PASS（静态） |
| `gate-cli cex options market underlyings` | market-commands.md:779 | PASS（静态） |
| `gate-cli cex options mmp get` | options-commands.md:99 | PASS（静态） |
| `gate-cli cex options mmp reset` | options-commands.md:118 | PASS（静态） |
| `gate-cli cex options mmp set` | options-commands.md:139 | PASS（静态） |
| `gate-cli cex options order amend` | options-commands.md:164 | PASS（静态） |
| `gate-cli cex options order cancel` | options-commands.md:188 | PASS（静态） |
| `gate-cli cex options order cancel-all` | options-commands.md:207 | PASS（静态） |
| `gate-cli cex options order countdown-cancel-all` | options-commands.md:228 | PASS（静态） |
| `gate-cli cex options order create` | options-commands.md:250 | PASS（静态） |
| `gate-cli cex options order get` | options-commands.md:276 | PASS（静态） |
| `gate-cli cex options order list` | options-commands.md:295 | PASS（静态） |
| `gate-cli cex options position close` | options-commands.md:318 | PASS（静态） |
| `gate-cli cex options position get` | options-commands.md:338 | PASS（静态） |
| `gate-cli cex options position list` | options-commands.md:357 | PASS（静态） |
| `gate-cli cex options position my-trades` | options-commands.md:376 | PASS（静态） |
| `gate-cli cex spot account batch-fee` | vip-fees-commands.md:105 | PASS（静态） |
| `gate-cli cex spot account book` | spot-commands.md:43 | PASS（静态） |
| `gate-cli cex spot account fee` | vip-fees-commands.md:124 | PASS（静态） |
| `gate-cli cex spot account get` | spot-commands.md:65 | PASS（静态） |
| `gate-cli cex spot account list` | spot-commands.md:84 | PASS（静态） |
| `gate-cli cex spot market candlesticks` | market-commands.md:796 | PASS（静态） |
| `gate-cli cex spot market currencies` | market-commands.md:817 | PASS（静态） |
| `gate-cli cex spot market currency` | market-commands.md:834 | PASS（静态） |
| `gate-cli cex spot market insurance` | market-commands.md:853 | PASS（静态） |
| `gate-cli cex spot market orderbook` | market-commands.md:876 | PASS（静态） |
| `gate-cli cex spot market pair` | market-commands.md:896 | PASS（静态） |
| `gate-cli cex spot market pairs` | market-commands.md:915 | PASS（静态） |
| `gate-cli cex spot market rpi-orderbook` | market-commands.md:1086 | PASS（静态） |
| `gate-cli cex spot market ticker` | market-commands.md:932 | PASS（静态） |
| `gate-cli cex spot market tickers` | market-commands.md:951 | PASS（静态） |
| `gate-cli cex spot market time` | market-commands.md:968 | PASS（静态） |
| `gate-cli cex spot market trades` | market-commands.md:985 | PASS（静态） |
| `gate-cli cex spot order all-open` | spot-commands.md:103 | PASS（静态） |
| `gate-cli cex spot order amend` | spot-commands.md:123 | PASS（静态） |
| `gate-cli cex spot order batch-amend` | spot-commands.md:150 | PASS（静态） |
| `gate-cli cex spot order batch-cancel` | spot-commands.md:171 | PASS（静态） |
| `gate-cli cex spot order batch-create` | spot-commands.md:192 | PASS（静态） |
| `gate-cli cex spot order buy` | spot-commands.md:213 | PASS（静态） |
| `gate-cli cex spot order cancel` | spot-commands.md:242 | PASS（静态） |
| `gate-cli cex spot order countdown-cancel-all` | spot-commands.md:264 | PASS（静态） |
| `gate-cli cex spot order cross-liquidate` | margin-commands.md:458 | PASS（静态） |
| `gate-cli cex spot order get` | spot-commands.md:286 | PASS（静态） |
| `gate-cli cex spot order list` | spot-commands.md:307 | PASS（静态） |
| `gate-cli cex spot order my-trades` | spot-commands.md:329 | PASS（静态） |
| `gate-cli cex spot order sell` | spot-commands.md:352 | PASS（静态） |
| `gate-cli cex spot pov cancel` | algo-commands.md:145 | PASS（静态） |
| `gate-cli cex spot pov cancel-all` | algo-commands.md:164 | PASS（静态） |
| `gate-cli cex spot pov create` | algo-commands.md:183 | PASS（静态） |
| `gate-cli cex spot pov get` | algo-commands.md:211 | PASS（静态） |
| `gate-cli cex spot pov list` | algo-commands.md:230 | PASS（静态） |
| `gate-cli cex spot price-trigger cancel` | spot-commands.md:380 | PASS（静态） |
| `gate-cli cex spot price-trigger cancel-all` | spot-commands.md:399 | PASS（静态） |
| `gate-cli cex spot price-trigger create` | spot-commands.md:418 | PASS（静态） |
| `gate-cli cex spot price-trigger get` | spot-commands.md:446 | PASS（静态） |
| `gate-cli cex spot price-trigger list` | spot-commands.md:465 | PASS（静态） |
| `gate-cli cex stock account assets` | stocks-commands.md:52 | PASS（静态） |
| `gate-cli cex stock account transactions` | stocks-commands.md:72 | PASS（静态） |
| `gate-cli cex stock market exchanges` | stocks-commands.md:98 | PASS（静态） |
| `gate-cli cex stock market fee-rate` | vip-fees-commands.md:143 | PASS（静态） |
| `gate-cli cex stock market orderbook` | stocks-commands.md:117 | PASS（静态） |
| `gate-cli cex stock market symbol` | stocks-commands.md:136 | PASS（静态） |
| `gate-cli cex stock market symbols` | stocks-commands.md:158 | PASS（静态） |
| `gate-cli cex stock order cancel` | stocks-commands.md:181 | PASS（静态） |
| `gate-cli cex stock order cancel-all` | stocks-commands.md:200 | PASS（静态） |
| `gate-cli cex stock order create` | stocks-commands.md:217 | PASS（静态） |
| `gate-cli cex stock order history` | stocks-commands.md:245 | PASS（静态） |
| `gate-cli cex stock order list` | stocks-commands.md:270 | PASS（静态） |
| `gate-cli cex stock order update` | stocks-commands.md:289 | PASS（静态） |
| `gate-cli cex stock position close` | stocks-commands.md:312 | PASS（静态） |
| `gate-cli cex stock position list` | stocks-commands.md:335 | PASS（静态） |
| `gate-cli cex tradfi account assets` | cfd-commands.md:43 | PASS（静态） |
| `gate-cli cex tradfi account info` | cfd-commands.md:60 | PASS（静态） |
| `gate-cli cex tradfi market categories` | cfd-commands.md:77 | PASS（静态） |
| `gate-cli cex tradfi market commissions` | cfd-commands.md:386 | PASS（静态） |
| `gate-cli cex tradfi market kline` | cfd-commands.md:94 | PASS（静态） |
| `gate-cli cex tradfi market symbol` | cfd-commands.md:115 | PASS（静态） |
| `gate-cli cex tradfi market symbols` | cfd-commands.md:134 | PASS（静态） |
| `gate-cli cex tradfi market ticker` | cfd-commands.md:151 | PASS（静态） |
| `gate-cli cex tradfi order cancel` | cfd-commands.md:170 | PASS（静态） |
| `gate-cli cex tradfi order create` | cfd-commands.md:189 | PASS（静态） |
| `gate-cli cex tradfi order history` | cfd-commands.md:216 | PASS（静态） |
| `gate-cli cex tradfi order list` | cfd-commands.md:238 | PASS（静态） |
| `gate-cli cex tradfi order log` | cfd-commands.md:406 | PASS（静态） |
| `gate-cli cex tradfi order update` | cfd-commands.md:255 | PASS（静态） |
| `gate-cli cex tradfi position close` | cfd-commands.md:279 | PASS（静态） |
| `gate-cli cex tradfi position history` | cfd-commands.md:302 | PASS（静态） |
| `gate-cli cex tradfi position list` | cfd-commands.md:324 | PASS（静态） |
| `gate-cli cex tradfi position update` | cfd-commands.md:341 | PASS（静态） |
| `gate-cli cex unified account currencies` | unified-commands.md:167 | PASS（静态） |
| `gate-cli cex unified account get` | unified-commands.md:184 | PASS（静态） |
| `gate-cli cex unified config collateral` | unified-commands.md:203 | PASS（静态） |
| `gate-cli cex unified config delta-neutral-get` | unified-commands.md:518 | PASS（静态） |
| `gate-cli cex unified config delta-neutral-set` | unified-commands.md:535 | PASS（静态） |
| `gate-cli cex unified config discount-tiers` | unified-commands.md:226 | PASS（静态） |
| `gate-cli cex unified config leverage-config` | unified-commands.md:243 | PASS（静态） |
| `gate-cli cex unified config leverage-get` | unified-commands.md:262 | PASS（静态） |
| `gate-cli cex unified config leverage-set` | unified-commands.md:281 | PASS（静态） |
| `gate-cli cex unified config leverage-set-all` | unified-commands.md:554 | PASS（静态） |
| `gate-cli cex unified config loan-tiers` | unified-commands.md:303 | PASS（静态） |
| `gate-cli cex unified loan create` | margin-commands.md:481 | PASS（静态） |
| `gate-cli cex unified loan history-rate` | margin-commands.md:504 | PASS（静态） |
| `gate-cli cex unified loan interest` | margin-commands.md:526 | PASS（静态） |
| `gate-cli cex unified loan list` | margin-commands.md:550 | PASS（静态） |
| `gate-cli cex unified loan quick-estimate` | unified-commands.md:573 | PASS（静态） |
| `gate-cli cex unified loan quick-repay` | unified-commands.md:590 | PASS（静态） |
| `gate-cli cex unified loan records` | margin-commands.md:572 | PASS（静态） |
| `gate-cli cex unified mode get` | unified-commands.md:320 | PASS（静态） |
| `gate-cli cex unified mode set` | unified-commands.md:337 | PASS（静态） |
| `gate-cli cex unified query borrowable` | unified-commands.md:358 | PASS（静态） |
| `gate-cli cex unified query borrowable-list` | unified-commands.md:377 | PASS（静态） |
| `gate-cli cex unified query estimate-rate` | unified-commands.md:396 | PASS（静态） |
| `gate-cli cex unified query transferable` | unified-commands.md:415 | PASS（静态） |
| `gate-cli cex unified query transferables` | unified-commands.md:434 | PASS（静态） |
| `gate-cli cex unified risk calculate` | unified-commands.md:453 | PASS（静态） |
| `gate-cli cex unified risk units` | unified-commands.md:477 | PASS（静态） |

## 附录C：审计工具指纹

| 文件 | SHA-256 |
| --- | --- |
| scripts/cex_skills.py | `211c747631b123cec97ab66bb3b33e2acd2341201a52226eb999429958b7df3b` |
| tests/cex/cli-contract.json | `98ac1a0e5b04f39594548be36275a1e0c94c838ae5f99aff919db4de028860c1` |
| tests/cex/test_cex_skills.py | `12e8987926f16302e8a11da20e59ee62bf5010f63b8eb3c15fb638b5d4407dc2` |
| tests/cex/test_trade_repair.py | `b9aa6a694a7c1f00bed3f1797c6bf8e35cb0435623d55079690721080a1a0417` |
| gate-cex-skill-audit/SKILL.md | `bda2964fb254b0f5442662e75b8aa8dcdd7e47b9cb66f18a6dfb7e253e5002c9` |
| gate-cex-skill-audit/references/auditor-regression.md | `6d2bf37ea2c58d5b9f44c71fc71ceba66784973dae7fa8de2e55d56223b851e4` |
| gate-cex-skill-audit/references/cli-verification.md | `caf145527e57cf2f88f0ce214a01472a21c3d7b7f8ff4accc1b5678b700be2a9` |
| gate-cex-skill-audit/references/coverage-profiles.md | `6fd5a4a05c6b8f52029d65c6797b75982207aeb9c1b35eeee9cf6ba4e24d8047` |
| gate-cex-skill-audit/references/enhanced-review.md | `646f1413b1de46034b94e7e389fd714664239d12cb308c7131fb71128ed8d702` |
| gate-cex-skill-audit/references/report-template.md | `a5bec25b41e5f78e23329cbabafce4362babe9ce629d0e38e8a38040e85c2669` |
| gate-cex-skill-audit/references/reuse-notes.md | `6ff7711289216384bd30c5fb06f5cfaa877c081e682bc079c9409545497bcf9a` |
| gate-cex-skill-audit/references/review-checklist.md | `e700abaf5629c9ee80f813f27702ddbbe9a666233165785f18c5e59e58d39a50` |
| gate-cex-skill-audit/references/safety-and-execution.md | `9293e91d02433f838d491b9505a2193c9e92bfdcba90cb1fe1e4fda191fbe1ba` |
| gate-cex-skill-audit/references/test-protocol.md | `9d7cf6b0d86d0b3f59fe2ab5bfae764cad142feaee9611183f81d392845bf8b1` |

清理记录：本次临时快照、venv、一次性脚本、构建中间目录与调试日志已清理；正式ZIP/安装目录、审查报告及其证据记录保留。HEAD/index与三处既有规则改动核对未变化，工作目录无本次生成的Python字节码。

## 提交范围记录

Milo 随后授权将本次修复与审查报告提交并推送到 GitLab `gate-skill-2.0`。提交从远端基线 `93e19c1db347872933a118439fdaa2e788e65a18` 的隔离工作树形成，仅纳入与该基线不同的本次 Trade 内容、正式测试、本文及6份验证附件。构建器与共享规则已存在于该基线，不产生重复修改。原工作树的6个其他本地审查提交、3处无关未提交规则变更、历史报告和dist产物均不纳入。

提交前再次核对全部56个源文件/共享依赖及构建器、两份测试的哈希，均与本次留存指纹一致。CLI正式契约及其他五个Skill直接来自远端93e19c1，与前述103项通过的基线隔离回归输入相同（区别于原分叉工作树的完整契约）；没有修改被测代码或Skill内容，因此复用该次实际测试结果。原分叉工作树的Earn失败记录保留为历史，不代表本提交基线失败。此记录不宣称真实交易/线上集成已验证。
