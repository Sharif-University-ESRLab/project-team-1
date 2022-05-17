from threading import Thread
from modules import handle_gps, handle_modules
from server import run_server
import sign_detection.main as sign_detection
import location

# Server port
SERVER_PORT = 8000

def init():
    sign_detection.init()
    location.init()


def create_threads():
    modules_thread = Thread(
        target=handle_modules, args=None, name='modules-thread', daemon=True)
    server_thread = Thread(
        target=run_server, args=(SERVER_PORT,), name='server-thread', daemon=True)

    # todo: wait for threads' initializations?
    modules_thread.start()
    server_thread.start()

    modules_thread.join()
    server_thread.join()


def main():
    init()
    print(sign_detection.predict_pic('20limit.png'))
    # handle_modules()
    # create_threads()


if __name__ == '__main__':
    main()
