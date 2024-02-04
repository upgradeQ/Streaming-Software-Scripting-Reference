import obspython as S
from types import SimpleNamespace as G

_G = G()
_G._my_key = ""


def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_text(props, "key", "Stream Key", S.OBS_TEXT_DEFAULT)
    S.obs_properties_add_button(props, "button", "Update", callback)
    return props


def script_update(settings):
    _G._my_key = S.obs_data_get_string(settings, "key")


def callback(props, prop):
    service = S.obs_frontend_get_streaming_service()
    settings = S.obs_service_get_settings(service)
    S.obs_data_set_string(settings, "key", _G._my_key)

    S.obs_data_release(settings)
    return True
