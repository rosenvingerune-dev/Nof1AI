# 🧪 TESTING CHECKLIST - EventBus & Reactive Pages

## 📋 Pre-Test Setup

### 1. Activate Reactive Components

**Edit:** `src/gui/app.py` (line 12)

**Before:**
```python
from src.gui.pages import dashboard, positions, history, market, reasoning, settings, recommendations, logs
```

**After:**
```python
from src.gui.pages import (
    dashboard_reactive as dashboard,
    positions_reactive as positions,
    history_optimized as history,
    market, reasoning, settings, recommendations, logs
)
```

### 2. Enable Debug Logging (Optional)

**Add to** `main.py` (after imports):
```python
import logging
logging.getLogger('src.gui.services.event_bus').setLevel(logging.DEBUG)
```

### 3. Start Application

```bash
python main.py
```

Expected output:
```
[INFO] NiceGUI app shutdown event triggered
NiceGUI ready at http://localhost:8081
```

Open browser: http://localhost:8081

---

## ✅ TEST 1: EventBus Unit Tests

**Run:**
```bash
pytest tests/test_event_bus.py -v
```

**Expected Results:**
- ✅ All 12 tests pass
- ✅ No errors or warnings
- ✅ Test coverage > 90%

**If tests fail:**
- Check import paths
- Verify Python version (3.8+)
- Install missing dependencies: `pip install pytest pytest-asyncio`

---

## ✅ TEST 2: CPU Usage (Baseline - Bot Stopped)

**Objective:** Verify CPU reduction when bot is idle

**Steps:**
1. Open Task Manager (Windows: Ctrl+Shift+Esc)
2. Find `python.exe` process
3. Note CPU usage
4. Navigate between pages (Dashboard → Positions → History)
5. Monitor CPU for 30 seconds

**Expected Results:**

| Metric | Old (Polling) | New (Reactive) | Status |
|--------|---------------|----------------|--------|
| CPU (idle, bot stopped) | 80% | **<20%** | ⬜ |
| CPU (navigating pages) | Spikes to 100% | **<30%** | ⬜ |
| Memory usage | 500MB | **<300MB** | ⬜ |

**Actual Results:**
- CPU Usage: _____%
- Memory: _____MB
- Pass/Fail: ⬜

---

## ✅ TEST 3: Dashboard - Event-Driven Updates

**Objective:** Verify instant updates without polling

**Steps:**
1. Open Dashboard page
2. Open browser DevTools (F12)
3. Go to Network tab → Filter "WS" (WebSocket)
4. Click "Start Bot"
5. Watch for state updates

**Expected Results:**
- ✅ Bot status changes to "🟢 Running" **within 2 seconds**
- ✅ Metrics update (Balance, Return, etc.) **within 5 seconds**
- ✅ WebSocket messages: **<10 per minute** (not 100+ like before)
- ✅ No `ui.timer` messages in console

**Browser Console Output (if debug enabled):**
```
[DEBUG] Publishing 'state_update' to 3 subscribers
[DEBUG] Publishing 'bot_started' to 1 subscriber
```

**Actual Results:**
- Bot status update time: _____s
- WebSocket msg/min: _____
- Pass/Fail: ⬜

---

## ✅ TEST 4: Positions - Real-Time Updates

**Objective:** Verify instant position updates

**Prerequisites:**
- Bot must be running
- At least 1 open position

**Steps:**
1. Navigate to Positions page
2. Note current PnL values
3. Wait 5 seconds
4. Check if values updated

**Expected Results:**
- ✅ Table updates **instantly** when position changes
- ✅ PnL values color-coded (green/red)
- ✅ No page reload or lag
- ✅ CPU usage stays **<20%**

**Test Close Position:**
1. Click "Close Position" button
2. Confirm dialog
3. Verify position removed **within 10 seconds**

**Actual Results:**
- Update latency: _____ms
- Close position time: _____s
- Pass/Fail: ⬜

---

## ✅ TEST 5: History - Lazy Loading

