from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)


class AlphaPopup(QWidget):
    def __init__(self, application, parent=None):
        super().__init__(parent)

        self.application = application

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.Tool
            | Qt.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.setFixedSize(310, 320)

        self.build_ui()

    def build_ui(self):
        self.frame = QFrame(self)

        self.frame.setGeometry(0, 0, 310, 320)

        self.frame.setStyleSheet("""
            QFrame {
                background: #101722;
                border: 1px solid #2585e8;
                border-radius: 16px;
            }

            QLabel {
                color: #e8edf5;
                background: transparent;
                border: none;
            }

            QPushButton {
                background: #18304a;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 9px;
                font-weight: 600;
            }

            QPushButton:hover {
                background: #24639a;
            }

            QPushButton:pressed {
                background: #0f2439;
            }

            QPushButton#updates {
                background: #1877e8;
            }

            QPushButton#updates:hover {
                background: #2587f5;
            }

            QPushButton#close {
                background: #a52f34;
            }

            QPushButton#close:hover {
                background: #c33a40;
            }
            QPushButton#exit {
                background: #a52f34;
            }
            
            QPushButton#exit:hover {
                background: #c33a40;
            }
        """)

        layout = QVBoxLayout(self.frame)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        title = QLabel("Alpha")

        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)

        layout.addWidget(title)

        self.subtitle = QLabel("What can I help you with?")
        self.subtitle.setStyleSheet(
            "color: #aab7c7; font-size: 12px;"
        )

        layout.addWidget(self.subtitle)

        self.status = QLabel("Checking package updates...")
        self.status.setStyleSheet(
            "color: #ffc533; font-weight: bold;"
        )

        layout.addWidget(self.status)

        self.package_info = QLabel("")
        self.package_info.setWordWrap(True)

        self.package_info.setStyleSheet("""
            color: #9eacbd;
            font-size: 11px;
        """)

        layout.addWidget(self.package_info)

        self.scan_button = QPushButton("Scan")
        self.scan_button.clicked.connect(
            self.application.scan
        )

        layout.addWidget(self.scan_button)

        self.updates_button = QPushButton("View Updates")
        self.updates_button.setObjectName("updates")

        self.updates_button.clicked.connect(
            self.application.show_updates
        )

        layout.addWidget(self.updates_button)

        self.upgrade_button = QPushButton("Upgrade")

        self.upgrade_button.clicked.connect(
            self.application.upgrade
        )

        layout.addWidget(self.upgrade_button)

        self.close_button = QPushButton("Close")
        self.close_button.setObjectName("close")

        self.close_button.clicked.connect(
            self.hide
        )

        layout.addWidget(self.close_button)
        self.exit_button = QPushButton("Exit")
        self.exit_button.setObjectName("exit")
        
        self.exit_button.clicked.connect(
            self.application.quit
        )
        
        layout.addWidget(self.exit_button)

    def set_status(self, text):
        self.status.setText(text)

    def set_packages(self, packages):
        if not packages:
            self.package_info.setText(
                "Your system is up to date."
            )
            return

        lines = []

        for package in packages[:4]:
            name = package.get("name", "")
            installed = package.get("installed", "")
            available = package.get("available", "")

            if available:
                lines.append(
                    f"{name}\n"
                    f"  {installed} → {available}"
                )
            else:
                lines.append(name)

        if len(packages) > 4:
            lines.append(
                f"... and {len(packages) - 4} more"
            )

        self.package_info.setText(
            "\n".join(lines)
        )

    def show_at_pet(self):
        pet = self.application.pet

        if pet is None:
            return

        pet_global = pet.mapToGlobal(
            QPoint(0, 0)
        )

        screen = pet.screen()

        if screen is None:
            self.move(
                pet_global.x() - self.width() - 8,
                pet_global.y(),
            )
            return

        available = screen.availableGeometry()

        # Prefer popup to the left of the pet.
        x = pet_global.x() - self.width() - 10

        # If there isn't enough room on the left,
        # put it to the right.
        if x < available.left():
            x = (
                pet_global.x()
                + pet.width()
                + 10
            )

        # Keep popup inside the desktop.
        x = max(
            available.left(),
            min(
                x,
                available.right() - self.width() + 1,
            ),
        )

        y = pet_global.y()

        y = max(
            available.top(),
            min(
                y,
                available.bottom() - self.height() + 1,
            ),
        )

        self.move(x, y)

    def showEvent(self, event):
        self.show_at_pet()
        super().showEvent(event)
