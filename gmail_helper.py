import argparse
import json
import os
import urllib.request
from pathlib import Path
from urllib.parse import urlencode

from dotenv import load_dotenv

parser = argparse.ArgumentParser(description="Read-only Gmail bridge helper")
parser.add_argument("--query", default=None, help="Gmail search query")
args = parser.parse_args()

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

token = os.getenv("JOE_BRIDGE_TOKEN")

if not token:
    print(json.dumps({"error": "Bridge authentication not configured"}))
    raise SystemExit(1)

url = "http://127.0.0.1:8765/emails"
if args.query is not None:
    url += "?" + urlencode({"q": args.query})

request = urllib.request.Request(
    url,
    headers={"X-Joe-Token": token},
    method="GET",
)

try:
    with urllib.request.urlopen(request, timeout=15) as response:
        emails = json.load(response)

    print(json.dumps(emails, indent=2))

except Exception:
    print(json.dumps({
        "error": "Unable to retrieve emails from the local Gmail bridge"
    }))
    raise SystemExit(1)