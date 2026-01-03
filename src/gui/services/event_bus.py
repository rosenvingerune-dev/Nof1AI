"""
Event Bus - Real-time event-driven state updates
Replaces polling-based architecture with reactive event system
"""

import asyncio
import logging
from collections import defaultdict
from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    """Event container with metadata"""
    type: str
    data: Any
    timestamp: str
    source: str = "unknown"


class EventBus:
    """
    Central event bus for real-time UI updates.

    Replaces timer-based polling with event-driven updates.
    Components subscribe to specific events and get notified instantly.

    Usage:
        # Subscribe to events
        event_bus.subscribe('state_update', on_state_change)

        # Publish events
        await event_bus.publish('state_update', new_state)

        # Unsubscribe
        event_bus.unsubscribe('state_update', on_state_change)
    """

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._event_history: List[Event] = []
        self._max_history = 100
        self.logger = logging.getLogger(__name__)
        self._stats = {
            'total_events': 0,
            'total_subscribers': 0,
            'events_by_type': defaultdict(int)
        }

    def subscribe(self, event_type: str, callback: Callable) -> None:
        """
        Subscribe to an event type.

        Args:
            event_type: Type of event to listen for (e.g., 'state_update', 'trade_executed')
            callback: Async or sync function to call when event occurs
        """
        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)
            self._stats['total_subscribers'] = sum(len(subs) for subs in self._subscribers.values())
            self.logger.debug(f"Subscriber added to '{event_type}' (total: {len(self._subscribers[event_type])})")

    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """
        Unsubscribe from an event type.

        Args:
            event_type: Event type to stop listening to
            callback: The callback function to remove
        """
        if callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)
            self._stats['total_subscribers'] = sum(len(subs) for subs in self._subscribers.values())
            self.logger.debug(f"Subscriber removed from '{event_type}' (remaining: {len(self._subscribers[event_type])})")

    async def publish(self, event_type: str, data: Any, source: str = "unknown") -> None:
        """
        Publish an event to all subscribers.

        Args:
            event_type: Type of event being published
            data: Event payload (can be any serializable object)
            source: Source of the event (for debugging)
        """
        event = Event(
            type=event_type,
            data=data,
            timestamp=datetime.utcnow().isoformat(),
            source=source
        )

        # Update statistics
        self._stats['total_events'] += 1
        self._stats['events_by_type'][event_type] += 1

        # Store in history
        self._event_history.append(event)
        if len(self._event_history) > self._max_history:
            self._event_history.pop(0)

        # Notify subscribers
        subscribers = self._subscribers.get(event_type, [])

        if not subscribers:
            self.logger.debug(f"No subscribers for event '{event_type}'")
            return

        self.logger.debug(f"Publishing '{event_type}' to {len(subscribers)} subscribers (source: {source})")

        # Call all subscribers (handle both async and sync callbacks)
        tasks = []
        for callback in subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    # Async callback - create task
                    tasks.append(callback(data))
                else:
                    # Sync callback - call directly
                    callback(data)
            except Exception as e:
                self.logger.error(f"Error in event callback for '{event_type}': {e}", exc_info=True)

        # Await all async callbacks
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    def publish_sync(self, event_type: str, data: Any, source: str = "unknown") -> None:
        """
        Synchronous version of publish (creates task in event loop).
        Use when calling from sync context.

        Args:
            event_type: Type of event
            data: Event payload
            source: Event source
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Schedule coroutine in running loop
                asyncio.create_task(self.publish(event_type, data, source))
            else:
                # Run in new loop
                loop.run_until_complete(self.publish(event_type, data, source))
        except RuntimeError:
            # No event loop - log error
            self.logger.error(f"Cannot publish event '{event_type}' - no event loop available")

    def get_event_history(self, event_type: Optional[str] = None, limit: int = 50) -> List[Event]:
        """
        Get recent event history for debugging.

        Args:
            event_type: Filter by event type (optional)
            limit: Maximum number of events to return

        Returns:
            List of recent events
        """
        if event_type:
            filtered = [e for e in self._event_history if e.type == event_type]
            return filtered[-limit:]
        return self._event_history[-limit:]

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get event bus statistics for monitoring.

        Returns:
            Dict with stats (total events, subscribers, events by type)
        """
        return {
            'total_events': self._stats['total_events'],
            'total_subscribers': self._stats['total_subscribers'],
            'events_by_type': dict(self._stats['events_by_type']),
            'subscriber_count_by_type': {
                event_type: len(callbacks)
                for event_type, callbacks in self._subscribers.items()
            },
            'history_size': len(self._event_history)
        }

    def clear_history(self) -> None:
        """Clear event history (for memory management)"""
        self._event_history.clear()
        self.logger.debug("Event history cleared")


# Global event bus instance
_global_event_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """
    Get the global event bus instance (singleton).

    Returns:
        Global EventBus instance
    """
    global _global_event_bus
    if _global_event_bus is None:
        _global_event_bus = EventBus()
    return _global_event_bus


# Event type constants (for type safety and autocomplete)
class EventTypes:
    """Standard event types used in the application"""
    STATE_UPDATE = "state_update"           # Bot state changed
    TRADE_EXECUTED = "trade_executed"       # Trade executed
    POSITION_OPENED = "position_opened"     # New position opened
    POSITION_CLOSED = "position_closed"     # Position closed
    ORDER_PLACED = "order_placed"           # Order placed
    ORDER_FILLED = "order_filled"           # Order filled
    ORDER_CANCELLED = "order_cancelled"     # Order cancelled
    ERROR_OCCURRED = "error_occurred"       # Error occurred
    BOT_STARTED = "bot_started"             # Bot started
    BOT_STOPPED = "bot_stopped"             # Bot stopped
    MARKET_DATA_UPDATE = "market_data_update"  # Market data refreshed
    PROPOSAL_CREATED = "proposal_created"   # Trade proposal created
    PROPOSAL_APPROVED = "proposal_approved" # Proposal approved
    PROPOSAL_REJECTED = "proposal_rejected" # Proposal rejected
