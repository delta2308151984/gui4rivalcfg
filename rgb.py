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
from language import tr

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

        self.build_rgb_section(
            layout,
            rgb_values
        )

        self.build_reactive_section(
            layout,
            effect_values
        )

        self.build_rainbow_section(
            layout
        )

        self.build_energy_section(
            layout
        )

        self.build_disable_section(
            layout
        )

        layout.addStretch()

        self.update_language()

    def build_rgb_section(
        self,
        layout,
        rgb_values
    ):

        #
        # RGB Zonen
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

        save_row = QHBoxLayout()

        self.save_button = QPushButton()

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

    def build_reactive_section(
        self,
        layout,
        effect_values
    ):

        if not self.effects.get(
            "reactive",
            False
        ):
            return

        reactive_color = effect_values.get(
            "reactive_color",
            "FF0000"
        )

        row = QHBoxLayout()

        self.reactive_label = QLabel()

        self.reactive_label.setFixedWidth(
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

        row.addWidget(
            self.reactive_label
        )

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

        self.reactive_on = QPushButton()
        self.reactive_off = QPushButton()

        self.reactive_on.setFixedWidth(
            self.BUTTON_WIDTH
        )

        self.reactive_off.setFixedWidth(
            self.BUTTON_WIDTH
        )

        self.reactive_on.clicked.connect(
            self.enable_reactive
        )

        self.reactive_off.clicked.connect(
            self.disable_reactive
        )

        button_row.addSpacing(
            self.LABEL_WIDTH
        )

        button_row.addWidget(
            self.reactive_on
        )

        button_row.addWidget(
            self.reactive_off
        )

        button_row.addStretch()

        layout.addLayout(
            button_row
        )

        layout.addWidget(
            self.separator()
        )

    def build_rainbow_section(
        self,
        layout
    ):

        if not self.effects.get(
            "rainbow",
            False
        ):
            return

        self.rainbow_label = QLabel()

        layout.addWidget(
            self.rainbow_label
        )

        rainbow_row = QHBoxLayout()

        self.rainbow_on = QPushButton()
        self.rainbow_off = QPushButton()

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

    def build_energy_section(
        self,
        layout
    ):

        self.energy_label = QLabel()

        layout.addWidget(
            self.energy_label
        )

        config = self.config.load()

        #
        # Dim Timer
        #

        dim_row = QHBoxLayout()

        self.dim_label = QLabel()

        self.dim_label.setFixedWidth(
            self.LABEL_WIDTH
        )

        self.dim_timer_field = QLineEdit(
            str(
                config.get(
                    "dim_timer",
                    30
                )
            )
        )

        self.dim_timer_field.setFixedWidth(
            self.FIELD_WIDTH
        )

        self.seconds_label = QLabel()

        dim_row.addWidget(
            self.dim_label
        )

        dim_row.addWidget(
            self.dim_timer_field
        )

        dim_row.addWidget(
            self.seconds_label
        )

        dim_row.addStretch()

        layout.addLayout(
            dim_row
        )

        #
        # Sleep Timer
        #

        sleep_row = QHBoxLayout()

        self.sleep_label = QLabel()

        self.sleep_label.setFixedWidth(
            self.LABEL_WIDTH
        )

        self.sleep_timer_field = QLineEdit(
            str(
                config.get(
                    "sleep_timer",
                    5
                )
            )
        )

        self.sleep_timer_field.setFixedWidth(
            self.FIELD_WIDTH
        )

        self.minutes_label = QLabel()

        sleep_row.addWidget(
            self.sleep_label
        )

        sleep_row.addWidget(
            self.sleep_timer_field
        )

        sleep_row.addWidget(
            self.minutes_label
        )

        sleep_row.addStretch()

        layout.addLayout(
            sleep_row
        )

        energy_row = QHBoxLayout()

        self.energy_button = QPushButton()

        self.energy_button.setFixedWidth(
            self.BUTTON_WIDTH
        )

        self.energy_button.clicked.connect(
            self.save_energy_settings
        )

        energy_row.addSpacing(
            self.LABEL_WIDTH
        )

        energy_row.addWidget(
            self.energy_button
        )

        energy_row.addStretch()

        layout.addLayout(
            energy_row
        )

        layout.addWidget(
            self.separator()
        )

    def build_disable_section(
        self,
        layout
    ):

        off_row = QHBoxLayout()

        self.rgb_off_button = QPushButton()

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

    def update_language(self):

        self.save_button.setText(
            tr("rgb_save")
        )

        self.rgb_off_button.setText(
            tr("rgb_disable")
        )

        self.energy_label.setText(
            tr("energy")
        )

        self.dim_label.setText(
            tr("dim_timer")
        )

        self.sleep_label.setText(
            tr("sleep_timer")
        )

        self.seconds_label.setText(
            tr("seconds")
        )

        self.minutes_label.setText(
            tr("minutes")
        )

        self.energy_button.setText(
            tr("save")
        )

        if hasattr(
            self,
            "reactive_label"
        ):

            self.reactive_label.setText(
                tr("reactive")
            )

        if hasattr(
            self,
            "rainbow_label"
        ):

            self.rainbow_label.setText(
                tr("rainbow")
            )

        if hasattr(
            self,
            "reactive_on"
        ):

            self.reactive_on.setText(
                tr("enable")
            )

            self.reactive_off.setText(
                tr("disable")
            )

        if hasattr(
            self,
            "rainbow_on"
        ):

            self.rainbow_on.setText(
                tr("enable")
            )

            self.rainbow_off.setText(
                tr("disable")
            )


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
                f"[INFO] {tr('rgb_saved')}"
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
                f"[INFO] {tr('reactive_enabled')}"
            )

        except Exception as e:

            self.main_window.log(
                f"[ERROR] {e}"
            )


    def disable_reactive(self):

        try:

            self.rivalcfg.disable_reactive()

            self.main_window.log(
                f"[INFO] {tr('reactive_disabled')}"
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
                f"[INFO] {tr('rainbow_enabled')}"
            )

        except Exception as e:

            self.main_window.log(
                f"[ERROR] {e}"
            )


    def disable_rainbow(self):

        try:

            self.rivalcfg.disable_rainbow()

            self.main_window.log(
                f"[INFO] {tr('rainbow_disabled')}"
            )

        except Exception as e:

            self.main_window.log(
                f"[ERROR] {e}"
            )

    def save_energy_settings(self):

        try:

            dim_timer = int(
                self.dim_timer_field.text()
            )

            sleep_timer = int(
                self.sleep_timer_field.text()
            )

            if not 0 <= dim_timer <= 1200:

                raise ValueError(
                    tr("dim_timer_invalid")
                )

            if not 0 <= sleep_timer <= 20:

                raise ValueError(
                    tr("sleep_timer_invalid")
                )

            self.rivalcfg.set_dim_timer(
                dim_timer
            )

            self.rivalcfg.set_sleep_timer(
                sleep_timer
            )

            config = self.config.load()

            config["dim_timer"] = dim_timer
            config["sleep_timer"] = sleep_timer

            self.config.save(
                config
            )

            self.main_window.log(
                f"[INFO] {tr('energy_saved')}"
            )

        except Exception as e:

            self.main_window.log(
                f"[ERROR] {e}"
            )

    def disable_rgb(self):

        try:

            self.rivalcfg.disable_rgb()

            self.main_window.log(
                f"[INFO] {tr('rgb_disabled')}"
            )

        except Exception as e:

            self.main_window.log(
                f"[ERROR] {e}"
            )


