"""Unit tests for ``gformlib_cli.auth.get_client``."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import typer
from gformlib.exceptions import AuthenticationError

from gformlib_cli.auth import get_client


@pytest.fixture()
def sa_file(tmp_path: Path) -> Path:
    f = tmp_path / "sa.json"
    f.write_text("{}", encoding="utf-8")
    return f


@pytest.fixture()
def creds_file(tmp_path: Path) -> Path:
    f = tmp_path / "client_secrets.json"
    f.write_text("{}", encoding="utf-8")
    return f


class TestGetClient:
    def test_service_account_success(self, sa_file: Path) -> None:
        mock = MagicMock()
        with patch(
            "gformlib_cli.auth.GoogleFormsClient.from_service_account",
            return_value=mock,
        ):
            result = get_client(sa_file, None)
        assert result is mock

    def test_service_account_auth_error(self, sa_file: Path) -> None:
        with patch(
            "gformlib_cli.auth.GoogleFormsClient.from_service_account",
            side_effect=AuthenticationError("bad key"),
        ):
            with pytest.raises(typer.Exit) as exc_info:
                get_client(sa_file, None)
        assert exc_info.value.exit_code == 1

    def test_oauth_credentials_success(self, creds_file: Path) -> None:
        mock = MagicMock()
        with patch(
            "gformlib_cli.auth.GoogleFormsClient.from_oauth_credentials",
            return_value=mock,
        ):
            result = get_client(None, creds_file)
        assert result is mock

    def test_oauth_credentials_auth_error(self, creds_file: Path) -> None:
        with patch(
            "gformlib_cli.auth.GoogleFormsClient.from_oauth_credentials",
            side_effect=AuthenticationError("oauth failed"),
        ):
            with pytest.raises(typer.Exit) as exc_info:
                get_client(None, creds_file)
        assert exc_info.value.exit_code == 1

    def test_env_var_success(self, sa_file: Path) -> None:
        mock = MagicMock()
        with patch.dict("os.environ", {"GOOGLE_APPLICATION_CREDENTIALS": str(sa_file)}):
            with patch(
                "gformlib_cli.auth.GoogleFormsClient.from_service_account",
                return_value=mock,
            ):
                result = get_client(None, None)
        assert result is mock

    def test_env_var_auth_error(self, sa_file: Path) -> None:
        with patch.dict("os.environ", {"GOOGLE_APPLICATION_CREDENTIALS": str(sa_file)}):
            with patch(
                "gformlib_cli.auth.GoogleFormsClient.from_service_account",
                side_effect=AuthenticationError("env creds invalid"),
            ):
                with pytest.raises(typer.Exit) as exc_info:
                    get_client(None, None)
        assert exc_info.value.exit_code == 1

    def test_no_credentials_exits(self) -> None:
        with patch.dict("os.environ", {"GOOGLE_APPLICATION_CREDENTIALS": ""}):
            with pytest.raises(typer.Exit) as exc_info:
                get_client(None, None)
        assert exc_info.value.exit_code == 1

    def test_service_account_takes_priority_over_credentials(
        self, sa_file: Path, creds_file: Path
    ) -> None:
        """service_account wins when both flags are passed."""
        mock = MagicMock()
        with patch(
            "gformlib_cli.auth.GoogleFormsClient.from_service_account",
            return_value=mock,
        ) as mock_sa:
            result = get_client(sa_file, creds_file)
        mock_sa.assert_called_once()
        assert result is mock
