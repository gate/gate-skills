# 项目与 CEX Skill 审查问题修复复核

日期：2026-11-03（Asia/Shanghai）。代码版本：6d13a6b48a876634c4618844bfdca4f6e478303d。
问题来源：[上轮完整审查](2026-11-03-project-cex-full-review.md)，基线 bb6a3f7；上轮报告提交 dd49e2d。

**本轮修复与工程静态复审：PASS。上轮 10 项问题全部关闭，未发现本轮范围内剩余的 Critical/Important 问题。**
该结论限于代码、规则、工程契约、独立包和实际执行的合成测试；不代表公开 CLI 全量兼容性、真实业务集成或宿主 Agent 行为已经验证。

## 范围与方法

修复实施共 36 个文件，含删除 8 张已核实失效的安装截图。重新核对 223 个项目/CEX 文件，排除 skills 下非 CEX 的 275 个路径，包括用户明确排除的 18 份副本。六个业务目录仍为 107 文件、专属共享规则仍为 6 文件；非 CEX 业务文件与 Pay 安装器实现均未修改。

工程内容使用 code-review 的 generic profile；Skill 使用当前 gate-cex-skill-audit 的格式、覆盖、CLI、资金/权限、可执行内容、来源一致性与新鲜度规则。按用户要求，**不使用 tech-cr**，没有创建技术方案。审查由当前 agent 完成，没有声称独立 reviewer、第三方安全扫描或真实模型执行通过。

复审覆盖修复 diff 和完整影响链：runner → schema/只读门禁 → stdio → verdict/report；构建入口 → 路径验证 → copy/共享链接 → 包检查/manifest；Skill 入口 → 产品/共享/工作流 → 生成包。未改动的产品字段表和 Go 注册导出器沿用上轮同一内容哈希的静态证据；没有用旧测试结果替代本次修改路径的实际测试。

[正式执行、文件哈希、动作与包/ZIP 清单](2026-11-03-project-cex-review-fixes-evidence.json)。

## 问题关闭表

| 上轮 ID | 修复和联动范围 | 本轮证据与关闭依据 |
|---|---|---|
| CR-FULL-01 | 新增唯一 fixture-safety.md；三个旧入口/指南引用它；移除地址/名称自动放行、必不成交、失败强制补偿和清理失败仍 PASS 等冲突 | 内容契约检查入口→依赖→拒绝语义；默认合成依赖，真实执行另行授权，缺证据 BLOCKED、零写。未声称模型已实际遵守 |
| CR-FULL-02 | safe_reads.py 为版本化公共只读契约；schema 在参数生成前、参数在调用前验证；未知/写/私有工具默认 SKIP | 单元与真实 runner E2E：已批准读正常调用；新写、零参数未知工具、伪造 readOnlyHint、写 overrides、额外字段均零调用。服务端边界为合成 peer |
| CR-FULL-03 | stdio_client.py 是唯一通信边界；非阻塞读写、单调 deadline、stderr 排空、帧/总字节/事件上界、异常/退出清理 | 正常及通知穿插、initialize/list/call 沉默、半行、stdin 堵塞、stderr 堵塞、畸形/EOF/错误 ID/洪泛、大小上界及回收用例通过 |
| CR-FULL-04 | 通用 build 在 mkdir/staging 前校验解析后输出路径和源链接；六包/单包共享该入口 | 单元断言拒绝前没有 copy、目录未变化；通用 CLI 嵌套路径实际拒绝；路径别名、共享目录、缺失父目录、已有输出、正常外置包通过 |
| CR-FULL-05 | Spot 删除旧绝对否定，保留已安装叶能力门禁和同账号生命周期规则；恢复并保留 spot-account-selection 锚点；checker 增加已知否定回归约束 | 正常源/包通过；把两类旧否定分别加入源/包，真实 check CLI 均以 C5 拒绝；283 次 Trade 动作检查仍通过 |
| CR-FULL-06 | HTML 的 label/status、服务/工具/模块名、参数/响应/skip/message 均在出口转义；文件名与展示名分离 | HTMLParser 检查不生成脚本、图片或事件属性；用户数据以文本保留、只转义一次，正常报表结构保留；未在浏览器执行攻击 |
| CR-FULL-07 | tools_in_order 改为精确顺序和次数匹配；结果及报告标 narrative-only，业务执行 NOT_EVALUATED | 正序通过；逆序、缺项、重复、额外事件失败。真实 CLI→场景文件解析→合成模型→判定→报告→退出码 E2E 通过 |
| CR-FULL-08 | profile 精确登记现有 Trade 公共 GET/WS 例外及私有 CLI 边界；同步 auditor/测试协议/README；Bot 预期引用补齐已批准的两份文档 | 当前批准路径不按 blanket CLI-only 误判；私有/任意路径仍受原门禁；增加 AR17/18 固定语料。内容检查不是 reviewer 准确率实测 |
| CR-FULL-09 | preflight 指南限定适用产品，六 CEX 指向自己的 preflight/setup/auth；移除所有新 Skill 一律 fallback 与版本字段普遍稳定的过度声明 | 内容及本地链接检查通过；没有修改 Pay 的 Exchange 连接、安装能力或配置 |
| CR-FULL-10 | 中英文 README 删除 8 张失效图及全部活跃引用，改为按真实 Skill 名/加载结果核验；保留其余有用通用 UI 图 | 图片不存在性/引用、本地路径/锚点检查通过；最后 README 调整后重跑 13 项受影响历史测试通过 |

