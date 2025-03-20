from waitress import serve
from flask import Flask, send_from_directory
from threading import Event, Thread
from time import sleep


APP = Flask(__name__, static_folder="../../pki-front-end/dist")


@APP.route('/')
def index():
    return send_from_directory(APP.static_folder, "index.html")


def start_socket() -> None:
    # TODO: Confirm this is the place to listen from
    serve(APP, listen='0.0.0.0:5000')


def start_socket_thread(stop_event: Event) -> None:
    server_thread = Thread(target=start_socket, daemon=True)
    server_thread.start()

    while not stop_event.is_set():
        sleep(1)
