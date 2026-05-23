"""Rich-based output helpers for gformlib-cli.

All user-visible output goes through this module so that formatting is
consistent and easy to change in one place (DRY).
"""

from typing import Any, Dict, List

import rich.box
from gformlib import FormInfo
from rich.console import Console
from rich.table import Table

# Two consoles: one for regular output, one for errors (stderr).
console = Console()
err_console = Console(stderr=True)


# ── Public formatters ─────────────────────────────────────────────────────────


def print_form_info(info: FormInfo) -> None:
    """Render a :class:`~gformlib.FormInfo` as a Rich table."""
    table = _form_table(info.title)
    table.add_row("Form ID", info.form_id)
    table.add_row("Title", info.title)
    table.add_row("Document Title", info.document_title)
    table.add_row(
        "Responder URI",
        f"[link={info.responder_uri}]{info.responder_uri}[/link]",
    )
    if info.linked_sheet_id:
        table.add_row("Linked Sheet ID", info.linked_sheet_id)
    if info.revision_id:
        table.add_row("Revision ID", info.revision_id)
    console.print(table)


def print_raw_form(data: Dict[str, Any]) -> None:
    """Render the raw dict returned by :meth:`~gformlib.GoogleFormsClient.get_form`."""
    info_block = data.get("info", {})
    title = info_block.get("title", "Form")
    uri = data.get("responderUri", "")

    table = _form_table(title)
    table.add_row("Form ID", data.get("formId", ""))
    table.add_row("Title", title)
    table.add_row("Document Title", info_block.get("documentTitle", ""))
    table.add_row("Responder URI", f"[link={uri}]{uri}[/link]" if uri else "")
    revision = data.get("revisionId", "")
    if revision:
        table.add_row("Revision ID", revision)
    table.add_row("Questions", str(len(data.get("items", []))))
    console.print(table)


def print_responses(responses: List[Dict[str, Any]], form_id: str) -> None:
    """Render a list of form responses."""
    count = len(responses)
    console.print(
        f"\n[bold cyan]{count}[/bold cyan] response(s) for form " f"[bold]{form_id}[/bold]\n"
    )
    for i, resp in enumerate(responses, 1):
        resp_id = resp.get("responseId", "unknown")
        submitted = resp.get("createTime", "")
        console.print(
            f"  [dim]{i}.[/dim] [green]{resp_id}[/green]"
            + (f" — submitted [dim]{submitted}[/dim]" if submitted else "")
        )


def print_success(message: str) -> None:
    """Print a green success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_error(message: str) -> None:
    """Print a red error message to stderr."""
    err_console.print(f"[bold red]✗[/bold red] {message}")


# ── Private helpers ───────────────────────────────────────────────────────────


def _form_table(title: str) -> Table:
    """Return a base Rich table styled for form info display."""
    table = Table(
        title=f"[bold]{title}[/bold]",
        show_header=False,
        box=rich.box.ROUNDED,
        padding=(0, 1),
    )
    table.add_column("Field", style="bold cyan", no_wrap=True)
    table.add_column("Value", overflow="fold")
    return table
