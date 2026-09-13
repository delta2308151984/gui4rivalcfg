import json
import re

from PySide6.QtCore import QTimer, QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame
)

from rivalcfg_wrapper import RivalCfg
from language import tr
from version import __version__

class InfoTab(QWidget):

    LATEST_RELEASE_API = (
        "https://api.github.com/repos/"
        "delta2308151984/gui4rivalcfg/releases/latest"
    )
    RELEASES_URL = (
        "https://github.com/delta2308151984/"
        "gui4rivalcfg/releases/latest"
    )

    def __init__(
        self,
        device_info,
        main_window
    ):
        super().__init__()

        self.device_info = device_info
        self.main_window = main_window

        self.cfg = RivalCfg()
        self.network_manager = QNetworkAccessManager(self)
        self.update_reply = None

        self.build_ui()
        self.update_language()
        QTimer.singleShot(0, self.check_for_update)

    def build_ui(self):

        layout = QVBoxLayout(self)

        self.device_label = QLabel()
        self.version_label = QLabel()
        self.latest_version_label = QLabel()
        self.update_notice_label = QLabel()
        self.rivalcfg_version_label = QLabel()
        self.battery_label = QLabel()

        layout.addWidget(
            self.device_label
        )

        layout.addWidget(
            self.version_label
        )

        layout.addWidget(
            self.latest_version_label
        )

        self.update_notice_label.setWordWrap(True)
        self.update_notice_label.setOpenExternalLinks(True)
        layout.addWidget(self.update_notice_label)

        layout.addWidget(
            self.rivalcfg_version_label
        )

        layout.addWidget(
            self.battery_label
        )

        self.refresh_button = QPushButton(
            tr("refresh_battery")
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
                "GUI4RivalCfg"
            )
        )

        layout.addSpacing(
            30
        )

        self.author_title = QLabel()

        layout.addWidget(
            self.author_title
        )

        layout.addWidget(
            QLabel(
                "delta2308151984"
            )
        )

        layout.addSpacing(
            10
        )

        self.github_title = QLabel()

        layout.addWidget(
            self.github_title
        )

        layout.addWidget(
            QLabel(
                "github.com/delta2308151984/gui4rivalcfg"
            )
        )

        layout.addStretch()



    def update_language(self):

        self.refresh_button.setText(
            tr("refresh_battery")
        )

        self.author_title.setText(
            tr("author") + ":"
        )

        self.github_title.setText(
            tr("github") + ":"
        )

        self.device_label.setText(
            f"{tr('device')}: "
            f"{self.device_info['device']}"
        )

        self.version_label.setText(
            f"{tr('installed_version')}: "
            f"{__version__}"
        )

        if self.update_reply is None and not self.latest_version_label.text():
            self.latest_version_label.setText(tr("checking_for_updates"))

        self.rivalcfg_version_label.setText(
            f"{tr('rivalcfg_version')}: "
            f"{self.device_info['rivalcfg_version']}"
        )

        self.refresh_battery()

    def check_for_update(self):

        self.latest_version_label.setText(
            tr("checking_for_updates")
        )
        self.update_notice_label.clear()

        request = QNetworkRequest(
            QUrl(self.LATEST_RELEASE_API)
        )
        request.setRawHeader(
            b"User-Agent",
            f"GUI4RivalCfg/{__version__}".encode("ascii")
        )

        self.update_reply = self.network_manager.get(request)
        self.update_reply.finished.connect(
            self.finish_update_check
        )
        QTimer.singleShot(10000, self.abort_update_check)

    def abort_update_check(self):

        if (
            self.update_reply is not None
            and self.update_reply.isRunning()
        ):
            self.update_reply.abort()

    def finish_update_check(self):

        reply = self.update_reply
        self.update_reply = None

        if reply is None:
            return

        try:
            if reply.error() != QNetworkReply.NetworkError.NoError:
                raise RuntimeError(reply.errorString())

            payload = json.loads(
                bytes(reply.readAll()).decode("utf-8")
            )
            latest_version = str(
                payload["tag_name"]
            ).lstrip("vV")

            self.latest_version_label.setText(
                f"{tr('latest_version')}: {latest_version}"
            )

            if self.version_tuple(latest_version) > self.version_tuple(__version__):
                self.update_notice_label.setText(
                    '<span style="color: #ffb74d; font-weight: bold;">'
                    f"{tr('update_available')}</span> "
                    f'<a href="{self.RELEASES_URL}">'
                    f"{tr('open_download')}</a>"
                )
                self.main_window.log(
                    f"[UPDATE] {tr('update_log_available')}: "
                    f"{latest_version}"
                )
            else:
                self.update_notice_label.setText(
                    '<span style="color: #66bb6a;">'
                    f"{tr('up_to_date')}</span>"
                )
                self.main_window.log(
                    f"[INFO] {tr('update_log_current')}: "
                    f"{__version__}"
                )

        except (KeyError, ValueError, TypeError, RuntimeError, json.JSONDecodeError):
            self.latest_version_label.setText(
                tr("update_check_failed")
            )
            self.update_notice_label.clear()
            self.main_window.log(
                f"[WARN] {tr('update_log_failed')}"
            )
        finally:
            reply.deleteLater()

    @staticmethod
    def version_tuple(version):

        match = re.match(
            r"^(\d+)\.(\d+)\.(\d+)",
            str(version).lstrip("vV")
        )
        if not match:
            raise ValueError("Ungültige Versionsnummer")
        return tuple(int(value) for value in match.groups())

    def refresh_battery(self):

        try:

            battery = (
                self.cfg
                .get_battery_level()
            )

            self.battery_label.setText(
                f"{tr('battery')}: {battery}"
            )

        except Exception:

            self.battery_label.setText(
                f"{tr('battery')}: n/a"
            )
