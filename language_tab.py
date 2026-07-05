from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QComboBox
)

from language import get_language, set_language, tr


class LanguageTab(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)

        self.language_label = QLabel()
        self.language_box = QComboBox()

        self.language_box.addItem("Deutsch", "de")
        self.language_box.addItem("English", "en")

        index = self.language_box.findData(get_language())
        if index >= 0:
            self.language_box.setCurrentIndex(index)

        self.language_box.currentIndexChanged.connect(
            self.change_language
        )

        layout.addWidget(self.language_label)
        layout.addWidget(self.language_box)
        layout.addStretch()

        self.update_language()

    def change_language(self):
        language = self.language_box.currentData()

        if not language or language == get_language():
            return

        set_language(language)
        self.main_window.update_language()
        self.main_window.log(
            f"[INFO] {tr('language_changed')}: {language}"
        )

    def update_language(self):
        self.language_label.setText(
            tr("language") + ":"
        )
