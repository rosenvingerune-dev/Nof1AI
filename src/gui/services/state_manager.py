"""
State Manager - Global reactive state management for UI
Now integrated with EventBus for real-time updates
"""

import asyncio
import logging
from typing import Optional
from src.backend.bot_engine import BotState
from src.gui.services.event_bus import get_event_bus, EventTypes


class StateManager:
    """
    Manages global application state for UI components.

    Now integrated with EventBus for reactive updates:
    - State changes automatically broadcast via EventBus
    - UI components subscribe to events instead of polling
    - Backwards compatible with legacy observer pattern
    """

    def __init__(self):
        self._state: BotState = BotState()
        self._observers = []  # Legacy observer pattern (deprecated)
        self.event_bus = get_event_bus()
        self.logger = logging.getLogger(__name__)

    def update(self, new_state: BotState):
        """
        Update state with new data from bot engine.
        Called by bot_service when bot state changes.

        Now broadcasts via EventBus for instant UI updates.
        """
        old_state = self._state
        self._state = new_state

        # Legacy observer pattern (kept for backwards compatibility)
        for observer in self._observers:
            try:
                observer(new_state)
            except Exception as e:
                self.logger.error(f"Error in legacy observer: {e}")

        # New: Broadcast via EventBus for reactive updates
        try:
            self.event_bus.publish_sync(
                EventTypes.STATE_UPDATE,
                new_state,
                source="StateManager"
            )
        except Exception as e:
            self.logger.error(f"Error publishing state update event: {e}")

        # Emit specific events for granular updates
        self._emit_specific_events(old_state, new_state)

    def _emit_specific_events(self, old_state: BotState, new_state: BotState):
        """
        Emit specific events for granular UI updates.
        Allows components to subscribe only to relevant changes.
        """
        try:
            # Bot status changed
            if old_state.is_running != new_state.is_running:
                event_type = EventTypes.BOT_STARTED if new_state.is_running else EventTypes.BOT_STOPPED
                self.event_bus.publish_sync(event_type, new_state, source="StateManager")

            # Positions changed
            if old_state.positions != new_state.positions:
                old_count = len(old_state.positions or [])
                new_count = len(new_state.positions or [])

                if new_count > old_count:
                    self.event_bus.publish_sync(EventTypes.POSITION_OPENED, new_state.positions, source="StateManager")
                elif new_count < old_count:
                    self.event_bus.publish_sync(EventTypes.POSITION_CLOSED, new_state.positions, source="StateManager")

            # Market data changed
            if hasattr(new_state, 'market_data') and old_state.market_data != new_state.market_data:
                self.event_bus.publish_sync(EventTypes.MARKET_DATA_UPDATE, new_state.market_data, source="StateManager")

            # Error occurred
            if new_state.error and new_state.error != old_state.error:
                self.event_bus.publish_sync(EventTypes.ERROR_OCCURRED, new_state.error, source="StateManager")

        except Exception as e:
            self.logger.error(f"Error emitting specific events: {e}")

    def get_state(self) -> BotState:
        """Get current application state"""
        return self._state

    def subscribe(self, callback):
        """
        Subscribe to state changes (legacy observer pattern).

        DEPRECATED: Use event_bus.subscribe(EventTypes.STATE_UPDATE, callback) instead.
        """
        if callback not in self._observers:
            self._observers.append(callback)
            self.logger.warning("Using legacy subscribe() - consider migrating to EventBus")

    def unsubscribe(self, callback):
        """Unsubscribe from state changes (legacy)"""
        if callback in self._observers:
            self._observers.remove(callback)

    def subscribe_to_event(self, event_type: str, callback):
        """
        Subscribe to specific event type via EventBus.

        Args:
            event_type: Event type constant from EventTypes
            callback: Async or sync callback function

        Example:
            state_manager.subscribe_to_event(EventTypes.STATE_UPDATE, on_state_change)
        """
        self.event_bus.subscribe(event_type, callback)

    def unsubscribe_from_event(self, event_type: str, callback):
        """Unsubscribe from event type"""
        self.event_bus.unsubscribe(event_type, callback)
