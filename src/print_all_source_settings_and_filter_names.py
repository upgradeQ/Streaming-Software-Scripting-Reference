import obspython as S


class Example:
    source_name = None

    def print_settings(self):
        if not self.source_name:
            print("select source name, will not proceed otherwise")
            return
        source = S.obs_get_source_by_name(self.source_name)
        settings = S.obs_source_get_settings(source)
        psettings = S.obs_source_get_private_settings(source)
        dsettings = S.obs_data_get_defaults(settings)
        pdsettings = S.obs_data_get_defaults(psettings)
        print("[---------- settings ----------")
        print(S.obs_data_get_json(settings))
        print("---------- private_settings ----------")
        print(S.obs_data_get_json(psettings))
        print("---------- default settings for this source type ----------")
        print(S.obs_data_get_json(dsettings))
        print("---------- default private settings for this source type ----------")
        print(S.obs_data_get_json(pdsettings))
        for s in (settings, psettings, dsettings, pdsettings):
            S.obs_data_release(s)
        S.obs_source_release(source)
        print("----------%s----------]" % self.source_name)

        filters = S.obs_source_backup_filters(source)
        filter_count = S.obs_source_filter_count(source)
        print("[--------- filter names --------")
        for i in range(filter_count):
            settings = S.obs_data_array_item(filters, i)
            filter_name = S.obs_data_get_string(settings, "name")
            S.obs_data_release(settings)
            print(filter_name)
        print(" filter names of %s --------" % self.source_name)
        S.obs_data_array_release(filters)

        raise Exception("> Focused to console window")


eg = Example()  # class created ,obs part starts


def button_pressed(props, prop):
    eg.print_settings()


def script_update(settings):
    eg.source_name = S.obs_data_get_string(settings, "source")


def script_properties():  # ui
    props = S.obs_properties_create()
    p = S.obs_properties_add_list(
        props,
        "source",
        "Select source",
        S.OBS_COMBO_TYPE_EDITABLE,
        S.OBS_COMBO_FORMAT_STRING,
    )
    sources = S.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = S.obs_source_get_unversioned_id(source)
            name = S.obs_source_get_name(source)
            S.obs_property_list_add_string(p, name, name)

        S.source_list_release(sources)

    S.obs_properties_add_button(
        props, "button", "Print source settings and filter names", button_pressed
    )
    return props
