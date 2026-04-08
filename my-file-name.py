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

        if path == "/healthcheck":
            self._send_response(200, {"status": "ok"})

        elif path == "/time":
            now = datetime.utcnow().isoformat()
            self._send_response(200, {"current_time": now})

        elif path == "/hello":
            self._send_response(200, "hello", content_type="text/plain")

        # 1. echo (возвращает query параметры)
        elif path == "/echo":
            self._send_response(200, {"query": query})

        # 2. sum (сумма чисел)
        elif path == "/sum":
            try:
                a = int(query.get("a", [0])[0])
                b = int(query.get("b", [0])[0])
                self._send_response(200, {"result": a + b})
            except ValueError:
                self._send_response(400, {"error": "invalid numbers"}) 

        # 3. user (заглушка пользователя)
        elif path == "/user":
            user_id = query.get("id", [None])[0]

            if user_id:
                response = {
                    "parentA": {
                        "info": "meta-info"
                    },
                    "families": [
                        {
                            "familyName": "Smith",
                            "members": [
                                {
                                    "childrenA": {
                                        "name": "Anna",
                                        "age": 10
                                    }
                                },
                                {
                                    "childrenB": {
                                        "name": "Bob",
                                        "age": 11
                                    }
                                },
                                {
                                    "childrenZ": {
                                        "name": "Mark",
                                        "age": 12
                                    }
                                }
                            ]
                        },
                        {
                            "familyName": "Johnson",
                            "members": [
                                {
                                    "childrenA": {
                                        "name": "Kate",
                                        "age": 9
                                    }
                                },
                                {
                                    "childrenB": {
                                        "name": "Tom",
                                        "age": 13
                                    }
                                }
                            ]
                        }
                    ],
                    "parentC": {
                        "info": "extra-info"
                    }
                }

                self._send_response(200, response)
            else:
                self._send_response(400, {"error": "id is required"})

        # 4./headers — возвращает заголовки запроса
        elif path == "/headers":
            headers_dict = dict(self.headers)
            self._send_response(200, {"headers": headers_dict})

        # 5./status — возвращает заданный статус код
        elif path == "/status":
            try:
                code = int(query.get("code", [200])[0])
                self._send_response(code, {"status": code})
            except ValueError:
                self._send_response(400, {"error": "invalid status code"})

        else:
            self._send_response(404, {"error": "not found"})                   

    # POST endpoint
    def do_POST(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == "/echo-body":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body)
                self._send_response(200, {"you_sent": data})
            except json.JSONDecodeError:
                self._send_response(400, {"error": "invalid json"})


def run(server_class=HTTPServer, handler_class=RequestHandler, port=9990):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    port = 9990
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    run(port=port)



