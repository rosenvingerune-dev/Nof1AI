# 📄 Paper Trading Guide - 100% Risk-Free Testing

Complete guide to using the paper trading backend for nof1.ai trading bot.

---

## 🎯 What is Paper Trading?

**Paper trading** (also called simulated trading or demo trading) lets you test trading strategies without risking real money.

### How it works:

✅ **Real-time prices** from Binance API
✅ **Simulated order execution** with realistic slippage
✅ **Local position tracking** with PnL calculation
✅ **No exchange account needed** - runs 100% locally
✅ **No API keys required** (except Gemini for AI)

---

## ✅ Why Use Paper Trading?

### Perfect for:

- **Learning**: Understand how the bot works before risking money
- **Testing strategies**: Validate your AI trading approach
- **Development**: Debug and improve the bot safely
- **Experimentation**: Try different assets, intervals, and configurations
- **Portfolio simulation**: See how strategies perform over time

### When to use paper vs real:

| Use Paper Trading | Use Real Exchange |
|-------------------|-------------------|
| First time using bot | Proven profitable on paper |
| Learning AI trading | Comfortable with risks |
| Testing new strategies | Small real capital to start |
| Debugging code changes | Ready for live trading |
| No exchange account | Have exchange account |

---

## 🚀 Quick Start - 5 Minutes

### Step 1: Set up `.env`

```env
# Trading Backend
TRADING_BACKEND=paper

# Paper Trading Settings
PAPER_TRADING_STARTING_BALANCE=10000.0
PAPER_TRADING_SLIPPAGE=0.0005  # 0.05%
PAPER_TRADING_PRICE_UPDATE_INTERVAL=5

# LLM (required)
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here

# Trading Config
ASSETS=BTC,ETH
INTERVAL=5m
TRADING_MODE=manual
```

**That's it!** No Hyperliquid wallet needed, no testnet tokens, no Discord faucet.

### Step 2: Run tests

```bash
python tests/test_05_paper_trading.py
```

**Expected:**
```
✅ Paper Trading API initialized
✅ Starting balance: $10,000.00
✅ BTC price fetched: $42,350.00
✅ Market order simulated successfully
```

### Step 3: Start bot

```bash
python main.py
```

Bot will:
1. Initialize with $10,000 simulated balance
2. Fetch real-time prices from Binance
3. Generate trade signals via Gemini
4. Execute trades in simulation (if manual mode: wait for your approval)
5. Track PnL locally

---

## 📋 Configuration Options

### Required Settings

```env
# Must be set to "paper"
TRADING_BACKEND=paper

# Gemini API key (for AI decisions)
GEMINI_API_KEY=your_key_here
```

### Optional Settings

```env
# Starting capital (default: 10000.0)
PAPER_TRADING_STARTING_BALANCE=25000.0

# Simulated slippage percentage (default: 0.0005 = 0.05%)
PAPER_TRADING_SLIPPAGE=0.001  # 0.1% slippage

# Price update frequency in seconds (default: 5)
PAPER_TRADING_PRICE_UPDATE_INTERVAL=10

# Trading mode (manual or auto)
TRADING_MODE=manual  # Recommended for paper trading
```

---

## 🔧 How Paper Trading Works

### Architecture

```
┌─────────────────┐
│   Bot Engine    │
└────────┬────────┘
         │
         ├─── Gemini AI (real)
         │
         ├─── TAAPI Indicators (real, optional)
         │
         └─── Paper Trading API (simulated)
              │
              ├─── Binance Price Feed (real-time)
              ├─── Simulated Orders
              ├─── Local Positions
              └─── PnL Calculation
```

### What's Real vs Simulated

| Component | Real or Simulated |
|-----------|-------------------|
| Gemini AI decisions | ✅ Real |
| Market prices | ✅ Real (from Binance) |
| Technical indicators | ✅ Real (TAAPI or simulated) |
| Order execution | ❌ Simulated |
| Balance/positions | ❌ Simulated (local tracking) |
| Exchange fees | ✅ Real simulation (0.05% default) |

