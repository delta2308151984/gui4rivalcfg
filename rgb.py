from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QColorDialog,
    QFrame
)

from config_manager import ConfigManager
from rivalcfg_wrapper import RivalCfg


class RgbTab(QWidget):

    LABEL_WIDTH = 100
    FIELD_WIDTH = 120
    PICKER_WIDTH = 40
    PREVIEW_WIDTH = 30
    BUTTON_WIDTH = 140

    def __init__(
        self,
        zones,
        effects,
        main_window
    ):
        super().__init__()

        self.main_window = main_window

        self.zones = [
            zone
            for zone in [
                "top",
                "middle",
                "bottom"
            ]
            if zone in zones
        ]

        self.effects = effects

        self.config = ConfigManager()
        self.rivalcfg = RivalCfg()

        self.fields = {}
        self.previews = {}

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout(self)

        config = self.config.load()

        rgb_values = config.get(
            "rgb",
            {}
        )

        effect_values = config.get(
            "effects",
            {}
        )

        #
        # RGB ZONEN
        #

        for zone in self.zones:

            row = QHBoxLayout()

            label = QLabel(
                zone.capitalize()
            )

            label.setFixedWidth(
                self.LABEL_WIDTH
            )

            value = rgb_values.get(
                zone,
                "FFFFFF"
            ).upper()

            field = QLineEdit(
                value
            )

            field.setFixedWidth(
                self.FIELD_WIDTH
            )

            field.setMaxLength(
                6
            )

            picker = QPushButton(
                "🎨"
            )

            picker.setFixedWidth(
                self.PICKER_WIDTH
            )

            preview = QLabel()

            preview.setFixedSize(
                self.PREVIEW_WIDTH,
                20
            )

            preview.setStyleSheet(
                f"""
                background-color: #{value};
                border: 1px solid gray;
                """
            )

            picker.clicked.connect(
                lambda checked=False,
                z=zone:
                self.pick_color(z)
            )

            field.textChanged.connect(
                lambda text,
                z=zone:
                self.update_preview(
                    z,
                    text
                )
            )

            self.fields[zone] = field
            self.previews[zone] = preview

            row.addWidget(label)
            row.addWidget(field)
            row.addWidget(picker)
            row.addWidget(preview)

            row.addStretch()

            layout.addLayout(
                row
            )

        #
        # RGB SPEICHERN
        #

        save_row = QHBoxLayout()

        self.save_button = QPushButton(
            "RGB speichern"
        )

        self.save_button.setFixedWidth(
            self.BUTTON_WIDTH
        )

        self.save_button.clicked.connect(
            self.save_rgb
        )

        save_row.addSpacing(
            self.LABEL_WIDTH
        )

        save_row.addWidget(
            self.save_button
        )

        save_row.addStretch()

        layout.addLayout(
            save_row
        )

        layout.addWidget(
            self.separator()
        )

        #
        # REACTIVE
        #

        if self.effects.get(
            "reactive",
            False
        ):

            reactive_color = (
                effect_values.get(
                    "reactive_color",
                    "FF0000"
                )
            )

            row = QHBoxLayout()

            label = QLabel(
                "Reactive"
            )

            label.setFixedWidth(
                self.LABEL_WIDTH
            )

            self.reactive_field = QLineEdit(
                reactive_color
            )

            self.reactive_field.setFixedWidth(
                self.FIELD_WIDTH
            )

            self.reactive_field.setMaxLength(
                6
            )

            picker = QPushButton(
                "🎨"
            )

            picker.setFixedWidth(
                self.PICKER_WIDTH
            )

            picker.clicked.connect(
                self.pick_reactive_color
            )

            self.reactive_preview = QLabel()

            self.reactive_preview.setFixedSize(
                self.PREVIEW_WIDTH,
                20
            )

            self.reactive_preview.setStyleSheet(
                f"""
                background-color: #{reactive_color};
                border: 1px solid gray;
                """
            )

            row.addWidget(label)

            row.addWidget(
                self.reactive_field
            )

            row.addWidget(
                picker
            )

            row.addWidget(
                self.reactive_preview
            )

            row.addStretch()

            layout.addLayout(
                row
            )

            button_row = QHBoxLayout()

            reactive_on = QPushButton(
                "Aktivieren"
            )

            reactive_off = QPushButton(
                "Deaktivieren"
            )

            reactive_on.setFixedWidth(
                self.BUTTON_WIDTH
            )

            reactive_off.setFixedWidth(
                self.BUTTON_WIDTH
            )

            reactive_on.clicked.connect(
                self.enable_reactive
            )

            reactive_off.clicked.connect(
                self.disable_reactive
            )

            button_row.addSpacing(
                self.LABEL_WIDTH
            )

            button_row.addWidget(
                reactive_on
            )

            button_row.addWidget(
                reactive_off
            )

            button_row.addStretch()

            layout.addLayout(
                button_row
            )

        layout.addWidget(
            self.separator()
        )

        #
        # RAINBOW
        #

        if self.effects.get(
            "rainbow",
            False
        ):

            layout.addWidget(
                QLabel(
                    "Rainbow"
                )
            )

            rainbow_row = QHBoxLayout()

            self.rainbow_on = QPushButton(
                "Aktivieren"
            )

            self.rainbow_off = QPushButton(
                "Deaktivieren"
            )

            self.rainbow_on.setFixedWidth(
                self.BUTTON_WIDTH
            )

            self.rainbow_off.setFixedWidth(
                self.BUTTON_WIDTH
            )

            self.rainbow_on.clicked.connect(
                self.enable_rainbow
            )

            self.rainbow_off.clicked.connect(
                self.disable_rainbow
            )

            rainbow_row.addSpacing(
                self.LABEL_WIDTH
            )

            rainbow_row.addWidget(
                self.rainbow_on
            )

            rainbow_row.addWidget(
                self.rainbow_off
            )

            rainbow_row.addStretch()

            layout.addLayout(
                rainbow_row
            )

        layout.addWidget(
            self.separator()
        )

        #
        # RGB AUS
        #

        off_row = QHBoxLayout()

        self.rgb_off_button = QPushButton(
            "RGB deaktivieren"
        )

        self.rgb_off_button.setFixedWidth(
            self.BUTTON_WIDTH
        )

        self.rgb_off_button.clicked.connect(
            self.disable_rgb
        )

        off_row.addSpacing(
            self.LABEL_WIDTH
        )

        off_row.addWidget(
            self.rgb_off_button
        )

        off_row.addStretch()

        layout.addLayout(
            off_row
        )

        layout.addStretch()

    def separator(self):

        line = QFrame()

        line.setFrameShape(
            QFrame.HLine
        )

        return line

    def pick_color(
        self,
        zone
    ):

        color = QColorDialog.getColor()

        if not color.isValid():
            return

        value = (
            color.name()
            .replace(
                "#",
                ""
            )
            .upper()
        )

        self.fields[zone].setText(
            value
        )

    def pick_reactive_color(self):

        color = QColorDialog.getColor()

        if not color.isValid():
            return

        value = (
            color.name()
            .replace(
                "#",
                ""
            )
            .upper()
        )

        self.reactive_field.setText(
            value
        )

        self.reactive_preview.setStyleSheet(
            f"""
            background-color: #{value};
            border: 1px solid gray;
            """
        )

    def update_preview(
        self,
        zone,
        value
    ):

        value = value.upper()

        if len(value) != 6:
            return

        try:
            int(value, 16)
        except ValueError:
            return

        self.previews[zone].setStyleSheet(
            f"""
            background-color: #{value};
            border: 1px solid gray;
            """
        )

    def save_rgb(self):

        try:

            rgb = {}

            for zone, field in self.fields.items():

                value = (
                    field.text()
                    .strip()
                    .upper()
                )

                rgb[zone] = value

            self.rivalcfg.set_rgb(
                rgb
            )

            config = self.config.load()

            config["rgb"] = rgb

            self.config.save(
                config
            )

            self.main_window.log(
                "[INFO] RGB gespeichert"
            )

        except Exception as e:

            self.main_window.log(
                f"[ERROR] {e}"
            )

    def enable_reactive(self):

        try:

            color = (
                self.reactive_field.text()
                .strip()
                .upper()
            )

            self.rivalcfg.set_reactive_color(
                color
            )

            self.main_window.log(
                "[INFO] Reactive aktiviert"
            )

        except Exception as e:

            self.main_window.log(
                f"[ERROR] {e}"
            )

    def disable_reactive(self):

        try:

            self.rivalcfg.disable_reactive()

            self.main_window.log(
                "[INFO] Reactive deaktiviert"
            )

        except Exception as e:

            self.main_window.log(
                f"[ERROR] {e}"
            )

    def enable_rainbow(self):

        try:

            #
            # Aerox 5 Wireless:
            # Reset aktiviert Rainbow zuverlässig
            #

            self.rivalcfg.enable_rainbow()

            self.main_window.log(
                "[INFO] Rainbow aktiviert"
            )

        except Exception as e:

            self.main_window.log(
                f"[ERROR] {e}"
            )

    def disable_rainbow(self):

        try:

            self.rivalcfg.disable_rainbow()

            self.main_window.log(
                "[INFO] Rainbow deaktiviert"
            )

        except Exception as e:

            self.main_window.log(
                f"[ERROR] {e}"
            )

    def disable_rgb(self):

        try:

            self.rivalcfg.disable_rgb()

            self.main_window.log(
                "[INFO] RGB deaktiviert"
            )

        except Exception as e:

            self.main_window.log(
                f"[ERROR] {e}"
            )
