"""A block that displays an alert line using rx.callout."""

import reflex as rx

from flexdown import types

from .markdown_block import MarkdownBlock


def markdown_with_shiki(*args, **kwargs):
    """Wrapper for the markdown component with a customized component map.
    Uses the experimental Shiki-based code block (rx._x.code_block)
    instead of the default CodeBlock component for code blocks.

    Note: This wrapper should be removed once the default codeblock
    in rx.markdown component map is updated to the Shiki-based code block.
    """
    return rx.markdown(
        *args,
        component_map={
            "codeblock": lambda value, **props: rx._x.code_block(value, **props)
        },
        **kwargs,
    )


font_family = "Instrument Sans"

base = {
    "font-family": font_family,
    "font-style": "normal",
    "font-weight": "500",
    "font-size": ["14px", "16px"],
    "line-height": ["20px", "24px"],
    "letter-spacing": "-0.015em",
}

code = {
    "font-family": "Source Code Pro",
    "font-size": "14px",
    "font-style": "normal",
    "font-weight": "400",
    "line-height": "24px",
    "letter-spacing": "-0.015em",
}


def get_code_style(color: str):
    """Get the style for the code block."""
    return {
        "p": {"margin_y": "0px"},
        "code": {
            "color": rx.color(color, 11),
            "border_radius": "4px",
            "border": f"1px solid {rx.color(color, 5)}",
            "background": rx.color(color, 4),
            **code,
        },
        **base,
    }


def alert_icon(status: str, color: str):
    """Get the icon for the alert status."""
    return rx.box(
        rx.match(
            status,
            ("info", rx.icon(tag="info", size=18, margin_right=".5em")),
            ("success", rx.icon(tag="circle_check", size=18, margin_right=".5em")),
            ("warning", rx.icon(tag="triangle_alert", size=18, margin_right=".5em")),
            ("error", rx.icon(tag="ban", size=18, margin_right=".5em")),
        ),
        color=f"{rx.color(color, 11)}",
    )


class AlertBlock(MarkdownBlock):
    """A block that displays a component along with its code."""

    starting_indicator = "```md alert"
    ending_indicator = "```"

    include_indicators = True

    def render(self, env: types.Env) -> rx.Component:
        """Render the block to a Reflex component."""
        if self.starting_indicator is None:
            raise ValueError("The starting indicator is required.")

        if self.render_fn is None:
            raise ValueError("The render function is required.")

        lines = self.get_lines(env)

        args = lines[0].removeprefix(self.starting_indicator).split()

        if len(args) == 0:
            args = ["info"]
        status = args[0]

        if lines[1].startswith("#"):
            title = lines[1].strip("#").strip()
            content = "\n".join(lines[2:-1])
        else:
            title = ""
            content = "\n".join(lines[1:-1])

        colors = {
            "info": "accent",
            "success": "grass",
            "warning": "amber",
            "error": "red",
        }

        color = colors.get(status, "blue")

        has_content = bool(content.strip())

        if has_content:
            return rx.accordion.root(
                rx.accordion.item(
                    rx.accordion.header(
                        rx.accordion.trigger(
                            rx.hstack(
                                alert_icon(status, color),
                                (
                                    markdown_with_shiki(
                                        title,
                                        margin_y="0px",
                                        style=get_code_style(color),
                                    )
                                    if title
                                    else self.render_fn(content=content)
                                ),
                                rx.spacer(),
                                rx.accordion.icon(color=f"{rx.color(color, 11)}"),
                                align_items="center",
                                justify_content="left",
                                text_align="left",
                                spacing="2",
                                width="100%",
                            ),
                            padding="0px",
                            color=f"{rx.color(color, 11)} !important",
                            background_color="transparent !important",
                            border_radius="12px",
                            _hover={},
                        ),
                    ),
                    (
                        rx.accordion.content(
                            markdown_with_shiki(content),
                            padding="0px",
                            margin_top="16px",
                        )
                        if title
                        else rx.fragment()
                    ),
                    border_radius="12px",
                    padding=["16px", "24px"],
                    background_color=f"{rx.color(color, 3)}",
                    border=f"1px solid {rx.color(color, 4)}",
                ),
                background="none !important",
                border_radius="0px",
                box_shadow="unset !important",
                collapsible=True,
                width="100%",
                margin_bottom="16px",
            )
        else:
            return rx.vstack(
                rx.hstack(
                    alert_icon(status, color),
                    markdown_with_shiki(
                        title,
                        color=f"{rx.color(color, 11)}",
                        margin_y="0px",
                        style=get_code_style(color),
                    ),
                    align_items="center",
                    width="100%",
                    spacing="1",
                    padding=["16px", "24px"],
                ),
                border=f"1px solid {rx.color(color, 4)}",
                background_color=f"{rx.color(color, 3)}",
                border_radius="12px",
                margin_bottom="16px",
            )
