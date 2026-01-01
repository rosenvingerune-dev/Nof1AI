# 🧪 Test Suite - nof1.ai Gemini Integration

Denne mappen inneholder comprehensive test-scripts for å verifisere at hele setupet fungerer korrekt.

---

## 📋 Test Oversikt

| Test | Fil | Beskrivelse | Kjøretid |
|------|-----|-------------|----------|
| **Test 1** | `test_01_environment.py` | Verifiserer .env konfigurasjon | ~5 sek |
| **Test 2** | `test_02_gemini_api.py` | Tester Gemini API connection | ~15 sek |
| **Test 3** | `test_03_hyperliquid_api.py` | Tester Hyperliquid exchange API | ~10 sek |
| **Test 4** | `test_04_gemini_trading_agent.py` | Tester trading agent med Gemini | ~30 sek |
| **All Tests** | `test_all.py` | Kjører alle tester i sekvens | ~60 sek |

---

## 🚀 Quickstart

### Kjør alle tester (anbefalt):

```bash
cd C:\Users\Rune\PycharmProjects\Nof1\nof1.ai-alpha-arena-nof1.ai-alpha-arena

python tests/test_all.py
```

**Forventet output hvis alt er OK:**
```
🚀🚀🚀... (banner)
Running: Environment Configuration
✅ PASS: All environment checks
...
🎉🎉🎉 ALL TESTS PASSED!
```

### Kjør individuelle tester:

```bash
# Test 1: Environment
python tests/test_01_environment.py

# Test 2: Gemini API
python tests/test_02_gemini_api.py

# Test 3: Hyperliquid API
python tests/test_03_hyperliquid_api.py

# Test 4: Trading Agent
python tests/test_04_gemini_trading_agent.py
```

---

## 📖 Detaljert Guide

### Test 1: Environment Configuration

**Formål:** Sjekker at .env fil er riktig konfigurert

**Sjekker:**
- ✅ LLM_PROVIDER er satt til "gemini" eller "openrouter"
- ✅ GEMINI_API_KEY er satt (hvis provider=gemini)
- ✅ HYPERLIQUID_PRIVATE_KEY eller MNEMONIC er satt
- ✅ HYPERLIQUID_NETWORK er satt (testnet/mainnet)
- ✅ ASSETS og INTERVAL er konfigurert
- ✅ TRADING_MODE er satt (manual/auto)

**Kjør:**
```bash
python tests/test_01_environment.py
```

**Hvis FAIL:**
1. Sjekk at .env finnes i project root
2. Verifiser at alle required keys er satt
3. Ingen placeholder values (`your_api_key_here`)

---

### Test 2: Gemini API Connection

**Formål:** Verifiserer at Gemini API fungerer

**Sjekker:**
- ✅ Gemini SDK er installert
- ✅ API key er gyldig
- ✅ Kan generere enkel tekst
- ✅ JSON structured output fungerer
- ✅ Function calling er tilgjengelig

**Kjør:**
```bash
python tests/test_02_gemini_api.py
```

**Hvis FAIL:**
1. Verifiser GEMINI_API_KEY i .env
2. Sjekk internett-tilkobling
3. Regenerer API key: https://makersuite.google.com/app/apikey
4. Sjekk quota limits

**Eksempel output:**
```
✓ Gemini SDK imported successfully
✓ API Key: AIzaSy...abc4
✓ Model: gemini-2.0-flash-exp
✓ Response received: 'Gemini API is working!'
✓ JSON response received: {"status": "success", ...}
✓ Function call detected!
```

---

### Test 3: Hyperliquid API Connection

**Formål:** Verifiserer exchange API fungerer

**Sjekker:**
- ✅ Hyperliquid SDK er installert
- ✅ Wallet credentials er gyldige
- ✅ Kan hente account balance
- ✅ Kan hente current prices
- ✅ Kan hente funding rates
- ✅ Kan hente open interest
- ✅ Kan hente open orders

**Kjør:**
```bash
python tests/test_03_hyperliquid_api.py
```

**Hvis FAIL:**
1. Verifiser HYPERLIQUID_PRIVATE_KEY eller MNEMONIC
2. Sjekk HYPERLIQUID_NETWORK setting
3. For testnet: få tokens fra Discord faucet
4. Sjekk Hyperliquid status: https://status.hyperliquid.xyz

**Eksempel output:**
```
✓ Network: testnet
✓ Wallet address: 0xabc123...
✓ Balance: $10,000.00 USDC
✓ BTC: $98,450.00
✓ ETH: $3,398.50
✓ BTC: +0.0100% per 8h funding
```

---

### Test 4: Gemini Trading Agent

**Formål:** Verifiserer at trading agent fungerer end-to-end

**Sjekker:**
- ✅ GeminiTradingAgent kan importeres
- ✅ Agent kan initialiseres
- ✅ Kan generere simple trading decisions
- ✅ Kan bruke tool calling (hvis TAAPI er satt)
- ✅ Kan håndtere multi-asset decisions
- ✅ Graceful error handling

**Kjør:**
```bash
python tests/test_04_gemini_trading_agent.py
```

