LANG = "de"

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
        "version": "rivalcfg Version"
    },

    "en": {
        "device": "Device",
        "battery": "Battery",
        "refresh_battery": "Refresh battery",
        "author": "Author",
        "github": "GitHub",
        "version": "rivalcfg Version"
    }
}


def tr(key):

    return TEXT[LANG][key]
