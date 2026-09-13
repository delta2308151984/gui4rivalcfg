import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

from PySide6.QtCore import QProcess, QTimer, QUrl, Signal
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QFrame
)

from config_manager import ConfigManager
from rivalcfg_wrapper import RivalCfg
from language import tr
from version import __version__

class InfoTab(QWidget):

    update_available = Signal()

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
        self.config = ConfigManager()
        self.network_manager = QNetworkAccessManager(self)
        self.update_reply = None
        self.download_reply = None
        self.latest_asset = None
        self.latest_version = None
        self.last_update_result = None
        self.update_result_logged = False
        self.update_status = "checking"

        self.build_ui()
        self.update_language()
        self.load_update_result()
        QTimer.singleShot(0, self.check_for_update)

    def build_ui(self):

        layout = QVBoxLayout(self)

        self.device_label = QLabel()
        self.version_label = QLabel()
        self.latest_version_label = QLabel()
        self.update_notice_label = QLabel()
        self.update_result_label = QLabel()
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

        self.update_result_label.setWordWrap(True)
        layout.addWidget(self.update_result_label)

        self.install_update_button = QPushButton()
        self.install_update_button.setVisible(False)
        self.install_update_button.clicked.connect(
            self.download_update
        )
        layout.addWidget(self.install_update_button)

        self.update_progress = QProgressBar()
        self.update_progress.setRange(0, 100)
        self.update_progress.setVisible(False)
        layout.addWidget(self.update_progress)

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

        if self.download_reply is None:
            self.install_update_button.setText(
                tr("install_update")
            )

        self.render_update_status()

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
        self.display_update_result()

    def check_for_update(self):

        self.latest_version_label.setText(
            tr("checking_for_updates")
        )
        self.update_notice_label.clear()
        self.install_update_button.setVisible(False)
        self.latest_asset = None
        self.latest_version = None
        self.update_status = "checking"

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
            self.latest_version = latest_version

            self.latest_version_label.setText(
                f"{tr('latest_version')}: {latest_version}"
            )

            if self.version_tuple(latest_version) > self.version_tuple(__version__):
                self.update_status = "available"
                expected_name = f"gui4rivalcfg-{latest_version}.tar.gz"
                asset = next(
                    (
                        item for item in payload.get("assets", [])
                        if item.get("name") == expected_name
                    ),
                    None
                )
                digest = str((asset or {}).get("digest", ""))
                if asset and digest.startswith("sha256:"):
                    asset_url = QUrl(asset["browser_download_url"])
                    if asset_url.scheme() != "https" or asset_url.host() != "github.com":
                        raise RuntimeError("Unexpected update download URL")
                    self.latest_asset = {
                        "url": asset_url.toString(),
                        "sha256": digest.split(":", 1)[1],
                    }
                    self.install_update_button.setVisible(True)

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
                self.update_available.emit()
            else:
                self.update_status = "current"
                self.install_update_button.setVisible(False)
                self.update_notice_label.setText(
                    '<span style="color: #66bb6a;">'
                    f"{tr('up_to_date')}</span>"
                )
                self.main_window.log(
                    f"[INFO] {tr('update_log_current')}: "
                    f"{__version__}"
                )

        except (KeyError, ValueError, TypeError, RuntimeError, json.JSONDecodeError):
            self.update_status = "failed"
            self.latest_version_label.setText(
                tr("update_check_failed")
            )
            self.update_notice_label.clear()
            self.main_window.log(
                f"[WARN] {tr('update_log_failed')}"
            )
        finally:
            reply.deleteLater()

    def render_update_status(self):

        if self.update_status == "checking":
            self.latest_version_label.setText(tr("checking_for_updates"))
        elif self.update_status == "available" and self.latest_version:
            self.latest_version_label.setText(
                f"{tr('latest_version')}: {self.latest_version}"
            )
            self.update_notice_label.setText(
                '<span style="color: #ffb74d; font-weight: bold;">'
                f"{tr('update_available')}</span> "
                f'<a href="{self.RELEASES_URL}">'
                f"{tr('open_download')}</a>"
            )
        elif self.update_status == "current" and self.latest_version:
            self.latest_version_label.setText(
                f"{tr('latest_version')}: {self.latest_version}"
            )
            self.update_notice_label.setText(
                '<span style="color: #66bb6a;">'
                f"{tr('up_to_date')}</span>"
            )
        elif self.update_status == "failed":
            self.latest_version_label.setText(tr("update_check_failed"))
            self.update_notice_label.clear()

    def download_update(self):

        if not self.latest_asset or not self.latest_version:
            return

        answer = QMessageBox.question(
            self,
            tr("update_title"),
            tr("update_confirmation").format(
                version=self.latest_version
            ),
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        self.install_update_button.setEnabled(False)
        self.install_update_button.setText(tr("downloading_update"))
        self.update_progress.setValue(0)
        self.update_progress.setVisible(True)

        request = QNetworkRequest(
            QUrl(self.latest_asset["url"])
        )
        request.setRawHeader(
            b"User-Agent",
            f"GUI4RivalCfg/{__version__}".encode("ascii")
        )
        self.download_reply = self.network_manager.get(request)
        self.download_reply.downloadProgress.connect(
            self.update_download_progress
        )
        self.download_reply.finished.connect(
            self.finish_update_download
        )
        QTimer.singleShot(120000, self.abort_update_download)

    def update_download_progress(self, received, total):

        if total > 0:
            self.update_progress.setValue(
                int(received * 100 / total)
            )

    def abort_update_download(self):

        if (
            self.download_reply is not None
            and self.download_reply.isRunning()
        ):
            self.download_reply.abort()

    def finish_update_download(self):

        reply = self.download_reply
        self.download_reply = None

        if reply is None:
            return

        try:
            if reply.error() != QNetworkReply.NetworkError.NoError:
                raise RuntimeError(reply.errorString())

            archive_data = bytes(reply.readAll())
            actual_digest = hashlib.sha256(archive_data).hexdigest()
            expected_digest = self.latest_asset["sha256"].lower()
            if actual_digest != expected_digest:
                raise RuntimeError("SHA-256 checksum mismatch")

            with tempfile.NamedTemporaryFile(
                prefix="gui4rivalcfg-update-",
                suffix=".tar.gz",
                delete=False
            ) as stream:
                stream.write(archive_data)
                archive_path = stream.name

            updater_path = str(
                Path(__file__).with_name("updater.py")
            )
            launcher_path = str(
                Path.home() / ".local/bin/gui4rivalcfg"
            )
            started, _process_id = QProcess.startDetached(
                sys.executable,
                [
                    updater_path,
                    "--archive", archive_path,
                    "--sha256", expected_digest,
                    "--version", self.latest_version,
                    "--launcher", launcher_path,
                    "--wait-pid", str(os.getpid()),
                ]
            )
            if not started:
                Path(archive_path).unlink(missing_ok=True)
                raise RuntimeError("Updater could not be started")

            self.main_window.log(
                f"[INFO] {tr('update_installing')}: "
                f"{self.latest_version}"
            )
            QApplication.quit()

        except (KeyError, OSError, RuntimeError, TypeError) as error:
            self.install_update_button.setEnabled(True)
            self.install_update_button.setText(tr("install_update"))
            self.update_progress.setVisible(False)
            self.update_notice_label.setText(
                '<span style="color: #ef5350; font-weight: bold;">'
                f"{tr('update_download_failed')}</span>"
            )
            self.main_window.log(
                f"[ERROR] {tr('update_download_failed')}: {error}"
            )
        finally:
            reply.deleteLater()

    def load_update_result(self):

        result_file = self.config.update_result_file
        if not result_file.is_file():
            return
        try:
            self.last_update_result = json.loads(
                result_file.read_text(encoding="utf-8")
            )
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            self.last_update_result = {"status": "error", "version": ""}
        finally:
            result_file.unlink(missing_ok=True)
        self.display_update_result()

    def display_update_result(self):

        if not self.last_update_result:
            return
        version = self.last_update_result.get("version", "")
        if self.last_update_result.get("status") == "success":
            message = tr("update_successful").format(version=version)
            self.update_result_label.setText(
                f'<span style="color: #66bb6a; font-weight: bold;">{message}</span>'
            )
            if not self.update_result_logged:
                self.main_window.log(f"[INFO] {message}")
        else:
            message = tr("update_failed").format(version=version)
            self.update_result_label.setText(
                f'<span style="color: #ef5350; font-weight: bold;">{message}</span>'
            )
            if not self.update_result_logged:
                self.main_window.log(f"[ERROR] {message}")
        self.update_result_logged = True

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
