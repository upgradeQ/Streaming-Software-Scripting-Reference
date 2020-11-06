import obspython as obs
from contextlib import contextmanager
from random import randint

# auto release context managers
@contextmanager
def source_ar(source_name):
    source = obs.obs_get_source_by_name(source_name)
    try:
        yield source
    finally:
        obs.obs_source_release(source)


@contextmanager
def source_create_ar(id, source_name, settings):
    try:
        _source = obs.obs_source_create(id, source_name, settings, None)
        yield _source
    finally:
        obs.obs_source_release(_source)


@contextmanager
def scene_create_ar(name):
    try:
        _scene = obs.obs_scene_create(name)
        yield _scene
    finally:
        obs.obs_scene_release(_scene)


@contextmanager
def data_ar(source_settings=None):
    if not source_settings:
        settings = obs.obs_data_create()
    if source_settings:
        settings = obs.obs_source_get_settings(source_settings)
    try:
        yield settings
    finally:
        obs.obs_data_release(settings)


@contextmanager
def scene_from_source_ar(source):
    source = obs.obs_scene_from_source(source)
    try:
        yield source
    finally:
        obs.obs_scene_release(source)


def add_random_text_source(scene):
    r = " random text # " + str(randint(0, 10))
    with data_ar() as settings:
        obs.obs_data_set_string(settings, "text", f"random text value {r}")
        with source_create_ar("text_ft2_source", f"random text{r}", settings) as source:
            pos = obs.vec2()
            pos.x = randint(0, 1920)
            pos.y = randint(0, 1080)
            scene_item = obs.obs_scene_add(scene, source)
            obs.obs_sceneitem_set_pos(scene_item, pos)


def add_scene_with_sources():
    current_scene_source = obs.obs_frontend_get_current_scene()
    with scene_from_source_ar(current_scene_source) as scene_source:
        with scene_create_ar("_nested_scene") as _scene:
            py_scene_source = obs.obs_scene_get_source(_scene)

            with scene_from_source_ar(py_scene_source) as scene:
                add_random_text_source(scene)
                add_random_text_source(scene)
                add_random_text_source(scene)

            # add created scene to current scene ( nested scene)
            _scene_source = obs.obs_scene_get_source(scene)
            obs.obs_scene_add(scene_source, _scene_source)


def callback(*p):
    add_scene_with_sources()


def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_button(props, "button1", "add to current scene", callback)
    return props
