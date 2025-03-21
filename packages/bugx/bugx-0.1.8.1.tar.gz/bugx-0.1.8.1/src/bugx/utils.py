"""utils"""

import subprocess
import sys
from typing import Literal, Optional, Union

import requests

from bugx import console


class Prettier:
    """prettier"""

    def __init__(self, message: str):
        self.message: str = message

    @property
    def bold_yellow(self) -> str:
        """bold yellow"""
        return f"[bold yellow]{self.message}[/bold yellow]"

    @property
    def bold_green(self) -> str:
        """bold green"""
        return f"[bold green]{self.message}[/bold green]"

    @property
    def bold_red(self) -> str:
        """bold red"""
        return f"[bold red]{self.message}[/bold red]"

    def apply(self, weight: Literal["bold", "italic"], color: str) -> str:
        """apply"""
        return f"[{weight} {color}]{self.message}[/{weight} {color}]"


class Display:
    """Display"""

    def __init__(self):
        self.print = console.print

    def interrupt(self, message: str, app_exit: bool = True) -> None:
        """interrupt"""
        self.print(
            f":unamused: :{Prettier(message=f"Dude you Interrupted me. {message}").bold_yellow}"
        )
        if app_exit:
            sys.exit(2)

    def success(self, message: str) -> None:
        """success"""
        self.print(f":white_check_mark: :{Prettier(message=message).bold_green}")

    def error(self, message: str, app_exit: bool = False, new_line: bool = False) -> None:
        """error"""
        self.print(
            f"{"\n" if new_line else ""}:x: :{Prettier(message=message).bold_red}",
            new_line_start=new_line,
        )
        if app_exit:
            sys.exit(1)

    def connection_error(
        self, message: str, app_exit: bool = False, new_line: bool = False
    ) -> None:
        """connection error"""
        self.print(
            f"{"\n" if new_line else ""}:sleeping: :{Prettier(message=message).bold_red}",
            new_line_start=new_line,
        )
        if app_exit:
            sys.exit(1)


class Network(Display):
    """Network"""

    def __init__(self, url: Optional[str]):
        super().__init__()
        self.timeout = 5
        self.url = "https://www.google.com" if not url else url

    def check(self, to_exit: bool) -> None:
        """checks for network"""
        try:
            r = requests.get(self.url, timeout=self.timeout)
            r.raise_for_status()
        except requests.exceptions.ConnectionError:
            self.connection_error(
                message="No Network. Please connect to Internet :signal_strength:.",
                app_exit=to_exit,
            )


class Command(Display):
    """command runner"""

    def __init__(self, command: Union[str, list[str]], verbose: bool = False):
        super().__init__()
        self.command: str | list[str] = command
        self.verbose: bool = verbose

    def run(self, error_msg: Optional[str] = None, app_exit: bool = True) -> str:
        """runs the command"""
        formatted_command: Literal[""] = ""
        cmd_list: list = []

        if isinstance(self.command, str):
            cmd_list = self.command.split()
            formatted_command = self.command
        if isinstance(self.command, list):
            cmd_list = self.command
            formatted_command = " ".join(self.command)
        if self.verbose:
            console.print(f"Running command: {formatted_command}")
        try:
            with subprocess.Popen(
                args=cmd_list,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
            ) as run_command:
                stdout, stderr = run_command.communicate()
                if self.verbose:
                    console.print(
                        f"Output: {stdout if stdout else "Empty"}\nError: {stderr if stderr else "Empty"}"
                    )
                if run_command.returncode != 0:
                    raise subprocess.CalledProcessError(
                        returncode=run_command.returncode,
                        cmd=cmd_list,
                        stderr=(
                            f"Failed to run the command {formatted_command}. {stderr}"
                            if not error_msg
                            else error_msg
                        ),
                        output=stdout,
                    )
            return stdout.strip()
        except FileNotFoundError as _:
            self.error(message=f"{formatted_command} command not found.", app_exit=app_exit)
        except KeyboardInterrupt as _:
            self.interrupt(message="While running the command.", app_exit=app_exit)


if __name__ == "__main__":
    # Display().error("mess")
    # Network(url=None).check(to_exit=True)
    try:
        print(
            Command(command=[sys.executable, "-m", "uv", "sync", "-P", "bugx"], verbose=False).run(
                app_exit=False
            )
        )
    except KeyboardInterrupt as e:
        print(e)
    except subprocess.CalledProcessError as err:
        print(err.stderr, err.returncode)
