import obspython as obs


def remove_duplicate(k, v):
    k = str(k)
    v = str(v)
    if k in v:
        return "    "
    else:
        return v


def refresh_pressed(props, prop):
    print("refresh pressed")
    data = vars(obs)
    data = {k: remove_duplicate(k, v) for k, v in data.items()}
    nice_data = str()
    for k, v in data.items():
        nice_data += (
            f"- [`{k}`](https://github.com/obsproject/obs-studio/search?q={k}) \n"
        )
    with open(script_path() + "export.md", "w") as f:
        f.write(nice_data)


def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
    return props
