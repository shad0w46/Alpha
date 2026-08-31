from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtWidgets import (
    QWidget,
    QMenu,
    QApplication,
)


class AlphaPet(QWidget):
    clicked = Signal()
    moved = Signal()

    def __init__(self, parent=None, image_path=None):
        super().__init__(parent)

        # =========================================================
        # WINDOW IDENTITY
        # =========================================================

        self.setObjectName("AlphaPet")
        self.setWindowTitle("AlphaPet")

        # =========================================================
        # WINDOW
        # =========================================================

        self.setFixedSize(96, 96)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowDoesNotAcceptFocus
        )

        # =========================================================
        # TRANSPARENT PET
        # =========================================================

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground,
            True,
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_NoSystemBackground,
            True,
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_ShowWithoutActivating,
            True,
        )

        # =========================================================
        # MOUSE
        # =========================================================

        self.setMouseTracking(True)

        self.setCursor(
            Qt.CursorShape.OpenHandCursor
        )

        # =========================================================
        # LOGO
        # =========================================================

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
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

        # =========================================================
        # CLICK / DRAG STATE
        # =========================================================

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
            QPainter.RenderHint.Antialiasing,
            True,
        )

        painter.setRenderHint(
            QPainter.RenderHint.SmoothPixmapTransform,
            True,
        )

        # ---------------------------------------------------------
        # COMPLETELY TRANSPARENT BACKGROUND
        # ---------------------------------------------------------

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
    # RIGHT CLICK MENU
    # =============================================================

    def show_context_menu(self, global_position):

        print(
            "[PET] Right-click menu",
            flush=True,
        )

        menu = QMenu()

        # ---------------------------------------------------------
        # MENU STYLE
        # ---------------------------------------------------------

        menu.setWindowFlag(
            Qt.WindowType.FramelessWindowHint,
            True,
        )

        menu.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground,
            True,
        )

        # ---------------------------------------------------------
        # ACTIONS
        # ---------------------------------------------------------

        close_action = menu.addAction(
            "Close Alpha Assistant"
        )

        # ---------------------------------------------------------
        # SHOW MENU
        # ---------------------------------------------------------

        action = menu.exec(
            global_position
        )

        # ---------------------------------------------------------
        # CLOSE ALPHA
        # ---------------------------------------------------------

        if action == close_action:

            print(
                "[PET] Closing Alpha Assistant",
                flush=True,
            )

            QApplication.quit()

    # =============================================================
    # MOUSE PRESS
    # =============================================================

    def mousePressEvent(self, event):

        button = event.button()

        global_position = (
            event.globalPosition().toPoint()
        )

        local_position = (
            event.position().toPoint()
        )

        print(
            "[PET] PRESS",
            f"button={button}",
            f"global={global_position}",
            f"local={local_position}",
            flush=True,
        )

        # ---------------------------------------------------------
        # RIGHT CLICK
        # ---------------------------------------------------------

        if button == Qt.MouseButton.RightButton:

            self.show_context_menu(
                global_position
            )

            event.accept()

            return

        # ---------------------------------------------------------
        # LEFT CLICK
        # ---------------------------------------------------------

        if button == Qt.MouseButton.LeftButton:

            self.mouse_down = True
            self.dragging = False

            self.press_global = (
                global_position
            )

            self.press_local = (
                local_position
            )

            self.setCursor(
                Qt.CursorShape.ClosedHandCursor
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

        # ---------------------------------------------------------
        # DRAG THRESHOLD
        # ---------------------------------------------------------

        if not self.dragging:

            if delta.manhattanLength() < 8:

                event.accept()

                return

            print(
                "[PET] >>> STARTING WINDOW MOVE <<<",
                flush=True,
            )

            self.dragging = True

            # -----------------------------------------------------
            # WAYLAND
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

        if event.button() == Qt.MouseButton.LeftButton:

            was_dragging = self.dragging

            self.mouse_down = False
            self.dragging = False

            self.setCursor(
                Qt.CursorShape.OpenHandCursor
            )

            # -----------------------------------------------------
            # DRAG
            # -----------------------------------------------------

            if was_dragging:

                print(
                    "[PET] DRAG COMPLETE",
                    f"position={self.pos()}",
                    flush=True,
                )

                self.moved.emit()

            # -----------------------------------------------------
            # CLICK
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