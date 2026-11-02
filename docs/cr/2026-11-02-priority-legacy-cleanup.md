# 优先历史内容清理与 CEX / Pay 执行边界验证

## 范围与结果

基线：远端 `gate-skill-2.0` 的 `a573e7113149b2501e233e45a3815a6c38e50a6e`。
按 Milo 授权，实施上一份清点报告的 A1–A5；六个 CEX Skill 保持 CLI-only，
Exchange 安装能力继续保留给旧 Pay。B 类规则副本、图片去重、Pay 规则文件迁移，
以及 C 类 README/分流/开发指南的其他整理均未实施，另行提出方案。

删除四个文件：

- `docs/git_readme.txt`：无引用的临时 Git 操作笔记。
- `image/.gitkeep`：已有跟踪图片目录中的占位文件。
- `test-for-skill/mcp-smoke-test/gen_fixtures.py` 和 `test_fixtures.json`：
  当前执行器未消费的旧导出链路；按用户本次清理授权移除，Git 历史仍可恢复。
  仓库外手工消费者未知，不声称已验证其不存在。

删除 `run_test.py` 未调用的 `classify_tool()`、配置中的
`skip_write_tools/default_test_params/read_prefixes/write_prefixes`，
以及 `auto_params.py` 中被同值覆盖的一个 `size` 项。
保留运行中的 `auto_params.py`、`test_overrides.json`、schema 发现、调用和报告链路。
失效配置的移除不构成执行器只读保证；该通用执行器仍可能调用写工具。

两份根级运行规则不再把六个 CEX Skill 导向旧交换服务；CEX 的执行与认证规则归
`skills/_shared/cex/` 所有。旧授权表保留在 Pay 适用范围内，CLI 二进制解析的 §4
保持可引用。移除根级旧 CEX 执行示例，避免维护第二套业务执行规则。
安装器两份说明明确 Exchange 模式用于旧 Pay；不把旧 Pay 误写成已迁移至 CLI。

## 依赖与兼容检查

- 安装器的脚本、合并工具和全部模板共33个文件，与基线字节完全一致。
  `main/cex-public/cex-exchange`、OAuth 和密钥配置能力均保留。
- 六个 CEX 源码及其六份专属共享规则与基线一致；全量文本扫描及构建后的六包
  均未发现 MCP 依赖内容。没有为 CEX 增加 Exchange 运行入口。
- Pay 引用的 `exchange-runtime-rules.md` 仍存在；二进制解析 §4 和原授权表保留。
  没有替换支付工具、渠道、权限或业务流程；未执行真实支付。
- 全仓调用方搜索未发现被删除函数/配置/夹具的其他使用者；历史审查报告中
  的旧路径作为版本证据保留。未发现对删除的根级执行章节的锚点依赖。

## 正式测试与边界

新增 `tests/test_mcp_smoke_test.py`、`tests/fixtures/smoke_server.py`，
并在 `tests/README.md` 记录统一执行入口与用例。

六个单元用例覆盖：活跃配置与退役导出契约、默认 size 与 0/负枚举边界、
空/嵌套 schema、缺失和损坏 overrides、零值覆盖、skip 和客户端异常，
以及六个 CEX / Pay 安装器边界。

四个 E2E 用例执行真实 runner 子进程，覆盖：

1. 配置读取 → live tools → 默认参数/override → stdio 调用 → MD/HTML 报告；
   断言精确请求以及被跳过的工具未被调用。
2. live 列表为空 → 本地 cache schema → 参数 → 调用和报告，不依赖旧 fixtures。
3. JSON-RPC schema 错误 → FAIL 汇总与报告。
4. server 不存在 → 提前退出，无调用与报告。

仅服务端 peer 为本地模拟，不连接外部服务或读取凭据；配置、缓存及产物均在
测试临时目录中。旧 runner 在单项 FAIL 时仍退出0，因此测试断言汇总/报告，
没有把进程退出0当作连通成功，也未在本次改变该历史行为。

## 实际执行记录

环境：Python 3.13，任务专用临时 venv；安装仓库声明的
`markdown-it-py==4.0.0`、`PyYAML==6.0.2`，
以及现有 Trade 脚本回归所需的 `websockets==15.0.1`。
初次运行分别因缺少 Markdown parser 和 websockets 失败；补齐临时依赖后重跑，
未修改系统 Python、项目依赖清单或降低断言。

- `python -B -m unittest discover -s tests -p 'test_*.py' -v`：
  18项通过，含新增6项单元/4项 E2E 和既有8项 Bot 打包测试。
- `python -B -m unittest discover -s tests/cex -p 'test_*.py' -v`：
  113项通过，包含既有审计修复、交易及流式行情的隔离回归。
- `python -B scripts/cex_skills.py build --source . --contract tests/cex/cli-contract.json --output <temporary>/packages`：
  PASS，六包；随后逐包扫描，未发现 MCP 依赖文本。包仅作验证，未新增发布产物。
- 安装器33个可执行/模板输入及六个 CEX 源码与基线字节比对通过；
  `git diff --check` 通过。

未执行任何真实账户、交易或支付集成；静态/模拟/打包通过不等同于实盘验收。
无新增配置项。通过精确暂存提交本任务文件，推送目标仅为指定分支；
原工作区未提交业务改动不混入本次提交。
