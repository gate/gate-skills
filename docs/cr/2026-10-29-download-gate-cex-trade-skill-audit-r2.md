# 下载版 gate-cex-trade 第二轮审查

## 1. 结论与审查边界

**FAIL：当前包仍不满足 gate-skill-2.0 的独立 trade Skill 要求。确认 4 个 P1、1 个 P2。** 本轮覆盖全部目标文件，按最新版下载内容重新检查，未把第一轮发现直接照搬。已修复项与剩余项分别记录；结论仅为静态审查，不表示执行过交易或观察到真实资金损失。

| 项目 | 核实结果 |
| --- | --- |
| 日期与目标 | 2026-10-29；`~/Downloads/gate-cex-trade`，独立包目录，metadata version `0.1.2` |
| 文件范围 | 16 个 Markdown，111,781 字节；没有未读目标文件、符号链接、隐藏文件、二进制、脚本、嵌套压缩包或 manifest |
| 目标指纹 | 排序后的 `(相对路径, 字节数, SHA256)` JSON 清单 SHA256：`80955ea6515789601598c365c1cb09caceda92976723476fb568420bd19caf17` |
| 对照分支 | `gate-skill-2.0@ba390fe6999026cd0d7328a4baac4eed788bd27a`；本次 read-only `git ls-remote` 与本地远端引用一致 |
| 审查入口 | 基线 `gate-cex-skill-audit/SKILL.md`；SHA256 `bda2964fb254b0f5442662e75b8aa8dcdd7e47b9cb66f18a6dfb7e253e5002c9` |
| 审查规则 | coverage-profiles、review-checklist、cli-verification、safety-and-execution、test-protocol、enhanced-review、report-template、reuse-notes。沿用同一冻结基线的已读规则，本轮重读入口、业务 profile、CLI/安全/报告要求；规则版本未改变 |
| 独立命令分母 | `tests/cex/cli-contract.json`，SHA256 `98ac1a0e5b04f39594548be36275a1e0c94c838ae5f99aff919db4de028860c1`，trade owner 共 282 个叶子 |
| 工程 CLI 证据 | 已有检出 `cd645f35e5630f0d5f5eaa4564c163c12059f845`；本轮复核 `cmd/cex`、`internal/client/client.go` 无工作树差异，并核查相关注册、handler、SDK 调用链 |
| SDK/API | 本地官方 Go SDK `v7.2.167`；本轮访问官方 API 入口（显示 v4.106.160）、公开 CFD 下单模型、多币种闪兑 create item 模型。工程源码存在不等于公共二进制已发布 |
| 前轮证据 | 同目录 `2026-10-29-download-gate-cex-trade-skill-audit.md`，本地报告提交 `25b83850e1f1e0b89bddc1248e387270ab7d5114`；旧目标指纹 `8f18efa323d2c889d478706b4cf76e87fa6a58ab069d538a253ae0f9c2d7426b` |

用户指定的 gate-skill-2.0 trade 基线仍适用，没有新的范围裁剪授权。目标关于 “supplied snapshot”“API-only” 的自述是待验证材料，不能替代基线。此前 Earn MR 的授权不适用于本 Trade 包。

本轮是小型、顺序、有界文本检查，不运行安装、构建或业务命令。检查时 16 GiB 内存、空闲比例 37%；磁盘可用约 18 GiB，df 显示 96% 已用，低于所要求的 5% 余量，因此不启动高负载/大产物操作；仅保留本报告及其小型 Git 对象，不清理用户已有文件。没有一次性落盘脚本、临时下载或测试产物。

## 2. 第一轮问题复核

| 原发现 | 本轮状态 | 依据与边界 |
| --- | --- | --- |
| F1 CFD 方向/价格类型/全平枚举 | 原资金语义错误已修正；旧适配器断言仍需更新，归 R3 | tradfi.md:34-38 现在写 API `1=sell,2=buy`、`market/trigger`、`1=partial,2=full`，并阻断冲突；workflows.md 的确认字段同步修正。不能继续把旧数值误报为本版仍会使用的下单值 |
| F2 修改一侧 TP/SL 清除另一侧 | 原缺陷已修正（静态） | tradfi.md:22,26,43 及 workflows.md:102 要求读两侧、回传未修改值，说明 omission/0 清除，缺信息阻断，并核对结果；未做真实写入验收 |
| F3 旧 Skill 依赖/多执行通道/共享安全缺口 | 部分修正；R1、R2 仍阻塞 | gate-exchange-* 硬依赖已移除，新增包内 runtime；直接 API 通道及关键共享规则缺失仍在 |
| F4 覆盖与过时 CLI 说明 | 部分修正；R3、R4 仍阻塞 | 新增 delivery/stock，有 REST 契约；delivery 覆盖明显增加，但 stock/POV/chase 等无基线 CLI 映射，旧不支持结论和关键变体缺口尚存 |
| F5 多币种闪兑误用 preview_id | 原核心缺陷已修正（静态） | flashswap.md:9-17、workflows.md:59 区分协议，使用 `params[]` 和 per-leg 结果；不再强制虚构统一 preview_id。v1 仍只说 “JSON schema returned by selected API”，端点版本及请求细节未全部具体化，不能认定全部闪兑契约已完整 |
| F6 内部来源信息 | 本轮已清理 | 原内部 GitLab URL、隐藏 checkout、提交来源叙述未再出现；16 文件公开依赖扫描无命中，人工审查未发现凭据或内网服务信息 |
| F7 重复确认 | 部分修正；R5 保留 | 入口及流程允许复用同一序列确认，但 workflows.md:26 仍绝对禁止无交互通道写入 |
| F8 规范元数据中英文混杂 | 已修正 | description 为英文；其余中文为实际用户意图和 toast 模板，属于允许的本地化示例 |

## 3. 九维结论

| ID | 维度 | 状态 | 证据 |
| --- | --- | --- | --- |
| C1 | Agent Skills 格式 | PASS | YAML 解析、重复键检查、目录/name、description 与字符串 metadata 检查；16 个 UTF-8 文本 |
| C2 | 架构与文件职责 | FAIL | CLI-only、共享 canonical 文件、独立算法参考与 MCL 所有者不符，R1 |
| C3 | 业务实质覆盖 | FAIL | 有 REST 索引仍不能替代要求的具体动作与变体，R3/R4 |
| C4 | CLI 完整与正确 | FAIL | 过时“不支持”结论、未列叶子、错误地把 Alpha 错误标签当 wire path，R3 |
| C5 | 解释与输入输出 | FAIL | 保护三态、Alpha 百分比、快速还款限额等必要语义不全，R4 |
| C6 | 引用/包完整性/对外内容 | FAIL | 14 个 Markdown 本地链接均存在；包内 runtime.md 也存在；内部信息专项本轮未发现问题，但基线共享/模型契约不齐，R1/R4 |
| C7 | 英文/术语 | PASS | description 已改为英文；中文意图示例和 toast 模板有明确用途。技术事实错误列入 C4/C5，不重复计语言问题 |
| C8 | 资金/身份/授权/隐私 | FAIL | 身份/权限绑定和安全变体缺口仍在，R2/R4；授权复用残留冲突 R5 |
| C9 | 可执行内容 | PASS（静态） | 没有目标脚本/二进制；命令文本作为数据检查，未执行。Agent 行为和真实接口集成 NOT_EVALUATED |

司法辖区和服务实体法律适用性 **NOT_EVALUATED**。本审查不作生产上线或全球合规认证。

## 4. 剩余发现

### R1 · P1 · 直接 API 执行通道及跨 Skill 写所有权仍不符合基线

- 位置：`SKILL.md:12,16,38`；`references/spot.md:122`；`references/futures.md:154`（保护操作的 API executor 备用路径）；`references/workflows.md:74`；`references/vipfee.md:19,23-24,32`。C2/C6/C8；置信度高。
- 入口允许任意 compatible transport adapter，流程明确执行 command **or API operation**，spot/futures 在 CLI 字段缺失时允许 compatible API executor。这是可调用替代通道，不是单纯列 REST 资料。基线明确业务执行只使用已注册的官方 `gate-cli cex`，不得 HTTP/SDK/MCP 旁路。
- 触发：所用 CLI 缺请求字段时，按新版可转入另一个 API 执行器；无法保证沿用 CLI 的身份、输出、超时和执行防护。应停在该能力缺口，不能自动构造另一条执行链。
- MCL create/repay/collateral 在 trade 形成了可执行写契约；coverage-profiles 的 canonical owner 是 gate-cex-earn。仅确认它是 MCL，不等于完成当前六 Skill 所有权交接。
- 结构证据：13 个 `*-commands.md`、`order-workflows.md` 和六个 `references/_shared/cex/*.md` 未按基线交付；新增 runtime.md 是独立规则副本，不是 canonical shared 的打包映射。相似文件有业务内容，不按“文件名缺失”就判零能力，但未有批准的新映射，而且 R2/R4 证明实质规则尚不等效。
- 最小修正：恢复官方 CLI 唯一执行业务边界；缺叶子/flags 时报告不支持；按基线打包 canonical 共享规则和 product/model 引用；MCL 写交给 earn，trade 可保留必要费率读取和明确 handoff。
- 复验：单包可独立读取本身全部依赖；模拟 CLI 缺字段时无 HTTP/SDK/MCP 后备写入；MCL 请求只路由到正确责任域，不在 trade 重新实现。

