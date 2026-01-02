
"""
UI State Management
Handles persistence of user interface state (filters, theme, layout options).
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class UIStateManager:
    """
    Manages persistence of UI-specific state like filters, active tabs, and user preferences.
    Separates purely visual state from business logic state.
    """
    
    def __init__(self, persistence_path: str = "data/user_prefs.json"):
        self.file_path = Path(persistence_path)
        self.state: Dict[str, Any] = {
            'theme': 'dark',
            'sidebar_expanded': True,
            'last_active_page': 'Dashboard',
            'filters': {}, # Store page-specific filters here
            'notifications': {
                'sound': True,
                'desktop': True
            }
        }
        self._load()

    def _load(self):
        """Load state from JSON file"""
        if not self.file_path.exists():
            return
            
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                # Deep update to preserve defaults for missing keys
                self._deep_update(self.state, loaded)
            logger.info(f"UI State loaded from {self.file_path}")
        except Exception as e:
            logger.error(f"Failed to load UI state: {e}")

    def save(self):
        """Save current state to JSON file"""
        try:
            self.file_path.parent.mkdir(exist_ok=True, parents=True)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2)
            logger.debug("UI State saved")
        except Exception as e:
            logger.error(f"Failed to save UI state: {e}")

    def get_filter(self, page_name: str, filter_key: str, default: Any = None) -> Any:
        """Get a specific filter value for a page"""
        page_filters = self.state.get('filters', {}).get(page_name, {})
        return page_filters.get(filter_key, default)

    def set_filter(self, page_name: str, filter_key: str, value: Any):
        """Set and persist a specific filter value for a page"""
        if 'filters' not in self.state:
            self.state['filters'] = {}
        if page_name not in self.state['filters']:
            self.state['filters'][page_name] = {}
            
        self.state['filters'][page_name][filter_key] = value
        self.save()

    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a root level preference"""
        return self.state.get(key, default)

    def set_preference(self, key: str, value: Any):
        """Set and persist a root level preference"""
        self.state[key] = value
        self.save()

    def _deep_update(self, base_dict, update_dict):
        """Recursive update for dictionaries"""
        for k, v in update_dict.items():
            if isinstance(v, dict) and k in base_dict and isinstance(base_dict[k], dict):
                self._deep_update(base_dict[k], v)
            else:
                base_dict[k] = v

# Singleton integration helper - usually handled by DI container
def get_ui_state_manager() -> UIStateManager:
    return UIStateManager()
