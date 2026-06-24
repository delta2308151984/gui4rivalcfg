LANG = "en"

def set_language(lang):

    global LANG

    LANG = lang

def get_language():

    return LANG

TEXT = {
    "de": {
        "device": "Gerät",
        "battery": "Batterie",
        "refresh_battery": "Batterie aktualisieren",
        "author": "Autor",
        "github": "GitHub",
        "version": "rivalcfg Version",
        "tab_dpi": "DPI",
        "tab_rgb": "RGB",
        "tab_buttons": "Buttons",
        "tab_info": "Info",
        "save": "Speichern",
        "dpi_saved": "DPI gespeichert und auf Maus geschrieben",
        "dpi_write_error": "DPI konnte nicht geschrieben werden"
    },

    "en": {
        "device": "Device",
        "battery": "Battery",
        "refresh_battery": "Refresh battery",
        "author": "Author",
        "github": "GitHub",
        "version": "rivalcfg Version",
        "tab_dpi": "DPI",
        "tab_rgb": "RGB",
        "tab_buttons": "Buttons",
        "tab_info": "Info",
        "save": "Save",
        "dpi_saved": "DPI saved and written to mouse",
        "dpi_write_error": "Failed to write DPI"
    }
}


def tr(key):

    return TEXT[LANG][key]
