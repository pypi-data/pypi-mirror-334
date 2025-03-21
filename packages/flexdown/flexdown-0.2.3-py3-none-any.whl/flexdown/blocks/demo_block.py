"""A block that displays a component along with its code."""

import textwrap
from typing import Any

import black
import reflex as rx

from flexdown import types
from flexdown.blocks import Block


@rx.memo
def code_block(code: str, language: str):
    """Create a code block."""
    return rx.box(
        rx._x.code_block(
            code,
            language=language,
            class_name="code-block",
            can_copy=True,
        ),
        class_name="relative mb-4",
    )


@rx.memo
def code_block_dark(code: str, language: str):
    """Create a dark code block."""
    return rx.box(
        rx._x.code_block(
            code,
            language=language,
            class_name="code-block",
            can_copy=True,
        ),
        class_name="relative",
    )


def docdemo(
    code: str,
    state: str | None = None,
    comp: rx.Component | None = None,
    context: bool = False,
    demobox_props: dict[str, Any] | None = None,
    theme: str | None = None,
    **props,
) -> rx.Component:
    """Create a documentation demo with code and output.

    Args:
        code: The code to render the component.
        state: Code for any state needed for the component.
        comp: The pre-rendered component.
        context: Whether to wrap the render code in a function.
        demobox_props: Props to apply to the demo box.
        theme: The theme of the code snippet.
        props: Props to apply to the demo.

    Returns:
        The styled demo.
    """
    demobox_props = demobox_props or {}
    # Render the component if necessary.
    if comp is None:
        comp = eval(code)

    # Wrap the render code in a function if needed.
    if context:
        code = f"""def index():
        return {code}
        """

    # Add the state code
    if state is not None:
        code = state + code

    if demobox_props.pop("toggle", False):
        return rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger(
                    rx.box(
                        "UI",
                    ),
                    value="tab1",
                    class_name="tab-style",
                ),
                rx.tabs.trigger(
                    rx.box(
                        "Code",
                    ),
                    value="tab2",
                    class_name="tab-style",
                ),
                class_name="justify-end",
            ),
            rx.tabs.content(
                rx.box(docdemobox(comp, **(demobox_props or {})), class_name="my-4"),
                value="tab1",
            ),
            rx.tabs.content(
                rx.box(
                    doccode(code, theme=theme) if theme else doccode(code),
                    class_name="my-4",
                ),
                value="tab2",
            ),
            default_value="tab1",
        )
    # Create the demo.
    return rx.box(
        docdemobox(comp, **(demobox_props or {})),
        doccode(code, theme=theme) if theme else doccode(code),
        class_name="py-4 gap-4 flex flex-col w-full",
        **props,
    )


def doccode(
    code: str,
    language: str = "python",
    lines: tuple[int, int] | None = None,
    theme: str = "light",
) -> rx.Component:
    """Create a documentation code snippet.

    Args:
        code: The code to display.
        language: The language of the code.
        lines: The start/end lines to display.
        theme: The theme of the code

    Returns:
        The styled code snippet.
    """
    # For Python snippets, lint the code with black.
    if language == "python":
        code = black.format_str(
            textwrap.dedent(code), mode=black.FileMode(line_length=60)
        ).strip()

    # If needed, only display a subset of the lines.
    if lines is not None:
        code = textwrap.dedent(
            "\n".join(code.strip().split("\n")[lines[0] : lines[1]])
        ).strip()

    # Create the code snippet.
    cb = code_block_dark if theme == "dark" else code_block
    return cb(
        code=code,
        language=language,
    )


def docdemobox(*children, **props) -> rx.Component:
    """Create a documentation demo box with the output of the code.

    Args:
        children: The children to display.
        props: The properties to apply to the demo box.

    Returns:
        The styled demo box.
    """
    return rx.box(
        *children,
        **props,
        class_name="flex flex-col p-6 rounded-xl overflow-x-auto border border-slate-4 bg-slate-2 items-center justify-center w-full",
    )


def docgraphing(
    code: str,
    comp: rx.Component | None = None,
    data: str | None = None,
):
    """Create a documentation demo with code and output."""
    return rx.box(
        rx.flex(
            comp,
            class_name="w-full flex flex-col p-6 rounded-xl overflow-x-auto border border-slate-4 bg-slate-2 items-center justify-center",
        ),
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Code", value="code", class_name="tab-style"),
                rx.tabs.trigger("Data", value="data", class_name="tab-style"),
                justify_content="end",
            ),
            rx.box(
                rx.tabs.content(doccode(code), value="code", class_name="w-full px-0"),
                rx.tabs.content(
                    doccode(data or ""), value="data", class_name="w-full px-0"
                ),
                class_name="w-full my-4",
            ),
            default_value="code",
            class_name="w-full mt-6 justify-end",
        ),
        class_name="w-full py-4 flex flex-col",
    )


class DemoBlock(Block):
    """A block that displays a component along with its code."""

    starting_indicator = "```python demo"
    ending_indicator = "```"
    include_indicators = True
    theme: str | None = None

    def render(self, env: types.Env) -> rx.Component:
        """Render the block to a Reflex component."""
        if self.starting_indicator is None:
            raise ValueError("The starting indicator is required.")

        lines = self.get_lines(env)
        code = "\n".join(lines[1:-1])

        args = lines[0].removeprefix(self.starting_indicator).split()

        exec_mode = env.get("__exec", False)
        comp = ""

        for arg in args:
            if arg.startswith("id="):
                comp_id = arg.rsplit("id=")[-1]
                break
        else:
            comp_id = None

        if "exec" in args:
            env["__xd"].exec(code, env, self.filename)
            if not exec_mode:
                comp = env[list(env.keys())[-1]]()
        elif "graphing" in args:
            env["__xd"].exec(code, env, self.filename)
            if not exec_mode:
                comp = env[list(env.keys())[-1]]()
                # Get all the code before the final "def".
                parts = code.rpartition("def")
                data, code = parts[0], parts[1] + parts[2]
                comp = docgraphing(code, comp=comp, data=data)
                return comp
        elif exec_mode:
            return comp  # pyright: ignore [reportReturnType]
        elif "box" in args:
            comp = eval(code, env, env)
            return rx.box(docdemobox(comp), margin_bottom="1em", id=comp_id)
        else:
            comp = eval(code, env, env)

        # Sweep up additional CSS-like props to apply to the demobox itself
        demobox_props = {}
        for arg in args:
            prop, equals, value = arg.partition("=")
            if equals:
                demobox_props[prop] = value

        if "toggle" in args:
            demobox_props["toggle"] = True

        return docdemo(
            code,
            comp=comp,  # pyright: ignore [reportArgumentType]
            demobox_props=demobox_props,
            theme=self.theme,
            id=comp_id,
        )


class DemoBlockDark(DemoBlock):
    """A block that displays a component along with its code."""

    theme = "dark"
