import obspython as obs
from contextlib import contextmanager


@contextmanager
def p_data_ar(data_type, field):
    settings = obs.obs_get_private_data()
    get = getattr(obs, f"obs_data_get_{data_type}")
    try:
        yield get(settings, field)
    finally:
        obs.obs_data_release(settings)


def print_private_data():
    with p_data_ar("string", "__private__") as value:
        print(value)


obs.timer_add(print_private_data, 1000)
