import asyncio

import urllib
import aiohttp
import logging
import re
from twilio.rest import Client as TwilioClient
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class MessagingService:
    def __init__(self):
        self.config = Config()

    async def send_message(self, phone, message):
        phone = self._sanitize_phone(phone)

        try:
            await self._send_gupshup(phone, message)
            return
        except Exception as e:
            logger.error(f"Gupshup failed: {e}")

        try:
            await self._send_twilio(phone, message)
            return
        except Exception as e:
            logger.warning(f"Twilio failed: {e}")

        try:
            await self._send_interakt(phone, message)
            return
        except Exception as e:
            logger.warning(f"Interakt failed: {e}")

        raise Exception("All messaging services failed")

    def _sanitize_phone(self, phone):
        # Keep only digits and '+'
        return re.sub(r"[^\d+]", "", phone)

    import urllib.parse

    import urllib.parse

    async def _send_gupshup(self, phone, message):
        logger.info(f"Gupshup config check - API Key: {'***' if self.config.GUPSHUP_API_KEY else 'MISSING'}, App: {self.config.GUPSHUP_APP_NAME}")
        if not self.config.GUPSHUP_API_KEY:
            raise Exception("Gupshup not configured")

        url = "https://api.gupshup.io/sm/api/v1/msg"
        headers = {
            "apikey": self.config.GUPSHUP_API_KEY,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        payload = {
            "channel": "whatsapp",
            "source": self.config.GUPSHUP_APP_NAME,
            "destination": phone,
            "src.name": self.config.GUPSHUP_APP_NAME,
            "message": f"{{\"type\":\"text\",\"text\":\"{message}\"}}"
        }

        logger.info(f"Sending Gupshup to {phone}: {payload}")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                resp_text = await response.text()
                logger.info(f"Gupshup response ({response.status}): {resp_text}")
                if response.status not in [200, 202]:
                    raise Exception(
                        f"Gupshup API error: {response.status} - {resp_text}"
                    )
                logger.info("Message sent via Gupshup")

    async def _send_twilio(self, phone, message):
        if not self.config.TWILIO_ACCOUNT_SID:
            raise Exception("Twilio not configured")

        def send_twilio_message():
            client = TwilioClient(
                self.config.TWILIO_ACCOUNT_SID, self.config.TWILIO_AUTH_TOKEN
            )
            return client.messages.create(
                from_=self.config.TWILIO_WHATSAPP_FROM,
                body=message,
                to=f"whatsapp:{phone}",
            )

        await asyncio.to_thread(send_twilio_message)
        logger.info("Message sent via Twilio")

    async def _send_interakt(self, phone, message):
        if not self.config.INTERAKT_API_KEY:
            raise Exception("Interakt not configured")

        url = "https://api.interakt.ai/v1/public/message/"
        headers = {
            "Authorization": f"Basic {self.config.INTERAKT_API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "countryCode": "+91",
            "phoneNumber": phone,
            "type": "Template",
            "template": {
                "name": "hello_world",
                "languageCode": "en",
                "bodyValues": [message],
            },
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                resp_text = await response.text()
                logger.debug(f"Interakt response ({response.status}): {resp_text}")
                if response.status != 200:
                    raise Exception(
                        f"Interakt API error: {response.status} - {resp_text}"
                    )
                logger.info("Message sent via Interakt")
