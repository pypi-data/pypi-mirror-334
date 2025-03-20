"""
Output formatting functions for different formats.
"""

from datetime import date, datetime
from io import StringIO
from configparser import ConfigParser
from typing import Any


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
