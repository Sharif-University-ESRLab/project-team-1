from threading import Thread
from time import sleep, time
from datetime import date, datetime
import os


t = datetime.now()
print(t)
print(datetime.timestamp(t))

t = time()
print(t)
print(datetime.fromtimestamp(t))