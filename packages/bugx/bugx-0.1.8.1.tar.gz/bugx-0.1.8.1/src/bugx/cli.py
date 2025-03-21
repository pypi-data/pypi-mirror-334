"""cli"""

import subprocess
from functools import wraps
from typing import Annotated, Any

import click
import typer
from typer.core import TyperGroup as TyperGroupBase

from bugx.__about__ import version
from bugx.bugreport_extractor import for_cli
from bugx.cli_constants import CliApplication, SelectOption, UpdateOption, WatchOption
from bugx.updater import update
from bugx.utils import Display, console
from bugx.watcher import watcher

display = Display()


class TyperGroup(TyperGroupBase):
    """Custom TyperGroup class."""

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)

    def get_usage(self, ctx: click.Context) -> str:
        """Override get_usage."""
        usage: str = super().get_usage(ctx)
        console.print(CliApplication.DESCRIPTION, justify=CliApplication.JUSTIFY)
        message: str = f"\n{usage}"
        return message


app = typer.Typer(
    name=CliApplication.APP_NAME,
    epilog=CliApplication.EPILOG,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
    add_completion=True,
    invoke_without_command=True,
    rich_markup_mode="rich",
    cls=TyperGroup,
)


def version_callback(value: bool) -> None:
    """Version callback"""
    if value:
        version()
        raise typer.Exit()


@app.callback(short_help=CliApplication.VERSION_FLAG_HELP, epilog=CliApplication.EPILOG)
def cli_version(  # pylint:disable=C0116
    display_version: Annotated[
        bool,
        typer.Option("--version", "-v", help=CliApplication.VERSION_FLAG_HELP, is_eager=True),
    ] = False,
) -> None:
    if display_version:
        version_callback(value=True)


def docstring(*examples):
    """docstring decorator"""

    def decorator(obj):
        if obj.__doc__:
            obj.__doc__ = obj.__doc__.format(*examples)
        return obj

    return decorator


def run_with(interrupt_message: str):
    """run with decorator"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt as run_with_interrupt:
                if not run_with_interrupt.args:
                    display.interrupt(message=interrupt_message)
                else:
                    display.interrupt(
                        message=f"{interrupt_message if not run_with_interrupt.args[0].args  else run_with_interrupt}"
                    )
            except (
                subprocess.CalledProcessError,
                ValueError,
                TypeError,
                AttributeError,
            ) as run_with_error:
                display.error(message=f"{func.__name__}: {run_with_error}")

        return wrapper

    return decorator


@app.command(
    name=SelectOption.OPTION_NAME,
    rich_help_panel="Commands :robot:",
    epilog=CliApplication.EPILOG,
    short_help=SelectOption.SHORT_HELP,
    help=SelectOption.EXAMPLES,
)
# @docstring(SelectOption.EXAMPLES)
@run_with(interrupt_message=SelectOption.INTERRUPT_MESSAGE)
def select(
    select_all: Annotated[
        bool, typer.Option("--all", "-a", help=SelectOption.ALL_FLAG_HELP)
    ] = False,
    to_display: Annotated[
        bool,
        typer.Option("--display", "-d", help=SelectOption.DISPLAY_FLAG_HELP),
    ] = False,
    _: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help=CliApplication.VERSION_FLAG_HELP,
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Prompts the user to select the bugreports."""
    for_cli(override=to_display, select_all=select_all)


@app.command(
    name=WatchOption.OPTION_NAME,
    rich_help_panel="Commands :robot:",
    epilog=CliApplication.EPILOG,
    help=WatchOption.EXAMPLES,
    short_help=WatchOption.SHORT_HELP,
)
@run_with(interrupt_message=WatchOption.INTERRUPT_MESSAGE)
def watch(
    to_display: Annotated[
        bool,
        typer.Option("--display", "-d", help=WatchOption.DISPLAY_FLAG_HELP),
    ] = False,
    _: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help=CliApplication.VERSION_FLAG_HELP,
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """looks for bugreports."""
    watcher(override=to_display)


@app.command(
    name=UpdateOption.OPTION_NAME,
    rich_help_panel="Settings :hammer_and_wrench:",
    help=UpdateOption.EXAMPLES,
    short_help=UpdateOption.SHORT_HELP,
)
@run_with(interrupt_message=UpdateOption.INTERRUPT_MESSAGE)
def updater(
    _: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help=CliApplication.VERSION_FLAG_HELP,
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """updates the package to latest version."""
    update()


if __name__ == "__main__":
    app()
