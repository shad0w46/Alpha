import re
import subprocess

from alpha.core.module import AlphaModule
from alpha.core.version import DebianVersion
from alpha.core.importance import PackageImportance


class PackagesModule(AlphaModule):

    module_id = "packages"

    name = "Package Intelligence"

    version = "0.3.0"

    def initialize(self, context):
        context["logger"].info(
            "Package Intelligence module initialized"
        )

    def _run_command(self, command):
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False
            )

            return (
                result.returncode,
                result.stdout,
                result.stderr
            )

        except Exception as error:
            return 1, "", str(error)

    def get_installed_packages(self):
        code, stdout, stderr = self._run_command(
            [
                "dpkg-query",
                "-W",
                "-f=${Package}\t${Version}\t${Status}\n"
            ]
        )

        if code != 0:
            raise RuntimeError(
                "Unable to read installed packages: "
                f"{stderr.strip()}"
            )

        packages = {}

        for line in stdout.splitlines():
            parts = line.split("\t")

            if len(parts) != 3:
                continue

            name, version, status = parts

            if status != "install ok installed":
                continue

            packages[name] = version

        return packages

    def get_available_updates(self):
        code, stdout, stderr = self._run_command(
            [
                "apt",
                "list",
                "--upgradable"
            ]
        )

        if code != 0:
            raise RuntimeError(
                "Unable to query APT updates: "
                f"{stderr.strip()}"
            )

        updates = {}

        for line in stdout.splitlines():

            line = line.strip()

            if not line:
                continue

            if line.startswith("Listing..."):
                continue

            match = re.match(
                r"^([^/]+)/[^\s]+\s+([^\s]+)",
                line
            )

            if not match:
                continue

            package = match.group(1)
            available_version = match.group(2)

            updates[package] = {
                "available": available_version
            }

        return updates

    def compare_versions(
        self,
        installed,
        available
    ):
        comparison = DebianVersion.compare(
            installed,
            available
        )

        if comparison < 0:
            return "update_available"

        if comparison > 0:
            return "downgrade_available"

        return "up_to_date"

    def scan(self, context):
        logger = context["logger"]

        logger.info(
            "Reading installed package database"
        )

        installed = self.get_installed_packages()

        logger.info(
            "Found %d installed packages",
            len(installed)
        )

        logger.info(
            "Checking APT for available updates"
        )

        candidates = self.get_available_updates()

        logger.info(
            "Found %d APT candidates",
            len(candidates)
        )

        updates = {}

        for package, data in candidates.items():

            available = data["available"]

            if package not in installed:
                continue

            installed_version = installed[package]

            status = self.compare_versions(
                installed_version,
                available
            )

            if status != "update_available":
                continue

            importance = PackageImportance.classify(
                package
            )

            updates[package] = {
                "installed": installed_version,
                "available": available,
                "version_status": status,
                "importance": importance
            }

        logger.info(
            "Found %d actual package updates",
            len(updates)
        )

        return {
            "installed_count": len(installed),
            "update_count": len(updates),
            "updates": updates
        }

    def analyze(self, context, scan_result):
        updates = scan_result.get(
            "updates",
            {}
        )

        return {
            "status": (
                "updates_available"
                if updates
                else "up_to_date"
            ),
            "installed_count": scan_result.get(
                "installed_count",
                0
            ),
            "update_count": len(updates),
            "updates": updates
        }

    def actions(self, context, analysis):
        return []

    def shutdown(self, context):
        pass
