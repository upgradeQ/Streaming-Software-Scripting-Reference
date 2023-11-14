from types import SimpleNamespace as _G
from ctypes import *
from ctypes.util import find_library
import obspython as S

G, ffi = _G(), _G()
ffi.obsffi = CDLL(find_library("obs"))  # ? PyDLL
G.lock = False
G.start_delay = 2
G.duration = 0
G.noise = 999
G.tick = 1000
G.tick_mili = G.tick * 0.001
G.interval_sec = 1.05
G.tick_acc = 0

G.render_texture = S.gs_texrender_create(S.GS_RGBA, S.GS_ZS_NONE)
G.rgba_4b = 4  # bytes
G.source_name = "big123"
G.surface = None


def wrap(funcname, restype, argtypes=None, use_lib=None):
    """Simplify wrapping ctypes functions"""
    if use_lib is not None:
        func = getattr(use_lib, funcname)
    else:
        func = getattr(ffi.obsffi, funcname)
    func.restype = restype
    if argtypes is not None:
        func.argtypes = argtypes
    ffi.__dict__[funcname] = func


class TexRender(Structure):
    pass


class StageSurf(Structure):
    pass


wrap("gs_stage_texture", None, argtypes=[POINTER(StageSurf), POINTER(TexRender)])
wrap("gs_stagesurface_create", POINTER(StageSurf), argtypes=[c_uint, c_uint, c_int])
wrap(
    "gs_stagesurface_map",
    c_bool,
    argtypes=[POINTER(StageSurf), POINTER(POINTER(c_ubyte)), POINTER(c_uint)],
)
wrap("gs_stagesurface_destroy", None, argtypes=[POINTER(StageSurf)])
wrap("gs_stagesurface_unmap", None, argtypes=[POINTER(StageSurf)])


def output_to_stdout():
    S.obs_enter_graphics()
    source = S.obs_get_source_by_name(G.source_name)
    if source and S.gs_texrender_begin(G.render_texture, 1920, 1080):
        S.obs_source_video_render(source)
        S.gs_texrender_end(G.render_texture)
        if not G.surface:
            G.surface = ffi.gs_stagesurface_create(
                c_uint(1920), c_uint(1080), c_int(S.GS_RGBA)
            )
        tex = S.gs_texrender_get_texture(G.render_texture)
        tex = c_void_p(int(tex))
        tex = cast(tex, POINTER(TexRender))
        ffi.gs_stage_texture(G.surface, tex)
        data = POINTER(c_ubyte)()

        if ffi.gs_stagesurface_map(G.surface, byref(data), byref(c_uint(G.rgba_4b))):
            print(data[0:100])
            ffi.gs_stagesurface_unmap(G.surface)
        S.gs_texrender_reset(G.render_texture)
    S.obs_source_release(source)
    S.obs_leave_graphics()


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


def script_unload():
    "clean up"
    S.obs_enter_graphics()
    ffi.gs_stagesurface_destroy(G.surface)
    S.gs_texrender_destroy(G.render_texture)
    S.obs_leave_graphics()
