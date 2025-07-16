@echo off
echo Starting n8n with Docker...
cd /d "%~dp0"
docker-compose up -d
echo.
echo n8n is now running!
echo Access at: http://localhost:5678
echo Username: admin
echo Password: securepassword123
echo.
echo To stop n8n, run: docker-compose down