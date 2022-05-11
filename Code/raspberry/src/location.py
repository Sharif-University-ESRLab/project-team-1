from cmath import acos
import time
import serial
import string
import pynmea2
import RPi.GPIO as gpio
from math import pi, cos, sin

PREV_SPEED_MUL = 0.7

SERIAL_PORT = "/dev/serial0"


gps = None


def init():
    global gps
    print("GPS is started!")
    gps = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=0.5)


def formatDegreesMinutes(coordinates, digits):

    parts = coordinates.split(".")

    if (len(parts) != 2):
        return coordinates

    if (digits > 3 or digits < 2):
        return coordinates

    left = parts[0]
    right = parts[1]
    degrees = str(left[:digits])
    minutes = str(right[:3])

    return degrees + "." + minutes


def get_location():
    global gps
    while True:
        data = gps.readline().decode().strip()
        message = data[0:6]
        if message == "$GPRMC":
            parts = data.split(",")
            if parts[2] == 'V':
                print("GPS receiver warning")
            else:
                longitude = formatDegreesMinutes(parts[5], 3)
                latitude = formatDegreesMinutes(parts[3], 2)
                print("Your position: lon = " +
                      str(longitude) + ", lat = " + str(latitude))
                return longitude, latitude


def calc_dist(loc1, loc2):
    loc1, loc2 = loc1 * pi / 180, loc2 * pi / 180
    e_rad = 6378100
    z1, rho1 = e_rad * sin(loc1[1]), e_rad * cos(loc1[1])
    x1, y1 = rho1 * cos(loc1[0]), rho1 * sin(loc1[0])
    z2, rho2 = e_rad * sin(loc2[1]), e_rad * cos(loc2[1])
    x2, y2 = rho2 * cos(loc2[0]), rho2 * sin(loc2[0])
    mul = x1 * x2 + y1 * y2 + z1 * z2
    theta = acos(mul / (e_rad * e_rad))
    return e_rad * theta


def calc_speed(loc1, loc2, interval):
    dist = calc_dist(loc1, loc2)
    mps_vel = dist / interval
    print(mps_vel + ' m/s')
    kph_vel = mps_vel * 60 / 1000
    return int(kph_vel)


def get_speed(locations, prev_speed):
    time1, loc1 = locations[-2]
    time2, loc2 = locations[-1]
    cur_speed = prev_speed * PREV_SPEED_MUL + \
        calc_speed(loc1, loc2, time2-time1) * (1-PREV_SPEED_MUL)
    return cur_speed
