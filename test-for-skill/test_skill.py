#!/usr/bin/env python3
"""
Skill Conversation Test Runner (通用版)

测试任意 SKILL.md 文档是否正确编写，通过模拟对话验证 AI 的行为是否符合预期。

Usage:
    # 设置 API Key
    export ANTHROPIC_API_KEY="your-api-key"
    
    # 测试指定 skill 的单个场景
    python test_skill.py --skill skills/gate-exchange-spot --scenario 1
    
    # 测试所有场景
    python test_skill.py --skill skills/gate-exchange-spot --all
    
    # 详细模式
    python test_skill.py --skill skills/gate-exchange-spot --scenario 1 --verbose
    
    # 列出可用场景
    python test_skill.py --skill skills/gate-exchange-spot --list
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("Error: anthropic not installed.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


class SkillTester:
    def __init__(self, skill_dir: Path, verbose: bool = False):
        self.verbose = verbose
        self.skill_dir = skill_dir
        self.skill_path = skill_dir / "SKILL.md"
        self.scenarios_path = skill_dir / "references" / "scenarios.md"
        
        if not self.skill_path.exists():
            raise FileNotFoundError(f"SKILL.md not found: {self.skill_path}")
        
        self.skill_content = self.skill_path.read_text()
        self.skill_name = self._extract_skill_name()
        self.scenarios = self._parse_scenarios()
        self.client = anthropic.Anthropic()
        
    def _extract_skill_name(self) -> str:
        """从 SKILL.md frontmatter 提取 skill 名称"""
        match = re.search(r'^name:\s*["\']?([^"\'\n]+)', self.skill_content, re.MULTILINE)
        return match.group(1).strip() if match else self.skill_dir.name
    
    def _parse_scenarios(self) -> list:
        """从 scenarios.md 解析场景"""
        scenarios = []
        
        if not self.scenarios_path.exists():
            print(f"Warning: scenarios.md not found: {self.scenarios_path}")
            return scenarios
        
        content = self.scenarios_path.read_text()
        
        # 匹配 ### Scenario N: Name 格式
        pattern = r'###\s*Scenario\s*(\d+):\s*([^\n]+)\n(.*?)(?=###\s*Scenario|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            scenario_id = int(match[0])
            name = match[1].strip()
            body = match[2]
            
            # 提取 User Prompt
            prompt_match = re.search(r'-\s*User Prompt:\s*`([^`]+)`', body)
            prompt = prompt_match.group(1) if prompt_match else ""
            
            # 提取 Tools
            tools_match = re.search(r'-\s*Tools:\s*`?([^`\n]+)`?', body)
            tools_str = tools_match.group(1) if tools_match else ""
            tools = [t.strip().split('(')[0] for t in tools_str.split('→')]
            tools = [t for t in tools if t]
            
            # 判断是否需要确认（包含 create_spot_order 的需要确认）
            must_confirm = 'create_spot_order' in tools_str
            
            # 判断不应调用的工具
            should_not_call = []
            if 'create_spot_order' not in tools_str and any(kw in name.lower() for kw in ['check', 'query', 'summary', 'readiness']):
                should_not_call = ['create_spot_order']
            
            scenarios.append({
                "id": scenario_id,
                "name": name,
                "prompt": prompt,
                "expected": {
                    "tools_in_order": tools,
                    "must_ask_confirmation": must_confirm,
                    "should_not_call": should_not_call
                }
            })
        
        return scenarios
        
    def create_system_prompt(self) -> str:
        """创建系统提示，要求 AI 严格按照 SKILL 执行"""
        return f"""你是一个严格按照 SKILL 文档执行的 AI 助手。

## 重要规则
1. 必须严格按照 SKILL 文档中定义的 Workflow 步骤执行
2. 工具调用顺序必须与文档中定义的一致
3. 对于需要下单的场景，必须在下单前请求用户确认
4. 输出格式必须符合 Report Template

## SKILL 文档

{self.skill_content}

## 输出格式要求
在执行过程中，请明确标注你调用的每个工具，格式如下：
[TOOL_CALL] tool_name

