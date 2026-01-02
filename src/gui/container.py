
"""
Dependency Injection Container
Manages the lifecycle and dependencies of core services.
"""
from typing import Optional
from src.gui.services.bot_service import BotService
from src.gui.services.state_manager import StateManager
from src.gui.services.event_bus import get_event_bus, EventBus
from src.gui.services.cache_manager import get_cache_manager, CacheManager
from src.gui.state.ui_state import UIStateManager

class Container:
    _instance = None

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
            
        # Core Infrastructure
        self.event_bus: EventBus = get_event_bus()
        self.cache_manager: CacheManager = get_cache_manager()
        
        # Domain Services
        self.state_manager: StateManager = StateManager()
        self.bot_service: BotService = BotService()
        self.ui_state: UIStateManager = UIStateManager()
        
        # Wiring
        self.bot_service.state_manager = self.state_manager
        
        self._initialized = True

    @classmethod
    def get_instance(cls) -> 'Container':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

def get_container() -> Container:
    """Get the singleton DI container"""
    return Container.get_instance()
