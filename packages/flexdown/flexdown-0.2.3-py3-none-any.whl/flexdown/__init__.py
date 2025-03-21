"""Flexdown is a superset of Markdown for creating Reflex-powered docs."""

from pathlib import Path

import reflex as rx

from . import namespace
from .document import Document
from .flexdown import Flexdown

# The default Flexdown instance.
flexdown = Flexdown()


def parse(source: str) -> Document:
    """Parse a Flexdown document.

    Args:
        source: The source code of the Flexdown document.

    Returns:
        The parsed Flexdown document.
    """
    return Document.from_source(source)


def render(source: str, **kwargs) -> rx.Component:
    """Render Flexdown source code into a Reflex component.

    Args:
        source: The source code of the Flexdown file.
        **kwargs: The keyword arguments to pass to the Flexdown constructor.

    Returns:
        The Reflex component representing the Flexdown file.
    """
    return Flexdown(**kwargs).render(source)


def render_file(path: str | Path, **kwargs) -> rx.Component:
    """Render a Flexdown file into a Reflex component.

    Args:
        path: The path to the Flexdown file.
        **kwargs: The keyword arguments to pass to the Flexdown constructor.

    Returns:
        The Reflex component representing the Flexdown file.
    """
    return Flexdown(**kwargs).render_file(path)


__all__ = ["app", "flexdown", "namespace", "parse", "render", "render_file"]
