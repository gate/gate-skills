# 下载版 gate-cex-trade 审查报告

## 1. 结论、范围与证据

**FAIL：不适合作为当前 gate-skill-2.0 的独立交易 Skill 发布或替换。** 确认 5 个 P1、3 个 P2；P1 均须修正后复审，涉及资金方向和保护字段的问题阻塞发布。此结论针对静态审查，不声称实际发生过反向交易、保护丢失或数据泄露。

| 项目 | 本次证据 |
| --- | --- |
| 审查日期 | 2026-10-29，Asia/Shanghai |
| 用户指定目标 | `~/Downloads/gate-cex-trade`，按独立安装包目录审查 |
| 对照基线 | GitLab `gate-skill-2.0@ba390fe6999026cd0d7328a4baac4eed788bd27a`；本次 `git ls-remote` 与本地远端引用一致 |
| 目标范围 | 全部 13 个 Markdown，97,591 字节；无符号链接、隐藏文件、脚本、二进制、嵌套压缩包或 manifest；没有未读目标文件 |
| 审查 Skill | 上述基线的 `gate-cex-skill-audit/SKILL.md`，SHA-256 `bda2964fb254b0f5442662e75b8aa8dcdd7e47b9cb66f18a6dfb7e253e5002c9` |
| 规则 | coverage-profiles、review-checklist、cli-verification、safety-and-execution、test-protocol、enhanced-review、report-template、reuse-notes；与本会话此前读取的 6ed9428 版逐文件无差异，复用其阅读记录 |
| 工程命令契约 | `tests/cex/cli-contract.json` SHA-256 `98ac1a0e5b04f39594548be36275a1e0c94c838ae5f99aff919db4de028860c1`；trade 所有者有 282 个业务叶子 |
| 基线检查器 | `scripts/cex_skills.py` SHA-256 `0c78461bbc6d56a2b7c9c32c40ec33326825ca874f9a3c5357be8983df6b2632` |
| 独立 CLI 证据 | 工作区已有 CLI 检出 `cd645f35e5630f0d5f5eaa4564c163c12059f845`；核对相关注册、handler、SDK 调用，已检查相关源文件没有未提交差异；没有构建、安装或执行 CLI |
| SDK | `github.com/gate/gateapi-go/v7@v7.2.167`，核对实际请求字段、序列化和 API 路径，关键模型另以官方公开版本交叉验证 |
| 公共证据 | 本次访问官方 API 文档入口、公开 CLI 源码及 SDK 模型；API 入口显示 v4.106.160。不是对所有线上产品、全部字段或已安装版本的集成验收 |

Milo 要求使用 gate-skill-2.0 的 trade 为基线，未批准本目标自行裁剪 delivery、stock、POV/chase 等范围。此前 Earn MR 的裁剪授权不适用于本 Trade 包。目标自述“routing layer”“supplied snapshot”不是改变审查范围的授权。

本机为 10 核、16 GiB，检查时 memory_pressure 空闲比例 48%，磁盘可用约 25 GiB。本次采用小型文本检查，不构建 Go、不安装依赖、不运行目标命令。预计新增磁盘仅为本报告及其 Git 对象，无高负载任务。

## 2. 九维审查结果

| ID | 维度 | 结论 | 依据 |
| --- | --- | --- | --- |
| C1 | Agent Skills 格式 | PASS | YAML 使用拒绝重复键的 SafeLoader 解析；name 与目录一致，description 152 字符，metadata 值均为字符串 |
| C2 | Gate 架构与约定 | FAIL | 旧 gate-exchange-* 依赖、CLI/MCP/API 多执行入口，不符合单独可用的六 Skill 架构，F3 |
| C3 | 业务完整性 | FAIL | 基线 delivery、stock、算法及多项变体没有对应可执行契约，F4；不能用 REST 路径列表替代 CLI 工作流 |
| C4 | CLI 正确性 | FAIL | CFD 枚举冲突、过时能力声明、闪兑请求结构不符，F1/F4/F5 |
| C5 | 说明质量 | FAIL | 缺保护字段省略语义和可构造的嵌套请求模型，F2/F5；泛化 JSON 说明不够 |
| C6 | 引用、包完整性与公开内容 | FAIL | 12 个可点击本地引用均存在，但六个共享运行时文件及外部旧 Skill 未包含，且发布内容出现内部来源，F3/F6 |
| C7 | 英文与表达 | FAIL | description 中的中文为规范性路由内容；本地化示例另作允许例外，F8 |
| C8 | 资金、身份、授权、隐私 | FAIL | 买卖枚举、保护清除风险及未内置共享身份/执行边界，F1/F2/F3；重复确认 F7 |
| C9 | 可执行内容 | PASS（静态） | 全目录仅 Markdown；检查命令文本，未发现目标脚本或二进制。独立脚本运行不适用；CLI/Agent 功能、真实交易未评估 |

司法辖区及服务实体法律适用性为 **NOT_EVALUATED**，不出具生产可用性或全局合规认证。

## 3. 确认发现

### F1 · P1 · CFD 买卖方向、价格类型和全平枚举不兼容指定基线

