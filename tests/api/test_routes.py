from src.backend.bot_engine import BotState

def test_read_root(client):
    response = client.get("/api/v1/bot/status")
    assert response.status_code == 200
    assert "is_running" in response.json()

def test_start_bot(client, mock_bot_service):
    payload = {"assets": ["BTC", "ETHT"], "interval": "1h"}
    response = client.post("/api/v1/bot/start", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "started"
    mock_bot_service.start.assert_called_once_with(assets=["BTC", "ETHT"], interval="1h")

def test_stop_bot(client, mock_bot_service):
    response = client.post("/api/v1/bot/stop")
    assert response.status_code == 200
    assert response.json()["status"] == "stopped"
    mock_bot_service.stop.assert_called_once()

def test_get_positions(client):
    response = client.get("/api/v1/positions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_close_position(client, mock_bot_service):
    response = client.post("/api/v1/positions/BTC/close")
    assert response.status_code == 200
    assert response.json()["success"] is True
    mock_bot_service.close_position.assert_called_with("BTC")

def test_get_trades(client):
    response = client.get("/api/v1/trades/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_refresh_market_data(client, mock_bot_service):
    response = client.post("/api/v1/market/refresh")
    assert response.status_code == 200
    assert response.json()["success"] is True
    mock_bot_service.refresh_market_data.assert_called_once()

def test_get_settings(client):
    response = client.get("/api/v1/settings/")
    assert response.status_code == 200
    assert "assets" in response.json()

def test_update_settings(client, mock_bot_service):
    payload = {"assets": ["SOL"]}
    response = client.put("/api/v1/settings/", json=payload)
    assert response.status_code == 200
    assert response.json()["success"] is True
    mock_bot_service.update_config.assert_called_with({"assets": ["SOL"]})
