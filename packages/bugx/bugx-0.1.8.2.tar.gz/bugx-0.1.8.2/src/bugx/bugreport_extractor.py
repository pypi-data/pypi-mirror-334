"""Bugreport extractor"""

import glob
import gzip
import os
import shutil
import time
from re import Match, Pattern, compile, findall, search  # pylint: disable =W0622
from typing import Any, Callable, List, Union
from zipfile import BadZipFile, ZipFile

from InquirerPy import inquirer
from prettytable import PrettyTable
from rich.console import Console
from rich.status import Status

from bugx.utils import Display

console = Console(soft_wrap=True)
cli_display = Display()

HOME: str = os.path.expanduser(path="~")
DOWNLOADS: str = os.path.join(HOME, "Downloads")
BUGREPORT_FILE_PATTERNS: set[str] = {"*report*.zip", "*report*.gz", "*dumpstate*.zip"}
WRITE_CONSOLE_WIDTH: int = 200
LOOKUP_FOLDERS: List[str] = ["Home", "Downloads", "Documents"]

STATUS_START = "[bold green]"
STATUS_END = "[/bold green]"

FILE_HIGHLIGHT_START = "[bold magenta]"
FILE_HIGHLIGHT_END = "[/bold magenta]"

INTERRUPT_START = "[bold yellow]"
INTERRUPT_END = "[/bold yellow]"

CLI_HEADER = """
╔════════════════════════════════════════════════════════════════════════════╗
║██████╗ ██╗   ██╗ ██████╗ ██╗  ██╗████████╗██████╗  █████╗  ██████╗████████╗║
║██╔══██╗██║   ██║██╔════╝ ╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝║
║██████╔╝██║   ██║██║  ███╗ ╚███╔╝    ██║   ██████╔╝███████║██║        ██║   ║
║██╔══██╗██║   ██║██║   ██║ ██╔██╗    ██║   ██╔══██╗██╔══██║██║        ██║   ║
║██████╔╝╚██████╔╝╚██████╔╝██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗   ██║   ║
║╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ║
╚════════════════════════════════════════════════════════════════════════════╝
                                          - Developed by Govardhan Ummadisetty    
"""

PACKAGE_PATTERN = r"Package \[(.*?)\]"
VERSION_NAME_PATTERN = r"versionName=(\S+)"
VERSION_CODE_PATTERN = r"versionCode=(\d+)"
LAST_UPDATE_TIME_PATTERN = r"lastUpdateTime=([\d\- :]+)"
TIME_ZONE_PATTERN = r"mEnvironment\.getDeviceTimeZone\(\)=([\w/]+)"

device_info_patterns: dict[str, Pattern[str]] = {
    "Serial": compile(pattern=r"\[ro\.serialno\]: \[([^\]]+)\]"),
    "Manufacturer": compile(pattern=r"\[ro\.product\.manufacturer\]: \[([^\]]+)\]"),
    "Model": compile(pattern=r"\[ro\.product\.model\]: \[([^\]]+)\]"),
    "Name": compile(pattern=r"\[ro\.product\.name\]: \[([^\]]+)\]"),
    "Build": compile(pattern=r"\[ro\.build\.description\]: \[([^\]]+)\]"),
    "Fingerprint": compile(pattern=r"\[ro\.(product|system)\.build\.fingerprint\]: \[([^\]]+)\]"),
    "Build date": compile(pattern=r"\[ro\.(product|system)\.build\.date\]: \[([^\]]+)\]"),
    "SDK Version": compile(pattern=r"\[ro\.build\.version\.sdk\]: \[([^\]]+)\]"),
    "Locale": compile(pattern=r"\[ro\.product\.locale\]: \[([^\]]+)\]"),
    "Device Timezone": compile(pattern=r"mEnvironment\.getDeviceTimeZone\(\)=([\w/]+)"),
    "WIFI Country Code": compile(pattern=r"\[ro\.boot\.wificountrycode\]: \[([^\]]+)\]"),
    "CPU Architecture": compile(pattern=r"\[ro\.product\.cpu\.abi\]: \[([^\]]+)\]"),
    "SOC Manufacturer": compile(pattern=r"\[ro\.soc\.manufacturer\]: \[([^\]]+)\]"),
    "SOC Model": compile(pattern=r"\[ro\.soc\.model\]: \[([^\]]+)\]"),
    "Last Used App": compile(pattern=r"Recent #\d+: .*A=([^ ]+) "),
}

other_info_patterns: dict[str, Pattern[str]] = {
    "Android ID": compile(pattern=r"AndroidId:\s([a-zA-Z0-9]+)"),
    "Onboarded Accounts": compile(pattern=r"Account\s\{name=(.+)@gmail\.com, type=com\.google\}"),
    "Device Uptime": compile(pattern=r"Uptime:\s(.+)"),
    "Boot Reason": compile(pattern=r"\[ro\.boot\.bootreason\]: \[([^\]]+)\]"),
    "Display Device": compile(pattern=r"deviceProductInfo=\{(.+)\}"),
}

