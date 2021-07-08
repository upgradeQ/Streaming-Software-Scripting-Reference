import obspython as S
from itertools import cycle

datacycle = cycle([1, 2, 3, 4, 5])
HOTKEY_ID = S.OBS_INVALID_HOTKEY_ID


class Example:
    def __init__(self, source_name=None):
        self.source_name = source_name

    def update_text(self):
        source = S.obs_get_source_by_name(self.source_name)
        if source is not None:
            data = str(next(datacycle))
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, "text", data)
            S.obs_source_update(source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(source)


eg = Example()  # class created ,obs part starts


def script_description():
    return "Hotkey example"


def script_save(settings):
    global HOTKEY_ID
    hotkey_save_array_htk = S.obs_hotkey_save(HOTKEY_ID)
    S.obs_data_set_array(settings, "htk_hotkey", hotkey_save_array_htk)
    S.obs_data_array_release(hotkey_save_array_htk)


def script_load(settings):
    global HOTKEY_ID

    def callback(pressed):
        if pressed:
            return eg.update_text()

    HOTKEY_ID = S.obs_hotkey_register_frontend("htk_id", "Example hotkey", callback)
    hotkey_save_array_htk = S.obs_data_get_array(settings, "htk_hotkey")
    S.obs_hotkey_load(HOTKEY_ID, hotkey_save_array_htk)
    S.obs_data_array_release(hotkey_save_array_htk)


def script_update(settings):
    eg.source_name = S.obs_data_get_string(settings, "source")


def script_properties():  # ui
    props = S.obs_properties_create()
    p = S.obs_properties_add_list(
        props,
        "source",
        "Text Source",
        S.OBS_COMBO_TYPE_EDITABLE,
        S.OBS_COMBO_FORMAT_STRING,
    )
    sources = S.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = S.obs_source_get_unversioned_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = S.obs_source_get_name(source)
                S.obs_property_list_add_string(p, name, name)

        S.source_list_release(sources)
    return props
