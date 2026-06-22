from rivalcfg_wrapper import RivalCfg
from rivalcfg_parser import RivalCfgParser


class DeviceDetector:

    SUPPORTED_MICE = [
        "Aerox",
        "Rival",
        "Sensei"
    ]

    def __init__(self):

        self.cfg = RivalCfg()
        self.parser = RivalCfgParser()

    def detect(self):

        version = self.cfg.get_version()

        devices = (
            self.cfg.get_connected_devices()
        )

        if not devices:

            raise RuntimeError(
                "Kein SteelSeries Gerät erkannt"
            )

        #
        # Unterstützte Maus suchen
        #

        mouse_name = None

        for device in devices:

            name = device["name"]

            if any(
                mouse in name
                for mouse in self.SUPPORTED_MICE
            ):

                mouse_name = (
                    name
                    .replace(
                        "SteelSeries ApS ",
                        ""
                    )
                    .replace(
                        "SteelSeries ",
                        ""
                    )
                )

                if "Aerox" in mouse_name:

                    mouse_name = (
                        mouse_name[
                            mouse_name.find(
                                "Aerox"
                            ):
                        ]
                    )

                elif "Rival" in mouse_name:

                    mouse_name = (
                        mouse_name[
                            mouse_name.find(
                                "Rival"
                            ):
                        ]
                    )

                elif "Sensei" in mouse_name:

                    mouse_name = (
                        mouse_name[
                            mouse_name.find(
                                "Sensei"
                            ):
                        ]
                    )

                break

        if not mouse_name:

            raise RuntimeError(
                "Keine unterstützte SteelSeries Maus erkannt"
            )

        #
        # rivalcfg Fähigkeiten laden
        #

        help_text = (
            self.cfg.get_help()
        )

        parsed = (
            self.parser.parse_all(
                help_text
            )
        )

        return {

            "rivalcfg_version":
                version,

            "device":
                mouse_name,

            "parsed_data":
                parsed
        }