---

## 💡 Features

### ✅ Realistic Simulation

**Order Execution:**
- Market orders execute at current price ± slippage
- TP/SL orders trigger when price crosses threshold
- Orders tracked locally in memory

**Position Tracking:**
- Long/short positions
- Entry price, current price
- Unrealized PnL calculation
- Leverage support (1x-10x)

**Account Management:**
- Balance tracking
- Total account value (balance + positions)
- Available margin calculation
- Position size validation

### ✅ Real-Time Prices

**Binance API:**
- Free, no API key needed
- Real-time ticker prices
- 5-second caching to avoid rate limits
- Supports all major crypto assets

**Supported Assets:**
```
BTC, ETH, SOL, AVAX, MATIC, LINK, UNI, AAVE, etc.
```

### ✅ Full Bot Compatibility

Paper trading API implements the **same interface** as Hyperliquid API:

```python
# These methods work identically in both paper and real trading
await api.get_user_state()
await api.get_current_price(asset)
await api.place_buy_order(asset, amount)
await api.place_sell_order(asset, amount)
await api.place_take_profit(asset, is_long, amount, price)
await api.place_stop_loss(asset, is_long, amount, price)
await api.cancel_order(asset, order_id)
await api.get_open_orders()
```

**No code changes needed!** Just switch `TRADING_BACKEND` in `.env`.

---

## 📊 Using the GUI

### Dashboard Page

Shows your simulated account:
- **Balance**: Available USDC
- **Total Value**: Balance + position value
- **Total Return**: Performance since start
- **Positions**: Active trades with PnL

### Positions Page

Track simulated trades:
- Entry price vs current price
- Unrealized PnL (profit/loss)
- TP/SL levels
- Close positions manually

### Recommendations Page (Manual Mode)

Review AI proposals before execution:
- Asset, action (buy/sell)
- Entry price, size
- TP/SL prices
- Rationale from Gemini
- **Approve** to execute in simulation
- **Reject** to skip

### Reasoning Page

See Gemini's full market analysis:
- Market structure assessment
- Indicator analysis
- Trade rationale
- Risk considerations

---

## 🧪 Testing Strategy

### Week 1: Observation

**Goal:** Understand the bot without executing trades

```env
TRADING_MODE=manual
INTERVAL=5m
ASSETS=BTC,ETH
```

**Actions:**
- Let bot run continuously
- Review all Gemini reasoning
- Observe proposed trades
- **Reject all proposals** (just learning)
- Document patterns in AI decisions

**Success Criteria:**
- Understand bot workflow
- Can predict when AI will suggest trades
- Comfortable with GUI

### Week 2: Selective Trading

**Goal:** Execute only high-confidence trades

```env
TRADING_MODE=manual
INTERVAL=15m
ASSETS=BTC,ETH,SOL
```

**Actions:**
- Approve only trades you agree with
- Start with small sizes ($100-500)
- Track win rate and PnL
- Refine your approval criteria

**Success Criteria:**
- 5-10 trades executed
- Win rate >50%
- Understanding of when AI is accurate

### Week 3: Automated Testing

**Goal:** Test auto mode in simulation

```env
TRADING_MODE=auto
INTERVAL=1h
ASSETS=BTC,ETH,SOL
```

**Actions:**
- Let bot trade automatically
- Monitor daily
- Track statistics
- Adjust configuration based on results

**Success Criteria:**
- Profitable over 20+ trades
- Consistent with strategy expectations
- Ready to consider real trading (testnet first!)

---

## 📈 Performance Tracking

### Data Saved Locally

**`data/diary.jsonl`** - Complete trade log:
```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "asset": "BTC",
  "action": "buy",
  "entry_price": 42350.50,
  "amount": 0.023,
  "allocation_usd": 1000,
  "tp_price": 43500,
  "sl_price": 41800,
  "rationale": "Strong bullish momentum, RSI oversold",
  "filled": true
}
```

