# 六个 CEX Skill：四项修复与全量复审

## 1. 范围、版本与依据

**结论：PASS，限于本次确认的业务范围、工程契约、源码与独立安装包静态审查，以及隔离执行测试。F1–F4 全部关闭，无新增必修发现。** 此结论不是所有公开 CLI 发行版或真实账户交易验收。

- 日期：2026-11-02，Asia/Shanghai。基线为远端 `gate-skill-2.0@320ed4f3b1a4c3536ee8f69e6c05439a4eee057d`；交付前再次 ls-remote 核对一致。最终受审输入逐文件哈希及总摘要见 [build-inputs](./2026-11-02-gate-cex-four-fixes-rereview/build-inputs.json)。报告与代码同批提交，摘要覆盖源码、共享规则、构建器、契约、测试和审计规则。
- 使用基线中的 `gate-cex-skill-audit/SKILL.md`，读取其 checklist、coverage、CLI、safety、test、enhanced、report、reuse 规则。Milo 本轮明确答复“按当前分支范围复审”：Earn 五产品范围及 Trade 固定公开 GET/WS 例外作为本轮依据，覆盖旧 auditor profile 的对应条款。没有恢复 Launchpool/CandyDrop 或扩大私有接口能力。
- 六个业务目录 107 文件，共享依赖 6 文件，共 113 文件；全量重新解析、扫描、对账、检查本地引用。六个修复文档与其他 107 文件分别逐项比对；未变文件和原审查证据具有相同内容身份，重新核查关键流程与本次完整影响链路。
- 检查契约仍有 421 个路径：379 个归属动作、42 个排除；Trade 复用一个 Assets 股票流水只读动作。检查器合计 380 次覆盖不能算作 380 个不同动作。完整账本见附件。
- 独立依据：已有 CLI Git 对象 `5dbdb218afa2200989884d9d83c7d7b1b24a6074` 的注册/handler，以及公共 Go SDK `v7.2.170`，Origin `e7d5db1a5f3ca532fcf96333966adac113d52992`。读取固定对象和已有缓存，未修改 CLI/SDK 检出或执行其业务命令。
- 本轮再次访问 [Agent Skills 规范](https://agentskills.io/specification) 与 [官方 CLI Release 列表](https://github.com/gate/gate-cli/releases)。部分公共 SDK 网页仍无法读取，使用已核实缓存及 CLI go.sum；没有读取实时 Wiki，未将工程快照当成完整公开发行目录。

原工作树有大量用户未提交修改，实施使用独立 detached worktree；未切换、stash、reset 或覆盖原源码。没有新增应用运行配置。目录中的开发检查契约不是业务运行配置，也不被复制进安装包。

资源：10 CPU、16 GiB，初始磁盘可用约 29 GiB；后续复查空闲内存 31%、磁盘可用约 27 GiB。串行轻量检查，未做 Go 构建/压测。固定解析依赖 PyYAML 6.0.2、markdown-it-py 4.0.0、websockets 15.0.1 位于临时 venv。macOS sandbox 禁止业务网络、真实 HOME 读取和临时范围外写入，三项真实探针均被拒绝。使用清空环境、临时 HOME/TMPDIR 和 Python `-B -I`；单个检查/构建进程 30 秒预算，完整套件 120 秒预算，日志小于 1 MiB。

## 2. 六包九维结论

| 维度 | Trade | Earn | Assets | Subaccount | Affiliate | Bot | 主要证据 |
|---|---|---|---|---|---|---|---|
| C1 格式与元数据 | PASS | PASS | PASS | PASS | PASS | PASS | 安全 YAML、命名/类型、完整入口 |
| C2 架构与文件职责 | PASS | PASS | PASS | PASS | PASS | PASS | 本轮确认范围、唯一共享规则、写 owner 与只读复用 |
| C3 当前业务完整性 | PASS | PASS | PASS | PASS | PASS | PASS | 47 项必需产品/工作流/共享文件全部可达；未变范围保留 |
| C4 工程命令契约 | PASS | PASS | PASS | PASS | PASS | PASS | 379 个归属动作逐项 flags/default/required/API 对账；F1/F2 补齐 |
| C5 参数、模型与结果 | PASS | PASS | PASS | PASS | PASS | PASS | F1/F3/F4 对照 typed SDK；条款与负向测试闭合 |
| C6 本地引用与公开内容 | PASS | PASS | PASS | PASS | PASS | PASS | 源/包闭合、哈希、无越界/隐藏文件/内部信息候选 |
| C7 规范性英文 | PASS | PASS | PASS | PASS | PASS | PASS | 新增正文/注释英文；本地化 JSON 仍为明示展示数据 |
| C8 资金、授权与隐私规则 | PASS | PASS | PASS | PASS | PASS | PASS | 未改变授权/UID/金额/未知写入规则；新增参数不会发起交易 |
| C9 可执行内容 | PASS | N/A | N/A | N/A | N/A | N/A | Trade 原有三份 Python 已检查并隔离测试；其余五包无脚本 |

PASS 的 C4 是指定工程证据及本次修复层级，未认证全部公开发行版；C6 的外部资料作为信息性来源，未取得的深层页面不计为已读。C8 是文档与实际离线检查器的结论，不代表模型宿主或后端已实测强制执行授权。命令示例全部静态处理，不执行交易。

## 3. 引用与业务覆盖

见 [逐文件 inventory](./2026-11-02-gate-cex-four-fixes-rereview/inventory.json) 与 [47 项引用矩阵](./2026-11-02-gate-cex-four-fixes-rereview/reference-ledger.json)。矩阵包含全部 35 个产品命令文件、6 个工作流和6 个共享文件；每项记录归属、路径、存在性与动作数，源码/安装包均完成本地路径、显式锚点、越界与可达性检查。没有未读、超限或不可解析的本地目标文件。

| Skill | 产品与主要边界 | 不同归属动作 |
|---|---|---:|
| Trade | Spot/Alpha/Perpetual/Delivery/Margin/Options/Stocks/CFD/Algo/Convert/Market/Unified/VIP-fees；固定公开行情例外保留 | 282 |
| Earn | Simple Earn/Staking/Dual/Auto-invest/MCL；原 PD 裁剪及五产品范围保留 | 32 |
| Assets | Balances/Transfers/Deposits/Withdrawals/Small-balance；精确网络、目标与状态 | 29 |
| Subaccount | Accounts/API-keys/Permissions；管理角色、HMAC、Secret sink 边界 | 12 |
| Affiliate | Relationships/Commissions/Statistics；角色、时间窗口、收入语义与隐私 | 12 |
| Bot | Spot/Margin/Infinite/Futures grid、两类 Martingale、Smart-position、Futures-combo 与统一生命周期 | 12 |

重新检查共享授权、上下文、精确金额、部分失败、未知结果不重放、跨包交接、保护保留和只读范围。共享文件字节与基线一致；正文没有恢复“写操作/私有读取之前必须先查询 UID”的门禁。业务收款 UID、目标子账户 ID 及用户任务本身需要的账户查询仍合法。

## 4. 四项发现关闭及命令核对

[命令 ledger](./2026-11-02-gate-cex-four-fixes-rereview/command-ledger.json) 逐行保留 421 项的归属/排除、位置、真实参数和 API。379 个归属动作无缺失、类型、required/default 或 API/access 差异；不以重复调用或父 help 增加分母。不提供未建立的“最新公开 CLI 覆盖率”。

| 发现 | 修正位置 | 独立依据与关闭结果 |
|---|---|---|
| F1 P1 | Earn `models/auto-invest.md:13`、`auto-invest-commands.md` | 必填 `asset_type: int32`，1=cryptocurrency、2=TradFi stocks，无默认；保留 money/items/ratio。CLI 的显式 1/2 校验与 SDK 一致；CLOSED |
| F2 P2 | Earn `simple-earn-commands.md:169`、命令契约 | 增加 status int32/show-status string；省略、显式 0/空串的传递语义一致；2 不是默认或唯一合法值；CLOSED |
| F3 P2 | Subaccount `models/permissions.md:13` | Key 备注 name 改为 string，与 typed SDK 一致；不增加查询/凭据输出；CLOSED |
| F4 P2 | Assets `models/transfers.md:54`、Trade `models/stocks.md:227` | detail 改为 map[string]any，保留标量/列表/对象/null 及未知字段；不改变资金 owner/重试行为；CLOSED |

源码/哈希证据见 [independent-models](./2026-11-02-gate-cex-four-fixes-rereview/independent-models.json)。检查器补充开发契约驱动的模型字段类型/必填检查，以及具体 JSON 示例的资产类型检查；源码与独立安装包走同一校验入口。正常 manifest 不能掩盖错误模型。Cobra 可选字符串允许显式空值；必填业务参数继续拒绝空值，避免为了 show-status 放宽其他请求。

新代码复用原有有界 JSON/Markdown 解析、源码/包检查和构建入口；没有增加业务客户端、网络调用、安装时下载、运行配置或第二写入口。模型门禁只声称验证已声明的审查字段，完整业务语义仍需要人工审查。前次可选英文重复建议未混入本次四项修复，不改变产品含义或阻塞本轮关闭。

## 5. 实际单元与 E2E 验证

新测试文件为 `tests/cex/test_audit_repairs.py`，已纳入原 `unittest.discover("tests/cex", pattern="test_*.py")` 统一入口，6 个单元方法、4 个 E2E 方法；子场景不重复计作独立测试数。

| 场景 | 正常/异常/边界及实际断言 |
|---|---|
| 资产类型 | 显式整数 1/2 通过；缺失、0、非法整数、越界、字符串、布尔、浮点、null、坏 JSON、重复/歧义 key、超大内容拒绝；诊断不回显 body |
| 模型门禁 | 正确类型通过；缺模型/字段、错误类型、重复字段、必填被改可选必须失败 |
| 参数存在性 | status 默认为0、show-status 默认空；显式空可选字符串与省略不同；缺值及空必填 JSON 拒绝 |
| 构建安装完整链路 | 真实 builder→六包→单包无兄弟 Skill 安装→真实 checker 子进程；无 pyc，无文件依赖逃逸 |
| 合法 manifest 下的回归 | 对四处模型注入旧错误并重算 manifest，仍须 C5 FAIL，不能仅靠旧哈希报错 |
| 错误示例与筛选 | min-amount 缺资产类型实例 C8 FAIL；status 0/show-status 空实例 PASS；错 flag 类型 C4 FAIL |
| 失败清理 | 错误源模型阻止发布，最终目录与临时构建 staging 均不残留 |

最终实际执行：

- CEX 正式全套：113 tests，77.871 秒，OK。包括全部 103 个历史测试与本次 10 个测试。
- Bot 正式包测试：8 tests，6.078 秒，OK。**最终共 121 tests，0 failure**。
- 最终六包源码检查、六个真实 ZIP 解压后的单包检查全部 PASS；输出/argv 见 [final-checks](./2026-11-02-gate-cex-four-fixes-rereview/final-checks.json)。
- `git diff --check`、Python AST、本地 JSON/YAML 与全部目标文件解析通过。CEX 与 Bot 原始输出见附件。

E2E 的被测业务链路是本仓库源码/契约→构建→独立安装→校验与拒绝发布，全部真实执行；没有 mock 掉解析、构建、文件映射或校验进程。原 public stream 历史用例只 mock WebSocket 连接，保留实际参数解析、编码、接收处理、十进制输出和关闭。没有把这些测试称为真实 Gate API 调用、成交或结算。

## 6. 六个安装包与公开内容

六包均重新构建，源码等价映射只允许规定的共享链接重写；缺失/额外/改变文件均为0，143 个业务/共享副本加6 个 manifest，共149文件。逐 ZIP 检查 CRC、路径、符号链接、总展开量、清单、字节一致性和独立解压安装；相同输入两次 ZIP 序列化字节一致。完整证据见 [archive-verification](./2026-11-02-gate-cex-four-fixes-rereview/archive-verification.json)。

| ZIP | 文件数（含 manifest） | SHA-256 |
|---|---:|---|
| `gate-cex-affiliate.zip` | 15 | `8b60c7842bde482a43df1aee8a91fd8ac4992e2f318a4ddbed16a478025f4e1e` |
| `gate-cex-assets.zip` | 19 | `12d810ab301ee019baea058d785e69ecdb34591ca669744682fc770628a9f5bd` |
| `gate-cex-bot.zip` | 24 | `82edeffed0819e546fade2e0860ff5042ac0b563102fdcfbd2a405b7c3baedfd` |
| `gate-cex-earn.zip` | 19 | `5ded8d9d87b935b6aeeb84d89bb01472b8d6b0468b6991b947a20f97a29f9d51` |
| `gate-cex-subaccount.zip` | 15 | `6f3f9d8626ebdb96be50225bf8a84f58621825852e12eb7fe8a392a673d355c7` |
| `gate-cex-trade.zip` | 57 | `235f4c36d53821bf669feb96bf39ffee04b053c1b37c2877b0923be0bebbbf17` |

安装包目录仍使用既有 `dist/gate-cex-2.0/`，含六个 ZIP、六个独立目录、SHA256SUMS 和 verification-report。按仓库既有 ignore 规则，dist 制品在本机交付；代码、测试、契约与本次复审报告进入 Git，包摘要在报告中留档。安装时校验 SHA-256，再解压对应命名目录。

对 113 源文件及包内全部条目重新扫描 URL/JSON 转义与公开依赖，没有私有主机、个人路径、内部文档或真实凭据候选；不存在强制查询 UID 的新要求。规范性 Markdown 为英文；Trade 本地化 JSON 保持展示/意图例外。记录必要 API/SDK 字段与业务 ID 不等于泄露秘密。

## 7. 增强检查及证据边界

| 项目 | 状态与适用依据 |
|---|---|
| 源码/ZIP 等价、独立安装、安全扫描 | PASS；实际六 ZIP、149 文件、manifest 与源码映射 |
| 四项修复与 oracle 新鲜度 | PASS；对应已交付 CLI/SDK，模型和参数均有独立证据 |
| 本轮产品/公开传输范围 | PASS；Milo 本轮明确选择当前分支范围，未仅凭目标自述覆盖旧 profile |
| 强制 UID/共享规则回归 | PASS（文本/流程层）；源码及包内共享字节相同，授权/权限检查仍保留 |
| 触发率、模型效果对照、宿主多 Skill 执行 | NOT_EVALUATED；静态路由与规则核对不当作模型事件 |
| 审计器模型回归/外部云扫描器 | NOT_EVALUATED；未修改 auditor 自身，开发检查器实际回归另列；未上传私人源码 |
| 完整公共发行兼容性 | NOT_EVALUATED；工程契约不是所有公开发行物，运行时仍须核对可信已安装叶子 |
| 真实账户/交易/八类策略结算 | NOT_EVALUATED；无业务网络/凭据，未用合成测试替代集成验收 |
| 司法辖区/服务实体法律适用性 | NOT_EVALUATED；非法律/全球发布认证 |

## 8. 结论、提交与清理

四个确认问题已修复，完整本地源码/工程契约、独立包及隔离测试通过；本轮确认范围内没有未关闭必修问题。源码或契约/共享/构建器/包字节改变后，相关证据失效，必须重新验证；本次哈希绑定的未变内容证据可复用。

用户已授权验证后提交并 push 到 gate-skill-2.0；仅提交本次9个修复/测试/契约文件及本报告/证据，排除 docs/config 和原工作树未提交内容。Git 推送结果在最终交付中报告，不把这段审查报告当成部署证明。独立工作树、临时依赖、测试安装和中间输出在正式证据、六包交付及远端核实后清理。

附件：[构建输入哈希](./2026-11-02-gate-cex-four-fixes-rereview/build-inputs.json)、[inventory](./2026-11-02-gate-cex-four-fixes-rereview/inventory.json)、[引用矩阵](./2026-11-02-gate-cex-four-fixes-rereview/reference-ledger.json)、[命令矩阵](./2026-11-02-gate-cex-four-fixes-rereview/command-ledger.json)、[独立模型依据](./2026-11-02-gate-cex-four-fixes-rereview/independent-models.json)、[最终检查记录](./2026-11-02-gate-cex-four-fixes-rereview/final-checks.json)、[六包证据](./2026-11-02-gate-cex-four-fixes-rereview/archive-verification.json)、[CEX 测试](./2026-11-02-gate-cex-four-fixes-rereview/cex-tests.txt)、[Bot 测试](./2026-11-02-gate-cex-four-fixes-rereview/bot-tests.txt)。
