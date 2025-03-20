"""
Data access functions for dotcat.
"""

from typing import Any, Dict

LIST_ACCESS_SYMBOL = "@"
SLICE_SYMBOL = ":"


def access_list(data: Any, key: str, index: str) -> Any:
    """
    Accesses a list within a dictionary using a key and an index or slice.

    Args:
        data: The dictionary containing the list.
        key: The key for the list.
        index: The index or slice to access.

    Returns:
        The accessed list item or slice.

    Raises:
        KeyError: If the index is invalid or the data is not a list.
    """
    try:
        if SLICE_SYMBOL in index:
            start, end = map(lambda x: int(x) if x else None, index.split(SLICE_SYMBOL))
            return data.get(key)[start:end]
        else:
            return data.get(key)[int(index)]
    except (IndexError, TypeError) as e:
        raise KeyError(f"Invalid index '{index}' for key '{key}': {str(e)}")


def from_attr_chain(data: Dict[str, Any], lookup_chain: str) -> Any:
    """
    Accesses a nested dictionary value with an attribute chain encoded by a dot-separated string.

    Args:
        data: The dictionary to access.
        lookup_chain: The dotted-path string representing the nested keys.

    Returns:
        The value at the specified nested key, or None if the key doesn't exist.
    """
    keys = lookup_chain.split(".")
    found_keys = []

    if data is None:
        chain = keys[0]
        raise KeyError(f"key '{chain}' not found")

    for key in keys:
        if LIST_ACCESS_SYMBOL in key:
            key, index = key.split(LIST_ACCESS_SYMBOL)
            data = access_list(data, key, index)
        else:
            data = data.get(key)
        if data is None:
            full_path = ".".join(found_keys + [key])
            raise KeyError(f"key '{key}' not found in path '{full_path}'")
        found_keys.append(key)
    return data
