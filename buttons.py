from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QScrollArea
)

from config_manager import ConfigManager
from rivalcfg_wrapper import RivalCfg

from button_mappings import (
    BUTTON_VALUES,
    DEFAULT_MAPPING,
    DISPLAY_NAMES,
    PHYSICAL_BUTTON_NAMES
)


class ButtonsTab(QWidget):

    LABEL_WIDTH = 180
    COMBO_WIDTH = 280
    BUTTON_WIDTH = 180

    def __init__(
        self,
        button_data,
        main_window
    ):
        super().__init__()

        self.main_window = main_window

        self.button_count = button_data.get(
            "count",
            0
        )

        self.config = ConfigManager()
        self.rivalcfg = RivalCfg()

        self.combos = {}

        self.build_ui()

    def build_ui(self):

        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        content = QWidget()

        layout = QVBoxLayout(
            content
        )

        config = self.config.load()

        saved_buttons = config.get(
            "buttons",
            {}
        )

        #
        # Button Dropdowns
        #

        for button_id in range(
            1,
            self.button_count + 1
        ):

            button_name = (
                f"button{button_id}"
            )

            row = QHBoxLayout()

            label = QLabel(
                PHYSICAL_BUTTON_NAMES.get(
                    button_name,
                    button_name
                )
            )

            label.setFixedWidth(
                self.LABEL_WIDTH
            )

            combo = QComboBox()

            combo.setFixedWidth(
                self.COMBO_WIDTH
            )

            for value in BUTTON_VALUES:

                display = (
                    DISPLAY_NAMES.get(
                        value,
                        value
                    )
                )

                combo.addItem(
                    display,
                    value
                )

            default_value = (
                saved_buttons.get(
                    button_name,
                    DEFAULT_MAPPING.get(
                        button_name,
                        "disabled"
                    )
                )
            )

            index = combo.findData(
                default_value
            )

            if index >= 0:

                combo.setCurrentIndex(
                    index
                )

            self.combos[
                button_name
            ] = combo

            row.addWidget(
                label
            )

            row.addWidget(
                combo
            )

            row.addStretch()

            layout.addLayout(
                row
            )

        #
        # Speichern
        #

        save_row = QHBoxLayout()

        self.save_button = QPushButton(
            "Buttons speichern"
        )

        self.save_button.setFixedWidth(
            self.BUTTON_WIDTH
        )

        self.save_button.clicked.connect(
            self.save_buttons
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

        layout.addStretch()

        scroll.setWidget(
            content
        )

        main_layout.addWidget(
            scroll
        )

    def build_mapping_string(self):

        parts = []

        parts.append(
            "layout=QWERTY"
        )

        for (
            button_name,
            combo
        ) in self.combos.items():

            value = (
                combo.currentData()
            )

            parts.append(
                f"{button_name}={value}"
            )

        parts.append(
            "scrollup=ScrollUp"
        )

        parts.append(
            "scrolldown=ScrollDown"
        )

        mapping = (
            "buttons("
            + "; ".join(parts)
            + ")"
        )

        return mapping

    def update_language(self):

        pass

    def save_buttons(self):

        try:

            mapping = (
                self.build_mapping_string()
            )

            self.rivalcfg.set_buttons(
                mapping
            )

            config = self.config.load()

            config["buttons"] = {}

            for (
                button_name,
                combo
            ) in self.combos.items():

                config["buttons"][
                    button_name
                ] = (
                    combo.currentData()
                )

            self.config.save(
                config
            )

            self.main_window.log(
                "[INFO] Buttons gespeichert"
            )

            self.main_window.log(
                mapping
            )

        except Exception as e:

            self.main_window.log(
                f"[ERROR] {e}"
            )
