import obspython as S


class Example:
    def __init__(self, scene_name=None):
        self.scene_name = scene_name

    def set_current_scene(self):
        scenes = S.obs_frontend_get_scenes()
        for scene in scenes:
            name = S.obs_source_get_name(scene)
            if name == self.scene_name:
                S.obs_frontend_set_current_scene(scene)
        S.source_list_release(scenes)


eg = Example()  # class created ,obs part starts


def set_pressed(props, prop):
    eg.set_current_scene()


def script_update(settings):
    eg.scene_name = S.obs_data_get_string(settings, "scene")


def script_properties():  # ui
    props = S.obs_properties_create()
    p = S.obs_properties_add_list(
        props,
        "scene",
        "Scene",
        S.OBS_COMBO_TYPE_EDITABLE,
        S.OBS_COMBO_FORMAT_STRING,
    )

    scenes = S.obs_frontend_get_scenes()
    for scene in scenes:
        name = S.obs_source_get_name(scene)
        S.obs_property_list_add_string(p, name, name)
    S.source_list_release(scenes)

    S.obs_properties_add_button(props, "button", "Set current scene", set_pressed)
    return props
