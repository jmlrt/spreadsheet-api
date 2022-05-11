class Config:
    # GCP service account to access the spreadsheet
    SERVICE_ACCOUNT_FILE = "credentials.json"

    # route name
    ROUTE_NAME = "datas"

    # https://docs.google.com/spreadsheets/d/<spreadsheetId>/
    SPREADSHEET_ID = "<spreadsheetId>"

    # worksheetName and range
    SPREADSHEET_RANGE = "Sheet1!A1:E9"

    # mapping of the column names (should contain an item for every column in the range)
    SPREADSHEET_COLUMNS = [
        "a",
        "b",
        "c",
        "d",
        "e",
    ]
