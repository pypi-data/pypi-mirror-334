#! /usr/bin/env python3
"""
This script reads values, including nested values, from structured data files (JSON, YAML, TOML, INI).

Usage:
    dotcat <file> <dotted-path>

Example:
    dotcat config.json python.editor.tabSize
    dotcat somefile.toml a.b.c

Exit Codes:
    2: Invalid usage (wrong number of arguments)
    3: File not found
    4: Parsing error
    5: Key not found
"""

from datetime import date, datetime
import sys
import os
import argparse
from configparser import ConfigParser
from io import StringIO
from typing import Any, Dict, List, Tuple, Union

from .__version__ import __version__

ParsedData = Union[Dict[str, Any], List[Any]]

LIST_ACCESS_SYMBOL = "@"
SLICE_SYMBOL = ":"

######################################################################
# Output formatting functions
######################################################################


def italics(text: str) -> str:
    """
    Returns the given text formatted in italics.

    Args:
        text: The text to format.

    Returns:
        The formatted text.
    """
    return f"\033[3m{text}\033[0m"


def bold(text: str) -> str:
    """
    Returns the given text formatted in bold.

    Args:
        text: The text to format.

    Returns:
        The formatted text.
    """
    return f"\033[1m{text}\033[0m"


def red(text: str) -> str:
    """
    Returns the given text formatted in red.

    Args:
        text: The text to format.

    Returns:
        The formatted text.
    """
    return f"\033[31m{text}\033[0m"


######################################################################
# Help text
######################################################################

USAGE = f"""
{bold('dotcat')}
Read values from structured data files (JSON, YAML, TOML, INI)

  Usage: dotcat <file> <dotted-path>

    <file>          The input file (JSON, YAML, TOML, INI).
    <dotted-path>   The dotted path to the desired data (e.g., project.authors).

{bold('EXAMPLES:')}
  dotcat config.json python.editor.tabSize
  dotcat pyproject.toml project.version
  dotcat package.json dependencies.react

  dotcat --version
  See `dotcat --help` for more information.
"""

HELP_CORE = (
    USAGE
    + f"""

{bold('OPTIONS:')}
  --version       Show version information
  --help          Show this help message and exit"""
)

HELP_EXAMPLE = """
    # Access data by attribute path
    dotcat data.json person.name.first

    # John
    dotcat data.json person.name.last # Doe

    # Controle your output format
    dotcat data.json person.name --output=yaml

    # name:
    #   first: John
    #   last: Doe
    dotcat data.json person.name --output=json
    # {"first": "John", "last": "Doe"}
    # List access
    dotcat data.json person.friends@0

    # {"name":{"first": "Alice", "last": "Smith"}, "age": 25} -> item access
    dotcat data.json person.friends@2:4

    # [{"name":{"first": "Alice", "last": "Smith"}, "age": 25}, {"name":{"first": "Bob", "last": "Johnson"}, "age": 30}]  -> slice access
    dotcat data.json person.friends@4:-1
"""

HELP = HELP_CORE + HELP_EXAMPLE

######################################################################
# Parsing functions
######################################################################


class ParseError(Exception):
    """Custom exception for parsing errors."""

    pass


def parse_ini(file: StringIO) -> Dict[str, Dict[str, str]]:
    """
    Parses an INI file and returns its content as a dictionary.

    Args:
        file: The file object to parse.

    Returns:
        The parsed content as a dictionary.
    """
    from configparser import ConfigParser

    config = ConfigParser()
    config.read_file(file)
    return {s: dict(config.items(s)) for s in config.sections()}


def parse_yaml(file: StringIO) -> ParsedData:
    """
    Parses a YAML file and returns its content.

    Args:
        file: The file object to parse.

    Returns:
        The parsed content.
    """
    import yaml

    try:
        return yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise ParseError(f"Unable to parse YAML file: {str(e)}")


def parse_json(file: StringIO) -> ParsedData:
    """
    Parses a JSON file and returns its content.

    Args:
        file: The file object to parse.

    Returns:
        The parsed content.
    """
    import json

    try:
        return json.load(file)
    except json.JSONDecodeError as e:
        raise ParseError(f"Unable to parse JSON file: {str(e)}")


def parse_toml(file: StringIO) -> ParsedData:
    """
    Parses a TOML file and returns its content.

    Args:
        file: The file object to parse.

    Returns:
        The parsed content.
    """
    import toml

    try:
        return toml.load(file)
    except toml.TomlDecodeError as e:
        raise ParseError(f"Unable to parse TOML file: {str(e)}")


