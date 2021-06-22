import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe

# Authentication of credentials
sheets_scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
sheets_credentials = Credentials.from_service_account_file(
    'YOUR CREDENTIALS FOR GOOGLE SHEETS OR DOCS API',
    scopes=sheets_scopes
)

# Creation of Your Spreadsheet, please take note of your spreadsheet ID by logging into your drive after that
gc = gspread.authorize(sheets_credentials)
sh = gc.create("YOUR WORKSHEET TITLE")
sh.share('YOUR EMAIL ADDRESS', perm_type = 'user', role = 'writer')
print(sh)
