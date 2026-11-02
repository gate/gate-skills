# Review: master 当前文件脱敏修复与全仓复审

日期：2026-11-03（Asia/Shanghai）。修复基线：`885b64f183d43e40823c30693530e3f20a4efde8`。
本次代码/资料以附带文件哈希清单绑定，由同一 Git 提交保存；不依赖个人检出目录。

**本次脱敏与当前仓库公开内容专项复审：PASS。上轮 DISC-01 至 DISC-04 均已关闭，本轮没有额外确认的披露问题。** 范围继续排除 GitLab 旧提交和 Key/Secret 示例；不把本结论当作全业务、全部外部服务或所有运行行为的安全认证。

## Loaded Profiles

`code-review` 的 generic 单遍规则与输出契约；`security-review` 的敏感数据规则。当前修改对象为文档、模板及 Python 测试，无 Go/Java 实现变化。Skill 按用户要求不使用 tech-cr；没有创建技术方案或运行其他审计代理。

## 变更概览

- 四平台 merchant-discovery 模板和安装 Skill 统一到现有 Pay 契约的公开 HTTPS 地址，保留可选商户发现、Pay/Exchange、DEX、Info/News 安装能力。
- 当前 changelog 删除旧开发/测试服务定位信息；不增加版本条目，不编造接口/参数变化。
- 三个 DEX CLI Skill 去掉非必需的内部 homepage，入口职责及下载/运行说明保留。
- 两份原始审查记录的个人目录改为通用 home 表达；另一份记录去掉内部归档定位，保留审查结论及追溯语义。
- 删除一张带个人终端信息的截图及中英文 README 引用，安装文字步骤和其余六张有用图片保留。
- 新增正式内容规则/反例测试，扩展既有四平台安装 E2E，并更新统一测试说明。产品未新增配置项、环境变量、CLI flag 或配置键。

## Intent Analysis

