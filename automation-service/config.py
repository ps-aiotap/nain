import os
from dataclasses import dataclass

@dataclass
class Config:
    # Google Sheets
    GOOGLE_CREDENTIALS_FILE: str = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
    GOOGLE_SHEET_ID: str = os.getenv('GOOGLE_SHEET_ID', '')
    GOOGLE_SHEET_NAME: str = os.getenv('GOOGLE_SHEET_NAME', 'Sheet1')
    
    # Messaging Services
    GUPSHUP_API_KEY: str = os.getenv('GUPSHUP_API_KEY', '')
    GUPSHUP_APP_NAME: str = os.getenv('GUPSHUP_APP_NAME', '')
    
    TWILIO_ACCOUNT_SID: str = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN: str = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_WHATSAPP_FROM: str = os.getenv('TWILIO_WHATSAPP_FROM', '')
    
    INTERAKT_API_KEY: str = os.getenv('INTERAKT_API_KEY', '')
    
    # Email Service
    SMTP_HOST: str = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT: int = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER: str = os.getenv('SMTP_USER', '')
    SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD', '')
    
    SENDGRID_API_KEY: str = os.getenv('SENDGRID_API_KEY', '')
    FROM_EMAIL: str = os.getenv('FROM_EMAIL', '')
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'automation.log')