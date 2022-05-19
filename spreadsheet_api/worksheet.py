# -*- coding: utf-8 -*-
"""Google worksheet"""

import json
from collections import namedtuple

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


class Worksheet:
    """A class representing a worksheet from a Google Spreadsheet"""

    def __init__(self, service_account, sid, srange, column_names):
        """Initialize a worksheet from a Google Spreadsheet"""
        self.service_account = service_account
        self.id = sid
        self.range = srange
        row_default_values = [""] * (len(column_names) - 1)
        self.row_named_tuple = namedtuple(
            "Row", column_names, defaults=row_default_values
        )
        self.rows = {}

    async def load_sheet(self, clear=False):
        """Load all worksheet rows"""
        if clear:
            self.rows.clear()
        else:
            # TODO check file modification date instead
            # https://developers.google.com/drive/api/v3/reference/files
            if len(self.rows) > 0:
                return
        async for row in self.load_sheet_row():
            try:
                key = len(self.rows) + 1
                row = self.row_named_tuple(*row)
                self.rows[key] = row
            # IndexError handle error for row with 0 columns
            # TypeError handle error for row returning None
            except (IndexError, TypeError):
                continue

    async def load_sheet_row(self):
        """Fetch the worksheet values and return line by line"""
        with open(self.service_account) as f:
            service_account_key = json.load(f)
        creds = ServiceAccountCreds(scopes=SCOPES, **service_account_key)
        async with Aiogoogle(service_account_creds=creds) as aiogoogle:
            service = await aiogoogle.discover("sheets", "v4")
            sheet = await aiogoogle.as_service_account(
                service.spreadsheets.values.get(spreadsheetId=self.id, range=self.range)
            )
        for line in sheet["values"]:
            yield line

    async def get_sheet(self):
        """Return all sheet rows"""
        await self.load_sheet()
        rows = []
        for key in self.rows.keys():
            rows.append(await self.get_row(key))
        return rows

    async def get_row(self, key):
        """Return the row for a given key"""
        await self.load_sheet()
        # TODO: filter fields starting by "empty_columns"
        row = {}
        row["id"] = key
        # This is using the union operator for merging dict introduced in
        # Python 3.9 (https://peps.python.org/pep-0584/)
        row |= self.rows[key]._asdict()
        return row
