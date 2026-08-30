from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QScrollArea,
)


class AlphaPopup(QWidget):

    scan_requested = Signal()
    view_updates_requested = Signal()
    close_requested = Signal()

    def __init__(
        self,
        updates=0,
        installed_count=0
    ):

        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground,
            True
        )

        self.setFixedWidth(
            330
        )

        self.build_ui()

        self.set_scan_finished({
            "update_count": updates,
            "installed_count": installed_count,
            "updates": {}
        })

    # ======================================================
    # UI
    # ======================================================

    def build_ui(self):

        outer = QVBoxLayout(
            self
        )

        outer.setContentsMargins(
            10,
            10,
            10,
            10
        )

        outer.setSpacing(
            0
        )

        self.card = QFrame()

        self.card.setObjectName(
            "card"
        )

        self.card.setStyleSheet("""
            QFrame#card {
                background: rgba(25, 28, 34, 245);
                border: 1px solid rgba(255, 255, 255, 35);
                border-radius: 16px;
            }

            QLabel {
                color: white;
            }

            QLabel#title {
                font-size: 20px;
                font-weight: bold;
            }

            QLabel#status {
                color: #c8ccd4;
                font-size: 13px;
            }

            QLabel#count {
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton {
                background: rgba(255, 255, 255, 18);
                color: white;
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 9px;
                padding: 8px 12px;
            }

            QPushButton:hover {
                background: rgba(255, 255, 255, 30);
            }

            QPushButton:pressed {
                background: rgba(255, 255, 255, 45);
            }

            QPushButton#close {
                background: rgba(180, 50, 50, 180);
            }

            QPushButton#close:hover {
                background: rgba(210, 60, 60, 220);
            }
        """)

        outer.addWidget(
            self.card
        )

        layout = QVBoxLayout(
            self.card
        )

        layout.setContentsMargins(
            16,
            14,
            16,
            14
        )

        layout.setSpacing(
            9
        )

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        self.title = QLabel(
            "Alpha"
        )

        self.title.setObjectName(
            "title"
        )

        layout.addWidget(
            self.title
        )

        self.status = QLabel(
            "Checking your system..."
        )

        self.status.setObjectName(
            "status"
        )

        self.status.setWordWrap(
            True
        )

        layout.addWidget(
            self.status
        )

        # --------------------------------------------------
        # COUNT
        # --------------------------------------------------

        self.count = QLabel(
            ""
        )

        self.count.setObjectName(
            "count"
        )

        layout.addWidget(
            self.count
        )

        # --------------------------------------------------
        # UPDATE LIST
        # --------------------------------------------------

        self.updates_area = QScrollArea()

        self.updates_area.setWidgetResizable(
            True
        )

        self.updates_area.setMaximumHeight(
            150
        )

        self.updates_area.setVisible(
            False
        )

        self.updates_container = QWidget()

        self.updates_layout = QVBoxLayout(
            self.updates_container
        )

        self.updates_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.updates_layout.setSpacing(
            4
        )

        self.updates_area.setWidget(
            self.updates_container
        )

        layout.addWidget(
            self.updates_area
        )

        # --------------------------------------------------
        # BUTTONS
        # --------------------------------------------------

        buttons = QHBoxLayout()

        self.scan_button = QPushButton(
            "Scan"
        )

        self.scan_button.clicked.connect(
            self.scan_requested.emit
        )

        self.updates_button = QPushButton(
            "View Updates"
        )

        self.updates_button.clicked.connect(
            self.view_updates_requested.emit
        )

        buttons.addWidget(
            self.scan_button
        )

        buttons.addWidget(
            self.updates_button
        )

        layout.addLayout(
            buttons
        )

        # --------------------------------------------------
        # CLOSE
        # --------------------------------------------------

        self.close_button = QPushButton(
            "Close Alpha"
        )

        self.close_button.setObjectName(
            "close"
        )

        self.close_button.clicked.connect(
            self.close_requested.emit
        )

        layout.addWidget(
            self.close_button
        )

    # ======================================================
    # SCANNING
    # ======================================================

    def set_scanning(self):

        self.status.setText(
            "Scanning packages..."
        )

        self.count.setText(
            "Please wait..."
        )

        self.scan_button.setEnabled(
            False
        )

    # ======================================================
    # SCAN COMPLETE
    # ======================================================

    def set_scan_finished(
        self,
        result
    ):

        self.scan_button.setEnabled(
            True
        )

        if not result:

            self.status.setText(
                "Scan failed."
            )

            self.count.setText(
                ""
            )

            return

        updates = result.get(
            "updates",
            {}
        )

        count = result.get(
            "update_count",
            len(updates)
        )

        installed = result.get(
            "installed_count",
            0
        )

        if count == 0:

            self.status.setText(
                "Your system is up to date."
            )

            self.count.setText(
                f"{installed:,} packages checked"
            )

        else:

            self.status.setText(
                "Updates are available."
            )

            self.count.setText(
                f"{count} update(s) • "
                f"{installed:,} packages checked"
            )

        self.populate_updates(
            updates
        )

    # ======================================================
    # UPDATE LIST
    # ======================================================

    def populate_updates(
        self,
        updates
    ):

        while (
            self.updates_layout.count()
        ):

            item = (
                self.updates_layout.takeAt(
                    0
                )
            )

            widget = item.widget()

            if widget:

                widget.deleteLater()

        # Show only a compact preview.
        items = list(
            updates.items()
        )[:5]

        for package, info in items:

            installed = info.get(
                "installed",
                "?"
            )

            available = info.get(
                "available",
                "?"
            )

            importance = info.get(
                "importance",
                {}
            )

            level = importance.get(
                "level",
                ""
            )

            text = (
                f"{package}\n"
                f"{installed} → {available}"
            )

            if level:

                text += (
                    f"  [{level}]"
                )

            label = QLabel(
                text
            )

            label.setWordWrap(
                True
            )

            label.setStyleSheet("""
                QLabel {
                    background: rgba(255,255,255,12);
                    border-radius: 7px;
                    padding: 6px;
                    color: #eeeeee;
                    font-size: 11px;
                }
            """)

            self.updates_layout.addWidget(
                label
            )

        if updates:

            self.updates_layout.addStretch()

    # ======================================================
    # SHOW UPDATES
    # ======================================================

    def show_updates(
        self,
        updates
    ):

        self.populate_updates(
            updates
        )

        self.updates_area.setVisible(
            bool(updates)
        )

        if updates:

            self.status.setText(
                f"{len(updates)} package update(s) available."
            )

        else:

            self.status.setText(
                "No package updates available."
            )

        self.adjustSize()
