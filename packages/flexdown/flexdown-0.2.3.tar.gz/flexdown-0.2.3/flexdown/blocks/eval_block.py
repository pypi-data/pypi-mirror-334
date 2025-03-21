"""A block that evaluates a Reflex component to display."""

import reflex as rx

from flexdown import types
from flexdown.blocks.block import Block


class EvalBlock(Block):
    """A block that evaluates a Reflex component to display."""

    starting_indicator = "```python eval"
    ending_indicator = "```"

    def render(self, env: types.Env) -> rx.Component:
        """Render the block to a Reflex component.

        Args:
            env: The environment to use for rendering.

        Returns:
            The Reflex component representing the block.
        """
        return eval(self.get_content(env), env, env)
