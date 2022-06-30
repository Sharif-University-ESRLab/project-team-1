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


# Initializes gps.
def init():
    global gps
    print("GPS is started!")
    gps = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=0.5)


# Formats gps information.
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


# Reads a location from gps stream.
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


# Calculates destination between LOC1 and LOC2.
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


# Gets speed based on locations data and previous speed.
def get_dist(locations, prev_speed):
    if len(locations) < 2:
        return 0
    loc1 = locations[-2]
    loc2 = locations[-1]
    cur_dist = calc_dist(loc1, loc2)
    return cur_dist
