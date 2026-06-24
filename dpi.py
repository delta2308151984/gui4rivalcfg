from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QLineEdit,
    QPushButton
)

from config_manager import ConfigManager
from rivalcfg_wrapper import RivalCfg
from language import tr

class DpiTab(QWidget):

    def __init__(
        self,
        dpi_data,
        main_window
    ):
        super().__init__()

        self.main_window = main_window

        self.dpi_data = dpi_data

        self.config = ConfigManager()
        self.rivalcfg = RivalCfg()

        self.checkboxes = []
        self.fields = []

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout(self)

        config = self.config.load()

        saved_values = config.get(
            "dpi",
            []
        )

        defaults = self.dpi_data[
            "default"
        ]

        values = (
            saved_values
            if saved_values
            else defaults
        )

        profiles = self.dpi_data[
            "profiles"
        ]

        for index in range(
            profiles
        ):

            row = QHBoxLayout()

            checkbox = QCheckBox()

            label = QLabel(
                f"DPI {index + 1}"
            )

            value = ""

            if index < len(values):

                value = str(
                    values[index]
                )

                checkbox.setChecked(
                    True
                )

            field = QLineEdit(
                value
            )

            field.setMaximumWidth(
                120
            )

            self.checkboxes.append(
                checkbox
            )

            self.fields.append(
                field
            )

            row.addWidget(
                checkbox
            )

            row.addWidget(
                label
            )

            row.addWidget(
                field
            )

            row.addStretch()

            layout.addLayout(
                row
            )

        layout.addStretch()

        self.save_button = QPushButton(
            tr("save")
        )

        self.save_button.clicked.connect(
            self.save_config
        )

        layout.addWidget(
            self.save_button
        )

        self.update_language()

    def update_language(self):

        self.save_button.setText(
            tr("save")
        )

    def get_selected_dpi(self):

        values = []

        for checkbox, field in zip(
            self.checkboxes,
            self.fields
        ):

            if not checkbox.isChecked():
                continue

            try:

                values.append(
                    int(
                        field.text()
                    )
                )

            except ValueError:
                pass

        return values

    def save_config(self):

        dpi_values = (
            self.get_selected_dpi()
        )

        config = self.config.load()

        config["dpi"] = dpi_values

        self.config.save(
            config
        )

        try:

            self.rivalcfg.set_dpi(
                dpi_values
            )

            self.main_window.log(
                f"[INFO] {tr('dpi_saved')}: {dpi_values}"
            )

        except Exception as e:

            self.main_window.log(
                f"[ERROR] {tr('dpi_write_error')}: {e}"
            )