**Objective:** Verify 95% faster initial load

**Prerequisites:**
- Create test data (10,000+ trades) using script below

**Steps:**
1. Navigate to History page
2. Start timer
3. Wait for first 50 trades to load
4. Note load time
5. Click "Load More" button
6. Verify next 50 trades load

**Expected Results:**

| Dataset Size | Old Load Time | New Load Time | Improvement |
|--------------|---------------|---------------|-------------|
| 100 trades | 0.5s | 0.2s | 60% faster |
| 1,000 trades | 2s | 0.3s | 85% faster |
| 10,000 trades | 8s | **0.4s** | **95% faster** |

**Test "Load More":**
- ✅ Button appears after first load
- ✅ Clicking loads next 50 trades
- ✅ Statistics update correctly
- ✅ No duplicate trades

**Actual Results:**
- Initial load time (50 trades): _____s
- Total trades available: _____
- Load More works: ⬜
- Pass/Fail: ⬜

---

## ✅ TEST 6: EventBus Statistics

**Objective:** Verify event propagation is working

**Steps:**
1. Open Python console:
```python
from src.gui.services.event_bus import get_event_bus

event_bus = get_event_bus()
stats = event_bus.get_statistics()

print(f"Total events: {stats['total_events']}")
print(f"Total subscribers: {stats['total_subscribers']}")
print(f"Events by type: {stats['events_by_type']}")
```

**Expected Results:**
```
Total events: 50+
Total subscribers: 10+
Events by type: {
    'state_update': 20+,
    'bot_started': 1,
    'position_opened': 0-5,
    ...
}
```

**Check Event History:**
```python
history = event_bus.get_event_history(limit=10)
for event in history:
    print(f"[{event.timestamp}] {event.type} from {event.source}")
```

**Actual Results:**
- Total events: _____
- Total subscribers: _____
- Pass/Fail: ⬜

---

## ✅ TEST 7: Page Navigation Performance

**Objective:** Verify no lag when switching pages

**Steps:**
1. Navigate: Dashboard → Positions → History → Settings
2. Repeat 5 times rapidly
3. Note any lag or freezing

**Expected Results:**
- ✅ Page switch: **<200ms** (feels instant)
- ✅ No white screen flash
- ✅ CPU stays **<30%** during navigation
- ✅ Memory stable (no leaks)

**Old Behavior:**
- Page switch: 2-5s (painful)
- White screen flash
- CPU spikes to 100%

**Actual Results:**
- Average switch time: _____ms
- Any lag: Yes/No
- Pass/Fail: ⬜

---

## ✅ TEST 8: Memory Leak Check

**Objective:** Verify no memory leaks over time

**Steps:**
1. Note initial memory usage
2. Run bot for 30 minutes
3. Navigate between pages randomly
4. Create/close positions (if available)
5. Note final memory usage

**Expected Results:**
- ✅ Memory increase: **<50MB** over 30 minutes
- ✅ No gradual increase over time
- ✅ Garbage collection working

**Old Behavior:**
- Memory increases 200MB+ per hour

**Actual Results:**
- Initial memory: _____MB
- After 30 min: _____MB
- Increase: _____MB
- Pass/Fail: ⬜

---

## ✅ TEST 9: Error Handling

**Objective:** Verify graceful error handling

**Test 1: Network Error**
1. Disconnect internet
2. Try to start bot
3. Verify error message displays
4. Reconnect internet

**Expected:**
- ✅ Error notification appears
- ✅ App doesn't crash
- ✅ Can retry after reconnecting

**Test 2: Invalid Data**
1. Corrupt `data/diary.jsonl` (add invalid JSON line)
2. Navigate to History page
3. Verify page loads (skips bad entries)

**Expected:**
- ✅ Page loads successfully
- ✅ Error logged (not shown to user)
- ✅ Valid entries still display

**Actual Results:**
- Error handling works: ⬜
- Pass/Fail: ⬜

---

