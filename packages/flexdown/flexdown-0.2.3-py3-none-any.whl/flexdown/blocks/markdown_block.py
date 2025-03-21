"""A block of Markdown."""

from typing import Callable

import reflex as rx

from flexdown import types, utils
from flexdown.blocks.block import Block


class MarkdownBlock(Block):
    """A block of Markdown."""

    line_transforms = [
        utils.evaluate_templates,
    ]
    render_fn: Callable | None = None

    def render(self, env: types.Env) -> rx.Component:
        """Render the block to a Reflex component.

        Args:
            env: The environment to use for rendering.

        Raises:
            ValueError: If the render function is not set.

        Returns:
            The Reflex component representing the block.
        """
        if self.render_fn is None:
            raise ValueError("The render function is not set.")
        return self.render_fn(content=self.get_content(env))
