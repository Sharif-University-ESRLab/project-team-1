from django.apps import AppConfig
import os
from threading import Thread
from time import sleep

SENSING_INTERVAL = 1


class InoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.inout'

    def ready(self):
        # This condition has to be checked so the function script won't run twice,
        # According to this: https://stackoverflow.com/questions/28489863/why-is-run-called-twice-in-the-django-dev-server/28504072#28504072
        if os.environ.get('RUN_MAIN') != 'true':
            t = Thread(target=handle_sensors, args=(None,), daemon=True)
            t.start()
            print('### Sensor handler thread started')


def handle_sensors(args):
    while True:
        sleep(SENSING_INTERVAL)
        print('.')
        handle_gps()
        handle_camera()
        handle_buzzer()


def handle_gps():
    # todo
    # get current location
    # calc speed according to previous locations
    pass


def handle_camera():
    # todo
    # get current picture
    # do image processing
    # save the sign (if there is one) somewhere
    pass


def handle_buzzer():
    # todo
    # get current speed
    # sound the buzzer if speed is inappropriate
    pass
