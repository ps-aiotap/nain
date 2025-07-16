import asyncio
import smtplib
import aiohttp
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.config = Config()
    
    async def send_notification(self, to_email, subject, message):
        # Try SendGrid first
        if self.config.SENDGRID_API_KEY:
            try:
                await self._send_sendgrid(to_email, subject, message)
                return
            except Exception as e:
                logger.warning(f"SendGrid failed: {str(e)}")
        
        # Fallback to SMTP
        try:
            await self._send_smtp(to_email, subject, message)
        except Exception as e:
            logger.error(f"SMTP failed: {str(e)}")
            raise Exception("All email services failed")
    
    async def _send_sendgrid(self, to_email, subject, message):
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            "Authorization": f"Bearer {self.config.SENDGRID_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "personalizations": [{
                "to": [{"email": to_email}]
            }],
            "from": {"email": self.config.FROM_EMAIL},
            "subject": subject,
            "content": [{
                "type": "text/plain",
                "value": message
            }]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status != 202:
                    raise Exception(f"SendGrid API error: {response.status}")
                logger.info("Email sent via SendGrid")
    
    async def _send_smtp(self, to_email, subject, message):
        if not self.config.SMTP_USER:
            raise Exception("SMTP not configured")
        
        def send_smtp_email():
            msg = MIMEMultipart()
            msg['From'] = self.config.SMTP_USER
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(self.config.SMTP_HOST, self.config.SMTP_PORT)
            server.starttls()
            server.login(self.config.SMTP_USER, self.config.SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
        
        await asyncio.to_thread(send_smtp_email)
        logger.info("Email sent via SMTP")