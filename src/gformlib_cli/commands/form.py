"""``gformcli form`` command group.

Commands
--------
create      Create a new Google Form from a JSON config file.
update      Update an existing Google Form from a JSON config file.
get         Retrieve metadata and structure of a Google Form.
responses   List responses submitted to a Google Form.
delete      Move a Google Form to the Drive trash.

Auth options (shared across all commands)
-----------------------------------------
Every command accepts the same trio of authentication options:

* ``--service-account / -s``  – path to a service account JSON key file.
* ``--credentials / -c``      – path to an OAuth 2.0 client secrets file.
* ``--token-file / -t``       – where to cache the OAuth token
  (only relevant with ``--credentials``).

If none of these are provided the command falls back to the
``GOOGLE_APPLICATION_CREDENTIALS`` environment variable.
"""

import json
from pathlib import Path
from typing import Annotated, Dict, Optional

import typer
from gformlib.exceptions import APIError, FormCreationError, FormUpdateError, GFormLibError

from ..auth import get_client
from ..output import (
    print_error,
    print_form_info,
    print_raw_form,
    print_responses,
    print_success,
)

app = typer.Typer(
    name="form",
    help="Create, update, inspect and delete Google Forms.",
    no_args_is_help=True,
)

# ── Shared Annotated option types (DRY) ──────────────────────────────────────

_SA_HELP = "Path to service account JSON key file."
_CREDS_HELP = "Path to OAuth 2.0 client secrets JSON file."
_TOKEN_HELP = "Path for caching the OAuth token (default: token.json)."

SaOpt = Annotated[
    Optional[Path],
    typer.Option("--service-account", "-s", help=_SA_HELP, show_default=False),
]
CredsOpt = Annotated[
    Optional[Path],
    typer.Option("--credentials", "-c", help=_CREDS_HELP, show_default=False),
]
TokenOpt = Annotated[
    Optional[Path],
    typer.Option("--token-file", "-t", help=_TOKEN_HELP, show_default=False),
]

# ── Private helpers ───────────────────────────────────────────────────────────


def _read_json(path: Path) -> Dict[str, object]:
    """Read and parse a JSON file, exiting cleanly on errors."""
    if not path.exists():
        print_error(f"File not found: {path}")
        raise typer.Exit(code=1)
    try:
        result: Dict[str, object] = json.loads(path.read_text(encoding="utf-8"))
        return result
    except json.JSONDecodeError as exc:
        print_error(f"Invalid JSON in '{path}': {exc}")
        raise typer.Exit(code=1) from exc


# ── Commands ──────────────────────────────────────────────────────────────────


@app.command("create")
def create(
    config_file: Annotated[Path, typer.Argument(help="JSON config file for the new form.")],
    service_account: SaOpt = None,
    credentials: CredsOpt = None,
    token_file: TokenOpt = None,
) -> None:
    """Create a new Google Form from a JSON config file.

    The config file must contain at minimum a ``"title"`` key.  Questions
    are defined under the ``"questions"`` key as a list of objects.

    \b
    Example config (form.json):
        {
          "title": "Customer Survey",
          "questions": [
            {"title": "Your name", "type": "short_answer", "required": true}
          ]
        }
    """
    config = _read_json(config_file)
    client = get_client(service_account, credentials, token_file)
    try:
        info = client.create_form(config)
    except (FormCreationError, GFormLibError) as exc:
        print_error(str(exc))
        raise typer.Exit(code=1) from exc
    print_success("Form created successfully.")
    print_form_info(info)


@app.command("update")
def update(
    form_id: Annotated[str, typer.Argument(help="ID of the form to update.")],
    config_file: Annotated[Path, typer.Argument(help="JSON config file with update data.")],
    service_account: SaOpt = None,
    credentials: CredsOpt = None,
    token_file: TokenOpt = None,
) -> None:
    """Update an existing Google Form from a JSON config file.

    Supported keys: ``"title"``, ``"description"``, ``"add_questions"``.
    Only the supplied keys are changed; everything else is left untouched.

    \b
    Example config (update.json):
        {
          "title": "Revised Survey",
          "add_questions": [
            {"title": "Any comments?", "type": "paragraph"}
          ]
        }
    """
    config = _read_json(config_file)
    client = get_client(service_account, credentials, token_file)
    try:
        info = client.update_form(form_id, config)
    except (FormUpdateError, GFormLibError) as exc:
        print_error(str(exc))
        raise typer.Exit(code=1) from exc
    print_success("Form updated successfully.")
    print_form_info(info)


@app.command("get")
def get(
    form_id: Annotated[str, typer.Argument(help="ID of the form to inspect.")],
    service_account: SaOpt = None,
    credentials: CredsOpt = None,
    token_file: TokenOpt = None,
) -> None:
    """Get metadata and structure of an existing Google Form."""
    client = get_client(service_account, credentials, token_file)
    try:
        data = client.get_form(form_id)
    except (APIError, GFormLibError) as exc:
        print_error(str(exc))
        raise typer.Exit(code=1) from exc
    print_raw_form(data)


@app.command("responses")
def responses(
    form_id: Annotated[str, typer.Argument(help="ID of the form.")],
    filter_str: Annotated[
        Optional[str],
        typer.Option(
            "--filter",
            "-f",
            help="API filter string, e.g. 'timestamp > 2024-01-01T00:00:00Z'.",
        ),
    ] = None,
    page_size: Annotated[
        int,
        typer.Option("--page-size", "-p", help="Responses per API page (max 100)."),
    ] = 100,
    service_account: SaOpt = None,
    credentials: CredsOpt = None,
    token_file: TokenOpt = None,
) -> None:
    """List responses submitted to a Google Form."""
    client = get_client(service_account, credentials, token_file)
    try:
        resp_list = client.list_responses(
            form_id,
            page_size=page_size,
            filter_str=filter_str,
        )
    except (APIError, GFormLibError) as exc:
        print_error(str(exc))
        raise typer.Exit(code=1) from exc
    print_responses(resp_list, form_id)


@app.command("delete")
def delete(
    form_id: Annotated[
        str, typer.Argument(help="ID of the form to delete (moves to Drive trash).")
    ],
    yes: Annotated[
        bool,
        typer.Option("--yes", "-y", help="Skip the confirmation prompt."),
    ] = False,
    service_account: SaOpt = None,
    credentials: CredsOpt = None,
    token_file: TokenOpt = None,
) -> None:
    """Delete a Google Form by moving it to the Drive trash.

    You will be asked to confirm unless [bold]--yes[/bold] is passed.
    """
    if not yes:
        typer.confirm(
            f"Are you sure you want to delete form '{form_id}'?",
            abort=True,
        )
    client = get_client(service_account, credentials, token_file)
    try:
        client.delete_form(form_id)
    except (APIError, GFormLibError) as exc:
        print_error(str(exc))
        raise typer.Exit(code=1) from exc
    print_success(f"Form '{form_id}' moved to trash.")
