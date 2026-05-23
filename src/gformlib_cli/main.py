"""Entry point for the gformcli command-line application."""

from typing import Optional

import typer

from . import __version__
from .commands import form

APP_NAME = "gformcli"

app = typer.Typer(
    name=APP_NAME,
    help="Command-line interface for the [bold]gformlib[/bold] Google Forms toolkit.",
    rich_markup_mode="rich",
    no_args_is_help=True,
)

app.add_typer(form.app, name="form")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{APP_NAME} {__version__}")
        raise typer.Exit()


@app.callback()
def callback(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        help="Show version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    """gformlib CLI – manage Google Forms from the terminal."""


def main() -> None:
    """Entry point registered as the ``gformcli`` console script."""
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
