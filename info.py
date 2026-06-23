from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame
)

from rivalcfg_wrapper import RivalCfg


class InfoTab(QWidget):

    def __init__(
        self,
        device_info,
        main_window
    ):
        super().__init__()

        self.device_info = device_info
        self.main_window = main_window

        self.cfg = RivalCfg()

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout(self)

        self.device_label = QLabel()
        self.version_label = QLabel()
        self.battery_label = QLabel()

        layout.addWidget(
            self.device_label
        )

        layout.addWidget(
            self.version_label
        )

        layout.addWidget(
            self.battery_label
        )

        self.refresh_button = QPushButton(
            "Batterie aktualisieren"
        )

        self.refresh_button.clicked.connect(
            self.refresh_battery
        )

        layout.addSpacing(
            10
        )

        layout.addWidget(
            self.refresh_button
        )

        #
        # About
        #

        layout.addSpacing(
            10
        )

        line = QFrame()

        line.setFrameShape(
            QFrame.HLine
        )

        layout.addWidget(
            line
        )

        layout.addSpacing(
            60
        )

        layout.addWidget(
            QLabel(
                "GUI4RivalCfg v1.0"
            )
        )

        layout.addSpacing(
            30
        )

        layout.addWidget(
            QLabel(
                "Autor:"
            )
        )

        layout.addWidget(
            QLabel(
                "delta2308151984"
            )
        )

        layout.addSpacing(
            10
        )

        layout.addWidget(
            QLabel(
                "GitHub:"
            )
        )

        layout.addWidget(
            QLabel(
                "github.com/delta2308151984/gui4rivalcfg"
            )
        )

        layout.addStretch()

        self.device_label.setText(
            f"Gerät: {self.device_info['device']}"
        )

        self.version_label.setText(
            f"rivalcfg Version: {self.device_info['rivalcfg_version']}"
        )

        self.refresh_battery()

    def refresh_battery(self):

        try:

            battery = (
                self.cfg
                .get_battery_level()
            )

            self.battery_label.setText(
                f"Batterie: {battery}"
            )

        except Exception:

            self.battery_label.setText(
                "Batterie: n/a"
            )
