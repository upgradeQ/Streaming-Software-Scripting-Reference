import obspython as S
from contextlib import contextmanager

G = lambda: ...


@contextmanager
def source_auto_release(source_name):
    source = S.obs_get_source_by_name(source_name)
    try:
        yield source
    finally:
        S.obs_source_release(source)


def send_json_event(*p):
    with source_auto_release(G.source_name) as source:
        print("begin test event")
        cd = S.calldata_create()
        ph = S.obs_source_get_proc_handler(source)
        S.calldata_set_string(cd, "eventName", "my-test-event")
        S.calldata_set_string(cd, "jsonString", '{"key123": "\\nvalue123"}')
        S.proc_handler_call(ph, "javascript_event", cd)
        S.calldata_destroy(cd)
        print("end test event")


def script_update(settings):
    G.source_name = S.obs_data_get_string(settings, "source")


def script_properties():  # ui
    props = S.obs_properties_create()
    p = S.obs_properties_add_list(
        props,
        "source",
        "Browser source",
        S.OBS_COMBO_TYPE_EDITABLE,
        S.OBS_COMBO_FORMAT_STRING,
    )
    S.obs_properties_add_button(props, "button1", "Send JSON", send_json_event)
    sources = S.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = S.obs_source_get_unversioned_id(source)
            if source_id == "browser_source":
                name = S.obs_source_get_name(source)
                S.obs_property_list_add_string(p, name, name)

        S.source_list_release(sources)
    return props