### R2 · P1 · 新 runtime 未建立有效交易身份及用户授权的完整绑定

- 位置：`references/runtime.md:7-15,21-23`；入口 `SKILL.md:16-20`。C8/C2；置信度高。
- 新版要求采用已选择 account/profile/base URL，检查 issuer/audience/scopes，但未解释完整 HMAC 凭据优先于 OAuth，也未要求同 origin 下核实实际 effective trading UID。profile 名称、OAuth 登录 UID、拥有 API scope 均不能直接证明本次将操作的账户及用户授予的权限。
- 独立证据：共享 cli-auth.md:14,73-75 明确凭据优先级和 effective UID；CLI `internal/client/client.go:84-85,102-110` 根据完整 key/secret 构造 HMAC 认证。场景：已有 OAuth 账户 A 和完整 HMAC 账户 B，仅按显示 profile/登录状态确认 A，仍有把写入发送给 B 的风险路径；本轮没有执行此场景，不声称已观察到误操作。
- 新版确认包含参数和停止条件，但未建立单次/累计额度、授权有效期与并发/跨会话可信账本边界；API scope 不等于用户资金授权。还缺不可信行情/错误/文档仅作数据、argv 注入边界、输出字节和分页/进程资源限额等共享约束。三次回查上限是已有改进，不能替代这些规则。
- 最小修正：复用基线 cli-auth/preflight/safety/execution-cli；先验证凭据最终来源、origin、effective UID，再绑定用户的操作/金额单位/期限/额度授权。无法核实身份或累计限额时停止对应私有任务，不自行扩大 scope。
- 复验：合成 OAuth A+HMAC B、profile 与 UID 不同、origin 切换、scope 有但用户未授权、授权过期/累计超限、恶意错误文本、输出截断场景；断言无越权写和盲重试。未运行这些 Agent 行为用例。

### R3 · P1 · 旧 CLI 快照结论仍导致必需能力缺失和错误阻断

- 位置：`references/stock.md:5,26`、`SKILL.md:36`、`references/margin.md:9,23`、`references/options.md:23`、`references/unified.md:37`、`references/alpha.md:33`、`references/tradfi.md:36-38`；完整逐叶矩阵见附录。C3/C4；置信度高。
- 本轮仍声称无 `cex stock`、spot 无 account/自动借还字段、options close/reduce-only 未暴露、Delta-neutral 无 CLI。基线契约与独立注册有 `stock` 13 个 trade 叶子，spot `--account/--auto-borrow/--auto-repay`，options `--close/--reduce-only`，unified `config delta-neutral-get|set`。注意 CLI 使用连字符，不能把 API 字段的下划线直接作为 flags。
- `spot pov` 和 `futures chase` 共 10 个叶子仍未给 CLI 映射；delivery 已增加 20/21 个产品叶子和 8 个 market 叶子，但仍缺 `delivery position close`；CFD 缺 commissions/log 叶子，VIP/费用仍缺 debit-fee/GT discount/rate-limit 等具体命令。REST 表存在的能力不当成完全未描述，但不算 CLI 契约完成。
- Alpha 再次把 `CommandError` 中的旧 path 字符串认成请求路径。已核 CLI `alpha/order.go:139,178` 实际调用 SDK，SDK `api_alpha.go:251,568` 使用 `/alpha/quote`、`/alpha/order`。新版仍据错误标签宣布 adapter drift 并阻止写前读取，会错误阻断正常链路。
- CFD 数值已改正确，但仍断言 supplied/configured CLI 使用旧值；工程证据已是字符串 price_type 和 1 partial/2 full。旧公开 CLI 源码可能不同，必须明确“版本条件”，不能把工程存在当成公共 release 已发布，也不能把旧 snapshot 当成所有安装的事实。
- 最小修正：按冻结命令表核查每项注册→handler→SDK；补全准确的命令、flags、单位/请求/返回/认证/错误。对公共安装的能力另行探测并阻断真实不兼容版本，不绕用内部构建。不凭 `--help` 退出码、日志标签或 REST 路径近似替代完整核验。
- 复验：全部 282 项有具体正确映射或已批准排除；Alpha 实际 wire path 与已记录错误标签分开；stock、delivery close、POV/chase、Delta-neutral 和费用读取逐项检查。命令提及数量不是可用性通过数。

### R4 · P1 · 已广告的交易/还款动作仍缺关键金额与保护语义

- 位置：`references/alpha.md:26-29`；`references/spot.md:70-80,122-125`；`references/unified.md:35,49`；相关 workflow 的泛化确认不能补齐产品语义。C5/C8；置信度高。
- Alpha 只说 quote currency 和 slippage 字段，未明确买入花费 **USDT**、custom 滑点为百分数（`10` 表示 10%），也未建立 quote/place 同有效 UID/origin/资产/方向/金额/gas/slippage 的完整绑定。独立 SDK `model_quote_request.go` 和基线 Alpha 模型给出确切单位。把用户的比例值直接填字段可能改变报价容忍范围；有 quote_id 不等于完整上下文已匹配。
- spot 未提供已支持的附带止盈止损契约：create 仅限 limit；amend 时遗漏或顶层 null 保留，只有字面 `{}` 取消，非法成员不得归一化成清除；保护变更仍需要经授权的 price/amount，不可为满足接口而回写陈旧价格。目标只有泛泛 protection 字段/价格触发说明，无法指导“改/清一侧保护”的正确请求。不能把 CFD 新规则套到 spot。
- quick repayment 只说两个币种数组和先估算，没有指出接口无 amount/spend-cap 参数。用户只准最多花费某金额时，选择 available_currencies 无法强制这个限额；一次 estimate 也不是服务端扣款上限。必须核实足够授权或拒绝无法表达的更紧上限。全币种杠杆的部分失败也未给可用结果处理契约（同时列入 R3 的缺叶子项，不重复计一个新发现）。
- 最小修正：补齐基线对应 product/model 变体；明示单位、省略/空值/清除、精确授权和实际返回判断，保持跨产品差异。闪兑 v1 的具体请求键和多币种端点版本也须填实，不能让执行者猜 schema。
- 复验：Alpha `10%` 与比例 `0.1` 输入、quote 字段/身份变更；spot omission/null/{}、未知/重复键及仅改保护；quick repayment 仅有币种权限与有严格金额上限；对每个场景验证实际 argv/request、禁发请求及结果断言。这里只给复验要求，没有宣称执行过这些用例。

### R5 · P2 · 无交互通道时仍无条件否定已有有效授权

- 位置：`references/workflows.md:26`；对照同文件:64,72、`SKILL.md:20` 允许有效确认复用。C5/C8；置信度高。
- 新流程允许 unchanged sequence 复用确认，但第 26 行仍规定无 interactive confirmation channel 就不得写。任务已有可验证、未过期、覆盖当前操作的完整授权且当前入口无交互时，该绝对条件仍阻断本应允许的操作。
- 最小修正英文：`If required authorization is missing or cannot be verified and no interactive channel is available, stop before writing. Reuse a valid existing grant within its verified scope and limits.` 运行暂停/恢复应重新核实授权和状态，不把暂停本身机械等同授权失效。
- 复验：同一明确授权在有/无交互通道下判定一致；缺失、过期、超范围时都停止并请求必要澄清。修正不得去掉真正需要的新授权。

## 5. 检查执行及证据限制

| 检查 | 实际结果与范围 |
| --- | --- |
| 全文件阅读 | 16/16，包括新增 runtime/delivery/stock；全部 111,781 字节低于审查预算 |
| 文件/元数据/链接 | Python 3.13 隔离模式 `-I -B`；YAML SafeLoader、重复键检查、UTF-8、文件类型/大小/hash、14 个 Markdown 本地链接存在性；无目标代码执行 |
| CLI 逐叶对照 | 读取基线 JSON，与每个文件行内命令和明确同表缩写展开对照；对关键问题人工追踪注册、handler、SDK，完整逐叶“提及定位”表见附录，不将该表叫作实测功能覆盖 |
| 公开内容扫描 | 从已审阅的冻结检查器 AST 中只提取无副作用的 `public_dependency_errors` 函数，用标准库在 16 个文本上运行，均为空；人工复核路径、内部引用、凭据及业务内容 |
| 扫描误报处理 | 补充模式的 `/Users/` 忽略大小写命中 `/tradfi/users/...` 三处，是公开 API 路径，非个人 home；不报告泄露。公开 `op-ws.gateio.live` 也不是内部服务，不能仅因不在某正则白名单就认定泄露 |
| 完整 checker/build | **NOT RUN**：`markdown_it` 依赖不存在；未安装依赖、未执行完整 checker 或重新打包。提取单函数扫描不等于 checker 全部通过 |
| CLI leaf help/真实业务 API | **NOT RUN**：没有执行下载包指令、CLI 二进制、交易、还款、账户修改或其他写入；源码检查不代替实际 help/业务集成 |
| 单元/E2E/模型行为 | **NOT_EVALUATED**：本次只生成审查文档，无产品代码修改；未运行 Agent trace、隔离功能或真实 E2E。报告中的修复验证场景是计划，不是通过记录 |
| 外部来源 | 官方 API/SDK 指定页面可访问；未读 live 内部 wiki，没有将不可访问资料作为已验证事实；没有逐一请求全部业务端点/WS |

