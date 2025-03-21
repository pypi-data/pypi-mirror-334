"""Module runner or Main entry point"""

from bugx.cli import app
from bugx.utils import Display


def run() -> None:
    """Main Runner"""
    try:
        app()
    except Exception as main_exception:  # pylint:disable="W0718"
        Display().error(message=main_exception, app_exit=True)


if __name__ == "__main__":
    run()
