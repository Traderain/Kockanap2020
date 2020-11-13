import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler


class S(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.rfile.read())

    def do_HEAD(self):
        print(self.rfile.read())

    def do_POST(self):
        print(self.rfile.read())


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()