FORMATS = [
    ([".json"], parse_json),
    ([".yaml", ".yml"], parse_yaml),
    ([".toml"], parse_toml),
    ([".ini"], parse_ini),
]


def parse_file(filename: str) -> ParsedData:
    """
    Tries to parse the file using different formats (JSON, YAML, TOML, INI).

    Args:
        filename: The name of the file to parse.

    Returns:
        The parsed content as a dictionary or list.
    """
    ext = os.path.splitext(filename)[1].lower()
    parsers = [parser for fmts, parser in FORMATS if ext in fmts]

    try:
        with open(filename, "r") as file:
            content = file.read().strip()
            if not content:
                raise ValueError("{red('[ERROR]')} {filename}: File is empty")
            for parser in parsers:
                try:
                    return parser(StringIO(content))
                except ParseError as e:
                    # Re-raise with filename for better error message
                    raise ValueError(f"{str(e)}")
                    continue
            msg = "Unsupported file format. Supported formats: JSON, YAML, TOML, INI"
            raise ValueError(f"{msg}")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {red(filename)}")
    except Exception as e:
        # Capture the original error message
        error_msg = str(e)
        if (
            "JSONDecodeError" in error_msg
            or "YAMLError" in error_msg
            or "TomlDecodeError" in error_msg
        ):
            raise ValueError("Unable to parse file")
        else:
            raise ValueError(f"Unable to parse file: {error_msg}")


######################################################################
# Formatting
######################################################################


def format_output(data: Any, output_format: str) -> str:
    """
    Formats the output based on the specified format.

    Args:
        data: The data to format.
        output_format: The format of the output.

    Returns:
        The formatted output.
    """

    if output_format == "raw":
        return str(data)
    if output_format in ("formatted", "json"):
        import json

        def date_converter(o):
            if isinstance(o, (date, datetime)):
                return o.isoformat()
            return o

        indent = 4 if output_format == "formatted" else None
        return json.dumps(data, indent=indent, default=date_converter)
    elif output_format == "yaml":
        import yaml

        return yaml.dump(data, default_flow_style=False)
    elif output_format == "toml":
        import toml

        # Check if it's a list of dicts
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            # If it's a list of dictionaries, wrap it in a dictionary with a key like "items"
            return toml.dumps({"items": data})  # Wrap the list
        else:
            return toml.dumps(data)  # Handle other cases as before

    elif output_format == "ini":
        config = ConfigParser()
        if not isinstance(data, dict) or not all(
            isinstance(v, dict) for v in data.values()
        ):
            data = {"default": data}
        for section, values in data.items():
            config[section] = values
        output = StringIO()
        config.write(output)
        return output.getvalue()
    else:
        return str(data)


######################################################################
# Data access functions
######################################################################


def access_list(data: Any, key: str, index: str) -> Any:
    """
    Accesses a list within a dictionary using a key and an index or slice.

    Args:
        data: The dictionary containing the list.
        key: The key for the list.
        index: The index or slice to access.

    Returns:
        The accessed list item or slice.
    """
    if SLICE_SYMBOL in index:
        start, end = map(lambda x: int(x) if x else None, index.split(SLICE_SYMBOL))
        return data.get(key)[start:end]
    else:
        return data.get(key)[int(index)]


def from_attr_chain(data: Dict[str, Any], lookup_chain: str) -> Any:
    """
    Accesses a nested dictionary value with an attribute chain encoded by a dot-separated string.

    Args:
        data: The dictionary to access.
        lookup_chain: The dotted-path string representing the nested keys.

    Returns:
        The value at the specified nested key, or None if the key doesn't exist.
    """
    if data is None:
        chain = lookup_chain.split(".")[0]
        raise KeyError(f"key '{chain}' not found")
    found_keys = []
    for key in lookup_chain.split("."):
        if LIST_ACCESS_SYMBOL in key:
            key, index = key.split(LIST_ACCESS_SYMBOL)
            data = access_list(data, key, index)
        else:
            data = data.get(key)
        if data is None:
            ".".join(found_keys)
            raise KeyError(f"key '{key}' not found")
        found_keys.append(key)
    return data


######################################################################
# Argument parsing, main, and run functions
######################################################################


