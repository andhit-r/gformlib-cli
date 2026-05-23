Installation
============

Requirements
------------

* Python 3.9 or newer
* A Google Cloud project with the **Google Forms API** enabled
* Either a **Service Account** key file or an **OAuth 2.0** client secrets file

Install from PyPI
-----------------

.. code-block:: console

   $ pip install gformlib-cli

This also installs `gformlib <https://pypi.org/project/gformlib/>`_ as a
dependency automatically.

Verify the installation
-----------------------

.. code-block:: console

   $ gformcli --version
   gformcli 0.1.0

Google Cloud setup
------------------

1. Go to the `Google Cloud Console <https://console.cloud.google.com/>`_.
2. Enable the **Google Forms API** and the **Google Drive API** for your project.
3. Create credentials:

   * **Service Account** (recommended for server/CI use) – download the JSON key
     file and pass it via ``--service-account``.
   * **OAuth 2.0 Desktop App** – download the ``client_secrets.json`` file and
     pass it via ``--credentials``.  The browser-based consent flow will run on
     first use and the resulting token is cached in ``token.json``.

Setting credentials via environment variable
--------------------------------------------

You can avoid passing ``--service-account`` on every command by setting:

.. code-block:: console

   $ export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json
