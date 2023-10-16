"""helper module for testing and validation stuff"""
from typing import Any


def parse_categories(categories: dict[str, Any]) -> list[list[str]]:
    """
    parse the categories portion in the news site config files to list of lists
    (to help validation purpose)
    """
    paths = []
    stack: list[tuple[list[str], dict[str, Any]]] = [([], categories)]

    while stack:
        curr_path, curr_dict = stack.pop()
        for key, val in curr_dict.items():
            new_path = curr_path + [key]

            paths.append(new_path)

            if isinstance(val, dict):
                stack.append((new_path, val))

    return paths
