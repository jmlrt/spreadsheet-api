===========
spreadsheet-api
===========

Generate a basic REST API from your Google spreadsheet

Requirements
============

This project is using ASDF_ and Poetry_.

A GCP service account with appropriate permissions is also required to read your
Google Spreadsheet:

- Enable the GoogleSheetAPI_ on your GCP project.
- Create a GoogleServiceAccount_.
- Retrieve the service account credentials.
- Share your Google Spreadsheet with the client email found in the service
  account credentials file (doesn't work with public spreadsheets).

.. _ASDF: https://asdf-vm.com/
.. _Poetry: https://python-poetry.org/
.. _GoogleSheetAPI: https://console.cloud.google.com/apis/library/sheets.googleapis.com
.. _GoogleServiceAccount: https://console.cloud.google.com/iam-admin/serviceaccounts/
