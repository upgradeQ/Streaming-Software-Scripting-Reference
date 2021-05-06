import obspython as obs
from contextlib import contextmanager

G = lambda: ...


@contextmanager
def source_auto_release(source_name):
    source = obs.obs_get_source_by_name(source_name)
    try:
        yield source
    finally:
        obs.obs_source_release(source)


def get_modifiers(key_modifiers):
    if key_modifiers:
        shift = key_modifiers.get("shift")
        control = key_modifiers.get("control")
        alt = key_modifiers.get("alt")
        command = key_modifiers.get("command")
    else:
        shift = control = alt = command = 0
    modifiers = 0

    if shift:
        modifiers |= obs.INTERACT_SHIFT_KEY
    if control:
        modifiers |= obs.INTERACT_CONTROL_KEY
    if alt:
        modifiers |= obs.INTERACT_ALT_KEY
    if command:
        modifiers |= obs.INTERACT_COMMAND_KEY
    return modifiers


def send_hotkey_to_browser(source, obs_htk_id, key_modifiers=None, key_up=False):

    key = obs.obs_key_from_name(obs_htk_id)
    vk = obs.obs_key_to_virtual_key(key)
    event = obs.obs_key_event()
    event.native_vkey = vk
    event.modifiers = get_modifiers(key_modifiers)
    event.native_modifiers = event.modifiers  # https://doc.qt.io/qt-5/qkeyevent.html
    event.native_scancode = vk
    event.text = ""
    obs.obs_source_send_key_click(source, event, key_up)


def press_tab(*p):
    with source_auto_release(G.source_name) as source:
        send_hotkey_to_browser(source, "OBS_KEY_TAB")
        send_hotkey_to_browser(source, "OBS_KEY_TAB", key_up=True)


def press_shift_tab(*p):
    with source_auto_release(G.source_name) as source:
        send_hotkey_to_browser(source, "OBS_KEY_TAB", {"shift": True})
        send_hotkey_to_browser(source, "OBS_KEY_TAB", {"shift": True}, key_up=True)


def send_mouse_click_to_browser(
    source,
    x=0,
    y=0,
    button_type=obs.MOUSE_LEFT,
    mouse_up=False,
    click_count=1,
    key_modifiers=None,
):
    event = obs.obs_mouse_event()
    event.modifiers = get_modifiers(key_modifiers)
    event.x = x
    event.y = y
    obs.obs_source_send_mouse_click(source, event, button_type, mouse_up, click_count)


def send_mouse_move_to_browser(
    source,
    x=0,
    y=0,
    key_modifiers=None,
):
    event = obs.obs_mouse_event()
    event.modifiers = get_modifiers(key_modifiers)
    event.x = x
    event.y = y
    obs.obs_source_send_mouse_move(source, event, False)  # do not leave


def move_mouse0(*p):
    with source_auto_release(G.source_name) as source:
        send_mouse_move_to_browser(source, 0, 0)


def move_mouse1(*p):
    with source_auto_release(G.source_name) as source:
        send_mouse_move_to_browser(source, 100, 200)


def click_at(*p):
    with source_auto_release(G.source_name) as source:
        send_mouse_click_to_browser(source, 100, 200)
        send_mouse_click_to_browser(source, 100, 200, mouse_up=True, click_count=2)


def script_update(settings):
    G.source_name = obs.obs_data_get_string(settings, "source")


def script_properties():  # ui
    props = obs.obs_properties_create()
    p = obs.obs_properties_add_list(
        props,
        "source",
        "Browser source",
        obs.OBS_COMBO_TYPE_EDITABLE,
        obs.OBS_COMBO_FORMAT_STRING,
    )
    obs.obs_properties_add_button(props, "button1", "Press tab", press_tab)
    obs.obs_properties_add_button(props, "button2", "Press shift+tab", press_shift_tab)
    obs.obs_properties_add_button(props, "button3", "Send LMB at [100,200]", click_at)
    obs.obs_properties_add_button(props, "button4", "Move to 0,0 ", move_mouse0)
    obs.obs_properties_add_button(props, "button5", "Move to 100,200 ", move_mouse1)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id == "browser_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)
    return props
