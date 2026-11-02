## Review: fix/skill-legacy-content-20261102

### Loaded Profiles

None (generic review)。使用 code-review/SKILL.md、generic checklist、
code-reviewer-template 和 quality-gate；没有 Go/Java 实现变更。
基线：745ae3222a4f5c5e80fde73a29025bcfafbf44bf。

### 变更概览

按已确认方案实施第一版基础整理：

- 两份 README 的命令统计改为379个唯一归属路径，Trade额外复用1项资产只读命令
  不重复计数；分开 CLI、独立 CEX 包和 Pay/其他产品的安装说明。
- 四处图片引用改指向保留文件，再删除两个逐字节相同的截图副本。
- Scenario19按业务意图/命令命名空间选路，移除CLI/terminal必导DEX的规则。
- Earn审计清单改为已确认的五类，删除历史398作为固定审计门槛。
- 现有MCP安装器在同一个复制入口过滤新旧CEX业务目录，
  显式保留gate-exchange-pay；Exchange连接模式与全部模板保留。
- 开发指南、旧validator/tester示例按当前产品边界整理；
  旧Python会话执行器明确声明其输入格式，不将现有不同格式的场景误写成兼容示例。
- 改动的带版本Skill说明更新元数据及相应README版本，未增加无API变化的changelog。

范围修正以Milo后续指令为准：9个旧Info/News里的18份规则**不在本次范围**，
不修改、不迁移、不删除。未确认内容先跳过，Pay迁移/旧根规则删除未实施。
13个兼容入口、直播、两个Pay、Bot迁移提示、正式历史记录及CEX业务源码均保留。

### Intent Analysis

本版目标是清除已确认的重复/失效说明并切断旧CEX源码的安装入口，
同时保留Pay所需Exchange安装与用户已有内容。检查了过滤顺序、默认与显式选项、
四个平台复制/配置链路、失败清理、范围例外和跨域路由文本。
没有把“名称看起来旧”作为删除业务能力的依据。

### Language-Specific

N/A (generic single-pass, no language-specific verification)。
Python 3.13、Bash和现有Node JSON合并工具；未更改Go/Java服务。

### Strengths

- `install.sh:133–139`集中定义复制范围，Pay例外优先；
  `:169`在删除或覆盖目标目录前过滤，保护用户已有CEX安装。
- `tests/test_skill_content.py:220`执行真实安装脚本，四平台重复安装，
  验证过滤、Exchange/Pay保留、无关配置和原有CEX安装不被覆盖。
- `gate-skills-disambiguation.md:349–354`分别约束CEX/Info/News/DEX/Pay，
  泛CLI意图先澄清，不因缺能力跨域替代。
- `coverage-profiles.md:40`维持独立的五类业务预期，
  不通过恢复退役产品或从被审Skill反推范围取得通过。

### Issues

#### Critical (Must Fix)

None in the implemented change.

#### Important (Should Fix)

None outstanding in the implemented change.
初次四平台测试把JSON客户端的Gate-Dex/Gate-Info/Gate-News误期望为小写；
核对既有模板后修正了oracle，重新执行通过，未修改实际模板或降低保留范围断言。
复查还消除了README下方残留“全部Gate Skills”与新过滤范围的矛盾。

#### Minor (Nice to Have)

None outstanding in the implemented change.

### Open Questions

按Milo指令不继续追问未确认项，跳过Pay契约/发布依赖迁移。
18份文件已明确排除，不再作为本任务待确认项。
真实模型解释选路规则的运行未执行；本版只有路由文本契约检查，
不把静态字符串断言或人工推演当成真实Agent事件轨迹。
以上不记为已验证，不将本版局部验收扩展成完整支付/发布/模型行为认证。

### Security Baseline Verdict

- **SQL injection** — N/A：没有SQL或数据查询。
- **Hardcoded secrets / credentials** — Pass：新增代码无真实密钥；
  测试仅使用合成服务/原模板占位符，生产配置未加字段。
