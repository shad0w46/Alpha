from alpha.core.importance import PackageImportance


def test_kernel_is_high():
    result = PackageImportance.classify(
        "linux-image-amd64"
    )

    assert result["level"] == "HIGH"


def test_libc_is_high():
    result = PackageImportance.classify(
        "libc6"
    )

    assert result["level"] == "HIGH"


def test_wireshark_is_medium():
    result = PackageImportance.classify(
        "wireshark"
    )

    assert result["level"] == "MEDIUM"


def test_unknown_package_is_low():
    result = PackageImportance.classify(
        "some-random-application"
    )

    assert result["level"] == "LOW"
