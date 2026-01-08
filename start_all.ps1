<#
.SYNOPSIS
    Starts the Nof1.ai Bot (Backend + Frontend)
.DESCRIPTION
    Launcher script that starts the FastAPI backend and React frontend in separate windows.
#>

$ErrorActionPreference = "Stop"
$ScriptDir = $PSScriptRoot

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   🚀 Nof1.ai Alpha Arena Launcher      " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 1. Check Environment
if (-not (Test-Path "$ScriptDir/.env")) {
    Write-Host "❌ Error: .env file not found!" -ForegroundColor Red
    Write-Host "   Please copy .env.example to .env and configure it."
    exit 1
}

# 2. Check Python Environment
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python not found in PATH." -ForegroundColor Red
    exit 1
}

# 3. Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Node.js not found in PATH." -ForegroundColor Red
    exit 1
}

# 4. Start Backend
Write-Host "`nbackend..." -ForegroundColor Yellow
$BackendArgs = '-NoExit', '-Command', "
    Write-Host 'Starting FastAPI Backend...' -ForegroundColor Cyan;
    cd '$ScriptDir';
    python -m uvicorn src.api.main:app --reload;
"
Start-Process powershell -ArgumentList $BackendArgs

# 5. Start Frontend
Write-Host "frontend..." -ForegroundColor Yellow
if (Test-Path "$ScriptDir/frontend") {
    $FrontendArgs = '-NoExit', '-Command', "
        Write-Host 'Starting React Frontend...' -ForegroundColor Green;
        cd '$ScriptDir/frontend';
        npm run dev;
    "
    Start-Process powershell -ArgumentList $FrontendArgs
} else {
    Write-Host "❌ Frontend directory not found at $ScriptDir/frontend" -ForegroundColor Red
}

Write-Host "`n✨ All systems launching!" -ForegroundColor Green
Write-Host "   Backend API: http://localhost:8000"
Write-Host "   Frontend UI: http://localhost:5173"
Write-Host "`nPress any key to exit this launcher (windows will remain open)..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
