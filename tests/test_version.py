from alpha.core.version import DebianVersion


def test_equal_versions():
    assert DebianVersion.compare(
        "1.0-1",
        "1.0-1"
    ) == 0


def test_older_version():
    assert DebianVersion.compare(
        "1.0-1",
        "1.1-1"
    ) == -1


def test_newer_version():
    assert DebianVersion.compare(
        "1.1-1",
        "1.0-1"
    ) == 1


def test_debian_version():
    assert DebianVersion.compare(
        "1.2.9",
        "1.2.10"
    ) == -1


def test_debian_revision():
    assert DebianVersion.compare(
        "1.0-1",
        "1.0-2"
    ) == -1
