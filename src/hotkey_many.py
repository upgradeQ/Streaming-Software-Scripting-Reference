import obspython as S


class Hotkey:
    def __init__(self, callback, obs_settings, _id):
        self.obs_data = obs_settings
        self.hotkey_id = S.OBS_INVALID_HOTKEY_ID
        self.hotkey_saved_key = None
        self.callback = callback
        self._id = _id

        self.load_hotkey()
        self.register_hotkey()
        self.save_hotkey()

    def register_hotkey(self):
        description = "Htk " + str(self._id)
        self.hotkey_id = S.obs_hotkey_register_frontend(
            "htk_id" + str(self._id), description, self.callback
        )
        S.obs_hotkey_load(self.hotkey_id, self.hotkey_saved_key)

    def load_hotkey(self):
        self.hotkey_saved_key = S.obs_data_get_array(
            self.obs_data, "htk_id" + str(self._id)
        )
        S.obs_data_array_release(self.hotkey_saved_key)

    def save_hotkey(self):
        self.hotkey_saved_key = S.obs_hotkey_save(self.hotkey_id)
        S.obs_data_set_array(
            self.obs_data, "htk_id" + str(self._id), self.hotkey_saved_key
        )
        S.obs_data_array_release(self.hotkey_saved_key)


class Keyboard:
    def __init__(self):
        self.hotkeys_map = {}
        self.hotkeys_obj = []
        self.inspect_self()

    def desc(description):
        def actual_decorator(func):
            func.desc = description
            return func

        return actual_decorator

    def do_load(self, settings):
        for h_id, cb in self.hotkeys_map.items():
            self.hotkeys_obj.append(Hotkey(cb, settings, h_id))

    def do_save(self, settings):
        for i in self.hotkeys_obj:
            if i is not None:
                i.save_hotkey()

    def inspect_self(self):
        for attr, value in vars(self.__class__).items():
            if callable(value) and hasattr(value, "desc"):
                self.hotkeys_map[value.desc] = value

    @desc("dh1test")
    def cb1(pressed):
        if pressed:
            print("cb1" + e1.txt)
        else:
            print("???")

    @desc("dh2test")
    def cb2(pressed):
        if pressed:
            print("cb2" + e2.txt)

    @desc("dh3test")
    def cb3(pressed):
        if not pressed:
            print("cb3" + e1.txt)

    @desc("dh4test")
    def cb4(pressed):
        if pressed:
            print("cb4" + e2.txt)


kbd = Keyboard()


class e:
    txt = "default txt"


e1 = e()
e2 = e()


def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_text(props, "_text1", "_text1:", S.OBS_TEXT_DEFAULT)
    S.obs_properties_add_text(props, "_text2", "_text2:", S.OBS_TEXT_DEFAULT)
    return props


def script_update(settings):
    _text1 = S.obs_data_get_string(settings, "_text1")
    _text2 = S.obs_data_get_string(settings, "_text2")
    e1.txt = _text1
    e2.txt = _text2


def script_load(settings):
    kbd.do_load(settings)


def script_save(settings):
    # it will crash! If you delete script then add it and bind the same hotkeys
    kbd.do_save(settings)
