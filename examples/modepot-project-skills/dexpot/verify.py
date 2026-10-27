"""Assert actual Dexpot HTTP contracts and stop only the owned subprocess."""
import json
from pathlib import Path
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

with socket.socket() as reservation:
    reservation.bind(("127.0.0.1", 0))
    port = reservation.getsockname()[1]

argv = [sys.executable, str(Path(__file__).with_name("app.py")), str(port)]
process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
results = {}
forced_kill = False


def request(path, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(f"http://127.0.0.1:{port}" + path, data=data,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode()


try:
    deadline = time.monotonic() + 10
    while True:
        assert process.poll() is None, "owned server exited before readiness"
        try:
            status, _ = request("/quotes/7")
            if status == 200:
                break
        except (OSError, urllib.error.URLError):
            pass
        assert time.monotonic() < deadline, "HTTP readiness deadline elapsed"
        time.sleep(0.02)
    results["valid_quote"] = request("/quotes", {"customer": "Ari", "amount": 25.5})
    assert results["valid_quote"] == (200, {"quote_id": 41, "customer": "Ari", "amount": 25.5})
    assert "internal_note" not in results["valid_quote"][1]
    results["invalid_body"] = request("/quotes", {"customer": 9, "amount": "bad"})
    assert results["invalid_body"][0] == 422, results["invalid_body"]
    results["typed_path"] = request("/quotes/7")
    assert results["typed_path"] == (200, {"quote_id": 7, "customer": "Ari", "amount": 25.5})
    results["invalid_path"] = request("/quotes/not-an-integer")
    assert results["invalid_path"][0] == 422, results["invalid_path"]
finally:
    if process.poll() is None:
        process.send_signal(signal.SIGINT)
    try:
        stdout, stderr = process.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        forced_kill = True
        process.kill()
        stdout, stderr = process.communicate(timeout=5)
    with socket.socket() as check:
        check.settimeout(0.5)
        assert check.connect_ex(("127.0.0.1", port)) != 0, "owned listener remains open"
    print(json.dumps({"server_argv": argv, "server_exit_code": process.returncode,
                      "server_stdout": stdout, "server_stderr": stderr,
                      "forced_kill": forced_kill, "listener_closed": True,
                      "results": results}))
