"""Local read-only Gmail bridge for Joe."""

import json
import os
import secrets
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit, parse_qs

from dotenv import load_dotenv
from main import ROOT, gmail_service, fetch_messages

load_dotenv(ROOT / ".env")

BRIDGE_TOKEN = os.getenv("JOE_BRIDGE_TOKEN")
if not BRIDGE_TOKEN:
    raise RuntimeError("JOE_BRIDGE_TOKEN is missing from .env")


HOST = "127.0.0.1"
PORT = 8765


class JoeBridge(BaseHTTPRequestHandler):
    def do_GET(self):
        request_url = urlsplit(self.path)
        if request_url.path != "/emails":
            self.send_error(404)
            return

        supplied_token = self.headers.get("X-Joe-Token", "")

        if not secrets.compare_digest(supplied_token, BRIDGE_TOKEN):
            self.send_error(401, "Unauthorized")
            return

        query = parse_qs(request_url.query).get("q", ["in:inbox"])[0]

        try:
            messages = fetch_messages(
                gmail_service(),
                count=5,
                query=query
            )

            results = [
                {
                    "from": msg["from"],
                    "subject": msg["subject"],
                    "date": msg["date"]
                }
                for msg in messages
            ]

            response = json.dumps(
                {"emails": results},
                ensure_ascii=False
            ).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

        except Exception:
            self.send_error(500, "Unable to retrieve emails")


if __name__ == "__main__":
    print(f"Joe Gmail bridge running at http://{HOST}:{PORT}")
    HTTPServer((HOST, PORT), JoeBridge).serve_forever()