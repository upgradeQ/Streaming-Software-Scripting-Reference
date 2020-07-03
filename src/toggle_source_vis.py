import obspython as obs


class Example:
    def __init__(self, source_name=None):
        self.source_name = source_name

    def toggle(self):
        current_scene = obs.obs_scene_from_source(obs.obs_frontend_get_current_scene())
        scene_item = obs.obs_scene_find_source(current_scene, self.source_name)
        boolean = not obs.obs_sceneitem_visible(scene_item)
        obs.obs_sceneitem_set_visible(scene_item, boolean)
        obs.obs_scene_release(current_scene)


eg = Example()  # class created ,obs part starts


def toggle_pressed(props, prop):
    eg.toggle()


def script_update(settings):
    eg.source_name = obs.obs_data_get_string(settings, "source")


def script_properties():  # ui
    props = obs.obs_properties_create()
    p = obs.obs_properties_add_list(
        props,
        "source",
        "Text Source",
        obs.OBS_COMBO_TYPE_EDITABLE,
        obs.OBS_COMBO_FORMAT_STRING,
    )
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            name = obs.obs_source_get_name(source)
            obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)
    obs.obs_properties_add_button(props, "button", "Toggle", toggle_pressed)
    return props
