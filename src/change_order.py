import obspython as S
import random
from contextlib import contextmanager


@contextmanager
def scene_ar(scene):
    scene = S.obs_scene_from_source(scene)
    try:
        yield scene
    finally:
        S.obs_scene_release(scene)


@contextmanager
def scene_enum(items):
    items = S.obs_scene_enum_items(items)
    try:
        yield items
    finally:
        S.sceneitem_list_release(items)


def get_order(scene_items=None):
    order = list()
    for i, s in enumerate(scene_items):
        source = S.obs_sceneitem_get_source(s)
        name = S.obs_source_get_name(source)
        order.append({"index": i, "name": name, "scene_item": s})
    return order


def reorder():
    current_scene = S.obs_frontend_get_current_scene()
    with scene_ar(current_scene) as scene:
        with scene_enum(scene) as scene_items:
            order = get_order(scene_items)
            # change second index with pre last
            order[1]["index"], order[-2]["index"] = (
                order[-2]["index"],
                order[1]["index"],
            )
            for s in sorted(order, key=lambda i: i["index"]):
                S.obs_sceneitem_set_order_position(s["scene_item"], s["index"])


def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_button(
        props, "button", "CHANGE ORDER", lambda *props: reorder()
    )
    return props
