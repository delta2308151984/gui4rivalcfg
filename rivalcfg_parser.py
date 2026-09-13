import re


class RivalCfgParser:

    DPI_REGEX = re.compile(
        r"up to\s+(\d+)\s+settings.*?from\s+(\d+)\s+dpi\s+to\s+(\d+)\s+dpi.*?default:\s*'([^']+)'",
        re.IGNORECASE | re.DOTALL
    )

    RGB_REGEX = re.compile(
        r"--([a-z]+)-color",
        re.IGNORECASE
    )

    BUTTON_REGEX = re.compile(
        r"button(\d+)",
        re.IGNORECASE
    )

    def parse_dpi(self, help_text):

        match = self.DPI_REGEX.search(help_text)

        if not match:
            return None

        defaults = []

        for value in match.group(4).split(","):
            value = value.strip()

            if value.isdigit():
                defaults.append(int(value))

        return {
            "profiles": int(match.group(1)),
            "min": int(match.group(2)),
            "max": int(match.group(3)),
            "default": defaults
        }

    def parse_rgb_zones(self, help_text):
        """Return the RGB controls using the names understood by the GUI.

        rivalcfg uses device-specific option names.  In particular, Rival 3
        calls its three strip zones ``--strip-*-color`` and has a separate
        ``--logo-color`` option.  The old parser returned strings such as
        ``strip-top``; the RGB tab then discarded them because it only knew
        ``top/middle/bottom``.  Keep a stable GUI vocabulary here.
        """
        options = set(re.findall(r"--([a-z0-9-]+)-color", help_text, re.IGNORECASE))
        zones = []

        aliases = {
            "top": ("strip-top", "top"),
            "middle": ("strip-middle", "middle"),
            "bottom": ("strip-bottom", "bottom"),
            "logo": ("logo",),
        }
        for zone, names in aliases.items():
            if any(name in options for name in names):
                zones.append(zone)

        # Devices with one generic LED control (e.g. Prime/Rival 100).
        if "--color" in help_text and not zones:
            zones.append("main")

        return zones

    def parse_effects(self, help_text):

        return {
            "reactive":
                "--reactive-color" in help_text,

            "rainbow":
                "--rainbow-effect" in help_text
        }

    def parse_buttons(self, help_text):

        buttons = sorted(
            set(
                int(v)
                for v in self.BUTTON_REGEX.findall(help_text)
            )
        )

        return {
            "count": len(buttons),
            "buttons": buttons
        }

    def parse_all(self, help_text):

        return {
            "dpi": self.parse_dpi(help_text),
            "rgb_zones": self.parse_rgb_zones(help_text),
            "effects": self.parse_effects(help_text),
            "buttons": self.parse_buttons(help_text)
        }
