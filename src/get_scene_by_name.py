import obspython as obs


class Example:
    def __init__(self, scene_name=None):
        self.scene_name = scene_name

    def set_current_scene(self):
        scenes = obs.obs_frontend_get_scenes()
        for scene in scenes:
            name = obs.obs_source_get_name(scene)
            if name == self.scene_name:
                obs.obs_frontend_set_current_scene(scene)
        obs.source_list_release(scenes)


eg = Example()  # class created ,obs part starts


def set_pressed(props, prop):
    eg.set_current_scene()


def script_update(settings):
    eg.scene_name = obs.obs_data_get_string(settings, "scene")


def script_properties():  # ui
    props = obs.obs_properties_create()
    p = obs.obs_properties_add_list(
        props,
        "scene",
        "Scene",
        obs.OBS_COMBO_TYPE_EDITABLE,
        obs.OBS_COMBO_FORMAT_STRING,
    )

    scenes = obs.obs_frontend_get_scenes()
    for scene in scenes:
        name = obs.obs_source_get_name(scene)
        obs.obs_property_list_add_string(p, name, name)
    obs.source_list_release(scenes)

    obs.obs_properties_add_button(props, "button", "Set current scene", set_pressed)
    return props
