import obspython as S


def connect_cur_scene():
    source = S.obs_frontend_get_current_scene()
    sh = S.obs_source_get_signal_handler(source)
    S.signal_handler_connect(sh, "item_add", callback)
    S.obs_source_release(source)


def callback(calldata):
    scene_item = S.calldata_sceneitem(calldata, "item")
    # scene = S.calldata_source(cd,"scene") # bad utf symbols
    scene = S.obs_sceneitem_get_scene(scene_item)
    name = S.obs_source_get_name
    source = S.obs_sceneitem_get_source
    scene_source = S.obs_scene_get_source
    scene_name = name(scene_source(scene))
    scene_item_name = name(source(scene_item))
    print(f"item {scene_item_name} has been added to scene {scene_name}")


def on_load(event):
    if event == S.OBS_FRONTEND_EVENT_FINISHED_LOADING:
        connect_cur_scene()


def script_load(settings):
    S.obs_frontend_add_event_callback(on_load)
