import obspython as obs
from itertools import count

counter = count()


def refresh_pressed(props, prop):
    print("refresh pressed")


def callback(props, prop, *args, **kwargs):  # pass settings implicitly
    p = obs.obs_properties_get(props, "button")
    n = next(counter)
    obs.obs_property_set_description(p, f"refresh pressed {n} times")
    return True


def script_description():
    return "Modify property "


def script_properties():
    props = obs.obs_properties_create()
    b = obs.obs_properties_add_button(
        props, "button", "refresh pressed 0 times", refresh_pressed
    )
    obs.obs_property_set_modified_callback(b, callback)
    return props
