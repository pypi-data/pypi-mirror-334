"""Utility functions for Flexdown."""

import hashlib
import os
import re
from pathlib import Path
from typing import Sequence

import reflex as rx

from flexdown import constants, types

from .document import Document


def parse_file(path: str | Path) -> Document:
    """Parse a Flexdown file.

    Args:
        path: The path to the Flexdown file.

    Returns:
        The parsed Flexdown document.
    """
    return Document.from_file(path)


def get_flexdown_files(
    path: str | Path, str_output: bool = False
) -> Sequence[str] | Sequence[Path]:
    """Recursively get the Flexdown files in a directory.

    Args:
        path: The path to the directory to search.
        str_output: Whether to return the paths as strings.

    Returns:
        The list of Flexdown files in the directory.
    """
    path = Path(path)
    flexdown_files = []
    for root, _, files in os.walk(path):
        root = Path(root)
        flexdown_files.extend(
            [
                root / file if not str_output else str(root / file)
                for file in files
                if file.endswith(constants.FLEXDOWN_EXTENSION)
            ]
        )
    return flexdown_files


def evaluate_templates(line: str, env: types.Env):
    """Evaluate template expressions in a line of text.

    Args:
        line: The line of text to evaluate.
        env: The environment variables to use for evaluation.
    """
    if line.startswith("<!--") and line.endswith("-->"):
        return line

    # Find all template placeholders in the line.
    matches = re.findall(constants.TEMPLATE_REGEX_WITHOUT_ESCAPE, line)

    # Iterate over each template placeholder.
    match = None
    try:
        for match in matches:
            # Evaluate the Python expression and replace the template placeholder
            eval_result = str(eval(match, env, env))
            line = line.replace("{" + match + "}", eval_result)
    except Exception:
        # If the evaluation fails, leave the template placeholder unchanged
        return line

    matches_with_escape = re.findall(constants.TEMPLATE_REGEX, line)

    for match in matches_with_escape:
        line = line.replace("\\{" + match + "}", "{" + match + "}")

    # Return the line with the template placeholders replaced.
    return line


def get_id(s: str) -> str:
    """Get a unique ID for a string."""
    hash_object = hashlib.sha256(s.encode())
    hex_dig = hash_object.hexdigest()
    return "_" + hex_dig


def get_route_from_filepath(
    file: str | Path, root_path: str | Path | None = None
) -> str:
    """Get the route from a file path."""
    file = Path(file)
    if root_path:
        root_path = Path(root_path)
        route = file.relative_to(root_path)
    else:
        route = file
    route = route.with_suffix("")
    route = str(route).replace(".md", "")
    return f"/{route}"


def google_fonts():
    """Get the Google Fonts link tags."""
    return [
        rx.el.link(
            rel="preconnect",
            href="https://fonts.googleapis.com",
        ),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            crossorigin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&family=Space+Mono:ital,wght@0,400;0,700;1,400;1,700&family=IBM+Plex+Mono:ital,wght@0,500;0,600;1,600&family=Source+Code+Pro:wght@400;500&display=swap&family=JetBrains+Mono:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ]
