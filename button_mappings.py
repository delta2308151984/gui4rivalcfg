BUTTON_VALUES = [

    #
    # Mausbuttons
    #

    "button1",
    "button2",
    "button3",
    "button4",
    "button5",
    "button6",
    "button7",
    "button8",
    "button9",

    #
    # Spezial
    #

    "dpi",
    "disabled",

    "ScrollUp",
    "ScrollDown",

    #
    # Multimedia
    #

    "Mute",
    "PlayPause",
    "Next",
    "Previous",
    "VolumeUp",
    "VolumeDown",

    #
    # Tastatur A-Z
    #

    *[chr(c) for c in range(ord("A"), ord("Z") + 1)],

    #
    # Zahlen
    #

    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",

    #
    # Funktionstasten
    #

    *[
        f"F{i}"
        for i in range(1, 13)
    ],

    #
    # Navigation
    #

    "PageUp",
    "PageDown",

    "Home",
    "End",

    "Insert",
    "Delete",

    #
    # Pfeile
    #

    "Up",
    "Down",
    "Left",
    "Right",

    #
    # Modifier
    #

    "Ctrl",
    "Alt",
    "Shift",

    "LeftCtrl",
    "RightCtrl",

    "LeftAlt",
    "RightAlt",

    "LeftShift",
    "RightShift",

    #
    # Sonstige
    #

    "Enter",
    "Escape",
    "Space",
    "Tab",
    "Backspace"
]


DEFAULT_MAPPING = {

    "button1": "button1",
    "button2": "button2",
    "button3": "button3",
    "button4": "button4",
    "button5": "button5",
    "button6": "dpi",
    "button7": "disabled",
    "button8": "disabled",
    "button9": "disabled"
}


#
# Physische Aerox-5-Tasten
#

PHYSICAL_BUTTON_NAMES = {

    "button1": "Linksklick",
    "button2": "Rechtsklick",
    "button3": "Mittelklick",

    "button4": "Seitentaste Zurück",
    "button5": "Seitentaste Vor",

    "button6": "DPI Taste",

    "button7": "Daumentaste Oben",
    "button8": "Daumentaste Mitte",
    "button9": "Daumentaste Unten"
}


DISPLAY_NAMES = {

    #
    # Maus
    #

    "button1": "Linksklick",
    "button2": "Rechtsklick",
    "button3": "Mittelklick",

    "button4": "Seitentaste Zurück",
    "button5": "Seitentaste Vor",

    "button6": "DPI Taste",

    "button7": "Daumentaste Oben",
    "button8": "Daumentaste Mitte",
    "button9": "Daumentaste Unten",

    #
    # Spezial
    #

    "dpi": "DPI Umschalten",

    "disabled": "Deaktiviert",

    "ScrollUp": "Mausrad Hoch",
    "ScrollDown": "Mausrad Runter",

    #
    # Multimedia
    #

    "Mute": "Stumm",

    "PlayPause": "Play / Pause",

    "Next": "Nächster Titel",
    "Previous": "Vorheriger Titel",

    "VolumeUp": "Lauter",
    "VolumeDown": "Leiser",

    #
    # Navigation
    #

    "PageUp": "Bild Hoch",
    "PageDown": "Bild Runter",

    "Home": "Pos1",
    "End": "Ende",

    "Insert": "Einfügen",
    "Delete": "Entfernen",

    #
    # Pfeile
    #

    "Up": "Pfeil Hoch",
    "Down": "Pfeil Runter",
    "Left": "Pfeil Links",
    "Right": "Pfeil Rechts",

    #
    # Modifier
    #

    "Ctrl": "Strg",
    "Alt": "Alt",
    "Shift": "Shift",

    "LeftCtrl": "Strg Links",
    "RightCtrl": "Strg Rechts",

    "LeftAlt": "Alt Links",
    "RightAlt": "Alt Rechts",

    "LeftShift": "Shift Links",
    "RightShift": "Shift Rechts",

    #
    # Sonstige
    #

    "Enter": "Enter",
    "Escape": "Escape",
    "Space": "Leertaste",
    "Tab": "Tabulator",
    "Backspace": "Backspace"
}
