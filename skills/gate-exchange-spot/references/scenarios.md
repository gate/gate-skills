# Scenarios

本文档按 25 个 case 提供标准化测试输入、接口调用顺序和判断逻辑。

## 一、买币与账户查询 (1-8)

### Scenario 1: 市价买币
- User Prompt: `我想买 100 块钱的 BTC，帮我看看钱够不够，够的话就按现在的价买。`
- Tools: `GET /spot/accounts` → `POST /spot/orders`
- Logic: 检查 USDT 可用余额，足够则创建市价买单。

### Scenario 2: 指定价格买币（限价）
- User Prompt: `买 100 块钱的 BTC，等 BTC 跌到 60000 的时候买。`
- Tools: `GET /spot/accounts` → `POST /spot/orders`
- Logic: 余额足够后创建 `type=limit` 的买单，价格设为 60000。

### Scenario 3: 余额全部买入
- User Prompt: `把我账户里所有的 USDT 全部买成 ETH。`
- Tools: `GET /spot/accounts` → `POST /spot/orders`
- Logic: 读取 USDT 全部可用余额，按当前可执行方式买入 ETH。

### Scenario 4: 币种买入体检
- User Prompt: `我想买 BTC，现在这个币能正常交易吗？买一个要花多少钱？`
- Tools: `GET /spot/currencies/{currency}` → `GET /spot/currency_pairs/{pair}` → `GET /spot/tickers`
- Logic: 检查币种状态、最小交易规则、并返回买 1 个的当前价格。

### Scenario 5: 账户资产简报
- User Prompt: `帮我看看我账户现在总共值多少钱？`
- Tools: `GET /spot/accounts` → `GET /spot/tickers`
- Logic: 将各币种余额按最新价格折算为 USDT 并汇总。

### Scenario 6: 批量撤单
- User Prompt: `帮我把还没成交的单子全撤了，再告诉我剩多少钱。`
- Tools: `DELETE /spot/orders` → `GET /spot/accounts`
- Logic: 一键撤销挂单后查询余额并返回。

### Scenario 7: 零钱卖出换钱
- User Prompt: `把我手里那点 DOGE 全卖了换成 USDT。`
- Tools: `GET /spot/accounts` → `GET /spot/currency_pairs/{pair}` → `POST /spot/orders`
- Logic: 读取 DOGE 全部可用数量，满足最小数量则卖出；不满足则明确提示。

### Scenario 8: 最小买入检查
- User Prompt: `我想买 5 块钱的 ETH，能买吗？`
- Tools: `GET /spot/currency_pairs/{pair}` → `POST /spot/orders`
- Logic: 先校验 `min_quote_amount`，不足（如 <10U）则提示补足，不强制下单。

## 二、智能盯盘与买卖 (9-16)

### Scenario 9: 便宜点再买（限价买）
- User Prompt: `帮我盯着，比现在便宜 2% 的时候帮我买 50U 的 BTC。`
- Tools: `GET /spot/tickers` → `POST /spot/orders`
- Logic: 读取现价，计算目标价 `现价 * 0.98`，创建限价买单。

### Scenario 10: 赚点就卖（限价卖）
- User Prompt: `如果 BTC 涨了 500 块钱，就帮我把手里的币全卖了。`
- Tools: `GET /spot/tickers` → `POST /spot/orders`
- Logic: 目标卖价为 `现价 + 500`，创建限价卖单（数量为持仓可用数量）。

### Scenario 11: 买在今天最低价
- User Prompt: `现在 ETH 是不是今天的最低价？是的话帮我买点。`
- Tools: `GET /spot/tickers` → `POST /spot/orders`
- Logic: 比较当前价与 24h low，接近阈值内时执行买入，否则仅反馈差距。

### Scenario 12: 止损卖出
- User Prompt: `帮我看着，如果 BTC 跌了 5% 就赶紧帮我卖了。`
- Tools: `GET /spot/tickers` → `POST /spot/orders`
- Logic: 基于现价计算止损价 `现价 * 0.95`，创建限价卖单。

### Scenario 13: 跟着涨幅榜买
- User Prompt: `现在哪个币涨得最厉害？帮我买 20 块钱的那个。`
- Tools: `GET /spot/tickers` → `POST /spot/orders`
- Logic: 在可交易币对中选 24h 涨幅最高标的并按 20U 买入。