def parse_args(args: List[str]) -> Tuple[str, str, str, bool, bool]:
    """
    Returns the filename, dotted-path, output format, and check_install flag.

    Args:
        args: The list of command-line arguments.

    Returns:
        The filename, dotted-path, output format, check_install flag, and version flag.
    """
    # Handle help commands
    if args is None or len(args) == 0:
        print(HELP)  # Show help for no arguments
        sys.exit(0)

    # Handle explicit help requests
    if "help" in args or "-h" in args or "--help" in args:
        print(HELP)  # Show help for help requests
        sys.exit(0)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("file", type=str, nargs="?", help="The file to read from")
    parser.add_argument(
        "dotted_path",
        type=str,
        nargs="?",
        help="The dotted-path to look up",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="raw",
        help="The output format (raw, formatted, json, yaml, toml, ini)",
    )
    parser.add_argument(
        "--check-install",
        action="store_true",
        help="Check if required packages are installed",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information",
    )

    parsed_args = parser.parse_args(args)
    return (
        parsed_args.file,
        parsed_args.dotted_path,
        parsed_args.output,
        parsed_args.check_install,
        parsed_args.version,
    )


def is_likely_dot_path(arg: str) -> bool:
    """
    Determines if an argument is likely a dotted-path rather than a file path.

    Args:
        arg: The argument to check.

    Returns:
        True if the argument is likely a dot path, False otherwise.
    """
    # If it contains dots and doesn't look like a file path
    if "." in arg and not os.path.exists(arg):
        # Check if it has multiple segments separated by dots
        return len(arg.split(".")) > 1
    return False


def run(args: List[str] = None) -> None:
    """
    Processes the command-line arguments and prints the value from the structured data file.

    Args:
        args: The list of command-line arguments.
    """
    # validates arguments
    filename, lookup_chain, output_format, check_install_flag, version_flag = (
        parse_args(args)
    )

    if check_install_flag:
        check_install()
        return

    if version_flag:
        print(f"dotcat version {__version__}")
        return

    # Special case: If we have only one argument and it looks like a dotted-path,
    # treat it as the dotted-path rather than the file
    if filename is not None and lookup_chain is None and len(args) == 1:
        if is_likely_dot_path(filename):
            # Swap the arguments
            lookup_chain = filename
            filename = None
            # Now filename is None and lookup_chain is not None

    # Handle cases where one of the required arguments is missing
    if lookup_chain is None or filename is None:
        if filename is not None and lookup_chain is None:
            # Case 1: File is provided but dotted-path is missing
            try:
                if os.path.exists(filename):
                    # File exists, but dotted-path is missing
                    print(
                        f"Dotted-path required. Which value do you want me to look up in {filename}?"
                    )
                    print(f"\n$dotcat {filename} {red('<dotted-path>')}")
                    sys.exit(2)  # Invalid usage
            except Exception:
                # If there's any error checking the file, fall back to general usage message
                pass
        elif filename is None and lookup_chain is not None:
            # Case 2: Dotted-path is provided but file is missing
            # Check if the argument looks like a dotted-path (contains dots)
            if "." in lookup_chain:
                # It looks like a dotted-path, so assume the file is missing
                print(
                    f"File path required. Which file contains the value at {lookup_chain}?"
                )
                print(f"\n$dotcat {red('<file>')} {lookup_chain}")
                sys.exit(2)  # Invalid usage
            # Otherwise, it might be a file without an extension or something else,
            # so fall back to the general usage message

        # General usage message for other cases
        print(USAGE)  # Display usage for invalid arguments
        sys.exit(2)  # Invalid usage

    # gets the parsed data
    try:
        data = parse_file(filename)
    except FileNotFoundError as e:
        print(str(e))
        sys.exit(3)  # File not found
    except ValueError as e:
        if "File is empty" in str(e):
            print(f"File is empty: {red(filename)}")
        elif "Unable to parse file" in str(e):
            print(f"Unable to parse file: {red(filename)}")
        else:
            print(f"{str(e)}: {red(filename)}")
        sys.exit(4)  # Parsing error

    # get the value at the specified key
    try:
        value = from_attr_chain(data, lookup_chain)
        print(format_output(value, output_format))
    except KeyError as e:
        key = e.args[0].split("'")[1] if "'" in e.args[0] else e.args[0]
        print(f"Key {red(key)} not found in {filename}")
        sys.exit(5)  # Key not found


def main() -> None:
    """
    The main entry point of the script.
    """
    run(sys.argv[1:])


def check_install():
    print("Dotcat is good to go.")
    return


if __name__ == "__main__":
    main()
