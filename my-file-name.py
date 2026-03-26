from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import json
import sys
from urllib.parse import urlparse, parse_qs


class RequestHandler(BaseHTTPRequestHandler):

    def _send_response(self, code, body, content_type="application/json"):
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.end_headers()

        if isinstance(body, (dict, list)):
            body = json.dumps(body)

        self.wfile.write(body.encode("utf-8"))

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        if self.path == "/healthcheck":
            self._send_response(200, {"status": "ok"})

        elif self.path == "/time":
            now = datetime.utcnow().isoformat()
            self._send_response(200, {"current_time": now})

        elif self.path == "/hello":
            self._send_response(200, "hello", content_type="text/plain")

        # 1. echo (возвращает query параметры)
        elif path == "/echo":
            self._send_response(200, {"query": query})

        else:
            self._send_response(404, {"error": "not found"})


    # POST endpoint
    def do_POST(self):
        if self.path == "/echo-body":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body)
                self._send_response(200, {"you_sent": data})
            except json.JSONDecodeError:
                self._send_response(400, {"error": "invalid json"})


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



