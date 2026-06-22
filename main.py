import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QTabWidget,
    QMessageBox
)

from theme import apply_dark_theme
from device_detector import DeviceDetector

from dpi import DpiTab
from rgb import RgbTab
from buttons import ButtonsTab
from info import InfoTab


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.device_info = (
            DeviceDetector()
            .detect()
        )

        self.setWindowTitle(
            "GUI4RivalCfg"
        )

        self.resize(
            1000,
            750
        )

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout(self)

        #
        # Tabs
        #

        self.tabs = QTabWidget()

        parsed = self.device_info[
            "parsed_data"
        ]

        #
        # DPI
        #

        if parsed.get("dpi"):

            dpi_tab = DpiTab(
                parsed["dpi"],
                self
            )

            self.tabs.addTab(
                dpi_tab,
                "DPI"
            )

        #
        # RGB
        #

        rgb_tab = RgbTab(
            parsed.get(
                "rgb_zones",
                []
            ),
            parsed.get(
                "effects",
                {}
            ),
            self
        )

        self.tabs.addTab(
            rgb_tab,
            "RGB"
        )

        #
        # Buttons
        #

        if parsed.get("buttons"):

            buttons_tab = ButtonsTab(
                parsed["buttons"],
                self
            )

            self.tabs.addTab(
                buttons_tab,
                "Buttons"
            )

        #
        # Info
        #

        info_tab = InfoTab(
            self.device_info,
            self
        )

        self.tabs.addTab(
            info_tab,
            "Info"
        )

        layout.addWidget(
            self.tabs
        )

        #
        # Logbox
        #

        self.logbox = QTextEdit()

        self.logbox.setReadOnly(
            True
        )

        self.logbox.setMaximumHeight(
            120
        )

        layout.addWidget(
            self.logbox
        )

        #
        # Startup Log
        #

        self.log(
            f"[INFO] Gerät erkannt: {self.device_info['device']}"
        )

        self.log(
            f"[INFO] rivalcfg Version: {self.device_info['rivalcfg_version']}"
        )

    def log(
        self,
        text
    ):

        self.logbox.append(
            text
        )


def main():

    app = QApplication(
        sys.argv
    )

    apply_dark_theme(
        app
    )

    try:

        window = MainWindow()

        window.show()

        sys.exit(
            app.exec()
        )

    except Exception as e:

        QMessageBox.critical(
            None,
            "Fehler",
            str(e)
        )

        sys.exit(1)


if __name__ == "__main__":
    main()
