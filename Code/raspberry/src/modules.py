from time import sleep
from time import time as get_time
import threading

import sign_detection.main as sign_detection
import location

# Periods are in second
CLK_PERIOD = 0.1
CAMERA_PERIOD = 1.0
GPS_PERIOD = 1.0

REOCRD_FILE = "./trajectory_history_30"

# Used for synchronization when threads access below variables.
lock = threading.Lock()

# These are used to store data as time passes.
locations = []  # Locations of the car in different timestamps
distances = []  # Speeds of the car in different timestamps
prev_dist = 0  # Last calculated speed
signs = []  # Traffic signs detected in different timestamps
speed_limits = []   # Speed limits in different timestamps


# Handles camera module.
def handle_camera(cur_time):
    global speed_limits, signs, lock

    lock.acquire()
    prediction = sign_detection.get_random_sign(0.2)
    if prediction != None:
        signs.append((cur_time, prediction[0]))
    new_speed_lim = sign_detection.get_speed_limit(speed_limits, signs)
    speed_limits.append((cur_time, new_speed_lim))
    lock.release()


# Handle GPS module and do the jobs related to the car's location and speed
def handle_gps():
    global locations, distances, prev_dist, lock, speed_limits

    lock.acquire()
    loc = location.get_location()
    locations.append(loc)
    cur_dist = location.get_dist(locations, prev_dist)
    distances.append(cur_dist)
    trajectory_histroy = open(REOCRD_FILE, "w")
    trajectory_histroy.write(f"{'{'}\"distance\":{cur_dist}, \"limit\":{speed_limits[-1]}{'}'}\n")
    prev_dist = cur_dist
    trajectory_histroy.close()
    lock.release()


# Handles modules and calls their functions periodically.
def handle_modules():
    last_camera_clk = 0
    while True:
        start = get_time()

        if get_time() - start > GPS_PERIOD:
            handle_gps()
        if start - last_camera_clk > CAMERA_PERIOD:
            last_camera_clk = start
            handle_camera(start)

        now = get_time()
        sleep(CLK_PERIOD - (now - start))