### Scenario 14: 跌幅榜捡便宜
- User Prompt: `BTC 和 ETH 哪个今天跌得惨？帮我买那个跌得多的。`
- Tools: `GET /spot/tickers` → `POST /spot/orders`
- Logic: 对比 BTC 与 ETH 的 24h 涨跌幅，选择跌幅更大者执行买入。

### Scenario 15: 买完自动挂卖单
- User Prompt: `帮我买 100U 的 BTC，买完后直接在价格高 2% 的地方挂个卖单。`
- Tools: `POST /spot/orders` → `POST /spot/orders`
- Logic: 先买入，后按成交参考价上浮 2% 创建限价卖单。

### Scenario 16: 手续费试算下单
- User Prompt: `我想买 1000U 的币，算上手续费一共要花多少钱？`
- Tools: `GET /wallet/fee` → `GET /spot/tickers`
- Logic: 根据费率与报价估算总成本（本金 + 手续费）并给出最终金额。

## 三、订单管理与改价 (17-25)

### Scenario 17: 未成交就改价
- User Prompt: `我的那个买单还没成交，帮我把价格调高一点。`
- Tools: `GET /spot/open_orders` → `PATCH /spot/orders`
- Logic: 找到目标 open 买单后提高限价，提升成交概率。

### Scenario 18: 交易成交并核实
- User Prompt: `我刚才买 BTC 成功了吗？实际到账了多少个，我现在总共有多少个 BTC？`
- Tools: `GET /spot/my_trades` → `GET /spot/accounts`
- Logic: 读取最近一笔买入成交数量 X，再读取账户总持仓 Y，返回 X 与 Y。

### Scenario 19: 没买到就撤单
- User Prompt: `查查我的 ETH 买单，要是还没买到就帮我撤了，看看钱退回账户没。`
- Tools: `GET /spot/open_orders` → `DELETE /spot/orders` → `GET /spot/accounts`
- Logic: 若该单仍为 open 则撤销，再查询 USDT 余额并确认资金回退。

### Scenario 20: 按上次价格再买点
- User Prompt: `我挺喜欢上次买 BTC 的价格，如果我现在的钱够的话，按那个价格再帮我买 100 块钱的。`
- Tools: `GET /spot/my_trades` → `GET /spot/accounts` → `POST /spot/orders`
- Logic: 取上次成交单价，余额够 100U 则按该价创建限价买单。

### Scenario 21: 帮我算算保本价
- User Prompt: `帮我看看我买 ETH 的成本是多少，如果现在卖掉不亏钱的话，就帮我全卖了。`
- Tools: `GET /spot/my_trades` → `GET /spot/tickers` → `POST /spot/orders`
- Logic: 计算历史买入均价（成本价），若现价高于成本价则执行全卖。

### Scenario 22: 资产置换
- User Prompt: `我想把手里所有的 DOGE 换成 BTC，帮我算算够不够 10 块钱，够的话就帮我换了。`
- Tools: `GET /spot/accounts` → `GET /spot/tickers` → `POST /spot/orders`(卖) → `POST /spot/orders`(买)
- Logic: 先估算 DOGE 总值，>=10U 才执行“先卖 DOGE 再买 BTC”。

### Scenario 23: 价格合适就下单
- User Prompt: `BTC 现在比 60000 便宜吗？要是便宜的话，帮我买 50 块钱的，买完告诉我余额。`
- Tools: `GET /spot/tickers` → `POST /spot/orders` → `GET /spot/accounts`
- Logic: 仅当 `现价 < 60000` 才买，完成后返回最新余额。

### Scenario 24: 行情合适就下单
- User Prompt: `帮我看看 BTC 最近几个小时是不是一直在涨？如果是的话就帮我买 100 块钱的。`
- Tools: `GET /spot/candlesticks` → `POST /spot/orders`
- Logic: 拉取近 4 小时 K 线，若 4 根中至少 3 根收阳则判定趋势向上并买入。

### Scenario 25: 快速成交下单
- User Prompt: `帮我看看现在大家都排在什么价格等着买 ETH？我也想买 50 块钱的，以最快成交方式帮我下单。`
- Tools: `GET /spot/order_book` → `POST /spot/orders`
- Logic: 读取对手盘最优价（ask1），用该价创建限价买单以提升成交速度。
