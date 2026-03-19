#!/usr/bin/env python3
"""
MCP Smoke Test — 自动化 MCP 工具连通性测试
读取 MCP 服务配置，扫描所有工具 schema，自动调用验证连通性，生成 HTML/MD 报告。
"""

import json
import os
import sys
import subprocess
import time
import signal
import glob
import re
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / "config.json"
VERBOSE = False

def vlog(msg):
    if VERBOSE:
        print(msg)

# ─── Config ──────────────────────────────────────────────────────────────────

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def resolve_cursor_mcp_config(config):
    path = os.path.expanduser(config["cursor_mcp_config"])
    with open(path) as f:
        return json.load(f)

def resolve_mcps_cache_dir(config):
    if config.get("mcps_cache_dir") != "auto":
        return Path(os.path.expanduser(config["mcps_cache_dir"]))
    workspace = SCRIPT_DIR.parent.parent
    ws_slug = str(workspace).replace("/", "-").lstrip("-")
    return Path.home() / ".cursor" / "projects" / ws_slug / "mcps"

# ─── Tool Discovery ─────────────────────────────────────────────────────────

def discover_tools_from_cache(mcps_dir, server_name):
    """Scan mcps cache directory for tool schemas."""
    pattern = f"user-{server_name}"
    candidates = list(mcps_dir.glob(f"{pattern}/tools/*.json"))
    if not candidates:
        for d in mcps_dir.iterdir():
            if d.is_dir() and server_name.lower() in d.name.lower():
                candidates = list((d / "tools").glob("*.json"))
                if candidates:
                    break
    tools = {}
    for f in sorted(candidates):
        with open(f) as fp:
            schema = json.load(fp)
        tools[schema["name"]] = schema
    return tools

def classify_tool(name, config):
    short = name.split("_", 2)[-1] if name.startswith("cex_") else name
    for prefix in config.get("write_prefixes", []):
        if short.startswith(prefix) or name.endswith(f"_{prefix.rstrip('_')}"):
            return "write", prefix.rstrip("_")
    for prefix in config.get("read_prefixes", []):
        if short.startswith(prefix):
            return "read", prefix.rstrip("_")
    return "unknown", ""

def extract_module(name):
    parts = name.split("_")
    if len(parts) >= 2 and parts[0] == "cex":
        return parts[1]
    return "other"

# ─── Parameter Generation ───────────────────────────────────────────────────

def generate_params(schema, defaults):
    """Auto-generate minimal safe parameters from tool schema."""
    args_schema = schema.get("arguments", schema.get("inputSchema", {}))
    properties = args_schema.get("properties", {})
    required = args_schema.get("required", [])
    params = {}
    for field in required:
        if field in defaults:
            params[field] = defaults[field]
        elif field in properties:
            prop = properties[field]
            ptype = prop.get("type", "string")
            if ptype == "number":
                params[field] = 1
            elif ptype == "integer":
                params[field] = 1
            elif ptype == "boolean":
                params[field] = False
            else:
                params[field] = field
    return params

# ─── MCP Client (stdio JSON-RPC) ────────────────────────────────────────────

class McpStdioClient:
    def __init__(self, command, args, env=None, timeout=30):
        self.command = command
        self.args = args
        self.env = {**os.environ, **(env or {})}
        self.timeout = timeout
        self.process = None
        self._id = 0

    def start(self):
        self.process = subprocess.Popen(
            [self.command] + self.args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.env,
        )
        self._initialize()

    def _next_id(self):
        self._id += 1
        return self._id

    def _send(self, method, params=None):
        msg = {"jsonrpc": "2.0", "id": self._next_id(), "method": method}
        if params:
            msg["params"] = params
        line = json.dumps(msg) + "\n"
        self.process.stdin.write(line.encode())
        self.process.stdin.flush()

    def _recv(self):
        line = self.process.stdout.readline()
        if not line:
            return None
        return json.loads(line.decode().strip())

    def _initialize(self):
        self._send("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "mcp-smoke-test", "version": "1.0.0"}
        })
        resp = self._recv()
        self._send("notifications/initialized")
        return resp

    def call_tool(self, name, arguments=None):
        self._send("tools/call", {"name": name, "arguments": arguments or {}})
        start = time.time()
        while time.time() - start < self.timeout:
            resp = self._recv()
            if resp is None:
                time.sleep(0.1)
                continue
            if "result" in resp or "error" in resp:
                return resp
        return {"error": {"code": -1, "message": "Timeout"}}

    def list_tools(self):
        self._send("tools/list")
        resp = self._recv()
        if resp and "result" in resp:
            return resp["result"].get("tools", [])
        return []

    def stop(self):
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()

