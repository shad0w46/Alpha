from PySide6.QtCore import (
    Qt,
    QPoint,
    QTimer,
)

from PySide6.QtGui import QFont

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)

from alpha.core.process_monitor import ProcessMonitor


class AlphaPopup(QWidget):

    def __init__(self, application, parent=None):
        super().__init__(parent)

        self.application = application

        # =========================================================
        # PROCESS MONITOR TIMER
        # =========================================================

        self.monitor_timer = QTimer(self)

        self.monitor_timer.timeout.connect(
            self.update_process_monitor
        )

        self.monitor_timer.start(2000)

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

        # Bigger because Process Monitor needs space.
        self.setFixedSize(
            310,
            430,
        )

        # =========================================================
        # UI
        # =========================================================

        self.build_ui()

    # =============================================================
    # BUILD UI
    # =============================================================

    def build_ui(self):

        self.frame = QFrame(self)

        self.frame.setGeometry(
            0,
            0,
            310,
            430,
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

        # =========================================================
        # MAIN LAYOUT
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

        title_font.setPointSize(
            18
        )

        title_font.setBold(
            True
        )

        self.title.setFont(
            title_font
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

        self.status.setStyleSheet(
            "color: #ffc533; "
            "font-weight: bold;"
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

        self.update_button.clicked.connect(
            self.show_update_page
        )

        self.main_layout.addWidget(
            self.update_button
        )

        # ---------------------------------------------------------
        # PROCESS MONITOR
        # ---------------------------------------------------------

        self.process_button = QPushButton(
            "Process Monitor"
        )

        self.process_button.clicked.connect(
            self.show_process_page
        )

        self.main_layout.addWidget(
            self.process_button
        )

        # ---------------------------------------------------------
        # CLOSE POPUP
        # ---------------------------------------------------------

        self.close_button = QPushButton(
            "Close"
        )

        self.close_button.setObjectName(
            "close"
        )

        # Only hide popup.
        self.close_button.clicked.connect(
            self.hide
        )

        self.main_layout.addWidget(
            self.close_button
        )

        # ---------------------------------------------------------
        # EXIT ALPHA
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
        # PROCESS MONITOR PAGE
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
        # RESOURCE SUMMARY
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

        self.system_info = QLabel(
            "CPU: --\n"
            "RAM: --\n"
            "Load: --"
        )

        self.system_info.setStyleSheet("""
            color: #e8edf5;
            font-size: 12px;
        """)

        self.process_layout.addWidget(
            self.system_info
        )

        # ---------------------------------------------------------
        # CPU
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

        self.cpu_processes = QLabel(
            "Loading..."
        )

        self.cpu_processes.setStyleSheet("""
            color: #9eacbd;
            font-size: 11px;
            font-family: monospace;
        """)

        self.cpu_processes.setWordWrap(
            False
        )

        self.process_layout.addWidget(
            self.cpu_processes
        )

        # ---------------------------------------------------------
        # MEMORY
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

        self.memory_processes = QLabel(
            "Loading..."
        )

        self.memory_processes.setStyleSheet("""
            color: #9eacbd;
            font-size: 11px;
            font-family: monospace;
        """)

        self.memory_processes.setWordWrap(
            False
        )

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
        # INITIAL PAGE
        # =========================================================

        self.show_main_page()

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

    # =============================================================
    # PROCESS MONITOR PAGE
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

        # Immediately refresh when opened.
        self.update_process_monitor()

    # =============================================================
    # PROCESS MONITOR
    # =============================================================

    def update_process_monitor(self):

        # Don't waste resources updating hidden UI.
        if not self.process_page.isVisible():
            return

        try:

            # -----------------------------------------------------
            # SYSTEM
            # -----------------------------------------------------

            info = (
                ProcessMonitor.get_system_info()
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

            cpu_processes = (
                ProcessMonitor.get_top_cpu(
                    5
                )
            )

            for process in cpu_processes:

                name = process["name"]

                if len(name) > 18:
                    name = name[:18]

                cpu_lines.append(
                    f"{name:<18} "
                    f"{process['cpu']:>6.1f}%"
                )

            if cpu_lines:

                self.cpu_processes.setText(
                    "\n".join(cpu_lines)
                )

            else:

                self.cpu_processes.setText(
                    "No process data"
                )

            # -----------------------------------------------------
            # TOP MEMORY
            # -----------------------------------------------------

            memory_lines = []

            memory_processes = (
                ProcessMonitor.get_top_memory(
                    5
                )
            )

            for process in memory_processes:

                name = process["name"]

                if len(name) > 18:
                    name = name[:18]

                memory_mb = (
                    process["memory"]
                    / (1024 ** 2)
                )

                memory_lines.append(
                    f"{name:<18} "
                    f"{memory_mb:>6.0f} MB"
                )

            if memory_lines:

                self.memory_processes.setText(
                    "\n".join(memory_lines)
                )

            else:

                self.memory_processes.setText(
                    "No process data"
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

    # =============================================================
    # PACKAGES
    # =============================================================

    def set_packages(self, packages):

        if not packages:

            self.package_info.setText(
                "Your system is up to date."
            )

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

    # =============================================================
    # SHOW AT PET
    # =============================================================

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
        # USE RIGHT IF LEFT IS TOO SMALL
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

        # Every time popup opens,
        # return to the main page.

        self.show_main_page()

        self.show_at_pet()

        super().showEvent(event)

