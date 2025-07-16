import os
from dotenv import load_dotenv

REQUIRED_ENV_VARS = [
    "GOOGLE_CREDENTIALS_FILE",
    "GOOGLE_SHEET_ID",
    "GOOGLE_SHEET_NAME",
    "GUPSHUP_API_KEY",
    "GUPSHUP_APP_NAME",
    "TWILIO_ACCOUNT_SID",
    "TWILIO_AUTH_TOKEN",
    "TWILIO_WHATSAPP_FROM",
    "INTERAKT_API_KEY",
    "SMTP_HOST",
    "SMTP_PORT",
    "SMTP_USER",
    "SMTP_PASSWORD",
    # Optional: Uncomment if using SendGrid
    # "SENDGRID_API_KEY",
    "FROM_EMAIL",
    "LOG_LEVEL",
    "LOG_FILE",
    "PORT",
]


def check_env():
    load_dotenv(dotenv_path=".env.local")
    missing = []

    for var in REQUIRED_ENV_VARS:
        value = os.getenv(var)
        if not value:
            missing.append(var)

    if missing:
        print("❌ Missing or empty environment variables:")
        for var in missing:
            print(f" - {var}")
        exit(1)
    else:
        print("✅ All required environment variables are set.")


if __name__ == "__main__":
    check_env()
