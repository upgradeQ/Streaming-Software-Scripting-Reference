import obspython as obs


def on_event(event):
    if event == obs.OBS_FRONTEND_EVENT_SCENE_CHANGED:
        raise Exception("Triggered when the current scene has changed.")


def script_load(settings):
    obs.obs_frontend_add_event_callback(on_event)


def script_description():
    "Triggered when the current scene has changed."
