"""Flexdown documents."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import reflex as rx
import yaml

from flexdown import constants, types


class Document(rx.Base):
    """A Flexdown document."""

    # Document metadata in the flexdown frontmatter.
    metadata: dict[str, Any] = {}

    # The content of the document.
    content: str

    # Filename if the document is from a file.
    filename: str | None = None

    @staticmethod
    def parse_front_matter(source: str) -> tuple[types.FrontMatter, str]:
        """Parse the front matter and content from a source string."""
        # Extract the front matter and content using the pattern
        match = re.match(constants.FRONT_MATTER_REGEX, source, re.DOTALL)

        # If there is no front matter, return an empty dictionary
        if not match:
            return {}, source

        # Get the front matter and content
        front_matter = yaml.safe_load(match.group(1))
        content = match.group(2)
        return front_matter, content

    @classmethod
    def from_source(cls, source: str) -> Document:
        """Create a document from a source string.

        Args:
            source: The source string of the document.

        Returns:
            The document.
        """
        front_matter, content = cls.parse_front_matter(source)
        return cls(metadata=front_matter, content=content)

    @classmethod
    def from_file(cls, path: str | Path) -> Document:
        """Create a document from a file.

        Args:
            path: The path to the file.

        Returns:
            The document.
        """
        path = Path(path)
        content = path.read_text(encoding="utf-8")
        doc = cls.from_source(content)
        doc.filename = str(path)
        return doc
