"""Run a local JSON API backed by the Python Minesweeper engine."""

from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit

from minesweeper_ai.web_adapter import WebGameAdapter


class MinesweeperRequestHandler(BaseHTTPRequestHandler):
    """Map local HTTP requests to a shared ``WebGameAdapter``."""

    adapter = WebGameAdapter()

    def do_GET(self) -> None:
        """Handle read-only API requests."""
        path = urlsplit(self.path).path

        if path == "/":
            self._write_json(
                {
                    "name": "Knowledge-Based Minesweeper AI API",
                    "endpoints": [
                        "POST /api/game",
                        "GET /api/game",
                        "POST /api/game/reveal",
                        "POST /api/game/flag",
                        "GET /api/game/suggestion",
                        "POST /api/game/helper",
                    ],
                }
            )
            return

        if path == "/api/game":
            self._write_json(self.adapter.state())
            return

        if path == "/api/game/suggestion":
            self._write_json(
                {
                    "suggestion": self.adapter.suggest_move(),
                    "game": self.adapter.state(),
                }
            )
            return

        self._write_error(HTTPStatus.NOT_FOUND, "Route not found.")

    def do_POST(self) -> None:
        """Handle game-changing API requests."""
        path = urlsplit(self.path).path

        try:
            if path == "/api/game":
                payload = self._read_json()
                state = self.adapter.new_game(payload.get("difficulty", "easy"))
                self._write_json(state, HTTPStatus.CREATED)
                return

            if path == "/api/game/reveal":
                payload = self._read_json()
                state = self.adapter.reveal(payload["row"], payload["col"])
                self._write_json(state)
                return

            if path == "/api/game/flag":
                payload = self._read_json()
                state = self.adapter.toggle_flag(payload["row"], payload["col"])
                self._write_json(state)
                return

            if path == "/api/game/helper":
                self._write_json(self.adapter.helper_move())
                return
        except KeyError as error:
            self._write_error(
                HTTPStatus.BAD_REQUEST,
                f"Missing field: {error.args[0]}.",
            )
            return
        except (TypeError, ValueError) as error:
            self._write_error(HTTPStatus.BAD_REQUEST, str(error))
            return

        self._write_error(HTTPStatus.NOT_FOUND, "Route not found.")

    def _read_json(self) -> dict[str, object]:
        """Read a JSON object from the request body."""
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)

        if not raw_body:
            return {}

        try:
            payload = json.loads(raw_body)
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise ValueError("Request body must contain valid JSON.") from error

        if not isinstance(payload, dict):
            raise ValueError("Request body must be a JSON object.")
        return payload

    def _write_json(
        self,
        payload: dict[str, object],
        status: HTTPStatus = HTTPStatus.OK,
    ) -> None:
        """Write one JSON response."""
        body = json.dumps(payload, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _write_error(self, status: HTTPStatus, message: str) -> None:
        """Write a JSON error response."""
        self._write_json({"error": message}, status)


def main() -> None:
    """Run the local development API server."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8000, type=int)
    args = parser.parse_args()

    server = HTTPServer((args.host, args.port), MinesweeperRequestHandler)
    print(f"Python-backed Minesweeper API: http://{args.host}:{args.port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
