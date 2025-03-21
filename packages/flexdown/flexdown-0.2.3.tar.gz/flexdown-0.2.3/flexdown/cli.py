"""The Flexdown CLI."""

from importlib.metadata import version
from pathlib import Path

import typer
from reflex.constants import Env, LogLevel
from reflex.utils.processes import new_process
from reflex_cli.utils import console

from flexdown import constants

__version__ = version("flexdown")

# The command line app.
app = typer.Typer()


@app.command()
def run(
    path: Path,
    app_name: str | None = typer.Option(
        None,
        "-n",
        "--name",
        help="The name of the project.",
    ),
    deploy: bool = typer.Option(False, help="Deploy the project after running."),
    deploy_project: str = typer.Option(None, help="The project to deploy."),
    token: str = typer.Option(
        None, "-t", "--token", help="The token to use for deployment."
    ),
    env: Env | None = typer.Option(None, help="The environment to run the project in."),
    enterprise: bool = typer.Option(
        False,
        "-e",
        "--enterprise",
        help="Whether to use the enterprise app template.",
    ),
    loglevel: LogLevel | None = typer.Option(None, help="The log level to use."),
):
    """Run a Flexdown project."""
    console.info(f"App Name: {app_name}")
    # Create a .flexdown directory in the current directory.
    constants.FLEXDOWN_DIR.mkdir(parents=True, exist_ok=True)

    # Create a reflex project.
    if not (constants.FLEXDOWN_DIR / "rxconfig.py").exists():
        command = ["reflex", "init", "--template", "blank"]

        if loglevel is not None:
            command.extend(["--loglevel", loglevel])
        new_process(command, cwd=constants.FLEXDOWN_DIR, show_logs=True, run=True)

        # Replace the app file with a template.
        write_app_content(path, enterprise)

        req_file = constants.FLEXDOWN_DIR / "requirements.txt"
        requirements = [req_file.read_text(), f"flexdown=={__version__}"]
        if enterprise:
            requirements.append("reflex-enterprise")
        req_file.write_text("\n".join(requirements))

    command = ["reflex"]
    if deploy:
        if not token:
            return typer.echo("A token is required for deployment.")
        if not deploy_project:
            return typer.echo("A project is required for deployment.")
        if env:
            return typer.echo("The environment flag cannot be used with deployment.")
        command.extend(["deploy", "--token", token, "--project", deploy_project])
        if app_name:
            command.extend(["--app-name", app_name])
    else:
        command.extend(["run"])
        match env:
            case Env.DEV:
                command.extend(["--env", "dev"])
            case Env.PROD:
                command.extend(["--env", "prod"])

    if loglevel is not None:
        command.extend(["--loglevel", loglevel])

    # Run the reflex project.
    new_process(command, cwd=constants.FLEXDOWN_DIR, show_logs=True, run=True)


def write_app_content(path: Path, enterprise: bool) -> None:
    """Write the content for the app file.

    Args:
        path: The path to the Flexdown project.
        enterprise: Whether to use the enterprise app template.
    """
    constants.FLEXDOWN_FILE.write_text(get_app_content(path, enterprise))


def get_app_content(path: Path, enterprise: bool) -> str:
    """Format the content of the root app file for flexdown.

    Args:
        path: The path to the Flexdown project.
        enterprise: Whether to use the enterprise app template.

    Returns:
        The content for the app file.
    """
    return constants.APP_TEMPLATE.format(
        path=Path().absolute() / path,
        module_name=path.stem,
        app_init=constants.ENTERPRISE_APP_INIT
        if enterprise
        else constants.DEFAULT_APP_INIT,
    )