01、08–10 含规范性文档修复，其关闭依据是规则一致性、静态链路和内容契约，不等于观察到另一个模型执行。07 的文本顺序判定即使 PASS，也不表示工具已被实际调用。

### 新增代码边界和兼容性

- 旧 smoke 默认范围收紧为两项已经核实名称和字段的公共读取：cex_spot_get_spot_tickers、cex_spot_list_currency_pairs。其他工具 SKIP，保留分母和原因；不是“整个服务连通性全部通过”。真实 server 必须是用户选择的可信 stdio 实现；远端描述本身不能证明实现安全。
- stdio 支持 POSIX（macOS/Linux）；其他宿主在启动子进程前明确失败。现有 timeout_seconds 保留，必须有限且位于 (0,300] 秒；单帧 8MiB、每次 exchange 接收总计 20MiB、未匹配事件最多 1,024；关闭 TERM/KILL 各最多 1 秒。超限失败、不自动重试工具或重启服务来扩大权限。
- 旧 runner 的“个别结果失败时进程仍可退出 0”是上轮已经记录的历史约定，本次不擅自改写。测试和文档继续要求消费 summary/report，SKIP 不算成功执行。
- 顺序判定更加严格，会拒绝旧版仅包含相同名称但顺序/次数错误的叙述；这是预期修复，不削弱为“顺序子集即可通过”。
- 无新增运行配置项、环境变量或写入开关。测试中 model API key 是明确的合成常量，未使用真实凭据。Go/Java 业务代码、SDK 与数据库没有改动。

## 测试与执行记录

| 命令（任务专用 venv） | 实际结果 | 证据层级 |
|---|---|---|
| python -B -m unittest discover -s tests -p 'test_*.py' -v | 52 tests，17.790s，OK | 正式单元/组件/CLI E2E，外部 peer/model/下载边界合成 |
| python -B -m unittest discover -s tests/cex -p 'test_*.py' -v | 114 tests，60.136s，OK | 正式 CEX 契约、包、公共流合成回归 |
| python -B -m unittest discover -s tests -p 'test_skill_content.py' -v | 13 tests，11.794s，OK | 最后 README 内容修改后的受影响历史回归，不另重复计算唯一用例 |
| canonical build，六源/六包 inspect | 6 包及 12 次检查 PASS | 本地真实构建与静态契约 |
| 独立 source→package 映射与 ZIP 比较 | 149 包文件，缺失/多余/非预期变化均 0；6 ZIP CRC/逐文件一致 | 本地真实产物验证 |
| 全范围 Python AST/JSON 与 diff --check | 22 Python、18 JSON 解析；diff 检查通过 | 静态检查 |

