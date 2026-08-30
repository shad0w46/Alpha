import sys

from alpha.gui.app import AlphaApplication


def main():
    application = AlphaApplication()
    sys.exit(application.run())


if __name__ == "__main__":
    main()
