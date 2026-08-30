import re
import subprocess
from pathlib import Path

from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtWidgets import QApplication

from alpha.gui.pet import AlphaPet
from alpha.gui.popup import AlphaPopup


class AlphaApplication:

    VERSION = "0.1.0"

    def __init__(self):

        print(
            "[APP] Starting Alpha GUI",
            flush=True,
        )

        self.qt_app = QApplication.instance()

        if self.qt_app is None:
            self.qt_app = QApplication([])

        self.qt_app.setApplicationName("Alpha")
        self.qt_app.setApplicationDisplayName("Alpha")

        self.pet = None
        self.popup = None

        self.updates = []

        self.logo_path = self.find_logo()

        print(
            f"[APP] Logo path: {self.logo_path}",
            flush=True,
        )

        self.create_pet()
        self.create_popup()

        # Do not immediately scan before the UI exists.
        QTimer.singleShot(
            300,
            self.scan,
        )

    # =========================================================
    # LOGO
    # =========================================================

    def find_logo(self):

        candidates = [

            Path.home()
            / "Projects"
            / "Alpha"
            / "Alpha_OS"
            / "alphaos-branding-main"
            / "assets"
            / "logo-no-background.png",

            Path(
                "/home/zero/Projects/Alpha/"
                "Alpha_OS/alphaos-branding-main/"
                "assets/logo-no-background.png"
            ),

            Path(__file__).resolve().parent
            / "assets"
            / "logo-no-background.png",
        ]

        for path in candidates:

            print(
                f"[APP] Checking logo: {path}",
                flush=True,
            )

            if path.exists():

                print(
                    f"[APP] FOUND logo: {path}",
                    flush=True,
                )

                return str(path)

        print(
            "[APP] ERROR: no logo found",
            flush=True,
        )

        return None

    # =========================================================
    # PET
    # =========================================================

    def create_pet(self):

        print(
            "[APP] Creating pet",
            flush=True,
        )

        self.pet = AlphaPet(
            image_path=self.logo_path
        )

        self.pet.clicked.connect(
            self.on_pet_clicked
        )

        self.pet.moved.connect(
            self.on_pet_moved
        )

        self.pet.show()

        print(
            "[APP] Pet shown",
            f"position={self.pet.pos()}",
            f"size={self.pet.size()}",
            flush=True,
        )

        # Put it near the right side of the desktop.
        screen = self.pet.screen()

        if screen:

            geometry = screen.availableGeometry()

            x = (
                geometry.right()
                - self.pet.width()
                - 30
            )

            y = (
                geometry.top()
                + 120
            )

            self.pet.move(x, y)

            print(
                "[APP] Initial pet position:",
                self.pet.pos(),
                flush=True,
            )

    # =========================================================
    # POPUP
    # =========================================================

    def create_popup(self):

        print(
            "[APP] Creating popup",
            flush=True,
        )

        self.popup = AlphaPopup(
            self,parent=self.pet
        )

        print(
            "[APP] Popup created",
            flush=True,
        )

    def on_pet_clicked(self):

        print(
            "[APP] PET CLICKED",
            flush=True,
        )

        self.toggle_popup()

    def on_pet_moved(self):

        print(
            "[APP] PET MOVED",
            f"position={self.pet.pos()}",
            flush=True,
        )

        self.follow_popup()

    def toggle_popup(self):

        if self.popup.isVisible():

            print(
                "[APP] Hiding popup",
                flush=True,
            )

            self.popup.hide()

        else:

            print(
                "[APP] Showing popup",
                flush=True,
            )

            self.popup.show()

            self.popup.show_at_pet()

            self.popup.raise_()

    def follow_popup(self):

        if (
            self.popup
            and self.popup.isVisible()
        ):

            print(
                "[APP] Following pet with popup",
                f"pet={self.pet.pos()}",
                flush=True,
            )

            self.popup.show_at_pet()

    # =========================================================
    # INSTALLED PACKAGES
    # =========================================================

    def installed_package_count(self):

        print(
            "[APT] Reading installed packages",
            flush=True,
        )

        try:

            result = subprocess.run(
                [
                    "dpkg-query",
                    "-W",
                    "-f=${binary:Package}\\n",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:

                print(
                    "[APT] dpkg-query failed",
                    result.stderr,
                    flush=True,
                )

                return 0

            packages = [
                line.strip()
                for line in result.stdout.splitlines()
                if line.strip()
            ]

            count = len(packages)

            print(
                f"[APT] Installed packages: {count}",
                flush=True,
            )

            return count

        except Exception as exc:

            print(
                f"[APT] Package count error: {exc}",
                flush=True,
            )

            return 0

    # =========================================================
    # APT UPDATES
    # =========================================================

    def get_apt_updates(self):

        print(
            "[APT] Checking for updates",
            flush=True,
        )

        updates = []

        try:

            result = subprocess.run(
                [
                    "apt",
                    "list",
                    "--upgradable",
                ],
                capture_output=True,
                text=True,
                stderr=subprocess.DEVNULL,
                timeout=30,
            )

            print(
                f"[APT] apt return code: "
                f"{result.returncode}",
                flush=True,
            )

            for line in result.stdout.splitlines():

                line = line.strip()

                if (
                    not line
                    or line.startswith("Listing...")
                ):
                    continue

                print(
                    f"[APT] Candidate: {line}",
                    flush=True,
                )

                match = re.match(
                    r"^([^/]+)/\S+\s+"
                    r"(\S+)\s+.*"
                    r"\[upgradable from:\s+([^\]]+)\]",
                    line,
                )

                if not match:

                    print(
                        "[APT] Could not parse line",
                        flush=True,
                    )

                    continue

                name = match.group(1)
                available = match.group(2)
                installed = match.group(3)

                updates.append(
                    {
                        "name": name,
                        "installed": installed,
                        "available": available,
                    }
                )

            print(
                f"[APT] Actual updates: "
                f"{len(updates)}",
                flush=True,
            )

        except Exception as exc:

            print(
                f"[APT] Update check error: {exc}",
                flush=True,
            )

        return updates

    # =========================================================
    # SCAN
    # =========================================================

    def scan(self):

        print(
            "[APP] =================================",
            flush=True,
        )

        print(
            "[APP] SCAN START",
            flush=True,
        )

        if self.popup:

            self.popup.set_status(
                "Scanning..."
            )

        self.qt_app.processEvents()

        def do_scan():

            count = (
                self.installed_package_count()
            )

            updates = (
                self.get_apt_updates()
            )

            self.updates = updates

            if not updates:

                status = (
                    "✓ System is up to date"
                )

            elif len(updates) == 1:

                status = (
                    "● 1 package update available"
                )

            else:

                status = (
                    f"● {len(updates)} "
                    "package updates available"
                )

            print(
                f"[APP] SCAN RESULT: "
                f"{count} installed, "
                f"{len(updates)} updates",
                flush=True,
            )

            if self.popup:

                self.popup.set_status(
                    status
                )

                self.popup.set_packages(
                    updates
                )

                self.popup.subtitle.setText(
                    f"{count:,} packages installed"
                )

            print(
                "[APP] SCAN COMPLETE",
                flush=True,
            )

            print(
                "[APP] =================================",
                flush=True,
            )

        QTimer.singleShot(
            100,
            do_scan,
        )

    # =========================================================
    # VIEW UPDATES
    # =========================================================

    def show_updates(self):

        print(
            "[APP] VIEW UPDATES",
            flush=True,
        )

        if not self.updates:

            print(
                "[APP] No updates cached; scanning",
                flush=True,
            )

            self.scan()
            return

        lines = [
            f"{len(self.updates)} "
            + (
                "package update available"
                if len(self.updates) == 1
                else "package updates available"
            ),
            "",
        ]

        for package in self.updates[:8]:

            lines.append(
                f"{package['name']}: "
                f"{package['installed']} → "
                f"{package['available']}"
            )

        if len(self.updates) > 8:

            lines.append(
                "",
            )

            lines.append(
                f"... and "
                f"{len(self.updates) - 8} more"
            )

        self.popup.set_status(
            f"● {len(self.updates)} updates available"
        )

        self.popup.package_info.setText(
            "\n".join(lines)
        )

        self.popup.show()
        self.popup.show_at_pet()
        self.popup.raise_()

    # =========================================================
    # UPGRADE
    # =========================================================

    def upgrade(self):

        print(
            "[APP] UPGRADE requested",
            flush=True,
        )

        if self.popup:

            self.popup.set_status(
                "Starting upgrade..."
            )

        self.qt_app.processEvents()

        command = (
            "apt-get update && "
            "DEBIAN_FRONTEND=noninteractive "
            "apt-get upgrade -y"
        )

        try:

            print(
                "[APP] Starting pkexec upgrade",
                flush=True,
            )

            subprocess.Popen(
                [
                    "pkexec",
                    "bash",
                    "-c",
                    command,
                ]
            )

            if self.popup:

                self.popup.set_status(
                    "Upgrade started"
                )

            QTimer.singleShot(
                5000,
                self.scan,
            )

        except Exception as exc:

            print(
                f"[APP] Upgrade error: {exc}",
                flush=True,
            )

            if self.popup:

                self.popup.set_status(
                    "Upgrade failed"
                )

    # =========================================================
    # QUIT
    # =========================================================

    def quit(self):

        print(
            "[APP] =================================",
            flush=True,
        )

        print(
            "[APP] QUIT",
            flush=True,
        )

        if self.popup:

            print(
                "[APP] Closing popup",
                flush=True,
            )

            self.popup.close()

        if self.pet:

            print(
                "[APP] Closing pet",
                flush=True,
            )

            self.pet.close()

        self.qt_app.quit()

    # =========================================================
    # RUN
    # =========================================================

    def run(self):

        print(
            "[APP] Qt event loop starting",
            flush=True,
        )

        return self.qt_app.exec()
