from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import json
import sys

class RequestHandler(BaseHTTPRequestHandler):

    def _send_response(self, code, body, content_type="application/json"):
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.end_headers()

        if isinstance(body, (dict, list)):
            body = json.dumps(body)

        self.wfile.write(body.encode("utf-8"))

    def do_GET(self):
        if self.path == "/healthcheck":
            self._send_response(200, {"status": "ok"})

        elif self.path == "/endpoint-error":
            self._send_response(200, {"status": "erRor"})

        elif self.path == "/crazy":
            self._send_response(200, {"status": "yes"})

        elif self.path == "/time":
            now = datetime.utcnow().isoformat()
            self._send_response(200, {"current_time": now})

        elif self.path == "/hello":
            self._send_response(200, "hello", content_type="text/plain")

        else:
            self._send_response(404, {"error": "not found"})


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    run(port=port)