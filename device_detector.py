from rivalcfg_wrapper import RivalCfg
from rivalcfg_parser import RivalCfgParser


class DeviceDetector:

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
                devices[0]["name"],

            "parsed_data":
                parsed
        }
