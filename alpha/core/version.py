import subprocess


class DebianVersion:

    @staticmethod
    def compare(version_a, version_b):
        """
        Compare two Debian package versions.

        Returns:
            -1 if version_a < version_b
             0 if version_a == version_b
             1 if version_a > version_b
        """

        result = subprocess.run(
            [
                "dpkg",
                "--compare-versions",
                version_a,
                "lt",
                version_b
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return -1

        result = subprocess.run(
            [
                "dpkg",
                "--compare-versions",
                version_a,
                "eq",
                version_b
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return 0

        return 1

    @classmethod
    def is_newer(cls, installed, available):
        return cls.compare(
            installed,
            available
        ) < 0

    @classmethod
    def is_older(cls, installed, available):
        return cls.compare(
            installed,
            available
        ) > 0

    @classmethod
    def is_equal(cls, installed, available):
        return cls.compare(
            installed,
            available
        ) == 0