- 位置：`references/tradfi.md:34-36`，关联 `workflows.md:59`。置信度：高。
- 目标写 `side: 1 buy, 2 sell`、`price_type: 0 market, 1 limit`、`close_type: 0 full, 1 partial`，并声称与 installed CLI 一致。
- 基线契约、独立 CLI 注册及对应 SDK 为 `1=sell, 2=buy`、字符串 `market|trigger`、`1=partial, 2=full`。CLI handler 校验数值后直接传递 side，不会按用户“买”意图反转；`close-type=0` 和数值价格类型会被当前实现拒绝。
- 触发与后果：当使用指定基线对应 CLI，若 agent 按目标把买入编码为 `side=1`，该值是合法卖出；显式纠正 price-type 不能修复方向错误。全平则可能直接失败。先读 help 的要求有助发现冲突，但不能把错误的固定语义变成正确契约，也没有实际 Agent 轨迹证明它总能拦截。
- 来源差异：本次公开 `gate-cli/main/cmd/cex/tradfi/order.go` 的抓取版本仍有旧枚举，与目标近似；这证明存在版本差异，不能声称所有公开 CLI 都使用基线枚举。与公开 SDK v7.2.167 也存在差异，必须核实 handler/SDK 线上的真实映射，不能只相信 help。
- 修正：按指定基线建立一致字段契约，先验证所用二进制、handler、SDK/API 版本；存在关键语义冲突时停止操作，不自动切换版本或转换未知枚举。
- 验证：合成买/卖、market/trigger、全平/部分平仓四类意图到实际 argv/request 的断言；相反方向不得发出。旧版本或语义未知时必须无写入。
- 公开证据：[下单模型](https://raw.githubusercontent.com/gate/gateapi-go/v7.2.167/model_trad_fi_order_request.go)、[平仓模型](https://raw.githubusercontent.com/gate/gateapi-go/v7.2.167/model_trad_fi_close_position_request.go)。

### F2 · P1 · CFD 单侧 TP/SL 修改没有保留另一侧保护的约束

- 位置：`references/tradfi.md:22-26`；关联 `workflows.md:95-99`。置信度：高。
- 目标说明修改 TP/SL，且只特别要求 order update 回传旧 price；全文没有说明省略 TP/SL 会清除原保护，也没有要求读出并回传未修改的一侧。
- SDK 的 `TradFiOrderUpdateRequest` 和 `TradFiPositionUpdateRequest` 明确：省略或传 `0` 会清除相应保护。CLI 对未提供的 `--tp/--sl` 保持 nil，序列化时省略。
- 可达反例：已有 TP 和 SL，用户只要求修改 TP；按目标允许的 `position update --id ... --tp ...` 不带 SL，会触发清除止损语义。用户对新 TP 的确认不等于批准撤销 SL；事后查询也不能消除已经出现的无保护窗口。
- 修正：操作前读同一订单/仓位的两侧保护，明确保持与清除意图，显式回传仍需保留的一侧；读取失败、对象变化或保留值不确定时停止。订单价格若会被同时提交，也应纳入明确授权，不能把陈旧价格无条件写回。
- 验证：已有双侧保护时仅改 TP、仅改 SL、明确取消一侧、读取失败及状态变化；断言未请求修改的保护保持。此处是契约核验，未实际发送保护修改。
- 公开证据：[持仓修改模型](https://raw.githubusercontent.com/gate/gateapi-go/v7.2.167/model_trad_fi_position_update_request.go)。

### F3 · P1 · 仍依赖旧 Skill 体系，无法按当前架构独立安全执行

- 位置：`SKILL.md:12-20,26-36`；`workflows.md:67-71`；`market.md:29-34`；`options.md:37,76-87`；`vipfee.md:19-32`。置信度：高。
- 入口要求先安装并读取 `gate-exchange-*` 的 runtime，否则禁止写；本包只有 13 个 Markdown，没有六个 `references/_shared/cex/{preflight,cli-setup,cli-auth,execution-cli,safety,templates}.md`，也无等效完整内置约束。这不是仅因命名不同而失败。
- 基线要求当前 trade 独立拥有 spot/Alpha/股票/CFD 等写操作。目标却把 Alpha 交给旧 `gate-exchange-alpha`，市场分析依赖旧 analysis Skill，MCL 找旧 mcl Skill；正确的独立贷款责任组件是 `gate-cex-earn`。
- 目标还允许 CLI/MCP 合同、执行“documented command or API operation”、无 CLI 时使用 API/WS route；不存在统一的官方 CLI-only 执行边界。REST 作为资料索引本身不违规，违规是将其转为替代执行通道。
- 缺失共享契约的实际影响：没有有效 HMAC/OAuth 来源优先级、同 origin 的有效 trading UID 验证、scope 与用户授权分离、授权有效期/累计限额、argv 防注入、输出/分页/进程上限及不可信内容边界。WS 表里的 UID 不等于 REST 私有任务身份核验。缺旧 Skill 时写操作会被阻塞；存在旧 Skill 时，其未知外部规则也不能被本次审查视为已满足。
- 修正：按基线重新组织独立 trade 与包内共享规则，通过真实注册 CLI 执行业务；只对资产转移、独立贷款等跨责任域操作转交当前拥有者，不要求安装其他五个包才能交易，不下载私有 runtime 补洞。
- 验证：仅安装本包，合成现货/Alpha 正常流程可解析；其他包缺失不影响自身业务；跨域写保持正确 handoff；身份不匹配、未授权 transport、恶意行情/错误文字均不得导致写入或权限扩张。

### F4 · P1 · 旧快照的覆盖范围和“不支持”结论替代了指定基线

- 位置：`SKILL.md:28-35,49`；`spot.md:122-125`；`options.md:23,129`；`unified.md:29-37`；`alpha.md:33`；`coverage.md:7-16`。置信度：高。
- 缺少 delivery 的 21 个业务叶子及 8 个 market 叶子，stock 的 13 个专属叶子，POV/chase 的 10 个叶子；没有获批裁剪依据。将股票混入 `tradfi` 不能替代独立 stock shares 契约。
- 基线和独立源码已有 `spot pov`、`futures chase`、options `--close/--reduce-only`、spot `--account/--auto-borrow/--auto-repay` 和 attached protection、unified Delta-neutral/quick-repay/leverage-set-all。目标仍把其中多项写成没有 CLI、API-only 或当前不支持。
- Alpha 的 `/alpha/orders/{id}` 与 `/alpha/orders/quote` 在所核 CLI 中是错误消息的 path 字符串；实际调用 SDK 的 `/alpha/order` 与 `/alpha/quote`。目标据此宣布实际网络适配器不兼容，遗漏了 handler→SDK 的核验链路。
- 尚缺准确单位/变体：Alpha 买入应明确 USDT、custom slippage 是百分数（10 表示 10%），quote/place 必须绑定同 UID/origin/金额/模式；spot 附带保护有 omission/null/{} 差异；quick repayment 的币种选择不是金额上限。这些不能由泛泛“看 help”替代。
- 数量口径：基线分母 282；对全文件 inline 命令及明确缩写作展开后，160 个叶子能定位到文字提及，122 个没有具体叶子映射。提及中包括被禁止的命令及参数不完整项，**不是 160 个正确可用，更不是功能覆盖率**；部分缺叶子项目只有 REST 索引。完整逐项矩阵在附录。
- 修正：按基线逐项建立 owner、真实 CLI、flags/default/required、嵌套请求、输出/access、资金变体和恢复路径；以独立证据修正不支持声明。保留真实未支持的 TWAP/VP 等边界，不为完成表格虚构接口。
- 验证：全部 282 项有正确契约或经用户批准的明确排除；新增变体覆盖正常、拒绝、过期、部分成功、未知结果；公共二进制缺能力时停止并报告，不自动换内部构建。

### F5 · P1 · 闪兑把不同协议泛化为 preview_id，缺少实际 JSON 请求契约

- 位置：`references/flashswap.md:17-21,27-30`；关联 `workflows.md:58,105-107`。置信度：高。
- 目标将 one-to-many/many-to-one create 描述为“JSON preview id and amounts”，通用 workflow 再强制提交 `preview_id`；没有列根字段、嵌套键或请求模型。
- 实际 CLI JSON 解码进入 `FlashSwapMultiCurrencyOneToManyOrderCreateReq` / `ManyToOneOrderCreateReq`，根字段为 `params`，每项有 `sell_asset/sell_amount/buy_asset/buy_amount`。这些模型没有 `preview_id`。标准一对一的字段不能直接搬到多币种请求。
- 触发与后果：按文字构造扁平 preview_id + amounts，typed 解码不会生成有效 params，导致无效请求；即使另行补齐 params，也不能宣称服务端按该未声明 preview_id 锁定了原报价。不得把文档理解与真实报价绑定混为一谈。
- 修正：分别说明标准、v1、一对多、多对一的准确 schema、报价有效性及对应约束、逐项错误和总额/余额核验。没有实际引用字段的协议不能虚构 quote ID 保证；金额精确、授权边界及必要的再确认仍需成立。
- 验证：各变体合成输入→SDK 序列化→请求形状断言；缺 params、未知字段、失败 item、陈旧报价和部分结果均有正确处理；不可依赖不存在的字段承诺价格。
- 公开证据：[多币种根模型](https://raw.githubusercontent.com/gate/gateapi-go/v7.2.167/model_flash_swap_multi_currency_one_to_many_order_create_req.go)、[每项字段](https://raw.githubusercontent.com/gate/gateapi-go/v7.2.167/model_flash_swap_multi_currency_create_param.go)。

### F6 · P2 · 公开包包含内部来源和本地检出记录

- 位置：`references/coverage.md:3,24`。置信度：高。
- 内容包含公司 GitLab 来源、认证失败经过、本地隐藏检出路径和固定提交来源。公开内容扫描在该文件报告非公开来源域名；人工补充识别路径及研发过程。
- 这些是内部引用/工程来源，不是可供外部用户依赖的官方公开安装说明。没有发现 API key、token、密码、私钥字面量或实际内网业务服务 IP；不把仓库 hostname 升级描述为凭据泄露。
- 修正：工程证据保留在开发审查记录，公开包仅引用已验证的官方公开 CLI/API 来源；使用 digest 绑定构建证据，不要求用户访问内部检出。
- 验证：对最终目录及生成 manifest/压缩包重新扫描可点击、裸文本和编码内容，并人工核查必需来源的公开可用性。

### F7 · P2 · 无条件写前确认覆盖了已有完整授权

- 位置：`SKILL.md:20`；`references/workflows.md:25,51,69`。置信度：高。
- 即使同 UID、环境、动作、金额和有效期内已有完整明确授权，目标仍要求写前再问一次；没有交互渠道就绝不执行。与指定基线 shared safety/templates 的有效授权复用规则冲突。
- 后果：已授权任务被额外阻塞；再次点击确认不能替代身份、预算、有效期和跨会话权威校验。
- 修正：展示摘要并检查现有授权；仅缺失、超范围、失效或实质参数变化时请求新的授权。报价过期/条件变化需要重新核对，不属于禁止重复确认的例外滥用。
- 验证：完整授权不重复阻塞；账号、金额、环境或有效期变化时新授权前无写入；不以本地计数器冒充跨会话预算控制。

### F8 · P2 · metadata 的规范性描述混入中文

- 位置：`SKILL.md:3`。置信度：高。
- description 的产品/意图路由说明使用中英混合文本，属于规范性描述，不是引述用户请求或本地化输出样例；违反当前业务 Skill 的英文内容规则。
- 建议英文：`Trade Gate spot, Alpha, perpetual and delivery futures, margin, options, stocks, CFDs and conversion; inspect markets, trading settings and fees. Use for explicit trading tasks, not fund transfers or investment products.` 该建议与基线完整范围绑定，须同步修正实际内容，不能仅改描述扩大能力承诺。
- 合法例外：`SKILL.md:17` 的中文用户话语；`workflows.md:19-23` 的用户意图样例及 `113-136` 的中文 toast 模板/示例。上下文明确用于用户语言输入/输出，不报告成中文规范性指令。
- 验证：全文件英文语义审查并记录本地化例外；字符扫描只能定位，不能单独判断违规。

## 4. 文件与业务映射

以下按目标相对路径；全部内容已阅读全文。基线的 13 个标准产品参考、13 个 model 文件、入口和 workflow，加六个共享文件构成不同的发布内容；不是简单链接重写可得到此目标。

| 目标 | 应对照的基线职责 | 审查结果 |
| --- | --- | --- |
| SKILL.md | 入口与十三产品路由 | 旧技能依赖、范围裁剪、元数据语言，F3/F4/F7/F8 |
| references/workflows.md | order-workflows + shared execution/safety | 有超时不重放、部分失败、状态区分优点；缺共享身份/预算/注入边界，确认强制，F3/F7 |
| references/coverage.md | 工程覆盖记录应放包外 | 不支持声明过时，内部来源，F4/F6 |
| references/spot.md | spot + 部分 market + algo | 买入 quote/base 语义正确；账户/自动借还/保护/POV 声明过时，F4 |
| references/alpha.md | alpha | 九项有提及，缺完整 flags/单位约束；旧 handoff 和错误路径阻塞判断，F3/F4 |
| references/margin.md | margin | 部分命令缩写存在；不完整生命周期与旧账户字段限制，F4 |
| references/futures.md | perpetual + 部分 market + algo | 拒绝非 USDT 的范围与基线不符，chase 无具体 CLI；保留未知写不重放及减仓验收 |
| references/options.md | options + 部分 market | 正确区分 close history 与实际平仓；实际平仓 flags 被标成没有，F4；WS 属非基线执行通道，F3 |
| references/unified.md | unified | Delta-neutral/quick repayment 等无映射；没有真实金额上限和批量失败语义，F4 |
| references/flashswap.md | convert + models/convert | 十一项有提及，schema 泛化错误，F5 |
| references/tradfi.md | cfd；不能替代 stocks | 枚举和保留保护错误，F1/F2；独立 stock 及其 shares 语义缺失，F4 |
| references/vipfee.md | vip-fees；MCL 归 earn | MCL 无正确拥有者 handoff；六项 fee/设置叶子没有映射，F3/F4 |
| references/market.md | market | 部分 REST/CLI 行可用，delivery/stock 专有路由不能靠 TradFi 标签覆盖；实际缺项以逐命令附录为准 |
| 缺 delivery-commands.md | delivery | 21 个专属业务叶子及 8 个 market 叶子没有具体 CLI 映射 |
| 缺 stocks-commands.md | stocks | 13 个专属业务叶子没有具体 CLI 映射 |
| 缺 algo-commands.md | POV/chase | 10 个算法叶子缺失；REST 概述不满足 CLI 生命周期 |
| 缺 references/_shared/cex 六文件 | preflight/setup/auth/execution/safety/templates | 没有完整自包含替代，F3 |
| 缺 models/ 各产品模型 | 嵌套请求/响应和省略语义 | 裸字段或泛化 JSON 没有补足实际协议，F1/F2/F5 |

## 5. 实际执行、推演和未验证范围

| 检查 | 层级与结果 |
| --- | --- |
| 远端分支身份 | 实际运行只读 git ls-remote，基线 ba390fe；没有 fetch/switch/reset 或更新被审查分支 |
| 全文件清单、大小、SHA-256 | 实际 Python 标准库读取，13 文件，无链接或非 Markdown；清单见附录 |
| frontmatter | 实际 safe YAML + duplicate-key 检查通过；metadata.version 为字符串 |
| 本地引用 | 实际检查 12 个 Markdown 本地链接，全部存在、无 fragment；正文反引号中的目标内部文件路径也经阅读全文核对；旧外部 Skill/runtime 依赖不能因此算通过 |
| 公开内容 | 从可信基线 AST 提取并执行已阅读的纯字符串 public_dependency_errors；coverage 命中，未发现凭据字面量。未执行目标提供的任何代码 |
| CLI 对照 | 实际读取 JSON 导出并对全文件命令与明确缩写展开；160 项仅有提及，122 项未定位具体叶子；人工对资金方向、保护、FlashSwap、关键新增 flags/handler/SDK 复核 |
| checker 全入口 | **NOT_EVALUATED**：系统 Python 有 PyYAML，缺 markdown_it；内置 runtime 两者均不提供。未安装依赖，未伪称运行完整 checker 或 builder；纯函数扫描不是整个检查器运行 |
| 安装包构建 | **NOT_EVALUATED**：本任务审查已有目录，没有重新构建或生成替代包 |
| CLI 命令/后端业务/登录/真实账户 | **NOT_EVALUATED**：零调用；无真实下单、改单、撤单、转账、借还或凭据读取 |

可重复读取入口如下；均为只读，不能替代业务测试：

```sh
# 固定基线并检查所用契约，避免把本地当前分支当成远端基线。
git ls-remote origin refs/heads/gate-skill-2.0
git show ba390fe6999026cd0d7328a4baac4eed788bd27a:tests/cex/cli-contract.json
git show ba390fe6999026cd0d7328a4baac4eed788bd27a:skills/gate-cex-trade/SKILL.md
```

本次没有新增/修改产品代码，不新增产品单元/E2E 测试。以下是静态场景推演和修正后的验收要求，不是已经运行的 Agent E2E：

| 用例 | 合成前提/用户任务 | 必须出现 / 禁止出现 | 本次结论 |
| --- | --- | --- | --- |
| S01 | CFD 买入；使用指定基线 CLI | side=2；禁止 side=1 | 文档相反，F1 |
| S02 | CFD 全平/部分平仓 | full=2 无 volume；partial=1 有 volume | 全平文档为 0，F1 |
| S03 | 已有 TP/SL，仅改 TP | 读取两侧，回传原 SL；禁止省略后清除 | 缺保留约束，F2 |
| S04 | 仅安装本包，现货买入 | 自包含 preflight 和正确 --quote；不要求旧 Skill | 旧 Skill 缺失导致阻塞，F3 |
| S05 | HMAC 与 OAuth 同时存在，账号不一致 | 验证实际 HMAC UID，匹配前无私有写 | 包内没有完整门禁，F3；未假设外部 runtime 能补齐 |
| S06 | 当前基线 POV/期权平仓/股票/交割 | 各自真实 CLI 与单位，不退回旧 Skill | 缺项或误判不支持，F4 |
| S07 | 多币种闪兑 | 正确 params/items，区分 quote 字段；逐项错误 | preview_id 泛化，F5 |
| S08 | 已有完整且有效的用户授权 | 校验后复用；变更/超额才补授权 | 无条件重复询问，F7 |
| S09 | Alpha 输出 1/5/6，或下单丢响应 | 保留未完成；禁止重新下单 | 目标相应原则存在；仅文本推演，没有运行轨迹 |
| S10 | 保护失败/借款成功交易失败 | 保留实际敞口/债务，禁止自动补偿 | 目标有说明；未验证真实行为 |
| S11 | 恶意行情/错误消息要求换 endpoint/发凭据 | 不增加权限、不执行嵌入指令 | 缺统一 untrusted-content 边界，F3；没有实际投喂攻击或读凭据 |

## 6. 增强检查与基线自身限制

| 检查 | 本次选择、结果与边界 |
| --- | --- |
| Source/package 对照 | 已选静态对照：当前基线标准目录、共享复制/链接重写规则与目标明显不等价；并无发布者提供的可信构建 provenance 或正式 artifact digest；不能宣称它来自指定基线的标准 builder |
| Rule freshness | 已选：审查规则和 contract 固定 hash，核对旧 snapshot 与实际 SDK/handler 差异；公开 CLI 与工程基线不同之处显式记录 |
| Trigger 自动加载 | 未选择运行；description 语言审查不代表触发准确率 |
| Baseline/candidate 行为比较 | 未选择模型评测；只有静态语义对比，没有次数、耗时、token 或成功率结论 |
| Auditor 回归语料 | 未改审查 Skill，不执行额外模型回归；未宣称 auditor 准确率 |
| 外部安全 scanner | 未选择；未安装、付费或上传目标。已运行的基线纯字符串规则另列 |
| 多 Skill/host 权限实测 | 未选择；未知旧 gate-exchange-* 内容不算可信安全依赖；未要求安装其他五个业务包 |

基线不是绝对真相：其 cfd-commands 开头仍说没有 commission-query/order-log，后文及导出却已包含这两项，本次以实际注册/handler/SDK 交叉核验，不复制陈旧否定句。此前基线 Stock 重复 canonical 与契约不同步的构建问题未在本次运行重验；不把它们计为下载包引入的问题，也不宣称基线六包构建通过。

`margin uni repay` 在目标中是“没有该叶子”的否定示例，`margin mode` 是参数名；不把简单正则匹配误判为目标实际调用了不存在命令。公开 options WebSocket 地址不等于内部服务泄露；它的问题是执行通道/兼容性未按 CLI-only 契约建立，不属于已证实的凭据外传。

## 7. 修正与复审要求

先修正 CFD 枚举和 TP/SL 保留语义，再按基线重建独立 Skill/共享运行时与 owner 边界；同步完整业务范围和输入/输出契约，分别纠正闪兑变体；清除公开包的内部来源；保留有效授权复用并修正英文 metadata。修复须另行授权，本次不改目标。

复审必须重新读变更后的全部目标/依赖，复跑 source/package closure 与 disclosure，对真实分发文件做 hash/映射核验；有可信隔离执行条件后运行上述合成场景。没有真实环境授权前不运行交易。格式通过、命令提及或构建通过均不能替代正确资金语义与独立可用性。

本报告按用户 2026-10-29 更新后的留档要求存放并精确提交到当前本地分支；不 push、不修改下载包、CLI/SDK 或其他工作树，不写 docs/config。没有新增配置或一次性落盘脚本/下载/测试产物。


## 附录 A：目标文件清单及内容身份

按文件名排序的 `(relative_path, bytes, sha256)` JSON 清单摘要：`8f18efa323d2c889d478706b4cf76e87fa6a58ab069d538a253ae0f9c2d7426b`。该摘要用于绑定本次审查，不是发行者签名。

| 文件 | 字节数 | SHA-256 |
| --- | ---: | --- |
| `SKILL.md` | 9126 | `656dccfb38199bf79fca35532b3bbfc363d349933064b93c48c65cfbf952dfe5` |
| `references/alpha.md` | 3308 | `fe0b89f9a417bffbccd2015ad7fac83a6eab14eb1e96b41177bb34db1cd2d37c` |
| `references/coverage.md` | 3333 | `d1bdd119a4633dd8f27df0f314865911dfb36f8e3e28d35d4bfcc04d25837b49` |
| `references/flashswap.md` | 3952 | `4104ce5fd6621b27de786ed05c5efc01d495143ed5b3e0ccedfdd7fb6fce9e39` |
| `references/futures.md` | 16297 | `e6b7b66a1dab69c8b761642ea9eb7ccf7b850ca8529cac1a358125f6e1f8df43` |
| `references/margin.md` | 4029 | `23ebc4f0206b3583099e9b0baa98c92163d86fb696c48e26ad13c6144b2c7f8b` |
| `references/market.md` | 4131 | `da907ad8770257357b3d38014787d3482ec725041946ab652371526a1b4c27e5` |
| `references/options.md` | 12386 | `620488e25a4ae13a2f3075baa3639f3d36bb0525050d8677fa6d7ac9ca2dc0f0` |
| `references/spot.md` | 10761 | `c3b668dc7dffe2595805cac56b1fe3bf97cbed597148e54cef965ed898f8c57d` |
| `references/tradfi.md` | 5579 | `cb8fe4697808d594265d88a9803e17ae72dacf914edc966123ed39c240503291` |
| `references/unified.md` | 5835 | `f1810152c5d57a843e29be92187b71b1fac160be9f9ff1bea7db3cda85b6639c` |
| `references/vipfee.md` | 3563 | `fbf35e96b6416926a6509bccce088a34b3dad95da70fe8b42b0842fd009e35cd` |
| `references/workflows.md` | 15291 | `8c1e551cad398bfb957b925fac46c734b796887752869485340441ca8d98581d` |

## 附录 B：基线完整命令矩阵

分母来自指定基线工程导出。以下“提及”只代表文件中可定位到该叶子，不能证明参数/单位/权限/返回正确，也包含明确禁止执行的提及。没有具体叶子映射的项目可能有 REST 路径说明，不能把这张表说成业务完全未提及清单。统一省略命令前缀 `gate-cli cex`。

| 基线 owning reference | CLI 叶子 | 目标定位 / 状态 |
| --- | --- | --- |
| `algo-commands.md` | `futures chase create` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `algo-commands.md` | `futures chase get` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `algo-commands.md` | `futures chase list` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `algo-commands.md` | `futures chase stop` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `algo-commands.md` | `futures chase stop-all` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `algo-commands.md` | `spot pov cancel` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `algo-commands.md` | `spot pov cancel-all` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `algo-commands.md` | `spot pov create` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `algo-commands.md` | `spot pov get` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `algo-commands.md` | `spot pov list` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `alpha-commands.md` | `alpha account balances` | 仅提及：`references/alpha.md:16` |
| `alpha-commands.md` | `alpha account book` | 仅提及：`references/alpha.md:17` |
| `alpha-commands.md` | `alpha market currencies` | 仅提及：`references/alpha.md:13` |
| `alpha-commands.md` | `alpha market tickers` | 仅提及：`references/alpha.md:15` |
| `alpha-commands.md` | `alpha market tokens` | 仅提及：`references/alpha.md:14` |
| `alpha-commands.md` | `alpha order get` | 仅提及：`references/alpha.md:19` |
| `alpha-commands.md` | `alpha order list` | 仅提及：`references/alpha.md:18` |
| `alpha-commands.md` | `alpha order place` | 仅提及：`references/alpha.md:21` |
| `alpha-commands.md` | `alpha order quote` | 仅提及：`references/alpha.md:20` |
| `cfd-commands.md` | `tradfi account assets` | 仅提及：`references/tradfi.md:19` |
| `cfd-commands.md` | `tradfi account info` | 仅提及：`references/tradfi.md:18` |
| `cfd-commands.md` | `tradfi market categories` | 仅提及：`references/market.md:15` |
| `cfd-commands.md` | `tradfi market commissions` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `cfd-commands.md` | `tradfi market kline` | 仅提及：`references/market.md:15` |
| `cfd-commands.md` | `tradfi market symbol` | 仅提及：`references/market.md:15` |
| `cfd-commands.md` | `tradfi market symbols` | 仅提及：`references/market.md:15` |
| `cfd-commands.md` | `tradfi market ticker` | 仅提及：`references/market.md:15` |
| `cfd-commands.md` | `tradfi order cancel` | 仅提及：`references/tradfi.md:23` |
| `cfd-commands.md` | `tradfi order create` | 仅提及：`references/tradfi.md:21` |
| `cfd-commands.md` | `tradfi order history` | 仅提及：`references/tradfi.md:24` |
| `cfd-commands.md` | `tradfi order list` | 仅提及：`references/tradfi.md:20` |
| `cfd-commands.md` | `tradfi order log` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `cfd-commands.md` | `tradfi order update` | 仅提及：`references/tradfi.md:22` |
| `cfd-commands.md` | `tradfi position close` | 仅提及：`references/tradfi.md:27` |
| `cfd-commands.md` | `tradfi position history` | 仅提及：`references/tradfi.md:28` |
| `cfd-commands.md` | `tradfi position list` | 仅提及：`references/tradfi.md:25` |
| `cfd-commands.md` | `tradfi position update` | 仅提及：`references/tradfi.md:26` |
| `convert-commands.md` | `flash-swap create` | 仅提及：`references/flashswap.md:15` |
| `convert-commands.md` | `flash-swap create-many-to-one` | 仅提及：`references/flashswap.md:21` |
| `convert-commands.md` | `flash-swap create-one-to-many` | 仅提及：`references/flashswap.md:19` |
| `convert-commands.md` | `flash-swap create-v1` | 仅提及：`references/flashswap.md:17` |
| `convert-commands.md` | `flash-swap order` | 仅提及：`references/flashswap.md:23` |
| `convert-commands.md` | `flash-swap orders` | 仅提及：`references/flashswap.md:22` |
| `convert-commands.md` | `flash-swap pairs` | 仅提及：`references/flashswap.md:13` |
| `convert-commands.md` | `flash-swap preview` | 仅提及：`references/flashswap.md:14` |
| `convert-commands.md` | `flash-swap preview-many-to-one` | 仅提及：`references/flashswap.md:20` |
| `convert-commands.md` | `flash-swap preview-one-to-many` | 仅提及：`references/flashswap.md:18` |
| `convert-commands.md` | `flash-swap preview-v1` | 仅提及：`references/flashswap.md:16` |
| `delivery-commands.md` | `delivery account book` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery account get` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery order cancel` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery order cancel-all` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery order create` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery order get` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery order list` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery order my-trades` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery position close` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery position get` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery position liquidates` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery position list` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery position settlements` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery position update-leverage` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery position update-margin` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery position update-risk-limit` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery price-trigger cancel` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery price-trigger cancel-all` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery price-trigger create` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery price-trigger get` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `delivery-commands.md` | `delivery price-trigger list` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `margin-commands.md` | `margin account book` | 仅提及：`references/margin.md:27` |
| `margin-commands.md` | `margin account funding` | 仅提及：`references/margin.md:27` |
| `margin-commands.md` | `margin account list` | 仅提及：`references/margin.md:13` |
| `margin-commands.md` | `margin account transferable` | 仅提及：`references/margin.md:27` |
| `margin-commands.md` | `margin account user-info` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `margin-commands.md` | `margin auto-repay get` | 仅提及：`references/margin.md:27` |
| `margin-commands.md` | `margin auto-repay set` | 仅提及：`references/margin.md:27` |
| `margin-commands.md` | `margin cross loans` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `margin-commands.md` | `margin cross repayments` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `margin-commands.md` | `margin leverage set` | 仅提及：`references/margin.md:27` |
| `margin-commands.md` | `margin tier market` | 仅提及：`references/margin.md:27` |
| `margin-commands.md` | `margin tier user` | 仅提及：`references/margin.md:27` |
| `margin-commands.md` | `margin uni borrowable` | 仅提及：`references/margin.md:27` |
| `margin-commands.md` | `margin uni estimate-rate` | 仅提及：`references/margin.md:27` |
| `margin-commands.md` | `margin uni interest-records` | 仅提及：`references/margin.md:27` |
| `margin-commands.md` | `margin uni lend` | 仅提及：`references/margin.md:22` |
| `margin-commands.md` | `margin uni loan-records` | 仅提及：`references/margin.md:27` |
| `margin-commands.md` | `margin uni loans` | 仅提及：`references/margin.md:27` |
| `margin-commands.md` | `margin uni pair` | 仅提及：`references/margin.md:27` |
| `margin-commands.md` | `margin uni pairs` | 仅提及：`references/margin.md:27` |
| `margin-commands.md` | `spot order cross-liquidate` | 仅提及：`references/spot.md:35` |
| `margin-commands.md` | `unified loan create` | 仅提及：`references/unified.md:22` |
| `margin-commands.md` | `unified loan history-rate` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `margin-commands.md` | `unified loan interest` | 仅提及：`references/unified.md:24` |
| `margin-commands.md` | `unified loan list` | 仅提及：`references/unified.md:21` |
| `margin-commands.md` | `unified loan records` | 仅提及：`references/unified.md:23` |
| `market-commands.md` | `delivery market candlesticks` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `delivery market contract` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `delivery market contracts` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `delivery market insurance` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `delivery market order-book` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `delivery market risk-limit-tiers` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `delivery market tickers` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `delivery market trades` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `futures market adl-risk-states` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `futures market batch-funding-rates` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `futures market candlesticks` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `futures market contract` | 仅提及：`references/futures.md:13` |
| `market-commands.md` | `futures market contracts` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `futures market contracts-all` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `futures market funding-rate` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `futures market index-constituents` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `futures market insurance` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `futures market liquidations` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `futures market orderbook` | 仅提及：`references/futures.md:15` |
| `market-commands.md` | `futures market premium` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `futures market risk-limit-table` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `futures market risk-limit-tiers` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `futures market rpi-orderbook` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `futures market stats` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `futures market ticker` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `futures market tickers` | 仅提及：`references/futures.md:14` |
| `market-commands.md` | `futures market trades` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `options market candlesticks` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `options market contract` | 仅提及：`references/market.md:14` |
| `market-commands.md` | `options market contracts` | 仅提及：`references/market.md:14` |
| `market-commands.md` | `options market expirations` | 仅提及：`references/market.md:14` |
| `market-commands.md` | `options market order-book` | 仅提及：`references/market.md:14` |
| `market-commands.md` | `options market settlement` | 仅提及：`references/options.md:33` |
| `market-commands.md` | `options market settlements` | 仅提及：`references/options.md:32` |
| `market-commands.md` | `options market tickers` | 仅提及：`references/market.md:14` |
| `market-commands.md` | `options market trades` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `options market underlying-candlesticks` | 仅提及：`references/options.md:36` |
| `market-commands.md` | `options market underlying-tickers` | 仅提及：`references/options.md:35` |
| `market-commands.md` | `options market underlyings` | 仅提及：`references/market.md:14` |
| `market-commands.md` | `spot market candlesticks` | 仅提及：`references/market.md:11` |
| `market-commands.md` | `spot market currencies` | 仅提及：`references/market.md:11` |
| `market-commands.md` | `spot market currency` | 仅提及：`references/market.md:11` |
| `market-commands.md` | `spot market insurance` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `spot market orderbook` | 仅提及：`references/market.md:11` |
| `market-commands.md` | `spot market pair` | 仅提及：`references/market.md:11` |
| `market-commands.md` | `spot market pairs` | 仅提及：`references/market.md:11` |
| `market-commands.md` | `spot market rpi-orderbook` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `spot market ticker` | 仅提及：`references/market.md:11` |
| `market-commands.md` | `spot market tickers` | 仅提及：`references/market.md:11` |
| `market-commands.md` | `spot market time` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `market-commands.md` | `spot market trades` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `options-commands.md` | `options account book` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `options-commands.md` | `options account get` | 仅提及：`references/options.md:19` |
| `options-commands.md` | `options account settlements` | 仅提及：`references/options.md:31` |
| `options-commands.md` | `options mmp get` | 仅提及：`references/options.md:27` |
| `options-commands.md` | `options mmp reset` | 仅提及：`references/options.md:29` |
| `options-commands.md` | `options mmp set` | 仅提及：`references/options.md:28` |
| `options-commands.md` | `options order amend` | 仅提及：`references/options.md:26` |
| `options-commands.md` | `options order cancel` | 仅提及：`references/options.md:24` |
| `options-commands.md` | `options order cancel-all` | 仅提及：`references/options.md:25` |
| `options-commands.md` | `options order countdown-cancel-all` | 仅提及：`references/options.md:30` |
| `options-commands.md` | `options order create` | 仅提及：`references/options.md:23` |
| `options-commands.md` | `options order get` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `options-commands.md` | `options order list` | 仅提及：`references/options.md:22` |
| `options-commands.md` | `options position close` | 仅提及：`references/options.md:34` |
| `options-commands.md` | `options position get` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `options-commands.md` | `options position list` | 仅提及：`references/options.md:20` |
| `options-commands.md` | `options position my-trades` | 仅提及：`references/options.md:21` |
| `perpetual-commands.md` | `futures account book` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures account dual-mode` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures account get` | 仅提及：`references/futures.md:16` |
| `perpetual-commands.md` | `futures account position-mode` | 仅提及：`references/futures.md:19` |
| `perpetual-commands.md` | `futures order add` | 仅提及：`references/futures.md:24` |
| `perpetual-commands.md` | `futures order amend` | 仅提及：`references/futures.md:27` |
| `perpetual-commands.md` | `futures order batch-amend` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures order batch-cancel` | 仅提及：`references/futures.md:29` |
| `perpetual-commands.md` | `futures order batch-create` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures order bbo` | 仅提及：`references/futures.md:30` |
| `perpetual-commands.md` | `futures order cancel` | 仅提及：`references/futures.md:28` |
| `perpetual-commands.md` | `futures order close` | 仅提及：`references/futures.md:25` |
| `perpetual-commands.md` | `futures order countdown-cancel-all` | 仅提及：`references/futures.md:31` |
| `perpetual-commands.md` | `futures order get` | 仅提及：`references/futures.md:20` |
| `perpetual-commands.md` | `futures order list` | 仅提及：`references/futures.md:21` |
| `perpetual-commands.md` | `futures order list-timerange` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures order long` | 仅提及：`references/futures.md:22` |
| `perpetual-commands.md` | `futures order my-trades` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures order my-trades-timerange` | 仅提及：`references/futures.md:48` |
| `perpetual-commands.md` | `futures order remove` | 仅提及：`references/futures.md:26` |
| `perpetual-commands.md` | `futures order short` | 仅提及：`references/futures.md:23` |
| `perpetual-commands.md` | `futures position adl` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures position close-history` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures position get` | 仅提及：`references/futures.md:17` |
| `perpetual-commands.md` | `futures position get-dual` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures position leverage` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures position liquidates` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures position list` | 仅提及：`references/futures.md:18` |
| `perpetual-commands.md` | `futures position list-timerange` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures position update-contract-leverage` | 仅提及：`references/futures.md:40` |
| `perpetual-commands.md` | `futures position update-cross-mode` | 仅提及：`references/futures.md:39` |
| `perpetual-commands.md` | `futures position update-dual-cross-mode` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures position update-dual-leverage` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures position update-dual-margin` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures position update-dual-risk-limit` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures position update-leverage` | 仅提及：`references/futures.md:38` |
| `perpetual-commands.md` | `futures position update-margin` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures position update-risk-limit` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `perpetual-commands.md` | `futures price-trigger cancel` | 仅提及：`references/futures.md:36` |
| `perpetual-commands.md` | `futures price-trigger cancel-all` | 仅提及：`references/futures.md:37` |
| `perpetual-commands.md` | `futures price-trigger create` | 仅提及：`references/futures.md:32` |
| `perpetual-commands.md` | `futures price-trigger get` | 仅提及：`references/futures.md:34` |
| `perpetual-commands.md` | `futures price-trigger list` | 仅提及：`references/futures.md:33` |
| `perpetual-commands.md` | `futures price-trigger update` | 仅提及：`references/futures.md:35` |
| `perpetual-commands.md` | `futures trail create` | 仅提及：`references/futures.md:41` |
| `perpetual-commands.md` | `futures trail get` | 仅提及：`references/futures.md:45` |
| `perpetual-commands.md` | `futures trail list` | 仅提及：`references/futures.md:44` |
| `perpetual-commands.md` | `futures trail log` | 仅提及：`references/futures.md:47` |
| `perpetual-commands.md` | `futures trail stop` | 仅提及：`references/futures.md:42` |
| `perpetual-commands.md` | `futures trail stop-all` | 仅提及：`references/futures.md:43` |
| `perpetual-commands.md` | `futures trail update` | 仅提及：`references/futures.md:46` |
| `spot-commands.md` | `spot account book` | 仅提及：`references/spot.md:25` |
| `spot-commands.md` | `spot account get` | 仅提及：`references/spot.md:24` |
| `spot-commands.md` | `spot account list` | 仅提及：`references/spot.md:23` |
| `spot-commands.md` | `spot order all-open` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `spot-commands.md` | `spot order amend` | 仅提及：`references/spot.md:30` |
| `spot-commands.md` | `spot order batch-amend` | 仅提及：`references/spot.md:31` |
| `spot-commands.md` | `spot order batch-cancel` | 仅提及：`references/spot.md:33` |
| `spot-commands.md` | `spot order batch-create` | 仅提及：`references/spot.md:34` |
| `spot-commands.md` | `spot order buy` | 仅提及：`references/margin.md:9` |
| `spot-commands.md` | `spot order cancel` | 仅提及：`references/spot.md:32` |
| `spot-commands.md` | `spot order countdown-cancel-all` | 仅提及：`references/spot.md:36` |
| `spot-commands.md` | `spot order get` | 仅提及：`references/spot.md:21` |
| `spot-commands.md` | `spot order list` | 仅提及：`references/spot.md:20` |
| `spot-commands.md` | `spot order my-trades` | 仅提及：`references/spot.md:22` |
| `spot-commands.md` | `spot order sell` | 仅提及：`references/margin.md:9` |
| `spot-commands.md` | `spot price-trigger cancel` | 仅提及：`references/spot.md:40` |
| `spot-commands.md` | `spot price-trigger cancel-all` | 仅提及：`references/spot.md:41` |
| `spot-commands.md` | `spot price-trigger create` | 仅提及：`references/spot.md:37` |
| `spot-commands.md` | `spot price-trigger get` | 仅提及：`references/spot.md:38` |
| `spot-commands.md` | `spot price-trigger list` | 仅提及：`references/spot.md:39` |
| `stocks-commands.md` | `stock account assets` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `stocks-commands.md` | `stock market exchanges` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `stocks-commands.md` | `stock market orderbook` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `stocks-commands.md` | `stock market symbol` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `stocks-commands.md` | `stock market symbols` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `stocks-commands.md` | `stock order cancel` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `stocks-commands.md` | `stock order cancel-all` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `stocks-commands.md` | `stock order create` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `stocks-commands.md` | `stock order history` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `stocks-commands.md` | `stock order list` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `stocks-commands.md` | `stock order update` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `stocks-commands.md` | `stock position close` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `stocks-commands.md` | `stock position list` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `unified-commands.md` | `account detail` | 仅提及：`references/vipfee.md:11` |
| `unified-commands.md` | `account stp add-users` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `unified-commands.md` | `account stp create` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `unified-commands.md` | `account stp list` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `unified-commands.md` | `account stp remove-user` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `unified-commands.md` | `account stp users` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `unified-commands.md` | `unified account currencies` | 仅提及：`references/unified.md:20` |
| `unified-commands.md` | `unified account get` | 仅提及：`references/unified.md:13` |
| `unified-commands.md` | `unified config collateral` | 仅提及：`references/unified.md:28` |
| `unified-commands.md` | `unified config delta-neutral-get` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `unified-commands.md` | `unified config delta-neutral-set` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `unified-commands.md` | `unified config discount-tiers` | 仅提及：`references/unified.md:27` |
| `unified-commands.md` | `unified config leverage-config` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `unified-commands.md` | `unified config leverage-get` | 仅提及：`references/unified.md:25` |
| `unified-commands.md` | `unified config leverage-set` | 仅提及：`references/unified.md:26` |
| `unified-commands.md` | `unified config leverage-set-all` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `unified-commands.md` | `unified config loan-tiers` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `unified-commands.md` | `unified loan quick-estimate` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `unified-commands.md` | `unified loan quick-repay` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `unified-commands.md` | `unified mode get` | 仅提及：`references/unified.md:14` |
| `unified-commands.md` | `unified mode set` | 仅提及：`references/unified.md:15` |
| `unified-commands.md` | `unified query borrowable` | 仅提及：`references/unified.md:16` |
| `unified-commands.md` | `unified query borrowable-list` | 仅提及：`references/unified.md:17` |
| `unified-commands.md` | `unified query estimate-rate` | 仅提及：`references/unified.md:19` |
| `unified-commands.md` | `unified query transferable` | 仅提及：`references/unified.md:18` |
| `unified-commands.md` | `unified query transferables` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `unified-commands.md` | `unified risk calculate` | 仅提及：`references/unified.md:36` |
| `unified-commands.md` | `unified risk units` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `vip-fees-commands.md` | `account debit-fee get` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `vip-fees-commands.md` | `account debit-fee set` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `vip-fees-commands.md` | `account rate-limit` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `vip-fees-commands.md` | `futures account fee` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `vip-fees-commands.md` | `spot account batch-fee` | 仅提及：`references/spot.md:26` |
| `vip-fees-commands.md` | `spot account fee` | 未定位具体 CLI 叶子；需补契约或获批排除 |
| `vip-fees-commands.md` | `stock market fee-rate` | 未定位具体 CLI 叶子；需补契约或获批排除 |

附录 B 已对明确的 `a|b` 叶子和 market 同行前缀缩写展开；没有把 REST endpoint 自动算作 CLI 支持。语义判定以正文发现和文件映射为准。
