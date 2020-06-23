import obspython as obs


class Example:
    def crete_text_source(self):
        current_scene = obs.obs_frontend_get_current_scene()
        scene = obs.obs_scene_from_source(current_scene)
        settings = obs.obs_data_create()

        obs.obs_data_set_string(
            settings, "text", "The quick brown fox jumps over the lazy dog"
        )
        # doesnt work on private sources
        source = obs.obs_source_create("text_gdiplus", "1test_py", settings, None)
        obs.obs_scene_add(scene, source)

        obs.obs_scene_release(scene)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)

    def add_filter_to_source(self):
        source = obs.obs_get_source_by_name("1test_py")
        settings = obs.obs_data_create()

        obs.obs_data_set_int(settings, "opacity", 50)
        source_color = obs.obs_source_create_private(
            "color_filter", "opacity to 50", settings
        )
        obs.obs_source_filter_add(source, source_color)

        obs.obs_source_release(source)
        obs.obs_data_release(settings)
        obs.obs_source_release(source_color)


eg = Example()  # class created ,obs part starts


def add_pressed(props, prop):
    eg.add_filter_to_source()


def txt_pressed(props, prop):
    eg.crete_text_source()


def script_description():
    return "click add text source to current scene, then add color correction "


def script_properties():  # ui
    props = obs.obs_properties_create()
    obs.obs_properties_add_button(props, "button1", "Add color source", add_pressed)
    obs.obs_properties_add_button(props, "button", "Add text source", txt_pressed)
    return props
