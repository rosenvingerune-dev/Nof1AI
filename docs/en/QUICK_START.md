# ⚡ Quick Start Guide - nof1.ai with Gemini

3-minute guide to get started with Gemini-driven trading bot.

---

## 🎯 Two options to start

### 🟢 Option A: Paper Trading (RECOMMENDED - 100% free)
**Advantages:**
- ✅ No exchange account needed
- ✅ No wallet setup
- ✅ No testnet tokens
- ✅ Start in 3 minutes
- ✅ 100% risk-free (only Gemini API key)

**What you need:**
- Gemini API key (free)
- Only 3 minutes setup

**[Go to Paper Trading Setup →](#paper-trading-setup)**

---

### 🟡 Option B: Hyperliquid Testnet (Requires wallet)
**Advantages:**
- ✅ Real exchange API
- ✅ Testnet (fake money)
- ✅ Ready for mainnet later

**What you need:**
- Gemini API key (free)
- Hyperliquid wallet with mainnet activity
- 15-30 minutes setup

**[Go to Hyperliquid Testnet Setup →](#hyperliquid-testnet-setup)**

---

## 🎯 What you get (both options)

- ✅ AI-driven trading bot (Gemini 2.0 Flash)
- ✅ Real-time market data
- ✅ Desktop GUI for monitoring
- ✅ Manual approval mode (you approve trades)
- ✅ Full position tracking and PnL

---

# Paper Trading Setup

## 📋 You need (2 minutes)

### 1. Gemini API Key (Free)
- Go to: https://makersuite.google.com/app/apikey
- Click "Create API Key"
- Copy the key (starts with `AIzaSy...`)

---

## 🚀 Setup (3 steps)

### Step 1: Install dependencies

```bash
cd C:\Users\Rune\PycharmProjects\Nof1\nof1.ai-alpha-arena-nof1.ai-alpha-arena
pip install -r requirements.txt
```

### Step 2: Create .env file

```bash
# Copy template
copy .env.example .env

# Open in editor
notepad .env
```

**Fill in (minimal config for PAPER TRADING):**
```env
# Trading Backend (IMPORTANT!)
TRADING_BACKEND=paper

# Paper Trading (no exchange needed!)
PAPER_TRADING_STARTING_BALANCE=10000.0

# LLM Provider
LLM_PROVIDER=gemini

# Gemini API
GEMINI_API_KEY=AIzaSy...  # <-- Your Gemini key here
GEMINI_MODEL=gemini-2.0-flash-exp

# Trading
ASSETS=BTC,ETH
INTERVAL=5m
TRADING_MODE=manual
```

### Step 3: Test setup

```bash
# Test paper trading
python tests/test_05_paper_trading.py
```

**Expected:**
```
✅ ALL PAPER TRADING TESTS PASSED!
   • Paper trading API initialized
   • Real-time prices from Binance
   • Order simulation working
```

---

## ▶️ Start Bot

```bash
python main.py
```

**GUI opens at:** http://localhost:3000

**You can now see:**
- Dashboard with $10,000 simulated balance
- Real-time BTC/ETH prices from Binance
- AI-generated trading signals from Gemini

**📚 Read more:** `PAPER_TRADING_GUIDE.md` for full guide

---

# Hyperliquid Testnet Setup

**⚠️ MUST have wallet with mainnet activity** - see `HYPERLIQUID_TESTNET_WORKAROUND.md`

## 📋 You need

### 1. Gemini API Key (Free)
- Go to: https://makersuite.google.com/app/apikey
- Click "Create API Key"
- Copy the key (starts with `AIzaSy...`)

### 2. Hyperliquid Wallet
**NOTE:** You need a wallet that has been active on Hyperliquid mainnet!

**Option 1: Use existing MetaMask wallet**
- If you have used Hyperliquid before
- Get private key from MetaMask
- See `HYPERLIQUID_TESTNET_WORKAROUND.md`

**Option 2: Generate new wallet and activate it**
```bash
python scripts/setup_hyperliquid_testnet.py
```
- Costs $5-10 to activate on mainnet
- See `HYPERLIQUID_TESTNET_WORKAROUND.md`

**Option 3: Use paper trading instead**
- 100% free
- No wallet needed
- See [Paper Trading Setup](#paper-trading-setup)

---

## 🚀 Setup (4 steps)

### Step 1: Install dependencies

```bash
cd C:\Users\Rune\PycharmProjects\Nof1\nof1.ai-alpha-arena-nof1.ai-alpha-arena
pip install -r requirements.txt
```

### Step 2: Check wallet activation

```bash
python scripts/check_wallet_activation.py
```

If **NOT activated**, see `HYPERLIQUID_TESTNET_WORKAROUND.md` for solutions.

### Step 3: Create .env file

```bash
# Copy template
copy .env.example .env

# Open in editor
notepad .env
```

**Fill in (minimal config for HYPERLIQUID TESTNET):**
```env
# Trading Backend
TRADING_BACKEND=hyperliquid

# Hyperliquid Testnet
HYPERLIQUID_NETWORK=testnet
HYPERLIQUID_PRIVATE_KEY=0x...  # <-- Your private key

# LLM Provider
LLM_PROVIDER=gemini

# Gemini API
GEMINI_API_KEY=AIzaSy...  # <-- Your Gemini key here
GEMINI_MODEL=gemini-2.0-flash-exp

# Trading
ASSETS=BTC,ETH
INTERVAL=5m
TRADING_MODE=manual
```

### Step 4: Test setup

```bash
python tests/test_all.py
```

**Expected:**
```
🎉 ALL TESTS PASSED!
```

---

## ▶️ Start Bot

```bash
python main.py
```

**GUI opens at:** http://localhost:3000

---

## 📱 Use GUI

### Dashboard
- Account balance
- Total PnL
- Active positions
- Recent trades

### Reasoning
- Gemini's full analysis
- Market structure breakdown
- Decision rationale

### Recommendations
- Trade proposals (manual mode)
- Approve/reject each trade
- Risk/reward metrics

### Positions
- Active trades
- Entry/current price
- PnL per position
- TP/SL levels

---

## 🎓 First Trading Session

### 1. Start bot (manual mode)
```bash
python main.py
```

### 2. Wait for first analysis
- Bot runs every 5th minute (INTERVAL=5m)
- Fetches market data
- Sends to Gemini for analysis

### 3. See Gemini's reasoning
- Go to "Reasoning" page in GUI
- Read full market analysis
- Understand why AI suggests trade

### 4. Review trade proposal
- Go to "Recommendations" page
- See proposed trade (BUY/SELL/HOLD)
- Check TP/SL prices
- Read rationale

### 5. Approve or reject
- Click "Approve" if you agree
- Click "Reject" if not
- Trade executes only if approved

### 6. Monitor position
- Go to "Positions" page
- See PnL in real-time
- TP/SL triggers automatically

---

## 💡 Tips for First Week

### Testing strategy:

**Day 1-3: Observe**
- Let the bot run without approving trades
- Study Gemini's reasoning
- Understand how AI thinks

**Day 4-7: Selective trading**
- Approve only trades you 100% agree with
- Start with small positions ($100-500)
- Document results

**Week 2: More active**
- Increase position size to $500-1000
- Test more assets (SOL, AVAX, etc.)
- Experiment with leverage (3x max)

---

## ⚙️ Adjust Settings

### Change assets:

**.env:**
```env
ASSETS=BTC,ETH,SOL
```

### Change interval:

```env
INTERVAL=15m  # Less frequent trades
# or
INTERVAL=1h   # Only 24 decisions/day
```

### Change to auto mode (when comfortable):

```env
TRADING_MODE=auto
```
⚠️ **WARNING:** Auto mode executes trades without approval!

---

## 🔍 Troubleshooting

### "GEMINI_API_KEY not found"
```bash
# Check that .env exists
dir .env

# Verify content
type .env

# Restart terminal
```

### "No testnet funds"
```bash
# Check balance
python scripts/check_testnet_balance.py

# If $0, go to Discord:
# 1. https://discord.gg/hyperliquid
# 2. #testnet-faucet channel
# 3. !faucet YOUR_ADDRESS
```

### "Tests failing"
```bash
# Run individually to isolate problem
python tests/test_01_environment.py
python tests/test_02_gemini_api.py
python tests/test_03_hyperliquid_api.py
python tests/test_04_gemini_trading_agent.py
```

---

## 📚 Documentation

### Get started:
1. **QUICK_START.md** (this document) ← Start here
2. **TESTING_QUICK_START.md** - Test guide
3. **HYPERLIQUID_TESTNET_GUIDE.md** - Testnet details

### Deeper learning:
4. **GEMINI_SETUP.md** - Full Gemini guide
5. **REVIEW_AND_ANALYSIS.md** - Project analysis
6. **IMPLEMENTATION_SUMMARY.md** - Technical overview

---

## ⚠️ Important Warnings

### Before you start:

- [ ] ✅ You are using TESTNET (not mainnet)
- [ ] ✅ TRADING_MODE=manual (not auto)
- [ ] ✅ You have read the README files
- [ ] ✅ You understand this is for learning/experimentation
- [ ] ✅ You know how to stop the bot (Ctrl+C)

### Never do this:

- ❌ Use testnet wallet on mainnet
- ❌ Commit .env to git
- ❌ Share private keys
- ❌ Start with auto mode
- ❌ Use real money before thorough testing

---

## 🎯 Success Metrics

### After first week, you should have:

- ✅ Run 50+ trading cycles
- ✅ Understood Gemini's reasoning pattern
- ✅ Approved and observed 5-10 trades
- ✅ Documented win rate
- ✅ Identified areas for improvement

### When ready for mainnet (in 2-4 weeks):

- ✅ Consistent profit on testnet (>55% win rate)
- ✅ Understand all bot functions
- ✅ Have tested error scenarios
- ✅ Comfortable with risk management
- ✅ Start with minimal capital ($100-500)

---

## 🆘 Help

### Resources:

1. **Documentation in project** (all .md files)
2. **Log files:**
   - `bot.log` - Bot activity
   - `llm_requests.log` - Gemini API calls
   - `data/diary.jsonl` - Trade history

3. **Community:**
   - Hyperliquid Discord: https://discord.gg/hyperliquid
   - Google AI Discord (Gemini support)

---

## 🎉 You are ready!

```bash
# Run these commands in order:

# 1. Setup testnet wallet
python scripts/setup_hyperliquid_testnet.py

# 2. Get tokens from Discord (follow instructions)

# 3. Check balance
python scripts/check_testnet_balance.py

# 4. Run tests
python tests/test_all.py

# 5. Start bot
python main.py

# 6. Open browser: http://localhost:3000

# 7. Observe, learn, and have fun! 🚀
```

---

**Good luck with AI trading! 🤖💰**

*Remember: Testnet is for learning. Take your time, experiment, and get comfortable before considering mainnet.*
