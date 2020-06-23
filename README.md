# OBS Studio Python Scripting Cheatsheet
`obspython` OBS Studio API.Obs scripts examples in /src. Each obs script example mostly will operate on *existsing* `TEXT SOURCE`
# Table of content 
- [Using classes](#using-classes)
- [with statement](#with-statement)
- [Passing arguments to callbacks](#passing-arguments-to-callbacks)
- [UI](#ui)
- [Property modification](#property-modification)
- [Additional input](#additional-input)
- [obs_data](#obs_data)
- [Add source](#add-source)
- [Move source](#move-source)
- [Add filter to source](#add-filter-to-source)
- [Timing (sequential primitives) ](#timing-sequential-primitives)
- [Hotkey](#hotkey)
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
```python
    ...
    data = vars(obs)
    with open('export1.txt','w') as f:
        pprint(data,stream=f,width=100)
    ...

```
[Full example](src/export_vars.py)  
[Generated export1.txt](src/export1.txt) contains all variables available in `obspython`  

Overall , properties share similar structure , in Python, Lua, C.
[Example C](https://github.com/obsproject/obs-studio/blob/05c9ddd2293a17717a1bb4189406dfdad79a93e1/plugins/oss-audio/oss-input.c#L626)

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
https://obsproject.com/docs/scripting.html#script-timers  

# Hotkey
```python
class Example:
    def __init__(self, source_name=None):
        self.source_name = source_name
        self.hotkey_id_htk = obs.OBS_INVALID_HOTKEY_ID
    ...
def script_save(settings):
    hotkey_save_array_htk = obs.obs_hotkey_save(eg.hotkey_id_htk)
    obs.obs_data_set_array(settings, "htk_hotkey", hotkey_save_array_htk)
    obs.obs_data_array_release(hotkey_save_array_htk)
    ...
def script_load(settings):
    def callback(pressed):
        if pressed:
            return eg.update_text()

    hotkey_id_htk = obs.obs_hotkey_register_frontend(
        "htk_id", "Example hotkey", callback
    )
    hotkey_save_array_htk = obs.obs_data_get_array(settings, "htk_hotkey")
    obs.obs_hotkey_load(hotkey_id_htk, hotkey_save_array_htk)
    obs.obs_data_array_release(hotkey_save_array_htk)
    ...
```
[Full example](src/hotkey_exmpl.py)
# Links
- [Scripts](https://obsproject.com/forum/resources/categories/scripts.5/)
- [Repo](https://github.com/obsproject/obs-studio)
- [Docs](https://obsproject.com/docs/)
- [Docs/scripting](https://obsproject.com/docs/scripting.html)
- [Docs index](https://obsproject.com/docs/genindex.html)
# Contribute
[Forks](https://help.github.com/articles/fork-a-repo) are a great way to contribute to a repository.
After forking a repository, you can send the original author a [pull request](https://help.github.com/articles/using-pull-requests)
