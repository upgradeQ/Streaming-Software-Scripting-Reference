import obspython as S


def send_hotkey(obs_htk_id, key_modifiers=None):
    if key_modifiers:
        shift = key_modifiers.get("shift")
        control = key_modifiers.get("control")
        alt = key_modifiers.get("alt")
        command = key_modifiers.get("command")
    else:
        shift = control = alt = command = 0
    modifiers = 0

    if shift:
        modifiers |= S.INTERACT_SHIFT_KEY
    if control:
        modifiers |= S.INTERACT_CONTROL_KEY
    if alt:
        modifiers |= S.INTERACT_ALT_KEY
    if command:
        modifiers |= S.INTERACT_COMMAND_KEY

    combo = S.obs_key_combination()
    combo.modifiers = modifiers
    combo.key = S.obs_key_from_name(obs_htk_id)

    if not modifiers and (
        # S.OBS_KEY_NONE = 0 ?
        combo.key == 0
        or combo.key >= S.OBS_KEY_LAST_VALUE
    ):
        raise Exception("invalid key-modifier combination")

    S.obs_hotkey_inject_event(combo, False)
    S.obs_hotkey_inject_event(combo, True)
    S.obs_hotkey_inject_event(combo, False)


def press_1(*p):
    send_hotkey("OBS_KEY_1")


def press_shift_1(*p):
    send_hotkey("OBS_KEY_1", {"shift": True})


def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_button(props, "button1", "Press 1", press_1)
    S.obs_properties_add_button(props, "button2", "Press shift + 1", press_shift_1)
    return props
