# gate-skill-2.0 项目与 CEX Skill 全量复审

审查日期：2026-11-03（Asia/Shanghai）。冻结版本：`bb6a3f7f9857a6e343190581d830b7c12804645f`。审查结束前远端分支仍为该版本。

**结论：FAIL，建议修正后复审。确认 10 项问题：6 项 P1、4 项 P2。** 其中 CEX 业务正文问题 1 项，项目构建/通用测试工具问题 6 项，规则与安装文档问题 3 项。没有据此认定已发生真实资金损失或凭据泄露。此次为整个快照的存量审查，不将所有问题归因于最近一次提交。

## 1. 意图、范围与证据

目标是确认当前项目的入口、开发/审计规则、脚本、测试、安装说明及六个 CEX 包是否一致、可用且具备合理安全边界。用户要求 `skills/` 下非 CEX 内容忽略，因此：

- 纳入 219 个 Git 文件，合计 5,950,028 字节；包含六个 CEX 目录 107 个文件、专属共享规则 6 个文件，以及分流文件的 CEX 相关条款。
- `skills/` 下其他目录与文件共 275 个不作业务内容审查，包括 CLI/MCP 安装器实现、Pay、DEX、Info/News。用户排除的 18 份规则副本不审、不改。根测试套件中已有安装器集成回归照常运行，不据此声称完成了安装器内容审查。
- 根 `test-for-skill/`、`.cursor/skills/` 属于项目开发工具，纳入审查；不因其中出现 MCP 就认定六个 CEX 有 MCP 依赖。
- 25 个历史审查/证据文件保留为历史材料，只做清单、解析与来源核对，不把其引用的旧问题当成当前生效规则。15 张安装图片均查看；项目外的 Gate CLI 仓库不作代码审查。
- 对文本执行逐文件读取、Markdown/JSON/Python 解析、CEX 全量结构/动作/参数/模型链接检查；人工重点走查六个入口、共享规则、全部业务工作流、产品专属约束、运行脚本和项目工具的正常/失败链路。机械生成的 SDK 字段表依赖工程契约进行静态对照，未逐项重新证明全部后端响应字段。
- 本轮只读审查，另在独立分支留存报告。没有修改业务源码、用户工作区或安装状态，没有交易、账户配置、付费模型调用，也没有 push。

执行使用当前仓库 `gate-cex-skill-audit`、本机 `code-review`，并对唯一 64 行 Go 注册导出器使用 `go-cr` 的微型单文件流程。按用户全量范围覆盖存量，覆盖范围优先于技能默认的 diff-only 审查。未创建技术方案或实施修复。

正式证据：

- [文件、35 份产品引用、379 条命令与源/包对照清单](2026-11-03-project-cex-full-review-evidence/audit-evidence.json)
- [隔离复现结果](2026-11-03-project-cex-full-review-evidence/probe-results.json)
- [执行与外部来源记录](2026-11-03-project-cex-full-review-evidence/verification.json)

### 基线和来源

采用当前分支已接受范围：Earn 的五个保留产品与既有裁剪、Trade 固定公共 GET/WS 行情例外、Bot 八类产品及每次创建/单实例停止的下一轮确认规则。不会要求恢复 Launchpool/CandyDrop，也不会把获批公共行情例外报成私有接口绕行。

工程动作基线是 `tests/cex/cli-contract.json`，SHA-256 见证据。它明确说明是保留的编写范围，不是完整当前公开发行版清单。独立覆盖分母来自该契约与审核 profile，而非仅统计 Skill 自述。

