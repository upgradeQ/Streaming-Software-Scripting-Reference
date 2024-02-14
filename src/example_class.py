import obspython as S
from itertools import cycle

datacycle = cycle([1, 2, 3, 4, 5])

class Example:
    def __init__(self,source_name=None):
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


def refresh_pressed(props, prop):
    print("refresh pressed")
    eg.update_text()


def script_description():
    return "Using classes example"


def script_update(settings):
    eg.source_name = S.obs_data_get_string(settings, "source")
    S.timer_remove(eg.update_text)
    if eg.source_name != "":
        S.timer_add(eg.update_text, 1 * 1000)


def script_properties(): # ui 
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
    S.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
    return props