这样我们可以验证工具调用顺序。
"""

    def extract_tool_calls(self, response_text: str) -> list:
        """从响应中提取工具调用"""
        tool_calls = []
        
        # 匹配 [TOOL_CALL] 标记
        pattern = r'\[TOOL_CALL\]\s*(\w+)'
        matches = re.findall(pattern, response_text)
        tool_calls.extend(matches)
        
        # 也匹配其他常见格式
        patterns = [
            r'调用\s*[`"\']?(\w+)[`"\']?',
            r'Call\s*[`"\']?(\w+)[`"\']?',
            r'使用\s*[`"\']?(\w+)[`"\']?\s*(?:工具|tool)',
            r'`(\w+)`\s*(?:→|->)',
        ]
        for p in patterns:
            matches = re.findall(p, response_text, re.IGNORECASE)
            for m in matches:
                if m not in tool_calls:
                    prefixes = ('get_', 'create_', 'list_', 'cancel_', 'amend_', 'update_')
                    if any(m.startswith(pre) for pre in prefixes):
                        tool_calls.append(m)
        
        return tool_calls

    def check_confirmation_request(self, response_text: str) -> bool:
        """检查是否请求了用户确认"""
        confirmation_keywords = [
            r"确认", r"Confirm", r"confirm", 
            r"请确认", r"是否下单", r"是否执行",
            r"回复.*确认", r"reply.*confirm",
            r"请.*确认", r"需要.*确认"
        ]
        for keyword in confirmation_keywords:
            if re.search(keyword, response_text, re.IGNORECASE):
                return True
        return False

    def run_scenario(self, scenario: dict) -> dict:
        """运行单个测试场景"""
        print(f"\n{'='*60}")
        print(f"Testing Scenario {scenario['id']}: {scenario['name']}")
        print(f"{'='*60}")
        print(f"Prompt: {scenario['prompt']}")
        
        if not scenario['prompt']:
            print("⚠️ No prompt found for this scenario, skipping...")
            return {
                "scenario_id": scenario['id'],
                "scenario_name": scenario['name'],
                "error": "No prompt defined",
                "overall_pass": False
            }
        
        try:
            # 发送请求
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system=self.create_system_prompt(),
                messages=[
                    {"role": "user", "content": scenario['prompt']}
                ]
            )
            
            response_text = response.content[0].text
            
            if self.verbose:
                print(f"\n--- AI Response ---")
                print(response_text[:2000] + "..." if len(response_text) > 2000 else response_text)
                print(f"--- End Response ---\n")
            
            # 分析结果
            tool_calls = self.extract_tool_calls(response_text)
            confirmation_asked = self.check_confirmation_request(response_text)
            
            expected = scenario['expected']
            
            # 验证结果
            results = {
                "scenario_id": scenario['id'],
                "scenario_name": scenario['name'],
                "prompt": scenario['prompt'],
                "response_preview": response_text[:500],
                "checks": {}
            }
            
            # 检查工具调用
            if 'tools_in_order' in expected and expected['tools_in_order']:
                expected_tools = expected['tools_in_order']
                tools_match = all(t in tool_calls for t in expected_tools)
                results['checks']['tools_called'] = {
                    'expected': expected_tools,
                    'actual': tool_calls,
                    'pass': tools_match
                }
                print(f"✓ Tools Expected: {expected_tools}")
                print(f"  Tools Actual:   {tool_calls}")
                print(f"  Result: {'✅ PASS' if tools_match else '❌ FAIL'}")
            
            # 检查是否要求确认
            if 'must_ask_confirmation' in expected:
                must_confirm = expected['must_ask_confirmation']
                confirm_check = confirmation_asked == must_confirm
                results['checks']['confirmation'] = {
                    'expected': must_confirm,
                    'actual': confirmation_asked,
                    'pass': confirm_check
                }
                print(f"✓ Confirmation Expected: {must_confirm}")
                print(f"  Confirmation Actual:   {confirmation_asked}")
                print(f"  Result: {'✅ PASS' if confirm_check else '❌ FAIL'}")
            
            # 检查不应调用的工具
            if expected.get('should_not_call'):
                forbidden_tools = expected['should_not_call']
                forbidden_called = [t for t in forbidden_tools if t in tool_calls]
                no_forbidden = len(forbidden_called) == 0
                results['checks']['forbidden_tools'] = {
                    'forbidden': forbidden_tools,
                    'called': forbidden_called,
                    'pass': no_forbidden
                }
                print(f"✓ Should NOT Call: {forbidden_tools}")
                print(f"  Actually Called: {forbidden_called if forbidden_called else 'None'}")
                print(f"  Result: {'✅ PASS' if no_forbidden else '❌ FAIL'}")
            
            # 总体结果
            all_passed = all(c['pass'] for c in results['checks'].values()) if results['checks'] else False
            results['overall_pass'] = all_passed
            
            print(f"\n{'='*20} Overall: {'✅ PASS' if all_passed else '❌ FAIL'} {'='*20}")
            
            return results
            
        except Exception as e:
            print(f"❌ Error running scenario: {e}")
            return {
                "scenario_id": scenario['id'],
                "scenario_name": scenario['name'],
                "error": str(e),
                "overall_pass": False
            }

    def run_all(self) -> list:
        """运行所有场景"""
        results = []
        for scenario in self.scenarios:
            result = self.run_scenario(scenario)
            results.append(result)
        return results

    def generate_report(self, results: list, output_path: Path):
        """生成测试报告"""
        report = f"""# Skill 测试报告

