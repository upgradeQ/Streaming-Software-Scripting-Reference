import obspython as obs
from itertools import cycle

datacycle = cycle([1, 2, 3, 4, 5])
HOTKEY_ID = obs.OBS_INVALID_HOTKEY_ID


class Example:
    def __init__(self, source_name=None):
        self.source_name = source_name

    def update_text(self):
        source = obs.obs_get_source_by_name(self.source_name)
        if source is not None:
            data = str(next(datacycle))
            settings = obs.obs_data_create()
            obs.obs_data_set_string(settings, "text", data)
            obs.obs_source_update(source, settings)
            obs.obs_data_release(settings)
            obs.obs_source_release(source)


eg = Example()  # class created ,obs part starts


def script_description():
    return "Hotkey example"


def script_save(settings):
    global HOTKEY_ID
    hotkey_save_array_htk = obs.obs_hotkey_save(HOTKEY_ID)
    obs.obs_data_set_array(settings, "htk_hotkey", hotkey_save_array_htk)
    obs.obs_data_array_release(hotkey_save_array_htk)


def script_load(settings):
    global HOTKEY_ID
    def callback(pressed):
        if pressed:
            return eg.update_text()

    HOTKEY_ID = obs.obs_hotkey_register_frontend(
        "htk_id", "Example hotkey", callback
    )
    hotkey_save_array_htk = obs.obs_data_get_array(settings, "htk_hotkey")
    obs.obs_hotkey_load(HOTKEY_ID, hotkey_save_array_htk)
    obs.obs_data_array_release(hotkey_save_array_htk)


def script_update(settings):
    eg.source_name = obs.obs_data_get_string(settings, "source")


def script_properties():  # ui
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
    return props
