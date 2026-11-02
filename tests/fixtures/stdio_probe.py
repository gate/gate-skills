"""Run the real transport in a bounded subprocess; only its peer is synthetic."""
import importlib.util
import json
from pathlib import Path
import sys
import time


def main():
    """Capture observable cleanup without exposing peer messages or credentials."""
    root, scenario = Path(sys.argv[1]), Path(sys.argv[2])
    spec = importlib.util.spec_from_file_location("transport", root / "test-for-skill/mcp-smoke-test/stdio_client.py")
    transport = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(transport)
    client = transport.McpStdioClient(
        sys.executable, ["-B", str(root / "tests/fixtures/smoke_server.py"), str(scenario)], timeout=json.loads(scenario.read_text()).get("probe_timeout", 0.2))
    started = time.monotonic()
    process = None
    result = {}
    try:
        client.start()
        process = client.process
        result["tools"] = client.list_tools()
        fixture = json.loads(scenario.read_text())
        size = fixture.get("request_bytes", 1024 * 1024 if fixture.get("pause_after_list") else 0)
        arguments = {"payload": "x" * size} if size else {}
        reply = client.call_tool("cex_spot_list_currency_pairs", arguments)
        result["timeout"] = reply.get("error", {}).get("message") == "Timeout"
    except Exception as error:
        result["error"] = type(error).__name__
        result["detail"] = str(error)[:160]
    finally:
        # start() also owns cleanup on a failed handshake.
        client.stop()
    result["elapsed"] = time.monotonic() - started
    result["running"] = client.process is not None
    if process is not None:
        result["exited"] = process.poll() is not None
        result["pipes_closed"] = all(p.closed for p in (process.stdin, process.stdout, process.stderr))
        result["pipe_states"] = [p.closed for p in (process.stdin, process.stdout, process.stderr)]
    print(json.dumps(result))


if __name__ == "__main__":
    main()
