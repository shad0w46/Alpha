class PackageImportance:

    HIGH_PACKAGES = {
        "linux-image",
        "linux-image-amd64",
        "linux-headers",
        "libc6",
        "libc-bin",
        "libsystemd0",
        "systemd",
        "systemd-sysv",
        "sudo",
        "openssh-client",
        "openssh-server",
        "openssl",
        "ca-certificates",
        "apt",
        "dpkg",
    }

    MEDIUM_PACKAGES = {
        "network-manager",
        "network-manager-gnome",
        "curl",
        "wget",
        "git",
        "python3",
        "python3-minimal",
        "bash",
        "zsh",
        "dbus",
        "polkit",
    }

    HIGH_PREFIXES = (
        "linux-image",
        "linux-headers",
        "linux-libc-dev",
        "libc6",
        "libssl",
        "openssl",
        "systemd",
    )

    MEDIUM_PREFIXES = (
        "libwireshark",
        "libwiretap",
        "libwsutil",
        "wireshark",
        "network-manager",
        "python3",
    )

    @classmethod
    def classify(cls, package_name):
        """
        Classify a package as LOW, MEDIUM, or HIGH.

        The result is deliberately deterministic and explainable.
        """

        package = package_name.lower()

        if package in cls.HIGH_PACKAGES:
            return {
                "level": "HIGH",
                "score": 90,
                "reason": (
                    "Core system or security-critical package"
                )
            }

        for prefix in cls.HIGH_PREFIXES:
            if package.startswith(prefix):
                return {
                    "level": "HIGH",
                    "score": 85,
                    "reason": (
                        "Core operating-system component"
                    )
                }

        if package in cls.MEDIUM_PACKAGES:
            return {
                "level": "MEDIUM",
                "score": 60,
                "reason": (
                    "Important system or commonly used software"
                )
            }

        for prefix in cls.MEDIUM_PREFIXES:
            if package.startswith(prefix):
                return {
                    "level": "MEDIUM",
                    "score": 55,
                    "reason": (
                        "System library or important application"
                    )
                }

        return {
            "level": "LOW",
            "score": 25,
            "reason": (
                "General application or library"
            )
        }
