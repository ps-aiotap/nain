# Automation Workflow Service

A production-grade Python microservice for external automation workflows that integrates seamlessly with n8n. This service provides webhook endpoints, Google Sheets logging, multi-provider messaging (WhatsApp), and email fallbacks.

## Features

- **FastAPI-based** high-performance async web service
- **Webhook endpoint** for receiving form submissions and external data
- **Google Sheets integration** with OAuth2 authentication
- **Multi-provider messaging** with automatic fallbacks:
  - Gupshup (primary)
  - Twilio (fallback)
  - Interakt (fallback)
- **Email notifications** via SendGrid or SMTP
- **Structured JSON logging** for production monitoring
- **Docker containerized** with health checks
- **Graceful error handling** and comprehensive fallback mechanisms

## Quick Start

1. **Clone and setup**:
```bash
cd automation-service
cp .env.example .env
# Edit .env with your API credentials
```

2. **Start with Docker Compose**:
```bash
cd ..
docker-compose up -d
```

3. **Test the service**:
```bash
curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "message": "Hello from automation service!"
  }'
```

## API Endpoints

### POST /webhook
Processes incoming webhook data and executes the automation workflow.

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "message": "Custom message text"
}
```

**Response**:
```json
{
  "success": true,
  "request_id": "20231201_143022_123456",
  "result": {
    "sheets_logged": true,
    "message_sent": true,
    "fallback_executed": false,
    "email_sent": false
  }
}
```

### GET /health
Health check endpoint for monitoring.

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Google Sheets Configuration
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_ID=your_google_sheet_id
GOOGLE_SHEET_NAME=Sheet1

# Messaging Services (configure at least one)
GUPSHUP_API_KEY=your_gupshup_api_key
GUPSHUP_APP_NAME=your_gupshup_app_name

TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+1234567890

INTERAKT_API_KEY=your_interakt_api_key

# Email Configuration (configure at least one)
SENDGRID_API_KEY=your_sendgrid_api_key
FROM_EMAIL=noreply@yourdomain.com

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Logging
LOG_LEVEL=INFO
LOG_FILE=automation.log
```

## Service Setup Instructions

### 1. Google Sheets API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Sheets API
4. Create service account credentials
5. Download JSON credentials file as `credentials.json`
6. Share your Google Sheet with the service account email
7. Copy the Sheet ID from the URL

### 2. Messaging Services Setup

#### Gupshup (Recommended)
1. Sign up at [Gupshup](https://www.gupshup.io/)
2. Create WhatsApp Business API app
3. Get API key and app name
4. Configure webhook URL (optional)

#### Twilio (Fallback)
1. Sign up at [Twilio](https://www.twilio.com/)
2. Get Account SID and Auth Token
3. Enable WhatsApp sandbox or get approved number
4. Set WhatsApp-enabled phone number

#### Interakt (Fallback)
1. Sign up at [Interakt](https://www.interakt.ai/)
2. Get API key from dashboard
3. Configure WhatsApp templates

### 3. Email Services Setup

#### SendGrid (Recommended)
1. Sign up at [SendGrid](https://sendgrid.com/)
2. Create API key with Mail Send permissions
3. Verify sender email address

#### SMTP (Fallback)
1. Use Gmail App Password or other SMTP provider
2. Enable 2FA and generate app-specific password
3. Configure SMTP settings

## Integration with n8n

1. **Create HTTP Request Node** in n8n workflow
2. **Set URL**: `http://automation-service:8080/webhook`
3. **Method**: POST
4. **Headers**: `Content-Type: application/json`
5. **Body**: Map your form data to the expected format

Example n8n workflow:
```
Form Trigger → Set Node (format data) → HTTP Request (automation-service) → End
```

## Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn app:app --reload --port 8080

# Run tests
python -m pytest tests/
```

### Docker Development
```bash
# Build image
docker build -t automation-service .

# Run container
docker run -p 8080:8080 --env-file .env automation-service
```

## Monitoring and Logging

The service provides structured JSON logging with the following fields:
- `timestamp`: ISO format timestamp
- `level`: Log level (INFO, ERROR, WARNING)
- `request_id`: Unique identifier for each request
- `message`: Log message
- `data`: Additional context data

Logs are output to both console (for Docker) and file (configurable).

## Production Deployment

### Security Considerations
- Use strong API keys and rotate regularly
- Implement rate limiting (via reverse proxy)
- Use HTTPS in production
- Restrict network access with firewall rules
- Monitor logs for suspicious activity

### Scaling
- Service is stateless and can be horizontally scaled
- Use load balancer for multiple instances
- Consider using external logging service (ELK stack)
- Monitor resource usage and set appropriate limits

## Troubleshooting

### Common Issues

1. **Google Sheets Permission Denied**
   - Ensure service account email has edit access to the sheet
   - Verify credentials.json file is properly mounted

2. **Messaging Service Failures**
   - Check API credentials and quotas
   - Verify phone number format (+country_code)
   - Review service-specific documentation

3. **Email Delivery Issues**
   - Check spam folders
   - Verify sender email is authenticated
   - Review SMTP/SendGrid logs

### Debug Mode
Set `LOG_LEVEL=DEBUG` in environment variables for detailed logging.

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review service logs
3. Consult API provider documentation
4. Create GitHub issue with logs and configuration (remove sensitive data)