# based on https://gist.github.com/Palakis/2b7a0e872c66d209050f6e01b60f1c94
import obspython as S

mediaSource = None  # Null pointer
outputIndex = 63  # Last index


def play_sound():
    mediaSource = S.obs_source_create_private(
        "ffmpeg_source", "Global Media Source", None
    )
    s = S.obs_data_create()
    S.obs_data_set_string(s, "local_file", script_path() + "alert.mp3")
    S.obs_source_update(mediaSource, s)
    S.obs_source_set_monitoring_type(
        mediaSource, S.OBS_MONITORING_TYPE_MONITOR_AND_OUTPUT
    )
    S.obs_data_release(s)

    S.obs_set_output_source(outputIndex, mediaSource)
    return mediaSource


def obs_play_sound_release_source():
    r = play_sound()
    S.obs_source_release(r)


def on_event(event):
    if event == S.OBS_FRONTEND_EVENT_SCENE_CHANGED:
        obs_play_sound_release_source()


def script_load(settings):
    S.obs_frontend_add_event_callback(on_event)


def script_unload():
    S.obs_set_output_source(outputIndex, None)
