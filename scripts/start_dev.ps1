
# Start Backend in a new standalone window
Write-Host "Starting Backend (FastAPI) in a new window..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn src.api.main:app --reload"

# Start Frontend in the current window
Write-Host "Starting Frontend (Vite)..." -ForegroundColor Green
Write-Host "You can access the Dashboard at http://localhost:5173" -ForegroundColor Yellow
Set-Location frontend
npm run dev
