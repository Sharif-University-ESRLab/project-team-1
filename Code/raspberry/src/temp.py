from threading import Thread
from time import sleep
from datetime import datetime


def f():
    while True:
        sleep(1)
        print('hi')


# t = Thread(target=f, daemon=False)
# t.start()
# t.join()

print(datetime.now())