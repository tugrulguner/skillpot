"""Deterministic loopback HTTP consumer verification; no live provider."""
from __future__ import annotations

import json
import socket
import threading
import time
import urllib.error
import urllib.request

import invoice_app as app
from summonpot import Exactly, FromRequest, Operation, Required, Summon
from summonpot.runtime import Runtime
from summonpot.server import build_app
from uvicorn import Config, Server


# Guard the actual model-backed branch, after deterministic dispatch selection.
original_agent_for = Runtime._agent_for


def forbidden_model_path(self, endpoint):
    raise AssertionError("model-backed branch entered during deterministic invoice probe")


Runtime._agent_for = forbidden_model_path


def post(port: int, body: dict) -> tuple[int, object]:
    request = urllib.request.Request(
        f"http://127.0.0.1:{port}/quote",
        data=json.dumps(body).encode(),
        headers={"content-type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read())


def verify_registration_rejection() -> None:
    def operation(hours: int) -> app.InvoiceQuote:
        return app.InvoiceQuote(customer="Acme", amount_cents=hours)

    contract = Operation(operation, bind={"missing": FromRequest("hours")}, output=app.InvoiceQuote)
    instance = Summon("invalid-registration")
    try:
        @instance("/invalid")
        def endpoint(request: app.QuoteRequest,
                     result=Required(contract, calls=Exactly(1))) -> app.InvoiceQuote:
            """Invalid contract must fail during registration."""
            ...
    except TypeError as error:
        expected = ("Endpoint 'endpoint' binds 'missing' for operation 'operation', "
                    "which takes no such argument. It takes: hours.")
        assert str(error) == expected, str(error)
        return
    raise AssertionError("invalid operation registration unexpectedly succeeded")


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("127.0.0.1", 0))
port = sock.getsockname()[1]
sock.listen(128)
server = Server(Config(build_app(app.summon), host="127.0.0.1", port=port, log_level="error"))
thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
try:
    thread.start()
    deadline = time.monotonic() + 5
    while not server.started and thread.is_alive() and time.monotonic() < deadline:
        time.sleep(0.01)
    assert server.started, "server readiness deadline elapsed"
    valid = post(port, {"customer": "Acme", "hours": 2})
    bad_customer = post(port, {"customer": "A", "hours": 2})
    bad_hours = post(port, {"customer": "Acme", "hours": 0})
    assert valid == (200, {"customer": "Acme", "amount_cents": 25000}), valid
    assert bad_customer[0] == 422, bad_customer
    assert bad_hours[0] == 422, bad_hours
    assert app.capability_calls == [("Acme", 2)], app.capability_calls
    verify_registration_rejection()
    print(json.dumps({"valid": valid, "bad_customer": bad_customer, "bad_hours": bad_hours,
                      "capability_calls": app.capability_calls,
                      "capability_call_count": len(app.capability_calls),
                      "model_path_guard": "installed Runtime._agent_for raises if entered",
                      "invalid_registration": "rejected with exact TypeError/message"}, sort_keys=True))
finally:
    server.should_exit = True
    if thread.ident is not None:
        thread.join(timeout=5)
    sock.close()
    Runtime._agent_for = original_agent_for
    assert not thread.is_alive(), "server thread did not stop"
    # Prove the selected loopback port is no longer bound/listening.
    check = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        check.settimeout(0.25)
        result = check.connect_ex(("127.0.0.1", port))
        assert result != 0, f"server port {port} remained open (connect_ex={result})"
    finally:
        check.close()
    print("SERVER_STOPPED_AND_PORT_CLOSED")
