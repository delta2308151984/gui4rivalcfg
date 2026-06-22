import json
from pathlib import Path


class ConfigManager:

    def __init__(self):
        self.file = Path("config.json")

    def default_config(self):

        return {
            "dpi": [],

            "rgb": {},

            "effects": {
                "reactive": False,
                "reactive_color": "FF0000",
                "rainbow": False
            },

            "buttons": {}
        }

    def load(self):

        if not self.file.exists():

            data = self.default_config()

            self.save(data)

            return data

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:

            data = self.default_config()

            self.save(data)

            return data

    def save(self, data):

        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )
