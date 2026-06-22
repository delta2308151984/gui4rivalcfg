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

        zones = []

        for zone in self.RGB_REGEX.findall(help_text):

            zone = zone.lower()

            if zone == "reactive":
                continue

            zones.append(zone)

        return sorted(set(zones))

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
