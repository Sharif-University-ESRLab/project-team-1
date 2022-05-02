import RPi.GPIO as GPIO
import time

BuzzPin = 11

def setup(pin):
    global BuzzerPin
    BuzzerPin = pin
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.output(BuzzerPin, GPIO.HIGH)


def on():
    GPIO.output(BuzzerPin, GPIO.LOW)


def off():
    GPIO.output(BuzzerPin, GPIO.HIGH)


def beep(x):
    print('beep')
    on()
    time.sleep(x)
    off()
    time.sleep(x)

def loop(v):
    while True:
        beep(v)

def destroy():
    GPIO.output(BuzzerPin, GPIO.HIGH)
    GPIO.cleanup()


setup(BuzzPin)
try:
    loop(1)

except KeyboardInterrupt:
    destroy()
