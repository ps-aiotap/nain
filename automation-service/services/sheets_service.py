import asyncio
import json
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import Config
import logging

logger = logging.getLogger(__name__)

class SheetsService:
    def __init__(self):
        self.config = Config()
        self.service = None
        self._initialize_service()
    
    def _initialize_service(self):
        try:
            if not self.config.GOOGLE_CREDENTIALS_FILE or not self.config.GOOGLE_SHEET_ID:
                logger.warning("Google Sheets credentials not configured")
                return
            
            credentials = Credentials.from_service_account_file(
                self.config.GOOGLE_CREDENTIALS_FILE,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self.service = build('sheets', 'v4', credentials=credentials)
            logger.info("Google Sheets service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets service: {str(e)}")
    
    async def log_data(self, data):
        if not self.service:
            raise Exception("Google Sheets service not initialized")
        
        try:
            # Prepare row data
            timestamp = datetime.utcnow().isoformat()
            row_data = [
                timestamp,
                json.dumps(data),
                data.get('name', ''),
                data.get('email', ''),
                data.get('phone', ''),
                data.get('message', '')
            ]
            
            # Append to sheet
            body = {
                'values': [row_data]
            }
            
            result = await asyncio.to_thread(
                self.service.spreadsheets().values().append,
                spreadsheetId=self.config.GOOGLE_SHEET_ID,
                range=f"{self.config.GOOGLE_SHEET_NAME}!A:F",
                valueInputOption='RAW',
                body=body
            )
            
            await asyncio.to_thread(result.execute)
            logger.info("Data logged to Google Sheets successfully")
            
        except HttpError as e:
            logger.error(f"Google Sheets API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Failed to log data to Google Sheets: {str(e)}")
            raise