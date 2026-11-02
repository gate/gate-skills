# Gate CEX 行情 Skill：当前需求与交付口径

2026-10-29，根据用户要求修复测试报告(2)的 BUG-02、BUG-06、BUG-17。
本地验收说明；不代表线上 PRD 已更新。原用户场景不变。
在 gate-skill-2.0 既有交易 Skill 中补充公共行情基础能力，保留交易路由、确认和安全规则；复杂请求由模型编排。

## 独立入口（BUG-02）

`skills/gate-cex-trade/SKILL.md` 是可发现、可单独安装的入口，使用本目录
references 和 scripts；通过既有构建器打包公共依赖后单独安装。
不恢复基线已删除的旧 skills，不引入跨兄弟包引用。

## 当前 CLI 的 CFD 参数（BUG-06）

当前已复测 CLI 为 c127b8a / SDK v7.2.167，其默认 M1 不会转换为 1m。
Skill 查询 1 分钟 K 线必须显式传 `--type 1m`，不能省略或传 M1；其他
周期使用 API 枚举 `1m, 15m, 1h, 4h, 1d, 7d, 30d`。例如：

```sh
gate-cli cex tradfi market kline --symbol XAUUSD --type 1m --limit 3 --format json
```

这解决 Skill/PRD 的调用口径，不代表 CLI 默认值或映射功能已修复。
结果为空、时间陈旧或环境接口失败时，如实披露，不改产品或切环境补数。

## 精简交付清单（BUG-17）

以下是当前验收结构，不要求按旧模板逐字替换 markets.md，也不要求八份分产品文件：

| 文件 | 用途 |
|---|---|
| [SKILL.md](../skills/gate-cex-trade/SKILL.md) | 保留完整交易路由的统一入口 |
| [markets.md](../skills/gate-cex-trade/references/markets.md) | REST/CLI 接口、参数、默认解析、兼容和单位；标题保留 Gate CEX Market Interfaces |
| [streams.md](../skills/gate-cex-trade/references/streams.md) | 共享 WS 总入口及产品小节；Alpha 明确无已确认 WS |
| [futures-streams.md](../skills/gate-cex-trade/references/futures-streams.md) | 永续详细参数及旧入口兼容 |
| [market-commands.md](../skills/gate-cex-trade/references/market-commands.md) / [共享执行规则](../skills/_shared/cex/execution-cli.md) | 复用基线契约，不恢复已删除清单 |
| [public-market-stream.py](../skills/gate-cex-trade/scripts/public-market-stream.py) | 共享有界公共订阅 |
| [futures-market-stream.py](../skills/gate-cex-trade/scripts/futures-market-stream.py) | 旧永续命令兼容 |
| [test_futures_market_stream.py](../skills/gate-cex-trade/scripts/test_futures_market_stream.py) | 既有脚本回归测试 |

Spot/Leverage、Perpetual/Delivery、Options、Stocks、CFD 和 Alpha 由 streams.md
中的同名小节承载；不新增八份重复说明。CrossEx、Flash Swap 和 compatibility
锚点保留，不能为匹配旧标题/模板破坏既有引用。

## 验收边界

- 使用既有构建器生成独立包后，入口、公共依赖、引用和脚本全部随包可用。
- 未修改的 c127b8a CLI 上，模型对 CFD 1m 显式传 1m；不依赖未发布补丁。
- 当前 PRD 修订版和仓库清单、标题、stream 路径相符；原用户场景保持不变。
- 本修订不修复 gate-cli、环境 502、停更、空数据或缺少测试 WS 地址。

完整附件的本地修订副本与测试结果随本次修复报告交付。未获得线上 PRD 可写入口，
故不将本地修订等同于线上原文已更新；线上复测前应替换为本修订口径。
