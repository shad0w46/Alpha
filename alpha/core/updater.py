import subprocess


class PackageUpdater:

    def __init__(self, logger):
        self.logger = logger

    def _run(self, command):
        self.logger.info(
            "Running: %s",
            " ".join(command)
        )

        return subprocess.run(
            command,
            text=True,
            check=False
        )

    def refresh(self):
        """
        Refresh APT package indexes.
        """

        self.logger.info(
            "Refreshing APT package indexes"
        )

        return self._run(
            [
                "sudo",
                "apt-get",
                "update"
            ]
        )

    def upgrade(self):
        """
        Upgrade installed packages.
        """

        self.logger.info(
            "Starting package upgrade"
        )

        return self._run(
            [
                "sudo",
                "apt-get",
                "upgrade"
            ]
        )

    def full_upgrade(self):
        """
        Perform a full distribution upgrade.

        This is intentionally separate from normal upgrade.
        """

        self.logger.info(
            "Starting full package upgrade"
        )

        return self._run(
            [
                "sudo",
                "apt-get",
                "full-upgrade"
            ]
        )
