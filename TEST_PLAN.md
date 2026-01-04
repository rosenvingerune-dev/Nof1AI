# Test Plan: Backend API & WebSocket (v0.3.0)

**Date:** 2026-01-04
**Scope:** Verify functionality of the new FastAPI backend, REST endpoints, and WebSocket real-time updates.

---

## 1. Automated API Tests (pytest)
We will create a test suite in `tests/api/` to verify all endpoints.

### 1.1 Bot Control Routes (`/api/v1/bot`)
- [ ] **GET /status**: Verify it returns default state (not running).
- [ ] **POST /start**: Verify it starts the bot engine (mocked) and returns success.
- [ ] **POST /start**: Verify error handling if invalid config.
- [ ] **POST /stop**: Verify it stops the bot and returns success.

### 1.2 Data Routes (`/positions`, `/trades`, `/market`)
- [ ] **GET /positions**: Verify returns list (mocked data).
- [ ] **GET /trades**: Verify pagination handling (limit/offset).
- [ ] **GET /market/data**: Verify returns market data structure.
- [ ] **POST /market/refresh**: Verify it triggers update.

### 1.3 Settings (`/api/v1/settings`)
- [ ] **GET /settings**: Verify returns current config (API keys masked/present).
- [ ] **PUT /settings**: Verify updates are applied to BotService.

---

## 2. WebSocket Integration Tests
We will use `pytest-asyncio` and `httpx`/`websockets` to test real-time features.

### 2.1 Connection
- [ ] Verify successful connection to `/ws`.
- [ ] Verify handling of disconnects.

### 2.2 Event Broadcasting
- [ ] **State Update**: Trigger a state update in `StateManager` and verify WS client receives `state_update` message.
- [ ] **Trade Execution**: Trigger `_on_trade_executed` in `BotService` and verify WS client receives `trade_executed` message.
- [ ] **Market Data**: Trigger market refresh and verify `market_data_update` message.

---

## 3. Manual Verification Steps
1. **Start Server**: `python -m uvicorn src.api.main:app --reload`
2. **Swagger UI**: Go to `http://localhost:8000/docs`.
   - Try `GET /bot/status` -> 200 OK.
   - Try `POST /bot/start` directly from UI.
3. **WebSocket Client**: Run `python scripts/test_ws.py`.
   - Keep running while performing actions in Swagger UI.
   - Verify events appear in console.

## 4. Execution Order
1. Create test infrastructure (`conftest.py` with FastAPI TestClient).
2. Implement `tests/api/test_routes.py`.
3. Implement `tests/api/test_websocket.py`.
4. Run all tests: `pytest tests/api/`.