# ─── Test Execution ─────────────────────────────────────────────────────────

class TestResult:
    def __init__(self, tool_name, module, tool_type, params, status, message, elapsed_ms, raw_request=None, raw_response=None, skip_reason=None):
        self.tool_name = tool_name
        self.module = module
        self.tool_type = tool_type
        self.params = params
        self.status = status      # PASS / FAIL / SKIP / ERROR
        self.message = message
        self.elapsed_ms = elapsed_ms
        self.raw_request = raw_request
        self.raw_response = raw_response
        self.skip_reason = skip_reason

def _truncate_json(obj, max_len=500):
    s = json.dumps(obj, ensure_ascii=False, indent=2)
    if len(s) > max_len:
        return s[:max_len] + "\n... (truncated)"
    return s

def run_tests(client, tools, config):
    results = []
    defaults = config.get("default_test_params", {})
    skip_write = config.get("skip_write_tools", True)
    total = len(tools)

    for i, (name, schema) in enumerate(sorted(tools.items()), 1):
        module = extract_module(name)
        tool_type, matched_prefix = classify_tool(name, config)
        params = generate_params(schema, defaults)

        print(f"  [{i}/{total}] {name} ({tool_type})...", end=" ", flush=True)

        if skip_write and tool_type == "write":
            reason = f"Write tool (matched prefix: '{matched_prefix}_*'), config skip_write_tools=true"
            results.append(TestResult(name, module, tool_type, params, "SKIP", reason, 0, skip_reason=reason))
            print(f"⏭ SKIP ({matched_prefix}_*)")
            vlog(f"         ↳ Reason: {reason}")
            continue

        vlog(f"\n         ↳ Request params: {json.dumps(params, ensure_ascii=False)}")

        start = time.time()
        try:
            resp = client.call_tool(name, params)
            elapsed = int((time.time() - start) * 1000)

            vlog(f"         ↳ Response ({elapsed}ms): {_truncate_json(resp)}")

            if "error" in resp:
                err = resp["error"]
                code = err.get("code", 0)
                msg = err.get("message", str(err))
                if code == -1:
                    results.append(TestResult(name, module, tool_type, params, "FAIL", f"Timeout ({config['timeout_seconds']}s)", elapsed, params, resp))
                    print(f"❌ TIMEOUT")
                elif "401" in msg or "403" in msg or "Unauthorized" in msg or "Forbidden" in msg:
                    results.append(TestResult(name, module, tool_type, params, "FAIL", f"Auth error: {msg[:100]}", elapsed, params, resp))
                    print(f"❌ AUTH")
                elif "404" in msg or "Not Found" in msg:
                    results.append(TestResult(name, module, tool_type, params, "FAIL", f"Not Found (404): {msg[:100]}", elapsed, params, resp))
                    print(f"❌ 404 NOT FOUND ({elapsed}ms)")
                elif "400" in msg or "INVALID" in msg.upper() or "missing" in msg.lower():
                    results.append(TestResult(name, module, tool_type, params, "PASS", f"Reachable (param error): {msg[:100]}", elapsed, params, resp))
                    print(f"⚠️ PASS (param err, {elapsed}ms)")
                else:
                    results.append(TestResult(name, module, tool_type, params, "FAIL", msg[:200], elapsed, params, resp))
                    print(f"❌ FAIL ({elapsed}ms)")
            else:
                result_data = resp.get("result", {})
                content = result_data.get("content", []) if isinstance(result_data, dict) else result_data
                is_error = result_data.get("isError", False) if isinstance(result_data, dict) else False
                if isinstance(content, list) and content:
                    first = content[0] if content else {}
                    text = first.get("text", str(first))[:200] if isinstance(first, dict) else str(first)[:200]
                else:
                    text = str(content)[:200]

                if "404" in text or "Not Found" in text:
                    results.append(TestResult(name, module, tool_type, params, "FAIL", f"Not Found (404): {text[:100]}", elapsed, params, resp))
                    print(f"❌ 404 NOT FOUND ({elapsed}ms)")
                elif is_error and ("401" in text or "403" in text or "Unauthorized" in text or "Forbidden" in text):
                    results.append(TestResult(name, module, tool_type, params, "FAIL", f"Auth error: {text[:100]}", elapsed, params, resp))
                    print(f"❌ AUTH ({elapsed}ms)")
                elif is_error:
                    results.append(TestResult(name, module, tool_type, params, "PASS", f"Reachable (API error): {text[:100]}", elapsed, params, resp))
                    print(f"⚠️ PASS (api err, {elapsed}ms)")
                else:
                    results.append(TestResult(name, module, tool_type, params, "PASS", f"OK: {text[:80]}", elapsed, params, resp))
                    print(f"✅ PASS ({elapsed}ms)")

        except Exception as e:
            elapsed = int((time.time() - start) * 1000)
            results.append(TestResult(name, module, tool_type, params, "ERROR", str(e)[:200], elapsed, params, {"exception": str(e)}))
            print(f"💥 ERROR ({elapsed}ms)")
            vlog(f"         ↳ Exception: {e}")

    return results

