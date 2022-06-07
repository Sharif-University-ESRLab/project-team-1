from time import sleep
from time import time as get_time
import threading

import sign_detection.main as sign_detection
import location

# Periods are in second
CLK_PERIOD = 0.1
CAMERA_PERIOD = 1.0

# Used for synchronization when threads access below variables.
lock = threading.Lock()

# These are used to store data as time passes.
locations = []  # Locations of the car in different timestamps
speeds = [] # Speeds of the car in different timestamps
prev_speed = 0  # Last calculated speed
signs = [] # Traffic signs detected in different timestamps
speed_limits = []   # Speed limits in different timestamps


def handle_camera(cur_time):
    global speed_limits, signs, lock

    lock.acquire()
    pic_name = 'None'  # replace 'None' with camera-capture-pic function: Yashar
    prediction = sign_detection.predict_pic(pic_name)
    if prediction != None:
        signs.append((cur_time, prediction[0]))
    new_speed_lim = sign_detection.get_speed_limit(speed_limits, signs)
    # if new_speed_lim != None:
    speed_limits.append((cur_time, new_speed_lim))
    lock.release()


# Handle GPS module and do the jobs related to the car's location and speed
def handle_gps(cur_time):
    global locations, speeds, prev_speed, lock
    
    lock.acquire()
    loc = location.get_location()
    locations.append((cur_time, loc))
    cur_speed = location.get_speed(locations, prev_speed)
    speeds.append((cur_time, cur_speed))
    prev_speed = cur_speed
    lock.release()


# Main module handling function which calls other functions periodically
def handle_modules():
    last_camera_clk = 0
    while True:
        start = get_time()

        handle_gps(start)
        if start - last_camera_clk > CAMERA_PERIOD:
            last_camera_clk = start
            # handle_camera(start)
        # handle_buzzer(start)
        
        now = get_time()
        sleep(CLK_PERIOD - (now - start))
