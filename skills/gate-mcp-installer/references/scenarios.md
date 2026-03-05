# Gate MCP Installer — Scenarios & Prompt Examples

## Scenario 1: First-Time Installation

**Context**: User wants to set up Gate MCP from scratch in their environment.

**Prompt Examples**:
- "帮我安装 Gate MCP"
- "配置一下 Gate MCP"
- "I want to set up Gate MCP"
- "Install Gate MCP for me"

**Expected Behavior**:
1. Run the installation script `scripts/install-gate-mcp.sh`
2. Install mcporter CLI globally via npm
3. Configure Gate MCP server endpoint
4. Verify connectivity by listing available tools
5. Show usage examples

---

## Scenario 2: Verification / Health Check

**Context**: User already has Gate MCP installed and wants to verify it's working correctly.

**Prompt Examples**:
- "Gate MCP 安装好了吗？"
- "检查一下 MCP 连接"
- "Verify my Gate MCP setup"
- "Is Gate MCP working?"

**Expected Behavior**:
1. Run `mcporter config get gate` to check config
2. Run `mcporter list gate --schema` to verify tools are accessible
3. Report status: connected / not configured / connection failed
4. Suggest fixes if issues are found

---

## Scenario 3: Troubleshooting

**Context**: User encounters errors when using Gate MCP and needs help diagnosing the issue.

**Prompt Examples**:
- "Gate MCP 连不上"
- "mcporter 命令找不到"
- "MCP 报错了怎么办？"
- "Gate MCP connection timeout, help"

**Expected Behavior**:
1. Check if mcporter is installed (`npx mcporter --version`)
2. Check config (`mcporter config get gate`)
3. Test connectivity
4. Diagnose based on error type (see troubleshooting table)
5. Apply fix or guide user through manual steps

---

## Scenario 4: Reinstallation / Update

**Context**: User wants to reinstall or update their Gate MCP setup.

**Prompt Examples**:
- "重新安装 Gate MCP"
- "更新一下 mcporter"
- "Reinstall Gate MCP"
- "Update mcporter to latest version"

**Expected Behavior**:
1. Run `npm i -g mcporter` to install/update to latest version
2. Re-run config setup if needed
3. Verify the updated installation works
4. Report the installed version
