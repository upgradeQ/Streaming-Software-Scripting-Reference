# OBS Studio Python Scripting Cheatsheet
Getting started:
- [Python](https://www.python.org/about/gettingstarted/)
- [OBS Studio Scripting](https://github.com/obsproject/obs-studio/wiki/Getting-Started-With-OBS-Scripting)

Consider cloning this repo and running examples(they are self contained) in OBS Studio,
most of them will operate on *existing* text soure. Tip: you can create a copy of script,
rename it, and add to OBS.So two of identical scripts will be run in parallel with separated namespaces. 
Also check out [issues](https://github.com/upgradeQ/OBS-Studio-Python-Scripting-Cheatsheet-obspython-Examples-of-API/issues)  if you found any error or have a suggestion and 
[discussions](https://github.com/upgradeQ/OBS-Studio-Python-Scripting-Cheatsheet-obspython-Examples-of-API/discussions) for collaboration,ideas and Q&A.

# Table of content 
- [Using classes](#using-classes)
- [with statement](#with-statement)
- [Passing arguments to callbacks](#passing-arguments-to-callbacks)
- [UI](#ui)
- [Property modification](#property-modification)
- [Additional input](#additional-input)
- [obs_data](#obs_data)
- [save settings as json](#save-settings-as-json)
- [Source's and filters with identifier string](#sources-and-filters-with-identifier-string)
- [Add source](#add-source)
- [Move source](#move-source)
- [Add filter to source](#add-filter-to-source)
- [Toggle sceneitem visibility](#toggle-sceneitem-visibility)
- [Set current scene](#set-current-scene)
- [Get set order in scene](#get-set-order-in-scene)
- [Add scene with sources to current scene](#add-scene-with-sources-to-current-scene)
- [Events](#events)
- [Program state](#program-state)
- [Signals](#signals)
- [Timing (sequential primitives) ](#timing-sequential-primitives)
- [Hotkeys](#hotkeys)
- [Play sound](#play-sound)
- [Read and write private data from scripts or plugins](#read-and-write-private-data-from-scripts-or-plugins)
- [Browser source interaction](#browser-source-interaction)
- [Debug](#debug)
- [Docs and code examples](#docs-and-code-examples)
- [Links](#links)
- [Contribute](#contribute)

## Using classes 
```python
class Example:
    def __init__(self,source_name=None):
        self.source_name = source_name

    def update_text(self):
        source = obs.obs_get_source_by_name(self.source_name)
        if source is not None:
            data = str(next(datacycle))
            settings = obs.obs_data_create()
            obs.obs_data_set_string(settings, "text", data)
            obs.obs_source_update(source, settings)
            obs.obs_data_release(settings)
            obs.obs_source_release(source)
```
[Full example](src/example_class.py)  

Or more compact:  
```python
class _G:
    source_name = ''
    data = None
    flag = False

G = _G()

def script_update(settings):
    G.source_name = ...
    if G.flag:
        pass
```

## with statement 
Automatically release .

```python
@contextmanager
def source_auto_release(source_name):
    source = obs.obs_get_source_by_name(source_name)
    try:
        yield source 
    finally:
        obs.obs_source_release(source)
...
# usage
with source_auto_release(self.source_name) as source:
    if source is not None:
        data = str(next(datacycle))
        with data_auto_release() as settings:
            obs.obs_data_set_string(settings, "text", data)
            obs.obs_source_update(source, settings)
```
[Full example](src/with_stmt.py)  
See also :   
https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager
## Passing arguments to callbacks
```python
from functools import partial
...
flag = obs.obs_data_get_bool(settings,"_obs_bool")
eg.update_text = partial(eg.update_text,flag_func=flag)
...
```
[Full example](src/callback_partial.py)
## UI
|Preview| 
| --- | 
| `obs.obs_properties_add_button(props, "button1", "Refresh1:",callback)` ![img](src/assets/button.png) |
|`obs.obs_properties_add_bool(props,"_bool","_bool:")` ![img](src/assets/bool.png) |
|`obs.obs_properties_add_int(props,"_int","_int:",1,100,1)` ![img](src/assets/int.png) |
|`obs.obs_properties_add_int_slider(props,"_slider","_slider:",1,100,1) ` ![img](src/assets/slider.png) |
|`obs.obs_properties_add_text(props, "_text", "_text:", obs.OBS_TEXT_DEFAULT) ` ![img](src/assets/text.png) |
|`obs.obs_properties_add_color(props,"_color","_color:") ` ![img](src/assets/color.png) |
|`obs.obs_properties_add_font(props,"_font","_font:")  ` ![img](src/assets/font.png) |
|`obs.obs_properties_add_font(props,"_font","_font:")  ` ![img](src/assets/font.png) |
|`bool_p = obs.obs_properties_add_bool(props, "_obs_bool", "Yes/No"); obs.obs_property_set_long_description(bool_p, "Check if yes,else uncheck")` ![img](src/assets/description.gif) |


See also :   
https://obsproject.com/docs/reference-properties.html#property-object-functions

## Property modification
```python
def callback(props, prop, *args, **kwargs):  # pass settings implicitly
    p = obs.obs_properties_get(props, "button")
    n = next(counter)
    obs.obs_property_set_description(p, f"refresh pressed {n} times")
    return True
...
def script_properties():
    props = obs.obs_properties_create()
    b = obs.obs_properties_add_button(
        props, "button", "refresh pressed 0 times", refresh_pressed
    )
    obs.obs_property_set_modified_callback(b, callback)
    return props
```
[Full example](src/property_modification.py)  
See also :  
https://obsproject.com/docs/reference-properties.html#property-modification-functions

## Additional input 
```python
def callback(props, prop, settings):
    _number = obs.obs_data_get_int(settings, "_int")
    _text_value = obs.obs_data_get_string(settings, "_text")
    text_property = obs.obs_properties_get(props, "_text")
    if _number > 50:
        eg.data = _text_value + str(_number)
        obs.obs_property_set_visible(text_property, True)
        return True
    else:
        eg.data = ""
        obs.obs_property_set_visible(text_property, False)
        return True
...

def script_properties():  # ui

    ...
    number = obs.obs_properties_add_int(props, "_int", "Number", 1, 100, 1)
    text_value = obs.obs_properties_add_text(
        props, "_text", "Additional input:", obs.OBS_TEXT_DEFAULT
    )
    obs.obs_property_set_visible(text_value, False)
    obs.obs_property_set_modified_callback(number, callback)
    ...
```
[Full example](src/modification_prop.py)  

Note: properties share similar structure , in Python, Lua, C.
[Example C](https://github.com/obsproject/obs-studio/blob/05c9ddd2293a17717a1bb4189406dfdad79a93e1/plugins/oss-audio/oss-input.c#L626)
See also :  
https://obsproject.com/docs/reference-properties.html#property-modification-functions

## obs_data

- `obs_data_get_string`
- `obs_data_get_int`
- `obs_data_get_double`
- `obs_data_get_bool`
- `obs_data_get_obj`
- `obs_data_get_array`

## Save settings as json

```python
p = Path(__file__).absolute()  # current script path
file = p.parent / "saved_settings.json"
try:
    content = obs.obs_data_get_json(Data._settings_)
    with open(file, "w") as f:
        f.write(content)
except Exception as e:
    print(e, "cannot write to file")
```
[Full example](src/save_json_data.py)  
See also :  
https://obsproject.com/docs/reference-settings.html  
https://obsproject.com/docs/scripting.html#getting-the-current-script-s-path  

# Source's and filters with identifier string
To identify with `obs_source_get_unversioned_id` , or creating source/filter.
## Source's
| Name | Source type identifier string |
| --- | --- | 
| Browser | browser_source | 
| Color Source | color_source |
| Display Capture | monitor_capture |
| Game Capture | game_capture |
| Image | image_source | 
| Image Slide Show | slideshow |
| Media Source | ffmpeg_source |
| Text (GDI+) | text_gdiplus |
| Window Capture | window_capture |
## Filters
| Name | Source type identifier string |
| --- | --- | 
| Async Delay | async_delay_filter |
| Chroma Key | chroma_key_filter |
| Chroma Key V2 | chroma_key_filter_v2 |
| Color Correction | color_filter |
| Color Correction V2 | color_filter_v2 |
| Color Key | color_key_filter |
| Color Key V2 | color_key_filter_v2 |
| Color Grade | color_grade_filter |
| Compressor | compressor_filter | 
| Crop/Pad | crop_filter | 
| Expander | expander_filter | 
| Gain | gain_filter | 
| GPU Delay | gpu_delay_filter | 
| Image Mask/Blend | mask_filter |
| Invert Polarity | invert_polarity_filter |
| Limiter | limiter_filter | 
| Luma Key | luma_key_filter |
| Luma Key V2 | luma_key_filter_v2 |
| Mask | mask_filter |
| Mask V2 | mask_filter_v2 |
| Noise Gate | noise_gate_filter |
| Noise Suppression | noise_suppress_filter |
| Noise Suppression V2 | noise_suppress_filter_v2 |
| Render Delay | gpu_delay |
| Scaling/Aspect Ratio | scale_filter |
| Scroll | scroll_filter | 
| Sharpen | sharpness_filter | 
| Sharpen V2 | sharpness_filter_v2 | 
| Video Delay (Async) | async_delay_filter |
| VST 2.x Plug-in | vst_filter |

# Add source
Create source and add it to current scene 
```python
obs.obs_data_set_string(settings, "text", "The quick brown fox jumps over the lazy dog")
source = obs.obs_source_create_private("text_gdiplus", "test_py", settings)
obs.obs_scene_add(scene, source)
```
[Full example](src/source_add.py)  
See also :  
https://obsproject.com/docs/reference-scenes.html

# Move source
Get current scene , get source name, move source to location 
```python
def __init__(self):
    pos = obs.vec2()
    self.location = pos
...
def move_text_source(self):
    current_scene = obs.obs_frontend_get_current_scene()
    source = obs.obs_get_source_by_name("test_py")
    scene = obs.obs_scene_from_source(current_scene)
    scene_item = obs.obs_scene_find_source(scene, "test_py")
    if scene_item:
        dx, dy = 10, 10
        print("old values", self.location.x)
        obs.obs_sceneitem_get_pos(
            scene_item, self.location
        )  # update to last position if its changed from OBS
        self.location.x += dx
        self.location.y += dy
        print("new values", self.location.x)
        obs.obs_sceneitem_set_pos(scene_item, self.location)
```
[Full example](src/move_source_.py)
# Add filter to source
Filters are sources,they are not listed in obspython module, you need to know its id from `obs_source_info`
```python
obs.obs_data_set_int(settings, "opacity", 50)
source_color = obs.obs_source_create_private(
    "color_filter", "opacity to 50", settings
)
obs.obs_source_filter_add(source, source_color)
```
[Full example](src/source_filter.py)  
See also :  
[Color correction source](https://github.com/obsproject/obs-studio/blob/c938ea712bce0e9d8e0cf348fd8f77725122b9a5/plugins/obs-filters/color-correction-filter.c#L408)  
https://obsproject.com/docs/reference-sources.html
# Toggle sceneitem visibility
```python
def toggle(self):
    current_scene = obs.obs_scene_from_source(obs.obs_frontend_get_current_scene())
    scene_item = obs.obs_scene_find_source(current_scene, self.source_name)
    boolean = not obs.obs_sceneitem_visible(scene_item)
    obs.obs_sceneitem_set_visible(scene_item, boolean)
```
[Full example](src/toggle_sceneitem_vis.py)

# Set current scene
```python
def set_current_scene(self):
    scenes = obs.obs_frontend_get_scenes()
    for scene in scenes:
        name = obs.obs_source_get_name(scene)
        if name == self.scene_name:
            obs.obs_frontend_set_current_scene(scene)
...
scenes = obs.obs_frontend_get_scenes() # Dropdown menu UI
for scene in scenes:
    name = obs.obs_source_get_name(scene)
    obs.obs_property_list_add_string(p, name, name) 
```
[Full example](src/get_scene_by_name.py)
# Get set order in scene
```python
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

```
[Full example](src/change_order.py)

# Add scene with sources to current scene
```python
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
```
Note: sometimes OBS crashes if one of such scenes has been deleted.  
- [Full example](src/add_nested.py)

# Events
```python
def on_event(event):
    if event == obs.OBS_FRONTEND_EVENT_SCENE_CHANGED:
        raise Exception("Triggered when the current scene has changed.")


def script_load(settings):
    obs.obs_frontend_add_event_callback(on_event)
```
[Full example](src/obs_event_exmpl.py)  
See also:  
https://obsproject.com/docs/reference-frontend-api.html#structures-enumerations  
# Program state
Those functions return true or false :
- `obs.obs_frontend_preview_program_mode_active()`
- `obs.obs_frontend_replay_buffer_active()`
- `obs.obs_frontend_recording_active()`
- `obs.obs_frontend_recording_paused()`
- `obs.obs_frontend_streaming_active()`
# Signals
[Signals](https://obsproject.com/docs/frontends.html#signals) , [callbacks](https://obsproject.com/docs/reference-libobs-callback.html) , [differences from C](https://obsproject.com/docs/scripting.html#other-differences-from-the-c-api)
## Core signals
```python
sh = obs.obs_get_signal_handler()
obs.signal_handler_connect(sh,"source_create",callback)
def callback(calldata):
    source = obs.calldata_source(cd,"source")
    print(obs.obs_source_get_name(source))
```
**source_create**, **source_destroy**, **source_remove**, **source_save**, **source_load**, **source_activate**, **source_deactivate**, **source_show**, **source_hide**, **source_rename**, **source_volume**, **source_transition_start**, **source_transition_video_stop**, **source_transition_stop**, **channel_change**, **master_volume**, **hotkey_layout_change**, **hotkey_register**, **hotkey_unregister**, **hotkey_bindings_changed** 

https://obsproject.com/docs/reference-core.html#core-obs-signals

## Scene signals
```python
def connect_cur_scene():
    source = obs.obs_frontend_get_current_scene()
    sh = obs.obs_source_get_signal_handler(source)
    obs.signal_handler_connect(sh, "item_add", callback)
    obs.obs_source_release(source)


def callback(calldata):
    scene_item = obs.calldata_sceneitem(calldata, "item")
    #scene = obs.calldata_source(cd,"scene") # bad utf symbols 
    scene =  obs.obs_sceneitem_get_scene(scene_item)
    name = obs.obs_source_get_name
    source = obs.obs_sceneitem_get_source
    scene_source = obs.obs_scene_get_source
    scene_name = name(scene_source(scene))
    scene_item_name = name(source(scene_item))
    print(f"item {scene_item_name} has been added to scene {scene_name}")
```
- [Full example](src/scene_sig_con.py)

**item_add**, **item_remove**, **reorder**, **refresh**, **item_visible**, **item_locked**, **item_select**, **item_deselect**, **item_transform**

https://obsproject.com/docs/reference-scenes.html#scene-signals
## Source signals 

```python
sh = obs.obs_source_get_signal_handler(some_source)
obs.signal_handler_connect(sh,"show",callback)
def callback(calldata):
    source = obs.calldata_source(cd,"source")
    print("on source show",obs.obs_source_get_name(source))
```

**destroy**, **remove**, **save**, **load**, **activate**, **deactivate**, **show**, **hide**, **mute**, **push_to_mute_changed**, **push_to_mute_delay**, **push_to_talk_changed**, **push_to_talk_delay**, **enable**, **rename**, **volume**, **update_properties**, **update_flags**, **audio_sync**, **audio_mixers**, **filter_add**, **filter_remove**, **reorder_filters**, **transition_start**, **transition_video_stop**, **transition_stop**, **media_started**, **media_ended**, **media_pause**, **media_play**, **media_restart**, **media_stopped**, **media_next**, **media_previous** 

https://obsproject.com/docs/reference-sources.html#source-signals

## Output signals 
```python
def connect_to_rec():
    sh = obs.obs_output_get_signal_handler(obs.obs_frontend_get_recording_output())
    obs.signal_handler_connect(sh, "pause", callback)

def callback(calldata):
    #out = obs.calldata_ptr(calldata, "output") # bad type
    print('output paused')
```

**start**, **stop**, **pause**, **unpause**, **starting**, **stopping**, **activate**, **deactivate**, **reconnect**, **reconnect_success**

https://obsproject.com/docs/reference-outputs.html#output-signals

# Timing (sequential primitives)

```python
def script_update(settings):
    eg.source_name = obs.obs_data_get_string(settings, "source")
    obs.timer_remove(eg.update_text)
    if eg.source_name != "":
        obs.timer_add(eg.update_text, 1 * 1000)
```
[Full example](src/example_class.py)  
Note: each time script updated it's removed first  
See also :   
[Version](src/start_stop_timer.py) with globals and only one timer allowed.  
https://obsproject.com/docs/scripting.html#script-timers  
## Thread
```python
def callback(pressed):
    if pressed:
        toggle_thread()


def busy_thread():
    while True:
        if not data.thread_paused:
            sleep(0.02)
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
```
- [Full example](src/busy_thread.py)

# Hotkeys
This hotkey example will create hotkeys in settings , but you need to bind it manually.
```python
class Hotkey:
    def __init__(self, callback, obs_settings, _id):
        self.obs_data = obs_settings
        self.hotkey_id = obs.OBS_INVALID_HOTKEY_ID
        self.hotkey_saved_key = None
        self.callback = callback
        self._id = _id

        self.load_hotkey()
        self.register_hotkey()
        self.save_hotkey()

...

class h:
    htk_copy = None  # this attribute will hold instance of Hotkey

...
h1 = h()
h2 = h()
...
def script_load(settings):
    h1.htk_copy = Hotkey(cb1, settings, "h1_id")
    h2.htk_copy = Hotkey(cb2, settings, "h2_id")


def script_save(settings):
    h1.htk_copy.save_hotkey()
    h2.htk_copy.save_hotkey()
```
This hotkey example will create hotkeys on fly from json settings , but you need to know internal id.
```python
ID = "htk_id"
JSON_DATA = '{"%s":[{"key":"OBS_KEY_1"}]}' % ID

def on_obs_key_1(pressed):
    if pressed:
        raise Exception("hotkey 1 pressed")

def script_load(settings):
    s = obs.obs_data_create_from_json(JSON_DATA)
    a = obs.obs_data_get_array(s, ID)
    h = obs.obs_hotkey_register_frontend(ID, ID, on_obs_key_1)
    obs.obs_hotkey_load(h, a)
```
Here is how send hotkey to OBS

```python
def send_hotkey(obs_htk_id, key_modifiers=None):
    if key_modifiers:
        shift = key_modifiers.get("shift")
        control = key_modifiers.get("control")
        alt = key_modifiers.get("alt")
        command = key_modifiers.get("command")
    ...
    combo = obs.obs_key_combination()
    combo.modifiers = modifiers
    combo.key = obs.obs_key_from_name(obs_htk_id)
    ...
    obs.obs_hotkey_inject_event(combo, False)
    obs.obs_hotkey_inject_event(combo, True)
    obs.obs_hotkey_inject_event(combo, False)
```

- [Full example](src/obs_httkeys.py) 
- [Example with global ](src/hotkey_exmpl.py)
- [Full example with json](src/hotkey_json.py)  
- [Full example with send hotkey](src/send_hotkey.py)

See also:  
https://github.com/obsproject/obs-studio/blob/master/libobs/obs-hotkeys.h
https://github.com/Palakis/obs-websocket/pull/595

# Play sound
```python
def play_sound():
    ...
    mediaSource = obs.obs_source_create_private(
        "ffmpeg_source", "Global Media Source", None
    )
    s = obs.obs_data_create()
    obs.obs_data_set_string(s, "local_file", script_path() + "alert.mp3")
    obs.obs_source_update(mediaSource, s)
    obs.obs_source_set_monitoring_type(
        mediaSource, obs.OBS_MONITORING_TYPE_MONITOR_AND_OUTPUT
    )
    ...
```
- [Full example](src/play_sound_globally.py)

# Read and write private data from scripts or plugins
Write in one script
```python 
def send_to_private_data(data_type, field, result):
    settings = obs.obs_data_create()
    set = getattr(obs, f"obs_data_set_{data_type}")
    set(settings, field, result)
    obs.obs_apply_private_data(settings)
    obs.obs_data_release(settings)

def write_private_data():
    result = "private value from " + str(__file__) + " " + str(randint(1, 10))
    send_to_private_data("string", "__private__", result)
```
Read from another 
```python
@contextmanager
def p_data_ar(data_type, field):
    settings = obs.obs_get_private_data()
    get = getattr(obs, f"obs_data_get_{data_type}")
    try:
        yield get(settings, field)
    finally:
        obs.obs_data_release(settings)

def print_private_data():
    with p_data_ar("string", "__private__") as value:
        print(value)
```
Lua is also supported
```lua
local obs = obslua
local settings = obs.obs_data_create()
obs.obs_data_set_int(settings,"__private__", 7)
obs.obs_apply_private_data(settings)
obs.obs_data_release(settings)
```

- [Full example read](src/read_private_data.py)
- [Full example write](src/write_private_data.py) 

# Browser source interaction
```python
def send_hotkey_to_browser(source, obs_htk_id, key_modifiers=None, key_up=False):

    key = obs.obs_key_from_name(obs_htk_id)
    vk = obs.obs_key_to_virtual_key(key)
    event = obs.obs_key_event()
    event.native_vkey = vk
    event.modifiers = get_modifiers(key_modifiers)
    event.native_modifiers = event.modifiers  # https://doc.qt.io/qt-5/qkeyevent.html
    event.native_scancode = vk
    event.text = ""
    obs.obs_source_send_key_click(source, event, key_up)


def press_tab(*p):
    with source_auto_release(G.source_name) as source:
        send_hotkey_to_browser(source, "OBS_KEY_TAB")
        send_hotkey_to_browser(source, "OBS_KEY_TAB", key_up=True)


def press_shift_tab(*p):
    with source_auto_release(G.source_name) as source:
        send_hotkey_to_browser(source, "OBS_KEY_TAB", {"shift": True})
        send_hotkey_to_browser(source, "OBS_KEY_TAB", {"shift": True}, key_up=True)

```
- [Full example read](src/browser_source_interaction.py)

# Debug
There is no stdin therefore you can't use pdb , options are:
- using `print`
- using pycharm remote debugging (localhost)
- using [vscode](https://code.visualstudio.com/docs/python/debugging) attach to the process:
    - Load python extension
    - open script file , `pip install debugpy` , place  `debugpy.breakpoint()` somewhere
        - Run (F5) select configuration ( Attach using Process ID)
        - select obs (on windows `obs64.exe`)
        - View  select Debug Console (ctrl+shift+y) 
- [Example debugpy obs ](src/debug_exmpl.py)

![screenshot](src/assets/debug.png)  

# Docs and code examples

[Generated export.md](src/export.md) contains all variables and functions available in `obspython` formatted with markdown. Table consist of links to appropriate search terms in OBS Studio repository, and obswebsocket,links to scripts in `obspython` and `obslua` with each script within github code search.`gs_*` and `matrix_*` functions exluded from that table.   
[Full example](src/export_md.py)  
`Note` : starting from 2020.12.17 Github Code Search no longer works as it was, see also this [thread](https://github.community/t/feedback-on-changes-to-code-search-indexing/150660)  


# Links
- [Scripts forum](https://obsproject.com/forum/resources/categories/scripts.5/) , [Github topic `obs-scripts`](https://github.com/topics/obs-scripts) , [Github topic `obs-script`](https://github.com/topics/obs-script)
- [OBS Studio Repo](https://github.com/obsproject/obs-studio) , [obs-scripting-python.c](https://github.com/obsproject/obs-studio/blob/master/deps/obs-scripting/obs-scripting-python.c)
- [Docs](https://obsproject.com/docs/) , [Docs/scripting](https://obsproject.com/docs/scripting.html) , [Docs/plugins](https://obsproject.com/docs/plugins.html) , [Docs index](https://obsproject.com/docs/genindex.html)
- obspython [Gist](https://gist.github.com/search?l=Python&q=obspython) , [Github](https://github.com/search?l=Python&o=desc&q=obspython&s=indexed&type=Code) , [grep.app](https://grep.app/search?q=obspython&filter[lang][0]=Python)
- obslua [Gist](https://gist.github.com/search?l=Lua&o=desc&q=obslua&s=updated) , [Github](https://github.com/search?l=Lua&o=desc&q=obslua&s=indexed&type=Code) , [grep.app](https://grep.app/search?q=obslua&filter[lang][0]=Lua)
- [A Python bundle for integration with OBS scripting](https://github.com/zooba/obs-python)
- [Lua tips and tricks](https://obsproject.com/forum/threads/tips-and-tricks-for-lua-scripts.132256/)
- [Python 3.6.8 , 64 bit installer](https://www.python.org/downloads/release/python-368/)
# Contribute
Contributions are welcome!
