import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from statoly import Statoly

MONITOR = {
    "id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
    "title": "Homepage",
    "type": "http",
    "status": "up",
    "active": True,
    "metadata": [{"key": "team", "value": "platform"}],
    "createdAt": "2026-01-02T03:04:05Z",
    "updatedAt": "2026-01-02T03:05:05Z",
}

received: list[tuple[str, str]] = []


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 - name imposed by http.server
        received.append((self.path, self.headers.get("Authorization", "")))
        body = json.dumps([MONITOR]).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


@pytest.fixture
def stub():
    server = HTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    received.clear()

    yield f"http://127.0.0.1:{server.server_port}"

    server.shutdown()


@pytest.mark.asyncio
async def test_sends_bearer_token_and_parses_response(stub):
    statoly = Statoly("org_tok_test", base_url=stub)

    monitors = await statoly.monitors.get()

    assert received == [("/monitors", "Bearer org_tok_test")]
    assert len(monitors) == 1
    assert str(monitors[0].id) == MONITOR["id"]
    assert monitors[0].title == "Homepage"
    # The spec says date-time, so the client must hand back a datetime rather
    # than the raw string. This is what the DTO layer exists to guarantee.
    assert monitors[0].created_at.year == 2026
    assert monitors[0].metadata[0].key == "team"


def test_refuses_an_empty_token():
    with pytest.raises(ValueError, match="token is required"):
        Statoly("")
