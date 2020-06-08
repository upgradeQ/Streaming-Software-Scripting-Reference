import obspython as obs
from pprint import pprint

def refresh_pressed(props, prop):
    print("refresh pressed")
    data = vars(obs)
    with open('export1.txt','w') as f:
        pprint(data,stream=f,width=100)

def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
    return props
