from threading import Thread
from inout import handle_sensors
from veiw import run_server

# Server port
SERVER_PORT = 8000


def main():
    inout_thread = Thread(
        target=handle_sensors, args=None, name='sensors-thread', daemon=True)
    view_thread = Thread(
        target=run_server, args=(SERVER_PORT,), name='view-thread', daemon=True)

    # todo: wait for threads' initializations?
    inout_thread.start()
    view_thread.start()

    inout_thread.join()
    view_thread.join()


if __name__ == '__main__':
    main()
