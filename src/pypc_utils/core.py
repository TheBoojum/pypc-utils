"""
This library contains various generic utility functions
"""

import getpass
import json
import os
import subprocess
import sys
import winsound
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from time import sleep

# #############################################################################
# Classes and similar
# #############################################################################


class RunMode(Enum):
    """
    Enum represeting the run mode.
    """

    INTERACTIVE = "interactive"
    NATIVE = "native"
    STANDARD = "standard"
    POWERSHELL = "powershell"


# #############################################################################
# Funtions
# #############################################################################


# .............................................................................
def format_timedelta(td: timedelta) -> str:
    """
    Format any timedelta into hh:mm:ss.sss,
    where .sss is three-digit milliseconds.

    Args:
        td (timedelta): The duration

    Returns:
        str: The duration in format 'HH:MM:SS.sss'
    """
    # Total milliseconds (exact integer)
    total_ms = td.days * 86400_000 + td.seconds * 1_000 + td.microseconds // 1_000

    hours, rem_ms = divmod(total_ms, 3_600_000)
    minutes, rem_ms = divmod(rem_ms, 60_000)
    seconds, milliseconds = divmod(rem_ms, 1_000)

    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"


# .............................................................................
def spawn_powershell_tail(logfile: str) -> subprocess:
    """
    Creates a separate window in which to display the progressbars.

    Args:
            logfile (str): The filename of the temporary log

    Returns:
            subprocess: The windows process that manages the progressbar
            windows
    """
    cmd = [
        "cmd.exe",
        "/c",
        "start",
        "powershell",
        "-NoExit",
        "-Command",
        f"Get-Content -Path '{logfile}' -Wait -Tail 0",
    ]

    return subprocess.Popen(cmd)


# .............................................................................
def import_list(list_path: Path) -> list[str]:
    """
    Generic function to read a file and return the contents as a list.

    Args:
        list_path (Path): The full path to the list file

    Returns:
        list[str]: The list of lines in the file
    """
    lst = []

    with list_path.open("r", encoding="utf-8") as f:
        for line in f:
            lst.append(line.rstrip("\n"))

    return lst


# .............................................................................
def load_sql_library(sql_module_list: list[str], library_path: Path) -> dict:
    """
    Creates a dictionary, key on module name, of the required SQL modules.

    Args:
        library_path (Path): The path to the library folder
        sql_module_list (list[str]): The list of modules to be loaded

    Returns:
        dict: The SQL code library

    Notes:
        Requires the following:
        A folder containing the SQL code, e.g. project/sqlite
        A file listing the SQL code to be imported, e.g.
            resources/lists/sql_modules.txt
    """
    this_dict = {}

    for sql_module in sql_module_list:
        this_dict[sql_module] = load_sql_module(library_path, sql_module)

    return this_dict


# .............................................................................
def load_sql_module(sql_code_path: Path, name: str) -> str:
    """
    Returns the 'name' SQL code from the SQL code library.

    Args:
        sql_code_path (Path): The path to the SQL code library
        name (str): The name of the SQL module

    Returns:
        str: The SQL code
    """
    sql_path = Path.resolve(sql_code_path / f"{name}.sql")
    return sql_path.read_text()


# .............................................................................
def end_script(start_time: datetime) -> None:
    """
    Generic end-of-script function to make a noise and display the execution
    time stats.

    Args:
        start_time (datetime): The time at which the script started
    """
    winsound.Beep(440, 250)
    sleep(0.05)
    winsound.Beep(600, 250)
    sleep(0.05)

    # Stop Timer
    finish_time = datetime.now()
    elapsed_time = finish_time - start_time
    print(
        f"\n{'-'*40}\n"
        "End of Script\n"
        f"{'-'*40}\n"
        f"Start time: {start_time.strftime('%H:%M:%S - %d-%b-%Y')}\n"
        f"End time:   {finish_time.strftime('%H:%M:%S - %d-%b-%Y')}\n"
        f"Run time:   {str(elapsed_time).split('.', maxsplit=1)[0]}\n"
        f"{'-'*40}\n"
    )


# .............................................................................
def cv_datetime(dt_string: str) -> str:
    """
    Converts a standard-format date/time sting into a friendly format.

    Args:
        dt_string (str): A string date in the ISO-8601 format, e.g.
        '2022-04-05T20:29:40.177Z'

    Returns:
        str: A string date in the format 'dd-mmm-yyyy, hh:mm'
    """
    dt = datetime.strptime(dt_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.strftime("%d-%b-%Y, %H:%M")


# .............................................................................
def run_mode() -> RunMode:
    """
    Identifies whether the script is running under NATIVE Python or an
    INTERACTIVE Jupyter envionment.

    Returns:
        RunMode: The run environment
    """
    return RunMode.INTERACTIVE if hasattr(sys, "ps1") else RunMode.NATIVE


# .............................................................................
def check_or_make_dir(p_path: Path) -> None:
    """
    Tries to create the specified directory. Indicates the (quite legitmate -
    it doesn't need to be created) reason for failure.

    Args:
        pPath (Path): The folder to be created
    """
    # Try to create the directory
    try:
        p_path.mkdir(parents=True, exist_ok=False)
        print(f"Directory '{p_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{p_path}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{p_path}'.")


# .............................................................................
def split_all(p_path: Path) -> list[str]:
    """
    Splits a path into a list of its constituent segments.

    Args:
        p_path (Path): The path to be parsed.

    Returns:
        list[str]: A list of the path segments.
    """
    l_path = p_path
    allparts = []

    while 1:
        parts = os.path.split(l_path)
        if parts[0] == p_path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
        elif parts[1] == p_path:  # sentinel for relative paths
            allparts.insert(0, parts[1])
        else:
            l_path = parts[0]
            allparts.insert(0, parts[1])

    return allparts


# .............................................................................
def text_to_camel(p_text: str) -> str:
    """
    Converts a string to Camel case, with spaces converted to underscore.

    Args:
        p_text (str): The source text.

    Returns:
        str: The text in camel case.
    """
    return p_text.lower().replace(" ", "_")


# .............................................................................
def list_env_vars() -> dict:
    """
    Writes the full list of environment variables to a dictionary.

    Returns:
        dict: A dictionary containing the environment names and values.
    """
    this_dict = {}

    for name, value in os.environ.items():
        this_dict[name] = value

    return this_dict


# .............................................................................
def dict_to_json(p_dict: dict, p_path: Path) -> None:
    """
    Writes a dictionary to the specified path, in JSON format.

    Args:
        p_dict (dict): The dictionary to be exported.
        p_path (Path): The path to which it is to be written.
    """
    json_object = json.dumps(p_dict, indent=4)

    with p_path.open("w", encoding="utf-8") as outfile:
        outfile.write(json_object)


# .............................................................................
def print_current_user() -> None:
    """
    Prints user account information.
    """

    print("os.getlogin():       ", os.getlogin())
    print("getpass.getuser():   ", getpass.getuser())
    print("USER env var:        ", os.environ.get("USERNAME"))
