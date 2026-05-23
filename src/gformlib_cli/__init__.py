"""gformlib-cli – Command-line interface for gformlib.

Manage Google Forms from the terminal::

    gformcli form create form.json --service-account sa.json
    gformcli form update <form-id> update.json --service-account sa.json
    gformcli form get <form-id> --service-account sa.json
    gformcli form responses <form-id> --service-account sa.json
    gformcli form delete <form-id> --yes --service-account sa.json
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("gformlib-cli")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

__all__ = ["__version__"]
