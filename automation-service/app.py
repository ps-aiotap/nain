import os
import asyncio
import logging
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, Any
import signal
import sys

from services.sheets_service import SheetsService
from services.messaging_service import MessagingService
from services.email_service import EmailService
from utils.logger import setup_logger
from config import Config

logger = setup_logger(__name__)

# Initialize services
sheets_service = SheetsService()
messaging_service = MessagingService()
email_service = EmailService()

def graceful_shutdown(signum, frame):
    logger.info("Received shutdown signal, gracefully shutting down...")
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting automation service...")
    yield
    logger.info("Shutting down automation service...")

app = FastAPI(
    title="Automation Workflow Service",
    description="Production-grade microservice for n8n automation workflows",
    version="1.0.0",
    lifespan=lifespan
)

class WebhookPayload(BaseModel):
    data: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    timestamp: str

class WebhookResponse(BaseModel):
    success: bool
    request_id: str
    result: Dict[str, bool]

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat()
    )

@app.post("/webhook", response_model=WebhookResponse)
async def webhook_handler(payload: Dict[str, Any]):
    request_id = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
    
    try:
        if not payload:
            raise HTTPException(status_code=400, detail="No data provided")
        
        logger.info(f"[{request_id}] Webhook received", extra={"request_id": request_id, "data": payload})
        
        # Process workflow
        result = await process_workflow(request_id, payload)
        
        return WebhookResponse(
            success=True,
            request_id=request_id,
            result=result
        )
        
    except Exception as e:
        logger.error(f"[{request_id}] Webhook processing failed: {str(e)}", extra={"request_id": request_id})
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "request_id": request_id,
                "error": str(e)
            }
        )

async def process_workflow(request_id, data):
    workflow_status = {
        "sheets_logged": False,
        "message_sent": False,
        "fallback_executed": False,
        "email_sent": False
    }
    
    # Step 1: Log to Google Sheets
    try:
        await sheets_service.log_data(data)
        workflow_status["sheets_logged"] = True
        logger.info(f"[{request_id}] Data logged to Google Sheets", extra={"request_id": request_id})
    except Exception as e:
        logger.error(f"[{request_id}] Failed to log to Google Sheets: {str(e)}", extra={"request_id": request_id})
    
    # Step 2: Send WhatsApp message
    phone = data.get('phone') or data.get('mobile') or data.get('whatsapp')
    message = data.get('message', 'Thank you for your submission!')
    
    if phone:
        try:
            await messaging_service.send_message(phone, message)
            workflow_status["message_sent"] = True
            logger.info(f"[{request_id}] Message sent successfully", extra={"request_id": request_id})
        except Exception as e:
            logger.error(f"[{request_id}] All messaging services failed: {str(e)}", extra={"request_id": request_id})
            workflow_status["fallback_executed"] = True
    
    # Step 3: Always send email notification
    email = data.get('email')
    if email:
        try:
            subject = "Form Submission Received" if workflow_status["message_sent"] else "Message Delivery Failed"
            body = f"Thank you for your submission: {message}" if workflow_status["message_sent"] else f"Could not deliver WhatsApp message: {message}"
            await email_service.send_notification(email, subject, body)
            workflow_status["email_sent"] = True
            logger.info(f"[{request_id}] Email notification sent", extra={"request_id": request_id})
        except Exception as email_error:
            logger.error(f"[{request_id}] Email notification failed: {str(email_error)}", extra={"request_id": request_id})
    
    # Log final status
    logger.info(f"[{request_id}] Workflow completed", extra={"request_id": request_id, "status": workflow_status})
    
    return workflow_status

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv('PORT', 8080)),
        reload=False,
        log_level="info"
    )