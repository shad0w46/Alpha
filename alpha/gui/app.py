import os
import re
import sys
import subprocess

from pathlib import Path

from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QMessageBox,
)


BASE_DIR = Path(__file__).resolve().parents[2]

LOGO_CANDIDATES = [
    BASE_DIR / "gui" / "assets" / "logo-no-background.png",
    Path.home() / "Projects/Alpha/Alpha_OS/alphaos-branding-main/assets/logo-no-background.png",
    Path.home() / "Projects/Alpha/Alpha_OS/config/includes.chroot/etc/calamares/branding/alphaos/logo-no-background.png",
]


class AlphaPopup(QWidget):
    def __init__(self, pet):
        super().__init__(
            None,
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.pet = pet

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(360, 250)

        self.build_ui()

    def build_ui(self):
        outer = QFrame(self)

        outer.setStyleSheet("""
            QFrame {
                background-color: #101722;
                border: 1px solid #285b91;
                border-radius: 18px;
            }

            QLabel {
                color: #e9f1fa;
                background: transparent;
                border: none;
            }

            QPushButton {
                background-color: #17283b;
                color: #edf5ff;
                border: none;
                border-radius: 8px;
                padding: 9px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #214263;
            }

            QPushButton:pressed {
                background-color: #102235;
            }

            QPushButton#primary {
                background-color: #1677e8;
            }

            QPushButton#primary:hover {
                background-color: #2588fa;
            }

            QPushButton#danger {
                background-color: #a52e32;
            }

            QPushButton#danger:hover {
                background-color: #c33b40;
            }
        """)

        layout = QVBoxLayout(outer)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        title = QLabel("Alpha")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
        """)

        subtitle = QLabel("What can I help you with?")
        subtitle.setStyleSheet("""
            color: #9eafc2;
            font-size: 13px;
        """)

        self.status = QLabel("Checking system status...")
        self.status.setStyleSheet("""
            color: #ffc43d;
            font-weight: 700;
            font-size: 14px;
        """)
        self.status.setWordWrap(True)

        self.details = QLabel("")
        self.details.setStyleSheet("""
            color: #aebed0;
            font-size: 12px;
        """)
        self.details.setWordWrap(True)

        self.scan_button = QPushButton("Scan")
        self.scan_button.clicked.connect(self.scan)

        self.updates_button = QPushButton("View Updates")
        self.updates_button.setObjectName("primary")
        self.updates_button.clicked.connect(self.view_updates)

        self.upgrade_button = QPushButton("Upgrade")
        self.upgrade_button.clicked.connect(self.upgrade)
        self.upgrade_button.hide()

        self.close_button = QPushButton("Close Alpha")
        self.close_button.setObjectName("danger")
        self.close_button.clicked.connect(self.close_alpha)

        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(self.scan_button)
        row.addWidget(self.updates_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(4)
        layout.addWidget(self.status)
        layout.addWidget(self.details)
        layout.addSpacing(3)
        layout.addLayout(row)
        layout.addWidget(self.upgrade_button)
        layout.addWidget(self.close_button)

        outer.setGeometry(0, 0, self.width(), self.height())

        self._outer = outer

    def show_at_pet(self):
        self.adjustSize()

        pet_pos = self.pet.mapToGlobal(QPoint(0, 0))
        pet_size = self.pet.size()

        popup_width = self.width()
        popup_height = self.height()

        screen = QApplication.screenAt(
            QPoint(
                pet_pos.x() + pet_size.width() // 2,
                pet_pos.y() + pet_size.height() // 2
            )
        )

        if screen is None:
            screen = QApplication.primaryScreen()

        available = screen.availableGeometry()

        # Prefer placing popup to the left of the pet.
        x = pet_pos.x() - popup_width - 10
        y = pet_pos.y() + pet_size.height() // 2 - popup_height // 2

        # If there isn't room on the left, put it to the right.
        if x < available.left():
            x = pet_pos.x() + pet_size.width() + 10

        # Keep inside the screen vertically.
        y = max(
            available.top() + 10,
            min(y, available.bottom() - popup_height - 10)
        )

        # Final horizontal clamp.
        x = max(
            available.left() + 10,
            min(x, available.right() - popup_width - 10)
        )

        self.move(x, y)
        self.show()
        self.raise_()

    def refresh_status(self, count=None, packages=None):
        if count is None:
            self.status.setText("Ready.")
            self.details.setText(
                "Click Scan to check for package updates."
            )
            self.upgrade_button.hide()
            return

        if count == 0:
            self.status.setText("✓ System is up to date")
            self.status.setStyleSheet("""
                color: #55d98a;
                font-weight: 700;
                font-size: 14px;
            """)
            self.details.setText(
                "No package updates are currently available."
            )
            self.upgrade_button.hide()
            return

        self.status.setText(
            f"● {count} package update{'s' if count != 1 else ''} available"
        )
        self.status.setStyleSheet("""
            color: #ffc43d;
            font-weight: 700;
            font-size: 14px;
        """)

        if packages:
            names = [p["name"] for p in packages[:5]]
            text = ", ".join(names)

            if count > 5:
                text += f" and {count - 5} more."

            self.details.setText(text)

        self.upgrade_button.show()

    def scan(self):
        self.status.setText("Scanning...")
        self.details.setText("Checking APT for available updates...")
        self.scan_button.setEnabled(False)
        self.updates_button.setEnabled(False)

        QApplication.processEvents()

        try:
            packages = self.get_upgradable_packages()

            self.pet.cached_updates = packages

            self.refresh_status(
                len(packages),
                packages
            )

        except Exception as exc:
            self.status.setText("Scan failed.")
            self.status.setStyleSheet("""
                color: #ff6268;
                font-weight: 700;
                font-size: 14px;
            """)

            self.details.setText(
                f"{type(exc).__name__}: {exc}"
            )

        finally:
            self.scan_button.setEnabled(True)
            self.updates_button.setEnabled(True)

    def view_updates(self):
        if not self.pet.cached_updates:
            self.scan()
            return

        packages = self.pet.cached_updates

        lines = []

        for package in packages[:8]:
            lines.append(
                f"• {package['name']}  "
                f"{package['installed']} → {package['available']}"
            )

        if len(packages) > 8:
            lines.append(
                f"\n...and {len(packages) - 8} more"
            )

        self.details.setText("\n".join(lines))
        self.adjustSize()
        self.show_at_pet()

    def upgrade(self):
        packages = self.pet.cached_updates

        if not packages:
            self.scan()
            return

        answer = QMessageBox.question(
            self,
            "Alpha",
            f"{len(packages)} package updates are available.\n\n"
            "Do you want Alpha to upgrade them?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        self.upgrade_button.setEnabled(False)
        self.scan_button.setEnabled(False)

        self.status.setText("Starting upgrade...")
        self.details.setText(
            "A system authentication window may appear."
        )

        QApplication.processEvents()

        try:
            command = [
                "pkexec",
                "apt-get",
                "upgrade",
                "-y",
            ]

            result = subprocess.run(
                command,
                text=True,
                capture_output=True
            )

            if result.returncode == 0:
                self.status.setText("✓ Upgrade completed")
                self.status.setStyleSheet("""
                    color: #55d98a;
                    font-weight: 700;
                    font-size: 14px;
                """)

                self.details.setText(
                    "Scanning again for remaining updates..."
                )

                QApplication.processEvents()

                self.pet.cached_updates = self.get_upgradable_packages()

                self.refresh_status(
                    len(self.pet.cached_updates),
                    self.pet.cached_updates
                )

            else:
                error = result.stderr.strip()

                if not error:
                    error = result.stdout.strip()

                self.status.setText("Upgrade failed.")
                self.status.setStyleSheet("""
                    color: #ff6268;
                    font-weight: 700;
                    font-size: 14px;
                """)

                self.details.setText(
                    error[-500:] if error else "APT returned an error."
                )

        except Exception as exc:
            self.status.setText("Upgrade failed.")
            self.details.setText(
                f"{type(exc).__name__}: {exc}"
            )

        finally:
            self.upgrade_button.setEnabled(True)
            self.scan_button.setEnabled(True)

    def get_upgradable_packages(self):
        result = subprocess.run(
            [
                "apt",
                "list",
                "--upgradable"
            ],
            text=True,
            capture_output=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip() or "APT command failed"
            )

        packages = []

        for raw_line in result.stdout.splitlines():
            line = raw_line.strip()

            if not line:
                continue

            if line.startswith("Listing..."):
                continue

            match = re.match(
                r"^([^/]+)/\S+\s+(\S+).*?\[upgradable from:\s*(.*?)\]",
                line
            )

            if not match:
                continue

            name = match.group(1)
            available = match.group(2)
            installed = match.group(3)

            packages.append({
                "name": name,
                "installed": installed,
                "available": available,
            })

        return packages

    def close_alpha(self):
        self.pet.close()
        self.close()

        QApplication.quit()

    def showEvent(self, event):
        super().showEvent(event)

        QTimer.singleShot(
            50,
            self.show_at_pet
        )


class AlphaPet(QWidget):
    def __init__(self):
        super().__init__()

        self.cached_updates = []

        self.dragging = False
        self.drag_start_position = QPoint()
        self.window_start_position = QPoint()

        self.popup = AlphaPopup(self)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_ShowWithoutActivating
        )

        self.setFixedSize(96, 96)

        self.build_pet()

        self.move_to_default_position()

        # Keep popup attached to pet while visible.
        self.position_timer = QTimer(self)
        self.position_timer.timeout.connect(self.follow_popup)
        self.position_timer.start(100)

    def build_pet(self):
        self.logo = QLabel(self)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_path = None

        for candidate in LOGO_CANDIDATES:
            if candidate.exists():
                logo_path = candidate
                break

        if logo_path is None:
            self.logo.setText("A")
            self.logo.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 48px;
                    font-weight: 800;
                }
            """)
        else:
            pixmap = QPixmap(str(logo_path))

            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    88,
                    88,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )

                self.logo.setPixmap(pixmap)

        self.logo.setGeometry(
            4,
            4,
            88,
            88
        )

        # The QLabel must not steal mouse events.
        self.logo.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

    def move_to_default_position(self):
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()

        self.move(
            geometry.right() - self.width() - 25,
            geometry.center().y() - self.height() // 2
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPosition().toPoint()
            self.window_start_position = self.pos()
            self.dragging = False

            event.accept()
            return

        if event.button() == Qt.MouseButton.RightButton:
            self.popup.show_at_pet()
            event.accept()
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (
            event.buttons() &
            Qt.MouseButton.LeftButton
        ):
            return

        current = event.globalPosition().toPoint()

        delta = current - self.drag_start_position

        # Small movement = still a click.
        if delta.manhattanLength() < 8:
            return

        self.dragging = True

        self.move(
            self.window_start_position + delta
        )

        if self.popup.isVisible():
            self.popup.show_at_pet()

        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:

            if not self.dragging:
                self.popup.show_at_pet()

            self.dragging = False

            event.accept()
            return

        super().mouseReleaseEvent(event)

    def follow_popup(self):
        if self.popup.isVisible():
            self.popup.show_at_pet()

    def enterEvent(self, event):
        self.setWindowOpacity(1.0)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setWindowOpacity(0.96)
        super().leaveEvent(event)


class AlphaApplication:
    def __init__(self):
        self.qt_app = QApplication.instance()

        if self.qt_app is None:
            self.qt_app = QApplication(sys.argv)

        self.qt_app.setApplicationName("Alpha")
        self.qt_app.setApplicationDisplayName("Alpha")

        self.pet = AlphaPet()

        self.pet.show()

        # Initial status without breaking startup.
        QTimer.singleShot(
            500,
            self.initial_scan
        )

    def initial_scan(self):
        if self.pet.popup.isVisible():
            self.pet.popup.scan()
        else:
            self.pet.popup.refresh_status()

    def run(self):
        return self.qt_app.exec()
