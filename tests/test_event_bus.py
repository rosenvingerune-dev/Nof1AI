"""
Test EventBus Implementation
Tests event propagation, subscriber management, and performance
"""

import asyncio
import pytest
from src.gui.services.event_bus import EventBus, EventTypes, get_event_bus


class TestEventBus:
    """Test suite for EventBus"""

    def setup_method(self):
        """Setup fresh EventBus for each test"""
        self.event_bus = EventBus()
        self.received_events = []

    def test_singleton_pattern(self):
        """Test that get_event_bus returns same instance"""
        bus1 = get_event_bus()
        bus2 = get_event_bus()
        assert bus1 is bus2, "EventBus should be singleton"

    def test_subscribe_and_publish_sync(self):
        """Test synchronous subscription and publishing"""
        received_data = []

        def callback(data):
            received_data.append(data)

        self.event_bus.subscribe('test_event', callback)
        self.event_bus.publish_sync('test_event', {'test': 'data'})

        # Allow event loop to process
        asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.1))

        assert len(received_data) == 1
        assert received_data[0] == {'test': 'data'}

    @pytest.mark.asyncio
    async def test_subscribe_and_publish_async(self):
        """Test async subscription and publishing"""
        received_data = []

        async def async_callback(data):
            received_data.append(data)

        self.event_bus.subscribe('test_event', async_callback)
        await self.event_bus.publish('test_event', {'async': 'test'})

        assert len(received_data) == 1
        assert received_data[0] == {'async': 'test'}

    def test_multiple_subscribers(self):
        """Test that all subscribers receive events"""
        results = []

        def callback1(data):
            results.append(('callback1', data))

        def callback2(data):
            results.append(('callback2', data))

        self.event_bus.subscribe('multi_test', callback1)
        self.event_bus.subscribe('multi_test', callback2)

        self.event_bus.publish_sync('multi_test', 'shared_data')
        asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.1))

        assert len(results) == 2
        assert ('callback1', 'shared_data') in results
        assert ('callback2', 'shared_data') in results

    def test_unsubscribe(self):
        """Test unsubscribing from events"""
        received = []

        def callback(data):
            received.append(data)

        self.event_bus.subscribe('unsub_test', callback)
        self.event_bus.publish_sync('unsub_test', 'first')

        asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.1))
        assert len(received) == 1

        # Unsubscribe
        self.event_bus.unsubscribe('unsub_test', callback)
        self.event_bus.publish_sync('unsub_test', 'second')

        asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.1))
        assert len(received) == 1  # Should not receive second event

    def test_event_history(self):
        """Test event history tracking"""
        self.event_bus.publish_sync('history_test1', 'data1')
        self.event_bus.publish_sync('history_test2', 'data2')
        self.event_bus.publish_sync('history_test1', 'data3')

        asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.1))

        # Get all history
        history = self.event_bus.get_event_history(limit=10)
        assert len(history) >= 3

        # Get filtered history
        filtered = self.event_bus.get_event_history('history_test1', limit=10)
        assert all(e.type == 'history_test1' for e in filtered)

    def test_statistics(self):
        """Test event bus statistics"""
        def callback(data):
            pass

        self.event_bus.subscribe('stats_test', callback)
        self.event_bus.subscribe('stats_test', callback)  # Duplicate - should not add twice
        self.event_bus.publish_sync('stats_test', 'data')

        asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.1))

        stats = self.event_bus.get_statistics()

        assert stats['total_events'] >= 1
        assert stats['total_subscribers'] >= 1
        assert 'stats_test' in stats['events_by_type']
        assert 'stats_test' in stats['subscriber_count_by_type']

    def test_error_handling(self):
        """Test that errors in callbacks don't crash EventBus"""
        received = []

        def good_callback(data):
            received.append('good')

        def bad_callback(data):
            raise ValueError("Intentional error")

        def another_good_callback(data):
            received.append('another_good')

        self.event_bus.subscribe('error_test', good_callback)
        self.event_bus.subscribe('error_test', bad_callback)
        self.event_bus.subscribe('error_test', another_good_callback)

        # Should not crash despite bad_callback error
        self.event_bus.publish_sync('error_test', 'data')
        asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.1))

        # Good callbacks should still run
        assert 'good' in received
        assert 'another_good' in received

    @pytest.mark.asyncio
    async def test_async_callback_with_delay(self):
        """Test async callbacks with delays"""
        results = []

        async def slow_callback(data):
            await asyncio.sleep(0.05)
            results.append(f"slow_{data}")

        async def fast_callback(data):
            results.append(f"fast_{data}")

        self.event_bus.subscribe('delay_test', slow_callback)
        self.event_bus.subscribe('delay_test', fast_callback)

        await self.event_bus.publish('delay_test', 'test')

        # Both should complete
        assert len(results) == 2
        assert 'slow_test' in results
        assert 'fast_test' in results

    def test_clear_history(self):
        """Test clearing event history"""
        for i in range(10):
            self.event_bus.publish_sync(f'clear_test_{i}', f'data_{i}')

        asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.1))

        history_before = self.event_bus.get_event_history(limit=100)
        assert len(history_before) >= 10

        self.event_bus.clear_history()

        history_after = self.event_bus.get_event_history(limit=100)
        assert len(history_after) == 0

    def test_event_types_constants(self):
        """Test that EventTypes constants exist"""
        assert hasattr(EventTypes, 'STATE_UPDATE')
        assert hasattr(EventTypes, 'TRADE_EXECUTED')
        assert hasattr(EventTypes, 'POSITION_OPENED')
        assert hasattr(EventTypes, 'BOT_STARTED')
        assert EventTypes.STATE_UPDATE == "state_update"

    @pytest.mark.asyncio
    async def test_high_volume_events(self):
        """Test EventBus with high volume of events"""
        counter = {'count': 0}

        def counting_callback(data):
            counter['count'] += 1

        self.event_bus.subscribe('volume_test', counting_callback)

        # Publish 100 events rapidly
        for i in range(100):
            await self.event_bus.publish('volume_test', i)

        # All events should be processed
        assert counter['count'] == 100


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
