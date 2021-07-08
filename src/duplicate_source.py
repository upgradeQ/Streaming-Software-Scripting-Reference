import obspython as S

# See also https://github.com/upgradeQ/OBS-Studio-Python-Scripting-Cheatsheet-obspython-Examples-of-API/issues/3


class Example:
    source_name = None
    scene_name = None

    def dup(self):
        current_scene = S.obs_scene_from_source(S.obs_frontend_get_current_scene())
        scene_item = S.obs_scene_find_source(current_scene, self.source_name)
        info = S.obs_transform_info()
        crop = S.obs_sceneitem_crop()
        S.obs_sceneitem_get_info(scene_item, info)
        S.obs_sceneitem_get_crop(scene_item, crop)
        duplicate = S.obs_sceneitem_get_source(scene_item)
        duplicated = S.obs_source_duplicate(
            duplicate, "duplicate" + self.source_name, False
        )

        scenes = S.obs_frontend_get_scenes()
        for scene in scenes:
            name = S.obs_source_get_name(scene)
            if name == self.scene_name:
                scene = S.obs_scene_from_source(scene)
                scene_item2 = S.obs_scene_add(scene, duplicated)
                S.obs_sceneitem_set_info(scene_item2, info)
                S.obs_sceneitem_set_crop(scene_item2, crop)
                S.obs_scene_release(scene)

        S.obs_source_release(duplicated)
        S.source_list_release(scenes)
        S.obs_scene_release(current_scene)


eg = Example()  # class created ,obs part starts


def button_pressed(props, prop):
    eg.dup()


def script_update(settings):
    eg.source_name = S.obs_data_get_string(settings, "source")
    eg.scene_name = S.obs_data_get_string(settings, "scene")


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

    _p = S.obs_properties_add_list(
        props,
        "scene",
        "Scene",
        S.OBS_COMBO_TYPE_EDITABLE,
        S.OBS_COMBO_FORMAT_STRING,
    )

    scenes = S.obs_frontend_get_scenes()
    for scene in scenes:
        name = S.obs_source_get_name(scene)
        S.obs_property_list_add_string(_p, name, name)
    S.source_list_release(scenes)

    S.obs_properties_add_button(props, "button", "Duplicate", button_pressed)
    return props
