import bpy
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading


class HttpRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["content-length"])
        body = self.rfile.read(content_length).decode("utf-8")

        json_obj = json.loads(body)

        path = json_obj["path"]

        bpy.types.Scene.ImportReq = path
        self.send_response(201)
        self.wfile.write(b"")


def setup():
    start_http_server()


def start_http_server():
    def launch_server():
        with HTTPServer(("localhost", 7225), HttpRequestHandler) as server:
            server.serve_forever()

    thread = threading.Thread(target=launch_server)
    thread.daemon = True
    thread.start()
