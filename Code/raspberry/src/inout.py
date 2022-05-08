from time import sleep
from time import time as cur_time

# Periods are in second
CLK_PERIOD = 0.1



def handle_camera():
    pass


def handle_gps():
    pass


# todo: needed?
def handle_buzzer():
    pass


def handle_sensors():
    while True:
        start = cur_time()
        handle_gps()
        handle_camera()
        handle_buzzer()
        now = cur_time()
        sleep(CLK_PERIOD - (now-start))
