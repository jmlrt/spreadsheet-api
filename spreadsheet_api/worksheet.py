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
        if clear:
            self.rows.clear()
        else:
            # TODO check file modification date instead
            # https://developers.google.com/drive/api/v3/reference/files
            if len(self.rows) > 0:
                return
        # get key (first column of the row)
        async for row in self.get_sheet_row():
            try:
                row = self.row_named_tuple(*row)
                self.rows[row[0]] = row
            # IndexError handle error for row with 0 columns
            # TypeError handle error for row returning None
            except (IndexError, TypeError):
                continue

    async def get_sheet_row(self):
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

    async def get_keys(self):
        """Get the keys (first column of the worksheet)"""
        await self.load_sheet()
        return self.rows.keys()

    async def get_row(self, key):
        """Get the row for a key (full row of the worksheet starting by the key)"""
        await self.load_sheet()
        # TODO: filter fields starting by "empty_columns"
        return self.rows[key]._asdict()
