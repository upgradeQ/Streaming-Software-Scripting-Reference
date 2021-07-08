import obspython as S
from random import choices

FLAG = True
INTERVAL = 100


class Example:
    def __init__(self):
        self.lock = True

    def random_numbers(self):
        print(choices(range(1, 10), k=3))

    def ticker(self):
        """how fast update.One callback at time with lock"""
        if self.lock:
            self.random_numbers()
        if not self.lock:
            S.remove_current_callback()


eg = Example()  # class created ,obs part starts


def stop_pressed(props, prop):
    global FLAG
    FLAG = True
    eg.lock = False


def start_pressed(props, prop):
    global FLAG  # to keep only one timer callback
    if FLAG:
        S.timer_add(eg.ticker, INTERVAL)
    eg.lock = True
    FLAG = False


def script_properties():  # ui
    props = S.obs_properties_create()
    S.obs_properties_add_button(props, "button", "Stop", stop_pressed)
    S.obs_properties_add_button(props, "button2", "Start", start_pressed)
    return props