公开核验来源：[Gate API v4](https://www.gate.com/docs/developers/apiv4/en/)、[CFD 下单模型](https://raw.githubusercontent.com/gate/gateapi-go/v7.2.167/model_trad_fi_order_request.go)、[多币种 create item](https://raw.githubusercontent.com/gate/gateapi-go/v7.2.167/model_flash_swap_multi_currency_create_param.go)。具体发布版本和账号可用性仍待选定安装环境核验。

## 6. 增强检查台账

| 检查 | 选择/结果 | 依据与限制 |
| --- | --- | --- |
| 规则新鲜度 | 已选；静态核实 | 远端分支仍为 ba390fe；审查规则、契约和相关 CLI 源码证据未变。目标显著变化，已全量重读；未沿用旧目标绿灯 |
| 源码/独立包映射 | 已选；FAIL | 目标是重写包，与基线 canonical product/models/shared 无完整生成映射；附录逐文件对照。没有生成 manifest，未假称完成正式构建一致性验证 |
| 对外内容 | 已选；本轮未发现泄露 | 16 文件扫描及人工复核，不等于保证不存在任何未知类型敏感信息 |
| 前轮问题复审 | 已选；部分已修复，整体 FAIL | 第一轮八项逐项处理见第 2 节；尚有四项 P1、一项 P2 |
| Trigger/模型效果对比 | 未选；NOT_EVALUATED | 没有调用模型服务或生成 skill-load 事件；不能推断真实触发效果 |
| 多 Skill/host 组合行为 | 未选；NOT_EVALUATED | 只审目标；MCL 所有者依据已批准 profile，不宣称其他包当前实现全局唯一 |
| 外部安全扫描器 | 未选；NOT_EVALUATED | 实际仅使用基线公开依赖函数及人工检查，未假称第三方扫描通过 |
| Auditor 回归 | NOT_APPLICABLE | 本次未修改审查 Skill，不运行 auditor 修改回归 |

## 7. 交付与最小复验范围

本报告与第一轮报告并存，只提交本报告到当前项目本地分支，不修改下载包、CLI 源码、安装包或其他报告，不 push。没有本次临时文件待清理。

修正 R1–R4 后，须复审所有受影响共享规则、入口、产品与模型契约，以及完整 282 项分母；同时复核 R5 的授权路径。已修复的 CFD 和闪兑核心语义作为回归案例保留。实际执行验证仍须在明确隔离且获授权的环境完成；当前 FAIL 不因内部信息已清理或部分命令提及增加而变为通过。

## 附录 A. 文件、业务与命令证据

以下清单由本轮目标和冻结基线读取生成，不执行目标内容。

### A1. 完整文件指纹

| 文件 | 字节 | SHA256 |
| --- | ---: | --- |
| `SKILL.md` | 9447 | `0d8ea6ccdb7c108c864521315c03f2f03e2719c99ca15b4b71c91e09f8730e3e` |
| `references/alpha.md` | 3307 | `428baab44de11efbe38e41efd038d6ac46264a6dcd0064adaafc2daff2b1b015` |
| `references/coverage.md` | 3581 | `88f4f237306e537ce1d8355fc197f3e71da907a68d05764bcdc3e2a65c03f83a` |
| `references/delivery.md` | 2718 | `faec0595d388903794518573694c800f2c7ce61ee10d0bed796d78f007c82794` |
| `references/flashswap.md` | 5351 | `e4594dc320f54d89e02d99e190faed753707343062a660e29f5f3ebda43170b3` |
| `references/futures.md` | 16167 | `f7e2344b74c6c017dbbdd1f96316c296a6838a1580807374585f37e3eee9f287` |
| `references/margin.md` | 4029 | `23ebc4f0206b3583099e9b0baa98c92163d86fb696c48e26ad13c6144b2c7f8b` |
| `references/market.md` | 4583 | `3df02b2477cf35b5a0e5ece48aa6dd1c0e9a2fb949501d17a59df467fb256476` |
| `references/options.md` | 12392 | `491de836d0051392e37b69f5e7ea3b9ca770e7388dbc9d1d4a1d8b3fed8d5b36` |
| `references/runtime.md` | 3727 | `657d9b2b9d2674eb978fcb5c977db9b68161472a801a812aa25e6733e81d9903` |
| `references/spot.md` | 10747 | `3a3528ec5b15493b7cc030d9cc154435d0d37f19252f76cf4ba4a286b531d036` |
| `references/stock.md` | 2292 | `1232ebddf04b56595c39d7c1f22b11a8fed99d8de6fa12d2996ed90c7503365a` |
| `references/tradfi.md` | 6453 | `b730e53416af6c229c31b0423c56bc72ee64e618cad6edabdd66b97ff07f3320` |
| `references/unified.md` | 5738 | `2aa3d4337ce0ec944824b21534e14dc53cf93803e414581c6486daa1109da671` |
| `references/vipfee.md` | 3497 | `c8fa4dce19188aa4397717886622df63f77a6db1f3445158e74d5f2b2bfcaec3` |
| `references/workflows.md` | 17752 | `95f400659ce3c01bb332cc10d44b602f48a00abd5f931fe752e9e1880c21c9f3` |

### A2. 逐产品/文件对照

“改名实质存在”不等于满足 canonical 布局，也不等于内容完整。算法须有独立责任文件；models 需有准确请求/响应及变体，不把只有路径表当模型。

| 基线预期参考 | 目标对应内容 | 具体叶子提及/基线分母 | 结论 |
| --- | --- | ---: | --- |
| `spot-commands.md` | spot.md | 19/20 | 部分；保护/账户变体不齐 |
| `alpha-commands.md` | alpha.md | 9/9 | 九叶子有提及；错误阻断与单位绑定缺口 |
| `perpetual-commands.md` | futures.md | 33/51 | 部分；缺命令/字段说明，API 旁路 |
| `delivery-commands.md` | delivery.md | 20/21 | 部分；缺 position close |
| `margin-commands.md` | margin.md | 22/26 | 部分；旧 CLI 借还字段结论 |
| `options-commands.md` | options.md | 14/17 | 部分；close/reduce-only 错误声明 |
| `stocks-commands.md` | stock.md | 0/13 | REST 内容存在；13 叶子未映射 |
| `cfd-commands.md` | tradfi.md | 16/18 | 方向/保护已修正；commissions/log 未映射 |
| `algo-commands.md` | spot.md + futures.md，无独立算法参考 | 0/10 | 10 叶子未映射；REST 索引不是 CLI 契约 |
| `convert-commands.md` | flashswap.md | 11/11 | 11 叶子可定位；协议细节仍需填实 |
| `market-commands.md` | market.md 及产品表 | 29/51 | 部分；RPI/ADL/多项市场读缺失 |
| `unified-commands.md` | unified.md + vipfee.md | 14/28 | 部分；Delta/quick/all-leverage 变体不齐 |
| `vip-fees-commands.md` | vipfee.md | 1/7 | 部分；MCL 写越界且费用命令缺失 |
| `order-workflows.md` | workflows.md | 不适用 | 有实质流程；R1/R5 仍在 |
| `references/_shared/cex/preflight.md` | 缺失；部分分散于 runtime.md/workflows.md | 不适用 | 非 canonical 打包，R1/R2 |
| `references/_shared/cex/cli-setup.md` | 缺失；部分分散于 runtime.md/workflows.md | 不适用 | 非 canonical 打包，R1/R2 |
| `references/_shared/cex/cli-auth.md` | 缺失；部分分散于 runtime.md/workflows.md | 不适用 | 非 canonical 打包，R1/R2 |
| `references/_shared/cex/execution-cli.md` | 缺失；部分分散于 runtime.md/workflows.md | 不适用 | 非 canonical 打包，R1/R2 |
| `references/_shared/cex/safety.md` | 缺失；部分分散于 runtime.md/workflows.md | 不适用 | 非 canonical 打包，R1/R2 |
| `references/_shared/cex/templates.md` | 缺失；部分分散于 runtime.md/workflows.md | 不适用 | 非 canonical 打包，R1/R2 |
| `references/models/algo.md` | 缺失；部分字段散在产品表 | 不适用 | 未建立基线模型映射；缺口见 R3/R4，不能仅因同名文件缺失判该业务完全不存在 |
| `references/models/alpha.md` | 缺失；部分字段散在产品表 | 不适用 | 未建立基线模型映射；缺口见 R3/R4，不能仅因同名文件缺失判该业务完全不存在 |
| `references/models/cfd.md` | 缺失；部分字段散在产品表 | 不适用 | 未建立基线模型映射；缺口见 R3/R4，不能仅因同名文件缺失判该业务完全不存在 |
| `references/models/convert.md` | 缺失；部分字段散在产品表 | 不适用 | 未建立基线模型映射；缺口见 R3/R4，不能仅因同名文件缺失判该业务完全不存在 |
| `references/models/delivery.md` | 缺失；部分字段散在产品表 | 不适用 | 未建立基线模型映射；缺口见 R3/R4，不能仅因同名文件缺失判该业务完全不存在 |
| `references/models/margin.md` | 缺失；部分字段散在产品表 | 不适用 | 未建立基线模型映射；缺口见 R3/R4，不能仅因同名文件缺失判该业务完全不存在 |
| `references/models/market.md` | 缺失；部分字段散在产品表 | 不适用 | 未建立基线模型映射；缺口见 R3/R4，不能仅因同名文件缺失判该业务完全不存在 |
| `references/models/options.md` | 缺失；部分字段散在产品表 | 不适用 | 未建立基线模型映射；缺口见 R3/R4，不能仅因同名文件缺失判该业务完全不存在 |
| `references/models/perpetual.md` | 缺失；部分字段散在产品表 | 不适用 | 未建立基线模型映射；缺口见 R3/R4，不能仅因同名文件缺失判该业务完全不存在 |
| `references/models/spot.md` | 缺失；部分字段散在产品表 | 不适用 | 未建立基线模型映射；缺口见 R3/R4，不能仅因同名文件缺失判该业务完全不存在 |
| `references/models/stocks.md` | 缺失；部分字段散在产品表 | 不适用 | 未建立基线模型映射；缺口见 R3/R4，不能仅因同名文件缺失判该业务完全不存在 |
| `references/models/unified.md` | 缺失；部分字段散在产品表 | 不适用 | 未建立基线模型映射；缺口见 R3/R4，不能仅因同名文件缺失判该业务完全不存在 |
| `references/models/vip-fees.md` | 缺失；部分字段散在产品表 | 不适用 | 未建立基线模型映射；缺口见 R3/R4，不能仅因同名文件缺失判该业务完全不存在 |

### A3. 282 个基线叶子逐项定位

本轮 188 个叶子可定位到文字提及，94 个没有具体叶子映射。**这是提及数，不是正确可用数或功能覆盖率。** 含被目标禁止、字段不全及与当前 CLI 冲突的条目；REST-only 项即使描述业务也不算有 CLI 叶子。

提取范围：全目标行内 `gate-cli cex ...`；显式 margin/trail 缩写；同一表格行中确定父命令后的短叶子（含数字），以及 `a|b` 展开。仅取完整注册路径或其参数前缀的最长匹配；未跨行猜测命令。对负面声明保留“提及”性质。初次扫描未展开带数字的 flash-swap 短叶子，已修正后生成本最终表。

| 命令 | Owner reference | API/访问类别（基线） | 效果 | 目标定位或缺失 |
| --- | --- | --- | --- | --- |
| `gate-cli cex account debit-fee get` | vip-fees-commands.md | `GET /api/v4/account/debit_fee` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex account debit-fee set` | vip-fees-commands.md | `POST /api/v4/account/debit_fee` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex account detail` | unified-commands.md | `GET /api/v4/account/detail` (private). | read | references/vipfee.md:11 |
| `gate-cli cex account rate-limit` | vip-fees-commands.md | `GET /api/v4/account/rate_limit` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex account stp add-users` | unified-commands.md | `POST /api/v4/account/stp_groups/{stp_id}/users` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex account stp create` | unified-commands.md | `POST /api/v4/account/stp_groups` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex account stp list` | unified-commands.md | `GET /api/v4/account/stp_groups` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex account stp remove-user` | unified-commands.md | `DELETE /api/v4/account/stp_groups/{stp_id}/users` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex account stp users` | unified-commands.md | `GET /api/v4/account/stp_groups/{stp_id}/users` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex alpha account balances` | alpha-commands.md | `GET /api/v4/alpha/accounts` (private). | read | references/alpha.md:16 |
| `gate-cli cex alpha account book` | alpha-commands.md | `GET /api/v4/alpha/account_book` (private). | read | references/alpha.md:17 |
| `gate-cli cex alpha market currencies` | alpha-commands.md | `GET /api/v4/alpha/currencies` (public). | read | references/alpha.md:13 |
| `gate-cli cex alpha market tickers` | alpha-commands.md | `GET /api/v4/alpha/tickers` (public). | read | references/alpha.md:15 |
| `gate-cli cex alpha market tokens` | alpha-commands.md | `GET /api/v4/alpha/tokens` (public). | read | references/alpha.md:14 |
| `gate-cli cex alpha order get` | alpha-commands.md | `GET /api/v4/alpha/order` (private). | read | references/alpha.md:19 |
| `gate-cli cex alpha order list` | alpha-commands.md | `GET /api/v4/alpha/orders` (private). | read | references/alpha.md:18 |
| `gate-cli cex alpha order place` | alpha-commands.md | `POST /api/v4/alpha/orders` (private). | write | references/alpha.md:21 |
| `gate-cli cex alpha order quote` | alpha-commands.md | `POST /api/v4/alpha/quote` (private). | read | references/alpha.md:20 |
| `gate-cli cex delivery account book` | delivery-commands.md | `GET /api/v4/delivery/{settle}/account_book` (private). | read | references/delivery.md:15 |
| `gate-cli cex delivery account get` | delivery-commands.md | `GET /api/v4/delivery/{settle}/accounts` (private). | read | references/delivery.md:15 |
| `gate-cli cex delivery market candlesticks` | market-commands.md | `GET /api/v4/delivery/{settle}/candlesticks` (public). | read | references/delivery.md:13 |
| `gate-cli cex delivery market contract` | market-commands.md | `GET /api/v4/delivery/{settle}/contracts/{contract}` (public). | read | references/delivery.md:13 |
| `gate-cli cex delivery market contracts` | market-commands.md | `GET /api/v4/delivery/{settle}/contracts` (public). | read | references/delivery.md:13 |
| `gate-cli cex delivery market insurance` | market-commands.md | `GET /api/v4/delivery/{settle}/insurance` (public). | read | references/delivery.md:14 |
| `gate-cli cex delivery market order-book` | market-commands.md | `GET /api/v4/delivery/{settle}/order_book` (public). | read | references/delivery.md:13 |
| `gate-cli cex delivery market risk-limit-tiers` | market-commands.md | `GET /api/v4/delivery/{settle}/risk_limit_tiers` (public). | read | references/delivery.md:14 |
| `gate-cli cex delivery market tickers` | market-commands.md | `GET /api/v4/delivery/{settle}/tickers` (public). | read | references/delivery.md:13 |
| `gate-cli cex delivery market trades` | market-commands.md | `GET /api/v4/delivery/{settle}/trades` (public). | read | references/delivery.md:13 |
| `gate-cli cex delivery order cancel` | delivery-commands.md | `DELETE /api/v4/delivery/{settle}/orders/{order_id}` (private). | write | references/delivery.md:17 |
| `gate-cli cex delivery order cancel-all` | delivery-commands.md | `DELETE /api/v4/delivery/{settle}/orders` (private). | write | references/delivery.md:17 |
| `gate-cli cex delivery order create` | delivery-commands.md | `POST /api/v4/delivery/{settle}/orders` (private). | write | references/delivery.md:17 |
| `gate-cli cex delivery order get` | delivery-commands.md | `GET /api/v4/delivery/{settle}/orders/{order_id}` (private). | read | references/delivery.md:17 |
| `gate-cli cex delivery order list` | delivery-commands.md | `GET /api/v4/delivery/{settle}/orders` (private). | read | references/delivery.md:17 |
| `gate-cli cex delivery order my-trades` | delivery-commands.md | `GET /api/v4/delivery/{settle}/my_trades` (private). | read | references/delivery.md:17 |
| `gate-cli cex delivery position close` | delivery-commands.md | `GET /api/v4/delivery/{settle}/position_close` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex delivery position get` | delivery-commands.md | `GET /api/v4/delivery/{settle}/positions/{contract}` (private). | read | references/delivery.md:16 |
| `gate-cli cex delivery position liquidates` | delivery-commands.md | `GET /api/v4/delivery/{settle}/liquidates` (private). | read | references/delivery.md:18 |
| `gate-cli cex delivery position list` | delivery-commands.md | `GET /api/v4/delivery/{settle}/positions` (private). | read | references/delivery.md:16 |
| `gate-cli cex delivery position settlements` | delivery-commands.md | `GET /api/v4/delivery/{settle}/settlements` (private). | read | references/delivery.md:18 |
| `gate-cli cex delivery position update-leverage` | delivery-commands.md | `POST /api/v4/delivery/{settle}/positions/{contract}/leverage` (private). | write | references/delivery.md:16 |
| `gate-cli cex delivery position update-margin` | delivery-commands.md | `POST /api/v4/delivery/{settle}/positions/{contract}/margin` (private). | write | references/delivery.md:16 |
| `gate-cli cex delivery position update-risk-limit` | delivery-commands.md | `POST /api/v4/delivery/{settle}/positions/{contract}/risk_limit` (private). | write | references/delivery.md:16 |
| `gate-cli cex delivery price-trigger cancel` | delivery-commands.md | `DELETE /api/v4/delivery/{settle}/price_orders/{order_id}` (private). | write | references/delivery.md:19 |
| `gate-cli cex delivery price-trigger cancel-all` | delivery-commands.md | `DELETE /api/v4/delivery/{settle}/price_orders` (private). | write | references/delivery.md:19 |
| `gate-cli cex delivery price-trigger create` | delivery-commands.md | `POST /api/v4/delivery/{settle}/price_orders` (private). | write | references/delivery.md:19 |
| `gate-cli cex delivery price-trigger get` | delivery-commands.md | `GET /api/v4/delivery/{settle}/price_orders/{order_id}` (private). | read | references/delivery.md:19 |
| `gate-cli cex delivery price-trigger list` | delivery-commands.md | `GET /api/v4/delivery/{settle}/price_orders` (private). | read | references/delivery.md:19 |
| `gate-cli cex flash-swap create` | convert-commands.md | `POST /api/v4/flash_swap/orders` (private). | write | references/flashswap.md:26 |
| `gate-cli cex flash-swap create-many-to-one` | convert-commands.md | `POST /api/v4/flash_swap/multi-currency/many-to-one/order/create` (private). | write | references/flashswap.md:29 |
| `gate-cli cex flash-swap create-one-to-many` | convert-commands.md | `POST /api/v4/flash_swap/multi-currency/one-to-many/order/create` (private). | write | references/flashswap.md:28 |
| `gate-cli cex flash-swap create-v1` | convert-commands.md | `POST /api/v4/flash_swap/order/create` (private). | write | references/flashswap.md:27 |
| `gate-cli cex flash-swap order` | convert-commands.md | `GET /api/v4/flash_swap/orders/{order_id}` (private). | read | references/flashswap.md:31 |
| `gate-cli cex flash-swap orders` | convert-commands.md | `GET /api/v4/flash_swap/orders` (private). | read | references/flashswap.md:30 |
| `gate-cli cex flash-swap pairs` | convert-commands.md | `GET /api/v4/flash_swap/currency_pairs` (public). | read | references/flashswap.md:24 |
| `gate-cli cex flash-swap preview` | convert-commands.md | `POST /api/v4/flash_swap/orders/preview` (private). | read | references/flashswap.md:25 |
| `gate-cli cex flash-swap preview-many-to-one` | convert-commands.md | `POST /api/v4/flash_swap/multi-currency/many-to-one/order/preview` (private). | read | references/flashswap.md:29 |
| `gate-cli cex flash-swap preview-one-to-many` | convert-commands.md | `POST /api/v4/flash_swap/multi-currency/one-to-many/order/preview` (private). | read | references/flashswap.md:28 |
| `gate-cli cex flash-swap preview-v1` | convert-commands.md | `GET /api/v4/flash_swap/order/preview` (private). | read | references/flashswap.md:27 |
| `gate-cli cex futures account book` | perpetual-commands.md | `GET /api/v4/futures/{settle}/account_book` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures account dual-mode` | perpetual-commands.md | `POST /api/v4/futures/{settle}/dual_mode` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures account fee` | vip-fees-commands.md | `GET /api/v4/futures/{settle}/fee` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures account get` | perpetual-commands.md | `GET /api/v4/futures/{settle}/accounts` (private). | read | references/futures.md:16 |
| `gate-cli cex futures account position-mode` | perpetual-commands.md | `POST /api/v4/futures/{settle}/set_position_mode` (private). | write | references/futures.md:19 |
| `gate-cli cex futures chase create` | algo-commands.md | `POST /api/v4/futures/{settle}/autoorder/v1/chase/create` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures chase get` | algo-commands.md | `GET /api/v4/futures/{settle}/autoorder/v1/chase/detail` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures chase list` | algo-commands.md | `GET /api/v4/futures/{settle}/autoorder/v1/chase/list` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures chase stop` | algo-commands.md | `POST /api/v4/futures/{settle}/autoorder/v1/chase/stop` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures chase stop-all` | algo-commands.md | `POST /api/v4/futures/{settle}/autoorder/v1/chase/stop_all` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures market adl-risk-states` | market-commands.md | `GET /api/v4/futures/{settle}/adl_risk_states` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures market batch-funding-rates` | market-commands.md | `POST /api/v4/futures/{settle}/funding_rates` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures market candlesticks` | market-commands.md | `GET /api/v4/futures/{settle}/candlesticks` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures market contract` | market-commands.md | `GET /api/v4/futures/{settle}/contracts/{contract}` (public). | read | references/futures.md:13 |
| `gate-cli cex futures market contracts` | market-commands.md | `GET /api/v4/futures/{settle}/contracts` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures market contracts-all` | market-commands.md | `GET /api/v4/futures/{settle}/contracts_all` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures market funding-rate` | market-commands.md | `GET /api/v4/futures/{settle}/funding_rate` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures market index-constituents` | market-commands.md | `GET /api/v4/futures/{settle}/index_constituents/{index}` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures market insurance` | market-commands.md | `GET /api/v4/futures/{settle}/insurance` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures market liquidations` | market-commands.md | `GET /api/v4/futures/{settle}/liq_orders` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures market orderbook` | market-commands.md | `GET /api/v4/futures/{settle}/order_book` (public). | read | references/futures.md:15 |
| `gate-cli cex futures market premium` | market-commands.md | `GET /api/v4/futures/{settle}/premium_index` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures market risk-limit-table` | market-commands.md | `GET /api/v4/futures/{settle}/risk_limit_table` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures market risk-limit-tiers` | market-commands.md | `GET /api/v4/futures/{settle}/risk_limit_tiers` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures market rpi-orderbook` | market-commands.md | `GET /api/v4/futures/{settle}/rpi_order_book` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures market stats` | market-commands.md | `GET /api/v4/futures/{settle}/contract_stats` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures market ticker` | market-commands.md | `GET /api/v4/futures/{settle}/tickers` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures market tickers` | market-commands.md | `GET /api/v4/futures/{settle}/tickers` (public). | read | references/futures.md:14 |
| `gate-cli cex futures market trades` | market-commands.md | `GET /api/v4/futures/{settle}/trades` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures order add` | perpetual-commands.md | `POST /api/v4/futures/{settle}/orders` (private). | write | references/futures.md:24 |
| `gate-cli cex futures order amend` | perpetual-commands.md | `PUT /api/v4/futures/{settle}/orders/{order_id}` (private). | write | references/futures.md:27 |
| `gate-cli cex futures order batch-amend` | perpetual-commands.md | `POST /api/v4/futures/{settle}/batch_amend_orders` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures order batch-cancel` | perpetual-commands.md | `POST /api/v4/futures/{settle}/batch_cancel_orders` (private). | write | references/futures.md:29 |
| `gate-cli cex futures order batch-create` | perpetual-commands.md | `POST /api/v4/futures/{settle}/batch_orders` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures order bbo` | perpetual-commands.md | `POST /api/v4/futures/{settle}/bbo_orders` (private). | write | references/futures.md:30 |
| `gate-cli cex futures order cancel` | perpetual-commands.md | `DELETE /api/v4/futures/{settle}/orders/{order_id}` (private); `DELETE /api/v4/futures/{settle}/orders` (private). | write | references/futures.md:28 |
| `gate-cli cex futures order close` | perpetual-commands.md | `POST /api/v4/futures/{settle}/orders` (private). | write | references/futures.md:25 |
| `gate-cli cex futures order countdown-cancel-all` | perpetual-commands.md | `POST /api/v4/futures/{settle}/countdown_cancel_all` (private). | write | references/futures.md:31 |
| `gate-cli cex futures order get` | perpetual-commands.md | `GET /api/v4/futures/{settle}/orders/{order_id}` (private). | read | references/futures.md:20 |
| `gate-cli cex futures order list` | perpetual-commands.md | `GET /api/v4/futures/{settle}/orders` (private). | read | references/futures.md:21 |
| `gate-cli cex futures order list-timerange` | perpetual-commands.md | `GET /api/v4/futures/{settle}/orders_timerange` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures order long` | perpetual-commands.md | `POST /api/v4/futures/{settle}/orders` (private). | write | references/futures.md:22 |
| `gate-cli cex futures order my-trades` | perpetual-commands.md | `GET /api/v4/futures/{settle}/my_trades` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures order my-trades-timerange` | perpetual-commands.md | `GET /api/v4/futures/{settle}/my_trades_timerange` (private). | read | references/futures.md:48 |
| `gate-cli cex futures order remove` | perpetual-commands.md | `POST /api/v4/futures/{settle}/orders` (private). | write | references/futures.md:26 |
| `gate-cli cex futures order short` | perpetual-commands.md | `POST /api/v4/futures/{settle}/orders` (private). | write | references/futures.md:23 |
| `gate-cli cex futures position adl` | perpetual-commands.md | `GET /api/v4/futures/{settle}/auto_deleverages` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures position close-history` | perpetual-commands.md | `GET /api/v4/futures/{settle}/position_close` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures position get` | perpetual-commands.md | `GET /api/v4/futures/{settle}/positions/{contract}` (private). | read | references/futures.md:17 |
| `gate-cli cex futures position get-dual` | perpetual-commands.md | `GET /api/v4/futures/{settle}/dual_comp/positions/{contract}` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures position leverage` | perpetual-commands.md | `GET /api/v4/futures/{settle}/get_leverage/{contract}` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures position liquidates` | perpetual-commands.md | `GET /api/v4/futures/{settle}/liquidates` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures position list` | perpetual-commands.md | `GET /api/v4/futures/{settle}/positions` (private). | read | references/futures.md:18 |
| `gate-cli cex futures position list-timerange` | perpetual-commands.md | `GET /api/v4/futures/{settle}/positions_timerange` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures position update-contract-leverage` | perpetual-commands.md | `POST /api/v4/futures/{settle}/positions/{contract}/set_leverage` (private). | write | references/futures.md:40 |
| `gate-cli cex futures position update-cross-mode` | perpetual-commands.md | `POST /api/v4/futures/{settle}/positions/cross_mode` (private). | write | references/futures.md:39 |
| `gate-cli cex futures position update-dual-cross-mode` | perpetual-commands.md | `POST /api/v4/futures/{settle}/dual_comp/positions/cross_mode` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures position update-dual-leverage` | perpetual-commands.md | `POST /api/v4/futures/{settle}/dual_comp/positions/{contract}/leverage` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures position update-dual-margin` | perpetual-commands.md | `POST /api/v4/futures/{settle}/dual_comp/positions/{contract}/margin` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures position update-dual-risk-limit` | perpetual-commands.md | `POST /api/v4/futures/{settle}/dual_comp/positions/{contract}/risk_limit` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures position update-leverage` | perpetual-commands.md | `POST /api/v4/futures/{settle}/positions/{contract}/leverage` (private). | write | references/futures.md:38 |
| `gate-cli cex futures position update-margin` | perpetual-commands.md | `POST /api/v4/futures/{settle}/positions/{contract}/margin` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures position update-risk-limit` | perpetual-commands.md | `POST /api/v4/futures/{settle}/positions/{contract}/risk_limit` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex futures price-trigger cancel` | perpetual-commands.md | `DELETE /api/v4/futures/{settle}/price_orders/{order_id}` (private). | write | references/futures.md:36 |
| `gate-cli cex futures price-trigger cancel-all` | perpetual-commands.md | `DELETE /api/v4/futures/{settle}/price_orders` (private). | write | references/futures.md:37 |
| `gate-cli cex futures price-trigger create` | perpetual-commands.md | `POST /api/v4/futures/{settle}/price_orders` (private). | write | references/futures.md:32 |
| `gate-cli cex futures price-trigger get` | perpetual-commands.md | `GET /api/v4/futures/{settle}/price_orders/{order_id}` (private). | read | references/futures.md:34 |
| `gate-cli cex futures price-trigger list` | perpetual-commands.md | `GET /api/v4/futures/{settle}/price_orders` (private). | read | references/futures.md:33 |
| `gate-cli cex futures price-trigger update` | perpetual-commands.md | `PUT /api/v4/futures/{settle}/price_orders/amend/{order_id}` (private). | write | references/futures.md:35 |
| `gate-cli cex futures trail create` | perpetual-commands.md | `POST /api/v4/futures/{settle}/autoorder/v1/trail/create` (private). | write | references/futures.md:41 |
| `gate-cli cex futures trail get` | perpetual-commands.md | `GET /api/v4/futures/{settle}/autoorder/v1/trail/detail` (private). | read | references/futures.md:45 |
| `gate-cli cex futures trail list` | perpetual-commands.md | `GET /api/v4/futures/{settle}/autoorder/v1/trail/list` (private). | read | references/futures.md:44 |
| `gate-cli cex futures trail log` | perpetual-commands.md | `GET /api/v4/futures/{settle}/autoorder/v1/trail/change_log` (private). | read | references/futures.md:47 |
| `gate-cli cex futures trail stop` | perpetual-commands.md | `POST /api/v4/futures/{settle}/autoorder/v1/trail/stop` (private). | write | references/futures.md:42 |
| `gate-cli cex futures trail stop-all` | perpetual-commands.md | `POST /api/v4/futures/{settle}/autoorder/v1/trail/stop_all` (private). | write | references/futures.md:43 |
| `gate-cli cex futures trail update` | perpetual-commands.md | `POST /api/v4/futures/{settle}/autoorder/v1/trail/update` (private). | write | references/futures.md:46 |
| `gate-cli cex margin account book` | margin-commands.md | `GET /api/v4/margin/account_book` (private). | read | references/margin.md:27 |
| `gate-cli cex margin account funding` | margin-commands.md | `GET /api/v4/margin/funding_accounts` (private). | read | references/margin.md:27 |
| `gate-cli cex margin account list` | margin-commands.md | `GET /api/v4/margin/accounts` (private). | read | references/margin.md:13 |
| `gate-cli cex margin account transferable` | margin-commands.md | `GET /api/v4/margin/transferable` (private). | read | references/margin.md:27 |
| `gate-cli cex margin account user-info` | margin-commands.md | `GET /api/v4/margin/user/account` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex margin auto-repay get` | margin-commands.md | `GET /api/v4/margin/auto_repay` (private). | read | references/margin.md:27 |
| `gate-cli cex margin auto-repay set` | margin-commands.md | `POST /api/v4/margin/auto_repay` (private). | write | references/margin.md:27 |
| `gate-cli cex margin cross loans` | margin-commands.md | `GET /api/v4/margin/cross/loans` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex margin cross repayments` | margin-commands.md | `GET /api/v4/margin/cross/repayments` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex margin leverage set` | margin-commands.md | `POST /api/v4/margin/leverage/user_market_setting` (private). | write | references/margin.md:27 |
| `gate-cli cex margin tier market` | margin-commands.md | `GET /api/v4/margin/loan_margin_tiers` (public). | read | references/margin.md:27 |
| `gate-cli cex margin tier user` | margin-commands.md | `GET /api/v4/margin/user/loan_margin_tiers` (private). | read | references/margin.md:27 |
| `gate-cli cex margin uni borrowable` | margin-commands.md | `GET /api/v4/margin/uni/borrowable` (private). | read | references/margin.md:27 |
| `gate-cli cex margin uni estimate-rate` | margin-commands.md | `GET /api/v4/margin/uni/estimate_rate` (private). | read | references/margin.md:27 |
| `gate-cli cex margin uni interest-records` | margin-commands.md | `GET /api/v4/margin/uni/interest_records` (private). | read | references/margin.md:27 |
| `gate-cli cex margin uni lend` | margin-commands.md | `POST /api/v4/margin/uni/loans` (private). | write | references/margin.md:22 |
| `gate-cli cex margin uni loan-records` | margin-commands.md | `GET /api/v4/margin/uni/loan_records` (private). | read | references/margin.md:27 |
| `gate-cli cex margin uni loans` | margin-commands.md | `GET /api/v4/margin/uni/loans` (private). | read | references/margin.md:27 |
| `gate-cli cex margin uni pair` | margin-commands.md | `GET /api/v4/margin/uni/currency_pairs/{currency_pair}` (public). | read | references/margin.md:27 |
| `gate-cli cex margin uni pairs` | margin-commands.md | `GET /api/v4/margin/uni/currency_pairs` (public). | read | references/margin.md:27 |
| `gate-cli cex options account book` | options-commands.md | `GET /api/v4/options/account_book` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex options account get` | options-commands.md | `GET /api/v4/options/accounts` (private). | read | references/options.md:19 |
| `gate-cli cex options account settlements` | options-commands.md | `GET /api/v4/options/my_settlements` (private). | read | references/options.md:31 |
| `gate-cli cex options market candlesticks` | market-commands.md | `GET /api/v4/options/candlesticks` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex options market contract` | market-commands.md | `GET /api/v4/options/contracts/{contract}` (public). | read | references/market.md:15 |
| `gate-cli cex options market contracts` | market-commands.md | `GET /api/v4/options/contracts` (public). | read | references/market.md:15 |
| `gate-cli cex options market expirations` | market-commands.md | `GET /api/v4/options/expirations` (public). | read | references/market.md:15 |
| `gate-cli cex options market order-book` | market-commands.md | `GET /api/v4/options/order_book` (public). | read | references/market.md:15 |
| `gate-cli cex options market settlement` | market-commands.md | `GET /api/v4/options/settlements/{contract}` (public). | read | references/options.md:33 |
| `gate-cli cex options market settlements` | market-commands.md | `GET /api/v4/options/settlements` (public). | read | references/options.md:32 |
| `gate-cli cex options market tickers` | market-commands.md | `GET /api/v4/options/tickers` (public). | read | references/market.md:15 |
| `gate-cli cex options market trades` | market-commands.md | `GET /api/v4/options/trades` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex options market underlying-candlesticks` | market-commands.md | `GET /api/v4/options/underlying/candlesticks` (public). | read | references/options.md:36 |
| `gate-cli cex options market underlying-tickers` | market-commands.md | `GET /api/v4/options/underlying/tickers/{underlying}` (public). | read | references/options.md:35 |
| `gate-cli cex options market underlyings` | market-commands.md | `GET /api/v4/options/underlyings` (public). | read | references/market.md:15 |
| `gate-cli cex options mmp get` | options-commands.md | `GET /api/v4/options/mmp` (private). | read | references/options.md:27 |
| `gate-cli cex options mmp reset` | options-commands.md | `POST /api/v4/options/mmp/reset` (private). | write | references/options.md:29 |
| `gate-cli cex options mmp set` | options-commands.md | `POST /api/v4/options/mmp` (private). | write | references/options.md:28 |
| `gate-cli cex options order amend` | options-commands.md | `PUT /api/v4/options/orders/{order_id}` (private). | write | references/options.md:26 |
| `gate-cli cex options order cancel` | options-commands.md | `DELETE /api/v4/options/orders/{order_id}` (private). | write | references/options.md:24 |
| `gate-cli cex options order cancel-all` | options-commands.md | `DELETE /api/v4/options/orders` (private). | write | references/options.md:25 |
| `gate-cli cex options order countdown-cancel-all` | options-commands.md | `POST /api/v4/options/countdown_cancel_all` (private). | write | references/options.md:30 |
| `gate-cli cex options order create` | options-commands.md | `POST /api/v4/options/orders` (private). | write | references/options.md:23 |
| `gate-cli cex options order get` | options-commands.md | `GET /api/v4/options/orders/{order_id}` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex options order list` | options-commands.md | `GET /api/v4/options/orders` (private). | read | references/options.md:22 |
| `gate-cli cex options position close` | options-commands.md | `GET /api/v4/options/position_close` (private). | read | references/options.md:34 |
| `gate-cli cex options position get` | options-commands.md | `GET /api/v4/options/positions/{contract}` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex options position list` | options-commands.md | `GET /api/v4/options/positions` (private). | read | references/options.md:20 |
| `gate-cli cex options position my-trades` | options-commands.md | `GET /api/v4/options/my_trades` (private). | read | references/options.md:21 |
| `gate-cli cex spot account batch-fee` | vip-fees-commands.md | `GET /api/v4/spot/batch_fee` (private). | read | references/spot.md:26 |
| `gate-cli cex spot account book` | spot-commands.md | `GET /api/v4/spot/account_book` (private). | read | references/spot.md:25 |
| `gate-cli cex spot account fee` | vip-fees-commands.md | `GET /api/v4/spot/fee` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex spot account get` | spot-commands.md | `GET /api/v4/spot/accounts` (private). | read | references/spot.md:24 |
| `gate-cli cex spot account list` | spot-commands.md | `GET /api/v4/spot/accounts` (private). | read | references/spot.md:23 |
| `gate-cli cex spot market candlesticks` | market-commands.md | `GET /api/v4/spot/candlesticks` (public). | read | references/market.md:11 |
| `gate-cli cex spot market currencies` | market-commands.md | `GET /api/v4/spot/currencies` (public). | read | references/market.md:11 |
| `gate-cli cex spot market currency` | market-commands.md | `GET /api/v4/spot/currencies/{currency}` (public). | read | references/market.md:11 |
| `gate-cli cex spot market insurance` | market-commands.md | `GET /api/v4/spot/insurance_history` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex spot market orderbook` | market-commands.md | `GET /api/v4/spot/order_book` (public). | read | references/market.md:11 |
| `gate-cli cex spot market pair` | market-commands.md | `GET /api/v4/spot/currency_pairs/{currency_pair}` (public). | read | references/market.md:11 |
| `gate-cli cex spot market pairs` | market-commands.md | `GET /api/v4/spot/currency_pairs` (public). | read | references/market.md:11 |
| `gate-cli cex spot market rpi-orderbook` | market-commands.md | `GET /api/v4/spot/rpi_order_book` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex spot market ticker` | market-commands.md | `GET /api/v4/spot/tickers` (public). | read | references/market.md:11 |
| `gate-cli cex spot market tickers` | market-commands.md | `GET /api/v4/spot/tickers` (public). | read | references/market.md:11 |
| `gate-cli cex spot market time` | market-commands.md | `GET /api/v4/spot/time` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex spot market trades` | market-commands.md | `GET /api/v4/spot/trades` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex spot order all-open` | spot-commands.md | `GET /api/v4/spot/open_orders` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex spot order amend` | spot-commands.md | `PATCH /api/v4/spot/orders/{order_id}` (private). | write | references/spot.md:30 |
| `gate-cli cex spot order batch-amend` | spot-commands.md | `POST /api/v4/spot/amend_batch_orders` (private). | write | references/spot.md:31 |
| `gate-cli cex spot order batch-cancel` | spot-commands.md | `POST /api/v4/spot/cancel_batch_orders` (private). | write | references/spot.md:33 |
| `gate-cli cex spot order batch-create` | spot-commands.md | `POST /api/v4/spot/batch_orders` (private). | write | references/spot.md:34 |
| `gate-cli cex spot order buy` | spot-commands.md | `POST /api/v4/spot/orders` (private). | write | references/margin.md:9 |
| `gate-cli cex spot order cancel` | spot-commands.md | `DELETE /api/v4/spot/orders/{order_id}` (private); `DELETE /api/v4/spot/orders` (private). | write | references/spot.md:32 |
| `gate-cli cex spot order countdown-cancel-all` | spot-commands.md | `POST /api/v4/spot/countdown_cancel_all` (private). | write | references/spot.md:36 |
| `gate-cli cex spot order cross-liquidate` | margin-commands.md | `POST /api/v4/spot/cross_liquidate_orders` (private). | write | references/spot.md:35 |
| `gate-cli cex spot order get` | spot-commands.md | `GET /api/v4/spot/orders/{order_id}` (private). | read | references/spot.md:21 |
| `gate-cli cex spot order list` | spot-commands.md | `GET /api/v4/spot/orders` (private). | read | references/spot.md:20 |
| `gate-cli cex spot order my-trades` | spot-commands.md | `GET /api/v4/spot/my_trades` (private). | read | references/spot.md:22 |
| `gate-cli cex spot order sell` | spot-commands.md | `POST /api/v4/spot/orders` (private). | write | references/margin.md:9 |
| `gate-cli cex spot pov cancel` | algo-commands.md | `DELETE /api/v4/spot/pov_orders/{order_id}` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex spot pov cancel-all` | algo-commands.md | `DELETE /api/v4/spot/pov_orders` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex spot pov create` | algo-commands.md | `POST /api/v4/spot/pov_orders` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex spot pov get` | algo-commands.md | `GET /api/v4/spot/pov_orders/{order_id}` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex spot pov list` | algo-commands.md | `GET /api/v4/spot/pov_orders` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex spot price-trigger cancel` | spot-commands.md | `DELETE /api/v4/spot/price_orders/{order_id}` (private). | write | references/spot.md:40 |
| `gate-cli cex spot price-trigger cancel-all` | spot-commands.md | `DELETE /api/v4/spot/price_orders` (private). | write | references/spot.md:41 |
| `gate-cli cex spot price-trigger create` | spot-commands.md | `POST /api/v4/spot/price_orders` (private). | write | references/spot.md:37 |
| `gate-cli cex spot price-trigger get` | spot-commands.md | `GET /api/v4/spot/price_orders/{order_id}` (private). | read | references/spot.md:38 |
| `gate-cli cex spot price-trigger list` | spot-commands.md | `GET /api/v4/spot/price_orders` (private). | read | references/spot.md:39 |
| `gate-cli cex stock account assets` | stocks-commands.md | `GET /api/v4/stock/users/assets` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex stock market exchanges` | stocks-commands.md | `GET /api/v4/stock/exchanges` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex stock market fee-rate` | vip-fees-commands.md | `GET /api/v4/stock/fee-rate` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex stock market orderbook` | stocks-commands.md | `GET /api/v4/stock/market/{symbol}/orderbook` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex stock market symbol` | stocks-commands.md | `GET /api/v4/stock/symbols/detail` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex stock market symbols` | stocks-commands.md | `GET /api/v4/stock/symbols` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex stock order cancel` | stocks-commands.md | `DELETE /api/v4/stock/orders/{order_id}` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex stock order cancel-all` | stocks-commands.md | `DELETE /api/v4/stock/orders` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex stock order create` | stocks-commands.md | `POST /api/v4/stock/orders` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex stock order history` | stocks-commands.md | `GET /api/v4/stock/orders/history` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex stock order list` | stocks-commands.md | `GET /api/v4/stock/orders` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex stock order update` | stocks-commands.md | `PUT /api/v4/stock/orders/{order_id}` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex stock position close` | stocks-commands.md | `POST /api/v4/stock/positions/close` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex stock position list` | stocks-commands.md | `GET /api/v4/stock/positions` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex tradfi account assets` | cfd-commands.md | `GET /api/v4/tradfi/users/assets` (private). | read | references/tradfi.md:19 |
| `gate-cli cex tradfi account info` | cfd-commands.md | `GET /api/v4/tradfi/users/mt5-account` (private). | read | references/tradfi.md:18 |
| `gate-cli cex tradfi market categories` | cfd-commands.md | `GET /api/v4/tradfi/symbols/categories` (public). | read | references/market.md:16 |
| `gate-cli cex tradfi market commissions` | cfd-commands.md | `GET /api/v4/tradfi/symbols/commissions` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex tradfi market kline` | cfd-commands.md | `GET /api/v4/tradfi/symbols/{symbol}/klines` (public). | read | references/market.md:16 |
| `gate-cli cex tradfi market symbol` | cfd-commands.md | `GET /api/v4/tradfi/symbols/detail` (private). | read | references/market.md:16 |
| `gate-cli cex tradfi market symbols` | cfd-commands.md | `GET /api/v4/tradfi/symbols` (public). | read | references/market.md:16 |
| `gate-cli cex tradfi market ticker` | cfd-commands.md | `GET /api/v4/tradfi/symbols/{symbol}/tickers` (public). | read | references/market.md:16 |
| `gate-cli cex tradfi order cancel` | cfd-commands.md | `DELETE /api/v4/tradfi/orders/{order_id}` (private). | write | references/tradfi.md:23 |
| `gate-cli cex tradfi order create` | cfd-commands.md | `POST /api/v4/tradfi/orders` (private). | write | references/tradfi.md:21 |
| `gate-cli cex tradfi order history` | cfd-commands.md | `GET /api/v4/tradfi/orders/history` (private). | read | references/tradfi.md:24 |
| `gate-cli cex tradfi order list` | cfd-commands.md | `GET /api/v4/tradfi/orders` (private). | read | references/tradfi.md:20 |
| `gate-cli cex tradfi order log` | cfd-commands.md | `GET /api/v4/tradfi/orders/log/{log_id}` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex tradfi order update` | cfd-commands.md | `PUT /api/v4/tradfi/orders/{order_id}` (private). | write | references/tradfi.md:22 |
| `gate-cli cex tradfi position close` | cfd-commands.md | `POST /api/v4/tradfi/positions/{position_id}/close` (private). | write | references/tradfi.md:27 |
| `gate-cli cex tradfi position history` | cfd-commands.md | `GET /api/v4/tradfi/positions/history` (private). | read | references/tradfi.md:28 |
| `gate-cli cex tradfi position list` | cfd-commands.md | `GET /api/v4/tradfi/positions` (private). | read | references/tradfi.md:25 |
| `gate-cli cex tradfi position update` | cfd-commands.md | `PUT /api/v4/tradfi/positions/{position_id}` (private). | write | references/tradfi.md:26 |
| `gate-cli cex unified account currencies` | unified-commands.md | `GET /api/v4/unified/currencies` (public). | read | references/unified.md:20 |
| `gate-cli cex unified account get` | unified-commands.md | `GET /api/v4/unified/accounts` (private). | read | references/unified.md:13 |
| `gate-cli cex unified config collateral` | unified-commands.md | `POST /api/v4/unified/collateral_currencies` (private). | write | references/unified.md:28 |
| `gate-cli cex unified config delta-neutral-get` | unified-commands.md | `GET /api/v4/unified/delta_neutral` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex unified config delta-neutral-set` | unified-commands.md | `POST /api/v4/unified/delta_neutral` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex unified config discount-tiers` | unified-commands.md | `GET /api/v4/unified/currency_discount_tiers` (public). | read | references/unified.md:27 |
| `gate-cli cex unified config leverage-config` | unified-commands.md | `GET /api/v4/unified/leverage/user_currency_config` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex unified config leverage-get` | unified-commands.md | `GET /api/v4/unified/leverage/user_currency_setting` (private). | read | references/unified.md:25 |
| `gate-cli cex unified config leverage-set` | unified-commands.md | `POST /api/v4/unified/leverage/user_currency_setting` (private). | write | references/unified.md:26 |
| `gate-cli cex unified config leverage-set-all` | unified-commands.md | `POST /api/v4/unified/leverage/user_setting` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex unified config loan-tiers` | unified-commands.md | `GET /api/v4/unified/loan_margin_tiers` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex unified loan create` | margin-commands.md | `POST /api/v4/unified/loans` (private). | write | references/unified.md:22 |
| `gate-cli cex unified loan history-rate` | margin-commands.md | `GET /api/v4/unified/history_loan_rate` (public). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex unified loan interest` | margin-commands.md | `GET /api/v4/unified/interest_records` (private). | read | references/unified.md:24 |
| `gate-cli cex unified loan list` | margin-commands.md | `GET /api/v4/unified/loans` (private). | read | references/unified.md:21 |
| `gate-cli cex unified loan quick-estimate` | unified-commands.md | `GET /api/v4/unified/estimated_quick_repayment` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex unified loan quick-repay` | unified-commands.md | `POST /api/v4/unified/quick_repayment` (private). | write | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex unified loan records` | margin-commands.md | `GET /api/v4/unified/loan_records` (private). | read | references/unified.md:23 |
| `gate-cli cex unified mode get` | unified-commands.md | `GET /api/v4/unified/unified_mode` (private). | read | references/unified.md:14 |
| `gate-cli cex unified mode set` | unified-commands.md | `PUT /api/v4/unified/unified_mode` (private). | write | references/unified.md:15 |
| `gate-cli cex unified query borrowable` | unified-commands.md | `GET /api/v4/unified/borrowable` (private). | read | references/unified.md:16 |
| `gate-cli cex unified query borrowable-list` | unified-commands.md | `GET /api/v4/unified/batch_borrowable` (private). | read | references/unified.md:17 |
| `gate-cli cex unified query estimate-rate` | unified-commands.md | `GET /api/v4/unified/estimate_rate` (private). | read | references/unified.md:19 |
| `gate-cli cex unified query transferable` | unified-commands.md | `GET /api/v4/unified/transferable` (private). | read | references/unified.md:18 |
| `gate-cli cex unified query transferables` | unified-commands.md | `GET /api/v4/unified/transferables` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |
| `gate-cli cex unified risk calculate` | unified-commands.md | `POST /api/v4/unified/portfolio_calculator` (public). | read | references/unified.md:36 |
| `gate-cli cex unified risk units` | unified-commands.md | `GET /api/v4/unified/risk_units` (private). | read | 未找到具体叶子映射（部分有 REST 索引） |

### A4. 冻结规则指纹

| 证据文件 | SHA256 |
| --- | --- |
| `gate-cex-skill-audit/SKILL.md` | `bda2964fb254b0f5442662e75b8aa8dcdd7e47b9cb66f18a6dfb7e253e5002c9` |
| `gate-cex-skill-audit/references/coverage-profiles.md` | `6fd5a4a05c6b8f52029d65c6797b75982207aeb9c1b35eeee9cf6ba4e24d8047` |
| `gate-cex-skill-audit/references/review-checklist.md` | `e700abaf5629c9ee80f813f27702ddbbe9a666233165785f18c5e59e58d39a50` |
| `gate-cex-skill-audit/references/cli-verification.md` | `90efb865cacac872ac7e2f19ab996b19ebf2e80d9218af514084f80c32daf2cb` |
| `gate-cex-skill-audit/references/safety-and-execution.md` | `9293e91d02433f838d491b9505a2193c9e92bfdcba90cb1fe1e4fda191fbe1ba` |
| `gate-cex-skill-audit/references/test-protocol.md` | `9d7cf6b0d86d0b3f59fe2ab5bfae764cad142feaee9611183f81d392845bf8b1` |
| `gate-cex-skill-audit/references/enhanced-review.md` | `646f1413b1de46034b94e7e389fd714664239d12cb308c7131fb71128ed8d702` |
| `gate-cex-skill-audit/references/report-template.md` | `a5bec25b41e5f78e23329cbabafce4362babe9ce629d0e38e8a38040e85c2669` |
| `gate-cex-skill-audit/references/reuse-notes.md` | `6ff7711289216384bd30c5fb06f5cfaa877c081e682bc079c9409545497bcf9a` |
| `tests/cex/cli-contract.json` | `98ac1a0e5b04f39594548be36275a1e0c94c838ae5f99aff919db4de028860c1` |
| `scripts/cex_skills.py` | `0c78461bbc6d56a2b7c9c32c40ec33326825ca874f9a3c5357be8983df6b2632` |
