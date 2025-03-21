"""The main flexdown module."""

import importlib
import importlib.util
import os
import shutil
import sys
from pathlib import Path
from typing import Callable, Iterator

import reflex as rx
from reflex_cli.utils import console

from flexdown import blocks, types, utils
from flexdown.blocks.block import Block
from flexdown.document import Document
from flexdown.namespace import FxNamespace

DEFAULT_BLOCKS = [
    blocks.ExecBlock,
    blocks.EvalBlock,
    blocks.AlertBlock,
    blocks.DemoBlock,
    blocks.CodeBlock,
    blocks.MarkdownBlock,
]

files = {}


class Flexdown(rx.Base):
    """Class to parse and render flexdown files."""

    # The list of accepted block types to parse.
    block_types: list[type[Block]] = []

    # The default block type.
    default_block_type: type[Block] = blocks.MarkdownBlock

    # The template to use when rendering pages.
    page_template: Callable[[rx.Component], rx.Component] = lambda body: rx.container(
        body, size="4"
    )

    # Mapping from markdown tag to a rendering function for Reflex components.
    component_map: types.ComponentMap = {}

    # The directory to save modules to.
    module_dir: str = "modules"

    def __init__(self, *args, **kwargs):
        """Initialize the Flexdown class."""
        super().__init__(*args, **kwargs)

        def flexdown_memo(content: str) -> rx.Component:
            return rx.markdown(content, component_map=self.component_map)

        # Give the function a unique name.
        import random

        flexdown_memo.__name__ = f"flexdown_memo_{random.randint(0, 100000)}"
        self.flexdown_memo = rx.memo(flexdown_memo)

    def get_full_module_dir(self):
        """Get the full path to the module directory."""
        return Path(__file__).resolve().parent / self.module_dir

    def get_default_block(self) -> Block:
        """Get the default block type.

        Returns:
            The default block type.
        """
        block = self.default_block_type()
        if isinstance(block, blocks.MarkdownBlock):
            block.render_fn = self.flexdown_memo
        return block

    def clear_module(self, filename: str | Path):
        """Clear a specific module file."""
        # Get the path to the the module should be.
        module_path = self.get_full_module_dir() / f"{utils.get_id(str(filename))}.py"

        # Delete the file.
        if module_path.exists():
            module_path.unlink()

    def clear_modules(self):
        """Clear the modules directory."""
        # Get the path to the directory where the module should be saved.
        module_dir = self.get_full_module_dir()

        # Delete the directory.
        if module_dir.exists():
            shutil.rmtree(module_dir)

    def _get_block(
        self, line: str, line_number: int, filename: str | None = None
    ) -> Block:
        """Get the block type for a line of text.

        Args:
            line: The line of text to check.
            line_number: The line number of the line.
            filename: The filename of the file containing the line.

        Returns:
            The block type for the line of text.
        """
        block_types = self.block_types + DEFAULT_BLOCKS

        # Search for a block type that can parse the line.
        for block_type in block_types:
            # Try to create a block from the line.
            block = block_type.from_line(
                line,
                line_number=line_number,
                component_map=self.component_map,
                filename=filename,
            )
            if isinstance(block, blocks.MarkdownBlock):
                block.render_fn = self.flexdown_memo

            # If a block was created, then return it.
            if block is not None:
                return block

        # If no block was created, then return the default block type.
        block = self.default_block_type().append(line)
        return block

    def exec(
        self, content: str, env: types.Env | None = None, filename: str | None = None
    ):
        """Execute a block of code."""
        if env is None:
            env = {}
        if filename is None:
            filename = ""
        # Get the path to the directory where the module should be saved.
        flexdown_dir = Path(__file__).resolve().parent
        module_dir = flexdown_dir / self.module_dir

        # Write the content to a file in the module directory.
        module_dir.mkdir(parents=True, exist_ok=True)

        # Each new block gets its own module to avoid re-exec'ing code.
        per_file_modules = files.setdefault(filename, [])
        module_file_name = utils.get_id(content + filename + str(len(per_file_modules)))
        module_path = module_dir / f"{module_file_name}.py"

        if per_file_modules:
            previous_module_name = f"flexdown.{self.module_dir}.{per_file_modules[-1]}"
            content = f"from {previous_module_name} import *\n\n" + content
        module_path.write_text(content + "\n")

        per_file_modules.append(module_file_name)

        # Import the module to execute the code.
        module_name = f"flexdown.{self.module_dir}.{module_file_name}"
        os.environ["PYTEST_CURRENT_TEST"] = "1"
        if module_name in sys.modules:
            raise RuntimeError(
                f"{module_name} from {filename} has already been imported. This is a bug."
            )
        else:
            spec = importlib.util.spec_from_file_location(module_name, str(module_path))
            if not spec:
                return
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            if spec and spec.loader:
                spec.loader.exec_module(module)

        del os.environ["PYTEST_CURRENT_TEST"]

        env.update(vars(module))

    def get_blocks(self, source: str, filename: str | None = None) -> Iterator[Block]:
        """Parse a Flexdown file into blocks.

        Args:
            source: The source code of the Flexdown file.
            filename: The filename of the Flexdown file.

        Returns:
            The iterator of blocks in the Flexdown file.
        """
        current_block = None

        # Iterate over each line in the source code.
        for line_number, line in enumerate(source.splitlines()):
            # If there is no current block, then create a new block.
            if current_block is None:
                # If the line is empty, then skip it.
                if line == "":
                    continue

                # Otherwise, create a new block.
                current_block = self._get_block(line, line_number, filename)

            else:
                # Add the line to the current block.
                current_block.append(line)

            # Check if the current block is finished.
            if current_block.is_finished():
                yield current_block
                current_block = None

        # Add the final block if it exists.
        if current_block is not None:
            current_block.finish()
            yield current_block

    def render(
        self, source: str | Document, filename: str | Path | None = None
    ) -> rx.Component:
        """Render a Flexdown file into a Reflex component.

        Args:
            source: The source code of the Flexdown file.
            filename: The filename of the Flexdown file.

        Returns:
            The Reflex component representing the Flexdown file.
        """
        if isinstance(filename, Path):
            filename = str(filename)

        if isinstance(source, Document) and filename is None:
            filename = source.filename

        # Convert the source to a document.
        if isinstance(source, str):
            source = Document.from_source(source)

        if filename is not None:
            self.clear_module(filename)
            files.pop(
                filename, None
            )  # Reset per file exec block count for consistent hashing.

        # The environment used for execing and evaling code.
        env: types.Env = source.metadata
        env["__xd"] = self

        # Get the content of the document.
        source = source.content

        # Render each block.
        out: list[rx.Component] = []
        for block in self.get_blocks(source, filename):
            if isinstance(block, blocks.MarkdownBlock):
                block.render_fn = self.flexdown_memo
            try:
                comp = block.render(env=env)
                if comp:
                    out.append(comp)
            except Exception:
                console.error(
                    f"Error while rendering {type(block)} on line {block.start_line_number}. "
                    f"\n{block.get_content(env)}"
                )
                raise

        # Wrap the output in the page template.
        return self.page_template(rx.fragment(*out))

    def render_file(self, path: str | Path) -> rx.Component:
        """Render a Flexdown file into a Reflex component.

        Args:
            path: The path to the Flexdown file.

        Returns:
            The Reflex component representing the Flexdown file.
        """
        # Render the source code.
        return self.render(Document.from_file(path), path)

    def add_all_pages(self, app: rx.App, namespace: FxNamespace):
        """Add all pages in a namespace to an app.

        Args:
            app: The app to add the pages to.
            namespace: The namespace to get the pages from.
        """
        for page in namespace.all_pages():
            app.add_page(
                self.render(page.doc),
                route=page.route,
                title=page.title,
            )
