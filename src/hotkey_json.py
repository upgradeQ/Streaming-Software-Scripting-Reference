import obspython as S

ID = "htk_id"
JSON_DATA = '{"%s":[{"key":"OBS_KEY_1"}]}' % ID


def on_obs_key_1(pressed):
    if pressed:
        raise Exception("hotkey 1 pressed")


def script_load(settings):
    s = S.obs_data_create_from_json(JSON_DATA)

    a = S.obs_data_get_array(s, ID)
    h = S.obs_hotkey_register_frontend(ID, ID, on_obs_key_1)
    S.obs_hotkey_load(h, a)

    S.obs_data_array_release(a)
    S.obs_data_release(s)
