import obspython as S


class Example:
    def __init__(self):
        pos = S.vec2()
        self.location = pos

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

    def move_text_source(self):
        current_scene = S.obs_frontend_get_current_scene()
        source = S.obs_get_source_by_name("test_py")
        scene = S.obs_scene_from_source(current_scene)
        scene_item = S.obs_scene_find_source(scene, "test_py")
        if scene_item:
            dx, dy = 10, 10
            print("old values", self.location.x)
            S.obs_sceneitem_get_pos(
                scene_item, self.location
            )  # update to last position if its changed from OBS
            self.location.x += dx
            self.location.y += dy
            print("new values", self.location.x)
            S.obs_sceneitem_set_pos(scene_item, self.location)

        S.obs_scene_release(scene)
        S.obs_source_release(source)


eg = Example()  # class created ,obs part starts


def add_pressed(props, prop):
    eg.crete_text_source()


def move_pressed(props, prop):
    eg.move_text_source()


def script_description():
    return "add text source to current scene"


def script_properties():  # ui
    props = S.obs_properties_create()
    S.obs_properties_add_button(props, "button", "Add text source", add_pressed)
    S.obs_properties_add_button(
        props, "button2", "Move source +10 pixels", move_pressed
    )
    return props
