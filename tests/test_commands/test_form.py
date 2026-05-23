"""Unit tests for ``gformcli form`` sub-commands.

All Google API calls are intercepted by patching ``get_client`` so that tests
run without any real credentials or network access.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from gformlib import FormInfo
from gformlib.exceptions import APIError, FormCreationError, FormUpdateError
from typer.testing import CliRunner

from gformlib_cli.main import app

runner = CliRunner()

# Patch target – get_client as imported inside the form command module.
_PATCH_GET_CLIENT = "gformlib_cli.commands.form.get_client"


# ── form create ───────────────────────────────────────────────────────────────


class TestFormCreate:
    def test_success(
        self,
        mock_client: MagicMock,
        sample_form_info: FormInfo,
        form_config_file: Path,
        sa_file: Path,
    ) -> None:
        mock_client.create_form.return_value = sample_form_info
        with patch(_PATCH_GET_CLIENT, return_value=mock_client):
            result = runner.invoke(
                app,
                ["form", "create", str(form_config_file), "-s", str(sa_file)],
            )
        assert result.exit_code == 0
        assert "form123" in result.output
        mock_client.create_form.assert_called_once()

    def test_missing_config_file(self, sa_file: Path) -> None:
        result = runner.invoke(
            app,
            ["form", "create", "does_not_exist.json", "-s", str(sa_file)],
        )
        assert result.exit_code != 0

    def test_invalid_json(self, tmp_path: Path, sa_file: Path, mock_client: MagicMock) -> None:
        bad = tmp_path / "bad.json"
        bad.write_text("not valid json", encoding="utf-8")
        with patch(_PATCH_GET_CLIENT, return_value=mock_client):
            result = runner.invoke(
                app,
                ["form", "create", str(bad), "-s", str(sa_file)],
            )
        assert result.exit_code == 1
        mock_client.create_form.assert_not_called()

    def test_api_error(
        self,
        mock_client: MagicMock,
        form_config_file: Path,
        sa_file: Path,
    ) -> None:
        mock_client.create_form.side_effect = FormCreationError("quota exceeded")
        with patch(_PATCH_GET_CLIENT, return_value=mock_client):
            result = runner.invoke(
                app,
                ["form", "create", str(form_config_file), "-s", str(sa_file)],
            )
        assert result.exit_code == 1

    def test_no_credentials(self, form_config_file: Path) -> None:
        """Exit code 1 when no credentials are supplied and env var is absent."""
        with patch.dict("os.environ", {"GOOGLE_APPLICATION_CREDENTIALS": ""}):
            result = runner.invoke(app, ["form", "create", str(form_config_file)])
        assert result.exit_code == 1


# ── form update ───────────────────────────────────────────────────────────────


class TestFormUpdate:
    def test_success(
        self,
        mock_client: MagicMock,
        sample_form_info: FormInfo,
        update_config_file: Path,
        sa_file: Path,
    ) -> None:
        mock_client.update_form.return_value = sample_form_info
        with patch(_PATCH_GET_CLIENT, return_value=mock_client):
            result = runner.invoke(
                app,
                ["form", "update", "form123", str(update_config_file), "-s", str(sa_file)],
            )
        assert result.exit_code == 0
        assert "form123" in result.output
        mock_client.update_form.assert_called_once_with("form123", {"title": "Updated Form"})

    def test_missing_config_file(self, sa_file: Path) -> None:
        result = runner.invoke(
            app,
            ["form", "update", "form123", "does_not_exist.json", "-s", str(sa_file)],
        )
        assert result.exit_code != 0

    def test_invalid_json(
        self, tmp_path: Path, sa_file: Path, mock_client: MagicMock
    ) -> None:
        bad = tmp_path / "bad.json"
        bad.write_text("{broken", encoding="utf-8")
        with patch(_PATCH_GET_CLIENT, return_value=mock_client):
            result = runner.invoke(
                app,
                ["form", "update", "form123", str(bad), "-s", str(sa_file)],
            )
        assert result.exit_code == 1

    def test_api_error(
        self,
        mock_client: MagicMock,
        update_config_file: Path,
        sa_file: Path,
    ) -> None:
        mock_client.update_form.side_effect = FormUpdateError(
            "Update failed", form_id="form123"
        )
        with patch(_PATCH_GET_CLIENT, return_value=mock_client):
            result = runner.invoke(
                app,
                ["form", "update", "form123", str(update_config_file), "-s", str(sa_file)],
            )
        assert result.exit_code == 1


# ── form get ──────────────────────────────────────────────────────────────────


class TestFormGet:
    def test_success(
        self,
        mock_client: MagicMock,
        sample_raw_form: dict,  # type: ignore[type-arg]
        sa_file: Path,
    ) -> None:
        mock_client.get_form.return_value = sample_raw_form
        with patch(_PATCH_GET_CLIENT, return_value=mock_client):
            result = runner.invoke(
                app,
                ["form", "get", "form123", "-s", str(sa_file)],
            )
        assert result.exit_code == 0
        assert "form123" in result.output
        mock_client.get_form.assert_called_once_with("form123")

    def test_api_error(self, mock_client: MagicMock, sa_file: Path) -> None:
        mock_client.get_form.side_effect = APIError("Not found")
        with patch(_PATCH_GET_CLIENT, return_value=mock_client):
            result = runner.invoke(
                app,
                ["form", "get", "form123", "-s", str(sa_file)],
            )
        assert result.exit_code == 1


# ── form responses ────────────────────────────────────────────────────────────


class TestFormResponses:
    def test_success(self, mock_client: MagicMock, sa_file: Path) -> None:
        mock_client.list_responses.return_value = [
            {"responseId": "resp1", "createTime": "2024-01-01T00:00:00Z"},
            {"responseId": "resp2", "createTime": "2024-01-02T00:00:00Z"},
        ]
        with patch(_PATCH_GET_CLIENT, return_value=mock_client):
            result = runner.invoke(
                app,
                ["form", "responses", "form123", "-s", str(sa_file)],
            )
        assert result.exit_code == 0
        assert "2" in result.output
        assert "resp1" in result.output

    def test_empty_responses(self, mock_client: MagicMock, sa_file: Path) -> None:
        mock_client.list_responses.return_value = []
        with patch(_PATCH_GET_CLIENT, return_value=mock_client):
            result = runner.invoke(
                app,
                ["form", "responses", "form123", "-s", str(sa_file)],
            )
        assert result.exit_code == 0
        assert "0" in result.output

    def test_with_filter(self, mock_client: MagicMock, sa_file: Path) -> None:
        mock_client.list_responses.return_value = []
        with patch(_PATCH_GET_CLIENT, return_value=mock_client):
            runner.invoke(
                app,
                [
                    "form",
                    "responses",
                    "form123",
                    "--filter",
                    "timestamp > 2024-01-01T00:00:00Z",
                    "-s",
                    str(sa_file),
                ],
            )
        mock_client.list_responses.assert_called_once_with(
            "form123",
            page_size=100,
            filter_str="timestamp > 2024-01-01T00:00:00Z",
        )

    def test_api_error(self, mock_client: MagicMock, sa_file: Path) -> None:
        mock_client.list_responses.side_effect = APIError("Forbidden")
        with patch(_PATCH_GET_CLIENT, return_value=mock_client):
            result = runner.invoke(
                app,
                ["form", "responses", "form123", "-s", str(sa_file)],
            )
        assert result.exit_code == 1


# ── form delete ───────────────────────────────────────────────────────────────


class TestFormDelete:
    def test_success_with_yes_flag(self, mock_client: MagicMock, sa_file: Path) -> None:
        with patch(_PATCH_GET_CLIENT, return_value=mock_client):
            result = runner.invoke(
                app,
                ["form", "delete", "form123", "--yes", "-s", str(sa_file)],
            )
        assert result.exit_code == 0
        mock_client.delete_form.assert_called_once_with("form123")

    def test_confirms_before_delete(self, mock_client: MagicMock, sa_file: Path) -> None:
        """Typing 'y' at the confirmation prompt proceeds with deletion."""
        with patch(_PATCH_GET_CLIENT, return_value=mock_client):
            result = runner.invoke(
                app,
                ["form", "delete", "form123", "-s", str(sa_file)],
                input="y\n",
            )
        assert result.exit_code == 0
        mock_client.delete_form.assert_called_once_with("form123")

    def test_aborts_on_no(self, mock_client: MagicMock, sa_file: Path) -> None:
        """Typing 'n' aborts and does not call delete_form."""
        with patch(_PATCH_GET_CLIENT, return_value=mock_client):
            result = runner.invoke(
                app,
                ["form", "delete", "form123", "-s", str(sa_file)],
                input="n\n",
            )
        assert result.exit_code != 0
        mock_client.delete_form.assert_not_called()

    def test_api_error(self, mock_client: MagicMock, sa_file: Path) -> None:
        mock_client.delete_form.side_effect = APIError("Delete failed")
        with patch(_PATCH_GET_CLIENT, return_value=mock_client):
            result = runner.invoke(
                app,
                ["form", "delete", "form123", "--yes", "-s", str(sa_file)],
            )
        assert result.exit_code == 1


# ── version flag ──────────────────────────────────────────────────────────────


class TestVersionFlag:
    def test_version_flag(self) -> None:
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "gformcli" in result.output
