import obspython as obs
from contextlib import contextmanager
from itertools import cycle

datacycle = cycle([1, 2, 3, 4, 5])

class Example_leak:
    def __init__(self,source_name=None):
        self.source_name = source_name

    def update_text(self):
        source = obs.obs_get_source_by_name(self.source_name)
        if source is not None:
            data = str(next(datacycle))
            settings = obs.obs_data_create()
            obs.obs_data_set_string(settings, "text", data)
            obs.obs_source_update(source, settings)
            #16:36:24.325: Number of memory leaks: 1543
            #obs.obs_data_release(settings)
            #obs.obs_source_release(source)

@contextmanager
def source_auto_release(source_name):
    source = obs.obs_get_source_by_name(source_name)
    try:
        yield source 
    finally:
        obs.obs_source_release(source)

@contextmanager
def data_auto_release():
    settings = obs.obs_data_create()
    try:
        yield settings 
    finally:
        obs.obs_data_release(settings)

class Example_with:
    def __init__(self,source_name=None):
        self.source_name = source_name

    def update_text(self):
        with source_auto_release(self.source_name) as source:
            if source is not None:
                data = str(next(datacycle))
                with data_auto_release() as settings:
                    obs.obs_data_set_string(settings, "text", data)
                    obs.obs_source_update(source, settings)
        # 16:49:11.270: Number of memory leaks: 0

eg = Example_with()  # class created ,obs part starts


def refresh_pressed(props, prop):
    print("refresh pressed")
    eg.update_text()


def script_description():
    return "with statement example"


def script_update(settings):
    eg.source_name = obs.obs_data_get_string(settings, "source")
    obs.timer_remove(eg.update_text)
    if eg.source_name != "":
        obs.timer_add(eg.update_text, 1 * 10)


def script_properties(): # ui 
    props = obs.obs_properties_create()
    p = obs.obs_properties_add_list(
        props,
        "source",
        "Text Source",
        obs.OBS_COMBO_TYPE_EDITABLE,
        obs.OBS_COMBO_FORMAT_STRING,
    )
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)
    obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
    return props
