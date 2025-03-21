"""Watcher for Bugreports"""

import os

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from bugx import HOME, console
from bugx.bugreport_extractor import for_watch_cli
from bugx.utils import Display, Prettier

display = Display()

observer = Observer()
DIR_NAMES = ["home", "documents", "downloads"]


def lookup_dir(dir_names: list[str]) -> list[str]:
    """lookup dir"""
    full_paths = [
        HOME if name.lower() == "home" else os.path.join(HOME, name.title()) for name in dir_names
    ]
    return full_paths


class FileDropHandler(PatternMatchingEventHandler):
    """File handler"""

    def __init__(self, cli_status, override):
        super().__init__(patterns=["*.zip", "*.gz"])
        self.cli_status = cli_status
        self.to_display: bool = override

    def on_created(self, event):
        if not event.is_directory:
            for_watch_cli(
                file_path=event.src_path, cli_status=self.cli_status, override=self.to_display
            )
            self.cli_status.update(
                status=Prettier(message="Looking for Bugreports :package:...").bold_green
            )


def watcher(override: bool):
    """watcher"""
    with console.status(
        status=Prettier(message="Looking for Bugreports :package:...").bold_green
    ) as looking_status:

        event_handler = FileDropHandler(cli_status=looking_status, override=override)

        for p in lookup_dir(dir_names=["documents", "downloads"]):
            observer.schedule(event_handler=event_handler, path=p, recursive=False)

        observer.start()

        try:
            while observer.is_alive():
                observer.join(1)
        except KeyboardInterrupt:
            display.success(message="Happy to watch for you.")
        finally:
            observer.stop()
            observer.join()


if __name__ == "__main__":
    watcher(override=False)
