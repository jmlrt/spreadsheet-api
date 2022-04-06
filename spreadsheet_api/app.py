# -*- coding: utf-8 -*-
"""Quart app and routes"""

from quart import Quart, jsonify

from spreadsheet_api.config import Config
from spreadsheet_api.worksheet import Worksheet

app = Quart(__name__)
app.config.from_object(Config)
app.config.from_envvar("QUART_CONFIG")


@app.route("/api/v1/keys", methods=["GET"])
async def get_keys():
    """Return spreadsheet keys"""
    worksheet = await get_worksheet()
    keys = await worksheet.get_keys()
    return jsonify({"keys": list(keys)})


@app.route("/api/v1/row/<key>", methods=["GET"])
async def get_row_by_key(key):
    """Return spreadsheet row for a key"""
    worksheet = await get_worksheet()
    row = await worksheet.get_row(key)
    return jsonify(row)


async def get_worksheet():
    """Load the worksheet if it wasn't loaded before, then return it"""
    if not hasattr(app, "worksheet"):
        app.logger.debug("worksheet not loaded")
        app.worksheet = Worksheet(
            app.config["SERVICE_ACCOUNT_FILE"],
            app.config["SPREADSHEET_ID"],
            app.config["SPREADSHEET_RANGE"],
            app.config["SPREADSHEET_COLUMNS"],
        )
    else:
        app.logger.debug(f"worksheet already loaded: {app.worksheet}")
    return app.worksheet
