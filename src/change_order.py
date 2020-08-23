import obspython as obs
import random
from contextlib import contextmanager


@contextmanager
def scene_ar(scene):
    scene = obs.obs_scene_from_source(scene)
    try:
        yield scene
    finally:
        obs.obs_scene_release(scene)


@contextmanager
def scene_enum(items):
    items = obs.obs_scene_enum_items(items)
    try:
        yield items
    finally:
        obs.sceneitem_list_release(items)


def get_order(scene_items=None):
    order = list()
    for i, s in enumerate(scene_items):
        source = obs.obs_sceneitem_get_source(s)
        name = obs.obs_source_get_name(source)
        order.append({"index": i, "name": name, "scene_item": s})
    return order


def reorder():
    current_scene = obs.obs_frontend_get_current_scene()
    with scene_ar(current_scene) as scene:
        with scene_enum(scene) as scene_items:
            order = get_order(scene_items)
            # change second index with pre last
            order[1]["index"], order[-2]["index"] = (
                order[-2]["index"],
                order[1]["index"],
            )
            for s in sorted(order, key=lambda i: i["index"]):
                obs.obs_sceneitem_set_order_position(s["scene_item"], s["index"])


def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_button(
        props, "button", "CHANGE ORDER", lambda *props: reorder()
    )
    return props
