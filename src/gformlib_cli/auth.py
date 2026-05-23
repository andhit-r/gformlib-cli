"""Authentication helpers for gformlib-cli.

Centralises credential resolution so every command goes through the same
priority chain:

1. ``--service-account`` flag → :meth:`~gformlib.GoogleFormsClient.from_service_account`
2. ``--credentials`` flag     → :meth:`~gformlib.GoogleFormsClient.from_oauth_credentials`
3. ``GOOGLE_APPLICATION_CREDENTIALS`` env var → service-account auth
4. Hard exit with a helpful error message.
"""

import os
from pathlib import Path
from typing import Optional

import typer
from gformlib import GoogleFormsClient
from gformlib.exceptions import AuthenticationError

from .output import print_error


def get_client(
    service_account: Optional[Path],
    credentials: Optional[Path],
    token_file: Optional[Path] = None,
) -> GoogleFormsClient:
    """Return an authenticated :class:`~gformlib.GoogleFormsClient`.

    Args:
        service_account: Path to a service account JSON key file.
        credentials: Path to an OAuth 2.0 client secrets JSON file.
        token_file: Path for caching the OAuth token (defaults to
            ``token.json`` in the current directory).

    Returns:
        An authenticated :class:`~gformlib.GoogleFormsClient`.

    Raises:
        :class:`typer.Exit`: With exit code ``1`` when authentication fails
            or no credentials are available.
    """
    if service_account is not None:
        try:
            return GoogleFormsClient.from_service_account(service_account)
        except AuthenticationError as exc:
            print_error(f"Service account authentication failed: {exc}")
            raise typer.Exit(code=1) from exc

    if credentials is not None:
        try:
            return GoogleFormsClient.from_oauth_credentials(
                credentials,
                token_file=token_file,
            )
        except AuthenticationError as exc:
            print_error(f"OAuth authentication failed: {exc}")
            raise typer.Exit(code=1) from exc

    # Fallback: GOOGLE_APPLICATION_CREDENTIALS environment variable
    env_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if env_creds:
        try:
            return GoogleFormsClient.from_service_account(env_creds)
        except AuthenticationError as exc:
            print_error(f"GOOGLE_APPLICATION_CREDENTIALS authentication failed: {exc}")
            raise typer.Exit(code=1) from exc

    print_error(
        "No credentials provided. Use [bold]--service-account[/bold], "
        "[bold]--credentials[/bold], or set the "
        "[bold]GOOGLE_APPLICATION_CREDENTIALS[/bold] environment variable."
    )
    raise typer.Exit(code=1)
