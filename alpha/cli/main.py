import argparse

from alpha.core.config import Config
from alpha.core.database import Database
from alpha.core.engine import AlphaEngine
from alpha.core.logger import setup_logger
from alpha.core.updater import PackageUpdater


def create_engine():
    config = Config()

    logger = setup_logger(
        config.get(
            "logging",
            "level",
            default="INFO"
        ),
        config.get(
            "logging",
            "file",
            default="logs/alpha.log"
        )
    )

    database = Database(
        config.get(
            "database",
            "path",
            default="data/alpha.db"
        )
    )

    engine = AlphaEngine(
        config=config,
        database=database,
        logger=logger
    )

    engine.initialize()

    return engine


def print_header(title):
    print()
    print("╭──────────────────────────────────────────╮")
    print(f"│ {title:^40} │")
    print("╰──────────────────────────────────────────╯")
    print()


def command_status(engine):
    version = engine.config.get(
        "alpha",
        "version",
        default="unknown"
    )

    modules = engine.database.get_modules()

    print_header("ALPHA")

    print(f"Version: {version}")
    print(f"Modules: {len(modules)}")
    print()

    if modules:
        print("Loaded modules")
        print("───────────────")

        for module_id, name, module_version, enabled in modules:
            state = "enabled" if enabled else "disabled"

            print(
                f"  {name:<24}"
                f"v{module_version:<10}"
                f"{state}"
            )
    else:
        print("No modules installed.")

    print()


def command_modules(engine):
    modules = engine.database.get_modules()

    print_header("ALPHA MODULES")

    if not modules:
        print("No modules installed.")
        print()
        return

    for module_id, name, version, enabled in modules:
        state = "enabled" if enabled else "disabled"

        print(
            f"  {module_id:<20}"
            f"{version:<10}"
            f"{state:<10}"
            f"{name}"
        )

    print()


def command_scan(engine):
    print_header("SYSTEM SCAN")

    print("Scanning system...")
    print()

    results = engine.scan()

    package_result = results.get("packages")

    if package_result:
        print_package_report(package_result)

    for module_id, result in results.items():
        if module_id == "packages":
            continue

        print(f"{module_id}:")
        print(f"  {result}")
        print()


def print_package_report(result):
    status = result.get("status")
    updates = result.get("updates", {})
    installed_count = result.get(
        "installed_count",
        0
    )
    update_count = result.get(
        "update_count",
        0
    )

    print("Package Intelligence")
    print("─────────────────────")
    print()

    print(
        f"Installed packages : {installed_count}"
    )

    print(
        f"Updates available  : {update_count}"
    )

    print()

    if status == "up_to_date":
        print("✓ System is up to date.")
        print()
        return

    print("Updates")
    print("───────")
    print()

    grouped = {
        "HIGH": [],
        "MEDIUM": [],
        "LOW": []
    }

    for package, data in updates.items():
        importance = data.get(
            "importance",
            {}
        )

        level = importance.get(
            "level",
            "LOW"
        )

        grouped.setdefault(
            level,
            []
        ).append(
            (
                package,
                data
            )
        )

    for level in ("HIGH", "MEDIUM", "LOW"):

        packages = grouped.get(
            level,
            []
        )

        if not packages:
            continue

        print(f"{level} PRIORITY")
        print("─" * 30)

        for package, data in packages:

            installed = data.get(
                "installed",
                "unknown"
            )

            available = data.get(
                "available",
                "unknown"
            )

            reason = data.get(
                "importance",
                {}
            ).get(
                "reason",
                "No reason available"
            )

            print()
            print(f"  {package}")
            print(
                f"    {installed} → {available}"
            )
            print(
                f"    {reason}"
            )

        print()

    print(
        f"{update_count} update(s) available."
    )
    print()


def command_update(engine):
    updater = PackageUpdater(
        engine.logger
    )

    print_header("ALPHA PACKAGE UPDATER")

    print(
        "Step 1/2: Refreshing package information..."
    )
    print()

    result = updater.refresh()

    if result.returncode != 0:
        print()
        print("✗ APT update failed.")
        print()
        return

    print()
    print("✓ Package information refreshed.")
    print()

    print(
        "Step 2/2: Installing available updates"
    )
    print()

    answer = input(
        "Continue with package upgrade? [y/N]: "
    ).strip().lower()

    if answer not in ("y", "yes"):
        print()
        print("Upgrade cancelled.")
        print()
        return

    print()
    print("Starting upgrade...")
    print()

    result = updater.upgrade()

    print()

    if result.returncode == 0:
        print("✓ Upgrade completed successfully.")
    else:
        print(
            f"✗ Upgrade finished with exit code "
            f"{result.returncode}."
        )

    print()


def main():
    parser = argparse.ArgumentParser(
        prog="alpha",
        description="AlphaOS system intelligence"
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    subparsers.add_parser(
        "status",
        help="Show Alpha status"
    )

    subparsers.add_parser(
        "modules",
        help="Show installed modules"
    )

    subparsers.add_parser(
        "scan",
        help="Scan the system"
    )

    subparsers.add_parser(
        "update",
        help="Refresh APT and upgrade packages"
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    engine = create_engine()

    try:
        if args.command == "status":
            command_status(engine)

        elif args.command == "modules":
            command_modules(engine)

        elif args.command == "scan":
            command_scan(engine)

        elif args.command == "update":
            command_update(engine)

    finally:
        engine.shutdown()
