import obspython as S
from itertools import cycle


class Example:
    def __init__(self, source_name=None):
        self.source_name = source_name
        self.data = ""

    def update_text(self):
        source = S.obs_get_source_by_name(self.source_name)
        if source is not None:
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, "text", self.data)
            S.obs_source_update(source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(source)


eg = Example()  # class created ,obs part starts


def callback(props, prop, settings):
    _number = S.obs_data_get_int(settings, "_int")
    _text_value = S.obs_data_get_string(settings, "_text")
    text_property = S.obs_properties_get(props, "_text")
    if _number > 50:
        eg.data = _text_value + str(_number)
        S.obs_property_set_visible(text_property, True)
        return True
    else:
        eg.data = ""
        S.obs_property_set_visible(text_property, False)
        return True


def script_description():
    return "Modification property example"


def script_update(settings):
    eg.source_name = S.obs_data_get_string(settings, "source")
    S.timer_remove(eg.update_text)
    if eg.source_name != "":
        S.timer_add(eg.update_text, 1 * 1000)


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
    number = S.obs_properties_add_int(props, "_int", "Number", 1, 100, 1)
    text_value = S.obs_properties_add_text(
        props, "_text", "Additional input:", S.OBS_TEXT_DEFAULT
    )
    S.obs_property_set_visible(text_value, False)
    S.obs_property_set_modified_callback(number, callback)
    return props
