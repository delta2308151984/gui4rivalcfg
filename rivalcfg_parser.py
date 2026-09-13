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

    def parse_profile(self, profile):
        """Read capabilities from rivalcfg's device profile.

        This is more stable than parsing the human-readable ``--help`` text,
        which can change its wrapping and wording between rivalcfg versions.
        """
        settings = profile.get("settings", {})
        sensitivity = settings.get("sensitivity")
        dpi = None

        if sensitivity:
            input_range = sensitivity.get("input_range", [])
            defaults = []
            for item in str(sensitivity.get("default", "")).split(","):
                item = item.strip()
                # XY-capable devices express a symmetric preset as 800:800.
                if ":" in item:
                    x_value, y_value = item.split(":", 1)
                    item = x_value if x_value == y_value else ""
                if item.isdigit():
                    defaults.append(int(item))

            if len(input_range) >= 2:
                dpi = {
                    "profiles": int(sensitivity.get("max_preset_count", 1)),
                    "min": int(input_range[0]),
                    "max": int(input_range[1]),
                    "default": defaults,
                }

        rgb_keys = {
            "z1_color": "top",
            "z2_color": "middle",
            "z3_color": "bottom",
            "logo_color": "logo",
            "color": "main",
        }
        rgb_zones = [
            zone for key, zone in rgb_keys.items()
            if key in settings
        ]

        button_setting = settings.get("buttons_mapping", {})
        button_names = button_setting.get("buttons", {})
        buttons = sorted({
            int(match.group(1))
            for name in button_names
            if (match := re.match(r"button(\d+)$", name, re.IGNORECASE))
        })

        return {
            "dpi": dpi,
            "rgb_zones": rgb_zones,
            "effects": {
                "reactive": "reactive_color" in settings,
                "rainbow": "rainbow_effect" in settings,
            },
            "buttons": {
                "count": len(buttons),
                "buttons": buttons,
            },
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
