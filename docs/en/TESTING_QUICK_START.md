# 🚀 Testing Quick Start

Fast guide to verify that the Gemini integration is working.

---

## ⚡ TL;DR - Get started in 5 minutes

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
copy .env.example .env

# 3. Edit .env with your API keys
notepad .env

# 4. Run all tests
python tests/test_all.py
```

If everything is green ✅ → You are ready to trade!

---

## 📋 Before you start

### You need:

- [ ] **Gemini API Key**
  - Get free key: https://makersuite.google.com/app/apikey
  - Copy the API key (starts with `AIzaSy...`)

- [ ] **Hyperliquid Testnet Wallet**
  - Generate new Ethereum private key
  - Get testnet tokens from Discord
  - Discord: https://discord.gg/hyperliquid

- [ ] **TAAPI Key** (optional)
  - Free tier: https://taapi.io
  - Required for tool calling test

---

## 🔧 Step-by-Step Setup

### Step 1: Generate Ethereum Wallet (for Hyperliquid testnet)

**Method A: Python script**
```python
from eth_account import Account

# Generate new wallet
account = Account.create()

print("=" * 60)
print("HYPERLIQUID TESTNET WALLET")
print("=" * 60)
print(f"Address: {account.address}")
print(f"Private Key: {account.key.hex()}")
print("\n⚠️  STORE PRIVATE KEY SAFELY!")
print("=" * 60)
```

**Method B: Use existing wallet**
- Use MetaMask or other Ethereum wallet
- **IMPORTANT:** Use ONLY testnet wallet, never main wallet!

### Step 2: Get Testnet Tokens

1. Join Hyperliquid Discord: https://discord.gg/hyperliquid
2. Go to `#testnet-faucet` channel
3. Send command:
   ```
   !faucet YOUR_WALLET_ADDRESS
   ```
4. Wait ~30 seconds
5. You receive 10,000 USDC testnet tokens

### Step 3: Configure .env

**Copy template:**
```bash
copy .env.example .env
```

**Minimal configuration (.env):**
```env
# LLM Provider
LLM_PROVIDER=gemini

# Gemini
GEMINI_API_KEY=AIzaSy_YOUR_KEY_HERE
GEMINI_MODEL=gemini-2.0-flash-exp

# Hyperliquid Testnet
HYPERLIQUID_NETWORK=testnet
HYPERLIQUID_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE

# Trading
ASSETS=BTC,ETH
INTERVAL=5m
TRADING_MODE=manual
```

**Replace:**
- `AIzaSy_YOUR_KEY_HERE` → Your Gemini API key
- `0xYOUR_PRIVATE_KEY_HERE` → Your testnet private key

### Step 4: Run Tests

**All tests (recommended):**
```bash
python tests/test_all.py
```

**Or individually:**
```bash
python tests/test_01_environment.py      # ~5 sec
python tests/test_02_gemini_api.py       # ~15 sec
python tests/test_03_hyperliquid_api.py  # ~10 sec
python tests/test_04_gemini_trading_agent.py  # ~30 sec
```

---

## ✅ Expected Output

### If everything works:

```
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
nof1.ai Gemini Integration - Complete Test Suite
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀

====================================================================
Running: Environment Configuration
====================================================================

TEST 1: Environment Configuration
====================================================================

✓ LLM Provider: gemini

--- Gemini Configuration ---
✓ API Key: AIzaSy...abc4 (hidden)
✓ Model: gemini-2.0-flash-exp

--- Hyperliquid Configuration ---
✓ Network: testnet
✓ Using TESTNET (safe for learning)
✓ Private Key: 0xabc1...def9 (hidden)

--- Trading Configuration ---
✓ Assets: BTC,ETH
✓ Interval: 5m
✓ Trading Mode: manual
✓ MANUAL mode activated - trades require approval

====================================================================
TEST SUMMARY
====================================================================
✅ PASS: Environment loaded
✅ PASS: Gemini configuration
✅ PASS: Hyperliquid configuration
✅ PASS: Trading configuration

Total: 4/4 tests passed

🎉 All tests passed! Configuration looks good.

[... more tests ...]

====================================================================
COMPLETE TEST SUITE SUMMARY
====================================================================
✅ PASS: Environment Configuration
✅ PASS: Gemini API Connection
✅ PASS: Hyperliquid API Connection
✅ PASS: Gemini Trading Agent

Total: 4/4 test suites passed

🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
ALL TESTS PASSED!
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉

Your nof1.ai setup with Gemini is fully configured!

✅ Next steps:
   1. Review GEMINI_SETUP.md for usage instructions
   2. Start the bot: python main.py
   3. Test in MANUAL mode first
   4. Monitor trades in the GUI
```

