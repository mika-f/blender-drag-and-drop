import bpy
import flask
import os
import threading


def setup():
    start_flask_server()


def start_flask_server():
    def launch_server():
        try:
            server.run(debug=True, port=7225, use_reloader=False)
            print("start flask server at port 7225")
        except OSError:
            print("failed to launch flask server at port 7225")

    thread = threading.Thread(target=launch_server)
    thread.daemon = True
    thread.start()


server = flask.Flask("Blender Server")
server.config["JSON_AS_ASCII"] = False


# get JSON from launcher such as { "path": "/c/path/to/drag/and/drop/file.fbx" }
@server.route("/", methods=["POST"])
def root():
    request = flask.request
    json = request.get_json()

    path = json["path"]
    _, ext = os.path.splitext(path)

    bpy.types.Scene.ImportReq = path
    return flask.Response(status=201)
