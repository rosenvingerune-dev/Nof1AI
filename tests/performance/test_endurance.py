
"""
Endurance Test Suite
Simulates long-running operation to detect memory leaks and state inconsistency.
"""
import pytest
import asyncio
import time
import psutil
import os
import random
from src.gui.services.event_bus import get_event_bus, EventTypes
from src.gui.services.state_manager import StateManager
from src.backend.bot_engine import BotState

class TestEndurance:

    @pytest.mark.asyncio
    async def test_stability_simulation(self):
        """
        Simulates 1 week of trading activity in compressed time.
        ~100 positions per week = ~15 trades per day.
        We will simulate 1000 events to be safe.
        """
        event_bus = get_event_bus()
        state_manager = StateManager()
        
        # Verify initial state
        assert state_manager.get_state().balance == 0.0

        # Create a dummy UI subscriber to simulate load
        received_events = 0
        
        async def ui_updater(state):
            nonlocal received_events
            received_events += 1
            # Simulate some minimal processing work
            _ = state.balance * 2 
            
        event_bus.subscribe(EventTypes.STATE_UPDATE, ui_updater)
        
        initial_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        print(f"\nInitial Memory: {initial_memory:.2f} MB")
        
        start_time = time.time()
        events_count = 1000
        
        for i in range(events_count):
            # 1. Generate new state
            market_data = {
                'BTC': {'price': 50000 + random.uniform(-100, 100)},
                'ETH': {'price': 3000 + random.uniform(-50, 50)}
            }
            
            # Create a full BotState object for update
            state = BotState()
            state.market_data = market_data
            state.balance = 10000 + (i * 0.1)
            state.positions = [] # Keep empty or fill if needed
            
            # 2. Update StateManager (this publishes to EventBus)
            state_manager.update(state)
            
            # 3. Simulate Trade Event (every 10 updates)
            if i % 10 == 0:
                trade = {
                    'asset': 'BTC',
                    'action': 'BUY',
                    'amount': 0.1,
                    'price': 50000
                }
                # Trades are published directly to bus by BotService usually
                await event_bus.publish(EventTypes.TRADE_EXECUTED, trade)
                
            # Allow async context switch to process events
            if i % 50 == 0:
                await asyncio.sleep(0.001)
                
        # Wait for all events to propagate
        await asyncio.sleep(0.1)
                
        end_time = time.time()
        duration = end_time - start_time
        
        final_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        print(f"Final Memory: {final_memory:.2f} MB")
        print(f"Duration: {duration:.2f}s for {events_count} updates")
        
        # Metrics
        events_per_sec = events_count / duration
        print(f"Throughput: {events_per_sec:.0f} updates/sec")
        
        # ASSERTIONS
        
        # 0. Verify events were processed
        assert received_events >= events_count, f"UI subscriber missed events. Got {received_events}/{events_count}"

        # 1. Memory stability (allow some growth due to Python internal caching/GC, but not linear)
        mem_growth = final_memory - initial_memory
        print(f"Memory Growth: {mem_growth:.2f} MB")
        assert mem_growth < 20.0, f"Memory usage grew too much ({mem_growth:.2f} MB)"
        
        # 2. State integrity
        current_state = state_manager.get_state()
        assert current_state.balance > 10000, "State failed to update balance"
        
        # 3. Performance
        assert events_per_sec > 100, "System too slow processing events"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
