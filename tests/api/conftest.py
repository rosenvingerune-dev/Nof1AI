import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock
from src.api.main import app
from src.api.dependencies import get_bot_service
from src.gui.services.bot_service import BotService
from src.backend.bot_engine import BotState

# Mock BotService
@pytest.fixture
def mock_bot_service():
    service = MagicMock(spec=BotService)
    
    # Setup default return values
    service.get_state.return_value = BotState(
        is_running=False, 
        balance=10000.0, 
        total_value=10000.0,
        total_return_pct=0.0,
        positions=[]
    )
    service.start = AsyncMock()
    service.stop = AsyncMock()
    service.get_trade_history.return_value = []
    service.close_position = AsyncMock(return_value=True)
    service.refresh_market_data = AsyncMock(return_value=True)
    service.get_current_config = AsyncMock(return_value={
        "assets": ["BTC", "ETH"],
        "interval": "5m"
    })
    service.update_config = AsyncMock(return_value=True)
    
    return service

# Override dependency
@pytest.fixture
def client(mock_bot_service):
    app.dependency_overrides[get_bot_service] = lambda: mock_bot_service
    return TestClient(app)
