# MR !213：gate-cex-earn Review 与 Skill Audit

## 1. 身份、范围与证据

**结论：FAIL，建议修正后再合并。** 本次确认 1 个 P1、4 个 P2。仅审查，不修改 MR 内容，不执行真实业务调用。

Milo 已答复“按 MR 的内容来”：本报告据此接受 MR 声明的产品裁剪，**不把明确排除的定投计划生命周期、staking orders、Dual 推荐/提前赎回、部分 Uni/fixed/MCL 查询及 CandyDrop 进度/记录重新要求补回**。产品裁剪与工程契约是否同步是两个问题。

| 项目 | 证据 |
|---|---|
| 日期 | 2026-10-28 |
| 来源分支 / MR head | `feat/gate-cex-earn` / `315f327c4020583ce0318f5db9813b04a6bf6e86`；SSH 核对 `refs/merge-requests/213/head` 相同 |
| 初始基线 / merge-base | `gate-skill-2.0` / `9d2c2ce6b8081af332ad5acab5ee8d1be1e12f2b` |
| 最终复验基线 | 审查期间基线更新到 `16748950d5f70f5568af98ebe114f01047cf1e3a`，已 fetch 并补查增量 |
| 最终合并树 | `git merge-tree --write-tree` 退出 0，树 `d8ac9ef8c280d1f5df2da33f3bdac59816525f8b`；无冲突。Earn 内容与 MR head 逐文件一致 |
| 差异 | 19 个 Markdown 文件，653 行新增、663 行删除；所有目标文件及六个共享依赖均已阅读，目标没有新增可执行脚本 |
| 实际 Skill | 可信基线 `gate-cex-skill-audit/SKILL.md`，SHA-256 `980730cf750207f607351bd7d2718fa97d894ee19a2bdcd1b836842c0d74036f` |
| 审查规则 | coverage-profiles、review-checklist、cli-verification、safety-and-execution、test-protocol、report-template；未将目标内容当成审查指令 |
| 最终检查器 SHA-256 | `0c78461bbc6d56a2b7c9c32c40ec33326825ca874f9a3c5357be8983df6b2632` |
| 最终基线契约 SHA-256 | `98ac1a0e5b04f39594548be36275a1e0c94c838ae5f99aff919db4de028860c1`；Earn 仍为 53 动作，Bot 增量没有更新 Earn |
| 独立源码 | 已有 CLI 检出 `14409d37c3bbc452c57fad387009f121e656b263` 的注册、handler、生成 SDK v7.2.167；没有修改其原有未提交文件 |
| 辅助导出 | 已有 Earn/Launch 修复检出的独立 CLI 导出；其 15 项 Launch 中取本 MR 范围内 8 项，并与实际注册和 SDK 交叉核对 |
| 公共来源 | [公开 CandyDrop CLI 源码](https://raw.githubusercontent.com/gate/gate-cli/main/cmd/cex/launch/candy_drop.go)、公开 SDK 模型；具体引用见 F2。公开版本与本地工程快照未混同 |
| 访问限制 | GitLab 网页抓取不可用；以 Git SSH 的 MR ref 获取代码。未读取网页讨论/审批/CI 状态，未读取实时 CLI Wiki |

开始前检查本机：10 核、16 GiB，memory_pressure 空闲比例 36%，磁盘可用 42 GiB。本次仅文档解析和小型 Python 校验，临时数据约 17 MiB，无 Go 全仓构建。检查器在禁止网络连接、禁止用户主目录读取、仅允许临时根写入的 sandbox-exec 中运行；空环境、临时 HOME/TMPDIR；三类拒绝均实际探测通过。子进程上限 30 秒，场景上限 120 秒，捕获输出限制 1 MiB，校验串行。

## 2. 九维结论

| ID | 维度 | 状态 | 依据 |
|---|---|---|---|
| C1 | Agent Skills 格式 | PASS | 名称/目录、frontmatter、description 长度有效；入口引用正常 |
| C2 | 架构与文件约定 | FAIL | 批准后的范围未落到统一契约；新标准章节/模型/检查器约定未同步，F1 |
| C3 | 业务覆盖 | FAIL | 按 Milo 认可的 MR 范围，40 个业务路径都有文档入口，被排除项不是遗漏；跨产品概览的处理路径仍冲突，见 F4 |
| C4 | CLI 正确性 | FAIL | 新增 8 叶子确实存在；标准参数/API 描述不完整且部分类型不符，F1；响应字段与实际 typed SDK 不符，F2 |
| C5 | 说明清晰度 | FAIL | APR/APY、资金/收益区分有改善；聚合意图出现互斥处理，F4；CandyDrop 字段约定错误，F2 |
| C6 | 引用与内容完整性 | PASS | 25 个目标/共享文件中未发现失效本地路径/锚点、私有地址、个人绝对路径、固定开发 revision 或凭据字面量；MR 安装包因门禁失败未发布，不能声称安装验收通过 |
| C7 | 英文 | PASS | 规范性内容为英文；一处排版笔误单列为编辑项，无本地化例外 |
| C8 | 资金、授权与隐私 | FAIL | 通用 UID、权限、十进制、未知写入不重放规则保留；fresh confirmation 与已有有效授权冲突，F3；未发现真实秘密 |
| C9 | 目标可执行内容 | NOT_APPLICABLE | MR 全为 Markdown，未新增脚本或二进制。示例只做静态分析，校验器的实际运行另列，不当作业务行为验证 |

司法辖区/服务实体法律适用性：**NOT_EVALUATED**。未执行真实交易、登录、凭据切换、付费模型评测或真实账户读取；不提供生产/法律合规认证。

## 3. 完整文件与能力覆盖

以下相对 `skills/gate-cex-earn/`；全部 19 个文件已读。六个共享文件另列。

| 文件 | 核验内容 | 结果/边界 |
|---|---|---|
| `SKILL.md` | S1 产品、S2 报价收益、S3 持仓收益、S4 操作；九条路由；共享门禁 | 格式正常；跨产品路由与后文不一致，F4 |
| `README.md` | 七产品、排除范围、CLI-only、测试环境说明 | 范围采用用户确认；不视为环境授权 |
| `CHANGELOG.md` | 两条版本记录 | 包含架构、PD、SDK/构建限制等非接口变更，F5 |
| `references/simple-earn-commands.md` | 12 动作；Uni lend/redeem、min_rate、固定产品/历史/预赎回 | 保留原有关键资金语义，没有发现新增反向操作 |
| `references/models/simple-earn.md` | 输入/响应、状态、fixed 请求字段、coupon、min_rate | 关键 lend 必须 min_rate、固定申购参数仍在；排除能力模型删除按范围处理 |
| `references/staking-commands.md` | find/assets/awards/swap；side0/1；多 pid/币种选择 | 4 路径保留，orders 按范围排除；F3 |
| `references/models/staking.md` | 产品/持仓/奖励/兑换模型 | find/assets 在 SDK 中为 map；部分展示字段的完整服务端语义仍需契约依据，未冒充真实赎回验收 |
| `references/dual-investment-commands.md` | 5 动作、卖高/买低、结算币种、reinvest、APY | 关键转换/状态说明保留；推荐/refund 排除已认可 |
| `references/models/dual-investment.md` | 计划/订单/余额/复投模型 | decimals/IDs 保留；公开示例小数 APY 与乘 100 的展示规则一致 |
| `references/auto-invest-commands.md` | coins/min-amount/orders，订单要求 plan-id/record-id | 3 项只读；计划生命周期不要求恢复；订单查询没有时间/分页 flag，不得按末尾通用文字虚构 flag |
| `references/models/auto-invest.md` | 资产、最低金额组合、订单模型 | 引用完整；ratio 单位说明不足列为补充项，不将原有缺口误作本次新缺陷 |
| `references/collateral-loan-commands.md` | 8 动作；collateral/loan/repay/LTV/records | 固定利率资料缺失时停止、不自动改 current；自动补偿禁止保留 |
| `references/models/collateral-loan.md` | fixed_type/fixed_rate、自动续借/还款、逐币结果 | 关键约束仍在；删除产品目录/利率/额度模型按范围处理 |
| `references/launchpool-commands.md` | 5 叶子，pid/rid/amount、收益/记录时间单位、恢复 | 实际路径/写入 body 存在；标准章节、API 行、页字段类型问题并入 F1 |
| `references/models/launchpool.md` | 项目/池/额度、pledge/redeem、记录 | 公开 SDK 实际有对应模型，应按它说明字段，不应写成缺少 SDK 而用旧契约替代；F2 关联修正 |
| `references/candydrop-commands.md` | 3 叶子、匿名读取/注册、排除 progress/records | 3 路径存在；缺标准 action 章节，F1；输出与确认分别见 F2/F3 |
| `references/models/candydrop.md` | 活动/规则/任务/注册请求和结果 | 存在当前 typed SDK 不会输出的字段，F2 |
| `references/earn-aggregation-commands.md` | 资产/奖励/订单聚合边界 | 不要求创造专用聚合 endpoint；应与现有逐产品概览明确区分，F4 |
| `references/earn-workflows.md` | 申购/赎回、只读定投、借贷、两类活动、跨产品概览 | 不重放、同身份和上下文保留；与聚合路由的冲突见 F4 |
| `../_shared/cex/preflight.md` | 实际 UID/来源/权限、可信 dev 版本 | MR 未改，已核验继承；不会仅因版本为 dev 拒绝 |
| `../_shared/cex/cli-setup.md` | 官方安装、校验和、来源、环境 | MR 未改；无自动获取私有制品 |
| `../_shared/cex/cli-auth.md` | HMAC/OAuth 优先级、身份读取、scope 与权限 | MR 未改；不把 profile 或本地有效 token 当实际 UID |
| `../_shared/cex/execution-cli.md` | argv、JSON、限时/限量、产品输出、未知结果 | MR 未改；没有通用 success envelope；业务示例未执行 |
| `../_shared/cex/safety.md` | 验证既有授权、限制资金影响、非可信内容 | MR 未改；与 fresh confirmation 冲突见 F3 |
| `../_shared/cex/templates.md` | 草稿、结果、未知状态 | MR 未改；模板不构造权限 |

## 4. CLI 对照与范围分母

本次采用的分母是 **40 个业务叶子**：基线 53 个 Earn 动作中排除 21 个，新增 5 个 Launchpool 与 3 个 CandyDrop。CLI 的其他能力存在不代表本 MR 必须暴露；HODLer/Idle、CandyDrop 的 progress/participations/airdrops 均不纳入。本次没有将已退役 activity-center 当作活动能力的替代入口。

| 组 | 接受范围内的叶子（省略 `gate-cli cex`） | 数量 |
|---|---|---:|
| Simple Earn | `earn fixed create/history/lends/pre-redeem/products`；`earn uni change/interest-records/interest-status/lend/lends/rate/records` | 12 |
| Staking | `earn staking assets/awards/find/swap` | 4 |
| Dual | `earn dual balance/modify-reinvest/orders/place/plans` | 5 |
| Auto-invest | `earn auto-invest coins/min-amount/orders` | 3 |
| MCL | `mcl collateral/create/ltv/order/orders/records/repay/repay-records` | 8 |
| Launchpool | `launch projects/pledge/redeem/pledge-records/reward-records` | 5 |
| CandyDrop | `launch candy-drop activities/rules/register` | 3 |

40 路径均能从目标文档找到，但只有 37 项采用现有 canonical 命令章节，CandyDrop 三项只有表格。**没有因此宣称 40/40 完整正确或 100% 功能通过。** 新增 8 项已核对独立 CLI 注册、handler 和 SDK；未运行真实业务 argv。

| 新增操作 | 已核实输入/访问 | 说明缺口 |
|---|---|---|
| Launch projects | status/limit-rule 等过滤与分页；public；page/page-size int32 | 当前数值注册缺省 0 与“Unset”混用；少 API 行 |
| Launch pledge | 必需 `--json`，pid/rid int32、amount string；private | 少标准 flag 表/API 行 |
| Launch redeem | 必需 `--json`，同项目/池/金额；private | 少标准 flag 表/API 行 |
| Launch pledge-records | private；page/page-size 为 int64；时间为格式化字符串 | 文档写 int32；缺省/方法路径契约不完整 |
| Launch reward-records | private；page/page-size/start-time/end-time 为 int64，时间秒 | 文档分别写 int32/int；方法路径契约不完整 |
| Candy activities | public；currency/status/rule-name/register-status/limit/offset | 查询参数不能推导响应也有 status/register_status；F2 |
| Candy rules | public；currency 或 activity-id；SDK 响应不是请求参数回显 | 文档虚列 activity_id 响应字段；F2 |
| Candy register | private；currency required，activity-id optional int64 | flags 正确；需明确可确认的 success 与不可确认的后续状态，不恢复已排除进度接口 |

21 项排除名单：auto-invest 的 add-position/config/create/plan-detail/plans/records/stop/update；dual recommend/refund/refund-preview；fixed products-asset；staking orders；uni chart/currencies/currency/interest；mcl currencies/current-rate/fix-rate/quota。它们只用于准确收敛工程契约，**不是本次“漏做 21 项”的缺陷清单**。

## 5. 确认的问题与修正要求

### F1 · P1 · C2/C4：同步批准范围与标准命令契约，恢复 Earn 构建

- 位置：`references/launchpool-commands.md:30-36`、`references/candydrop-commands.md:18-33`；关联未更新的 `tests/cex/cli-contract.json`、profiles 及标准参数/API 章节。
- 置信度：高，最终基线和实际无冲突合并树均已执行校验/构建。
- 触发：使用项目现有 checker 或统一 builder 发布此 Earn Skill。
- 证据：最终基线 Earn source PASS、单 Earn build PASS；合并后 Earn source FAIL（C2=3、C4=33）、单 Earn build FAIL，无输出。接受产品裁剪不自动修改脚本读入的契约。
- 为排除旧范围误报，本次仅在临时诊断契约移除已批准排除的 21 项、加入独立确认的 8 项并加入 aggregation 参考；检查仍 FAIL（C2=2、C4=23）。三个 CandyDrop 标准章节缺失；Launchpool 五项 API 行缺失，写入缺 flag 表，历史分页/时间 flag 的类型与注册不一致。
- 后果：MR 没有可通过项目现有流程生成的 Earn 安装包；旧契约被保留，后续检查结果不能准确反映已批准范围。
- 修正：精确更新 Earn 的 owner/profile/命令导出与文档，保留其他 Skill 契约；补齐三项 CandyDrop canonical action 和八项真实 API/flag/default/required/access 信息。MCP 工具名对照移出执行路由，否定 MCP 的文字不要被校验器误判为执行兜底。保留有效检查，不能删断言或跳过检查让构建变绿。
- 复验：scope 分母 40、所有路径/flag/锚点与安装包内容一致；单 Earn 构建及独立 package 检查通过。六包构建另须等待下文所列基线 Stock 问题处理。

### F2 · P2 · C4/C5：CandyDrop 响应模型包含实际 CLI 不会返回的字段

- 位置：`references/models/candydrop.md:13-16,25`；关联 `candydrop-commands.md:20` 的活动状态要求和 `models/candydrop.md:5-8` 的模型来源说明。
- 置信度：高，基于指定 SDK 和 CLI 的实际返回类型，不是根据接口名推断。
- 触发：通过当前已核实 CLI 执行 activities/rules 后，按 Skill 的“CLI field contract”读取活动 status/register_status 或 rules.activity_id。
- 证据：CLI 使用 SDK typed response，再打印该对象。公开 [CandyDropV4ActivityCd01](https://raw.githubusercontent.com/gate/gateapi-go/v7.2.167/model_candy_drop_v4_activity_cd01.go) 不含 status/register_status；[CandyDropV4ActivityRulesCd03](https://raw.githubusercontent.com/gate/gateapi-go/v7.2.167/model_candy_drop_v4_activity_rules_cd03.go) 不含 activity_id。即使原始 HTTP JSON 有未声明属性，typed 解码后也不会原样透传。将这些字段标为 optional 并不能证明当前 CLI 可输出它们。
- 后果：规范要求的状态展示/查询关联缺少相应数据来源，Agent 容易等待不存在字段、错误推断状态或宣称已经核实。没有证据表明实际发生过奖励误发或注册重放。
- 修正：按实际 SDK 保留可输出字段；请求 ID 从已验证请求上下文保留，不能声称服务端已回显；未知状态明确未知。如果另有可信新 CLI 能保留字段，写明能力证据再启用。Launchpool/CandyDrop 已有生成 SDK，不应以“本仓库不提供 SDK 模型”为理由沿用未经核验的旧字段。
- 复验：通过合成 raw JSON → 实际 SDK 类型 → CLI 输出验证字段集合，并检查状态缺失时不虚构值。此报告完成了静态类型链路核对，未声称运行了这一业务 E2E。

### F3 · P2 · C8：fresh confirmation 与共享的有效授权复用规则矛盾

- 位置：`references/staking-commands.md:138-142`、`references/candydrop-commands.md:35-38`，关联 `models/candydrop.md:55-56`。
- 置信度：高，规范文本直接冲突；未运行 Agent 行为评测。
- 触发：已有同 UID、环境、产品、参数、限额、有效期内的完整明确授权，用户要求执行原授权动作。
- 证据：目标要求 draft 后 fresh confirmation；继承的 shared safety 明确复用可验证已有授权，且 `SKILL.md:67` 仍采用该规则。
- 后果：同一 Skill 内两套授权规则，导致已授权操作被无条件再阻塞；并不增加实际 UID/限额验证能力。
- 修正：已有完整有效授权可复用；仅对缺失、超范围、过期或变更的授权请求补充确认。不要把“用户认可 MR 的产品范围”解释成废弃共享授权协议。
- 复验：完整授权不固定再问一次；账户、金额、环境或期限变化时在新授权前无写入。

### F4 · P2 · C3/C5：同一跨产品概览请求被导向两种互斥行为

- 位置：`SKILL.md:26`、`references/earn-aggregation-commands.md:13-15`；关联 `SKILL.md:59-61` 与 `earn-workflows.md:27-34`。
- 置信度：高；静态路由推演。
- 触发：用户询问“我的 Earn 持仓/收益，按产品展示”。
- 证据：入口的 cross-product assets/rewards 路由指向 aggregation，该文件要求报告 CLI pending，并把产品记录替代聚合判为不等价；入口后文和 workflow 对相同场景却要求调用各产品、分组展示并标注缺失来源。两者没有区分用户要的是分组概览、统一服务记录，还是统一统计口径。
- 后果：同一个已支持的逐产品展示请求可能被直接拒绝，或把不完整组合冒充统一聚合；不是在要求新增聚合接口。
- 修正：明确逐产品分组概览走 workflow；真正要求统一服务端资产/券/订单口径、但现有 CLI 无法等价提供的请求才走 boundary。不得自动恢复被排除产品，也不应无条件扩大用户读取范围。
- 复验：分组持仓、累计收益、统一券记录、跨产品订单、部分产品失败各自有唯一处理路径；缺失来源明确标注，无伪造总额。

### F5 · P2 · 对外文档规则：CHANGELOG 记录了非接口变更与研发中间状态

- 位置：`CHANGELOG.md:6-11,16-23`。
- 置信度：高；与工作区已确认的 changelog 规则直接不符。
- 触发：随 Skill 源码/安装内容发布该 CHANGELOG。
- 证据：条目包含采用参考架构、PD P0 清单、等待 CLI 注册、去固定构建约束、补模型与路由等过程说明。工作区要求仅记录接口/参数实际新增、删除、修改，不记录研发过程、内部架构和中间状态。
- 后果：发布说明混入非接口与内部过程信息，不能直接作为长期对外记录使用。未发现真实凭据或内部服务地址，不把这些过程描述升级为秘密泄露。
- 修正：逐条核实是否存在真实接口或参数变化；仅保留接口及字段层面的变化。纯 Skill 文档整理没有此类变化时，不新增版本条目；工程背景保留在非运行时的审查记录。
- 复验：所有最终条目可关联真实接口/参数差异，不能把“新增已有接口的文档”写成新发布接口。

### 编辑项与未确认项

- `earn-aggregation-commands.md:14`：`Reward/coupon histor  y` 改为 `Reward/coupon history`；排版笔误，不单列阻塞缺陷。
- `models/auto-invest.md:18` 的 ratio 只有 string 类型，没有百分数单位。独立 SDK 注释为 `e.g.100`，建议补明确单位/例子；原 min-amount 模型也缺此说明，不把它当作本次新增缺陷，也不为了补它恢复已排除的 create 路由。
- `auto-invest-commands.md` 末尾提示缩短时间窗口/翻页，但 orders 只有 plan-id/record-id；应避免误读成支持不存在的 flags。它是模板化说明问题，实际是否截断仍按 shared execution 处理。
- Staking map 响应的最大质押量、赎回期类型在已知 schema 与示例间有历史不一致。redeem_amount 的可用余额语义未取得独立充分证据，需留为未验证；没有据此新增“已确认资金错误”。

## 6. 实际验证、工具结果解释与限制

| ID | 实际执行 / 层级 | 结果 |
|---|---|---|
| E01 | Git SSH 取 MR ref、两次核对来源；初始/最新 merge-tree | head 相同；两次无冲突；最终合并树已独立保存检查 |
| E02 | 目标 19 Markdown + 六共享依赖；静态格式/本地链接/锚点/英文/公开内容扫描 | C1/C6/C7 未出现机器错误；公开内容扫描零命中，另经全文人工检查 |
| E03 | 初始基线 checker 查基线 Earn 与 MR Earn | 基线 PASS；MR FAIL C2=3/C4=33 |
| E04 | 初始六包构建基线与 MR | 两者均首先在相同 Stock 问题失败，不是 MR 独有；最终目录均不存在 |
| E05 | 初始版 builder 诊断只取 earn profile，命令规则不减弱 | 基线 Earn 单包 PASS，MR Earn FAIL；没有据此宣称六包通过 |
| E06 | 最终基线更新后，按新 checker 重跑基线与真实合并树 Earn | 基线 PASS；合并树 FAIL C2=3/C4=33 |
| E07 | 最终 builder 原生 `profiles=['earn']`，保持完整原契约 | 基线 Earn 单包 PASS；合并树 Earn FAIL，无产物 |
| E08 | 最终六包构建，分别检查基线与合并树 | 都在同一 Stock 错误失败，无产物，无 staging 遗留 |
| E09 | 临时诊断契约仅采用 Milo 确认的 40 动作并补 aggregation profile；使用最新 checker | FAIL C2=2/C4=23。不是正式修复、未写回仓库；用于排除旧范围误报 |
| E10 | 独立 CLI 注册/handler、SDK 字段和嵌套 JSON 对照 | 新增 8 叶子存在；pledge/redeem JSON 和 register flags 有证据；实际返回字段见 F2 |

最终 E07 使用可信工具的 `build(source, output, full_contract, profiles=['earn'])`，没有屏蔽 Earn 验证。初始 E05 是因旧 builder 尚无选 profile 参数，临时把 profiles 缩为 earn，但保留原全部命令；两种办法都没有获得 MR 的成功构建。

可重复入口（目录占位需要替换；必须保留前述沙箱与资源边界）：

```text
# 源码与独立契约对照，不执行文档里的业务命令。
python -I <checker>/scripts/cex_skills.py check --target <tree>/skills/gate-cex-earn --contract <base>/tests/cex/cli-contract.json
# 全六包对照：本次基线和合并树都因已存在的 Stock 问题失败。
python -I <checker>/scripts/cex_skills.py build --source <tree> --output <new-directory> --contract <base>/tests/cex/cli-contract.json
# 新版可信模块支持 profiles=['earn']，用于隔离其他产品已存在错误。
cex_skills.build(source, output, full_contract, profiles=['earn'])
```

机器结果需校正：C2 对 aggregation 的旧 profile 限制属于 F1 的同步问题；CandyDrop 表中的 MCP 映射、aggregation 的“禁止 MCP”文字会触发 CLI-only 正则，**不能由此宣称 MR 实际调用了 MCP 兜底**。旧契约中的 21 个 missing 已按用户要求排除，新增命令的 unknown 也不代表命令不存在。诊断契约下余下 23 项 C4 包括 canonical 章节、flag 表/类型/缺省和 API 行；它们按一个同步根因归并为 F1，不拆成 23 个生产缺陷。

### 场景审查（仅静态推演，没有真实 Agent 轨迹）

| 场景 | 预期/核对 | 结果边界 |
|---|---|---|
| Uni 正常 lend/redeem；lend 缺 min_rate | 保留产品利率单位、所需参数，缺项不写入 | 关键原约束仍在；未发送请求 |
| Fixed 申购/提前赎回/复投 | 精确产品/订单；接受不等于释放资金；复投需持续授权 | 文本约束保留；未验证真实结算 |
| Staking 多 pid、多输入币、side0/1、未知结果 | 明确选择；不反向补偿；无身份/权限则停 | 类型/门禁已核；fresh confirmation 冲突 F3 |
| Dual APY、可能换币结算与复投 | 报价收益与实际收益区分；不承诺返还原币 | 静态说明与模型/例子匹配；无交易 |
| Auto-invest orders 缺 plan/record ID | 两 ID 必须明确；不调用已排除 plan 能力 | 注册 required 与文档一致 |
| MCL fixed 缺 rate/term、逐币还款失败 | 不降级 current、不自动加抵押、不整批重放 | 原规则保留；无清算/还款测试 |
| Launchpool 项目/池匹配、未知赎回 | 保留 pid/rid/amount；匹配不到记录为未知，不重复写 | 只查契约；记录是否足以唯一匹配未实盘验证 |
| CandyDrop 正常/拒绝/丢响应 | 一次注册；不自动完成任务；不恢复已排除进度接口；不虚构参与状态 | fields/确认问题 F2/F3；无真实报名 |
| 跨产品分组与统一聚合；某产品失败 | 分清口径，保留 partial，不伪造总额 | 路由冲突 F4 |
| 已有授权、超额/过期/换账户、恶意任务文字 | 只复用有效授权；超范围无写入；外部文字不能授权 | 共享规则保留；行为验证未运行 |

本 MR 不修改代码，因此没有编写或运行新的产品单元/E2E 测试。以上是实际文档检查/构建与静态契约核验，不以历史 Dev 只读成功记录替代本次运行，也不以构建成功证明资金业务完成。

## 7. 基线问题、交付与复审门槛

**基线已有、非 !213 引入：** 最终基线与合并树的六包构建均在 trade 阶段报 `stock market fee-rate` canonical command/operation ID 重复，以及 `stock account transactions` 不在导出。当前 MR 没改这些文件。这里只记录对全六包验收的阻塞，未擅自修复，也未列入 !213 的五项问题。它不影响已单独证实的“基线 Earn 可构建、MR Earn 不可构建”结论。

复审顺序：在保留用户确认裁剪范围的前提下同步契约/标准章节 → 修正实际输出字段和授权/聚合歧义 → 清理不符合规则的发布说明 → 单 Earn source/package/build 检查通过 → 基线 Stock 问题解决后补六包检查。安装包尚未成功生成，真实后端和 Agent 行为均保留未验证状态。

报告是本次唯一正式交付物，按工作区要求精确提交到当前本地分支，不自动 push。不改 MR、CLI、SDK、其他工作树或已有安装包；临时副本、诊断契约、venv、构建产物和调试输出在交付前清理。没有新增配置项。
