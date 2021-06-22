import obspython as S  # studio
from types import SimpleNamespace
from ctypes import *
from ctypes.util import find_library

obsffi = CDLL(find_library("obs"))
G = SimpleNamespace()


def wrap(funcname, restype, argtypes):
    """Simplify wrapping ctypes functions in obsffi"""
    func = getattr(obsffi, funcname)
    func.restype = restype
    func.argtypes = argtypes
    globals()["g_" + funcname] = func


class Source(Structure):
    pass


class Volmeter(Structure):
    pass


volmeter_callback_t = CFUNCTYPE(
    None, c_void_p, POINTER(c_float), POINTER(c_float), POINTER(c_float)
)
wrap("obs_get_source_by_name", POINTER(Source), argtypes=[c_char_p])
wrap("obs_source_release", None, argtypes=[POINTER(Source)])
wrap("obs_volmeter_create", POINTER(Volmeter), argtypes=[c_int])
wrap("obs_volmeter_destroy", None, argtypes=[POINTER(Volmeter)])
wrap(
    "obs_volmeter_add_callback",
    None,
    argtypes=[POINTER(Volmeter), volmeter_callback_t, c_void_p],
)
wrap(
    "obs_volmeter_remove_callback",
    None,
    argtypes=[POINTER(Volmeter), volmeter_callback_t, c_void_p],
)
wrap(
    "obs_volmeter_attach_source",
    c_bool,
    argtypes=[POINTER(Volmeter), POINTER(Source)],
)


@volmeter_callback_t
def volmeter_callback(data, mag, peak, input):
    G.noise = float(peak[0])


def output_to_file(volume):
    with open("current_db_volume_of_source_status.txt", "w", encoding="utf-8") as f:
        f.write(str(volume))


OBS_FADER_LOG = 2
G.lock = False
G.start_delay = 3
G.duration = 0
G.noise = 999
G.tick = 16
G.tick_mili = G.tick * 0.001
G.interval_sec = 0.05
G.tick_acc = 0
G.source_name = "Media Source"
G.volmeter = "not yet initialized volmeter instance"
G.callback = output_to_file


def event_loop():
    """wait n seconds, then execute callback with db volume level within interval"""
    if G.duration > G.start_delay:
        if not G.lock:
            print("setting volmeter")
            source = g_obs_get_source_by_name(G.source_name.encode("utf-8"))
            G.volmeter = g_obs_volmeter_create(OBS_FADER_LOG)
            g_obs_volmeter_add_callback(G.volmeter, volmeter_callback, None)
            if g_obs_volmeter_attach_source(G.volmeter, source):
                g_obs_source_release(source)
                G.lock = True
                print("Attached to source")
                return
        G.tick_acc += G.tick_mili
        if G.tick_acc > G.interval_sec:
            G.callback(G.noise)
            G.tick_acc = 0
    else:
        G.duration += G.tick_mili


def script_unload():
    g_obs_volmeter_remove_callback(G.volmeter, volmeter_callback, None)
    g_obs_volmeter_destroy(G.volmeter)
    print("Removed volmeter & volmeter_callback")


S.timer_add(event_loop, G.tick)
