from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFrame,
)


class AlphaMenu(QWidget):

    scan_requested = Signal()
    quit_requested = Signal()

    def __init__(self, parent=None):

        super().__init__(
            parent,
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool,
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground,
            True,
        )

        self.setFixedSize(
            190,
            125,
        )

        self._build()

    def _build(self):

        frame = QFrame(self)

        frame.setObjectName(
            "menu"
        )

        frame.setGeometry(
            3,
            3,
            184,
            119,
        )

        frame.setStyleSheet(
            """
            QFrame#menu {
                background: #07111f;
                border: 1px solid #245b91;
                border-radius: 12px;
            }

            QLabel {
                background: transparent;
                color: white;
            }

            QLabel#title {
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton {
                background: #14283d;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 7px;
                text-align: left;
                font-size: 12px;
            }

            QPushButton:hover {
                background: #1d4265;
            }

            QPushButton#quit {
                color: #ff6b6b;
            }

            QPushButton#quit:hover {
                background: #4a2025;
            }
            """
        )

        layout = QVBoxLayout(frame)

        layout.setContentsMargins(
            10,
            8,
            10,
            8,
        )

        layout.setSpacing(
            5
        )

        title = QLabel(
            "Alpha"
        )

        title.setObjectName(
            "title"
        )

        layout.addWidget(
            title
        )

        scan = QPushButton(
            "⟳  Scan System"
        )

        scan.clicked.connect(
            self._scan
        )

        layout.addWidget(
            scan
        )

        quit_button = QPushButton(
            "✕  Quit Alpha"
        )

        quit_button.setObjectName(
            "quit"
        )

        quit_button.clicked.connect(
            self._quit
        )

        layout.addWidget(
            quit_button
        )

    def _scan(self):

        self.scan_requested.emit()

        self.close()

    def _quit(self):

        self.quit_requested.emit()

        self.close()
