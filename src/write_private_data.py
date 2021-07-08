import obspython as S
from contextlib import contextmanager
from random import randint


def send_to_private_data(data_type, field, result):
    settings = S.obs_data_create()
    set = getattr(obs, f"obs_data_set_{data_type}")
    set(settings, field, result)
    S.obs_apply_private_data(settings)
    S.obs_data_release(settings)


def write_private_data():
    result = "private value from " + str(__file__) + " " + str(randint(1, 10))
    send_to_private_data("string", "__private__", result)


S.timer_add(write_private_data, 1000)
