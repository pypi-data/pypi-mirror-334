"""About"""

from typing import LiteralString

from bugx import console

__all__: list[str] = ["__version__", "author", "app_name", "description"]

__version__ = "0.1.8.1"
author: LiteralString = "Govardhan Ummadisetty"
app_name: LiteralString = "bugx"
description: LiteralString = """
╔════════════════════════════════════════════════════════════════════════════╗
║██████╗ ██╗   ██╗ ██████╗ ██╗  ██╗████████╗██████╗  █████╗  ██████╗████████╗║
║██╔══██╗██║   ██║██╔════╝ ╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝║
║██████╔╝██║   ██║██║  ███╗ ╚███╔╝    ██║   ██████╔╝███████║██║        ██║   ║
║██╔══██╗██║   ██║██║   ██║ ██╔██╗    ██║   ██╔══██╗██╔══██║██║        ██║   ║
║██████╔╝╚██████╔╝╚██████╔╝██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗   ██║   ║
║╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ║
╚════════════════════════════════════════════════════════════════════════════╝
                 A simple CLI tool for Bug report Extraction"""


description_color: LiteralString = """
[bold blue]╔════════════════════════════════════════════════════════════════════════════╗
║[bold green]██████╗ ██╗   ██╗ ██████╗ ██╗  ██╗████████╗██████╗  █████╗  ██████╗████████╗[/bold green]║
║[bold green]██╔══██╗██║   ██║██╔════╝ ╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝[/bold green]║
║[bold yellow]██████╔╝██║   ██║██║  ███╗ ╚███╔╝    ██║   ██████╔╝███████║██║        ██║   [/bold yellow]║
║[bold yellow]██╔══██╗██║   ██║██║   ██║ ██╔██╗    ██║   ██╔══██╗██╔══██║██║        ██║[/bold yellow]   ║
║[bold red]██████╔╝╚██████╔╝╚██████╔╝██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗   ██║[/bold red]   ║
║[bold red]╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   [/bold red]║
╚════════════════════════════════════════════════════════════════════════════╝[/bold blue]
[bold bright_white]        A simple CLI tool for Bug report Extraction[/bold bright_white]"""

short_description: LiteralString = r"""
   ___            _  ____               __ 
  / _ )__ _____ _| |/_/ /________ _____/ /_
 / _  / // / _ `_>  </ __/ __/ _ `/ __/ __/
/____/\_,_/\_, /_/|_|\__/_/  \_,_/\__/\__/ 
          /___/                            
A simple CLI tool for Bug report Extraction
"""

short_description_color: LiteralString = r"""
[bold italic red]   ___            _  ____               __ [/bold italic red]
[bold italic yellow]  / _ )__ _____ _| |/_/ /________ _____/ /_ [/bold italic yellow]
[bold italic green] / _  / // / _ `_>  </ __/ __/ _ `/ __/ __/ [/bold italic green]
[bold italic blue]/____/\_,_/\_, /_/|_|\__/_/  \_,_/\__/\__/ [/bold italic blue]
[bold italic magenta]          /___/                         [/bold italic magenta]   
[bold white]A simple CLI tool for Bug report Extraction [/bold white]
"""


def version():
    """version"""
    from bugx.cli_constants import CliApplication  # pylint:disable=C0415
    from bugx.updater import get_changelog  # pylint:disable=C0415

    console.print(f"{CliApplication.DESCRIPTION}\n", justify=CliApplication.JUSTIFY)
    console.print(f":sparkles: {CliApplication.APP_NAME} version {CliApplication.VERSION}")
    get_changelog(app_exit=False)
    console.print(CliApplication.EPILOG)


if __name__ == "__main__":
    version()
