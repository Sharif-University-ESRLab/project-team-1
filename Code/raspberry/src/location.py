import time
import serial
import string
import pynmea2
import RPi.GPIO as gpio

PREV_SPEED_MUL = 0.7

ser = None


def init():
    global ser
    gpio.setmode(gpio.BCM)
    port = "/dev/ttyAMA0"  # the serial port to which the pi is connected.
    # create a serial object
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)


# todo: change this code: Yashar
def get_location():
    global ser
    while 1:
        print('sth')
        try:
            data = ser.readline()
        except:
            print("loading")
    # wait for the serial port to churn out data

        # the long and lat data are always contained in the GPGGA string of the NMEA data
        if data[0:6] == '$GPGGA':

            msg = pynmea2.parse(data)

            # parse the latitude and print
            latval = msg.lat
            concatlat = "lat:" + str(latval)
            print(concatlat)

            # parse the longitude and print
            longval = msg.lon
            concatlong = "long:" + str(longval)
            print(concatlong)
        time.sleep(0.5)  # wait a little before picking the next data.


def calc_speed(loc1, loc2, interval):
    # todo: calc speed according to loc1 and loc2. something like dist(loc2, loc1) / interval: Yashar
    pass


def get_speed(locations, prev_speed):
    time1, loc1 = locations[-2]
    time2, loc2 = locations[-1]
    cur_speed = prev_speed * PREV_SPEED_MUL + \
        calc_speed(loc1, loc2, time2-time1) * (1-PREV_SPEED_MUL)
    return cur_speed