bugreports: list[str] = []


def pattern_builder(dir_name: str, patterns: set[str]) -> set[str]:
    """Generates the file patterns

    Args:
        dir_path (str): Directory Name
        patterns (set[str]) file patterns for matching

    Returns:
        set[str]: set of path with file patterns

    """
    dir_path: str = os.path.join(HOME, dir_name)
    return {os.path.join(dir_path, pattern) for pattern in patterns if pattern}


def get_bugreports(dirs: list[str] = [""]) -> dict[str, str]:  # pylint:disable=W0102
    """Fetches the list of bugreports

    Args:
        dirs (list[str]): list of Names of directory for lookup.

    Returns:
        dict[str, str]: dictionary of file name and file path
    """
    file_patterns: set[str] = set()
    for name in dirs:
        if name == "Home":
            name = ""
        file_patterns.update(pattern_builder(dir_name=name, patterns=BUGREPORT_FILE_PATTERNS))

    time_stamp: Callable[..., float] = lambda file: os.stat(
        path=file
    ).st_mtime  # pylint: disable = C3001
    for file_format in file_patterns:
        bugreports.extend(glob.glob(pathname=file_format))
    files_with_paths: List[str] = sorted(bugreports, key=time_stamp, reverse=True)
    if len(files_with_paths) == 0:
        raise FileNotFoundError(
            f"No Bugreports exists in {", ".join(dirs)} director{"ies" if len(dirs) > 1 else "y"}."
        )
    return {"/".join(file.rsplit("/", 2)[-2:]): file for file in files_with_paths}


def select_bugreport(dirs: str, select_all: bool = False) -> Union[List[str], None]:
    """Prompt the user for selection.

    Args:
        dirs (list[str]): Directory name for file lookup.

    Returns:
        Union[List[str], str]: List of selected bugreports.
    """
    key_bindings: dict[str, list[dict[str, str]]] = {
        "toggle": [{"key": "right"}, {"key": "left"}],  # toggle choice and move down (tab)
        "answer": [{"key": "enter"}],  # answer the prompt
        "interrupt": [{"key": "c-c"}],  # raise KeyboardInterrupt
        "skip": [{"key": "c-z"}],  # skip the prompt
        "toggle-all": [{"key": "space"}],  # to select all the files
    }

    try:
        bugreport_files: dict[str, str] = get_bugreports(dirs=dirs)

        file_count = len(bugreport_files)

        if len(bugreport_files) == 1:
            return list(bugreport_files.values())

        if select_all:
            console.print(
                f":point_right: :Parsing {file_count} Bugreports :package: in {", ".join(dirs)} :open_file_folder:."
            )
            return list(bugreport_files.values())

        console.print(
            f":point_right: : {file_count} Bugreports :package: listed below from {", ".join(dirs)} :open_file_folder:.\n"
        )

        selected_files = inquirer.fuzzy(  # type: ignore
            message="Select the Bugreports 📦 to proceed:",
            choices=bugreport_files,
            multiselect=True,
            keybindings=key_bindings,  # type: ignore
            mandatory=False,
            border=True,
            qmark="🚀",
            match_exact=True,
            raise_keyboard_interrupt=True,
            transformer=lambda result: (
                f"selected {f"{count} bugreports 📦" \
                if (count := len(result))> 1 else f"{count} bugreport"}."
            ),
        ).execute()

        if not selected_files:
            raise TypeError("You skipped the Bugreport 📦 selection.")

        return [bugreport_files.get(file) for file in selected_files]

    except (FileNotFoundError, TypeError) as e:
        console.print(e)
        return []
    except KeyboardInterrupt as selection_interrrupt:
        raise KeyboardInterrupt("Instead of selecting the Bugreports.") from selection_interrrupt


def _parse_file(file_path: str) -> tuple[str, str]:
    """parses the zip/gz files

    Args:
        file_path (str): zip/gz file path.
    """
    try:
        _file_path: str = ""
        if file_path.endswith(".gz"):
            tmp_file_path: str = f"{HOME}/.tmp.zip"
            with (
                open(file=tmp_file_path, mode="wb") as tmp_file,
                gzip.open(
                    filename=file_path,
                ) as tmp_zip,
            ):
                tmp_file.write(tmp_zip.read())

            _file_path = tmp_file_path
        else:
            _file_path = file_path

        with ZipFile(file=_file_path) as bugreport_file:
            raw_bugreport_txt: str = [
                _ for _ in bugreport_file.namelist() if _.startswith("bugreport")
            ][0]

            with bugreport_file.open(name=raw_bugreport_txt) as dumpstate:
                dumpstate_txt: str = dumpstate.read().decode(encoding="utf-8", errors="replace")

        return (dumpstate_txt, raw_bugreport_txt)
    except BadZipFile as _:
        cli_display.error(message=f"{file_path} is not Valid Bugreport :package:.", new_line=True)
        return ("empty", "empty")  # pylint:disable=W0101
    except (IndexError, ValueError) as _:
        cli_display.error(
            message=f"{file_path} doesn't have Bugreport files :package:.", new_line=True
        )
        return ("empty", "empty")  # pylint:disable=W0101


