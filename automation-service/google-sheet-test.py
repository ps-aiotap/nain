import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file("credentials.json")
client = gspread.authorize(creds)
sheet = client.open_by_key("your_google_sheet_id_here")
worksheet = sheet.worksheet("Sheet1")
worksheet.append_row(["Test", "Row", "Success"])