**`bot.log`** - Execution log:
```
2025-01-15 10:30:00 [INFO] Trading backend: PAPER
2025-01-15 10:35:00 [INFO] Executed buy BTC: 0.023 @ 42350.50
2025-01-15 10:35:01 [INFO] Placed TP order @ 43500
```

### Analyzing Results

**Calculate Win Rate:**
```python
import json

trades = []
with open('data/diary.jsonl') as f:
    for line in f:
        trades.append(json.loads(line))

# Filter closed trades
closed = [t for t in trades if t.get('action') == 'hold' and 'pnl' in t]

wins = len([t for t in closed if t['pnl'] > 0])
total = len(closed)
win_rate = (wins / total) * 100 if total > 0 else 0

print(f"Win Rate: {win_rate:.1f}% ({wins}/{total})")
```

---

## 🔄 Switching Between Paper and Real

### From Paper to Testnet

1. **Verify paper trading results:**
   - Win rate >55%
   - 50+ trades executed
   - Consistent profitability

2. **Update `.env`:**
   ```env
   TRADING_BACKEND=hyperliquid
   HYPERLIQUID_NETWORK=testnet
   HYPERLIQUID_PRIVATE_KEY=0x...
   ```

3. **Get testnet funds** (see HYPERLIQUID_TESTNET_GUIDE.md)

4. **Start with manual mode** on testnet

### From Testnet to Mainnet

1. **Verify testnet results:**
   - Profitable for 2-4 weeks
   - Comfortable with all bot functions
   - Tested error scenarios

2. **Update `.env`:**
   ```env
   TRADING_BACKEND=hyperliquid
   HYPERLIQUID_NETWORK=mainnet
   HYPERLIQUID_PRIVATE_KEY=0x...  # SEPARATE wallet!
   ```

3. **Start with minimal capital** ($100-500)

4. **Use manual mode first**

---

## ⚠️ Limitations of Paper Trading

### What Paper Trading Can't Simulate

❌ **Emotional pressure** of risking real money
❌ **Slippage variance** in volatile markets
❌ **Exchange outages** or network issues
❌ **Liquidation cascades** in extreme moves
❌ **Order book depth** and large order impact

### Paper vs Real Performance

**Paper trading typically shows better results** because:
1. No emotional decisions (fear, FOMO)
2. Perfect execution (no rejected orders)
3. Idealized slippage (0.05% constant)
4. No exchange downtime

**Rule of thumb:**
- If paper trading is profitable: Real trading *might* be
- If paper trading loses money: Real trading will definitely lose

---

## 🐛 Troubleshooting

### "Binance API error: 429 Too Many Requests"

**Cause:** Fetching prices too frequently

**Solution:**
```env
PAPER_TRADING_PRICE_UPDATE_INTERVAL=10  # Increase from 5 to 10 seconds
```

### "Asset DOGE not found on Binance"

**Cause:** Asset symbol mismatch

**Solution:**
Paper trading uses Binance symbols. Some assets may differ:
```
Hyperliquid → Binance
DOGE       → DOGE
SHIB       → SHIB
PEPE       → PEPE (check if listed)
```

### Balance doesn't decrease after trades

**Cause:** Orders not executing in simulation

**Check:**
```bash
# View log
cat bot.log | grep "Executed"

# Verify diary
cat data/diary.jsonl | tail -5
```

### Positions not showing in GUI

**Cause:** Position tracking issue

**Fix:**
1. Restart bot: `Ctrl+C` then `python main.py`
2. Check `bot.log` for errors
3. Verify paper trading API initialization

---

## 📝 Best Practices

### Configuration

✅ **Start with manual mode:**
```env
TRADING_MODE=manual
```

✅ **Use reasonable starting balance:**
```env
PAPER_TRADING_STARTING_BALANCE=10000  # Not 1,000,000
```

✅ **Realistic slippage:**
```env
PAPER_TRADING_SLIPPAGE=0.001  # 0.1% (conservative)
```

### Testing Approach

