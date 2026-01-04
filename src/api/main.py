from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import bot, positions, trades, market, settings, websocket, proposals

app = FastAPI(
    title="NOF1 Trading Bot API",
    description="Backend API for NOF1 Trading Bot",
    version="0.3.0"
)

# CORS Middleware
origins = [
    "http://localhost:5173",  # React Dev Server
    "http://localhost:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(bot.router, prefix="/api/v1/bot", tags=["Bot"])
app.include_router(positions.router, prefix="/api/v1/positions", tags=["Positions"])
app.include_router(trades.router, prefix="/api/v1/trades", tags=["Trades"])
app.include_router(market.router, prefix="/api/v1/market", tags=["Market"])
app.include_router(settings.router, prefix="/api/v1/settings", tags=["Settings"])
app.include_router(proposals.router, prefix="/api/v1/proposals", tags=["Proposals"])
app.include_router(websocket.router, tags=["WebSocket"])

@app.get("/")
def read_root():
    return {"status": "ok", "message": "NOF1 Trading Bot API is running"}
