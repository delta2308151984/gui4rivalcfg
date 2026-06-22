import json
from pathlib import Path


class ConfigManager:

    def __init__(self):

        self.file = Path(
            "config.json"
        )

    def default_config(self):

        return {

            #
            # DPI
            #

            "dpi": [],

            #
            # RGB
            #

            "rgb": {},

            #
            # Effekte
            #

            "effects": {

                "reactive": False,

                "reactive_color": "FF0000",

                "rainbow": False
            },

            #
            # Energie
            #

            "dim_timer": 30,

            "sleep_timer": 5,

            #
            # Buttons
            #

            "buttons": {}
        }

    def load(self):

        if not self.file.exists():

            data = (
                self.default_config()
            )

            self.save(
                data
            )

            return data

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(
                    f
                )

        except Exception:

            data = (
                self.default_config()
            )

            self.save(
                data
            )

            return data

        #
        # Fehlende Schlüssel ergänzen
        #

        defaults = (
            self.default_config()
        )

        changed = False

        for key, value in defaults.items():

            if key not in data:

                data[key] = value

                changed = True

        #
        # Effects ergänzen
        #

        if "effects" not in data:

            data["effects"] = (
                defaults["effects"]
            )

            changed = True

        else:

            for key, value in defaults[
                "effects"
            ].items():

                if (
                    key
                    not in data["effects"]
                ):

                    data["effects"][
                        key
                    ] = value

                    changed = True

        if changed:

            self.save(
                data
            )

        return data

    def save(
        self,
        data
    ):

        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )
