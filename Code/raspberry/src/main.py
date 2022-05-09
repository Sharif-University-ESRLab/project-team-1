from threading import Thread
from handler import handle_sensors
from server import run_server
import sign_detection.main as sign_detection
import location
from time import sleep

# Server port
SERVER_PORT = 8000


def init():
    sign_detection.init()
    # location.init()


def create_threads():
    inout_thread = Thread(
        target=handle_sensors, args=None, name='modules-thread', daemon=True)
    view_thread = Thread(
        target=run_server, args=(SERVER_PORT,), name='view-thread', daemon=True)

    # todo: wait for threads' initializations?
    inout_thread.start()
    view_thread.start()

    inout_thread.join()
    view_thread.join()


def main():
    init()
    print(sign_detection.predict_pic('20limit.png'))
    # create_threads()


if __name__ == '__main__':
    main()
