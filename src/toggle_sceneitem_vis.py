import obspython as S


class Example:
    def __init__(self, source_name=None):
        self.source_name = source_name

    def toggle(self):
        current_scene = S.obs_scene_from_source(S.obs_frontend_get_current_scene())
        scene_item = S.obs_scene_find_source(current_scene, self.source_name)
        boolean = not S.obs_sceneitem_visible(scene_item)
        S.obs_sceneitem_set_visible(scene_item, boolean)
        S.obs_scene_release(current_scene)


eg = Example()  # class created ,obs part starts


def toggle_pressed(props, prop):
    eg.toggle()


def script_update(settings):
    eg.source_name = S.obs_data_get_string(settings, "source")


def script_properties():  # ui
    props = S.obs_properties_create()
    p = S.obs_properties_add_list(
        props,
        "source",
        "Text Source",
        S.OBS_COMBO_TYPE_EDITABLE,
        S.OBS_COMBO_FORMAT_STRING,
    )
    sources = S.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = S.obs_source_get_unversioned_id(source)
            name = S.obs_source_get_name(source)
            S.obs_property_list_add_string(p, name, name)

        S.source_list_release(sources)
    S.obs_properties_add_button(props, "button", "Toggle", toggle_pressed)
    return props
