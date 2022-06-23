from threading import Thread
from modules import handle_modules
from server import run_server
import sign_detection.main as sign_detection
import location

# Server port
SERVER_PORT = 8000


# Initializes program modules.
def init():
    sign_detection.init()
    location.init()


# Create program threads.
def create_threads():
    # Handles modules.
    modules_thread = Thread(
        target=handle_modules, args=None, name='modules-thread', daemon=True)
    # Handles the server serving the android app.
    server_thread = Thread(
        target=run_server, args=(SERVER_PORT,), name='server-thread', daemon=True)

    modules_thread.start()
    server_thread.start()

    modules_thread.join()
    server_thread.join()


def main():
    init()
    create_threads()


if __name__ == '__main__':
    main()