**Skill**: {self.skill_name}  
**路径**: {self.skill_dir}  
**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 测试概览

| 场景 | 名称 | 结果 |
|------|------|------|
"""
        for r in results:
            status = "✅ PASS" if r.get('overall_pass') else "❌ FAIL"
            report += f"| {r['scenario_id']} | {r['scenario_name']} | {status} |\n"
        
        passed = sum(1 for r in results if r.get('overall_pass'))
        total = len(results)
        
        report += f"""
## 统计

- **通过**: {passed}/{total}
- **失败**: {total - passed}/{total}
- **通过率**: {passed/total*100:.1f}%

## 详细结果

"""
        for r in results:
            report += f"### Scenario {r['scenario_id']}: {r['scenario_name']}\n\n"
            report += f"**Prompt**: `{r.get('prompt', 'N/A')}`\n\n"
            if 'error' in r:
                report += f"**Error**: {r['error']}\n\n"
            else:
                for check_name, check_result in r.get('checks', {}).items():
                    status = "✅" if check_result['pass'] else "❌"
                    report += f"- {status} **{check_name}**: "
                    if check_name == 'tools_called':
                        report += f"\n  - Expected: `{check_result['expected']}`\n  - Actual: `{check_result['actual']}`\n"
                    elif check_name == 'confirmation':
                        report += f"Expected `{check_result['expected']}`, Got `{check_result['actual']}`\n"
                    elif check_name == 'forbidden_tools':
                        report += f"Forbidden `{check_result['forbidden']}`, Called `{check_result['called']}`\n"
            report += "\n---\n\n"
        
        output_path.write_text(report)
        print(f"\n📄 Report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Test SKILL.md through conversations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_skill.py --skill skills/gate-exchange-spot --scenario 1
  python test_skill.py --skill skills/gate-exchange-spot --all
  python test_skill.py --skill skills/gate-exchange-spot --list
        """
    )
    parser.add_argument('--skill', '-k', required=True, help='Path to skill directory')
    parser.add_argument('--scenario', '-s', type=int, help='Run specific scenario by ID')
    parser.add_argument('--all', '-a', action='store_true', help='Run all scenarios')
    parser.add_argument('--list', '-l', action='store_true', help='List available scenarios')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show full AI responses')
    parser.add_argument('--output', '-o', help='Output report path (default: <skill>/tests/TEST_RESULTS.md)')
    args = parser.parse_args()
    
    # 解析 skill 路径
    skill_dir = Path(args.skill)
    if not skill_dir.is_absolute():
        skill_dir = Path.cwd() / skill_dir
    
    if not skill_dir.exists():
        print(f"❌ Error: Skill directory not found: {skill_dir}")
        sys.exit(1)
    
    # 列出场景
    if args.list:
        try:
            tester = SkillTester(skill_dir)
            print(f"\n📋 Scenarios for: {tester.skill_name}")
            print(f"{'='*60}")
            for s in tester.scenarios:
                print(f"  {s['id']:2d}. {s['name']}")
                if s['prompt']:
                    print(f"      Prompt: {s['prompt'][:60]}...")
            print(f"\nTotal: {len(tester.scenarios)} scenarios")
        except Exception as e:
            print(f"❌ Error: {e}")
        sys.exit(0)
    
    # 检查 API Key
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nPlease run:")
        print("  export ANTHROPIC_API_KEY='your-api-key'")
        sys.exit(1)
    
    # 创建测试器
    try:
        tester = SkillTester(skill_dir, verbose=args.verbose)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    print(f"\n🧪 Testing Skill: {tester.skill_name}")
    print(f"📁 Path: {skill_dir}")
    print(f"📝 Scenarios: {len(tester.scenarios)}")
    
    # 运行测试
    if args.scenario:
        scenario = next((s for s in tester.scenarios if s['id'] == args.scenario), None)
        if not scenario:
            print(f"❌ Error: Scenario {args.scenario} not found")
            print(f"Available scenarios: {[s['id'] for s in tester.scenarios]}")
            sys.exit(1)
        results = [tester.run_scenario(scenario)]
    elif args.all:
        results = tester.run_all()
    else:
        print("Please specify --scenario N, --all, or --list")
        parser.print_help()
        sys.exit(1)
    
    # 生成报告
    if args.output:
        report_path = Path(args.output)
    else:
        tests_dir = skill_dir / 'tests'
        tests_dir.mkdir(exist_ok=True)
        report_path = tests_dir / 'TEST_RESULTS.md'
    
    tester.generate_report(results, report_path)
    
    # 返回退出码
    all_passed = all(r.get('overall_pass') for r in results)
    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    main()
