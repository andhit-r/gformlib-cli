"""Shared pytest fixtures for the gformlib-cli test suite."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock

import pytest
from gformlib import FormInfo


@pytest.fixture()
def mock_client() -> MagicMock:
    """A pre-configured MagicMock standing in for GoogleFormsClient."""
    return MagicMock()


@pytest.fixture()
def sample_form_info() -> FormInfo:
    """A minimal :class:`~gformlib.FormInfo` used across multiple tests."""
    return FormInfo(
        form_id="form123",
        title="Test Form",
        document_title="Test Form Doc",
        responder_uri="https://docs.google.com/forms/d/form123/viewform",
        revision_id="rev1",
    )


@pytest.fixture()
def sample_raw_form() -> Dict[str, Any]:
    """Simulated raw dict returned by ``client.get_form()``."""
    return {
        "formId": "form123",
        "info": {
            "title": "Test Form",
            "documentTitle": "Test Form Doc",
        },
        "responderUri": "https://docs.google.com/forms/d/form123/viewform",
        "revisionId": "rev1",
        "items": [],
    }


@pytest.fixture()
def form_config_file(tmp_path: Path) -> Path:
    """A minimal valid form config JSON file."""
    f = tmp_path / "form.json"
    f.write_text(json.dumps({"title": "Test Form"}), encoding="utf-8")
    return f


@pytest.fixture()
def update_config_file(tmp_path: Path) -> Path:
    """A minimal valid update config JSON file."""
    f = tmp_path / "update.json"
    f.write_text(json.dumps({"title": "Updated Form"}), encoding="utf-8")
    return f


@pytest.fixture()
def sa_file(tmp_path: Path) -> Path:
    """A fake service account file (content irrelevant; auth is always mocked)."""
    f = tmp_path / "sa.json"
    f.write_text("{}", encoding="utf-8")
    return f
