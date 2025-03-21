"""Constants used in flexdown."""

from pathlib import Path

# The extension for Flexdown files.
FLEXDOWN_EXTENSION = ".md"

# The Flexdown app directory.
FLEXDOWN_DIR = Path(".flexdown/flexd")
FLEXDOWN_FILE = FLEXDOWN_DIR / "flexd/flexd.py"
FLEXDOWN_MODULES_DIR = "modules"

# Regex for front matter.
FRONT_MATTER_REGEX = r"^---\s*\n(.+?)\n---\s*\n(.*)$"
# Regex for template placeholders.
TEMPLATE_REGEX_WITHOUT_ESCAPE = r"(?<!\\)(?<!\\\\){(?!\\)(.*?)(?<!\\)}"
TEMPLATE_REGEX = r"{([^{}]*)}"

# The default app initialization code.
DEFAULT_APP_INIT = """
app = rx.App(
    head_components=flexdown.utils.google_fonts(),
)
"""

# The enterprise app initialization code.
ENTERPRISE_APP_INIT = """import reflex_enterprise as rxe

app = rxe.App(
    head_components=flexdown.utils.google_fonts(),
)
"""

# The default app template.
APP_TEMPLATE = """import flexdown
import reflex as rx
{app_init}

component_map = {{
    "a": lambda value, **props: rx.link(value, color="blue", **props),
}}

path = "{path}"
{module_name} = flexdown.namespace.FxNamespace(path, prefix=path)

fxapp = flexdown.Flexdown(component_map=component_map)
fxapp.add_all_pages(app, {module_name})
"""
