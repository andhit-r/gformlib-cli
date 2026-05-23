Usage
=====

All commands follow the pattern::

   gformcli form <command> [ARGS] [OPTIONS]

Authentication options are the same for every command:

.. option:: --service-account, -s <PATH>

   Path to a service account JSON key file.

.. option:: --credentials, -c <PATH>

   Path to an OAuth 2.0 client secrets JSON file.

.. option:: --token-file, -t <PATH>

   Where to cache the OAuth token (default: ``token.json``).

If none of these options are provided the ``GOOGLE_APPLICATION_CREDENTIALS``
environment variable is used as a fallback.

----

form create
-----------

Create a new Google Form from a JSON config file.

.. code-block:: console

   $ gformcli form create form.json --service-account sa.json

**Config file format:**

.. code-block:: json

   {
     "title": "Customer Satisfaction Survey",
     "description": "Tell us how we're doing.",
     "questions": [
       {
         "title": "Your name",
         "type": "short_answer",
         "required": true
       },
       {
         "title": "Overall rating",
         "type": "scale",
         "low": 1,
         "high": 5,
         "low_label": "Poor",
         "high_label": "Excellent"
       },
       {
         "title": "Favourite option",
         "type": "multiple_choice",
         "options": ["Option A", "Option B", "Option C"]
       }
     ]
   }

Supported question types: ``short_answer``, ``paragraph``, ``multiple_choice``,
``checkboxes``, ``dropdown``, ``scale``, ``date``, ``time``, ``file_upload``.

----

form update
-----------

Update an existing Google Form.

.. code-block:: console

   $ gformcli form update <FORM_ID> update.json --service-account sa.json

**Update config file format:**

.. code-block:: json

   {
     "title": "Revised Survey",
     "description": "Updated description.",
     "add_questions": [
       {"title": "Any comments?", "type": "paragraph"}
     ]
   }

All keys are optional. Only the keys that are present will be applied.

----

form get
--------

Retrieve metadata and question structure of an existing form.

.. code-block:: console

   $ gformcli form get <FORM_ID> --service-account sa.json

----

form responses
--------------

List response submissions for a form.

.. code-block:: console

   $ gformcli form responses <FORM_ID> --service-account sa.json

Filter by timestamp:

.. code-block:: console

   $ gformcli form responses <FORM_ID> \
       --filter "timestamp > 2024-01-01T00:00:00Z" \
       --service-account sa.json

----

form delete
-----------

Move a form to the Google Drive trash.

.. code-block:: console

   $ gformcli form delete <FORM_ID> --yes --service-account sa.json

Omitting ``--yes`` shows an interactive confirmation prompt.
