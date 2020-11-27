import obspython as obs
import threading
from time import sleep


def hook(obs_htk_id, htk_id, callback):
    json_data = '{"%s":[{"key":"%s"}]}' % (htk_id, obs_htk_id)
    s = obs.obs_data_create_from_json(json_data)

    a = obs.obs_data_get_array(s, htk_id)
    h = obs.obs_hotkey_register_frontend(htk_id, obs_htk_id, callback)
    obs.obs_hotkey_load(h, a)

    obs.obs_data_array_release(a)
    obs.obs_data_release(s)


data = lambda: ...
data.thread_paused = True
data.status = "empty"


def toggle_thread():
    data.thread_paused = not data.thread_paused


def callback(pressed):
    if pressed:
        toggle_thread()


def busy_thread():
    while True:
        if not data.thread_paused:
            sleep(0.3)
            data.status = "active"
            # print to stdoud crashes OBS on exit
        else:
            sleep(0.5)
            data.status = "inactive"


print('Press the "~" to toggle on/off')
hook("OBS_KEY_ASCIITILDE", "id_", callback)
obs.timer_add(lambda: print(data.status), 500)
t = threading.Thread(target=busy_thread)
t.start()
