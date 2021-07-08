import obspython as S
from pathlib import Path


class Data:
    _text_ = None
    _int_ = None
    _settings_ = None


def save(prop, props):
    if not Data._settings_:
        return
    p = Path(__file__).absolute()  # current script path
    file = p.parent / "saved_settings.json"
    try:
        content = S.obs_data_get_json(Data._settings_)
        with open(file, "w") as f:
            f.write(content)
    except Exception as e:
        print(e, "cannot write to file")


def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_text(props, "_text", "text", S.OBS_TEXT_DEFAULT)
    S.obs_properties_add_int(props, "_int", "int", 1, 100, 1)

    S.obs_properties_add_button(props, "save", "Save", save)
    return props


def script_update(settings):
    Data._text_ = S.obs_data_get_string(settings, "_text")
    Data._int_ = S.obs_data_get_int(settings, "_int")
    Data._settings_ = settings
