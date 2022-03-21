# -*- coding: utf-8 -*-
"""Spreadsheet API"""

import argparse

from spreadsheet_api.app import get_app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--config", help="path of the configuration file", required=True
    )
    args = parser.parse_args()
    app = get_app(args.config)
    app.run()


if __name__ == "__main__":
    main()