## ✅ TEST 10: Backwards Compatibility

**Objective:** Verify old pages still work

**Steps:**
1. Edit `app.py` to use old pages:
```python
from src.gui.pages import dashboard, positions, history  # Original
```
2. Restart app
3. Verify pages work (but with polling)

**Expected:**
- ✅ Old pages work unchanged
- ✅ Can switch between old/new easily
- ✅ No breaking changes

**Actual Results:**
- Old pages work: ⬜
- Pass/Fail: ⬜

---

## 🔧 CREATE TEST DATA (For History Testing)

**Script:** `scripts/generate_test_trades.py`

```python
import json
from pathlib import Path
from datetime import datetime, timedelta
import random

def generate_test_trades(count=10000):
    """Generate test trades for performance testing"""
    diary_path = Path("data/diary.jsonl")
    diary_path.parent.mkdir(exist_ok=True)

    assets = ['BTC', 'ETH', 'SOL', 'AVAX', 'MATIC']
    actions = ['buy', 'sell', 'hold']

    base_time = datetime.now()

    with open(diary_path, 'w', encoding='utf-8') as f:
        for i in range(count):
            timestamp = (base_time - timedelta(minutes=i)).isoformat()
            asset = random.choice(assets)
            action = random.choice(actions)

            trade = {
                'timestamp': timestamp,
                'asset': asset,
                'action': action,
                'entry_price': random.uniform(1000, 50000),
                'exit_price': random.uniform(1000, 50000) if action != 'hold' else None,
                'size': random.uniform(0.001, 1.0),
                'pnl': random.uniform(-500, 500) if action != 'hold' else None,
                'pnl_pct': random.uniform(-10, 10) if action != 'hold' else None,
                'rationale': f'Test trade {i} for performance testing'
            }

            f.write(json.dumps(trade) + '\n')

    print(f"✅ Generated {count} test trades in {diary_path}")

if __name__ == '__main__':
    generate_test_trades(10000)
```

**Run:**
```bash
python scripts/generate_test_trades.py
```

---

## 📊 SUMMARY REPORT

### Performance Metrics

| Metric | Target | Actual | Pass/Fail |
|--------|--------|--------|-----------|
| CPU (idle) | <20% | ____% | ⬜ |
| CPU (active) | <40% | ____% | ⬜ |
| Memory | <300MB | ____MB | ⬜ |
| Update latency | <200ms | ____ms | ⬜ |
| Page switch | <200ms | ____ms | ⬜ |
| Initial load (1k trades) | <500ms | ____ms | ⬜ |
| Initial load (10k trades) | <1s | ____ms | ⬜ |

### Feature Tests

| Feature | Works | Notes |
|---------|-------|-------|
| EventBus unit tests | ⬜ | |
| Dashboard reactive | ⬜ | |
| Positions reactive | ⬜ | |
| History lazy loading | ⬜ | |
| Event statistics | ⬜ | |
| Error handling | ⬜ | |
| Backwards compat | ⬜ | |

### Overall Assessment

**CPU Reduction Achieved:** _____%
**Performance Improvement:** ____x faster
**Recommendation:** ⬜ Continue with NiceGUI / ⬜ Migrate to Qt

---

## 🐛 Issues Found

**Issue 1:**
- Description: ___________
- Severity: Critical / High / Medium / Low
- Fix needed: ___________

**Issue 2:**
- Description: ___________
- Severity: ___________
- Fix needed: ___________

---

## ✅ PASS CRITERIA

**To proceed with NiceGUI:**
- ✅ CPU reduction ≥ 70%
- ✅ Update latency < 200ms
- ✅ No critical bugs
- ✅ All reactive pages working

**To migrate to Qt:**
- ❌ CPU reduction < 50%
- ❌ Still laggy/slow
- ❌ Critical bugs in EventBus
- ❌ NiceGUI limitations too severe

---

**Tester:** _____________
**Date:** 2026-01-02
**Time:** _____________
**Result:** PASS / FAIL