def _handle_device_info(info_txt: str) -> dict:
    """Fetches device info from the dumpstate text.

    Args:
        info_txt (str): dumpstate text.

    Returns:
        dict: device info.
    """
    device_info: dict[Any, Any] = {}

    for info, pattern in device_info_patterns.items():
        match: Match[str] | None = search(pattern=pattern, string=info_txt)
        if match:
            if info in ("Fingerprint", "Build date"):
                device_info[info] = match.group(2)
            else:
                device_info[info] = match.group(1)

    return device_info


def _handle_other_info(info_txt: str) -> dict:
    """Fetches other info from the dumpstate text.

    Args:
        info_txt (str): dumpstate text.

    Returns:
        dict: other info.
    """
    other_info: dict[Any, Any] = {}

    for info, pattern in other_info_patterns.items():
        if info == "Onboarded Accounts":
            accounts: list = []
            match: list[Any] = findall(pattern=pattern, string=info_txt)
            for acc in match:
                if acc not in accounts and not acc.startswith("Account") and acc.count("type=") < 1:
                    accounts.append(acc)
            other_info[info] = accounts
        else:
            match: Match[str] | None = search(pattern=pattern, string=info_txt)
            if match:
                other_info[info] = match.group(1)

    return other_info


def _handle_packages(info_txt: str) -> list[dict[str, Union[str, Any]]]:
    """Fetches the package name, version name, version code and last updatetime.

    Args:
        info_txt (str): dumpstate text

    Returns:
        list[dict[str, Union[str, Any]]]: package list.
    """
    package_info_list: list[Any] = []

    blocks: list[str] = info_txt.split(sep="Package [")

    for block in blocks[1:]:  # Skip the first split part as it does not contain a package
        block: str = (  # type: ignore
            "Package [" + block
        )  # Adding back the "Package [" for consistency

        package: Match[str] | None = search(pattern=PACKAGE_PATTERN, string=block)
        version_name: Match[str] | None = search(pattern=VERSION_NAME_PATTERN, string=block)
        version_code: Match[str] | None = search(pattern=VERSION_CODE_PATTERN, string=block)
        last_update_time: Match[str] | None = search(pattern=LAST_UPDATE_TIME_PATTERN, string=block)

        if package and version_name and version_code and last_update_time:
            package_info_list.append(
                {
                    "package": package.group(1),
                    "versionName": version_name.group(1),
                    "versionCode": version_code.group(1),
                    "lastUpdateTime": last_update_time.group(1),
                }
            )
    return package_info_list


def get_aligned(section_name: str, section_data: dict, ignore_values: list) -> str:
    """aligns the data"""
    multiplier = 20
    table = PrettyTable(border=False, header=False, padding_width=1, align="l")
    res = f"\n{"-"*multiplier} {section_name.title()} {"-"*multiplier}\n"

    for key, value in section_data.items():
        if value in ignore_values:
            continue
        table.add_row([key, f": {value}"])

    res += table.get_string()
    res += f"\n{"-"*(2*multiplier + len(section_name) + 2)}\n"

    return res


def _generate_files(
    dumpstate_text: str, parsed_output_text: str, file_name: str, copy_file: bool = True, **kwargs
):
    """Generates the rawbugreport and packageversion text files.

    Args:
        dumpstate_text (str): dumpstate text.
        parsed_output_text (str): text after parsing the raw dumpstate text.
        file_name (str): file name to be stored.
        copy_file (bool): copies the file into generated folder.

    Returns:
        str: folder_path
    """
    destination_root: str = f"{HOME}/reports"
    folder_path: str = os.path.join(
        destination_root, file_name.replace("bugreport", "processed-bugreport").strip(".txt")
    )
    raw_bugreport_file_path = os.path.join(folder_path, file_name)
    package_version_file_name = file_name.replace("bugreport", "package-versions")
    package_version_file_path = os.path.join(folder_path, package_version_file_name)

    os.makedirs(name=destination_root, exist_ok=True)

    os.makedirs(name=folder_path, exist_ok=True)

    with open(file=raw_bugreport_file_path, mode="w", encoding="utf-8") as write_raw_bugreport:
        write_raw_bugreport.write(dumpstate_text)

    with open(file=package_version_file_path, mode="w", encoding="utf-8") as package_versions:
        package_versions.write(parsed_output_text)

    if copy_file:
        main_file = kwargs.get("file_path")
        shutil.copy(main_file, folder_path)

    return folder_path


