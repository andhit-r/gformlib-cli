# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] – 2026-05-23

### Added
- Initial release.
- `gformcli form create` – create a Google Form from a JSON config file.
- `gformcli form update` – update title, description, or add questions.
- `gformcli form get` – retrieve form metadata and structure.
- `gformcli form responses` – list submitted responses with pagination.
- `gformcli form delete` – move a form to Drive trash (with confirmation).
- Service account, OAuth 2.0, and `GOOGLE_APPLICATION_CREDENTIALS` auth support.
- Rich terminal output with tables and coloured status messages.
- Full type annotations and PEP 561 `py.typed` marker.
- Unit tests with pytest and `pytest-mock`.
- GitHub Actions: test (lint + pytest matrix), publish to PyPI, ReadTheDocs docs trigger.
- Sphinx documentation with ReadTheDocs theme.

[Unreleased]: https://github.com/andhit-r/gformlib-cli/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/andhit-r/gformlib-cli/releases/tag/v0.1.0
