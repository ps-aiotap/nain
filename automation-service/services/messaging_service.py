import asyncio
import aiohttp
import logging
from twilio.rest import Client as TwilioClient
from config import Config

logger = logging.getLogger(__name__)

class MessagingService:
    def __init__(self):
        self.config = Config()
    
    async def send_message(self, phone, message):
        # Try Gupshup first
        try:
            await self._send_gupshup(phone, message)
            return
        except Exception as e:
            logger.warning(f"Gupshup failed: {str(e)}")
        
        # Try Twilio
        try:
            await self._send_twilio(phone, message)
            return
        except Exception as e:
            logger.warning(f"Twilio failed: {str(e)}")
        
        # Try Interakt
        try:
            await self._send_interakt(phone, message)
            return
        except Exception as e:
            logger.warning(f"Interakt failed: {str(e)}")
        
        raise Exception("All messaging services failed")
    
    async def _send_gupshup(self, phone, message):
        if not self.config.GUPSHUP_API_KEY:
            raise Exception("Gupshup not configured")
        
        url = "https://api.gupshup.io/sm/api/v1/msg"
        headers = {
            "apikey": self.config.GUPSHUP_API_KEY,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "channel": "whatsapp",
            "source": self.config.GUPSHUP_APP_NAME,
            "destination": phone,
            "message": message
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                if response.status != 200:
                    raise Exception(f"Gupshup API error: {response.status}")
                logger.info("Message sent via Gupshup")
    
    async def _send_twilio(self, phone, message):
        if not self.config.TWILIO_ACCOUNT_SID:
            raise Exception("Twilio not configured")
        
        def send_twilio_message():
            client = TwilioClient(self.config.TWILIO_ACCOUNT_SID, self.config.TWILIO_AUTH_TOKEN)
            return client.messages.create(
                from_=self.config.TWILIO_WHATSAPP_FROM,
                body=message,
                to=f"whatsapp:{phone}"
            )
        
        await asyncio.to_thread(send_twilio_message)
        logger.info("Message sent via Twilio")
    
    async def _send_interakt(self, phone, message):
        if not self.config.INTERAKT_API_KEY:
            raise Exception("Interakt not configured")
        
        url = "https://api.interakt.ai/v1/public/message/"
        headers = {
            "Authorization": f"Basic {self.config.INTERAKT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "countryCode": "+91",
            "phoneNumber": phone,
            "type": "Template",
            "template": {
                "name": "hello_world",
                "languageCode": "en",
                "bodyValues": [message]
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status != 200:
                    raise Exception(f"Interakt API error: {response.status}")
                logger.info("Message sent via Interakt")