#!/usr/bin/env python3
"""
MCP Connectivity Test — 自动化 MCP 工具连通性测试
读取已信任的 stdio 服务配置，只调用 safe_reads.py 登记的公共只读工具。
未知、写操作或 schema 变化的工具默认跳过；生成 HTML/MD 报告。
判断标准：服务端返回业务响应（含业务错误）即为通过，仅 MCP 错误/404/超时 为失败。
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
import math
from html import escape
from stdio_client import McpStdioClient
from safe_reads import PUBLIC_READS, read_rejection
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

# ─── Auto Connectivity Test Engine ───────────────────────────────────────────

from auto_params import generate_params, load_overrides, apply_overrides

OVERRIDES_PATH = SCRIPT_DIR / "test_overrides.json"


class TestResult:
    def __init__(self, tool_name, module, tool_type, params, status, message, elapsed_ms, raw_request=None, raw_response=None, skip_reason=None):
        self.tool_name = tool_name
        self.module = module
        self.tool_type = tool_type
        self.params = params
        self.status = status
        self.message = message
        self.elapsed_ms = elapsed_ms
        self.raw_request = raw_request
        self.raw_response = raw_response
        self.skip_reason = skip_reason


def _truncate_json(obj, max_len=500):
    s = json.dumps(obj, ensure_ascii=False, indent=2)
    return s[:max_len] + "\n... (truncated)" if len(s) > max_len else s


def _parse_response(resp):
    """Parse MCP response. Returns (text, is_error, http_status)."""
    if "error" in resp:
        err = resp["error"]
        return err.get("message", str(err)), True, None

    result_data = resp.get("result", {})
    content = result_data.get("content", []) if isinstance(result_data, dict) else result_data
    is_error = result_data.get("isError", False) if isinstance(result_data, dict) else False

    text = ""
    if isinstance(content, list) and content:
        first = content[0]
        text = first.get("text", str(first)) if isinstance(first, dict) else str(first)
    else:
        text = str(content)

    http_status = None
    sm = re.search(r'"status"\s*:\s*(\d+)', text)
    if sm:
        http_status = int(sm.group(1))
    return text, is_error, http_status


def _is_connectivity_pass(text, is_error, http_status, resp):
    """
    Connectivity test pass criteria:
    - PASS: Server returned any business response (200, 400 biz errors, etc.)
    - FAIL: MCP error, timeout, 404 (bad route), missing params schema error
    """
    if "error" in resp:
        err = resp["error"]
        code = err.get("code", 0)
        msg = err.get("message", "")
        if code == -1:
            return False, "TIMEOUT"
        if "MCP" in msg or "schema" in msg.lower() or "validation" in msg.lower():
            return False, "MCP_ERROR"
        if '"status"' in msg or "'status'" in msg:
            return True, "BIZ_ERROR"
        return False, "UNKNOWN_ERROR"

    if http_status == 401:
        return False, "AUTH_401"
    if http_status == 403:
        return False, "FORBIDDEN_403"
    if http_status == 404:
        biz_404_labels = ("ORDER_NOT_FOUND", "ORDER_NOT_EXISTS", "NOT_FOUND",
                          "POSITION_NOT_FOUND", "CONTRACT_NOT_FOUND")
        for lbl in biz_404_labels:
            if lbl in text:
                return True, "BIZ_ERROR"
        if '"label"' in text:
            return True, "BIZ_ERROR"
        if "Not Found" in text:
            return True, "BIZ_ERROR"
        return False, "NOT_FOUND_404"
    if http_status and http_status >= 500:
        return True, "SERVER_ERROR"
    if is_error:
        return True, "BIZ_ERROR"
    return True, "OK"


def run_connectivity_tests(client, tools, overrides_data):
    """Run connectivity test for all tools. Each tool called once with auto-generated params."""
    results = []
    overrides = overrides_data
    total = len(tools)

    for i, (name, schema) in enumerate(sorted(tools.items()), 1):
        module = extract_module(name)
        print(f"  [{i}/{total}] {name}...", end=" ", flush=True)

        tool_ov = overrides.get(name, {})
        if tool_ov.get("skip"):
            reason = tool_ov.get("skip_reason", "skipped in overrides")
            print(f"⏭ SKIP ({reason})")
            results.append(TestResult(name, module, "auto", {}, "SKIP", reason, 0, raw_request={}, raw_response={"skip": reason}))
            continue

        # A discovered name/annotation is untrusted; unknown tools are never invoked.
        if name not in PUBLIC_READS:
            reason = "not in the reviewed public read-only catalog"
            results.append(TestResult(name, module, "auto", {}, "SKIP", reason, 0, skip_reason=reason))
            continue
        # Reject malformed/changed schemas before the parameter generator sees them.
        reason = read_rejection(name, schema, {}, require_values=False)
        if not reason:
            params = apply_overrides(name, generate_params(name, schema), overrides)
            reason = read_rejection(name, schema, params)
        if reason:
            results.append(TestResult(name, module, "auto", {}, "SKIP", reason, 0, skip_reason=reason))
            continue
        vlog(f"\n         ↳ Params: {json.dumps(params, ensure_ascii=False)}")

        start = time.time()
        try:
            resp = client.call_tool(name, params)
            elapsed = int((time.time() - start) * 1000)
            vlog(f"         ↳ Response ({elapsed}ms): {_truncate_json(resp)}")

            text, is_error, http_status = _parse_response(resp)
            passed, reason = _is_connectivity_pass(text, is_error, http_status, resp)

            if passed:
                if reason == "OK":
                    msg = f"OK: {text[:80]}"
                    print(f"✅ PASS ({elapsed}ms)")
                elif reason == "BIZ_ERROR":
                    msg = f"Biz error (chain OK): {text[:100]}"
                    print(f"✅ PASS [biz err] ({elapsed}ms)")
                else:
                    msg = f"Server responded ({reason}): {text[:80]}"
                    print(f"⚠️ PASS [{reason}] ({elapsed}ms)")
                results.append(TestResult(name, module, "auto", params, "PASS", msg, elapsed, raw_request=params, raw_response=resp))
            else:
                msg_short = text[:120] if text else "no response"
                if reason == "TIMEOUT":
                    print(f"❌ TIMEOUT ({elapsed}ms)")
                    msg = f"Timeout: {msg_short}"
                elif reason == "NOT_FOUND_404":
                    print(f"❌ 404 ({elapsed}ms)")
                    msg = f"404 Not Found: {msg_short}"
                elif reason == "AUTH_401":
                    print(f"❌ 401 Auth ({elapsed}ms)")
                    msg = f"401 Auth: {msg_short}"
                elif reason == "FORBIDDEN_403":
                    print(f"❌ 403 Forbidden ({elapsed}ms)")
                    msg = f"403 Forbidden: {msg_short}"
                elif reason == "MCP_ERROR":
                    print(f"❌ MCP Error ({elapsed}ms)")
                    msg = f"MCP Error: {msg_short}"
                else:
                    print(f"❌ FAIL ({elapsed}ms)")
                    msg = f"Error: {msg_short}"
                results.append(TestResult(name, module, "auto", params, "FAIL", msg, elapsed, raw_request=params, raw_response=resp))

        except Exception as e:
            elapsed = int((time.time() - start) * 1000)
            results.append(TestResult(name, module, "auto", params, "ERROR", str(e)[:200], elapsed, raw_request=params, raw_response={"exception": str(e)}))
            print(f"💥 ERROR ({elapsed}ms)")

    return results


# ─── Report Generation ──────────────────────────────────────────────────────

def _classify_http_response(raw_response, message):
    """Classify a test result's HTTP response. Returns (category, http_code, label, verdict).
    verdict: 'ok' = connectivity confirmed, 'warn' = needs attention, 'fail' = broken.
    """
    import re as _re

    search_str = message or ""

    if isinstance(raw_response, dict):
        exec_log = raw_response.get("execute")
        if isinstance(exec_log, dict) and "response_preview" in exec_log:
            search_str += " " + (exec_log.get("response_preview") or "")
            if exec_log.get("error"):
                search_str += " " + str(exec_log["error"])
        else:
            search_str += " " + json.dumps(raw_response, ensure_ascii=False)
    else:
        search_str += " " + str(raw_response)

    sm = _re.search(r'''["']status["']:\s*(\d+)''', search_str)
    http = int(sm.group(1)) if sm else None

    label_m = _re.search(r'''["']label["']:\s*["']([^"'{}]+)''', search_str)
    label = label_m.group(1).strip() if label_m else ""

    if "MCP error" in search_str:
        return "MCP Schema 校验失败", None, "", "warn"

    if http is None or http < 400:
        return "200 OK", 200, "", "ok"

    if http == 502:
        return "502 Bad Gateway", 502, "", "warn"
    if http == 504:
        return "504 Gateway Timeout", 504, "", "warn"
    if http == 500:
        return "500 服务端错误", 500, label, "ok"

    if http == 404:
        if label:
            return "404 业务资源不存在", 404, label, "ok"
        if "Not Found" in search_str and '"body"' in search_str:
            return "404 路由可能不存在", 404, "", "warn"
        return "404 Not Found", 404, "", "warn"

    if http == 403:
        return "403 无权限", 403, label, "fail"
    if http == 401:
        return "401 认证失败", 401, label, "fail"

    if http == 400:
        known_biz = ("ORDER_NOT_FOUND", "ORDER_NOT_EXISTS", "POSITION_EMPTY",
                      "NO_CHANGE", "USER_LOAN_EXCEEDED", "MODE_SET",
                      "ACCOUNT_NOT_FOUND", "MMP_DISABLED", "MMP_DISABLE",
                      "INVALID_CURRENCY", "CONTRACT_NOT_FOUND",
                      "RISK_LIMIT_TABLE_NOT_FOUND", "AUTO_ORDER_NOT_FOUND",
                      "PERPETUAL_CONTRACT_TRANSFER_USDT_EXCEPTION",
                      "OPERATION_ERROR", "BALANCE_NOT_ENOUGH",
                      "FORBIDDEN", "NOT_FOUND")
        known_param = ("INVALID_PARAM_VALUE", "INVALID_ARGUMENT", "INVALID_PARAMS",
                       "MISSING_REQUIRED_PARAM", "COMMON_PARAM_BIND_ERROR",
                       "INVALID_REQUEST_BODY", "AUTO_INVALID_PARAM_PRICE",
                       "INVALID_CREDENTIALS", "MISSING_REQUIRED_HEADER")
        known_srv = ("DATA_ERROR", "INTERNAL_SERVER_ERROR")

        def _label_in(candidates):
            if not label:
                return False
            for c in candidates:
                if label.startswith(c) or c.startswith(label):
                    return True
            return False

        if _label_in(known_biz):
            return "业务错误(预期)", 400, label, "ok"
        if _label_in(known_param):
            return "参数校验(预期)", 400, label, "ok"
        if _label_in(known_srv):
            return "服务端异常", 400, label, "ok"
        if label:
            return f"业务错误(预期)", 400, label, "ok"
        msg_m = _re.search(r'''["']message["']:\s*["']([^"']+)["']''', search_str)
        body_msg = msg_m.group(1).lower() if msg_m else ""
        if "data is being updated" in body_msg or "please check" in body_msg:
            return "服务端异常", 400, "", "warn"
        return "业务错误(预期)", 400, "", "ok"
    return f"{http} Other", http, label, "ok"


def _build_http_analysis(results):
    """Build HTTP response classification. Returns {verdict: {category: [results]}}."""
    analysis = {"ok": defaultdict(list), "warn": defaultdict(list), "fail": defaultdict(list), "skip": []}
    for r in results:
        if r.status == "SKIP":
            analysis["skip"].append(r)
            continue
        cat, http, label, verdict = _classify_http_response(r.raw_response, r.message)
        analysis[verdict][cat].append(r)
    return analysis


def _get_result_http_tag(r):
    """Return (category, http_code, label, verdict) for a single result."""
    if r.status == "SKIP":
        return "SKIP", None, "", "skip"
    return _classify_http_response(r.raw_response, r.message)

def generate_md_report(results, server_name, tools, report_dir, prefix="smoke-test"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(results)
    passed = sum(1 for r in results if r.status == "PASS")
    failed = sum(1 for r in results if r.status == "FAIL")
    errors = sum(1 for r in results if r.status == "ERROR")
    skipped = sum(1 for r in results if r.status == "SKIP")

    modules = defaultdict(list)
    for r in results:
        modules[r.module].append(r)

    analysis = _build_http_analysis(results)
    ok_count = sum(len(v) for v in analysis["ok"].values())
    warn_count = sum(len(v) for v in analysis["warn"].values())
    fail_count = failed + errors
    skip_count = len(analysis["skip"])
    tested = total - skip_count
    conn_rate = ok_count * 100 // tested if tested else 0

    lines = []
    lines.append(f"# MCP 连通性测试报告")
    lines.append(f"")
    lines.append(f"## 测试概要")
    lines.append(f"")
    lines.append(f"| 项目 | 内容 |")
    lines.append(f"|------|------|")
    lines.append(f"| 测试时间 | {now} |")
    lines.append(f"| MCP 服务 | {server_name} |")
    lines.append(f"| 工具总数 | {len(tools)} |")
    lines.append(f"| 测试总数 | {total} |")
    lines.append(f"| ✅ 连通正常 | {ok_count} |")
    lines.append(f"| ⚠️ 需关注 | {warn_count} |")
    lines.append(f"| ❌ 失败 | {fail_count} |")
    lines.append(f"| ⏭ 跳过 | {skip_count} |")
    lines.append(f"| 连通率 | **{conn_rate}%** ({ok_count}/{tested}) |")
    lines.append(f"")
    lines.append(f"> 判断标准：服务端返回业务响应（含400业务错误、403权限、401认证、404订单不存在等）均为**连通正常**，")
    lines.append(f"> 仅 MCP Schema 校验失败、504 超时等为**需关注**，500/服务端异常算连通但会标注。")
    lines.append(f"")

    if warn_count > 0:
        lines.append(f"## ⚠️ 需关注 ({warn_count}个)")
        lines.append(f"")
        lines.append(f"> 以下工具虽然连通，但返回了非预期的错误，可能需要排查。")
        lines.append(f"")
        for cat, items in sorted(analysis["warn"].items()):
            lines.append(f"### {cat} ({len(items)}个)")
            lines.append(f"")
            for r in sorted(items, key=lambda x: x.tool_name):
                _, hc, hl, _ = _get_result_http_tag(r)
                label_tag = f" `{hc} {hl}`" if hl else (f" `{hc}`" if hc else "")
                lines.append(f"- `{r.tool_name}` [{r.module}]{label_tag}")
            lines.append(f"")

    if fail_count > 0:
        lines.append(f"## ❌ 失败 ({fail_count}个)")
        lines.append(f"")
        for r in results:
            if r.status in ("FAIL", "ERROR"):
                icon = "❌" if r.status == "FAIL" else "💥"
                lines.append(f"- {icon} `{r.tool_name}` [{r.module}]: {r.message[:100]}")
        lines.append(f"")

    lines.append(f"## ✅ 连通正常 — 响应分类明细")
    lines.append(f"")
    lines.append(f"> 以下所有工具链路均已打通，按服务端返回类型分类。")
    lines.append(f"")
    ok_200 = analysis["ok"].get("200 OK", [])
    ok_others = {cat: items for cat, items in analysis["ok"].items() if cat != "200 OK"}

    lines.append(f"### 200 OK ({len(ok_200)}个)")
    lines.append(f"")
    if ok_200:
        by_mod = defaultdict(list)
        for r in ok_200:
            by_mod[r.module].append(r.tool_name)
        for mod in sorted(by_mod.keys()):
            tools_list = ", ".join(f"`{t}`" for t in sorted(by_mod[mod]))
            lines.append(f"- **{mod}** ({len(by_mod[mod])}): {tools_list}")
        lines.append(f"")

    for cat in sorted(ok_others.keys()):
        items = ok_others[cat]
        lines.append(f"### {cat} ({len(items)}个)")
        lines.append(f"")
        for r in sorted(items, key=lambda x: x.tool_name):
            _, hc, hl, _ = _get_result_http_tag(r)
            label_tag = f" `{hl}`" if hl else ""
            lines.append(f"- `{r.tool_name}` [{r.module}]{label_tag}")
        lines.append(f"")

    lines.append(f"## 按模块统计")
    lines.append(f"")
    lines.append(f"| 模块 | 总数 | ✅ 连通 | ⚠️ 关注 | ❌ 失败 | ⏭ 跳过 | 连通率 |")
    lines.append(f"|------|------|---------|---------|--------|--------|--------|")
    for mod in sorted(modules.keys()):
        rs = modules[mod]
        m_ok = m_warn = m_fail = m_skip = 0
        for r in rs:
            if r.status == "SKIP":
                m_skip += 1
            else:
                _, _, _, v = _get_result_http_tag(r)
                if v == "ok":
                    m_ok += 1
                elif v == "warn":
                    m_warn += 1
                else:
                    m_fail += 1
            if r.status in ("FAIL", "ERROR"):
                m_fail += 1
                if v == "warn":
                    m_warn -= 1
        mt = len(rs) - m_skip
        rate = f"{m_ok*100//mt}%" if mt else "N/A"
        lines.append(f"| {mod} | {len(rs)} | {m_ok} | {m_warn} | {m_fail} | {m_skip} | {rate} |")
    lines.append(f"")

    status_icon = {"PASS": "✅", "FAIL": "❌", "ERROR": "💥", "SKIP": "⏭"}

    for mod in sorted(modules.keys()):
        lines.append(f"## {mod.upper()} 模块详情")
        lines.append(f"")
        for r in sorted(modules[mod], key=lambda x: x.tool_name):
            cat, http_code, http_label, verdict = _get_result_http_tag(r)
            if r.status in ("FAIL", "ERROR"):
                icon = status_icon[r.status]
                display_status = r.status
            elif verdict == "warn":
                icon = "⚠️"
                display_status = cat
            elif verdict == "ok" and cat != "200 OK":
                icon = "✅"
                display_status = f"连通 ({cat}{' ' + http_label if http_label else ''})"
            else:
                icon = status_icon.get(r.status, "❓")
                display_status = r.status
            ms = f"{r.elapsed_ms}ms" if r.elapsed_ms else "-"
            lines.append(f"### {icon} `{r.tool_name}` ({r.tool_type}) — {display_status} {ms}")
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

    md_path = Path(report_dir) / f"{prefix}-{server_name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path



def generate_html_report(results, server_name, tools, report_dir, prefix="smoke-test"):
    server_display = escape(server_name, quote=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(results)
    passed = sum(1 for r in results if r.status == "PASS")
    failed = sum(1 for r in results if r.status == "FAIL")
    errors = sum(1 for r in results if r.status == "ERROR")
    skipped = sum(1 for r in results if r.status == "SKIP")
    tested = total - skipped

    analysis = _build_http_analysis(results)
    ok_count = sum(len(v) for v in analysis["ok"].values())
    warn_count = sum(len(v) for v in analysis["warn"].values())
    fail_count = failed + errors
    skip_count = len(analysis["skip"])
    conn_rate = ok_count * 100 // tested if tested else 0

    status_class = {"PASS": "pass", "FAIL": "fail", "ERROR": "error", "SKIP": "skip"}
    status_icon = {"PASS": "✅", "FAIL": "❌", "ERROR": "💥", "SKIP": "⏭"}

    results_by_module = defaultdict(list)
    for r in results:
        results_by_module[r.module].append(r)

    rows_by_module = []
    for mod in sorted(results_by_module.keys()):
        rs = sorted(results_by_module[mod], key=lambda x: x.tool_name)
        m_ok = m_warn = m_fail = m_skip = 0
        for r in rs:
            if r.status == "SKIP":
                m_skip += 1
            elif r.status in ("FAIL", "ERROR"):
                m_fail += 1
            else:
                _, _, _, v = _get_result_http_tag(r)
                if v == "ok":
                    m_ok += 1
                else:
                    m_warn += 1
        mt = len(rs) - m_skip
        mrate = f"{m_ok*100//mt}%" if mt else "N/A"

        detail_rows = ""
        for r in rs:
            cat, http_code, http_label, verdict = _get_result_http_tag(r)

            if r.status in ("FAIL", "ERROR"):
                display_cls = status_class[r.status]
                display_icon = status_icon[r.status]
                display_status = r.status
            elif verdict == "warn":
                display_cls = "warn"
                display_icon = "⚠️"
                display_status = cat
            elif verdict == "ok" and cat != "200 OK":
                display_cls = "pass"
                display_icon = "✅"
                hl = f" {http_label}" if http_label else ""
                display_status = f"连通 ({cat}{hl})"
            else:
                display_cls = status_class.get(r.status, "")
                display_icon = status_icon.get(r.status, "")
                display_status = r.status

            elapsed = f"{r.elapsed_ms}ms" if r.elapsed_ms else "-"
            msg_escaped = escape((r.message or "")[:120], quote=True)

            if r.skip_reason:
                skip_escaped = escape(r.skip_reason, quote=True)
                detail_html = f'<div class="detail-skip">Skip reason: {skip_escaped}</div>'
            else:
                params_json = escape(json.dumps(r.params, ensure_ascii=False, indent=2), quote=True)
                resp_raw = ""
                if r.raw_response:
                    resp_raw = escape(json.dumps(r.raw_response, ensure_ascii=False, indent=2)[:1000], quote=True)
                else:
                    resp_raw = msg_escaped
                detail_html = f'''<details><summary>Show request &amp; response</summary>
<div class="detail-block"><b>Request params:</b><pre>{params_json}</pre><b>Response:</b><pre>{resp_raw}</pre></div></details>'''

            detail_rows += f'<tr class="{display_cls}"><td><code>{escape(str(r.tool_name), quote=True)}</code></td><td>{escape(str(r.tool_type), quote=True)}</td><td>{display_icon} {escape(str(display_status), quote=True)}</td><td>{elapsed}</td><td>{msg_escaped}</td></tr>\n'
            detail_rows += f'<tr class="detail-row {display_cls}"><td colspan="5">{detail_html}</td></tr>\n'
        rows_by_module.append((mod, len(rs), m_ok, m_warn, m_fail, m_skip, mrate, detail_rows))

    module_summary_rows = ""
    for mod, cnt, m_ok, m_warn, m_fail, m_skip, mrate, _ in rows_by_module:
        module_summary_rows += f'<tr><td><a href="#{escape(str(mod), quote=True)}">{escape(str(mod), quote=True)}</a></td><td>{cnt}</td><td>{m_ok}</td><td>{m_warn}</td><td>{m_fail}</td><td>{m_skip}</td><td>{mrate}</td></tr>\n'

    module_detail_sections = ""
    for mod, cnt, m_ok, m_warn, m_fail, m_skip, mrate, detail_rows in rows_by_module:
        module_detail_sections += f'''
<h2 id="{escape(str(mod), quote=True)}">{escape(str(mod).upper(), quote=True)} ({cnt} tools, 连通率 {mrate})</h2>
<table><thead><tr><th>Tool</th><th>Type</th><th>Status</th><th>Time</th><th>Message</th></tr></thead>
<tbody>{detail_rows}</tbody></table>
'''

    bar_ok = conn_rate
    bar_warn = (warn_count * 100 // tested) if tested else 0
    bar_fail = 100 - bar_ok - bar_warn

    # Build warn section
    warn_html = ""
    if warn_count > 0:
        warn_html += '<h2>⚠️ 需关注</h2>\n'
        warn_html += '<p style="color:#666;font-size:.9rem">以下工具返回了非预期错误，可能需要排查。</p>\n'
        for cat, items in sorted(analysis["warn"].items()):
            by_mod = defaultdict(list)
            for r in items:
                by_mod[r.module].append(r.tool_name)
            mods_str = ", ".join(f'{m}({len(ts)})' for m, ts in sorted(by_mod.items(), key=lambda x: -len(x[1])))
            tool_tags = []
            for r in sorted(items, key=lambda x: x.tool_name):
                _, hc, hl, _ = _get_result_http_tag(r)
                tag = f'<code>{escape(str(r.tool_name), quote=True)}</code>'
                if hl:
                    tag += f' <span class="tag warn-tag">{escape(str(hl), quote=True)}</span>'
                tool_tags.append(tag)
            tools_html = ", ".join(tool_tags)
            warn_html += f'<div class="warn-group"><h3>{escape(str(cat), quote=True)} ({len(items)}个) <span style="font-weight:400;font-size:.85rem;color:#666">— {escape(str(mods_str), quote=True)}</span></h3>'
            warn_html += f'<div style="font-size:.85rem;line-height:1.8">{tools_html}</div></div>\n'

    # Build fail section
    fail_html = ""
    if fail_count > 0:
        fail_html += '<h2>❌ 失败</h2>\n'
        fail_items = "".join(f'<li><code>{escape(str(r.tool_name), quote=True)}</code> <span class="tag mod">{escape(str(r.module), quote=True)}</span> — {escape((r.message or "")[:80], quote=True)}</li>' for r in results if r.status in ("FAIL", "ERROR"))
        fail_html += f'<div class="fail-group"><ul>{fail_items}</ul></div>\n'

    # Build OK detail section
    ok_detail_html = '<h2>✅ 连通正常 — 响应分类</h2>\n'
    ok_detail_html += '<p style="color:#666;font-size:.9rem;margin-bottom:12px">以下所有工具链路均已打通，按服务端返回类型分类展示。</p>\n'
    ok_detail_html += '<table><thead><tr><th>响应类型</th><th>数量</th><th>工具列表</th></tr></thead><tbody>\n'

    ok_200 = analysis["ok"].get("200 OK", [])
    if ok_200:
        by_mod = defaultdict(list)
        for r in ok_200:
            by_mod[r.module].append(r.tool_name)
        mod_summary = ", ".join(f'{m}({len(ts)})' for m, ts in sorted(by_mod.items(), key=lambda x: -len(x[1])))
        ok_detail_html += f'<tr><td style="color:#22c55e;font-weight:600">200 OK</td><td>{len(ok_200)}</td><td style="font-size:.8rem">{escape(str(mod_summary), quote=True)}</td></tr>\n'

    for cat in sorted(c for c in analysis["ok"] if c != "200 OK"):
        items = analysis["ok"][cat]
        tool_tags = []
        for r in sorted(items, key=lambda x: x.tool_name):
            _, hc, hl, _ = _get_result_http_tag(r)
            tag = f'<code>{escape(str(r.tool_name), quote=True)}</code>'
            if hl:
                tag += f' <span class="tag ok-tag">{escape(str(hl), quote=True)}</span>'
            tool_tags.append(tag)
        tools_str = ", ".join(tool_tags)
        ok_detail_html += f'<tr><td style="color:#0891b2;font-weight:600">{escape(str(cat), quote=True)}</td><td>{len(items)}</td><td style="font-size:.8rem">{tools_str}</td></tr>\n'

    ok_detail_html += '</tbody></table>\n'

    html = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MCP 连通性测试 — {server_display}</title>
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
.bar .ok{{background:#22c55e}}.bar .warn{{background:#f59e0b}}.bar .fail{{background:#ef4444}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.1);margin-bottom:16px;font-size:.9rem}}
th{{background:#f8f8f8;padding:8px 12px;text-align:left;font-weight:600;border-bottom:2px solid #e5e5e5}}
td{{padding:6px 12px;border-bottom:1px solid #f0f0f0}}
tr.pass td:nth-child(3){{color:#16a34a}} tr.fail td:nth-child(3){{color:#dc2626;font-weight:600}} tr.error td:nth-child(3){{color:#dc2626;font-weight:600}} tr.skip td:nth-child(3){{color:#9ca3af}} tr.warn td:nth-child(3){{color:#d97706;font-weight:600}} tr.warn{{background:#fffbeb}}
code{{background:#f1f5f9;padding:2px 6px;border-radius:4px;font-size:.85rem}}
.meta{{color:#888;font-size:.85rem;margin-bottom:16px}}
.detail-row td{{padding:0 12px 8px;border-bottom:1px solid #e5e5e5}}
.detail-block{{background:#f8f9fa;border:1px solid #e5e5e5;border-radius:6px;padding:12px;margin:6px 0;font-size:.82rem}}
.detail-block pre{{background:#fff;border:1px solid #ddd;border-radius:4px;padding:8px;overflow-x:auto;max-height:300px;overflow-y:auto;font-size:.8rem;margin:4px 0 8px}}
.detail-skip{{color:#9ca3af;font-style:italic;font-size:.85rem;padding:4px 0}}
details summary{{cursor:pointer;color:#4b6bfb;font-size:.85rem;padding:4px 0}}
details summary:hover{{text-decoration:underline}}
.fail-group,.warn-group{{background:#fff;border-radius:8px;padding:16px;margin:8px 0;box-shadow:0 1px 3px rgba(0,0,0,.1)}}
.fail-group h3{{font-size:1rem;margin-bottom:8px;color:#ef4444}}
.warn-group h3{{font-size:1rem;margin-bottom:8px;color:#d97706}}
.fail-group ul{{list-style:none;padding:0}}
.fail-group li{{padding:3px 0;font-size:.9rem}}
.tag.mod{{background:#e0e7ff;color:#3b5bdb;padding:1px 6px;border-radius:4px;font-size:.78rem;margin-left:6px}}
.tag.ok-tag{{background:#dcfce7;color:#15803d;padding:1px 6px;border-radius:4px;font-size:.78rem;margin-left:4px}}
.tag.warn-tag{{background:#fef3c7;color:#92400e;padding:1px 6px;border-radius:4px;font-size:.78rem;margin-left:4px}}
.criteria{{background:#f0f9ff;border:1px solid #bae6fd;border-radius:8px;padding:12px 16px;margin:12px 0;font-size:.85rem;color:#0369a1}}
</style></head><body>
<h1>MCP 连通性测试报告</h1>
<div class="meta">{now} &nbsp;|&nbsp; Server: <b>{server_display}</b> &nbsp;|&nbsp; Tools: {len(tools)}</div>
<div class="criteria">
<b>判断标准：</b>服务端返回业务响应（含 400 业务错误、403 权限、401 认证、404 订单不存在等）= <b>✅ 连通正常</b>；
MCP Schema 校验失败、504 超时 = <b>⚠️ 需关注</b>；500/服务端异常 = 连通但标注。
</div>
<div class="summary">
  <div class="card"><div class="num">{total}</div><div class="label">Total</div></div>
  <div class="card"><div class="num" style="color:#22c55e">{ok_count}</div><div class="label">✅ 连通正常</div></div>
  <div class="card"><div class="num" style="color:#d97706">{warn_count}</div><div class="label">⚠️ 需关注</div></div>
  <div class="card"><div class="num" style="color:#ef4444">{fail_count}</div><div class="label">❌ 失败</div></div>
  <div class="card"><div class="num" style="color:#9ca3af">{skip_count}</div><div class="label">⏭ 跳过</div></div>
  <div class="card"><div class="num">{conn_rate}%</div><div class="label">连通率</div></div>
</div>
<div class="bar"><div class="ok" style="width:{bar_ok}%"></div><div class="warn" style="width:{bar_warn}%"></div><div class="fail" style="width:{bar_fail}%"></div></div>
{warn_html}
{fail_html}
{ok_detail_html}
<h2>Module Summary</h2>
<table><thead><tr><th>Module</th><th>Total</th><th>✅ 连通</th><th>⚠️ 关注</th><th>❌ 失败</th><th>⏭ 跳过</th><th>连通率</th></tr></thead>
<tbody>{module_summary_rows}</tbody></table>
{module_detail_sections}
<div class="meta" style="margin-top:32px;text-align:center">Generated by mcp-connectivity-test</div>
</body></html>'''

    # A display name is data, never a filesystem path.
    filename = re.sub(r"[^A-Za-z0-9_.-]", "_", f"{prefix}-{server_name}")
    html_path = Path(report_dir) / f"{filename}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html, encoding="utf-8")
    return html_path


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    global VERBOSE
    parser = argparse.ArgumentParser(description="MCP Smoke Test — 自动化连通性测试")
    parser.add_argument("-v", "--verbose", action="store_true", help="打印详细请求/响应日志")
    parser.add_argument("--filter", type=str, default=None, help="只测试匹配此关键词的工具名（如 'triggered' 或 'spot'）")
    parser.add_argument("server", nargs="?", help="Target MCP server name (overrides config)")
    parsed = parser.parse_args()

    VERBOSE = parsed.verbose

    print("=" * 60)
    print(f"  MCP Connectivity Test — 自动化连通性测试")
    if VERBOSE:
        print("  (Verbose mode ON — 详细请求/响应日志)")
    if parsed.filter:
        print(f"  (Filter: {parsed.filter})")
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

        print(f"\n🧪 Running connectivity tests...\n")

        overrides_data = load_overrides(str(OVERRIDES_PATH))
        if parsed.filter:
            wrapped = {k: v for k, v in wrapped.items() if parsed.filter.lower() in k.lower()}
            print(f"   Filtered to {len(wrapped)} tools matching '{parsed.filter}'")
        results = run_connectivity_tests(client, wrapped, overrides_data)


    except (OSError, ValueError, RuntimeError, TimeoutError, EOFError) as error:
        print(f"❌ Connectivity run stopped: {type(error).__name__}")
        sys.exit(1)
    finally:
        client.stop()

    report_dir = SCRIPT_DIR / config.get("report_dir", "reports")
    print(f"\n📝 Generating reports...")
    report_prefix = f"connectivity-test"
    md_path = generate_md_report(results, server_name, wrapped, report_dir, report_prefix)
    html_path = generate_html_report(results, server_name, wrapped, report_dir, report_prefix)

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