公开核查使用 [Agent Skills 规范](https://agentskills.io/specification)、[Gate CLI 项目](https://github.com/gate/gate-cli) 与[公开 Releases](https://github.com/gate/gate-cli/releases)。抓取的公开 `v0.8.0` 树为 `8cb3ef2d92f3447f01c7e302454f6eba0ed6ffb9`；另读取该标签的 Spot order 源码作版本差异样本。未安装/构建 CLI，未验证全部 379 条命令在公开二进制中的可用性；不能把工程契约全绿解释成公开版本全支持。Web 对具体源码页返回 cache miss，后通过保留 TLS 校验的 curl 读取官方 raw/API；Python 默认 CA 校验失败的尝试未绕过证书校验。未读取本轮外部 Wiki 或后台实时 schema。

## 2. 确认问题

### CR-FULL-01 — P1：旧 Fixture 以地址/名称代替写入隔离证明

位置：`test-for-skill/skill-tester/SKILL.md:342`、`:353`；`references/fixture-templates.md:35`、`:127`。

**确信，静态链路。** 规则优先把内网/非标端口、HTTP 或含 test/dev 的 server 名判成测试环境，随后允许自动 Setup → 写操作 → Teardown。故 `test` 命名但实际指向正式账户的连接，或经内网代理访问正式后端的连接，可走入自动写路径；价格偏离 30%、最小数量也不能证明不会成交。Fixture 还会自动构建反向平仓/状态恢复，这些都是另一次真实写入。

六个新 CEX 已有前置分流，**此问题不等于它们仍使用旧 Fixture**；风险位于保留通用框架的其他可写目标。当前上层“服从用户授权”约束能限制执行，但该环境判定本身仍错误，不能作为真实写入的安全门禁。

最小修正：默认只在可强制隔离的合成依赖中运行 Fixture；真实集成必须核实端点、账户、权限、数据和每项 Setup/Execute/Teardown 的授权。地址/名称只作线索，不能自动授予写入。同步两处表格及 execution-guide 的引用。

验证：加入正式端点但 server 名含 test、内网代理正式账户、HTTP 正式代理、隔离证据缺失及明确合成环境的用例；前三者必须零真实写事件。此轮仅做规则反例推演，未运行真实写入或另一个模型的执行轨迹。

### CR-FULL-02 — P1：连通性测试默认执行全部未显式 skip 的工具

位置：`test-for-skill/mcp-smoke-test/run_test.py:288`、`:295`、`:301`；schema 发现/调用入口 `:898`、`:946`。

**确信，隔离 E2E 已复现。** 入口获取 live/cached 工具列表，逐个生成参数并调用；唯一阻止条件是具体工具的 `skip` 条目，没有已核实的只读白名单、写操作授权或隔离证明。因此新工具未加入 overrides 时会直接执行；最小金额、名字推断或预期报业务错都不构成无副作用保证。

使用项目正式合成 stdio peer 注册 `fixture_transfer_funds`，没有写入许可或 overrides：真实 runner 完成配置读取 → live schema → 参数生成 → stdio 调用，记录到 `amount="0.0001"` 的工具调用，退出 0。被替换的只是服务端，不曾发生真实转账。

最小修正：默认仅允许有可信语义证明的只读工具，未知/写工具保持跳过；需要写入的验证改走明确隔离且逐项授权的测试入口。不要只补齐当前黑名单。同步 config、overrides 约定、README 与历史回归。

验证：新未知写工具、零参数写工具和未识别语义工具都不能被默认调用；允许的只读工具应继续走完整协议链。单测参数/选择逻辑，E2E 断言服务端实际调用日志。

### CR-FULL-03 — P1：stdio 超时包在阻塞 readline 外，无法生效

位置：`test-for-skill/mcp-smoke-test/run_test.py:130`、`:136`、`:154`、`:170`。

**确信，进程隔离复现。** `_recv()` 使用阻塞 `stdout.readline()`；call/list 外层检查 timeout 无法中断它，initialize 更没有有效期限。对端保持进程和管道开启但不回包时，runner 不会按 timeout 返回，正常 stop 也无法抵达。持续 stderr 未被排空亦会放大挂起风险，但本轮不以其作独立已复现结论。

合成 peer 正常回复 initialize 后忽略工具调用；配置 timeout=0.1 秒，0.8 秒外部守卫触发时仍未返回，观测约 0.807 秒。已终止整个测试进程组并回收，没有留下服务进程。

最小修正：在实际读边界实施单调时钟 deadline，正确处理 EOF/半行/通知消息，并保证 initialize、list、call、异常退出都能取消和回收子进程；集中管理 stdio 与 stderr，不能只再包一层轮询时间判断。

验证：沉默 peer、只发半行、初始化沉默、无匹配 ID、EOF、stderr 持续输出、取消及清理。正常响应仍须能按请求 ID 匹配。

### CR-FULL-04 — P1：通用打包器允许 staging 位于被复制的 Skill 内

位置：`scripts/cex_skills.py:776`、`:777`、`:786`。对照已有保护：`scripts/build_cex_bot.py`。

**确信，临时源副本复现。** `build()` 只拒绝已存在的 output；若新 output 是 `skills/gate-cex-bot/new-output`，staging 先创建在该 Skill 内。空 staging 不被 file_set 的文件校验拒绝，随后 copytree 把包含自己的源目录复制到自身子目录，递归放大 I/O，最终出现 `File name too long`。这不是正常的“拒绝危险路径”，而是复制已经发生后才失败。默认 README 输出路径不触发，但公开 `--output` 接口可达。

以完整 Bot 与六份共享规则的临时副本调用真实 `build(..., profiles=("bot",))`，实际产生递归路径错误；设置 3 秒额外守卫，生产 finally 清理了 staging，最终输出未发布。六包通用入口使用同一实现。专用 Bot 包装器虽有保护，不能保护直接调用通用构建器的入口。

最小修正：在 mkdir/staging/inspect 前统一规范化 source、输入目录和 output，拒绝 output/staging 落入任一被复制输入或其子树，并处理符号链接父路径。复用统一边界，不依赖某一包装器才安全。

验证：六包入口和单包入口覆盖正常外置路径、源 Skill/共享目录内路径、相对路径与符号链接别名、已存在输出；拒绝时断言没有创建目录/复制文件，允许路径仍可完整构建并验包。

### CR-FULL-05 — P1（C4/C5）：Spot 同一正文同时否定和声明账号/自动借还款参数

位置：`skills/gate-cex-trade/references/spot-commands.md:519`、`:521` 对 `:524`、`:526`、`:533`；同文件 buy/get 等参数表及当前工程契约。

**确信，静态语义冲突。** “Account-field limits” 无条件称 buy/sell 不暴露 `--account`、auto-borrow/auto-repay，get/list/cancel 也没有账号选择；紧接的 “Account selection and borrowing” 则明确给出这些参数和账号限制。当前契约也包含这些 flags。代理即使发现兼容已安装 CLI，也可能按旧段落拒绝本应支持的 margin/unified 路径，或得到相互冲突的账号/回查要求；金融任务不能靠任意选一段解释。

六个包的确定性检查全部 PASS，仍把冲突正文原样收入 Trade 包；已确认这是现有检查的语义盲点。没有执行真实订单，也没有证明任意公开版本支持该参数。

最小修正：删除无版本限定的旧否定，保留实际兼容门禁和当前参数规则。可改为：**“Older builds may omit account-selection or automatic borrowing/repayment flags. Verify the installed leaf; when supported, preserve the same explicit account across the order lifecycle.”** 参数表、场景和 checker 的否定契约一起更新，不能仅再追加另一段正确说明。

验证：兼容 CLI 的 spot/margin/unified/cross_margin 正常路径；旧 CLI 缺 flag 时拒绝；账号不一致、越权借款、isolated auto-repay 不支持时拒绝。源文件与包内各检查一次，并增加对旧绝对否定的回归。

### CR-FULL-06 — P1：HTML 报告把响应 label 当成可信 HTML

位置：`test-for-skill/mcp-smoke-test/run_test.py:374`、`:678`、`:679`、`:701`，另有 tool_name/module/server_name 插值出口。

**确信，HTML 生成复现。** `label` 来自服务端响应，进入 display_status 后未经 HTML 转义插入表格。仅对 message/JSON 的尖括号替换不覆盖这个出口。给定合成 `status=500` 和脚本标签 label，生成文件保留原始 script 元素。用户打开此 HTML 时内容可被浏览器当成脚本执行；其具体权限受打开方式/浏览器策略影响，不能推断已能读取任意本地文件。

此轮只检查生成 HTML，**没有在浏览器中执行标签或进行任何外传**。

最小修正：全部不可信字段在各自 HTML 文本/属性出口统一使用正确 escaping 或自动转义模板；可信固定脚本与数据分离。覆盖 label、工具/模块/服务名与 skip/message 等出口，不能只过滤 `<script>` 字符串。

验证：包含尖括号、引号、实体、标签及事件属性的合成响应/名称；HTML 解析断言它们保持文本且不会生成额外可执行节点。正常报告内容、折叠与统计仍须可用。

### CR-FULL-07 — P2：旧对话检查器并未验证其声明的工具调用顺序

位置：`test-for-skill/test_skill.py:136`、`:193`、`:227`。

**确信，替换外部模型边界后复现。** `tools_in_order` 实际使用 `all(t in tool_calls ...)`，只验证存在；模型文本里的标记也不是实际工具调用轨迹。要求 get_quote → create_order，合成响应逆序 create_order → get_quote，仍得到 overall_pass=true。这在旧格式适用目标中也成立，不依赖把当前 CEX 误送入此 runner。

最小修正：至少按定义验证顺序、重复与禁止事件；仅有文本时明确输出“叙述顺序检查”，不得作为已执行业务链路的证明。运行级测试必须来自真实执行器记录事件。

验证：正序、逆序、缺失、重复、额外禁止动作、仅说明未执行等；E2E mock 仅替换模型 API，保留解析、判定、报告和退出码。当前 CEX 继续使用专属协议。

### CR-FULL-08 — P2：独立 auditor 的 bundled profile 没有登记获批公共行情例外

位置：`gate-cex-skill-audit/references/coverage-profiles.md:15`；对照 `skills/gate-cex-trade/references/runtime.md`、`markets.md`、`streams.md` 与 `docs/gate-cex-market-skill-requirements.md`。

**确信，规则对照。** profile 仍无条件禁止 business direct HTTP/SDK；当前批准的 Trade 则允许固定路径、无认证、无重定向的有界公共 GET 和公共 WS helper。独立安装的 auditor 未拿到仓库外新计划时，容易把合法公共行情当成 C2 失败。此轮依据已确认范围裁决，**没有据旧 profile 否定现有例外**。

最小修正：在 bundled profile 和相关 CLI-only 检查说明中精确登记 Trade 的固定公共只读例外、环境/路径/预算限制；私有读和所有写仍只经 CLI。Bot 新增两份产品引用也应与当前 approved mapping 对齐，不能靠推测扩充任意业务。

验证：批准的公共样例不误报；私有 HTTP、任意 origin、凭据或超界路径仍失败。按 auditor AR13 的新已批准范围情形复核；不能只删除“HTTP”安全条款。

### CR-FULL-09 — P2：通用 preflight 指南仍把旧 fallback 规则施加于“所有新 Skill”

位置：`docs/preflight-and-diagnostics.md:7`、`:90`、`:109`。

**确信，适用范围缺失。** 开头规定所有新 Skill 必须运行该 preflight，后面允许输出 `__FALLBACK__` 交给旧 wrapper。CEX 当前规则却要求特定 CLI 能力检查、缺能力停止、无 MCP fallback。维护者照指南新增 CEX 时会重新引入已移除的架构。文档也将过往多个版本样例作为字段稳定性的统一表述，不能代替逐版本核查。

最小修正：明确该指南只适用于声明该诊断/fallback 契约的产品；六个 CEX 指向专属 preflight 与安装/认证规则，禁止 fallback。保留其他产品需要的诊断内容，不整份删除，不擅自停用 Pay 的 Exchange 安装能力。

验证：新增 CEX 文档/流程不产生 MCP fallback；原有适用产品仍能使用其诊断说明。规则检查和开发指南入口同步核对。

### CR-FULL-10 — P2：当前安装说明仍引用旧 Skill 名称与旧路径截图

位置：`README.md:391` 附近及后续安装章节、`README_zh.md:391`、`:421`、`:445`、`:474`、`:478`；图片 `general-install-1/2.png`、`claude-install-1/2.png`、`codex-nl-install-2.png`、`codex-manual-install-3/4.png`。

**确信，15 图视觉检查。** 文字已换成当前产品安装边界，但截图仍显示 gate-market/gate-trading/gate-exchange-market，Claude 图还有 `~/.claude/skills/.claude/` 与旧 install-gate-mcp.sh 路径。图片没有被清楚标为历史示意；用户按图选择/核验会寻找已经移除的入口。图片中普通用户名/文件名未被误报成凭据。

最小修正：重录与当前文字相符的必要图片，或移除失效截图并用当前文本/清单说明；同时修正中英文引用。仅保留实际有用的 UI 图；不需要重建或恢复旧 CEX。

验证：扫描图片引用、人工核对图中文字与真实目录/安装结果；已有 link/anchor 测试继续运行，补充截图内容更新的人工验收记录。图片存在性测试不能证明内容仍正确。

## 3. 六个 CEX 的九维结论

以下是**静态编写/独立包层面**，不是后端联调、LLM 自主执行或上线认证。工程 checker 的 PASS 与 auditor 语义结论分别列出。

| 维度 | Trade | Earn | Assets | Subaccount | Affiliate | Bot | 依据/限制 |
|---|---|---|---|---|---|---|---|
| C1 格式 | PASS | PASS | PASS | PASS | PASS | PASS | 入口 YAML、命名、说明与元数据类型；按公开规范 |
| C2 架构 | PASS | PASS | PASS | PASS | PASS | PASS | 六业务边界、共享源/包内共享、单一写所有者；采用获批 GET/WS 与 Bot 新范围 |
| C3 业务完整性 | PASS | PASS | PASS | PASS | PASS | PASS | 对已批准工程编写范围，35 份产品契约与 6 份工作流齐全可达；不代表任意 API/发行版本全部能力 |
| C4 CLI 正确性 | FAIL | REQUIRES_REVIEW | REQUIRES_REVIEW | REQUIRES_REVIEW | REQUIRES_REVIEW | REQUIRES_REVIEW | Trade 有 CR-FULL-05；其余工程契约一致，全部公开二进制/部署 schema 尚未逐叶核实 |
| C5 解释质量 | FAIL | PASS | PASS | PASS | PASS | PASS | Trade 同文档冲突；其他静态抽核覆盖单位、资金/状态、权限、恢复与产品限制 |
| C6 引用与完整性 | PASS | PASS | PASS | PASS | PASS | PASS | 源/包内依赖与本地锚点检查通过；外部引用非全部在线逐页核实，见来源限制 |
| C7 英文与术语 | PASS | PASS | PASS | PASS | PASS | PASS | 未发现额外规范性中文；有意本地化数据例外单列；CR-FULL-05 的语义冲突计入 C5 |
| C8 资金/授权/隐私 | PASS | PASS | PASS | PASS | PASS | PASS | 静态：无强制 UID 身份查询、私有操作 CLI、未知写不重试、授权边界；非真实安全执行证明 |
| C9 可执行内容 | PASS | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | Trade 三个 Python 文件完成语法/现有合成回归；其他五包无可执行脚本，命令模板已静态检查 |

C4 的公开可用性不确定不抵消已确认问题。即使工程包 checker 全 PASS，整体仍 FAIL。未逐条执行/重新独立证明所有响应字段，因此对该部分保留证据限制。

C7 例外：`skills/gate-cex-trade/references/localized-examples.json` 的 `intent_examples[].user_prompt` 与 `failure_messages[].toast/next_step` 是显式 zh-CN 用户输入/输出样例；英文 purpose 明确其只是数据，规范性工作流仍英文。例外位置约第 6–25、29–109 行，不把 JSON 容器当成任意中文指令的豁免。

### 产品引用与动作覆盖

完整逐文件、逐命令矩阵见 evidence JSON，包含路径、行号、API/effect、字节和内容哈希。

| Profile | 源文件 | 必需产品引用 | 独立拥有命令 | checker 校验命令 | 工作流 | 源/包 checker |
|---|---:|---:|---:|---:|---|---|
| Trade | 50 | 13 | 282 | 283 | order-workflows.md | PASS / PASS |
| Earn | 12 | 5 | 32 | 32 | earn-workflows.md | PASS / PASS |
| Assets | 12 | 5 | 29 | 29 | asset-workflows.md | PASS / PASS |
| Subaccount | 8 | 3 | 12 | 12 | subaccount-workflows.md | PASS / PASS |
| Affiliate | 8 | 3 | 12 | 12 | affiliate-workflows.md | PASS / PASS |
| Bot | 17 | 6 | 12 | 12 | bot-workflows.md | PASS / PASS |

35/35 产品引用存在，全部非占位、入口可达。379/379 已批准归属命令存在且符合工程契约；Trade 额外复用一个 Assets 所有的只读动作，合计检查次数 380，不重复计入唯一命令。缺失文件清单为空。不能用这些数字声明“整个当前 Gate CLI 100% 覆盖”。

对语义重点的人工核查：Alpha 买卖单位/报价绑定/1、5、6 非完成状态；Spot 预算与账号/保护三态；期权全平/部分减仓与历史查询分离；交割/永续保护局限；CFD 双侧保护保持；快速还款无金额 cap 时停止；杠杆设置部分成功不重放；资产链/标签/转账方向和未知结果；子账户 HMAC/密钥安全交接；Affiliate 窗口/时区/币种；Earn 收益与本金分离、PD 裁剪与固定贷缺少条款时停止；Bot 两轮确认、推荐排除、八类型模型和残余敞口。上述为静态推演，非真实交易通过记录。

### 源包一致性

六包文件数（含 manifest）：Trade 57、Earn 19、Assets 19、Subaccount 15、Affiliate 15、Bot 24，共 149。

独立重建允许的 shared Markdown 链接变换后，逐文件比较字节与 SHA-256：缺失 0、多余 0、非预期变化 0；manifest 文件哈希与工程契约摘要均一致。各包的六份共享规则来自同一规范源。公开分发模式扫描未发现新增内部地址/内部资料引用、凭据字面量或强制 UID 查询要求。该结论覆盖本次生成包，不把仓库历史审查记录当成公开运行包。

## 4. 工程验证与可复现边界

| 执行 | 结果 | 范围与边界 |
|---|---|---|
| `python -B -m unittest discover -s tests -p 'test_*.py' -v` | 31 tests PASS | 正式 root 套件；本地合成 stdio、安装器宿主边界 |
| `python -B -m unittest discover -s tests/cex -p 'test_*.py' -v` | 113 tests PASS | 正式 CEX 契约/包/公共流合成回归；不是已调用每条业务命令 |
| `python -B scripts/cex_skills.py build --source . --contract tests/cex/cli-contract.json --output <isolated-output>` | 六包 PASS | 新输出目录；未安装到用户宿主 |
| 六源目录及六生成包 `inspect` | 12 次 PASS | 结构、链接、工程契约 |
| 独立 source/package 字节/摘要比较 | PASS | 149 包文件，无未解释差异 |
| 16 个范围内 Python AST、15 个 JSON 解析 | PASS | 静态解析，无业务执行 |
| `gofmt -l scripts/export_cex_cli.go` | PASS，输出为空 | 只证明语法/格式可解析 |
| 本轮隔离反例 | 已复现 6 类 | 自动写、超时失效、递归打包、HTML 插入、逆序误判，以及已知退出码行为 |

上表 Python 在任务专用 venv 执行：markdown-it-py 4.0.0、PyYAML 6.0.2、mdurl 0.1.2、websockets 15.0.1；未改系统依赖。两套单测最多 2 个进程并发；起始检查为 10 CPU、16GiB 内存、可用磁盘约 95GiB，轻量任务峰值预算低于 1GiB，不进行 CLI 全量构建或负载测试。一次性副本、venv、生成包、探针、下载与原始输出在交付前清理，保留正式摘要/证据。

### 反例与场景证据

| ID | 等级 | 预期安全边界 | 实际观察 |
|---|---|---|---|
| RP-01 | 隔离行为 | 新写工具没有逐项许可不得调用 | 完整 runner 调用合成 transfer，记录 amount=0.0001 |
| RP-02 | 隔离行为 | 0.1s 期限内返回超时 | 0.8s 守卫仍阻塞，进程组已回收 |
| RP-03 | 隔离行为 | 输入内部的输出应在副作用前拒绝 | copytree 递归至路径过长；finally 清理，未发布输出 |
| RP-04 | 隔离行为 | 响应 label 作为文本 | HTML 中出现原始脚本元素；浏览器执行 NOT_EXECUTED |
| RP-05 | 隔离行为 | 叙述/事件顺序必须符合要求 | 逆序文本仍 overall_pass=true；仅模型 API 是合成响应 |
| RP-06 | 隔离行为 | 区分失败摘要与进程状态 | Fail=1、Pass Rate=0%、exit=0；报告生成成功 |
| DW-01 | 静态推演 | 同一 Spot 账号能力口径一致 | 旧否定与新 flag 表/专节冲突 |
| DW-02 | 静态推演 | 无隔离证明不得自动 fixture 写入 | 地址/名称规则可错误放行 |
| DW-03 | 静态推演 | 批准公共 GET/WS 不误判，私有旁路拒绝 | bundled profile 未同步例外 |
| DW-04 | 静态推演 | CEX 缺 CLI 能力停止 | 通用 preflight 文档仍声称全局 fallback |
| VIS-01 | 视觉检查 | 图文与当前安装目录一致 | 存在旧目录名/旧路径截图 |

RP-06 是项目测试文档和既有测试**已经明确记录的历史行为**，本轮不单独列为新缺陷，也不把 exit=0 当成连通性通过。未发现仓库内使用该退出码直接作为发布门禁的调用方。本轮发现不靠扩大这个已知约定凑问题数量。

## 5. Go 导出器专项与安全基线

`scripts/export_cex_cli.go` 是只读 Cobra 注册导出器；预期读取静态命令树/本地 flags，记录 handler 符号并编码 JSON，不执行 handler。已按意图 → 实现 → 调用交互核对 nil RunE/Run 分支、树遍历、flag 注解、错误传播和输出用途。当前使用的是 Cobra 自身有限命令树；没有用户输入网络接口、goroutine、存储或资金写入。没有确认的独立 Go 缺陷；stdout 编码错误导致开发工具退出不被夸大成生产服务 P0。

本仓库没有 go.mod、Makefile 或 golangci 配置；该文件依赖外部 approved CLI checkout。**没有运行 go build/vet/test/race/lint 或执行 cmd.Root 导出**，也未为本次审查构建 Gate CLI；这些集成检查为 NOT_EVALUATED，gofmt 不替代它们。Go 2/5/9 的资源核查限于一次性有限树遍历；3/6（并发/协程）、13/14/20/21（DB/Redis/MQ/搜索）、15/16（容器/K8s）、17/18/19/22（业务交易/公网入口/服务指标/调度）无可达目标，记 NOT_APPLICABLE，不套用后端服务设施要求。

统一 Code Review 输出：

- **Strengths**：六包闭包和共享事实源清晰；工程契约与 package digest 分离；现有测试不访问真实账户；新 CEX 的 UID/MCP 边界有效。
- **Critical**：没有已证实 P0；不以“无 P0”抵消本轮 P1。
- **Important**：CR-FULL-01 至 06，需要修正；属于独立失败门禁，不按评分平均。
- **Minor**：CR-FULL-07 至 10，需同步流程/文档。
- **Security Baseline Verdict**：输入/执行授权与输出转义 FAIL（01、02、06）；运行资源/期限 FAIL（03、04）；六个 CEX 静态秘密/权限边界未发现新增问题。SQL 注入、持久化读写、缓存/MQ、服务部署不适用本项目范围，不能机械写已通过。
- **Project Rules**：尊重非 CEX 排除、无业务修复/配置新增、无真实资金行为；只提交本轮报告/证据，不包含 docs/config，不 push。
- **Assessment**：FAIL；实际业务/公开二进制全量集成证据不足，独立记录为未验证。

## 6. 增强检查与剩余工作

| 检查 | 选择/状态 | 证据与限制 |
|---|---|---|
| source/package equivalence | 已选，PASS | 独立链接重写、字节和 digest、149 文件清单 |
| rule freshness | 已选，FAIL | Spot、auditor、preflight、截图旧口径 |
| trigger accuracy | 未选，NOT_EVALUATED | 没有真实宿主 skill-load 事件；静态路由不能代替准确率 |
| comparative effectiveness / 多模型 | 未选，NOT_EVALUATED | 无付费调用、无比较分数 |
| auditor 回归语料实际运行 | 未选，NOT_EVALUATED | 读取 AR01–16 检查协议适用性；未声称独立 reviewer 执行精确率/召回率 |
| 外部专用安全 scanner | 未选，NOT_EVALUATED | 自有静态检查不伪装成第三方全量扫描 |
| 跨 Skill/宿主真实行为 | 未选，NOT_EVALUATED | 只核对声明的传递边界与既有合成回归，不审忽略的业务 |
| 公共 CLI 全量能力/后端 | REQUIRES_REVIEW | 工程379命令非公开版本承诺；只读取公开来源样本 |
| 司法辖区/服务实体适用性 | NOT_EVALUATED | 不作法律/合规认证 |

后续最小复审范围：先处理 01/02/03/04/06 的通用工具安全与资源门禁、05 的 Spot 单一事实源，更新正式单元/E2E与既有检查契约；再同步 07–10。重新执行两套正式测试、隔离反例、六包构建和源包比较。真实业务联调、公开发行版全量覆盖和宿主 Agent 行为如需验证，应另按明确环境/授权执行，不能由本报告替代。

审查已完成并留存；修复尚未实施，发布验收未通过。
