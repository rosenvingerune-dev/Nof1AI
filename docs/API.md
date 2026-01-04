# NOF1 Trading Bot API Documentation

## Overview
This API provides a backend for the NOF1 Trading Bot, separating the trading logic from the user interface. It is built with **FastAPI** and supports both REST and WebSocket interfaces.

## Base URL
`http://localhost:8000/api/v1`

## Authentication
Currently, the API runs locally and does not enforce authentication. Future versions may implement JWT tokens.

## Endpoints

### 🤖 Bot Control (`/bot`)
- **GET /bot/status**
  - Returns current bot state (running status, balance, PnL).
- **POST /bot/start**
  - Starts the trading bot engine.
  - Body: `{ "assets": ["BTC", "ETH"], "interval": "5m" }`
- **POST /bot/stop**
  - Stops the trading bot engine.

### 📊 Positions (`/positions`)
- **GET /positions**
  - Returns list of active positions.
- **POST /positions/{asset}/close**
  - Manually closes a position for a specific asset.

### 📜 Trades (`/trades`)
- **GET /trades**
  - Returns trade history with pagination.
  - Query params: `limit`, `offset`, `asset`, `action`.

### 📈 Market Data (`/market`)
- **GET /market/data**
  - Returns current market data (prices, funding rates).
- **POST /market/refresh**
  - Forces a refresh of market data from the exchange.

### ⚙️ Settings (`/settings`)
- **GET /settings**
  - Returns current configuration.
- **PUT /settings**
  - Updates configuration.
  - Body: `{ "assets": [...], "interval": "..." }`

## WebSocket API
**URL:** `ws://localhost:8000/ws`

The WebSocket API provides real-time updates for the frontend.

### Event Types
- `state_update`: Full bot state update (balance, totals).
- `trade_executed`: A trade has been executed.
- `market_data_update`: New market prices/data available.
- `bot_started` / `bot_stopped`: Bot lifecycle events.
- `error_occurred`: System errors.

### Message Format
```json
{
  "type": "state_update",
  "data": {
    "is_running": true,
    "balance": 10000.0,
    ...
  },
  "timestamp": "2026-01-04T12:00:00Z"
}
```