# ─── Report Generation ──────────────────────────────────────────────────────

def generate_md_report(results, server_name, tools, report_dir):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(results)
    passed = sum(1 for r in results if r.status == "PASS")
    failed = sum(1 for r in results if r.status == "FAIL")
    errors = sum(1 for r in results if r.status == "ERROR")
    skipped = sum(1 for r in results if r.status == "SKIP")

    modules = defaultdict(list)
    for r in results:
        modules[r.module].append(r)

    lines = []
    lines.append(f"# MCP Smoke Test Report")
    lines.append(f"")
    lines.append(f"## 测试概要")
    lines.append(f"")
    lines.append(f"| 项目 | 内容 |")
    lines.append(f"|------|------|")
    lines.append(f"| 测试时间 | {now} |")
    lines.append(f"| MCP 服务 | {server_name} |")
    lines.append(f"| 工具总数 | {len(tools)} |")
    lines.append(f"| 测试总数 | {total} |")
    lines.append(f"| ✅ 通过 | {passed} |")
    lines.append(f"| ❌ 失败 | {failed} |")
    lines.append(f"| 💥 异常 | {errors} |")
    lines.append(f"| ⏭ 跳过 | {skipped} |")
    lines.append(f"| 通过率 | {passed}/{total - skipped} ({passed*100//(total-skipped) if total-skipped else 0}%) |")
    lines.append(f"")

    fail_404 = [r for r in results if r.status == "FAIL" and "404" in r.message]
    fail_auth = [r for r in results if r.status == "FAIL" and ("Auth" in r.message or "401" in r.message or "403" in r.message)]
    fail_other = [r for r in results if r.status == "FAIL" and r not in fail_404 and r not in fail_auth]
    error_list = [r for r in results if r.status == "ERROR"]

    if fail_404:
        lines.append(f"### 404 Not Found ({len(fail_404)} 个)")
        lines.append(f"")
        for r in sorted(fail_404, key=lambda x: x.tool_name):
            lines.append(f"- `{r.tool_name}` [{r.module}]")
        lines.append(f"")

    if fail_auth:
        lines.append(f"### Auth 权限失败 ({len(fail_auth)} 个)")
        lines.append(f"")
        for r in sorted(fail_auth, key=lambda x: x.tool_name):
            lines.append(f"- `{r.tool_name}` [{r.module}]")
        lines.append(f"")

    if fail_other:
        lines.append(f"### 其他失败 ({len(fail_other)} 个)")
        lines.append(f"")
        for r in sorted(fail_other, key=lambda x: x.tool_name):
            lines.append(f"- `{r.tool_name}` [{r.module}]: {r.message[:100]}")
        lines.append(f"")

    if error_list:
        lines.append(f"### 异常 ({len(error_list)} 个)")
        lines.append(f"")
        for r in sorted(error_list, key=lambda x: x.tool_name):
            lines.append(f"- `{r.tool_name}` [{r.module}]: {r.message[:100]}")
        lines.append(f"")

    lines.append(f"## 按模块统计")
    lines.append(f"")
    lines.append(f"| 模块 | 总数 | ✅ | ❌ | 💥 | ⏭ | 通过率 |")
    lines.append(f"|------|------|-----|-----|-----|-----|--------|")
    for mod in sorted(modules.keys()):
        rs = modules[mod]
        mp = sum(1 for r in rs if r.status == "PASS")
        mf = sum(1 for r in rs if r.status == "FAIL")
        me = sum(1 for r in rs if r.status == "ERROR")
        ms = sum(1 for r in rs if r.status == "SKIP")
        tested = len(rs) - ms
        rate = f"{mp*100//tested}%" if tested else "N/A"
        lines.append(f"| {mod} | {len(rs)} | {mp} | {mf} | {me} | {ms} | {rate} |")
    lines.append(f"")

    status_icon = {"PASS": "✅", "FAIL": "❌", "ERROR": "💥", "SKIP": "⏭"}

    for mod in sorted(modules.keys()):
        lines.append(f"## {mod.upper()} 模块详情")
        lines.append(f"")
        for r in sorted(modules[mod], key=lambda x: x.tool_name):
            icon = status_icon.get(r.status, "❓")
            ms = f"{r.elapsed_ms}ms" if r.elapsed_ms else "-"
            lines.append(f"### {icon} `{r.tool_name}` ({r.tool_type}) — {r.status} {ms}")
            lines.append(f"")
            if r.skip_reason:
                lines.append(f"**Skip reason:** {r.skip_reason}")
                lines.append(f"")
            else:
                lines.append(f"**Request params:**")
                lines.append(f"```json")
                lines.append(json.dumps(r.params, ensure_ascii=False, indent=2))
                lines.append(f"```")
                lines.append(f"")
                lines.append(f"**Response:**")
                lines.append(f"```")
                resp_text = r.message[:500] if r.message else "(empty)"
                lines.append(resp_text)
                lines.append(f"```")
                lines.append(f"")

    if failed + errors > 0:
        lines.append(f"## 失败/异常汇总")
        lines.append(f"")
        for r in results:
            if r.status in ("FAIL", "ERROR"):
                icon = status_icon[r.status]
                lines.append(f"- {icon} **{r.tool_name}** [{r.module}]: {r.message}")
        lines.append(f"")

    md_path = Path(report_dir) / f"smoke-test-{server_name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path


