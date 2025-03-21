"""updater"""

import subprocess
import sys
import time
from typing import LiteralString, NoReturn

import requests
from flagsmith import Flagsmith
from flagsmith.exceptions import FlagsmithAPIError

from bugx.__about__ import __version__, app_name
from bugx.utils import Command, Display, Network, Prettier, console

display = Display()

APP_NAME: LiteralString = app_name.title()


def get_changelog() -> NoReturn:
    """gives the changelog"""
    try:
        Network(url=None).check(to_exit=True)
        flagsmith = Flagsmith(
            environment_key="ser.NJ2Sh3B2NJGLC9hYsKYrJx",
        )
        changelog = flagsmith.get_environment_flags().get_feature_value(feature_name="changelog")
        console.print(Prettier(message="Here is the changelog:").bold_green)
        console.print(changelog)
    except FlagsmithAPIError as api_error:
        display.connection_error(message=api_error)


def get_latest_version() -> str:
    """gives the latest version."""
    try:
        time.sleep(2)
        url: LiteralString = f"https://pypi.python.org/pypi/{app_name}/json"
        r: requests.Response = requests.get(url=url, timeout=5)
        r.raise_for_status()
        return r.json()["info"]["version"]
    except requests.exceptions.ConnectionError as connection_error:
        raise ConnectionError(
            f"Failed to fetch the latest {APP_NAME} version."
        ) from connection_error


def update():
    """update"""
    try:
        with console.status(status="Checking for Updates...") as update_status:
            update_status.start()
            latest_version = get_latest_version()
            current_version = __version__

            if latest_version == current_version:
                update_status.update(
                    status=f"Got a new version {latest_version}. Kicking myself to update."
                )
                Command(command=[sys.executable, "-m", "pip", "install", "--upgrade", app_name]).run(
                    app_exit=True, error_msg="internal error."
                )
                update_status.stop()
                display.success(f"Updated to v{__version__}.")
                get_changelog()
            else:
                console.print(":sparkles: Hola... Im already updated.")
    except IOError as e:
        display.connection_error(e)
    except KeyboardInterrupt as _:
        display.interrupt(f"While updating {APP_NAME}.")
    except subprocess.CalledProcessError as update_error:
        display.error(f"Failed to update {app_name} due to {update_error.stderr}")


if __name__ == "__main__":
    update()
