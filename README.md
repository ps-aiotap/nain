# n8n Docker Setup with Automation Service

This setup provides a complete automation platform with:
- **n8n**: Visual workflow automation (Port 5678)
- **Automation Service**: Production-grade Python microservice (Port 8080)
- Data persistence and networking between services

## Services

### n8n (Workflow Automation)
- Visual workflow builder
- Basic authentication enabled
- Webhook and API integrations

### Automation Service (Python Microservice)
- FastAPI-based webhook processor
- Google Sheets logging
- Multi-provider WhatsApp messaging (Gupshup, Twilio, Interakt)
- Email fallback notifications
- Structured logging and error handling

## Quick Start

1. **Configure automation service**:
```bash
cd automation-service
cp .env .env.local
# Edit .env.local with your API credentials
```

2. **Start all services**:
```bash
docker-compose up -d
```

3. **Access services**:
- n8n: http://localhost:5678 (admin/securepassword123)
- Automation API: http://localhost:8080
- Health check: http://localhost:8080/health

4. **Test automation webhook**:
```bash
curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -d @automation-service/example_payload.json
```

5. **Stop services**:
```bash
docker-compose down
```

## Configuration

Edit the `.env` file to change:
- `N8N_HOST`: Hostname for webhooks
- `N8N_BASIC_AUTH_USER`: Admin username
- `N8N_BASIC_AUTH_PASSWORD`: Admin password

## Data Persistence

All n8n data is stored in the `n8n_data` Docker volume. This ensures your workflows, credentials, and settings persist between container restarts.

## Integration Example

Create an n8n workflow that sends data to the automation service:

1. **HTTP Request Node** in n8n:
   - URL: `http://automation-service:8080/webhook`
   - Method: POST
   - Headers: `Content-Type: application/json`
   - Body: Your form/trigger data

2. **Automation Service** will:
   - Log data to Google Sheets
   - Send WhatsApp message
   - Send email fallback if messaging fails
   - Return structured status response

## Security Notes

- Change default passwords in `.env` files
- Configure API credentials in `automation-service/.env`
- Use HTTPS with reverse proxy in production
- Restrict network access and implement rate limiting
- Monitor logs for security events

## Troubleshooting

### Service Communication
- Services communicate via Docker network `n8n-network`
- Use service names as hostnames (e.g., `automation-service:8080`)
- Check logs: `docker-compose logs automation-service`

### Common Issues
- **Port conflicts**: Ensure ports 5678 and 8080 are available
- **Credential errors**: Verify API keys in automation-service/.env
- **Network issues**: Check Docker network connectivity

For detailed setup and troubleshooting, see `automation-service/README.md`