正式新增用例纳入既有统一入口，位于 tests/test_review_repairs.py、test_cex_builder_boundaries.py、cex/test_full_review_repairs.py，复用 tests/fixtures/smoke_server.py；另有正式 stdio_probe.py 负责可回收、外层受限的进程验证。没有留下仅供本次使用的孤立测试入口。

第一轮检测到的锚点遗漏与已退出进程组信号错误已修复；其后的完整套件包含这些路径并通过。最后 HTML 校验修正了双重转义，并验证解析后正常文本保真。没有忽略失败或降低业务断言；HTML 的文本断言允许单元格前已有固定状态图标。

两套测试最多 2 个进程并行，起始可用内存 35%、磁盘约 94GiB，任务为轻量构建/合成 IO，预算低于 1GiB。未进行真实服务负载测试或 Gate CLI 构建。临时 venv、原始日志、一次性文件在交付前删除；保留正式证据和六包交付物。

## 六个 CEX Skill 的九维复核

批准范围保持：Earn 现有五产品；Trade 现有有界公共行情例外；Bot 八产品及逐动作下一轮确认；所有私有读取和写入用 CLI，无 Exchange MCP 引用，无恢复强制 UID 查询。

| 维度 | Trade | Earn | Assets | Subaccount | Affiliate | Bot |
|---|---|---|---|---|---|---|
| C1 Agent Skills 格式 | PASS | PASS | PASS | PASS | PASS | PASS |
| C2 架构与边界 | PASS | PASS | PASS | PASS | PASS | PASS |
| C3 已批准编写范围覆盖 | PASS | PASS | PASS | PASS | PASS | PASS |
| C4 工程 CLI 契约 | PASS | PASS | PASS | PASS | PASS | PASS |
| C5 参数/结果/恢复解释 | PASS | PASS | PASS | PASS | PASS | PASS |
| C6 本地引用与包完整性 | PASS | PASS | PASS | PASS | PASS | PASS |
| C7 英文与术语 | PASS | PASS | PASS | PASS | PASS | PASS |
| C8 静态资金/权限/隐私边界 | PASS | PASS | PASS | PASS | PASS | PASS |
| C9 可执行脚本 | PASS（合成） | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |

**C4 范围解释：** 本表 C4 只评价已批准工程编写契约与当前文档的一致性，379 条唯一归属路径全部对照通过。上轮列为 REQUIRES_REVIEW 的“完整公开二进制可用性”没有被本轮测试证明，仍为 REQUIRES_REVIEW，不能据本表宣称所有公开版本/部署都支持。这里对证据层级作明确拆分，不把未验证事实改成 PASS。

完整对外发行能力/真实运行认证仍缺上述证据；如果以它为目标，总体结论仍为 INCOMPLETE。本轮请求的十项修复与静态/合成复核则已完成。上轮公开规范/官方项目访问记录可追溯至原报告；本轮没有重新下载/安装 Gate CLI，也没有构建它来让能力检查通过。

全部 35 份产品引用和 6 份工作流完整、可达、非占位。唯一命令分母不变：Trade 282、Earn 32、Assets 29、Subaccount 12、Affiliate 12、Bot 12，总 379；Trade 另复用一个 Assets 只读动作，因此工程检查动作次数为 380。无发现新增重复写所有者、兄弟包运行依赖、内部资料引用、凭据字面量或强制 UID 查询。

C7 继续保留 Trade localized-examples.json 的 zh-CN 用户输入/输出数据例外，英文 purpose 与规范性规则不变。其他未改动产品文件按源哈希及本轮解析/引用/契约结果复用原语义审查证据，而不是虚构每条 CLI 的实跑轨迹。

## 包交付与来源一致性

本地产物位于 dist/gate-cex-review-fixed-20261103：

| 包 | 含 manifest 文件数 | ZIP |
|---|---:|---|
| gate-cex-trade | 57 | archives/gate-cex-trade.zip |
| gate-cex-earn | 19 | archives/gate-cex-earn.zip |
| gate-cex-assets | 19 | archives/gate-cex-assets.zip |
| gate-cex-subaccount | 15 | archives/gate-cex-subaccount.zip |
| gate-cex-affiliate | 15 | archives/gate-cex-affiliate.zip |
| gate-cex-bot | 24 | archives/gate-cex-bot.zip |