目标是在保留正常使用的前提下消除当前主干的不宜公开信息。先核实来源再改动：Pay Skill 已有公开商户发现 HTTPS 地址，且 [Gate 官方公开 Pay 文档](https://raw.githubusercontent.com/gate/gate-skills/master/skills/gate-pay-x402/SKILL.md) 同样声明该地址，因此只统一现有 `url` 字段，不猜测新地址或删除功能。来源文档 SHA-256 见证据，来源可公开不等于本次已验证服务部署与账户权限。

按“目的→实现→跨模块影响”复核：公开内容→四平台 fragment→真实安装器→生成 JSON/TOML/mcporter argv；Skill 元数据→普通入口；文档→README 引用→图片；规则→合成反例→当前文件扫描。排除旧提交不等于偷偷清空历史；保留公开示例不等于把它们声称为私人凭据泄漏。

## 问题关闭与影响链

| ID | 修正位置 | 关闭证据 |
|---|---|---|
| DISC-01 / 原 P1 | skills/gate-mcp-installer/SKILL.md、四平台 merchant-discovery fragment；相关两个安装器 changelog 和 DEX wallet changelog | 模板指向 `https://openplatform.gateapi.io/pay-mcp-server/mcp`，与未修改的 Pay 文档及官方公开来源一致；四平台全选重复安装和 discovery-only E2E 均断言实际生成地址；旧开发/测试引用没有残留 |
| DISC-02 / 原 P2 | skills/gate-dex-market-cli、gate-dex-trade-cli、gate-dex-wallet-cli 的 SKILL.md | 仅移除可选 homepage；frontmatter、描述及其余字段保持；当前全仓检查不再有对应内部仓库定位 |
| DISC-03 / 原 P2 | 两份 download Skill 审查报告、中英文 README、image/codex-terminal-install-1.png | 通用路径替换；敏感图片已删除且引用已移除；README 本地路径/锚点测试通过；其余六图重新本地 OCR 且与既有目视证据哈希一致 |
| DISC-04 / 原 P2 | docs/cr/2026-10-28-gate-cex-disclosure-cleanup-verification.md | 移除归档目录定位，只保留受控留档/追溯事实；不删除原审查记录，不对 Git 历史作清理承诺 |

不复写旧地址、个人用户名、完整本机路径或 Key/Secret 值来展示 before/after。已移除主机的回归约束只保留不可执行的摘要，测试诊断只返回类别/行号。

## 全仓覆盖与证据

复审实现输入 **500 文件：494 个文本、6 张 PNG**；不是仅检查 diff、README 或 CEX 目录。原始主干 500 文件中删除一图、新增一份测试，随后本次报告及证据作为另两份文件加入，最终提交包含 502 个当前文件。

- 所有输入逐文件读取、类型识别、SHA-256 和文本/编码/引用候选扫描；JSON 解析和 Python AST 检查完成，未读/超限条目为空。
- 对服务域名、个人目录、内部归档、配置模板和发布说明重新核对，剩余疑似开发/内部 URL 候选全部是明确的合成测试数据，不被部署或请求。
- 六张保留图片本轮重新离线 OCR（127 个识别片段，零解码/OCR 错误）、枚举当前 PNG 元数据。像素哈希与上轮目视复核一致；没有发现新增个人目录、私人凭据或内部服务内容。EXIF 仅有已核实的颜色空间/像素维度标签。
- 六个 CEX Skill 和专属共享规则的 113 文件哈希与修复基线一致；20 份 Info/News 本地规则副本仍在范围内检查且内容未改，不按文件名删除。
- 当前树没有压缩包、原生业务二进制、LFS 指针或子模块；外部下载产物没有被假称为已审。新报告和证据也在最后的公开内容检查范围内。

[完整文件哈希、图片结果、来源及执行证据](2026-11-03-master-disclosure-cleanup-rereview-evidence.json)。文件清单绑定实现输入；报告文件由 Git 同提交绑定，证据本身不制造自引用哈希。

## Language-Specific

N/A（generic 专项）。没有 Go/Java 业务代码变更，不虚构 build/vet/race 结果。Python/模板的正式单元、组件和进程 E2E 实际执行如下。

## 测试及检查结果

| 实际命令/检查 | 结果 | 证据范围 |
|---|---|---|
| python -B -m unittest discover -s tests -p 'test_*.py' -v | **60 tests，17.942s，OK** | 包括新增公开内容正/反例、负向编码/路径、fixture 例外优先级、四平台 discovery-only 和重复全选安装 |
| python -B -m unittest discover -s tests/cex -p 'test_*.py' -v | **114 tests，60.255s，OK** | 现有 CEX 正式契约/包/合成 helper 回归；不是线上交易 |
| 全仓重新读取/哈希/候选复核 | **500 输入文件，无本轮确认问题残留** | 不把合成域名和通用 home 路径当成真实设施/人员 |
| 六图片 OCR/元数据/同一性 | **6 图、127 片段、零错误** | 本地 Apple Vision；原有目视裁决按同字节复用，不上传图片 |
| diff 空白、精确暂存与 docs/config 检查 | 完成 | 无新增空白问题；只提交本任务修改；该禁止路径没有变更 |

报告和证据加入暂存后，另执行 `python -B -m unittest discover -s tests -p 'test_disclosure_cleanup.py' -v`：7 tests，0.408s，OK。该轮覆盖新交付文档，不重复计算唯一用例数量。

新增/修改正式测试纳入既有 `tests/` 目录和两个历史 unittest 入口，不只留下临时脚本。安装 E2E 的 mock 仅是 Git 下载与 mcporter 等外部边界，真实选项解析、fragment 选择、JSON/TOML 生成、配置合并、过滤和清理链路及断言仍执行。覆盖四类宿主、仅 discovery、全选重复安装、无关已有配置、既有 CEX 安装保留；历史异常选择/克隆失败等回归一并执行。没有实际运行 npx、交易工具或商户 API。

测试使用任务 venv 的 Python 3.13、既有 Node，依赖固定为 markdown-it-py 4.0.0、PyYAML 6.0.2、websockets 15.0.1；临时 HOME/TMPDIR 与受控 PATH，不继承真实账户凭据。两个独立套件最多两个 worker、每进程 180 秒上界。没有把该环境说成 OS 级网络沙箱或真实业务 E2E。

## Strengths

- 已有 Pay 契约与公开来源支持地址选择，四平台配置 E2E 验证实际输出，避免只检查文案一致。
- 个人信息从图片和入口引用同时处理；回归规则不把原内部主机名重新放进测试源码。
- 凭据示例、真实配置、合成反例、个人路径及普通运行路径分别裁决，保留既有功能和追溯。

## Issues

### Critical (Must Fix)

None（本次修改与当前文件披露专项）。

### Important (Should Fix)

None（本次修改与当前文件披露专项）。

### Minor (Nice to Have)

None（本次修复范围没有新增确认项）。

## Open Questions / 未覆盖范围

本轮不验证实际 merchant-discovery 部署连通性、账户权限或支付/交易结算；没有从文档存在推断服务可用。GitLab 旧提交及 Key/Secret 示例按用户要求排除。既有 Trade/Earn 展示规则冲突 RCE-02 不在这四项存量内容脱敏内，仍按上轮记录保持开放；不据此宣称全业务没有任何问题。

当前文件未发现本轮确认问题残留，不是对任意隐藏编码、加密数据、运行时输出、其他仓库或外部下载物作绝对无泄漏保证。

## Security Baseline Verdict

- **SQL injection — N/A：** 没有数据库访问或 SQL 改动。
- **Hardcoded secrets / credentials — Pass（本次范围）：** 修改不引入真实凭据；用户排除的公开 Key/Secret 示例保持。没有调用接口验证凭据。
- **Authentication / authorization — N/A（实现未改）：** 没有新增鉴权入口、授权头或权限；仅现有 catalog 的 url 值与公开契约对齐，未由此认证服务端权限。
- **Sensitive data exposure — Pass：** 四项披露修复、全仓检查、图片复扫及报告自查闭合，诊断不回显私人匹配值。
- **Input validation — Pass（变更范围）：** 正式内容规则覆盖编码/路径反例和 fixture 例外边界；URL 的实际生成配置有端到端断言。没有新增接收业务输入的运行接口。

## Project Rules

No REVIEW.md at repo root — baseline review only。

- 用户限定：旧提交和 Key/Secret 示例排除；不擅自修复其余功能。Info/News 副本、六 CEX 正文及 Pay 执行/安装实现保持。
- 配置：没有新增配置项/环境变量/flag/配置键，仅调整既有 URL 值。
- 文档：原审查记录保留并脱敏；不加工程过程型 changelog 版本；新复审资料保存 docs/cr。
- 提交：直接在 master 工作树实施，精确暂存；docs/config 无变更，原用户工作区内容保持。
- 测试与资源：正式新旧测试实际执行。10 CPU/16GiB 主机，起始可用内存约 28%、磁盘约 82GiB；套件与 OCR 有界运行，期间内存可用比例在 41%–42% 左右，未耗尽资源。一次性脚本、OCR 原文、环境与测试输出交付前清理，正式证据保留必要摘要/哈希。

## Assessment

**Quality Gate: PASS（当前文件脱敏修复及静态/合成复审范围）。**
**Reasoning:** 四类确认披露均已修正，174 项正式回归通过，全仓与新交付文档检查未发现本轮残留或新增披露项。实际线上权限、交易/支付和原有范围外事项不计为已验证。
**Loaded profiles:** [generic, security-review 专项]。
