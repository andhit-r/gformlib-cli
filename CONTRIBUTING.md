# Contributing

Thank you for your interest in contributing to **gformlib-cli**!

## Development setup

```bash
git clone https://github.com/andhit-r/gformlib-cli
cd gformlib-cli
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Running tests

```bash
pytest                             # run all tests
pytest tests/test_auth.py -v       # single file
pytest --cov=gformlib_cli          # with coverage
```

## Linting & formatting

```bash
black src tests                    # auto-format
isort src tests                    # sort imports
flake8 src tests                   # lint
mypy src/gformlib_cli              # type-check
```

Or run everything via tox:

```bash
tox -e lint,type
```

## Branching & pull requests

1. Fork the repository and create a feature branch:
   ```bash
   git checkout -b feat/my-feature
   ```
2. Make your changes, add tests, and ensure everything passes.
3. Open a pull request against `master`.

Please keep PRs focused on a single concern and include tests for new behaviour.

## Versioning

This project uses [Semantic Versioning](https://semver.org/). Version numbers
are updated in `pyproject.toml` before tagging a release.