---

## ❌ Common Errors & Solutions

### ❌ "GEMINI_API_KEY not found"

**Problem:** .env file missing or not loaded

**Solution:**
```bash
# Check that .env exists
dir .env

# Open and verify content
notepad .env

# Restart terminal after .env changes
```

### ❌ "Invalid API key"

**Problem:** Wrong API key or expired

**Solution:**
1. Go to https://makersuite.google.com/app/apikey
2. Create new API key
3. Update GEMINI_API_KEY in .env
4. Run test again

### ❌ "Hyperliquid balance is 0"

**Problem:** No testnet tokens

**Solution:**
```bash
# 1. Join Discord
https://discord.gg/hyperliquid

# 2. In #testnet-faucet channel:
!faucet YOUR_ADDRESS

# 3. Verify that you received tokens:
python tests/test_03_hyperliquid_api.py
```

### ❌ "ModuleNotFoundError: No module named 'google.generativeai'"

**Problem:** Gemini SDK not installed

**Solution:**
```bash
pip install google-generativeai>=0.8.0
```

### ❌ "Rate limit exceeded"

**Problem:** Too many API calls

**Solution:**
- Wait 60 seconds
- Gemini free tier: 60 requests/minute
- Run tests slower (one by one)

---

## 🎯 Test Breakdown

### Test 1: Environment (5 seconds)
**What it does:**
- Checks that .env file is correctly configured
- Verifies API keys are set
- Validates trading configuration

**Fail conditions:**
- .env missing
- API keys are placeholders
- Trading mode is not set

### Test 2: Gemini API (15 seconds)
**What it does:**
- Tests Gemini API connection
- Verifies JSON structured output
- Tests function calling

**Fail conditions:**
- GEMINI_API_KEY is invalid
- Internet connection fails
- API quota exhausted

### Test 3: Hyperliquid API (10 seconds)
**What it does:**
- Tests exchange API connection
- Fetches account balance
- Fetches market prices

**Fail conditions:**
- Private key is wrong
- Testnet is down
- No testnet funds

### Test 4: Trading Agent (30 seconds)
**What it does:**
- Tests full trading decision flow
- Verifies AI reasoning
- Tests tool calling (if TAAPI)

**Fail conditions:**
- Tests 1-3 fail
- Gemini returns invalid JSON
- System prompt is too restrictive

---

## 🔄 What happens after tests?

### ✅ If all tests pass:

**You are ready to start bot:**
```bash
python main.py
```

**GUI opens at:** http://localhost:3000

**First time running:**
1. Bot starts in background
2. Waits until first 5-minute interval
3. Fetches market data
4. Sends to Gemini for analysis
5. Shows trade proposals in GUI
6. In manual mode: You approve via "Recommendations" page

### ❌ If any tests fail:

**Do not start bot yet!**

1. Read error message carefully
2. Fix problem (see "Common Errors" above)
3. Run test again
4. When all are green → Start bot

---

## 📚 Further Reading

- **GEMINI_SETUP.md** - Detailed Gemini guide
- **tests/README.md** - Full test documentation
- **REVIEW_AND_ANALYSIS.md** - Project analysis
- **.env.example** - All configuration options

---

## 💡 Pro Tips

### Save time:

```bash
# Run only relevant tests
python tests/test_02_gemini_api.py  # Only Gemini

# Debugging: Enable verbose output
python -v tests/test_all.py
```

### Logging:

```bash
# See Gemini API requests
type llm_requests.log

# See bot activity
type bot.log

# Live monitoring (PowerShell)
Get-Content llm_requests.log -Wait

# OR (Recommended):
# Use "Logs" page in Web GUI under "SYSTEM" menu!
```

### Performance:

- Gemini 2.0 Flash: Free, fast (~1s response)
- Gemini 1.5 Pro: Paid, better quality (~2s response)
- Start with Flash, upgrade if necessary

---

## 🆘 Need help?

### Resources:

1. **Documentation**
   - Read GEMINI_SETUP.md
   - Check tests/README.md

2. **Log files**
   - llm_requests.log (Gemini errors)
   - bot.log (General errors)

3. **Community**
   - Hyperliquid Discord (testnet support)
   - Google AI Discord (Gemini support)

### Debugging checklist:

- [ ] .env file exists and is correctly formatted
- [ ] API keys are valid (not placeholders)
- [ ] Python 3.10+ installed
- [ ] Dependencies installed (requirements.txt)
- [ ] Internet connection working
- [ ] Testnet wallet has funds (if testnet)

---

**Good luck! 🚀**

*Start with test_all.py and follow instructions. You are ready in 5 minutes!*
