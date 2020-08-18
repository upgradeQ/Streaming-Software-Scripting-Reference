import obspython as obs
import debugpy


class Hotkey:
    def __init__(self, callback, obs_settings, _id):
        self.obs_data = obs_settings
        self.hotkey_id = obs.OBS_INVALID_HOTKEY_ID
        self.hotkey_saved_key = None
        self.callback = callback
        self._id = _id

        self.load_hotkey()
        self.register_hotkey()
        self.save_hotkey()

    def register_hotkey(self):
        description = "Htk " + str(self._id)
        self.hotkey_id = obs.obs_hotkey_register_frontend(
            "htk_id" + str(self._id), description, self.callback
        )
        obs.obs_hotkey_load(self.hotkey_id, self.hotkey_saved_key)

    def load_hotkey(self):
        self.hotkey_saved_key = obs.obs_data_get_array(
            self.obs_data, "htk_id" + str(self._id)
        )
        obs.obs_data_array_release(self.hotkey_saved_key)

    def save_hotkey(self):
        self.hotkey_saved_key = obs.obs_hotkey_save(self.hotkey_id)
        obs.obs_data_set_array(
            self.obs_data, "htk_id" + str(self._id), self.hotkey_saved_key
        )
        obs.obs_data_array_release(self.hotkey_saved_key)


class h:
    htk_copy = None  # this attribute will hold instance of Hotkey


def cb1(pressed):
    debugpy.breakpoint()
    if pressed:
        print("callback1: " + e1.txt)


class e:
    txt = "default txt"


e1 = e()
h1 = h()


def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "_text1", "_text1:", obs.OBS_TEXT_DEFAULT)
    return props


def script_update(settings):
    _text1 = obs.obs_data_get_string(settings, "_text1")
    e1.txt = _text1


def script_load(settings):
    h1.htk_copy = Hotkey(cb1, settings, "h1_id")


def script_save(settings):
    h1.htk_copy.save_hotkey()