def generate_html_report(results, server_name, tools, report_dir):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(results)
    passed = sum(1 for r in results if r.status == "PASS")
    failed = sum(1 for r in results if r.status == "FAIL")
    errors = sum(1 for r in results if r.status == "ERROR")
    skipped = sum(1 for r in results if r.status == "SKIP")
    tested = total - skipped
    rate = passed * 100 // tested if tested else 0

    status_class = {"PASS": "pass", "FAIL": "fail", "ERROR": "error", "SKIP": "skip"}
    status_icon = {"PASS": "✅", "FAIL": "❌", "ERROR": "💥", "SKIP": "⏭"}

    results_by_module = defaultdict(list)
    for r in results:
        results_by_module[r.module].append(r)

    rows_by_module = []
    for mod in sorted(results_by_module.keys()):
        rs = sorted(results_by_module[mod], key=lambda x: x.tool_name)
        mp = sum(1 for r in rs if r.status == "PASS")
        mf = sum(1 for r in rs if r.status == "FAIL")
        me = sum(1 for r in rs if r.status == "ERROR")
        ms_ = sum(1 for r in rs if r.status == "SKIP")
        mt = len(rs) - ms_
        mrate = f"{mp*100//mt}%" if mt else "N/A"
        detail_rows = ""
        for r in rs:
            cls = status_class.get(r.status, "")
            icon = status_icon.get(r.status, "")
            elapsed = f"{r.elapsed_ms}ms" if r.elapsed_ms else "-"
            msg_escaped = (r.message or "").replace("<", "&lt;").replace(">", "&gt;")[:120]

            if r.skip_reason:
                skip_escaped = r.skip_reason.replace("<", "&lt;").replace(">", "&gt;")
                detail_html = f'<div class="detail-skip">Skip reason: {skip_escaped}</div>'
            else:
                params_json = json.dumps(r.params, ensure_ascii=False, indent=2).replace("<", "&lt;").replace(">", "&gt;")
                resp_raw = ""
                if r.raw_response:
                    resp_raw = json.dumps(r.raw_response, ensure_ascii=False, indent=2)[:1000].replace("<", "&lt;").replace(">", "&gt;")
                else:
                    resp_raw = msg_escaped
                detail_html = f'''<details><summary>Show request &amp; response</summary>
<div class="detail-block"><b>Request params:</b><pre>{params_json}</pre><b>Response:</b><pre>{resp_raw}</pre></div></details>'''

            detail_rows += f'<tr class="{cls}"><td><code>{r.tool_name}</code></td><td>{r.tool_type}</td><td>{icon} {r.status}</td><td>{elapsed}</td><td>{msg_escaped}</td></tr>\n'
            detail_rows += f'<tr class="detail-row {cls}"><td colspan="5">{detail_html}</td></tr>\n'
        rows_by_module.append((mod, len(rs), mp, mf, me, ms_, mrate, detail_rows))

    module_summary_rows = ""
    for mod, cnt, mp, mf, me, ms_, mrate, _ in rows_by_module:
        module_summary_rows += f'<tr><td><a href="#{mod}">{mod}</a></td><td>{cnt}</td><td>{mp}</td><td>{mf}</td><td>{me}</td><td>{ms_}</td><td>{mrate}</td></tr>\n'

    module_detail_sections = ""
    for mod, cnt, mp, mf, me, ms_, mrate, detail_rows in rows_by_module:
        module_detail_sections += f'''
<h2 id="{mod}">{mod.upper()} ({cnt} tools, {mrate} pass)</h2>
<table><thead><tr><th>Tool</th><th>Type</th><th>Status</th><th>Time</th><th>Message</th></tr></thead>
<tbody>{detail_rows}</tbody></table>
'''

    bar_p = rate
    bar_f = (failed * 100 // tested) if tested else 0
    bar_e = 100 - bar_p - bar_f

    fail_404 = [r for r in results if r.status == "FAIL" and "404" in r.message]
    fail_auth = [r for r in results if r.status == "FAIL" and ("Auth" in r.message or "401" in r.message or "403" in r.message)]
    fail_other = [r for r in results if r.status == "FAIL" and r not in fail_404 and r not in fail_auth]
    error_list = [r for r in results if r.status == "ERROR"]

    fail_summary_html = ""
    if fail_404 or fail_auth or fail_other or error_list:
        fail_summary_html += '<h2>Failure Summary</h2>\n'

        if fail_404:
            items = "".join(f'<li><code>{r.tool_name}</code> <span class="tag mod">{r.module}</span></li>' for r in sorted(fail_404, key=lambda x: x.tool_name))
            fail_summary_html += f'<div class="fail-group"><h3 style="color:#ef4444">404 Not Found ({len(fail_404)})</h3><ul>{items}</ul></div>\n'

        if fail_auth:
            items = "".join(f'<li><code>{r.tool_name}</code> <span class="tag mod">{r.module}</span></li>' for r in sorted(fail_auth, key=lambda x: x.tool_name))
            fail_summary_html += f'<div class="fail-group"><h3 style="color:#d97706">Auth Failed ({len(fail_auth)})</h3><ul>{items}</ul></div>\n'

        if fail_other:
            items = "".join(f'<li><code>{r.tool_name}</code> <span class="tag mod">{r.module}</span> — {(r.message or "")[:80].replace("<","&lt;")}</li>' for r in sorted(fail_other, key=lambda x: x.tool_name))
            fail_summary_html += f'<div class="fail-group"><h3 style="color:#ef4444">Other Failures ({len(fail_other)})</h3><ul>{items}</ul></div>\n'

        if error_list:
            items = "".join(f'<li><code>{r.tool_name}</code> <span class="tag mod">{r.module}</span> — {(r.message or "")[:80].replace("<","&lt;")}</li>' for r in sorted(error_list, key=lambda x: x.tool_name))
            fail_summary_html += f'<div class="fail-group"><h3 style="color:#d97706">Errors ({len(error_list)})</h3><ul>{items}</ul></div>\n'

    html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MCP Smoke Test — {server_name}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#f5f5f5;color:#333;padding:24px;max-width:1200px;margin:0 auto}}
h1{{font-size:1.6rem;margin-bottom:8px}}
h2{{font-size:1.2rem;margin:24px 0 8px;padding-top:16px;border-top:1px solid #ddd}}
.summary{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;margin:16px 0}}
.card{{background:#fff;border-radius:8px;padding:16px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.1)}}
.card .num{{font-size:2rem;font-weight:700}}
.card .label{{font-size:.85rem;color:#666;margin-top:4px}}
.bar{{height:24px;border-radius:12px;overflow:hidden;display:flex;margin:16px 0;background:#eee}}
.bar .p{{background:#22c55e}}.bar .f{{background:#ef4444}}.bar .e{{background:#f59e0b}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.1);margin-bottom:16px;font-size:.9rem}}
th{{background:#f8f8f8;padding:8px 12px;text-align:left;font-weight:600;border-bottom:2px solid #e5e5e5}}
td{{padding:6px 12px;border-bottom:1px solid #f0f0f0}}
tr.pass td:nth-child(3){{color:#16a34a}} tr.fail td:nth-child(3){{color:#dc2626;font-weight:600}} tr.error td:nth-child(3){{color:#d97706}} tr.skip td:nth-child(3){{color:#9ca3af}}
code{{background:#f1f5f9;padding:2px 6px;border-radius:4px;font-size:.85rem}}
.meta{{color:#888;font-size:.85rem;margin-bottom:16px}}
.detail-row td{{padding:0 12px 8px;border-bottom:1px solid #e5e5e5}}
.detail-block{{background:#f8f9fa;border:1px solid #e5e5e5;border-radius:6px;padding:12px;margin:6px 0;font-size:.82rem}}
.detail-block pre{{background:#fff;border:1px solid #ddd;border-radius:4px;padding:8px;overflow-x:auto;max-height:300px;overflow-y:auto;font-size:.8rem;margin:4px 0 8px}}
.detail-skip{{color:#9ca3af;font-style:italic;font-size:.85rem;padding:4px 0}}
details summary{{cursor:pointer;color:#4b6bfb;font-size:.85rem;padding:4px 0}}
details summary:hover{{text-decoration:underline}}
.fail-group{{background:#fff;border-radius:8px;padding:16px;margin:8px 0;box-shadow:0 1px 3px rgba(0,0,0,.1)}}
.fail-group h3{{font-size:1rem;margin-bottom:8px}}
.fail-group ul{{list-style:none;padding:0}}
.fail-group li{{padding:3px 0;font-size:.9rem}}
.tag.mod{{background:#e0e7ff;color:#3b5bdb;padding:1px 6px;border-radius:4px;font-size:.78rem;margin-left:6px}}
</style></head><body>
<h1>MCP Smoke Test Report</h1>
<div class="meta">{now} &nbsp;|&nbsp; Server: <b>{server_name}</b> &nbsp;|&nbsp; Tools: {len(tools)}</div>
<div class="summary">
  <div class="card"><div class="num">{total}</div><div class="label">Total</div></div>
  <div class="card"><div class="num" style="color:#22c55e">{passed}</div><div class="label">✅ Pass</div></div>
  <div class="card"><div class="num" style="color:#ef4444">{failed}</div><div class="label">❌ Fail</div></div>
  <div class="card"><div class="num" style="color:#f59e0b">{errors}</div><div class="label">💥 Error</div></div>
  <div class="card"><div class="num" style="color:#9ca3af">{skipped}</div><div class="label">⏭ Skip</div></div>
  <div class="card"><div class="num">{rate}%</div><div class="label">Pass Rate</div></div>
</div>
<div class="bar"><div class="p" style="width:{bar_p}%"></div><div class="f" style="width:{bar_f}%"></div><div class="e" style="width:{bar_e}%"></div></div>
{fail_summary_html}
<h2>Module Summary</h2>
<table><thead><tr><th>Module</th><th>Total</th><th>✅</th><th>❌</th><th>💥</th><th>⏭</th><th>Rate</th></tr></thead>
<tbody>{module_summary_rows}</tbody></table>
{module_detail_sections}
<div class="meta" style="margin-top:32px;text-align:center">Generated by mcp-smoke-test</div>
</body></html>'''

    html_path = Path(report_dir) / f"smoke-test-{server_name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html, encoding="utf-8")
    return html_path

# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    global VERBOSE
    parser = argparse.ArgumentParser(description="MCP Smoke Test — 自动化连通性测试")
    parser.add_argument("-v", "--verbose", action="store_true", help="打印详细请求/响应日志")
    parser.add_argument("server", nargs="?", help="Target MCP server name (overrides config)")
    parsed = parser.parse_args()

    VERBOSE = parsed.verbose

    print("=" * 60)
    print("  MCP Smoke Test — 自动化连通性测试")
    if VERBOSE:
        print("  (Verbose mode ON — 详细请求/响应日志)")
    print("=" * 60)

    config = load_config()
    server_name = parsed.server or config["mcp_server"]
    print(f"\n📦 Target MCP Server: {server_name}")

    cursor_config = resolve_cursor_mcp_config(config)
    server_cfg = cursor_config.get("mcpServers", {}).get(server_name)
    if not server_cfg:
        print(f"❌ Server '{server_name}' not found in Cursor MCP config.")
        print(f"   Available: {', '.join(cursor_config.get('mcpServers', {}).keys())}")
        sys.exit(1)

    if "url" in server_cfg:
        print(f"   Type: SSE (url: {server_cfg['url']})")
        print(f"   ⚠️  SSE transport not yet supported. Use stdio servers.")
        sys.exit(1)

    cmd = server_cfg["command"]
    args = server_cfg.get("args", [])
    env = server_cfg.get("env", {})
    print(f"   Type: stdio ({cmd} {' '.join(args)})")

    mcps_dir = resolve_mcps_cache_dir(config)
    cached_tools = discover_tools_from_cache(mcps_dir, server_name)
    print(f"\n🔍 Cached tool schemas found: {len(cached_tools)}")

    print(f"\n🚀 Starting MCP server...")
    client = McpStdioClient(cmd, args, env, timeout=config.get("timeout_seconds", 30))
    try:
        client.start()
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

    time.sleep(2)

    print(f"   Fetching live tool list...")
    live_tools = client.list_tools()
    live_names = {t["name"] for t in live_tools} if live_tools else set()
    print(f"   Live tools: {len(live_names)}")

    if cached_tools and live_names:
        new_tools = live_names - set(cached_tools.keys())
        removed_tools = set(cached_tools.keys()) - live_names
        if new_tools:
            print(f"\n   🆕 New tools (not in cache): {len(new_tools)}")
            for t in sorted(new_tools):
                print(f"      + {t}")
        if removed_tools:
            print(f"\n   🗑️  Removed tools (in cache but not live): {len(removed_tools)}")
            for t in sorted(removed_tools):
                print(f"      - {t}")

    all_tools = {}
    if live_tools:
        for t in live_tools:
            all_tools[t["name"]] = t.get("inputSchema", {})
    elif cached_tools:
        all_tools = cached_tools
        print("   ⚠️  Using cached schemas (live list unavailable)")
    else:
        print("   ❌ No tools found")
        client.stop()
        sys.exit(1)

    wrapped = {}
    for name, schema in all_tools.items():
        if isinstance(schema, dict) and "arguments" not in schema and "properties" in schema:
            wrapped[name] = {"name": name, "arguments": schema}
        elif isinstance(schema, dict) and "arguments" in schema:
            wrapped[name] = schema
        else:
            wrapped[name] = {"name": name, "arguments": {"properties": {}, "required": []}}

    modules = defaultdict(int)
    for name in wrapped:
        modules[extract_module(name)] += 1
    print(f"\n📊 Tool breakdown by module:")
    for mod in sorted(modules):
        print(f"   {mod}: {modules[mod]}")

    print(f"\n🧪 Running smoke tests ({len(wrapped)} tools)...\n")
    results = run_tests(client, wrapped, config)

    client.stop()

    report_dir = SCRIPT_DIR / config.get("report_dir", "reports")
    print(f"\n📝 Generating reports...")
    md_path = generate_md_report(results, server_name, wrapped, report_dir)
    html_path = generate_html_report(results, server_name, wrapped, report_dir)

    total = len(results)
    passed = sum(1 for r in results if r.status == "PASS")
    failed = sum(1 for r in results if r.status == "FAIL")
    errors = sum(1 for r in results if r.status == "ERROR")
    skipped = sum(1 for r in results if r.status == "SKIP")
    tested = total - skipped

    print(f"\n{'=' * 60}")
    print(f"  Test Complete!")
    print(f"  ✅ Pass: {passed}  ❌ Fail: {failed}  💥 Error: {errors}  ⏭ Skip: {skipped}")
    print(f"  Pass Rate: {passed*100//tested if tested else 0}% ({passed}/{tested})")
    print(f"  📄 MD:   {md_path}")
    print(f"  🌐 HTML: {html_path}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
