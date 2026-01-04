from functools import lru_cache
from src.gui.services.bot_service import BotService
from src.gui.services.state_manager import StateManager

@lru_cache()
def get_state_manager() -> StateManager:
    return StateManager()

@lru_cache()
def get_bot_service() -> BotService:
    bot_service = BotService()
    state_manager = get_state_manager()
    bot_service.state_manager = state_manager
    return bot_service
