import shutil
import subprocess
import re


class RivalCfg:

    def __init__(self):

        self.binary = shutil.which(
            "rivalcfg"
        )

        if not self.binary:

            raise RuntimeError(
                "rivalcfg wurde nicht gefunden"
            )

    #
    # BASIS
    #

    def run(self, *args):

        cmd = [self.binary]
        cmd.extend(args)

        print(
            "RIVALCFG:",
            " ".join(cmd)
        )

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        print(
            "RETURNCODE:",
            result.returncode
        )

        if result.stderr:

            print(
                "STDERR:",
                result.stderr
            )

        if result.returncode != 0:

            raise RuntimeError(
                result.stderr.strip()
            )

        return result.stdout.strip()

    def get_version(self):

        return self.run(
            "--version"
        )

    def get_help(self):

        return self.run(
            "--help"
        )

    def print_debug(self):

        return self.run(
            "--print-debug"
        )

    def list_supported_devices(self):

        return self.run(
            "--list"
        )

    #
    # GERÄTE
    #

    def get_connected_devices(self):

        result = subprocess.run(
            ["lsusb"],
            capture_output=True,
            text=True
        )

        devices = []

        for line in result.stdout.splitlines():

            if "SteelSeries" not in line:
                continue

            match = re.search(
                r"ID ([0-9a-fA-F]{4}):([0-9a-fA-F]{4})",
                line
            )

            if not match:
                continue

            devices.append(
                {
                    "vid": match.group(1).lower(),
                    "pid": match.group(2).lower(),
                    "name": line.strip()
                }
            )

        return devices

    #
    # DPI
    #

    def set_dpi(
        self,
        values
    ):

        dpi_string = ",".join(
            str(v)
            for v in values
        )

        return self.run(
            "--sensitivity",
            dpi_string
        )

    #
    # RGB
    #

    def set_rgb(
        self,
        rgb_values
    ):

        args = []

        if "top" in rgb_values:

            args.extend(
                [
                    "--top-color",
                    rgb_values["top"]
                ]
            )

        if "middle" in rgb_values:

            args.extend(
                [
                    "--middle-color",
                    rgb_values["middle"]
                ]
            )

        if "bottom" in rgb_values:

            args.extend(
                [
                    "--bottom-color",
                    rgb_values["bottom"]
                ]
            )

        if not args:
            return

        return self.run(*args)

    def set_top_color(
        self,
        color
    ):

        return self.run(
            "--top-color",
            color
        )

    def set_middle_color(
        self,
        color
    ):

        return self.run(
            "--middle-color",
            color
        )

    def set_bottom_color(
        self,
        color
    ):

        return self.run(
            "--bottom-color",
            color
        )

    #
    # REACTIVE
    #

    def set_reactive_color(
        self,
        color
    ):

        return self.run(
            "--reactive-color",
            color
        )

    def disable_reactive(self):

        return self.run(
            "--reactive-color",
            "off"
        )

    #
    # RAINBOW
    #
    # Aerox 5 Wireless:
    # rivalcfg --reset aktiviert Rainbow
    #

    def enable_rainbow(self):

        return self.run(
            "--reset"
        )

    def disable_rainbow(self):

        return self.run(
            "--top-color",
            "000000",
            "--middle-color",
            "000000",
            "--bottom-color",
            "000000"
        )

    #
    # RGB KOMPLETT AUS
    #

    def disable_rgb(self):

        return self.run(
            "--top-color",
            "000000",
            "--middle-color",
            "000000",
            "--bottom-color",
            "000000"
        )

    #
    # DEFAULT LIGHTING
    #

    def set_default_lighting(
        self,
        mode
    ):

        return self.run(
            "--default-lighting",
            mode
        )

    #
    # POLLING RATE
    #

    def set_polling_rate(
        self,
        value
    ):

        return self.run(
            "--polling-rate",
            str(value)
        )

    #
    # SLEEP TIMER
    #

    def set_sleep_timer(
        self,
        value
    ):

        return self.run(
            "--sleep-timer",
            str(value)
        )

    def set_dim_timer(
        self,
        value
    ):

        return self.run(
            "--dim-timer",
            str(value)
        )

    #
    # BATTERIE
    #

    def get_battery_level(self):

        return self.run(
            "--battery-level"
        )

    #
    # RESET
    #

    def reset_device(self):

        return self.run(
            "--reset"
        )

    #
    # BUTTONS
    #

    def set_buttons(
        self,
        mapping_string
    ):

        return self.run(
            "--buttons",
            mapping_string
        )