def parse_bugreport(file_path: str, display: bool) -> str:
    """Parses the bugreport file

    Args:
        file_path (str): file path.
    """

    dumpstate_text, file_name = _parse_file(file_path=file_path)

    if dumpstate_text == "empty" or file_name == "empty":
        return "empty"

    device_info: dict[Any, Any] = _handle_device_info(info_txt=dumpstate_text)

    other_info: dict[Any, Any] = _handle_other_info(info_txt=dumpstate_text)

    package_info_list: List[dict[str, str | Any]] = _handle_packages(info_txt=dumpstate_text)

    table = PrettyTable()
    table.field_names = ["Package", "Version Name", "Version Code", "Last Updated time"]
    table.sortby = "Package"
    table.align = "l"
    # table._max_width = {"Version Name": 60}  # pylint: disable=W0212

    table.add_rows(rows=[list(pkg.values()) for pkg in package_info_list if pkg])

    table.title = f"List of packages in the {str(object=device_info.get("Name").title())} device"

    device_info_str = get_aligned(
        section_name="device info", section_data=device_info, ignore_values=[]
    )

    other_info_str = get_aligned(
        section_name="other info", section_data=other_info, ignore_values=["relativeAddress=[]"]
    )

    if display:
        console.print(CLI_HEADER, justify="right")
        console.print(
            device_info_str,
        )
        console.print(other_info_str)
        console.print(table, justify="center")

    write_console = Console(width=WRITE_CONSOLE_WIDTH, soft_wrap=True)

    with write_console.capture() as capture:
        write_console.print(CLI_HEADER, justify="right", highlight=False, width=180)
        write_console.print(device_info_str, highlight=False)
        write_console.print(other_info_str, highlight=False)
        write_console.print(table, highlight=False, justify="center", overflow="fold")

    parsed_output = capture.get()

    stored_path = _generate_files(
        dumpstate_text=dumpstate_text,
        parsed_output_text=parsed_output,
        file_name=file_name,
        file_path=file_path,
    )

    return stored_path


def for_cli(override: bool = False, select_all: bool = False):
    """select cli"""
    try:
        files: List[str] | str = select_bugreport(dirs=LOOKUP_FOLDERS, select_all=select_all)
        to_display: bool = True

        if (count := len(files)) > 1:
            status_message = f"{STATUS_START}Parsing {count} bugreports...{STATUS_END}"
            to_display = False
        else:
            status_message = f"{STATUS_START}Parsing {count} bugreport...{STATUS_END}"
            to_display = True

        with console.status(status=status_message) as cli_status:
            console.print("")
            cli_status.start()
            time.sleep(1)
            for file in files:
                cli_status.update(
                    status=f"{STATUS_START}Parsing {FILE_HIGHLIGHT_START}{file.rsplit("/")[-1]}{FILE_HIGHLIGHT_END}.{STATUS_END}"
                )
                time.sleep(2)
                stored_path = parse_bugreport(file_path=file, display=to_display or override)
                if to_display:
                    console.print("\n")
                if stored_path != "empty":
                    console.print(
                        f":open_file_folder: :{STATUS_START}Processed in {FILE_HIGHLIGHT_START}{stored_path}{STATUS_END}{FILE_HIGHLIGHT_END}."
                    )
                    console.print("")
    except KeyboardInterrupt as cli_interrupt:
        raise KeyboardInterrupt(cli_interrupt) from cli_interrupt


def for_watch_cli(file_path: str, cli_status: Status, override: bool = False):
    """for cli watch"""
    try:
        files: List[str] = [file_path]
        for file in files:
            cli_status.update(" ")
            console.print("\n")
            stored_path: str = parse_bugreport(file_path=file, display=override)
            if stored_path != "empty":
                console.print(
                    f"\n:open_file_folder: :{STATUS_START}Processed in {FILE_HIGHLIGHT_START}{stored_path}{STATUS_END}{FILE_HIGHLIGHT_END}."
                )
        cli_status.update(" ")
        console.print("\n")
    except KeyboardInterrupt as cli_interrupt:
        raise KeyboardInterrupt(cli_interrupt) from cli_interrupt


if __name__ == "__main__":
    parse_bugreport(
        file_path="/Users/govardhanu/Downloads/bugreport-sabrina-STTL.241013.003-2025-03-10-17-58-44.zip",
        display=True,
    )
