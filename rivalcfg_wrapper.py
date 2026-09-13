import os
import json
import re
import shutil
import subprocess
import sys


class RivalCfg:

    def __init__(self):

        # The installer puts rivalcfg into the application's virtualenv.
        # The desktop launcher does not necessarily add that venv's bin
        # directory to PATH, so checking PATH alone makes a valid install
        # look as if rivalcfg were missing.
        venv_binary = os.path.join(
            os.path.dirname(sys.executable),
            "rivalcfg",
        )
        self.binary = shutil.which("rivalcfg") or (
            venv_binary if os.path.isfile(venv_binary) else None
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

        # The option names differ between mouse families.  Rival 3 uses
        # --strip-*-color, while older devices use --top-color, etc.
        help_text = self.get_help()
        option_aliases = {
            "top": ("--strip-top-color", "--top-color"),
            "middle": ("--strip-middle-color", "--middle-color"),
            "bottom": ("--strip-bottom-color", "--bottom-color"),
            "logo": ("--logo-color", "--color"),
            "main": ("--color",),
        }
        for zone, value in rgb_values.items():
            for option in option_aliases.get(zone, ()):
                if option in help_text:
                    args.extend([option, value])
                    break

        if not args:
            return

        return self.run(*args)

    def get_saved_rgb(self, vendor_id, product_id):
        """Read rivalcfg's last persisted device settings.

        rivalcfg has no read-current-RGB CLI command for these mice.  It does
        persist the values used for the device in its per-device JSON file;
        reading that file avoids showing the GUI's unrelated defaults.
        """
        if not vendor_id or not product_id:
            return {}
        try:
            from rivalcfg.mouse_settings import get_settings_path
            path = get_settings_path(int(vendor_id, 16), int(product_id, 16))
            with open(path, encoding="utf-8") as stream:
                settings = json.load(stream).get("default", {})
        except (OSError, ValueError, TypeError, ImportError):
            return {}

        mapping = {
            "z1_color": "top",
            "z2_color": "middle",
            "z3_color": "bottom",
            "logo_color": "logo",
            "color": "main",
        }
        result = {}
        for source, zone in mapping.items():
            value = settings.get(source)
            if value:
                result[zone] = self._color_to_hex(value)
        return result

    @staticmethod
    def _color_to_hex(value):
        try:
            from rivalcfg.color_helpers import parse_color_string
            return "%02X%02X%02X" % parse_color_string(str(value))
        except (ValueError, TypeError, ImportError):
            return str(value).lstrip("#").upper()

    def set_top_color(
        self,
        color
    ):
        return self.set_rgb({"top": color})

    def set_middle_color(
        self,
        color
    ):
        return self.set_rgb({"middle": color})

    def set_bottom_color(
        self,
        color
    ):
        return self.set_rgb({"bottom": color})

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
        return self.disable_rgb()

    #
    # RGB KOMPLETT AUS
    #

    def disable_rgb(self):
        help_text = self.get_help()
        args = []

        # Add every color zone supported by the detected mouse. Rival 3 uses
        # three --strip-*-color options and a separate --logo-color option.
        zone_options = (
            ("--strip-top-color", "--top-color"),
            ("--strip-middle-color", "--middle-color"),
            ("--strip-bottom-color", "--bottom-color"),
            ("--logo-color",),
            ("--wheel-color",),
        )
        for alternatives in zone_options:
            for option in alternatives:
                if option in help_text:
                    args.extend([option, "000000"])
                    break

        # Mice with one generic LED zone use --color.
        if not args and "--color" in help_text:
            args.extend(["--color", "000000"])

        # Stop effects that could immediately light the LEDs again and keep
        # lighting disabled after reconnecting devices that support it.
        if "--reactive-color" in help_text:
            args.extend(["--reactive-color", "off"])
        if "--light-effect" in help_text:
            args.extend(["--light-effect", "steady"])
        if "--default-lighting" in help_text:
            args.extend(["--default-lighting", "off"])

        if not args:
            raise RuntimeError(
                "rgb_disable_unsupported"
            )

        return self.run(*args)

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
