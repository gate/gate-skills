# Gate CEX 对外内容清理与安装包复查

日期：2026-10-28。基线：f0c594b。范围：此前信息暴露报告中的 F01–F03、O01/O02，及其直接关联的 CEX 作者工具、工程附件和六包发布边界。

## 结论与处理

本次清理和离线验证完成：六个当前业务包及审核 Skill 未检出内部主机、个人路径或凭据字面值，结构、引用、命令契约、manifest 及解压后验证通过。未执行业务 API、真实交易或公开发布。

| 原项 | 处理 | 验证 |
|---|---|---|
| F01 内部 CLI 来源和真实测试地址 | 契约仅保留官方公共仓库入口，移除内部分支/提交/SDK 工程基线及 handler/source/line 来源字段；测试改用保留示例域和文档 IP | 411 条命令的参数/归属/排除及 required_variants 与原契约做递归差分完全一致；398 条属于六包，13 条为排除项 |
| F02 内部工程资料 | 56 份 CEX 方案、CR、CSV/JSON 和原始需求表附件从当前仓库文件树移出，原件在仓库外内部留档；README 去掉工程资料依赖 | 56 份留档原件逐字节匹配基线 Git 内容；仓库剩余 docs 不引用已移出的 CEX 方案作为运行前置 |
| F03 旧包 | 两套 before-* 旧包与陈旧当前包一并移出 dist，内部保留 | dist 仅保留新构建的 gate-cex-2.0 发布集合 |
| O01 工程沿革 | 审核 Skill 改为独立评审边界，去旧工具目录、历史 runner 和计划接口引用 | 8 份审核文档全量扫描与本地链接检查 |
| O02 陈旧包 | 当前源码重新构建六个目录包，另提供六个 ZIP 和 SHA256SUMS | 六源码、六目录包、六个 ZIP 解压包全部通过；每个 manifest 校验成功 |

原资料已转为受控内部留档，不属于本项目公开分发内容；原相对路径在内部留档中保留，用于追溯。本轮没有改写 Git 历史，因此旧提交仍可能含旧资料；清理完成范围是当前 CEX 源文件和重建包，不能把旧历史直接镜像为已脱敏仓库。非 CEX 产品不属于本轮清理范围。

**更正首次报告误报**：`docs/preflight-and-diagnostics.md` 使用的是 username 占位路径，没有真实用户标识，应保留；公开说明里 Feishu 产品名称也不是内部租户。真实 UID、密钥、内部 IP 与通用字段名、保留测试地址分别判断。

## 保留正常使用能力

六个业务 Skill 与共享 CEX 文件共 86 个源码文件逐字节等于基线，未删除接口、参数、模型、安全约束、认证指引或产品边界。保留公开 CLI/API 地址和必要本地配置路径。

只从作者契约移除工程来源元数据，没有把内部版本伪称为公共发布版本。保留 coverage_scope 的能力/发布区分；安装后的命令可用性仍需按原 Skill 的 preflight 检查。

## 校验工具修改和正式测试

复用 `scripts/cex_skills.py` 的唯一构建/检查入口，未新增用户配置项：

- 用当前 CEX 运行文档所需的公共主机集合约束引用，避免在规则中继续公开公司专属域名；覆盖普通文本、URL、编码后的域名和裸非公网 IPv4。
- 扫描所有文本和 JSON 附件/manifest；JSON 先解析，防止 Unicode 转义藏匿内部引用；坏 JSON 返回 C6。
- 识别 PEM 私钥、常见供应商 Token、JWT 和带值的常见凭据字段，诊断仅输出分类，不回显内容。
- 原大小/数量上限、路径/符号链接保护、暂存构建后发布、失败清理机制保留。
- 允许的公共主机为 GitHub、其原始文件服务、Agent Skills 标准站点及现用 Gate 官方 API/站点。新增外部依赖需审查后更新规则，不能依靠未识别域名绕过。

正式测试位于 `tests/cex/test_cex_skills.py`，沿用 unittest 统一入口；新增 5 个方法，共 **67 tests / 49.493s / OK**。首次新增契约测试把总条数误设为 398，实际为 411（其中 398 归属六包）；修正为按 owner 检查后重跑通过，未删有效业务断言。

