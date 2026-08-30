from pathlib import Path

from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel


class AlphaPet(QWidget):

    clicked = Signal()
    position_changed = Signal()

    def __init__(self):
        super().__init__()

        self.dragging = False
        self.drag_position = QPoint()

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground,
            True
        )

        self.setFixedSize(96, 96)

        self.logo = QLabel(self)

        self.logo.setAlignment(
            Qt.AlignCenter
        )

        self.logo.setAttribute(
            Qt.WA_TransparentForMouseEvents,
            True
        )

        self.logo.setGeometry(
            0,
            0,
            96,
            96
        )

        project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        logo_path = (
            project_root
            / "alphaos-branding-main"
            / "assets"
            / "logo-no-background.png"
        )

        # Fallback for an installed/build-tree copy.
        if not logo_path.exists():

            fallback_paths = [

                Path(
                    "/etc/calamares/branding/alphaos/logo-no-background.png"
                ),

                project_root
                / "Alpha_OS"
                / "alphaos-branding-main"
                / "assets"
                / "logo-no-background.png",

            ]

            for fallback in fallback_paths:

                if fallback.exists():

                    logo_path = fallback
                    break

        pixmap = QPixmap(
            str(logo_path)
        )

        if not pixmap.isNull():

            self.logo.setPixmap(
                pixmap.scaled(
                    88,
                    88,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

        self.setCursor(
            Qt.PointingHandCursor
        )

    # ======================================================
    # MOUSE PRESS
    # ======================================================

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            self.dragging = False

            event.accept()

            return

        event.ignore()

    # ======================================================
    # MOUSE MOVE
    # ======================================================

    def mouseMoveEvent(self, event):

        if (
            event.buttons()
            & Qt.LeftButton
        ):

            current_position = (
                event.globalPosition().toPoint()
            )

            new_position = (
                current_position
                - self.drag_position
            )

            # Only consider this a drag after
            # the pointer actually moved.
            if (
                new_position
                != self.pos()
            ):

                self.dragging = True

                self.move(
                    new_position
                )

                self.position_changed.emit()

            event.accept()

            return

        event.ignore()

    # ======================================================
    # MOUSE RELEASE
    # ======================================================

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:

            was_dragging = (
                self.dragging
            )

            self.dragging = False

            # A click is generated only when the
            # user didn't actually move the pet.
            if not was_dragging:

                self.clicked.emit()

            event.accept()

            return

        event.ignore()
