from config_manager import ConfigManager

_config_manager = ConfigManager()
_config = _config_manager.load()

LANG = _config.get(
    "language",
    "en"
)


TEXT = {

    "de": {

        #
        # Tabs
        #

        "tab_dpi": "DPI",
        "tab_rgb": "RGB",
        "tab_buttons": "Buttons",
        "tab_info": "Info",

        #
        # Allgemein
        #

        "save": "Speichern",
        "enable": "Aktivieren",
        "disable": "Deaktivieren",

        #
        # Info
        #

        "device": "Gerät",
        "battery": "Batterie",
        "refresh_battery": "Batterie aktualisieren",
        "author": "Autor",
        "github": "GitHub",
        "version": "GUI4RivalCfg Version",

        #
        # DPI
        #

        "dpi_saved": "DPI gespeichert",
        "dpi_write_error": "DPI konnte nicht geschrieben werden",

        #
        # RGB
        #

        "rgb_save": "RGB speichern",
        "rgb_saved": "RGB gespeichert",
        "rgb_disable": "RGB deaktivieren",
        "rgb_disabled": "RGB deaktiviert",

        #
        # Reactive
        #

        "reactive": "Reactive",
        "reactive_enabled": "Reactive aktiviert",
        "reactive_disabled": "Reactive deaktiviert",

        #
        # Rainbow
        #

        "rainbow": "Rainbow",
        "rainbow_enabled": "Rainbow aktiviert",
        "rainbow_disabled": "Rainbow deaktiviert",

        #
        # Energie
        #

        "energy": "Energie",
        "dim_timer": "Dim Timer",
        "sleep_timer": "Sleep Timer",
        "seconds": "Sekunden",
        "minutes": "Minuten",

        "energy_saved":
            "Energieeinstellungen gespeichert",

        "energy_save_error":
            "Energieeinstellungen konnten nicht gespeichert werden",

        "dim_timer_invalid":
            "Dim Timer muss zwischen 0 und 1200 Sekunden liegen",

        "sleep_timer_invalid":
            "Sleep Timer muss zwischen 0 und 20 Minuten liegen",
    },

    "en": {

        #
        # Tabs
        #

        "tab_dpi": "DPI",
        "tab_rgb": "RGB",
        "tab_buttons": "Buttons",
        "tab_info": "Info",

        #
        # General
        #

        "save": "Save",
        "enable": "Enable",
        "disable": "Disable",

        #
        # Info
        #

        "device": "Device",
        "battery": "Battery",
        "refresh_battery": "Refresh Battery",
        "author": "Author",
        "github": "GitHub",
        "version": "GUI4RivalCfg Version",

        #
        # DPI
        #

        "dpi_saved": "DPI saved",
        "dpi_write_error": "Failed to write DPI",

        #
        # RGB
        #

        "rgb_save": "Save RGB",
        "rgb_saved": "RGB saved",
        "rgb_disable": "Disable RGB",
        "rgb_disabled": "RGB disabled",

        #
        # Reactive
        #

        "reactive": "Reactive",
        "reactive_enabled": "Reactive enabled",
        "reactive_disabled": "Reactive disabled",

        #
        # Rainbow
        #

        "rainbow": "Rainbow",
        "rainbow_enabled": "Rainbow enabled",
        "rainbow_disabled": "Rainbow disabled",

        #
        # Power
        #

        "energy": "Power",
        "dim_timer": "Dim Timer",
        "sleep_timer": "Sleep Timer",
        "seconds": "Seconds",
        "minutes": "Minutes",

        "energy_saved":
            "Power settings saved",

        "energy_save_error":
            "Failed to save power settings",

        "dim_timer_invalid":
            "Dim timer must be between 0 and 1200 seconds",

        "sleep_timer_invalid":
            "Sleep timer must be between 0 and 20 minutes",
    }
}


def set_language(lang):

    global LANG

    LANG = lang

    config = _config_manager.load()

    config["language"] = lang

    _config_manager.save(config)


def get_language():

    return LANG


def tr(key):

    return TEXT.get(
        LANG,
        TEXT["en"]
    ).get(
        key,
        key
    )
