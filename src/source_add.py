import obspython as obs


class Example:
    def crete_text_source(self):
        current_scene = obs.obs_frontend_get_current_scene()
        scene = obs.obs_scene_from_source(current_scene)
        settings = obs.obs_data_create()

        obs.obs_data_set_string(
            settings, "text", "The quick brown fox jumps over the lazy dog"
        )
        source = obs.obs_source_create_private("text_gdiplus", "test_py", settings)
        obs.obs_scene_add(scene, source)

        obs.obs_scene_release(scene)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)


eg = Example()  # class created ,obs part starts


def add_pressed(props, prop):
    eg.crete_text_source()


def script_description():
    return "add text source to current scene"


def script_properties():  # ui
    props = obs.obs_properties_create()
    obs.obs_properties_add_button(props, "button", "Add text source", add_pressed)
    return props
