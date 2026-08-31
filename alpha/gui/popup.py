from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QSizePolicy,
)

from alpha.core.process_monitor import ProcessMonitor

class AlphaPopup(QWidget):

    def __init__(self, application, parent=None):
        super().__init__(parent)

        self.application = application

        # =========================================================
        # WINDOW
        # =========================================================

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground,
            True,
        )

        # Minimum size instead of fixed size.
        self.setMinimumWidth(310)
        self.setMaximumWidth(420)

        self.setMinimumHeight(180)

        # Let Qt calculate the height.
        self.adjustSize()

        # =========================================================
        # PROCESS MONITOR
        # =========================================================

        self.monitor_timer = QTimer(self)

        self.monitor_timer.timeout.connect(
            self.update_process_monitor
        )

        self.monitor_timer.start(2000)

        # =========================================================
        # BUILD
        # =========================================================

        self.build_ui()

    # =============================================================
    # BUILD UI
    # =============================================================

    def build_ui(self):

        # =========================================================
        # OUTER LAYOUT
        # =========================================================

        outer_layout = QVBoxLayout(self)

        outer_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        # =========================================================
        # FRAME
        # =========================================================

        self.frame = QFrame()

        self.frame.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

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
                padding: 9px 12px;
                font-weight: 600;
                min-height: 18px;
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

            QPushButton#back {
                background: #263342;
            }

            QPushButton#back:hover {
                background: #35475b;
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

        outer_layout.addWidget(
            self.frame
        )

        # =========================================================
        # FRAME LAYOUT
        # =========================================================

        self.layout = QVBoxLayout(
            self.frame
        )

        self.layout.setContentsMargins(
            16,
            14,
            16,
            14,
        )

        self.layout.setSpacing(8)

        # =========================================================
        # TITLE
        # =========================================================

        self.title = QLabel(
            "Alpha"
        )

        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)

        self.title.setFont(
            title_font
        )

        self.title.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        self.layout.addWidget(
            self.title
        )

        # =========================================================
        # SUBTITLE
        # =========================================================

        self.subtitle = QLabel(
            "What can I help you with?"
        )

        self.subtitle.setWordWrap(
            True
        )

        self.subtitle.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        self.subtitle.setStyleSheet(
            "color: #aab7c7; font-size: 12px;"
        )

        self.layout.addWidget(
            self.subtitle
        )

        # =========================================================
        # STATUS
        # =========================================================

        self.status = QLabel(
            "Checking package updates..."
        )

        self.status.setWordWrap(
            True
        )

        self.status.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        self.status.setStyleSheet(
            "color: #ffc533; font-weight: bold;"
        )

        self.layout.addWidget(
            self.status
        )

        # =========================================================
        # PACKAGE INFORMATION
        # =========================================================

        self.package_info = QLabel(
            ""
        )

        self.package_info.setWordWrap(
            True
        )

        self.package_info.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        self.package_info.setStyleSheet("""
            color: #9eacbd;
            font-size: 11px;
        """)

        self.layout.addWidget(
            self.package_info
        )

        # =========================================================
        # MAIN PAGE
        # =========================================================

        self.main_page = QWidget()

        self.main_page.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        self.main_layout = QVBoxLayout(
            self.main_page
        )

        self.main_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.main_layout.setSpacing(
            8
        )

        # ---------------------------------------------------------
        # UPDATE
        # ---------------------------------------------------------

        self.update_button = QPushButton(
            "Update"
        )

        self.update_button.setObjectName(
            "updates"
        )

        self.main_layout.addWidget(
            self.update_button
        )

        self.update_button.clicked.connect(
            self.show_update_page
        )

        # ---------------------------------------------------------
        # PROCESS MONITOR
        # ---------------------------------------------------------

        self.process_button = QPushButton(
            "Process Monitor"
        )

        self.main_layout.addWidget(
            self.process_button
        )

        self.process_button.clicked.connect(
            self.show_process_page
        )

        # ---------------------------------------------------------
        # CLOSE
        # ---------------------------------------------------------

        self.close_button = QPushButton(
            "Close"
        )

        self.close_button.setObjectName(
            "close"
        )

        self.close_button.clicked.connect(
            self.hide
        )

        self.main_layout.addWidget(
            self.close_button
        )

        # ---------------------------------------------------------
        # EXIT
        # ---------------------------------------------------------

        self.exit_button = QPushButton(
            "Exit"
        )

        self.exit_button.setObjectName(
            "exit"
        )

        self.exit_button.clicked.connect(
            self.application.quit
        )

        self.main_layout.addWidget(
            self.exit_button
        )

        self.layout.addWidget(
            self.main_page
        )

        # =========================================================
        # UPDATE PAGE
        # =========================================================

        self.update_page = QWidget()

        self.update_layout = QVBoxLayout(
            self.update_page
        )

        self.update_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.update_layout.setSpacing(
            8
        )

        # ---------------------------------------------------------
        # SCAN
        # ---------------------------------------------------------

        self.scan_button = QPushButton(
            "Scan"
        )

        self.scan_button.clicked.connect(
            self.application.scan
        )

        self.update_layout.addWidget(
            self.scan_button
        )

        # ---------------------------------------------------------
        # UPDATE
        # ---------------------------------------------------------

        self.view_updates_button = QPushButton(
            "Update"
        )

        self.view_updates_button.setObjectName(
            "updates"
        )

        self.view_updates_button.clicked.connect(
            self.application.show_updates
        )

        self.update_layout.addWidget(
            self.view_updates_button
        )

        # ---------------------------------------------------------
        # UPGRADE
        # ---------------------------------------------------------

        self.upgrade_button = QPushButton(
            "Upgrade"
        )

        self.upgrade_button.clicked.connect(
            self.application.upgrade
        )

        self.update_layout.addWidget(
            self.upgrade_button
        )

        # ---------------------------------------------------------
        # BACK
        # ---------------------------------------------------------

        self.update_back_button = QPushButton(
            "← Back"
        )

        self.update_back_button.setObjectName(
            "back"
        )

        self.update_back_button.clicked.connect(
            self.show_main_page
        )

        self.update_layout.addWidget(
            self.update_back_button
        )

        self.layout.addWidget(
            self.update_page
        )

        # =========================================================
        # PROCESS PAGE
        # =========================================================

        self.process_page = QWidget()

        self.process_layout = QVBoxLayout(
            self.process_page
        )

        self.process_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.process_layout.setSpacing(
            6
        )

        # ---------------------------------------------------------
        # RESOURCE TITLE
        # ---------------------------------------------------------

        self.resource_title = QLabel(
            "System Resources"
        )

        self.resource_title.setStyleSheet(
            "color: #2585e8; "
            "font-weight: bold;"
        )

        self.process_layout.addWidget(
            self.resource_title
        )

        # ---------------------------------------------------------
        # RESOURCE INFO
        # ---------------------------------------------------------

        self.system_info = QLabel(
            "CPU: --\n"
            "RAM: --\n"
            "Load: --"
        )

        self.system_info.setWordWrap(
            True
        )

        self.process_layout.addWidget(
            self.system_info
        )

        # ---------------------------------------------------------
        # CPU TITLE
        # ---------------------------------------------------------

        self.cpu_title = QLabel(
            "Top 5 CPU"
        )

        self.cpu_title.setStyleSheet(
            "color: #2585e8; "
            "font-weight: bold;"
        )

        self.process_layout.addWidget(
            self.cpu_title
        )

        # ---------------------------------------------------------
        # CPU PROCESSES
        # ---------------------------------------------------------

        self.cpu_processes = QLabel(
            "Loading..."
        )

        self.cpu_processes.setWordWrap(
            False
        )

        self.cpu_processes.setTextInteractionFlags(
            Qt.TextInteractionFlag.NoTextInteraction
        )

        self.cpu_processes.setStyleSheet("""
            color: #9eacbd;
            font-size: 11px;
            font-family: monospace;
        """)

        self.process_layout.addWidget(
            self.cpu_processes
        )

        # ---------------------------------------------------------
        # MEMORY TITLE
        # ---------------------------------------------------------

        self.memory_title = QLabel(
            "Top 5 Memory"
        )

        self.memory_title.setStyleSheet(
            "color: #2585e8; "
            "font-weight: bold;"
        )

        self.process_layout.addWidget(
            self.memory_title
        )

        # ---------------------------------------------------------
        # MEMORY PROCESSES
        # ---------------------------------------------------------

        self.memory_processes = QLabel(
            "Loading..."
        )

        self.memory_processes.setWordWrap(
            False
        )

        self.memory_processes.setTextInteractionFlags(
            Qt.TextInteractionFlag.NoTextInteraction
        )

        self.memory_processes.setStyleSheet("""
            color: #9eacbd;
            font-size: 11px;
            font-family: monospace;
        """)

        self.process_layout.addWidget(
            self.memory_processes
        )

        # ---------------------------------------------------------
        # BACK
        # ---------------------------------------------------------

        self.process_back_button = QPushButton(
            "← Back"
        )

        self.process_back_button.setObjectName(
            "back"
        )

        self.process_back_button.clicked.connect(
            self.show_main_page
        )

        self.process_layout.addWidget(
            self.process_back_button
        )

        self.layout.addWidget(
            self.process_page
        )

        # =========================================================
        # INITIAL STATE
        # =========================================================

        self.show_main_page()

        self.update_size()

    # =============================================================
    # RESPONSIVE SIZE
    # =============================================================

    def update_size(self):

        self.adjustSize()

        # Keep popup within reasonable bounds.
        screen = self.screen()

        if screen is None:
            return

        available = screen.availableGeometry()

        max_height = int(
            available.height() * 0.85
        )

        if self.height() > max_height:

            self.resize(
                self.width(),
                max_height,
            )

    # =============================================================
    # MAIN PAGE
    # =============================================================

    def show_main_page(self):

        self.main_page.show()
        self.update_page.hide()
        self.process_page.hide()

        self.title.setText(
            "Alpha"
        )

        self.subtitle.setText(
            "What can I help you with?"
        )

        self.update_size()

    # =============================================================
    # UPDATE PAGE
    # =============================================================

    def show_update_page(self):

        self.main_page.hide()
        self.update_page.show()
        self.process_page.hide()

        self.title.setText(
            "Update"
        )

        self.subtitle.setText(
            "Manage your system updates."
        )

        self.update_size()

    # =============================================================
    # PROCESS PAGE
    # =============================================================

    def show_process_page(self):

        self.main_page.hide()
        self.update_page.hide()
        self.process_page.show()

        self.title.setText(
            "Process Monitor"
        )

        self.subtitle.setText(
            "System resource usage"
        )

        self.update_process_monitor()

        self.update_size()

    # =============================================================
    # PROCESS MONITOR
    # =============================================================

    def update_process_monitor(self):

        if not self.process_page.isVisible():
            return

        try:

            info = (
                self.application.process_monitor
                .get_system_info()
                if hasattr(
                    self.application,
                    "process_monitor",
                )
                else ProcessMonitor.get_system_info()
            )

            memory_used = (
                info["memory_used"]
                / (1024 ** 3)
            )

            memory_total = (
                info["memory_total"]
                / (1024 ** 3)
            )

            load = info["load"]

            self.system_info.setText(
                f"CPU:  {info['cpu']:.1f}%\n"
                f"RAM:  {memory_used:.1f} / "
                f"{memory_total:.1f} GB "
                f"({info['memory_percent']:.1f}%)\n"
                f"Load: "
                f"{load[0]:.2f}  "
                f"{load[1]:.2f}  "
                f"{load[2]:.2f}"
            )

            # -----------------------------------------------------
            # TOP CPU
            # -----------------------------------------------------

            cpu_lines = []

            for process in ProcessMonitor.get_top_cpu(5):

                name = str(
                    process["name"]
                )

                if len(name) > 22:
                    name = name[:19] + "..."

                cpu_lines.append(
                    f"{name:<22} "
                    f"{process['cpu']:>6.1f}%"
                )

            self.cpu_processes.setText(
                "\n".join(cpu_lines)
                if cpu_lines
                else "No process data"
            )

            # -----------------------------------------------------
            # TOP MEMORY
            # -----------------------------------------------------

            memory_lines = []

            for process in ProcessMonitor.get_top_memory(5):

                name = str(
                    process["name"]
                )

                if len(name) > 22:
                    name = name[:19] + "..."

                memory_mb = (
                    process["memory"]
                    / (1024 ** 2)
                )

                memory_lines.append(
                    f"{name:<22} "
                    f"{memory_mb:>6.0f} MB"
                )

            self.memory_processes.setText(
                "\n".join(memory_lines)
                if memory_lines
                else "No process data"
            )

        except Exception as exc:

            print(
                "[MONITOR] ERROR:",
                repr(exc),
                flush=True,
            )

            self.system_info.setText(
                "Unable to read system resources."
            )

            self.cpu_processes.setText(
                "Monitor error"
            )

            self.memory_processes.setText(
                "Monitor error"
            )

    # =============================================================
    # STATUS
    # =============================================================

    def set_status(self, text):

        self.status.setText(
            text
        )

        self.update_size()

    # =============================================================
    # PACKAGES
    # =============================================================

    def set_packages(self, packages):

        if not packages:

            self.package_info.setText(
                "Your system is up to date."
            )

            self.update_size()

            return

        lines = []

        for package in packages[:4]:

            name = package.get(
                "name",
                "",
            )

            installed = package.get(
                "installed",
                "",
            )

            available = package.get(
                "available",
                "",
            )

            if available:

                lines.append(
                    f"{name}\n"
                    f"  {installed} → "
                    f"{available}"
                )

            else:

                lines.append(
                    name
                )

        if len(packages) > 4:

            lines.append(
                f"... and "
                f"{len(packages) - 4} more"
            )

        self.package_info.setText(
            "\n".join(lines)
        )

        self.update_size()

    # =============================================================
    # SHOW AT PET
    # =============================================================

    def show_at_pet(self):

        pet = self.application.pet

        if pet is None:
            return

        # Make sure layout has its final size
        self.update_size()

        pet_global = pet.mapToGlobal(
            QPoint(0, 0)
        )

        screen = pet.screen()

        if screen is None:

            self.move(
                pet_global.x()
                - self.width()
                - 8,
                pet_global.y(),
            )

            return

        available = (
            screen.availableGeometry()
        )

        # ---------------------------------------------------------
        # PREFER LEFT
        # ---------------------------------------------------------

        x = (
            pet_global.x()
            - self.width()
            - 10
        )

        # ---------------------------------------------------------
        # FALL BACK TO RIGHT
        # ---------------------------------------------------------

        if x < available.left():

            x = (
                pet_global.x()
                + pet.width()
                + 10
            )

        # ---------------------------------------------------------
        # KEEP INSIDE SCREEN
        # ---------------------------------------------------------

        x = max(
            available.left(),
            min(
                x,
                available.right()
                - self.width()
                + 1,
            ),
        )

        y = pet_global.y()

        y = max(
            available.top(),
            min(
                y,
                available.bottom()
                - self.height()
                + 1,
            ),
        )

        self.move(
            x,
            y,
        )

    # =============================================================
    # SHOW EVENT
    # =============================================================

    def showEvent(self, event):

        self.show_main_page()

        self.show_at_pet()

        super().showEvent(event)