**Hvis FAIL:**
1. Sjekk at Test 1-3 passerer først
2. Review llm_requests.log for Gemini errors
3. Verifiser at model støtter function calling
4. Test med enklere prompt

**Eksempel output:**
```
✓ GeminiTradingAgent initialized
✓ Model: gemini-2.0-flash-exp
✓ Decision received!

--- GEMINI REASONING ---
Analyzing BTC: 4h MACD shows bullish crossover...

--- TRADE DECISIONS ---
BTC:
  Action: BUY
  Allocation: $500.00
  TP: $99,500.00
  SL: $97,500.00
  Rationale: Bullish MACD + low funding...
```

---

## 🔍 Troubleshooting

### Alle tester feiler

**Løsning:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Verify .env exists
ls .env

# Check Python version (should be 3.10+)
python --version
```

### "ModuleNotFoundError: No module named 'google.generativeai'"

**Løsning:**
```bash
pip install google-generativeai>=0.8.0
```

### "GEMINI_API_KEY not found"

**Løsning:**
1. Kopier .env.example til .env
2. Fyll inn GEMINI_API_KEY
3. Restart terminal (for å laste .env)

### "Invalid API key"

**Løsning:**
1. Gå til https://makersuite.google.com/app/apikey
2. Generer ny API key
3. Oppdater .env fil
4. Kjør test på nytt

### "Hyperliquid connection failed"

**Løsning:**
```bash
# Sjekk wallet address
python -c "from eth_account import Account; print(Account.from_key('YOUR_PRIVATE_KEY').address)"

# Verify network
# .env: HYPERLIQUID_NETWORK=testnet
```

### "Rate limit exceeded"

**Løsning:**
- Vent 60 sekunder
- Sjekk Gemini quota: https://makersuite.google.com
- Oppgrader til paid tier hvis nødvendig

---

## 📊 Forventet Test Flow

```
┌─────────────────────────────┐
│  test_all.py                │
└──────────┬──────────────────┘
           │
           ├─► Test 1: Environment
           │   ✅ .env konfigurert
           │   ✅ API keys satt
           │
           ├─► Test 2: Gemini API
           │   ✅ SDK funker
           │   ✅ API key gyldig
           │   ✅ JSON mode OK
           │   ✅ Function calling OK
           │
           ├─► Test 3: Hyperliquid API
           │   ✅ Wallet tilkoblet
           │   ✅ Balance hentet
           │   ✅ Prices tilgjengelig
           │
           └─► Test 4: Trading Agent
               ✅ Agent initialisert
               ✅ Decisions generert
               ✅ Tool calling funker

┌─────────────────────────────┐
│  🎉 ALL TESTS PASSED!       │
│  Ready to trade!            │
└─────────────────────────────┘
```

---

## 💡 Tips

### Før du starter tester:

1. **Installer dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Lag .env fil:**
   ```bash
   cp .env.example .env
   # Rediger .env med dine API keys
   ```

3. **Verifiser Python version:**
   ```bash
   python --version  # Should be 3.10+
   ```

### Under testing:

1. **Kjør tester i rekkefølge:**
   - Test 1 → Test 2 → Test 3 → Test 4

2. **Fikse feil før du går videre:**
   - Hvis Test 2 feiler, Test 4 vil også feile

3. **Les error messages nøye:**
   - Testene gir konkrete fix-instruksjoner

### Etter testing:

1. **Hvis alt er grønt:**
   - Start bot: `python main.py`
   - Test i MANUAL mode først

2. **Hvis noe er rødt:**
   - Fix errors basert på output
   - Kjør individuelle tester på nytt
   - Sjekk log-filer (bot.log, llm_requests.log)

---

## 📝 Logging

Testene logger til følgende filer:

- **llm_requests.log** - Gemini API requests/responses
- **bot.log** - General bot activity (hvis bot kjører)
- **Console output** - Real-time test results

**Bruk logs for debugging:**
```bash
# Windows
type llm_requests.log

# Linux/Mac
cat llm_requests.log

# Live monitoring (PowerShell)
Get-Content llm_requests.log -Wait
```

---

## ✅ Success Criteria

Alle tester skal vise:

```
✅ PASS: Environment configuration
✅ PASS: Gemini configuration
✅ PASS: API authentication
✅ PASS: Simple text generation
✅ PASS: JSON structured output
✅ PASS: Function calling
✅ PASS: API initialization
✅ PASS: Get user state
✅ PASS: Get current prices
✅ PASS: Get funding rates
✅ PASS: Agent import
✅ PASS: Agent initialization
✅ PASS: Simple trading decision
✅ PASS: Multi-asset decision

Total: 14/14 tests passed

🎉 ALL TESTS PASSED!
```

---

## 🆘 Får du ikke testene til å virke?

1. **Les GEMINI_SETUP.md** - Detaljert setup guide
2. **Sjekk nof1AI_review.md** - Prosjektdokumentasjon
3. **Review .env.example** - Alle konfigurasjonsmuligheter
4. **Opprett issue** - Hvis alt annet feiler

---

**Lykke til med testingen! 🚀**
