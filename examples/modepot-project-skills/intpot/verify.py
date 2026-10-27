"""Execute Intpot CLI export and Python conversion against actual CLI and HTTP consumers."""
import argparse
import importlib.util
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request

import intpot
from uvicorn import Config, Server

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from invoice import app, quote


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    args.evidence.mkdir(parents=True, exist_ok=False)
    records = []

    def run(argv, cwd):
        result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=30)
        records.append({"argv": argv, "cwd": str(cwd), "exit_code": result.returncode,
                        "stdout": result.stdout, "stderr": result.stderr})
        (args.evidence / "commands.json").write_text(json.dumps(records, indent=2) + "\n")
        return result

    cases = [(2, 12500, 0), (3, 1099, 100), (1, 0, 0)]
    http_results = []
    with tempfile.TemporaryDirectory(prefix="intpot-invoice-") as directory:
        generated = Path(directory)
        cli = generated / "invoice_cli.py"
        cli_command = str(Path(sys.executable).with_name("intpot"))
        result = run([cli_command, "inspect", str(HERE / "foreign_cli.py"), "--json"], HERE)
        assert result.returncode == 0, result.stderr
        result = run([cli_command, "to", "api", str(HERE / "foreign_cli.py"), "--dry-run"], HERE)
        assert result.returncode == 0, result.stderr
        result = run([cli_command, "eject", str(HERE / "invoice.py"), "--to", "cli",
                      "--output", str(cli)], HERE)
        assert result.returncode == 0, result.stderr
        compile(cli.read_text(), str(cli), "exec")
        for quantity, price, discount in cases:
            argv = [sys.executable, str(cli), str(quantity), str(price)]
            if discount:
                argv += ["--discount-cents", str(discount)]
            result = run(argv, generated)
            assert result.returncode == 0, result.stderr
            assert int(result.stdout.strip()) == quote(quantity, price, discount)
        invalid = run([sys.executable, str(cli), "0", "12500"], generated)
        assert invalid.returncode != 0

        loaded = intpot.load(str(HERE / "foreign_cli.py"))
        assessment = loaded.assess()
        (args.evidence / "assessment.txt").write_text(repr(assessment) + "\n")
        loaded.project("api")
        api_sources = {"native_export": app.eject("api"), "framework_conversion": loaded.to_api()}
        for label, code in api_sources.items():
            path = generated / (label + ".py")
            path.write_text(code)
            compile(code, str(path), "exec")
            spec = importlib.util.spec_from_file_location(label, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[label] = module
            spec.loader.exec_module(module)
            listener = socket.socket()
            listener.bind(("127.0.0.1", 0))
            port = listener.getsockname()[1]
            listener.listen(128)
            server = Server(Config(module.app, log_level="critical"))
            thread = threading.Thread(target=server.run, kwargs={"sockets": [listener]}, daemon=True)
            thread.start()
            try:
                deadline = time.monotonic() + 10
                while not server.started:
                    assert thread.is_alive() and time.monotonic() < deadline, "HTTP startup failed"
                    time.sleep(0.01)

                def request(payload):
                    req = urllib.request.Request(
                        f"http://127.0.0.1:{port}/quote", data=json.dumps(payload).encode(),
                        headers={"Content-Type": "application/json"})
                    try:
                        with urllib.request.urlopen(req, timeout=3) as response:
                            return response.status, json.loads(response.read())
                    except urllib.error.HTTPError as error:
                        raw = error.read().decode()
                        return error.code, raw

                for quantity, price, discount in cases:
                    payload = {"quantity": quantity, "unit_price_cents": price}
                    if discount:
                        # Framework conversion preserves the Typer option's public alias.
                        key = "discount_cents" if label == "native_export" else "discount-cents"
                        payload[key] = discount
                    status, body = request(payload)
                    assert status == 200, (label, status, body)
                    expected = quote(quantity, price, discount)
                    # Native App export returns the value directly. Framework conversion
                    # deliberately wraps non-dict returns (core/transforms.py).
                    expected_body = expected if label == "native_export" else {"result": expected}
                    assert body == expected_body, (label, body, expected_body)
                    http_results.append({"path": label, "input": payload, "status": status, "body": body})
                status, body = request({"quantity": "invalid", "unit_price_cents": 12500})
                assert status == 422, (label, status, body)
                http_results.append({"path": label, "case": "invalid_integer", "status": status})
            finally:
                server.should_exit = True
                thread.join(5)
                listener.close()
                assert not thread.is_alive(), "owned server did not stop"
            with socket.socket() as probe:
                probe.settimeout(0.5)
                assert probe.connect_ex(("127.0.0.1", port)) != 0, "owned listener still open"
        (args.evidence / "http-results.json").write_text(json.dumps(http_results, indent=2) + "\n")
    print(json.dumps({"outcome": "passed", "cli_cases": len(cases), "http_results": http_results,
                      "invalid_cli_rejected": True, "owned_servers_stopped": True}))


if __name__ == "__main__":
    main()
