# OBS Studio Python Scripting Cheatsheet
- `obspython` OBS Studio API.Obs scripts examples in `/src` 
- Each obs script example mostly will operate on *existsing* text source
- It is possible to duplicate scripts and re-add them to OBS ( names must be different) 
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
- [Toggle source visibility](#toggle-source-visibility)
- [Set current scene](#set-current-scene)
- [Get set order in scene](#get-set-order-in-scene)
- [Events](#events)
- [Program state](#program-state)
- [Timing (sequential primitives) ](#timing-sequential-primitives)
- [Hotkeys](#hotkeys)
- [Debug](#debug)
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
|code   | result  |
| ---   | ---     |
|`obs.obs_properties_add_button(props, "button1", "Refresh1:",callback)` | ![img](src/button.png) |
|`obs.obs_properties_add_bool(props,"_bool","_bool:")` | ![img](src/bool.png) |
|`obs.obs_properties_add_int(props,"_int","_int:",1,100,1)` | ![img](src/int.png) |
|`obs.obs_properties_add_int_slider(props,"_slider","_slider:",1,100,1) ` | ![img](src/slider.png) |
|`obs.obs_properties_add_text(props, "_text", "_text:", obs.OBS_TEXT_DEFAULT) ` | ![img](src/text.png) |
|`obs.obs_properties_add_color(props,"_color","_color:") ` | ![img](src/color.png) |
|`obs.obs_properties_add_font(props,"_font","_font:")  `|  ![img](src/font.png) |

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
See also :  
https://obsproject.com/docs/reference-properties.html#property-modification-functions

## obs_data

- `obs_data_get_string`
- `obs_data_get_int`
- `obs_data_get_double`
- `obs_data_get_bool`
- `obs_data_get_obj`
- `obs_data_get_array`

 Introspection of `obspython`: 
```python
    ...
    data = vars(obs)
    with open('export1.txt','w') as f:
        pprint(data,stream=f,width=100)
    ...

```
[Full example](src/export_vars.py)  
[Generated export1.txt](src/export1.txt) contains all variables available in `obspython`  

Note: properties share similar structure , in Python, Lua, C.
[Example C](https://github.com/obsproject/obs-studio/blob/05c9ddd2293a17717a1bb4189406dfdad79a93e1/plugins/oss-audio/oss-input.c#L626)

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
| Compressor | compressor_filter | 
| Expander | expander_filter | 
| Gain | gain_filter | 
| Invert Polarity | invert_polarity_filter |
| Limiter | limiter_filter | 
| Noise Gate | noise_gate_filter |
| Noise Suppression | noise_suppress_filter |
| VST 2.x Plug-in | vst_filter |
| Video Delay (Async) | async_delay_filter |
| Chroma Key | chroma_key_filter |
| Color Correction | color_filter |
| Color Key | color_key_filter |
| Crop/Pad | crop_filter | 
| Image Mask/Blend | mask_filter |
| Luma Key | luma_key_filter |
| Render Delay | gpu_delay |
| Scaling/Aspect Ratio | scale_filter |
| Scroll | scroll_filter | 
| Sharpen | sharpness_filter | 


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
# Toggle source visibility
```python
def toggle(self):
    current_scene = obs.obs_scene_from_source(obs.obs_frontend_get_current_scene())
    scene_item = obs.obs_scene_find_source(current_scene, self.source_name)
    boolean = not obs.obs_sceneitem_visible(scene_item)
    obs.obs_sceneitem_set_visible(scene_item, boolean)
```
[Full example](src/toggle_source_vis.py)

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
- [Full example](src/obs_httkeys.py) 
- [Example with global ](src/hotkey_exmpl.py)
- [Full example with json](src/hotkey_json.py)  

See also:  
https://github.com/obsproject/obs-studio/blob/master/libobs/obs-hotkeys.h

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

![screenshot](src/debug.png)  

# Links
- [Scripts](https://obsproject.com/forum/resources/categories/scripts.5/)
- [Repo](https://github.com/obsproject/obs-studio)
- [Docs](https://obsproject.com/docs/) , [Docs/scripting](https://obsproject.com/docs/scripting.html) , [Docs index](https://obsproject.com/docs/genindex.html)
- [Gist](https://gist.github.com/search?l=Python&q=obspython)
- [Github](https://github.com/search?l=Python&o=desc&q=obspython&s=indexed&type=Code)
# Contribute
Contributions are welcome!
