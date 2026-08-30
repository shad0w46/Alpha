from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtWidgets import QWidget


class AlphaPet(QWidget):
    clicked = Signal()
    moved = Signal()

    def __init__(self, parent=None, image_path=None):
        super().__init__(parent)

        # ---------------------------------------------------------
        # WINDOW
        # ---------------------------------------------------------

        self.setFixedSize(96, 96)

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.Tool
            | Qt.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground,
            True,
        )

        self.setAttribute(
            Qt.WA_NoSystemBackground,
            True,
        )

        self.setMouseTracking(True)

        self.setCursor(Qt.OpenHandCursor)

        # ---------------------------------------------------------
        # LOGO
        # ---------------------------------------------------------

        self.pixmap = QPixmap()

        if image_path:
            print(
                f"[PET] Loading logo: {image_path}",
                flush=True,
            )

            self.pixmap = QPixmap(image_path)

            if self.pixmap.isNull():
                print(
                    "[PET] ERROR: Could not load logo",
                    flush=True,
                )
            else:
                print(
                    "[PET] Logo loaded "
                    f"{self.pixmap.width()}x"
                    f"{self.pixmap.height()}",
                    flush=True,
                )

                self.pixmap = self.pixmap.scaled(
                    88,
                    88,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )

        # ---------------------------------------------------------
        # CLICK / DRAG STATE
        # ---------------------------------------------------------

        self.mouse_down = False
        self.dragging = False

        self.press_global = QPoint()
        self.press_local = QPoint()

        print(
            "[PET] AlphaPet created",
            flush=True,
        )

    # =============================================================
    # PAINT
    # =============================================================

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing,
            True,
        )

        painter.setRenderHint(
            QPainter.SmoothPixmapTransform,
            True,
        )

        # Completely transparent background.
        # Only the actual PNG is drawn.
        if not self.pixmap.isNull():

            x = (
                self.width()
                - self.pixmap.width()
            ) // 2

            y = (
                self.height()
                - self.pixmap.height()
            ) // 2

            painter.drawPixmap(
                x,
                y,
                self.pixmap,
            )

        painter.end()

    # =============================================================
    # MOUSE PRESS
    # =============================================================

    def mousePressEvent(self, event):

        print(
            "[PET] PRESS",
            f"button={event.button()}",
            f"global={event.globalPosition().toPoint()}",
            f"local={event.position().toPoint()}",
            flush=True,
        )

        if event.button() == Qt.LeftButton:

            self.mouse_down = True
            self.dragging = False

            self.press_global = (
                event.globalPosition().toPoint()
            )

            self.press_local = (
                event.position().toPoint()
            )

            self.setCursor(
                Qt.ClosedHandCursor
            )

            print(
                "[PET] LEFT BUTTON DOWN",
                flush=True,
            )

            event.accept()
            return

        super().mousePressEvent(event)

    # =============================================================
    # MOUSE MOVE
    # =============================================================

    def mouseMoveEvent(self, event):

        if not self.mouse_down:
            return

        current_global = (
            event.globalPosition().toPoint()
        )

        delta = (
            current_global
            - self.press_global
        )

        print(
            "[PET] MOVE",
            f"global={current_global}",
            f"delta={delta}",
            flush=True,
        )

        # ---------------------------------------------------------
        # DON'T START DRAGGING FOR A SIMPLE CLICK
        # ---------------------------------------------------------

        if not self.dragging:

            if delta.manhattanLength() < 8:

                print(
                    "[PET] movement below threshold",
                    flush=True,
                )

                event.accept()
                return

            print(
                "[PET] >>> STARTING NATIVE WINDOW MOVE <<<",
                flush=True,
            )

            self.dragging = True

            # -----------------------------------------------------
            # WAYLAND FIX
            #
            # DO NOT USE:
            #
            # self.move(...)
            #
            # Wayland does not allow an application to arbitrarily
            # reposition a top-level window.
            #
            # startSystemMove() asks the compositor to perform the
            # actual window movement.
            # -----------------------------------------------------

            window = self.windowHandle()

            if window is not None:

                try:

                    started = (
                        window.startSystemMove()
                    )

                    print(
                        "[PET] startSystemMove:",
                        started,
                        flush=True,
                    )

                except Exception as exc:

                    print(
                        "[PET] startSystemMove ERROR:",
                        repr(exc),
                        flush=True,
                    )

            else:

                print(
                    "[PET] ERROR: No QWindow handle",
                    flush=True,
                )

            event.accept()
            return

        event.accept()

    # =============================================================
    # MOUSE RELEASE
    # =============================================================

    def mouseReleaseEvent(self, event):

        print(
            "[PET] RELEASE",
            f"button={event.button()}",
            f"global={event.globalPosition().toPoint()}",
            f"dragging={self.dragging}",
            flush=True,
        )

        if event.button() == Qt.LeftButton:

            was_dragging = self.dragging

            self.mouse_down = False
            self.dragging = False

            self.setCursor(
                Qt.OpenHandCursor
            )

            # -----------------------------------------------------
            # DRAG FINISHED
            # -----------------------------------------------------

            if was_dragging:

                print(
                    "[PET] DRAG COMPLETE",
                    f"position={self.pos()}",
                    flush=True,
                )

                self.moved.emit()

            # -----------------------------------------------------
            # NORMAL CLICK
            # -----------------------------------------------------

            else:

                print(
                    "[PET] CLICK detected",
                    flush=True,
                )

                self.clicked.emit()

            event.accept()
            return

        super().mouseReleaseEvent(event)

    # =============================================================
    # MOVE EVENT
    # =============================================================

    def moveEvent(self, event):

        position = self.pos()

        print(
            "[PET] WINDOW MOVE",
            f"position={position}",
            flush=True,
        )

        self.moved.emit()

        super().moveEvent(event)

    # =============================================================
    # ENTER
    # =============================================================

    def enterEvent(self, event):

        print(
            "[PET] Mouse ENTER",
            flush=True,
        )

        super().enterEvent(event)

    # =============================================================
    # LEAVE
    # =============================================================

    def leaveEvent(self, event):

        print(
            "[PET] Mouse LEAVE",
            flush=True,
        )

        super().leaveEvent(event)