✅ **Test for weeks, not days**
✅ **Try different market conditions** (bull, bear, sideways)
✅ **Document all trades** and rationale
✅ **Analyze failures** as much as wins
✅ **Don't curve-fit** to past results

### Transition to Real Trading

✅ **Never skip testnet** after paper trading
✅ **Start small** on mainnet (10-20% of capital)
✅ **Keep manual mode** for first month
✅ **Have stop-loss rules** independent of bot
✅ **Monitor daily** even in auto mode

---

## 🆘 FAQ

### Q: Can I use paper trading without Gemini API?

**A:** No, you still need Gemini for AI decisions. But you DON'T need:
- Hyperliquid account
- Testnet tokens
- TAAPI key (optional)

### Q: Does paper trading use real technical indicators?

**A:** Yes, if you set up TAAPI:
```env
TAAPI_API_KEY=your_key_here
```

If not set, indicators will be simulated (basic calculations).

### Q: Can I backtest historical data?

**A:** Not currently. Paper trading uses real-time prices only.

For backtesting, you'd need to:
1. Download historical price data
2. Modify paper trading API to use historical prices
3. Run bot in accelerated time

### Q: How accurate is paper trading vs real?

**A:** Price data is 100% real (from Binance). Execution differs:

| Aspect | Paper | Real |
|--------|-------|------|
| Prices | Real-time | Real-time |
| Slippage | Fixed 0.05% | Variable |
| Execution | Instant | Delayed |
| Fees | Simulated | Real |
| Emotions | None | High impact |

**Expect 10-20% worse results on real exchange.**

### Q: Can I switch between paper and real without restarting?

**A:** No, you must restart the bot:
1. Stop bot: `Ctrl+C`
2. Edit `.env`: Change `TRADING_BACKEND`
3. Restart: `python main.py`

---

## 🎓 Learning Path

### Beginner (Week 1-2)

**Goal:** Understand the bot

```env
TRADING_BACKEND=paper
TRADING_MODE=manual
INTERVAL=15m
ASSETS=BTC,ETH
PAPER_TRADING_STARTING_BALANCE=10000
```

**Actions:**
- Observe 50+ AI decisions
- Read all reasoning
- Reject all trades
- Understand market data

### Intermediate (Week 3-4)

**Goal:** Selective execution

```env
TRADING_BACKEND=paper
TRADING_MODE=manual
INTERVAL=5m
ASSETS=BTC,ETH,SOL
```

**Actions:**
- Execute 10-20 trades
- Track win rate
- Refine approval criteria
- Experiment with intervals

### Advanced (Week 5-8)

**Goal:** Auto mode testing

```env
TRADING_BACKEND=paper
TRADING_MODE=auto
INTERVAL=1h
ASSETS=BTC,ETH,SOL,AVAX
```

**Actions:**
- Run continuously for 2+ weeks
- Analyze statistics
- Optimize configuration
- Prepare for testnet

---

## 🚀 Next Steps

### After successful paper trading:

1. **Read:** `HYPERLIQUID_TESTNET_GUIDE.md`
2. **Setup:** Hyperliquid testnet account
3. **Switch:** `TRADING_BACKEND=hyperliquid`
4. **Test:** On testnet with fake money
5. **Graduate:** To mainnet with small capital

### Resources:

- **QUICK_START.md** - Full setup guide
- **TESTING_QUICK_START.md** - Test procedures
- **GEMINI_SETUP.md** - AI configuration
- **tests/test_05_paper_trading.py** - Paper trading tests

---

## 📞 Support

### Issues:

1. Check `bot.log` for errors
2. Review `data/diary.jsonl` for trade history
3. Run tests: `python tests/test_05_paper_trading.py`
4. Read FAQ above

### Community:

- Hyperliquid Discord: https://discord.gg/hyperliquid
- Google AI Discord (Gemini support)

---

**Happy Paper Trading! 📄💰**

*Remember: Paper profits are not real profits. Use paper trading to learn, test, and build confidence before risking real capital.*
