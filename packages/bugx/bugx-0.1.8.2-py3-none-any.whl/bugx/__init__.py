"""Init"""

import os

# import shellingham
from rich.console import Console

# from bugx.__about__ import app_name

console = Console(emoji=True)
terminal_width = console.width
HOME = os.path.expanduser("~")

# DOT_FILES: dict[str, str] = {
#     "zsh": os.path.join(HOME, ".zshr"),
#     "bash": os.path.join(HOME, ".bash_profile"),
# }


# def detect_shell():
#     """detects shell"""
#     return shellingham.detect_shell()[0]


# def write_dot_file():
#     activate: str = f"source ~/{app_name}/bin/activate"
#     if detect_shell() == "zsh":
#         print("writing")
#         with open(DOT_FILES.get("zsh"), mode="a+", encoding="utf-8") as zshrc:
#             zshrc.write(activate)