- **Authentication / authorization** — Pass within scope：没有业务调用或权限扩展，
  保留原Exchange配置选择；支付认证/执行链路未修改、未宣称通过。
- **Sensitive data exposure** — Pass within scope：测试不读取主机凭据，
  使用子进程专属客户端目标目录与本地替身；正式记录不包含真实账户数据或秘密。
- **Input validation** — Pass within scope：新增过滤器为固定模式，
  Pay精确例外优先；空值及新旧CEX名拒绝。传参和路径继续使用带引号的现有边界，
  回归包含空值、未来产品名、带空格目录名及未知安装选项。

### Project Rules

No REVIEW.md at repo root — baseline review only。

- 用户范围：18份及未知Pay迁移跳过；原工作区修改保留，隔离分支实施。
- 单写/统一依赖：复用install_gate_skills_to与原Git/mcporter集成边界，
  未增加第二个复制/配置写入实现。
- 测试：新增13项（7项单元/内容契约，6项子进程E2E），
  集成到根unittest及tests/README.md；旧CEX套件照常执行。
- 注释：生产过滤器说明Pay例外及先过滤再触碰目标的原因；
  测试文件说明mock与真实链路边界。
- 配置：无新增产品配置项。INSTALL_TEST_*仅为测试替身输入，
  已有客户端目录选项仅限子进程，不改变主机配置。
- Git/清理：仅精确暂存本任务文件，排除docs/config及其他工作树改动；
  报告本地提交，不自动push。临时venv、日志和校验包完成后清理。
- Changelog：本版没有业务API/参数变化，不添加工程过程或提交状态条目。

### 实际验证

在任务专用venv中复用仓库依赖markdown-it-py4.0.0、PyYAML6.0.2，
以及现有流式行情回归所需websockets15.0.1，不修改系统Python或项目依赖清单。
以10核/16GiB整机评估，执行前可用内存约34%、磁盘约98GiB；
最多两个测试进程，执行中可用内存约31%，未做高负载压测。

| 命令/范围 | 实际结果 |
|---|---|
| `python -B -m unittest discover -s tests -p 'test_*.py' -v` | 31项通过 |
| `python -B -m unittest discover -s tests/cex -p 'test_*.py' -v` | 113项通过 |
| `python -B -m unittest discover -s tests -p 'test_skill_content.py' -v` | 最后文档修订后定向复跑13项通过 |
| `python -B scripts/cex_skills.py build --source . --contract tests/cex/cli-contract.json --output <temporary>/packages` | PASS，六包；逐文件哈希与无MCP依赖文本检查通过 |
| `bash -n skills/gate-mcp-installer/scripts/install.sh`、`git diff --check` | 通过 |
| 与基线比对CEX、Info/News、Pay、Exchange模板/合并器 | 无内容变化；安装器仅复制范围函数与调用变化 |

根31项加CEX113项，共144个不同测试。末轮仅改Skill版本、范围说明和README元数据，
不改变安装/打包逻辑；定向复跑覆盖新增13项，原有18+113项证据仍适用。
没有删除有效断言、屏蔽失败或只编译后宣称通过。

E2E边界：真实install.sh参数解析→默认/显式选择→本地Git下载替身→实际复制→
实际JSON/TOML合并或mcporter注册替身→最终目录/配置断言。
覆盖四平台重复运行、main/cex-public/cex-exchange及两个Pay模式、
--no-skills、非法选项、clone失败和临时目录清理。
模型客户端仅在旧runner的--help测试中替换导入，断言不创建客户端。
没有执行真实交易、支付、外部发布、用户安装目录变更或付费模型测试。

### Assessment

**Quality Gate: PASS**

**Reasoning:** 本版已实施范围内无未解决的Critical/Important；
安装过滤在真实离线链路中验证，Exchange能力与已有用户CEX目录保留，
文档与当前统计/业务范围一致。模型选路、支付集成和发布审核未验收，
不属于本次通过结论。

**Loaded profiles:** [generic]
