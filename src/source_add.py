import obspython as S


class Example:
    def crete_text_source(self):
        current_scene = S.obs_frontend_get_current_scene()
        scene = S.obs_scene_from_source(current_scene)
        settings = S.obs_data_create()

        S.obs_data_set_string(
            settings, "text", "The quick brown fox jumps over the lazy dog"
        )
        source = S.obs_source_create_private("text_gdiplus", "test_py", settings)
        S.obs_scene_add(scene, source)

        S.obs_scene_release(scene)
        S.obs_data_release(settings)
        S.obs_source_release(source)


eg = Example()  # class created ,obs part starts


def add_pressed(props, prop):
    eg.crete_text_source()


def script_description():
    return "add text source to current scene"


def script_properties():  # ui
    props = S.obs_properties_create()
    S.obs_properties_add_button(props, "button", "Add text source", add_pressed)
    return props
