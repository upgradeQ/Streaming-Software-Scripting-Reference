import obspython as obs


def connect_cur_scene():
    source = obs.obs_frontend_get_current_scene()
    sh = obs.obs_source_get_signal_handler(source)
    obs.signal_handler_connect(sh, "item_add", callback)
    obs.obs_source_release(source)


def callback(calldata):
    scene_item = obs.calldata_sceneitem(calldata, "item")
    # scene = obs.calldata_source(cd,"scene") # bad utf symbols
    scene = obs.obs_sceneitem_get_scene(scene_item)
    name = obs.obs_source_get_name
    source = obs.obs_sceneitem_get_source
    scene_source = obs.obs_scene_get_source
    scene_name = name(scene_source(scene))
    scene_item_name = name(source(scene_item))
    print(f"item {scene_item_name} has been added to scene {scene_name}")


def on_load(event):
    if event == obs.OBS_FRONTEND_EVENT_FINISHED_LOADING:
        connect_cur_scene()


def script_load(settings):
    obs.obs_frontend_add_event_callback(on_load)
