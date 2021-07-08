from types import SimpleNamespace as _G
from ctypes import *
from ctypes.util import find_library
import obspython as S

G = _G()
G.obsffi = CDLL(find_library("obs"))
G.obsffi_front = CDLL(find_library("obs-frontend-api"))


def wrap(funcname, restype, argtypes=None, use_lib=None):
    """Simplify wrapping ctypes functions"""
    if use_lib is not None:
        func = getattr(use_lib, funcname)
    else:
        func = getattr(G.obsffi, funcname)
    func.restype = restype
    if argtypes is not None:
        func.argtypes = argtypes
    G.__dict__[funcname] = func


class Config(Structure):
    pass


wrap("obs_frontend_get_profile_config", POINTER(Config), use_lib=G.obsffi_front)
# const char *config_get_string(config_t *config, const char *section,
#                  const char *name)
wrap("config_get_string", c_char_p, argtypes=[POINTER(Config), c_char_p, c_char_p])
wrap("config_num_sections", c_size_t, argtypes=[POINTER(Config)])
wrap("config_get_section", c_char_p, argtypes=[POINTER(Config), c_size_t])


def output_to_stdout():
    cfg = G.obs_frontend_get_profile_config()
    e = lambda x: x.encode("utf-8")
    s = G.config_get_string(cfg, e("SimpleOutput"), e("FilePath"))
    l = G.config_num_sections(cfg)
    for i in range(l):
        tag = G.config_get_section(cfg, c_size_t(i))
    print(s, l)


G.lock = False
G.start_delay = 2
G.duration = 0
G.noise = 999
G.tick = 16
G.tick_mili = G.tick * 0.001
G.interval_sec = 1.05
G.tick_acc = 0
G.callback = output_to_stdout


def event_loop():
    """wait n seconds, then execute callback within certain interval"""
    if G.duration > G.start_delay:
        G.tick_acc += G.tick_mili
        if G.tick_acc > G.interval_sec:
            G.callback()
            G.tick_acc = 0
            return
    else:
        G.duration += G.tick_mili


S.timer_add(event_loop, G.tick)
