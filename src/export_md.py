import obspython as S


def remove_duplicate(k, v):
    k = str(k)
    v = str(v)
    if k in v:
        return "    "
    else:
        return v


def button_pressed(props, prop):
    data = vars(S)
    data = {k: remove_duplicate(k, v) for k, v in data.items()}
    nice_data = str()
    nice_data += f"OBS Studio version {S.obs_get_version_string()} \n"
    nice_data += "| name | source code | latest docs | scripting | \n"
    nice_data += "| ---: | :---: | :---: | :---: |\n"
    for k, v in sorted(data.items(), key=lambda i: i[0]):
        gs = bool(k.lower().startswith("gs"))
        underscore = bool(k.startswith("_"))
        quat = bool(k.lower().startswith("quat"))
        matrix = bool(k.lower().startswith("matrix"))
        vec = bool(k.lower().startswith("vec"))

        # skip draw
        if any([gs, underscore, quat, matrix, vec]):
            continue

        source_code = (
            f"[`source_code`](https://github.com/obsproject/obs-studio/search?q={k})"
        )
        latest_docs = f"[`latest_docs`](https://github.com/obsproject/obs-studio/search?q={k}+path%3Adocs%2Fsphinx&type=code)"
        # "obspython" + "search_term" excluding obspython.py fork spam
        obspython = f'[`obspython`](https://github.com/search?l=Python&o=desc&q=%22obspython%22+"{k}"+-filename%3Aobspython&type=Code) OR '
        obslua = f'[`obslua`](https://github.com/search?l=Lua&o=desc&q=%22obslua%22+"{k}"&type=Code)'
        scripting = obspython + obslua

        nice_data += f"| `{k}` |{source_code}| {latest_docs} | {scripting} | \n"
    nice_data += f"\n Exported {len(data)} entries "
    with open(script_path() + "export.md", "w") as f:
        f.write(nice_data)
    print(f"Done! See {script_path()}export.md")


def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_button(props, "button", "Generate .md index", button_pressed)
    return props
