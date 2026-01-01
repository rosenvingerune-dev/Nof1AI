# Ensure we are in the project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$ScriptDir/.."

Write-Host "Stopping existing bot..."
docker compose down

Write-Host "Rebuilding and starting..."
docker compose up -d --build
Write-Host "Bot started in background! 🚀"
Write-Host "Access UI at http://localhost:8081"
Write-Host "To stop: docker compose down"
