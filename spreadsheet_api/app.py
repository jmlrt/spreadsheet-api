# -*- coding: utf-8 -*-
"""Quart app and routes"""

import toml
from quart import Quart

from spreadsheet_api.worksheet import Worksheet

_APP = None


def get_app(config_file=None):
    """Initialize Quart app if it doesn't exists"""
    global _APP

    if _APP is None:
        _APP = Quart(__name__)
        _APP.worksheet = None
    if _APP.worksheet is None and config_file is not None:
        _APP.config.from_file(config_file, load=toml.load)
        _APP.worksheet = Worksheet(
            _APP.config["SERVICE_ACCOUNT_FILE"],
            _APP.config["SPREADSHEET"]["ID"],
            _APP.config["SPREADSHEET"]["RANGE"],
            _APP.config["SPREADSHEET"]["COLUMN_NAMES"],
        )
    return _APP


@get_app().route("/keys", methods=["GET"])
async def get_keys():
    """Return spreadsheet keys"""
    keys = await _APP.worksheet.get_keys()
    return {"keys": list(keys)}


@get_app().route("/row/<key>", methods=["GET"])
async def get_row_by_key(key):
    """Return spreadsheet row for a key"""
    return await _APP.worksheet.get_row(key)
