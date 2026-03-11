# Gate MCP

一键安装所有 Gate MCP 服务器，支持 spot 交易、合约、钱包、行情和新闻查询。

## ✨ 特性

- 🚀 **一键安装** - 默认安装所有 MCP 服务器
- 🔧 **灵活选择** - 支持单独安装某个服务器
- 🔐 **安全配置** - 自动管理 API 密钥
- 📦 **开箱即用** - 下载即可运行

## 📋 包含的 MCP 服务器

| 服务器 | 类型 | 功能 | 认证 |
|--------|------|------|------|
| `gate` | stdio | Spot/Futures/Options 交易 | ✅ API Key + Secret |
| `gate-dex` | HTTP | DEX 操作 | ✅ x-api-key 已内置（MCP_AK_8W2N7Q） |
| `gate-info` | HTTP | 行情数据 | ❌ 无需认证 |
| `gate-news` | HTTP | 新闻资讯 | ❌ 无需认证 |

## 🚀 快速开始

### 安装

```bash
# 在 gate-skills 仓库根目录执行（需先克隆 https://github.com/gate/gate-skills）
./skills/gate-mcp-openclaw-installer/scripts/install.sh
```

### 使用

```bash
# 查看 BTC 价格（无需认证）
mcporter call gate-info.list_tickers currency_pair=BTC_USDT

# 查看账户余额（需要认证）
mcporter call gate.list_spot_accounts

# 查看新闻（无需认证）
mcporter call gate-news.list_news

# 查看已安装的服务器
mcporter config list | grep gate
```

## 🔧 安装选项

### 默认：安装全部
```bash
./skills/gate-mcp-openclaw-installer/scripts/install.sh
```

### 选择性安装
```bash
./skills/gate-mcp-openclaw-installer/scripts/install.sh --select
# 或
./skills/gate-mcp-openclaw-installer/scripts/install.sh -s
```

## 📖 详细文档

查看 [SKILL.md](SKILL.md) 获取完整使用说明。

## 🔑 获取 API Keys

1. 访问 **https://www.gate.com/myaccount/profile/api-key/manage**（登录后：头像 → API 管理）
2. 创建 API Key，选择所需权限：
   - **读取** - 行情查询、账户信息
   - **交易** - Spot/Margin/Futures
   - **提币** - 钱包操作

**Gate-Dex 授权**：当 gate-dex 查询（余额/转账/Swap 等）返回需要授权时，请先打开 [https://web3.gate.com/](https://web3.gate.com/) 创建或绑定钱包；助手会返回可点击的 Google 授权链接，点击即可跳转完成授权。

## 📄 开源协议

MIT License