独立重算允许的 shared Markdown 链接变换后，与源字节逐文件比较；六份共享文件均与规范源相同；重新核对 manifest 文件哈希及工程契约 digest。每个 ZIP 仅含自己的一个包目录，内容与经审查目录逐文件一致；SHA256SUMS 和证据 JSON 保存归档摘要。这里对比可信源映射，不只信任包自己生成的 manifest。

目录和 ZIP 是本轮正式本地交付物，保留供安装/复核；未向用户宿主安装、未上传或发布。构建产物按既有 dist 忽略约定不混入源码提交，可由上述已提交版本重建。

## Code Review 结论

### Strengths

复用通用构建器与既有测试入口；通信只有一个集成边界；只读许可不能由未信任 annotations、名称前缀或 overrides 扩大；资金与 CEX 运行范围未扩展。

### Issues

Critical：无本轮剩余发现。Important：无本轮剩余发现。Minor：无新增必修项。旧退出码、未验证的公开能力和宿主执行按已知边界单列，不伪装为已解决或已实测。

### Open Questions

不影响这十项修复落地的剩余证据：全部公开 CLI 叶与部署 schema、真实业务集成、实际宿主/模型执行及 auditor 新鲜 reviewer 回归准确率。没有依赖这些未知而静默打开业务能力。

### Security Baseline Verdict

| 项目 | 结论 | 依据 |
|---|---|---|
| SQL injection | NOT_APPLICABLE | 无 DB/SQL 路径或修改 |
| Hardcoded secrets / configuration | PASS | 无新增产品配置/凭据；测试只用合成值，未读取真实账户配置执行回归 |
| Authentication / authorization | PASS（本轮边界） | 公共只读 catalog、未知/写拒绝；Fixture 逐项授权规范；CEX 原授权保留 |
| Sensitive data exposure | PASS（修改出口） | HTML 全部不可信展示出口转义，stderr 丢弃不回显；未作全服务认证 |
| Input validation / resource bounds | PASS | schema/参数、真实路径、stdin/stdout/消息与事件上界、deadline/清理反例通过 |

### Project Rules

非 CEX skills、18 副本、Pay 安装器与 docs/config 均未修改；没有新增配置或权限开关。代码包含必要意图/约束注释；正式单元与 E2E 均实际执行。用户原工作区保持原状态；只对独立工作树的本任务文件精确提交。没有 push。按用户要求不做 tech-cr Skill 评审。

### Assessment

Quality Gate：PASS（本轮修复、工程代码及包静态/合成范围）。
Loaded profiles：generic；Skill 另用 gate-cex-skill-audit。
完整公开发行能力/真实业务与 Agent 执行：未认证，保留上述未验证项。

## 增强检查与复用限制

| 检查 | 状态 | 证据层级 |
|---|---|---|
| 源包等价、manifest/ZIP、公开内容 | PASS | 实际构建、字节/digest、静态扫描与人工裁决 |
| 规则新鲜度及十项复核 | PASS（本轮问题） | 全影响链核对和对应回归 |
| 自动触发准确率/多模型比较 | NOT_EVALUATED | 未运行真实宿主或付费模型 |
| AR01–18 新鲜 reviewer 准确率 | NOT_EVALUATED | 更新语料并静态审查，不冒充 TP/FP 实测 |
| 专用外部安全 scanner | NOT_EVALUATED | 自有检查不冒充第三方扫描 |
| 真实业务/公开 CLI 全量覆盖 | REQUIRES_REVIEW | 工程 379 路径不是公开发行承诺 |
| 法律/辖区/服务实体适用性 | NOT_EVALUATED | 本轮不作合规认证 |

后续代码、契约、规则或包字节变化会使相应证据失效，须重跑受影响正式用例与源包核对；共享规则变化需覆盖六个依赖包。真实集成另按明确授权与隔离边界开展，不能由本轮静态/合成 PASS 自动推导。
