# -*- coding: utf-8 -*-
"""Quart app and routes"""

from quart import Quart, jsonify, render_template

from spreadsheet_api.config import Config
from spreadsheet_api.worksheet import Worksheet

app = Quart(__name__)
app.config.from_object(Config)
app.config.from_envvar("QUART_CONFIG")
route = app.config["ROUTE_NAME"]


@app.route("/", methods=["GET"])
async def index():
    """Return API index"""
    return await render_template(
        "index.html", spreadsheet_id=app.config["SPREADSHEET_ID"], route=route
    )


@app.route(f"/api/v1/{route}", methods=["GET"])
async def get_sheet():
    """Return spreadsheet keys"""
    app.logger.debug("/api/v1/%s", route)
    worksheet = await get_worksheet()
    sheet = await worksheet.get_sheet()
    return jsonify({route: sheet})


@app.route(f"/api/v1/{route}/<int:key>", methods=["GET"])
async def get_row_by_key(key):
    """Return spreadsheet row for a key"""
    app.logger.debug("/api/v1/%s/<key>", route)
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
        app.logger.debug("worksheet already loaded: %s", app.worksheet)
    return app.worksheet
