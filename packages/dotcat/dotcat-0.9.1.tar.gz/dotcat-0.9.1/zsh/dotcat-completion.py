#!/usr/bin/env python3
"""
Dotcat completion helper script.

This script extracts dotted paths from structured data files (JSON, YAML, TOML, INI)
to provide autocompletion suggestions for the dotcat command.

Usage:
    dotcat-completion.py <file> [prefix]

Arguments:
    file:   The file to extract paths from
    prefix: Optional prefix to filter paths (e.g., "project" to get "project.name", "project.version", etc.)

Output:
    A newline-separated list of dotted paths
"""

import sys
import os
import json
from configparser import ConfigParser


def extract_paths_from_dict(data, prefix="", paths=None):
    """
    Recursively extract all possible dotted paths from a dictionary.

    Args:
        data: The dictionary to extract paths from
        prefix: The current path prefix
        paths: The set of paths found so far

    Returns:
        A set of all dotted paths in the dictionary
    """
    if paths is None:
        paths = set()

    if not isinstance(data, dict):
        return paths

    for key, value in data.items():
        # Skip numeric keys
        if isinstance(key, str) and key.isdigit():
            continue

        current_path = f"{prefix}.{key}" if prefix else key
        paths.add(current_path)

        if isinstance(value, dict):
            extract_paths_from_dict(value, current_path, paths)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    extract_paths_from_dict(item, f"{current_path}@{i}", paths)

    return paths


def parse_json(file_path):
    """Parse a JSON file and extract dotted paths."""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return extract_paths_from_dict(data)
    except json.JSONDecodeError:
        sys.stderr.write(f"Error: Unable to parse JSON file: {file_path}\n")
        return set()


def parse_yaml(file_path):
    """Parse a YAML file and extract dotted paths."""
    try:
        import yaml

        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
        return extract_paths_from_dict(data)
    except ImportError:
        sys.stderr.write(
            "Warning: PyYAML not installed. YAML completion unavailable.\n"
        )
        return set()
    except yaml.YAMLError:
        sys.stderr.write(f"Error: Unable to parse YAML file: {file_path}\n")
        return set()


def parse_toml(file_path):
    """Parse a TOML file and extract dotted paths."""
    try:
        import toml

        with open(file_path, "r") as f:
            data = toml.load(f)
        return extract_paths_from_dict(data)
    except ImportError:
        sys.stderr.write("Warning: toml not installed. TOML completion unavailable.\n")
        return set()
    except Exception:
        sys.stderr.write(f"Error: Unable to parse TOML file: {file_path}\n")
        return set()


def parse_ini(file_path):
    """Parse an INI file and extract dotted paths."""
    try:
        config = ConfigParser()
        config.read(file_path)

        paths = set()
        for section in config.sections():
            paths.add(section)
            for key in config[section]:
                paths.add(f"{section}.{key}")

        return paths
    except Exception:
        sys.stderr.write(f"Error: Unable to parse INI file: {file_path}\n")
        return set()


def get_file_parser(file_path):
    """Get the appropriate parser based on file extension."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".json":
        return parse_json
    elif ext in (".yaml", ".yml"):
        return parse_yaml
    elif ext == ".toml":
        return parse_toml
    elif ext == ".ini":
        return parse_ini
    else:
        sys.stderr.write(f"Error: Unsupported file extension: {ext}\n")
        return None


def filter_paths_by_prefix(paths, prefix):
    """Filter paths by prefix and return the next segment."""
    if not prefix:
        # If no prefix, return top-level segments
        return {path.split(".")[0] for path in paths}

    # Find paths that start with the prefix
    matching_paths = {path for path in paths if path.startswith(prefix + ".")}

    # Extract the next segment after the prefix
    next_segments = set()
    prefix_len = len(prefix) + 1  # +1 for the dot

    for path in matching_paths:
        # Get the part after the prefix
        remainder = path[prefix_len:]
        # Get the next segment (up to the next dot)
        next_segment = remainder.split(".", 1)[0]
        if next_segment:
            next_segments.add(f"{prefix}.{next_segment}")

    return next_segments


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        sys.stderr.write(__doc__)
        sys.exit(1)

    file_path = sys.argv[1]
    prefix = sys.argv[2] if len(sys.argv) > 2 else ""

    if not os.path.isfile(file_path):
        sys.stderr.write(f"Error: File not found: {file_path}\n")
        sys.exit(1)

    parser = get_file_parser(file_path)
    if not parser:
        sys.exit(1)

    paths = parser(file_path)

    if prefix:
        # If we have a prefix, filter paths and get the next segments
        suggestions = sorted(filter_paths_by_prefix(paths, prefix))
        for suggestion in suggestions:
            print(suggestion)
    else:
        # If no prefix, get top-level segments
        top_level = sorted({path.split(".")[0] for path in paths})
        for path in top_level:
            print(path)


if __name__ == "__main__":
    main()
