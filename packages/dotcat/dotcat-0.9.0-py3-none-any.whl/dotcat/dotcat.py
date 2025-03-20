#! /usr/bin/env python3
"""
This script reads values, including nested values, from structured data files (JSON, YAML, TOML, INI).

Usage:
    dotcat <file> <dot_separated_key>

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

ParsedData = Union[Dict[str, Any], List[Any]]

LIST_ACCESS_SYMBOL = '@'
SLICE_SYMBOL = ':'

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


USAGE = f"""
{bold('dotcat')}
Read values, including nested values, from structured data files (JSON, YAML, TOML, INI)

{bold('USAGE:')}
dotcat <file> <dot_separated_key>

{bold('EXAMPLE:')}
dotcat config.json python.editor.tabSize
dotcat somefile.toml a.b.c
"""

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
        raise ParseError(
            f"[ERROR] {file.name}: Unable to parse YAML file: {str(e)}")


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
        raise ParseError(
            f"[ERROR] {file.name}: Unable to parse JSON file: {str(e)}")


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
        raise ParseError(
            f"[ERROR] {file.name}: Unable to parse TOML file: {str(e)}")


FORMATS = [
    (['.json'], parse_json),
    (['.yaml', '.yml'], parse_yaml),
    (['.toml'], parse_toml),
    (['.ini'], parse_ini)
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
        with open(filename, 'r') as file:
            content = file.read().strip()
            if not content:
                raise ValueError(f"[ERROR] {filename}: File is empty")
            for parser in parsers:
                try:
                    return parser(StringIO(content))
                except ParseError:
                    continue
            msg = "Unsupported file format. Supported formats: JSON, YAML, TOML, INI"
            raise ValueError(f"[ERROR] { filename}:{msg} ")
    except FileNotFoundError:
        raise FileNotFoundError(f"[ERROR] {filename}: File not found")
    except Exception as e:
        raise ValueError(f"[ERROR] {filename}: Unable to parse file: {str(e)}")

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

    if output_format == 'raw':
        return str(data)
    if output_format in ('formatted', 'json'):
        import json

        def date_converter(o):
            if isinstance(o, (date, datetime)):
                return o.isoformat()
            return o

        indent = 4 if output_format == 'formatted' else None
        return json.dumps(data, indent=indent, default=date_converter)
    elif output_format == 'yaml':
        import yaml
        return yaml.dump(data, default_flow_style=False)
    elif output_format == 'toml':
        import toml
        # Check if it's a list of dicts
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            # If it's a list of dictionaries, wrap it in a dictionary with a key like "items"
            return toml.dumps({"items": data})  # Wrap the list
        else:
            return toml.dumps(data)  # Handle other cases as before

    elif output_format == 'ini':
        config = ConfigParser()
        if not isinstance(data, dict) or not all(isinstance(v, dict) for v in data.values()):
            data = {'default': data}
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
        adict: The dictionary to access.
        lookup_path: The dot-separated string representing the nested keys.

    Returns:
        The value at the specified nested key, or None if the key doesn't exist.
    """
    if data is None:
        chain = lookup_chain.split('.')[0]
        raise KeyError(
            f"[ERROR] key '{bold({chain})}' not found in {italics('')}")
    found_keys = []
    for key in lookup_chain.split('.'):
        if LIST_ACCESS_SYMBOL in key:
            key, index = key.split(LIST_ACCESS_SYMBOL)
            data = access_list(data, key, index)
        else:
            data = data.get(key)
        if data is None:
            keys = '.'.join(found_keys)
            raise KeyError(f"[ERROR] key '{key}' not found in { keys}")
        found_keys.append(key)
    return data

######################################################################
# Argument parsing, main, and run functions
######################################################################


def parse_args(args: List[str]) -> Tuple[str, str, str, bool]:
    """
    Returns the filename, lookup chain, output format, and check_install flag.

    Args:
        args: The list of command-line arguments.

    Returns:
        The filename, lookup chain, output format, and check_install flag.
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('file', type=str, nargs='?', help='The file to read from')
    parser.add_argument('dot_separated_key', type=str, nargs='?', help='The dot-separated key to look up')
    parser.add_argument('--output', type=str, default='raw', help='The output format (raw, formatted, json, yaml, toml, ini)')
    parser.add_argument('--check-install', action='store_true', help='Check if required packages are installed')

    if args is None or len(args) < 1:
        print(USAGE)
        sys.exit(2)

    parsed_args = parser.parse_args(args)
    return parsed_args.file, parsed_args.dot_separated_key, parsed_args.output, parsed_args.check_install

def run(args: List[str] = None) -> None:
    """
    Processes the command-line arguments and prints the value from the structured data file.

    Args:
        args: The list of command-line arguments.
    """
    # validates arguments
    filename, lookup_chain, output_format, check_install_flag = parse_args(args)

    if check_install_flag:
        check_install()
        return

    # gets the parsed data
    try:
        data = parse_file(filename)
    except FileNotFoundError as e:
        print(e)
        sys.exit(3)  # File not found
    except ValueError as e:
        print(e)
        sys.exit(4)  # Parsing error

    # get the value at the specified key
    try:
        value = from_attr_chain(data, lookup_chain)
        print(format_output(value, output_format))
    except KeyError as e:
        print(f"[ERROR] {filename}: " + e.args[0].strip('"'))
        sys.exit(5)  # Key not found


def main() -> None:
    """
    The main entry point of the script.
    """
    run(sys.argv[1:])

def check_install():
    import json, yaml, toml
    print("Dotcat is good to go.")
    return

if __name__ == '__main__':
    main()
