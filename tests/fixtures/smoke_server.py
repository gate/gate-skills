"""Synthetic stdio peer for smoke-runner tests; never opens a socket or uses keys."""

import json
import os
import signal
import sys
from pathlib import Path


def main():
    """Serve only the declared synthetic tools and record calls for assertions."""
    scenario = json.loads(Path(sys.argv[1]).read_text())
    if scenario.get("peer_pid"):
        Path(scenario["peer_pid"]).write_text(str(os.getpid()))
    for line in sys.stdin:
        request = json.loads(line)
        method = request["method"]
        if method == "notifications/initialized":
            continue
        # Faults are synthetic transport events; no network or credentials exist here.
        if scenario.get("silence") == method:
            continue
        if scenario.get("eof") == method:
            return
        if scenario.get("partial") == method:
            sys.stdout.write('{"jsonrpc":'); sys.stdout.flush()
            continue
        if scenario.get("malformed") == method:
            print("not-json", flush=True)
            continue
        if scenario.get("stderr_bytes") and method == "tools/call":
            sys.stderr.write("x" * scenario["stderr_bytes"]); sys.stderr.flush()
        for _ in range(scenario.get("unmatched", 0)):
            print(json.dumps({"jsonrpc": "2.0", "method": "synthetic/notice"}), flush=True)
        response = {"jsonrpc": "2.0", "id": request["id"]}
        if method == "initialize":
            response["result"] = {"protocolVersion": "2024-11-05", "capabilities": {}}
        elif method == "tools/list":
            response["result"] = {"tools": scenario["tools"]}
        elif method == "tools/call":
            with Path(scenario["calls"]).open("a") as log:
                log.write(json.dumps(request["params"]) + "\n")
            if scenario.get("error"):
                response["error"] = {"code": -32602, "message": "schema validation failed"}
            else:
                text = "x" * scenario["response_bytes"] if scenario.get("response_bytes") else "fixture response"
                response["result"] = {"content": [{"type": "text", "text": text}]}
        else:
            response["error"] = {"code": -32601, "message": "unsupported fixture method"}
        if scenario.get("wrong_id") and method == "tools/call":
            response["id"] = True  # JSON booleans must not match numeric request IDs.
        print(json.dumps(response), flush=True)
        if scenario.get("pause_after_list") and method == "tools/list":
            signal.pause()  # Synthetic peer stops consuming stdin until cleanup signals it.


if __name__ == "__main__":
    main()
