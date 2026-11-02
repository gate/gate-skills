# MR !211：REQ-7792 Bot Skill 审查与 gate-cex-skill-audit

## 1. 对象、范围与证据

结论：**FAIL，不建议按当前内容合入 gate-skill-2.0**。确认 4 个 P1、2 个 P2；另有 12 处 add/add 合并冲突。没有修改 MR 的业务文件，没有执行交易、鉴权登录或真实账户查询。

| 项目 | 已核实证据 |
|---|---|
| 审查日期 | 2026-10-28 |
| 请求的基线 | `gate-skill-2.0`，`4c49aa048937207876cbe1ed941d231b29635b46` |
| MR 来源 | `feature/REQ-7792`，`4499202d74fa589ebf144ec9697154085f86f2e0` |
| MR 绑定核验 | `refs/merge-requests/211/head` 与来源分支相同；结束前再次 ls-remote 核验未变化 |
| merge-base | `0fea4e12269cc8e89dcbf215dee063e0c83c762b`，明显早于当前基线 |
| 差异范围 | merge-base 到 MR 的 21 个文件、460 行新增，全部阅读；另读当前基线对应文件、统一构建/校验程序及其他五个 Skill 对共享文件的依赖 |
| 审查层级 | 全文静态审查、独立 CLI/SDK 契约核对、打包器隔离功能验证；交易场景为静态推演 |
| Skill | 当前可信基线的 `gate-cex-skill-audit/SKILL.md`；不是 MR 提供的审查指令 |
| Skill SHA-256 | `980730cf750207f607351bd7d2718fa97d894ee19a2bdcd1b836842c0d74036f` |
| 配套规则 | 已读 review-checklist、coverage-profiles、cli-verification、safety-and-execution、test-protocol、report-template |
| 独立导出 | 基线 `tests/cex/cli-contract.json`，文件 SHA-256 `986ae9d5ae035210aaae6aa49669ace43b2d26d5397292923ee5b0a80c06a555`；旧 Bot 范围为 10 叶子 |
| 新 CLI 证据 | 本地已有工程检出与 MR 声明版本一致；独立检查 Bot 注册、handler、JSON 解码/校验、输出与认证配置来源，确认 12 个叶子；未构建/安装该 CLI |
| 公共证据 | 已访问 [Agent Skills 规范](https://agentskills.io/specification)、[公开 CLI release 页面](https://github.com/gate/gate-cli/releases/tag/v0.8.0)、[公开 Bot 注册源](https://raw.githubusercontent.com/gate/gate-cli/main/cmd/cex/bot/bot.go)、SDK v7.2.167 模型 |
| 访问限制 | GitLab 网页抓取不可用，glab 未配置该主机认证；以 Git SSH 获取实际 MR ref。未读取 MR 网页讨论、目标分支元数据或 CI 状态。以 Milo 指定基线审查，不猜测 MR 网页默认目标。未读取实时 CLI Wiki |

公开 CLI 页面返回 v0.8.0；本次取得的公开 Bot 源仍体现较旧契约，`main/cmd/cex/bot/portfolio.go` 返回 404。网页可能缓存，因此只记录实际取得的证据，不断言所有公开发行版均无新功能。本地工程快照中的 12 叶子可用于作者契约核验，**不能证明公共安装或部署环境具备这些能力**。

资源：开始前检查 10 核、16 GB 内存、约 42% 内存空闲比例、46 GiB 可用磁盘；本次仅静态解析和小型 Python 子进程，临时目录峰值约 18 MB。目标测试串行；每个子进程 30 秒以内，单次场景 120 秒以内、输出限制 1 MiB，无 Go 全仓构建。沙箱禁止网络连接、用户主目录读取及临时根外写入；三项实际拒绝均验证。使用空环境和临时 HOME，未读取真实凭据。

### 基线整合口径

`git merge-tree --write-tree --name-only <base> <head>` 返回退出码 1，12 处冲突：六个共享文件，以及 Bot 的 SKILL、bot-lifecycle、bot-workflows、futures-grid、martingale、spot-grid 文档。

不存在可直接测试的无冲突合并结果。本次分别验证：

1. MR 独立树，代表作者分支自身。
2. 当前基线，作为对照。
3. **假设冲突文件选择 MR 版本、其他基线文件保留的覆盖副本**，用于复现整合风险。它不是实际合并结果，不代表所有冲突解决策略都会失败。

## 2. 九维结论

| ID | 维度 | 状态 | 证据与限制 |
|---|---|---|---|
| C1 | Agent Skills 格式 | PASS | Bot 与迁移入口名称/目录一致，YAML frontmatter 有效；说明长度符合规范 |
| C2 | Gate 架构与文件约定 | FAIL | 通用共享规则变为 Bot 专用；新构建器与基线模型文件及 manifest 契约冲突；F2/F3 |
| C3 | 业务线与实质完整性 | REQUIRES_REVIEW | 八产品与生命周期均有可达参考；旧模型说明在 MR 独立树缺失、整合后成为未引用文件；部分后端语义未独立验证 |
| C4 | CLI 完整性与正确性 | FAIL | 12 个叶子名称/新 flags 与工程源码吻合；共享成功响应规则与非 Bot CLI 冲突；F2。正式公共发行可用性未建立 |
| C5 | CLI 说明清晰度 | FAIL | 新产品金额/权重/退出方式有说明，但通用结果判定和账户识别退化；F1/F2 |
| C6 | 引用和内容完整性 | FAIL | 原始包本地链接通过；开发来源重新进入安装内容，公开内容检查被绕开；F4。坏链接失败留下半包；F5 |
| C7 | 英文与术语 | PASS | 全部 19 个 Markdown 文件已读；无中文规范性指令，无需本地化例外；未发现需独立上报的语法问题 |
| C8 | 资金、授权与隐私 | FAIL | 实际 UID 校验缺失、固定再次确认和公开分发限制退化；F1/F4/F6。未知写入不重放、保留原 ID 等规则仍保留 |
| C9 | 可执行内容 | FAIL | 2 个 Python 文件 AST 解析通过、4 个原有测试通过；新增负向复现发现整合拒绝、污染接受和失败残留；F3/F4/F5 |

司法辖区及服务实体法律适用性：**NOT_EVALUATED**。此报告不是生产发布、市场准入或法律合规证明。

## 3. 文件与业务覆盖

所有路径相对项目根；本节逐项覆盖本次 21 个变更文件。行号以下均指 MR head，而非当前基线。

| 文件/能力 | 实际内容和证据 | 结果 |
|---|---|---|
| `skills/gate-cex-bot/SKILL.md` | 入口、七组意图路由、兼容性与场景链接 | 路由齐全；开发快照依赖见 F4 |
| `references/spot-grid-commands.md` | spot/margin/infinite 三叶子、JSON 字段、推荐映射、存量退出规则 | 金额字符串/整数/布尔类型核对；自然语言间距映射及产品退出行为仍需后端证据 |
| `references/futures-grid-commands.md` | futures grid、方向词汇、杠杆、推荐映射 | CLI 路径、JSON 类型吻合；默认方向和间距含义未用真实后端验证 |
| `references/martingale-commands.md` | spot/contract、追加次数、周期止损、固定价格及价格依据 | 新 CLI 校验固定价与依据成对；完整阶梯预算算法未独立验证 |
| `references/smart-position-commands.md` | 组合权重、period/threshold、三种停止模式 | 对应公开 SDK 创建/停止模型；枚举组合与 CLI 校验吻合；真实停止原子性/重试断言未验证 |
| `references/futures-combo-commands.md` | 双向腿、权重/杠杆、可空保护、恢复与结算 | 对应公开 SDK 和 CLI；业务范围限制及资金结算未做真实验收 |
| `references/bot-lifecycle-commands.md` | running/detail/stop；八类型、部分仓位、保存配置、pending | 不虚构零、不重放保留；page-size 50 是目标业务声明，CLI 注册本身不证明服务上限 |
| `references/bot-workflows.md` | 推荐、排除上个候选、手工/推荐转换、创建与停止 | 新排除 flag 存在；仅 market/type 工作流为明确范围收窄，不把 legacy APR/drawdown 排除误报为漏写命令 |
| `references/compatibility.md` | 12 叶子、开发来源、环境与发布边界 | 新能力非凭空捏造；不得用工程来源替代公共安装路径，F4 |
| `references/scenarios.md` | 14 个验收场景要求 | 属于设计清单；未把清单当成已执行用例或实际交易轨迹 |
| `README.md` | 独立 QA 构建方式与候选用途 | 本次能够运行作者分支构建；基线整合失败，F3 |
| `CHANGELOG.md` | 开发候选、SDK/CLI 固定版本及 QA 状态 | 工程过程/中间状态应移出面向用户版本说明；与 F4 同一发布内容修正一起处理 |
| `skills/_shared/cex/preflight.md` | profile/env、Bot help、按需认证 | 缺少强制有效 UID/来源核验，F1 |
| `skills/_shared/cex/cli-auth.md` | key/env、Bot scope、冲突凭据建议 | 不能替代实际身份读取，F1；Bot 特例应归 Bot |
| `skills/_shared/cex/execution-cli.md` | Bot JSON、统一 code=200、一次写入 | 六个 Skill 共用导致输出误判，F2 |
| `skills/_shared/cex/safety.md` | 草稿、下一轮确认、不重放 | 固定重复确认取代可验证已有授权，F6 |
| `skills/_shared/cex/templates.md` | Bot 草稿和结果 | 应保留通用模板，Bot 字段局部扩展；F2/F6 |
| `skills/_shared/cex/cli-setup.md` | 校验和、回退二进制、开发版本 | 原公共项目链接/安装细节被简化，开发来源边界需修复；F4 |
| `migrations/gate-exchange-bot/SKILL.md` | 仅迁移指引、不转交授权或自动执行 | 静态 PASS；不属于新的业务执行入口 |
| `scripts/build_cex_bot.py` | 文件白名单、复制、链接检查、manifest | 静态与隔离执行完成；F3/F4/F5 |
| `tests/test_build_cex_bot.py` | 可复现、已有目录、缺共享规则、符号链接 | 4 个测试通过；未覆盖本次补充发现 |

前十二项中未带目录前缀的文件均位于 `skills/gate-cex-bot/`。基线还包含 `references/models/{bot-lifecycle,futures-grid,martingale,spot-grid}.md`，MR 没有迁移或更新这些文件与统一契约。

## 4. 独立 CLI 对照

工程源码独立枚举为 **12 个业务叶子**，MR 中能找到 **12 个叶子的名称或模板**。此数字仅表示路径提及覆盖，不能当作 12/12 参数、身份、部署或业务语义均正确。基线导出仍为 10 个叶子；新增两个不能因为旧导出未收录就判定为不存在。

| `gate-cli cex bot` 后的叶子 | 核对内容 | 文档位置/结论 |
|---|---|---|
| `recommend` | market/type/scene/refresh-context/exclude；handler 要求认证 | workflows；新排除 flag 与工程注册吻合，推荐仍是私有请求 |
| `running` | market/type/page/page-size；认证；集合结果 | lifecycle；缺省值来自 CLI，服务端最大页待验证 |
| `detail` | strategy-id 与 strategy-type 必需；认证 | lifecycle；保存配置与执行完成明确区分 |
| `stop` | id/type；smart_position 必选 mode；limit 必有 price/expiration；其他类型禁止 options | lifecycle/smart-position/combo；与工程验证器吻合 |
| `grid spot` | 必需 json；strategy_type/market/create_params | spot-grid；主要字段类型吻合 |
| `grid margin` | 必需 json；leverage 字符串 | spot-grid；主要字段类型吻合 |
| `grid infinite` | 必需 json；money/price_floor/profit_per_grid | spot-grid；不强要普通网格参数正确 |
| `grid futures` | 必需 json；direction 及 leverage | futures-grid；主要类型吻合 |
| `martingale spot` | 必需 json；stop_loss_per_cycle；无固定价保护字段 | martingale；不把固定价静默换算成比率 |
| `martingale contract` | 必需 json；stop_loss_price 与 price_type 成对；last/index/mark | martingale；新校验和文档吻合 |
| `smart-position create` | 必需 json；strategy_type；period XOR threshold | smart-position；类型和停止 options 见公开模型 |
| `futures-combo create` | 必需 json；整数杠杆；period XOR threshold | futures-combo；nullable 保护字段与 SDK 指针字段吻合 |

公开模型：[Smart-position 创建参数](https://raw.githubusercontent.com/gate/gateapi-go/v7.2.167/model_ai_hub_rebalance_create_params.go)、[Futures-combo 创建参数](https://raw.githubusercontent.com/gate/gateapi-go/v7.2.167/model_ai_hub_futures_combo_create_params.go)。其他格网、马丁、停止选项与订单模型由本地同版本 SDK 核对。SDK 可序列化某个值不等于后端允许该值。

`--version` 与 `version` 均在独立 CLI 根注册存在，没有把该差异当作错误。示例中的 `<...>` 是语法占位，不是已执行 argv。无 MCP/HTTP 业务兜底调用被实际执行；否定 MCP 的文字不能按关键词视作存在兜底。

## 5. 确认的问题

### F1 · P1 · C8：恢复执行前对有效账户 UID 的强制核验

- 位置：`skills/_shared/cex/preflight.md:3`，关联 `cli-auth.md:3-5`。
- 置信度：高；静态控制流与独立 CLI 配置源码相互印证。
- 触发：已存在可用凭据，Agent 记录用户选定 profile 后进入业务路径。新 preflight 仅在凭据缺失/冲突时加载认证说明；没有读取有效 UID、比较授权目标、身份不明时拒绝私有写入的要求。
- 证据：基线明确要求同一 endpoint 读取有效身份，说明环境凭据优先于 profile、完整 HMAC 优先于 OAuth。独立 CLI 的 `internal/config/config.go:141-155` 确认环境/flag 覆盖。有效但属于另一账户的凭据可以通过服务器认证，服务器不能替 Agent 判断它是否是用户授权的目标。
- 后果：用户确认的是账户 A 的草稿，实际用账户 B 的现存有效 key 发出创建/停止；仅展示 profile 和再次确认不能建立身份绑定。没有声称已发生真实错账户交易。
- 修正：保留共享的有效凭据/endpoint/UID 门禁及“无法验证则停止”规则，Bot scope 说明作为产品补充。不要读取/输出密钥值来诊断。
- 复验：合成 profile A + 环境 key B、OAuth A + HMAC B、身份接口不可用三场景；在目标身份不符或未知时断言业务写入计数为零。

### F2 · P1 · C4/C5：不要把 Bot 响应封装设为所有 CEX 命令的成功条件

- 位置：`skills/_shared/cex/execution-cli.md:5`，关联 preflight/templates 的 Bot 专用化。
- 置信度：高。
- 触发：其他五个 Skill 继续加载同一路径的共享 execution 文件，执行正常现货下单或对象/数组查询。
- 证据：新规则无条件要求 `code=200` 与 data。独立 CLI `cmd/cex/spot/order.go:193-218` 成功时直接打印 SDK `Order`；SDK 订单是含 id/status 等字段的对象，不含该 Bot envelope。基线明确“没有通用 success envelope”。
- 后果：合法返回被标为未验证/失败，后续验证与用户结果说明失真；Bot 所需 code/data 规则污染其他业务。没有把“不重放”规则曲解为它会自动重下单。
- 修正：恢复通用的“按具体产品实际输出判定”；Bot envelope、Bot help 和 Bot 专用字段放在 Bot 引用内。保留原有限时、有限分页、JSON 与最大输出约束。
- 复验：分别使用普通订单对象、资产数组、Bot code200、Bot code200 pending、Bot 业务拒绝的合成输出；前三者按各自契约读取，pending 不作完成、拒绝不作成功。

### F3 · P1 · C2/C9：先整合 gate-skill-2.0 的模型、契约与统一构建入口

- 位置：`scripts/build_cex_bot.py:65-71`；关联整个 Bot 文档变更和 `tests/test_build_cex_bot.py:55-63`。
- 置信度：高；实际复现。
- 触发：在当前基线保留已有模型文件，并按 MR 更新同名文档后，执行新构建器。
- 实测：新白名单拒绝四个 `references/models/*.md`，退出 1；MR 独立树可以构建 18 个内容文件，但该成功没有涵盖指定基线。
- 额外证据：原统一 source checker 在基线 Bot 上 PASS；MR/覆盖副本出现 C2=6、C4=10，安装包再增加 manifest 契约不符。旧机器检查的 10 个“undocumented”指 canonical 章节/参数表格式丢失，**不是声称文章完全没提到这 10 个命令**。新增产品旧 profile 未收录必须更新契约，不应删产品来迎合旧表。
- 后果：指定基线无法按作者入口构建；原六包流水线也拒绝覆盖副本。单独增加另一套构建/manifest 规则绕不开此整合责任。
- 修正：先解决 12 处冲突，保留通用规则；将八产品纳入既有独立契约、模型说明、统一构建与检查入口。明确模型保留或等价迁移，并同步受影响测试。
- 复验：真实解决冲突的分支上运行六包构建、六包独立安装检查、旧/新 Bot 命令契约和新增两产品验证。不能仅测试 MR 自身旧基底。

### F4 · P1 · C6/C8：公开分发限制被新的打包路径绕开

- 位置：`scripts/build_cex_bot.py:33-36,84-90`；实际内容 `skills/gate-cex-bot/references/compatibility.md:3` 和 `SKILL.md:8`。
- 置信度：高；实际内容与负向构建均核实。
- 触发：直接使用 README 指向的新构建器生成安装包。
- 证据：新构建只验证局部 Markdown 链接，对任何外部 scheme/netloc 直接跳过，不运行基线的 public dependency 检查。安装内容重新要求固定开发分支/CLI revision，manifest 写入工程来源和 QA 状态；部分产品文档还包含后台分配/调度与写入竞争等工程细节。
- 实测：在临时副本追加一个保留域名链接和文档用 IP（均为合成数据），构建仍 exit 0，生成 manifest 并完整复制污染内容。没有联网访问该域名/IP。
- 后果：绕过本分支刚建立的公开内容门禁，后续误放的内部地址/引用能够进入可安装目录。QA/development 标签不改变文件仍被打包的事实。
- 修正：复用原统一公开内容检查，校验所有 Markdown/JSON/manifest；工程来源、QA/中间状态留在工程证据，运行时只给公共项目入口和实际能力检查。CHANGELOG 按用户规则只保留接口及参数变化。
- 复验：实际公开包无固定开发来源依赖；合成内部引用、编码引用及凭据形态在 source/package/manifest 均被拒绝且不回显敏感值。
- 限定：本次 **未发现真实密钥、token 或实际内部服务地址明文**；当前确认的是开发来源/工程内容重新入包和门禁缺失，不能写成已泄露可用凭据。公开 SDK 版本本身不是秘密。

### F5 · P2 · C9：链接校验失败后应清理未发布产物

- 位置：`scripts/build_cex_bot.py:72-84`。
- 置信度：高；实际复现。
- 触发：白名单文件含失效相对链接，复制完成后 `validate_links()` 抛错。
- 实测：exit 1，但输出目录仍有 SKILL、引用和共享规则，共 18 个文件，没有 manifest；再次对同一路径构建被“目录已存在”拒绝。
- 后果：失败产物仍是可被发现的 Skill 目录，且阻塞原路径重试；用户难以区分完整发布与半包。
- 修正：复用基线“临时目录校验完成后一次发布，失败 finally 清理”的实现，不覆盖用户原有输出。
- 复验：坏链接/坏锚点/复制失败不产生最终输出、不遗留 staging；既有目录保持不变；修复输入后同一路径可成功构建。

### F6 · P2 · C8：不要强制已有完整授权的用户下一轮再次确认

- 位置：`skills/_shared/cex/safety.md:3`；关联 `templates.md:10`、`bot-workflows.md:14` 与 smart-position 停止说明。
- 置信度：高；规则直接矛盾，行为场景未运行 Agent。
- 触发：用户已明确给定并授权同一 UID、环境、产品、参数、额度、期限内的一次操作，或有可验证的有效已有授权。
- 证据：新规则要求 every create/stop 都等待 immediately following user turn，并使不相关回复自动使草稿失效。基线与 auditor 核心回归明确允许复用有效且完整的 scoped authorization。
- 后果：已授权操作被不必要阻塞，跨业务共享协议不一致；增加一轮聊天也不能修复 F1 的身份问题。
- 修正：保留对未知、过期、超范围或变更参数的澄清；完整授权可复用，不设置固定词或固定下一轮规则。
- 复验：完整已有授权不重复索批；额度、账户、环境、参数、期限改变后，在重新取得有效授权前无写入。

## 6. 可执行与场景证据

先逐行阅读两个 Python 文件，再做 AST 解析，最后在 macOS sandbox-exec 中运行。`env -i`、临时 HOME/TMPDIR、网络连接拒绝、用户主目录读取拒绝、临时根外写入拒绝均实际验证。初始隔离探针仅创建 socket，不足以证明网络连接被拒绝；已改成实际 connect 并确认 PermissionError，随后才运行补充检查。没有把单纯清空环境当成完整沙箱。

| ID / 层级 | 前置/执行及预期 | 实际结果 |
|---|---|---|
| E01 / 静态 | 两 Python 文件 `ast.parse` | PASS；不是功能验证替代 |
| E02 / 隔离功能 | `python -I tests/test_build_cex_bot.py -v`；包含原有可复现/保留已有目录/缺规则/根目录及父目录 symlink 四项 | 4 tests，0 failures，0.966 s；真实运行 subprocess |
| E03 / 隔离功能 | MR 原树 `scripts/build_cex_bot.py --output <new>` | exit 0；18 内容文件+manifest；无远程执行 |
| E04 / 隔离功能 | 基线+MR 覆盖副本，保留基线模型；同入口构建 | exit 1；准确报四个模型文件不在白名单；F3 |
| E05 / 隔离负向 | SKILL.md 追加缺失本地链接；预期拒绝且无最终输出 | 拒绝但 18 文件留存、无 manifest；F5 |
| E06 / 隔离负向 | SKILL.md 追加合成保留域名链接和文档 IP；预期公开内容门禁拒绝 | exit 0、有 manifest、污染文本保留；F4 |
| E07 / 隔离对照 | 基线 checker：`cex_skills.py check --target <base-bot> --contract <base-contract>` | PASS |
| E08 / 隔离整合 | 同 checker 查 MR 和覆盖副本；另查规范目录名安装包并加 `--package` | source 均 FAIL：C2=6/C4=10；package 另 C6=1；见下方解释 |
| E09 / 隔离构建 | 基线 `cex_skills.py build --source <base> --output <new> --contract <base-contract>` | PASS，六包完整构建及内置检查通过 |
| E10 / 隔离构建 | 同入口构建覆盖副本 | FAIL，首个 trade 在共享文件检查被拒绝；最终输出不存在，staging 0 |
| S01 / 静态推演 | 八种手工创建；字段类型/required 与独立注册、SDK 对照；不执行业务 argv | 路径/主要类型吻合；未验证真实 Agent 参数补全顺序及交易 |
| S02 / 静态推演 | 新推荐排除/刷新 ID 与上下文；禁止伪造候选与自动扩大筛选 | 新 flag 注册吻合；后台排除先于排序未验证 |
| S03 / 静态推演 | smart-position 三模式及 limit options，contract 固定止损成对 | CLI 分支吻合；持久化、竞争、到期不转市价等后端行为未运行 |
| S04 / 静态推演 | code200 pending、超时/丢响应、残余持仓；禁止重建/重复转账 | 目标规则保留原 ID、不重放；非 Bot envelope 见 F2；无真实事件轨迹 |
| S05 / 静态推演 | 选定 profile 与有效 UID 不一致、身份不可读 | 门禁缺口 F1；未操作真实凭据 |
| S06 / 静态推演 | 已有完整授权 vs 账户/额度/期限变更 | 固定再次确认冲突 F6；无 Agent 运行记录 |

**机器输出的人工校正：**

- C2 中两个新产品不在旧 profile：契约更新缺口，不证明新 CLI 不存在。
- C2 中四处 CLI-only 命中来自 MCP/内部头的否定说明或来源描述，不能把否定文字误报成主动执行 MCP。E10 的直接阻塞也是这种现有检查器兼容问题，仍须整合，但不是已发现新 MCP 业务调用。
- C4=10 表示旧 canonical 章节/操作标识/参数表约定未保留，不是 10 个路径全都缺失；已另外人工建立 12 叶子矩阵。
- 原机器 public-dependency 正则没有识别本次所有开发来源写法。F4 来自全文审查与独立污染复现，没有因为机器未命中而通过。
- MR `scenarios.md` 的 14 项没有可执行交易轨迹；本次没有重新运行其声称的历史 authenticated read、数据库写入或真实资金验收。

本次未修改产品代码，未新增实现测试；执行了 MR 自带正式打包测试及独立补充复现。没有跑无关 Go/Java 全量构建、vet/race，也没有把 AST/模拟结果写成后端集成通过。

### 可复验方式

使用上述固定 revisions 分别准备只含本次输入的临时副本；目标脚本必须先检查后执行，保留本报告沙箱限制。以下是所执行入口的参数形式，`<...>` 替换为隔离目录，不是 shell 可直接执行的字面占位。

```text
# 原 MR 正式测试；必须置于前述 sandbox-exec 与空环境中。
python -I <mr>/tests/test_build_cex_bot.py -v
# 分别在 MR 树和保留模型的覆盖副本运行。
python -I <repo>/scripts/build_cex_bot.py --output <new-output>
# 使用可信基线的检查器，依赖固定为 requirements-cex.txt 中的版本。
python -I <base>/scripts/cex_skills.py check --target <skill> --contract <base>/tests/cex/cli-contract.json
python -I <base>/scripts/cex_skills.py check --target <installed/gate-cex-bot> --package --contract <base>/tests/cex/cli-contract.json
python -I <base>/scripts/cex_skills.py build --source <repo> --output <new-output> --contract <base>/tests/cex/cli-contract.json
```

负向 fixture 只改临时副本：坏链接为 `[Missing reference](references/missing.md)`；污染为保留测试域名链接和文档用 IP，不含真实秘密或真实内部服务。分别断言退出码、是否发布输出、manifest 存在性、残留文件集合；补充测试揭示的是缺陷，不是“全部测试通过”。

## 7. 交付与复审门槛

本次为审查，不修改 MR 实现、不替用户解决冲突或发布候选包。必修顺序：恢复通用身份/输出/授权规则；将八产品更新接入基线契约和统一构建；恢复公共内容门禁；保证失败不留半包。六项修正后，复审真实解决冲突的完整分支，而不是重复审查当前独立旧基底。

仍待验证：公共安装的新能力、真实后端参数边界、网格间距/默认方向、保存保护与退出行为、并发停止/恢复、资金最终结算；本次没有可供宣称通过的实盘或 Agent 行为轨迹。真实资金测试必须另有明确范围与环境。

报告是唯一保留交付物；临时检出副本、venv、合成 fixture、隔离构建包和调试输出在交付前清理。它不进入六个运行时安装包。本次报告按工作区要求精确提交到当前分支，不自动推送。
