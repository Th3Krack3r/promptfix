"""PromptFix server. Python 3 standard library only.

Run:  python3 app.py
Then open http://localhost:8000 in a browser.

Optional:  python3 app.py 8899   (or set the PORT env var)
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import config  # noqa: E402
from improve import improve  # noqa: E402

HERE = Path(__file__).parent


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # keep stdout clean
        pass

    def _send(self, status, body, content_type):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            html = (HERE / "index.html").read_text(encoding="utf-8")
            # Inject monetization config; everything else stays static.
            html = html.replace("{{AD_SLOT_HTML}}", config.AD_SLOT_HTML)
            html = html.replace("{{STRIPE_PRO_LINK}}",
                                config.STRIPE_PRO_LINK)
            self._send(200, html, "text/html; charset=utf-8")
        else:
            self._send(404, "Not found", "text/plain; charset=utf-8")

    def do_POST(self):
        if self.path != "/api/improve":
            self._send(404, "Not found", "text/plain; charset=utf-8")
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length) or b"{}")
            prompt = str(payload.get("prompt", ""))
        except (ValueError, TypeError):
            self._send(400, json.dumps({"error": "Invalid JSON"}),
                       "application/json")
            return
        if not prompt.strip():
            self._send(400, json.dumps({"error": "Prompt is empty"}),
                       "application/json")
            return
        if len(prompt) > 5000:
            self._send(400, json.dumps(
                {"error": "Prompt is too long (max 5000 characters)"}),
                "application/json")
            return
        self._send(200, json.dumps(improve(prompt)), "application/json")


def main():
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    elif os.environ.get("PORT"):
        port = int(os.environ["PORT"])
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"PromptFix running at http://localhost:{port} "
          f"(Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
