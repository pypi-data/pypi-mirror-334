"""cli constants"""

from dataclasses import dataclass
from typing import ClassVar

from bugx import terminal_width
from bugx.__about__ import (
    __version__,
    app_name,
    author,
    description_color,
    short_description_color,
)


@dataclass
class CliApplication:
    """CLI Application params"""

    EPILOG: ClassVar[str] = (
        f"""\n{":pleading_face: : Please Maximize the terminal for Better Experience.\n\n" if terminal_width <= 70 else ""}[bold yellow]Developed by {author} :sunglasses:.[/bold yellow]"""
    )
    DESCRIPTION: ClassVar[str] = (
        description_color if terminal_width >= 80 else short_description_color
    )
    JUSTIFY: ClassVar[str] = "center" if terminal_width >= 80 else "left"
    VERSION: ClassVar[str] = __version__
    APP_NAME: ClassVar[str] = app_name.title()
    VERSION_FLAG_HELP: ClassVar[str] = "Prints the Version and Changelog."


@dataclass
class SelectOption:
    """Select Option params"""

    OPTION_NAME: ClassVar[str] = "select"

    SHORT_HELP: ClassVar[str] = "Prompts the users to select the Bugreports."

    EXAMPLES: ClassVar[
        str
    ] = f"""
    
 {app_name.title()} will prompts the user to select the files using Right/Left arrow to select/unselect, Up/Down to navigate.\
 Press ENTER after selecting the files.\n\n
   
 Examples:
 
     $ {app_name} {OPTION_NAME} --display
     $ {app_name} {OPTION_NAME} -d
     
     $ {app_name} {OPTION_NAME} --all
     $ {app_name} {OPTION_NAME} -a
     
 Recommended to use :  {app_name} {OPTION_NAME} -d
    """

    DISPLAY_FLAG_HELP: ClassVar[str] = "Displays the output in the terminal."
    ALL_FLAG_HELP: ClassVar[str] = "Parses all Bugreports."
    INTERRUPT_MESSAGE: ClassVar[str] = f"while running {OPTION_NAME} Operation."


@dataclass
class ParseOption:
    """parse option"""

    SHORT_HELP: ClassVar[str] = "Allows user to drag and drop the Bugreports."
    EXAMPLES: ClassVar[
        str
    ] = f"""
    
 Allows the user to drag and drop the Bugreports.\n\n
   
 Examples:
 
     $ {app_name} parse --display
     $ {app_name} parse -d
     
     $ {app_name} select --all
     $ {app_name} select -a
     
 Recommended to use :  {app_name} parse -d
    """
    DISPLAY_FLAG_HELP: ClassVar[str] = "Displays the output in the terminal."


@dataclass
class WatchOption:
    """watch option"""

    OPTION_NAME: ClassVar[str] = "watch"

    SHORT_HELP: ClassVar[str] = "Looks for newly added/downloaded Bugreports."
    EXAMPLES: ClassVar[
        str
    ] = f"""
    
 {app_name.title()} automatically looks for new bugreports in both Downloads & Documents folders.
 If a new bugreport added/downloaded/dropped into any of the two folders it will be automatically processed.\n\n
   
 Examples:
 
     $ {app_name} {OPTION_NAME} --display
     $ {app_name} {OPTION_NAME} -d

 Recommended to use :  {app_name} {OPTION_NAME} -d
    """
    DISPLAY_FLAG_HELP: ClassVar[str] = "Displays the output in the terminal."
    INTERRUPT_MESSAGE: ClassVar[str] = f"while running {OPTION_NAME} Operation."


@dataclass
class UpdateOption:
    """Update option"""

    OPTION_NAME: ClassVar[str] = "update"

    SHORT_HELP: ClassVar[str] = f"Updates the {app_name.title()} to the Latest version."
    EXAMPLES: ClassVar[
        str
    ] = f"""
    
 {app_name.title()} automatically looks for new bugreports in both Downloads & Documents folders.
 If a new bugreport added/downloaded/dropped into any of the two folders it will be automatically processed.\n\n
   
 Examples:
 
     $ {app_name} {OPTION_NAME}

 Recommended to use :  {app_name} {OPTION_NAME}
    """
    INTERRUPT_MESSAGE: ClassVar[str] = f"while running {OPTION_NAME} Operation."
