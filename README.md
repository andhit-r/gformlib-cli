# gformlib-cli

[![PyPI version](https://badge.fury.io/py/gformlib-cli.svg)](https://pypi.org/project/gformlib-cli/)
[![Python versions](https://img.shields.io/pypi/pyversions/gformlib-cli.svg)](https://pypi.org/project/gformlib-cli/)
[![CI](https://github.com/andhit-r/gformlib-cli/actions/workflows/test.yml/badge.svg)](https://github.com/andhit-r/gformlib-cli/actions/workflows/test.yml)
[![Documentation Status](https://readthedocs.org/projects/gformlib-cli/badge/?version=latest)](https://gformlib-cli.readthedocs.io/en/latest/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**gformlib-cli** is the official command-line interface for
[gformlib](https://github.com/andhit-r/gformlib) — manage Google Forms
directly from your terminal.

## Features

- Create Google Forms from a JSON config file
- Update form title, description, and add questions
- Retrieve form metadata and structure
- List form responses with optional filtering
- Delete forms (with confirmation)
- Service account & OAuth 2.0 authentication
- Beautiful Rich terminal output
- Full type annotations (PEP 561 compliant)

## Installation

```bash
pip install gformlib-cli
```

## Quickstart

### Authenticate

Pass a service account key file with every command:

```bash
gformcli form create form.json --service-account sa.json
```

Or set the environment variable once:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json
gformcli form create form.json
```

### Create a form

```bash
gformcli form create form.json --service-account sa.json
```

`form.json`:

```json
{
  "title": "Customer Survey",
  "description": "Tell us how we're doing.",
  "questions": [
    {"title": "Your name", "type": "short_answer", "required": true},
    {
      "title": "Overall rating",
      "type": "scale",
      "low": 1,
      "high": 5,
      "low_label": "Poor",
      "high_label": "Excellent"
    }
  ]
}
```

### Update a form

```bash
gformcli form update <FORM_ID> update.json --service-account sa.json
```

### Get form info

```bash
gformcli form get <FORM_ID> --service-account sa.json
```

### List responses

```bash
gformcli form responses <FORM_ID> --service-account sa.json
```

### Delete a form

```bash
gformcli form delete <FORM_ID> --yes --service-account sa.json
```

## Authentication

| Method | Flag | Notes |
|---|---|---|
| Service Account | `--service-account / -s` | Recommended for server/CI |
| OAuth 2.0 | `--credentials / -c` | Browser consent on first run |
| Env var | `GOOGLE_APPLICATION_CREDENTIALS` | Fallback, service account |

## Command reference

```
gformcli form create   CONFIG_FILE  [AUTH OPTIONS]
gformcli form update   FORM_ID  CONFIG_FILE  [AUTH OPTIONS]
gformcli form get      FORM_ID  [AUTH OPTIONS]
gformcli form responses FORM_ID  [--filter STR]  [--page-size N]  [AUTH OPTIONS]
gformcli form delete   FORM_ID  [--yes]  [AUTH OPTIONS]
```

Run `gformcli --help` or `gformcli form <command> --help` for full option details.

## Development

```bash
git clone https://github.com/andhit-r/gformlib-cli
cd gformlib-cli
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## License

MIT — see [LICENSE](LICENSE).
