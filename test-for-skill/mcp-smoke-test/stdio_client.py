"""One bounded stdio transport; never retries a tool or emits peer diagnostics."""
import json
import math
import os
import selectors
import signal
import subprocess
import time

MAX_MESSAGE = 8 * 1024 * 1024
MAX_EXCHANGE = 20 * 1024 * 1024
MAX_EVENTS = 1024


class McpStdioClient:
    """Own the subprocess, framing, deadlines and cleanup for sequential requests."""

    def __init__(self, command, args, env=None, timeout=30):
        if not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or not 0 < timeout <= 300:
            raise ValueError("timeout must be finite and within (0, 300] seconds")
        self.command, self.args = command, args
        self.env = {**os.environ, **(env or {})}
        self.timeout = timeout
        self.process = None
        self._selector = None
        self._buffer = bytearray()
        self._id = 0
        self._busy = False
        self._bytes = 0
        self._frame_size = 0

    def start(self):
        """Configure nonblocking pipes before the first protocol exchange."""
        if os.name != "posix":
            raise RuntimeError("bounded stdio transport requires a POSIX host")
        if self.process is not None:
            raise RuntimeError("client already started")
        try:
            self.process = subprocess.Popen(
                [self.command, *self.args], stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                env=self.env, start_new_session=True, bufsize=0)
            self._selector = selectors.DefaultSelector()
            for pipe in (self.process.stdin, self.process.stdout, self.process.stderr):
                os.set_blocking(pipe.fileno(), False)
            self._selector.register(self.process.stdout, selectors.EVENT_READ, "stdout")
            self._selector.register(self.process.stderr, selectors.EVENT_READ, "stderr")
            response = self._request("initialize", {
                "protocolVersion": "2024-11-05", "capabilities": {},
                "clientInfo": {"name": "mcp-smoke-test", "version": "1.0.0"}})
            if "error" in response or not isinstance(response.get("result"), dict):
                raise ValueError("initialization failed")
            self._request("notifications/initialized", notification=True)
        except BaseException:
            self.stop()
            raise

    def _pump(self, deadline):
        """Drain both read pipes while waiting; stderr is discarded, never logged."""
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("stdio deadline exceeded")
        events = self._selector.select(remaining)
        if not events:
            raise TimeoutError("stdio deadline exceeded")
        writable = False
        for key, _ in events:
            if key.data == "stdin":
                writable = True
                continue
            chunk = os.read(key.fileobj.fileno(), 65536)
            if not chunk:
                self._selector.unregister(key.fileobj)
                if key.data == "stdout":
                    raise EOFError("peer closed stdout before completing the response")
                continue
            self._bytes += len(chunk)
            if self._bytes > MAX_EXCHANGE:
                raise ValueError("stdio exchange byte limit exceeded")
            if key.data == "stdout":
                self._buffer.extend(chunk)
                # Inspect each new byte once instead of repeatedly splitting a growing frame.
                parts = chunk.split(b"\n")
                for index, part in enumerate(parts):
                    self._frame_size += len(part)
                    if self._frame_size > MAX_MESSAGE:
                        raise ValueError("stdio message byte limit exceeded")
                    if index < len(parts) - 1:
                        self._frame_size = 0
        return writable

    def _write(self, payload, deadline):
        pipe = self.process.stdin
        self._selector.register(pipe, selectors.EVENT_WRITE, "stdin")
        try:
            remaining = memoryview(payload)
            while remaining:
                if self._pump(deadline):
                    written = os.write(pipe.fileno(), remaining)
                    remaining = remaining[written:]
        finally:
            if self._selector is not None:
                self._selector.unregister(pipe)

    def _recv(self, deadline):
        while b"\n" not in self._buffer:
            self._pump(deadline)
        line, _, rest = self._buffer.partition(b"\n")
        self._buffer = bytearray(rest)
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError("JSON-RPC response must be an object")
        return value

    def _request(self, method, params=None, notification=False):
        """A timeout invalidates the transport so late replies cannot satisfy another call."""
        if self.process is None:
            raise RuntimeError("client is not running")
        if self._busy:
            raise RuntimeError("concurrent stdio requests are not supported")
        self._busy = True
        self._bytes = 0
        deadline = time.monotonic() + self.timeout
        self._id += 1
        request_id = self._id
        request = {"jsonrpc": "2.0", "method": method}
        if not notification:
            request["id"] = request_id
        if params is not None:
            request["params"] = params
        try:
            payload = (json.dumps(request) + "\n").encode()
            if len(payload) > MAX_MESSAGE:
                raise ValueError("stdio request byte limit exceeded")
            self._write(payload, deadline)
            if notification:
                return None
            for _ in range(MAX_EVENTS):
                if time.monotonic() >= deadline:
                    raise TimeoutError("stdio deadline exceeded")
                response = self._recv(deadline)
                if time.monotonic() >= deadline:
                    raise TimeoutError("stdio deadline exceeded")
                if type(response.get("id")) is int and response["id"] == request_id and ("result" in response or "error" in response):
                    return response
            raise ValueError("stdio unmatched event limit exceeded")
        except BaseException:
            self.stop()
            raise
        finally:
            self._busy = False

    def call_tool(self, name, arguments=None):
        try:
            return self._request("tools/call", {"name": name, "arguments": arguments or {}})
        except TimeoutError:
            return {"error": {"code": -1, "message": "Timeout"}}

    def list_tools(self):
        response = self._request("tools/list")
        result = response.get("result")
        if "error" in response or not isinstance(result, dict) or not isinstance(result.get("tools"), list):
            raise ValueError("invalid tools/list response")
        return result["tools"]

    def stop(self):
        """Reap the whole owned process group and close every pipe on all exit paths."""
        process, self.process = self.process, None
        if process is None:
            return
        def signal_group(sig):
            try:
                os.killpg(process.pid, sig)
            except ProcessLookupError:
                pass
            except PermissionError:
                # Some POSIX hosts deny signalling an already reaped group. A live
                # process must still surface failure; it cannot be silently abandoned.
                if process.poll() is None:
                    raise

        try:
            for sig, grace in ((signal.SIGTERM, 1), (signal.SIGKILL, 1)):
                signal_group(sig)
                try:
                    process.wait(timeout=grace)
                    break
                except subprocess.TimeoutExpired:
                    continue
            else:
                raise RuntimeError("stdio subprocess did not exit after SIGKILL")
        finally:
            try:
                # A wrapper may exit while its descendants ignore SIGTERM.
                signal_group(signal.SIGKILL)
            finally:
                if self._selector is not None:
                    self._selector.close()
                    self._selector = None
                for pipe in (process.stdin, process.stdout, process.stderr):
                    if pipe is not None:
                        pipe.close()
                self._buffer.clear()
                self._frame_size = 0