| 新用例 | 层级 | 验证内容 |
|---|---|---|
| test_public_reference_policy_and_secret_literals | 单元 | 公开引用/占位符正常；未知主机、文档 IP、私钥标记、Token、凭据字段和坏 URL 拒绝；诊断不回显 |
| test_json_attachments_reject_escaped_private_reference_and_invalid_json | 组件 | 实际 inspector 读取正常/恶意/Unicode 转义/坏 JSON，保留正常附件 |
| test_public_contract_preserves_profiles_without_private_provenance | 单元 | 公开来源、398 归属动作及无内部修订字段 |
| test_real_checker_process_rejects_json_secret_without_echo | 进程 E2E | 文件→实际 check 命令→C6/非零退出；stdout/stderr 无原值 |
| test_real_builder_rejects_private_json_without_publishing | 进程 E2E | 受污染源码→实际 build→失败；无发布目录、无暂存残留、无内部地址回显 |

历史成功构建、独立包、manifest 篡改、丢引用、参数边界、真实检查器进程等 62 项一起执行。E2E 保留完整离线构建/检查链路，无 mock 被测功能，无外部交易依赖。

```bash
# 在安装了 scripts/requirements-cex.txt 固定依赖的 Python 环境运行。
python -m unittest discover -s tests/cex -p 'test_*.py' -q
# 新构建路径必须不存在；禁止覆盖旧包。
python scripts/cex_skills.py build --source . --contract tests/cex/cli-contract.json --output dist/gate-cex-2.0
# 六个目标分别使用 package 模式复查；ZIP 解压后使用相同命令。
python scripts/cex_skills.py check --target dist/gate-cex-2.0/gate-cex-trade --package --contract tests/cex/cli-contract.json
```

## 复查与交付边界

实际完成：作者工具和测试人工检查、CEX 源文件全量规则扫描、六个安装包全部文件扫描、模型/示例/引用复核、Markdown 引用闭合、源/包/ZIP 三层契约检查、文件摘要验证、留档原件验证、业务源码字节一致性验证及 Git diff 空白检查。源码和 ZIP 均不包含内部留档、测试契约、工程工具或 docs。固定规则无法证明未知格式或任意编码的秘密绝对不存在，结论限于实际扫描与复核范围。

既有技术方案原件整体移出并保留，未修改其设计内容，也未将其旧审查结论冒充本次全案通过；本次没有新增技术方案或修改业务系统架构。

资源：10 核/16 GiB 主机，检查时 memory_pressure 可用 35%、磁盘余量 49 GiB。最多两个轻量 Python 验证进程，无业务服务/大工程构建。任务临时 venv、解压目录和中间输出交付后删除；正式 ZIP、目录包、摘要和内部留档保留。

## 六包摘要

安装时解压所需 ZIP，将完整 gate-cex-* 目录放入宿主 Skill 目录。以下各包均可独立使用，包含本包共享引用。

| Skill | 归属动作 | 文件（含 manifest） | ZIP SHA-256 |
|---|---:|---:|---|
| gate-cex-trade | 282 | 35 | `d478781d9e3621e50302ac13bceec57b94ed54d734441ce87822542c0eb4a47d` |
| gate-cex-earn | 53 | 21 | `610356af60dfe75d4645081b90da5aafaa803c438901e51782c5bfab2eeeb684` |
| gate-cex-assets | 29 | 19 | `e40dc8b9550a67d9641cad2f6bbebd83159c43ec79e73268506e9e3b083d7e44` |
| gate-cex-subaccount | 12 | 15 | `97f02d6a3078dbf4367ddb06898b7a75fb58be7c7614d5124dce2d3cbe7217d6` |
| gate-cex-affiliate | 12 | 15 | `ccc647351888ad3d81ceb7ea786825f32f02a2757165399e6b1eb5b83d66f587` |
| gate-cex-bot | 10 | 17 | `bdf97fd6552d6b7f0d2640e76613e8e33f287f621b3891684c136b496613ebf7` |

正式产物位于 `dist/gate-cex-2.0/`；6 个 ZIP 的校验值同时保存在 `SHA256SUMS`。dist 按既有规则不提交 Git；复查报告和源码清理精确提交当前分支，不 push。
